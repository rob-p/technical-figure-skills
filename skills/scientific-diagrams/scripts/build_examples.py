#!/usr/bin/env python3
"""Render original, manuscript-informed examples; never edits the manuscript."""
import argparse
import json
from pathlib import Path
from vector import Diagram, BLUE, PURPLE, GOLD, TEAL, SURFACE, MUTED, RED
from vector import exact_probe_counts, sum_to_genes, bloom_pass, pack_location

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def validate_data(data):
    if data.get("schematic") is not True:
        raise ValueError("Examples require explicitly schematic input")
    if bloom_pass(data["bits"], data["reject_positions"]):
        raise ValueError("Rejecting query must encounter a zero")
    if not bloom_pass(data["bits"], data["pass_positions"]):
        raise ValueError("Passing query must encounter only ones")
    pos, query = data["position"], data["query"]
    if data["segment_sequence"][pos:pos+len(query)] != query:
        raise ValueError("Query does not match illustrated segment interval")
    pack_location(data["segment"], data["canonical"], pos)
    counts = exact_probe_counts(data["records"])
    genes = sum_to_genes(counts, data["probe_genes"])
    if sum(genes.values()) != sum(counts.values()):
        raise ValueError("Probe-to-gene aggregation did not conserve counts")
    return counts, genes


def workflow(data, out):
    counts, genes = validate_data(data)
    d = Diagram(height=444, title="From probe panel to sample-cell counts",
                description="A reusable probe index supports mapping to RAD v2, sample-aware barcode correction, nested sample-cell grouping, per-probe UMI resolution, and gene aggregation. All data are schematic.")
    d.panel("a", "One index, reused across experiments", 20)
    d.box("panel", 14, 40, 126, 67)
    for y, label, seq in [(49,"P1","ACGTAC"), (77,"P2","TGCATG")]:
        d.text(24, y+10, label, 8)
        d.sequence(label, 48, y, seq, marked=range(6))
    d.text(77, 118, "P1 + P2 → gene G", 8, color=MUTED, align="center")
    d.box("index", 176, 48, 125, 50, BLUE)
    d.text(238.5, 63, "Build tiny index", 9, bold=True, align="center")
    d.text(238.5, 82, "piscem · keys + locations", 7.5, color=MUTED, align="center")
    d.box("experiment-1", 363, 41, 127, 30)
    d.box("experiment-2", 363, 87, 127, 30)
    d.text(426.5, 56, "Experiment 1", 8.5, align="center")
    d.text(426.5, 102, "Experiment 2 …", 8.5, align="center")
    d.connect(d.port("panel","e"), d.port("index","w"))
    d.fork(d.port("index","e"), [d.port("experiment-1","w"),d.port("experiment-2","w")], (334,73))

    d.panel("b", "Each experiment: carry identities through the workflow", 147)
    xs = [14,137,260,383]
    for x, name, title in zip(xs, ["map","rad","correct","group"],
                              ["Map read pairs","RAD v2","Correct barcodes","Group by identity"]):
        d.box(name, x, 174, 107, 128)
        d.text(x+8, 189, title, 8.6, bold=True)
    # Index is a dependency of mapping. It is not rebuilt on this path.
    source, target = d.port("index","s",.15), d.port("map","n",.75)
    d.route(source,target,[(source.xy[0],130),(6,130),(6,164),(target.xy[0],164)],radius=6)
    for a,b in [("map","rad"),("rad","correct"),("correct","group")]:
        d.connect(d.port(a,"e"), d.port(b,"w"))
    d.text(22,211,"R1",7.5); d.sequence("r1",42,201,"ACGT",marked=range(4),cell=13)
    d.text(22,239,"R2",7.5); d.sequence("r2",42,229,"TGCA",cell=13)
    d.text(22,273,"Probe assignment: P1",7.4,color=MUTED)
    d.text(22,288,"piscem",7.5,color=MUTED)
    d.table("rad-rows",142,205,["S","C","U","P"],
            [["A","x","u1","P1"],["B","x","u1","P1"],["A","x","u1","P1"]],
            [24,24,24,24], [BLUE,PURPLE,GOLD,SURFACE], row_h=19,size=7.5)
    d.text(190.5,292,"Record excerpt",7.2,color=MUTED,align="center")
    d.text(268,211,"Within sample A",7.5,color=MUTED)
    d.sequence("observed",268,226,"ACGT",cell=10,marked=[3],fill=GOLD)
    d.sequence("accepted",320,226,"ACGA",cell=10,marked=[3],fill=PURPLE)
    d.connect(d.port("observed","e"),d.port("accepted","w"))
    d.text(268,258,"observed",7.2); d.text(320,258,"accepted",7.2)
    d.text(268,280,"Permit list +",7.5,color=MUTED)
    d.text(268,292,"correction map",7.5,color=MUTED)
    for y, sample in [(208,"A"),(253,"B")]:
        d.box(f"sample-{sample}",391,y,91,37,BLUE)
        d.text(398,y+11,f"Sample {sample}",7.5,bold=True)
        d.box(f"cell-{sample}",416,y+19,58,15,PURPLE,radius=4)
        d.text(445,y+26.5,"cell x",7.5,align="center")

    d.box("outputs",14,331,211,84)
    d.text(22,344,"Resolved counts",8.8,bold=True)
    columns = ["A/x","B/x"]
    values = [[counts[(s,"x",p)] for s in ["A","B"]] for p in ["P1","P2"]]
    d.matrix("probe-counts",22,355,["P1","P2"],columns,values,cell=29)
    d.matrix("gene-counts",133,355,["G"],columns,[[genes[(s,"x","G")] for s in ["A","B"]]],cell=26)
    d.connect((110,387),(133,387),color=TEAL)
    d.text(123,367,"Σ",8.5,align="center",color=TEAL)
    d.box("resolve",260,331,230,84)
    d.text(270,344,"Resolve UMIs per probe · sample A / cell x",8,bold=True)
    for y,p in [(359,"P1"),(383,"P2")]:
        d.text(270,y+9,p,8)
        umis = [r[3] for r in data["records"] if r[:3] == ["A","x",p]]
        d.umi(f"umis-{p}",294,y,umis)
        d.connect((372,y+9),(398,y+9),color=TEAL)
        d.pill(f"resolved-{p}",406,y,str(counts[("A","x",p)]),BLUE,width=26)
    d.connect(d.port("group","s"),d.port("resolve","n",.76),color=TEAL)
    d.connect(d.port("resolve","w"),d.port("outputs","e"),color=TEAL)
    d.text(14,432,"Schematic data · S sample, C cell, U UMI, P probe · probe counts optionally retained",7.5,color=MUTED)
    return d.save(out,"workflow")


