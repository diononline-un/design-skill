# L2 · Slop catalog

Vocabulary for defaults that arrive uninvited: name the tell, then say what to do
instead. A tell is evidence of a default nobody chose, not proof a model wrote it, and
not automatically wrong.

## Rules

- **Scripts first.** These IDs are detected by `audit.py scan` and arrive with their fix,
  so do not re-check them by reading: C1 C2 C3 C5 S2 S3 S4 S8 K1 K3 K4 K5 K7 I1 I2 I3 I4
  M2-M10 T1 T2 T3 T6 T8 L3 L4 F1 A2-A4 B1 SD1-SD3 SD6. `audit.py copy` covers W1-W22 and
  T7; `render-audit.py` covers contrast, overflow, overlap and focus; `check-design.py`
  covers drift from a declared paper (the strongest form of L10).
- **Density, not presence.** Act on 3+ distinct P0/P1 tells; below that, report P0s only.
  Never flag in isolation: rounded corners, cards, Inter, gradients, glass, bento grids,
  aurora backgrounds. Designers shipped all of them before LLMs.
- **Declare the brand first.** Once the paper names a palette and faces, a legitimately
  violet brand is no longer told its violet is slop; the question becomes "is this off
  the decision we made?" The scan skips palette and face tells when a token block exists.
- **Fix, never accuse.** Repo signals (CLAUDE.md, AGENTS.md, co-author trailers) prove
  tooling, not bad design: an audit note at most, never an accusation.

## Tells that need eyes

| ID | Tell | Sev | Fix |
|---|---|---|---|
| L1 | pill badge, centred H1, centred sub, two CTAs | P0 | left-align, or let type carry the hero |
| L2 | three identical icon-topped feature cards | P0 | rank them: alternating rows, one showcase, or prose |
| W25 | swap test fails on hero or section heads | P0 | rewrite from what is true here |
| L5 | cookie-cutter section order (5+ of the 8 stock sections) | P1 | order by what the reader needs to decide |
| L7 | bento grid where tile size encodes nothing | P1 | only when size means importance |
| L8 | oversized hero pushing content below the fold | P1 | let content start above the fold |
| L9 | default 4-column footer + newsletter + socials | P1 | build from what the site has |
| S1 | `rounded-2xl` + shadow on every surface | P1 | vary radius and elevation by role |
| T4 | one accented word in the headline (colour, italic, weight) | P1 | emphasis through the type system |
| K2 | an icon in a tinted rounded square per feature | P1 | make it a decision or drop the chips |
| I5 | thin-line outline icons, one stroke, generic mapping | P1 | choose weight and mapping deliberately |
| I6 | stock "diverse team at a laptop" | P1 | real product or work imagery |
| I7 | glossy 3D blobs, iridescent abstract hero art | P1 | show the product |
| C7 | dark mode nobody asked for | P1 | pick light or dark from the use scene |
| C8 | timid palette spread evenly | P1 | 60/30/10 discipline |
| W23 | an arrow welded to every link | P1 | name the action and its object |
| SD0 | a direction you already shipped in your last projects | P1 | your own last three passes are a style menu too |
| C4 | coloured glow shadow | P2 | shadow means elevation; keep it neutral |
| C6 | one hue pretending to be two (<20° apart, different jobs) | P2 | give the second colour a different job or drop it |
| T5 | one family, one weight, flat scale (see scan inventory) | P2 | a real type scale |
| S5 | off-scale spacing (scan inventory `off_4px_grid`) | P2 | one scale |
| S6 | uniform padding and gap, no rhythm | P2 | soft signal: never lead with it |
| S7 | cards inside cards | P2 | one level of containment |
| L6 | one container width everywhere | P2 | vary the measure by section role |
| K6 | status chips with no real state behind them | P2 | chips only for changing state |
| I8 | full-page grain overlay | P2 | texture needs a reason |
| M1 | the same fade-up on every section | P2 | one or two staggered moments |
| W24 | tricolon slogan | P2 | one concrete claim |
| SD4 | template chrome: mono micro-labels, `A · B · C`, `WORD - fragment` | P2 | drop the chrome |
| SD5 | broadsheet cosplay on a non-publication | P2 | type from the subject |

## Caveats found in practice

- `:focus-visible` in a global stylesheet counts; the scan is project-wide for that reason.
- Source reading is not enough: overlap, clipping, sideways scroll and painted contrast
  only show in the render. A page clean by every rule here can still stack text at 420px.
- Font names are not verdicts: a brand that owns Inter declares it in the paper, and the
  question becomes "does it fit?" instead of "is it Inter?".
