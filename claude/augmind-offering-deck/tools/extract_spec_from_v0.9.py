"""One-off: read the v0.9 deck data and write the full offering spec (all 26 slides).

This exists so the regenerated deck uses v0.9's exact wording and links (no retyping).
Usage: extract_spec_from_v09.py <v0.9_full.json> <out_spec.json>
"""
import json
import re
import sys

deck = json.load(open(sys.argv[1]))["content"]["slides"]
RAW = {s["objectId"]: s for s in deck}
TAGS = {"Platform rule": "platform", "Official guidance": "official", "AugMind's choice": "own", "Open": "open"}
PT = 12700


def hx(c):
    if not c:
        return None
    if "themeColor" in c:
        return "T:" + c["themeColor"]
    r = c.get("rgbColor", {})
    return "%02X%02X%02X" % tuple(round(r.get(k, 0) * 255) for k in ("red", "green", "blue"))


class El:
    def __init__(self, e):
        self.e, self.id = e, e["objectId"]
        t, z = e.get("transform", {}), e.get("size", {})
        self.x, self.y = t.get("translateX", 0) / PT, t.get("translateY", 0) / PT
        self.w = z.get("width", {}).get("magnitude", 0) * t.get("scaleX", 1) / PT
        self.h = z.get("height", {}).get("magnitude", 0) * t.get("scaleY", 1) / PT
        if "table" in e:
            self.kind, self.fill = "TABLE", None
        else:
            sh = e["shape"]
            self.kind = {"TEXT_BOX": "T", "ROUND_RECTANGLE": "RR", "RECTANGLE": "R"}[sh["shapeType"]]
            f = sh["shapeProperties"].get("shapeBackgroundFill", {})
            self.fill = None if f.get("propertyState") == "NOT_RENDERED" else hx(f.get("solidFill", {}).get("color"))

    def paras(self):
        """List of paragraphs; each is a list of run dicts."""
        out, cur = [], None
        for te in self.e["shape"].get("text", {}).get("textElements", []):
            if "paragraphMarker" in te:
                cur = []
                out.append(cur)
            elif "textRun" in te:
                t = te["textRun"]["content"].rstrip("\n")
                if t:
                    st = te["textRun"]["style"]
                    cur.append({"t": t, "b": bool(st.get("bold")), "url": st.get("link", {}).get("url"),
                                "size": st.get("fontSize", {}).get("magnitude"), "color": hx(st.get("foregroundColor", {}).get("opaqueColor"))})
        return out

    def text(self):
        return "\n".join("".join(r["t"] for r in p) for p in self.paras()).strip()

    def lines(self):
        return ["".join(r["t"] for r in p).strip() for p in self.paras()]


def els(sid):
    return [El(e) for e in RAW[sid]["pageElements"]]


def by_id(sid):
    return {e.id: e for e in els(sid)}


def content(sid):
    return [e for e in els(sid) if 120 <= e.y < 509]


def title(sid):
    return next(e.text() for e in els(sid) if e.kind == "T" and 77 <= e.y < 79)


def crumbs(sid):
    c = [e for e in els(sid) if e.kind == "T" and 52 <= e.y < 55 and e.x < 800 and e.text() != "›"]
    return [e.text() for e in sorted(c, key=lambda e: e.x)]


def inside(card, texts):
    return sorted([t for t in texts if card.x - 1 <= t.x < card.x + card.w and card.y - 1 <= t.y < card.y + card.h], key=lambda t: (t.y, t.x))


def is_heading(t):
    ps = t.paras()
    if len(ps) != 1 or not ps[0]:
        return False
    txt = "".join(r["t"] for r in ps[0])
    return all(r["b"] and r["color"] == "2322EF" and r["size"] == 10.5 for r in ps[0]) and txt.upper() == txt


def note_line(sid):
    for e in content(sid):
        if e.kind == "T" and abs(e.y - 485.3) < 1 and e.w > 800 and not e.text().startswith("Platform rule"):
            return e.text()
    return None


def lead_ins(el):
    return [[p[0]["t"].strip(), "".join(r["t"] for r in p[1:]).strip()] for p in el.paras()]


def strip_number(s):
    return re.sub(r"^\d+\s+", "", s)


register = {}


