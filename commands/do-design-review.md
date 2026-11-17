# do-design-review

Check a change against the paper. The cheapest command and the most used: one page of
output at most, read-only unless asked.

1. **Read the paper** (`DESIGN.md` §2-§9) before any code. No paper: say so in one line,
   review against `layers/00-craft-floor.md` only (findings will be generic), offer a retrofit.
2. **Scope to the diff**: `git diff --stat`, then `git diff -- <UI files>`. Review what
   changed and its direct neighbours. A whole-app review is `do-audit`.
3. **Run `scripts/check-design.py --root P`.** Colour, font, radius, spacing, gradient
   text, emoji and reduced motion are now settled by the script. Read the diff yourself
   for durations and easing (§7), shadows (§6) and font weights (§3).
4. **Judge, in order; stop at the first structural failure:**
   1. *Contradiction*: does the change argue with a rule's reason, not only its value? A
      palette blue used as a second accent still breaks "one accent".
   2. *Craft floor*: only the items the change can affect.
   3. *States*: a new control without hover, focus-visible, active, disabled, loading, error?
   4. *Consistency*: grep how the same pattern is done elsewhere.
5. **Verdict: exactly one of three.**
   - ✅ `Compliant. All values from the paper (v1.0). No new tokens, states complete.`
   - ⚠️ Drift: one line each, `file:line - value - rule (nearest token)`, then offer to apply.
   - ❌ Contradicts: quote the rule and version, give two ways forward (keep the paper /
     amend §N and state the new value's job), and do not pick: it changes the system.
6. **Stale paper?** If the code is better than the paper, say so with the evidence and
   propose an amendment with a version bump. Never silently edit the paper to match the
   code: that turns it into a record of accidents.

Always quote rule and version ("§2 of v1.0") so the user can check.
