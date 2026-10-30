"""MBGL medium/long-term growth, margin and FCF outlook: chart-ready workbook.
Blue = input, black = formula, green = cross-sheet link. Tiers: [D] disclosed, [IR] management, [C] computed, [E] estimate."""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.chart import BarChart, LineChart, ScatterChart, Reference, Series

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f'{W}/deliverables/MBGL_Growth_Margin_Outlook.xlsx'

NAVY, SEC = '1F3864', 'D9E1F2'
F = lambda **k: Font(**{'name': 'Arial', 'size': 10, **k})
HDR_FONT, HDR_FILL = F(bold=True, color='FFFFFF'), PatternFill('solid', fgColor=NAVY)
SEC_FILL = PatternFill('solid', fgColor=SEC)
BLUE, BLACK, GREEN = F(color='0000FF'), F(color='000000'), F(color='008000')
BOLD = F(bold=True)
THIN = Border(top=Side(style='thin'))
MONEY, PCT, PT = '#,##0;(#,##0);"-"', '0.0%', '0.0" pt";(0.0" pt");"-"'

wb = Workbook()


def sheet(name, title, widths):
    ws = wb.create_sheet(name)
    ws['A1'] = title; ws['A1'].font = F(bold=True, size=13, color=NAVY)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[L(i)].width = w
    ws.sheet_view.showGridLines = False
    return ws


def header(ws, r, labels):
    for i, v in enumerate(labels, 1):
        c = ws.cell(r, i, v); c.font = HDR_FONT; c.fill = HDR_FILL
        c.alignment = Alignment(horizontal='center' if i > 1 else 'left', wrap_text=True, vertical='center')


def section(ws, r, text, ncol):
    for i in range(1, ncol + 1):
        ws.cell(r, i).fill = SEC_FILL
    ws.cell(r, 1, text).font = BOLD


def put(ws, r, c, v, font=BLACK, fmt=None, bold=False):
    cell = ws.cell(r, c, v)
    cell.font = Font(name='Arial', size=10, color=font.color, bold=bold)
    if fmt: cell.number_format = fmt
    return cell


# ---------------------------------------------------------------- Notes
ws = sheet('Notes', 'MBGL: medium/long-term growth, margin & FCF outlook (chart data)', [110])
notes = [
    'Purpose: chart-ready tables for the medium-term (2028-30) and long-term (2030+) outlook. Every table is laid out as a clean block (labels in column A, series in columns) so Excel charts can be built directly from it; ready-made charts are on the "Charts" tab.',
    'Colour code: blue = input/assumption (change freely), black = formula, green = link to another tab.',
    'Tiers: [D] disclosed in filings; [IR] management statement (Investor Day 12-May-26, Q2-26 call 7-Aug-26, Goldman Sachs conference 10-Sep-26); [C] computed; [E] analyst estimate (inference, not guidance).',
    'What management has guided: only the group medium-term framework (7.5-10% organic, core 5-7% "majority in value" + new products 1-2% + international 1-2%; 50bp+ annual margin expansion from 2028; 8-11% Adj. EBITDA growth; 25-27% medium-term effective tax rate; SBC 3-4% of revenue; capex "relatively low"; 75%+ of FCF returned; ~2.5x gross leverage). No segment targets and nothing beyond ~2030.',
    'Segment driver splits (CARFAX, B2B), the 2026-2040 projection and long-run margins are [E]. Price evidence: Q2-26 10-Q "price increases of approximately $16 million and $36 million" (Q2/6M) vs new business ~$8m/$20m [D]; CARFAX subscription growth "primarily driven by price increases", B2B "primarily due to continued new business growth" [D].',
    'Adjusted EBITDA adds back stock-based compensation (SBC). "After SBC" rows treat SBC as a real cost.',
    'Cash tax = ETR x (EBITDA - one-offs - SBC - depreciation - interest) + (cash-tax gap $89m - ETR x $296m non-deductible IHS Markit deal amortization) while the amortization lasts (to 2037). The $89m is cash tax above the book provision (CFO); it is a book/cash difference, so cash tax does not fall when it ends.',
    'Peer metrics on the Peers tab are approximate from general knowledge and NOT verified against filings in this project; replace before external use.',
    'FY23-25 actuals: Form 10/A carve-out [D]. IHS Markit Transportation FY14-21: IHS Markit 10-Ks [D] (Nov FYE; includes Maritime & Trade; not comparable with the carve-out).',
]
for i, n in enumerate(notes, 3):
    c = ws.cell(i, 1, n); c.font = BLACK; c.alignment = Alignment(wrap_text=True, vertical='top')
    ws.row_dimensions[i].height = 42

# ---------------------------------------------------------------- 1 Group framework
ws = sheet('Group Framework', 'Group medium-term growth framework (2028+, "target range every year") [IR]', [34, 10, 10, 10, 70])
header(ws, 3, ['Component (% organic growth p.a.)', 'Low', 'High', 'Mid', 'Management statement / source'])
rows = [('Core (price/value + volume)', .05, .07, '"the 5%-7% revenue growth visibility that we typically have every year"; "value plus volume ... the majority of that is in value" (CFO, Investor Day)'),
        ('New products', .01, .02, 'Listings/Showroom, CARFAX for Life, Data Studio/FAST/PIQ, AI products (GS conference)'),
        ('International', .01, .02, 'Canada largest; Germany/Italy/Spain/Poland; Chinese OEMs; India. "More mid-to-long term" (GS conference)')]
