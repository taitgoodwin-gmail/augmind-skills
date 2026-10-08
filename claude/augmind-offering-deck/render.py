"""AugMind offering deck renderer.

Reads an offering spec (JSON) and draws the full deck in the locked v0.9 look:
  cover; start section (model map, offering matrix, roles); each phase (overview, inputs and roles,
  task grids with continuation pages, extra bands and a task-to-section mapping, deliverables and
  approval); cross-phase section (report tiers, rule cards, a panel slide, evidence, source register,
  decisions).

All geometry is in points on a 960 x 540 slide. Constants were measured from the v0.9 deck.
Every text box is checked against its box; anything that will not fit is reported as a warning.

Slide references: any text in the spec may contain {slide:REF}; the renderer replaces it with the
page number, so text never carries a hand-typed slide number. REF is one of:
  cover, model_map, matrix, roles, phaseN:overview, phaseN:inputs, phaseN:deliverables,
  stepX.Y (first page of that step), taskX.Y.Z (the page that task's card is on),
  and the cross-phase view types: tiers, cards, panel, evidence, sources, decisions.

Usage: render.py <spec.json> <out.pptx> [--logo path | --no-logo]
The cover logo defaults to assets/augmind-logo-cover.png beside this file.
Exit code 0: nothing must be fixed. Exit code 2: at least one MUST FIX line was printed.
Needs: python-pptx, Pillow, lxml, and the Inter font (Regular and Bold; copies sit in the fonts folder beside this file).
"""
import copy
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field
from typing import List, Optional

from lxml import etree
from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu

# ------------------------------------------------------------------------------------ tokens
PT = 12700
W, H = 960.0, 540.0
LEFT = 43.2                 # left margin
TEXT_W = 871.2              # width of title / footer / notes
GRID_W = 873.4              # width of card grids (v0.9 cards run 2.2pt past the text edge)
NOTE_Y = 485.3              # evidence note / legend line

INK, MUTED, FAINT = "14161F", "5B6072", "9AA0B5"
BLUE, LAVENDER, GRAY, ORANGE_FILL = "2322EF", "EEEEFF", "F1F2F7", "FFF4E5"
BORDER, PAGE, WHITE = "D8DAE5", "FAFAFC", "FFFFFF"
ON_BLUE_SOFT = "DCDDFF"
COVER_BG, COVER_EYEBROW, COVER_SUB, COVER_FAINT = "14161F", "BFC2FF", "D8DAE5", "A9ADC4"
LINK = "0563C1"
GREEN, ORANGE, MAGENTA = "0B6E4F", "B4530A", "9D174D"
TAG_COLOR = {"platform": MAGENTA, "official": GREEN, "own": MUTED, "open": ORANGE}
TAG_LABEL = {"platform": "Platform rule", "official": "Official guidance", "own": "AugMind's choice", "open": "Open"}
TAG_FILL = {"platform": WHITE, "official": WHITE, "own": GRAY, "open": ORANGE_FILL}
PANEL_FILL = {"white": WHITE, "gray": GRAY, "open": ORANGE_FILL, "lavender": LAVENDER}
LETTER_COLOR = {"A": BLUE, "R": INK, "V": ORANGE, "S": GREEN, "C": MUTED, "—": BORDER}

FONT = "Inter"
FONT_NAMES = {False: "Inter-Regular.otf", True: "Inter-Bold.otf"}
FONT_FOLDERS = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"),      # the copies kept beside this file
                "/usr/share/fonts/opentype/inter", os.path.expanduser("~/.fonts")]
LINE = 1.21                 # Inter line height at 100% spacing, as a multiple of font size
RADIUS = 6.0
WRAP_SAFETY = 0.985         # estimate wraps slightly early, so the overflow check errs on the safe side

# card text styles: sizes for number, name, text, tag, sources; title box height; where the body starts
NORMAL = {"num": 11.5, "name": 12, "text": 10.5, "tag": 9.5, "src": 9, "title_h": 21.6, "body_y": 30.2}
LARGE = {"num": 14, "name": 14, "text": 12, "tag": 11, "src": 11, "title_h": 23.6, "body_y": 34.6}

# ------------------------------------------------------------------------------------ text model
_fonts = {}


def _font(bold):
    if bold not in _fonts:
        for folder in FONT_FOLDERS:
            path = os.path.join(folder, FONT_NAMES[bold])
            if os.path.exists(path):
                _fonts[bold] = ImageFont.truetype(path, 200)
                break
        else:
            sys.exit(f"Cannot measure text: {FONT_NAMES[bold]} was not found in {FONT_FOLDERS}. The fit check depends on it.")
    return _fonts[bold]


def text_width(s, size, bold=False):
    return _font(bold).getlength(s) / 200.0 * size


@dataclass
class R:                      # a run of text
    text: str
    size: float = 10.5
    bold: bool = False
    color: str = INK
    url: Optional[str] = None


@dataclass
class P:                      # a paragraph
    runs: List[R] = field(default_factory=list)
    before: float = 0.0       # space above, pt
    align: str = "l"
    bullet: bool = False


BULLET_INDENT, BULLET_FIRST = 12.0, 5.75


def para_lines(p: P, width):
    """Greedy word wrap of a mixed-style paragraph. Returns (line_count, tallest font size)."""
    avail = (width - (BULLET_INDENT if p.bullet else 0)) * WRAP_SAFETY
    lines, x, biggest = 1, 0.0, 0.0
    for run in p.runs:
        biggest = max(biggest, run.size)
        pieces = run.text.replace(" ", " ").split(" ")
        for i, word in enumerate(pieces):
            token = word + (" " if i < len(pieces) - 1 else "")
            if x > 0 and x + text_width(word, run.size, run.bold) > avail:
                lines += 1
                x = 0.0
            x += text_width(token, run.size, run.bold)
    return lines, biggest or 10.5


def paras_height(paras, width):
    h = 0.0
    for i, p in enumerate(paras):
        n, size = para_lines(p, width)
        h += n * size * LINE + (p.before if i else 0)
    return h


def lines_of(text, size, width, bold=False):
    return para_lines(P([R(text, size, bold)]), width)[0]


def bullets(items, size=11.5, before=4):
    return [P([R(i, size)], before=before, bullet=True) for i in items]


def numbered(items, size=11, before=3, start=1):
    return [P([R(f"{start + k}  {i}", size)], before=before) for k, i in enumerate(items)]


def lead_in(lead, body, size=11, before=5, color=INK):
    return P([R(lead + "  ", size, True, color), R(body, size, False, color)], before=before)


# ------------------------------------------------------------------------------------ drawing
def rgb(hexstr):
    return RGBColor.from_string(hexstr)


class Slide:
    def __init__(self, deck, key, bg):
        self.deck, self.key = deck, key
        self.s = deck.prs.slides.add_slide(deck.blank)
        self.s.background.fill.solid()
        self.s.background.fill.fore_color.rgb = rgb(bg)

    def box(self, x, y, w, h, fill=None, line=None, line_w=0.75, radius=RADIUS, pill=False, dash=False, square=False, link=None):
        kind = MSO_SHAPE.RECTANGLE if square else MSO_SHAPE.ROUNDED_RECTANGLE
        sh = self.s.shapes.add_shape(kind, Emu(round(x * PT)), Emu(round(y * PT)), Emu(round(w * PT)), Emu(round(h * PT)))
        style = sh._element.find(qn("p:style"))          # drop the theme style so no shadow is inherited
        if style is not None:
            sh._element.remove(style)
        if not square:
            sh.adjustments[0] = 0.5 if pill else min(0.5, radius / max(1.0, min(w, h)))
        if fill:
            sh.fill.solid()
            sh.fill.fore_color.rgb = rgb(fill)
        else:
            sh.fill.background()
        if line:
            sh.line.color.rgb = rgb(line)
            sh.line.width = Emu(round(line_w * PT))
            if dash:
                sh.line.dash_style = MSO_LINE.DASH
        else:
            sh.line.fill.background()
        if link:
            self.deck.pending_links.append((sh, link))
        return sh

    def rule(self, x, y, w, h, color=MUTED):
        """A thin solid bar, used for connectors and table lines."""
        return self.box(x, y, w, h, fill=color, square=True)

    def text(self, x, y, w, h, paras, anchor="top", link=None, check=True, what=""):
        if isinstance(paras, P):
            paras = [paras]
        tb = self.s.shapes.add_textbox(Emu(round(x * PT)), Emu(round(y * PT)), Emu(round(w * PT)), Emu(round(h * PT)))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "mid": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[p.align]
            para.line_spacing = 1.0
            para.space_before = Emu(round(p.before * PT)) if i else Emu(0)
            para.space_after = Emu(0)
            if p.bullet:
                pPr = para._p.get_or_add_pPr()
                pPr.set("marL", str(round(BULLET_INDENT * PT)))
                pPr.set("indent", str(round((BULLET_FIRST - BULLET_INDENT) * PT)))
                etree.SubElement(pPr, qn("a:buChar")).set("char", "•")
            for run in p.runs:
                r = para.add_run()
                r.text = run.text
                r.font.name = FONT
                r.font.size = Emu(round(run.size * PT))
                r.font.bold = run.bold
                r.font.italic = False
                if run.url:
                    r.hyperlink.address = run.url
                    r.font.underline = True
                    r.font.color.rgb = rgb(LINK)
                else:
                    r.font.color.rgb = rgb(run.color)
        if link:
            self.deck.pending_links.append((tb, link))
        if check:
            need = paras_height(paras, w)
            if need > h + 1.5:
                first = paras[0].runs[0].text[:40] if paras and paras[0].runs else ""
                self.deck.warnings.append(f"{self.key}: text needs {need:.0f}pt but its box is {h:.0f}pt {what} [{first}...]")
        return tb


