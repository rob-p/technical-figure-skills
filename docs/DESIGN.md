# Design decisions

The pre-implementation inspection found an upstream raster-illustration planner
with progressive references, presets, preference handling, saved prompts, and a
separate rendering step. The manuscript log showed completed scientific-content
revisions for Figures 1 and 4, with Python, SVG and seven-inch width already chosen.
The user's follow-up clarified that the missing capability was aesthetic polish:
harsh boxes, angular arrows, and disconnected paths, with content already sound.

Accordingly the skill starts with a polish mode and a frozen-content contract.
Visual grammar is central; semantic checks protect the content during that pass.
New-figure planning remains available, but does not take over ordinary polishing.
Baoyu's content-to-position analysis and saved rendering record are adapted under
MIT. Its raster backend is left intact; no hidden SVG substitution is performed.

The reusable code is deliberately small and explicit. Named geometry and ports
prevent independent arrowhead positioning; rounded routes support deliberate
obstacle avoidance; branch paths share a junction. Surface, line, glyph and label
layers are distinct so pale backgrounds do not hide internal arrows. The examples
use original code and synthetic data instead of vendoring a private drawing script.

The RECOMB2027 case study supplies concrete needs: per-panel index reuse, structured
RAD records, sample-aware correction/collation, probe-level UMI collapse and gene
aggregation, bit tests, packed segment fields, and separate probe occurrences.
The skill includes exon-track guidance for later genomics use without inventing
chemistry-specific read geometry or isoform-level evidence.

The package includes only reusable instructions, helper code, toy inputs, and
provenance/licenses. Repository-level examples, tests, release tooling, and CI stay
outside the installed skill. No fonts, decorative icons, or unused assets are
vendored. Graphviz/TikZ are optional documented choices; the tested runtime is Python.

An independent agent evaluation was not performed. Validation used realistic
manuscript-informed renders, scientific invariants, deliberate failure cases,
archive round trips, repeated export hashes, and direct visual review.
