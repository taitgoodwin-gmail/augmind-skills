"""Check the sizes in SPEC.md: fill every field of the example spec to the length SPEC.md says fits.

Usage: make_limit_spec.py ../examples/spec_digital-marketing_v0.9.json /tmp/limit_spec.json
Then render /tmp/limit_spec.json. Pass = "MUST FIX ... 0" (the list of uncited sources is expected here).
If a size in SPEC.md changes, change the matching number in this file, and the other way round.
"""
import json, sys, copy
src = json.load(open(sys.argv[1]))
BASE = ("The client sponsor confirms the scope and the records before any work starts, and the engagement lead "
        "keeps a dated note of each decision so a reviewer can follow what was agreed and why. ")
def fill(n, caps=False):
    t = (BASE * 10)[:n].rstrip()
    if len(t) == n and not t.endswith("."):
        t = t[:t.rfind(" ")] if " " in t[-12:] else t
    return t.upper() if caps else t
s = copy.deepcopy(src)
i = s["identity"]
i.update(offering_name=fill(45), eyebrow=fill(40, True), cover_title=fill(60), tagline=fill(75), status_line=fill(100), disclaimer=fill(280), pointer=fill(110))
mm = s["start"]["model_map"]
mm.update(title=fill(62), model_label=fill(20, True), model_sub=fill(45), offering_label=fill(20, True), offering_sub=fill(45), evidence=fill(190))
for m in mm["model"]: m["text"] = fill(45)
mm["cards"] = [{"label": fill(28, True), "text": fill(230)}, {"label": fill(28, True), "highlight": True, "lines": [["1", fill(30)], ["1.1", fill(30)], ["1.1.5", fill(30)]]}, {"label": fill(28, True), "text": fill(230)}]
mx = s["start"]["matrix"]
mx.update(title=fill(62), note=[fill(12), fill(130)], evidence=fill(190))
for k, r in enumerate(mx["rows"]): r["cells"] = [fill(105 if k != 2 else 70)] * 3
ro = s["start"]["roles"]
ro.update(title=fill(62), chart_heading=fill(40, True), evidence=fill(230))
ro["chart"]["lead"] = {"name": fill(25), "sub": fill(35)}
ro["chart"]["second"] = {"name": fill(25), "sub": fill(38)}
ro["chart"]["team"] = [{"name": fill(22)}, {"name": fill(22)}, {"name": fill(22), "open": True, "open_note": "(fractional)"}, {"name": fill(22)}]
ro["chart"]["outside"] = {"name": fill(18), "open": True, "text": fill(75)}
ro["table"]["rows"] = [{"name": fill(24), "does": fill(70), "open": k == 3, "letters": ["A", "R", "C"]} for k in range(11)]
srcs = [x["name"] for x in s["sources"]]
long_srcs = sorted(srcs, key=len)[-12:]
mid_srcs = sorted(srcs, key=len)[15:35]
for ph in s["phases"]:
    ov = ph["overview"]
    ov.update(title=fill(62), purpose=fill(200), notes=[[fill(14), fill(130)] for _ in range(3)])
    for c in ov["columns"]: c["items"] = [fill(27)] * 5 + [fill(54)] * 3
    ir = ph["inputs_roles"]
    ir.update(title=fill(62), inputs_heading=fill(45, True), roles_heading=fill(25, True), evidence=fill(190))
    ir.pop("gray_cards", None)
    n = 5 if ph["number"] == 3 else 7
    ir["inputs"] = [{"name": fill(38), "from": fill(30), "text": fill(105)} for _ in range(n)]
    ir["gray_cards"] = [{"name": fill(22), "text": fill(160)}]
    if ph["number"] == 3:
        ir["choices"] = {"heading": fill(40, True), "items": [{"name": fill(30), "text": fill(45)} for _ in range(5)]}
    else:
        ir.pop("choices", None)
    ir["role_groups"] = [{"label": "AugMind", "client": False, "roles": [{"name": fill(22), "open": k == 3, "does": fill(47)} for k in range(5)]},
                         {"label": "Client", "client": True, "roles": [{"name": fill(18), "open": False, "does": fill(47)} for k in range(3)]}]
    for st in ph["steps"]:
        st["title"] = fill(62)
        st.pop("bands", None); st.pop("mapping", None)
        st["tasks"] = [{"number": f"{st['number']}.{k+1}", "name": fill(30), "text": fill(135), "tag": ["platform", "official", "own", "open"][k % 4],
                        "sources": mid_srcs[k:k+2] if k % 4 < 2 else [], **({"note": fill(60)} if k % 4 >= 2 else {})} for k in range(9)]
    dv = ph["deliverables"]
    dv.update(title=fill(62), approval_heading=fill(50, True), evidence=fill(230))
    dv["lists"] = [{"name": fill(22), "subtitle": fill(40), "items": [fill(30)] * 10} for _ in range(2)]
    dv["texts"] = [{"name": fill(30), "text": fill(220)} for _ in range(2)]
    dv["approval"] = [{"text": fill(80), "confirms": fill(22), "highlight": k > 2} for k in range(5)]
for v in s["all_phases"]:
    v["title"] = fill(62)
    t = v["type"]
    if t == "tiers":
        for x in v["tiers"]: x["text"] = fill(110)
        v["rules"] = [fill(95)] * 6
        for c in v["cards"]: c["text"] = fill(70)
        v["evidence"] = fill(190)
    elif t == "cards":
        v["cards"] = [{"number": str(k+1), "name": fill(30), "text": fill(140), "tag": ["platform", "official", "own"][k % 3], "sources": long_srcs[k:k+3] if k % 3 < 2 else [], **({"note": fill(60)} if k % 3 == 2 else {})} for k in range(6)]
    elif t == "panel":
        v["steps"] = [fill(55)] * 7
        v["notes"] = [[fill(8), fill(142)] for _ in range(4)]
        v["footnote"] = fill(150)
    elif t == "evidence":
        for p in v["panels"]: p["items"] = [fill(85)] * 5
        v["evidence"] = fill(230)
    elif t == "decisions":
        v["gating"] = {"callout": fill(100, True), "items": [fill(250)] * 2}
        v["decisions"] = [fill(160)] * 3
        v["right"] = [{"label": fill(20, True), "style": "gray", "bullets": [fill(65)] * 3 + [fill(120)] * 3}, {"label": fill(20, True), "style": "lavender", "numbered": [fill(65)] * 2 + [fill(120)] * 2}]
        v["evidence"] = fill(230)
json.dump(s, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