class Deck:
    def __init__(self, spec, logo=None):
        self.spec, self.logo = spec, logo
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = Emu(round(W * PT)), Emu(round(H * PT))
        self.blank = self.prs.slide_layouts[6]
        self.pending_links, self.warnings = [], []     # warnings: text that does not fit; each one must be fixed in the spec
        self.notes = []                                  # notes: small automatic size changes that kept text inside its box
        self.slides, self.order = {}, []
        self.source_url = {s["name"]: s["url"] for s in spec.get("sources", [])}
        self.grid_cache = {}
        self.page_of = {}                # planned page number of each slide key
        self.aliases = {}                # short reference name -> slide key (first use wins)
        self.cited = set()               # source names used on any slide
        self.uncited = []                # register entries no slide cites
        self.tag_label = dict(TAG_LABEL)
        for label, tag, _desc in spec.get("legend", []):
            self.tag_label[tag] = label

    def add(self, key, bg=PAGE, alias=None):
        s = Slide(self, key, bg)
        self.slides[key] = s
        self.order.append(key)
        if alias:
            self.alias(alias, key)
        return s

    def alias(self, name, key):
        self.aliases.setdefault(name, key)

    def references(self):
        """Every name a {slide:REF} may use, with its page number."""
        refs = {key: i for i, key in enumerate(self.order, 1)}
        for name, key in self.aliases.items():
            refs[name] = refs[key]
        return refs

    def page_number(self, key):
        return self.order.index(key) + 1

    def finish(self, path):
        made = skipped = 0
        for shape, target in self.pending_links:
            if target in self.slides:
                shape.click_action.target_slide = self.slides[target].s
                made += 1
            else:
                skipped += 1
        used = {self.blank.part.partname}
        for layout in list(self.prs.slide_layouts):          # drop the template's unused layouts
            if layout.part.partname not in used:
                self.prs.slide_layouts.remove(layout)
        self.prs.save(path)
        return made, skipped


# ------------------------------------------------------------------------------------ frame
def frame(deck, s, section, view_index, title, counter_suffix=""):
    """Phase tabs, breadcrumb row, counter, headline, footer and page number."""
    spec = deck.spec
    tabs = [("start", spec["model"]["start_label"], "start:0")]
    for ph in spec["phases"]:
        tabs.append((f"phase{ph['number']}", f"{ph['number']}  {ph['name'].upper()}", f"phase{ph['number']}:overview"))
    tabs.append(("all", spec["model"]["all_phases_label"], "all:0"))
    x = LEFT
    for sec, label, target in tabs:
        w = text_width(label, 10, True) + 30.3
        active = sec == section["id"]
        s.box(x, 21.6, w, 23.0, fill=BLUE if active else PAGE, line=BLUE if active else BORDER, line_w=1.0, pill=True)
        s.text(x, 21.6, w, 23.0, P([R(label, 10, True, WHITE if active else MUTED)], align="c"), anchor="mid", link=target, check=False)
        x += w + 7.2
    x = LEFT
    views = section["views"]
    for i, (label, target) in enumerate(views):
        w = text_width(label, 10, True) + 21.6
        if i == view_index:
            s.box(x, 53.3, w, 20.2, fill=LAVENDER, line=LAVENDER, line_w=1.0)
            s.text(x, 53.3, w, 20.2, P([R(label, 10, True, BLUE)], align="c"), anchor="mid", check=False)
        else:
            s.text(x, 53.3, w, 20.2, P([R(label, 10, False, MUTED)], align="c"), anchor="mid", link=target, check=False)
        x += w + 1.35
        if i < len(views) - 1:
            s.text(x, 53.3, 11.5, 20.2, P([R("›", 11, True, FAINT)], align="c"), anchor="mid", check=False)
            x += 11.5 + 1.35
    if x > 800:
        deck.warnings.append(f"{s.key}: breadcrumb row is {x:.0f}pt wide and runs into the counter; shorten view names")
    s.text(806.4, 53.3, 110.2, 20.2, P([R(f"{view_index + 1} of {len(views)}{counter_suffix}", 10, False, MUTED)], align="r"), anchor="mid", check=False)
    size = 25.0
    while text_width(title, size, True) > TEXT_W and size > 19:
        size -= 0.5
    if text_width(title, size, True) > TEXT_W:
        deck.warnings.append(f"{s.key}: headline is too long for one line even at {size}pt; shorten it [{title[:50]}...]")
    elif size < 25:
        deck.notes.append(f"{s.key}: headline set at {size}pt (not 25pt) to fit one line [{title[:50]}...]")
    s.text(LEFT, 77.8, TEXT_W, 41.8, P([R(title, size, True, INK)]), anchor="mid", check=False)
    idn = spec["identity"]
    footer = "  ·  ".join([idn["offering_name"]] + idn["footer_parts"])
    s.text(LEFT, 509.0, 756.0, 18.7, P([R(footer, 9, True, INK)]), anchor="mid", check=False)
    s.text(878.4, 509.0, 38.2, 18.7, P([R(str(deck.page_number(s.key)), 9, False, MUTED)], align="r"), anchor="mid", check=False)


def evidence_note(s, text, y=NOTE_Y, size=9.5):
    if text:
        s.text(LEFT, y, TEXT_W, 21.6, P([R(text, size, False, MUTED)]), what="(note line)")


def legend(deck, s):
    runs = []
    items = deck.spec["legend"]
    for i, (label, tag, desc) in enumerate(items):
        runs.append(R(label, 9, True, TAG_COLOR[tag]))
        runs.append(R("  " + desc + ("      " if i < len(items) - 1 else ""), 9, False, MUTED))
    s.text(LEFT, NOTE_Y, TEXT_W, 21.6, P(runs), check=False)


def source_runs(deck, names, size, note=None):
    runs = []
    if note:
        runs.append(R(note + ("  " if names else ""), size, False, MUTED))
    for k, name in enumerate(names or []):
        url = deck.source_url.get(name)
        deck.cited.add(name)
        if not url:
            msg = f"source '{name}' is cited but is not in the source register"
            if msg not in deck.warnings:
                deck.warnings.append(msg)
        if k:
            runs.append(R("  ·  ", size, False, MUTED))
        runs.append(R(name, size, False, MUTED, url))
    return runs


