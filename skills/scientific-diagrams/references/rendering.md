# Rendering and validation

## Python, SVG first

The `vector.py` helper uses points as coordinates (72 pt = 1 in), top-left origin.
It exports a live-text SVG, embedded-TrueType PDF, PNG, grayscale PNG when Pillow
is installed, and JSON QA. Set the desired final width before positioning text.
The default width is 504 pt / 7 in, a case-study choice, not a venue rule.

```python
from vector import Diagram, BLUE
d = Diagram(width=504, height=150, title="A transformation", description="Input becomes output.")
d.box("input", 20, 45, 130, 45, BLUE)
d.box("output", 330, 45, 150, 45)
d.text(85, 67.5, "Input", align="center")
d.text(405, 67.5, "Output", align="center")
d.connect(d.port("input", "e"), d.port("output", "w"))
d.save("review", "transform")
```

Import by placing the skill's `scripts/` directory on `sys.path` or copying the
module beside your figure source. Node names must be unique SVG-safe identifiers
(letters/digits/hyphens recommended). The helper rejects duplicate names.

| API | Use |
| --- | --- |
| `box(name,x,y,w,h,fill,edge,radius)` | Quiet grouping surface or rounded token; returns immutable node geometry |
| `port(name,side,fraction)` | Actual boundary attachment; side n/e/s/w; fraction in [0,1] |
| `connect(source,target,bend,via,head)` | Continuous cubic curve; endpoints are ports or point pairs |
| `route(source,target,waypoints,radius)` | Continuous rounded path through explicit axis-aligned waypoints |
| `fork(source,targets,junction)` | One shared junction and visible branch node |
| `sequence`, `table`, `matrix`, `umi` | Sequence strips, open rows, feature counts, UMI tokens |
| `bitstrip`, `track`, `exon_track` | Queried bits, segment occurrence, schematic exon layout |

For a port with fraction 0 or 1 on a rounded rectangle, the geometric corner is
outside the visible arc. Prefer mid-edge ports or offset by at least the radius.
Nodes are immutable: recreate ports if a figure is rebuilt with different geometry.
Create all needed nodes before connections; connectors render above pale surfaces
and below labels. They are not obstacle-aware. Tracks put the backbone above the
group surface and the segment above the backbone; preserve that layer distinction.

## Determinism and fonts

No random layout or timestamps; fixed SVG hash salt; bundled Matplotlib DejaVu
regular/bold/monospace fonts are selected by file. Font hashes, Python/Matplotlib
versions, final dimensions, and export hashes go into the QA JSON. SVG/PDF/PNG
are byte-reproducible in the same pinned environment. Cross-version or OS byte
identity is not promised. The repository's `requirements-lock.txt` records the
validated environment; `requirements.txt` declares the broader supported range.

SVG keeps editable text and therefore relies on installed fonts when opened
elsewhere; the PDF embeds fonts. If a venue requires outlined text, create a
separate outlined submission copy using an available vector editor and retain
the live-text master. The skill does not package font files or require TeX.

## Optional backends

- **Graphviz** is suitable for graph topology that benefits from automatic layout.
  Save DOT, use `splines=true`, `style=rounded`, restrained strokes and a fixed font;
  export with `dot -Tsvg source.dot -o figure.svg` and `dot -Tpdf ...`. Inspect ports,
  label placement, and final dimensions; automatic layout is a starting point.
  Record the Graphviz version. Do not substitute graph nodes for a sequence or
  byte-layout drawing that needs fixed geometry.
- **TikZ/PGF** is useful when mathematical typography must match LaTeX. Save a
  standalone `.tex`, define shared styles and named anchors, use rounded corners
  and Bézier `to[out=...,in=...]` connections, compile with the available TeX
  engine, and convert a copy to SVG if a converter exists. Keep TeX/PDF source
  if SVG conversion is unavailable. Report that limitation; do not claim an export
  was generated. No TeX or Graphviz dependency is required for the Python path.

These are optional workflows, not advertised as implemented exporter switches.

## Automated checks vs visual review

`Diagram.save()` stops for text outside the canvas, undersized text, out-of-bounds
shape/control geometry, and overlapping text extents. Its text metrics are from
Agg, so check the exported vector too. It does not identify every text-shape or
arrow-shape collision. A mathematically connected path can still be ugly.

`scripts/check_exports.py <directory>` checks output triplets, SVG active/external
content and live text, canvas dimensions, recorded export hashes, and QA errors.
It is a structural check, not an SVG sanitizer for arbitrary untrusted input.

For each intended deliverable inspect color and grayscale at print width and
enlarged. Rasterize PDF using `pdftoppm -scale-to 1200 -png figure.pdf review` when
available. Render SVG using a trusted SVG renderer or browser and compare. Check
font embedding with `pdffonts` and text extraction with `pdftotext` when available.
Save a separate visual-review record with findings, fixes, output hashes, and
remaining limits. Do not turn `visual_review: pending` into a pass automatically.

If inserted into a manuscript, inspect its compiled page at actual size. A good
standalone preview does not prove acceptable placement or pagination. The worked
examples deliberately use expanded canvases and require a separate integration
pass; they are not drop-in replacements for the existing RECOMB2027 figures.
