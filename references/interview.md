# L2 · The design interview

Read the project and run the research first, so every question is about a choice, never
a fact you could have looked up. Ask in batches, with the consequence attached. Ask to
confirm an inference rather than to collect: "The code uses copper `#8C5A3C` as a single
signal with a serif. That reads as craft and heritage. Is that the business, or a leftover?"

Stop when you can predict the answer to a question you have not asked yet.

## Batches (skip what research already answered)

1. **Positioning, first, everything depends on it.** Who is it for, specifically enough to
   exclude someone, and who not? What should a visitor feel in three seconds? One thing
   to remember tomorrow? Fit the sector or depart? Offer the consequence: "Fitting in buys
   trust, people already know how to read it. Standing out buys attention but costs a
   beat of confusion. Which does this business need more?"
2. **Colour.** A colour you own or refuse, and why? Light, dark or both, which primary?
   What must never appear? If they name a colour, ask its role: "is it what people click,
   or what they sit on?"
3. **Type.** An existing brand face (check the logo and print material first)? If choosing:
   offer two characters, not five. A sentence, a paragraph or pages per screen? That
   decides body face and scale.
4. **Density.** Dense or airy, and how much per screen? These are one question: surface a
   conflict ("airy and lots of content") now, or whoever codes first resolves it by accident.
5. **Motion.** Calm or alive, and the ceiling? "Alive" means entrances, continuous motion
   or interaction feedback: ask which.
6. **Imagery.** Real photos, of what, by whom? Illustration: none, some, a system? What
   shows when a slot has no image? (The question that prevents shipped grey placeholders.)
7. **Voice.** Three words for the tone; reject clean, modern, sleek, premium once ("would
   it be false if a competitor said it?"). Words you hate? Paste something you wrote that
   sounds like you: the most useful input of the interview.
8. **Constraints.** Accessibility beyond AA? Assets that must stay? Deadline and budget:
   they set the ambition, and a 3-week launch does not get a 4-level elevation system.

## Red flags in answers

| Answer | Usually means | Follow up |
|---|---|---|
| "modern and clean" | nothing decided yet | "Show me two sites you call modern. What do they share?" |
| "like Apple" | restraint without a reason | "Apple's look is a retail decision. What is the equivalent here?" |
| "whatever looks good" | taste delegated | "Then I decide and write down why. You get one revision." |
| "make it pop" | emphasis without hierarchy | "Which one thing must pop? Only one can." |
| "we want to stand out" | afraid of being boring | "Standing out costs a beat of confusion. Worth it, and where?" |
| silence, then "you decide" | they do not know their audience yet | back to batch 1, question 1; everything else is guesswork |

## Retrofit (an existing project)

Ask what is true, not what they want: which tokens in the code are deliberate and which
accidents (`check-design.py --init` lists them by frequency, one-offs flagged)? Which
patterns repeat across pages? What in the code contradicts what you think the design is?
What would you fix first if time were free? Then write the paper as v1.0 of what actually
ships, plus a delta list (each gap with its evidence and a proposed fix). Values that still ship
but must not spread go into `legacy:`. If several design documents exist, the paper replaces them
as the one source: mark the old ones as superseded and point AGENTS.md at the paper. A retrofit that demands a rewrite is abandoned; one that
codifies reality and prices the gaps is adopted.
