# do-design

Design work with a **guardrail**. Five slash commands, a layered rulebook, a
scoring system, and a checker that catches design drift even when nobody invokes
the skill.

Works with Claude Code, Cursor, Codex, Copilot, DeepSeek/Hermes, and any agent
that reads `SKILL.md`.

```bash
npx degit <you>/design-skill .claude/skills/do-design   # Claude Code
# or copy the folder to .cursor/skills/ · .agents/skills/ · ~/.hermes/skills/
```

---

## The problem

Ask three coding agents to style the same app and you get three palettes. Not
because any choice was wrong — because **nobody wrote the decision down**.

The usual fix is a style guide. It fails for two reasons:

1. **Nobody reads it.** An agent doesn't know it exists, and a human forgets.
2. **It grows without bound.** Every project produces a 900-line design doc that
   gets loaded in full on every task and contradicts itself by month three.

`do-design` takes a different route: a **small binding paper**, a **lazy-loading
rulebook**, and **numbers instead of adjectives**.

---

## The five commands

| Command | When | What it produces |
|---|---|---|
| **`do-audit`** | "How good is this?" | Seven-field score, P0–P3 findings, three-field work list |
| **`do-design-new`** | "Build X" | Conventional, competent, on-paper |
| **`do-design-review`** | "Does this match the paper?" | ✅ / ⚠️ / ❌ verdict, ~2.5k tokens |
| **`do-design-renew`** | "Redo this" | Replaces the look, keeps product truth |
| **`do-crazy`** | "Something nobody would expect" | Off-distribution, after real research |

**The three risk levels**, because "bold" and "safe" are not the same request:

```
do-design-new    → conventional. Direction → confirm → build.        low risk
do-design-renew  → replaces a world. Audit → direction → confirm.    medium
do-crazy         → research first, 3 worlds, pick, commit fully.     high, by design
```

`do-crazy` is not "more effects". It's a different *structural world* — and the
test is: **would this look at home next to the competitors you researched?** If
yes, it failed.

---

## The guardrail

This is the part that works without anyone remembering the skill exists.

```bash
./scripts/install-guardrails.sh /path/to/project
```

It writes three things:

1. **`DESIGN.md`** — the binding paper (from `templates/DESIGN.md`)
2. **A block in `AGENTS.md` / `CLAUDE.md`** — the file agents read at session start
3. **`scripts/check-design.py`** — a stdlib-only drift checker

### Why placement beats documentation

An agent doesn't need to know this skill exists to obey the paper. `AGENTS.md` is
loaded automatically at session start, so:

> *Before you change any colour, size, radius, font, shadow or spacing value: find
> the token in `DESIGN.md` §2–§6. Use the token. If the task needs a value the
> paper lacks, **stop and ask**.*

That is the entire mechanism. No invocation, no skill recall, no user memory.

### What the checker catches

```bash
python3 scripts/check-design.py
# design drift — 2 files scanned against DESIGN.md
# P0 (1)  src/bad.css:7  gradient-text        background-clip: text
# P1 (3)  src/bad.css:4  hex-outside-palette  #2563EB
#         src/bad.tsx:1  emoji-ui             🚀
#         src/bad.css    motion-ungated       no prefers-reduced-motion anywhere
# P2 (2)  src/bad.css:2  spacing-outside-scale 13px
```

| Check | Severity |
|---|---|
| `hex-outside-palette` | P1 |
| `radius-outside-scale` | P2 |
| `spacing-outside-scale` | P2 |
| `font-outside-paper` | P1 |
| `gradient-text` | **P0** |
| `emoji-ui` | P1 |
| `motion-ungated` | P1 |

Exit codes: `0` clean · `1` drift · `2` no paper/tokens.

**Deliberately narrow.** It checks what is mechanically checkable and says nothing
about taste. A checker that cries wolf gets disabled within a week.

---

## The scoring system

Seven weighted fields, because "looks good" is not a report.

