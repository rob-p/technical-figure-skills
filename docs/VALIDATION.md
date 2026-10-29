# Validation record

Validated 2026-10-29 on Python 3.12.3 / Matplotlib 3.11.2 / Pillow 13.0.0. Exact
installed dependencies are in the packaged `scripts/requirements-lock.txt`.

- Skill-creator's bundled `quick_validate.py`: passed name/frontmatter validation.
- 16 unit tests: passed scientific identity/aggregation invariants, Bloom behavior,
  packed field limits, query/segment matching, named-port and junction continuity,
  rounded-route endpoints, deliberate overlap/clipping failures, SVG bold styling,
  byte-identical SVG/PDF/PNG reproduction, tamper detection, and package safety.
- Three complete examples: generated SVG/PDF/300-dpi PNG and grayscale PNG.
  Structural export checks passed; no text extent/overlap or canvas errors.
- SVG text remains editable, with accessible title/description and no embedded
  raster, active element, or external asset. PDF fonts are embedded and text is
  extractable. SVG CSS now explicitly retains bold weight.
- Independent SVG rendering with Sharp/librsvg and PDF rendering with Poppler
  were inspected, along with color and grayscale previews and enlarged originals.
  The separate `examples/recomb2027/visual-review.json` records actual review and
  final export hashes; raw renderer QA intentionally still says review is pending.
- The archive has one skill root, deterministic ZIP metadata, valid CRCs, safe paths,
  and a SHA-256 file manifest. Round-trip extraction and standalone rendering work
  without access to repository-level example files or the private manuscript.
- The original upstream MIT license is byte-identical to its pinned source. Source
  hashes and adaptation scope are recorded in the package. Private manuscript files
  are fingerprinted and summarized, not copied or edited.

The visual pass caught and fixed hidden internal connectors, a path crossing a
panel heading, an overflow path crossing an output container, a footer overlap,
and SVG/PDF font-weight inconsistency. These illustrate why geometry checks alone
cannot certify presentation quality.

The examples use seven-inch width with expanded heights, retain central scientific
contracts, and simplify selected details. They are style demonstrators, not
content-identical replacement figures. No manuscript build or placement validation
was performed because this task creates a skill and separate examples. No benchmark,
component speedup estimate, upstream Rust execution, independent-agent evaluation,
Graphviz/TikZ execution, clean package installation, or remote CI run is claimed.
The optional backends are documented guidance. Supported version ranges beyond the
pinned environment have not been exhaustively tested.

The local repository is committed and clean on `main`, with no remote configured.
Publication remains a separate action. CI is provided for future pushes, but has
not run remotely.
