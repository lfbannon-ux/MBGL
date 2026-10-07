# ---------------------------------------------------------------- Segment History (structured, era-by-era) — inserted into build_workbook.py
pred = rd('predecessor.csv')
SH_P = [f'FY{y}' for y in range(2014, 2026)]
SH_LAB = {p: p + ('\nNov-30' if int(p[2:]) <= 2021 else '\nDec-31') for p in SH_P}
def pick(doc_prefix, sec_re, line_re, period, unit=None):
    """As originally reported: prefer the document for the same fiscal year; else the EARLIEST later document printing it (comparative)."""
    c = [r for r in pred if r['source_doc'].startswith(doc_prefix) and r['fiscal_period'] == period
         and re.search(sec_re, r['section']) and re.search(line_re, r['line_item']) and (unit is None or r['unit'] == unit)]
    if not c: return None
    own = [r for r in c if r['source_doc'].endswith(period)]
    if own: return own[0], False
    c.sort(key=lambda r: r['source_doc'])
    return c[0], True
ws = wb.create_sheet('Segment History'); COLS['Segment History'] = SH_P
setup(ws, 'Segment history — IHS Markit "Transportation" (FY2014–21) → S&P Global "Mobility" (FY2022–25) → Mobility Global carve-out (FY2023–25)',
      'Each era as originally reported by its owner; growth computed ONLY within an era. Bold-italic blue = taken from a later filing\'s comparative column (no own-year document on Quartr). NON-COMPARABLE across eras: scope, fiscal year-end, profit measure.', len(SH_P) + 1)
header(ws, 4, [SH_LAB[p] for p in SH_P] + ['Source / basis'])
for i, p in enumerate(SH_P):
    ws.cell(4, i + 2).fill = PatternFill('solid', fgColor='2E5597' if int(p[2:]) <= 2021 else NAVY)
F_CMP = Font(name='Arial', size=9, color='0000FF', bold=True, italic=True)
SHR = {}
def sh_in(r, key, label, doc, sec, line, unit, fmt, periods, bold=False, src=''):
    ws.cell(r, 1, label).font = F_SEC if bold else F_BASE
    for i, p in enumerate(SH_P):
        if p not in periods: continue
        got = pick(doc, sec, line, p, unit)
        if not got: continue
        row, cmp_ = got
        try: v = float(row['value'])
        except ValueError: v = row['value']
        c = ws.cell(r, i + 2, v); c.number_format = fmt
        c.font = F_CMP if cmp_ else (F_IN_B if bold else F_IN)
    ws.cell(r, len(SH_P) + 2, src).font = F_NOTE
    SHR[key] = r
def sh_fx(r, key, label, fn, periods, fmt, bold=False, src='[C]', chk=False):
    ws.cell(r, 1, label).font = F_NOTE if chk else (F_FX_B if bold else F_FX)
    for i, p in enumerate(SH_P):
        if p not in periods: continue
        e = fn(p, L(i + 2), L(i + 1))
        if e is None: continue
        c = ws.cell(r, i + 2, '=' + e); c.number_format = fmt
        c.font = (F_X if '!' in e else F_FX) if not bold else F_FX_B
    ws.cell(r, len(SH_P) + 2, src).font = F_NOTE
    if chk:
        ws.cell(r, MARK, 'CHECK')
        for cc in range(1, len(SH_P) + 2): ws.cell(r, cc).fill = FILL_CHK
    SHR[key] = r
P0 = [f'FY{y}' for y in range(2014, 2022)]; P1 = [f'FY{y}' for y in range(2022, 2026)]; P2 = ['FY2023', 'FY2024', 'FY2025']
def prevok(era):  # growth only when the prior year is in the same era
    return lambda p: p in era and era.index(p) > 0
