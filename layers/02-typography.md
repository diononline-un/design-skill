# L1 · Typography

## The model

- **Two families maximum.** One for interface/body, at most one partner (display
  or mono). A third needs a stated job.
- **Fixed scale**, 5–7 steps, named by role not by pixel value.
  A 1.2–1.333 ratio is the conventional range.
- **Weights 400 and 500 as the working pair**, 600 for rare emphasis.
  700+ headings are a decision to defend, not a default.
- **Hierarchy from size and colour first**, weight second. A page whose only
  hierarchy is weight looks shouty and undifferentiated.
- **Measure 60–75 characters**, target ~65. Line height 1.5–1.7 body,
  1.0–1.2 display.
- **Sentence case** as default. Title Case and tracked ALL-CAPS are decisions.
- **Self-host the files.** No third-party font requests — privacy, speed, and
  you own the asset.

## Choosing the face

The face is a **positioning argument**, not a taste.

| Character | Faces tend toward |
|---|---|
| Industrial, direct, loud | heavy condensed grotesk |
| Considered, editorial, expensive | light serif |
| Technical, precise | neutral grotesk + mono |
| Friendly, soft, generic | rounded geometric — careful: this is the friendly *default* |
| Craft, human, made | humanist sans or a workhorse serif |

A quiet serif on a page claiming hard practical work is a contradiction the
visitor feels without being able to name it.

**Faces that read as "the tasteful free font set"** — fine when earned, but never
because it's what the last three projects used: Space Grotesk, Geist, Syne, Sora,
Instrument Serif, Fraunces, Cal Sans, Plus Jakarta. **Inter as the only face** is
a default, not a decision — state the reason if you keep it (e.g. "largest
x-height at 12–13 px, where 80 % of this UI lives").

## The CSS pass — defects that are individually invisible

Each is one line. Together they are the difference between *designed* and
*generated*. Check them all in one pass through the stylesheet.

**Vertical metrics**

1. **Reserve bold width** where text changes weight (active nav, toggle) — else
   the row shifts.
   ```css
   .tab::after { content: attr(data-label); font-weight: 700; height: 0;
                 visibility: hidden; display: block; overflow: hidden; }
   ```
2. **Descenders make centred text sit high** — centre glyphs, not the line box.
   ```css
   .label { text-box: trim-both cap alphabetic; text-box-trim: trim-both; }
   ```
3. **`sub`/`sup` inflate the line box** and make every row a different height.
   ```css
   sub, sup { line-height: 0; }
   ```

**Underlines and quotes**

4. Default underlines get chopped by `g`, `y`, `p`.
   ```css
   a { text-decoration-thickness: 1px; text-underline-offset: .18em; }
   ```
5. **Curly quotes**, and `’` for apostrophes: `“ ” ‘ ’`. Straight quotes read as
   a typewriter.
6. **Real `small-caps`**, never uppercase + `font-size: .8em` — that thins the
   strokes and breaks the cap-height relationship.
   ```css
   .acronym { font-variant-caps: small-caps; }
   ```

**Overflow**

7. **Truncate filenames in the middle**, not the end — end-truncation eats the
   extension. Needs the head/tail split in markup.
8. **`hyphens: auto`** on narrow columns — and set the right `lang` on `<html>`,
   or it hyphenates with the wrong dictionary and breaks *worse* than none.
9. **`line-clamp` on card titles**, not whole cards, or a long title makes one
   card taller and the row goes ragged.

**Responsive type**

10. **`clamp()` with a mixed middle value.** `clamp(2rem, 5vw + 1rem, 4.5rem)` —
    pure `vw` collapses to the floor on phones and jumps to the ceiling on laptops.
11. **`text-wrap: balance`** on headings, `pretty` on paragraphs.
12. **`tabular-nums`** wherever figures are compared or change; one number format
    product-wide.

## Quick audit strings

```bash
grep -rn "text-decoration:\s*underline\|text-underline-offset" src/
grep -rn "background-clip:\s*text\|-webkit-background-clip" src/   # BAN
grep -rn "font-variant-caps\|small-caps" src/
grep -rn "hyphens" src/  && grep -o 'lang="[^"]*"' index.html
grep -rn "line-clamp\|clamp(" src/ | head
grep -rn "tabular-nums\|font-variant-numeric" src/
```