r = 4
for lab, lo, hi, src in rows:
    put(ws, r, 1, lab); put(ws, r, 2, lo, BLUE, PCT); put(ws, r, 3, hi, BLUE, PCT)
    put(ws, r, 4, f'=AVERAGE(B{r}:C{r})', BLACK, PCT); put(ws, r, 5, src)
    r += 1
put(ws, r, 1, 'Sum of components', bold=True)
for c in (2, 3, 4):
    put(ws, r, c, f'=SUM({L(c)}4:{L(c)}{r-1})', BLACK, PCT, bold=True).border = THIN
put(ws, r, 5, 'Components sum to 7-11%; management states the total as 7.5-10%')
r += 1
put(ws, r, 1, 'Stated organic revenue target', bold=True); put(ws, r, 2, .075, BLUE, PCT); put(ws, r, 3, .10, BLUE, PCT)
put(ws, r, 4, f'=AVERAGE(B{r}:C{r})', BLACK, PCT); put(ws, r, 5, '"We are targeting 7.5%-10% organic growth in the medium term"; medium term = "2028 and beyond" (CFO)')
r += 1
put(ws, r, 1, 'Organic Adj. EBITDA growth target', bold=True); put(ws, r, 2, .08, BLUE, PCT); put(ws, r, 3, .11, BLUE, PCT)
put(ws, r, 4, f'=AVERAGE(B{r}:C{r})', BLACK, PCT); put(ws, r, 5, '"8% to 11% annual organic adjusted EBITDA growth" (CFO)')
r += 1
put(ws, r, 1, 'Annual Adj. EBITDA margin expansion'); put(ws, r, 2, .005, BLUE, '0.0%'); put(ws, r, 5, '"50 basis point margin expansion or more" after the reset; full 50bp "not ... until 2028" (CFO)')

r += 3
section(ws, r, 'Long-term opportunity statements [IR] ($m unless stated)', 5); r += 1
header(ws, r, ['Opportunity', 'Today', 'Target / size', 'Today as % of target', 'Statement']); r += 1
opp = [('B2B addressable market ($m)', 600, 18000, 'B2B >$600m revenue; "$6 billion addressable market, about 10% market share ... path to an $18 billion opportunity" (LaFeir)'),
       ('US listings market ($m; CARFAX share <10%)', 300, 3000, '"north of $3 billion ... not even at 10% of that yet" (Eager, GS). Today = 10% ceiling'),
       ('CARFAX for Life, US & Canada ($m)', 53, 150, '"His goal in the U.S. and Canada is not $53 million, it\'s $150 million" (Eager)'),
       ('CARFAX for Life, global ($m)', 53, 1000, '"... and it\'s $1 billion globally" (Eager)')]
for lab, a, b, s in opp:
    put(ws, r, 1, lab); put(ws, r, 2, a, BLUE, MONEY); put(ws, r, 3, b, BLUE, MONEY)
    put(ws, r, 4, f'=B{r}/C{r}', BLACK, PCT); put(ws, r, 5, s); r += 1


# ---------------------------------------------------------------- 2/3 Segment drivers
def drivers(name, title, rows, note):
    ws = sheet(name, title, [40, 9, 9, 9, 9, 9, 9, 9, 75])
    header(ws, 3, ['Driver (pt of segment growth p.a.) [E]', 'MT low', 'MT mid', 'MT high', 'LT low', 'LT mid', 'LT high', 'Price? (1=yes)', 'Basis'])
    r = 4
    for lab, mt, lt, pr, basis in rows:
        put(ws, r, 1, lab)
        for j, v in enumerate(mt + lt):
            put(ws, r, 2 + j, v, BLUE, PT)
        put(ws, r, 8, pr, BLUE, '0'); put(ws, r, 9, basis)
        r += 1
    last = r - 1
    put(ws, r, 1, 'Segment growth (sum of drivers)', bold=True)
    for c in range(2, 8):
        put(ws, r, c, f'=SUM({L(c)}4:{L(c)}{last})', BLACK, PT, bold=True).border = THIN
    put(ws, r, 9, 'Low/high totals are extreme cases (every driver at its low/high); use the mid case')
    tot = r; r += 1
    put(ws, r, 1, 'of which price (pt)')
    for c in range(2, 8):
        put(ws, r, c, f'=SUMPRODUCT({L(c)}4:{L(c)}{last},$H$4:$H${last})', BLACK, PT)
    pr_r = r; r += 1
    put(ws, r, 1, 'of which volume / other (pt)')
    for c in range(2, 8):
        put(ws, r, c, f'={L(c)}{tot}-{L(c)}{pr_r}', BLACK, PT)
    r += 1
    put(ws, r, 1, 'Price share of segment growth', bold=True)
    for c in range(2, 8):
        put(ws, r, c, f'=IF({L(c)}{tot}=0,0,{L(c)}{pr_r}/{L(c)}{tot})', BLACK, PCT, bold=True)
    r += 2
    put(ws, r, 1, note).alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9); ws.row_dimensions[r].height = 45
    return ws, tot, pr_r


