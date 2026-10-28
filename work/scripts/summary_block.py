# ---------------------------------------------------------------- Annual Summary FY14–FY26 (front tab). exec'd from build_workbook.py
# Clean annual P&L / balance sheet / cash flow with segment detail. Every historical number is a cross-sheet link (green)
# to the tab that holds the as-reported figure; FY2026E is company guidance (blue input, cited). Eras are labelled and growth
# is only computed within an era.
AS_Y = [f'FY{y}' for y in range(2014, 2026)]
AS_COLS = AS_Y + ['FY2026E', '', '1H25', '1H26']
ERA = {**{y: 'A' for y in AS_Y[:8]}, 'FY2022': 'B', 'FY2023': 'C', 'FY2024': 'C', 'FY2025': 'C', 'FY2026E': 'G', '1H25': 'C', '1H26': 'C'}
ERA_LAB = {'A': 'IHS Markit Transportation segment\n(Nov-30 FYE)', 'B': 'S&P Global Mobility segment\n(~10 months)',
           'C': 'Mobility Global\ncombined (carve-out)', 'G': 'Guidance\n(8-K 2026-08-07)'}
ERA_FILL = {'A': '2E5597', 'B': '44546A', 'C': NAVY, 'G': '7F6000'}
ws = wb.create_sheet('Annual Summary')
NC = len(AS_COLS)
setup(ws, 'Mobility Global (MBGL): annual summary FY2014–FY2026E. P&L, balance sheet, cash flow and segments',
      'Every historical figure links to the as-reported tab (green). Eras are NOT comparable, so growth is computed only within an era. FY2026E = company guidance '
      'midpoint (revenue $1,870–1,885m; Adj. EBITDA $745–760m), not an actual. 1H = six months to 30 June. USD millions.', NC + 1, label_w=46)
for i, p in enumerate(AS_COLS):
    ws.column_dimensions[L(i + 2)].width = 9.5 if p else 2
ws.column_dimensions[L(NC + 2)].width = 46
# two header rows: era band + period
for i, p in enumerate(AS_COLS):
    if not p: continue
    e = ERA[p]
    c = ws.cell(4, i + 2, ERA_LAB[e] if (i == 0 or ERA.get(AS_COLS[i - 1]) != e) else None)
    c.fill = PatternFill('solid', fgColor=ERA_FILL[e]); c.font = Font(name='Arial', size=7, bold=True, color='FFFFFF')
    c.alignment = Alignment(wrap_text=True, vertical='top')
    h = ws.cell(5, i + 2, p.replace('FY20', 'FY')); h.fill = PatternFill('solid', fgColor=ERA_FILL[e]); h.font = F_HDR
    h.alignment = Alignment(horizontal='center')
ws.cell(4, 1, '').fill = FILL_N; ws.cell(5, 1, 'USD millions').font = F_HDR; ws.cell(5, 1).fill = FILL_N
ws.cell(5, NC + 2, 'Source / basis').font = F_HDR; ws.cell(5, NC + 2).fill = FILL_N
ws.row_dimensions[4].height = 34
ws.freeze_panes = ws.cell(6, 2)

def acol(p): return L(AS_COLS.index(p) + 2)
SHC = lambda p: L(SH_P.index(p) + 2)                 # Segment History column
PLC = lambda p: L(FLOW_P.index(p) + 2)               # IS / CF / Segment P&L column
BSC = lambda p: L(BS_P.index(p) + 2)                 # BS column
HMAP = {'1H25': '6M-2025', '1H26': '6M-2026'}
def flow_p(p): return HMAP.get(p, p)
AR = {}
r = 6
def sec(t):
    global r
    section(ws, r, t, NC); r += 1
def row(key, label, getter, fmt=MONEY, bold=False, src='', indent=False):
    """getter(p) -> formula string (without '=') or number (input) or None"""
    global r
    ws.cell(r, 1, ('   ' if indent else '') + label).font = F_SEC if bold else F_BASE
    for p in AS_COLS:
        if not p: continue
        v = getter(p)
        if v is None: continue
        c = ws.cell(r, AS_COLS.index(p) + 2)
        if isinstance(v, str):
            c.value = '=' + v
            c.font = (F_X_B if bold else F_X) if '!' in v else (F_FX_B if bold else F_FX)
        else:
            c.value = v; c.font = F_IN_B if bold else F_IN
        c.number_format = fmt
    ws.cell(r, NC + 2, src).font = F_NOTE
    AR[key] = r; r += 1
