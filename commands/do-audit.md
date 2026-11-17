# do-audit

Score an existing UI and rank what to fix. Read-only unless asked.

1. **Scope, one line**: surface, mode, and what you can render. Never audit from the
   prompt alone.
2. **Measure first** (independent, run together):
   - `scripts/audit.py scan P` and `scripts/audit.py copy P`
   - `scripts/check-design.py --root P` when a paper exists
   - `scripts/render-audit.py <url|file>`; add `--shots DIR` only for the fields that
     need eyes (hierarchy, distinction, composition), and look at 390 first.
   No render possible: the fields that depend on it are `u`.
3. **Judge what no script can**: hierarchy, distinction, content truth, usability, the
   judgment-only tells in the slop catalog, and the rubric (cognitive load, heuristics,
   personas, edge probes). Apply the density rule to tells; drift from a paper and P0s
   are always reported.
4. **Score** the seven fields, one line of evidence each, then `audit.py score`.
5. **Findings** P0-P3, script findings under their ID.
6. **Close with the work list**: the three worst fields, one action each, in order.

```
Mode: Persuade · rendered at 1280/768/390
1 Hierarchy    3 - headline leads; the three CTAs below it compete
2 Legibility   4 - render: no contrast or size findings, 68ch measure
3 System       2 - scan inventory: radii 6/8/14, three scales in use
4 Craft        3 - render: row_misaligned on the pricing cards at 768
5 Content      2 - copy: W2 x4 ("seamless"), three unsourced figures
6 Usability    4 - task completes, errors recoverable
7 Distinction  1 - swap test fails: the copy fits any agency
47/100 Failing: the direction is the problem, not the polish.

[P0] src/Hero.tsx:41 - C3 gradient-clipped headline - solid ink, emphasis via size
[P1] src/Features.tsx:12 - three identical icon cards (L2) - rank them, one showcase
[P2] src/Card.tsx:8 - inner radius 14 = outer 14 - calc(14px - 4px)

Fix these three, in order:
1. Distinction (1): rewrite the hero around the one figure the client would rather hide.
2. Content truth (2): source the three numbers or cut them.
3. System (2): one radius scale.
```

False-positive guards: a `:focus-visible` rule in a global stylesheet counts (the scan is
project-wide); a colour or face declared in the paper is a decision, not a tell.
