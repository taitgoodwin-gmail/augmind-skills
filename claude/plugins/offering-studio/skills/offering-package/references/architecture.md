# Architecture: how to draw it from the spec and the input

## What it holds

1. **Systems**: each system the offering runs or reads, with who hosts it and who owns the account. One box each.
2. **Flows**: what moves between systems, in what direction, on what trigger (a weekly run, a webhook, a user action).
3. **Data held**: what the brand stores about customers and their clients, where, for how long, and whether it can be restored.
4. **Decisions already made**: the cloud, the data route, the sign-in method, with the record and date each was decided. Draw them; never reopen them.
5. **Open parts**: anything the input leaves undecided. Dashed box, the word "open" inside, and a line on the deck's decisions slide.

## Rules

- Every box carries the card number or the record it comes from (`REQ-19`, `task 2.1.3`, `architecture review Oct 21`). A box with no source is a proposal and is dashed and labeled "proposed".
- Vendor limits (a sandbox cap, a retention default, a region) come from the vendor's own page, opened in this run, and are listed under the diagram like deck sources.
- Keep one page: the diagram above, the record below (a table of systems, then flows, then data held, then decisions). An SVG inside one HTML file; same tokens as the home page.
- Words as well as lines: every dashed line also says "open" or "proposed" in text, so the page does not rely on style alone.
- Where the `deploy-on-aws` plugin's `aws-architecture-diagram` skill is listed and the stack is AWS, let it draw the diagram and keep the record here.
