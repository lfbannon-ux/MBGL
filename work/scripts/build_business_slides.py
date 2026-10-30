#!/usr/bin/env python3
"""Build one slide per business line, in two versions:
  deliverables/MBGL_Business_Lines_Presentation.pptx  (presentation-ready: plain English, fewer words)
  deliverables/MBGL_Business_Lines_Internal.pptx      (internal research: denser, source tiers, more quotes)
House style: navy/teal, Source Sans Pro Bold (headings, numbers) + Source Sans Pro Light (body). 16:9.
Content: scripts/business_slides_content.py (facts sourced in research_notes/slides/*.md)."""
import os
import sys

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from business_slides_content import BUSINESSES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOLD, LIGHT = 'Source Sans Pro', 'Source Sans Pro Light'
NAVY, TEAL, LTEAL, GREY, MUTED = '1F3864', '0E7C86', '7FC4CB', 'A6A6A6', '595959'
TXT, PANEL, GRID, AMBER = '262626', 'F2F2F2', 'D9D9D9', 'C9861A'

E = lambda inch: Emu(int(round(inch * 914400)))
rgb = lambda h: RGBColor.from_string(h)

# Layout (inches) on a 13.333 x 7.5 canvas
M = 0.5
W = 13.333 - 2 * M
LX, LW = M, 5.2
RX = M + LW + 0.3
RW = 13.333 - M - RX
TOP = 2.4
FOOT_Y = 6.98
QY = 5.95  # quote band top

SIZES = {  # per version
    'pres': dict(title=20, body=10.5, sec=11.5, quote=10.5, attr=8.5, table=9, chart=9, stat=19, statlab=9),
    'int': dict(title=18, body=9, sec=10, quote=9, attr=7.5, table=8, chart=8, stat=17, statlab=8),
}


def run(p, text, font=LIGHT, size=11, color=TXT, bold=False, italic=False):
    r = p.add_run()
    r.text = text
    f = r.font
    f.name, f.size, f.bold, f.italic = font, Pt(size), bold, italic
    f.color.rgb = rgb(color)
    return r


def textbox(slide, x, y, w, h, name, anchor=MSO_ANCHOR.TOP, margin=0.0):
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ('left', 'right', 'top', 'bottom'):
        setattr(tf, f'margin_{side}', E(margin))
    return tf


def bullet(p, char='•', indent=0.14):
    pPr = p._p.get_or_add_pPr()
    pPr.set('marL', str(int(indent * 914400)))
    pPr.set('indent', str(int(-indent * 914400)))
    for tag in ('a:buNone', 'a:buChar', 'a:buAutoNum'):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    buf = etree.SubElement(pPr, qn('a:buFont'))
    buf.set('typeface', 'Arial')
    bu = etree.SubElement(pPr, qn('a:buChar'))
    bu.set('char', char)


def rect(slide, x, y, w, h, fill, name, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, E(x), E(y), E(w), E(h))
    s.name = name
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(fill)
    s.line.fill.background()
    st = s._element.find(qn('p:style'))
    if st is not None:
        s._element.remove(st)
    return s


def header(slide, b, v, S):
    tf = textbox(slide, M, 0.3, W, 0.25, 'Kicker')
    run(tf.paragraphs[0], b['kicker'], BOLD, 10, TEAL, bold=True)
    tf = textbox(slide, M, 0.52, W, 0.78, 'Title', anchor=MSO_ANCHOR.TOP)
    run(tf.paragraphs[0], b['title'][v], BOLD, S['title'], NAVY, bold=True)
    tf = textbox(slide, M, 1.33, W, 0.25, 'Subtitle')
    run(tf.paragraphs[0], b['subtitle'], LIGHT, 9.5 if v == 'pres' else 8.5, MUTED)