cf_rows = [
    ('Price / value on existing dealer base', (4, 5, 6), (4, 4.5, 5), 1, '10-Q: CARFAX subscription growth "primarily driven by price increases" [D]; 6M-26 company price ~$36m = at most ~6% of CARFAX revenue [C]; "report as % of car price continues to decline" (Fredericks)'),
    ('Dealer count (rooftops)', (0, 0.5, 1), (0, 0, 0.5), 0, 'Franchise "highly pinned"; ~40k US dealers; small-independent churn and AutoCheck switching (expert calls, D16)'),
    ('Products per dealer (attach / upsell)', (1, 1.5, 2), (0.5, 1, 1.5), 0, '"Most dealers are only on 1.5 products ... three or four or five" (Fredericks)'),
    ('Listings & Showroom', (1, 1.5, 2), (1, 1, 2), 0, '<10% share of a >$3bn US market; "more immediate" 12-18 month lever (Eager, GS)'),
    ('International (Canada, Europe)', (0.5, 1, 2), (0.5, 1, 3), 0, 'Germany launched Jul-26, plus Italy/Spain; global opportunity large but unproven'),
    ('Insurers & lenders (per-VIN)', (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), 0, 'Per-VIN pricing up 3-8% (experts); underwriting volumes cyclical'),
]
drivers('CARFAX Drivers', 'CARFAX: medium-term (2028-30) and long-term (2030+) growth drivers [E]', cf_rows,
        'Required growth: with B2B at 4-6% and ~35% of revenue, CARFAX must grow ~9-12% for the group to reach 7.5-10% [C]. History [D]: FY24 +12%, FY25 +10%, Q2-26 +8%. Analogue: Auto Trader UK, where flat retailer count and ~6-8% ARPR growth drive almost all growth (approximate, not verified).')

b2b_rows = [
    ('Price / escalators', (1, 1.5, 2), (1, 1.5, 2), 1, 'Never disclosed; planning competitor is a "low-cost alternative" (LaFeir), so inflation-type pricing assumed'),
    ('New business / penetration', (1.5, 2, 3), (1, 1.5, 2), 0, '10-Q: B2B growth "primarily due to continued new business growth" [D]; "<50% penetrated" with top-40 OEMs (Eager)'),
    ('automotiveMastermind', (0.5, 1, 1.5), (0.5, 0.5, 1), 0, '"Growing at double digits" (LaFeir); 3,200 dealers'),
    ('New products (FAST, PIQ, Data Studio)', (0, 0.5, 1), (0.5, 1, 2), 0, 'All "in their early stages" (Eager, GS)'),
    ('International (Chinese OEMs, India)', (0, 0.5, 1), (0.5, 0.5, 1), 0, 'Investor Day strategy'),
    ('Recall / transactional', (-1, -0.5, 0), (-0.5, 0, 0.5), 0, 'Recall the "one minor exception" to growth (CFO); planning projects cyclical (Q2-26)'),
]
drivers('B2B Drivers', 'B2B: medium-term (2028-30) and long-term (2030+) growth drivers [E]', b2b_rows,
        'History [D]: FY24 +3%, FY25 +6%, Q1-26 +8%, Q2-26 +4% (subscription +6%, transactional -4%). Growth above ~6% would require the "$18bn opportunity" to convert; nothing in the record shows it yet.')

# ---------------------------------------------------------------- Projection (assumptions + segment + margin + FCF)
YEARS = list(range(2023, 2041))
NY = len(YEARS)
C0 = 2  # first year column
col = {y: C0 + i for i, y in enumerate(YEARS)}
ws = sheet('Projection', 'Segment revenue, margin and FCF projection, FY2023A-FY2040E ($m) [A = actual, E = estimate]', [44] + [9] * NY + [60])
SRC = C0 + NY
header(ws, 3, ['$m'] + [f'FY{y}{"A" if y <= 2025 else "E"}' for y in YEARS] + ['Basis'])
R = {}
r = 4


def row(key, label, vals=None, fmt=MONEY, font=BLACK, bold=False, basis='', formula=None):
    """vals: dict year->value (inputs); formula: f(year)->str. Missing years blank."""
    global r
    R[key] = r
    put(ws, r, 1, label, bold=bold)
    for y in YEARS:
        c = col[y]
        if vals is not None and y in vals and vals[y] is not None:
            put(ws, r, c, vals[y], font if formula is None or y <= 2025 else font, fmt, bold)
        elif formula is not None:
            f = formula(y)
            if f is not None:
                put(ws, r, c, f, BLACK, fmt, bold)
    if basis: put(ws, r, SRC, basis).alignment = Alignment(wrap_text=False)
    R[key] = r; r += 1