r = 5
section(ws, r, 'A. IHS Markit — Transportation segment (FYE Nov 30; includes Maritime & Trade throughout and Aerospace & Defense until sold 2019-12-02)', len(SH_P) + 1); r += 1
sh_in(r, 'a_rev', 'Transportation revenue [D]', 'INFO', r'Revenue by Segment$', r'^Transportation$', 'usd_m', MONEY, P0, True, 'INFO 10-K MD&A "Revenue by Segment"; FY2014/15 from FY2016/FY2017 10-K comparatives'); r += 1
sh_fx(r, 'a_g', 'Revenue growth y/y [C]', lambda p, c, pc: f'{c}{SHR["a_rev"]}/{pc}{SHR["a_rev"]}-1' if prevok(P0)(p) else None, P0, PCT_C); r += 1
sh_in(r, 'a_gp', 'Revenue growth — as printed [D]', 'INFO', r'Revenue by Segment$', r'^Transportation % Change', 'pct', PCT_P, P0, src='Printed, rounded'); r += 1
sh_in(r, 'a_org', '  Organic growth (pp) [D]', 'INFO', r'growth drivers', r'Transportation revenue - Organic', 'pct', PCT_P, P0, src='MD&A revenue growth drivers'); r += 1
sh_in(r, 'a_acq', '  Acquisitive (pp) [D]', 'INFO', r'growth drivers', r'Transportation revenue - Acquisitive', 'pct', PCT_P, P0); r += 1
sh_in(r, 'a_fx', '  Foreign currency (pp) [D]', 'INFO', r'growth drivers', r'Transportation revenue - Foreign Currency', 'pct', PCT_P, P0); r += 1
sh_in(r, 'a_rorg', 'Recurring revenue organic growth [D]', 'INFO', r'Transaction Type', r'recurring revenue organic growth', 'pct', PCT_P, P0, src='MD&A narrative; FY2019 own-year figure not printed in FY2019 10-K text'); r += 1
sh_in(r, 'a_ebitda', 'Transportation Adjusted EBITDA [D]', 'INFO', r'Segment Adjusted EBITDA$', r'^Transportation Adjusted EBITDA$', 'usd_m', MONEY, P0, True, 'IHS Markit segment measure (pre-D&A, pre-SBC; company definition)'); r += 1
sh_fx(r, 'a_eg', 'Adjusted EBITDA growth y/y [C]', lambda p, c, pc: f'{c}{SHR["a_ebitda"]}/{pc}{SHR["a_ebitda"]}-1' if prevok(P0)(p) else None, P0, PCT_C); r += 1
sh_fx(r, 'a_m', 'Adjusted EBITDA margin [C]', lambda p, c, pc: f'{c}{SHR["a_ebitda"]}/{c}{SHR["a_rev"]}', P0, PCT_C, True); r += 1
sh_in(r, 'a_mp', 'Adjusted EBITDA margin — as printed [D]', 'INFO', r'Segment Adjusted EBITDA$', r'as a percent of segment revenue', 'pct', PCT_P, P0); r += 1
sh_fx(r, 'a_inc', 'Incremental Adj. EBITDA margin (ΔEBITDA/Δrevenue) [C]', lambda p, c, pc: f'({c}{SHR["a_ebitda"]}-{pc}{SHR["a_ebitda"]})/({c}{SHR["a_rev"]}-{pc}{SHR["a_rev"]})' if prevok(P0)(p) else None, P0, PCT_C); r += 1
sh_in(r, 'a_tot', 'IHS Markit total revenue [D]', 'INFO', r'Revenue by Segment$', r'Total revenue \(IHS Markit consolidated\)', 'usd_m', MONEY, P0); r += 1
sh_fx(r, 'a_sh', 'Transportation share of IHS Markit revenue [C]', lambda p, c, pc: f'{c}{SHR["a_rev"]}/{c}{SHR["a_tot"]}', P0, PCT_C); r += 1
sh_in(r, 'a_ta', 'Transportation segment total assets [D]', 'INFO', r'Total assets by segment', r'Total Assets - Transportation', 'usd_m', MONEY, P0); r += 1
sh_in(r, 'a_gw', 'Transportation goodwill, Nov 30 [D]', 'INFO', r'Goodwill activity', r'Balance at November 30', 'usd_m', MONEY, P0); r += 1
sh_fx(r, 'a_roa', 'Adj. EBITDA / segment total assets [C]', lambda p, c, pc: f'{c}{SHR["a_ebitda"]}/{c}{SHR["a_ta"]}', P0, PCT_C); r += 1
sh_fx(r, 'a_chk1', 'CHECK organic + acquisitive + FX vs printed growth (0 = within ±1pp rounding)',
      lambda p, c, pc: f'IF(ABS({c}{SHR["a_org"]}+{c}{SHR["a_acq"]}+{c}{SHR["a_fx"]}-{c}{SHR["a_gp"]})<=1,0,{c}{SHR["a_org"]}+{c}{SHR["a_acq"]}+{c}{SHR["a_fx"]}-{c}{SHR["a_gp"]})' if prevok(P0)(p) else None, P0, MONEY, chk=True); r += 1
