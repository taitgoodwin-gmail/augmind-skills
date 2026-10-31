---
name: offering-deck
description: Builds an evidence-tagged offering deck (PowerPoint) for a named brand from any input (a website, an existing offering, notes, files, an article, an idea). Use when someone asks for an offering deck, a service or product design deck, or a new version of a deck this skill built. Not for client sales decks, website copy, pricing, or decks in another look.
---

# Offering deck from any input

The requester points at something and names the brand. This skill reads the input, researches it, designs the offering, writes one spec file, and draws the deck with the bundled renderer in the locked look, in that brand's colors, logo and words.

**Thesis: the deck states what was opened and read, marks everything else as open, and is drawn by the renderer, never by hand.**

## What comes out

One PowerPoint for the brand's decision makers and subject experts, 18 to 22 slides, never more: the cover; the opening slides (a delivery-model slide only if the brand has one, the offering on one page, roles); three phases, each with an overview, inputs and roles, one slide of task cards per step, and deliverables and approval; then the cross-phase slides, which always end with evidence, the source register and the decisions. Beside it, a build folder with the spec and the source notes, which `offering-package` and any later revision read.

A full run takes more than an hour. Say so in one line at the start.

## 1. Prove the renderer runs

Everything needed ships in this skill's folder. Nothing is fetched from anywhere else.

| Path (inside this skill) | What it is |
|---|---|
| `render.py` | Reads a spec (JSON) and writes the deck. The look is locked here; the brand is a parameter. |
| `SPEC.md` | Every spec field and how much text fits in it. Read it in full before writing a spec. |
| `brands/<id>/brand.json` | Brand packs: logo, colors, font, the standing words. Shipped: `augmind`, `levarum`, `neutral`. |
| `examples/spec_example_v0.1.json` | A neutral example (fictional Example Co). The model for shape, length and tone. |
| `scripts/check_spec_brand.py` | Fails a spec that names another brand, carries a price, or mismatches its pack. |
| `scripts/evidence_counts.py` | Counts sources and cards by tag from the spec and writes the evidence tiles. |
| `tools/preview.py` | Turns a deck into slide pictures and contact sheets. Needs LibreOffice and pdftoppm. |
| `tests/smoke_test.sh` | Renders the neutral example with the neutral pack and with no pack. Must print `MUST FIX ... 0` twice and "smoke test passed". |

The skill folder may be read-only. Run scripts from where they are; write every output to a working folder.

1. Install `python-pptx`, `Pillow` and `lxml` if missing (`pip install --break-system-packages python-pptx Pillow lxml`).
2. Run `bash ${CLAUDE_SKILL_DIR}/tests/smoke_test.sh <working folder>/smoke`. If it fails, stop and say exactly that. Do not draw the deck another way.
3. Read `SPEC.md` and the example spec in full.

## 2. Pick the brand

The brand pack decides the look and the standing words. Pick it before reading the input:

- The requester names it, or the input is plainly one company's. Shipped packs: `augmind` (AugMind, with its Advise, Implement, Operate delivery model), `levarum` (Levarum, formerly Signal and MindLeverX, no delivery model), `neutral` (fictional Example Co, for tests).
- A pack the requester points at by path works the same way.
- No clear brand: ask once, with the shipped packs as the options. Unattended: use `neutral` and say so.

