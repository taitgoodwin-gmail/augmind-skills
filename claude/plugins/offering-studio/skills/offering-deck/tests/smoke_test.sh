#!/bin/bash
# Smoke test: the renderer runs, the neutral example renders with nothing to fix (with the neutral pack and
# with no pack), and the brand check passes on it. Run before any deck: bash smoke_test.sh <working folder>.
# The byte-for-byte v0.9 regression (confidential fixture) lives in the private repo, not in this plugin.
set -e
set -o pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SK="$HERE/.."
OUT="${1:-/tmp/offering-deck-smoke}"
mkdir -p "$OUT"
python3 -c "import pptx, PIL, lxml" || { echo "install python-pptx Pillow lxml first"; exit 1; }
python3 "$SK/scripts/check_spec_brand.py" "$SK/examples/spec_example_v0.1.json" "$SK/brands/neutral"
python3 "$SK/render.py" "$SK/examples/spec_example_v0.1.json" "$OUT/example_neutral.pptx" --brand "$SK/brands/neutral" | sed -n "1,2p"
python3 "$SK/render.py" "$SK/examples/spec_example_v0.1.json" "$OUT/example_default.pptx" | sed -n "2p"
echo "smoke test passed: see $OUT"
