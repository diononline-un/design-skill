# L1 · Space and layout

## Space

- **One scale**: 4px base for UI, 8px for marketing; conventionally
  `4 8 12 16 24 32 48 64 96 128`. A value between steps is a bug, not a nudge: if the
  design needs one, the scale has a gap; amend the scale.
- **Proximity groups.** Inside a group < between groups. A border needed to show a
  relationship means the gap is wrong.
- **Density is one decision per product**; mixing is a tell.
  compact (data-dense): panel 16, card 20, page edge 24, rows 32-36 ·
  comfortable (marketing): card 24-32, section gap 64-96 ·
  generous (editorial): section gap 96-128, one idea per screen.
- More space above a heading than below: it belongs to what follows.
- Under-filled containers read cheap; empty space reads considered.

## Layout

- Container per content type: prose ~65ch · content grid 1120-1280 · full-bleed imagery.
- Grid: 12 columns general, 4 for simple marketing; gutter 16-24.
- Breakpoints named once, used everywhere; three usually suffice (~390, ~768, ~1280+).
- Above the fold is a contract: what must the visitor know before scrolling? That
  decides the composition, not the reverse.
- Mobile is a composition, not a collapse: decide what leads, what reorders, what becomes
  a rail, what disappears. A two-column hero is a stack at 390 and its order is the real
  reading order. Compose at 390 before 1440.
- Navigation follows convention; novelty is a tax on every visit. Logo, existing links,
  one action; a second button beside the primary competes with it.

## The hero

More generic output lands here than anywhere else, because it is where a model reaches
for what it has seen most.

| Rule | Why |
|---|---|
| one protagonist, not headline + facts table + screenshot | three subjects means none |
| evidence over assertion: a checkable figure beats a sentence | belief is expensive, verification cheap |
| the best figure is often the one the client would rather hide | "one in five scoping weeks ends with us saying don't build it" earns trust no accuracy % can |
| don't fill the right column because it is empty | a definition list beside a headline is filler |
| whatever leads sets the contract | lead with a number and every section must keep paying in numbers |

Without imagery, weight comes from real content at display scale: a figure, a record of
what shipped, one ruled line of particulars. Invent nothing to fill the hole. If nothing
can carry it, type and space are a finished answer.

## What breaks at narrow widths (`render-audit.py` measures the result)

- Fixed heights on text containers: use `min-height`; text grows with font fallback,
  language and width.
- Flex/grid children without `min-width: 0`: a long word pushes the page sideways.
- No `overflow-wrap: anywhere` on URLs, emails, long IDs.
- Repeated cards with unequal bodies: card `display:flex; flex-direction:column`, body
  `flex: 1`, or the trailing labels misalign; this single issue makes careful pages look
  amateur.
- Tap targets under 24px on the short side: grow them with padding, not font size.