def growth(key, label, base, eras=('A', 'C')):
    def g(p):
        i = AS_COLS.index(p)
        if p == '1H26': return f'{acol(p)}{AR[base]}/{acol("1H25")}{AR[base]}-1'
        if p == 'FY2026E':
            return f'{acol(p)}{AR[base]}/{acol("FY2025")}{AR[base]}-1' if ws.cell(AR[base], AS_COLS.index(p) + 2).value is not None else None
        if p in ('1H25',) or i == 0: return None
        prev = AS_COLS[i - 1]
        if ERA.get(prev) != ERA[p] or ERA[p] not in eras: return None
        return f'{acol(p)}{AR[base]}/{acol(prev)}{AR[base]}-1'
    row(key, label, g, PCT_C, src='[C] within era only; FY2026E vs FY2025; 1H26 vs 1H25', indent=True)
def ratio(key, label, num, den):
    row(key, label, lambda p: f'IF({acol(p)}{AR[den]}=0,"",{acol(p)}{AR[num]}/{acol(p)}{AR[den]})' if ws.cell(AR[num], AS_COLS.index(p) + 2).value is not None
        and ws.cell(AR[den], AS_COLS.index(p) + 2).value is not None else None, PCT_C, src='[C]', indent=True)
IS_ = lambda key: (lambda p: f"'IS'!{PLC(flow_p(p))}{REF[('IS', key)]}" if ERA[p] == 'C' else None)
CF_ = lambda key: (lambda p: f"'CF'!{PLC(flow_p(p))}{REF[('CF', key)]}" if ERA[p] == 'C' and (key, flow_p(p)) and canon.get((key, flow_p(p))) is not None else None)
SP_ = lambda seg, key: (lambda p: f"'Segment P&L'!{PLC(flow_p(p))}{SR[(seg, key)]}" if ERA[p] == 'C' else None)
_SHWS = wb['Segment History']
def _has(sheet_ws, rr, cc): return sheet_ws.cell(rr, cc).value is not None
SH_A = lambda key: (lambda p: f"'Segment History'!{SHC(p)}{SHR[key]}" if ERA[p] == 'A' and _has(_SHWS, SHR[key], SH_P.index(p) + 2) else None)
SH_B = lambda key: (lambda p: f"'Segment History'!{SHC(p)}{SHR[key]}" if p in ('FY2022',) else None)
def first(*fs):
    return lambda p: next((v for v in (f(p) for f in fs) if v is not None), None)

# ============================== P&L
sec('Income statement')
row('rev', 'Revenue', first(SH_A('a_rev'), SH_B('b_rev'), IS_('IS.revenue'), lambda p: 1877.5 if p == 'FY2026E' else None), bold=True,
    src='FY14–21 IHS Markit 10-Ks; FY22 SPGI 10-K (Mar–Dec); FY23+ IS tab; FY26E guide midpoint')
growth('rev_g', 'Revenue growth y/y', 'rev')
row('org', 'Organic growth (as printed)', SH_A('a_org'), PCT_P, src='IHS Markit 10-K growth bridge [D]; MBGL prints no organic growth', indent=True)
row('sub', 'Subscription revenue (FY20: IHS "recurring")', first(
    lambda p: f"'Segment History'!{L(QP.index('FY2020') + 2)}{QR['rec']}" if p == 'FY2020' else None,
    SH_B('b_sub'), SP_('Total', 'sub')), src='FY20 IHS decks; FY22 SPGI; FY23+ Segment P&L', indent=True)
row('non', 'Non-subscription revenue (FY20: "non-recurring")', first(
    lambda p: f"'Segment History'!{L(QP.index('FY2020') + 2)}{QR['non']}" if p == 'FY2020' else None,
    SH_B('b_non'), SP_('Total', 'nonsub')), indent=True)