# ------------------------------------------------------------------------------------ cover
def cover(deck):
    idn = deck.spec["identity"]
    s = deck.add("cover", COVER_BG)
    x, w = 57.6, 842.4
    s.text(x, 57.6, 432.0, 28.8, P([R(idn["eyebrow"], 13, True, COVER_EYEBROW)]), anchor="mid", check=False)
    tsize = 42.0
    while lines_of(idn["cover_title"], tsize, w, True) > 2 and tsize > 30:
        tsize -= 1.0
    if tsize < 42:
        deck.notes.append(f"cover: title set at {tsize:.0f}pt (not 42pt) to fit two lines")
    s.text(x, 136.8, w, 115.2, P([R(idn["cover_title"], tsize, True, WHITE)]), anchor="bottom", what="(cover title)")
    s.text(x, 262.8, w, 43.2, P([R(idn["tagline"], 22, False, COVER_SUB)]), anchor="mid", what="(tagline)")
    px = x
    for ph in deck.spec["phases"]:
        s.box(px, 338.4, 144.0, 36.0, fill=BLUE, line=BLUE, line_w=1.0, pill=True)
        s.text(px, 338.4, 144.0, 36.0, P([R(f"{ph['number']}  {ph['name'].upper()}", 13, True, WHITE)], align="c"), anchor="mid",
               link=f"phase{ph['number']}:overview", check=False)
        px += 158.4
    s.text(x, 399.6, w, 25.9, P([R(idn["status_line"], 15, True, WHITE)]), anchor="mid", what="(status line)")
    disc = P([R(idn["disclaimer"], 12, False, COVER_FAINT)])
    dh = paras_height([disc], w)
    s.text(x, 432.0, w, dh + 2, disc)
    if idn.get("pointer"):
        s.text(x, 432.0 + dh + 8.5, w, 22.0, P([R(idn["pointer"], 13, True, WHITE)]), what="(pointer)")
    if deck.logo:
        from PIL import Image
        iw, ih = Image.open(deck.logo).size
        lh = 96.0
        lw = lh * iw / ih
        pad = 9.0
        tx, ty = W - 57.6 - (lw + 2 * pad), 43.2
        s.box(tx, ty, lw + 2 * pad, lh + 2 * pad, fill="FBFAFB", radius=10.0)
        s.s.shapes.add_picture(deck.logo, Emu(round((tx + pad) * PT)), Emu(round((ty + pad) * PT)), Emu(round(lw * PT)), Emu(round(lh * PT)))
    return s


# ------------------------------------------------------------------------------------ start section
def steps_phrase(ph, style):
    nums = [st["number"] for st in ph.get("steps", [])]
    if not nums:
        return ""
    if len(nums) == 1:
        return f"Step {nums[0]}"
    if style == "list":
        return "Steps " + ", ".join(nums)
    return "Steps " + ", ".join(nums[:-1]) + " and " + nums[-1]


def model_map(deck, section):
    mm = deck.spec["start"]["model_map"]
    s = deck.add("start:0", alias="model_map")
    frame(deck, s, section, 0, mm["title"])
    s.text(LEFT, 136.8, 187.2, 20.2, P([R(mm["model_label"], 10.5, True, BLUE)]), anchor="mid", check=False)
    s.text(LEFT, 158.4, 187.2, 43.2, P([R(mm["model_sub"], 12, False, MUTED)]), what="(model label)")
    s.text(LEFT, 244.8, 187.2, 20.2, P([R(mm["offering_label"], 10.5, True, BLUE)]), anchor="mid", check=False)
    s.text(LEFT, 266.4, 187.2, 43.2, P([R(mm["offering_sub"], 12, False, MUTED)]), what="(offering label)")
    phases = deck.spec["phases"]
    n = len(mm["model"])
    gap = 8.6
    cw = (GRID_W - 201.6 - gap * (n - 1)) / n
    for i, m in enumerate(mm["model"]):
        x = 244.8 + i * (cw + gap)
        s.box(x, 133.2, cw, 75.6, fill=WHITE, line=BORDER)
        s.text(x, 140.4, cw, 25.2, P([R(m["name"], 14, True)], align="c"), anchor="mid", what="(model stage)")
        s.text(x + 14.4, 167.0, cw - 28.8, 36.0, P([R(m["text"], 12, False, MUTED)], align="c"), what="(model stage text)")
        s.rule(x + cw / 2 - 0.7, 208.8, 1.4, 28.8)
        if i < len(phases):
            ph = phases[i]
            s.box(x, 237.6, cw, 72.0, fill=BLUE, line=BLUE, line_w=1.0, link=f"phase{ph['number']}:overview")
            s.text(x, 244.8, cw, 28.8, P([R(f"{ph['number']}  {ph['name'].upper()}", 16, True, WHITE)], align="c"), anchor="mid", what="(phase name)")
            s.text(x, 273.6, cw, 25.2, P([R(steps_phrase(ph, "and"), 12, False, ON_BLUE_SOFT)], align="c"), anchor="mid", check=False)
    cards = mm["cards"]
    k = len(cards)
    cgap = 14.4
    cw = (GRID_W - cgap * (k - 1)) / k
    for i, c in enumerate(cards):
        x = LEFT + i * (cw + cgap)
        s.box(x, 334.8, cw, 140.4, fill=LAVENDER if c.get("highlight") else WHITE, line=BORDER)
        s.text(x + 14.4, 343.4, cw - 29.5, 20.2, P([R(c["label"], 10.5, True, BLUE)]), anchor="mid", what="(card label)")
        size = c.get("size", 12)
        if c.get("lines"):
            body = [P([R(a, size, True), R("  " + b, size)], before=4) for a, b in c["lines"]]
        else:
            body = [P([R(c["text"], size)])]
        s.text(x + 14.4, 366.5, cw - 28.8, 104.4, body, what=f"({c['label']})")
    evidence_note(s, mm.get("evidence"))
    return s


def offering_matrix(deck, section):
    mx = deck.spec["start"]["matrix"]
    s = deck.add("start:1", alias="matrix")
    frame(deck, s, section, 1, mx["title"])
    phases = deck.spec["phases"]
    col_x, col_w = [158.4, 415.1, 671.8], 244.8
    if len(phases) != 3:
        col_w = (GRID_W - 115.2 - 11.9 * (len(phases) - 1)) / len(phases)
        col_x = [158.4 + i * (col_w + 11.9) for i in range(len(phases))]
    for i, ph in enumerate(phases):
        x = col_x[i]
        s.box(x, 129.6, col_w, 44.6, fill=BLUE, line=BLUE, link=f"phase{ph['number']}:overview")
        s.text(x + 13.0, 132.5, col_w - 25.9, 21.6, P([R(f"{ph['number']}  {ph['name'].upper()}", 14, True, WHITE)]), anchor="mid", what="(phase name)")
        first, last = deck.page_of.get(f"phase{ph['number']}:first"), deck.page_of.get(f"phase{ph['number']}:last")
        sub = steps_phrase(ph, "list") + (f"  ·  slides {first} to {last}" if first else "")
        s.text(x + 13.0, 152.6, col_w - 25.9, 17.3, P([R(sub, 10, False, ON_BLUE_SOFT)]), anchor="mid", check=False)
        if i < len(phases) - 1:
            s.text(x + col_w - 1.4, 136.8, 14.8, 28.8, P([R("›", 16, True, BLUE)], align="c"), anchor="mid", check=False)
    y = 181.4
    cell_w = col_w - 21.6
    for r, row in enumerate(mx["rows"]):
        most = max(lines_of(c, 11, cell_w) for c in row["cells"])
        h = max(41.8, most * 11 * LINE + 15.2)
        s.box(LEFT, y, GRID_W, h, fill=WHITE if r % 2 == 0 else GRAY, line=BORDER, square=True)
        s.text(54.7, y, 93.6, h, P([R(row["label"], 10.5, True, BLUE)]), anchor="mid", what="(row label)")
        for i, cell in enumerate(row["cells"]):
            s.text(col_x[i] + 13.0, y, cell_w, h, P([R(cell, 11)]), anchor="mid", what=f"({row['label']} cell)")
        y += h
    if mx.get("note"):
        s.text(LEFT, y + 15.8, TEXT_W, 21.6, lead_in(mx["note"][0], mx["note"][1], 11, 0), what="(matrix note)")
    if y + 15.8 + 14 > NOTE_Y:
        deck.warnings.append(f"{s.key}: the matrix rows run to {y:.0f}pt and crowd the note lines")
    evidence_note(s, mx.get("evidence"))
    return s


