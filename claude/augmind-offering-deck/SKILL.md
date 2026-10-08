---
name: "augmind-offering-deck-v1-2026-10-07"
description: "Use when Tait points at a website, an existing offering, notes, files, an article or an idea and wants an AugMind offering deck: researches it, designs the offering on AugMind's three-phase model, and builds the PowerPoint in the locked v0.9 look."
---

# AugMind offering deck from any input (v1, 7 Oct 2026)

Tait points at something: a website, an offering AugMind already has, notes, files, an article or an idea. This skill does the rest. It reads the input, researches it, designs the offering, and builds one deck with the same look and the same elements as "Digital Marketing Performance & Revenue" v0.9.

**Thesis: the deck states what was opened and read, marks everything else as open, and is drawn by the renderer, never by hand.**

## Use / don't use

Use for: a new AugMind offering deck, or a new version of a deck this skill built.
Not for: client sales decks, website copy (that is offering-site-copy), fees or pricing, or a deck in any other look.

## What comes out

One PowerPoint file for the partners and the subject experts, about 20 to 30 slides: the cover; three opening slides (where the offering fits the AugMind model, the offering on one page, roles); three phases, each with an overview, inputs and roles, one slide of task cards per step, and deliverables and approval; then the cross-phase slides, which always end with evidence, the source register and the decisions the partners must make.

A full run takes more than an hour. Say so in one line at the start.

## 1. Get the renderer and prove it runs

The renderer lives in Tait's private GitHub repository `taitgoodwin-gmail/augmind-skills`, in the folder `claude/augmind-offering-deck/`. Attach the repository to the session and clone it. If the folder is not on the default branch, look on the branch `claude/offering-deck-renderer`.

1. Run `bash tests/run_regression.sh`. It must print 26 slides, `MUST FIX ... 0` twice, and `slides with any difference: 0`. Install `python-pptx`, `Pillow` and `lxml` first if they are missing.
2. Read `SPEC.md` and `examples/spec_digital-marketing_v0.9.json` in full. The example is the model for structure, length and tone.

If the repository cannot be reached or the test fails, stop and say exactly that. Do not draw the deck another way. The look is locked in `render.py`.

## 2. Read the input. Never draft from memory.

Open every input in full before designing anything. If one cannot be opened, name it and carry on with the rest.

| Input | How to treat it |
|---|---|
| Another company's website | A lead, not a source. It shows what the market sells and the words buyers use. AugMind builds its own offering. Do not copy its wording, cite it as evidence, or name the company in the deck. |
| An AugMind offering, deck or document | Authoritative for AugMind's own choices. Keep its names, decisions and wording. Fill gaps as open items. |
| Notes or an idea | Everything the notes do not say is a proposal. |
| Files, GitHub requirements, an article | Read in full. An article is a lead unless it is itself an official source. |

Take from the Digital Marketing deck its structure only. Its content decisions (its roles, its reviewer rule, one agreement per phase) belong to that offering. Reuse one only when the input says so; otherwise it is a proposal.

## 3. Outline, then stop once

When the input is thin (a website, an idea, short notes), get two reads before writing the outline. Each runs once, as a separate agent, at the same time:

- **Product challenge**: who the buyer is, what problem they have today, and the riskiest assumptions in the offering.
- **Market scan**: how others package and sell this kind of work, read from their own pages.

Use both to shape the outline. What comes from them is a proposal. Competitor names and facts stay out of the deck.

Write the outline and send it to Tait. Ask one pop-up question: build from it, or change it. This is the only stop. After the answer, run to the end without asking anything else; where a choice comes up, make it and mark it open.

The outline holds: the offering name and tagline; the three phases, with the name the offering uses for each and what each settles; the steps in each phase with every task name; the deliverables and who approves them in each phase; which optional cross-phase slides are included and why; and how many items will be marked as Claude's proposals.

Test the outline before sending it: would the partners be proud to show this, and could three people run phase one from it? If not, fix the structure first.

If Tait is not there (a scheduled or unattended run), take the most reasonable reading, say at the top of the final report which reading you took, and carry on.

## 4. Research and tag

For every task card and every rule, look for an official source: the own documentation page of the company that makes the platform, tool or system; a government body; a standards body; a professional body. Not blogs, agencies, vendor marketing or AI summaries.

- **Open the page before citing it.** A search result is a lead. If the page will not open, do not cite it.
- Keep working notes as you go (`source_notes.json`): for each source its name ("Publisher: short topic"), URL, the date opened, and in a few of your own words what the page says that backs each card that cites it.
- Tag each card by what the opened page says:

| Tag | Use it when |
|---|---|
| `platform` | The maker's own page says what the card says. |
| `official` | A government, standards or professional body says what the card says. |
| `own` | It is AugMind's design. A link may sit on the card as background; write "Background, not backing:" in the note. |
| `open` | It is not validated, or it is your proposal and the partners have not decided it. |

- A card claims no more than its page. Every number, date and limit on a card is on the page.
- **Your own proposals are tagged `open`**, carry the note "Proposed by Claude. Partners to confirm.", and are listed on the decisions slide. Never present a proposal as AugMind's decision.
- No names of experts, contractors or clients unless the input gives them.
- No fees, prices, rates, hours or revenue promises anywhere in the deck.