Read the pack's `words` once. Every standing line in the spec is written from them: `eyebrow`, `legal_line` (in the status line, footer and disclaimer), `audience_line`, `decision_makers` (who the decisions slide addresses), `own_meaning` (the legend's third row), `own_panel_label` (the evidence slide's middle panel), `provider_group_label` (the first role group), `file_prefix` (the file name), and `model`. The legend's `own` label is the pack's `own_label`, exactly.

**The model slide.** If `words.model` is set, write `start.model_map` from it and give `start.views` three labels. If it is `null`, leave `model_map` out and give `start.views` two labels. Never invent a delivery model for a brand that has none.

**Never name another brand** in a spec: not as a model, a comparison or an aside. `check_spec_brand.py` fails the spec if you do.

## 3. Read the input. Never draft from memory.

Open every input in full before designing anything. If one cannot be opened, name it and carry on with the rest.

| Input | How to treat it |
|---|---|
| Another company's website | A lead, not a source. It shows what the market sells and the words buyers use. The brand builds its own offering. Do not copy its wording, cite it as evidence, or name the company in the deck. |
| The brand's own offering, deck, record or document | Authoritative for the brand's own choices. Keep its names, decisions and wording. Fill gaps as open items. |
| Notes or an idea | Everything the notes do not say is a proposal. |
| Files, requirements, an article | Read in full. An article is a lead unless it is itself an official source. |

Take from the example its structure only. Its content decisions belong to Example Co.

## 4. Service or product: pick the frame

Decide which frame the offering takes, from the input. Apply the A rules (architecture) and P rules (prototype) in `${CLAUDE_SKILL_DIR}/../offering-package/references/decision-rules.md`, and record every answer with the sentence it rests on in the build folder's `decisions.json`, in that file's shape and vocabulary (`architecture`: full, card or none; `prototype`: full, screens or none). `offering-package` reads it and does not re-decide:

- **Product** (P1 and P2 true): a buyer or user works in a screen the brand controls (P1), and gets value without a person from the brand doing the work for that user (P2).
- **Service** (P1 false): people from the brand do the work.
- **Hybrid** (P1 true, P2 false): a service with a portal.

Both frames keep exactly three phases, because the look is built for three.

| | Service frame | Product frame |
|---|---|---|
| The three phases | Engagement phases, under the offering's own names (the brand's delivery model, if it has one, maps onto them) | The customer's journey with the product, under the offering's own names (for example set up, measure, act) |
| Roles | People: the brand's team, then the client | The product team (owner, engineer, delivery, support), then the customer's roles |
| Approval tests | Sign-off by a named person | Acceptance and release gates with evidence, confirmed by a named person |
| Task cards | What the brand's people do at each step | What the product does at each step; `platform` for the platforms it reads, `own` for its design |

## 5. Outline, then stop once

When the input is thin (a website, an idea, short notes), get two reads before writing the outline. Each runs once, as a separate agent, at the same time; where no agent can be started, do each read yourself from the question below and say so on the evidence slide.

- **Product challenge**: who the buyer is, what problem they have today, and the riskiest assumptions in the offering.
- **Market scan**: how others package and sell this kind of work, read from their own pages. Competitor names and facts stay out of the deck.

Write the outline and send it to the requester. Ask one pop-up question: build from it, or change it. This is the only stop. After the answer, run to the end without asking anything else; where a choice comes up, make it and mark it open.

The outline holds: the brand and frame; the offering name and tagline; the three phases, with the name the offering uses for each and what each settles; the steps in each phase with every task name; the deliverables and who approves them in each phase; which optional cross-phase slides are included and why; and how many items will be marked as Claude's proposals; and the slide count with where each folded step went.

**Slide cap: 22, target 20.** A deck that cannot be read in one sitting does not get decided, so the cap is fixed. Only the requester can lift it, by naming a larger number; never propose it.

- Floor: 18 (cover, two opening slides, four per phase with one step slide each, evidence, sources, decisions), plus one when the brand has a delivery model.
- One step slide per phase by default. One page holds, at full card length: nine grid cards with no `bands`; six grid cards with one band; or three grid cards with up to three bands (bands of up to three cards). Anything more spills to a second page and costs a slide.
- When the input has more steps than slides, fold them: the phase's main step takes the grid, each other input step becomes a `bands` row under its own name, and its tasks are condensed to the cards that carry a decision or a source. Every input step's sign-off moves to the phase's deliverables-and-approval slide, so no approval is lost.
- A second step slide in a phase only when its approval gate cannot share a slide with the first (different approver and different deliverable). At most one per phase.
- At most one optional cross-phase slide (`tiers`, `cards`, `panel`), the one the decision makers most need.
- Every 26 sources add a sources page. Cite the strongest source per card; drop a second source that adds nothing.
- Count before writing the outline. The outline states the count and, for every input step folded or optional slide left out, one line saying where its content went.

Test the outline before sending it: would the decision makers be proud to show this, and could three people run phase one from it? If not, fix the structure first.

Unattended (a scheduled run, or no answer): take the most reasonable reading, say at the top of the final report which reading you took, and carry on.