| # | Field | Question | Weight |
|---|---|---|---|
| 1 | Hierarchy | Can the most important thing be named in 2 s? | 3 |
| 2 | Legibility | Contrast, size, measure, real copy at every width | 3 |
| 3 | System | One palette, scale, radius logic, motion language | 2 |
| 4 | Craft | Alignment, rhythm, states, browser surfaces | 2 |
| 5 | Content truth | Real data, specific copy, no invented claims | 3 |
| 6 | Usability | Task completes; errors recoverable | 3 |
| 7 | Distinction | Could this sit on a competitor unchanged? | 2 |

| Score | Band | Action |
|---|---|---|
| 85–100 | Strong | Ship; fix P0 only |
| 70–84 | Sound | Ship after named P1s |
| 50–69 | Weak | A real pass before shipping |
| <50 | Failing | The direction is wrong — rebuild |

**A field you couldn't verify scores 0 and is marked `unverified`.** Never estimated.

---

## Layered, so it stays cheap

| Layer | Contents | Loaded |
|---|---|---|
| **L0** | `SKILL.md` — router, model, scoring, guardrail | always |
| **L1** | `layers/` — colour, type, space, motion, voice, research | only what the task touches |
| **L2** | `references/` — slop catalog, critique rubric, render audit, interview | only when a command names it |

| State | ~Tokens (measured) |
|---|---|
| Idle (subscribed, not invoked) | 90 |
| `do-design-review` | 3.8k |
| `do-crazy` | 6.5k |
| `do-design-new` | 7.9k |
| `do-audit` | 15.3k |

A task about a button does not load the layout layer. That is the whole point of
the structure — see [RATIONALE.md](RATIONALE.md) for why this matters more than
it sounds.

---

## Four modes

Before any command, state the mode. It decides how hard to push.

| Mode | Visitor is… | Convention is… |
|---|---|---|
| **Persuade** | deciding and acting | a failure |
| **Operate** | completing a task | a feature |
| **Read** | understanding | a requirement |
| **Experience** | inside the work | irrelevant |

Pick by **surface, not product**: a dev tool's landing page is Persuade; its
settings screen is Operate.

---

## Sources

Synthesised from nine sources, de-duplicated, with contradictions resolved
explicitly:

| Source | Contributed |
|---|---|
| **pbakaus/impeccable** (Apache 2.0) | Mode system, craft floor, lazy-load architecture, hook pattern |
| **SalvatoreCampagnese/unslop-skill** (MIT) | 45 machine-checkable tells, density rule, brand-over-checklist |
| **heydamir/unslop** (CC BY 4.0) | Nine ordered passes, tokens with real values, direction five-liner |
| **Refactoring UI** (Wathan/Schoger) | Hierarchy from weight *and* colour contrast, spacing scale discipline |
| **The Design of Everyday Things** (Norman) | Affordances, signifiers, feedback, error recovery |
| **Don't Make Me Think** (Krug) | Scannability, the "self-evident" test, trunk test |
| **Laws of UX** (Yablonski) | Fitts, Hick, Miller, Jakob, Doherty — with thresholds |
| **Nielsen's 10 heuristics** | Usability scoring rubric |
| **20 principles of UX & animation** | Motion: anticipation, follow-through, timing |

Attribution and licence notes per file: [RATIONALE.md §Sources](RATIONALE.md).

---

## Files

```
SKILL.md              L0 router — the only always-loaded file
commands/             five playbooks
layers/               L1 fundamentals (7 files)
references/           L2 depth (loaded on demand)
templates/DESIGN.md   the paper template (copy into a project)
scripts/
  check-design.py     drift checker — stdlib only, no Node
  install-guardrails.sh
examples/             two filled papers that disagree on nearly every value
```

---

## Quick start

```bash
# in your project
./scripts/install-guardrails.sh .
python3 scripts/check-design.py --init     # print the token block
```

Then in your agent:

```
do-design-review the pricing section
do-audit the whole landing page
do-crazy the hero — I want something nobody in this sector does
```

---

MIT · see [LICENSE](LICENSE)