## 5. Write the spec

Write one JSON file that follows `SPEC.md`. Start from the example's shape.

- Plain words, American English, short sentences. Say what a thing is; do not sell it. A newcomer must understand every line with nothing explained.
- The levels are offering, phase, step and task. "The AugMind model" is Advise, Implement, Operate; do not call those three phases.
- Row labels are Inputs, Activities, Deliverables, Approval and Roles.
- Name the parties: the client, AugMind, a job title, a specialist contractor. Never "we" or "you".
- Spell out an acronym at first use. Write dates month-day-year. No serial comma.
- Label an expert's view as one person's view.
- Where housing, employment, credit or health rules apply, the offering works inside them, never around them.
- A headline states a finding or a count ("Step 1.1 Audit: nine tasks, eight tied to an outside source"). Count before you write a number.
- Never type a slide number. Use `{slide:REF}`.
- Keep the example's standing lines (eyebrow, tab labels, legend, footer pieces). Change the name, version (start at "Draft v0.1"), date and status.
- The cover disclaimer is true for this offering: who has and has not approved it, whether anyone has bought it or run it, and that Claude drafted it from the named input.
- Cross-phase slides: always `evidence`, `sources`, `decisions`. Add `tiers`, `cards` or `panel` only when the offering has that content. Leave out a slide rather than fill it.
- Evidence slide: compute every count from the spec with a short script (sources opened, cards by tag, proposals). Its note line says how and when the sources were checked, as it actually happened.
- Decisions slide: first the decisions the offering cannot go ahead without, then every open item (grouped where there are many), then next steps.

## 6. Render, fix, look

1. `python3 render.py <spec>.json "<deck name>.pptx"`
2. Fix every line under MUST FIX by shortening the text in the spec. Run again until the exit code is 0. Never change `render.py` or a font size to make one deck fit.
3. `python3 tools/preview.py "<deck name>.pptx" preview/`, then look at every contact sheet, and open any slide that looks crowded. Look for text outside its box, text over text, a nearly empty slide, and a `platform` or `official` card with no source.

## 7. Three reads, once each

Partners rely on this deck, so people who did not write it check it. Start three separate agents at the same time. None has seen the drafting. Give each the spec and the source notes.

| Read | What it checks | What to do with the findings |
|---|---|---|
| **Compliance** | What the offering cannot say or do as written, and which clients or cases need extra steps. | Fix the wording. Put special cases on the `panel` slide and questions for a lawyer on the decisions slide. This is not legal advice; say so. |
| **Wording** | Claims with no support, promises of results, mixed terms, and the wording rules in section 5. | Fix the wording. |
| **Sources** | It reopens each cited page and reports, for every `platform` and `official` card: backed, partly backed, not backed, or page did not open. It also checks that every `open` item is on the decisions slide and that the evidence counts match the spec. | Reword the card to what the page says, or change the tag to `own` or `open`. |

Apply the findings in that order and render again. Do one round, then stop; a second round mostly finds faults made by the first round's fixes.

If no separate agent can be started, do the three reads yourself and say on the evidence slide that the check was not independent.

## 8. Deliver

- File name: `AugMind_<Offering name>_Offering deck - <YYYY-MM-DD>_v0.1_Draft.pptx`.
- Place: the folder Tait names. If he names none, the Desktop folder "AugMind Offering Template" when the session can reach his computer; otherwise send the file in the conversation. Do not upload to Google Drive unless he asks.
- Beside the deck, in a subfolder named "Build files - <offering name> (working parts, not for reading)", save the spec and the source notes. A later session needs them to revise the deck.
- Report in a few lines: the file and its slide count; how many sources were opened; how many items are open, and the few that most need a partner decision; anything that was left out, and why. Do the work that is in scope instead of offering it.

## Other skills

Use these when they are listed in the session. The product, market, compliance and wording reads are the ones the Digital Marketing deck went through. Each read runs once.

| Step | Skill | Used for |
|---|---|---|
| 2 | deep-research | The first scan of the field: what the work involves, and which makers and official bodies publish rules for it. Its report is a lead; section 4 still applies to every page a card cites. |
| 3 | product-management:product-brainstorming | The product challenge. |
| 3 | marketing:competitive-brief | The market scan. |
| 3 | proud-work-bar (any version) | The test of the outline. |
| 7 | legal:compliance-check | The compliance read. |
| 7 | marketing:brand-review | The wording read, against section 5. |
| 7 | red-team and completion-gate (any version) | The sources read and the last check before delivery. |

If a skill is not listed, the agent does that read from the question in this file.

Do not run a design review or use a presentation or design skill. The renderer draws every slide, and the look is locked. It does not rely on color alone: every tag, open seat and status is also written in words. Website copy comes later, through offering-site-copy, and is not part of this skill.

## Changing a deck later

Change the spec and render again. Never edit the PowerPoint from code. If Tait has edited the deck by hand, read his version first and carry his changes into the spec.

## Changing the look

Only when Tait asks. Change `render.py` on a branch, run `tests/run_regression.sh`, and tell him the change applies to every future deck.
