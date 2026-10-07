#!/usr/bin/env python3
"""Part E builder: MBGL initiation research document (Word, python-docx).

Deterministic. Reads:
  work/analysis/*.md, work/deliverables/PART_A_SUMMARY.md, work/transcripts/*.md,
  work/canonical/primary.csv, work/canonical/accounting_notes.csv, work/market/PART_B_SERIES_PLAN.md
Writes:
  work/deliverables/MBGL_Research_Document.docx

House style: Arial; navy (#1F3864) headings; banded tables (navy header row, #D9E1F2 alternate rows);
quote callouts (left navy border, shaded, italic quote + attribution); tier tags styled on every figure;
orange bold [TO COLLECT] placeholders (#E36C09) collected into a placeholder register at the back.

Two-pass build: pass 1 is converted to PDF with LibreOffice (if available) to locate the page of every
section heading and every placeholder; pass 2 writes those page numbers into the contents list and the
placeholder register. Without LibreOffice the page column falls back to "n/a".

Rules: every number in the text comes from the input files (tables are parsed from the analysis files,
financials from primary.csv, quotes verbatim from the transcript quote banks; the builder asserts each quote
exists). Anything not in the inputs is a [TO COLLECT] placeholder.
"""
import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import OrderedDict

from docx import Document
from docx.enum.section import WD_ORIENT  # noqa: F401
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Inches, Emu

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AN = os.path.join(ROOT, "analysis")
TR = os.path.join(ROOT, "transcripts")
CAN = os.path.join(ROOT, "canonical")
OUT = os.path.join(ROOT, "deliverables", "MBGL_Research_Document.docx")

NAVY = RGBColor(0x1F, 0x38, 0x64)
NAVY_HEX = "1F3864"
BAND_HEX = "D9E1F2"
QUOTE_FILL = "EEF2F9"
ORANGE = RGBColor(0xE3, 0x6C, 0x09)
GREY = RGBColor(0x59, 0x59, 0x59)
TAGC = RGBColor(0x2E, 0x54, 0x8C)
FONT = "Arial"
DOC_DATE = "2026-10-06"


# ----------------------------------------------------------------------------- input readers
def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


LINK_RE = re.compile(r"\[([^\[\]]*)\]\((?:https?://)[^)]*\)")


def clean(s):
    s = LINK_RE.sub(r"\1", s)
    s = s.replace("<br>", " ").strip()
    return s


def md_table(path, anchor, cols=None, keep=None, drop_cols_tags=False):
    """Return (header, rows) of the markdown table whose header line starts with `anchor`."""
    lines = read(path).splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith(anchor):
            start = i
            break
    if start is None:
        raise SystemExit(f"table anchor not found: {anchor!r} in {path}")
    block = []
    for ln in lines[start:]:
        if not ln.startswith("|"):
            break
        block.append(ln)
    parsed = []
    for ln in block:
        cells = [clean(c) for c in ln.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c.strip()) or c.strip() == "" for c in cells) and any("-" in c for c in cells):
            continue
        parsed.append(cells)
    header, rows = parsed[0], parsed[1:]
    if keep:
        rows = [r for r in rows if keep(r)]
    if cols is not None:
        header = [header[c] for c in cols]
        rows = [[r[c] if c < len(r) else "" for c in cols] for r in rows]
    return header, rows