def ref(key, y, absolute=False):
    return f'{L(col[y])}{R[key]}'


def prev(y): return y - 1


section(ws, r, 'Assumptions (blue = change freely)', SRC); r += 1
cf_g = {2026: .085, 2027: .09, 2028: .10, 2029: .10, 2030: .10}
for i, y in enumerate(range(2031, 2036)): cf_g[y] = round(.10 - .004 * (i + 1), 4)
for y in range(2036, 2041): cf_g[y] = .08
b2b_g = {y: .05 for y in range(2026, 2041)}
cf_p = {2026: .06, 2027: .05, 2028: .05, 2029: .05, 2030: .05}
for y in range(2031, 2041): cf_p[y] = .045
b2b_p = {y: .015 for y in range(2026, 2041)}
mg = {2026: .401, 2027: .395, 2028: .400, 2029: .405, 2030: .410}
for i, y in enumerate(range(2031, 2036)): mg[y] = round(.410 + .006 * (i + 1), 4)
for i, y in enumerate(range(2036, 2041)): mg[y] = round(.440 + .004 * (i + 1), 4)
sbc = {2026: .019, 2027: .030}
for y in range(2028, 2041): sbc[y] = .035
etr = {2026: .2925, 2027: .28, 2028: .27}
for y in range(2029, 2041): etr[y] = .26
row('cf_g', 'CARFAX organic growth', {y: v for y, v in cf_g.items()}, PCT, BLUE, basis='[E] FY26 from guidance mid; 2028-30 = CARFAX Drivers MT mid; fades to LT mid (8%)')
row('b2b_g', 'B2B organic growth', b2b_g, PCT, BLUE, basis='[E] B2B Drivers MT/LT mid (~5%)')
row('cf_p', 'CARFAX price contribution (pt)', cf_p, PCT, BLUE, basis='[E] FY26 ~6% upper bound from 10-Q price $; then CARFAX Drivers price row')
row('b2b_p', 'B2B price contribution (pt)', b2b_p, PCT, BLUE, basis='[E] B2B Drivers price row')
row('mg', 'Group Adj. EBITDA margin', {2023: None, **mg}, PCT, BLUE, basis='[IR] FY26 guide mid ~40.1%; FY27 39.5% (FY25 40.6% - 150bp standalone + efficiency); +50bp/yr 2028-30 [IR]; +60bp/yr 2031-35, +40bp/yr 2036-40 [E]')
row('sbc', 'SBC % of revenue', sbc, PCT, BLUE, basis='[IR] ~1% rising to 3-4%; FY26 = H1 actual $9m + H2 ramp [E]')
row('etr', 'Effective tax rate', etr, PCT, BLUE, basis='[IR] FY26 GAAP 28-30.5%; medium-term 25-27% (CFO, Investor Day)')
row('capex_pct', 'Recurring capex % of revenue', {y: .014 for y in range(2026, 2041)}, PCT, BLUE, basis='[D] FY23-25 0.9-1.4%; "relatively low" [IR]')
row('dep_pct', 'Tax-deductible depreciation % of revenue', {y: .008 for y in range(2026, 2041)}, PCT, BLUE, basis='[D] FY25 depreciation $14m')
row('wc_pct', 'Working capital inflow % of revenue increase', {y: .10 for y in range(2026, 2041)}, PCT, BLUE, basis='[C] deferred-revenue inflow; FY25 ~$23m on +$137m revenue')
row('lev', 'Gross leverage (Debt / Adj. EBITDA)', {y: 2.5 for y in range(2028, 2041)}, '0.0"x"', BLUE, basis='[IR] target ~2.5x gross; FY26-27 = $2.0bn bonds (non-prepayable)')
row('rate', 'Cash interest rate on debt', {y: .056 for y in range(2028, 2041)}, PCT, BLUE, basis='[D] 5.74% weighted incl. fee amortization; ~5.6% cash coupon [E]')
row('amort', 'Non-deductible deal amortization', {y: (296 if y <= 2037 else 0) for y in range(2026, 2041)}, MONEY, BLUE, basis='[D] FY25 amortization of intangibles $296m; ~12 years from 2026 [IR]')
row('gap', 'Cash tax above book provision', {y: (89 if y <= 2037 else 0) for y in range(2026, 2041)}, MONEY, BLUE, basis='[IR] "for the next 12 years, cash taxes will be approximately $89 million higher than our tax provision"')

r += 1
section(ws, r, 'Segment revenue', SRC); r += 1
row('cf_rev', 'CARFAX revenue', {2023: 928, 2024: 1039, 2025: 1142}, MONEY, BLUE,
    formula=lambda y: f'={ref("cf_rev", y-1)}*(1+{ref("cf_g", y)})' if y > 2025 else None, basis='[D] Form 10/A FY23-25')
row('b2b_rev', 'B2B revenue', {2023: 557, 2024: 574, 2025: 608}, MONEY, BLUE,
    formula=lambda y: f'={ref("b2b_rev", y-1)}*(1+{ref("b2b_g", y)})' if y > 2025 else None, basis='[D] Form 10/A FY23-25')
