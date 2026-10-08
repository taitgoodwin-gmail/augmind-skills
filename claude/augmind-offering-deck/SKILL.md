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

- Plain words, American English, short sentences. Say what a thing is; do not sell it.
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

## 7. One independent read

Partners rely on this deck, so someone who did not write it checks it once.

Start a separate agent that has not seen the drafting. Give it the spec and the source notes. It reopens each cited page and reports, for every `platform` and `official` card: backed, partly backed, not backed, or page did not open. It also checks that every `open` item is on the decisions slide and that the evidence counts match the spec.

Fix what it finds: reword the card to what the page says, or change the tag to `own` or `open`. Render again. Do one round, then stop; a second round mostly finds faults made by the first round's fixes.

If no separate agent can be started, reread the pages yourself and say on the evidence slide that the check was not independent.

## 8. Deliver

- File name: `AugMind_<Offering name>_Offering deck - <YYYY-MM-DD>_v0.1_Draft.pptx`.
- Place: the folder Tait names. If he names none, the Desktop folder "AugMind Offering Template" when the session can reach his computer; otherwise send the file in the conversation. Do not upload to Google Drive unless he asks.
- Beside the deck, in a subfolder named "Build files - <offering name> (working parts, not for reading)", save the spec and the source notes. A later session needs them to revise the deck.
- Report in a few lines: the file and its slide count; how many sources were opened; how many items are open, and the few that most need a partner decision; anything that was left out, and why. Do the work that is in scope instead of offering it.

## Other skills

This skill is complete without any other. Use these when they are listed in the session:

- **deep-research**: for the first scan of the field before the outline (what the work involves, and which platform makers and official bodies publish rules for it). Its report is a lead. Every page a card cites is still opened under section 4.
- **proud-work-bar** (any version): at the outline, in section 3.
- **red-team** and **completion-gate** (any version): for the independent read in section 7 and before delivery. If they are not listed, sections 6 and 7 are the check.

Formatting needs no other skill. Do not use a presentation or design skill; the renderer draws every slide. Website copy comes later, through offering-site-copy, and is not part of this skill.

## Changing a deck later

Change the spec and render again. Never edit the PowerPoint from code. If Tait has edited the deck by hand, read his version first and carry his changes into the spec.

## Changing the look

Only when Tait asks. Change `render.py` on a branch, run `tests/run_regression.sh`, and tell him the change applies to every future deck.
