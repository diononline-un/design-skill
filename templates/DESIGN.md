# Design Constitution — <Project>

**Version** 1.0 · **Stand** <YYYY-MM-DD> · **Amended by** <name>
**Status:** binding. Read before any UI work. Amend via §12, never by improvisation.

---

## 0. Why this document exists

<Three lines. What drifts without it. What it fixes. Written for the agent who
reads it in six months with no context.>

---

## 1. Positioning

- **For:** <specific enough to exclude someone>
- **Not for:** <the excluded group>
- **First 3 seconds should feel:** <three concrete words>
- **One thing to remember tomorrow:** <single sentence>
- **Convention stance:** <fits the sector | deliberately departs>
  — because <reason>

---

## 2. Colour

| Role | Token | Value | Allowed to | Never |
|---|---|---|---|---|
| Ground | `--ground` | | page, card, panel | carry meaning |
| Ink | `--ink` | | all body and heading text | decoration |
| Ink secondary | `--ink-2` | | supporting text, captions | headlines |
| Ink muted | `--ink-3` | | meta, disabled | anything load-bearing |
| Line | `--line` | ink @ 10 % | borders, dividers | emphasis |
| Accent | `--signal` | | primary action, one figure | body text, large fills |
| Accent ink | `--signal-ink` | | text placed ON the accent | anything else |
| Surface raised | `--surface-2` | | cards, popovers | page background |

**Contrast floors** — measured with a checker, not estimated:
- Body text ≥ **4.5:1** against its actual painted background
- Large text (≥24 px or ≥19 px bold) and UI boundaries ≥ **3:1**
- Text on accent ≥ **4.5:1**, checked separately from accent-as-text

**Accent budget:** ≤ 5 % of any screen, at most two instances.
**Ramps:** derived from ink (3–4 steps), never picked per component.
**Borders:** translucent, so they work on every surface. No solid hex borders.
**Dark mode:** <yes / no / both> — <how it is derived; if yes, it is a second
design, not an inversion>
**Banned colours:** <list, with reason>

**Reason for this palette:** <one paragraph, traced to the subject's world or the
audience's expectations from research step 2>

---

## 3. Typography

**Faces**

| Job | Face | Weights | Used for | Never for |
|---|---|---|---|---|
| Display | | | h1, h2 | body, UI labels |
| Body / UI | | | paragraphs, labels, buttons | display headlines |
| Mono | | | code, IDs, figures, meta | prose |

**Scale** (role → size / line-height / tracking)

| Role | Size | Line height | Tracking |
|---|---|---|---|
| Display XL | | | |
| Display | | | |
| Heading | | | |
| Body | | | |
| Small | | | |
| Meta | | | |

**Rules**
- Hierarchy from **size and colour first**, weight second.
- Negative tracking only on display ≥ 32 px. Never on small text.
- Body measure **45–75 characters**, target 60–70.
- Numbers: `tabular-nums` wherever figures are compared or change. One format.
- Sentence case is the default. Title Case and tracked ALL-CAPS are decisions.
- Self-hosted only. No third-party font requests.

**Reason:** <why these faces for this character>

---

## 4. Space

- **Base unit:** <4 px | 8 px>
- **Scale:** 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128
- **Density:** <compact | comfortable | generous> — <what it means here>
- **Section gap:** <desktop value> / <mobile value>
- **Grouping:** proximity first. Borders only when spacing cannot carry it.
- **Off-scale values:** not permitted. If a value is needed, it is a scale gap —
  amend the scale, don't invent a number.

**Reason:** <matches content density because…>

---

## 5. Layout

- **Containers:** prose <…ch> · content <…px max> · full-bleed for <…>
- **Grid:** <12 | 4> columns, gutter <…px>
- **Breakpoints:** <…>
- **Mobile:** leads with <…>; reorders <…>; disappears <…>; becomes a rail <…>
- **Above the fold:** the visitor must know <…> before scrolling.
- **Navigation:** <pattern> — conventional because navigation novelty is a tax.

**Reason:** <…>

---

## 6. Shape & depth

- **Radius scale:** control <…> · card <…> · panel <…> · pill <…or "we have none">
- **Nesting:** inner radius = outer − padding, derived with `calc()`.
- **Elevation model:** <borders-only | 3-level shadow stack | lightness steps>
  — pick **one**, define it here:
  - level 1: <…>
  - level 2: <…>
  - level 3: <…>
- **Shadows:** <definition, or "none — we use borders">
- **Dark mode depth:** lighter surfaces, not shadows.

**Reason:** <…>

---

## 7. Motion

- **Durations:** instant <…ms> · standard <…ms> · slow <…ms>
- **Easing:** `<curve>` for arrival · `<curve>` for departure
- **Patterns allowed (max two):** <…>
- **Never:** `linear` for UI · animating width/height/top/left/margin ·
  looping decoration · motion that doesn't answer "what changed?"
- **Reduced motion:** remove transform and parallax, **keep** opacity and colour
  feedback.

**Reason:** <…>

---

## 8. Imagery

- **Type:** <photography | illustration | code-drawn | none> — one, or a stated
  rule for combining.
- **Treatment:** crop ratio <…> · colour grade <…> · corner <…> · stroke weight <…>
- **Sourcing:** <who shoots, where from, licence>
- **When unavailable:** <code-built visual | honest empty space>
  — **never** a shipped grey placeholder.
- **Alt text:** part of the design, written by whoever adds the image.

**Reason:** <why this imagery type belongs to this subject>

---

## 9. Voice

- **Tone:** <three concrete words>. Words like clean, modern, sleek, premium are
  not permitted as descriptions — they decide nothing.
- **Banned words:** <list>
- **Sentence rhythm:** mostly short, one long. Uniform length is the machine tell.
- **Headlines:** <pattern — what it must say and for whom>
- **Claims:** checkable or cut. Every number has a source or is labelled as an
  estimate.
- **Punctuation:** em dash <allowed/not> · exclamation marks <allowed/not> ·
  periods on short strings <none>
- **Example of our voice:** <paste a real paragraph>

**Reason:** <…>

---

## 10. Precedent

| ✅ Right, because | ❌ Wrong, because |
|---|---|
| `<path>` — <the specific thing it does right> | `<path>` — <the specific rule it breaks> |
| | |
| | |

*Update whenever a new good example appears. This is the section that ages into
project memory.*

---

## 11. We deliberately do not

Each line prevents a future session from re-proposing something already rejected.

- **<thing>** — rejected because <reason>.
- **<thing>** — rejected because <reason>.
- **<thing>** — rejected because <reason>.

---

## 12. Amendment

- **Proposer:** <who may propose> · **Decides:** <who>
- **Version bump:** minor for additions, major for changes that invalidate
  existing work.
- **A deliberate one-off** is permitted once, with the reason recorded in the log
  below — not silently.
- **Uncovered decision:** if the paper doesn't cover it, the change is *not*
  free. Amend first, then build.

### Log

| Version | Date | Change | Why |
|---|---|---|---|
| 1.0 | | initial | |