row('rev', 'Group revenue', formula=lambda y: f'={ref("cf_rev", y)}+{ref("b2b_rev", y)}', bold=True, basis='[C]')
row('rev_g', 'Group revenue growth', formula=lambda y: f'={ref("rev", y)}/{ref("rev", y-1)}-1' if y > 2023 else None, fmt=PCT, basis='[C]')
row('cf_g_act', 'CARFAX growth (actual / assumed)', formula=lambda y: f'={ref("cf_rev", y)}/{ref("cf_rev", y-1)}-1' if y > 2023 else None, fmt=PCT, basis='[C]')
row('b2b_g_act', 'B2B growth (actual / assumed)', formula=lambda y: f'={ref("b2b_rev", y)}/{ref("b2b_rev", y-1)}-1' if y > 2023 else None, fmt=PCT, basis='[C]')
row('cf_share', 'CARFAX share of revenue', formula=lambda y: f'={ref("cf_rev", y)}/{ref("rev", y)}', fmt=PCT, basis='[C]')
row('b2b_share', 'B2B share of revenue', formula=lambda y: f'={ref("b2b_rev", y)}/{ref("rev", y)}', fmt=PCT, basis='[C]')
row('price_pt', 'Group growth from price (pt)', formula=lambda y: f'={ref("cf_p", y)}*{ref("cf_rev", y-1)}/{ref("rev", y-1)}+{ref("b2b_p", y)}*{ref("b2b_rev", y-1)}/{ref("rev", y-1)}' if y > 2025 else None, fmt=PCT, basis='[C] segment price pt weighted by prior-year mix')
row('vol_pt', 'Group growth from volume / other (pt)', formula=lambda y: f'={ref("rev_g", y)}-{ref("price_pt", y)}' if y > 2025 else None, fmt=PCT, basis='[C]')
row('price_share', 'Price share of group growth', formula=lambda y: f'={ref("price_pt", y)}/{ref("rev_g", y)}' if y > 2025 else None, fmt=PCT, basis='[C] H1-26 actual ~56% [D/C]')

r += 1
section(ws, r, 'Margins', SRC); r += 1
row('ebitda', 'Adj. EBITDA', {2023: 598, 2024: 658, 2025: 711}, MONEY, BLUE,
    formula=lambda y: f'={ref("rev", y)}*{ref("mg", y)}' if y > 2025 else None, bold=True, basis='[D] FY23-25; FY26 guide mid $752.5m')
row('mg_act', 'Adj. EBITDA margin', formula=lambda y: f'={ref("ebitda", y)}/{ref("rev", y)}', fmt=PCT, basis='[C]')
row('sbc_d', 'Stock-based compensation', {2023: 20, 2024: 28, 2025: 22}, MONEY, BLUE,
    formula=lambda y: f'={ref("rev", y)}*{ref("sbc", y)}' if y > 2025 else None, basis='[D] FY23-25 cash flow statement')
row('mg_sbc', 'Adj. EBITDA margin after SBC', formula=lambda y: f'=({ref("ebitda", y)}-{ref("sbc_d", y)})/{ref("rev", y)}', fmt=PCT, basis='[C]')
row('cf_seg_mg', 'CARFAX segment Adj. EBITDA margin', {2023: 422 / 928, 2024: 476 / 1039, 2025: 536 / 1142}, PCT, BLUE, basis='[D/C] segment Adj. EBITDA 422/476/536')
row('b2b_seg_mg', 'B2B segment Adj. EBITDA margin', {2023: 191 / 557, 2024: 203 / 574, 2025: 197 / 608}, PCT, BLUE, basis='[D/C] segment Adj. EBITDA 191/203/197')

r += 1
section(ws, r, 'Cash flow (FY23-25 actual bridge; FY26+ estimate)', SRC); r += 1
row('oneoff', 'One-offs, expensed', {2023: -30, 2024: -23, 2025: -40, 2026: -25, 2027: -25}, MONEY, BLUE,
    formula=lambda y: '=0' if y > 2027 else None, basis='[D] FY23-25; FY26-27 = 50% expensed x ~$50m/yr of ~$100m spin cost [IR]')
row('debt', 'Gross debt (year end)', {2026: 2000, 2027: 2000}, MONEY, BLUE,
    formula=lambda y: f'=MAX(2000,{ref("lev", y)}*{ref("ebitda", y)})' if y > 2027 else None, basis='[D] $2.0bn senior notes; then leverage x EBITDA (buybacks funded)')
row('int', 'Cash interest', {2023: -17, 2024: -15, 2025: -13, 2026: -65, 2027: -112}, MONEY, BLUE,
    formula=lambda y: f'=-{ref("rate", y)}*{ref("debt", y)}' if y > 2027 else None, basis='[D] FY23-25 related-party; FY26 ~$5m + $60m Q4 coupon [IR]; FY27 5.6% x $2.0bn')