def tiny_dict(data,out):
    validate_data(data)
    d = Diagram(height=545,title="From negative filtering to probe occurrences",
                description="An enabled Bloom filter rejects a queried zero and sends passes to exact lookup. A 31/1/32-bit dictionary value locates a k-mer in a segment. A separate table stores a single probe occurrence inline or points to multiple occurrences. Schematic examples.")
    d.panel("a","Filter negatives; verify every pass",20)
    for name,y,pos in [("q0",61,data["reject_positions"]),("q1",108,data["pass_positions"])]:
        d.text(14,y+10,name,8.5,bold=True)
        d.bitstrip(name,43,y,data["bits"],pos,cell=16)
    d.box("absent",205,60,101,24,GOLD)
    d.text(255.5,72,"Absent · stop",8.5,align="center")
    d.connect(d.port("q0","e"),d.port("absent","w"),color=RED)
    d.box("exact",205,103,125,34,BLUE)
    d.text(267.5,120,"Exact dictionary lookup",8,align="center")
    d.connect(d.port("q1","e"),d.port("exact","w"),color=TEAL)
    d.box("hit",382,92,108,23,BLUE)
    d.box("fp",382,130,108,23,GOLD)
    d.text(436,103.5,"Key present: hit",8,align="center")
    d.text(436,141.5,"Key absent: stop",8,align="center")
    d.fork(d.port("exact","e"),[d.port("hit","w"),d.port("fp","w")],(355,120))
    d.text(382,164,"Bloom false positive",7.4,color=MUTED)
    d.text(14,184,"Same 64-bit block, shortened to an 8-bit excerpt; four marked positions per query.",7.5,color=MUTED)

    d.panel("b","An exact hit returns a segment location",211)
    d.table("dictionary",14,231,["key","value"],[[data["query"],"packed"]],[68,52],row_h=22,size=8)
    field_x, widths, labels, values = 165,[129,60,129],["segment · 31 bits","flag · 1 bit","position · 32 bits"],["s7","1","3"]
    for i,(width,label,value) in enumerate(zip(widths,labels,values)):
        d.box(f"field-{i}",field_x,231,width-2,44,[BLUE,PURPLE,GOLD][i],radius=4)
        d.text(field_x+(width-2)/2,243,label,7.5,align="center")
        d.text(field_x+(width-2)/2,261,value,9,bold=True,align="center",mono=True)
        field_x += width
    d.connect(d.port("dictionary","e"),d.port("field-0","w"))
    d.text(14,300,"Segment s7",8.2,bold=True)
    d.sequence("segment",110,289,data["segment_sequence"],marked=range(3,9),cell=14)
    d.text(267,299,"ACGTAC begins at position 3 (zero-based)",7.5,color=MUTED)
    d.text(14,324,"Flag: canonical-orientation relationship. Fields are not drawn to bit scale.",7.5,color=MUTED)

    d.panel("c","Translate segment locations into probe occurrences",351)
    d.box("single",14,370,225,133)
    d.box("multiple",253,370,237,133)
    d.text(26,385,"One occurrence",9,bold=True)
    d.text(265,385,"Shared segment · separate example",8.5,bold=True)
    d.text(26,412,"P1",8); d.track("s7",53,403,165,(28,96),"s7")
    d.text(265,408,"P2",8); d.track("s8-p2",294,399,176,(25,86),"s8",PURPLE)
    d.text(265,433,"P3",8); d.track("s8-p3",294,424,176,(70,131),"s8",PURPLE)
    d.box("inline",31,444,191,25,BLUE,radius=4)
    d.text(126.5,456.5,"tag 0 · inline (P1, 12, +)",8,align="center")
    d.connect(d.port("s7","s"),d.port("inline","n"))
    d.box("overflow-index",265,456,84,26,PURPLE,radius=4)
    d.text(307,469,"tag 1 | index j",7.5,align="center")
    d.box("overflow-list",376,456,102,39,PURPLE,radius=4)
    d.text(427,467,"(P2, 8, +)",7.8,align="center",mono=True)
    d.text(427,484,"(P3, 24, −)",7.8,align="center",mono=True)
    source,target = d.port("s8-p3","s"),d.port("overflow-index","n")
    d.route(source,target,[(source.xy[0],449),(target.xy[0],449)],radius=4)
    d.connect(d.port("overflow-index","e"),d.port("overflow-list","w"))
    d.text(265,510,"Additional list fetch",7.5,color=MUTED)
    d.text(14,533,"Schematic · filter use is conditional; bit positions may coincide · no timing or cache-miss scale",7.5,color=MUTED)
    return d.save(out,"tiny-dict")