def links(par):
    names, note = [], ""
    for r in par:
        if r["url"]:
            names.append(r["t"].strip())
            assert register.get(r["t"].strip(), r["url"]) == r["url"], ("link differs from the register", r["t"])
        elif r["t"].strip() not in ("·", ""):
            note += r["t"]
    return names, note.strip()


def task_card(title_el, body_el):
    tp = title_el.paras()[0]
    first = tp[0]["t"].strip()
    numbered_title = len(tp) > 1 and tp[0]["color"] == "2322EF" and re.fullmatch(r"[\d.]+", first)
    card = {"name": "".join(r["t"] for r in (tp[1:] if numbered_title else tp)).strip()}
    if numbered_title:
        card["number"] = first
    bp = body_el.paras()
    card["text"] = "".join(r["t"] for r in bp[0]).strip()
    if len(bp) > 1:
        card["tag"] = TAGS["".join(r["t"] for r in bp[1]).strip()]
    if len(bp) > 2:
        names, note = links(bp[2])
        if names:
            card["sources"] = names
        if note:
            card["note"] = note
    return card


# ------------------------------------------------------------------------------- source register
def read_register():
    out = []
    for sid in ("p22", "p23"):
        for e in sorted([x for x in els(sid) if x.kind == "TABLE"], key=lambda x: x.x):
            for row in e.e["table"]["tableRows"][1:]:
                cells = row["tableCells"]
                runs = [te["textRun"] for te in cells[0].get("text", {}).get("textElements", []) if "textRun" in te and te["textRun"]["content"].strip()]
                if not runs:
                    continue
                name = "".join(r["content"] for r in runs).strip()
                url = next((r["style"].get("link", {}).get("url") for r in runs if r["style"].get("link")), None)
                status = "".join(te["textRun"]["content"] for te in cells[1].get("text", {}).get("textElements", []) if "textRun" in te).strip()
                out.append({"name": name, "url": url, "status": status})
    return out


sources = read_register()
register.update({s["name"]: s["url"] for s in sources})

# ------------------------------------------------------------------------------- cover and frame
c = by_id("p1")
spec = {"identity": {
    "offering_name": "Digital Marketing Performance & Revenue",
    "eyebrow": c["p1_i2"].text(), "cover_title": c["p1_i3"].text(), "tagline": c["p1_i4"].text(),
    "status_line": c["p1_i11"].text(), "disclaimer": c["p1_i12"].text(), "pointer": c["p1_read"].text(),
    "footer_parts": [p.strip() for p in by_id("p5")["p5_i24"].text().split("·")][1:]},
    "model": {"start_label": "START", "all_phases_label": "ALL PHASES"},
    "legend": [["Platform rule", "platform", "the platform's own page."], ["Official guidance", "official", "a government, standards or professional body."],
               ["AugMind's choice", "own", "AugMind's own design; any link is background."], ["Open", "open", "not validated."]]}

# ------------------------------------------------------------------------------- start section
p = by_id("p2")
cards = [{"label": p["p2_i48"].text(), "text": p["p2_i49"].text()},
         {"label": p["p2_i51"].text(), "highlight": True,
          "lines": [[par[0]["t"].strip(), "".join(r["t"] for r in par[1:]).strip()] for par in p["p2_i52"].paras()]},
         {"label": p["p2_i54"].text(), "text": p["p2_i55"].text(), "size": 11.5}]
model_map = {"title": title("p2"), "model_label": p["p2_i22"].text(), "model_sub": p["p2_i23"].text(),
             "offering_label": p["p2_i36"].text(), "offering_sub": p["p2_i37"].text(),
             "model": [{"name": p[a].text(), "text": p[b].text()} for a, b in (("p2_i25", "p2_i26"), ("p2_i29", "p2_i30"), ("p2_i33", "p2_i34"))],
             "cards": cards, "evidence": note_line("p2")}

p = by_id("p3")
rows = [{"label": p[f"p3_i{k}"].text(), "cells": [p[f"p3_i{k + j}"].text() for j in (1, 2, 3)]} for k in (34, 39, 44, 49, 54)]
matrix = {"title": title("p3"), "rows": rows, "note": lead_ins(p["p3_i58"])[0], "evidence": note_line("p3")}

p = by_id("p4")


