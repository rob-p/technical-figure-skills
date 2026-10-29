---
name: scientific-diagrams
description: Improve the visual design of scientific paper diagrams while preserving their technical content, or create new workflow, algorithm, and data-structure figures. Use for editable publication figures, especially computational genomics and single-cell processing; includes deterministic Python-to-SVG/PDF rendering. Ordinary numerical plots and decorative article illustrations are outside this skill's focus.
license: MIT; upstream attribution in THIRD_PARTY_NOTICES.md
metadata:
  version: "0.1.0"
---

# Scientific diagrams

Make the operation visible and the presentation deliberate. When a figure's
content is already sound, improve its aesthetics without redesigning its science.
Preserve the editable source and the user's existing backend where practical.

## Choose the work

- **Polish an existing figure:** inspect source, current render, caption, and final
  manuscript placement. Record a short content contract: labels, relations,
  branching, qualifications, counts, and coordinate conventions to preserve.
  Diagnose hierarchy, enclosure, spacing, typography, and connector defects.
  Read [visual design](references/visual-design.md) and change those presentation
  decisions first. Do not add explanatory panels or scientific claims merely to
  make the image busier.
- **Create or restructure:** read the nearby manuscript; identify the reader's
  question, transformations, and useful figure placement. Draft a panel contract
  before drawing. Read [workflow](references/workflow.md).
- **Genomics/single-cell:** also read [domain semantics](references/genomics.md).
  For the worked application, read [RECOMB2027](references/recomb2027.md).

## Working contract

Save a concise `figure-brief.md` before rendering: purpose, frozen content, panel
roles, size in mm or inches, backend, semantic palette, and intended changes.
For multiple figures, save an `outline.md` mapping each to its manuscript location.
Treat these as reusable plans, not a required approval ceremony. Use the user's
preferences and established context; ask only about consequential missing facts.

Carry forward baoyu-article-illustrator's content analysis, placement planning,
separation of information structure/style/palette, saved rendering instructions,
and revision discipline. This is a **separate vector adaptation**, not an override
of upstream's raster-only backend. See [integration](references/baoyu-integration.md).

## Design and render

Use restrained rounded containers, open data structures, aligned type, generous
internal padding, and a small hierarchy of stroke weights. Prefer whitespace to
another rectangle. Use curves where a turn is needed, not ornamental wiggles.
Define named source/target ports and shared junctions; all branches must meet the
same point. Route arrows behind content and around labels. Never terminate a flow
in an unexplained gap. Keep colors tied to entities and supplement them with labels.

SVG is the primary editable figure; export PDF for submission and PNG for review.
For an existing Python/Matplotlib project, preserve it and improve its primitives.
For a new one, use the bundled `scripts/vector.py`: rounded surfaces, sequence
strips, tables, nested groups, UMI tokens, matrices, bit strips, packed fields,
probe tracks, and port-attached Bézier connectors. It renders SVG first with live
text, then PDF with embedded fonts and a same-scene PNG. It requires Python 3.10+
and Matplotlib 3.8+; Pillow is used for grayscale review. No image-generation or
network dependency is required.

Install the helper dependencies with `python -m pip install -r
/path/to/scientific-diagrams/scripts/requirements.txt`. The adjacent
`requirements-lock.txt` records the validated Python 3.12 environment.

Run the complete, schematic worked examples from any directory:

```sh
python /path/to/scientific-diagrams/scripts/build_examples.py --out ./figure-review
```

Use [rendering and validation](references/rendering.md) for the API, deterministic
export rules, optional Graphviz/TikZ choices, and manuscript integration checks.
The examples are visual starting points, not a universal layout template.

## Review and deliver

Review at intended print width, enlarged, and in grayscale. Inspect the SVG or its
rasterization as well as a PDF rasterization; agreement between backends matters.
Check especially arrowhead attachment, branch continuity, crossings, cramped
labels, border density, small text, and whether the new visual hierarchy explains
the same content. Fix source and re-render. For polish, compare before/after with
the frozen content contract. Stop when remaining changes are taste rather than
an identifiable defect; report any unresolved issue.

The bundled renderer writes text-extent and connection reports. They catch several
layout failures, **not** scientific correctness, all overlaps, or aesthetic quality.
Record actual visual review separately from automated checks. If rendering or
inspection is unavailable, keep editable source and state what was not verified.

Deliver editable source, SVG, PDF if supported, PNG preview, caption/alt text,
reproduction command, and a short validation note. Update manuscript references
and rebuild only within the requested editing scope. Avoid incidental regeneration
of unrelated figures. Do not publish a repository or upload private manuscript
content unless the user requested that external action.