def hierarchy(data,out):
    validate_data(data)
    d = Diagram(height=304,title="Schema roles preserve nested identities",
                description="Role metadata in the file prelude defines sample, cell, and UMI fields. Per-read values flow through sample assignment and within-sample correction into distinct A/x and B/x groups. Schematic excerpts, two hierarchy levels.")
    d.panel("a","Declare roles once in the RAD v2 prelude",20)
    d.table("schema",14,40,["tag","type","role payload"],
            [["b0","u32/u64","Barcode(level 0, Ls)"],
             ["b1","u32/u64","Barcode(level 1, Lc)"],
             ["u","u32/u64","Umi(Lu)"]],[51,82,217], [SURFACE,SURFACE,BLUE],row_h=20,size=8)
    d.text(381,60,"Level 0: sample",8.5,bold=True)
    d.text(381,85,"Level 1: cell",8.5,bold=True)
    d.text(14,134,"Role suffix: code:u8 | payload length:u8 | payload bytes. Ls, Lc, Lu: nucleotide lengths.",7.5,color=MUTED)
    d.panel("b","Carry values; correct and group by sample + cell",161)
    d.table("record",14,187,["n align","S","C","U","assignments"],
            [["1","A","x","u1","P1"],["1","B","x","u1","P1"]],[40,25,25,28,75],
            [SURFACE,BLUE,PURPLE,GOLD,SURFACE],row_h=21,size=7.5)
    d.box("correction",234,186,113,57)
    d.text(290.5,201,"Assign sample",8.5,bold=True,align="center")
    d.text(290.5,220,"then correct cell",8,align="center")
    d.text(290.5,234,"within that sample",7.5,color=MUTED,align="center")
    d.connect(d.port("record","e"),d.port("correction","w"))
    for y,s in [(186,"A"),(245,"B")]:
        d.box(f"sample-{s}",388,y,102,43,BLUE)
        d.text(396,y+11,f"Sample {s}",8,bold=True)
        d.box(f"cell-{s}",422,y+20,60,18,PURPLE,radius=4)
        d.text(452,y+29,"cell x",8,align="center")
    d.fork(d.port("correction","e"),[d.port("sample-A","w"),d.port("sample-B","w")],(367,225))
    d.text(14,270,"Schematic record excerpts; identities remain distinct: A/x ≠ B/x.",8,color=MUTED)
    d.text(14,290,"Two-bit-encoded values; schema is not repeated per read. Current example has two barcode levels.",7.5,color=MUTED)
    return d.save(out,"rad-hierarchy")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--figures",nargs="+",choices=["workflow","tiny-dict","rad-hierarchy"],
                        default=["workflow","tiny-dict","rad-hierarchy"])
    args = parser.parse_args()
    data = json.loads((ASSETS/"toy-data.json").read_text())
    builders = {"workflow":workflow,"tiny-dict":tiny_dict,"rad-hierarchy":hierarchy}
    for name in args.figures:
        report = builders[name](data,args.out)
        print(f"{name}: SVG/PDF/PNG, {report['min_font_pt']} pt minimum; visual review pending")


if __name__ == "__main__":
    main()
