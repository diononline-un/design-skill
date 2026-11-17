# do-design

Design work with a **guardrail**: five commands, a lazy-loaded rulebook, a scoring
system, and scripts for everything measurable, so the model spends its context on
judgment instead of on reading CSS, counting contrast ratios or guessing what customers
search for.

Works with any agent that reads `SKILL.md` (Claude Code, Cursor, Codex, Copilot and others).

```bash
git clone <this-repo> ~/.claude/skills/do-design      # Claude Code, user-wide
# or copy the folder into .claude/skills/ · .cursor/skills/ · .agents/skills/
```

Requirements: Python 3.8+ (stdlib only). Chrome, Chromium, Edge or Brave for the render
audit, page profiles and raster logos; everything else runs without a browser.

---

## Commands

| Command | When | Produces |
|---|---|---|
| `do-design-review` | "Does this match the paper?" | ✅ / ⚠️ / ❌ verdict scoped to the diff |
| `do-audit` | "How good is this?" | seven-field score, P0-P3 findings, three-field work list |
| `do-design-new` | "Build X" | conventional, competent, on-paper (research first when the brief is thin) |
| `do-design-renew` | "Redo this" | a new world that keeps product truth |
| `do-crazy` | "Something nobody in this sector does" | off-distribution, after real research |

```
do-design-new    conventional. direction -> confirm -> build                low risk
do-design-renew  replaces a world. audit -> research -> direction -> build  medium
do-crazy         research first, three worlds, client picks, full commit    high, by design
```

## Scripts

| Script | What it does instead of the model |
|---|---|
| `check-design.py` | drift from the paper's token block: hex/rgb/hsl/oklch colours, Tailwind palette classes, radii, spacing (incl. Tailwind arbitrary values and JSX style objects), fonts, gradient text, emoji icons, ungated animation. `--init` drafts a token block from the code with one-off values flagged as likely accidents; `legacy:` tolerates retrofit leftovers (counted, not failed); `skip:` in the paper keeps archives out of every check |
| `audit.py scan` | ~40 source tells (purple gradients, stock effect components, worn icon sets, placeholder avatars, layout-property transitions, missing focus styles, missing alt, disabled zoom, untouched browser surfaces, second-order palette defaults computed in OKLCH) plus a value inventory |
| `audit.py copy` | ~23 prose and microcopy tells (hype words in EN and DE, AI-vocabulary density, negative parallelism, vague attribution, chatbot leftovers, open gap markers, generic CTAs, greetings, Title Case, sentence-rhythm variation) |
| `audit.py contrast` / `score` | WCAG ratios per mode from the paper; the weighted score, band and work list |
| `render-audit.py` | the painted page at 1280/768/390 over the DevTools protocol: sideways scroll with the offending element, text overlap, squeezed and clipped text, contrast against the composited background, tiny text, tap targets, misaligned card rows, heading order, alt, lang, and keyboard focus that changes nothing visible. Measures after a scroll pass with reduced motion, so reveals and count-ups are final; `--inject-css` tests a fix on the deployed page |
| `research.py` | `suggest`: real search phrasing from autocomplete · `profile`: competitor page facts (title, H1/H2, nav, CTAs, schema, phone above the fold, fonts, palette by area, trust signals, load time) · `logo`: logo colours by share with contrast and role hints · `arena`: are.na channels for a subject |
| `install-guardrails.sh` | DESIGN.md from the template, the agent block in AGENTS.md (CLAUDE.md imports it), the checker copied into the project |

Every script prints compact text and takes `--json`. Tests: `python3 tests/test_scripts.py`
(the browser tests skip when no Chrome is found).

## The guardrail

```bash
bash ~/.claude/skills/do-design/scripts/install-guardrails.sh /path/to/project
```

An agent does not need to know this skill exists to obey the paper: the block in
`AGENTS.md`/`CLAUDE.md` is loaded at session start and tells it to use tokens, stop and
ask when one is missing, and run `python3 scripts/check-design.py` after UI changes.
The block is ~170 tokens (half of v1.0) because it is paid in every session of that project.

```
$ python3 scripts/check-design.py
design drift: 2 files scanned against DESIGN.md
P0 (1)  src/bad.css:5  gradient-text  background-clip: text
P1 (4)  src/bad.css:4  hex-outside-palette  #2563EB
        src/bad.tsx:3  tailwind-palette  bg-blue-500
        ...
```

Exit codes: `0` clean · `1` drift · `2` no paper or no filled token block. A paper can
switch a rule off on purpose (`allow: gradient-text`): the brief wins, but in writing.

## Context cost

Measured as characters / 4 for the files each command loads (the project's DESIGN.md
comes on top for review):

| State | v1.0 | now |
|---|---|---|
| idle (description only) | ~110 | ~95 |
| `do-design-review` | 3.8k | 2.5k |
| `do-design-new` (3 layers) | 6.9k | 5.0k |
| `do-design-renew` | 6.2k | 5.4k |
| `do-crazy` | 6.5k | 5.5k |
| `do-audit` (6 layers, rubric, catalog) | 15.2k | 8.8k |

