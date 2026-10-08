#!/bin/bash
# Regression test: rebuild the v0.9 deck from the example spec and compare every word and link with the
# deck data read from Google Slides on 2026-10-07. Run this after any change to render.py.
# Pass = "MUST FIX ... 0", 26 slides, and "slides with any difference: 0".
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-/tmp/offering-deck-regression}"
mkdir -p "$OUT"
python3 "$HERE/../render.py" "$HERE/../examples/spec_digital-marketing_v0.9.json" "$OUT/v0.9_rebuilt.pptx"
python3 "$HERE/check_words_against_v0.9.py" "$HERE/v0.9_deck_data.json" "$OUT/v0.9_rebuilt.pptx"
# Second check: the sizes stated in SPEC.md still fit. Pass = "MUST FIX ... 0" again.
python3 "$HERE/make_limit_spec.py" "$HERE/../examples/spec_digital-marketing_v0.9.json" "$OUT/limit_spec.json"
python3 "$HERE/../render.py" "$OUT/limit_spec.json" "$OUT/limit_test.pptx" | sed -n "1,2p"