ratio('sub_sh', 'Subscription share of revenue', 'sub', 'rev')
row('us', 'U.S. revenue', first(SH_B('b_us'), SP_('Total', 'us')), indent=True)
row('intl', 'International revenue', first(SH_B('b_intl'), SP_('Total', 'intl')), indent=True)
row('cfx_rev', 'CARFAX segment revenue', SP_('CARFAX', 'rev'), src='Segment P&L tab (Form 10/A; 10-Q)', indent=True)
row('b2b_rev', 'B2B segment revenue', SP_('B2B', 'rev'), indent=True)
growth('cfx_g', 'CARFAX growth y/y', 'cfx_rev', eras=('C',))
growth('b2b_g', 'B2B growth y/y', 'b2b_rev', eras=('C',))
row('oprel', 'Operating-related expenses', IS_('IS.oprel'), src='IS tab')
row('sg', 'Selling and general expenses', IS_('IS.sg'))
row('dep', 'Depreciation', IS_('IS.dep'))
row('amort', 'Amortization of acquired intangibles', IS_('IS.amort'), src='IHS Markit merger step-up')
row('da22', 'Depreciation & amortization (segment total)', SH_B('b_da'), src='FY22 SPGI segment note', indent=True)
row('op', 'Operating profit', first(SH_B('b_op'), IS_('IS.op_f')), bold=True, src='FY22 SPGI segment OP; FY23+ IS')
ratio('op_m', 'Operating margin', 'op', 'rev')
row('int', 'Interest expense, net', IS_('IS.int'))
row('pbt', 'Income before taxes', IS_('IS.pbt_f'))
row('tax', 'Provision for taxes', IS_('IS.tax'))
row('ni', 'Net income', IS_('IS.ni_f'), bold=True, src='Carve-out; excludes $2.0bn notes issued May-2026 (interest from 2H26)')
sec('Adjusted EBITDA (company definition of each era) and segment profit')
row('ebitda', 'Adjusted EBITDA', first(SH_A('a_ebitda'),
    lambda p: f"'Segment P&L'!{PLC(flow_p(p))}{SR[('Total', 'adj_rep')]}" if ERA[p] == 'C' else None,
    lambda p: 752.5 if p == 'FY2026E' else None), bold=True,
    src='IHS Adj. EBITDA (FY14–21); MBGL Adj. EBITDA (10 exclusions to Q1-26, 6 after); FY26E guide midpoint. FY22: n/a')
growth('ebitda_g', 'Adjusted EBITDA growth y/y', 'ebitda')
ratio('ebitda_m', 'Adjusted EBITDA margin', 'ebitda', 'rev')
row('ebitda_u', 'Memo: operating profit + D&A (unadjusted) [C]', first(SH_B('b_ebitda'),
    lambda p: f'{acol(p)}{AR["op"]}+{acol(p)}{AR["dep"]}+{acol(p)}{AR["amort"]}' if ERA[p] == 'C' else None), src='FY22 SPGI segment; FY23+ IS', indent=True)
for _sg in ('CARFAX', 'B2B', 'Corporate'):
    row(f'adj_{_sg}', f'Segment Adj. EBITDA: {_sg}', SP_(_sg, 'adj'), src='Segment P&L tab (company-reported)', indent=True)
ratio('cfx_m', 'CARFAX Adj. EBITDA margin', 'adj_CARFAX', 'cfx_rev')
ratio('b2b_m', 'B2B Adj. EBITDA margin', 'adj_B2B', 'b2b_rev')

# ============================== Balance sheet
sec('Balance sheet (period-end). Segment assets only before FY2024')
BSP = {'FY2024': 'FY2024', 'FY2025': 'FY2025', '1H26': 'Q2-2026'}
BS_ = lambda key: (lambda p: f"'BS'!{BSC(BSP[p])}{REF[('BS', key)]}" if p in BSP and canon.get((key, BSP[p])) is not None or (p in BSP and key.endswith('_f')) else None)
row('seg_ta', 'Segment total assets (IHS Transportation / SPGI Mobility)', first(SH_A('a_ta'),
    lambda p: f"'Segment History'!{SHC(p)}{SHR['b_ta']}" if p in ('FY2022', 'FY2023') else None), src='IHS / SPGI segment notes. FY22 jump = S&P Global purchase accounting (goodwill/intangibles step-up), not growth')