def chart_box(el):
    ps = el.paras()
    return {"name": ps[0][0]["t"].strip(), "sub": "".join(r["t"] for r in ps[1]).strip() if len(ps) > 1 else ""}


team = []
for k in ("p4_i33", "p4_i35", "p4_i37", "p4_i39"):
    ps = p[k].paras()
    t = {"name": ps[0][0]["t"].strip()}
    if len(ps) > 1:
        sub = "".join(r["t"] for r in ps[1]).strip()
        t["open"] = True
        extra = sub.replace("seat open", "").strip()
        if extra:
            t["open_note"] = extra
    team.append(t)
ops = p["p4_i41"].paras()
outside = {"name": ops[0][0]["t"].strip(), "open": any("seat open" in r["t"] for r in ops[0]), "text": "".join(r["t"] for r in ops[1]).strip()}
trows = []
tbl = p["p4_g7"].e["table"]["tableRows"]


def cell_runs(cell):
    return [te["textRun"] for te in cell.get("text", {}).get("textElements", []) if "textRun" in te and te["textRun"]["content"].strip()]


for row in tbl[1:]:
    rr = cell_runs(row["tableCells"][0])
    name = "".join(r["content"] for r in rr if r["style"].get("bold")).strip()
    does = "".join(r["content"] for r in rr if not r["style"].get("bold")).strip()
    is_open = "(seat open)" in name
    trows.append({"name": name.replace("(seat open)", "").strip(), "does": does, "open": is_open,
                  "letters": ["".join(r["content"] for r in cell_runs(cc)).strip() for cc in row["tableCells"][1:]]})
legend_pairs, cur = [], None
for r in p["p4_i43"].paras()[0]:
    if r["b"]:
        cur = r["t"].strip()
    else:
        txt = r["t"]
        if "—" in txt:
            a, b = txt.split("—")
            legend_pairs.append([cur, a.strip()])
            legend_pairs.append(["—", b.strip()])
        else:
            legend_pairs.append([cur, txt.strip()])
roles = {"title": title("p4"), "chart_heading": p["p4_i22"].text(),
         "chart": {"lead": chart_box(p["p4_i24"]), "second": chart_box(p["p4_i27"]), "team": team, "outside": outside},
         "table": {"header": "".join(r["content"] for r in cell_runs(tbl[0]["tableCells"][0])).strip(), "rows": trows},
         "legend": legend_pairs, "evidence": note_line("p4")}
spec["start"] = {"views": crumbs("p2"), "model_map": model_map, "matrix": matrix, "roles": roles}


# ------------------------------------------------------------------------------- phases (position based)
def overview(sid):
    cn = content(sid)
    texts = [e for e in cn if e.kind == "T"]
    cards = sorted([e for e in cn if e.kind == "RR" and e.h > 150], key=lambda e: e.x)
    purpose = next(t for t in texts if t.text().startswith("Purpose"))
    cols = []
    for card in cards:
        lab, sub, body = inside(card, texts)[:3]
        items = body.lines()
        is_num = all(re.match(r"^\d+\s", i) for i in items)
        cols.append({"label": lab.text(), "subtitle": sub.text(), "numbered": is_num,
                     "items": [strip_number(i) for i in items] if is_num else items, "highlight": card.fill == "EEEEFF"})
    bottom = max(c.y + c.h for c in cards)
    notes = [t for t in texts if t.w > 800 and bottom <= t.y < 480]
    return {"title": title(sid), "purpose": lead_ins(purpose)[0][1], "columns": cols, "notes": lead_ins(notes[0]) if notes else []}


def role_list(el):
    out, ps = [], el.paras()
    for i in range(0, len(ps), 2):
        out.append({"name": ps[i][0]["t"].strip(), "open": any("seat open" in r["t"] for r in ps[i]), "does": "".join(r["t"] for r in ps[i + 1]).strip()})
    return out


