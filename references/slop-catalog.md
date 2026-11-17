# The unslop catalog — 45 machine-detectable tells

Vendored from **SalvatoreCampagnese/unslop-skill** (MIT, see `scripts/UNSLOP-LICENSE`). Reproduced here because it is the only source in this skill with **deterministic, runnable detection** — findings are located (file:line) rather than vibes.

**The authoritative doc is the repo.** This file is a working summary; the scanners in `scripts/` are the real implementation.

## How to run the scanners

```bash
SK=~/.hermes/skills/creative/ui-design-polish

# frontend source (HTML/CSS/React/Vue/Svelte/Astro/Tailwind/shadcn)
node $SK/scripts/detect-ui.mjs <paths...>

# prose (Markdown/HTML/text, EN + IT)
node $SK/scripts/detect-text.mjs <paths...>

# what actually got painted — headless Chrome at 1280/768/420
node $SK/scripts/audit-render.mjs <page> --widths=1280,768,420
```

Flags: `--json`, `--min=P1`, `--max-score=N`, `--strict`, `--rules`, `--init-config`, `--record=<project>`, `--no-config`.

**Write the config (`unslop.palette.json` + `unslop.style.json`) before trusting the score.** Declared brand colours silence the generic-violet rules and invert `X1` to report *drift from your own palette*. Without a config, a legitimately violet brand gets told its violet is slop.

## Score bands

| Score | Meaning |
|---|---|
| 0–9 | clean |
| 10–24 | traces — look, don't rewrite |
| 25–49 | slop-leaning — a real pass is justified |
| 50+ | rebuild the direction |

## The rule that governs it

> **A tell is evidence of a default nobody chose. It is not proof a model wrote it, and not automatically wrong.**

Fix, never accuse. Never report "this is AI-generated" to a client. **Density, not presence**: one gradient is not slop, one em dash is not slop — act on clusters. Below ~3 co-occurring P0/P1 tells, report nothing.

**Do not flag in isolation:** rounded corners, cards, Inter, gradients, glassmorphism, bento grids, aurora backgrounds. Designers shipped all of these before LLMs. Restraint executed well is a decision, not timidity.

## Colour

| ID | Tell | Sev | Fix |
|---|---|---|---|
| C1 | Purple/indigo→violet gradient | **P0** | Tonal gradient inside one brand hue, or flat ground |
| C2 | Violet primary action | P1 | Tie primary to brand; add real states |
| C3 | Gradient clipped into headline text | **P0** | Solid ink; let scale carry emphasis |
| C4 | Coloured glow shadow | P2 | Shadow means elevation; keep neutral |
| C5 | Aurora / blurred gradient blobs | P1 | Earn the space with content |
| C6 | One hue pretending to be two (<20° apart) | P2 | Give the second colour a different job |
| A1 | Muted text below 4.5:1 | P1 | Raise until it clears AA |
| C7 | Dark mode nobody asked for | P1 | Pick light or dark on purpose |
| C8 | Timid palette, evenly distributed | P1 | 60/30/10 discipline |
| C9 | Low-contrast dark mode (grey on grey) | P1 | Real dark palette at AA |

## Typography

| ID | Tell | Sev | Fix |
|---|---|---|---|
| T1 | Inter / Roboto / Arial / `system-ui` as the only face | **P0** | Choose faces for the brief; separate display and body |
| T2 | The "tasteful free font" set: **Space Grotesk, Geist, Syne, Sora, Instrument Serif, Fraunces, Cal Sans, Plus Jakarta** | P1 | Keep only if earned. Never the face your last three projects used |
| T3 | Tracked all-caps eyebrow above every heading | P1 | Keep only if it carries information |
| T4 | One accented word in the headline (colour, italic, weight) | P1 | Emphasis through the type system |
| T5 | One family, one weight, flat scale | P2 | A real type scale |
| T6 | Face declared but never shipped | P1 | Ship the files |
| T7 | Title Case everywhere | P2 | Sentence case |

## Shape and surface

| ID | Tell | Sev | Fix |
|---|---|---|---|
| S1 | `rounded-2xl` + shadow on every surface | P1 | Vary radius and elevation by role |
| S2 | shadcn `--radius` left at 0.5/0.625rem | P1 | A radius that says something |
| S3 | Coloured 3–4px accent stripe on cards | P1 | Drop it; rank with weight, scale, position |
| S4 | `backdrop-blur` by reflex | P1 | Blur only where content really passes under |
| S5 | Off-scale spacing (24/28/32 with no system) | P2 | 4-8-16-24-32-48-64 |
| S6 | Uniform padding and gap, no rhythm | P2 | Soft signal — don't lead with it |
| S7 | Cards inside cards | P2 | One level of containment |

## Layout

| ID | Tell | Sev | Fix |
|---|---|---|---|
| L1 | Pill badge → centered H1 → centered sub → two CTAs | **P0** | Left-align, or let type carry the hero |
| L2 | Three identical icon-topped feature cards | **P0** | Rank them: alternating rows, one showcase, or prose |
| L3 | Round-number stat strip | P1 | Real numbers or cut the strip |
| L4 | Decorative `01 / 02 / 03` | P1 | Number only real sequences |
| L5 | Cookie-cutter section order (5+ of 8 stock sections) | P1 | Order by what the reader needs to *decide* |
| L6 | One container width everywhere | P2 | Vary measure by section role |
| L7 | Bento grid where tile size encodes nothing | P1 | Only when size means importance |
| L8 | Oversized hero pushing content below the fold | P1 | Let content start above the fold |
| L9 | Default 4-column footer + newsletter + socials | P1 | Build from what the site has |
| L10 | Design-system drift across pages | **P0** | Lock a `DESIGN.md` contract |

