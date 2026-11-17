# L1 · Craft floor

Must pass in every mode, before any opinion. Load before any UI edit; pass it without
announcing it. Items marked (script) are measured by `render-audit.py` / `audit.py scan`.

## Verify on the rendered result

- **Contrast** (script): body and placeholder ≥4.5:1, large text (≥24px, ≥18.7px bold)
  and UI boundaries ≥3:1, against the background actually painted, not the token. On a
  coloured surface tint secondary text from that hue or use the foreground, never plain grey.
- **Depth**: a shadow has an offset and a soft blur. A zero-offset coloured halo is
  decoration, not elevation.
- **Spacing**: tight inside groups, generous between them; more space above a heading
  than below it. Read computed values, not class names.
- **Type**: body measure 45-75ch (target ~65), display max ~6rem, tracking floor
  -0.04em, balanced headings, clearly distinct scale steps. Real copy at every width;
  fix what overflows (script).
- **Motion**: one authored moment, not the same entrance on every section; exponential
  ease-out from an already-visible default.
- **States**: hover, focus-visible (script), active, disabled, loading, error, empty.
- **Browser surfaces** (script): selection colour, caret, scrollbar, focus ring,
  underline offset, tabular figures. They ship as defaults that belong to no system and
  are the cheapest proof a page was built rather than assembled. Models skip them reliably.
- **Copy**: the product's own language; controls name their action; errors name the
  problem and the recovery.
- **Coverage**: every requirement of the brief is present and findable within seconds.

## Refuse by default (the brief can earn any of these back, recorded in the paper)

Page scaffolds:
- Same-size cards of icon + heading + text as the page structure; cards are the lazy
  container, and cards inside cards are always wrong.
- The hero-metric template: big number, small label, supporting stats, accent.
- A kicker/eyebrow above a heading, unless it carries information the heading cannot
  (a date, a step, a category the reader filters by).
- Section numbers `01 / 02 / 03` unless the sequence carries information.
- A modal for a task that needs neither interruption nor protected focus.

Surface habits:
- Gradient-clipped text; emphasis comes from weight or size.
- Glass and blur as decoration rather than a specific effect.
- A coloured `border-left/right` above 1px on cards, list items, callouts.
- Hard offset shadows (`4px 4px 0`) outside a deliberately neobrutalist world.
- Sparklines, progress rings, soft-shadowed rounded rectangles standing in for content.
- Monospace as a costume for "technical" rather than for code, data or measurement.
- A system display face (Impact, Arial Black, platform sans) as the display voice of a
  page with its own world: source and self-host a face whose character matches.
- Unicode glyphs or emoji standing in for an icon system; icons are drawn, one stroke
  and weight.
- Geometric masks approximating a photographic subject's edge: derive a real alpha
  matte or omit the effect.
- Light or dark picked by category: pick it from the use scene (who, where, what light).

## Earn vs. inherit

For each element: did someone decide this, or did it arrive? An inherited default is
fine on a boring axis (field borders, table stripes) and a failure on the axis the
visitor judges (the hero, the product visual, the primary colour, the signature
interaction). Spend decisions there; usually that is one thing per surface.
