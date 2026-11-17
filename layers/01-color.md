# L1 · Colour

## Roles: three and one accent

| Role | Job | Share of screen | Never |
|---|---|---|---|
| Ground | the canvas | 60-70 % | carries meaning |
| Ink | text and hairlines, 3-4 derived steps | 25-35 % | decoration |
| Accent | the one thing to act on or believe | ≤5 %, at most two instances | body text, large fills, hover decoration |
| Semantic | success / warning / error only | <2 % | brand |

Anything beyond these needs a written justification in the paper.

## Derive, don't pick

- One neutral ramp, tinted toward the brand's world, saturation very low: a surface
  should never read as a colour of its own.
- Ink steps are derived: primary, secondary (~65 % contrast), muted (~45 %), line
  (primary at 8-12 % alpha), not four hand-picked greys.
- Borders translucent, `rgb(ink / .08-.12)`: a solid hex border is right on exactly one
  background, a translucent one on all.
- The accent is measured twice, as text on the ground and as a fill with text on it;
  both ≥4.5:1 (`audit.py contrast`). A colour can pass one and fail the other.

## Perceptual space

Build and scale ramps in OKLCH, not HSL: `hsl(60 100% 50%)` and `hsl(240 100% 50%)` claim
equal lightness and look nothing alike.

```css
--signal: oklch(0.62 0.19 45);
--signal-hover: oklch(0.56 0.19 45);   /* move L only; the hue stays clean */
```

Fixed L across hues gives equal perceived brightness; C is saturation without a
lightness shift. `linear-gradient(in oklch, …)` removes the grey middle of sRGB
interpolation. Keep a hex fallback for critical brand colours; the token block lists hex.

## Accent discipline

One accent per product unless the paper names a second and its job. On dark themes an
off-white primary button with dark text often reads more deliberate than a coloured one;
the accent then lives only where it matters (selection, the one figure, the discrepancy).

## Dark mode is a second design

Same role names, re-measured values, not an inversion. Depth from surface lightness
(`--surface-0/1/2`, each ~4-6 L lighter), not shadows: black on near-black is invisible.
The accent usually needs less chroma (saturated colour vibrates on near-black); semantic
colours need their own dark values.

## Banned, with reason

| Banned | Why |
|---|---|
| purple-to-blue or violet-to-pink gradient | the most recognisable generated default |
| gradient-clipped text | kills legibility, adds nothing emphasis can't |
| coloured glow shadows | shadow means elevation, not mood |
| aurora / blurred blobs behind content | decoration standing in for an idea |
| glass cards with white inner highlight + coloured shadow | glassmorphism as reflex |
| neon or high-contrast coloured borders | compete with content |
| five near-identical tints of one hue | ten greys pretending to be a system |

## Squint test

Squint: can you still tell what the accent is? If it disappears, its share is too small
to do its job. If everything stays loud, there is no accent, just a lot of colour.
