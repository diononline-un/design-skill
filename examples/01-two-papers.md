# Worked examples — what a filled paper looks like

Two examples at opposite ends of the spectrum. Read both: the difference between
them is the point. Neither is a template to copy — they show the *shape* of a
answer, and how far the answers diverge for two different subjects.

---

# Example A — an airy consumer product

**Ridgeline** — a note and planning app for people who think on walks.

## 1. Positioning
- **For:** people who plan by walking and want the plan to survive the walk
- **Not for:** project managers who want boards, dependencies and gantt charts
- **First 3 seconds:** calm, outdoors, unhurried
- **Remember:** "your thinking has a place, and it's outside"
- **Convention stance:** departs from note-app convention (white canvas,
  sidebar, monospace density) because the subject is a landscape, not a desk
- **Reference qualities taken:** the light in a Hiroshi Yoshida print, the
  restraint of a topo map's line weight — qualities only, no layout copied

## 2. Colour
| Role | Token | Value | Allowed | Never |
|---|---|---|---|---|
| Ground | `--ground` | `#F7F4EE` | page, cards | meaning |
| Ink | `--ink` | `#1F1B16` | all text | decoration |
| Ink secondary | `--ink-2` | `#5E554A` | captions, meta | headlines |
| Line | `--line` | ink @ 10 % | rules, dividers | emphasis |
| Accent | `--signal` | `#B4653A` | one action, one figure | body text |
| Accent ink | `--signal-ink` | `#1F1B16` | text on the accent | else |

- Warm ramp because the subject is outdoors in daylight, not a screen at night.
- **Accent budget:** one instance per screen. The warm tone is the only saturated
  moment; everything else is ramp.
- **Dark mode:** yes — "dusk", not inverted. Ground becomes `#17150F`, ink stays
  warm; the accent **loses** saturation at dusk (it vibrates on dark).
- **Banned:** pure white, pure black, any blue, any gradient between hues.

## 3. Typography
| Job | Face | Weights | Used for |
|---|---|---|---|
| Display | Newsreader | 400 | h1, h2 |
| Body | A humanist sans, self-hosted | 400, 500 | everything else |
| Mono | none | — | — |

- Display is a serif because the product is about *reflection*, and serifs read as
  considered rather than fast.
- No mono at all: there are no IDs, hashes or figures worth aligning. Adding a
  mono "for tech feel" would contradict the positioning.
- Body measure capped at 62ch — long lines make reading feel like work, which is
  the opposite of the promise.

## 4. Space
- Base 8 px (marketing-facing product, not data-dense).
- **Density: generous.** One thought per screen is the unit.
- Section gap 96 desktop / 48 mobile.
- Whitespace is the product's main visual argument, so it is a rule, not a taste.

## 5. Layout
- Prose container 62ch; content container 1120 px; maps are full-bleed.
- Mobile leads with the current note, the map reorders below, the sidebar
  becomes a bottom sheet.
- Above the fold: what this is, and the *one* thing it does differently.

## 6. Shape & depth
- Radius: control 8 · card 14 · panel 18. No pills anywhere.
- **Elevation: borders-only.** No shadows at all except one soft neutral shadow
  on the floating capture button (the only thing that floats).
- Dark mode depth: surface lightness steps, never shadows.

## 7. Motion
- 120 ms instant / 240 ms standard.
- Arrivals `ease-out`, departures `ease-in`. Nothing else.
- Two patterns: (1) content fade-and-rise 8 px on enter, (2) map pan follows the
  finger 1:1 with no easing.
- Forbidden: parallax, looping animation, scroll-triggered reveals per element.

## 8. Imagery
- **Type: photography, one treatment.** Landscape photography, shot at 4:5 or
  16:9 only, slightly desaturated, no people facing camera.
- The map is code-drawn, never a screenshot of another map product.
- When no photo suits a slot: no image. Space is allowed.

## 9. Voice
- **Tone:** unhurried, plain, dry.
- **Banned:** seamless, effortless, unlock, journey, mindful, space (as a verb).
- Rhythm: mostly 6–12 word sentences, one long one per section.
- Headlines name a situation, never a benefit ("A walk that ends with a plan",
  not "Plan better").
- No exclamation marks anywhere, including the marketing page.

## 10. Precedent
| ✅ Right | ❌ Wrong |
|---|---|
| `app/(marketing)/page.tsx` — the hero is 70 % empty and the emptiness is the argument | `app/(app)/sidebar.tsx` — three grey steps of near-identical weight; violates the 3-step ink rule |
| `components/note-card.tsx` — radius 14, no shadow, hairline only | `components/legacy/tag.tsx` — pills, contradicts "we have no pills" |

## 11. We deliberately do not
- **Have a sidebar in the editor.** Rejected: it turns thinking into filing.
- **Use an icon set.** Rejected: the UI has fewer than six actions; words are
  clearer and warmer.
- **Show streaks, counts or progress.** Rejected: the product is not a habit
  tracker and the numbers create guilt.

---

# Example B — a dense professional tool

**Lattice** — inventory reconciliation for 5–50 person distributors.