def stats(slide, b, S):
    n, gap, y, h = len(b['stats']), 0.15, 1.66, 0.6
    w = (W - gap * (n - 1)) / n
    for i, (val, lab) in enumerate(b['stats']):
        x = M + i * (w + gap)
        rect(slide, x, y, w, h, PANEL, f'Stat {i+1} panel')
        tf = textbox(slide, x + 0.12, y + 0.06, w - 0.24, h - 0.1, f'Stat {i+1}', margin=0)
        run(tf.paragraphs[0], val, BOLD, S['stat'], NAVY, bold=True)
        p = tf.add_paragraph()
        run(p, lab, LIGHT, S['statlab'], MUTED)


def left_column(slide, b, v, S):
    tf = textbox(slide, LX, TOP, LW, FOOT_Y - TOP - 0.1, 'Business description')
    first = True
    for hdr, items in b['sections'][v]:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        if not first:
            p.space_before = Pt(7 if v == 'pres' else 5)
        first = False
        run(p, hdr, BOLD, S['sec'], TEAL, bold=True)
        for j, it in enumerate(items):
            q = tf.add_paragraph()
            q.space_before = Pt(2)
            is_example = it.startswith('Example:') or it.startswith('e.g.')
            if is_example:
                run(q, 'Example: ' if it.startswith('Example:') else '', BOLD, S['body'], NAVY, bold=True)
                run(q, it.split(':', 1)[1].strip() if it.startswith('Example:') else it, LIGHT, S['body'], TXT)
                bullet(q, '›')
            else:
                run(q, it, LIGHT, S['body'], TXT)
                if len(items) > 1:
                    bullet(q)


def style_chart(chart, S, legend):
    chart.font.name = LIGHT
    chart.font.size = Pt(S['chart'])
    chart.font.color.rgb = rgb(MUTED)
    chart.has_title = False
    chart.has_legend = legend
    if legend:
        chart.legend.position = XL_LEGEND_POSITION.TOP
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(S['chart'])
        chart.legend.font.name = LIGHT


def axes(chart, S, pct=False, vmax=None):
    va, ca = chart.value_axis, chart.category_axis
    va.visible = False
    va.has_major_gridlines = False
    if vmax:
        va.maximum_scale = vmax
    va.minimum_scale = 0
    ca.format.line.color.rgb = rgb(GRID)
    ca.tick_labels.font.size = Pt(S['chart'])
    ca.tick_labels.font.name = LIGHT
    ca.has_major_gridlines = False


def no_invert(chart):
    for ser in chart.plots[0].series:
        ser.invert_if_negative = False


def labels(plot, S, fmt, color=TXT, pos=None, bold=False):
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format, dl.number_format_is_linked = fmt, False
    dl.font.size = Pt(S['chart'])
    dl.font.name = BOLD if bold else LIGHT
    dl.font.bold = bold
    dl.font.color.rgb = rgb(color)
    if pos is not None:
        dl.position = pos


