#!/usr/bin/env python3
"""Check the package's HTML files against the deck spec.

Usage: check_package.py <spec.json> <build folder> [--brand <id>] [--brands-dir <folder of brand packs>]
The brand comes from --brand or from decisions.json in the build folder.
Reads every .html under the build folder (home-page/, prototype/, architecture/). For each file it reports:
  resolved    data-claim values that name a card in the spec with tag platform, official or own
  unresolved  data-claim values that name no card
  open        data-claim values that name a card tagged open (cannot ship)
  prices      currency symbols or per-month wording in the file's text
  other brands  names of other brand packs found in the file's text
Exit 0 ("pass") only when every file has unresolved 0, open 0, prices 0 and other brands 0.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

CLAIM = re.compile(r'data-claim="([^"]+)"')
PRICE = re.compile(r"[$€£]\s?\d|\b\d+\s?(USD|EUR|GBP)\b|\bper (month|hour|year|seat)\b|/\s?(month|mo|hour|hr|yr)\b", re.I)


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def cards(spec):
    """Every card with a number: task cards, band cards, the mapping card, and cross-phase rule cards.
    Keep in step with evidence_counts.py in offering-deck."""
    out = {}
    for ph in spec.get("phases", []):
        for st in ph.get("steps", []):
            for t in st.get("tasks", []):
                if t.get("number"):
                    out[str(t["number"])] = t.get("tag", "open")
            for band in st.get("bands", []) or []:
                for t in band.get("cards", []):
                    if t.get("number"):
                        out[str(t["number"])] = t.get("tag", "open")
            if st.get("mapping") and st["mapping"].get("number"):
                out[str(st["mapping"]["number"])] = st["mapping"].get("tag", "open")
    for v in spec.get("all_phases", []):
        for t in v.get("cards", []) or []:
            if isinstance(t, dict) and t.get("number"):
                out[str(t["number"])] = t.get("tag", "open")
    return out


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    spec = json.load(open(args[0]))
    folder = args[1]
    brands_dir = args[args.index("--brands-dir") + 1] if "--brands-dir" in args else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "offering-deck", "brands")
    own = args[args.index("--brand") + 1] if "--brand" in args else None
    if own is None:                                  # the deck's build folder records the brand
        dpath = os.path.join(folder, "decisions.json")
        if os.path.exists(dpath):
            own = os.path.basename(json.load(open(dpath)).get("brand", "") or "")
    if own is None:
        sys.exit("name the deck's brand: --brand <id>, or run in a build folder that has decisions.json")
    others = []
    if os.path.isdir(brands_dir):
        for d in sorted(os.listdir(brands_dir)):
            p = os.path.join(brands_dir, d, "brand.json")
            if os.path.exists(p) and d != own:
                b = json.load(open(p))
                others += [n for n in (b.get("brand_name"), b.get("company"), *b.get("former_names", [])) if n]
            elif os.path.exists(p):              # the deck's own brand: its former names must not appear either
                others += json.load(open(p)).get("former_names", [])
    tag_of = cards(spec)
    files = [os.path.join(r, f) for r, _, fs in os.walk(folder) for f in fs if f.endswith(".html")]
    if not files:
        sys.exit(f"no .html files under {folder}")
    ok = True
    for path in sorted(files):
        html = open(path, encoding="utf-8").read()
        claims = CLAIM.findall(html)
        resolved = [c for c in claims if tag_of.get(c) in ("platform", "official", "own")]
        unresolved = [c for c in claims if c not in tag_of]
        opened = [c for c in claims if tag_of.get(c) == "open"]
        t = Text()
        t.feed(html)
        text = " ".join(t.parts)
        prices = PRICE.findall(text)
        brands = [n for n in others if re.search(r"\b" + re.escape(n) + r"\b", text)]   # case-sensitive: "Signal", not "a signal of"
        rel = os.path.relpath(path, folder)
        print(f"{rel}: resolved {len(resolved)}, unresolved {len(unresolved)} {unresolved or ''}, open {len(opened)} {opened or ''}, prices {len(prices)}, other brands {brands or 0}")
        if unresolved or opened or prices or brands:
            ok = False
    print("pass" if ok else "FAIL: fix every unresolved or open claim, remove prices, remove other brand names")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