## 1. Positioning
- **For:** operations leads at small distributors who reconcile stock weekly
- **Not for:** enterprise WMS buyers; not for retailers with one location
- **First 3 seconds:** precise, serious, fast
- **Remember:** "it finds the differences so you don't have to"
- **Convention stance:** *fits* the sector. Trust is the purchase, and trust comes
  from looking like a tool, not a startup.
- **Reference qualities taken:** the density of a terminal, the calm of a bank
  statement — not their styling

## 2. Colour
| Role | Token | Value | Allowed | Never |
|---|---|---|---|---|
| Ground | `--ground` | `#0F0F10` | app shell | meaning |
| Surface | `--surface-2` | `#19191B` | cards, rows | page |
| Ink | `--ink` | `#EDEDED` | all text | decoration |
| Ink secondary | `--ink-2` | `#A1A1A6` | labels, meta | headlines |
| Ink muted | `--ink-3` | `#85858B` | disabled | anything load-bearing |
| Line | `--line` | ink @ 8 % | every divider | emphasis |
| Accent | `--signal` | `#3E7BFA` | selection, one figure, focus ring | buttons, fills |
| Semantic | warn / error | | discrepancies only | brand |

- **Neutral-first, deliberately.** Users stare at this for six hours; the
  *content* carries colour, never the chrome.
- **The primary button is off-white, not accent.** Deliberate: the accent stays
  reserved for the discrepancy itself, which is the thing the user hunts.
- Light mode exists but is secondary; the product was designed for a desk with a
  monitor.

## 3. Typography
| Job | Face | Weights | Used for |
|---|---|---|---|
| UI | Inter | 400, 500, 600 | everything |
| Mono | a mono with tabular figures | 400 | quantities, SKUs, dates, deltas |

- Inter here is **a decision, not a default**: it has the largest x-height of the
  candidates at 12–13 px, which is where 80 % of this UI lives. Recorded so
  nobody "upgrades" it later.
- Body size is 13 px, not 16: density is the feature.
- Every number is mono with `tabular-nums`. Quantities align in a column or the
  table is unreadable.

## 4. Space
- Base 4 px.
- **Density: compact.** Row height 32, gap 2, cell padding 8.
- Section gap 24 — sections are panels, not pages.
- Padding follows density: panels 16, cards 20, page edges 24.

## 5. Layout
- Shell fills the viewport. Sidebar 248 px, content fluid capped at 1600.
- 12-column grid inside the content, gutter 16.
- Mobile: the table becomes a card list; the sidebar becomes a drawer. The
  discrepancy count stays visible at all times — it is the reason they opened it.
- Above the fold: how many discrepancies, and the filter that narrows them.

## 6. Shape & depth
- Radius: control 8 · card 12 · panel 14. No pills; counts are quiet mono text.
- **Elevation: lightness steps only.** `--surface-2` for cards, `--surface-3` for
  popovers. No shadows except one on floating menus.
- Nested radii derived with `calc(--r - --pad)`.

## 7. Motion
- 100 ms feedback / 180 ms transitions. Nothing slower; slow tools feel broken.
- `ease-out` only.
- One pattern: state change = colour and opacity transition. No movement.
- Forbidden: any entrance animation on data. A table that animates in is a table
  the user waits for.

## 8. Imagery
- **Type: none.** This is a tool. No hero photography, no illustration.
- "Richness" comes from a well-drawn chart and beautifully set figures.
- If a marketing page needs a visual, it is a **real screenshot with plausible
  data**, never a mockup with lorem ipsum.

## 9. Voice
- **Tone:** exact, unexcited, literal.
- **Banned:** smart, seamless, powerful, AI-powered, insights (as a noun).
- Labels are nouns: "Discrepancies", not "See your discrepancies".
- A change says what it compares to: "+12 vs last week", never "+12".
- No greeting headlines. The page title is the period: "October 2026".

## 10. Precedent
| ✅ Right | ❌ Wrong |
|---|---|
| `features/reconcile/table.tsx` — 32 px rows, mono quantities, hairline dividers, one accent on the count | `features/dashboard/stat-cards.tsx` — four cards with sparklines nobody reads; sparklines are decoration |
| `features/recon/empty.tsx` — names the next action and shows where the import goes | *(none yet)* |

## 11. We deliberately do not
- **Have a dashboard of charts.** Rejected: the user has one question — what
  doesn't match — and a dashboard answers eleven others.
- **Animate row insertion.** Rejected: at 400 rows, movement is noise.
- **Use a marketing sans for the app.** Rejected: it reads as unserious at 13 px.

---

## What the two examples prove

| | Ridgeline | Lattice |
|---|---|---|
| Density | generous | compact |
| Base unit | 8 | 4 |
| Elevation | borders-only | lightness steps |
| Accent used for | the one action | the discrepancy |
| Mono | none | everywhere |
| Imagery | photography | none |
| Motion | fade-and-rise | colour only |

**Nearly every value is opposite.** That is the whole point: a constitution is
not a style guide applied to everything — it is a set of decisions *derived from
the subject*. If your paper for a logistics tool looks like your paper for a
meditation app, the research step failed.
