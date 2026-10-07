# ---------------------------------------------------------------- Segment P&L — uniform rows across every carve-out period (exec'd from build_workbook.py)
spl = {}
for x in csv.DictReader(open(f'{W}/canonical/segment_pl.csv')):
    spl[(x['concept'], x['segment'], x['period'])] = (float(x['value']), f"{x['source_doc']} p{x['page']}")
ws = wb.create_sheet('Segment P&L'); COLS['Segment P&L'] = FLOW_P
setup(ws, 'Segment P&L — uniform layout, CARFAX / B2B / Corporate (carve-out, as originally reported)',
      'Same rows in every period. Uniform Adjusted EBITDA = segment operating profit + amortization + depreciation + SBC + special items (all printed). FY & Q1: Form 10/A; Q2 & 6M: 10-Q. '
      'Company Adj. EBITDA definition changed (10 → 6 exclusions) at Q2-2026; the uniform build re-expresses every period on one basis. Blue = as filed; black = formula; green = cross-sheet.', len(FLOW_P) + 1)
header(ws, 4, [PLAB[p] for p in FLOW_P] + ['Source / note'])
prior_p = {'FY2024': 'FY2023', 'FY2025': 'FY2024', 'Q1-2026': 'Q1-2025', 'Q2-2026': 'Q2-2025', '6M-2026': '6M-2025'}
SR = {}
def col(p): return L(FLOW_P.index(p) + 2)
def s_in(seg, concept, label, fmt=MONEY, bold=False, note=''):
    global r
    ws.cell(r, 1, label).font = F_SEC if bold else F_BASE
    srcs = set()
    for p in FLOW_P:
        if (concept, seg, p) in spl:
            v, sref = spl[(concept, seg, p)]; srcs.add(sref.split(' ')[0])
            c = ws.cell(r, FLOW_P.index(p) + 2, v); c.font = F_IN_B if bold else F_IN; c.number_format = fmt
    ws.cell(r, len(FLOW_P) + 2, (note + ' ' if note else '') + '; '.join(sorted(srcs))).font = F_NOTE
    SR[(seg, concept)] = r; r += 1
def s_fx(seg, key, label, fn, fmt=MONEY, bold=False, note='[C]', chk=None):
    global r
    ws.cell(r, 1, label).font = F_NOTE if chk else (F_FX_B if bold else F_FX)
    for p in FLOW_P:
        if chk is not None and not chk(p):
            ws.cell(r, FLOW_P.index(p) + 2, 'n/a').font = F_NOTE; continue
        e = fn(p, col(p))
        if e is None: continue
        c = ws.cell(r, FLOW_P.index(p) + 2, '=' + e); c.number_format = fmt
        c.font = (F_X if '!' in e else F_FX) if chk else ((F_X_B if '!' in e else F_FX_B) if bold else (F_X if '!' in e else F_FX))
    ws.cell(r, len(FLOW_P) + 2, note).font = F_NOTE
    if chk is not None:
        ws.cell(r, MARK, 'CHECK')
        for cc in range(1, len(FLOW_P) + 2): ws.cell(r, cc).fill = FILL_CHK
    SR[(seg, key)] = r; r += 1
def g(seg, key):  # growth vs prior comparable period
    return lambda p, c: f'{c}{SR[(seg, key)]}/{col(prior_p[p])}{SR[(seg, key)]}-1' if p in prior_p else None
ADDBACKS = [('amort', '+ Amortization of acquired intangibles [D]'), ('dep', '+ Depreciation [D]'), ('sbc', '+ Stock-based compensation [D]'),
            ('trans', '+ Transaction (separation) costs [D]'), ('sev', '+ Employee severance & other [D]'), ('acq', '+ Acquisition / integration / legal recovery / ELT [D]')]
GAPS = {('CARFAX', 'FY2025'): 'segment split of FY2025 "Other" ($2m total) not legible',
        ('Corporate', 'FY2025'): 'segment split of FY2025 "Other" ($2m total) not legible',
        ('B2B', 'Q1-2026'): 'B2B Q1-2026 depreciation illegible in Form 10 and 10/A'}
