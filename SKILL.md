---
name: do-design
description: >
  UI and visual design against a binding DESIGN.md, with scripts for everything
  measurable. Use to design or restyle pages and components, review UI changes,
  audit and score a UI, redesign a site, research a market before designing, push
  a bold direction, or install a design guardrail in a repo. Commands: do-audit,
  do-design-new, do-design-review, do-design-renew, do-crazy.
license: MIT
metadata:
  version: 1.1.0
---

# do-design

Paths are relative to this skill's folder; `P` is the project root. Scripts are
stdlib Python 3.8+. **Run the script before reasoning about anything it measures**,
cite its output, and never re-derive or estimate what it reports.

## Model

1. **The project's `DESIGN.md` (the paper) is binding** and beats this skill. On conflict the paper wins; say so.
2. **Every rule carries its reason.** A rule without one is deleted the first time it is inconvenient.
3. **Evidence before defaults.** A thin brief ("make it new" + a logo) is a reason to research, not to fall back on the usual look or to invent facts. No source, no claim: mark the gap or ask.
4. **Load lazily.** Only the files the command table names. Extra layers "for completeness" are a method failure.
5. **Convention is the default, not the failure.** The mode decides how far to depart.

## Modes: state one line at the start of every command

| Mode | The visitor is | Push |
|---|---|---|
| Persuade | deciding and acting | hard: a template is a failure |
| Operate | completing a task | restraint: convention is a feature |
| Read | understanding something | medium: reading comfort wins |
| Experience | inside the work itself | hard: the artifact leads |

Pick by surface, not product: a dev tool's landing page is Persuade, its settings screen Operate.

## Commands: load one command file, plus what its row names

| Command | Use when | Also load | Risk |
|---|---|---|---|
| `do-design-review` | "does this match the paper?" Cheapest, run most | the project's DESIGN.md | - |
| `do-audit` | "how good is this?" Score + ranked findings | `references/critique-rubric.md`, `references/slop-catalog.md`, layers 00-05 the scope touches | - |
| `do-design-new` | "build X": conventional, competent, on-paper | `layers/00`, the 1-3 layers the task touches; `layers/06` when the brief is thin or customer-facing | low |
| `do-design-renew` | "redo this look": new world, same product truth | `layers/00`, `layers/06` | medium |
| `do-crazy` | "something nobody in this sector would do" | `layers/00`, `layers/06` | high, by design |

Layers: `00-craft-floor` (every mode) · `01-color` · `02-typography` · `03-space-layout` ·
`04-motion-states` · `05-voice` · `06-research`. Writing a paper: `templates/DESIGN.md`,
`examples/01-two-papers.md`, `references/interview.md`.

## Scripts (all take `--json`)

| Run | Gives |
|---|---|
| `scripts/check-design.py --root P` | drift from the paper's token block. Exit 0 clean, 1 drift, 2 no paper/tokens. `--init` drafts tokens from the code |
| `scripts/audit.py scan P` | source tells (IDs as in the slop catalog), a11y and browser-surface gaps, value inventory |
| `scripts/audit.py copy P` | prose and microcopy tells, sentence rhythm, unfilled gap markers |
| `scripts/audit.py contrast FG BG` / `--paper P/DESIGN.md` | WCAG ratios |
| `scripts/audit.py score H L S C T U D` | weighted score, band, work list |
| `scripts/render-audit.py URL-or-file [--shots DIR] [--inject-css FILE]` | the painted page at 1280/768/390: overlap, sideways scroll, clipping, painted contrast, tap targets, focus visibility. `--inject-css` measures a CSS fix against the deployed page before deploying. Needs Chrome/Chromium |
| `scripts/research.py suggest\|profile\|logo\|arena` | real search phrasing, competitor page facts, logo colours, reference channels |
| `bash scripts/install-guardrails.sh P` | DESIGN.md from the template, the AGENTS.md/CLAUDE.md block, the checker |

Screenshots cost far more context than script output: take them only for what needs
eyes (hierarchy, distinction, composition), viewport only, 390 first. Scripts can be wrong
too: before reporting a P0 that looks implausible, confirm it once (a targeted screenshot or
the element's geometry), and fix the script if it was a false positive.

## Shared definitions

**Swap test.** Replace the product name with a competitor's. If nothing breaks, the page
says nothing about this product: unchosen, not ugly. Fix it in the copy, the visual and
one signature detail, never by adding decoration.

**Direction, five lines.** Written before building, shown, then wait for a yes (if told
"just do it", state the assumption in one line and go):
```
Product:    what it does, for whom, one plain sentence
Character:  2-3 concrete words (never clean, modern, sleek, minimal, premium)
World:      the place or material it belongs to; sets neutral tint, accent, imagery
Moments:    1-2 places where the screen gets rich
Signature:  one detail only this product has, used consistently
```

**Gap marker.** `[number needed]`, `[source needed]`, `[photo needed]` where a fact or
asset is missing. `audit.py copy` lists the ones still open; none may ship.

## Scoring: every evaluating command ends with it

| # | Field | Question | W |
|---|---|---|---|
| 1 | Hierarchy | Can the most important thing be named in 2 seconds? | 3 |
| 2 | Legibility | Contrast, size, measure, real copy at every width | 3 |
| 3 | System | One palette, one scale, one radius logic, one motion language | 2 |
| 4 | Craft | Alignment, spacing rhythm, states, browser surfaces | 2 |
| 5 | Content truth | Real data, specific copy, no invented claims | 3 |
| 6 | Usability | Task completes; affordances obvious; errors recoverable | 3 |
| 7 | Distinction | Does it pass the swap test? | 2 |

Score each 0-4 (4 = genuinely excellent, not "fine") and compute with `audit.py score`.
Bands: 85+ Strong, ship and fix P0 only · 70-84 Sound, ship after the named P1s ·
50-69 Weak, a real pass first · <50 Failing, the direction is wrong: rebuild (`do-design-renew`).
Score the render, not the source. A field you could not check is `u`: it scores 0 and
reads `unverified`, never an estimate. Distinction gets 4 only if you can name what makes
it this product's. The three worst fields are the work list, one action each.

Severity: **P0** blocks shipping (broken, unreadable, hard ban), report all · **P1**
damages trust, top 5 · **P2** craft, top 5 · **P3** polish, list only.
Finding format: `[Pn] location - what is wrong - fix`; script findings keep their ID.

## No paper

Say "No DESIGN.md: the guardrail has nothing to enforce." Offer to write it (template +
interview), or a retrofit from the code (`check-design.py --init` + interview §Retrofit): v1.0 is
what ships, old values go into `legacy:` (counted, not failed), gaps into the paper's delta list.
Archives and demos stay out of every scan via `skip:` in the token block (or `--skip a,b`),
by folder or file. Grep for imports before skipping: archive folders often hold live parts.
Never invent a paper so the checker passes.

## Non-negotiables

1. **Never break working code.** Props, state, routing, handlers and a11y survive; copy keeps its meaning.
2. **The brief wins.** A stated brand, font or colour outranks taste, even on a refuse list. Write it into the paper (`allow:` in the token block switches a checker rule or audit ID off on purpose).
3. **Never invent facts, assets or sources.** Cut a vague claim; never replace it with an invented specific. Use a gap marker.
4. **Keep the author's voice.** Cut machine habits, keep the person's quirks.
5. **Density, not presence.** Act on clusters (3+ distinct P0/P1 tells), never on one gradient or one em dash. A clean result is valid; never manufacture findings.
6. **Fix, never accuse.** Never say "this looks AI-generated"; name what is unchosen and what to do instead.
7. **Read-only unless asked** for reviews and audits.
