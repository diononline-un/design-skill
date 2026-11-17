# do-design-review

**Job:** check work against the project's paper. The cheapest command and the one
you'll run most. Designed to cost ~2.5k tokens.

**Loads:** this file + `DESIGN.md`. Nothing else, unless a finding needs depth.

---

## 1. Read the paper

Read `DESIGN.md` §2–§9 before looking at any code. You cannot review against a
contract you haven't read.

**No paper?** Say so in one line and fall back to the craft floor:

> No `DESIGN.md`. Reviewing against general craft only — findings will be generic.
> I can draft the paper from the existing code (retrofit, ~15 min) if you want
> future reviews to be project-specific.

## 2. Check the diff, not the world

If the user changed something, review **what changed** and its immediate
neighbours. Reviewing an entire app because someone edited a button is a token
sink and produces findings nobody asked for.

```bash
git diff --stat          # scope
git diff -- '*.css' '*.tsx' '*.html'
```

## 3. The five checks

Run these in order. Stop at the first one that fails and report — don't continue
to craft findings when the paper was violated structurally.

**1. Token compliance** — does every changed value come from the paper?

| Check | Ask |
|---|---|
| Colour | Is every hex/oklch in §2? Any new tint? |
| Type | Any face, size or weight not in §3? |
| Space | Values on the §4 scale? |
| Radius/shadow | On the §6 scale? Nested correctly? |
| Motion | Durations and easing from §7? |

**2. Contradiction** — does the change argue with the paper's *reason*, not just
its values? A new blue that happens to be in the palette but used as a second
accent still violates §2's "one accent".

**3. Craft floor** — run `layers/00-craft-floor.md` Verify list. Only the items
the change could plausibly affect.

**4. States** — did the change add an interactive element without hover, focus,
disabled, loading, error?

**5. Consistency** — does it match how the same pattern is done elsewhere?

## 4. The verdict format

Three outcomes only. Never a vague "looks good".

### ✅ Compliant — no action

```
Compliant. All values from the paper (v1.0). No new tokens, states complete.
```

### ⚠️ Compliant with drift — fix or explain

```
Drift, 2 items:
  · src/Button.tsx:14 — `#2563EB` not in §2 (nearest: --signal #1D4E6B)
  · src/Button.tsx:22 — radius 6px, scale has 4/8 (nearest: 4px)

Both are one-line fixes. Want me to apply them?
```

### ❌ Contradicts the paper — stop and ask

```
This contradicts DESIGN.md v1.0 §2 ("one accent per product"):
  · adds a second accent (--warning used as brand colour on three CTAs)

Two ways forward:
  1. Use --signal for these CTAs; keep --warning semantic-only  ← paper stays intact
  2. Amend §2 to allow a second accent, and say what its job is  ← paper changes

Which? I won't pick silently — this changes the system, not just the file.
```

## 5. When the paper is wrong

Sometimes the code is right and the paper is stale. Say so:

```
The code uses 10px radius on inputs; the paper says 8px. The 10px is better here
(larger touch targets). The paper is stale, not the code.
Proposal: amend §6 to control 10 / card 14. Confirm and I'll update both.
```

**Never silently update the paper to match the code.** That's how a paper becomes
a description of accidents. Amend explicitly, with a version bump.

## Rules

- **Read-only by default.** Report, don't edit, unless asked. A review that
  quietly rewrites things isn't a review.
- **Scope to the diff.** Unless asked for a full audit — that's `do-audit`.
- **Don't manufacture.** Three clean checks is a valid result.
- **Quote the rule and its version.** "§2 of v1.0" — so the user can check.
- **One page max.** This command should be fast or it won't be used.
