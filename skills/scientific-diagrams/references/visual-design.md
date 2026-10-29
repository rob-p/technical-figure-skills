# A visual grammar for technical figures

## Diagnose before polishing

Read the figure at final width and identify its visual problem in concrete terms:
too many equal-weight boxes; flow hidden by turns; labels competing with headings;
insufficient padding; identical objects drawn differently; arrows ending in gaps.
Keep scientifically correct content as a constraint, not an invitation to rewrite.

Choose one coherent treatment for a figure family. The supplied examples use
**quiet scientific**: white page, pale grouped surfaces, rounded outer corners,
dark slate type, muted blue/purple/ochre semantic fills, and slender curved arrows.
This is a default, not a claim of journal compliance. Match the venue and nearby
figures when their style is established.

## Hierarchy and enclosure

- Separate panel, stage, and data levels with space and type before using borders.
  Outer group surfaces can have no stroke; table cells can share separators.
  Avoid a box around every word or nucleotide.
- Use roughly 4–8 pt corner radii on stage containers at seven-inch width, smaller
  radii on tokens. Retain square cells where a byte layout or matrix needs them.
  Round the enclosure rather than implying that field boundaries are fuzzy.
- Use one aligned label baseline and equal padding for repeated structures.
  Align by visual grouping, not a grid that forces a connector through data.
- A useful starting range is 8–9 pt body, 9–11 pt stage labels, and 11–12 pt panel
  headings at final size. Around 7 pt may be needed for dense field labels, but
  recompose before shrinking. Venue requirements take precedence.
- Differentiate headings with weight and position, not all caps everywhere.
  Use a real monospace face for sequences and field values. Keep math with its
  scientific meaning; a missing glyph is not an acceptable typographic compromise.

## Connector topology and routing

A connector is a relationship, not a decorative line. Draw its topology first.

1. Define ports on actual shape boundaries: north/east/south/west and a fractional
   position along the side. Recalculate ports if the shape moves or resizes.
2. For a branch, define one junction coordinate. The trunk and all branches share
   it exactly. A small filled node may make the junction unambiguous. Lines that
   cross without a node mean no connection; route around if ambiguous.
3. Use straight connectors for direct neighbors; cubic Bézier or rounded elbow
   paths for turns. Control-point tangents should follow the departure/arrival
   direction. Avoid two 90-degree bends where one gentle arc will work.
4. Attach the arrow tip to the target boundary, with the shaft outside the shape.
   Do not combine a visibly shortened shaft with a floating arrowhead. Avoid
   clipping the head at the panel edge. Ports on the same side can require a
   waypoint outside both shapes; an automatic curve cannot infer this.
5. Keep crossings rare, labels off shafts, and optional outputs explicitly labeled.
   A dashed optional branch is redundant with text, not a substitute for it.

The bundled `connect()` creates one continuous curve ending at a named port;
`fork()` uses an explicit shared junction. Use `via` only for a deliberately routed
waypoint, and inspect it. Its geometry report checks endpoint contracts, not path
obstacle avoidance. More complex layouts need manual routing.

## Restrained color and line work

Use dark text on light fills. Give entity roles consistent colors across figures;
different sample identities need text even if colors differ. Use 0.6–0.9 pt arrows
and structural rules as starting values; de-emphasize group boundaries below that.
Avoid dense black outlines, heavy arrowheads, shadows, gradients, decorative DNA
helices, and generic database cylinders unless they encode something needed.
Test grayscale: order, labels, borders, and token IDs must still carry meaning.

Avoid encoding count or runtime with shape area, token frequency, or arrow width
unless those encodings are declared and supported by data. A toy count matrix
must be internally consistent and labeled schematic.

## Aesthetic review is a separate pass

Check at final size: can the eye find the input, the key transformation, and output
without reading a paragraph? Do curves look intentional? Are repeated objects
consistent? Does a group look quieter than the data it contains? Are corners,
padding, font weights, and arrowheads consistent across panels?

Keep a before/after preview for a polish task. List presentation changes and
confirm which scientific content stayed fixed. If content was deliberately omitted
or restructured, call that out rather than describing the change as only polish.