r = 5
for seg, title in [('CARFAX', 'CARFAX segment'), ('B2B', 'B2B segment (Marketing & Sales; Strategy & Planning)'), ('Corporate', 'Corporate (unallocated)')]:
    section(ws, r, title, len(FLOW_P) + 1); r += 1
    if seg != 'Corporate':
        s_in(seg, 'rev', 'Revenue [D]', bold=True)
        s_fx(seg, 'rev_g', '  Revenue growth y/y [C]', g(seg, 'rev'), PCT_C)
        s_in(seg, 'sub', '  Subscription [D]'); s_in(seg, 'nonsub', '  Non-subscription [D]')
        s_fx(seg, 'sub_sh', '  Subscription share [C]', lambda p, c, s=seg: f'{c}{SR[(s, "sub")]}/{c}{SR[(s, "rev")]}', PCT_C)
        s_in(seg, 'us', '  U.S. [D]'); s_in(seg, 'intl', '  International [D]')
        s_fx(seg, 'intl_g', '  International growth y/y [C]', g(seg, 'intl'), PCT_C)
        s_in(seg, 'oprel', 'Memo: operating-related expenses (FY & Q1 only — not split in 10-Q) [D]')
    s_in(seg, 'sg', 'Memo: selling & general expenses (FY & Q1 only) [D]')
    s_in(seg, 'op', 'Segment operating profit (GAAP) [D]', bold=True)
    if seg != 'Corporate':
        s_fx(seg, 'op_m', '  Operating margin [C]', lambda p, c, s=seg: f'{c}{SR[(s, "op")]}/{c}{SR[(s, "rev")]}', PCT_C)
    for k, lab in ADDBACKS: s_in(seg, k, '  ' + lab)
    s_fx(seg, 'adj_b', 'Adjusted EBITDA — uniform build [C]', lambda p, c, s=seg: '+'.join(f'{c}{SR[(s, k)]}' for k in ['op'] + [a for a, _ in ADDBACKS]), MONEY, True,
         'Operating profit + all printed add-backs')
    s_in(seg, 'adj', 'Adjusted EBITDA — as reported by the company [D]', note='FY/Q1: Form 10/A "Segment Adjusted EBITDA" (10-exclusion def.); Q2/6M: 10-Q (6-exclusion def.).')
    s_fx(seg, 'chk', 'CHECK uniform build − reported', lambda p, c, s=seg: f'{c}{SR[(s, "adj_b")]}-{c}{SR[(s, "adj")]}',
         note='n/a: ' + '; '.join(sorted({v for (sg, p), v in GAPS.items() if sg == seg})) if any(sg == seg for sg, _ in GAPS) else '0 = bridge ties', chk=lambda p, s=seg: (s, p) not in GAPS)
    if seg != 'Corporate':
        s_fx(seg, 'adj_m', '  Adjusted EBITDA margin [C]', lambda p, c, s=seg: f'{c}{SR[(s, "adj")]}/{c}{SR[(s, "rev")]}', PCT_C, True)
        s_fx(seg, 'adj_g', '  Adjusted EBITDA growth y/y [C]', g(seg, 'adj'), PCT_C)
        s_fx(seg, 'inc', '  Incremental Adj. EBITDA margin (Δ EBITDA / Δ revenue) [C]',
             lambda p, c, s=seg: f'({c}{SR[(s, "adj")]}-{col(prior_p[p])}{SR[(s, "adj")]})/({c}{SR[(s, "rev")]}-{col(prior_p[p])}{SR[(s, "rev")]})' if p in prior_p else None, PCT_C)
        s_fx(seg, 'cost', '  Cash operating costs = revenue − Adj. EBITDA [C]', lambda p, c, s=seg: f'{c}{SR[(s, "rev")]}-{c}{SR[(s, "adj")]}', MONEY)
        s_fx(seg, 'da_m', '  D&A % revenue [C]', lambda p, c, s=seg: f'({c}{SR[(s, "amort")]}+{c}{SR[(s, "dep")]})/{c}{SR[(s, "rev")]}', PCT_C)
        s_fx(seg, 'sbc_m', '  SBC % revenue [C]', lambda p, c, s=seg: f'{c}{SR[(s, "sbc")]}/{c}{SR[(s, "rev")]}', PCT_C)
    r += 1
# Total = sum of segments for every uniform row
section(ws, r, 'Total company = CARFAX + B2B + Corporate (formulas)', len(FLOW_P) + 1); r += 1
def tsum(key, segs=('CARFAX', 'B2B', 'Corporate')):
    return lambda p, c: '+'.join(f'{c}{SR[(s, key)]}' for s in segs if (s, key) in SR)
s_fx('Total', 'rev', 'Revenue [C]', tsum('rev'), MONEY, True)
s_fx('Total', 'rev_g', '  Revenue growth y/y [C]', g('Total', 'rev'), PCT_C)
for k, lab in [('sub', '  Subscription'), ('nonsub', '  Non-subscription'), ('us', '  U.S.'), ('intl', '  International')]:
    s_fx('Total', k, lab + ' [C]', tsum(k))