def add_chart(slide, b, S, x, y, w, h):
    c = b['chart']
    tf = textbox(slide, x, y, w, 0.25, 'Chart title')
    run(tf.paragraphs[0], c['title'], BOLD, S['sec'] - 0.5, NAVY, bold=True)
    cy, ch = y + 0.27, h - 0.27 - 0.22
    kind = c['kind']
    if kind == 'dual':
        half = (w - 0.2) / 2
        for k, (sub, xx, col, fmt) in enumerate([(c['left'], x, NAVY, '#,##0'), (c['right'], x + half + 0.2, TEAL, '#,##0')]):
            cd = CategoryChartData()
            cd.categories = sub['cats']
            for name, vals in sub['series']:
                cd.add_series(name, vals)
            gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, E(xx), E(cy), E(half), E(ch), cd)
            gf.name = f'Chart {k+1}'
            ch_ = gf.chart
            style_chart(ch_, S, False)
            axes(ch_, S, vmax=max(sub['series'][0][1]) * 1.18)
            pl = ch_.plots[0]
            pl.gap_width = 60
            pl.series[0].format.fill.solid()
            pl.series[0].format.fill.fore_color.rgb = rgb(col)
            labels(pl, S, fmt, pos=XL_LABEL_POSITION.OUTSIDE_END, bold=True)
            no_invert(ch_)
    elif kind == 'donut':
        cd = CategoryChartData()
        cd.categories = c['cats']
        cd.add_series(*c['series'][0])
        gf = slide.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, E(x), E(cy), E(w * 0.55), E(ch), cd)
        gf.name = 'Chart'
        ch_ = gf.chart
        style_chart(ch_, S, True)
        ch_.legend.position = XL_LEGEND_POSITION.RIGHT
        pl = ch_.plots[0]
        for i, col in enumerate([NAVY, LTEAL]):
            pt = pl.series[0].points[i]
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = rgb(col)
        labels(pl, S, '0"%"', color='FFFFFF', bold=True)
        # side facts
        tf = textbox(slide, x + w * 0.58, cy + 0.15, w * 0.42, ch - 0.2, 'Chart side facts')
        facts = [('$608m', 'B2B revenue FY25'), ('82% / 18%', 'subscription / transactional'), ('79% / 21%', 'US / international'), ('~10%', 'share of $6bn core market')]
        for i, (a, l) in enumerate(facts):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            if i:
                p.space_before = Pt(4)
            run(p, a + '  ', BOLD, S['body'] + 1, NAVY, bold=True)
            run(p, l, LIGHT, S['body'] - 0.5, MUTED)
    else:
        cd = CategoryChartData()
        cd.categories = c['cats']
        for name, vals in c['series']:
            cd.add_series(name, vals)
        if kind == 'stacked100':
            ctype = XL_CHART_TYPE.BAR_STACKED_100
        elif kind in ('bar', 'bar_target'):
            ctype = XL_CHART_TYPE.COLUMN_CLUSTERED
        gf = slide.shapes.add_chart(ctype, E(x), E(cy), E(w), E(ch), cd)
        gf.name = 'Chart'
        ch_ = gf.chart
        pl = ch_.plots[0]
        if kind == 'stacked100':
            style_chart(ch_, S, True)
            axes(ch_, S)
            ch_.category_axis.reverse_order = True
            pl.gap_width = 45
            pl.overlap = 100
            for ser, col in zip(pl.series, [NAVY, AMBER]):
                ser.format.fill.solid()
                ser.format.fill.fore_color.rgb = rgb(col)
            labels(pl, S, '0"%"', color='FFFFFF', pos=XL_LABEL_POSITION.CENTER, bold=True)
        else:
            style_chart(ch_, S, False)
            vals = c['series'][0][1]
            axes(ch_, S, vmax=max(vals) * 1.2)
            pl.gap_width = 70
            ser = pl.series[0]
            ser.format.fill.solid()
            ser.format.fill.fore_color.rgb = rgb(GREY)
            fmt = '#,##0'
            labels(pl, S, fmt, pos=XL_LABEL_POSITION.OUTSIDE_END, bold=True)
            for i in range(len(vals)):
                pt = ser.points[i]
                pt.format.fill.solid()
                if kind == 'bar_target' and i == len(vals) - 1:
                    pt.format.fill.fore_color.rgb = rgb('FFFFFF')
                    pt.format.line.color.rgb = rgb(TEAL)
                    pt.format.line.width = Pt(1.25)
                    pt.format.line.dash_style = 4  # dash
                elif i == 0 or kind == 'bar_target':
                    pt.format.fill.fore_color.rgb = rgb(NAVY if kind == 'bar' else TEAL)
                else:
                    pt.format.fill.fore_color.rgb = rgb(GREY)
        no_invert(ch_)
    tf = textbox(slide, x, y + h - 0.2, w, 0.2, 'Chart note')
    run(tf.paragraphs[0], c['note'], LIGHT, 7.5, MUTED, italic=True)


