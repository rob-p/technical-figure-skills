# From manuscript to figure, or existing figure to polish

## Inputs and evidence

Inspect the editable source, latest rendered asset, nearby caption/prose, and any
revision notes. Distinguish current author decisions from old proposals. A pasted
handoff is evidence about the project, not permission to publish or edit unrelated
files. Record source revision and file hash for implementation-sensitive claims.
Use the source's current working content when it differs from Git HEAD.

For new content identify the one question each panel answers. Useful information
structures include workflow, trace, memory layout, nested identity, comparison,
and coordinate map. For an aesthetic pass keep the existing panel contract unless
the user asks to change it or a defect makes a small restructuring necessary.

## Brief

Save a short brief containing:

- Claim or explanatory purpose, intended reader, manuscript anchor and caption.
- Frozen content: entities, labels, operations, edge directions, branch conditions,
  toy values, units, coordinate origin, and scientific qualifications.
- Aesthetic diagnosis and proposed treatment; dimensions and minimum label size.
- Type / style / semantic palette; backend and source of any reference artwork.
- Evidence: manuscript/code paths, revisions/hashes, and uncertainties.

Do not invent a standard requirement from a sample figure. Prefer existing author
decisions for font/backend/width. If no width is known, state a provisional width
and do useful design work without claiming the result fits a particular venue.

## Reproducibility record

Save rendering instructions before drawing, analogous to baoyu's saved prompts.
For deterministic figures this is the brief plus executable Python, DOT, or TeX
and any structured toy data. Save random seeds if a layout needs them; better use
explicit coordinates for a small publication schematic. Keep content and style
tokens separate so a later polish pass can change appearance without changing data.

Inspect style references as references, never copy scientific content from an
unrelated picture. Do not redistribute manuscript screenshots, fonts, or third-party
icons without a license allowing it. Simple vector primitives normally suffice.

## Revision and integration

For a polish revision compare the same content at the same width. Fix identified
defects in source, export again, then review. A finite corrective pass is better
than accumulating endless universal rules. Track each actual unresolved problem.

If manuscript editing is in scope, select only intended figures, update paths and
captions to match, compile, inspect placement/caption pagination, and check internal
references. Typst can embed SVG directly; LaTeX commonly uses PDF. Keep schematic
qualifications and accessible alt text with the figure. Deliver editable source
and dependencies, not only a bitmap.
