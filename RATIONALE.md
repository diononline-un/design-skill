# Rationale

Why this skill is built the way it is. Read this if you're adapting it, or if
you're deciding whether to use it at all.

---

## 1. Why a guardrail instead of a style guide

**The honest problem with design documents for agents:** they are written,
committed, and never read.

Three failure modes, in order of frequency:

| Failure | Mechanism | Fix in this skill |
|---|---|---|
| **Not read** | The agent doesn't know it exists | The rule lives in `AGENTS.md`, loaded at session start |
| **Read, then ignored** | "We prefer restrained accent use" isn't a rule | Imperative phrasing with numbers in it |
| **Read, then wrong** | The doc contradicts itself after three months | A checker, so contradictions become visible |

The third one is the one nobody talks about, and it's the most expensive. A
document with two contradictory rules is worse than no document: the agent picks
one at random and is *confidently* wrong.

**A real example:** a project had three design docs, 17.9 kB total (~4.5k tokens),
loaded on every design task. Five of six core values contradicted each other —
headline size, shadow policy, radius, display face, palette. Thirty per cent of
those tokens actively taught the wrong thing. That's not thoroughness; it's
negative-value documentation.

**Therefore:** the paper must be small, versioned, single-source, and checkable.
Everything else is decoration.

---

## 2. Why the skill is layered

A skill file is a **permanent tax on every session it's loaded in**. If `SKILL.md`
is 900 lines, that cost is paid whether the task is "rename this button" or
"rebuild the whole site".

The alternative is to make the always-loaded part a **router**, and load depth
only when a command asks for it.

| Layer | Loaded when | Cost |
|---|---|---|
| L0 — router | always | ~4k |
| L1 — one layer | the task touches that axis | ~1k |
| L2 — one reference | a command names it | ~2–8k |

**Why this matters more than it sounds:** an agent's context is finite, and every
token spent on a rule that doesn't apply is a token not spent on the actual code.
A skill that costs 30k to load for a 200-line component makes the model worse at
the task it was invoked for.

The counter-argument — "but then it might not know something" — is answered by the
router naming what exists. The agent knows the layout layer is there; it just
doesn't have to carry it.

---

## 3. Why scoring instead of prose review

Prose reviews produce the same report every time: "the hierarchy could be
stronger, the colours are a bit much, the copy is generic." Three paragraphs that
could apply to any page, and no way to tell whether the second pass improved
anything.

**Numbers make three things possible:**

1. **Comparison over time.** 47 → 78 is a defensible claim that the work
   improved. "Much better" is not.
2. **A work list.** The three lowest-weighted fields *are* the next three tasks,
   in order. No prioritisation debate.
3. **Honest uncertainty.** A field you couldn't verify scores 0 and says
   `unverified` — which is information, not a gap.

**Why seven fields and not thirty:** thirty fields produce a dashboard nobody
reads. Seven produces a report you can act on. The weights encode a real opinion
(hierarchy, legibility and content truth matter more than distinction) rather than
pretending all quality is equal.

**Why the fields are weighted:** a beautiful, undistinctive page that works is a
better outcome than a distinctive page nobody can use. The weights say so.

---

## 4. Why three levels of boldness

The single most common design-request failure is **misread ambition**.

A client says "make it better" and means one of three completely different things:

| They mean | They want | Command |
|---|---|---|
| "Fix the mess" | competent and on-brand | `do-design-new` |
| "This looks dated" | a new world, same product | `do-design-renew` |
| "Surprise me" | something nobody in this sector does | `do-crazy` |

Running `do-crazy` on a request that meant "fix the mess" produces something the
client rejects as unserious — and they conclude design can't help. Running
`do-design-new` on "surprise me" produces the template they were trying to escape.

**Naming the three levels makes the misread visible before any work is done.**

`do-crazy` also has a hard precondition — research — because "bold" without
research is just "random". The failure mode of unresearched boldness is that it
lands on the current tasteful default (cream + terracotta, near-black + acid)
with more confidence. That's not off-distribution; it's a different template.

---

## 5. Why "research the world, not the trends"

Design that derives from the subject is distinctive **for free** — because the
subject is specific and the trends are shared.

A PV installer's world contains ridge lines, cadastral maps, shade from a chimney,
DC cable, scaffolding. None of those are in any style guide, and all of them
suggest colour, texture, type and composition that no competitor would arrive at
by copying each other.

**The mechanics:** write 8–12 nouns from the physical world, cross out the ones
that are generic to the industry, keep the specific ones. The survivors are the
material.

The alternative — looking at what's trending — produces convergence by
construction. Everyone reading the same references lands on the same answer, and
that answer becomes the next tell.

