# Prototype: how to build the core journey from the spec

## First, check for a real app

Look for a repository, screenshots in the design system, or a live sign-in in the input. If a working app exists, do not rebuild it. Prototype only the screens the deck adds or changes, and say in the build note which screens exist already.

## Screens (five to nine)

Walk the three phases as the customer sees them. For each phase, the first screen, the screen where the approval test happens, and the result screen. Typical product set: sign-up or checkout result, setup, the approval screen (the customer confirms something), a "running" screen, the report, the change note, settings.

## Each screen

- One HTML file in `prototype/`, named `01-setup.html` and so on, each linking to the next and back. Same tokens as the home page.
- Every claim sentence carries `data-claim="<card number>"`, like the page.
- Sample data labeled "Sample", plausible, and consistent across screens (the same brand, competitors and numbers everywhere).
- Every state the deck's approval tests imply: not yet run, running, done, failed, empty. Draw them on the screen or as linked variants.
- Keyboard reachable; focus visible; headings in order; no horizontal scroll at phone width.

## What a prototype never does

- Promise a result the deck does not back.
- Show a price unless the input supplies it.
- Name another brand or a real competitor as sample data; use neutral sample names.
