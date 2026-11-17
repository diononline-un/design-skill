# L1 · Motion and states

## Motion is feedback about a state change, never decoration

Every animation answers "what changed?"

| Duration | Use |
|---|---|
| 100-150 ms | instant feedback: hover, press, toggle |
| 200-300 ms | substantial: panels, sheets, modals |
| >400 ms | must earn it: entrances, large transformations |

- One easing family: ease-out arriving, ease-in leaving, ease-in-out travelling. Never
  `linear` for UI; nothing in the world moves that way.
- At most two motion patterns per product (one entrance, one state transition).
- Animate `transform` and `opacity`, never width, height, top, left or margin (they stutter).
- Never `transition: all`; name the properties.
- One authored moment, not the same entrance on every section.
- `prefers-reduced-motion` missing is a defect. Strip transform and parallax; keep opacity
  and colour feedback: an unacknowledged state change is worse for those users.

When motion is wanted, at 10 % strength (cartoon physics on a business UI reads unserious):
anticipation (a small wind-up gives the eye a beat) · follow-through (parts settle after
the whole stops) · stagger (children a few dozen ms apart read as depth) · an origin
(a transition from the touch point feels causal; a crossfade from nowhere feels like a glitch).

## The seven states of every interactive element

| State | Must show |
|---|---|
| default | the affordance is obvious without hover |
| hover | a visible change, inside the palette |
| focus-visible | a real ring, ≥3:1 against its surroundings, keyboard only |
| active | the press landed |
| disabled | distinguishable, and why is discoverable |
| loading | progress within 100 ms, skeleton after 400 ms, text after 2 s |
| error | the problem and the recovery, in a sentence, not just red |

Empty states are a state: name what is missing and the next action. Never a blank region.

## Response time

<100 ms feels instant · 100-400 ms responsive, no indicator · 400 ms-2 s spinner or
skeleton required · >2 s explanation + progress, or redesign the task. Productivity rises
below ~400 ms, so perceived speed is a design property. Past 400 ms of real work, show an
optimistic state instead of a silent wait.

## Cut

Looping animation on anything not live (pulse, shimmer on headings, breathing glows) ·
`hover:scale` on cards, anything moving more than a few px on hover · parallax,
scroll-jacking, autoplay · bounce and elastic easing · count-up numbers (show the real
one) · entrance animation on data tables (the user waits for it).