sh_fx(r, 'a_chk2', 'CHECK computed vs printed margin (0 = within ±0.6pp rounding)',
      lambda p, c, pc: f'IF(ABS({c}{SHR["a_m"]}*100-{c}{SHR["a_mp"]})<=0.6,0,{c}{SHR["a_m"]}*100-{c}{SHR["a_mp"]})', P0, MONEY, chk=True); r += 1
r += 1
section(ws, r, 'B. S&P Global — Mobility segment (FYE Dec 31; FY2022 ≈ 10 months from 2022-02-28 merger close; profit measure = operating profit AFTER acquired-intangible amortization)', len(SH_P) + 1); r += 1
sh_in(r, 'b_rev', 'Mobility revenue [D]', 'SPGI', r'MD&A Mobility segment table$', r'^Revenue$', 'usd_m', MONEY, P1, True, 'SPGI 10-K MD&A Mobility table'); r += 1
sh_fx(r, 'b_g', 'Revenue growth y/y [C] (FY2023 vs ~10-month FY2022 — not like-for-like)', lambda p, c, pc: f'{c}{SHR["b_rev"]}/{pc}{SHR["b_rev"]}-1' if prevok(P1)(p) else None, P1, PCT_C); r += 1
sh_in(r, 'b_sub', '  Subscription revenue [D]', 'SPGI', r'MD&A Mobility segment table$', r'^Subscription revenue$', 'usd_m', MONEY, P1); r += 1
sh_in(r, 'b_non', '  Non-subscription revenue [D]', 'SPGI', r'MD&A Mobility segment table$', r'^Non-subscription revenue$', 'usd_m', MONEY, P1); r += 1
sh_fx(r, 'b_subp', '  Subscription share [C]', lambda p, c, pc: f'{c}{SHR["b_sub"]}/{c}{SHR["b_rev"]}', P1, PCT_C); r += 1
sh_in(r, 'b_us', '  U.S. revenue [D]', 'SPGI', r'MD&A Mobility segment table$', r'^U\.S\. revenue$', 'usd_m', MONEY, P1); r += 1
sh_in(r, 'b_intl', '  International revenue [D]', 'SPGI', r'MD&A Mobility segment table$', r'^International revenue$', 'usd_m', MONEY, P1); r += 1
sh_in(r, 'b_op', 'Mobility operating profit [D]', 'SPGI', r'MD&A Mobility segment table$', r'^Operating profit$', 'usd_m', MONEY, P1, True); r += 1
sh_fx(r, 'b_m', 'Operating margin [C]', lambda p, c, pc: f'{c}{SHR["b_op"]}/{c}{SHR["b_rev"]}', P1, PCT_C); r += 1
sh_in(r, 'b_am', '  incl. amortization of acquired intangibles [D]', 'SPGI', r'footnote 1', r'amortization of intangibles from acquisitio', 'usd_m', MONEY, P1); r += 1
sh_in(r, 'b_da', 'Depreciation & amortization [D]', 'SPGI', r'Segment information$', r'Depreciation & Amortization', 'usd_m', MONEY, P1); r += 1
sh_fx(r, 'b_ebitda', 'Operating profit + D&A [C] (proxy; NOT a company-defined measure)', lambda p, c, pc: f'{c}{SHR["b_op"]}+{c}{SHR["b_da"]}', P1, MONEY, True); r += 1
sh_fx(r, 'b_em', 'Operating profit + D&A margin [C]', lambda p, c, pc: f'{c}{SHR["b_ebitda"]}/{c}{SHR["b_rev"]}', P1, PCT_C); r += 1
sh_in(r, 'b_capex', 'Capital expenditures [D]', 'SPGI', r'Segment information$', r'Capital Expenditures', 'usd_m', MONEY, P1); r += 1
sh_in(r, 'b_ta', 'Mobility segment total assets [D]', 'SPGI', r'Segment information \(as of', r'^Total Assets$', 'usd_m', MONEY, P1); r += 1
sh_fx(r, 'b_chk', 'CHECK subscription + non-subscription = revenue', lambda p, c, pc: f'{c}{SHR["b_sub"]}+{c}{SHR["b_non"]}-{c}{SHR["b_rev"]}', P1, MONEY, chk=True); r += 1
sh_fx(r, 'b_chk2', 'CHECK U.S. + International = revenue', lambda p, c, pc: f'{c}{SHR["b_us"]}+{c}{SHR["b_intl"]}-{c}{SHR["b_rev"]}', P1, MONEY, chk=True); r += 1
r += 1
section(ws, r, 'C. Mobility Global — combined (carve-out) statements (green = links to IS tab)', len(SH_P) + 1); r += 1
def islink(key):
    return lambda p, c, pc: f"'IS'!{xcol('IS', p)}{REF[('IS', key)]}" if p in P2 else None