s_fx('Total', 'op', 'Operating profit [C]', tsum('op'), MONEY, True)
s_fx('Total', 'op_m', '  Operating margin [C]', lambda p, c: f'{c}{SR[("Total", "op")]}/{c}{SR[("Total", "rev")]}', PCT_C)
for k, lab in ADDBACKS: s_fx('Total', k, '  ' + lab.replace('[D]', '[C]'), tsum(k))
s_fx('Total', 'adj_b', 'Adjusted EBITDA — uniform build [C]', tsum('adj_b'), MONEY, True)
s_fx('Total', 'adj', 'Adjusted EBITDA — sum of reported segments [C]', tsum('adj'), MONEY)
s_fx('Total', 'adj_m', '  Adjusted EBITDA margin (reported segments) [C]', lambda p, c: f'{c}{SR[("Total", "adj")]}/{c}{SR[("Total", "rev")]}', PCT_C, True)
s_fx('Total', 'adj_g', '  Adjusted EBITDA growth y/y [C]', g('Total', 'adj'), PCT_C)
s_fx('Total', 'cost', '  Cash operating costs [C]', lambda p, c: f'{c}{SR[("Total", "rev")]}-{c}{SR[("Total", "adj")]}')
s_fx('Total', 'mix', '  CARFAX share of revenue [C]', lambda p, c: f'{c}{SR[("CARFAX", "rev")]}/{c}{SR[("Total", "rev")]}', PCT_C)
s_fx('Total', 'mixe', '  CARFAX share of segment Adj. EBITDA (before Corporate) [C]', lambda p, c: f'{c}{SR[("CARFAX", "adj")]}/({c}{SR[("CARFAX", "adj")]}+{c}{SR[("B2B", "adj")]})', PCT_C)
r += 1
section(ws, r, 'Reconciliation to reported totals', len(FLOW_P) + 1); r += 1
s_in('Total', 'adj', 'Company-reported total Adjusted EBITDA [D]')
SR[('Total', 'adj_rep')] = SR[('Total', 'adj')]; SR[('Total', 'adj')] = SR[('Total', 'adj')]  # keep reference to sum row below
s_fx('Total', 'rec_adj', 'Sum of reported segments − company-reported total [C] (printed-table footing differences)',
     lambda p, c: f'{c}{r - 0 - 0}' if False else None, MONEY)
r -= 1  # replace the placeholder row with a real formula
ws.cell(r, 1, 'Sum of reported segments − company-reported total [C] (printed footing: FY23 597 vs 598; FY24 659 vs 658)').font = F_FX
sum_row = [rr for (sg, k), rr in SR.items() if sg == 'Total' and k == 'adj_m'][0] - 1
for p in FLOW_P:
    c = ws.cell(r, FLOW_P.index(p) + 2, f'={col(p)}{sum_row}-{col(p)}{SR[("Total", "adj_rep")]}'); c.number_format = MONEY; c.font = F_FX
r += 1
s_fx('Total', 'chk_rev', 'CHECK revenue = IS revenue', lambda p, c: f"{c}{SR[('Total', 'rev')]}-'IS'!{xcol('IS', p)}{REF[('IS', 'IS.revenue')]}", chk=lambda p: True)
s_fx('Total', 'chk_op', 'CHECK operating profit = IS operating profit', lambda p, c: f"{c}{SR[('Total', 'op')]}-'IS'!{xcol('IS', p)}{REF[('IS', 'IS.op_f')]}", chk=lambda p: True)
s_fx('Total', 'chk_sub', 'CHECK subscription + non-subscription = revenue (segments)', lambda p, c: f"{c}{SR[('Total', 'sub')]}+{c}{SR[('Total', 'nonsub')]}-{c}{SR[('Total', 'rev')]}", chk=lambda p: True)
s_fx('Total', 'chk_geo', 'CHECK U.S. + International = revenue (segments)', lambda p, c: f"{c}{SR[('Total', 'us')]}+{c}{SR[('Total', 'intl')]}-{c}{SR[('Total', 'rev')]}", chk=lambda p: True)
for seg in ('CARFAX', 'B2B', 'Corporate'):
    s_fx(seg, 'chk6m', f'CHECK {seg}: 6M = Q1 + Q2 (operating profit and reported Adj. EBITDA, across the definition change)',
         lambda p, c, s=seg: f'ABS({c}{SR[(s, "op")]}-{col("Q1-"+p[3:])}{SR[(s, "op")]}-{col("Q2-"+p[3:])}{SR[(s, "op")]})+ABS({c}{SR[(s, "adj")]}-{col("Q1-"+p[3:])}{SR[(s, "adj")]}-{col("Q2-"+p[3:])}{SR[(s, "adj")]})',
         chk=lambda p: p.startswith('6M'))
r += 1
for note in ['Uniform basis: every period is expressed as segment operating profit plus the same add-back categories, so the definition change in Q2-2026 (10 → 6 company exclusions) does not break the series — in these periods the excluded items are fully captured by the add-back rows.',
             'Special items are grouped: "transaction" = separation costs; "severance & other" incl. the Q1-2025 "Other" and FY2025 total "Other (1)"; "acquisition / integration / legal recovery / ELT" = FY2023–25 Form 10/A items (legal recovery and ELT benefit are negative).',
             'Gaps (no derivation): FY2025 CARFAX/Corporate split of a $2m "Other" item; Q1-2026 B2B depreciation (≈$1m implied, not recorded). Corporate has no revenue, amortization, depreciation or SBC in any period.',
             'Q2 & 6M segment operating-related / selling & general split is not disclosed in the 10-Q (segment "expenses" there exclude D&A, SBC and special items) — memo rows left blank.']:
    ws.cell(r, 1, note).font = F_NOTE; r += 1
ws.column_dimensions[L(len(FLOW_P) + 2)].width = 48
