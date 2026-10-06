#!/usr/bin/env python3
"""Deterministic builder: deliverables/deck_content.json -> deliverables/MBGL_Research_Deck.pptx.

House style: 16:9, Arial, navy (#1F3864) action titles, teal/blue accents,
light-grey panels, source footnote and slide number on every slide, tier tags
on figures. All geometry is integer EMU; every bar series carries an explicit
<c:invertIfNegative val="0"/>.
"""
import copy
import json
import re
import sys

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_MARKER_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

ROOT = "/home/user/MBGL/work"
SRC = f"{ROOT}/deliverables/deck_content.json"
OUT = f"{ROOT}/deliverables/MBGL_Research_Deck.pptx"

EMU_PER_IN = 914400
FONT = "Arial"
NAVY, TEAL, BLUE = "1F3864", "0E7C86", "2E75B6"
LTEAL, GREY, AMBER, RED = "7FC4CB", "8C8C8C", "C9861A", "B0413E"
TXT, MUTED, PANEL, GRID = "262626", "595959", "F2F2F2", "D9D9D9"
TIER_COLORS = {"D": NAVY, "C": TEAL, "E": AMBER, "IR": "5B6F95", "X": GREY}


def E(inches):
    """Inches -> integer EMU (never a float)."""
    return int(round(float(inches) * EMU_PER_IN))


def rgb(h):
    return RGBColor.from_string(h)


def clean(t):
    return str(t).replace("**", "")


# ----------------------------------------------------------------------------- text helpers
def _set_run(run, text, size, bold=False, color=TXT, italic=False):
    run.text = clean(text)
    f = run.font
    f.name = FONT
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = rgb(color)


def textbox(slide, box, text="", size=12, bold=False, color=TXT, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, italic=False, margins=(0.04, 0.02), name=None):
    x, y, w, h = box
    tb = slide.shapes.add_textbox(Emu(E(x)), Emu(E(y)), Emu(E(w)), Emu(E(h)))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = tf.margin_right = Emu(E(margins[0]))
    tf.margin_top = tf.margin_bottom = Emu(E(margins[1]))
    tf.vertical_anchor = anchor
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if isinstance(line, list):  # runs: [(text, {opts})]
            for t, o in line:
                _set_run(p.add_run(), t, o.get("size", size), o.get("bold", bold), o.get("color", color), o.get("italic", italic))
        else:
            _set_run(p.add_run(), line, size, bold, color, italic)
    return tb


def _bullet(p, level=0):
    pPr = p._p.get_or_add_pPr()
    ind = 0.17 + 0.2 * level
    pPr.set("marL", str(E(ind)))
    pPr.set("indent", str(-E(0.17)))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buFont"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    buFont = etree.SubElement(pPr, qn("a:buFont"))
    buFont.set("typeface", FONT)
    bu = etree.SubElement(pPr, qn("a:buChar"))
    bu.set("char", "•")


def bullets(slide, box, items, size=12, color=TXT, space_after=6):
    x, y, w, h = box
    tb = slide.shapes.add_textbox(Emu(E(x)), Emu(E(y)), Emu(E(w)), Emu(E(h)))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = tf.margin_right = Emu(E(0.04))
    tf.margin_top = tf.margin_bottom = Emu(E(0.02))
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        _bullet(p, it.get("level", 0))
        p.space_after = Pt(space_after)
        if it.get("head"):
            _set_run(p.add_run(), it["head"], size, True, NAVY)
        _set_run(p.add_run(), it.get("text", ""), size, it.get("bold", False), color)
    return tb


def rect(slide, box, fill, line=None, shape=MSO_SHAPE.RECTANGLE, name=None, radius=None):
    x, y, w, h = box
    s = slide.shapes.add_shape(shape, Emu(E(x)), Emu(E(y)), Emu(E(w)), Emu(E(h)))
    if name:
        s.name = name
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(0.75)
    s.shadow.inherit = False
    st = s._element.find(qn("p:style"))
    if st is not None:
        s._element.remove(st)
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    tf = s.text_frame
    tf.margin_left = tf.margin_right = Emu(E(0.06))
    tf.margin_top = tf.margin_bottom = Emu(E(0.03))
    return s


