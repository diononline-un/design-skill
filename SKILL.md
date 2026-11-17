---
name: do-design
description: >
  Design work with a guardrail. Commands: do-audit (score an existing UI),
  do-design-new (design something new), do-design-review (check work against the
  project's design paper), do-design-renew (deliberate redesign of an existing
  surface), do-crazy (off-rails creative direction after real market research).
  Also installs guardrails that flag design changes contradicting the project's
  DESIGN.md without anyone invoking this skill.
license: MIT
version: 1.0.0
---

# do-design

Five commands, one model of how design actually gets decided, and a guardrail
that runs without being asked.

**Read §Model before your first command.** It is the part that makes the
commands work, and it is short.

---

## §Model — the four things that matter

**1. Design is a set of decisions, not a set of rules.** A rule without a reason
is deleted the first time it's inconvenient. Every rule in the project paper
carries its reason.

**2. Three layers, loaded as needed.** This is how the skill stays cheap.

| Layer | What it is | Loaded |
|---|---|---|
| **L0 — This file** | Router, model, guardrail, scoring key | Always |
| **L1 — `layers/`** | The fundamentals: colour, type, space, layout, motion, voice, research. ~1k tokens each | Only the layers the task touches |
| **L2 — `references/`** | Depth: the slop catalog (45 named tells + voice), the critique rubric (thresholds + personas), the interview. Plus `examples/` — two worked papers | Only when the command says so |

**Never load a layer "for completeness".** A task about a button does not need
the layout layer. This is the whole point of the structure.

**3. The project paper beats this skill.** `DESIGN.md` in the project root is
binding. This skill is the *method* for producing and enforcing it — not a
competing opinion. When they conflict, the paper wins and you say so.

**4. Convention is the default, not the failure.** Fitting the category is right
for tools, dashboards, checkout, docs. Departing is right for landing pages and
anything selling a point of view. Which one applies is decided by the **mode**
(§Modes), never by taste.

---

## §Modes — decide this before anything else

State the mode in one line at the start of every command. It decides how hard to
push and which layer wins conflicts.

| Mode | The visitor is… | Design's job | Push |
|---|---|---|---|
| **Persuade** | deciding and acting | earn attention, prove the offer | hard — a template is a failure |
| **Operate** | completing a task | get out of the way, be predictable | restraint — convention is a feature |
| **Read** | understanding something | structure for comprehension | medium — reading comfort wins |
| **Experience** | inside the work itself | recede, let the artifact lead | hard — the artifact is the design |

Pick by **surface, not product**. A dev tool's landing page is Persuade. The same
product's settings screen is Operate.

---

## §Commands

| Command | Use when | Loads |
|---|---|---|
| **`do-audit`** | "How good is this?" — score an existing UI, ranked findings | L1 all + `commands/do-audit.md` + rubric |
| **`do-design-new`** | "Build X" — new surface, conventional-safe | mode layer + 2–3 L1 + `commands/do-design-new.md` |
| **`do-design-review`** | "Does this match the paper?" — check work in progress | `commands/do-design-review.md` + `DESIGN.md` |
| **`do-design-renew`** | "Redo this" — deliberate replacement of an existing look | `commands/do-design-renew.md` + craft floor |
| **`do-crazy`** | "Make me something nobody would expect" — after research | `commands/do-crazy.md` + research protocol |

**Safe vs. bold, in one table:**

| | Produces | Ceremony | Risk |
|---|---|---|---|
| `do-design-new` | conventional, competent, on-paper | direction → confirm → build | low |
| `do-design-renew` | replaces a look, keeps product truth | audit → direction → confirm → build | medium |
| `do-crazy` | off-distribution, one dominant move | **research first** → 3 directions → pick → build | high, by design |

`do-crazy` is not "more styling". It is a different *world* — a structure, a
material, a composition the category wouldn't attempt. If the output would look
at home next to competitors, `do-crazy` failed.

---

## §Scoring — the seven fields

Every command that evaluates ends with this table. Numbers, not adjectives.
Score 0–4 each; a 4 means genuinely excellent, not "fine".

| # | Field | The question | Weight |
|---|---|---|---|
| 1 | **Hierarchy** | Can the most important thing be named in 2 seconds? | 3 |
| 2 | **Legibility** | Contrast, type size, line length, real copy at every width | 3 |
| 3 | **System** | One palette, one scale, one radius logic, one motion language | 2 |
| 4 | **Craft** | Alignment, spacing rhythm, states, browser surfaces, detail | 2 |
| 5 | **Content truth** | Real data, specific copy, no invented claims | 3 |
| 6 | **Usability** | Task completes; affordances obvious; errors recoverable | 3 |
| 7 | **Distinction** | Could this be swapped onto a competitor unchanged? | 2 |

**Weighted score** = Σ(field × weight) / 72 × 100.

| Score | Band | What to do |
|---|---|---|
| 85–100 | **Strong** | Ship. Fix only P0. |
| 70–84 | **Sound** | Ship after the P1s the report names. |
| 50–69 | **Weak** | A real pass is justified before shipping. |
| <50 | **Failing** | The direction is wrong; rebuild, don't polish. |

**Rules for scoring:**
- Score the **rendered result**, never the source.
- A field you could not check scores **0** and is marked `unverified` — never estimated.
- `Distinction` scores 4 only if you can name what makes it *this* product's.
- Report the **three worst fields** as the work list. A wall of findings is not a report.

---

## §Guardrails — the part that runs uninvited

The problem: a coding agent edits a button, picks a new blue because it needed
one, and nobody notices for three months. A document nobody is told to read
cannot prevent that.

