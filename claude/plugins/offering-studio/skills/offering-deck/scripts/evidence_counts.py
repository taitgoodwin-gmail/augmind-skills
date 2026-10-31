#!/usr/bin/env python3
"""Count what the evidence slide reports, from the spec itself. Never type these numbers from memory.

Usage: evidence_counts.py <spec.json> [--write]
Prints: sources in the register, sources opened live, task cards by tag, open items, and whether every
open card is named on the decisions slide. With --write, sets the four evidence tiles in the spec:
  tile 1 = sources opened live, tile 2 = cards tagged platform or official,
  tile 3 = cards tagged own, tile 4 = cards tagged open (tone open).
Edit the tile texts yourself if the deck counts something else; the script only sets the numbers.
"""
import json
import re
import sys


def cards(spec):
    for ph in spec.get("phases", []):
        for st in ph.get("steps", []):
            for t in st.get("tasks", []):
                yield t
            for band in st.get("bands", []) or []:
                for t in band.get("cards", []):
                    yield t
            if st.get("mapping"):
                yield st["mapping"]
    for v in spec.get("all_phases", []):
        for t in v.get("cards", []) or []:
            if isinstance(t, dict) and "tag" in t:
                yield t


def main():
    path = sys.argv[1]
    spec = json.load(open(path))
    tags = {"platform": 0, "official": 0, "own": 0, "open": 0}
    open_numbers = []
    for c in cards(spec):
        tags[c.get("tag", "open")] = tags.get(c.get("tag", "open"), 0) + 1
        if c.get("tag") == "open" and c.get("number"):
            open_numbers.append(str(c["number"]))
    sources = spec.get("sources", [])
    live = sum(1 for s in sources if s.get("status", "").lower().startswith("opened live"))
    decisions = [v for v in spec.get("all_phases", []) if v.get("type") == "decisions"]
    dec_text = json.dumps(decisions) if decisions else ""
    missing = [n for n in open_numbers if not re.search(re.escape(n), dec_text)]
    print(f"sources: {len(sources)} in register, {live} opened live")
    print("cards by tag:", tags)
    print(f"open cards: {len(open_numbers)}; not named on the decisions slide: {missing or 'none'}")
    if "--write" in sys.argv:
        for v in spec.get("all_phases", []):
            if v.get("type") == "evidence" and len(v.get("tiles", [])) == 4:
                v["tiles"][0]["number"] = str(live)
                v["tiles"][1]["number"] = str(tags["platform"] + tags["official"])
                v["tiles"][2]["number"] = str(tags["own"])
                v["tiles"][3]["number"] = str(tags["open"])
                v["tiles"][3]["tone"] = "open"
        json.dump(spec, open(path, "w"), indent=2, ensure_ascii=False)
        print("evidence tiles written")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