def primary():
    d = {}
    with open(os.path.join(CAN, "primary.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d.setdefault(r["canon_key"], {})[r["period"]] = float(r["value"])
    return d


P = primary()


def pv(key, per):
    return P.get(key, {}).get(per)


QUOTE_FILES = {
    "ID": "MBGL_2026-05-12_investor-day.md",
    "Q2": "MBGL_2026-08-07_q2-2026-earnings-call.md",
    "GS": "MBGL_2026-09-10_goldman-sachs-communacopia.md",
}
QLINE = re.compile(
    r'^- "(?P<q>.*)" — (?P<name>[^(]+?) \((?P<title>.*)\), (?P<event>[^,]+), '
    r"(?P<date>\d{4}-\d{2}-\d{2}), \[(?P<ts>[\d.]+)s\]\((?P<url>[^)]+)\)\s*$"
)
_QCACHE = {}


def get_quote(bank, needle):
    if bank not in _QCACHE:
        _QCACHE[bank] = [ln for ln in read(os.path.join(TR, QUOTE_FILES[bank])).splitlines() if ln.startswith('- "')]
    hits = [ln for ln in _QCACHE[bank] if needle in ln]
    if len(hits) != 1:
        raise SystemExit(f"quote needle {needle!r} in {bank}: {len(hits)} hits")
    m = QLINE.match(hits[0])
    if not m:
        raise SystemExit(f"quote line unparsable: {hits[0][:120]}")
    return m.groupdict()


# ----------------------------------------------------------------------------- formatting helpers
def fmt(x, dec=0, paren=True):
    if x is None:
        return "—"
    if dec == 0:
        s = f"{abs(x):,.0f}"
    else:
        s = f"{abs(x):,.{dec}f}"
    if x < 0:
        return f"({s})" if paren else f"−{s}"
    return s


def pct(a, b, dec=1):
    if a is None or b is None or b == 0:
        return "—"
    return f"{100.0 * a / b:.{dec}f}%"


def growth(a, b, dec=1):
    if a is None or b is None or b == 0:
        return "—"
    g = 100.0 * (a / b - 1)
    return f"{g:+.{dec}f}%".replace("-", "−")


# ----------------------------------------------------------------------------- document state
class Builder:
    TAG_RE = r"\[(?:D|C|E|IR|X|context|gap)(?:[^\[\]]{0,28})\]"
    TOKEN = re.compile(r"(\*\*.+?\*\*|\{\{TC:.+?\}\}|" + TAG_RE + ")")

    def __init__(self, pages=None):
        self.doc = Document()
        self.pages = pages or {}
        self.section = "Cover"
        self.placeholders = []  # (id, section, item)
        self.headings = []  # (number, title)
        self._setup()

    # -- setup
    def _font(self, style, size=None, bold=None, color=None, italic=None):
        f = style.font
        f.name = FONT
        rpr = style.element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts")
            rpr.insert(0, rf)
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            if rf.get(qn(a)) is not None:
                del rf.attrib[qn(a)]
        for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rf.set(qn(a), FONT)
        if size:
            f.size = Pt(size)
        if bold is not None:
            f.bold = bold
        if italic is not None:
            f.italic = italic
        if color is not None:
            f.color.rgb = color

    def _setup(self):
        d = self.doc
        sec = d.sections[0]
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)
        sec.left_margin = sec.right_margin = Inches(0.85)
        sec.top_margin, sec.bottom_margin = Inches(0.8), Inches(0.75)
        st = d.styles
        self._font(st["Normal"], 9.5)
        pf = st["Normal"].paragraph_format
        pf.space_after = Pt(4)
        pf.line_spacing = 1.12
        for name, size, sb, sa in (("Heading 1", 15, 14, 6), ("Heading 2", 11.5, 10, 4), ("Heading 3", 10, 8, 3)):
            s = st[name]
            self._font(s, size, True, NAVY, False)
            s.paragraph_format.space_before = Pt(sb)
            s.paragraph_format.space_after = Pt(sa)
            s.paragraph_format.keep_with_next = True
        for name in ("List Bullet", "List Number", "List Bullet 2", "Title"):
            self._font(st[name], 9.5 if name != "Title" else 24)
        st["List Bullet"].paragraph_format.space_after = Pt(2)
        st["List Bullet 2"].paragraph_format.space_after = Pt(1)
        st["List Number"].paragraph_format.space_after = Pt(3)
        # header / footer
        sec.different_first_page_header_footer = True
        hp = sec.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = hp.add_run("Mobility Global Inc. (NYSE: MBGL) · Initiation research document · " + DOC_DATE)
        r.font.size, r.font.color.rgb, r.font.name = Pt(7.5), GREY, FONT
        fp = sec.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = fp.add_run("Prepared from primary filings via Quartr; see Appendix A for source limitations.   Page ")
        r.font.size, r.font.color.rgb, r.font.name = Pt(7.5), GREY, FONT
        self._field(fp, "PAGE")

    def _field(self, p, code):
        r = p.add_run()
        r.font.size, r.font.name = Pt(7.5), FONT
        for t, txt in (("begin", None), (None, code), ("end", None)):
            if t:
                e = OxmlElement("w:fldChar")
                e.set(qn("w:fldCharType"), t)
                r._r.append(e)
                if t == "begin":
                    it = OxmlElement("w:instrText")
                    it.set(qn("xml:space"), "preserve")
                    it.text = code
                    r._r.append(it)
                    sep = OxmlElement("w:fldChar")
                    sep.set(qn("w:fldCharType"), "separate")
                    r._r.append(sep)
                    t2 = OxmlElement("w:t")
                    t2.text = "1"
                    r._r.append(t2)

    # -- inline rich text
    def rich(self, p, text, size=None, bold=False, italic=False, color=None):
        for tok in self.TOKEN.split(text):
            if not tok:
                continue
            if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
                self.rich(p, tok[2:-2], size, True, italic, color)
                continue
            if tok.startswith("{{TC:"):
                item = tok[5:-2].strip()
                n = len(self.placeholders) + 1
                self.placeholders.append((n, self.section, item))
                r = p.add_run(f"[TO COLLECT #{n}: {item}]")
                r.bold = True
                r.font.color.rgb = ORANGE
                if size:
                    r.font.size = Pt(size)
                continue
            if re.fullmatch(self.TAG_RE, tok):
                r = p.add_run(tok)
                r.bold = True
                r.font.size = Pt((size or 9.5) - 1.5)
                r.font.color.rgb = TAGC
                continue
            r = p.add_run(tok)
            r.bold = bold
            r.italic = italic
            if size:
                r.font.size = Pt(size)
            if color is not None:
                r.font.color.rgb = color
        return p

    # -- block elements
    def h1(self, title, number=None, page_break=True):
        label = f"{number} {title}" if number is not None else title
        self.section = label
        self.headings.append(label)
        h = self.doc.add_heading(label, level=1)
        h.paragraph_format.page_break_before = page_break
        return h

    def h2(self, title):
        return self.doc.add_heading(title, level=2)

    def h3(self, title):
        return self.doc.add_heading(title, level=3)

    def p(self, text, size=None, italic=False, color=None, align=None, space_after=None):
        para = self.doc.add_paragraph()
        self.rich(para, text, size=size, italic=italic, color=color)
        if align:
            para.alignment = align
        if space_after is not None:
            para.paragraph_format.space_after = Pt(space_after)
        return para

    def note(self, text):
        return self.p(text, size=7.5, italic=True, color=GREY, space_after=6)

    def bullets(self, items, style="List Bullet"):
        for it in items:
            if isinstance(it, (list, tuple)):
                for sub in it:
                    self.rich(self.doc.add_paragraph(style="List Bullet 2"), sub)
            else:
                self.rich(self.doc.add_paragraph(style=style), it)

    def numbered(self, items):
        for i, it in enumerate(items, 1):
            para = self.doc.add_paragraph()
            para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.first_line_indent = Inches(-0.25)
            para.paragraph_format.space_after = Pt(4)
            r = para.add_run(f"{i}.  ")
            r.bold = True
            r.font.color.rgb = NAVY
            self.rich(para, it)

    @staticmethod
    def _shade(cell, fill):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), fill)
        tcPr.append(shd)

    @staticmethod
    def _borders(tbl, spec):
        tblPr = tbl._tbl.tblPr
        b = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement(f"w:{edge}")
            val, sz, color = spec.get(edge, ("nil", 0, "auto"))
            e.set(qn("w:val"), val)
            e.set(qn("w:sz"), str(sz))
            e.set(qn("w:space"), "0")
            e.set(qn("w:color"), color)
            b.append(e)
        tblPr.append(b)

    @staticmethod
    def _cell_margins(tbl, top=40, bottom=40, left=70, right=70):
        tblPr = tbl._tbl.tblPr
        m = OxmlElement("w:tblCellMar")
        for k, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
            e = OxmlElement(f"w:{k}")
            e.set(qn("w:w"), str(v))
            e.set(qn("w:type"), "dxa")
            m.append(e)
        tblPr.append(m)

    def table(self, header, rows, widths=None, size=8, num_cols=None, first_col_bold=False, caption=None, source=None):
        """Banded table: navy header, #D9E1F2 alternate rows. widths in inches (relative ok)."""
        if caption:
            cp = self.doc.add_paragraph()
            cp.paragraph_format.space_before = Pt(4)
            cp.paragraph_format.space_after = Pt(2)
            cp.paragraph_format.keep_with_next = True
            self.rich(cp, caption, size=8.5, bold=True, color=NAVY)
        ncol = len(header)
        tbl = self.doc.add_table(rows=1 + len(rows), cols=ncol)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        self._borders(tbl, {e: ("single", 4, "BFBFBF") for e in ("top", "left", "bottom", "right", "insideH", "insideV")})
        self._cell_margins(tbl)
        total = 6.8
        if widths is None:
            widths = [1] * ncol
        s = float(sum(widths))
        w_in = [total * w / s for w in widths]
        num_cols = set(num_cols or [])
        for ri, row in enumerate([header] + rows):
            tr = tbl.rows[ri]
            trPr = tr._tr.get_or_add_trPr()
            cs = OxmlElement("w:cantSplit")
            trPr.append(cs)
            if ri == 0:
                th = OxmlElement("w:tblHeader")
                trPr.append(th)
            for ci in range(ncol):
                cell = tr.cells[ci]
                cell.width = Inches(w_in[ci])
                txt = row[ci] if ci < len(row) else ""
                para = cell.paragraphs[0]
                para.paragraph_format.space_after = Pt(0)
                para.paragraph_format.line_spacing = 1.0
                if ri == 0:
                    self._shade(cell, NAVY_HEX)
                    self.rich(para, txt.replace("**", ""), size=size, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
                    for r in para.runs:
                        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                else:
                    if ri % 2 == 0:
                        self._shade(cell, BAND_HEX)
                    self.rich(para, txt, size=size, bold=(first_col_bold and ci == 0))
                if ci in num_cols and ri > 0:
                    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                elif ci in num_cols and ri == 0:
                    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        # set grid widths
        grid = tbl._tbl.tblGrid
        for ci, gc in enumerate(grid.findall(qn("w:gridCol"))):
            gc.set(qn("w:w"), str(int(w_in[ci] * 1440)))
        if source:
            self.note(source)
        else:
            sp = self.doc.add_paragraph()
            sp.paragraph_format.space_after = Pt(2)
        return tbl

    def callout(self, body_runs, attribution, fill=QUOTE_FILL):
        """Indented box with a thick navy left border."""
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        self._borders(tbl, {"left": ("single", 24, NAVY_HEX)})
        self._cell_margins(tbl, 90, 90, 160, 120)
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(6.2)
        grid = tbl._tbl.tblGrid
        for gc in grid.findall(qn("w:gridCol")):
            gc.set(qn("w:w"), str(int(6.2 * 1440)))
        self._shade(cell, fill)
        trPr = tbl.rows[0]._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
        p1 = cell.paragraphs[0]
        p1.paragraph_format.space_after = Pt(3)
        body_runs(p1)
        if attribution:
            p2 = cell.add_paragraph()
            p2.paragraph_format.space_after = Pt(0)
            self.rich(p2, attribution, size=7.5, color=NAVY)
        else:
            p1.paragraph_format.space_after = Pt(0)
        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(2)

    def quote(self, bank, needle, comment=None):
        q = get_quote(bank, needle)

        def body(p):
            r = p.add_run("“" + q["q"] + "”")
            r.italic = True
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(0x26, 0x26, 0x26)

        attr = f"— {q['name']} ({q['title']}), {q['event']}, {q['date']} · Quartr t={q['ts']}s [IR]"
        if comment:
            attr += "   " + comment
        self.callout(body, attr)

    def question_box(self, text, attribution):
        def body(p):
            self.rich(p, text, size=9, italic=True)

        self.callout(body, attribution, fill="F2F2F2")

    def keybox(self, title, lines):
        def body(p):
            r = p.add_run(title)
            r.bold = True
            r.font.color.rgb = NAVY
            r.font.size = Pt(9.5)
            for ln in lines:
                p.add_run("\n")
                self.rich(p, ln, size=8.5)

        self.callout(body, "", fill="F7F9FC")


# ----------------------------------------------------------------------------- content
def build(pages=None):
    b = Builder(pages)
    D = b.doc
    A = lambda f: os.path.join(AN, f)  # noqa: E731
    K = A("K_session_tables.md")

    # ======================================================================= COVER
    for _ in range(5):
        D.add_paragraph()
    t = D.add_paragraph()
    r = t.add_run("Mobility Global Inc.")
    r.bold, r.font.size, r.font.color.rgb = True, Pt(30), NAVY
    t = D.add_paragraph()
    r = t.add_run("NYSE: MBGL  ·  Automotive data & analytics")
    r.font.size, r.font.color.rgb = Pt(13), GREY
    t = D.add_paragraph()
    t.paragraph_format.space_before = Pt(18)
    r = t.add_run("Initiation research document (Part E)")
    r.bold, r.font.size, r.font.color.rgb = True, Pt(18), NAVY
    t = D.add_paragraph()
    r = t.add_run("Business, moat, unit economics, financial history, guidance credibility, incentives and risks")
    r.font.size, r.font.color.rgb = Pt(11), GREY
    t = D.add_paragraph()
    t.paragraph_format.space_before = Pt(24)
    r = t.add_run(f"Date: {DOC_DATE}")
    r.bold, r.font.size = True, Pt(11)
    t = D.add_paragraph()
    r = t.add_run("Prepared from primary filings via Quartr; see source limitations (Appendix A).")
    r.font.size, r.italic = Pt(10), True
    D.add_paragraph()
    b.keybox(
        "How to read this document",
        [
            "Every figure carries a tier tag: [D] disclosed in a filing or company deck · [C] computed by us from disclosed inputs (method stated) · "
            "[E] our estimate (assumption stated) · [IR] management verbal statement · [X] third party · [context] general knowledge, not from the filings.",
            "Orange bold **[TO COLLECT #n: …]** marks data that does not exist in the source set yet. All placeholders are listed with section and page "
            "in the Placeholder register at the back; that register is the field-work list.",
            "Quotes are verbatim from the transcript quote banks (Investor Day 2026-05-12, Q2-26 call 2026-08-07, Goldman Sachs Communacopia 2026-09-10).",
            "Eras are not comparable (IHS Markit Transportation, S&P Global Mobility, carve-out, standalone). See §8.4 before reading any long-run series.",
            "No rating or price target: market data (share price, market value) was not available in the source set.",
        ],
    )

    # ======================================================================= CONTENTS
    b.section = "Contents"
    D.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    D.add_heading("Contents", level=1)
    toc_titles = [
        "1 Executive summary", "2 Business overview & history", "3 Segments & revenue model", "4 Market & industry",
        "5 Moat & competitive position", "6 Value proposition by customer", "7 Unit economics", "8 Financial history",
        "9 Group decomposition & standalone earnings", "10 Guidance vs execution & targets timeline", "11 Pricing",
        "12 Demand drivers & cyclicality", "13 Management & incentives", "14 Disclosure changes & red flags",
        "15 Pre-mortem & risks", "16 Questions for management", "17 Honest counters",
        "Appendix A Source limitations & verification", "Appendix B Accounting notes", "Appendix C Glossary of tiers & source keys",
        "Placeholder register",
    ]
    pg = (pages or {}).get("headings", {})
    for ttl in toc_titles:
        para = D.add_paragraph()
        para.paragraph_format.space_after = Pt(1)
        para.paragraph_format.tab_stops.add_tab_stop(Inches(6.7), alignment=2, leader=1)  # right, dots
        r = para.add_run(ttl)
        r.font.size = Pt(10)
        if not ttl[0].isdigit():
            r.bold = True
        r2 = para.add_run("\t" + str(pg.get(ttl, "–")))
        r2.font.size = Pt(10)

    # ======================================================================= 1 EXECUTIVE SUMMARY
    b.h1("Executive summary", 1)
    b.h2("1.1 Thesis")
    b.p(
        "Mobility Global (MBGL) was spun from S&P Global on 2026-07-01 [D] and is a VIN-keyed automotive data utility with two segments. "
        "**CARFAX** (≈65% of revenue [IR]; FY25 segment Adj. EBITDA margin 46.9% [C]) sells vehicle-history subscriptions, Listings, Car Care and lender/insurer data (BIG). "
        "**B2B** (≈35% [IR]; FY25 margin 32.4% [C]) sells automotiveMastermind, Polk audiences and recall, Market Scan and planning forecasts. "
        "FY25 revenue was $1,750m [D], 81% subscription [D], ~60% from dealers and ~10% from OEMs [D], 17% international [C]. "
        "The model is B2B2C: the consumer creates the demand, the dealer pays [D] (10A p.380)."
    )
    b.p(
        "**Our reading.** The CARFAX franchise is a wide moat that is still widening on every audited or disclosed measure (sources, records, segment margin, growth vs industry). "
        "B2B's moat is moderate: it grew +3.1% / +5.9% in FY24 / FY25 [C] against named “low-cost alternative[s]” [IR]. The debate is therefore not moat durability. "
        "It is whether a business now growing ~7% (≈4.2pt of it price [C]), resetting to a ~39.1% Adj. EBITDA margin [IR] with 2.7x gross leverage [IR], "
        "and retreating on disclosure, should be priced as the 9–10% compounder its history suggests (D11)."
    )
    b.keybox(
        "The moat in one sentence",
        [
            "MBGL owns the only VIN-level history record that a dealer can hand to a consumer: built from ~177k give-get sources and 38bn+ records growing ~9% a year [D/C], "
            "backed by a brand consumers ask for by name and by 36 OEM certified-pre-owned (CPO) mandates [IR] — wide in CARFAX; only moderate in B2B, where low-cost substitutes exist (D1 §1, §5).",
        ],
    )
    b.h2("1.2 Key numbers")
    rev = lambda p: pv("IS.revenue", p)  # noqa: E731
    adj = {"FY2023": 598, "FY2024": 658, "FY2025": 711, "6M-2025": 357, "6M-2026": 386}
    fcf = {p: pv("CF.cfo", p) + pv("CF.capex", p) for p in ("FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026")}
    kn = [
        ["Revenue, $m [D]", fmt(rev("FY2023")), fmt(rev("FY2024")), fmt(rev("FY2025")), fmt(rev("6M-2025")), fmt(rev("6M-2026"))],
        ["Revenue growth [C]", "—", growth(rev("FY2024"), rev("FY2023")), growth(rev("FY2025"), rev("FY2024")), "—", growth(rev("6M-2026"), rev("6M-2025"))],
        ["Adj. EBITDA (company def.), $m [D]"] + [fmt(adj[p]) for p in ("FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026")],
        ["Adj. EBITDA margin [C]"] + [pct(adj[p], rev(p)) for p in ("FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026")],
        ["Operating profit (GAAP), $m [D]"] + [fmt(pv("IS.op", p)) for p in ("FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026")],
        ["Net income (carve-out), $m [D]"] + [fmt(pv("IS.ni", p)) for p in ("FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026")],
        ["Free cash flow (CFO − capex), $m [C]"] + [fmt(fcf[p]) for p in ("FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026")],
        ["FCF / Adj. EBITDA [C]"] + [pct(fcf[p], adj[p], 0) for p in ("FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026")],
    ]
    b.table(["", "FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026"], kn, widths=[2.6, 1, 1, 1, 1, 1], num_cols=[1, 2, 3, 4, 5],
            caption="Exhibit 1.1 — Carve-out financial summary ($m)",
            source="Source: canonical/primary.csv (Form 10/A, 10-Q Q2-26); Adj. EBITDA from analysis/K_session_tables.md (D3). FY23/FY24 Adj. EBITDA are printed totals (segments foot to 597/659).")
    kv = [
        ["FY26 guidance (2026-08-07)", "Revenue $1,870–1,885m (+6.9–7.7% reported) [D]; Adj. EBITDA $745–760m (~40%) [D]", "Q2 deck p.9"],
        ["Cash / long-term debt at 6/30/26", f"${fmt(pv('BS.cash','Q2-2026'))}m [D] / ${fmt(pv('BS.ltd','Q2-2026'))}m [D] ($2.0bn notes, 5.53% weighted coupon [C])", "10-Q p.6, 11"],
        ["Leverage", "Gross 2.7x, net 2.4x; net debt $1.8bn [IR]; target gross ~2.5x [IR]", "GS 2026-09-10; Q2 call"],
        ["Standalone normalized NI", "~$171m FY25 base (range 161–182) / ~$209m FY26 run-rate [C/E] vs carve-out $220m [D]", "D3 §4"],
        ["Dividend", "$0.06/qtr = $70.8m a year [C] (34–44% of normalized NI [C]; ~19% of standalone FCF ~$365m [C])", "D3 §5"],
        ["Shares outstanding", "294,821,320 at the 2026-06-15 record date [D]", "10-Q p.11"],
        ["Share price / market value / EV", "{{TC: MBGL share price, market capitalisation and enterprise value as of " + DOC_DATE + "}}", "market data"],
        ["Valuation multiples", "{{TC: EV/Adj. EBITDA, P/E on normalized NI, FCF yield — requires market data}}", "market data"],
    ]
    b.table(["Item", "Value", "Source"], kv, widths=[1.7, 4.0, 1.1], caption="Exhibit 1.2 — Capital structure, guidance and market data")

    b.h2("1.3 Five key findings")
    b.numbered([
        "**Growth is now mostly price, and new business is fading.** The 10-Q attributes ~$36m of the $64m 6M-26 revenue increase to price and ~$20m to new business [D] — "
        "≈4.2pt of 7.4% growth [C]. New business fell from ~$12m (Q1, implied) to ~$8m (Q2) [C]. The Form 10/A had called the same Q1 growth “new business” ($26m) [D] (D7 §5; D4 §3).",
        "**The CARFAX moat is wide and widening; B2B's is not.** Growth beat industry units in 10 of 11 years, by ~+10pt a year on average [C]; sources grew ~6.5% and records ~9.3% a year FY16–25 [C]; "
        "CARFAX Adj. EBITDA margin rose 45.5% → 46.9% → 48.0% (6M-26) [C]. B2B grew +3.1% / +5.9% with −18% FY25 Adj. EBITDA flow-through [C] (D1, D2).",
        "**The margin narrative keeps resetting.** S&P Global's 41–43% Mobility target was missed by 110–310bp while revenue was on plan [D/C]. The standalone cost drifted to the high end "
        "(~150bp ≈ $26m [C]), one-time costs to $75–110m [D], expansion pushed to 2028 [IR], and SBC rises from ~1% to 3–4% of revenue [IR] (D10, D3, D4 §7–9).",
        "**The standalone capital structure changes the earnings picture, not the cash picture.** Interest goes from $13m to ~$110m [C] (≈31% of normalized OP [C]). "
        "The “25% of normalized NI” dividend is 34–44% of reproducible normalized NI [C], yet only ~19% of FCF [C] (D3 §3–5).",
        "**Disclosure retreated as metrics weakened, and pay is loosely tied to per-share value.** NRR pulled, organic constant-currency growth no longer printed, business lines dropped, "
        "and the segment measure switched in the quarter B2B segment OP fell to $3m [D] (D4 §0). PSUs converted to time-vested awards; no TSR metric; committee discretion unlimited; insiders hold <1% [D] (D5).",
    ])
    b.quote("Q2", "Given our first half top-line performance")
    b.h2("1.4 Key risks (detail in §15)")
    b.table(*md_table(A("D11_premortem.md"), "| Risk | Impact | Likelihood |"), widths=[2.0, 0.6, 0.8, 3.4],
            caption="Exhibit 1.3 — Risk summary (impact / likelihood)", source="Source: analysis/D11_premortem.md §2. H/M/L are analyst judgements [E].")
    b.p("**Inference (D11):** cases 1, 2, 4 and 6 are one cluster — organic growth stays at ~6–7% and margins do not expand. The most likely way to lose is not a moat collapse; "
        "it is a slow re-rating of a 6–7% grower with ~39% margins and 2.7x leverage that is being priced as a 9–10% compounder. "
        "Whether that is priced in cannot be judged here: {{TC: consensus estimates and current valuation multiple to test what growth is priced in}}.")

    # ======================================================================= 2 BUSINESS OVERVIEW
    b.h1("Business overview & history", 2)
    b.h2("2.1 What MBGL is")
    b.p("MBGL describes itself as an automotive data, solutions and insights provider reporting two segments, CARFAX and B2B (10A p.262, 340) [D]. Scale at 12/31/25 [D]:")
    b.bullets([
        "more than 177,000 data sources and more than 38bn vehicle-history records; more than 13bn transaction records; ~832m unique VINs; more than 2,000 attributes per vehicle [D] (10A p.262, 268);",
        "more than 40,000 dealer customers; the top 40 global automakers (96% of global production) are customers [D];",
        "Polk heritage dates to 1870, with more than 30 years of ownership data [D] (10A p.268);",
        "more than 3,400 FTEs at 12/31/25 and ~3,522 at 3/31/26 [D] (10A p.268, 384); headquarters leased in Centreville, VA [D];",
        "FY25 revenue $1,750m (+8.5%) and net income $220m (+5.8%) [D]; Q1-26 revenue $455m (+8.1%) [D] (10A p.262).",
    ])
    b.h2("2.2 Eras of ownership and reporting")
    eras = [
        ["Polk / CARFAX private", "1870 → 2013", "Private", "—", "No financials in the source set", "{{TC: pre-2013 CARFAX/Polk history incl. 2008–09}}"],
        ["IHS Inc. → IHS Markit “Transportation”", "2013 → FY2021", "Segment of IHS / IHS Markit", "Nov", "Includes Maritime & Trade; Aerospace & Defense to Dec-2019; automotive ~80% → >90% of segment [D]", "Not comparable"],
        ["S&P Global Mobility", "2022-02-28 → 2026-06-30", "SPGI segment", "Dec", "FY22 is ~10 months; SPGI adjusted OP margin measure [D]", "Partly (D4 §12)"],
        ["Carve-out combined (Form 10/A, 10-Q)", "FY2023 → Q2-2026", "Combined statements incl. SPGI allocations", "Dec", "~$100m allocations [C]; no standalone debt or costs [D]", "Base for this report"],
        ["MBGL standalone", "from 2026-07-01", "Listed company", "Dec", "First standalone quarter is Q3-26 {{TC: Q3-26 10-Q / results (first standalone quarter, adjusted NI definition)}}", "—"],
    ]
    b.table(["Era", "Period", "Reporting entity", "FYE", "Scope notes", "Comparable to carve-out?"], eras, widths=[1.4, 1.0, 1.1, 0.4, 2.0, 1.1],
            caption="Exhibit 2.1 — Reporting eras", source="Source: PART_A_SUMMARY.md structural breaks; accounting_notes.csv (BREAK rows); SYNTHESIS.md caveats.")
    b.h2("2.3 Corporate and deal timeline")
    h, rows = md_table(A("QUALITATIVE.md"), "| Date | Event | Source |")
    b.table(h, rows, widths=[0.9, 4.6, 1.3], caption="Exhibit 2.2 — Corporate events timeline [D]",
            source="Source: analysis/QUALITATIVE.md §11 (Form 10/A, 10-Q, IHS 10-Ks). Deal values for the 2013 IHS–Polk transaction are not available in Quartr.")
    b.p("Acquisition values disclosed [D]: CARPROOF $459.2m net of cash (2015-12-24); automotiveMastermind 78% for ~$432–433m (2017-09-25; the remaining 22% treated as compensation); "
        "Market Scan $223m (2023-02-16). Catalyst for Aftersales was sold in Aug-2023 at a loss under $1m [D]. "
        "{{TC: 2013 IHS–R.L. Polk purchase price and CARFAX allocation}}; {{TC: outcome of the 2017 dealer antitrust re-filing against CARFAX}}.")
    b.quote("GS", "But when it came to competing for resources")
    b.h2("2.4 Separation mechanics")
    h, rows = md_table(A("QUALITATIVE.md"), "| Item | Fact | Source |")
    b.table(h, rows, widths=[1.3, 4.3, 1.2], caption="Exhibit 2.3 — Separation mechanics [D]", source="Source: analysis/QUALITATIVE.md §9.")
    b.p("Open items: {{TC: TSA fee amounts by service and exit timetable}}; {{TC: Employee Matters Agreement schedules and Form S-8 Ex.99.1 (LTIP full text)}}.")

    # ======================================================================= 3 SEGMENTS
    b.h1("Segments & revenue model", 3)
    b.h2("3.1 Segment revenue and profitability")
    seg = [
        ["CARFAX revenue, $m [D]", "928", "1,039", "1,142", "+12.0% / +9.9% [C]"],
        ["B2B revenue, $m [D]", "557", "574", "608", "+3.1% / +5.9% [C]"],
        ["CARFAX Adj. EBITDA, $m [D]", "422", "476", "536", "margin 45.5% / 45.8% / 46.9% [C]"],
        ["B2B Adj. EBITDA, $m [D]", "191", "203", "197", "margin 34.3% / 35.4% / 32.4% [C]"],
        ["Corporate Adj. EBITDA, $m [D]", "(16)", "(20)", "(22)", "1.1% / 1.2% / 1.3% of revenue [C]"],
        ["CARFAX segment OP (after amortization), $m [D]", "210", "259", "322", "OP margin 23% → 25% → 28% [D/C]"],
        ["B2B segment OP (after amortization), $m [D]", "61", "69", "62", "B2B carries ~$107m/yr amortization [D]"],
    ]
    b.table(["", "FY2023", "FY2024", "FY2025", "Growth / margin"], seg, widths=[2.4, 0.8, 0.8, 0.8, 2.0], num_cols=[1, 2, 3],
            caption="Exhibit 3.1 — Segment revenue and profit ($m)",
            source="Source: analysis/K_session_tables.md (D6, D3); D2 (d). Segment Adj. EBITDA margins [C] from printed $. B2B revenue = total − CARFAX.")
    b.p("1H-26 [D]: CARFAX revenue $610m (+8%) and B2B +6%; Q2-26 CARFAX +8%, B2B +4% [D]. CARFAX Adj. EBITDA margin 48.0% (6M-26) [C]; B2B 32.6% [C] (D3 §1, D10 §3).")
    b.h2("3.2 Brands and products")
    prods = [
        ["CARFAX", "Advantage (vehicle history reports)", "<40% of CARFAX revenue [IR]; ≈38% FY25 per deck [D-deck]; 28m+ dealer-presented reports a month [D]"],
        ["CARFAX", "Car Listings (2014), Showroom (premium listing, Q2-26)", "≈22% of CARFAX ≈ $251m [C]; US listings market >$3bn, CARFAX <10% [IR]"],
        ["CARFAX", "CARFAX For Life / Car Care / Service Loyalty", "53m+ Car Care consumers [D]; goal reframed from 150m US+CA to >100m US [IR]"],
        ["CARFAX", "BIG (Banking & Insurance Group)", "17 of the top 20 banks and insurers [D]; underwriting volumes +$17m FY24 / +$13m FY25 [D]"],
        ["CARFAX", "International (Canada via CARPROOF; Spain, Italy, Poland; Germany Jul-26)", "CARFAX International revenue $137m / $155m / $168m FY23–25 [D]"],
        ["B2B · Marketing & Sales", "automotiveMastermind (BPS, EEQ), Polk audiences, Recall, Market Scan, Data Studio, VIN Solutions", "≈74% of B2B ≈ $450m [C, deck %]; aM 3,200 dealers [IR]; Market Scan ~10,500 dealerships [D]"],
        ["B2B · Strategy & Planning", "Polk market reporting, Vehicle & Supply-Chain Forecasting, FAST, PIQ, Global Reporting", "≈26% of B2B ≈ $158m [C, deck %]; 100% of top-40 OEMs, 94% of top-100 suppliers [D]"],
    ]
    b.table(["Segment", "Brand / product", "Disclosed anchors"], prods, widths=[1.2, 2.5, 3.1], caption="Exhibit 3.2 — Product map",
            source="Source: analysis/QUALITATIVE.md §1; D2 (a)/(c)/(f); deck mix percentages are unaudited marketing figures [D-deck].")
    b.p("Revenue by brand or product is not disclosed in any filing: {{TC: revenue by product (Advantage, Listings, Car Care, BIG, aM, Polk, Market Scan, Planning) from the first 10-K or management}}; "
        "{{TC: B2B business-line revenue in dollars (Marketing & Sales vs Strategy & Planning) for FY23–25}}.")
    b.quote("ID", "That's the CARFAX Advantage line you see there")
    b.h2("3.3 Revenue model")
    b.bullets([
        "**Subscription vs transactional.** FY25 subscription $1,426m (81%) vs non-subscription $324m (19%) [D] (10A p.349). B2B subscription 76% → 80% → 82% FY23–25 [D].",
        "**CARFAX driver definition [D]:** “number of dealer locations enrolled … the average monthly price per location on each product, and the number of BIG customers and their average monthly price per customer” (10A p.340). "
        "Neither driver is quantified: {{TC: enrolled CARFAX dealer locations by year and average monthly price per location}}.",
        "**Pricing mechanics [D]:** monthly, annual or multi-year subscriptions; “BIG minimums with usage tiers”; Market Scan API “priced by dealer rooftops”; consumer pay-per-report and volume-based recall outreach are transactional (10A p.341).",
        "**Billing and backlog [D]:** generally invoiced annually in advance; contracts carry no obligation beyond the initial term; RPO $78m (12/31/25) → $102m (6/30/26), i.e. 5.5% of FY25 subscription revenue [C].",
        "**Concentration [D]:** no customer ≥10% of revenue (FY23–25) or of receivables.",
    ])
    h, rows = md_table(A("D6_value_prop.md"), "| Basis | Dealers | OEM |")
    b.table(h, rows, widths=[1.3, 0.9, 0.7, 1.0, 1.4, 1.5], caption="Exhibit 3.3 — Revenue by customer group, FY25 (two bases)",
            source="Source: analysis/D6_value_prop.md. The filing and deck bases differ and are non-additive; on the deck basis dealers ≈ $1,085m, OEM & supplier ≈ $350m, financial/consumer/other ≈ $315m [C].")
    h, rows = md_table(A("QUALITATIVE.md"), "| Period | U.S. $m |")
    b.table(h, rows, widths=[1, 1, 1, 0.8, 0.8, 1.2], num_cols=[1, 2, 3, 4], caption="Exhibit 3.4 — Revenue by geography [D]",
            source="Source: analysis/QUALITATIVE.md §3. B2B is 79% U.S. / 21% international (Q2-26, 6M-26) [D]. Main FX exposures CAD, EUR, GBP [D].")

    # ======================================================================= 4 MARKET & INDUSTRY
    b.h1("Market & industry", 4)
    b.p("**Status.** The public industry series planned in Part B (FRED, BEA, Census, BLS, Fed, Cox/Manheim, NADA, NHTSA, KBA, StatCan) could not be fetched: the network allowlist blocks them and Quartr was the only source. "
        "This section therefore uses only (i) market sizes asserted by the company or its unnamed consultant [D]/[X], (ii) the FRED new-vehicle series as reproduced on management's own slide 91 [D-deck], "
        "and (iii) [context] general knowledge, flagged as such. Every series needed to close the section is a placeholder.")
    b.h2("4.1 Market size claims")
    tam = [
        ["Global auto market", "≈$8.0tn: new LV $3.2tn, used $2.8tn, maintenance & repair $1.3tn, M/H commercial $0.7tn", "[D] management estimate (10A p.266)"],
        ["MBGL TAM (third party)", "$75–81bn: core $13–15bn, extended core $25–27bn, adjacencies $37–39bn; deck midpoint $78bn", "[X] unnamed consulting firm, cited in [D] 10A p.266; ID deck p.27"],
        ["B2B addressable market", "$6bn, ~10% share; “path to an $18 billion opportunity”", "[IR] LaFeir, Investor Day"],
        ["CARFAX TAM", "$26bn (CEO) vs $60bn (slide 71, core + extended vs total)", "[IR] / [D-deck] (D4 §13)"],
        ["US listings", ">$3bn; CARFAX “not even at 10%”", "[IR] Eager, GS 2026-09-10"],
        ["Used-vehicle market (US units, prices)", "{{TC: US used-vehicle retail units 2014–2026 (Cox Automotive estimates) and Manheim index}}", "Part B §B"],
        ["Dealer universe", "{{TC: US franchised and independent dealer rooftop counts 2014–2026 (NADA; Census CBP 44111/44112)}}", "Part B §C"],
    ]
    b.table(["Market", "Size / claim", "Tier and source"], tam, widths=[1.5, 3.4, 1.9], caption="Exhibit 4.1 — Market size claims",
            source="The consultant behind the $75–81bn TAM is never named in any document read (D4 §13). " )
    b.p("{{TC: identity and methodology of the third-party TAM consultant}}.")
    h, rows = md_table(K, "| Claim | Arithmetic | Verdict |")
    b.table(h, rows, widths=[2.0, 2.4, 2.4], caption="Exhibit 4.2 — Share-claim adjudication [C]",
            source="Source: analysis/K_session_tables.md (D1 §5). “Share” = share of a dollar TAM from unnamed consultants [X]; no unit-share series exists.")
    b.quote("ID", "When we look at the B2B side of the house")
    b.h2("4.2 Industry growth vs company growth")
    h, rows = md_table(K, "| Year | Rev $m | Reported growth |")
    b.table(h, rows, widths=[0.7, 0.9, 1.3, 0.9, 0.9, 0.8], num_cols=[1, 2, 3, 4, 5], caption="Exhibit 4.3 — Mobility automotive revenue vs US new-vehicle sales growth, 2014–2025 [D-deck]/[C]",
            source="Source: Investor Day slide 91 labels [D-deck], year mapping by analyst [C] (K_session_tables.md). The slide is footnoted “NOT prepared on a consistent basis”. "
                   "“Industry” = FRED new light-vehicle sales (inference), not used-vehicle transactions.")
    b.p("Compounded 2015–25, organic ≈ ×2.80 (≈9.8% a year) vs industry units ≈ ×0.99 (≈0% a year) [C]; reported CAGR 2014–25 ≈ 11.5% [C]. "
        "The relevant comparator for CARFAX is used-vehicle transactions, which is missing: {{TC: replace slide-91 comparator with used-vehicle transactions (Cox) and rerun the gap and regression}}.")
    b.h2("4.3 Competitive landscape (as named)")
    b.p("Competitors are named only in Business (10A p.382) [D]: automotive data and analytics (J.D. Power, Cox Automotive); data and information providers (Experian, GlobalData); "
        "BI and consulting firms and niche players (unnamed). Risk factors name no competitors [D]. Management says no single competitor spans the lifecycle [IR]. "
        "{{TC: competitor revenue/scale benchmarks — Experian AutoCheck, Cox (KBB, Autotrader, vAuto), J.D. Power, GlobalData/LMC}}; "
        "{{TC: CARFAX vs AutoCheck dealer penetration or report-volume share}}.")
    b.h2("4.4 Part B industry series — collection status")
    pb = [
        ["New-vehicle SAAR (TOTALSA, ALTSALES)", "FRED / BEA", "Reproduce slide 91; episode dating", "{{TC: FRED TOTALSA and ALTSALES 2010–2026}}"],
        ["Used-vehicle retail units", "Cox Automotive estimates", "Main CARFAX volume driver", "{{TC: Cox used retail units (annual, 2014–2026)}}"],
        ["Used-vehicle prices", "Manheim UVVI; BLS CPI used cars", "Dealer gross / price headroom", "{{TC: Manheim UVVI and CPI CUSR0000SETA02 monthly history}}"],
        ["Dealer profitability", "NADA Data", "Retention / price-increase capacity (SPGI Q1-23 admission)", "{{TC: NADA dealer gross profit per used unit 2018–2026}}"],
        ["Recall campaigns", "NHTSA flat file", "Recall revenue (−$15m FY24)", "{{TC: NHTSA recall campaigns and vehicles affected by year}}"],
        ["Vehicles in operation / average age", "S&P/MBGL releases; FHWA MV-1", "Car Care / service lifecycle", "{{TC: US VIO and average age 2014–2026 (reconcile 12.0 slide label vs 12.5–12.8 press releases)}}"],
        ["Auto lending", "Fed G.19; NY Fed; SLOOS", "Credit availability, BIG demand", "{{TC: auto loan rates, 84-month share, delinquency and SLOOS standards}}"],
        ["Auto insurance", "BLS CPI motor-vehicle insurance; LexisNexis", "Underwriting volumes (BIG)", "{{TC: CPI CUSR0000SETE and insurance shopping index}}"],
        ["International markets", "StatCan; KBA; ACI/UNRAE; ANFAC", "Canada softness; Germany/Italy/Spain TAM", "{{TC: Canada sales and Germany/Italy/Spain used-vehicle ownership transfers}}"],
        ["OEM marketing / incentive spend", "OEM 10-Ks; KBB / J.D. Power incentive data", "B2B Marketing & Sales demand", "{{TC: OEM advertising and incentive spend per unit 2018–2026}}"],
    ]
    b.table(["Series", "Source", "Use in analysis", "Status"], pb, widths=[1.7, 1.4, 1.7, 2.0], caption="Exhibit 4.4 — Industry series to collect",
            source="Source: market/PART_B_SERIES_PLAN.md (nothing fetched yet; series IDs marked “verify” there are from memory).")

    # ======================================================================= 5 MOAT
    b.h1("Moat & competitive position", 5)
    b.p("**MBGL owns the only VIN-level vehicle record that a dealer can hand to a consumer.** It is built over decades through give-get contributions from about 177,000 sources and backed by a brand "
        "consumers ask for by name; its cost to replicate keeps rising as the archive ages (D1 §1). The dealer pays for the consumer's trust; contributors keep sending data because they get value back; "
        "every year of history that a newcomer did not collect is lost to that newcomer for good. Polk registration and ownership data is a second, related moat on the B2B side, but it has a "
        "credible low-cost substitute (Experian) and lower growth.")
    b.h2("5.1 Architecture of the moat")
    arch = [
        ["Data contribution network", "177,000+ sources; 38bn+ VH records; ~6m records added a day [D]; give-get relationships “often on an exclusive basis” [D] (10A p.381)", "[D]"],
        ["Archive that cannot be rebuilt", "Records grew 17bn (FY16) → 38bn (FY25), ≈9.3% a year [C]; old data “just doesn't exist anymore anywhere else” [IR]", "[D]/[C]/[IR]"],
        ["DMV / public data custody", "DMV data a “high barrier to entry … due to the significant cost relative to potential monetization” [D]; DPPA custodianship >30 years [D]", "[D]"],
        ["Two-sided brand", "96% in-market awareness [D]; ~2m “Show me the CARFAX” requests a month [X survey]; $1.5bn media since 2000 [D-deck]; ad expense $134m / $152m / $176m FY23–25 [D]", "[D]/[X]"],
        ["OEM relationships", "36 OEM CPO programs require a CARFAX report [IR]; 36 OEMs contribute data [D]; 14 OEMs allow co-op dollars for Lifetime [IR]", "[D]/[IR]"],
        ["Polk registration data (B2B)", "30+ years ownership data; 13bn+ records; “gold standard” market reporting [D]; serves >90% of US volume (coverage, not share) [IR]", "[D]/[IR]"],
        ["Workflow embedding", "95 dealer-tool integrations; 17 of top-20 FIs [D-deck]; Market Scan in ~10,500 dealers [D]", "[D]"],
        ["Exclusivity tested in court", "2013 dealer antitrust suit (~469 dealers) — summary judgment for CARFAX 2016-09-30; new complaint Jan-2017 [D]", "[D]"],
    ]
    b.table(["Element", "Strongest evidence", "Tier"], arch, widths=[1.6, 4.4, 0.8], caption="Exhibit 5.1 — Moat elements and evidence",
            source="Source: analysis/D1_moat.md §2; QUALITATIVE.md §1, §4.")
    h, rows = md_table(K, "| FY | Sources | VH records |")
    b.table(h, rows, widths=[1, 1.4, 1.4, 1.6], caption="Exhibit 5.2 — Growth of the data network [D]",
            source="CAGR FY16–25 [C]: sources ≈ 6.5% a year; records ≈ 9.3% a year (K_session_tables.md, D1).")
    b.quote("ID", "Every one of those 177,000 sources")
    b.quote("Q2", "some of that data that's seven years old")
    b.quote("ID", "You want to put in brand Z in front of them")
    b.h2("5.2 Defensibility against each competitor class")
    h, rows = md_table(A("D1_moat.md"), "| Competitor class |", cols=[0, 1, 3])
    b.table(h, rows, widths=[1.5, 1.6, 3.7], size=7.5, caption="Exhibit 5.3 — Competitor classes",
            source="Source: analysis/D1_moat.md §3. [context] items are general knowledge, not from the filings.")
    b.h2("5.3 What the moat is not")
    b.bullets([
        "**Not exclusivity across the board.** Management called data rights “a mix” [IR].",
        "**Not software.** Management: “We're not a software company, right?” [IR]; MBGL has been “application agnostic for decades” [IR].",
        "**Not proven by retention data.** NRR was pulled from the Investor Day deck and described only as “meaningfully north of 100%” [IR]; no churn, ARPU or price per rooftop is disclosed [D]. "
        "{{TC: gross revenue retention and NRR for CARFAX dealers and B2B enterprise contracts}}.",
        "**Not a transaction owner.** In listings MBGL is “the newest of the four” with <10% of a >$3bn market after 12 years [IR]/[C]: the brand does not carry automatically into adjacent categories.",
    ])
    b.h2("5.4 Barriers to entry")
    h, rows = md_table(A("D6_value_prop.md"), "| Layer | What it takes |", cols=[0, 2, 3, 4])
    b.table(h, rows, widths=[1.3, 2.4, 2.0, 1.1], size=7.5, caption="Exhibit 5.4 — Entry-cost stack for a vehicle-history entrant [E]",
            source="Source: analysis/D6_value_prop.md §3.1. Order-of-magnitude judgements built from MBGL's disclosed spend and counts. Net: barriers to obtaining data have risen; barriers to processing it (AI) have fallen.")
    b.h2("5.5 Strategic boundaries: what MBGL does not do")
    h, rows = md_table(A("D8_category_structure.md"), "| Product / activity |", cols=[0, 2, 4])
    b.table(h, rows, widths=[2.0, 4.0, 0.8], size=7.5, caption="Exhibit 5.5 — Activities MBGL explicitly avoids", source="Source: analysis/D8_category_structure.md §2.")
    b.h2("5.6 Erosion watch-list")
    h, rows = md_table(A("D1_moat.md"), "| # | Watch-item |", cols=[0, 1, 3, 4])
    b.table(h, rows, widths=[0.3, 2.0, 2.4, 2.1], size=7.5, caption="Exhibit 5.6 — Moat erosion watch-items", source="Source: analysis/D1_moat.md §6.")
    b.p("Signals that cannot be monitored today: {{TC: CARFAX monthly unique visitors and VHR views time series (only point values 23m and 28m+ disclosed)}}; "
        "{{TC: data-acquisition cost and its growth (no cost-of-data line disclosed)}}; {{TC: share of service records sourced via DMS vendors that also compete with MBGL}}.")

    # ======================================================================= 6 VALUE PROP
    b.h1("Value proposition by customer", 6)
    b.p("One dataset is monetised four ways (D6 §1, inference). The consumer is the source of pricing power but mostly not the payer; the dealer pays because consumers trust the brand; "
        "the OEM pays indirectly through CPO mandates and co-op dollars from 14 OEMs [IR]; lenders pay because the same record de-risks collateral.")
    h, rows = md_table(A("D6_value_prop.md"), "| Segment (≈ share of revenue) |", cols=[0, 1, 2, 3])
    b.table(h, rows, widths=[1.3, 1.6, 2.0, 1.9], size=7.5, caption="Exhibit 6.1 — Value proposition by customer segment",
            source="Source: analysis/D6_value_prop.md §1. ROI, turn and lift figures are management or commissioned studies [IR]/[X], not audited.")
    b.quote("ID", "Most consumers, though, the typical scenario")
    b.quote("GS", "What we're able to do is by really creating the scores")
    b.h2("6.1 Where the advantage comes from")
    h, rows = md_table(A("D6_value_prop.md"), "| Source of advantage |")
    b.table(h, rows, widths=[1.5, 2.6, 0.8, 1.9], size=7.5, caption="Exhibit 6.2 — Sources of competitive advantage", source="Source: analysis/D6_value_prop.md §2.")
    b.p("Independent validation of the value claims is missing: {{TC: dealer survey or channel checks on CARFAX ROI, willingness to pay and AutoCheck substitution}}; "
        "{{TC: OEM / supplier interviews on Polk vs Experian/GlobalData switching}}.")

    # ======================================================================= 7 UNIT ECONOMICS
    b.h1("Unit economics", 7)
    b.p("**Ground rule.** MBGL discloses no price per rooftop, ARPU, churn, NRR, report volumes, brand-level P&L or country P&L [D] (segments_kpi_NOTES). Every per-unit number below is a printed KPI "
        "or a [C] ratio of two printed numbers whose denominators are known to be imperfect. The economic units are the CARFAX dealer-rooftop subscription and the B2B OEM/enterprise contract.")
    b.h2("7.1 CARFAX dealer economics")
    h, rows = md_table(A("D2_unit_economics.md"), "| Ratio | Value | Method | Caveat |")
    b.table(h, rows, widths=[1.8, 1.4, 1.4, 2.2], size=7.5, caption="Exhibit 7.1 — Computed per-dealer ratios, FY25 [C]",
            source="Source: analysis/D2_unit_economics.md (a). If rooftops are ~1.3–1.5x customers, per-rooftop revenue would be ~$11–13k, not $17k (D2 honest counters).")
    b.quote("Q2", "the average dealer has between one and a half and two products")
    b.bullets([
        "**Advertising is the main variable cost of the dealer model:** $134m / $152m / $176m FY23–25 = 9.0% / 9.4% / 10.1% of revenue [D/C]; the 10/A says customer-acquisition cost “is rising” [D] (10A p.343). "
        "{{TC: advertising expense split by segment}}.",
        "**Consumer reports** sit in CARFAX non-subscription ($180m / $196m / $215m FY23–25 [D]) with other transactional items. {{TC: consumer report price, volume and revenue}}; {{TC: consumer CAC, LTV and payback}}.",
        "**Lifetime bundle failure (2026):** 1,600 sign-ups ≈ 4% of dealer customers [C]; bundle needed “two yeses” and was reversed in June 2026 [IR]; fewer than half of franchise Advantage dealers take Service Loyalty [IR].",
    ])
    b.h2("7.2 Incremental margins (flow-through)")
    h, rows = md_table(K, "| Period | Segment | ΔRev |")
    b.table(h, rows, widths=[0.8, 0.9, 0.8, 1.2, 0.8, 1.1, 1.2], num_cols=[2, 3, 4, 5, 6], caption="Exhibit 7.2 — Flow-through by segment [C] (ΔProfit / ΔRevenue, $m)",
            source="Source: analysis/K_session_tables.md (D2). OP basis = Form 10/A segment OP; Adj. EBITDA basis = 10/A Segment Adj. EBITDA (FY/Q1) and 10-Q Adj. EBITDA (Q2/6M); the two tie for Q1-26.")
    b.p("Reading (D2 (d)): CARFAX incremental Adj. EBITDA margins of ~45–58% sit at or just above the segment average, so price-led growth is being reinvested in advertising and “strategic investments”. "
        "B2B FY25 is the anomaly: operating-related expenses +11% (232 → 258) and S&G +9% (162 → 177) on +6% revenue [D]. {{TC: B2B FY25 cost-line drivers (FAST/PIQ/Data Studio build, merit, data costs)}}.")
    b.h2("7.3 B2B contract economics")
    b.bullets([
        "OEM revenue ≈ 10% × $1,750m ≈ $175m [C] → ≤ ~$4.4m per top-40 OEM per year (ceiling) [C].",
        "OEM & supplier ≈ 20% × $1,750m ≈ $350m [C, deck %] → ~$2.6m per named enterprise customer (40 OEMs + 94 suppliers) [C].",
        "B2B dealer revenue ≲ $400m [C] → ≤ ~$36k per US B2B dealer (11K) per year [C]; cannot be split between aM and Market Scan.",
        "RPO / FY25 subscription revenue = 5.5% [C]: multi-year lock-in is not evidenced in the accounting.",
        "B2B underlying subscription growth ~6% in 1H-26 vs a goal of “high single digits” [IR]; printed 6M-26 B2B subscription +8% [D].",
        "{{TC: automotiveMastermind revenue, pricing and dealer count trend}}; {{TC: B2B contract escalator terms and renewal rates}}.",
    ])
    b.h2("7.4 Capital intensity and returns")
    h, rows = md_table(A("D2_unit_economics.md"), "| | FY23 | FY24 | FY25 | 6M-25 | 6M-26 |")
    b.table(h, rows, widths=[2.4, 0.9, 0.9, 0.9, 0.9, 0.9], num_cols=[1, 2, 3, 4, 5], caption="Exhibit 7.3 — Capex and cash conversion [D]/[C]",
            source="Source: analysis/D2_unit_economics.md (e); 10A p.361, 463; 10Q p.7.")
    b.bullets([
        "No capitalized-software asset is disclosed; acquired “Databases and software” cost is unchanged at $1,077m FY23–25 and gross PP&E is ~$100m [D]. Inference: development cost runs through the P&L, so FCF is not flattered by capitalization.",
        "One-time stand-up spend: ~$100m, ~50% capitalized [IR] → ~$50m of capitalized stand-up over 2026–27 vs $24m FY25 capex [C].",
        "ROIC (not printed): FY25 NOPAT ≈ $256m on ~$11.7bn carve-out invested capital ≈ 2.2%, or ≈ 3.9% before amortization [C] — an artefact of pushed-down purchase prices (goodwill $8,845m [D]); incremental returns are very high (capex ~1% of revenue).",
        "{{TC: maintenance vs growth capex split}}; {{TC: R&D expense included in S&G}}.",
    ])
    b.h2("7.5 International and new products")
    h, rows = md_table(A("D2_unit_economics.md"), "| Anchor | Value | Tier / source |")
    b.table(h, rows, widths=[2.0, 3.0, 1.8], size=7.5, caption="Exhibit 7.4 — International expansion anchors", source="Source: analysis/D2_unit_economics.md (f).")
    b.p("No Canada revenue, margin, payback or IRR, and no Germany set-up cost, operating loss or break-even is disclosed [D]: "
        "{{TC: Canada (CARPROOF) revenue and margin}}; {{TC: Europe set-up cost, annual operating loss and break-even year}}.")
    h, rows = md_table(A("D2_unit_economics.md"), "| Product | Printed anchors |")
    b.table(h, rows, widths=[1.6, 3.4, 1.8], size=7.5, caption="Exhibit 7.5 — New-product economics", source="Source: analysis/D2_unit_economics.md (g). AI is a cost-avoidance and reinvestment story, not a revenue line [Inference].")

    # ======================================================================= 8 FINANCIAL HISTORY
    b.h1("Financial history", 8)
    b.p("All statements are **carve-out (combined) financials** of S&P Global Mobility from the Form 10/A and the 10-Q, as originally reported, $m [D]. They include S&P Global corporate allocations "
        "and do not include standalone debt, costs or SBC levels (accounting_notes BASIS). Figures are read directly from canonical/primary.csv (390 cells; 0 collisions).")
    b.h2("8.1 Income statement")
    per = ["FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026"]
    def row(label, key, sign=1):
        return [label] + [fmt(None if pv(key, p) is None else sign * pv(key, p)) for p in per]
    is_rows = [
        row("Revenue [D]", "IS.revenue"),
        row("Operating-related expenses [D]", "IS.oprel"),
        row("Selling and general expenses [D]", "IS.sg"),
        row("Depreciation [D]", "IS.dep"),
        row("Amortization of acquired intangibles [D]", "IS.amort"),
        row("Total expenses [D]", "IS.totexp"),
        row("Operating profit [D]", "IS.op"),
        row("Other (income) expense, net [D]", "IS.other"),
        row("Interest expense, net [D]", "IS.int"),
        row("Income before taxes [D]", "IS.pbt"),
        row("Provision for income taxes [D]", "IS.tax"),
        row("Net income [D]", "IS.ni"),
        ["EPS, basic = diluted ($) [D]", "n/p", "n/p", "n/p", f"{pv('IS.eps_b','6M-2025'):.2f}", f"{pv('IS.eps_b','6M-2026'):.2f}"],
        ["Revenue growth [C]", "—", growth(rev("FY2024"), rev("FY2023")), growth(rev("FY2025"), rev("FY2024")), "—", growth(rev("6M-2026"), rev("6M-2025"))],
        ["Operating margin [C]"] + [pct(pv("IS.op", p), rev(p)) for p in per],
        ["Effective tax rate [C]"] + [pct(pv("IS.tax", p), pv("IS.pbt", p)) for p in per],
        ["Net margin [C]"] + [pct(pv("IS.ni", p), rev(p)) for p in per],
    ]
    b.table([""] + per, is_rows, widths=[2.6, 0.85, 0.85, 0.85, 0.85, 0.85], num_cols=[1, 2, 3, 4, 5], caption="Exhibit 8.1 — Combined statements of income / operations ($m)",
            source="Source: canonical/primary.csv (Form 10/A p.440; 10-Q p.4). Other (income) expense: negative = income (FY23 2, FY24 1). EPS for carve-out periods printed in the 10-Q on 294,821,320 shares; "
                   "the Form 10 said EPS could not be presented (n/p) — see §14.")
    qper = ["Q1-2025", "Q2-2025", "Q1-2026", "Q2-2026"]
    qadj = {"Q1-2025": 169, "Q2-2025": 188, "Q1-2026": 184, "Q2-2026": 202}
    q_rows = [
        ["Revenue [D]"] + [fmt(rev(p)) for p in qper],
        ["Revenue growth y/y [C]", "—", "—", growth(rev("Q1-2026"), rev("Q1-2025")), growth(rev("Q2-2026"), rev("Q2-2025"))],
        ["Operating profit [D]"] + [fmt(pv("IS.op", p)) for p in qper],
        ["Net income [D]"] + [fmt(pv("IS.ni", p)) for p in qper],
        ["Adj. EBITDA (10-Q basis) [D]"] + [fmt(qadj[p]) for p in qper],
        ["Adj. EBITDA margin [C]"] + [pct(qadj[p], rev(p)) for p in qper],
        ["Transaction costs in period [D]", "—", "2", "21", "36"],
    ]
    b.table([""] + qper, q_rows, widths=[2.6, 1, 1, 1, 1], num_cols=[1, 2, 3, 4], caption="Exhibit 8.2 — Quarterly profile ($m)",
            source="Source: primary.csv; K_session_tables.md (D3). Q1-25 Adj. EBITDA 169 on the 10-Q basis (170 in the Investor Day deck); Q2-25 recast 186 → 188 (D4 §5). Transaction costs: QUALITATIVE §9; Q2 call.")
    b.h2("8.2 Balance sheet")
    bper = ["FY2024", "FY2025", "Q1-2026", "Q2-2026"]
    def brow(label, key):
        return [label] + [fmt(pv(key, p)) for p in bper]
    bs_rows = [
        brow("Cash and cash equivalents [D]", "BS.cash"), brow("Accounts receivable, net [D]", "BS.ar"), brow("Prepaid and other current assets [D]", "BS.prepaid"),
        brow("Due from S&P Global (current) [D]", "BS.duefrom_c"), brow("Total current assets [D]", "BS.tca"), brow("PP&E, net [D]", "BS.ppe_net"),
        brow("Right-of-use assets [D]", "BS.rou"), brow("Goodwill [D]", "BS.gw"), brow("Other intangible assets, net [D]", "BS.intang"),
        brow("Other non-current assets [D]", "BS.onca"), brow("Total assets [D]", "BS.ta"),
        brow("Accounts payable [D]", "BS.ap"), brow("Accrued compensation [D]", "BS.accomp"), brow("Unearned revenue [D]", "BS.unearned"),
        brow("Other current liabilities [D]", "BS.ocl"), brow("Due to S&P Global (current) [D]", "BS.dueto_c"), brow("Total current liabilities [D]", "BS.tcl"),
        brow("Long-term debt [D]", "BS.ltd"), brow("Deferred tax liability, net [D]", "BS.dtl"), brow("Operating lease liabilities, non-current [D]", "BS.lease_nc"),
        brow("Due to S&P Global, non-current (Canada Carfax Loan) [D]", "BS.dueto_nc"), brow("Other non-current liabilities [D]", "BS.oncl"), brow("Total liabilities [D]", "BS.tl"),
        brow("Net parent investment [D]", "BS.npi"), brow("Accumulated other comprehensive income [D]", "BS.aoci"), brow("Total equity [D]", "BS.te"),
        brow("Total liabilities and equity [D]", "BS.tle"),
    ]
    b.table(["$m", "12/31/2024", "12/31/2025", "3/31/2026", "6/30/2026"], bs_rows, widths=[3.0, 0.95, 0.95, 0.95, 0.95], num_cols=[1, 2, 3, 4], size=7.5,
            caption="Exhibit 8.3 — Combined balance sheets ($m)",
            source="Source: canonical/primary.csv (Form 10/A p.424, 442; 10-Q p.6). No FY2023 balance sheet and no 3/31/25 or 6/30/25 balance sheets are disclosed [D]. 6/30/26 reflects the $2.0bn notes (LTD 1,981 net of $19m) "
                   "and the $2.0bn dividend to S&P Global; the Canada Carfax Loan was contributed and eliminated on 2026-06-25 [D].")
    b.h2("8.3 Cash flow")
    cper = ["FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026"]
    def crow(label, key):
        return [label] + [fmt(pv(key, p)) for p in cper]
    resid = []
    for p in cper:
        s = sum(pv(k, p) or 0 for k in ("CF.ni", "CF.dep", "CF.amort", "CF.deftax", "CF.sbc", "CF.prov"))
        resid.append(fmt(pv("CF.cfo", p) - s))
    cf_rows = [
        crow("Net income [D]", "CF.ni"), crow("Depreciation [D]", "CF.dep"), crow("Amortization of acquired intangibles [D]", "CF.amort"),
        crow("Deferred income taxes [D]", "CF.deftax"), crow("Stock-based compensation [D]", "CF.sbc"), crow("Provision for losses on receivables [D]", "CF.prov"),
        ["Working capital and other (residual) [C]"] + resid,
        crow("Cash provided by operating activities [D]", "CF.cfo"), crow("Capital expenditures [D]", "CF.capex"), crow("Acquisitions, net of cash [D]", "CF.acq"),
        crow("Cash used for investing activities [D]", "CF.cfi"), crow("Net transfers to parent [D]", "CF.parent"), crow("Proceeds from senior notes [D]", "CF.notes"),
        crow("Cash from (used for) financing activities [D]", "CF.cff"), crow("Net change in cash [D]", "CF.chg"),
        ["Free cash flow (CFO − capex) [C]"] + [fmt(fcf[p]) for p in cper],
        ["Cash interest paid (supplemental) [D]"] + [fmt(pv("CF.sup_int", p)) for p in cper],
        ["Cash taxes paid (supplemental) [D]"] + [fmt(pv("CF.sup_tax", p)) for p in cper],
    ]
    b.table([""] + cper, cf_rows, widths=[2.6, 0.85, 0.85, 0.85, 0.85, 0.85], num_cols=[1, 2, 3, 4, 5], size=7.5, caption="Exhibit 8.4 — Combined cash flow statements ($m)",
            source="Source: canonical/primary.csv (Form 10/A p.425, 443; 10-Q p.7). Annual working-capital lines are unreadable in the Quartr text (accounting_notes DATAQ), so working capital is shown as a residual [C].")
    b.p("{{TC: annual cash-flow working-capital lines FY2023–25 and Q1 components from the native Form 10/A PDF (p.443, p.425)}}; {{TC: standalone Q2-2026 cash-flow statement (only 6M printed)}}.")
    b.h2("8.4 Margins and cash conversion")
    cc_rows = [
        ["Adj. EBITDA margin [C]"] + [pct(adj[p], rev(p)) for p in cper],
        ["CARFAX Adj. EBITDA margin [C]", "45.5%", "45.8%", "46.9%", "—", "48.0%"],
        ["B2B Adj. EBITDA margin [C]", "34.3%", "35.4%", "32.4%", "—", "32.6%"],
        ["GAAP operating margin [C]"] + [pct(pv("IS.op", p), rev(p)) for p in cper],
        ["Operating profit + D&A margin [C]"] + [pct(pv("IS.op", p) + pv("IS.dep", p) + pv("IS.amort", p), rev(p)) for p in cper],
        ["SBC / revenue [C]"] + [pct(pv("CF.sbc", p), rev(p)) for p in cper],
        ["Capex / revenue [C]"] + [pct(-pv("CF.capex", p), rev(p)) for p in cper],
        ["FCF margin [C]"] + [pct(fcf[p], rev(p)) for p in cper],
        ["FCF / Adj. EBITDA [C]"] + [pct(fcf[p], adj[p], 0) for p in cper],
        ["FCF / net income [C]"] + [pct(fcf[p], pv("IS.ni", p), 0) for p in cper],
        ["Advertising / revenue [D/C]", "9.0%", "9.4%", "10.1%", "—", "—"],
    ]
    b.table([""] + cper, cc_rows, widths=[2.6, 0.85, 0.85, 0.85, 0.85, 0.85], num_cols=[1, 2, 3, 4, 5], caption="Exhibit 8.5 — Margin and cash-conversion ratios",
            source="Source: computed from primary.csv and K_session_tables.md; segment margins from D3 §1; advertising from 10A p.450 (D2). Company-printed FCF conversion 63% / 63% / 65% ties [D].")
    b.bullets([
        "**Margins are flat at ~40% on the generous measure** (40.3% → 40.8% → 40.6% [C]); GAAP operating margin rose 16.1% → 19.4% [C] because ~$296m a year of IHS-merger amortization [D] is fixed.",
        "**Cash conversion is high and capex-light:** FCF/Adj. EBITDA 63–65% FY23–25 [C]. 6M-26 fell to 46% [C] on working capital and $57m of mostly-cash transaction costs [D].",
        "**SBC is low pre-spin (~1.3% of revenue [C])** and is guided to 3–4% [IR]; it is excluded from Adj. EBITDA [D].",
        "**Tax:** FY25 ETR 32.5% [C]; FY26 GAAP guide 28–30.5% (call) / 28–31% (deck) [IR]; medium-term 25–27% [IR]; cash taxes will run ~$89m a year above the provision for 12 years (DTL unwind) [IR].",
    ])
    b.h2("8.5 Predecessor history (non-comparable eras)")
    h, rows = md_table(A("SYNTHESIS.md"), "| Series | Period |")
    b.table(h, rows, widths=[1.5, 1.0, 1.3, 1.4, 0.9, 0.7], size=7.5, caption="Exhibit 8.6 — Long-run series by era (do not splice)",
            source="Source: analysis/SYNTHESIS.md numbers story (predecessor.csv, D1, D2, D3, D4, D10).")
    b.p("**Non-comparability caveats** (SYNTHESIS):")
    b.bullets([
        "The IHS era is broader: it includes Maritime & Trade, and Jane's until 2019; automotive was ~80% → >90% of the segment [D]. It uses a Nov FYE and an IHS Adj. EBITDA definition that excluded aM performance compensation. "
        "The 47.6% FY21 margin therefore **cannot** be read as “margin fell to 40%”.",
        "FY22 is a ~10-month S&P Global period; Dec-2021–Feb-2022 is in neither era [D].",
        "Slide 91 is labelled “NOT prepared on a consistent basis” [D-deck].",
        "The carve-out includes ~$100m of S&P allocations [C] (D3 §2), and the MBGL Adj. EBITDA measure is +0.7–1.8pt above SPGI adjusted OP on the same business [C] (D4 §12).",
        "The Q2-26 Adj. EBITDA definition shrank from 10 to 6 exclusions [D]; FY25 $711m has not been republished on the new definition.",
        "2020 (COVID, IHS era): Transportation organic −2% but recurring organic +3% [D]; Adj. EBITDA −1% while margin rose 41.8% → 44.7% [D] (INFO20).",
    ])
    # --- IHS Markit Transportation detail (annual + quarterly), from extraction/predecessor.csv (same pick rule as the model's Segment History tab)
    import csv as _csv, re as _re
    _pred = list(_csv.DictReader(open(os.path.join(ROOT, "extraction", "predecessor.csv"))))
    def _pick(sec_re, line_re, per, docs=None):
        c = [x for x in _pred if x["fiscal_period"] == per and x["unit"] != "text" and _re.search(sec_re, x["section"]) and _re.search(line_re, x["line_item"])
             and (docs is None or x["source_doc"] in docs) and x["source_doc"].startswith("INFO")]
        if not c: return None
        own = [x for x in c if x["source_doc"].endswith(per)]
        return float(sorted(own or c, key=lambda x: x["source_doc"])[0]["value"])
    _yrs = [f"FY{y}" for y in range(2014, 2022)]
    _rev = {y: _pick(r"Revenue by Segment$", r"^Transportation$", y) for y in _yrs}
    _eb = {y: _pick(r"Segment Adjusted EBITDA$", r"^Transportation Adjusted EBITDA$", y) for y in _yrs}
    _org = {y: _pick(r"growth drivers", r"Transportation revenue - Organic", y) for y in _yrs}
    _rorg = {y: _pick(r"Transaction Type", r"recurring revenue organic growth", y) for y in _yrs}
    _fmt = lambda v, d=1: "—" if v is None else f"{v:,.{d}f}"
    _rows = [["Revenue, $m [D]"] + [_fmt(_rev[y]) for y in _yrs],
             ["Growth y/y [C]"] + ["—"] + [f"{(_rev[y]/_rev[_yrs[i]]-1)*100:.1f}%" for i, y in enumerate(_yrs[1:])],
             ["Organic growth [D]"] + [("—" if _org[y] is None else f"{_org[y]:.0f}%") for y in _yrs],
             ["Recurring organic growth [D]"] + [("—" if _rorg[y] is None else f"{_rorg[y]:.0f}%") for y in _yrs],
             ["Adj. EBITDA, $m [D]"] + [_fmt(_eb[y]) for y in _yrs],
             ["Adj. EBITDA margin [C]"] + [f"{_eb[y]/_rev[y]*100:.1f}%" for y in _yrs]]
    b.table(["IHS Markit Transportation"] + [y.replace("FY", "FY ") for y in _yrs], _rows, widths=[1.7] + [0.62] * 8, size=7.5, num_cols=list(range(1, 9)),
            caption="Exhibit 8.7 — IHS Markit Transportation segment, FY2014–FY2021 (Nov FYE)",
            source="Source: IHS Markit 10-K FY2016–FY2021 via extraction/predecessor.csv; FY2014/15 from later comparatives. Model tab: Segment History (block A).")
    _q = ["Q1-FY2020", "Q2-FY2020", "Q3-FY2020", "Q4-FY2020", "Q1-FY2021", "Q2-FY2021", "Q3-FY2021"]
    _qd = ["INFO_10Q_Q2-FY2021", "INFO_8K_Q2-FY2021", "INFO_Slides_Q2-FY2021", "INFO_10Q_Q3-FY2021", "INFO_Slides_Q3-FY2021"]
    def _qp(line_re, per, sec_re="."):
        c = [x for x in _pred if x["source_doc"] in _qd and x["fiscal_period"] == per and x["unit"] != "text" and _re.search(line_re, x["line_item"]) and _re.search(sec_re, x["section"])]
        if not c: return None
        own = [x for x in c if x["source_doc"].endswith(per)]
        return float(sorted(own or c, key=lambda x: _qd.index(x["source_doc"]))[0]["value"])
    _qr = {q: _qp(r"^(Revenue - Transportation|Total - Transportation)$", q) for q in _q}
    _qrec = {q: (_qp(r"^Transportation$", q, r"Supplemental Revenue Disclosure - Recurr") or _qp(r"^Recurring - Transportation$", q)) for q in _q}
    _qe = {q: _qp(r"^(Adjusted EBITDA - Transportation|Transportation Adjusted EBITDA)$", q) for q in _q}
    _qo = {q: _qp(r"^Total - Transportation organic growth", q) for q in _q}
    _qro = {q: _qp(r"^Recurring - Transportation organic growth", q) for q in _q}
    _rows = [["Revenue, $m [D]"] + [_fmt(_qr[q]) for q in _q],
             ["  of which recurring, $m [D]"] + [_fmt(_qrec[q]) for q in _q],
             ["Organic growth, total [D]"] + [("—" if _qo[q] is None else f"{_qo[q]:.0f}%") for q in _q],
             ["Organic growth, recurring [D]"] + [("—" if _qro[q] is None else f"{_qro[q]:.0f}%") for q in _q],
             ["Adj. EBITDA, $m [D]"] + [_fmt(_qe[q]) for q in _q],
             ["Adj. EBITDA margin [C]"] + [("—" if not (_qe[q] and _qr[q]) else f"{_qe[q]/_qr[q]*100:.1f}%") for q in _q]]
    b.table(["Quarter"] + [q.replace("-FY", " FY") for q in _q], _rows, widths=[1.7] + [0.71] * 7, size=7.5, num_cols=list(range(1, 8)),
            caption="Exhibit 8.8 — IHS Markit Transportation by quarter, Q1 FY2020 – Q3 FY2021",
            source="Source: IHS Markit 10-Q Q2/Q3 FY2021, 8-K Q2 FY2021, Q2/Q3 FY2021 decks (rounded where only deck figures exist). Quartr holds no earlier quarterly segment data; implied Q4 FY2021 = $351m revenue / $161m Adj. EBITDA [C].")
    b.bullets([
        "**Recurring revenue was ~76–79% of Transportation** in FY2020–21 [C]; Transportation had no recurring-variable revenue [D].",
        "**COVID trough was one quarter:** Q2 FY2020 total organic −16% (recurring −10%, non-recurring −31%) [D-deck], then +39% in Q2 FY2021 on the easy comparison [D].",
        "**Margin expanded through the downturn:** Q2 FY2020 41.8% → Q2 FY2021 49.6% [D]; FY2020 44.7% vs FY2019 41.8% [D].",
    ])
    b.p("Open reconciliation items: {{TC: bridge of IHS-era Transportation margin (47.6% FY21) to carve-out ~40% by scope, allocations and definition}}; "
        "{{TC: EDGAR XBRL cross-check of ~8 headline items for every period (sec.gov blocked)}}.")

    # ======================================================================= 9 GROUP DECOMPOSITION
    b.h1("Group decomposition & standalone earnings", 9)
    b.p("Two bases, never mixed (D3): **Basis 1** = Form 10/A segment operating profit (after acquired-intangible amortization and special items, before Corporate Unallocated). "
        "**Basis 2** = Adjusted EBITDA (10/A Segment Adj. EBITDA for FY/Q1; 10-Q Note 7 Adj. EBITDA for Q2/6M). The identities hold in every period on both bases [D/C].")
    h, rows = md_table(K, "| Period | CARFAX OP | B2B OP |")
    b.table(h, rows, widths=[0.8] + [0.75] * 8, num_cols=list(range(1, 9)), caption="Exhibit 9.1 — Segment + segment − corporate = group ($m) [D]",
            source="Source: analysis/K_session_tables.md (D3). *Printed total; the segment columns sum to 597 / 659.")
    h, rows = md_table(A("D3_group_decomposition.md"), "| | CARFAX | B2B | Corporate | Total |")
    b.table(["FY2025, $m"] + h[1:], rows, widths=[2.6, 1, 1, 1, 1], num_cols=[1, 2, 3, 4], caption="Exhibit 9.2 — Basis 1 → Basis 2 walk by segment, FY25",
            source="Source: analysis/D3_group_decomposition.md §1 (10A p.359, 350). 2026 special items sit mainly in B2B: 6M-26 transaction costs B2B $33m, Corporate $24m [D].")
    b.h2("9.1 The corporate wedge and the S&P Global allocations")
    alloc = [
        ["FY2023", "89", "89", "6.0%"], ["FY2024", "90", "90", "5.6%"], ["FY2025", "112", "~100", "5.7%"],
        ["Q1-2026", "28", "~21", "4.6%"], ["Q2-2026", "36", "~19", "4.1%"], ["6M-2026", "64", "~40", "4.3%"],
    ]
    b.table(["Period", "Allocations from S&P Global, total [D]", "Ex one-time [C]", "Ex one-time, % revenue [C]"], alloc, widths=[1.2, 2.2, 1.4, 2.0], num_cols=[1, 2, 3],
            caption="Exhibit 9.3 — Corporate allocations ($m)", source="Source: analysis/D3_group_decomposition.md §2 (10A p.434, 465; 10Q p.16).")
    b.p("Inference (D3): the allocations (~$100m) are 4–5x the recurring Corporate Unallocated wedge (~$22m), so most allocated cost already sits inside the CARFAX and B2B segment lines. "
        "Management has flagged a “slight reallocation of costs between CARFAX and B2B” [IR] — expect Corporate to widen and segment margins to rise mechanically from Q3/Q4-26.")
    h, rows = md_table(A("D3_group_decomposition.md"), "| Layer | Amount | Tier | Treatment |")
    b.table(h, rows, widths=[1.5, 2.8, 0.7, 1.8], size=7.5, caption="Exhibit 9.4 — Standalone vs allocated vs one-time costs", source="Source: analysis/D3_group_decomposition.md §2.")
    b.p("{{TC: dollar bridge from S&P allocations (~$100m) to the standalone corporate cost base}}; {{TC: overlap between $78m of transaction costs expensed and the ~$100m one-time guide}}.")
    b.h2("9.2 Interest burden on the $2.0bn notes")
    h, rows = md_table(A("D3_group_decomposition.md"), "| Tranche | Principal |")
    b.table(h, rows, widths=[1.7, 1.3, 1.3, 1.8], num_cols=[1, 3], caption="Exhibit 9.5 — Senior notes (issued 2026-05-29) [D]", source="Source: 10Q p.11; 10A p.337 (D3 §3).")
    h, rows = md_table(A("D3_group_decomposition.md"), "| Measure | Value | Tier |")
    b.table(h, rows, widths=[3.0, 2.6, 1.2], size=7.5, caption="Exhibit 9.6 — Interest, coverage and leverage", source="Source: analysis/D3_group_decomposition.md §3.")
    b.h2("9.3 Standalone normalized net income")
    b.p("Assumptions (D3 §4): FY25 non-recurring adjustments of $40m added back [D-deck]; standalone increment 150bp × FY25 revenue = $26.3m [IR→C]; SBC held at $22m in the base case; "
        "interest $110m run-rate; tax 29.5% (FY26 guide midpoint) [IR]; acquired-intangible amortization of ~$296m stays in GAAP NI.")
    h, rows = md_table(A("D3_group_decomposition.md"), "| Step | FY25 base |")
    b.table(h, rows, widths=[3.0, 1.2, 2.6], num_cols=[1], caption="Exhibit 9.7 — Carve-out NI → standalone normalized NI, FY25 base ($m)", source="Source: analysis/D3_group_decomposition.md §4.")
    h, rows = md_table(A("D3_group_decomposition.md"), "| | Tax 26% |")
    b.table(["NI (payout)"] + h[1:], rows, widths=[1.7, 1.7, 1.7, 1.7], num_cols=[1, 2, 3], caption="Exhibit 9.8 — Sensitivity of normalized NI ($m) and dividend payout [C]",
            source="Further cases [C/E]: SBC at 3% of revenue → NI ≈ 150 (payout 47%); FY26 run-rate NI ≈ 209 (34%); FY27 illustrative ≈ 234 (30%) [E]; NI ex after-tax amortization ≈ 390 (18%). "
                   "The Form 10/A pro forma FY25 NI is 139 [D].")
    b.h2("9.4 Testing the “25% of normalized net income” dividend")
    h, rows = md_table(A("D3_group_decomposition.md"), "| NI definition | NI | Payout |")
    b.table(h, rows, widths=[3.6, 1.6, 1.6], num_cols=[2], caption="Exhibit 9.9 — Payout ratio by NI definition ($0.06 × 4 × 294.8m = $70.8m) [C]",
            source="Source: analysis/D3_group_decomposition.md §5. A 25% payout requires normalized NI of ~$283m [C].")
    b.quote("GS", "We pegged at 25% of GAAP net income.")
    b.quote("GS", "You would peg the dividend, and we call it a normalized GAAP net income.")
    b.p("**Verdict (D3 §5).** On every GAAP-consistent construction available, $0.06 a quarter is 30–51% of standalone NI, not 25% [C]. The 25% fits only if “normalized” adds back roughly half of the "
        "after-tax amortization, or if management is pegging to a year near FY28 [Inference]. Affordability is not the issue: standalone FCF ≈ $365m [C], dividend ≈ 19% of it, and the ≥75% FCF return target "
        "implies ~$200m+ a year of buybacks from 2027 [C]. {{TC: management's definition and reconciliation of “normalized GAAP net income” (first adjusted NI print due with Q3-26)}}.")

    # ======================================================================= 10 GUIDANCE
    b.h1("Guidance vs execution & targets timeline", 10)
    b.p("Verdict scale (D10), judged against the *initial* guide: Beat = above the top of the initial range; Met = inside it; Missed-lowered = below the initial but inside a later, lowered range; Missed = below every range.")
    h, rows = md_table(A("D10_guidance_vs_execution.md"), "| Year / item | Initial |")
    b.table(h, rows, widths=[1.6, 1.2, 1.7, 1.2, 1.1], size=7.5, caption="Exhibit 10.1 — Guidance scorecard, S&P Global era and MBGL",
            source="Source: analysis/D10_guidance_vs_execution.md §1 (SPGI guidance slides; MBGL Q2 deck; transcripts). (pos.) = slide cell mapped by position.")
    b.bullets([
        "**SPGI era, revenue:** 2 beats and 1 missed-lowered over three years. **Margin:** 1 met and 2 missed-lowered, plus the 41–43% multi-year target missed by 110–310bp [C].",
        "**MBGL era:** one revenue cut within 3 months of reaffirming the guide.",
        "**Pattern [Inference]:** revenue guides were roughly reliable; margin guides and targets were repeatedly too high. Misses came from recall/transactional revenue (2024) and go-to-market (2026), not core subscription.",
    ])
    b.h2("10.1 FY2026: reaffirmed, then cut")
    b.quote("ID", "You saw we just reaffirmed guidance for 2026 at 7.5%-9%.")
    b.p("At reaffirmation, Q1-26 organic constant-currency growth was ≈ (455 − 4)/420 − 1 ≈ 7.4% [C] — below the 7.5% floor (rounded inputs, ±0.3pt), and the Q1 numbers had been public in the Form 10 five days earlier. "
        "Q2-26 grew 6.6% reported, ≈6.4% ex-FX [C]; 1H-26 7.45% reported, ≈6.9% ex-FX [C]. On a like-for-like OCC basis the cut is ~0.9–1.6pt [C], not the 0.6–1.3pt the headline implies (D4 §4).")
    b.quote("Q2", "Given our first half top-line performance")
    h, rows = md_table(A("D10_guidance_vs_execution.md"), "| | Low | High |")
    b.table(["$m"] + h[1:], rows, widths=[3.4, 1.7, 1.7], num_cols=[1, 2], caption="Exhibit 10.2 — What the new FY26 guide implies for 2H-26 [C]",
            source="Source: D10 §3. 2H-25 Adj. EBITDA (~354) mixes the 10/A FY definition and the 10-Q 1H recast (D4 §5). FY margin check: 39.8%–40.3% [C].")
    h, rows = md_table(A("D10_guidance_vs_execution.md"), "| | Q1-25 | Q2-25 | Q1-26 |")
    b.table([""] + h[1:], rows, widths=[1.5, 0.9, 1.0, 1.0, 1.1, 1.3], size=7.5, caption="Exhibit 10.3 — Quarterly actuals vs prior year [D]/[C]", source="Source: D10 §3. No quarterly guidance is given.")
    b.p("Stated causes of the Q2 shortfall [IR]: the CARFAX bundle go-to-market; softer non-US transactional revenue; ~$1m of recall revenue slipped to 2H; delays to Planning projects. "
        "{{TC: Q3-26 actuals vs the implied 2H run-rate (revenue +6.3–8.0%, Adj. EBITDA margin 37.9–38.9%)}}.")
    b.h2("10.2 Targets timeline (management voice)")
    h, rows = md_table(os.path.join(TR, "TARGETS_TIMELINE.md"), "| Metric | Investor Day")
    rows = [[re.sub(r"\s*\b(?:ID|Q2|GS) \d+(?:\.\d+)?s\b", "", c).strip() for c in r] for r in rows]
    b.table(h, rows, widths=[1.3, 1.5, 1.4, 1.4, 1.2], size=7, caption="Exhibit 10.4 — Targets and guidance by event [IR]",
            source="Source: transcripts/TARGETS_TIMELINE.md (every cell a management statement linked to a Quartr timestamp in that file; timestamps omitted here). "
                   "Note D4 §4: the “−60/−130bp” headline understates the like-for-like cut.")
    b.p("**Key revisions, in order:** (1) FY26 revenue growth cut 7.5–9% → 6.9–7.7%; (2) standalone costs to the high end (~150bp; 75bp in 2026, 150bp in 2027); (3) one-time stand-up cash to ~$100m, ~50% capitalised; "
        "(4) margin-expansion start set at 2028 from a ~39.1% pro-forma base; (5) dividend set at the top of the payout range; (6) CARFAX Germany pulled forward to July 2026; (7) Car Care goal reframed to >100m US [IR].")
    b.quote("GS", "So we're probably not going to get to the full 50 basis point expansion target until 2028.")
    b.p("Implication for modelling (D10 §4, inference): use ~6.5–7.5% OCC growth for FY26–27 rather than the 7.5–10% medium-term band, which starts in 2028 per the CFO; haircut margin targets; "
        "model the ~$100m one-time cost and the $78m of transaction costs to date as real cash. {{TC: FY27 guidance (promised broader scope) when issued}}.")

    # ======================================================================= 11 PRICING
    b.h1("Pricing", 11)
    b.bullets([
        "**Only one hard quantification of price exists.** The 10-Q: growth “driven primarily by price increases of approximately $16 million and $36 million” (Q2 / 6M-26) vs “continued new business growth of approximately $8 million and $20 million” [D] (10Q p.27). "
        "Price ≈ 55–56% of revenue growth [C]; ≈3.6pt (Q2) and ≈4.2pt (6M) of growth [C].",
        "**CARFAX is the price engine** (“primarily driven by price increases”); B2B growth is “primarily due to continued new business growth” [D] (10Q p.28–29).",
        "**Doctrine is value-based, not escalator-based** [IR]; pricing actions land early in the year [IR].",
        "**Vocabulary history:** S&P Global named price as the Dealer driver every quarter of 2023, then switched to “new business growth” from Q1-24; the Form 10/A used “improved contract terms”; the 10-Q is the first MBGL filing to say “price increases” (D7 §1; D4 §3).",
    ])
    h, rows = md_table(K, "| | Q1-26 (implied) |")
    b.table([""] + h[1:], rows, widths=[2.2, 1.6, 1.5, 1.5], num_cols=[1, 2, 3], caption="Exhibit 11.1 — Price vs new business, 1H-26 ($m)",
            source="Source: K_session_tables.md (D7; 10Q p.27). Q1 = 6M − Q2. The Form 10/A attributed $26m of Q1-26 to new business and $2m to underwriting (D4 §3).")
    b.quote("ID", "this is not as simple as saying we've got this very static product")
    b.quote("ID", "it's value plus volume in the 5%-7%")
    b.quote("Q2", "The preponderance of our pricing actions take effect early in the year")
    h, rows = md_table(A("D7_pricing.md"), "| Lever | What is said |")
    b.table(h, rows, widths=[1.4, 3.6, 1.8], size=7.5, caption="Exhibit 11.2 — Pricing levers and what is quantified", source="Source: analysis/D7_pricing.md §3.")
    h, rows = md_table(A("D7_pricing.md"), "| Date | Episode |")
    b.table(h, rows, widths=[1.2, 3.6, 2.0], size=7.5, caption="Exhibit 11.3 — Pricing episode timeline", source="Source: analysis/D7_pricing.md §4.")
    b.p("**Inference (D7 §5).** Price is the larger share and new business is fading; Q2 price (~$16m) was below implied Q1 (~$20m), consistent with early-year pricing, so 2H growth leans on new business recovering. "
        "The “5–7% core, majority value” algorithm matches ~4pt price + ~2pt new business [C], but the volume leg is visible only in dollars.")
    b.p("Data that does not exist in any filing, deck or transcript read: {{TC: price per dealer location and share of dealers taking a price increase at last renewal}}; {{TC: dealer rooftop counts by product}}; "
        "{{TC: B2B price escalator terms}}; {{TC: Lifetime bundle pricing and uplift}}; {{TC: AI / agent monetisation pricing model and revenue}}.")

    # ======================================================================= 12 DEMAND DRIVERS
    b.h1("Demand drivers & cyclicality", 12)
    b.bullets([
        "**Management never quantifies a macro sensitivity** (10/A, 10-Q, three MBGL events, 16 SPGI calls 2022–25). It says the company is “relatively acyclical”, has a “natural hedge” from new to used, and that transactional revenue is “non-cyclical” [IR]/[D].",
        "**Growth has decoupled from the industry except in a real shock.** Slide-91 organic growth was 9–18% in every year 2015–25 except 2020 (−2%) while US vehicle sales growth ranged −15% to +13% [D-deck]. "
        "Correlation 0.54 full sample; −0.39 excluding 2020–21 [C].",
        "**The real exposures are second-order and sit in the minority lines:** B2B transactional and Planning (OEM discretionary spend, tariffs, recall timing), international transactional (Canada 2026), and slow dealer consolidation. "
        "The 81% subscription base is driven by price and product adoption, not volumes [D]/[IR].",
        "**Inference (D9):** the right driver model is price + attach on a slowly drifting rooftop base, plus a ~19% transactional “beta” sleeve; a regression of revenue on SAAR or used units is the wrong shape.",
    ])
    b.quote("ID", "we are not just counter-cyclical, we're relatively acyclical")
    h, rows = md_table(A("D9_demand_drivers.md"), "| Exposure | Size |")
    b.table(h, rows, widths=[2.4, 2.0, 2.4], caption="Exhibit 12.1 — Exposure map", source="Source: analysis/D9_demand_drivers.md §1. “70% used” (SPGI) and “60% dealer + 10% OEM” (10/A) are different, non-additive bases.")
    h, rows = md_table(K, "| FY | MBGL organic (slide 91) |")
    b.table(["FY", "MBGL organic, % [D-deck]", "INFO Transportation organic, % [D]", "US vehicle sales growth, % [D-deck]"], rows, widths=[0.8, 1.8, 2.2, 2.0], num_cols=[1, 2, 3],
            caption="Exhibit 12.2 — Organic growth vs US vehicle sales, 2015–2025",
            source="Source: K_session_tables.md (D9). [C] mean organic 9.9% (sd 4.8) vs industry 0.2% (sd 7.2); OLS beta 0.36 full sample, −0.11 ex-2020/21; lag-1 correlation −0.32.")
    h, rows = md_table(A("D1_moat.md"), "| Episode | Evidence |")
    b.table(h, rows, widths=[1.1, 2.9, 0.8, 2.0], size=7.5, caption="Exhibit 12.3 — Downturn evidence", source="Source: analysis/D1_moat.md §4.2.")
    drv = [
        ["Used-vehicle retail transactions", "Supports demand; volume link denied (“not directly associated with number of transactions”) [IR]; CARFAX driver definition has no transaction term [D]", "None", "{{TC: used retail units series for elasticity test}}"],
        ["New-vehicle SAAR", "Hits aM / Marketing & Sales and Planning [D]", "None", "{{TC: SAAR monthly series}}"],
        ["Dealer count / consolidation", "Consolidation and OEM direct sales can reduce revenue [D] (10A p.299)", "None", "{{TC: rooftop counts and buy-sell deal counts (NADA, Haig)}}"],
        ["OEM marketing / recall", "Recall −$15m FY24, −$3m FY25; discretionary budgets −$2m FY25 [D]; recall guide cut −50bp implies ≥50% decremental [C]", "Recall only", "{{TC: NHTSA recall volumes}}"],
        ["VIO / average age", "TAM and whitespace; Car Care [IR]", "None", "{{TC: VIO and average age}}"],
        ["Auto lending", "Credit availability drives vehicle sales [D]; >20% of loans at 84 months [IR]", "None", "{{TC: G.19 rates and delinquency}}"],
        ["Insurance underwriting", "+$17m FY24, +$13m FY25, +$2m Q1-26 [D] — fading tailwind", "$ only", "{{TC: insurance shopping / CPI motor insurance}}"],
        ["Tariffs / international", "SPGI Manufacturing −3% Q3-25 [IR]; Canada and Planning soft in Q2-26 [IR]", "None", "{{TC: Canada and Germany market series}}"],
    ]
    b.table(["Driver", "Stated relationship / evidence", "Quantified sensitivity", "Series needed"], drv, widths=[1.4, 2.9, 0.9, 1.6], size=7.5,
            caption="Exhibit 12.4 — Driver-by-driver summary", source="Source: analysis/D9_demand_drivers.md §2.")
    b.quote("ID", "We can create demand in a lot of places.")
    b.quote("Q2", "Secondly, softer automotive activity outside the U.S.")
    h, rows = md_table(A("D9_demand_drivers.md"), "| Qtr | Total | Dealer |", cols=[0, 1, 2, 3, 4])
    b.table(h, rows, widths=[1.0, 1.4, 1.4, 1.5, 1.5], num_cols=[1, 2, 3, 4], caption="Exhibit 12.5 — S&P Global Mobility growth by business line, as stated on SPGI calls [IR]",
            source="Source: analysis/D9_demand_drivers.md §4. n/a = not stated in the retrieved passage.")
    b.p("{{TC: SPGI quarterly supplements to fill n/a cells in Exhibit 12.5 (Dealer / Manufacturing / Financials growth)}}. "
        "Stress template (D9 §3, inference): hold subscription at low-single-digit growth with price concessions, cut transactional 20–40%, recover within 12 months. The 2008–09 test is impossible with current data: {{TC: 2008–09 CARFAX/Polk revenue and pricing behaviour}}.")

    # ======================================================================= 13 MANAGEMENT & INCENTIVES
    b.h1("Management & incentives", 13)
    b.p("There is no DEF 14A yet; the first proxy is expected in 2027 [D]. Evidence comes from the Form 10/A CD&A, the 10-Q exhibits and the transcripts (D5).")
    h, rows = md_table(A("D5_incentives.md"), "| Name | MBGL role |", cols=[0, 1, 2, 3])
    b.table(h, rows, widths=[1.4, 1.3, 2.8, 1.3], size=7.5, caption="Exhibit 13.1 — Executive officers", source="Source: analysis/D5_incentives.md §1 (10/A p.386, 391).")
    h, rows = md_table(A("D5_incentives.md"), "| Director | Role |")
    b.table(h, rows, widths=[1.4, 1.2, 2.8, 1.4], size=7.5, caption="Exhibit 13.2 — Board after the spin",
            source="Source: D5 §1 (10/A pp.387–390). 8 members, annually elected, independent chair; compensation and nominating combined in one committee. Director pay: $80k cash + $220k annual RSU; one-time $400k separation RSU (3-year cliff) [D].")
    h, rows = md_table(A("D5_incentives.md"), "| NEO | Year | Salary |")
    b.table(h, rows, widths=[0.9, 0.5, 1.0, 1.3, 1.1, 0.9, 1.1], num_cols=[2, 3, 4, 5, 6], size=7.5, caption="Exhibit 13.3 — FY2025 Summary Compensation Table (paid by S&P Global) [D]",
            source="Source: D5 §2.1 (10/A p.398). ¹ Includes a $53,845 CARFAX PTO cash-out. Not in the SCT: LaFeir $700k retention bonus; Matharu $216k retention [D].")
    h, rows = md_table(A("D5_incentives.md"), "| NEO | Plan | Range |", cols=[0, 1, 3, 4, 5, 6])
    b.table(h, rows, widths=[0.8, 1.1, 2.6, 0.9, 0.7, 0.7], size=7.5, caption="Exhibit 13.4 — FY2025 short-term incentive outcomes",
            source="Source: D5 §2.2. Eager earned 120% with both revenue metrics below target (SPGI 7.1% vs 7.4%; Mobility 8.0% vs 8.7%) [D]. 2023–25 PSUs paid ~182–184% of target [C].")
    h, rows = md_table(A("D5_incentives.md"), "| Exec | Base | Target STI |")
    b.table(h, rows, widths=[0.8, 0.8, 0.8, 0.9, 1.1, 2.4], size=7.5, caption="Exhibit 13.5 — 2026 pay targets set by S&P Global before the spin",
            source="Source: D5 §2.4. The CFO's target pay exceeds the CEO's ($5.05m vs $4.50m) [C]; the CFO letter commits SPGI to explore “founder shares” with no set value or terms [D].")
    b.h2("13.1 Post-spin plans")
    b.bullets([
        "**2026 LTIP:** reserve of 14% of post-distribution shares (~41.3m [C]); liberal share recycling; converted awards do not count; no performance metrics specified; the committee may amend outstanding awards; CIC treatment discretionary [D].",
        "**Conversion of SPGI awards:** RSUs convert like-for-like; in-flight PSUs convert on actual performance to the distribution and **2026 PSUs convert at target into time-based RSUs** [D] — effectively no performance-conditioned equity for ~FY26–28 [E].",
        "**Annual Incentive Plan (Ex.10.17):** salary × target × Company Performance Factor × Individual Performance Factor; metrics not disclosed; committee may adjust goals mid-year [D].",
        "**Executive Severance Plan (Ex.10.18):** CEO 2× base (non-CIC) and 2× (base + target bonus) on CIC, double trigger, no gross-up; Good Reason includes any cut in target bonus [D].",
        "**Ownership:** all directors and officers <1% [D]; no ownership guidelines disclosed; BlackRock 8.21% and Vanguard 7.59% [D]. SBC was ~1.3% of revenue in FY25 [C], guided to 3–4% [IR] (≈$56–75m on FY26 revenue [C]).",
    ])
    h, rows = md_table(A("D5_incentives.md"), "| # | Risk | Evidence | Tag |")
    b.table(h, rows, widths=[0.3, 3.4, 2.0, 1.1], size=7.5, caption="Exhibit 13.6 — Incentive misalignment risks", source="Source: analysis/D5_incentives.md §5.")
    b.p("Counter-view (D5): unit EBITA metrics are defensible for a 40%+ margin data business; converting PSUs on actual performance is the shareholder-friendly spin variant; severance terms are mid-market. "
        "To resolve: {{TC: first DEF 14A (~Apr-2027): FY26 STI metrics and weights, 2027 PSU design (TSR / FCF per share), ownership guidelines}}; "
        "{{TC: beneficial-ownership share counts for directors and officers (flattened in Quartr text)}}; {{TC: any Item 5.02 8-K founder or spin grants}}.")

    # ======================================================================= 14 DISCLOSURE CHANGES
    b.h1("Disclosure changes & red flags", 14)
    b.p("Scoring (D4): for each change, “Unflattering?” asks whether it coincided with the affected metric turning worse — Yes, No (neutral or hurts the company's optics) or Mixed.")
    h, rows = md_table(A("D4_disclosure_changes.md"), "| # | Change | Vintage |")
    b.table(h, rows, widths=[0.3, 3.4, 1.2, 1.9], size=7.5, caption="Exhibit 14.1 — Red flags that matter, ranked", source="Source: analysis/D4_disclosure_changes.md §0.")
    h, rows = md_table(A("D4_disclosure_changes.md"), "| Document (vintage) | Exact short wording |")
    b.table(h, rows, widths=[1.6, 4.0, 1.2], size=7.5, caption="Exhibit 14.2 — Adjusted EBITDA definition: 10 exclusions → 6", source="Source: D4 §1. The Q2 deck still prints the 10-item text beside a 6-line reconciliation.")
    h, rows = md_table(A("D4_disclosure_changes.md"), "| Segment OP, $m |")
    b.table(h, rows, widths=[1.5, 0.7, 0.8, 0.7, 0.8, 0.7, 0.8, 0.8], size=7.5, caption="Exhibit 14.3 — What the old segment measure would have shown [D]/[C]",
            source="Source: D4 §2. Stand-up transaction costs were booked in B2B ($13m Q1-26, $20m Q2-26) [D].")
    h, rows = md_table(K, "| Item | FY23 SPGI |")
    b.table(h, rows, widths=[0.9, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 2.3], size=7, caption="Exhibit 14.4 — S&P Global Mobility segment vs Form 10/A carve-out, FY23–25 ($m) [D]/[C]",
            source="Source: K_session_tables.md (D4 §12). MBGL Adj. EBITDA margin is +1.5 / +1.8 / +0.7pt above SPGI adjusted OP margin on the same business [C].")
    h, rows = md_table(A("D4_disclosure_changes.md"), "| Disclosure | Last predecessor print |")
    b.table(h, rows, widths=[1.5, 2.4, 1.8, 1.1], size=7.5, caption="Exhibit 14.5 — Disclosures printed by predecessors that MBGL does not print", source="Source: D4 §11.")
    h, rows = md_table(A("D4_disclosure_changes.md"), "| Item | Vintages | Unflattering? |")
    b.table(h, rows, widths=[4.2, 1.2, 1.4], size=7.5, caption="Exhibit 14.6 — Smaller items", source="Source: D4 §13.")
    b.h2("14.1 Other red flags (SYNTHESIS)")
    b.bullets([
        "The FY26 guide was “reaffirmed” on May-12 while Q1 constant-currency growth (~7.4% [C]) was already below its 7.5% floor; it was cut 3 months later (D10 §3).",
        "Units changed when the dollar figure would have breached the range: the standalone cost moved from “$20–25m” to “150bp” (≈$26m [C]) (D4 §8).",
        "One-time costs: $75–100m → ~$100m (call) → $75–110m (10-Q) on the same day, with ~50% newly capitalised [D]/[IR] (D4 §7).",
        "Ad expense grew faster than revenue (+31% vs +18% FY23–25 [C]) and the 10/A says customer-acquisition cost is rising [D] (D1 §6).",
        "Carve-out EPS printed in the 10-Q although the Form 10 said it could not be presented — methodology inconsistency, not flattering (EPS −18% [C]) (D4 §6).",
    ])
    b.p("**Counter-view (D4 honest counters).** Spin-offs routinely move to Adj. EBITDA segment measures and drop parent-format organic growth; several changes cut against the company (the Q2-25 recast 186 → 188 lowers growth; "
        "the 10-Q volunteered the price split); management stated the guide cut in the first ~4 minutes of the Q2 call. {{TC: management confirmation of the “new business” vs “price” definitions (D4 §3)}}; "
        "{{TC: FY25 Adj. EBITDA restated on the 6-item definition}}.")

    # ======================================================================= 15 PRE-MORTEM
    b.h1("Pre-mortem & risks", 15)
    b.p("Ground rule (D11): every bear case extrapolates something **already observed** in the record. Magnitudes are gaps against a “plan” of the medium-term 7.5–10% organic growth (midpoint 8.75%) from the FY26 guide midpoint "
        "(revenue $1,877.5m, Adj. EBITDA $752.5m [D]): FY28 plan revenue ≈ $2,220m and Adj. EBITDA ≈ $870m [E]. Magnitudes are not additive (cases 1, 2 and 4 overlap).")
    h, rows = md_table(A("D11_premortem.md"), "| # | Bear case |", cols=[0, 1, 5, 6])
    b.table(["#", "Bear case", "Leading indicator to watch", "Magnitude [E]"], rows, widths=[0.3, 1.8, 2.3, 2.4], size=7.5, caption="Exhibit 15.1 — How can we lose?",
            source="Source: analysis/D11_premortem.md §1 (observed-evidence and mechanism columns omitted here; see the source file).")
    h, rows = md_table(A("D11_premortem.md"), "| Risk | Impact | Likelihood |")
    b.table(h, rows, widths=[2.0, 0.6, 0.8, 3.4], size=7.5, caption="Exhibit 15.2 — Risk summary", source="Source: D11 §2.")
    b.quote("ID", "This is the year we're grinding it")
    b.p("Inputs the pre-mortem cannot size today: {{TC: data and processing cost base (assumed ~$200–300m in D11 case 8, not disclosed)}}; {{TC: Europe start-up losses (assumed ~$10–20m a year in D11 case 11)}}; "
        "{{TC: share of CARFAX traffic arriving via search and AI answer engines}}.")

    # ======================================================================= 16 QUESTIONS
    b.h1("Questions for management", 16)
    b.p("Selection logic (D12): the three primary questions target the three load-bearing assumptions of a long thesis — (1) core growth is durable though now mostly price; (2) margins expand from a reset base; "
        "(3) the consumer-brand leg of the moat survives AI and search. Each is built so that a numerical answer confirms or refutes a D11 bear case.")
    d12 = read(A("D12_management_QA.md"))
    qs = re.findall(r'\*\*Question \(verbatim as asked\):\*\*\n> "(.+?)"\n', d12, flags=re.S)
    if len(qs) != 3:
        raise SystemExit("expected 3 primary questions in D12")
    prim = [
        ("Q1 · Price, volume and retention (bear case #1)", [
            "Price ≈ 4.2pt of 7.4% 6M-26 growth; new business ≈ 2.3pt [D/C]; the 10/A said $26m of Q1-26 was new business, the 10-Q implies ~$12m [C].",
            "Good answer: location count up low single digits, gross retention mid-90s, price on a defined share of the base, and a commitment to print a KPI. Evasive: “We're not a software company”; NRR “meaningfully above 100%” with no number.",
        ]),
        ("Q2 · The margin bridge and its credibility (bear cases #6, #10)", [
            "SPGI target missed by 110–310bp [C]; MBGL measure +0.7–1.8pt above SPGI's [C]; definition now has an “and other” catch-all [D]; standalone ≈ $26m [C]; SBC +$34–53m a year [C].",
            "Good answer: a dollar bridge (allocations replaced, standalone cost, reallocations, stand-up capex), a named list for “other”, and an incentive metric that charges SBC. Evasive: “40% range for three years”.",
        ]),
        ("Q3 · Consumer traffic, ad intensity and AI (bear case #3)", [
            "Ad expense $134m → $176m (9.0% → 10.1% of revenue) [D/C]; CAC rising [D]; search and AI named as traffic threats [D]; IP protection against AI uncertain [D].",
            "Good answer: traffic-mix numbers with stable cost per visitor, and concrete licensing terms for AI agents. Evasive: “Our data is behind a firewall”; AI only as internal productivity.",
        ]),
    ]
    for (title, why), q in zip(prim, qs):
        b.h3(title)
        b.question_box("“" + " ".join(q.split()) + "”", "Proposed analyst question (analysis/D12_management_QA.md) — not a management statement")
        b.bullets(why)
    b.h2("16.1 Secondary questions")
    h, rows = md_table(A("D12_management_QA.md"), "| # | Question |")
    b.table(h, rows, widths=[0.3, 2.6, 2.0, 1.9], size=7.5, caption="Exhibit 16.1 — Secondary questions", source="Source: analysis/D12_management_QA.md.")
    b.p("Answers to all of the above are themselves field-work items: {{TC: management answers to primary questions Q1–Q3 (meeting notes)}}; {{TC: management answers to secondary questions 4–10}}.")

    # ======================================================================= 17 HONEST COUNTERS
    b.h1("Honest counters", 17)
    b.p("The best evidence against this document's own conclusions (SYNTHESIS; D11 §3):")
    b.numbered([
        "**The moat evidence is strong and largely audited** (revenue, margins, source and record counts). Subscription revenue held even in 2020 (recurring organic +3% [D]); downturns produced price relief, not churn (D9 §3).",
        "**Revenue guidance has mostly been met.** Two of three SPGI-era years beat the initial revenue guide; the FY26 cut is ~1pt like-for-like [C] (D10).",
        "**Several flags cut against the company's own optics:** the Q2-25 recast lowers growth; the 10-Q volunteered the price split; carve-out EPS shows a −18% decline (D4).",
        "**The B2B dip may be a one-year investment cycle.** 6M-26 B2B Adj. EBITDA flow-through recovered to ~50% and Q2 margin rose 32.7% → 34.0% [C] (D2 (d)).",
        "**Capex is ~1% of revenue, there is no capitalized-software asset, and standalone FCF is ~$365m [C].** The dividend is ~19% of FCF; the “25%” problem is labelling, not cash (D3 §5).",
        "**The cost and margin resets are standard spin mechanics.** Standalone costs (~$26m [C]) are ~1.4% of revenue, and SBC moving to peer levels improves alignment (D5).",
        "**The AI risk has a counter-argument in the record:** the data sits “behind a firewall or a paywall” [IR], AI lowers MBGL's own processing costs, and an answer engine still needs a licensed, trusted source — potentially a new licensing channel (inference, untested).",
        "**The bear cluster is a de-rating risk, not an impairment risk.** It applies only if the market prices MBGL as a 9–10% compounder — which this document could not test without market data.",
        "**Price may be partly mix and upsell** (customers moving to higher tiers or adding products at renewal) rather than like-for-like list price; the 10-Q does not define “price increases” (D7 counters).",
    ])
    b.quote("GS", "We are finding that the brand is actually becoming more and more valuable.")

    # ======================================================================= APPENDIX A
    b.h1("Source limitations & verification", "Appendix A")
    b.h2("A.1 What the source set is")
    b.bullets([
        "Primary filings and transcripts accessed through Quartr only: Form 10 (2026-05-07), Form 10/A (2026-05-27), 10-Q Q2-26 and 8-K (2026-08-07), Investor Day and Q2 decks, three MBGL transcripts, S&P Global and IHS Markit 10-Ks and earnings materials.",
        "Quartr page text, not native PDFs: several tables were flattened or scrambled (annual cash-flow working capital, Q1 cash-flow components, tax provision 2024/23 split, lease maturities, Market Scan PPA liabilities, beneficial-ownership counts, part of the severance table).",
        "sec.gov (EDGAR XBRL), FRED, BEA, Census, BLS, the Fed and third-party sites were blocked by sandbox egress. Part B (industry series) is unfetched; [context] items are general knowledge.",
        "No market data (share price, market value, consensus) was available, so there is no valuation section.",
    ])
    b.h2("A.2 Verification performed (Part A)")
    ver = read(os.path.join(CAN, "VERIFICATION.md"))
    m = re.search(r"6/6 matched:\n\s*(.+?)\. No annual", ver)
    b.bullets([
        "Extraction: 4,859 rows across 6 files, self-verified for footing and ties; canonical layer 390 primary cells, 0 collisions (59 identical duplicates absorbed and logged), 0 leftovers, 3 logged MD&A gap-fills (PART_A_SUMMARY).",
        "Independent check: Quartr standardized financials matched 6 of 6 Q2-2026 values" + (f" ({m.group(1).strip()})" if m else "") + "; no annual periods are available there.",
        "Cross-document: Form 10 vs Form 10/A identical (annual + Q1); 10-Q 6M = Form 10/A Q1 + 10-Q Q2 on every IS line; 8-K IS/BS = 10-Q.",
        "Workbook recalc: 0 formula errors; 106 integrity-check cells, 0 failures.",
        "This document: every quote is asserted verbatim against the transcript quote banks at build time; financial tables are read from canonical/primary.csv; analysis tables are parsed from the analysis files.",
    ])
    b.h2("A.3 Outstanding verification")
    b.bullets([
        "{{TC: EDGAR XBRL company-facts cross-check of headline items for every period}}",
        "{{TC: native Form 10/A PDF: tax provision 2024/23 split, lease maturity table, Market Scan PPA liabilities (lines sum 59 vs printed 39)}}",
        "{{TC: Investor Day slide 91 image re-read to confirm the year mapping of organic and industry labels}}",
        "{{TC: PDF check of SPGI guidance slide cells mapped by position (FY23/FY24 Q3 revisions)}}",
    ])
    b.h2("A.4 Genuine non-disclosures (Part A)")
    b.bullets([
        "Revenue by brand or product, and by B2B business line; organic or constant-currency growth (S&P Global printed it every quarter); retention / NRR, ACV / ARR, ARPU, churn;",
        "segment assets (dropped in the 10-Q); TSA fees; deferred-revenue roll-forward; a standalone Q2 cash-flow statement.",
    ])

    # ======================================================================= APPENDIX B
    b.h1("Accounting notes", "Appendix B")
    rows = []
    with open(os.path.join(CAN, "accounting_notes.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append([r["type"], r["area"], r["item"], r["source"], r["treatment"]])
    b.table(["Type", "Area", "Item", "Source", "Treatment"], rows, widths=[0.6, 0.8, 3.2, 1.1, 1.1], size=7,
            caption=f"Exhibit B.1 — Accounting notes ({len(rows)} rows) [D]",
            source="Source: canonical/accounting_notes.csv. Types: BASIS = basis of preparation; RESTATE = restatement check; DEFN = definition change; DATAQ = data-quality issue; NONDISC = not disclosed; BREAK = structural break.")

    # ======================================================================= APPENDIX C
    b.h1("Glossary of tiers & source keys", "Appendix C")
    tiers = [
        ["[D]", "Disclosed", "Printed in a filing (Form 10/A, 10-Q, 8-K, predecessor 10-K) or company deck. [D-deck]/[D-pres] = company presentation (unaudited marketing figure); [D-flag] = printed but inconsistent."],
        ["[C]", "Computed", "Calculated by us from disclosed inputs; the method is stated next to the figure or in the source analysis file."],
        ["[E]", "Estimate", "Our estimate; the assumption is stated. Not a forecast of record."],
        ["[IR]", "Management verbal", "Said by management at an event (Investor Day, earnings call, conference) or on a predecessor call. Not audited."],
        ["[X]", "Third party", "Survey, consultant or data vendor (e.g., unnamed TAM consultant, Semrush, Teneo). Often unverifiable."],
        ["[context]", "General knowledge", "Background not taken from the source set; to be replaced by Part B series."],
        ["[gap]", "Not in sources", "The fact is not available in the documents read."],
        ["[TO COLLECT #n]", "Placeholder", "Data that does not exist in the source set; listed in the Placeholder register."],
    ]
    b.table(["Tag", "Meaning", "Use"], tiers, widths=[1.0, 1.2, 4.6], caption="Exhibit C.1 — Tier tags")
    keys = [
        ["10A / F10", "Form 10/A (2026-05-27, Quartr 3603533) / Form 10 (2026-05-07, 3603535); page numbers are Quartr pages"],
        ["10Q / 8K", "10-Q Q2-2026 (3699447) / Q2 release 8-K (3699450)"],
        ["ID / Q2 / GS", "Investor Day 2026-05-12 (event 676565) / Q2-26 call 2026-08-07 (704668) / Goldman Sachs Communacopia 2026-09-10 (725748)"],
        ["PRES s.N / ID-deck", "Investor Day slide N (doc 3352878)"],
        ["INFOyy / SPGIyy", "IHS Markit 10-K FY20yy / S&P Global 10-K FY20yy"],
        ["D1–D12, QUALITATIVE, SYNTHESIS, K", "Part D analysis files in work/analysis/"],
        ["OCC", "Organic constant currency"], ["BIG", "CARFAX Banking & Insurance Group"], ["CPO", "Certified pre-owned"],
        ["NRR", "Net revenue retention"], ["RPO", "Remaining performance obligations"], ["TSA / TMA / EMA", "Transition Services / Tax Matters / Employee Matters Agreement"],
        ["VHR / VIO / MUV", "Vehicle history report / vehicles in operation / monthly unique visitors"],
    ]
    b.table(["Key", "Meaning"], keys, widths=[1.8, 5.0], caption="Exhibit C.2 — Source keys and abbreviations")

    # ======================================================================= PLACEHOLDER REGISTER
    b.h1("Placeholder register")
    b.p(f"Auto-generated from the {len(b.placeholders)} [TO COLLECT] placeholders in this document. Page numbers are taken from a LibreOffice rendering of the document (approximate in Word). This register is the field-work list.")
    ppages = (pages or {}).get("placeholders", {})
    reg = [[str(n), sec, str(ppages.get(n, "n/a")), item] for n, sec, item in b.placeholders]
    b.table(["#", "Section", "Approx. page", "Item to collect"], reg, widths=[0.35, 1.9, 0.6, 3.95], size=7.5, num_cols=[2])
    return b


# ----------------------------------------------------------------------------- page location pass
def locate_pages(docx_path, builder):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return None
    try:
        import pymupdf as fitz  # noqa
    except Exception:
        try:
            import fitz  # noqa
        except Exception:
            return None
    tmp = tempfile.mkdtemp(prefix="mbgl_doc_")
    try:
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, docx_path],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
        pdf = os.path.join(tmp, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")
        doc = fitz.open(pdf)
        texts = [re.sub(r"\s+", " ", pg.get_text()) for pg in doc]
        res = {"headings": {}, "placeholders": {}, "npages": len(texts)}
        for n, _, _ in builder.placeholders:
            pat = re.compile(r"COLLECT\s*#\s*%d\s*:" % n)
            for i, t in enumerate(texts):
                if pat.search(t):
                    res["placeholders"][n] = i + 1
                    break
        contents_idx = next((i for i, t in enumerate(texts) if "Contents" in t), 1)
        for h in builder.headings:
            pat = re.compile(r"\s+".join(re.escape(w) for w in h.split()))
            for i, t in enumerate(texts):
                if i <= contents_idx:
                    continue
                if pat.search(t):
                    res["headings"][h] = i + 1
                    break
        # map "Appendix A Source ..." headings to TOC titles
        return res
    except Exception as e:  # pragma: no cover
        print("page location failed:", e, file=sys.stderr)
        return None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    b1 = build()
    b1.doc.save(OUT)
    pages = locate_pages(OUT, b1)
    if pages:
        b2 = build(pages)
        b2.doc.save(OUT)
        n = len(b2.placeholders)
        missing = [k for k, _, _ in b2.placeholders if k not in pages["placeholders"]]
        print(f"wrote {OUT}: ~{pages['npages']} pages, {len(b2.headings)} sections, {n} placeholders"
              + (f", page not located for {missing}" if missing else ""))
    else:
        print(f"wrote {OUT}: {len(b1.placeholders)} placeholders (page numbers unavailable: LibreOffice/pymupdf missing)")


if __name__ == "__main__":
    main()
