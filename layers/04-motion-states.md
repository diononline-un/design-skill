# L1 · Motion and states

## Motion

**The one rule:** motion is feedback about a state change, never decoration.
Every animation answers "what changed?"

| Duration | Use |
|---|---|
| 100–150 ms | instant feedback: hover, press, toggle |
| 200–300 ms | substantial: panels, sheets, modals |
| >400 ms | must earn it — entrances, large transformations |

- **One easing family.** `ease-out` for arrival, `ease-in` for departure,
  `ease-in-out` for travel. **Never `linear` for UI** — nothing in the world moves
  that way, and it's the cheapest tell after the gradient blob.
- **Two motion patterns maximum** across a product, used consistently. One
  entrance, one state transition.
- **Never animate layout properties** — width, height, top, left, margin. They
  stutter. Animate `transform` and `opacity`.
- **Never `transition: all`.** Name the properties.
- **One authored moment**, not one identical entrance on every section.
- **`prefers-reduced-motion` is a defect if missing**, not a nicety. Strip
  transform and parallax; **keep** opacity and colour feedback — a state change
  with no acknowledgment is worse for those users.

### When motion is *wanted* (a few principles worth knowing)

- **Anticipation:** a small wind-up before a move — gives the eye a beat.
- **Follow-through:** parts settle after the whole stops — reads as physical.
- **Stagger:** children start a few dozen ms apart — reads as depth, not as a fade.
- **An origin:** a transition that starts at the touch point feels causal. A
  crossfade from nowhere feels like a glitch.

Use these at 10 % strength. Cartoon physics on a business interface reads as
unserious.

## States — the seven every interactive element needs

| State | Must show |
|---|---|
| default | affordance is obvious without hover |
| hover | a *visible* change, inside the palette |
| focus-visible | a real ring, ≥3:1 against its surroundings, keyboard-only |
| active/pressed | confirms the press landed |
| disabled | distinguishable from enabled, and *why* is discoverable |
| loading | progress within 100 ms; skeleton after 400 ms; text after 2 s |
| error | names the problem **and** the recovery, in a sentence not just red |

**Empty states** are a state, not an absence. Name what's missing and the next
action. Never ship a blank region.

## Responsiveness of feedback (the thresholds)

| Time | User perceives |
|---|---|
| <100 ms | instant — feels like direct manipulation |
| 100–400 ms | responsive — acceptable, no indicator needed |
| 400 ms–2 s | a spinner or skeleton is required |
| >2 s | explanation + progress, or the task is redesigned |

If real work exceeds 400 ms, show optimistic state rather than a silent wait.

## The Doherty floor

Productivity rises when response is under ~400 ms. This is why a slow app makes
every task feel longer regardless of the actual work — and why perceived speed
is a design property, not an engineering one.

## Cut without mercy

- Looping animation on things that aren't live (`animate-pulse`, shimmer on
  headings, breathing glows)
- `hover:scale` on cards, anything moving more than a few px on hover
- Parallax, scroll-jacking, autoplay
- Bounce and elastic easing
- Count-up stat animation — show the real number
- Entrance animation on data tables (the user waits for it)