Script output replaces reading source and screenshots: a render audit at three widths
is a few hundred tokens, a single full-page screenshot is more than a thousand.

---

## Why it is built this way

**A guardrail, not a style guide.** Design documents for agents fail three ways: not
read (the agent does not know they exist; fixed by placement in AGENTS.md), read and
ignored ("we prefer restrained accents" is not a rule; fixed by imperative rules with
numbers), read and wrong (two contradictory rules make the agent confidently wrong;
fixed by a checker that makes contradictions visible). One real project had three design
docs, ~4.5k tokens loaded on every task, with five of six core values contradicting each
other. The paper must be small, versioned, single-source and checkable.

**Layered and scripted, because context is finite.** Every token spent on a rule that
does not apply, or on CSS a script could have read, is not spent on the task. The
always-loaded part is a router; depth loads only when a command names it; measurement
runs outside the context.

**Evidence before defaults.** Given "make it new" and a logo, a model reaches for the
look it has seen most and fills gaps with plausible inventions. The research protocol
replaces that with sources: what customers type (autocomplete), who ranks and what their
pages share (profiles), what customers praise and complain about (reviews, forums), and
references read for qualities, never layouts. Every finding has to answer "does it fit
us, and how do we make it ours?"

**Numbers instead of adjectives.** A score makes progress comparable (47 -> 78), turns
the three weakest fields into the work list, and makes uncertainty explicit (`unverified`
scores 0). Seven weighted fields, because thirty make a dashboard nobody reads and the
weights encode an opinion: a usable, undistinctive page beats a distinctive unusable one.

**Three levels of boldness**, because "make it better" means "fix the mess", "this looks
dated" or "surprise me", and running the wrong one wastes the client's trust.

**Narrow checks.** A linter that reports on taste is disabled within a week. The checker
only reports what is mechanically unambiguous; the audit scripts report evidence with a
density rule; judgment stays with the model and the score.

**Known limits.** The checker needs a filled token block. It reads values, not class
names: Tailwind utilities like `rounded-xl` or a custom `text-ink` are invisible to it
(arbitrary values like `rounded-[6px]` and default palette classes are checked). Scores vary by about ±5
between reviewers; the fields and their order matter more than the last digit. Layer
discipline depends on the agent following the router. Autocomplete shows phrasing and
order, not search volume, and leans toward the caller's region; page profiles see
on-page factors only, not backlinks or Google Business data. savee and mobbin need the
user's own login and are skipped otherwise.

**Left out on purpose:** a component library (every project has one), framework-specific
advice (ages badly), a voice generator (voice comes from a person), an LLM-based slop
detector (deterministic beats probabilistic for a checker), Playwright or any npm
dependency (the scripts drive Chrome over the DevTools protocol directly).

---

## Sources and credits

The skill files carry no references; everything is stated directly. Attribution lives here.

| Source | Licence | Contributed |
|---|---|---|
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Apache 2.0 | mode taxonomy (Persuade/Operate/Read/Experience), craft floor structure, lazy-load architecture, guardrail-as-hook pattern, critique rubric and personas |
| [SalvatoreCampagnese/unslop-skill](https://github.com/SalvatoreCampagnese/unslop-skill) | MIT | the tell catalog, "density not presence", brand config over checklist, second-order defaults |
| [heydamir/unslop](https://github.com/heydamir/unslop) | CC BY 4.0 | ordered build passes, real token values, the five-line direction, "quiet chrome, rich content" |
| Wikipedia, *Signs of AI writing* (WikiProject AI Cleanup) | CC BY-SA 4.0 | prose tells, the "restore these" list and the do-not-flag list behind `audit.py copy` |
| Refactoring UI (Wathan, Schoger) | book | hierarchy from weight and colour, spacing scale discipline, empty space |
| The Design of Everyday Things (Norman) | book | affordances, signifiers, feedback, error recovery |
| Don't Make Me Think (Krug) | book | scannability, self-evidence, the ancestor of the swap test |
| Laws of UX (Yablonski) | book/site | Fitts, Hick, Jakob, Doherty (the ~400 ms threshold) |
| Nielsen's 10 usability heuristics (NN/g) | method | the heuristic scoring; NN/g's finding that sparkle icons do not read as "AI" |
| Cowan (2001), revising Miller (1956) | paper | working memory of about four items |
| WCAG 2.x | standard | contrast thresholds and the relative-luminance formula |
| Björn Ottosson, OKLab | published formulas | the OKLCH conversion used in the scripts |
| 20 principles of UX and animation | article | anticipation, follow-through, timing, stagger |
| land-book.com, cosmos.so, are.na, savee.com, mobbin.com | services | reference sources named in the research protocol (are.na via its public API) |
| Google Autocomplete | service | real search phrasing in `research.py suggest` |

Where sources contradicted each other, the skill resolved explicitly rather than
averaging: Inter is a default to justify, not a ban; ornaments are judged in clusters,
never one by one; shadows are a per-project elevation decision recorded in the paper,
not a universal rule. **The paper decides; the skill provides the method.**

---

MIT · see [LICENSE](LICENSE)