sh_fx(r, 'c_rev', 'Revenue [D]', islink('IS.revenue'), P2, MONEY, True, 'IS tab (Form 10/A)'); r += 1
sh_fx(r, 'c_g', 'Revenue growth y/y [C]', lambda p, c, pc: f'{c}{SHR["c_rev"]}/{pc}{SHR["c_rev"]}-1' if prevok(P2)(p) else None, P2, PCT_C); r += 1
sh_fx(r, 'c_op', 'Operating profit [D]', islink('IS.op_f'), P2, MONEY, False, 'IS tab'); r += 1
adj = {r_['fiscal_period']: float(r_['value']) for r_ in seg if r_['statement'] == 'NONGAAP' and r_['source_doc'].startswith('Form10A')
       and r_['line_item'].strip() == 'Adjusted EBITDA' and r_['page'] == '358' and r_['fiscal_period'] in P2}
ws.cell(r, 1, 'Adjusted EBITDA — company definition [D]').font = F_SEC
for i, p in enumerate(SH_P):
    if p in adj: c = ws.cell(r, i + 2, adj[p]); c.font = F_IN_B; c.number_format = MONEY
ws.cell(r, len(SH_P) + 2, 'Form 10/A p.358 (10-exclusion definition)').font = F_NOTE; SHR['c_adj'] = r; r += 1
sh_fx(r, 'c_am', 'Adjusted EBITDA margin [C]', lambda p, c, pc: f'{c}{SHR["c_adj"]}/{c}{SHR["c_rev"]}', P2, PCT_C); r += 1
sh_fx(r, 'c_d1', 'Carve-out revenue − S&P Global segment revenue [C]', lambda p, c, pc: f'{c}{SHR["c_rev"]}-{c}{SHR["b_rev"]}', P2, MONEY, src='≈ $3m/yr data-sharing revenue S&P Global eliminates (analysis/D4)'); r += 1
sh_fx(r, 'c_d2', 'Carve-out operating profit − S&P Global segment operating profit [C]', lambda p, c, pc: f'{c}{SHR["c_op"]}-{c}{SHR["b_op"]}', P2, MONEY, src='Corporate allocations + amortization basis differences (analysis/D4)'); r += 1
r += 1
section(ws, r, 'Era CAGRs [C] (within-era only)', len(SH_P) + 1); r += 1
def cagr(label, key, y0, y1):
    global r
    ws.cell(r, 1, label).font = F_BASE
    c0, c1 = L(SH_P.index(y0) + 2), L(SH_P.index(y1) + 2)
    c = ws.cell(r, 2, f'=({c1}{SHR[key]}/{c0}{SHR[key]})^(1/{int(y1[2:]) - int(y0[2:])})-1'); c.number_format = PCT_C; c.font = F_FX
    ws.cell(r, 3, f'{y0}→{y1}').font = F_NOTE; r += 1