row('tax', 'Cash taxes', {2023: -156, 2024: -178, 2025: -196}, MONEY, BLUE,
    formula=lambda y: (f'=-({ref("etr", y)}*({ref("ebitda", y)}+{ref("oneoff", y)}-{ref("sbc_d", y)}-{ref("dep_pct", y)}*{ref("rev", y)}+{ref("int", y)})'
                       f'+{ref("gap", y)}-{ref("etr", y)}*{ref("amort", y)})') if y > 2025 else None,
    basis='[D] FY23-25 current tax; FY26+: ETR x tax base + ($89m gap - ETR x $296m amortization)')
row('capex', 'Capex, recurring', {2023: -18, 2024: -15, 2025: -24}, MONEY, BLUE,
    formula=lambda y: f'=-{ref("capex_pct", y)}*{ref("rev", y)}' if y > 2025 else None, basis='[D] FY23-25')
row('capex1', 'Capex, one-off (spin, capitalised)', {2023: 0, 2024: 0, 2025: 0, 2026: -25, 2027: -25}, MONEY, BLUE,
    formula=lambda y: '=0' if y > 2027 else None, basis='[IR] "roughly 50% of these one-time costs will be capitalized"')
row('wc', 'Working capital & other', {2023: 18 - 20, 2024: 13 - 28, 2025: 45 - 22}, MONEY, BLUE,
    formula=lambda y: f'={ref("wc_pct", y)}*({ref("rev", y)}-{ref("rev", y-1)})' if y > 2025 else None, basis='[D/C] reported "Other" less SBC add-back')
row('fcf', 'FCF before SBC', formula=lambda y: f'={ref("ebitda", y)}+{ref("oneoff", y)}+{ref("int", y)}+{ref("tax", y)}+{ref("capex", y)}+{ref("capex1", y)}+{ref("wc", y)}', bold=True, basis='[C] FY23-25 tie to reported CFO - capex: 375 / 412 / 461')
row('fcf_sbc', 'FCF after SBC', formula=lambda y: f'={ref("fcf", y)}-{ref("sbc_d", y)}', bold=True, basis='[C] SBC treated as a cash-equivalent cost')
row('fcf_rec', 'Recurring FCF after SBC (ex one-offs)', formula=lambda y: f'={ref("fcf_sbc", y)}-{ref("oneoff", y)}-{ref("capex1", y)}', basis='[C]')
row('fcf_m', 'FCF margin before SBC', formula=lambda y: f'={ref("fcf", y)}/{ref("rev", y)}', fmt=PCT, basis='[C]')
row('fcf_m_sbc', 'FCF margin after SBC', formula=lambda y: f'={ref("fcf_sbc", y)}/{ref("rev", y)}', fmt=PCT, basis='[C]')
row('fcf_conv', 'FCF after SBC / Adj. EBITDA', formula=lambda y: f'={ref("fcf_sbc", y)}/{ref("ebitda", y)}', fmt=PCT, basis='[C]')
row('chk', 'CHECK: FY23-25 FCF vs reported (375/412/461)', {}, MONEY,
    formula=lambda y: f'={ref("fcf", y)}-{ {2023: 375, 2024: 412, 2025: 461}[y]}' if y <= 2025 else None, basis='should be 0')
ws.cell(R['chk'], 1).font = F(italic=True, color='808080')
ws.freeze_panes = 'B4'
P = ws

# ---------------------------------------------------------------- Chart data (clean, contiguous blocks pulled from Projection)
ws = sheet('Chart Data', 'Chart-ready series (linked to Projection; green = link)', [36] + [9] * NY)
header(ws, 3, ['Series'] + [f'FY{y}' for y in YEARS])
CD = {}
cr = 4
blocks = [
    ('Revenue mix ($m)', [('CARFAX', 'cf_rev', MONEY), ('B2B', 'b2b_rev', MONEY)]),
    ('Growth (%)', [('Group', 'rev_g', PCT), ('CARFAX', 'cf_g_act', PCT), ('B2B', 'b2b_g_act', PCT)]),
    ('Group growth: price vs volume (pt)', [('Price', 'price_pt', PCT), ('Volume / other', 'vol_pt', PCT)]),
    ('Margins (%)', [('Adj. EBITDA margin', 'mg_act', PCT), ('Adj. EBITDA margin after SBC', 'mg_sbc', PCT), ('FCF margin before SBC', 'fcf_m', PCT), ('FCF margin after SBC', 'fcf_m_sbc', PCT)]),
    ('FCF ($m)', [('Adj. EBITDA', 'ebitda', MONEY), ('FCF before SBC', 'fcf', MONEY), ('FCF after SBC', 'fcf_sbc', MONEY)]),
]
for title, series in blocks:
    section(ws, cr, title, NY + 1); cr += 1
    for lab, key, fmt in series:
        put(ws, cr, 1, lab)
        for y in YEARS:
            put(ws, cr, col[y], f"=IF(Projection!{L(col[y])}{R[key]}=\"\",NA(),Projection!{L(col[y])}{R[key]})", GREEN, fmt)
        CD[key] = cr; cr += 1
    cr += 1
CDWS = ws

