"""Print one compact line per element of chosen v0.9 slides (units: points; slide is 960 x 540)."""
import json, sys
d = json.load(open(sys.argv[1]))["content"]["slides"]
by = {s["objectId"]: s for s in d}
def hx(c):
    if not c: return "-"
    if "themeColor" in c: return "T:" + c["themeColor"][:5]
    r = c.get("rgbColor", {}); return "%02X%02X%02X" % tuple(round(r.get(k, 0) * 255) for k in ("red", "green", "blue"))
for sid in sys.argv[2:]:
    s = by[sid]; print(f"=== {sid}  bg={hx(s.get('pageProperties',{}).get('pageBackgroundFill',{}).get('solidFill',{}).get('color'))}")
    for e in s["pageElements"]:
        t = e.get("transform", {}); z = e.get("size", {})
        x, y = t.get("translateX", 0) / 12700, t.get("translateY", 0) / 12700
        w = z.get("width", {}).get("magnitude", 0) * t.get("scaleX", 1) / 12700
        h = z.get("height", {}).get("magnitude", 0) * t.get("scaleY", 1) / 12700
        if "table" in e:
            print(f"{e['objectId'][-9:]:>9} TABLE x{x:6.1f} y{y:6.1f} w{w:6.1f} h{h:6.1f} {e['table']['rows']}x{e['table']['columns']}"); continue
        sh = e["shape"]; p = sh.get("shapeProperties", {})
        f = p.get("shapeBackgroundFill", {}); fill = "-" if f.get("propertyState") == "NOT_RENDERED" else hx(f.get("solidFill", {}).get("color"))
        o = p.get("outline", {}); line = "-" if o.get("propertyState") == "NOT_RENDERED" else hx(o.get("outlineFill", {}).get("solidFill", {}).get("color")) + ("/" + str(round(o.get("weight", {}).get("magnitude", 0) / 12700, 2))) + ("D" if o.get("dashStyle") == "DASH" else "")
        kind = {"TEXT_BOX": "T", "ROUND_RECTANGLE": "RR", "RECTANGLE": "R"}.get(sh["shapeType"], sh["shapeType"])
        lk = p.get("link", {}).get("pageObjectId", "")
        segs = []; pcount = 0; pst = ""
        for te in sh.get("text", {}).get("textElements", []):
            if "paragraphMarker" in te:
                pcount += 1
                st = te["paragraphMarker"].get("style", {})
                if pcount <= 2:
                    pst += "[%s%s sa%s sb%s%s]" % (st.get("alignment", "")[:1], "" if st.get("lineSpacing", 100) == 100 else " ls%d" % st["lineSpacing"], st.get("spaceAbove", {}).get("magnitude", 0), st.get("spaceBelow", {}).get("magnitude", 0), " BUL i%s/%s" % (st.get("indentStart", {}).get("magnitude", 0), st.get("indentFirstLine", {}).get("magnitude", 0)) if "bullet" in te["paragraphMarker"] else "")
            tr = te.get("textRun")
            if tr and tr["content"].strip():
                st = tr["style"]
                segs.append("%s%s/%s%s|%s" % (st.get("fontSize", {}).get("magnitude", "?"), "b" if st.get("bold") else "", hx(st.get("foregroundColor", {}).get("opaqueColor")), "L" if st.get("link") else "", tr["content"].strip()[:22]))
        txt = (" P%d %s " % (pcount, pst) + " ; ".join(segs[:4]) + (" ..+%d" % (len(segs) - 4) if len(segs) > 4 else "")) if segs else ""
        print(f"{e['objectId'][-9:]:>9} {kind:2} x{x:6.1f} y{y:6.1f} w{w:6.1f} h{h:6.1f} f={fill:6} l={line:11} {p.get('contentAlignment','')[:3]:3} {('->'+lk) if lk else ''}{txt}")
