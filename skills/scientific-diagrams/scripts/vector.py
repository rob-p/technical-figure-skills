"""Small publication-diagram vocabulary. Coordinates are final-size points, y down.

SVG is exported first. No timestamps, randomness, user fonts, or external assets.
Geometry is explicit; this is not an automatic layout or scientific inference engine.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "scientific-diagrams-mpl"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle
from matplotlib.path import Path as MplPath

INK = "#243746"
MUTED = "#526777"
LINE = "#728695"
BLUE = "#e7f1f6"
PURPLE = "#eeeaf7"
GOLD = "#fcf0d8"
TEAL = "#287b89"
SURFACE = "#f4f7f9"
RED = "#a44635"


@dataclass(frozen=True)
class Node:
    name: str
    x: float
    y: float
    w: float
    h: float


@dataclass(frozen=True)
class Port:
    node: Node
    side: str
    fraction: float = .5

    def __post_init__(self):
        if self.side not in ("n", "e", "s", "w") or not 0 <= self.fraction <= 1:
            raise ValueError("Port needs side n/e/s/w and fraction in [0,1]")

    @property
    def xy(self):
        n, f = self.node, self.fraction
        return {"n": (n.x + f*n.w, n.y), "s": (n.x + f*n.w, n.y+n.h),
                "w": (n.x, n.y+f*n.h), "e": (n.x+n.w, n.y+f*n.h)}[self.side]

    @property
    def normal(self):
        return {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}[self.side]


def bloom_pass(bits, positions):
    """Logical bit test; repeated positions are allowed, not a hash implementation."""
    if not positions or not bits or any(b not in (0, 1) for b in bits):
        raise ValueError("Expected nonempty binary block and queried positions")
    if any(not isinstance(i, int) or i < 0 or i >= len(bits) for i in positions):
        raise ValueError("Bit position outside displayed block")
    return all(bits[i] for i in positions)


def exact_probe_counts(records):
    """Toy exact-identity UMI collapse; not a model of cr-like error correction."""
    groups = {}
    for sample, cell, probe, umi in records:
        groups.setdefault((sample, cell, probe), set()).add(umi)
    return {key: len(umis) for key, umis in sorted(groups.items())}


def sum_to_genes(counts, probe_genes):
    result = {}
    for (sample, cell, probe), count in counts.items():
        key = (sample, cell, probe_genes[probe])
        result[key] = result.get(key, 0) + count
    return dict(sorted(result.items()))


def pack_location(segment, canonical, position):
    """Worked example layout: 31-bit segment, 1-bit flag, 32-bit position."""
    if not 0 <= segment < 2**31 or canonical not in (0, 1) or not 0 <= position < 2**32:
        raise ValueError("Value outside 31/1/32-bit layout")
    return (segment << 33) | (canonical << 32) | position


class Diagram:
    def __init__(self, width=504, height=330, title="Scientific schematic", description=""):
        if width <= 0 or height <= 0:
            raise ValueError("Canvas dimensions must be positive points")
        matplotlib.rcParams.update({"svg.fonttype": "none", "svg.hashsalt": "scientific-diagrams-v1",
                                    "pdf.fonttype": 42, "font.size": 8.5,
                                    "savefig.facecolor": "white"})
        self.width, self.height = width, height
        self.title, self.description = title, description
        self.fig = plt.figure(figsize=(width/72, height/72), dpi=144)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set(xlim=(0, width), ylim=(height, 0))
        self.ax.axis("off")
        self.nodes, self.labels, self.connections = {}, [], []
        self.fontdir = Path(matplotlib.get_data_path()) / "fonts" / "ttf"

    def text(self, x, y, value, size=8.5, bold=False, color=INK, align="left", mono=False):
        font = ("DejaVuSansMono" if mono else "DejaVuSans") + ("-Bold" if bold else "") + ".ttf"
        # File selects Agg/PDF face; explicit weight also survives SVG CSS export.
        props = FontProperties(fname=str(self.fontdir/font), size=size,
                               weight="bold" if bold else "normal")
        label = self.ax.text(x, y, str(value), ha=align, va="center", color=color,
                             fontproperties=props, linespacing=1.35, zorder=5, clip_on=False)
        label.set_gid(f"label-{len(self.labels)+1}")
        self.labels.append(label)
        return label

    def box(self, name, x, y, w, h, fill=SURFACE, edge="none", radius=6, lw=.6, zorder=2):
        if name in self.nodes or w <= 0 or h <= 0:
            raise ValueError(f"Duplicate node or nonpositive shape: {name}")
        if radius < 0 or radius > min(w, h)/2:
            raise ValueError("Corner radius outside shape")
        node = Node(name, x, y, w, h)
        patch = FancyBboxPatch((x, y), w, h,
                               boxstyle=f"round,pad=0,rounding_size={radius}",
                               facecolor=fill, edgecolor=edge, linewidth=lw, zorder=zorder)
        patch.set_gid(name)
        self.ax.add_patch(patch)
        self.nodes[name] = node
        return node

    def port(self, name, side, fraction=.5):
        return Port(self.nodes[name], side, fraction)

    def rule(self, x1, y1, x2, y2, color=LINE, lw=.65, zorder=3):
        self.ax.plot([x1, x2], [y1, y2], color=color, lw=lw, solid_capstyle="round", zorder=zorder)

    def connect(self, source, target, color=LINE, bend=None, head=True, dashed=False, via=None):
        """Ports or point pairs. `via` is a deliberate two-curve waypoint."""
        a = source.xy if isinstance(source, Port) else tuple(source)
        b = target.xy if isinstance(target, Port) else tuple(target)
        distance = math.dist(a, b)
        if distance == 0:
            raise ValueError("Zero-length connector")
        unit = ((b[0]-a[0])/distance, (b[1]-a[1])/distance)
        na = source.normal if isinstance(source, Port) else unit
        nb = target.normal if isinstance(target, Port) else (-unit[0], -unit[1])
        arm = min(60, distance*.38) if bend is None else bend
        c1 = (a[0]+na[0]*arm, a[1]+na[1]*arm)
        c2 = (b[0]+nb[0]*arm, b[1]+nb[1]*arm)
        if via is None:
            vertices = [a, c1, c2, b]
        else:
            # Shared tangent through waypoint gives positional/tangent continuity.
            m = tuple(via)
            tangent = unit
            v1 = (m[0]-tangent[0]*arm*.35, m[1]-tangent[1]*arm*.35)
            v2 = (m[0]+tangent[0]*arm*.35, m[1]+tangent[1]*arm*.35)
            vertices = [a, c1, v1, m, v2, c2, b]
        path = MplPath(vertices, [MplPath.MOVETO] + [MplPath.CURVE4]*(len(vertices)-1))
        patch = FancyArrowPatch(path=path, arrowstyle="-|>" if head else "-",
                                mutation_scale=7, linewidth=.8, color=color,
                                linestyle=(0, (3, 2)) if dashed else "-", zorder=3.5,
                                capstyle="round", joinstyle="round", clip_on=False)
        patch.set_gid(f"connector-{len(self.connections)+1}")
        self.ax.add_patch(patch)
        self.connections.append({"start": a, "end": b, "vertices": vertices,
                                 "source": source.node.name if isinstance(source, Port) else None,
                                 "target": target.node.name if isinstance(target, Port) else None,
                                 "head": head})

    def route(self, source, target, waypoints, radius=7, color=LINE):
        """One continuous path through explicit orthogonal waypoints, rounded turns.

        Use for obstacle avoidance that a direct Bézier cannot provide. Waypoints
        are authored deliberately; the helper does not discover obstacles.
        """
        a = source.xy if isinstance(source, Port) else tuple(source)
        b = target.xy if isinstance(target, Port) else tuple(target)
        points = [a, *map(tuple, waypoints), b]
        if radius <= 0 or any(math.dist(p,q) == 0 for p,q in zip(points,points[1:])):
            raise ValueError("Route needs positive radius and distinct adjacent points")
        for p,q in zip(points,points[1:]):
            if p[0] != q[0] and p[1] != q[1]:
                raise ValueError("Rounded route segments must be axis aligned")
        vertices, codes = [a], [MplPath.MOVETO]
        for prev,p,nxt in zip(points,points[1:],points[2:]):
            before, after = math.dist(prev,p), math.dist(p,nxt)
            r = min(radius,before/2,after/2)
            entry = (p[0]+(prev[0]-p[0])*r/before,p[1]+(prev[1]-p[1])*r/before)
            leave = (p[0]+(nxt[0]-p[0])*r/after,p[1]+(nxt[1]-p[1])*r/after)
            vertices.extend([entry,p,leave])
            codes.extend([MplPath.LINETO,MplPath.CURVE3,MplPath.CURVE3])
        vertices.append(b); codes.append(MplPath.LINETO)
        patch = FancyArrowPatch(path=MplPath(vertices,codes), arrowstyle="-|>",
                                mutation_scale=7,linewidth=.8,color=color,zorder=3.5,
                                capstyle="round",joinstyle="round",clip_on=False)
        patch.set_gid(f"connector-{len(self.connections)+1}")
        self.ax.add_patch(patch)
        self.connections.append({"start":a,"end":b,"vertices":vertices,
                                 "source":source.node.name if isinstance(source,Port) else None,
                                 "target":target.node.name if isinstance(target,Port) else None,"head":True})

    def fork(self, source, targets, junction, color=LINE):
        self.connect(source, junction, color=color, head=False)
        for target in targets:
            self.connect(junction, target, color=color)
        self.ax.add_patch(Circle(junction, 1.4, facecolor=color, edgecolor="none", zorder=3))

    def panel(self, letter, title, y, x=14):
        self.box(f"panel-{letter}", x, y-8, 16, 16, TEAL, radius=5)
        self.text(x+8, y, letter, size=9, bold=True, color="white", align="center")
        self.text(x+24, y, title, size=10.5, bold=True)

    def pill(self, name, x, y, label, fill=BLUE, width=32, size=8):
        node = self.box(name, x, y, width, 19, fill, radius=5)
        self.text(x+width/2, y+9.5, label, size=size, align="center", mono=True)
        return node

    def sequence(self, name, x, y, bases, marked=(), cell=13, fill=BLUE):
        if not bases or set(bases.upper()) - set("ACGTN"):
            raise ValueError("Expected DNA sequence")
        node = self.box(name, x, y, cell*len(bases), 20, "#fafbfd", radius=4)
        for i, base in enumerate(bases):
            if i in marked:
                self.box(f"{name}-base-{i}", x+i*cell+.5, y+1, cell-1, 18, fill, radius=2)
            self.text(x+(i+.5)*cell, y+10, base, size=8, align="center", mono=True)
        return node

    def table(self, name, x, y, headers, rows, widths, fills=None, row_h=21, size=8):
        if not widths or len(headers) != len(widths) or any(len(r) != len(widths) for r in rows):
            raise ValueError("Table dimensions disagree")
        fills = fills or [BLUE]*len(widths)
        if len(fills) != len(widths) or any(w <= 0 for w in widths):
            raise ValueError("Invalid column widths/fills")
        node = self.box(name, x, y, sum(widths), row_h*(len(rows)+1), "white", radius=0)
        offset = x
        for j, (header, width) in enumerate(zip(headers, widths)):
            self.box(f"{name}-header-{j}", offset, y, width-1, row_h-1, fills[j], radius=3)
            self.text(offset+width/2, y+row_h/2, header, size=size, bold=True, align="center")
            offset += width
        for i, row in enumerate(rows):
            offset = x
            for value, width in zip(row, widths):
                self.text(offset+width/2, y+row_h*(i+1.5), value, size=size, align="center", mono=True)
                offset += width
            self.rule(x+3, y+row_h*(i+2)-.5, x+sum(widths)-3, y+row_h*(i+2)-.5, "#dce5eb", .4)
        return node

    def matrix(self, name, x, y, rows, columns, values, cell=29):
        if len(values) != len(rows) or any(len(v) != len(columns) for v in values):
            raise ValueError("Matrix dimensions disagree")
        node = self.box(name, x, y, (len(columns)+1)*cell, (len(rows)+1)*20, "white", radius=0)
        for j, col in enumerate(columns):
            self.text(x+(j+1.5)*cell, y+10, col, size=7.5, align="center")
        for i, (label, row) in enumerate(zip(rows, values)):
            self.text(x+cell*.45, y+(i+1.5)*20, label, size=8, align="center")
            for j, value in enumerate(row):
                self.box(f"{name}-{i}-{j}", x+(j+1)*cell, y+(i+1)*20, cell-2, 18,
                         BLUE if value else SURFACE, radius=3)
                self.text(x+(j+1.5)*cell-1, y+(i+1.5)*20-1, value, size=8, align="center")
        return node

    def umi(self, name, x, y, values):
        for i, value in enumerate(values):
            self.pill(f"{name}-{i}", x+i*25, y, value, GOLD, width=22, size=7.5)

    def bitstrip(self, name, x, y, bits, positions, cell=15):
        passed = bloom_pass(bits, positions)
        self.box(name, x, y, len(bits)*cell, 20, SURFACE, radius=3)
        for i, bit in enumerate(bits):
            selected = i in positions
            if selected:
                self.box(f"{name}-bit-{i}", x+i*cell, y, cell-1, 20,
                         BLUE if bit else GOLD, radius=2)
            self.text(x+(i+.5)*cell, y+10, bit, 8, bold=selected, align="center", mono=True,
                      color=RED if selected and not bit else INK)
            if selected:
                self.connect((x+(i+.5)*cell, y-8), (x+(i+.5)*cell, y), color=TEAL if bit else RED)
        return passed

    def track(self, name, x, y, width, interval, label, fill=BLUE):
        lo, hi = interval
        if not 0 <= lo < hi <= width:
            raise ValueError("Track interval outside backbone")
        self.rule(x, y+9, x+width, y+9, lw=1)
        node = self.box(name, x+lo, y, hi-lo, 18, fill, radius=4, zorder=4)
        self.text(x+(lo+hi)/2, y+9, label, size=7.8, align="center")
        return node

    def exon_track(self, name, x, y, exons, label):
        """Schematic transcript backbone; exons are local (start,end) coordinates."""
        if not exons or any(a < 0 or a >= b for a, b in exons):
            raise ValueError("Invalid exon intervals")
        if any(exons[i][1] > exons[i+1][0] for i in range(len(exons)-1)):
            raise ValueError("Exons must be ordered and non-overlapping")
        self.text(x-5, y+7, label, size=8, align="right")
        self.rule(x+exons[0][0], y+7, x+exons[-1][1], y+7)
        for i, (a, b) in enumerate(exons):
            self.box(f"{name}-{i}", x+a, y, b-a, 14, PURPLE, radius=2)

    def review(self, min_font=7):
        self.fig.canvas.draw()
        renderer = self.fig.canvas.get_renderer()
        inverse = self.ax.transData.inverted()
        labels, violations, overlaps = [], [], []
        for t in self.labels:
            bb = t.get_window_extent(renderer).transformed(inverse)
            x0, x1 = sorted((bb.x0, bb.x1)); y0, y1 = sorted((bb.y0, bb.y1))
            record = {"text": t.get_text(), "pt": t.get_fontsize(), "bbox": [x0,y0,x1,y1]}
            labels.append(record)
            if x0 < 1 or y0 < 1 or x1 > self.width-1 or y1 > self.height-1:
                violations.append(f"Text outside canvas margin: {t.get_text()}")
            if t.get_fontsize() < min_font:
                violations.append(f"Text below {min_font} pt: {t.get_text()}")
        for i, a in enumerate(labels):
            for b in labels[i+1:]:
                x0,y0,x1,y1 = a["bbox"]; u0,v0,u1,v1 = b["bbox"]
                if min(x1,u1)-max(x0,u0) > .5 and min(y1,v1)-max(y0,v0) > .5:
                    overlaps.append([a["text"], b["text"]])
        for n in self.nodes.values():
            if n.x < 0 or n.y < 0 or n.x+n.w > self.width or n.y+n.h > self.height:
                violations.append(f"Shape outside canvas: {n.name}")
        for c in self.connections:
            if any(not (0 <= x <= self.width and 0 <= y <= self.height) for x,y in c["vertices"]):
                violations.append("Connector control geometry outside canvas")
        return {"canvas_pt": [self.width,self.height], "min_font_pt": min(t["pt"] for t in labels),
                "violations": violations, "text_overlaps": overlaps, "labels": labels,
                "connections": self.connections,
                "limits": "No obstacle routing, text-shape collision, scientific, or aesthetic certification."}

    def save(self, out, stem, dpi=300):
        out = Path(out); out.mkdir(parents=True, exist_ok=True)
        report = self.review()
        if report["violations"] or report["text_overlaps"]:
            (out/f"{stem}.qa.json").write_text(json.dumps(report, indent=2)+"\n")
            raise ValueError(f"Fix layout before export: {report['violations']}; overlaps: {report['text_overlaps']}")
        svg = out/f"{stem}.svg"
        self.fig.savefig(svg, metadata={"Date": None, "Creator": "scientific-diagrams", "Title": self.title})
        # Insert accessible text without rewriting Matplotlib namespaces/formatting.
        import html
        content = svg.read_text()
        start = content.index("<svg "); end = content.index(">", start)
        content = content[:end] + ' role="img" aria-labelledby="figure-title figure-description"' + content[end:]
        end = content.index(">", start)
        content = (content[:end+1] + '\n<title id="figure-title">'+html.escape(self.title)+'</title>'
                   + '\n<desc id="figure-description">'+html.escape(self.description)+'</desc>' + content[end+1:])
        # Matplotlib leaves spaces at wrapped path lines; normalize for clean diffs.
        svg.write_text("\n".join(line.rstrip() for line in content.splitlines())+"\n")
        self.fig.savefig(out/f"{stem}.pdf", metadata={"CreationDate": None, "ModDate": None,
                                                     "Creator": "scientific-diagrams", "Title": self.title})
        self.fig.savefig(out/f"{stem}.png", dpi=dpi, metadata={"Software": "scientific-diagrams"})
        try:
            from PIL import Image
            with Image.open(out/f"{stem}.png") as preview:
                preview.convert("L").save(out/f"{stem}-gray.png")
        except ImportError:
            report["grayscale"] = "Not generated: install Pillow"
        report.update({"python": platform.python_version(), "matplotlib": matplotlib.__version__,
                       "font_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                       for p in sorted(self.fontdir.glob("DejaVuSans*.ttf"))},
                       "sha256": {ext: hashlib.sha256((out/f"{stem}.{ext}").read_bytes()).hexdigest()
                                  for ext in ("svg", "pdf", "png")},
                       "visual_review": "pending; inspect final-size color/grayscale and PDF rasterization"})
        (out/f"{stem}.qa.json").write_text(json.dumps(report, indent=2)+"\n")
        plt.close(self.fig)
        return report
