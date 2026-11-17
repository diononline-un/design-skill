# L1 · Colour

## The model: three roles and one accent

| Role | Job | Share of screen | Never |
|---|---|---|---|
| **Ground** | The canvas | 60–70 % | carries meaning |
| **Ink** | Text and hairlines, in 3–4 derived steps | 25–35 % | used as decoration |
| **Accent** | The one thing to act on or believe | ≤5 % | body text, large fills, decoration |
| **Semantic** | Success / warn / error only | <2 % | used as brand |

Anything beyond these four needs a written justification in the paper.

## Derive, don't pick

- **One neutral ramp**, tinted toward the brand's world. Saturation stays very
  low — a *surface* should never read as a colour on its own.
- **Ink steps are derived**: primary, secondary (≈65 % contrast), muted (≈45 %),
  line (primary at 8–12 % alpha). Not four hand-picked greys.
- **Borders are translucent.** `rgba(ink, .08–.12)`. A solid hex border is correct
  on exactly one background; translucent works on all of them.
- **Accent is measured twice:** as a fill *with text on it*, and as text *on* a
  surface. Both ≥4.5:1. A colour can pass one and fail the other.

## Perceptual space

Build and scale ramps in **OKLCH**, not HSL. HSL lies about brightness:
`hsl(60 100% 50%)` (yellow) and `hsl(240 100% 50%)` (blue) claim identical
lightness and look nothing alike.

```css
--signal: oklch(0.62 0.19 45);          /* L C H */
--signal-hover: oklch(0.56 0.19 45);    /* move L only — hue stays clean */
```

- Fixed `L` across a set of hues → genuinely equal perceived brightness.
- Chroma `C` is the saturation dial that doesn't shift lightness.
- Gradients: `linear-gradient(in oklch, …)` kills the grey middle that sRGB
  interpolation produces between complementary colours.

Keep a hex fallback for critical brand colours — support is good, not universal.

## Accent discipline

- **≤5 % of any screen.** Count the instances: more than two is too many.
- **Never body text**, never a large fill, never a hover decoration.
- **One accent per product** unless the paper names a second and its job.
- On dark themes, an off-white primary button with dark text often reads more
  deliberate than a coloured one — the accent then lives only on the thing that
  matters (selection, the one figure, the discrepancy).

## Dark mode is a second design

- Same **role names**, re-measured **values**. Not an inversion.
- **Depth comes from surface lightness** (`--surface-0/1/2`, each ~4–6 L
  lighter), not from shadows — a black shadow on near-black is invisible.
- Accent usually needs **less** chroma on dark; a saturated colour vibrates
  against near-black.
- Semantic colours need their own dark values; the light-mode green will glow.

## Banned, with reason

| Banned | Why |
|---|---|
| Purple→blue or violet→pink gradient | The single most recognisable generated default |
| Gradient-clipped text | Kills legibility, adds nothing emphasis can't |
| Coloured glow shadows | Shadow means elevation, not mood |
| Aurora / blurred blobs behind content | Decoration standing in for an idea |
| Glass cards with white inner highlight + coloured shadow | Glassmorphism as reflex |
| Neon or high-contrast coloured borders | Compete with content for attention |
| Five near-identical tints of one hue | Ten greys pretending to be a system |

## Test

Squint at the screen. Can you still tell what the accent is? If the accent
disappears when you squint, it's too small a share to be doing its job. If
everything is still visible, there is no accent — there is just a lot of colour.