row('seg_gw', 'Segment goodwill (IHS Transportation)', SH_A('a_gw'), indent=True)
row('cash', 'Cash and cash equivalents', BS_('BS.cash'), src='BS tab (combined); 1H26 = 30 Jun 2026')
row('ar', 'Accounts receivable, net', BS_('BS.ar'))
row('gw', 'Goodwill', BS_('BS.gw'))
row('intang', 'Other intangible assets, net', BS_('BS.intang'))
row('ta', 'Total assets', BS_('BS.ta_f'), bold=True)
row('unearned', 'Unearned revenue', BS_('BS.unearned'))
row('ltd', 'Long-term debt (Senior Notes)', BS_('BS.ltd'), src='$2.0bn notes issued 29 May 2026')
row('dtl', 'Deferred tax liability', BS_('BS.dtl'))
row('tl', 'Total liabilities', BS_('BS.tl_f'))
row('te', 'Total equity (parent company investment)', BS_('BS.te_f'), bold=True, src='Fell by the $2.0bn dividend to S&P Global in 2026')
row('nd', 'Net debt (cash) [C]', lambda p: f'{acol(p)}{AR["ltd"]}-{acol(p)}{AR["cash"]}' if p in BSP else None, indent=True)

# ============================== Cash flow
sec('Cash flow')
row('cfo', 'Cash from operations', CF_('CF.cfo'), bold=True, src='CF tab')
row('capex', 'Capital expenditures', first(CF_('CF.capex'), lambda p: f"-'Segment History'!{SHC(p)}{SHR['b_capex']}" if p == 'FY2022' else None),
    src='FY22 SPGI segment capex; FY23+ CF')
row('fcf', 'Free cash flow (CFO + capex) [C]', lambda p: f'{acol(p)}{AR["cfo"]}+{acol(p)}{AR["capex"]}' if ERA[p] == 'C' and canon.get(('CF.capex', flow_p(p))) is not None else None, bold=True)
ratio('fcf_conv', 'FCF / Adjusted EBITDA', 'fcf', 'ebitda')
row('acq', 'Acquisitions, net of cash', CF_('CF.acq'), src='FY23 Market Scan')
row('parent', 'Net transfers to S&P Global (parent)', CF_('CF.parent'), src='1H26 includes the $2.0bn dividend')
row('notes', 'Proceeds from Senior Notes', CF_('CF.notes'))

# ============================== checks + notes
sec('Checks')
def chk(label, fn):
    global r
    ws.cell(r, 1, label).font = F_NOTE
    for p in AS_COLS:
        if not p or ERA[p] != 'C': continue
        c = ws.cell(r, AS_COLS.index(p) + 2, '=' + fn(p)); c.number_format = MONEY; c.font = F_FX
    ws.cell(r, MARK, 'CHECK')
    for cc in range(1, NC + 2): ws.cell(r, cc).fill = FILL_CHK
    r += 1
chk('CHECK CARFAX + B2B revenue = revenue', lambda p: f'{acol(p)}{AR["cfx_rev"]}+{acol(p)}{AR["b2b_rev"]}-{acol(p)}{AR["rev"]}')
chk('CHECK subscription + non-subscription = revenue', lambda p: f'{acol(p)}{AR["sub"]}+{acol(p)}{AR["non"]}-{acol(p)}{AR["rev"]}')
chk('CHECK U.S. + International = revenue', lambda p: f'{acol(p)}{AR["us"]}+{acol(p)}{AR["intl"]}-{acol(p)}{AR["rev"]}')
r += 1
for note in [
    'Eras: FY14–21 = IHS Markit "Transportation" segment (Nov-30 year-end; includes Maritime & Trade throughout and Aerospace & Defense until Dec-2019; automotive ~80% → >90% of revenue). '
    'FY22 = S&P Global "Mobility" segment from the 28-Feb-2022 merger (~10 months; Dec-2021–Feb-2022 in neither era). FY23+ = Mobility Global combined (carve-out) statements.',
    'Not comparable across eras: scope, fiscal year-end and profit measure differ (IHS Adj. EBITDA vs MBGL Adj. EBITDA; SPGI reported only segment operating profit). No growth is computed across a boundary.',
    'FY14–15 IHS figures come from later 10-K comparatives (IHS Inc. filings not on Quartr). Balance sheet before FY2024 = segment assets only; no carve-out balance sheet was printed for FY2023 or earlier.',
    'FY2026E: guidance midpoints only (8-K 2026-08-07). 1H26 interest and tax predate most of the new $2.0bn debt service (≈$55m 2H26 interest guided).',
    'Detail and audit trail: IS / BS / CF / Segment P&L / Segment History tabs; Accounting Notes for every break and gap.']:
    c = ws.cell(r, 1, note); c.font = F_NOTE; r += 1