def inputs(sid):
    cn = content(sid)
    texts = [e for e in cn if e.kind == "T"]
    cards = sorted([e for e in cn if e.kind == "RR"], key=lambda e: (round(e.y), e.x))
    heads = sorted([t for t in texts if is_heading(t) and not any(c.x <= t.x < c.x + c.w and c.y <= t.y < c.y + c.h for c in cards)], key=lambda t: (t.x >= 630, t.y))
    left_heads = [h for h in heads if h.x < 630]
    out = {"title": title(sid), "view_label": crumbs(sid)[1], "inputs_heading": left_heads[0].text(),
           "roles_heading": next(h.text() for h in heads if h.x >= 630), "inputs": [], "gray_cards": [], "role_groups": []}
    choice_items = []
    for card in cards:
        inner = inside(card, texts)
        if card.x >= 630:
            out["role_groups"].append({"label": inner[0].text(), "client": card.fill == "EEEEFF", "roles": role_list(inner[1])})
        elif card.fill == "EEEEFF" and card.w < 150:
            choice_items.append({"name": inner[0].text().replace("\n", " "), "text": inner[1].text()})
        elif len(inner) == 3:
            out["inputs"].append({"name": inner[0].text(), "from": inner[1].text().replace("From: ", ""), "text": inner[2].text()})
        else:
            out["gray_cards"].append({"name": inner[0].text(), "text": inner[1].text()})
    if choice_items:
        out["choices"] = {"heading": left_heads[1].text(), "items": choice_items}
    out["evidence"] = note_line(sid)
    return out


def step(number, name, sids):
    st = {"number": number, "name": name, "title": title(sids[0]), "tasks": [], "bands": []}
    for sid in sids:
        cn = content(sid)
        texts = [e for e in cn if e.kind == "T"]
        tables = [e for e in cn if e.kind == "TABLE"]
        cards = sorted([e for e in cn if e.kind == "RR"], key=lambda e: (round(e.y), e.x))
        heads = sorted([t for t in texts if is_heading(t) and t.w > 400], key=lambda t: t.y)
        for card in cards:
            inner = inside(card, texts)
            tc = task_card(inner[0], inner[1])
            table = next((t for t in tables if card.x <= t.x < card.x + card.w and card.y <= t.y < card.y + card.h), None)
            if table:
                rows_ = [["".join(r["content"] for r in cell_runs(cc)).strip() for cc in row["tableCells"]] for row in table.e["table"]["tableRows"]]
                tc["pairs"] = [[r[0], r[1]] for r in rows_] + [[r[2], r[3]] for r in rows_]
                st["mapping"] = tc
            elif heads and card.y > heads[0].y:
                h = max([x for x in heads if x.y < card.y], key=lambda x: x.y)
                band = next((b for b in st["bands"] if b["heading"] == h.text()), None)
                if band is None:
                    band = {"heading": h.text(), "cards": [], "fill": "lavender" if card.fill == "EEEEFF" else None}
                    st["bands"].append(band)
                band["cards"].append(tc)
            else:
                st["tasks"].append(tc)
    if not st["bands"]:
        del st["bands"]
    return st


def deliv(sid):
    cn = content(sid)
    texts = [e for e in cn if e.kind == "T"]
    cards = [e for e in cn if e.kind == "RR"]
    top = sorted([c_ for c_ in cards if c_.y < 370], key=lambda e: (e.x, e.y))
    out = {"title": title(sid), "lists": [], "texts": [], "approval": []}
    for card in top:
        inner = inside(card, texts)
        if len(inner) >= 4:
            items = []
            for col in sorted(inner[2:], key=lambda t: t.x):
                items += [strip_number(i) for i in col.lines()]
            out["lists"].append({"name": inner[0].text(), "subtitle": inner[1].text(), "items": items})
        else:
            out["texts"].append({"name": inner[0].text(), "text": inner[1].text()})
    out["approval_heading"] = next(t.text() for t in texts if is_heading(t) and t.y > 360)
    for card in sorted([c_ for c_ in cards if c_.y >= 390], key=lambda e: e.x):
        inner = inside(card, texts)
        out["approval"].append({"text": inner[1].text(), "confirms": inner[2].text(), "highlight": card.fill == "EEEEFF"})
    out["evidence"] = note_line(sid)
    return out


def phase(number, name, ov, ir, step_sids, dv):
    cr = crumbs(ov)
    steps = []
    for label, sids in zip([x for x in cr if x.startswith("Step ")], step_sids):
        _w, num, nm = label.split(" ", 2)
        steps.append(step(num, nm, sids))
    return {"number": number, "name": name, "overview": overview(ov), "inputs_roles": inputs(ir), "steps": steps, "deliverables": deliv(dv)}


