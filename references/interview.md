# The design interview

Ask in **batches**, not one at a time. Read the project first (step 1) so that
every question here is about a *choice*, never a fact you could have looked up.

**Never ask a question you can infer.** Ask to confirm an inference instead:
> "I read the code: you're using copper `#8C5A3C` as a single signal with a serif.
> That reads as craft and heritage. Is that the business, or a leftover?"

---

## Batch 1 — Positioning (ask first, everything else depends on it)

1. Who is this for, **specifically enough to exclude someone**? Who is it *not* for?
2. What should a visitor feel in the first three seconds?
3. If they remember one thing tomorrow, what is it?
4. Should this look like its sector, or deliberately not?

> For Q4, offer the consequence, don't ask open:
> *"Fitting in buys trust — people already know how to read it. Standing out buys
> attention but costs a beat of confusion. Which does this business need more?"*

---

## Batch 2 — Colour

5. Is there a colour you **own**, or one you refuse? Why that one?
6. Light, dark, or both? Which is primary?
7. What must never appear on this site?

If they name a colour, follow up on **role**, not taste:
> "Is that colour the thing people click, or the thing they sit on?"
> (Accent vs. ground — the two most confused roles.)

---

## Batch 3 — Typography

8. Any existing brand face, or are we choosing? (Check the logo and any print
   material first — often there's a face nobody mentioned.)
9. If choosing: hard, soft, technical, editorial, or friendly? *(Offer two, not five.)*
10. How much text does a typical page carry — a sentence, a paragraph, or pages?

> Q10 decides the body face and the scale. A one-sentence-per-section site can
> afford a display face for body; a documentation site cannot.

---

## Batch 4 — Space and density

11. Dense and information-rich, or airy and sparse?
12. How much content should one screen hold?

> These two are the same question. If the answers conflict ("airy *and* lots of
> content"), surface the conflict now — it's the most common one and it will
> otherwise be resolved accidentally by whoever codes first.

---

## Batch 5 — Motion

13. Should it feel static and calm, or alive? What's the ceiling?
14. Any animation you've seen that you liked — or hated?

> "Alive" usually means three things and only one is wanted: entrance animation,
> continuous background motion, or responsive interaction feedback. Ask which.

---

## Batch 6 — Imagery

15. Are there real photos? Of what? Who takes them?
16. Illustration budget: none, some, or a system?
17. What should we show when we have no image for a slot?

> Q17 is the one that prevents shipped grey placeholders.

---

## Batch 7 — Voice

18. Three adjectives for the tone. *(Reject clean, modern, sleek, premium — they
    describe every template, so they decide nothing. Push once: "if a competitor
    said that about themselves, would it be false?")*
19. What words do you hate?
20. Paste something you wrote that sounds like you. *(The most useful input in
    the whole interview. A transcript, an email, a post — the real voice is in
    there, and it's usually better than the website copy.)*

---

## Batch 8 — Constraints

21. Accessibility requirements beyond AA?
22. Existing assets that must stay (logo, colours, fonts, imagery)?
23. Deadline and budget shape?

> Q23 decides ambition, which decides the system's complexity. A 3-week launch
> does not get a 4-tier elevation system.

---

## When to stop

Stop when you can **predict their answer** to a question you haven't asked. That
is the signal the model is complete — not when the list is exhausted.

---

## Red flags in answers

| Answer | What it usually means | Follow up with |
|---|---|---|
| "Modern and clean" | No decision has been made yet | "Show me two sites you'd call modern. What do they share?" |
| "Like Apple" | Wants restraint without a reason for it | "Apple's look is a retail decision. What's the equivalent here?" |
| "Whatever looks good" | Delegating taste to you — fine, but make it explicit | "Then I'll decide and write down why. You'll get one revision." |
| "Make it pop" | Wants emphasis, has no hierarchy | "What's the one thing on the page that must pop? Only one can." |
| "We want to stand out" | Usually means "we're afraid of being boring" | "Standing out costs a beat of confusion. Worth it? Where?" |
| Long silence, then "you decide" | Real answer: they don't know their audience yet | Go back to Batch 1, Q1. Everything downstream is guesswork. |

---

## For an existing project: the retrofit variant

Don't ask what they *want*. Ask what's **true**:

1. Which of these tokens in the code were deliberate, and which are accidents?
2. Which of these patterns appears on more than one page?
3. Is there anything in the code that contradicts what you *think* the design is?
4. What would you fix first if time were free?

Then write the paper as **v1.0 of what actually ships**, plus a delta list. A
retrofit that demands a rewrite gets abandoned; one that codifies reality and
prices the gaps gets adopted.
