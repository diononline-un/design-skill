# do-design-renew

**Job:** deliberately replace an existing look while keeping product truth.
For repositioning, a stale brand, or a surface that never worked.

**Loads:** `layers/00-craft-floor.md` + `layers/06-research.md` + mode layer +
the existing paper.

**The difference from `do-design-new`:** there is an incumbent. It is *evidence
about what doesn't work*, never a foundation to build on.

---

## 1. What must survive

Before anything else, list what is **not** up for change. Get this wrong and you
will rebuild something the client already rejected for a reason.

| Stays | Usually |
|---|---|
| Product truth | what it does, features, pricing logic |
| Content | real copy meaning, real numbers, real testimonials |
| Function | flows, states, required fields |
| Native affordances | nav position, cart, checkout, login — convention |
| Constraints | legal text, accessibility, embedded third-party widgets |

Write it down:

```
Survives: product claims, the price table structure, the contact form fields,
the nav items, all legal copy.
Replaced: the visual world — palette, type, imagery, composition, motion.
```

## 2. Audit the incumbent as anti-reference

Run the `do-audit` scoring on the current design. Then, crucially, **state what
the incumbent got right** — you're replacing a look, not a product, and
occasionally something was working.

```
What doesn't work: the palette (four blues, no accent), the hero (centred stack,
no protagonist), typography (Inter everywhere, flat scale).
What does work: the number-led proof section — that's the strongest thing on the
site and survives into the new direction as a *pattern*.
```

## 3. Research — required, not optional

Run `layers/06-research.md` in full. A renewal without research produces the
*next tasteful default*, and you'll renew again in two years.

Pay particular attention to **step 3** (category conventions). A renewal is
almost always either "fit the category properly" or "depart decisively" — and the
client usually wants one without saying which.

## 4. Choose the replacement world — and stop

Write the five direction lines, then add the two renewal-specific lines:

```
Product:    <unchanged, from step 1>
Character:  <new, 2–3 concrete words>
World:      <the material world the new design belongs to>
Moments:    <1–2 rich places>
Signature:  <one detail>

From the incumbent, keep:   <the thing that worked>
From the incumbent, kill:   <the thing that defined the old world>
Risk:       <what the audience might misread>
```

**Show this and wait.** A renewal is the single most expensive thing to get
wrong, because the client will have approved it visually before you write a line.

## 5. Replace, don't polish

**The failure mode of renewal is a half-measure.** You soften the violet to slate,
keep the layout, and produce the template again in a different colour. This is a
lateral move, not a renewal.

Rules:

- **The old look gets zero credit.** Don't keep a component because it "already
  works" unless it's on the survival list.
- **One dominant move.** The new world needs one thing the old could never do —
  a composition, a material, a structural idea. Not five small improvements.
- **Replace the paper, don't append.** Write `DESIGN.md` v2.0 as a new document
  with a new §1, not a diff of the old one. Archive v1.0 in `docs/archive/`.
- **Never split the difference.** If you're keeping half the old palette "for
  recognition", you haven't decided.

## 6. Build

Same seven passes as `do-design-new` §5: hierarchy → layout → colour → type →
surface → states → motion.

Renewal-specific: **build the hero twice.** Once conservative, once at full
commitment to the new world. Show both. The conservative one is usually what the
client *says* they want; the committed one is what they hired you for. Seeing them
side by side makes the choice real.

## 7. Migration

A renewal that ships half-migrated is worse than either state.

- List every surface that carries the old world.
- Order them by traffic / importance.
- Ship the highest-traffic surface complete, not all surfaces partially.
- The paper's v2.0 §10 precedent should name the first migrated surface as the ✅
  example, so later work has a reference.

## 8. Report

```
Mode: Persuade
Survives: <list>   Replaced: <list>
Direction: <five lines + kept/killed/risk>
Paper: v1.0 → v2.0 (v1.0 archived)
Built: <files>
Score before → after: 47 → 78
Migrated: <surface> — remaining: <list>
```

## Common failures

- **Polishing the old world.** New colours on the old composition is not a renewal.
- **Losing product truth.** The new hero claims something the product doesn't do.
- **Skipping the research** because "we already know what we want". Then producing
  cream-and-terracotta, the current tasteful default.
- **Showing one option.** Two options make the decision real; one option invites
  "make it a bit like the old one".
- **No migration plan.** Half the site in the new world, half in the old, for
  months.
