#!/usr/bin/env python3
"""Check financials.json before the financial model sheet is built.

Usage: check_financials.py <financials.json>

Fails when a line has no tag or an unknown tag, a platform or official line lacks source, url or opened date,
low/base/high are missing or out of order, a price line is tagged platform or official, or an id repeats.
Prints one line per failure, then a count of lines by tag. Exit code 0 only on "pass".
"""
import json
import sys

TAGS = {"platform", "official", "own", "open"}
GROUPS = {"cost", "capacity", "price", "volume"}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    data = json.load(open(sys.argv[1]))
    failures, seen, counts = [], set(), {t: 0 for t in TAGS}
    for key in ("brand", "offering", "currency", "as_of", "lines"):
        if not data.get(key):
            failures.append(f"missing top-level '{key}'")
    for i, line in enumerate(data.get("lines", [])):
        lid = line.get("id") or f"line {i + 1}"
        if lid in seen:
            failures.append(f"{lid}: id used twice")
        seen.add(lid)
        tag, group = line.get("tag"), line.get("group")
        if tag not in TAGS:
            failures.append(f"{lid}: tag {tag!r} is not one of {sorted(TAGS)}")
        else:
            counts[tag] += 1
        if group not in GROUPS:
            failures.append(f"{lid}: group {group!r} is not one of {sorted(GROUPS)}")
        if not line.get("name") or not line.get("unit"):
            failures.append(f"{lid}: needs a name and a unit")
        vals = [line.get(k) for k in ("low", "base", "high")]
        if not all(isinstance(v, (int, float)) for v in vals):
            failures.append(f"{lid}: low, base and high must all be numbers")
        elif not vals[0] <= vals[1] <= vals[2]:
            failures.append(f"{lid}: low <= base <= high is not true ({vals})")
        if tag in ("platform", "official"):
            missing = [k for k in ("source", "url", "opened", "basis") if not line.get(k)]
            if missing:
                failures.append(f"{lid}: a {tag} line needs {', '.join(missing)}")
        if tag == "open" and not line.get("basis"):
            failures.append(f"{lid}: an open line needs a basis (why it is open, who confirms it)")
        if group == "price" and tag in ("platform", "official"):
            failures.append(f"{lid}: a price is the brand's decision; tag it open (proposed) or own (decided)")
    summary = ", ".join(f"{t} {counts[t]}" for t in ("platform", "official", "own", "open"))
    if failures:
        print(f"check_financials: {len(failures)} failure(s)")
        for f in failures:
            print("  - " + f)
        print("lines by tag: " + summary)
        sys.exit(1)
    print(f"check_financials: pass ({len(data['lines'])} lines; {summary})")


if __name__ == "__main__":
    main()