cagr('Transportation revenue CAGR', 'a_rev', 'FY2014', 'FY2021')
cagr('Transportation revenue CAGR (pre-COVID)', 'a_rev', 'FY2014', 'FY2019')
cagr('Transportation Adj. EBITDA CAGR', 'a_ebitda', 'FY2014', 'FY2021')
cagr('S&P Global Mobility revenue CAGR (full years)', 'b_rev', 'FY2023', 'FY2025')
cagr('S&P Global Mobility operating profit CAGR', 'b_op', 'FY2023', 'FY2025')
cagr('Carve-out revenue CAGR', 'c_rev', 'FY2023', 'FY2025')
r += 1
for note in ['Era breaks: (1) IHS Inc. pre-FY2016 filings not on Quartr — FY2014/15 come only from comparative columns; (2) 2016-07 IHS–Markit merger; (3) A&D sold 2019-12-02 (≈$470m) — FY2020 acquisitive −6pp; (4) 2022-02-28 S&P Global merger: Dec FYE, purchase-accounting reset, Maritime & Trade moved out, profit measure changes to operating profit after amortization; Dec-2021–Feb-2022 falls in neither era; (5) 2025 realignment into CARFAX / B2B.',
             'Automotive share of Transportation revenue as printed: "about 80%" (FY2016–18), ~80%+ (FY2019), "more than 90 percent" (FY2020–21) — see Predecessor Segments tab (text rows).',
             'Quarterly IHS Markit segment data (FY2021 10-Qs / 8-K) appear on the Predecessor Segments tab where printed.']:
    ws.cell(r, 1, note).font = F_NOTE; r += 1
ws.column_dimensions[L(len(SH_P) + 2)].width = 55

# ---- D. IHS Markit Transportation — quarterly (Quartr holds FY2021 Q2/Q3 releases, 10-Qs and decks; FY2020 quarters only as comparatives)
QP = ['Q1-FY2020', 'Q2-FY2020', 'Q3-FY2020', 'Q4-FY2020', 'FY2020', 'Q1-FY2021', 'Q2-FY2021', 'Q3-FY2021', '9M-FY2021', 'FY2021']
DOC_ORDER = ['INFO_10Q_Q2-FY2021', 'INFO_8K_Q2-FY2021', 'INFO_Slides_Q2-FY2021', 'INFO_10Q_Q3-FY2021', 'INFO_Slides_Q3-FY2021']
def qpick(line_res, period):
    c = [x for x in pred if x['source_doc'] in DOC_ORDER and x['fiscal_period'] == period and x['unit'] != 'text'
         and any(re.search(lr, x['line_item']) for lr in line_res)]
    if not c: return None
    own = [x for x in c if x['source_doc'].endswith(period)]
    pool = own or c
    pool.sort(key=lambda x: DOC_ORDER.index(x['source_doc']))
    return pool[0], not own