**The corollary that's easy to miss:** the anti-slop aesthetic became its own
template. Cream-and-terracotta, near-black-and-acid, mono micro-labels — these
are now defaults in exactly the way the violet gradient was. Escaping one template
into another is a lateral move.

---

## 6. Why the checker is deliberately narrow

A design linter that reports on taste gets disabled within a week.

So `check-design.py` checks **only what is mechanically unambiguous**:

- a hex value that isn't in the palette — unambiguous
- `background-clip: text` — unambiguous (and a hard ban)
- an emoji in a JSX text node — unambiguous
- a radius of 6px when the scale is 0/4/8/12 — unambiguous
- an animation with no `prefers-reduced-motion` anywhere in the project — unambiguous

It says **nothing** about spacing rhythm, hierarchy, copy quality or whether the
composition is any good. Those need judgement, and judgement belongs in the
`do-audit` score, not in a grep.

**Seven checks is the right number.** Enough to catch the drift that actually
happens (a new blue, a stray radius, an unguarded animation); few enough that a
finding is always worth acting on.

**Why stdlib-only Python:** the checker must run in any project, on any machine,
without a build step. Every dependency is a reason not to run it.

---

## 7. What was deliberately left out

| Left out | Why |
|---|---|
| A component library | Every project has one; adding a second is worse than none |
| Framework-specific advice | Ages badly, and the principles don't need it |
| A "brand voice generator" | Voice is the one thing that must come from a person |
| Screenshot-based visual regression | Valuable, but infrastructure, not a skill |
| An LLM-based slop detector | Deterministic beats probabilistic for a checker; see §6 |
| A full audit of every page | Expensive, and rarely what the request needs |

---

## 8. Known limits

- **The checker needs a filled `DESIGN.md`.** On a project without one it exits
  with code 2 and says so. That's correct behaviour, not a bug — but it means the
  guardrail does nothing until step 1 is done.
- **The score is subjective.** Two reviewers will differ by ±5. Its value is in
  the *fields* and the *order*, not the last digit.
- **Layer discipline requires the agent to comply.** A model that loads all seven
  layers "to be safe" defeats the design. `SKILL.md` says not to; nothing enforces
  it.
- **`do-crazy` can fail.** By construction: it's the command with real risk. The
  honesty gate in step 6 catches the failure mode that matters (bold but broken),
  not the one that doesn't (safe but boring — that's `do-design-new`'s job).

---

## Sources and licences

| Source | Licence | What was taken | What was not |
|---|---|---|---|
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Apache 2.0 | Mode taxonomy (Persuade/Operate/Read/Experience), craft floor structure, lazy-load architecture, hook-as-guardrail pattern, critique rubric | The binary launcher, the live/generate tooling, the 62-rule engine (this skill uses 7 checks + judgement instead) |
| [SalvatoreCampagnese/unslop-skill](https://github.com/SalvatoreCampagnese/unslop-skill) | MIT | Tell catalog (condensed into `references/slop-catalog.md`), "density not presence", brand-config-over-checklist, second-order defaults | The Node scanners — replaced by the narrower Python checker |
| [heydamir/unslop](https://github.com/heydamir/unslop) | CC BY 4.0 | Nine ordered passes, real token values (spacing/ramp tables), the direction five-liner, "quiet chrome, rich content" | The story-video renderer, the RTL reference |
| Refactoring UI (Wathan & Schoger) | — | Hierarchy via weight *and* colour, scale discipline, "don't fill empty space" | — |
| The Design of Everyday Things (Norman) | — | Affordances, signifiers, feedback, error recovery | — |
| Don't Make Me Think (Krug) | — | Scannability, self-evidence, the swap test's ancestor | — |
| Laws of UX (Yablonski) | — | Fitts, Hick, Miller, Jakob, Doherty — with the actual thresholds | — |
| Nielsen's 10 heuristics | — | Usability rubric structure | — |
| 20 principles of UX & animation | — | Anticipation, follow-through, timing, stagger | — |

**On synthesising:** where sources contradicted, this skill resolved explicitly
rather than averaging. The main resolutions:

- **Inter as a default vs. a decision.** Unslop flags it as P0; Impeccable's own
  docs use it freely. Resolution: it's a *default*, not a ban — declare the reason
  in the paper if you keep it.
- **"Remove ornaments" vs. "keep personality".** The TikTok/anti-slop sources say
  delete; both GitHub unbundlers say density matters. Resolution: act on
  *clusters*, never on single instances.
- **Shadows: allowed or banned?** Sources disagree. Resolution: it's a per-project
  decision, recorded as one elevation model in the paper (§6). Not a universal rule.

That last one is the most important principle in this skill: **the paper decides,
the skill provides the method.** A skill that picks the answer for every project
becomes the template it was built to prevent.
