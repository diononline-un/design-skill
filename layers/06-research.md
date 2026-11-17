# L1 · Research

Required for `do-crazy` and `do-design-renew`, and for `do-design-new` whenever the brief
is thin. The point is not to find something to copy: it is to find the material the
project legitimately belongs to and what its real customers look for, so the design
derives from the subject instead of from a template.

## Rules

- **Thin brief = research, not defaults.** "Make it new" + a logo means: collect evidence
  until the direction can be argued from it. Never fill a gap with the usual look or an
  invented fact.
- **Every finding carries its source** (URL, script output, or "user said"). No source,
  no claim. What cannot be found is written as `unknown`, and becomes a question for the
  user only if it changes the direction.
- **Every finding ends in "for us"**: does it fit this business, and how do we make it
  our own? A finding without that line is trivia.
- **Tools.** Use whatever web search and page-fetch tools are available; a browser for
  JS-heavy pages; the scripts below for anything measurable. Never enter credentials:
  sources behind a login are used only where the user is already signed in, otherwise
  skipped and named as skipped. Search with sector and place, never with private data.

## 1. What exists

Logo: `scripts/research.py logo FILE` (colours by share, contrast, role hints). Existing
site: `research.py profile URL`, `render-audit.py URL`, `audit.py copy`. Photos, print
material, texts the owner wrote: list them. These are constraints and the first evidence.

## 2. The subject's physical world

What does the business actually touch? Write 8-12 nouns, cross out the ones generic to
the industry, keep the ones specific to this operation. They are the only source of
distinctiveness that does not have to be invented: colour, texture, imagery and type
come from here.

> SHK firm: boiler room, copper pipe, press fittings, the van, the bathroom before and
> after, the heat pump in a front garden, the emergency call at 6 am, the Meister
> certificate. Generic: "comfort", "energy", "solutions" (cut). Specific: copper,
> before/after, the call at 6 am (material).

## 3. Search demand: what people actually type

`research.py suggest "<service>" "<service> <town>" --lang de --expand` for each core
service. Cluster the phrases into intents (emergency, renovation, replacement, cost,
subsidy, maintenance) and map each cluster to a page, a heading or an FAQ answer.
Autocomplete gives real phrasing and a popularity order, not volume: say so.

## 4. Who ranks, and why

Search the 3-5 core queries with the place. Take the top organic results (skip ads,
directories and portals, note them separately as competition for the click). Profile 5-8
firms: `research.py profile URL ... [--shots DIR]`. Record what the ranking pages share:
title and H1 pattern, one page per service, place names, phone above the fold, schema
types, reviews, subsidy or price information, word count, speed. That is the on-page
part of "why". Backlinks, domain age and the Google Business profile are outside a
page profile: name them as unknown unless a source shows them.

## 5. What real customers want

Read what customers write, not what firms claim: reviews of the competitors' Google
Business listings and trade directories, forum threads, "People also ask" boxes, Q&A
sites. Collect 5-10 quotes with links: what gets praised, what gets complained about,
what people were burned by (often the trust signal to lead with). Trust is
audience-specific: a 60-year-old homeowner and a property manager read different signals.

## 6. Category conventions, and the decision about them

From the profiles: palette, type character, density, imagery, and the one thing each
firm owns.

| The category | Positions available |
|---|---|
| looks all the same | fit and be instantly legible, or depart and be the anomaly; choose by mode |
| is visually chaotic | fit: calm is the differentiator |
| is outdated | depart, but only if the audience reads "modern" as trustworthy |

Write the decision down with its reason. A departure without a reason is taste.

## 7. Visual references: qualities, never layouts

| Source | Good for | Access |
|---|---|---|
| land-book.com | landing pages by category and style | browser only (plain fetches are blocked) |
| cosmos.so | moodboards: light, material, type | `cosmos.so/search/elements/<term>`, browser (JS) |
| are.na | worlds and materials, archives, research boards | `research.py arena "<term>"` lists channels; open them in a browser |
| savee.com | visual moodboards | login only: use it if the user is signed in, else skip |
| mobbin.com | real app and web flows (booking, checkout, forms) | login/paid: only in the user's signed-in session |

Search the subject's nouns from step 2, not the industry ("copper pipe", "boiler room
light"), plus the character words. Collect 5-10 references. From each take the quality:
composition, light, density and rhythm, restraint, type character. Never the layout,
palette, section order, components or the specific face. The derivation test: can you
name in one sentence what you took, and would it still be true in another medium? "The
calm line weight of a technical drawing" transfers. "Their hero layout" is templating.

## 8. Make it ours

One table, written into the research file. Only rows with a "for us" column count.

| Finding | Source | Fits us because / does not because | Make it ours by |
|---|---|---|---|
| Top 3 rankers put the emergency number in the header | profiles of x, y, z | fits: 30 % of suggest phrases are "notdienst" | number in the header, plus the real response time from the owner `[number needed]` |
| Reviews praise "clean site after the job" | 6 quotes, Google listings | fits: owner's photos show it | before/after pairs as the signature moment |

Then the five direction lines (SKILL.md), each traceable to a row, and the anti-default
gate: for every line ask "would I have arrived here for any similar project?" If yes,
revise and say what changed. Check against the second-order defaults, the tasteful
looks that became templates themselves:

| Default | Why it is a trap |
|---|---|
| cream ground + terracotta + serif | the tasteful default of recent years |
| near-black + one acid-green or vermilion accent | the "serious tech" default |
| emerald or teal accent | purple-avoidance, still a default |
| orange accent + serif | the "I avoided purple" signature |
| mono micro-labels, `A · B · C`, `WORD - fragment` | template chrome |
| broadsheet type on a non-publication | editorial cosplay |
| one big photo + centred headline + pill CTA | the "designed" default |
| engraving or woodcut as a filter | only when the whole brand lives there |

Escaping one template into another is a lateral move. The test is not "better than the
violet gradient" but "this product's answer".

## 9. State the risk

What might the audience misread? What does the direction make harder (conversion, trust,
scannability)? What is the fallback? A direction with no stated risk was not ambitious
enough or not thought through.

## 10. Keep it

Write steps 1-9 to `docs/design-research.md` in the project: sources, quotes, profiles,
the table. The paper's §1 cites it; the next session reads it instead of researching again.
