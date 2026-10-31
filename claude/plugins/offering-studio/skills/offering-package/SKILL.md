---
name: offering-package
description: "Builds the rest of an offering's launch package from a finished offering-deck spec, for the same brand: a technical architecture when the offering depends on software or client systems, a home page always, a clickable prototype when the offering is a product, and an internal financial model (costs, capacity, price assumptions, unit economics) when asked or once the deck is approved. Use when someone asks for the architecture, the website home page, the prototype, the financial model or \"the package\" for an offering that already has a deck."
---

# Offering package: architecture, home page, prototype, financial model

This skill starts where `offering-deck` ends. It reads the deck's build folder (the spec, `source_notes.json`, `decisions.json`), decides which outputs the offering needs, builds them for the same brand, and checks that every claim on the page traces to a card in the deck.

**Thesis: one spec, several outputs. Nothing on the page or in the prototype says more than a deck card says.**

## What comes out

| Output | When | Form |
|---|---|---|
| Technical architecture | Two or more of the A rules below are true | A diagram (SVG in an HTML page) and a short record: systems, flows, data held, who hosts, decisions already made |
| Home page | Always | One self-contained HTML file at desktop and phone widths, real copy, every claim marked with the card it comes from |
| Clickable prototype | The frame is product (or hybrid, for the screens the page shows) | Static linked screens for the core journey, one HTML file per screen, each state designed |
| Financial model | Always offered; built when asked for or when the deck is approved | `financials.json` (every figure tagged like a deck card) and a spreadsheet drawn from it: assumptions, unit economics, capacity, open items. Internal only; its figures never appear on the page or in the prototype |

Each output is a file in the build folder first, because the checker needs a file. Where the session can publish artifacts, publish the page and the prototype privately for review after the checker passes; the file stays the record.

Allow one output per session. Each is an hour or more of work; the spec file is the handoff between sessions. Say so in one line at the start.

## 1. Read the build folder

Open in full: the spec, `source_notes.json`, `decisions.json`, and the brand pack the deck used (`${CLAUDE_SKILL_DIR}/../offering-deck/brands/<brand>/brand.json`, or the path in `decisions.json`). If the deck has no build folder, stop and say that `offering-deck` has to run first; do not rebuild the offering from the PowerPoint.

`decisions.json` holds the frame and the A and P rule answers that `offering-deck` recorded (vocabulary in `references/decision-rules.md`). Use them as they stand. If the file is missing, apply the rules yourself to the input the deck was built from, record each answer with the sentence it rests on, and say so in the package note. Unknown counts as no.

## 2. Architecture (if needed)

Read `references/architecture.md`. Rules in short:

- Start from decisions already recorded in the input (a design record, an architecture review, a decided cloud). Never reopen a decision; draw it and name where it was decided.
- Draw only what a card or the input states: systems, the flows between them, the data each holds, who hosts and who owns each account. Every box carries the card number or record it comes from.
- Mark undecided parts in words ("open: data route") as well as by dashed lines. Put each on the deck's decisions list if it is not there.
- Vendor limits come from the vendor's own page, opened, and are cited like deck cards.
- When the `deploy-on-aws` plugin's `aws-architecture-diagram` skill is listed and the stack is AWS, use it for the diagram; otherwise draw an SVG by hand in one HTML page.

## 3. Home page (always)

Read `references/home-page.md`. Rules in short:

