# Genomics and single-cell semantics

Use these invariants to choose primitives. Assay- and implementation-specific
details need local evidence; this is not a universal chemistry specification.

| Primitive | Visual purpose | Preserve |
| --- | --- | --- |
| Sequence strip / highlighted interval | Query, probe, k-mer, read match | Alphabet, strand, coordinate origin, interval endpoints; mark excerpts |
| Paired reads | Two observations from one fragment | Pair relationship; no chemistry-specific field positions without evidence |
| Barcode / UMI token | Identity and molecular observation | Observed vs corrected identity; barcode is not a UMI |
| Record row / schema fields | Data carried between stages | Schema metadata vs per-read values; logical vs on-disk layout |
| Nested sample/cell group | Composite identity | Same cell sequence across samples can represent different cells |
| UMI collapse | Reads become molecular counts | Feature and sample–cell scope; error-correction policy is not always exact collapse |
| Probe-to-gene matrix | Feature aggregation | Count conservation; distinguish aggregation from another deduplication |
| Bloom block | Conditional negative rejection | Any queried zero rejects; pass needs exact lookup; positions may repeat |
| Packed fields | Stored representation | Field widths and ordering from code; identify non-proportional layouts |
| Segment / occurrence tracks | Coordinate translation | Segment coordinate vs probe coordinate, orientation, inline vs overflow |
| Transcript / exon tracks | Probe coverage, isoform compatibility | Exon order, strand, introns, junction-spanning evidence; schematic or scaled |
| Compatibility set / sparse matrix | Ambiguity and feature layout | A compatible transcript set is not a unique assignment or measured abundance |

For canonical k-mers, do not label a canonical-orientation flag as the final
read/probe strand. A hash key need not be a probe ID. A logical data-structure
access is not one CPU access, cache miss, or measured unit of runtime.

Label synthetic sequences, bits, groups, and counts as schematic. Define a toy
example's scope and verify its arithmetic. In the bundled exact-UMI toy, identical
UMIs collapse only within `(sample, cell, probe)`; probe counts then sum by gene.
This demonstrates the manuscript default without simulating all real UMI policies.

For a real biological figure, distinguish gene, transcript, and probe identifiers;
do not infer isoform resolution from a probe that matches several isoforms. Exon
or junction glyphs can convey annotation, but do not turn them into quantitative
splicing or expression conclusions without corresponding analysis.