# ---------------------------------------------------------------- Peers
ws = sheet('Peers', 'Peer benchmarks: medium/long-term growth and margin (APPROXIMATE, not verified)', [30, 12, 26, 10, 10, 10, 12, 30, 52])
header(ws, 3, ['Company', 'Ticker', 'Group', 'Organic growth low', 'Organic growth high', 'Growth mid', 'EBITDA margin (approx.)', 'Price share of growth', 'Relevance'])
peers = [
    ('Mobility Global (target)', 'MBGL', 'Subject', .075, .10, .406, 'Majority (~55% H1-26)', 'Medium-term framework [IR]; FY25 margin [D]'),
    ('Auto Trader Group', 'AUTO LN', 'Dealer-pay marketplace', .07, .10, .70, 'High (ARPR-led)', 'Best analogue for mature CARFAX: flat retailer count, ARPR growth'),
    ('Verisk', 'VRSK', 'Data & analytics', .07, .08, .55, 'Mixed', 'Contributed data / insurance; data-margin ceiling'),
    ('CCC Intelligent Solutions', 'CCCS', 'Auto data & software', .07, .09, .41, 'Mixed (cross-sell)', 'Auto claims, insurers, repairers; B2B analogue'),
    ('Fair Isaac (Scores)', 'FICO', 'Data & analytics', .10, .12, .55, 'Very high', 'Limits of pricing power; regulatory backlash risk'),
    ('Experian', 'EXPN LN', 'Credit bureau', .05, .08, .37, 'Moderate', 'Owns AutoCheck; contributed-data economics'),
    ('Equifax', 'EFX', 'Credit bureau', .05, .08, .33, 'Moderate', 'Contributed-data economics'),
    ('TransUnion', 'TRU', 'Credit bureau', .05, .08, .36, 'Moderate', 'Contributed-data economics'),
    ('CarGurus', 'CARG', 'Dealer-pay marketplace', .03, .06, .30, 'Mixed', 'Competes for same US dealer budget'),
    ('Cars.com', 'CARS', 'Dealer-pay marketplace', .02, .05, .29, 'Mixed', 'Competes for same US dealer budget'),
    ('REA Group', 'REA AU', 'Dominant-brand marketplace', .08, .12, .57, 'High', 'Dominant-brand pricing benchmark'),
    ('Rightmove', 'RMV LN', 'Dominant-brand marketplace', .07, .10, .70, 'High', 'Dominant-brand pricing benchmark (operating margin)'),
]
for i, p in enumerate(peers, 4):
    name, tk, grp, lo, hi, m, ps, rel = p
    put(ws, i, 1, name, bold=(tk == 'MBGL')); put(ws, i, 2, tk); put(ws, i, 3, grp)
    put(ws, i, 4, lo, BLUE, PCT); put(ws, i, 5, hi, BLUE, PCT); put(ws, i, 6, f'=AVERAGE(D{i}:E{i})', BLACK, PCT)
    put(ws, i, 7, m, BLUE, PCT); put(ws, i, 8, ps); put(ws, i, 9, rel)
PEER_LAST = 3 + len(peers)
put(ws, PEER_LAST + 2, 1, 'Peer figures are approximate from general knowledge and NOT verified for this project. Auto Trader and Rightmove are operating margins. Replace with filed figures before external use.').font = F(italic=True, color='C00000')

# ---------------------------------------------------------------- History
ws = sheet('History', 'History: IHS Markit Transportation (FY14-21, Nov FYE) and Mobility carve-out (FY23-25) [D]', [26, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11])
header(ws, 3, ['$m', 'FY2014', 'FY2015', 'FY2016', 'FY2017', 'FY2018', 'FY2019', 'FY2020', 'FY2021', 'FY2023', 'FY2024', 'FY2025'])
hist_rev = [662.6, 758.4, 892.8, 991.6, 1160.2, 1246.1, 1151.6, 1354.4, 1485, 1613, 1750]
hist_e = [234.3, 282.7, 353.3, 408.6, 479.3, 520.9, 514.7, 645.0, 598, 658, 711]
put(ws, 4, 1, 'Revenue'); put(ws, 5, 1, 'Adj. EBITDA'); put(ws, 6, 1, 'Adj. EBITDA margin'); put(ws, 7, 1, 'Basis')
for j, (a, b) in enumerate(zip(hist_rev, hist_e)):
    c = 2 + j
    put(ws, 4, c, a, BLUE, MONEY); put(ws, 5, c, b, BLUE, MONEY); put(ws, 6, c, f'={L(c)}5/{L(c)}4', BLACK, PCT)
    put(ws, 7, c, 'IHS Transp.' if j < 8 else 'Carve-out')
put(ws, 9, 1, 'Not comparable across eras: IHS Markit segment EBITDA includes Maritime & Trade (~$100-145m revenue, moved to S&P Global Market Intelligence) and different cost allocations; FY22 (S&P Global, ~10 months) omitted. FY21 S&P Global pro forma Mobility: revenue $1,209m ($1,246m adjusted), adjusted operating profit $492m.').alignment = Alignment(wrap_text=True)
ws.merge_cells('A9:L9'); ws.row_dimensions[9].height = 45
HWS = ws