def shape_text(s, lines, size=11, bold=False, color=TXT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tf = s.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if isinstance(line, list):
            for t, o in line:
                _set_run(p.add_run(), t, o.get("size", size), o.get("bold", bold), o.get("color", color), o.get("italic", False))
        else:
            _set_run(p.add_run(), line, size, bold, color)


def tier_tag(slide, x_right, y, tier, h=0.22):
    t = clean(tier)
    w = 0.16 + 0.085 * len(t) + 0.12
    first = re.split(r"[/ ]", t)[0]
    col = TIER_COLORS.get(first, GREY)
    s = rect(slide, (x_right - w, y, w, h), col, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.3, name=f"Tier tag {t}")
    s.text_frame.margin_left = s.text_frame.margin_right = Emu(0)
    s.text_frame.margin_top = s.text_frame.margin_bottom = Emu(0)
    shape_text(s, [f"[{t}]"], size=8, bold=True, color="FFFFFF", align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return s


# ----------------------------------------------------------------------------- chart helpers
def fact_val(doc, fid, scale=1.0):
    v = doc["facts"][fid]["value"]
    return float(v) * scale


def set_invert_if_negative_false(chart):
    """Explicit <c:invertIfNegative val="0"/> on every bar-chart series (schema position after c:spPr)."""
    cs = chart._chartSpace
    for ser in cs.iter(qn("c:ser")):
        parent = ser.getparent()
        if parent.tag != qn("c:barChart"):
            continue
        existing = ser.find(qn("c:invertIfNegative"))
        if existing is None:
            existing = etree.Element(qn("c:invertIfNegative"))
            # insert after idx/order/tx/spPr (whichever present last)
            anchor_tags = [qn("c:spPr"), qn("c:tx"), qn("c:order"), qn("c:idx")]
            pos = None
            for i, child in enumerate(ser):
                if child.tag in anchor_tags:
                    pos = i
            ser.insert((pos + 1) if pos is not None else 0, existing)
        existing.set("val", "0")


def style_axis(ax, size=10, color=MUTED, visible=True, line=True):
    ax.visible = visible
    ax.tick_labels.font.size = Pt(size)
    ax.tick_labels.font.name = FONT
    ax.tick_labels.font.color.rgb = rgb(color)
    if line:
        ax.format.line.color.rgb = rgb("BFBFBF")
    else:
        ax.format.line.fill.background()


def chart_title_row(slide, el):
    x, y, w, h = el["box"]
    textbox(slide, (x, y, w - 0.9, 0.3), el.get("title", ""), size=11, bold=True, color=NAVY)
    if el.get("tier"):
        tier_tag(slide, x + w - 0.02, y + 0.04, el["tier"])


def add_chart(slide, el, doc):
    x, y, w, h = el["box"]
    chart_title_row(slide, el)
    note_h = 0.32 if el.get("note") else 0.0
    cx, cy, cw, ch = x, y + 0.34, w, h - 0.34 - note_h
    kind = el["chart"]
    cd = CategoryChartData()
    cd.categories = el["categories"]
    for s in el["series"]:
        scale = s.get("scale")
        vals = []
        for i, fid in enumerate(s["facts"]):
            sc = scale[i] if isinstance(scale, list) else (scale or 1.0)
            vals.append(fact_val(doc, fid, sc))
        cd.add_series(s["name"], vals)
    ctype = {"column": XL_CHART_TYPE.COLUMN_CLUSTERED, "column_stacked": XL_CHART_TYPE.COLUMN_STACKED,
             "bar": XL_CHART_TYPE.BAR_CLUSTERED, "line": XL_CHART_TYPE.LINE_MARKERS,
             "doughnut": XL_CHART_TYPE.DOUGHNUT}[kind]
    gf = slide.shapes.add_chart(ctype, Emu(E(cx)), Emu(E(cy)), Emu(E(cw)), Emu(E(ch)), cd)
    gf.name = f"Chart: {el.get('title', '')}"[:60]
    chart = gf.chart
    chart.font.name = FONT
    chart.font.size = Pt(10)
    chart.font.color.rgb = rgb(MUTED)
    chart.has_title = False
    legend = el.get("legend", "bottom")
    if legend == "none":
        chart.has_legend = False
    else:
        chart.has_legend = True
        chart.legend.position = {"bottom": XL_LEGEND_POSITION.BOTTOM, "right": XL_LEGEND_POSITION.RIGHT,
                                 "top": XL_LEGEND_POSITION.TOP}[legend]
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(10)
        chart.legend.font.name = FONT
    plot = chart.plots[0]
    nf = el.get("number_format", "General")
    lsize = el.get("label_size", 9)

    if kind == "doughnut":
        colors = el.get("colors", [NAVY, TEAL, LTEAL])
        ser = plot.series[0]
        for i, pt in enumerate(ser.points):
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = rgb(colors[i % len(colors)])
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.number_format = nf
        dl.number_format_is_linked = False
        dl.show_value = True
        dl.font.size = Pt(12)
        dl.font.bold = True
        dl.font.color.rgb = rgb("FFFFFF")
        dl.font.name = FONT
        dn = chart._chartSpace.find(".//" + qn("c:doughnutChart"))
        hs = dn.find(qn("c:holeSize"))
        if hs is None:
            hs = etree.SubElement(dn, qn("c:holeSize"))
        hs.set("val", "55")
    else:
        if kind in ("column", "column_stacked", "bar"):
            if "gap" in el:
                plot.gap_width = int(el["gap"])
            if "overlap" in el:
                plot.overlap = int(el["overlap"])
        va = chart.value_axis
        ca = chart.category_axis
        style_axis(ca, size=10)
        ca.has_major_gridlines = False
        ca.major_tick_mark = 2  # none
        from pptx.enum.chart import XL_TICK_MARK, XL_TICK_LABEL_POSITION
        ca.major_tick_mark = XL_TICK_MARK.NONE
        ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
        if kind == "bar":
            style_axis(va, size=9, visible=False, line=False)
            va.has_major_gridlines = False
            if el.get("reverse"):
                ca.reverse_order = True
        else:
            style_axis(va, size=9, line=False)
            va.has_major_gridlines = True
            va.major_gridlines.format.line.color.rgb = rgb(GRID)
            va.major_gridlines.format.line.width = Pt(0.5)
            va.major_tick_mark = XL_TICK_MARK.NONE
            va.tick_labels.number_format = nf
            va.tick_labels.number_format_is_linked = False
        if "y_min" in el:
            va.minimum_scale = el["y_min"]
        if "y_max" in el:
            va.maximum_scale = el["y_max"]
        if "major_unit" in el:
            va.major_unit = el["major_unit"]
        for i, s in enumerate(el["series"]):
            ser = plot.series[i]
            col = s.get("color", NAVY)
            if kind == "line":
                ser.format.line.color.rgb = rgb(col)
                ser.format.line.width = Pt(2.25)
                ser.smooth = False
                ser.marker.style = XL_MARKER_STYLE.CIRCLE
                ser.marker.size = 7
                ser.marker.format.fill.solid()
                ser.marker.format.fill.fore_color.rgb = rgb(col)
                ser.marker.format.line.color.rgb = rgb(col)
            else:
                ser.format.fill.solid()
                ser.format.fill.fore_color.rgb = rgb(col)
                ser.format.line.fill.background()
                ser.invert_if_negative = False
                for pi, pc in (el.get("point_colors") or {}).items():
                    pt = ser.points[int(pi)]
                    pt.format.fill.solid()
                    pt.format.fill.fore_color.rgb = rgb(pc)
            dl = ser.data_labels
            dl.show_value = True
            dl.number_format = nf
            dl.number_format_is_linked = False
            dl.font.size = Pt(lsize)
            dl.font.name = FONT
            pos = el.get("label_pos", "outEnd")
            if kind == "column_stacked":
                dl.position = XL_LABEL_POSITION.CENTER
                dark = col.upper() in (NAVY, TEAL, "4F6D8F", BLUE, RED)
                dl.font.color.rgb = rgb("FFFFFF" if dark else TXT)
                dl.font.bold = True
            elif kind == "line":
                dl.position = XL_LABEL_POSITION.ABOVE
                dl.font.color.rgb = rgb(TXT)
                dl.font.bold = True
            else:
                dl.position = {"outEnd": XL_LABEL_POSITION.OUTSIDE_END, "inEnd": XL_LABEL_POSITION.INSIDE_END,
                               "ctr": XL_LABEL_POSITION.CENTER}.get(pos, XL_LABEL_POSITION.OUTSIDE_END)
                dl.font.color.rgb = rgb(TXT)
        set_invert_if_negative_false(chart)
    if el.get("note"):
        textbox(slide, (x, y + h - note_h, w, note_h), el["note"], size=9.5, color=MUTED, italic=True)
    return gf


def add_waterfall(slide, el, doc):
    x, y, w, h = el["box"]
    chart_title_row(slide, el)
    steps = el["steps"]
    base, vals, kinds, labels = [], [], [], []
    running = 0.0
    for st in steps:
        v = fact_val(doc, st["fact"])
        k = st["kind"]
        if k == "total":
            base.append(0.0)
            vals.append(v)
            running = v
        elif k == "up":
            base.append(running)
            vals.append(v)
            running += v
        else:
            running -= v
            base.append(running)
            vals.append(v)
        kinds.append(k)
        labels.append(st["label"])
    cd = CategoryChartData()
    cd.categories = labels
    cd.add_series("Base", base)
    cd.add_series("Value", vals)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Emu(E(x)), Emu(E(y + 0.34)), Emu(E(w)), Emu(E(h - 0.34)), cd)
    gf.name = "Chart: standalone NI bridge (waterfall)"
    chart = gf.chart
    chart.font.name = FONT
    chart.font.size = Pt(10)
    chart.has_legend = False
    plot = chart.plots[0]
    plot.gap_width = 45
    from pptx.enum.chart import XL_TICK_MARK, XL_TICK_LABEL_POSITION
    va, ca = chart.value_axis, chart.category_axis
    style_axis(ca, size=9)
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    style_axis(va, size=9, line=False)
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = rgb(GRID)
    va.major_tick_mark = XL_TICK_MARK.NONE
    va.minimum_scale = 0
    sb, sv = plot.series[0], plot.series[1]
    sb.format.fill.background()
    sb.format.line.fill.background()
    sb.invert_if_negative = False
    sv.invert_if_negative = False
    colmap = {"total": NAVY, "up": TEAL, "down": RED}
    for i, pt in enumerate(sv.points):
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(colmap[kinds[i]])
        pt.format.line.fill.background()
        dl = pt.data_label
        tf = dl.text_frame
        v = vals[i]
        txt = f"({v:,.0f})" if kinds[i] == "down" else (f"+{v:,.0f}" if kinds[i] == "up" else f"{v:,.0f}")
        tf.text = txt
        r = tf.paragraphs[0].runs[0]
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.name = FONT
        r.font.color.rgb = rgb("FFFFFF")
        dl.position = XL_LABEL_POSITION.CENTER
    set_invert_if_negative_false(chart)
    return gf


# ----------------------------------------------------------------------------- table
VERDICT = {"yes": RED, "missed-lowered": RED, "cut": RED, "missed 110-310bp": RED, "beat": TEAL, "met": TEAL, "no": TEAL,
           "mixed": AMBER, "unknown": AMBER}
HML = {"H": RED, "M": AMBER, "L": TEAL}


def add_table(slide, el):
    x, y, w, h = el["box"]
    cols, rows = el["columns"], el["rows"]
    if el.get("tier"):
        cols = list(cols)
        cols[0] = (cols[0] + "  " if cols[0] else "") + f"[{el['tier']}]"
    nr, nc = len(rows) + 1, len(cols)
    gf = slide.shapes.add_table(nr, nc, Emu(E(x)), Emu(E(y)), Emu(E(w)), Emu(E(h)))
    gf.name = "Table"
    tbl = gf.table
    # remove default table style banding flags
    tblPr = tbl._tbl.tblPr
    tblPr.set("bandRow", "0")
    tblPr.set("firstRow", "1")
    cw = el.get("col_widths") or [w / nc] * nc
    tot = sum(cw)
    widths = [E(c / tot * w) for c in cw]
    widths[-1] = E(w) - sum(widths[:-1])
    for i, wd in enumerate(widths):
        tbl.columns[i].width = Emu(int(wd))
    hdr_h = el.get("header_h", 0.5 if any(len(str(c)) * el.get("font_size", 10) * 0.0078 > (cw[i] / tot * w - 0.12) for i, c in enumerate(cols)) else 0.36)
    body_h = (h - hdr_h) / (nr - 1)
    tbl.rows[0].height = Emu(E(hdr_h))
    for r in range(1, nr):
        tbl.rows[r].height = Emu(E(body_h))
    fs = el.get("font_size", 10)
    for c, txt in enumerate(cols):
        cell = tbl.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(NAVY)
        _cell_text(cell, txt, fs, True, "FFFFFF")
    for r, row in enumerate(rows, start=1):
        last = r == nr - 1
        for c, txt in enumerate(row):
            cell = tbl.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb("FFFFFF" if r % 2 else PANEL)
            bold = (c == 0) or (el.get("bold_last") and last)
            color = NAVY if c == 0 else TXT
            align = PP_ALIGN.LEFT
            if el.get("verdict_col") == c:
                key = str(txt).lower()
                color = VERDICT.get(key, TXT)
                bold = True
            if c in el.get("hml_cols", []):
                color = HML.get(str(txt), TXT)
                bold = True
                align = PP_ALIGN.CENTER
            _cell_text(cell, txt, fs, bold, color, align)
    return gf


def _cell_text(cell, txt, size, bold, color, align=PP_ALIGN.LEFT):
    cell.margin_left = cell.margin_right = Emu(E(0.06))
    cell.margin_top = cell.margin_bottom = Emu(E(0.03))
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    _set_run(p.add_run(), txt, size, bold, color)


# ----------------------------------------------------------------------------- composite elements
def add_cards(slide, el):
    x, y, w, h = el["box"]
    cols, rows, gap = el["cols"], el["rows"], el.get("gap", 0.15)
    cw = (w - gap * (cols - 1)) / cols
    chh = (h - gap * (rows - 1)) / rows
    ts, bs = el.get("title_size", 12), el.get("body_size", 10.5)
    for i, it in enumerate(el["items"]):
        r, c = divmod(i, cols)
        bx, by = x + c * (cw + gap), y + r * (chh + gap)
        rect(slide, (bx, by, cw, chh), el.get("fill", PANEL), shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, name=f"Card {i + 1}")
        tag_w = 0.0
        if it.get("tag"):
            tg = tier_tag(slide, bx + cw - 0.1, by + 0.1, it["tag"])
            tag_w = tg.width / EMU_PER_IN + 0.08
        textbox(slide, (bx + 0.12, by + 0.07, cw - 0.24 - tag_w, 0.42), it["title"], size=ts, bold=True, color=NAVY)
        title_lines = 1 if len(it["title"]) * ts * 0.0075 < (cw - 0.24 - tag_w) else 2
        ty = by + 0.07 + 0.22 * title_lines + 0.12
        body = it["body"] if isinstance(it["body"], list) else [it["body"]]
        paras = []
        for para in body:
            if isinstance(para, dict):
                paras.append([(para["head"], {"bold": True, "color": TEAL}), (para["text"], {})])
            else:
                paras.append(para)
        tb = textbox(slide, (bx + 0.12, ty, cw - 0.24, chh - (ty - by) - 0.06), paras, size=bs, color=TXT)
        for p in tb.text_frame.paragraphs:
            p.space_after = Pt(8)


def add_kpis(slide, el):
    x, y, w, h = el["box"]
    cols = el["cols"]
    items = el["items"]
    rows = (len(items) + cols - 1) // cols
    gap = 0.12
    cw = (w - gap * (cols - 1)) / cols
    chh = (h - gap * (rows - 1)) / rows
    vs = el.get("value_size", 22)
    for i, it in enumerate(items):
        r, c = divmod(i, cols)
        bx, by = x + c * (cw + gap), y + r * (chh + gap)
        rect(slide, (bx, by, cw, chh), el.get("fill", PANEL), shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08, name=f"KPI {i + 1}")
        if it.get("tier"):
            tier_tag(slide, bx + cw - 0.06, by + 0.06, it["tier"], h=0.2)
        vh = vs / 72 * 1.25
        textbox(slide, (bx + 0.08, by + 0.2, cw - 0.16, vh), it["value"], size=vs, bold=True, color=NAVY)
        textbox(slide, (bx + 0.08, by + 0.2 + vh, cw - 0.16, chh - 0.22 - vh), it["label"], size=10, color=MUTED)


def add_quote(slide, el, doc):
    q = doc["quotes"][el["quote"]]
    x, y, w, h = el["box"]
    qt = q["text"] if q["text"][0].isupper() else "…" + q["text"]
    size = el.get("size", 11)
    textbox(slide, (x, y, w, h), [[("“" + qt + "”", {"italic": True, "color": NAVY, "size": size}),
                                   ("   " + q["who"], {"color": MUTED, "size": size - 1.5})]],
            size=size, anchor=MSO_ANCHOR.MIDDLE)


def add_twocol(slide, el):
    x, y, w, h = el["box"]
    gap = 0.2
    cw = (w - gap) / 2
    for k, side in enumerate(("left", "right")):
        bx = x + k * (cw + gap)
        rect(slide, (bx, y, cw, h), PANEL, name=f"{side} column panel")
        hd = rect(slide, (bx, y, cw, 0.4), el[f"{side}_color"], name=f"{side} column header")
        shape_text(hd, [el[f"{side}_title"]], size=12, bold=True, color="FFFFFF", anchor=MSO_ANCHOR.MIDDLE)
        bullets(slide, (bx + 0.1, y + 0.52, cw - 0.2, h - 0.6), [{"text": t} for t in el[side]], size=11, space_after=7)


def add_timeline(slide, el):
    x, y, w, h = el["box"]
    t0, t1 = el["start"], el["end"]

    def X(t):
        return x + (t - t0) / (t1 - t0) * w

    band_y, band_h = y + 1.0, 0.44
    for era in el["eras"]:
        bx0, bx1 = X(era["start"]), X(era["end"])
        s = rect(slide, (bx0, band_y, bx1 - bx0, band_h), era["color"], name=f"Era {era['label'][:20]}")
        shape_text(s, [era["label"]], size=10, bold=True, color="FFFFFF", align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    for yr in range(int(t0), int(t1) + 1):
        textbox(slide, (X(yr) - 0.3, band_y + band_h + 0.02, 0.6, 0.22), str(yr), size=8, color=MUTED, align=PP_ALIGN.CENTER)
    lw = 2.15
    for ev in el["events"]:
        cx = X(ev["x"])
        lx = min(max(cx - lw / 2, x), x + w - lw)
        if ev["pos"] == "up":
            ly = band_y - 0.95
            line_y0, line_y1 = ly + 0.55, band_y
        else:
            ly = band_y + band_h + 0.62 if ev.get("level", 1) == 1 else band_y + band_h + 1.25
            line_y0, line_y1 = band_y + band_h + 0.25, ly
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(E(cx)), Emu(E(line_y0)), Emu(E(cx)), Emu(E(line_y1)))
        conn.line.color.rgb = rgb("A6A6A6")
        conn.line.width = Pt(0.75)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Emu(E(cx - 0.05)), Emu(E((line_y1 if ev["pos"] == "up" else line_y0) - 0.05)), Emu(E(0.1)), Emu(E(0.1)))
        dot.fill.solid()
        dot.fill.fore_color.rgb = rgb(NAVY)
        dot.line.fill.background()
        align = PP_ALIGN.CENTER
        if lx <= x + 0.001:
            align = PP_ALIGN.LEFT
        elif lx >= x + w - lw - 0.001:
            align = PP_ALIGN.RIGHT
        textbox(slide, (lx, ly, lw, 0.55), [[(ev["date"], {"bold": True, "color": NAVY})], ev["label"]], size=10, align=align,
                anchor=MSO_ANCHOR.BOTTOM if ev["pos"] == "up" else MSO_ANCHOR.TOP)


