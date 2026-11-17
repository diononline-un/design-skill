# L2 · Critique rubric

Thresholds and the persona→interface table. Nielsen's ten heuristics themselves,
the cognitive-load theory and the persona write-ups are not reproduced here —
they are widely known and the model already has them. What follows is only the
part that has to be *stated*: numbers, and which lens to apply when.

## Cognitive load — thresholds

Load is three kinds: **intrinsic** (the task itself — structure it, can't remove
it), **extraneous** (bad design — remove ruthlessly), **germane** (learning —
support it).

Eight checks. Count the failures:

| Failures | Verdict |
|---|---|
| 0–1 | low — good |
| 2–3 | moderate — address soon |
| 4+ | critical — fix before shipping |

The eight, with the numbers that make them testable:

| Check | Threshold |
|---|---|
| Single focus | primary task completable without competing elements |
| Chunking | **≤4 items per group** |
| Grouping | related items share proximity/region |
| Visual hierarchy | most important element identifiable in **≤2 s** |
| One thing at a time | one decision before the next |
| Minimal choices | **≤4 visible options** at any decision point |
| Working memory | no recall from a previous screen required |
| Progressive disclosure | complexity revealed on need |

**Working memory is 4, not 7.** Miller's 7±2 was revised (Cowan, 2001):

| Items | Status |
|---|---|
| ≤4 | within limits |
| 5–7 | pushing it — group or disclose progressively |
| 8+ | overloaded |

Applied: navigation ≤5 top-level items; docs sidebar ≤4 siblings before grouping.

## Scoring each heuristic

**0–4.** A 4 means genuinely excellent, not "fine".

| Score | Means |
|---|---|
| 0 | absent — user is guessing |
| 1 | rare — most cases fail |
| 2 | partial — major gaps |
| 3 | good — minor gaps |
| 4 | excellent — holds edge to edge |

Use this scale for whatever heuristic set you apply. Report per heuristics with
one line of evidence each; the field scores in `SKILL.md` §Scoring are the
summary, this is the detail.

## Personas — which lens for which surface

Five archetypes, selected by interface type. Test like this, not by inventing
demographics.

| Interface | Primary personas | The risk being tested |
|---|---|---|
| Landing / marketing | Jordan (first-timer), Riley (skeptic), Casey (mobile) | impression, trust, small screen |
| Dashboard / admin | Alex (power user), Sam (accessibility) | efficiency, keyboard |
| E-commerce / checkout | Casey, Riley, Jordan | mobile, edge cases, clarity |
| Onboarding | Jordan, Casey | confusion, interruption |
| Data-heavy / analytics | Alex, Sam | speed, keyboard nav |
| Form / wizard | Jordan, Sam, Casey | clarity, a11y, mobile |

**The archetypes, compressed to what each is *for*:**

| Persona | The question it asks |
|---|---|
| **Alex** — power user | can the core task finish in **<60 s**? is there a keyboard path? |
| **Jordan** — first-timer | is the first action obvious in **<5 s**? |
| **Sam** — accessibility-dependent | focus order, contrast, works with the keyboard alone |
| **Riley** — skeptic | does this claim survive "prove it"? what's hidden? |
| **Casey** — distracted mobile | thumb reach, 390px, interrupted mid-task |

**Project-specific personas beat these five** when the product has real users.
Derive from the audience described in the brief — 2–3 characteristics, 3–4
behaviours, 3–4 red flags. Never invent audience details; fall back to the five
when there is no context.

## Edge cases — the four probes

Run these on any data-driven surface. They find more than a visual review does:

1. **Zero** — what does it say when there is nothing?
2. **One** — does the layout hold with a single item?
3. **Many** — 1000 items: paginate, virtualise, or does it break?
4. **Long** — a 200-character name, a URL, an email, a non-Latin script.