## 6. Research and tag

For every task card and every rule, look for an official source: the own documentation page of the company that makes the platform, tool or system; a government body; a standards body; a professional body. Not blogs, agencies, vendor marketing or AI summaries.

- **Open the page before citing it.** A search result is a lead. If the page will not open, do not cite it.
- Keep `source_notes.json` in the build folder as you go: for each source its name ("Publisher: short topic"), URL, the date opened, and in a few of your own words what the page says that backs each card that cites it.
- Tag each card by what the opened page says:

| Tag | Use it when |
|---|---|
| `platform` | The maker's own page says what the card says. |
| `official` | A government, standards or professional body says what the card says. |
| `own` | It is the brand's design. A link may sit on the card as background; write "Background, not backing:" in the note. |
| `open` | It is not validated, or it is your proposal and the decision makers have not decided it. |

- A card claims no more than its page. Every number, date and limit on a card is on the page.
- **Your own proposals are tagged `open`**, carry the note "Proposed by Claude. <Decision makers> to confirm.", and are listed on the decisions slide. Never present a proposal as the brand's decision.
- No names of experts, contractors or clients unless the input gives them.
- No fees, prices, rates, hours or revenue promises anywhere in the deck. `check_spec_brand.py` fails the spec on a currency symbol or "per month".

## 7. Write the spec

Write one JSON file in the build folder that follows `SPEC.md`. Start from the example's shape.

- Plain words, American English, short sentences. Say what a thing is; do not sell it. A newcomer must understand every line with nothing explained.
- The levels are offering, phase, step and task.
- Row labels are Inputs, Activities, Deliverables, Approval and Roles.
- Name the parties: the client or customer, the brand, a job title, a specialist contractor. Never "we" or "you".
- Spell out an acronym at first use. Write dates month-day-year. No serial comma.
- Label an expert's view as one person's view.
- Where housing, employment, credit or health rules apply, the offering works inside them, never around them.
- A headline states a finding or a count ("Step 1.1 Audit: nine tasks, eight tied to an outside source"). Count before you write a number.
- Never type a slide number. Use `{slide:REF}`.
- Version starts at "Draft v0.1". The cover disclaimer is true for this offering: who has and has not approved it, whether anyone has bought it or run it, and that Claude drafted it from the named input.
- Cross-phase slides: always `evidence`, `sources`, `decisions`. Add `tiers`, `cards` or `panel` only when the offering has that content. Leave out a slide rather than fill it.
- Evidence slide: run `python3 ${CLAUDE_SKILL_DIR}/scripts/evidence_counts.py <spec> --write`; it sets the four tiles and fails if an open card is missing from the decisions slide. Its note line says how and when the sources were checked, as it actually happened.
- Decisions slide: first the decisions the offering cannot go ahead without, then every open item (grouped where there are many), then next steps.

## 8. Check, render, fix, look

Task progress (copy and tick off):

- [ ] `python3 ${CLAUDE_SKILL_DIR}/scripts/check_spec_brand.py <spec> ${CLAUDE_SKILL_DIR}/brands/<brand>`. Fix every line it prints. Only proceed when it prints "pass".
- [ ] `python3 ${CLAUDE_SKILL_DIR}/render.py <spec> "<deck name>.pptx" --brand ${CLAUDE_SKILL_DIR}/brands/<brand>`. Fix every line under MUST FIX by shortening the text in the spec. Run again until the exit code is 0. Never change `render.py`, a brand pack's colors or a font size to make one deck fit.
- [ ] `python3 ${CLAUDE_SKILL_DIR}/tools/preview.py "<deck name>.pptx" preview/`, then look at every contact sheet, and open any slide that looks crowded. Look for text outside its box, text over text, a nearly empty slide, a headline whose count does not match the cards, and a `platform` or `official` card with no source.
- [ ] Search the deck's text for every other brand's name (the packs in `brands/` list them). Zero hits.

## 9. Three reads, once each

Decision makers rely on this deck, so people who did not write it check it. Start three separate agents at the same time; none has seen the drafting. Give each the spec and the source notes.