def _arrow(slide, x0, y0, x1, y1, color=TEAL, width=1.75):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(E(x0)), Emu(E(y0)), Emu(E(x1)), Emu(E(y1)))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(width)
    ln = c.line._get_or_add_ln()
    tail = etree.SubElement(ln, qn("a:tailEnd"))
    tail.set("type", "triangle")
    tail.set("w", "med")
    tail.set("len", "med")
    return c


def add_flow(slide, el):
    x, y, w, h = el["box"]
    colw_side, colw_c = 3.55, 3.3
    lx, rx = x, x + w - colw_side
    cxx = x + (w - colw_c) / 2
    top = y + 0.38
    n = len(el["left"])
    gap = 0.12
    bh = 0.82
    body_h = n * bh + (n - 1) * gap
    for (cx0, cw0, ttl) in ((lx, colw_side, el["left_title"]), (cxx, colw_c, el["center_title"]), (rx, colw_side, el["right_title"])):
        textbox(slide, (cx0, y, cw0, 0.3), ttl, size=10.5, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
    for side, x0, fill in (("left", lx, "EEF3F8"), ("right", rx, "E6F2F3")):
        for i, it in enumerate(el[side]):
            by = top + i * (bh + gap)
            s = rect(slide, (x0, by, colw_side, bh), fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1, name=f"{side} node {i + 1}")
            shape_text(s, [[(it["title"], {"bold": True, "color": NAVY, "size": 11.5})], [(it["stat"], {"color": TXT, "size": 10.5})]],
                       anchor=MSO_ANCHOR.MIDDLE)
            s.text_frame.margin_left = Emu(E(0.12))
            mid = by + bh / 2
            if side == "left":
                _arrow(slide, x0 + colw_side + 0.04, mid, cxx - 0.06, top + body_h / 2 + (i - (n - 1) / 2) * 0.35)
            else:
                _arrow(slide, cxx + colw_c + 0.06, top + body_h / 2 + (i - (n - 1) / 2) * 0.35, x0 - 0.04, mid)
    c = rect(slide, (cxx, top, colw_c, body_h), NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, name="Archive node")
    lines = [[("VIN-keyed archive", {"bold": True, "color": "FFFFFF", "size": 13})]]
    for t in el["center"]:
        lines.append([(t, {"color": "FFFFFF", "size": 11})])
    shape_text(c, lines, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    for p in c.text_frame.paragraphs:
        p.space_after = Pt(5)
    fb_y = top + body_h + 0.14
    fb = slide.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Emu(E(lx)), Emu(E(fb_y)), Emu(E(w)), Emu(E(0.5)))
    fb.name = "Feedback loop arrow"
    fb.fill.solid()
    fb.fill.fore_color.rgb = rgb("D5ECEE")
    fb.line.fill.background()
    fb.adjustments[0] = 0.62
    fb.adjustments[1] = 0.35
    shape_text(fb, [el["feedback"]], size=10.5, color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ----------------------------------------------------------------------------- slide frame
def add_slide_number(slide, n):
    tb = textbox(slide, (12.3, 7.02, 0.6, 0.3), "", size=9, color=MUTED, align=PP_ALIGN.RIGHT, name="Slide number")
    p = tb.text_frame.paragraphs[0]
    fld = etree.SubElement(p._p, qn("a:fld"))
    fld.set("id", "{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}")
    fld.set("type", "slidenum")
    rPr = etree.SubElement(fld, qn("a:rPr"))
    rPr.set("lang", "en-US")
    rPr.set("sz", "900")
    sf = etree.SubElement(rPr, qn("a:solidFill"))
    c = etree.SubElement(sf, qn("a:srgbClr"))
    c.set("val", MUTED)
    lat = etree.SubElement(rPr, qn("a:latin"))
    lat.set("typeface", FONT)
    t = etree.SubElement(fld, qn("a:t"))
    t.text = str(n)


def add_footer(slide, sources, n, dark=False):
    txt = "Source: " + "; ".join(sources)
    textbox(slide, (0.45, 6.9, 11.7, 0.5), txt, size=8.5, color=("BFC8D6" if dark else MUTED), name="Source footnote",
            anchor=MSO_ANCHOR.TOP)
    add_slide_number(slide, n)


def build_title(prs, s, doc):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    bg = rect(sl, (0, 0, 13.333, 7.5), NAVY, name="Background")
    textbox(sl, (0.7, 1.0, 11.0, 0.35), s["kicker"], size=12, bold=True, color=LTEAL)
    textbox(sl, (0.7, 1.45, 11.6, 1.9), s["title"], size=32, bold=True, color="FFFFFF")
    textbox(sl, (0.7, 3.45, 11.4, 0.7), s["subtitle"], size=15, color="D5ECEE")
    chips = s.get("chips", [])
    cw, gap = 2.85, 0.2
    for i, ch in enumerate(chips):
        bx = 0.7 + i * (cw + gap)
        r = rect(sl, (bx, 4.45, cw, 1.05), "2B4A7E", shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08, name=f"Chip {i + 1}")
        shape_text(r, [[(ch["value"], {"bold": True, "size": 22, "color": "FFFFFF"})], [(ch["label"], {"size": 10.5, "color": "D5ECEE"})]],
                   anchor=MSO_ANCHOR.MIDDLE)
        r.text_frame.margin_left = Emu(E(0.15))
    textbox(sl, (0.7, 5.75, 11.6, 0.95), s["meta"], size=11, color="D5ECEE")
    add_footer(sl, s["sources"], s["n"], dark=True)
    return sl


def build_content(prs, s, doc):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    bgr = sl.background.fill
    bgr.solid()
    bgr.fore_color.rgb = rgb("FFFFFF")
    textbox(sl, (0.45, 0.25, 12.4, 0.26), s["kicker"], size=10, bold=True, color=TEAL, name="Section label")
    textbox(sl, (0.45, 0.5, 12.45, 0.9), s["title"], size=20, bold=True, color=NAVY, name="Title", anchor=MSO_ANCHOR.TOP)
    for el in s.get("elements", []):
        t = el["type"]
        if t == "text":
            textbox(sl, el["box"], el["text"], size=el.get("size", 12), bold=el.get("bold", False), color=el.get("color", TXT))
        elif t == "bullets":
            bullets(sl, el["box"], el["items"], size=el.get("size", 12))
        elif t == "panel":
            rect(sl, el["box"], el.get("fill", PANEL), shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04, name="Panel")
        elif t == "callout":
            r = rect(sl, el["box"], "E6F2F3", shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12, name="Callout")
            r.text_frame.margin_left = r.text_frame.margin_right = Emu(E(0.15))
            shape_text(r, [el["text"]], size=el.get("size", 11), color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
        elif t == "banner":
            r = rect(sl, el["box"], el.get("fill", "FBEFD9"), name="Banner")
            r.text_frame.margin_left = Emu(E(0.15))
            shape_text(r, [el["text"]], size=10.5, bold=True, color=el.get("color", "7A4E00"), anchor=MSO_ANCHOR.MIDDLE)
        elif t == "chart":
            add_chart(sl, el, doc)
        elif t == "waterfall":
            add_waterfall(sl, el, doc)
        elif t == "table":
            add_table(sl, el)
        elif t == "cards":
            add_cards(sl, el)
        elif t == "kpis":
            add_kpis(sl, el)
        elif t == "quote":
            add_quote(sl, el, doc)
        elif t == "twocol":
            add_twocol(sl, el)
        elif t == "timeline":
            add_timeline(sl, el)
        elif t == "flow":
            add_flow(sl, el)
        else:
            raise ValueError(t)
    add_footer(sl, s["sources"], s["n"])
    return sl


def set_theme_fonts(prs):
    for part in prs.part.package.iter_parts():
        if part.partname.endswith("theme1.xml") or "/theme/" in str(part.partname):
            blob = part.blob.decode("utf8")
            blob = re.sub(r'(<a:latin typeface=")[^"]*(")', r"\1Arial\2", blob)
            part._blob = blob.encode("utf8")


def main():
    doc = json.load(open(SRC))
    prs = Presentation()
    prs.slide_width = Emu(12192000)  # exact 13.333in
    prs.slide_height = Emu(6858000)  # exact 7.5in
    set_theme_fonts(prs)
    for s in doc["slides"]:
        sl = build_title(prs, s, doc) if s["layout"] == "title" else build_content(prs, s, doc)
        sl.notes_slide.notes_text_frame.text = clean(s["notes"])
    prs.core_properties.title = "MBGL Research Deck"
    prs.core_properties.author = "Part E research"
    prs.save(OUT)
    print(f"saved {OUT} ({len(doc['slides'])} slides)")


if __name__ == "__main__":
    main()
