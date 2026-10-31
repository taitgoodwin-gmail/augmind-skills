# Home page: how to build it from the spec

## Before writing

Write a six-line build note at the top of `home-page/build-note.md`:
who uses the page (from the deck's customer or client roles); on what device (phone first unless the input says otherwise); what they are trying to do (the first approval in phase one, usually "decide whether to start"); what success means (they take the primary action, or they understand the offering well enough to ask a good question); which design system or brand pack sets the look; whether a live site exists.

## Structure (adjust sections as needed)

1. Header: the brand's wordmark from the pack or design system, three links at most, one primary action.
2. Hero: one sentence that says what the offering is, in the deck's tagline words, and one that says who it is for. The primary action, once.
3. The problem, in the customer's words, from the product challenge.
4. The three phases as the customer experiences them, one short block each, in the deck's phase names.
5. Evidence: how the offering shows its work (the deck's evidence slide in plain words). This section carries the most `data-claim` marks.
6. Who it is for and who it is not for (from the gray "Not part of" cards).
7. Questions people ask, five at most, including the one about guarantees, answered honestly from the deck.
8. Final action and footer with the legal line from the brand pack.

## Copy rules

- Every claim sentence carries `data-claim="<card number>"`. A sentence with no card is description, not a claim; keep those few and plain.
- Never claim results, rank, revenue or "guaranteed". Say what is measured, verified, documented or checked.
- No prices unless supplied. Write "See plans" or "Ask about plans" as the placeholder and say so in the build note.
- Button labels are verbs. Headlines are sentence case. No exclamation marks, superlatives or emoji.
- Label sample visuals "Sample" or "Illustrative" in small text.

## Build rules

- One self-contained HTML file: styles and script inline, no external scripts except fonts from Google Fonts if the design system names one.
- Design tokens as CSS custom properties on `:root`, from the design system or the brand pack. Dark mode when the design system defines it.
- Phone width first: 16px side gutter, no horizontal scroll, touch targets at least 44px.
- Contrast at WCAG 2.2 AA; visible focus (two-tone ring where the design system defines one); `prefers-reduced-motion` honored; landmarks (`header`, `main`, `nav`, `footer`) and one `h1`.
- Design every state the page has: form loading, empty, error, success.
- Avoid the templated defaults listed in SKILL.md unless the design system sets them.