r += 1
section(ws, r, 'D. IHS Markit — Transportation quarterly (FYE Nov 30). Precise $ from 10-Q/8-K where printed; otherwise rounded deck figures ($m, integers). Bold-italic = comparative from a later document.', len(SH_P) + 1); r += 1
for i, p in enumerate(QP):
    c = ws.cell(r, i + 2, p.replace('-FY', '\nFY')); c.font = F_HDR; c.fill = PatternFill('solid', fgColor='2E5597'); c.alignment = Alignment(horizontal='center', wrap_text=True)
ws.cell(r, 1, 'USD millions unless stated').font = F_HDR; ws.cell(r, 1).fill = PatternFill('solid', fgColor='2E5597'); r += 1
QR = {}
def q_in(key, label, line_res, fmt, bold=False, src=''):
    global r
    ws.cell(r, 1, label).font = F_SEC if bold else F_BASE
    for i, p in enumerate(QP):
        got = qpick(line_res, p)
        if not got: continue
        x, cmp_ = got
        c = ws.cell(r, i + 2, float(x['value'])); c.number_format = fmt
        c.font = F_CMP if cmp_ else (F_IN_B if bold else F_IN)
    ws.cell(r, len(SH_P) + 2, src).font = F_NOTE
    QR[key] = r; r += 1
def q_fx(key, label, fn, fmt, chk=False, src='[C]'):
    global r
    ws.cell(r, 1, label).font = F_NOTE if chk else F_FX
    for i, p in enumerate(QP):
        e = fn(p, L(i + 2))
        if e is None: continue
        c = ws.cell(r, i + 2, '=' + e); c.number_format = fmt; c.font = F_FX
    ws.cell(r, len(SH_P) + 2, src).font = F_NOTE
    if chk:
        ws.cell(r, MARK, 'CHECK')
        for cc in range(1, len(SH_P) + 2): ws.cell(r, cc).fill = FILL_CHK
    QR[key] = r; r += 1
q_in('rev', 'Transportation revenue [D]', [r'^Revenue - Transportation$', r'^Transportation$', r'^Total - Transportation$'], MONEY, True, '10-Q Note 16 / 8-K / decks; FY2020 & FY2021 annual from 10-K')
q_in('rec', '  Recurring revenue [D]', [r'^Recurring - Transportation$'], MONEY, src='8-K supplemental (Q2) / decks; Transportation has no recurring-variable revenue')
q_in('non', '  Non-recurring revenue [D]', [r'^Non-Recurring - Transportation$'], MONEY)
# 8-K precise recurring/non-recurring for Q2 periods live under section-qualified caption "Transportation"
for key, sec_re in (('rec', r'Supplemental Revenue Disclosure - Recurr'), ('non', r'Supplemental Revenue Disclosure - Non-re')):
    for i, p in enumerate(QP):
        x = [y for y in pred if y['source_doc'] == 'INFO_8K_Q2-FY2021' and y['fiscal_period'] == p and re.search(sec_re, y['section']) and y['line_item'] == 'Transportation']
        if x:
            c = ws.cell(QR[key], i + 2, float(x[0]['value'])); c.number_format = MONEY
            c.font = F_IN if x[0]['source_doc'].endswith(p) else F_CMP
q_fx('recsh', '  Recurring share of revenue [C]', lambda p, c: f'{c}{QR["rec"]}/{c}{QR["rev"]}' if qpick([r'^Recurring - Transportation$'], p) else None, PCT_C)
q_in('ebitda', 'Transportation Adjusted EBITDA [D]', [r'^Adjusted EBITDA - Transportation$', r'^Transportation Adjusted EBITDA$'], MONEY, True)
# annual columns: link revenue / Adj. EBITDA to the 10-K values in block A (in-sheet formula), not rounded deck figures
for key, akey in (('rev', 'a_rev'), ('ebitda', 'a_ebitda')):
    for p in ('FY2020', 'FY2021'):
        c = ws.cell(QR[key], QP.index(p) + 2, f'={L(SH_P.index(p) + 2)}{SHR[akey]}'); c.font = F_FX_B; c.number_format = MONEY
