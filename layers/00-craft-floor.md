# L1 · Craft floor

The checks that must pass in **every** mode, before any opinion. Load this before
any UI edit. No announcing, just pass them.

## Verify (on the rendered result, not the intention)

- **Contrast:** body and placeholder ≥4.5:1; large text and UI boundaries ≥3:1.
  Measured against the **actually painted** background, not the token value.
  On coloured surfaces, tint secondary text from that hue or use the foreground —
  never plain grey.
- **Depth:** a shadow carries an offset and a soft blur. A zero-offset coloured
  halo is decoration, not elevation.
- **Spacing:** tight groups, generous separation; more space above a heading than
  below it. Read the computed values, not the class names.
- **Type:** body measure 60–75ch; display max ~6rem; tracking floor −0.04em;
  balanced headings; obvious steps between scale sizes. Run the real copy at
  every breakpoint and fix what overflows.
- **Motion:** one authored moment, not one identical entrance on every section.
  Exponential ease-out from an already-visible default.
- **States:** hover, focus-visible, active, disabled, loading, error, empty.
  Plus keyboard focus that is visible and real.
- **Browser surfaces:** selection colour, caret, scrollbar, focus ring, underline
  offset, tabular figures. These ship with browser defaults that belong to no
  design system and are the cheapest signal that a page was *built* rather than
  assembled. Models skip this reliably.
- **Copy:** the product's own language. Controls name their action; errors name
  the problem *and* the recovery.
- **Coverage:** every requirement of the brief is present and findable within
  seconds.

## Refuse (defaults, not bans — the brief can earn any of them back)

**Page scaffolds**

- Same-size cards of icon + heading + text as the page structure. Cards are the
  lazy container. Nested cards are always wrong.
- The hero-metric template: big number, small label, supporting stats, accent.
- **A kicker/eyebrow above a heading — this is a ban, not a default.** No brief
  earns it back. The heading carries its own weight.
- Section numbers `01 / 02 / 03` unless the sequence itself carries information.
- A modal for a task that needs neither interruption nor protected focus.

**Surface habits**

- Gradient-clipped text. Emphasis comes from weight or size.
- Glass and blur as decoration rather than a specific effect.
- A coloured `border-left`/`border-right` above 1px on cards, list items, callouts.
- Hard offset shadows (`4px 4px 0`) outside a genuinely neobrutalist world.
- Sparklines, progress rings, soft-shadowed rounded rectangles standing in for content.
- Monospace as a costume for "technical" rather than for code, data or measurement.
- A system display face (Impact, Arial Black, platform sans) as the display voice
  of a page with its own world. Source and self-host a face whose character matches.
- Unicode glyphs or emoji standing in for an icon system. Icons are drawn, in one
  stroke and weight.
- Geometric masks approximating a photographic subject's edge. Derive a real alpha
  matte or omit the effect.
- Light/dark picked by category. Pick it from the use scene: who, where, what light.

## The swap test

The most useful single check in the whole skill.

> Replace the product name with a competitor's. Does anything break?

If nothing breaks, the page says nothing about *this* product. It is not
necessarily ugly — it is **unchosen**. Fix it in the copy, the visual and the
one signature detail — not by adding decoration.

## Earn vs. inherit

For each element, ask: *did someone decide this, or did it arrive?*

- An inherited default is fine when the axis is boring (form field borders, table stripes).
- An inherited default is a failure when the axis is the point (the hero, the
  product visual, the primary colour, the signature interaction).

Spend decisions on the axis the visitor will judge. That is usually one thing per
surface.
