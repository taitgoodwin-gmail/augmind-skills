# Offering spec reference

The spec is one JSON file. It holds every word of the deck and nothing about layout. `render.py` reads it and draws the deck in the locked v0.9 look.

The complete worked example is `examples/spec_digital-marketing_v0.9.json`. It rebuilds the v0.9 deck word for word. **Copy its shape. Read it before writing a new spec.**

## Rules that apply everywhere

1. **Text only.** Every value is plain text. No markdown, no line breaks, no manual bullets or numbers (the renderer adds them).
2. **Never type a slide number.** Write `{slide:REF}` and the renderer fills in the page number. Valid REF values:
   `cover`, `model_map`, `matrix`, `roles`, `phase1:overview`, `phase1:inputs`, `phase1:deliverables` (same for phases 2 and 3), `step1.2` (first page of that step), `task1.2.7` (the page that task's card is on), and the cross-phase view types `tiers`, `cards`, `panel`, `evidence`, `sources`, `decisions`.
3. **Sources are cited by name.** A card lists source names in `sources`. Each name must match a `name` in the top-level `sources` register exactly. The renderer turns the name into a link.
4. **Tags.** Every task card and rule card carries one tag. The tag sets the card's color.

   | Tag | Meaning | Card color |
   |---|---|---|
   | `platform` | The maker of the platform, tool or system says this on its own page, and that page was opened. | white |
   | `official` | A government, standards or professional body says this, and that page was opened. | white |
   | `own` | AugMind's own design. Any link on the card is background, not backing; say so in `note`. | gray |
   | `open` | Not validated, or proposed and not yet decided by the partners. | orange |

5. **The renderer is the judge of what fits.** The sizes below are character counts that were filled in and rendered together on 2026-10-07 with nothing overflowing. Start inside them, run the renderer, and fix every line it prints under MUST FIX by shortening the text in the spec. Never edit `render.py` to make one deck fit.
6. **Exactly three phases.** The look is built for the three-phase skeleton (Advise, Implement, Operate, under whatever names the offering uses).

## Top level

```
identity      cover and footer text
model         the two fixed tab labels
legend        the four tag labels and their one-line meanings
start         the three opening slides
phases        three phases
all_phases    the cross-phase slides, in order
sources       the source register
```

### identity

| Key | What it is | Fits |
|---|---|---|
| `offering_name` | Short name, used in every footer | 45 characters |
| `eyebrow` | Small line above the cover title, in capitals | 40 |
| `cover_title` | Cover title | 60 (two lines) |
| `tagline` | One line under the title | 75 |
| `status_line` | Bold line: what kind of draft, version, confidentiality | 100 |
| `disclaimer` | Small print on the cover | 280 |
| `pointer` | Optional. Bold last line, e.g. "Partners: read slide {slide:decisions} first." | 110 |
| `footer_parts` | List of footer pieces after the name: version, date, status, confidentiality, audience | 5 short pieces |

### model

`{"start_label": "START", "all_phases_label": "ALL PHASES"}`. Keep as is.

### legend

Four rows of `[label, tag, meaning]`, one per tag, in the order platform, official, own, open. The label is what cards show. Change `"Platform rule"` only if the offering has no platforms (for example to `"Vendor's own page"`).

### sources

One row per source: `{"name": "Google Ads: experiments", "url": "https://...", "status": "Opened live, Oct 6"}`.

- `name`: "Publisher: short topic". 55 characters at most. This exact text is what cards cite.
- `status`: how the page was last read. Text that starts with "Opened live" shows green. Anything else shows gray.
- 26 sources fit on a page; the renderer adds pages as needed.
- The renderer reports any cited name missing from the register (MUST FIX) and any register row that no slide cites.

## start: the three opening slides

`views` is the three breadcrumb labels: `["Where this fits", "The offering", "Roles"]`. All three slides are required.

### start.model_map (slide 2)

| Key | What it is | Fits |
|---|---|---|
| `title` | Headline | 62 |
| `model_label`, `model_sub` | Left label for the AugMind model row and its one-line meaning | 20 / 45 |
| `offering_label`, `offering_sub` | Left label for this offering's row and its one-line meaning | 20 / 45 |
| `model` | Three stages `{name, text}`: ADVISE, IMPLEMENT, OPERATE and what each means | text 45 |
| `cards` | Three cards. Each is `{label, text}` or `{label, lines: [[bold, plain], ...]}`; add `"highlight": true` for a lavender card | text 230 |
| `evidence` | The note line at the foot | 190 |

The blue phase boxes and their step numbers are drawn from `phases`.

### start.matrix (slide 3)

| Key | What it is | Fits |
|---|---|---|
| `title` | Headline | 62 |
| `rows` | Five rows `{label, cells: [phase 1, phase 2, phase 3]}`: INPUTS, ACTIVITIES, DELIVERABLES, APPROVAL, ROLES | each cell 105 (three lines); keep every cell of at least one row to 70 |
| `note` | `[bold lead, sentence]` under the table | 130 |
| `evidence` | Note line | 190 |

The column heads, step numbers and "slides a to b" are drawn from `phases`.

### start.roles (slide 4)

| Key | What it is | Fits |
|---|---|---|
| `title` | Headline | 62 |
| `chart_heading` | Heading above the chart | 40 |
| `chart.lead` | `{name, sub}` the accountable role | 25 / 35 |
| `chart.second` | Optional `{name, sub}` role between the lead and the team | 25 / 38 |
| `chart.team` | Team roles `{name}`; add `"open": true` and optional `"open_note"` for an unfilled seat | 4 roles (6 at most) |
| `chart.outside` | Optional `{name, open, text}` a role outside the team, such as a reviewer | text 75 |
| `table.header` | Column head for the role column | 30 |
| `table.rows` | One per role: `{name, does, open, letters: [phase 1, phase 2, phase 3]}` | 11 rows; `does` 70 |
| `legend` | The letters used and their meaning, e.g. `["A", "accountable"]`. Letters with set colors: A, R, V, S, C and — | 6 |
| `evidence` | Note line | 230 (two lines) |

## phases

Each phase: `{number, name, overview, inputs_roles, steps, deliverables}`. `number` is 1, 2 or 3. `name` is one word if possible (it appears in every tab).

### overview

| Key | What it is | Fits |
|---|---|---|
| `title` | Headline: the phase name and what it settles | 62 |
| `purpose` | One or two sentences | 200 |
| `columns` | Four columns `{label, subtitle, numbered, items, highlight}`: INPUTS, ACTIVITIES, DELIVERABLES, APPROVAL. Set `"numbered": true` for an ordered list and `"highlight": true` on APPROVAL | 8 items per column. A line holds about 27 characters and a column holds 11 lines, so at most three of eight items can run to two lines |
| `notes` | Up to three `[bold lead, sentence]` lines under the columns | each 130 |

### inputs_roles

| Key | What it is | Fits |
|---|---|---|
| `title` | Headline | 62 |
| `view_label` | Optional breadcrumb label. Default "Inputs and roles" | 28 |
| `inputs_heading`, `roles_heading` | The two small headings | 45 / 25 |
| `inputs` | Cards `{name, from, text}`: what is needed and who provides it | 8 cards; name 38, text 105 |
| `gray_cards` | Optional gray cards `{name, text}` that share the grid, e.g. "Not part of this phase" | counts toward the 8; text 160 |
| `choices` | Optional band under the grid: `{heading, items: [{name, text}]}` for options the client picks from | 5 items; with a band, 6 cards above it |
| `role_groups` | Two groups `{label, client, roles: [{name, open, does}]}`: AugMind, then the client with `"client": true` | 5 + 3 roles; `does` 47 |
| `evidence` | Note line | 190 |

### steps

Each step: `{number, name, title, tasks, bands, mapping}`. `number` is "1.1", "1.2" and so on. `name` is short because it sits in the breadcrumb row: a phase's step names together should stay under about 45 characters.

| Key | What it is | Fits |
|---|---|---|
| `title` | Headline: "Step 1.1 Audit: nine tasks, eight tied to an outside source" | 62 |
| `tasks` | Cards `{number, name, text, tag, sources, note}`. `number` is "1.1.1" and so on; leave it out for a card that is a rule rather than a task | name 30; text 135; two sources (three if short). Nine cards at that size fit on one page. Longer cards still fit their boxes but move the last row to a second page |
| `bands` | Optional. Extra rows under the grid on the step's first page: `[{heading, cards: [...]}]`, cards shaped like tasks | 2 or 3 cards |
| `mapping` | Optional. One wide card with a two-column table: `{name, text, tag, note, pairs: [[left, right], ...]}` | 10 pairs |

- `note` is the small gray line under the tag. Use it to say why a card is `own` or `open`, or to mark a link as background ("Background, not backing:").
- A step with more cards than fit continues on a second page by itself. The headline and counter are written for you.

### deliverables

| Key | What it is | Fits |
|---|---|---|
| `title` | Headline | 62 |
| `lists` | One or two documents with numbered sections: `{name, subtitle, items}` | 10 items, each 30 |
| `texts` | One to three documents described in a sentence: `{name, text}` | two at 220 each |
| `approval_heading` | Small heading | 50 |
| `approval` | Five tests `{text, confirms, highlight}`: what must be true and who confirms it. `"highlight": true` on the tests the client signs | text 80; confirms 22 |
| `evidence` | Note line | 230 (two lines) |

## all_phases: the cross-phase slides

A list of views in the order they appear. Every view has `view` (breadcrumb label, 20 characters), `type` and `title` (62). **Always include `evidence`, `sources` and `decisions`, in that order, last.** Add the other three only when the offering needs them.

### type "tiers" (optional)

A three-level structure on the left, rules on the right, three source cards below. In v0.9: how reports separate what was observed from what a platform claims.

`tiers`: three `{name, when, text, style}`; style is `solid`, `highlight` or `optional` (dashed). Text 110.
`rules_heading`, `rules`: up to six bullets, each 95.
`cards_heading`, `cards`: three cards shaped like tasks, text 70.
`evidence`: note line.

### type "cards" (optional)

Large cards for rules that hold in every phase. `cards`: shaped like tasks, with `number` "1", "2" and so on. Six fit on a page; text 140.

### type "panel" (optional)

One panel for a special case that adds steps. In v0.9: regulated industries.

`heading`, `steps` (up to seven numbered lines, each 55), `notes` (up to four `[bold lead, sentence]`, 600 characters in all), `sources` (names), `footnote` (one line under the panel, 150).

### type "evidence" (required)

`tiles`: four `{number, text}` counts; add `"tone": "open"` for a count of what is missing. **Compute the numbers from the register; never type them from memory.**
`panels`: three `{label, style, items, note, sources}`: what is strong (`white`), what is AugMind's own (`gray`), what is open (`open`). Five bullets each, 85 characters a bullet.
`evidence`: note line saying how and when the sources were checked (230).

### type "sources" (required)

`title` and `evidence` only. The rows come from the top-level `sources`.

### type "decisions" (required)

`decisions_label`: small heading.
`gating`: optional orange box `{callout, items}` for the decisions everything else waits on. Two items, each 250.
`decisions`: the remaining decisions. Numbering continues from the gating items. Two gating items and three decisions fit at those lengths (160 each for the decisions).
`right`: two blocks `{label, style, bullets}` or `{label, style, numbered}`: for example questions for a lawyer and next steps. Ten items across the two blocks; a line holds about 65 characters, and up to five items can run to two lines.
`evidence`: note line (230).

Everything tagged `open` anywhere in the deck must appear on this slide, either by itself or grouped ("tasks 1.2.7 to 1.2.10").

## What the renderer prints

```
slides: 26  |  slide links made: 238, pointing at slides not in this build: 0
MUST FIX (text that does not fit, or a broken reference): 0
adjusted automatically (fits; shorten the text to get the standard size back): 1
sources on the register that no slide cites: 0
page numbers: cover=1, model_map=2, ...
```

Exit code 0 means nothing must be fixed. Exit code 2 means at least one MUST FIX line.

| Message | What to do in the spec |
|---|---|
| `text needs Npt but its box is Mpt (what) [first words...]` | Shorten that text. Each line of text is about 12pt. |
| `breadcrumb row is ... wide` | Shorten the step names or the view labels in that section. |
| `headline is too long for one line` | Shorten the title. |
| `N input cards need ...` | Shorten the card texts or remove a card. |
| `a row of cards runs to ...` | Shorten the longest card in that step. |
| `source '...' is cited but is not in the source register` | Fix the name, or add the source to the register after opening it. |
| `{slide:...} does not match any slide` | Use one of the REF names listed at the top of this file. |
| `the right-hand blocks need ...` / `the panel runs to ...` / `the matrix rows run to ...` | Cut lines from that slide. |
