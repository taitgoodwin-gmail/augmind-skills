# AugMind offering deck renderer

This folder holds the working parts behind the skill `augmind-offering-deck-v1-2026-10-07`. The skill turns an input (a website, an existing offering, notes, files, an article or an idea) into an AugMind offering deck. The parts here draw that deck as a PowerPoint file in the locked look of "Digital Marketing Performance & Revenue" v0.9.

Added 2026-10-07.

## What is here

| File or folder | What it is |
|---|---|
| `SKILL.md` | A copy of the skill's instructions. The live copy is the one saved in Tait's Claude skills. |
| `SPEC.md` | The reference for the offering spec: every field, and how much text fits in it. |
| `render.py` | Reads a spec (JSON) and writes the deck (.pptx). Checks that all text fits and reports what does not. |
| `examples/spec_digital-marketing_v0.9.json` | The spec that rebuilds the v0.9 deck word for word. The model for every new spec. |
| `assets/augmind-logo-cover.png` | The logo placed on the cover (Teal and Silver, white background, cropped). |
| `fonts/` | Inter Regular and Bold, used to measure text, with the font's license. |
| `tools/preview.py` | Turns a deck into pictures so every slide can be looked at. |
| `tests/run_regression.sh` | Rebuilds v0.9 and compares every word and link with the deck data read from Google Slides. Then checks that the sizes in `SPEC.md` still fit. |
| `tests/v0.9_deck_data.json` | Every element of the v0.9 deck, read from Google Slides on 2026-10-07. |
| `tools/extract_spec_from_v0.9.py`, `tools/redraw_v0.9_slides.py`, `tools/print_v0.9_measurements.py` | One-off tools used to measure v0.9 and to build the example spec. Kept for the record. |

## Run it

```
pip install python-pptx Pillow lxml
python3 render.py examples/spec_digital-marketing_v0.9.json out.pptx
python3 tools/preview.py out.pptx preview/
bash tests/run_regression.sh
```

`render.py` exits with code 0 when nothing must be fixed and code 2 when it printed a MUST FIX line.

## What was checked on 2026-10-07

- The rebuilt v0.9 deck has 26 slides and matches the original on every word and every link (`tests/run_regression.sh`).
- All 26 rebuilt slides were compared by eye with the original, rendered with LibreOffice.
- Every size in `SPEC.md` was filled to its stated length and rendered with nothing overflowing.
- A differently shaped offering (other phase names, one to three steps a phase, three cross-phase slides) rendered without crashing, and the renderer listed the texts that did not fit.

Not checked: how the file looks in PowerPoint, Keynote or Google Slides on a computer without the Inter font installed. The deck names Inter as its font, as v0.9 does, and a .pptx file does not carry its fonts with it.

## Confidential content

The example spec and the test data hold the full text of the v0.9 partner draft, marked AugMind Confidential 2026. Keep this repository private.

## Rules for changing the renderer

1. Change the look only when Tait asks. A change here applies to every future deck.
2. Work on a branch. Run `tests/run_regression.sh` before and after.
3. If a size in `SPEC.md` changes, change the matching number in `tests/make_limit_spec.py`.
4. Never change the renderer to make one deck fit. Shorten that deck's text in its spec.