def est_lines(text, width_in, size, bold=False):
    """Rough line count: ~130/size chars per inch for Light, 10% fewer for Bold (conservative for QA fonts)."""
    cpi = 140.0 / size * (0.9 if bold else 1.0)
    per = max(1, int(width_in * cpi))
    words, lines, cur = text.split(), 1, 0
    for wd in words:
        if cur + len(wd) + (1 if cur else 0) > per:
            lines, cur = lines + 1, len(wd)
        else:
            cur += len(wd) + (1 if cur else 0)
    return lines


def add_table(slide, b, S, x, y, w):
    """Returns the bottom y of the table (row heights sized to wrapped text)."""
    t = b['table']
    tf = textbox(slide, x, y, w, 0.24, 'Table title')
    run(tf.paragraphs[0], t['title'], BOLD, S['sec'] - 0.5, NAVY, bold=True)
    rows, cols = len(t['rows']) + 1, len(t['cols'])
    widths = t.get('widths', [0.31, 0.32, 0.37])
    line_h = S['table'] * 1.22 / 72
    heights = []
    for i in range(rows):
        vals = t['cols'] if i == 0 else t['rows'][i - 1]
        n = max(est_lines(vals[j], w * widths[j] - 0.1, S['table'], bold=(i == 0 or j == 0)) for j in range(cols))
        heights.append(n * line_h + 0.05)
    gf = slide.shapes.add_table(rows, cols, E(x), E(y + 0.26), E(w), E(sum(heights)))
    gf.name = 'Table'
    tbl = gf.table
    for j in range(cols):
        tbl.columns[j].width = E(w * widths[j])
    for i in range(rows):
        tbl.rows[i].height = E(heights[i])
        vals = t['cols'] if i == 0 else t['rows'][i - 1]
        for j in range(cols):
            cell = tbl.cell(i, j)
            cell.margin_left = cell.margin_right = E(0.05)
            cell.margin_top = cell.margin_bottom = E(0.01)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(NAVY if i == 0 else ('FFFFFF' if i % 2 else PANEL))
            tfc = cell.text_frame
            tfc.word_wrap = True
            p = tfc.paragraphs[0]
            if i == 0:
                run(p, vals[j], BOLD, S['table'], 'FFFFFF', bold=True)
            else:
                run(p, vals[j], BOLD if j == 0 else LIGHT, S['table'], NAVY if j == 0 else TXT, bold=(j == 0))
    tblPr = tbl._tbl.tblPr
    tblPr.set('firstRow', '1')
    tblPr.set('bandRow', '0')
    return y + 0.26 + sum(heights)


def quotes_height(b, v, w, qsize, asize):
    h = 0.08 + (S_SEC := 0.24)
    for qt, who in b['quotes'][v]:
        n = est_lines('\u201c' + qt + '\u201d  — ' + who, w - 0.3, qsize)
        h += n * qsize * 1.22 / 72 + 0.06
    return h + 0.06


def add_quotes(slide, b, v, S, x, y, w, h):
    qs, ats = S['quote'], S['attr']
    while quotes_height(b, v, w, qs, ats) > h and qs > 7.5:
        qs, ats = qs - 0.5, ats - 0.5
    rect(slide, x, y, w, h, PANEL, 'Quotes panel')
    tf = textbox(slide, x + 0.15, y + 0.08, w - 0.3, h - 0.12, 'Quotes')
    p = tf.paragraphs[0]
    run(p, 'Outlook, quality & risks: in their words' if v == 'pres' else 'Verbatim evidence', BOLD, S['sec'] - 0.5, TEAL, bold=True)
    for qt, who in b['quotes'][v]:
        p = tf.add_paragraph()
        p.space_before = Pt(4 if v == 'pres' else 3)
        run(p, '\u201c' + qt + '\u201d', LIGHT, qs, TXT, italic=True)
        run(p, '  — ' + who, BOLD, ats, MUTED, bold=True)
    return qs


def left_height(b, v, S):
    h = 0
    for k, (hdr, items) in enumerate(b['sections'][v]):
        h += (S['sec'] * 1.25 / 72) + (0.1 if k else 0)
        for it in items:
            h += est_lines(it, LW - 0.2, S['body']) * S['body'] * 1.2 / 72 + 0.03
    return h


