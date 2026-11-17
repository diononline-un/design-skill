# L2 · Critique rubric

The numbers and the lens choice. Field scores in SKILL.md are the summary; this is the detail.

## Cognitive load

Three kinds: intrinsic (the task: structure it), extraneous (bad design: remove it),
germane (learning: support it). Eight checks; count the failures: 0-1 low, 2-3 address
soon, 4+ fix before shipping.

| Check | Threshold |
|---|---|
| single focus | the primary task completes without competing elements |
| chunking | ≤4 items per group |
| grouping | related items share proximity or a region |
| visual hierarchy | the most important element found in ≤2 s |
| one thing at a time | one decision before the next |
| minimal choices | ≤4 visible options at a decision point |
| working memory | no recall from a previous screen needed |
| progressive disclosure | complexity revealed on need |

Working memory holds about 4 items, not 7: ≤4 fine, 5-7 group or disclose, 8+ overloaded.
Applied: ≤5 top-level nav items; ≤4 siblings per docs sidebar level before grouping;
1 primary action, 1-2 secondary, the rest in a menu.

## Heuristics, scored 0-4

Visibility of system status · match with the real world · user control and freedom ·
consistency and standards · error prevention · recognition over recall · flexibility and
efficiency · aesthetic and minimalist design · error recognition and recovery · help and
documentation.

0 absent, the user guesses · 1 rare · 2 partial, major gaps · 3 good, minor gaps ·
4 excellent edge to edge. One line of evidence per heuristic.

## Personas: which lens for which surface

| Persona | The question it asks |
|---|---|
| Alex, power user | does the core task finish in <60 s; is there a keyboard path? |
| Jordan, first-timer | is the first action obvious in <5 s; are icons labelled? |
| Sam, assistive tech | keyboard-only flow, focus order, contrast, announced state changes |
| Riley, sceptic | does every claim survive "prove it"; what is hidden? |
| Casey, distracted on mobile | thumb reach, 390px, interrupted mid-task, slow connection |

| Interface | Personas |
|---|---|
| landing / marketing | Jordan, Riley, Casey |
| dashboard / admin, data-heavy | Alex, Sam |
| e-commerce / checkout | Casey, Riley, Jordan |
| onboarding | Jordan, Casey |
| form / wizard | Jordan, Sam, Casey |

Project personas beat these five when the research or the brief describes real users:
2-3 characteristics, 3-4 behaviours, 3-4 red flags, each traceable to a source. Never
invent audience details.

## Edge probes for any data-driven surface

Zero (what does it say when empty?) · one (does the layout hold?) · many (1000 items:
paginate, virtualise, or break?) · long (a 200-character name, a URL, an email, a
non-Latin script).
