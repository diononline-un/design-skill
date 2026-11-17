# do-audit

**Job:** score an existing UI and rank what to fix. Read-only — audit mode does
not edit unless asked.

**Loads:** all L1 layers + `references/critique-rubric.md` + the project paper if
one exists.

---

## 1. Scope, in one line

State: what surface, what mode (Persuade/Operate/Read/Experience), what you can
actually see. If you can't render it, say so and mark the affected fields
`unverified`.

**Never audit from the prompt alone.** Read the files, open the page, take a
screenshot at 1280 / 768 / 390.

## 2. Score the seven fields

Use the §Scoring table in SKILL.md. For each field, one line of evidence:

```
1. Hierarchy    3/4  — headline leads clearly; the three CTAs below it compete
2. Legibility   4/4  — 16.2:1 body, 72ch measure, real copy at all widths
3. System       2/4  — two radii scales in use (8px controls, 14px cards, 6px chips)
4. Craft        3/4  — card footers misalign when titles wrap to 2 lines
5. Content      2/4  — "seamless digital transformation" and three unsourced numbers
6. Usability    4/4  — task completes; errors recoverable
7. Distinction  1/4  — swap test fails: copy fits any agency unchanged
```

**Weighted total: 47/100 → Failing.** Direction is the problem, not the polish.

## 3. Rank findings P0–P3

| Sev | Means | Count in report |
|---|---|---|
| **P0** | Blocks shipping. Broken, unreadable, or a hard ban | all |
| **P1** | A designer or dev would notice; damages trust | top 5 |
| **P2** | Craft; visible on close reading | top 5 |
| **P3** | Polish; only worth it if everything else is green | list only |

Format: **`[ID] — location — what's wrong — fix`**

```
[P0] src/Hero.tsx:41 — gradient-clipped headline (ban) — solid --ink, emphasis via size
[P1] src/Pricing.tsx:12 — three identical icon-top cards (L2) — rank them, alternate rows
[P1] copy — swap test fails on hero + 3 section heads — rewrite from what's actually true
[P2] src/Card.tsx:8 — inner radius 14 = outer 14 (not concentric) — calc(14px - 4px)
```

## 4. The three-field work list

End with the **three worst fields** and one action each. That is the work. A wall
of 40 findings is not a report, it's anxiety.

> **Fix these three, in this order:**
> 1. **Distinction (1/4)** — rewrite the hero around the one figure the client
>    would rather hide.
> 2. **Content truth (2/4)** — cut or source the three numbers.
> 3. **System (2/4)** — collapse to one radius scale.

## 5. Bands, and what each means for effort

| Score | Say this |
|---|---|
| 85+ | "Ship it. Only P0s below." |
| 70–84 | "Sound. A day's work on the named P1s." |
| 50–69 | "A real pass is justified before this ships." |
| <50 | "Don't polish — the direction is wrong. Rebuild with do-design-renew." |

## Rules

- **Score the render.** A 0 for anything you couldn't verify, marked `unverified`.
- **A clean audit is valid.** Don't manufacture findings to look thorough.
- **Fix, never accuse.** Never write "this looks AI-generated".
- **Density, not presence.** Below ~3 co-occurring P1+ tells, report nothing —
  one gradient is not a finding.
- **K3-style false positives:** `:focus-visible` in a global stylesheet counts.
  Grep before reporting missing focus states.