spec["phases"] = [phase(1, "Discover", "p5", "p6", [["p7"], ["p8", "p8new"]], "p9"),
                  phase(2, "Implement", "p10", "p11", [["p12"]], "p13"),
                  phase(3, "Run", "p14", "p15", [["p16"], ["p17"]], "p18")]

# ------------------------------------------------------------------------------- cross-phase section
views = [x for x in crumbs("p19")]
p = by_id("p19")
reports = {"view": "Reports", "type": "tiers", "title": title("p19"),
           "tiers": [{"name": p[a].text(), "when": p[b].text(), "text": p[c_].text(), "style": st_}
                     for a, b, c_, st_ in (("p19_i29", "p19_i30", "p19_i31", "solid"), ("p19_i33", "p19_i34", "p19_i35", "highlight"), ("p19_i37", "p19_i38", "p19_i39", "optional"))],
           "rules_heading": p["p19_i40"].text(), "rules": p["p19_i41"].lines(), "cards_heading": p["p19_i42"].text(),
           "cards": [task_card(p[a], p[b]) for a, b in (("p19_i44", "p19_i45"), ("p19_i47", "p19_i48"), ("p19_i50", "p19_i51"))],
           "evidence": note_line("p19")}
p = by_id("p20")
rules = {"view": "Rules", "type": "cards", "title": title("p20"),
         "cards": [task_card(p[f"p20_i{k + 1}"], p[f"p20_i{k + 2}"]) for k in range(28, 46, 3)]}
p = by_id("p20reg")
reg = {"view": "Regulated industries", "type": "panel", "title": title("p20reg"), "heading": p["p20r_i47"].text(),
       "steps": [strip_number(x) for x in p["p20r_i48"].lines()], "notes": lead_ins(p["p20r_i49"]),
       "sources": links(p["p20r_i50"].paras()[0])[0], "footnote": p["p20r_i51"].text()}
p = by_id("p21")
note_names, note_text = links(p["p21_i49"].paras()[0])
evid = {"view": "Evidence", "type": "evidence", "title": title("p21"),
        "tiles": [{"number": p[a].text(), "text": p[b].text(), **({"tone": "open"} if p[bg].fill == "FFF4E5" else {})}
                  for bg, a, b in (("p21_i28", "p21_i29", "p21_i30"), ("p21_i31", "p21_i32", "p21_i33"), ("p21_i34", "p21_i35", "p21_i36"), ("p21_i37", "p21_i38", "p21_i39"))],
        "panels": [{"label": p["p21_i41"].text(), "style": "white", "items": p["p21_i42"].lines(), "note": note_text, "sources": note_names},
                   {"label": p["p21_i44"].text(), "style": "gray", "items": p["p21_i45"].lines()},
                   {"label": p["p21_i47"].text(), "style": "open", "items": p["p21_i48"].lines()}],
        "evidence": note_line("p21")}
src = {"view": "Sources", "type": "sources", "title": re.sub(r"\s*\(\d+ of \d+\)$", "", title("p22")), "evidence": note_line("p22")}
p = by_id("p24")
dec = {"view": "Decisions", "type": "decisions", "title": title("p24"), "decisions_label": p["p24_i29"].text(),
       "gating": {"callout": p["p24_i31"].text(), "items": [strip_number(x) for x in p["p24_i32"].lines()]},
       "decisions": [strip_number(x) for x in p["p24_i33"].lines()],
       "right": [{"label": p["p24_i35"].text(), "style": "gray", "bullets": p["p24_i36"].lines()},
                 {"label": p["p24_i38"].text(), "style": "lavender", "numbered": [strip_number(x) for x in p["p24_i39"].lines()]}],
       "evidence": note_line("p24")}
spec["all_phases"] = [reports, rules, reg, evid, src, dec]
spec["sources"] = sources
assert [v["view"] for v in spec["all_phases"]] == ["Reports", "Rules", "Regulated industries", "Evidence", "Sources", "Decisions"]
json.dump(spec, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
print("sources in register:", len(sources), "| phases:", [(ph["name"], [(s["number"], len(s["tasks"]), len(s.get("bands", []))) for s in ph["steps"]]) for ph in spec["phases"]])
print("all-phases crumbs in v0.9:", views)