## Components

| ID | Tell | Sev | Fix |
|---|---|---|---|
| K1 | Untouched shadcn base (zinc/slate/neutral, stock tokens) | **P0** | Theme base colour, radius, button, card |
| K2 | Icon in a tinted rounded square, one per feature | P1 | Make it a decision or drop the chips |
| K3 | No `:focus-visible` / no interaction states | P1 | hover, focus-visible, active, disabled |
| K4 | Stock effect-library components (Spotlight, BackgroundBeams, ShimmerButton, NumberTicker, Meteors, BorderBeam) | P1 | One effect that belongs here, or none |
| K5 | Three pricing tiers with a "Most Popular" ring | P1 | Structure follows the real offer |
| K6 | Status chips with no real state behind them | P2 | Chips only for changing state |
| K7 | Fake window chrome as hero visual | P2 | A real screenshot |

## Icons and imagery

| ID | Tell | Sev | Fix |
|---|---|---|---|
| I1 | ✨ Sparkles as the AI glyph | P1 | NN/g tested it: nobody reads "AI" from sparkles. Use words |
| I2 | The worn Lucide set (Zap, Rocket, Shield, BarChart3, ArrowRight, CheckCircle2) | P1 | Icons for meaning, not availability |
| I3 | Emoji as interface icons | P1 | A real set, or nothing |
| I4 | Placeholder identities (dicebear, pravatar, picsum, grey `aspect-video`) | P1 | Real avatars and screenshots, or remove the slot |
| I5 | Thin-line outline set, one stroke weight, generic mapping | P1 | Choose weight and mapping deliberately |
| I6 | Stock "diverse team at a laptop" | P1 | Real product imagery |
| I7 | Glossy 3D blobs / iridescent abstract hero art | P1 | Show the product |
| I8 | Full-page grain overlay | P2 | Texture needs a reason |

## Motion

| ID | Tell | Sev | Fix |
|---|---|---|---|
| M1 | Same fade-up on every section | P2 | One or two staggered moments |
| M2 | Animation with no `prefers-reduced-motion` | P1 | Gate it. A defect, not taste |
| M3 | Bounce / elastic easing | P2 | Ease out without overshoot, 150–250ms |
| M4 | Count-up stat animation | P2 | Show the real number |
| M5 | Cursor-following hero glow | P2 | Cut it |
| M6 | Hover lift on every card; buttons that just fade | P2 | One shared motion language |

## Microcopy

| ID | Tell | Sev | Fix |
|---|---|---|---|
| P1 | Vague aspirational headline ("Elevate your…", "The all-in-one platform for…") | P1 | What it does, for whom, what changes |
| P2 | Generic superlatives (seamless, powerful, robust, cutting-edge) | P2 | A number, a verb, or a disputable claim |
| P3 | Arrow welded to every link | P1 | Name the action and its object |
| P4 | Tricolon slogan | P2 | One concrete claim |
| P5 | Generic CTA labels | P2 | Verb + object, consistent across the page |
| P6 | **Swap test**: paste the copy on a competitor's site. Nothing breaks → it says nothing | **P0** | Rewrite from what is actually true here |

## Second-order defaults — the most important section

**The anti-slop advice became training data. "Tasteful" is now its own template.** This is the trap that catches anyone who reads a de-slop list and applies it.

| ID | Tell | Sev |
|---|---|---|
| SD0 | A direction you already shipped (hue within 14° of a recorded run) | P1 |
| SD1 | Cream ground `#F4F1EA` + terracotta `#D97757` + serif | P1 |
| SD2 | Near-black ground + one acid-green or vermilion accent | P1 |
| SD3 | Emerald/teal as the purple-avoiding accent | P2 |
| SD4 | Template chrome bundle: mono micro-labels + `A · B · C` + `WORD — fragment` | P2 |
| SD5 | Broadsheet cosplay on a non-publication | P2 |
| SD6 | Orange accent + serif, the 2026 "I avoided purple" signature | P2 |

Record every direction with `--record=<project>`; `SD0` fires when a new pass lands within 14° of hue of one you already shipped. **Your own last three passes are a style menu too.**

## Drift and fingerprints

| ID | Tell | Sev |
|---|---|---|
| X1 | Colour off the declared palette (only with config) | P2 |
| X2 | Radius off the declared scale (only with config) | P2 |
| F1 | Builder signature shipped (`lovable-tagger`, `v0.dev`, `bolt.new`, `<meta generator>`) | P1 |

Repo-level signals (`CLAUDE.md`, `AGENTS.md`, `claude/*` branches, co-author trailers) prove **tooling**, not bad design. Audit note only — never in the rewrite, never as an accusation.

## The six non-negotiables (from the original skill)

1. **Never break working code.** Props, state, routing, handlers, a11y survive intact.
2. **The brief wins, and the brief is a file.** A stated brand outranks taste — write it into the config rather than arguing with findings one at a time.
3. **Never invent facts.** You may cut a vague claim; you may not replace it with a specific one you made up. Leave a marked gap.
4. **Keep the author's voice.** The failure mode of a prose unslopper is replacing a voice with a different default.
5. **Density, not presence.** Act on clusters.
6. **A clean audit is a valid result.** Do not manufacture findings.

## Caveats found in practice

- **K3 false-positives** when `:focus-visible` lives in a global stylesheet rather than the component. Verify by grepping `globals.css` before reporting it.
- The scanners read **source**, so `audit-render.mjs` (headless Chrome) is the only way to catch overlap, clipping, sideways scroll and painted-contrast failures — a page can score 0 and still ship text stacked on itself at 420px.
- `T1`/`T2` fire on font *names* — a brand that legitimately owns Inter must declare it in `unslop.style.json` or it will be flagged forever.