def add_quote_cards(slide, b, v, S):
    qs = b['quotes'][v]
    n, gap, h = len(qs), 0.15, FOOT_Y - 0.08 - QY
    w = (W - gap * (n - 1)) / n
    size = S['quote']
    def need(sz):
        return max(est_lines('\u201c' + q + '\u201d', w - 0.28, sz) * sz * 1.2 / 72 + est_lines(a, w - 0.28, sz - 1.5, True) * (sz - 1.5) * 1.2 / 72 for q, a in qs) + 0.2
    while need(size) > h and size > 8:
        size -= 0.5
    if need(size) > h:
        print(f"  WARN {v} {b['key']}: quotes need {need(size):.2f} > {h:.2f}")
    for i, (q, a) in enumerate(qs):
        x = M + i * (w + gap)
        rect(slide, x, QY, w, h, PANEL, f'Quote card {i+1}')
        tf = textbox(slide, x + 0.14, QY + 0.08, w - 0.28, h - 0.12, f'Quote {i+1}')
        run(tf.paragraphs[0], '\u201c' + q + '\u201d', LIGHT, size, TXT, italic=True)
        p = tf.add_paragraph()
        p.space_before = Pt(3)
        run(p, a, BOLD, size - 1.5, TEAL, bold=True)


def footer(slide, b, v, idx, n):
    tf = textbox(slide, M, FOOT_Y, W - 0.6, 0.38, 'Sources')
    run(tf.paragraphs[0], 'Sources: ', BOLD, 7.5, MUTED, bold=True)
    txt = b['sources']
    if v == 'int':
        txt += '  Tags: [D] filing, [D-deck] Investor Day deck (unaudited), [IR] management, [X] AlphaSense expert call (unaudited), [3P] third party, [C] arithmetic on disclosed data.'
    run(tf.paragraphs[0], txt, LIGHT, 7.5, MUTED)
    tf = textbox(slide, 13.333 - M - 0.5, FOOT_Y, 0.5, 0.2, 'Page')
    tf.paragraphs[0].alignment = PP_ALIGN.RIGHT
    run(tf.paragraphs[0], f'{idx}', LIGHT, 8, MUTED)


def build(v, out):
    prs = Presentation()
    prs.slide_width, prs.slide_height = E(13.333), E(7.5)
    blank = prs.slide_layouts[6]
    S = SIZES[v]
    for i, b in enumerate(BUSINESSES, 1):
        s = prs.slides.add_slide(blank)
        header(s, b, v, S)
        stats(s, b, S)
        left_column(s, b, v, S)
        # right column: chart, table, quotes
        ch_h = 1.55
        add_chart(s, b, S, RX, TOP, RW, ch_h)
        ty = add_table(s, b, S, RX, TOP + ch_h + 0.06, RW)
        if ty > QY - 0.1:
            print(f"  WARN {v} {b['key']}: table bottom {ty:.2f} > {QY - 0.1:.2f}")
        lh = left_height(b, v, S)
        if TOP + lh > QY - 0.1:
            print(f"  WARN {v} {b['key']}: left text est. bottom {TOP + lh:.2f}")
        add_quote_cards(s, b, v, S)
        footer(s, b, v, i, len(BUSINESSES))
        notes = s.notes_slide.notes_text_frame
        notes.text = (f"{b['kicker']}. Sources: {b['sources']} Full citations with page numbers and timestamped links: "
                      f"work/research_notes/slides/{b['key']}.md")
    prs.core_properties.title = 'Mobility Global: business lines' + (' (internal research)' if v == 'int' else '')
    prs.core_properties.author = 'MBGL research'
    prs.save(out)
    print('saved', out)


if __name__ == '__main__':
    build('pres', f'{ROOT}/deliverables/MBGL_Business_Lines_Presentation.pptx')
    build('int', f'{ROOT}/deliverables/MBGL_Business_Lines_Internal.pptx')