**The fix is placement.** Put the rule where every agent already looks.

### Install

Run `scripts/install-guardrails.sh <project-root>`. It does three things:

1. **Writes `DESIGN.md`** if missing (from `templates/DESIGN.md`), or verifies the
   existing one has a `<!-- TOKENS -->` block.
2. **Appends a block to `AGENTS.md`** (and `CLAUDE.md`, `.cursorrules` if present)
   — the file agents read at session start.
3. **Writes `scripts/check-design.py`** — a dependency-free checker.

### The AGENTS.md block (this is the guardrail)

```markdown
## Design guardrail (read before any UI change)

`DESIGN.md` is binding. It lives in the repo root, section 2 holds the tokens.

Before you change any colour, size, radius, font, shadow or spacing value:
1. Find the token in DESIGN.md §2–§6.
2. Use the token. Do not introduce a value that is not in the paper.
3. If the task genuinely needs a value the paper lacks, **stop and ask**:
   "The paper has no token for X. Add one (§12 amendment), or use <nearest>?"

After changing UI files, run: `python3 scripts/check-design.py`
It reports drift from the paper. Fix drift or explain it. Do not silence it.

Hard rules, no exceptions without an amendment:
- No colour outside the palette in §2, including in gradients and shadows.
- No font outside §3. No new weights.
- No radius, spacing or shadow value outside §4 and §6.
- Accent colour: ≤5% of any screen, never body text.
- No emoji as UI icons. No gradient-clipped text.
- Every animation gated by `prefers-reduced-motion`.
```

**Why this placement works:** `AGENTS.md`/`CLAUDE.md` is loaded automatically by
coding agents at session start — no invocation, no skill recall, no user memory
involved. The agent doesn't need to know this skill exists to obey the paper.

### The checker — what it actually catches

`scripts/check-design.py` is ~120 lines, stdlib only, no Node, no deps. It reads
the token block from `DESIGN.md` and greps the source tree for values that aren't
in it:

| Check | Catches |
|---|---|
| `hex-outside-palette` | Any `#RRGGBB` in CSS/TSX not declared in §2 |
| `radius-outside-scale` | `border-radius` values not in §6 |
| `spacing-outside-scale` | padding/margin/gap values not in §4 |
| `font-outside-paper` | `font-family` declarations not in §3 |
| `gradient-text` | `background-clip: text` — a ban, not a default |
| `emoji-ui` | Emoji inside JSX/HTML attribute or text nodes |
| `motion-ungated` | `@keyframes` or `animation:` with no `prefers-reduced-motion` in the file set |

Exit code 1 on findings, 0 on clean. `--json` for tooling.

**It is deliberately narrow.** It checks what is *mechanically* checkable and
stays silent about taste. A checker that cries wolf gets disabled in a week.

### When the project has no paper

The guardrail still works — it just operates on *nothing*. Say so explicitly:

> No `DESIGN.md`. The guardrail has no contract to enforce. Run
> `do-design-new` or `do-design-review` to create one, or I can draft it from
> the existing code (retrofit mode, ~15 min).

Never invent a paper so the checker passes. That is the failure mode this whole
skill exists to prevent.

---

## §Non-negotiables

1. **Never break working code.** Props, state, routing, handlers, a11y survive.
   Copy keeps its meaning.
2. **The brief wins.** A stated brand, font or colour outranks your taste — even
   when it asks for something on the ban list. Write it into the paper rather
   than arguing.
3. **Never invent facts.** You may cut a vague claim; you may not replace it with
   a specific one you made up. Mark the gap.
4. **Load lazily.** Loading all layers when the task needs one is a failure of
   the method, not thoroughness.
5. **A clean result is a valid result.** Do not manufacture findings.
6. **Fix, never accuse.** Never tell a client "this looks AI-generated". Report
   what is unchosen and what to do instead.

---

## §Files

```
SKILL.md              ← you are here (L0, always loaded)
commands/             ← the five playbooks
layers/               ← L1 fundamentals, ~1k tokens each
references/           ← L2 depth, loaded on demand
templates/DESIGN.md   ← the paper template
scripts/              ← guardrail installer + checker
examples/             ← two filled papers that disagree
```

| Layer file | Covers |
|---|---|
| `layers/00-craft-floor.md` | The absolute floor — the checks that must pass in every mode |
| `layers/01-color.md` | Roles, ramps, accent budget, contrast, dark mode |
| `layers/02-typography.md` | Faces, scale, measure, figures, the CSS pass |
| `layers/03-space-layout.md` | Scale, density, grid, containers, responsive |
| `layers/04-motion-states.md` | Durations, easing, entrance, loading/empty/error |
| `layers/05-voice.md` | Tone, headlines, labels, banned words, copy tests |
| `layers/06-research.md` | Market/world research protocol (required for `do-crazy`) |

---

## §Token discipline

This skill is designed to be cheap. Numbers, measured on this file set:

| State | Loaded | ~Tokens |
|---|---|---|
| Idle (subscribed, not invoked) | description only | ~90 |
| `do-design-review` | L0 + command + paper | ~3.8k |
| `do-crazy` | + research layer + craft floor | ~6.5k |
| `do-design-new` | + command + 4 layers | ~7.9k |
| `do-audit` | + all layers + rubric | ~15.3k |

Measured, not estimated (`wc -c / 4`). All seven layers together are ~6.7k — the
reason `do-audit` is the only command that loads them all.

Never load all five command files. Never load `references/` unless a command
names the file it needs.
