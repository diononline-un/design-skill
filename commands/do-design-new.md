# do-design-new

Design something new: conventional, competent, on-paper. The safe path. Use `do-crazy`
when the brief asks for off-distribution work, `do-design-renew` when a look exists and
is being replaced.

1. **Mode, one line.** Operate/Read: follow convention, win on precision. Persuade/
   Experience: the direction gets full commitment.
2. **Paper?** Yes: read `DESIGN.md` §1-§9; it fixes palette, scale, radii, motion and
   voice; do not re-derive them. No: ask which, (a) write the paper first (worth it when
   more than one screen is coming; template + `references/interview.md`) or (b) proceed
   on stated assumptions, listed in the report as a known gap.
3. **Thin brief?** If the input is little more than a name, a logo or "make it new", run
   `layers/06-research.md` before asking anything. Defaults are what a thin brief
   produces without research.
4. **Ask only what you cannot read or research**: batched, at most five, each with its
   consequence (patterns in `references/interview.md`). Ask to confirm an inference
   rather than to collect a fact: "The code uses copper as a single signal with a serif.
   That reads as craft and heritage. Is that the business, or a leftover?"
5. **Direction, five lines** (SKILL.md), then stop and wait.
6. **Build in passes**, each across the whole surface before the next, because each
   decides what the next should be:
   1. Hierarchy: decides what exists; can delete whole sections.
   2. Layout: arrange for balance; check it at 390 before 1440.
   3. Colour: the structure is stable, now the palette applies.
   4. Type: copy length decides sizes; after layout, before detail.
   5. Surface: radii, borders, elevation, the craft floor.
   6. States: hover, focus, loading, empty, error.
   7. Motion: last; the screen must work without it.
   Starting at pass 5 produces beautiful radii on a page with no idea.
7. **Before showing**: `check-design.py` (paper), `audit.py copy` (gap markers, tells),
   `render-audit.py` (overflow, contrast at 390), the swap test, and the squint test
   (exactly one thing leads).
8. **Report**
```
Mode: Persuade
Direction: <five lines, compact>
Paper: DESIGN.md v1.0 read | no paper (declared gap)
Evidence: <research file or "none, brief was sufficient">
Built: <files> - <one line per pass>
Checks: drift 0 · render P0/P1 0 · open gap markers 2
Score: 78/100 Sound - H4 L4 S3 C3 T3 U4 D2
Open: <assets, numbers, decisions only the client has>
```

Failures to avoid: polishing an undecided page; ten open questions instead of three
with consequences; all seven passes at once; filling an empty region because it is
empty; inventing a number to make a section work.