| Read | What it checks | What to do with the findings |
|---|---|---|
| **Compliance** | What the offering cannot say or do as written, and which clients or cases need extra steps. | Fix the wording. Put special cases on the `panel` slide and questions for a lawyer on the decisions slide. This is not legal advice; say so. |
| **Wording** | Claims with no support, promises of results, mixed terms, and the rules in section 7. | Fix the wording. |
| **Sources** | It reopens each cited page and reports, for every `platform` and `official` card: backed, partly backed, not backed, or page did not open. It also checks that every `open` item is on the decisions slide and that the evidence counts match the spec. | Reword the card to what the page says, or change the tag to `own` or `open`. |

Apply the findings in that order and render again. Do one round, then stop; a second round mostly finds faults made by the first round's fixes.

If no separate agent can be started (claude.ai chat ignores agents), do the three reads yourself and say on the evidence slide that the check was not independent.

## 10. Deliver

- File name: `<file_prefix><Offering name>_Offering deck - <YYYY-MM-DD>_v0.1_Draft.pptx` for a draft; later drafts count up (v0.2, v0.3).
- Place: the folder the requester names. If none is named, send the file in the conversation. Drafts are not uploaded anywhere.
- Beside the deck, a subfolder "Build files - <offering name> (working parts, not for reading)" holding the spec, `source_notes.json` and `decisions.json`. `offering-package` and any later revision need them.

**When a deck is final.** Drive holds the record, so only a deck the requester has seen and called final goes there.

- Trigger: in a later message, the requester calls a delivered deck final. "Final" in the first request does not count. "Final once you fix X": fix, send back, copy on confirmation. Unattended runs never copy; they say the deck is ready to copy.
- Relabel: version v1.0 (or the version named, or the next whole number after an earlier final); remove "Draft" from the eyebrow, `status_line` and `footer_parts`; the cover disclaimer says who called it final and when. Render and check (section 8). File: `<file_prefix><Offering name>_Offering deck - <date made final>_v1.0.pptx`.
- Folder: ask once per conversation; reuse it.
- Permissions, before every copy: a file takes its folder's access. If anyone besides the requester can open the folder (people, groups, the whole organization, Shared Drive members, anyone with the link, another owner), say who and ask. If permissions cannot be read, say so and ask. If the answer is no, ask for another folder or send the files in the conversation. Never share or change sharing.
- Copy: the .pptx as is, plus "Build files - <offering name> v1.0" holding exactly the spec, `source_notes.json` and `decisions.json`. A later final sits beside the earlier one; never overwrite.
- Report the Drive link. With no Drive connector, say so and send the files in the conversation.
- Report in a few lines: the file and its slide count; the brand and frame; how many sources were opened; how many items are open, and the few that most need a decision; anything left out, and why. Do the work that is in scope instead of offering it.

## Other skills

Use these when they are listed in the session. Each read runs once. If a skill is not listed, the agent does that read from the question in this file.

| Step | Skill | Used for |
|---|---|---|
| 3 | deep-research | The first scan of the field. Its report is a lead; section 6 still applies to every page a card cites. |
| 5 | product-management:product-brainstorming | The product challenge. |
| 5 | marketing:competitive-brief | The market scan. |
| 5 | proud-work-bar (any version) | The test of the outline. |
| 9 | legal:compliance-check or product-legal:marketing-claims-review | The compliance read. |
| 9 | marketing:brand-review | The wording read, against section 7. |
| 9 | red-team and completion-gate (any version) | The sources read and the last check before delivery. |

Do not run a design review or use a presentation or design skill on the deck. The renderer draws every slide, and the look is locked. It does not rely on color alone: every tag, open seat and status is also written in words.

## Changing a deck later

Change the spec and render again. Never edit the PowerPoint from code. If someone has edited the deck by hand, read that version first and carry the changes into the spec.

## Changing the look or a brand pack

The look (`render.py`) changes only when Tait Goodwin, the plugin's owner, asks. Change it in a working copy, run the private repo's v0.9 regression before and after, and say that the change applies to every future deck. A brand pack changes when its owner asks (AugMind and Levarum: Tait); re-run `tests/smoke_test.sh` after. Colors in a pack must keep white text readable on `accent` and dark text readable on `page`, `white`, `gray` and `accent_soft`.
