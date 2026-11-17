# L1 · Space and layout

## Space

- **One scale.** 4px base for UI, 8px for marketing. Conventional:
  `4 8 12 16 24 32 48 64 96 128`. A value between steps is a bug, not a nudge —
  if the design needs one, the scale has a gap; amend the scale.
- **Proximity does the grouping.** Inside a group < between groups. If you need a
  border to show a relationship, the gap is wrong.
- **Density is one decision per product:** compact (data-dense), comfortable
  (marketing), generous (editorial). Mixing them is a tell.
  - compact: panel 16, card 20, page edge 24, row 32–36
  - comfortable: card 24–32, section gap 64–96
  - generous: section gap 96–128, one idea per screen
- **Section rhythm:** more space above a heading than below it — the heading
  belongs to what follows.
- **Whitespace is quality.** Under-filled containers read cheap; empty space
  reads considered. "What you remove defines what remains."

## Layout

- **Container decision per content type**, not one width for everything:
  prose ~65ch · content grid 1120–1280 · full-bleed for imagery.
- **Grid:** 12 columns general, 4 for simple marketing. Gutter 16–24.
- **Breakpoints:** name them once, use them everywhere. 3 are usually enough
  (mobile ~390, tablet ~768, desktop ~1280+).
- **Above the fold is a contract:** what must the visitor know before scrolling?
  That decides the composition. Not the reverse.
- **Mobile is a composition, not a collapse.** Decide explicitly: what leads,
  what reorders, what becomes a horizontal rail, what disappears.
  A two-column hero has no balance at 390px — it becomes a stack, and the stacked
  order is the real reading order. Compose at 390 before 1440.
- **Navigation follows convention.** Novel navigation is a tax on every visit.
  Logo, existing links, one action. A second button next to the primary is a
  competing action.

## The hero

Where more generic output lands than anywhere else, because it's where a model
reaches for what it has seen most.

| Rule | Why |
|---|---|
| **One protagonist** — not a headline *and* a facts table *and* a screenshot | Three subjects means no subject |
| **Evidence over assertion** — a checkable figure beats a sentence they must believe | Belief is expensive; verification is cheap |
| **The best figure is often the one the client would rather hide** | "One in five scoping weeks ends with us saying don't build it" earns trust no accuracy % can — nobody fabricates a statistic that costs them work |
| **Don't fill the right column because it's empty** | A definition list beside a headline is a filler paragraph |
| **Whatever leads sets the contract** | Lead with a number and every section below must keep paying in numbers |
| **Compose at 390 first** | The phone layout is the honest one |

**Without imagery, weight must come from real content at display scale** — a
figure, a record of what shipped, one ruled line of particulars. Invent nothing
to fill the hole. If the subject has nothing that can carry it, the hero is type
and space — and that is a finished answer, not an unfinished one.

## Breakpoints that break

Common causes of layout failure at narrow widths:

- **Fixed heights on text containers.** Use `min-height`. Text grows when the font
  falls back, the language changes, or the viewport narrows.
- **Missing `min-width: 0`** on flex/grid children — a long word forces sideways
  page scroll. This is the usual cause of a page that scrolls horizontally.
- **No `overflow-wrap: anywhere`** on anything receiving a URL, email or long ID.
- **Repeated cards with unequal bodies** — make the card a column flex and give
  the body `flex: 1`, or the trailing labels don't align. This single issue makes
  an otherwise careful page look amateur.
- **Tap targets under 24px** on the short side. Grow with padding, not font-size.
- **Testing at one width.** 1280 proves nothing about 420.