- Who uses it, on what device, to do what, and what success means come from the deck's roles and the product challenge. Write them at the top of the page's build note.
- Real copy, written from the deck. Every sentence that claims something carries `data-claim="<card number>"` naming the card it comes from. A card tagged `open` cannot be claimed. A card tagged `own` can (a brand may state its own design).
- No prices unless the requester supplies them in the input. The checker flags currency symbols.
- No promises of results, rank or revenue. "Measured", "verified", "documented" are the words.
- The brand's design system, when the session lists one (the Design System artifact type, or a `tokens.json` in the pack), sets the colors, type and spacing. Otherwise the brand pack's colors and font do.
- Hierarchy first: one primary action per screen. Design every state: loading, empty, error, success.
- Accessibility is a requirement: WCAG 2.2 AA contrast, keyboard and screen-reader support, visible focus, reduced-motion support, no horizontal scroll at phone width, 16px side gutter.
- Avoid the templated defaults: cream or off-white page backgrounds (unless the design system sets them), italic accent words in headlines, numbered "01/02/03" section labels, monospace labels (unless the design system sets them), pill-shaped buttons, purple gradients, interchangeable card grids.

## 4. Prototype (if a product)

Read `references/prototype.md`. Rules in short:

- First check whether a working app already exists (a repository, screenshots in the brand's design system). If it does, do not duplicate it; prototype only the screens the deck adds or changes, and say so.
- The core journey is the three phases as the customer sees them: the first screen of each phase, the screen where approval happens, and the report or result screen. Five to nine screens.
- Each screen is one HTML file in `prototype/`, linked to the next; every claim on a screen carries `data-claim` like the page. Sample data is labeled "Sample" and is plausible and consistent across screens.
- Every state the deck's approval tests imply is drawn: not yet run, running, done, failed, empty.

## 5. Financial model (when asked, or once the deck is approved)

Read `references/financial-model.md`. Rules in short:

- Write `financials.json` first; the sheet is drawn from it. Every figure carries a tag with the deck's meaning, and a `platform` or `official` figure is on a page opened this session.
- Prices are always `open` (Claude's proposed range) or `own` (the brand decided, with the record). Claude never sets a price.
- Run `scripts/check_financials.py` and fix what it prints before building the sheet.
- The unit economics use Downside, Base and Upside scenarios, not columns taken straight across the lines; the reference says which end of each range each scenario uses.
- Build the sheet from the Sheets artifact type when listed, otherwise an .xlsx with the `xlsx` skill. Formulas, not typed results. Publish privately.
- No figure from the model goes into the deck, the home page or the prototype. The no-price checks stay as they are.

## 6. Check

Task progress (copy and tick off):

- [ ] `python3 ${CLAUDE_SKILL_DIR}/scripts/check_package.py <spec> <build folder> --brand <id>` (the id of the deck's brand pack; the script also reads it from `decisions.json`). It reads every HTML file in the folder and prints, per file: claims resolved, claims unresolved (no such card), claims on `open` cards, currency symbols found, other brands named. Only proceed when it prints "pass".
- [ ] Open the page and each prototype screen at phone width and desktop width (a headless browser screenshot is enough). Look for text that overflows, a control with no visible focus, and a primary action that is not the one the deck's approval names.
- [ ] Design read by a separate agent that did not build the page, from a demanding design lead's point of view: hierarchy, consistency, accessibility, whether it looks templated. Use the `design:design-critique` and `design:accessibility-review` skills when listed; otherwise the agent reads from this file. Fix what it finds, then run the checker again. One round.
- [ ] Claims read: when `product-legal:marketing-claims-review` is listed, run it on the page copy; otherwise a separate agent reads for promises of results and claims without a card. Fix, re-check.

Where no separate agent can be started, do the reads yourself and say so in the build note.

## 7. Deliver

- Files stay in the build folder beside the deck: `architecture/`, `home-page/index.html`, `prototype/`, `financials.json` with its sheet, and `package-note.md` (which rules fired and on what sentence, which reads ran and whether they were independent, what was left out and why).
- Send the files in the conversation, or place them in the folder the requester names. Publish privately for review only where the session can, after the checker passes. Do not upload anywhere shared unless asked.
- Report in a few lines: which outputs were built and why the others were not; the checker's counts (for the model: lines by tag, and base and downside gross margin per customer with the open lines they depend on); the two or three findings from the reads that most need a decision.