q_fx('m', 'Adjusted EBITDA margin [C]', lambda p, c: f'{c}{QR["ebitda"]}/{c}{QR["rev"]}', PCT_C)
q_in('mp', 'Adjusted EBITDA margin — as printed [D]', [r'^Adjusted EBITDA Margin % - Transportation$'], PCT_P)
q_in('org_r', 'Organic growth — recurring [D]', [r'^Recurring - Transportation organic growth'], PCT_P, src='Decks; Q2-FY20, Q3-FY20, FY20, Q3-FY21 printed in the deck\'s "Normalized" columns')
q_in('org_n', 'Organic growth — non-recurring [D]', [r'^Non-Recurring - Transportation organic growth'], PCT_P)
q_in('org_t', 'Organic growth — total [D]', [r'^Total - Transportation organic growth'], PCT_P)
q_fx('q4', 'Implied Q4-FY2021 revenue / Adj. EBITDA (FY2021 − 9M) [C]', lambda p, c: (f'{L(QP.index("FY2021")+2)}{QR["rev"]}-{L(QP.index("9M-FY2021")+2)}{QR["rev"]}' if p == 'Q1-FY2020' else
      (f'{L(QP.index("FY2021")+2)}{QR["ebitda"]}-{L(QP.index("9M-FY2021")+2)}{QR["ebitda"]}' if p == 'Q2-FY2020' else None)), MONEY,
      src='Col 1 = revenue, col 2 = Adj. EBITDA; Q4-FY2021 release/10-K quarterly data not on Quartr')
ci = {p: L(QP.index(p) + 2) for p in QP}
q_fx('chk1', 'CHECK recurring + non-recurring = revenue (0 = within ±1 rounding)', lambda p, c: f'IF(ABS({c}{QR["rec"]}+{c}{QR["non"]}-{c}{QR["rev"]})<=1,0,{c}{QR["rec"]}+{c}{QR["non"]}-{c}{QR["rev"]})' if qpick([r'^Recurring - Transportation$'], p) else None, MONEY, chk=True)
q_fx('chk2', 'CHECK FY2020 = sum of quarters (revenue; 0 = within ±2 rounding)', lambda p, c: f'IF(ABS({ci["Q1-FY2020"]}{QR["rev"]}+{ci["Q2-FY2020"]}{QR["rev"]}+{ci["Q3-FY2020"]}{QR["rev"]}+{ci["Q4-FY2020"]}{QR["rev"]}-{c}{QR["rev"]})<=2,0,1)' if p == 'FY2020' else None, MONEY, chk=True)
q_fx('chk3', 'CHECK 9M-FY2021 = Q1 + Q2 + Q3 (revenue & Adj. EBITDA; 0 = within ±1.5)', lambda p, c: f'IF(AND(ABS({ci["Q1-FY2021"]}{QR["rev"]}+{ci["Q2-FY2021"]}{QR["rev"]}+{ci["Q3-FY2021"]}{QR["rev"]}-{c}{QR["rev"]})<=1.5,ABS({ci["Q1-FY2021"]}{QR["ebitda"]}+{ci["Q2-FY2021"]}{QR["ebitda"]}+{ci["Q3-FY2021"]}{QR["ebitda"]}-{c}{QR["ebitda"]})<=1.5),0,1)' if p == '9M-FY2021' else None, MONEY, chk=True)
for note in ['Conflicts kept as printed (see predecessor_NOTES.md): Q4-FY2020 recurring organic growth 5% (Q2-FY21 deck) vs 6% (Q3-FY21 deck); A&D sale ≈$470m (FY2019 10-K) vs ≈$466m (10-Qs).',
             'Not on Quartr: IHS Markit quarterly releases/decks before Q2-FY2021 and anything for Q4-FY2021; quarterly segment data before Q1-FY2020 therefore unavailable. CARFAX / automotive / maritime revenue never printed in dollars.']:
    ws.cell(r, 1, note).font = F_NOTE; r += 1
