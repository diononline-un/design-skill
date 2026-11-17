# do-design-new

**Job:** design something new. Conventional, competent, on-paper. The safe path.

**Loads:** mode layer + only the L1 layers the task touches (usually
`00-craft-floor` + `01-color` + `02-typography`, plus others as named).

**Use `do-crazy` instead if** the brief asks for something off-distribution.
**Use `do-design-renew` if** a look already exists and is being replaced.

---

## 1. State the mode (one line)

> **Mode: Persuade** — a landing page for a PV installer. Convention may be
> departed; the hero is the axis the visitor judges.

Mode decides the rest. Operate/Read → follow the paper's conventions and win on
precision. Persuade/Experience → the paper's direction gets full commitment.

## 2. Does a paper exist?

**Yes →** read `DESIGN.md` §2–§9. That is your palette, scale, radii, motion and
voice. Do not re-derive what the paper already fixes. Confirm your plan against it
before building.

**No →** two options, ask which:

- **Write the paper first.** Good when more than one screen is coming. Use
  `templates/DESIGN.md`; it takes ~15 min and prevents every later inconsistency.
- **Proceed with the defaults** and note it in the report as a known gap.

## 3. Ask only what you can't infer

Read the codebase and the brief first. Then ask — **batched, max 5, with
consequences, not open questions**:

| Ask | Not this |
|---|---|
| "Fitting the sector buys instant legibility; departing buys attention but costs a beat of confusion. Which does this need?" | "What style do you want?" |
| "Dense and information-rich, or airy?" | "How should it feel?" |
| "Copper reads as craft; blue reads as software. Which is the business?" | "What colour?" |
| "One sentence per section, or paragraphs?" | "How much text?" |

**Never ask what you could have read.** Ask to *confirm* an inference instead:
> "Reading the code: copper as a single signal, serif for headings. That reads as
> craft and heritage. Is that the business, or a leftover?"

## 4. Direction, in five lines — then stop

Exactly the five from `layers/06-research.md` §5:

```
Product:    <what it does, for whom>
Character:  <2–3 concrete words>
World:      <place/material — sets neutral tint, accent, visual>
Moments:    <1–2 places the screen gets rich>
Signature:  <one detail only this product has>
```

**Show the direction and wait.** Changing direction later means redoing
everything. If the user said "just do it", skip the wait and state the assumption
in one line.

## 5. Build in this order

Order matters because each pass changes what the next one should be.

| # | Pass | Why here |
|---|---|---|
| 1 | **Hierarchy** | Decides what exists. Can delete whole sections. |
| 2 | **Layout** | Arrange for balance. Checkpoint: does it feel balanced? |
| 3 | **Colour** | Now that the structure is stable, the palette applies. |
| 4 | **Type** | Copy length decides the size — after layout, before detail. |
| 5 | **Surface** | Radii, borders, elevation, the craft floor. |
| 6 | **States** | Hover, focus, loading, empty, error. |
| 7 | **Motion** | Last — it should fit a screen that works without it. |

Each pass runs across the whole surface before the next starts. **Never do pass 5
before pass 1** — that's how a page ends up with beautiful radii and no idea.

## 6. The honesty checks

Before showing anything:

- **Swap test** — replace the product name with a competitor's. Does anything break?
- **Squint test** — does exactly one thing lead?
- **Real copy at 390px** — not lorem, not the desktop text shrunk.
- **The three numbers** — if the copy claims something, can it be checked?

## 7. Report

```
Mode: Persuade
Direction: <the five lines, compact>
Paper: DESIGN.md v1.0 read / no paper (declared gap)
Built: <files> — <one line per pass>
Score: 78/100 (Sound) — hierarchy 4, legibility 4, system 3, craft 3, content 3, usability 4, distinction 2
Open: <what needs real assets, real numbers, or a decision>
```

## Common failures

- **Skipping pass 1.** The most expensive mistake. Polishing an undecided page.
- **Asking ten open questions** instead of three with consequences.
- **Building all seven passes at once** and losing track of which decision caused
  which problem.
- **Filling an empty region because it's empty.** Space is a decision.
- **Inventing a number** to make a section work. Leave `[number needed]`.
- **Starting at pass 5.** Glass, gradients and animation on a page with no
  hierarchy is impressive-looking confusion.
