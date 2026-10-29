# RECOMB2027 aesthetic demonstrators

These original examples apply a shared visual treatment to the manuscript's three
methods-figure topics. They illustrate reusable design decisions, not drop-in
replacements. The current request prioritizes presentation: softer boundaries,
continuous attached flow, better spacing/type, and preserved technical meaning.
The private manuscript is read-only and is not distributed here.

## Design contract

Type: workflow / dictionary trace / schema and hierarchy. Style: quiet scientific.
Palette: muted blue for sample/index structures, purple for cell/flag fields,
ochre for UMI/rejection emphasis; text labels reinforce every role. Width: seven
inches. Heights are expanded to 6.17, 7.57, and 4.22 inches for these demonstrations.
Typography: installed Matplotlib DejaVu Sans, real monospace sequences, live SVG
text and embedded PDF fonts. All synthetic inputs live in the packaged toy JSON.

Frozen scientific invariants: reusable index; RAD before correction/collation;
within-sample cell correction; distinct A/x and B/x; per-probe exact-UMI toy collapse
before gene summation; Bloom negatives versus exact lookup after pass; separate
31/1/32-bit segment location and tagged probe occurrences; prelude schema versus
read values. Counts in matrices are derived from records, not hand-entered.

The examples simplify the miniature index table, some stage/software annotations,
full RAD role-byte layout and field encoding details. Schema `u32/u64` indicates
length-dependent alternatives, not simultaneous types in a real descriptor.
The exact-UMI toy does not implement every cr-like resolution/error policy. A real
content-identical polish pass must retain the source's complete labels and details.

## Reproduction

From the repository root:

```sh
python skills/scientific-diagrams/scripts/build_examples.py --out examples/recomb2027
python skills/scientific-diagrams/scripts/check_exports.py examples/recomb2027
```

Source is `skills/scientific-diagrams/scripts/build_examples.py`; shared primitives
are in `scripts/vector.py`; inputs are `assets/toy-data.json` within that skill.
See `skills/scientific-diagrams/upstream.json` for source fingerprints and
`references/recomb2027.md` for manuscript anchors and implementation evidence.

## Captions

**Workflow.** A probe-panel index is built once and reused across experiments.
Mapping writes assignments and identities to RAD v2; sample-aware barcode correction
and collation preserve composite sample–cell identities. The schematic exact-UMI
example resolves molecules separately per probe, then sums probe counts to gene G.
Probe counts can also be retained. Records, sequences and counts are schematic;
read-field positions and chemistry-specific geometry are not shown.

**Tiny dictionary.** The enabled Bloom path rejects a query containing a tested zero;
a pass still requires exact membership checking and may be a false positive. A
packed value identifies a segment, canonical-orientation relationship and position.
A separate occurrence table stores one occurrence inline or a tagged overflow index.
Fields are not to bit scale. The bit strip is an excerpt of a 64-bit block; four
positions may coincide in practice. Filter use is conditional. No component timing
or cache-miss measurement is implied. Segment s8 is a separate shared-segment example.

**RAD hierarchy.** Role metadata is declared once in the prelude; records contain
encoded values and assignments. Sample assignment precedes within-sample cell
correction. The same cell sequence in two samples remains two identities. Two
hierarchy levels are shown; names and record rows are schematic excerpts.

## Alt text

The accessible SVG descriptions summarize each figure's relationships. In the
workflow, identical UMI labels collapse within a probe; P1 counts 2/1 and P2 counts
1/1 produce G counts 3/2 for A/x and B/x. In the dictionary, q0 stops at a zero;
q1 proceeds to exact lookup with present/absent outcomes, followed by separate
segment-location and occurrence examples. In the hierarchy, prelude role fields
lead to record values, correction, and separate sample A/cell x and sample B/cell x.
