# L1 · Typography

## The model

- At most two families: one for interface and body, one partner (display or mono). A
  third needs a stated job.
- A fixed scale of 5-7 steps named by role, ratio 1.2-1.333.
- Weights 400 and 500 as the working pair, 600 for rare emphasis; 700+ headings are a
  decision to defend.
- Hierarchy from size and colour first, weight second: weight-only hierarchy looks shouty.
- Measure 45-75 characters, target ~65. Line height 1.5-1.7 body, 1.0-1.2 display.
- Sentence case by default; Title Case and tracked all-caps are decisions.
- Self-host the files: no third-party font requests (privacy, speed, ownership).

## Choosing the face: a positioning argument, not a taste

| Character | Tends toward |
|---|---|
| industrial, direct, loud | heavy condensed grotesk |
| considered, editorial, expensive | light serif |
| technical, precise | neutral grotesk + mono |
| friendly, soft | rounded geometric (careful: the friendly default) |
| craft, human, made | humanist sans or a workhorse serif |

A quiet serif on a page claiming hard practical work is a contradiction visitors feel
without naming it. The tasteful free set (Space Grotesk, Geist, Syne, Sora, Instrument
Serif, Fraunces, Cal Sans, Plus Jakarta) is fine when earned, never because the last
three projects used it. Inter alone is a default until the paper states a reason
(e.g. "largest x-height at 12-13px, where 80 % of this UI lives").

## The CSS pass: defects invisible one by one

Each is one line; together they separate designed from generated. One pass through the
stylesheet.

1. Reserve bold width where weight changes (active nav, toggles) or the row shifts:
   `.tab::after{content:attr(data-label);font-weight:700;height:0;visibility:hidden;display:block;overflow:hidden}`
2. Descenders make centred labels sit high: `text-box: trim-both cap alphabetic`.
3. `sub, sup { line-height: 0 }` or every row with one gets taller.
4. `a { text-decoration-thickness: 1px; text-underline-offset: .18em }` so g, y, p are not chopped.
5. Curly quotes and apostrophes (“ ” ‘ ’); straight quotes read as a typewriter.
6. Real small caps (`font-variant-caps: small-caps`), never uppercase + smaller size.
7. Truncate filenames in the middle (keep the extension); needs a head/tail split in markup.
8. `hyphens: auto` on narrow columns, with the right `lang` on `<html>`, or it breaks worse than none.
9. `line-clamp` on card titles, not whole cards, or one long title makes the row ragged.
10. `clamp(2rem, 5vw + 1rem, 4.5rem)`: a mixed middle value; pure vw collapses on phones.
11. `text-wrap: balance` on headings, `pretty` on paragraphs.
12. `tabular-nums` wherever figures are compared or change; one number format product-wide.

`audit.py scan` reports which of these surfaces the project never touches.
