#!/usr/bin/env python3
"""Check a deck spec against its brand pack before rendering.

Usage: check_spec_brand.py <spec.json> <brand folder> [--brands-dir <folder of packs>]
Exit 0 when every check passes; exit 1 with one line per failure otherwise.

Checks:
  1. No other brand's name appears anywhere in the spec (the packs in --brands-dir define the names;
     the pack's own brand_name and company are allowed). Catches "modeled on the AugMind deck".
  2. The legend's "own" label matches the brand pack's own_label.
  3. No fees, prices or rates: currency symbols, "USD", "per month", "/month", "per hour".
  4. start.model_map is present only when the brand pack has a delivery model (words.model), and
     start.views has one label per start slide.
  5. Every source name a card cites is in the register (the renderer also checks this; here it fails early).
"""
import json
import os
import re
import sys

PRICE = re.compile(r"[$€£]\s?\d|\b\d+\s?(USD|EUR|GBP)\b|\bper (month|hour|year|seat)\b|/\s?(month|mo|hour|hr|yr)\b", re.I)


def walk(node, path="spec"):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, f"{path}.{k}")


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    spec_path, brand_dir = args[0], args[1]
    brands_dir = args[args.index("--brands-dir") + 1] if "--brands-dir" in args else os.path.dirname(os.path.abspath(brand_dir))
    spec = json.load(open(spec_path))
    brand = json.load(open(os.path.join(brand_dir, "brand.json")))
    own_names = {brand.get("brand_name", ""), brand.get("company", "")} - {""}
    failures = []

    other_names = set()
    for d in sorted(os.listdir(brands_dir)):
        p = os.path.join(brands_dir, d, "brand.json")
        if os.path.exists(p):
            b = json.load(open(p))
            for n in (b.get("brand_name"), b.get("company"), *b.get("former_names", [])):
                if n and n not in own_names:
                    other_names.add(n)        # another brand, or a name this or another brand no longer uses
    former = set(brand.get("former_names", []))
    for path, text in walk(spec):
        for n in other_names:
            if re.search(r"\b" + re.escape(n) + r"\b", text):      # case-sensitive: "Signal", not "a signal of"
                kind = "former name" if n in former else "other brand"
                failures.append(f"{kind} '{n}' at {path}: {text[:70]!r}")
        if PRICE.search(text):
            failures.append(f"price or rate at {path}: {text[:70]!r}")

    legend_own = [row[0] for row in spec.get("legend", []) if len(row) > 1 and row[1] == "own"]
    if legend_own and legend_own[0] != brand.get("own_label"):
        failures.append(f"legend 'own' label is {legend_own[0]!r}; brand pack says {brand.get('own_label')!r}")

    start = spec.get("start", {})
    has_model = bool(brand.get("words", {}).get("model"))
    if "model_map" in start and not has_model:
        failures.append("start.model_map is present but the brand pack has no delivery model (words.model is null)")
    if has_model and "model_map" not in start:
        failures.append("brand pack has a delivery model but start.model_map is missing")
    present = [k for k in ("model_map", "matrix", "roles") if k in start]
    if len(start.get("views", [])) != len(present):
        failures.append(f"start.views has {len(start.get('views', []))} labels for {len(present)} start slides")

    register = {s["name"] for s in spec.get("sources", [])}
    for path, text in walk(spec):
        if path.endswith("]") and ".sources[" in path and text not in register:
            failures.append(f"cited source not in register at {path}: {text!r}")

    if failures:
        print(f"check_spec_brand: {len(failures)} failure(s)")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("check_spec_brand: pass (no other brand names, no prices, legend and start section match the pack)")


if __name__ == "__main__":
    main()
