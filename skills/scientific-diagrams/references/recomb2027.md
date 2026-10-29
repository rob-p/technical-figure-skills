# RECOMB2027 case study

Inspected 2026-10-29. The manuscript is Typst, not LaTeX. `MANUSCRIPT_REFINEMENTS.md`
records a completed Figure 1/4 content redesign; the current request adds aesthetic
improvement. Older review proposals are superseded by the completed entries.
No manuscript file is edited or redistributed by this skill. This reference is
an original, concise requirements summary; source hashes are in `upstream.json`.

## Source map and figure needs

| Figure | Manuscript anchor / source | Concrete figure contract |
| --- | --- | --- |
| 1: workflow | `main.typ`, `fig-workflow`; `figures/methods/draw_figures.py:workflow` | Reusable probe index; reads → RAD → sample-aware correction → nested groups → per-probe UMIs → probe/gene counts |
| 4: tiny dictionary | `main.typ`, `fig-tiny-dict`; `draw_figures.py:tiny_dict` | Conditional Bloom test; exact hit → packed segment location; separate inline or overflow probe occurrences |
| 5: RAD hierarchy | `main.typ`, `fig-rad-hierarchy`; `draw_figures.py:rad_hierarchy` | Prelude descriptors and role payloads versus read values; ordered sample–cell identities |

Evidence includes the refinement log, nearby manuscript source and captions,
`figures/methods/HANDOFF.txt`, `validation.json`, and `provenance/sources.json`.
The handoff contains older build/font statements; the latest refinement log and
current source take precedence. Implementation claims here follow that recorded
evidence; this work does not independently benchmark or re-audit the Rust tools.

## Content to preserve while polishing

Build the index once per probe dataset. Mapping carries probe assignments,
barcodes, and UMIs into RAD v2 before correction/collation. Correct cell barcodes
within assigned samples. A/x and B/x remain different identities. The default
simpleaf workflow resolves UMIs within probes, then sums to genes, with optional
probe output; do not insert a second gene-level deduplication. Other supported
quantification modes described in the manuscript do not change that default.

The dictionary's value contains segment ID (31 bits), canonical-orientation flag
(1 bit), and within-segment position (32 bits). Probe coordinates come from a
separate occurrence table. Bloom rejection proves absence; a pass requires exact
lookup and may be a false positive. Filter use is conditional; four hash-derived
positions may coincide. Single occurrence is inline, high bit 0; high bit 1 points
to overflow. Show reduced dependent work without invented timings/cache misses.

RAD roles, not tag names, declare semantics: sample level 0, cell level 1, separate
UMI role. Schema is in the prelude, values in records. Do not imply arbitrary-depth
hierarchical processing is implemented: this application supports two levels.
Shortened sequences, bit excerpts, groups, and matrices are schematic, not data.

## Presentation brief

Keep content stable while softening dense rectangle outlines, creating hierarchy
with whitespace and pale surfaces, opening table rows, aligning labels, and using
continuous port-attached curves and explicit junctions. Preserve meaningful field
boundaries. Correct disconnected shafts and arrowheads. Keep qualifiers in a
caption or close to the operation. The examples use the manuscript's muted field
colors and Python choice but fresh drawing code and schematic data.

The existing manuscript figures are seven inches wide with roughly 7–9 pt labels.
The bundled examples have expanded heights and changed layouts to demonstrate the
style and primitives. They preserve the central scientific contracts but simplify
some content (for example, the miniature index table and full role-byte details).
They are **style demonstrators**, not certified content-identical polish revisions
or replacement manuscript assets. A real polish request must freeze every label
and relationship, retain current source, and fit the manuscript's available height.

For an authorized manuscript revision, adapt the current Python primitives in
place, use `--figures workflow tiny-dict` to avoid rewriting Figure 5, retain original
assets for comparison, and update captions only when the drawing requires it.
Build with the existing Makefile and inspect placement and split PDFs. Do not
restore working-tree manuscript edits or change benchmark values.

## Further opportunities, outside this implementation

Nearby source discusses variable Flex v2 anchor/spacer geometry and probe-to-isoform
compatibility/splicing annotation. Those could benefit from sequence-window or
transcript/exon schematics if requested. Chemistry-specific field positions and
biological examples need their own evidence; these opportunities do not authorize
new figure panels, speculative geometry, or expression claims.