# ---------------------------------------------------------------- Charts
ws = sheet('Charts', 'Charts (all linked to the data tabs; edit blue inputs and they update)', [2])
X = Reference(CDWS, min_col=2, max_col=1 + NY, min_row=3)


def place(ch, anchor, title, ytitle=None, w=18, h=8.5):
    ch.title = title; ch.width = w; ch.height = h
    if ytitle: ch.y_axis.title = ytitle
    ch.y_axis.delete = False; ch.x_axis.delete = False
    ws.add_chart(ch, anchor)


def series_rows(ch, keys):
    for k in keys:
        ch.add_data(Reference(CDWS, min_col=1, max_col=1 + NY, min_row=CD[k]), from_rows=True, titles_from_data=True)
    ch.set_categories(X)


c1 = BarChart(); c1.type = 'col'; c1.grouping = 'stacked'; c1.overlap = 100
series_rows(c1, ['cf_rev', 'b2b_rev']); place(c1, 'B3', 'Revenue by segment, FY23A-FY40E ($m)', '$m')
c2 = LineChart(); series_rows(c2, ['rev_g', 'cf_g_act', 'b2b_g_act']); c2.y_axis.number_format = '0%'
place(c2, 'L3', 'Organic growth: group vs segments')
c3 = BarChart(); c3.type = 'col'; c3.grouping = 'stacked'; c3.overlap = 100
series_rows(c3, ['price_pt', 'vol_pt']); c3.y_axis.number_format = '0%'
place(c3, 'B21', 'Group growth split: price vs volume/other (FY26E+)')
c4 = LineChart(); series_rows(c4, ['mg_act', 'mg_sbc', 'fcf_m', 'fcf_m_sbc']); c4.y_axis.number_format = '0%'
place(c4, 'L21', 'Adj. EBITDA and FCF margins (before / after SBC)')
c5 = BarChart(); c5.type = 'col'; series_rows(c5, ['ebitda', 'fcf', 'fcf_sbc'])
place(c5, 'B39', 'Adj. EBITDA vs FCF ($m)', '$m')

# Driver stacks: MT mid vs LT mid for each segment
for k, (sname, anchor) in enumerate([('CARFAX Drivers', 'L39'), ('B2B Drivers', 'B57')]):
    sw = wb[sname]
    ch = BarChart(); ch.type = 'col'; ch.grouping = 'stacked'; ch.overlap = 100
    for rr in range(4, 10):  # one series per driver; categories = MT/LT low/mid/high
        ch.add_data(Reference(sw, min_col=1, max_col=7, min_row=rr), from_rows=True, titles_from_data=True)
    ch.set_categories(Reference(sw, min_col=2, max_col=7, min_row=3))
    place(ch, anchor, f'{sname.split()[0]}: growth drivers (pt), MT and LT low/mid/high')

c8 = BarChart(); c8.type = 'col'
c8.add_data(Reference(wb['Group Framework'], min_col=2, max_col=4, min_row=3, max_row=6), titles_from_data=True)
c8.set_categories(Reference(wb['Group Framework'], min_col=1, min_row=4, max_row=6)); c8.y_axis.number_format = '0%'
place(c8, 'L57', 'Group medium-term framework by component [IR]')

pw = wb['Peers']
c9 = ScatterChart(); c9.style = 13
for i in range(4, PEER_LAST + 1):
    s = Series(Reference(pw, min_col=7, min_row=i), Reference(pw, min_col=6, min_row=i), title=pw.cell(i, 1).value)
    s.marker.symbol = 'circle'; s.marker.size = 9; s.graphicalProperties.line.noFill = True
    clr = 'C00000' if pw.cell(i, 2).value == 'MBGL' else ['1F3864', '4472C4', '70AD47', 'ED7D31', 'A5A5A5', '7030A0'][i % 6]
    s.marker.graphicalProperties.solidFill = clr; s.marker.graphicalProperties.line.solidFill = clr
    c9.series.append(s)
c9.x_axis.title = 'Organic growth (mid)'; c9.y_axis.title = 'EBITDA margin (approx.)'
c9.x_axis.number_format = '0%'; c9.y_axis.number_format = '0%'
place(c9, 'B75', 'Peers: growth vs margin (approximate)')

c10 = BarChart(); c10.type = 'col'
c10.add_data(Reference(HWS, min_col=1, max_col=12, min_row=4), from_rows=True, titles_from_data=True)
c10.set_categories(Reference(HWS, min_col=2, max_col=12, min_row=3))
l10 = LineChart(); l10.add_data(Reference(HWS, min_col=1, max_col=12, min_row=6), from_rows=True, titles_from_data=True)
l10.y_axis.axId = 200; l10.y_axis.number_format = '0%'; l10.y_axis.crosses = 'max'; l10.y_axis.title = 'Margin'
c10 += l10
place(c10, 'L75', 'History: revenue and Adj. EBITDA margin (IHS Transp. FY14-21; carve-out FY23-25)', '$m')

del wb['Sheet']
wb._sheets.insert(0, wb._sheets.pop(wb._sheets.index(wb['Notes'])))
wb.save(OUT)
print('saved', OUT)