def roles_chart(deck, section):
    ro = deck.spec["start"]["roles"]
    s = deck.add("start:2", alias="roles")
    frame(deck, s, section, 2, ro["title"])
    ch = ro["chart"]
    s.text(LEFT, 126.7, 288.0, 20.2, P([R(ro["chart_heading"], 10.5, True, BLUE)]), anchor="mid", check=False)
    s.box(75.6, 149.8, 216.0, 47.5, fill=BLUE, line=BLUE)
    s.text(75.6, 149.8, 216.0, 47.5, [P([R(ch["lead"]["name"], 12, True, WHITE)], align="c"), P([R(ch["lead"]["sub"], 10, False, WHITE)], align="c")], anchor="mid", what="(lead role)")
    y = 197.3
    if ch.get("second"):
        s.rule(182.9, y, 1.4, 14.4)
        s.box(75.6, 211.7, 216.0, 44.6, fill=LAVENDER, line=BORDER)
        s.text(75.6, 211.7, 216.0, 44.6, [P([R(ch["second"]["name"], 11.5, True)], align="c"), P([R(ch["second"]["sub"], 10)], align="c")], anchor="mid", what="(second role)")
        y = 256.3
    s.rule(182.9, y, 1.4, 267.8 - y)
    s.rule(111.6, 267.8, 144.0, 1.4)
    s.rule(111.6, 267.8, 1.4, 10.1)
    s.rule(254.2, 267.8, 1.4, 10.1)
    team = ch["team"]
    rows = math.ceil(len(team) / 2)
    pitch = min(51.9, (382.0 - 277.9) / max(1, rows))
    bh = min(44.6, pitch - 6.0)
    for i, t in enumerate(team):
        x = LEFT + (i % 2) * 143.3
        ty = 277.9 + (i // 2) * pitch
        is_open = t.get("open")
        s.box(x, ty, 136.8, bh, fill=WHITE, line=ORANGE if is_open else BORDER, line_w=1.0 if is_open else 0.75, dash=bool(is_open))
        paras = [P([R(t["name"], 11, True)], align="c")]
        if is_open:
            sub = [R("seat open", 9.5, True, MUTED)]
            if t.get("open_note"):
                sub.append(R(" " + t["open_note"], 9.5, True, "FF0000"))
            paras.append(P(sub, align="c"))
        s.text(x, ty, 136.8, bh, paras, anchor="mid", what="(team role)")
    out = ch.get("outside")
    if out:
        oy = 277.9 + rows * pitch + 8.5
        name = [R(out["name"], 11.5, True)]
        if out.get("open"):
            name.append(R("  seat open", 9.5, True, MUTED))
        s.box(LEFT, oy, 280.1, 66.2, fill=ORANGE_FILL, line=ORANGE, line_w=1.0, dash=True)
        s.text(54.0, oy, 259.2, 66.2, [P(name, align="c"), P([R(out["text"], 10)], align="c")], anchor="mid", what="(outside role)")
    # responsibility table
    tb = ro["table"]
    tx = 349.2
    widths = [318.2, 79.2, 90.7, 79.2]
    cols = [tx, tx + widths[0], tx + widths[0] + widths[1], tx + widths[0] + widths[1] + widths[2]]
    s.text(tx, 126.7, widths[0], 20.2, P([R(tb["header"], 10, True, MUTED)]), anchor="mid", check=False)
    for i, ph in enumerate(deck.spec["phases"][:3]):
        s.text(cols[i + 1], 126.7, widths[i + 1], 20.2, P([R(f"{ph['number']}  {ph['name'].upper()}", 10, True, MUTED)], align="c"), anchor="mid", check=False)
    rows_ = tb["rows"]
    pitch = min(27.5, (443.0 - 148.5) / max(1, len(rows_)))
    if pitch < 24.5:
        deck.warnings.append(f"{s.key}: {len(rows_)} roles in the table leave only {pitch:.0f}pt per row; two-line rows need 25pt")
    for i, r in enumerate(rows_):
        ry = 148.5 + i * pitch
        name = r["name"] + (" (seat open)" if r.get("open") else "")
        s.text(tx, ry + 1.0, widths[0], pitch - 1.0, [P([R(name, 10, True, MUTED if r.get("open") else INK)]), P([R(r["does"], 9)])], anchor="mid", what="(role row)")
        for k, letter in enumerate(r["letters"]):
            s.text(cols[k + 1], ry, widths[k + 1], pitch, P([R(letter, 13, True, LETTER_COLOR.get(letter, INK))], align="c"), anchor="mid", check=False)
    bottom = 148.5 + len(rows_) * pitch
    s.rule(tx, bottom, sum(widths), 0.75, BORDER)
    runs = []
    for i, (letter, meaning) in enumerate(ro["legend"]):
        runs.append(R(letter, 9, True, MUTED if letter == "—" else LETTER_COLOR.get(letter, INK)))
        runs.append(R((" " if letter != "—" else "  ") + meaning + ("    " if i < len(ro["legend"]) - 1 else ""), 9, False, MUTED))
    s.text(tx, bottom + 2.0, sum(widths), 18.7, P(runs), anchor="mid", what="(letter legend)")
    evidence_note(s, ro.get("evidence"))
    return s


# ------------------------------------------------------------------------------------ phase overview
def phase_overview(deck, ph, section):
    ov = ph["overview"]
    s = deck.add(f"phase{ph['number']}:overview")
    frame(deck, s, section, 0, ov["title"])
    purpose = P([R("Purpose  ", 14, True), R(ov["purpose"], 14)])
    lines, _ = para_lines(purpose, TEXT_W)
    ph_h = lines * 14 * LINE + 3.5
    s.text(LEFT, 126.7, TEXT_W, ph_h, purpose)
    notes = [lead_in(lead, body) for lead, body in ov.get("notes", [])]
    notes_h = paras_height(notes, TEXT_W) if notes else 0.0
    notes_bottom = min(499.0, max(485.5, 435.6 + notes_h))
    notes_y = notes_bottom - notes_h
    top = 126.7 + ph_h + 8.7
    bottom = (notes_y - 10.8) if notes else 481.0
    cols = ov["columns"]
    n = len(cols)
    gap = 15.85
    cw = (TEXT_W - gap * (n - 1)) / n
    for i, col in enumerate(cols):
        x = LEFT + i * (cw + gap)
        s.box(x, top, cw, bottom - top, fill=LAVENDER if col.get("highlight") else WHITE, line=BORDER)
        s.text(x + 14.4, top + 11.5, cw - 28.8, 20.2, P([R(col["label"], 10.5, True, BLUE)]), anchor="mid", check=False)
        s.text(x + 14.4, top + 31.7, cw - 28.8, 20.2, P([R(col["subtitle"], 11.5, False, MUTED)]), anchor="mid", what="(column subtitle)")
        body = numbered(col["items"]) if col.get("numbered") else bullets(col["items"])
        s.text(x + 14.4, top + 57.6, cw - 25.2, bottom - top - 57.6 - 7.2, body, what=f"({col['label']} column)")
        if i < n - 1:
            s.text(x + cw, top + (bottom - top) / 2 - 14.4, gap, 28.8, P([R("›", 18, True, BLUE)], align="c"), anchor="mid", check=False)
    if notes:
        s.text(LEFT, notes_y, TEXT_W, notes_h + 2, notes)
    return s


# ------------------------------------------------------------------------------------ inputs and roles
def inputs_roles(deck, ph, section, view_index):
    ir = ph["inputs_roles"]
    s = deck.add(f"phase{ph['number']}:inputs")
    frame(deck, s, section, view_index, ir["title"])
    s.text(LEFT, 126.7, 568.8, 20.2, P([R(ir["inputs_heading"], 10.5, True, BLUE)]), anchor="mid", check=False)
    cw, gap, text_w = 282.6, 7.2, 259.6
    cards = [("input", c) for c in ir["inputs"]] + [("gray", c) for c in ir.get("gray_cards", [])]
    rows = math.ceil(len(cards) / 2)
    top, limit = 148.3, 475.9
    choices = ir.get("choices")
    if choices:
        items = choices["items"]
        k = len(items)
        cgap = 7.25
        ccw = (572.4 - cgap * (k - 1)) / k
        most_c = max(lines_of(c["text"], 9.5, ccw - 14.4) for c in items)
        name_lines = max(lines_of(c["name"], 10.5, ccw - 14.4, True) for c in items)
        c_h = 2.9 + max(2, name_lines) * 10.5 * LINE + 3.4 + most_c * 9.5 * LINE + 8.7
        band_top = 478.1 - c_h - 20.2
        limit = band_top - 5.7
    size = ch = need = None
    for size in (10.0, 9.5):
        most = 1
        for kind, c in cards:
            most = max(most, lines_of(c["text"], size, text_w) - (0 if kind == "input" else 1))
        need = 38.2 + most * size * LINE + 2.0
        if rows * need + (rows - 1) * gap <= limit - top + 0.5:
            # cards share the available height (v0.9: 76.5pt with four rows, 104.4pt with three); never taller than 104.4pt
            ch = max(need, min(104.4, (limit - top - (rows - 1) * gap) / rows))
            break
    if ch is None:
        ch = need
        deck.warnings.append(f"{s.key}: {len(cards)} input cards need {rows * need + (rows - 1) * gap:.0f}pt but only {limit - top:.0f}pt is available; shorten or remove cards")
    elif size < 10:
        deck.notes.append(f"{s.key}: input card text set at {size}pt (not 10pt) so every card fits")
    for i, (kind, c) in enumerate(cards):
        x = LEFT + (i % 2) * (cw + gap)
        y = top + (i // 2) * (ch + gap)
        if kind == "input":
            s.box(x, y, cw, ch, fill=WHITE, line=BORDER)
            s.text(x + 11.5, y + 4.3, text_w, 18.7, P([R(c["name"], 12, True)]), anchor="mid", what="(input name)")
            s.text(x + 11.5, y + 23.8, text_w, 13.0, P([R("From: " + c["from"], 9, True, BLUE)]), anchor="mid", what="(input source)")
            s.text(x + 11.5, y + 38.2, text_w, ch - 38.2 - 1.0, P([R(c["text"], size)]), what="(input card)")
        else:
            s.box(x, y, cw, ch, fill=GRAY, line=BORDER)
            s.text(x + 11.5, y + 4.3, text_w, 18.7, P([R(c["name"], 12, True, MUTED)]), anchor="mid", what="(card name)")
            s.text(x + 11.5, y + 23.8, text_w, ch - 23.8 - 1.0, P([R(c["text"], size)]), what="(gray card)")
    if choices:
        s.text(LEFT, band_top, 568.8, 20.2, P([R(choices["heading"], 10.5, True, BLUE)]), anchor="mid", check=False)
        for i, c in enumerate(items):
            x = LEFT + i * (ccw + cgap)
            y = band_top + 20.2
            s.box(x, y, ccw, c_h, fill=LAVENDER, line=BORDER)
            nh = max(2, name_lines) * 10.5 * LINE + 3.4
            s.text(x + 7.2, y + 2.9, ccw - 14.4, nh, P([R(c["name"], 10.5, True)]), what="(choice name)")
            s.text(x + 7.2, y + 2.9 + nh, ccw - 14.4, c_h - nh - 4.0, P([R(c["text"], 9.5)]), what="(choice card)")
    rx, rw = 640.8, 275.8
    s.text(rx, 126.7, 273.6, 20.2, P([R(ir["roles_heading"], 10.5, True, BLUE)]), anchor="mid", check=False)
    y = 148.3
    for group in ir["role_groups"]:
        body = []
        for k, role in enumerate(group["roles"]):
            name = [R(role["name"], 10.5, True)]
            if role.get("open"):
                name.append(R("  seat open", 9, True, MUTED))
            body.append(P(name, before=5 if k else 0))
            body.append(P([R(role["does"], 10.5)]))
        bh = paras_height(body, 249.8)
        ph_ = 27.4 + bh + 16.0
        s.box(rx, y, rw, ph_, fill=LAVENDER if group.get("client") else WHITE, line=BORDER)
        s.text(rx + 13.0, y + 5.8, 249.8, 20.2, P([R(group["label"], 11.5, True, MUTED)]), anchor="mid", check=False)
        s.text(rx + 13.0, y + 27.4, 249.8, bh + 2, body)
        y += ph_ + 8.7
    if y - 8.7 > 481.0:
        deck.warnings.append(f"{s.key}: role panels run to {y - 8.7:.0f}pt, past the content area (481pt)")
    evidence_note(s, ir.get("evidence"))
    return s


# ------------------------------------------------------------------------------------ card grids
CARD_PAD = 11.5


def card_paragraphs(deck, c, st=NORMAL):
    title = []
    if c.get("number"):
        title.append(R(str(c["number"]) + "  ", st["num"], True, BLUE))
    title.append(R(c["name"], st["name"], True))
    body = [P([R(c["text"], st["text"])])]
    if c.get("tag"):
        body.append(P([R(deck.tag_label[c["tag"]], st["tag"], True, TAG_COLOR[c["tag"]])], before=5))
    third = source_runs(deck, c.get("sources"), st["src"], c.get("note"))
    if third:
        body.append(P(third))
    return P(title), body


def title_extra(title, w, st):
    """Extra height a card needs when its title wraps past one line."""
    return (para_lines(title, w - 2 * CARD_PAD)[0] - 1) * st["name"] * LINE


def card_need(deck, c, w, st=NORMAL, pad=7.2):
    title, body = card_paragraphs(deck, c, st)
    return st["body_y"] + title_extra(title, w, st) + paras_height(body, w - 2 * CARD_PAD) + pad


def draw_card(deck, s, c, x, y, w, h, fill=None, st=NORMAL):
    title, body = card_paragraphs(deck, c, st)
    extra = title_extra(title, w, st)
    s.box(x, y, w, h, fill=fill or TAG_FILL.get(c.get("tag"), WHITE), line=BORDER)
    if extra:
        s.text(x + CARD_PAD, y + 7.2 + (st["title_h"] - st["name"] * LINE) / 2, w - 2 * CARD_PAD, st["name"] * LINE + extra + 1.0, title, what="(card title)")
    else:
        s.text(x + CARD_PAD, y + 7.2, w - 2 * CARD_PAD, st["title_h"], title, anchor="mid", what="(card title)")
    s.text(x + CARD_PAD, y + st["body_y"] + extra, w - 2 * CARD_PAD, h - st["body_y"] - extra - 2.5, body, what="(card)")


def mapping_need(deck, m, w):
    _t, body = card_paragraphs(deck, m)
    return 30.2 + paras_height(body, w - 2 * CARD_PAD) + 6.0 + math.ceil(len(m["pairs"]) / 2) * 18.1 + 11.5


def draw_mapping(deck, s, m, x, y, w, h):
    title, body = card_paragraphs(deck, m)
    s.box(x, y, w, h, fill=TAG_FILL.get(m.get("tag"), WHITE), line=BORDER)
    s.text(x + CARD_PAD, y + 7.2, w - 2 * CARD_PAD, 21.6, title, anchor="mid", what="(mapping title)")
    bh = paras_height(body, w - 2 * CARD_PAD)
    s.text(x + CARD_PAD, y + 30.2, w - 2 * CARD_PAD, bh + 2, body)
    pairs = m["pairs"]
    half = math.ceil(len(pairs) / 2)
    tw = w - 2 * CARD_PAD - 4.8
    shares = [177.2, 66.9, 192.9, 114.2]
    widths = [tw * v / sum(shares) for v in shares]
    ty = y + 30.2 + bh + 6.0
    for r in range(half):
        cells = list(pairs[r]) + (list(pairs[r + half]) if r + half < len(pairs) else ["", ""])
        cx = x + CARD_PAD
        for k, cell in enumerate(cells):
            s.box(cx, ty + r * 18.1, widths[k], 18.1, line="E3D5BF", line_w=0.5, square=True)
            bold = k in (1, 3) and cell[:1].isdigit()
            s.text(cx + 5.0, ty + r * 18.1, widths[k] - 8.0, 18.1, P([R(cell, 10, bold)]), anchor="mid", what="(mapping cell)")
            cx += widths[k]


def paginate(deck, cards, bands, mapping, gap, top, limit, st, cols=3, pad=7.2, band_gap=11.6, band_extra=3.0):
    """Split cards into pages. Bands go on the first page, the mapping on the last."""
    cw = (GRID_W - gap * (cols - 1)) / cols
    rows = [cards[i:i + cols] for i in range(0, len(cards), cols)]
    need = [max(card_need(deck, c, cw, st, pad) for c in row) for row in rows]
    band_layout, band_total = [], 0.0
    for b in bands or []:
        n = len(b["cards"])
        bw = (GRID_W - gap * (n - 1)) / n
        bh = max(card_need(deck, c, bw, st, pad) for c in b["cards"]) + band_extra
        band_layout.append((b, bw, bh))
        band_total += band_gap + 21.6 + bh
    pages, i, first = [], 0, True
    while i < len(rows) or first:
        avail = limit - top - (band_total if first else 0.0)
        take, used = [], 0.0
        while i < len(rows) and used + need[i] + (gap if take else 0) <= avail + 0.5:
            used += need[i] + (gap if take else 0)
            take.append(i)
            i += 1
        if not take and i < len(rows):          # one row taller than the page: place it anyway
            take.append(i)
            used = need[i]
            i += 1
        pages.append({"rows": take, "used": used, "avail": avail, "bands": band_layout if first else [], "band_total": band_total if first else 0.0, "mapping": None})
        first = False
    if mapping:
        last = pages[-1]
        n = len(last["rows"])
        free = (cols - len(rows[last["rows"][-1]])) if n else 0
        if free:
            span = free * cw + (free - 1) * gap
            m_top = top + sum(need[r] for r in last["rows"][:-1]) + gap * (n - 1)
        else:
            span = GRID_W
            m_top = top + last["used"] + (gap if n else 0)
        m_need = mapping_need(deck, mapping, span)
        if m_top + m_need > limit - last["band_total"] + 0.5:
            pages.append({"rows": [], "used": 0.0, "avail": limit - top, "bands": [], "band_total": 0.0,
                          "mapping": {"x": LEFT, "w": GRID_W, "free": 0, "need": mapping_need(deck, mapping, GRID_W)}})
        else:
            last["mapping"] = {"x": LEFT + (cols - free) * (cw + gap) if free else LEFT, "w": span, "free": free, "need": m_need}
    extra = 36.0                                 # how much every row can grow, kept equal across pages
    for pg in pages:
        n = len(pg["rows"])
        if not n:
            continue
        room = pg["avail"] - pg["used"]
        mp = pg["mapping"]
        if mp and mp["free"]:
            allow = room / n
            if n > 1:
                before = top + sum(need[r] for r in pg["rows"][:-1]) + gap * (n - 1)
                allow = min(allow, (limit - mp["need"] - before) / (n - 1))
        elif mp:
            allow = (room - gap - mp["need"]) / n
        else:
            allow = room / n
        extra = min(extra, max(0.0, allow))
    return {"pages": pages, "rows": rows, "need": need, "cw": cw, "gap": gap, "top": top, "limit": limit, "extra": extra,
            "band_gap": band_gap, "args": dict(gap=gap, top=top, limit=limit, pad=pad, band_gap=band_gap, band_extra=band_extra)}


def choose_layout(deck, cache_key, cards, bands, mapping, st):
    """Try roomy spacing first, then tighter spacing if that saves a page."""
    if cache_key in deck.grid_cache:
        return deck.grid_cache[cache_key]
    before = len(deck.warnings)
    best = None
    tries = (dict(gap=8.6, top=129.6, limit=482.4),                                   # roomy
             dict(gap=5.7, top=129.6, limit=482.4),                                   # tighter gaps
             dict(gap=5.7, top=122.4, limit=482.4),                                   # start higher
             dict(gap=5.7, top=122.4, limit=482.4, pad=4.0, band_gap=4.0, band_extra=0.0))   # compact cards
    for args in tries:
        lay = paginate(deck, cards, bands, mapping, st=st, **args)
        if best is None or len(lay["pages"]) < len(best["pages"]):
            best = lay
    del deck.warnings[before:]                    # paginate is run several times; keep one set of source warnings
    paginate(deck, cards, bands, mapping, st=st, **best["args"])
    deck.grid_cache[cache_key] = best
    return best


def grid_view(deck, section, view_index, base_key, title, cont_title, cards, bands=None, mapping=None, st=NORMAL, note=None):
    lay = choose_layout(deck, base_key, cards, bands, mapping, st)
    rows, need, cw, gap, extra, top, limit = lay["rows"], lay["need"], lay["cw"], lay["gap"], lay["extra"], lay["top"], lay["limit"]
    band_gap = lay["band_gap"]
    keys = []
    for pi, page in enumerate(lay["pages"]):
        key = base_key + (f":{pi + 1}" if pi else "")
        s = deck.add(key)
        frame(deck, s, section, view_index, title if pi == 0 else cont_title([c for r in page["rows"] for c in rows[r]]), " (cont.)" if pi else "")
        y = top
        row_y = row_h = None
        for r in page["rows"]:
            row_y, row_h = y, need[r] + extra
            if row_y + row_h > limit + 0.5:
                deck.warnings.append(f"{key}: a row of cards runs to {row_y + row_h:.0f}pt, past the content area; shorten the longest card")
            for k, c in enumerate(rows[r]):
                draw_card(deck, s, c, LEFT + k * (cw + gap), row_y, cw, row_h, st=st)
                if c.get("number"):
                    deck.alias(f"task{c['number']}", key)
            y += row_h + gap
        mp = page["mapping"]
        if mp:
            if mp["free"] and page["rows"]:
                draw_mapping(deck, s, mapping, mp["x"], row_y, mp["w"], max(mp["need"], row_h))
            else:
                draw_mapping(deck, s, mapping, mp["x"], y if page["rows"] else top, mp["w"], mp["need"])
        by = limit - page["band_total"]
        for b, bw, bh in page["bands"]:
            s.text(LEFT, by + band_gap, 648.0, 20.2, P([R(b["heading"], 10.5, True, BLUE)]), anchor="mid", check=False)
            for k, c in enumerate(b["cards"]):
                draw_card(deck, s, c, LEFT + k * (bw + gap), by + band_gap + 21.6, bw, bh, fill=LAVENDER if b.get("fill") == "lavender" else None, st=st)
            by += band_gap + 21.6 + bh
        if note:
            evidence_note(s, note)
        else:
            legend(deck, s)
        keys.append(key)
    return keys


def step_view(deck, ph, section, view_index, step):
    def cont(cards_on_page):
        nums = [c["number"] for c in cards_on_page if c.get("number")]
        if nums:
            return f"Step {step['number']} {step['name']}, continued: tasks {nums[0]} to {nums[-1]}"
        return f"Step {step['number']} {step['name']}, continued"
    deck.alias(f"step{step['number']}", f"phase{ph['number']}:step{step['number']}")
    return grid_view(deck, section, view_index, f"phase{ph['number']}:step{step['number']}", step["title"], cont,
                     step["tasks"], step.get("bands"), step.get("mapping"))


# ------------------------------------------------------------------------------------ deliverables and approval
def deliverables(deck, ph, section, view_index):
    dv = ph["deliverables"]
    s = deck.add(f"phase{ph['number']}:deliverables")
    frame(deck, s, section, view_index, dv["title"])
    top, hh = 129.6, 234.0
    x = LEFT
    for lst in dv["lists"]:
        w = 244.8
        s.box(x, top, w, hh, fill=WHITE, line=BORDER)
        s.text(x + 14.4, top + 10.1, 216.0, 23.0, P([R(lst["name"], 15, True)]), anchor="mid", what="(deliverable name)")
        s.text(x + 14.4, top + 34.6, 216.0, 28.8, P([R(lst["subtitle"], 10.5, False, MUTED)]), what="(deliverable subtitle)")
        items = lst["items"]
        half = math.ceil(len(items) / 2)
        for col, chunk, start in ((0, items[:half], 1), (1, items[half:], half + 1)):
            s.text(x + 14.4 + col * 111.6, top + 68.4, 108.0, hh - 68.4 - 7.2, numbered(chunk, 10.5, 4, start), what=f"({lst['name']} sections)")
        x += w + 14.4
    texts = dv.get("texts", [])
    if texts:
        tw = LEFT + GRID_W - x
        gap = 13.6
        th = (hh - gap * (len(texts) - 1)) / len(texts)
        for k, t in enumerate(texts):
            y = top + k * (th + gap)
            s.box(x, y, tw, th, fill=WHITE, line=BORDER)
            s.text(x + 14.4, y + 8.6, tw - 28.8, 21.6, P([R(t["name"], 14, True)]), anchor="mid", what="(deliverable name)")
            s.text(x + 14.4, y + 33.1, tw - 28.8, th - 33.1 - 4.4, P([R(t["text"], 10.5)]), what=f"({t['name']})")
    s.text(LEFT, 374.4, 576.0, 20.2, P([R(dv["approval_heading"], 10.5, True, BLUE)]), anchor="mid", check=False)
    tests = dv["approval"]
    n = len(tests)
    gap = 10.8
    cw = (GRID_W - gap * (n - 1)) / n
    for k, t in enumerate(tests):
        cx = LEFT + k * (cw + gap)
        s.box(cx, 396.0, cw, 82.1, fill=LAVENDER if t.get("highlight") else WHITE, line=BORDER)
        s.text(cx + 10.1, 400.3, 21.6, 17.3, P([R(str(k + 1), 11, True, BLUE)]), anchor="mid", check=False)
        s.text(cx + 10.1, 417.6, cw - 20.2, 38.9, P([R(t["text"], 10)]), what="(approval test)")
        s.text(cx + 10.1, 457.9, cw - 20.2, 17.3, P([R(t["confirms"], 9.5, True, MUTED)]), anchor="mid", what="(who confirms)")
    evidence_note(s, dv.get("evidence"))
    return s


# ------------------------------------------------------------------------------------ cross-phase section
def tiers_view(deck, section, vi, v, key):
    s = deck.add(key)
    frame(deck, s, section, vi, v["title"])
    y = 133.2
    for t in v["tiers"]:
        style = t.get("style", "solid")
        optional = style == "optional"
        s.box(LEFT, y, 525.6, 69.1, fill={"solid": WHITE, "highlight": LAVENDER, "optional": "F6F6F9"}[style],
              line=MUTED if optional else BLUE, line_w=1.0 if optional else 2.25, dash=optional)
        s.text(59.0, y + 8.6, 244.8, 21.6, P([R(t["name"], 13, not optional, MUTED if optional else BLUE)]), anchor="mid", what="(tier name)")
        s.text(309.6, y + 8.6, 244.8, 21.6, P([R(t["when"], 11, False, MUTED)], align="r"), anchor="mid", what="(tier note)")
        s.text(59.0, y + 32.4, 496.8, 33.1, P([R(t["text"], 11.5, False, MUTED if optional else INK)]), what="(tier text)")
        y += 79.2
    s.text(597.6, 129.6, 316.8, 20.2, P([R(v["rules_heading"], 10.5, True, BLUE)]), anchor="mid", check=False)
    s.text(597.6, 152.6, 319.0, 216.0, bullets(v["rules"], 11.5, 6), what="(rules list)")
    cards = v.get("cards", [])
    if cards:
        s.text(LEFT, 370.1, 432.0, 20.2, P([R(v["cards_heading"], 10.5, True, BLUE)]), anchor="mid", check=False)
        gap = 8.6
        cw = (GRID_W - gap * (len(cards) - 1)) / len(cards)
        for i, c in enumerate(cards):
            draw_card(deck, s, c, LEFT + i * (cw + gap), 391.7, cw, 87.8)
    evidence_note(s, v.get("evidence"))
    return [key]


def cards_view(deck, section, vi, v, key):
    return grid_view(deck, section, vi, key, v["title"], lambda _c: v["title"] + ", continued", v["cards"], st=LARGE)


def panel_view(deck, section, vi, v, key):
    s = deck.add(key)
    frame(deck, s, section, vi, v["title"])
    steps = numbered(v["steps"], 13, 2)
    notes = [lead_in(a, b, 12, 4 if i else 0) for i, (a, b) in enumerate(v["notes"])]
    src = P([R("Sources: ", 10.5, True, MUTED)] + source_runs(deck, v.get("sources"), 10.5)) if v.get("sources") else None
    body_h = max(paras_height(steps, 330.7), paras_height(notes, 496.1))
    src_h = paras_height([src], 846.0) if src else 0.0
    src_gap = 14.0                                    # space between the two columns and the sources line
    ph_ = 39.7 + body_h + (src_gap + src_h if src else 0) + 16.0
    s.box(LEFT, 129.6, GRID_W, ph_, fill=LAVENDER, line=BORDER)
    s.text(57.6, 137.5, 472.4, 20.1, P([R(v["heading"], 12, True, BLUE)]), anchor="mid", what="(panel heading)")
    s.text(57.6, 169.3, 330.7, body_h + 2, steps)
    s.text(409.4, 169.3, 496.1, body_h + 2, notes)
    if src:
        s.text(57.6, 169.3 + body_h + src_gap, 846.0, src_h + 2, src)
    foot_y = 129.6 + ph_ + 9.0
    if v.get("footnote"):
        s.text(LEFT, foot_y, TEXT_W, 21.6, P([R(v["footnote"], 11, False, MUTED)]), what="(panel footnote)")
    if foot_y + 14 > 505:
        deck.warnings.append(f"{key}: the panel runs to {129.6 + ph_:.0f}pt and pushes its footnote into the footer")
    return [key]


def evidence_view(deck, section, vi, v, key):
    s = deck.add(key)
    frame(deck, s, section, vi, v["title"])
    tiles = v["tiles"]
    n = len(tiles)
    gap = 12.96
    tw = (GRID_W - gap * (n - 1)) / n
    for i, t in enumerate(tiles):
        x = LEFT + i * (tw + gap)
        is_open = t.get("tone") == "open"
        s.box(x, 129.6, tw, 97.2, fill=ORANGE_FILL if is_open else WHITE, line=BORDER)
        s.text(x + 14.4, 135.4, tw - 28.8, 43.2, P([R(str(t["number"]), 32, True, ORANGE if is_open else BLUE)]), anchor="mid", check=False)
        s.text(x + 14.4, 180.0, tw - 25.2, 43.2, P([R(t["text"], 10.5)]), what="(tile caption)")
    panels = v["panels"]
    k = len(panels)
    pgap = 14.4
    pw = (GRID_W - pgap * (k - 1)) / k
    for i, p in enumerate(panels):
        x = LEFT + i * (pw + pgap)
        s.box(x, 244.8, pw, 230.4, fill=PANEL_FILL[p.get("style", "white")], line=BORDER)
        s.text(x + 14.4, 252.0, pw - 29.5, 20.2, P([R(p["label"], 10.5, True, BLUE)]), anchor="mid", what="(panel label)")
        has_note = bool(p.get("note") or p.get("sources"))
        note_h = 0.0
        if has_note:                                  # the note sits at the foot of the panel and takes the lines it needs
            note = P(source_runs(deck, p.get("sources"), 9, p.get("note")))
            note_h = max(25.9, paras_height([note], pw - 25.9) + 1.0)
            s.text(x + 14.4, 472.3 - note_h, pw - 25.9, note_h, note, what="(panel note)")
        s.text(x + 14.4, 276.5, pw - 25.9, (472.3 - note_h - 4.3 if has_note else 469.5) - 276.5, bullets(p["items"], 10.5, 4), what=f"({p['label']} list)")
    evidence_note(s, v.get("evidence"))
    return [key]


SOURCES_PER_PAGE = 26


def sources_views(deck, section, vi, v, key_base):
    srcs = deck.spec["sources"]
    pages = [srcs[i:i + SOURCES_PER_PAGE] for i in range(0, len(srcs), SOURCES_PER_PAGE)] or [[]]
    keys = []
    for pi, chunk in enumerate(pages):
        key = f"all:{vi + pi}"
        s = deck.add(key)
        title = v["title"] + (f" ({pi + 1} of {len(pages)})" if len(pages) > 1 else "")
        frame(deck, s, section, vi + pi, title)
        half = math.ceil(len(chunk) / 2) if len(chunk) > SOURCES_PER_PAGE // 2 else len(chunk)
        for col, part in enumerate((chunk[:half], chunk[half:])):
            if not part:
                continue
            x = LEFT + col * 446.4
            s.text(x + 1.0, 129.6, 300.0, 15.6, P([R("Source", 9.5, True, MUTED)]), anchor="mid", check=False)
            s.text(x + 302.4, 129.6, 124.6, 15.6, P([R("Status", 9.5, True, MUTED)]), anchor="mid", check=False)
            for r, src in enumerate(part):
                ry = 148.3 + r * 19.8
                s.text(x + 1.0, ry, 298.0, 19.8, P([R(src["name"], 10.5, False, MUTED, src.get("url"))]), anchor="mid", what="(source name)")
                live = src.get("status", "").lower().startswith("opened live")
                s.text(x + 302.4, ry, 124.6, 19.8, P([R(src.get("status", ""), 9.5, False, GREEN if live else MUTED)]), anchor="mid", what="(source status)")
            s.rule(x, 148.3 + len(part) * 19.8, 427.0, 0.75, BORDER)
        evidence_note(s, v.get("evidence"))
        keys.append(key)
    return keys


def decisions_view(deck, section, vi, v, key):
    s = deck.add(key)
    frame(deck, s, section, vi, v["title"])
    s.box(LEFT, 129.6, 432.0, 345.6, fill=WHITE, line=BORDER)
    s.text(57.6, 136.8, 360.0, 20.2, P([R(v["decisions_label"], 10.5, True, BLUE)]), anchor="mid", check=False)
    y = 161.3
    count = 0
    g = v.get("gating")
    if g:
        callout = P([R(g["callout"], 9.5, True, ORANGE)])
        ch = paras_height([callout], 381.6)
        items = numbered(g["items"], 11.5, 6)
        ih = paras_height(items, 381.6)
        bh = 4.3 + ch + 3.0 + ih + 7.0
        s.box(57.6, y, 403.2, bh, fill=ORANGE_FILL, line=BORDER)
        s.text(68.4, y + 4.3, 381.6, ch + 1, callout)
        s.text(68.4, y + 4.3 + ch + 3.0, 381.6, ih + 2, items)
        y += bh + 13.0
        count = len(g["items"])
    rest = numbered(v.get("decisions", []), 11.5, 7, count + 1)
    if rest:
        s.text(57.6, y, 403.2, 470.9 - y, rest, what="(decisions list)")
    right = v.get("right", [])
    ry = 129.6
    needs = []
    for blk in right:
        body = numbered(blk["numbered"], 11, 4) if blk.get("numbered") else bullets(blk["bullets"], 11, 4)
        needs.append((blk, body, 30.2 + paras_height(body, 399.6) + 10.0))
    total = sum(n for _b, _p, n in needs) + 10.8 * max(0, len(needs) - 1)
    spare = max(0.0, 345.6 - total)
    for blk, body, need in needs:
        h = need + spare / len(needs)
        s.box(488.2, ry, 428.4, h, fill=PANEL_FILL[blk.get("style", "white")], line=BORDER)
        s.text(502.6, ry + 7.2, 360.0, 20.2, P([R(blk["label"], 10.5, True, BLUE)]), anchor="mid", check=False)
        s.text(502.6, ry + 30.2, 399.6, h - 30.2 - 4.0, body, what=f"({blk['label']})")
        ry += h + 10.8
    if total > 345.6:
        deck.warnings.append(f"{key}: the right-hand blocks need {total:.0f}pt but only 346pt is available")
    evidence_note(s, v.get("evidence"))
    return [key]


VIEW_DRAWERS = {"tiers": tiers_view, "cards": cards_view, "panel": panel_view, "evidence": evidence_view, "decisions": decisions_view}


# ------------------------------------------------------------------------------------ build
def phase_views(ph):
    n = ph["number"]
    views = [("Overview", f"phase{n}:overview"), (ph["inputs_roles"].get("view_label", "Inputs and roles"), f"phase{n}:inputs")]
    for st in ph["steps"]:
        views.append((f"Step {st['number']} {st['name']}", f"phase{n}:step{st['number']}"))
    views.append(("Deliverables and approval", f"phase{n}:deliverables"))
    return views


def all_views(spec):
    views, i = [], 0
    for v in spec.get("all_phases", []):
        if v["type"] == "sources":
            pages = max(1, math.ceil(len(spec.get("sources", [])) / SOURCES_PER_PAGE))
            for p in range(pages):
                views.append((v["view"] + (f" {p + 1}" if pages > 1 else ""), f"all:{i}"))
                i += 1
        else:
            views.append((v["view"], f"all:{i}"))
            i += 1
    return views


def plan_pages(deck):
    """Work out page numbers before drawing, so early slides can point at later ones."""
    spec = deck.spec
    page = 1                                               # cover
    start = spec.get("start", {})
    page += sum(1 for k in ("model_map", "matrix", "roles") if k in start)
    for ph in spec["phases"]:
        if "overview" not in ph:
            continue
        n = ph["number"]
        deck.page_of[f"phase{n}:first"] = page + 1
        count = 2
        for st in ph["steps"]:
            count += len(choose_layout(deck, f"phase{n}:step{st['number']}", st["tasks"], st.get("bands"), st.get("mapping"), NORMAL)["pages"])
        count += 1
        page += count
        deck.page_of[f"phase{n}:last"] = page


REF = re.compile(r"\{slide:([^}]+)\}")


def fill_refs(node, lookup):
    """Replace every {slide:REF} in the spec's text. lookup(ref) returns the text to put there."""
    if isinstance(node, str):
        return REF.sub(lambda m: lookup(m.group(1).strip()), node)
    if isinstance(node, list):
        return [fill_refs(v, lookup) for v in node]
    if isinstance(node, dict):
        return {k: fill_refs(v, lookup) for k, v in node.items()}
    return node


def build(spec, out_path, logo=None):
    """Draw the deck. If the spec uses {slide:REF}, draw once to learn the page numbers, then draw again with them filled in."""
    if not REF.search(json.dumps(spec)):
        return build_once(spec, out_path, logo)
    draft, _m, _s = build_once(fill_refs(copy.deepcopy(spec), lambda ref: "00"), None, logo)
    refs, unknown = draft.references(), []

    def lookup(ref):
        if ref not in refs:
            unknown.append(ref)
            return "?"
        return str(refs[ref])
    deck, made, skipped = build_once(fill_refs(copy.deepcopy(spec), lookup), out_path, logo)
    for ref in sorted(set(unknown)):
        deck.warnings.append(f"{{slide:{ref}}} does not match any slide; valid names include: {', '.join(sorted(k for k in refs if not k.startswith('task'))[:40])}")
    if deck.order != draft.order:
        deck.warnings.append("page numbers moved when slide references were filled in; check every 'slide N' in the deck")
    return deck, made, skipped


def build_once(spec, out_path, logo=None):
    deck = Deck(spec, logo)
    plan_pages(deck)
    cover(deck)
    start = spec.get("start", {})
    if start:
        views = [(lab, f"start:{i}") for i, lab in enumerate(start["views"])]
        section = {"id": "start", "views": views}
        if "model_map" in start:
            model_map(deck, section)
        if "matrix" in start:
            offering_matrix(deck, section)
        if "roles" in start:
            roles_chart(deck, section)
    for ph in spec["phases"]:
        if "overview" not in ph:
            continue
        section = {"id": f"phase{ph['number']}", "views": phase_views(ph)}
        phase_overview(deck, ph, section)
        inputs_roles(deck, ph, section, 1)
        for k, st in enumerate(ph["steps"]):
            step_view(deck, ph, section, 2 + k, st)
        deliverables(deck, ph, section, 2 + len(ph["steps"]))
    if spec.get("all_phases"):
        section = {"id": "all", "views": all_views(spec)}
        i = 0
        for v in spec["all_phases"]:
            if v["type"] == "sources":
                deck.alias("sources", f"all:{i}")
                i += len(sources_views(deck, section, i, v, "all"))
            else:
                deck.alias(v["type"], f"all:{i}")
                VIEW_DRAWERS[v["type"]](deck, section, i, v, f"all:{i}")
                i += 1
    register = [src["name"] for src in spec.get("sources", [])]
    deck.uncited = [n for n in register if n not in deck.cited]
    made, skipped = deck.finish(out_path) if out_path else (0, 0)
    return deck, made, skipped


if __name__ == "__main__":
    args = sys.argv[1:]
    bundled = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "augmind-logo-cover.png")
    logo = args[args.index("--logo") + 1] if "--logo" in args else (bundled if os.path.exists(bundled) and "--no-logo" not in args else None)
    spec = json.load(open(args[0]))
    deck, made, skipped = build(spec, args[1], logo)
    print(f"slides: {len(deck.order)}  |  slide links made: {made}, pointing at slides not in this build: {skipped}")
    print("MUST FIX (text that does not fit, or a broken reference):", len(deck.warnings))
    for wmsg in deck.warnings:
        print("  -", wmsg)
    print("adjusted automatically (fits; shorten the text to get the standard size back):", len(deck.notes))
    for nmsg in deck.notes:
        print("  -", nmsg)
    print("sources on the register that no slide cites:", len(deck.uncited))
    for name in deck.uncited:
        print("  -", name)
    print("page numbers:", ", ".join(f"{k}={v}" for k, v in sorted(deck.references().items(), key=lambda kv: (kv[1], kv[0])) if not k.startswith("task")))
    sys.exit(2 if deck.warnings or skipped else 0)
