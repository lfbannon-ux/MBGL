"""Uniform segment P&L (CARFAX / B2B / Corporate / Total) across all carve-out periods.
Rows are identical for every period; each cell is a printed value [D] from the period's primary document.
Add-backs are classified into a uniform bridge: Segment operating profit + amortization + depreciation + SBC + special items = Adjusted EBITDA.
Output: canonical/segment_pl.csv (+ map log)."""
import csv, re, os, collections
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(f'{W}/extraction/segments_kpi.csv')))
FY = ['FY2023', 'FY2024', 'FY2025']; Q1 = ['Q1-2025', 'Q1-2026']; Q2 = ['Q2-2025', 'Q2-2026', '6M-2025', '6M-2026']
A, F, Q = 'Form10A_2026-05-27', 'Form10_2026-05-07', '10Q_Q2-2026'
SEGS = ['CARFAX', 'B2B', 'Corporate', 'Total']
# concept -> list of (doc, periods, section regex, caption regex after "SEG: ")
SPEC = {
 'rev':      [(A, FY, r'^Audited Note 8 Segment and Geographic Information - operating results', r'^Revenue$'),
              (A, Q1, r'^Interim Note 7 Segment and Geographic Information - operating results', r'^Revenue$'),
              (Q, Q2, r'^Note 7 Segment and Geographic Information - segment table', r'^Revenue$')],
 'sub':      [(A, FY, r'^Audited Note 8 revenue disaggregated', r'^Subscription$'), (A, Q1, r'^Interim Note 7 revenue disaggregated', r'^Subscription$'),
              (Q, Q2, r'^Note 7 revenue disaggregated by revenue type', r'^Subscription$')],
 'nonsub':   [(A, FY, r'^Audited Note 8 revenue disaggregated', r'^Non - subscription$'), (A, Q1, r'^Interim Note 7 revenue disaggregated', r'^Non - subscription$'),
              (Q, Q2, r'^Note 7 revenue disaggregated by revenue type', r'^Non-subscription$')],
 'op':       [(A, FY + Q1, r'^MD&A Adjusted operating profit and Segment Adjusted EBITDA reconciliation', r'^Operating profit$'),
              (Q, Q2, r'^MD&A Non-GAAP reconciliation of Net income to Adjusted EBITDA by segment', r'^Operating profit \(GAAP\)$')],
 'amort':    [(A, FY + Q1, r'^MD&A Adjusted operating profit and Segment', r'^Amortization of intangibles$'),
              (Q, Q2, r'^MD&A Non-GAAP reconciliation of Net income', r'Amortization of intangibles$')],
 'dep':      [(A, FY + Q1, r'^MD&A Adjusted operating profit and Segment', r'^Depreciation$'),
              (Q, Q2, r'^MD&A Non-GAAP reconciliation of Net income', r'Depreciation$')],
 'sbc':      [(A, FY + Q1, r'^MD&A Adjusted operating profit and Segment', r'^Stock - based compensation$'),
              (F, Q1, r'^MD&A Adjusted operating profit and Segment', r'^Stock - based compensation$'),
              (Q, Q2, r'^MD&A Non-GAAP reconciliation of Net income', r'Stock-based compensation$')],
 'trans':    [(A, FY + Q1, r'^MD&A Adjusted operating profit and Segment', r'^Transaction costs$'),
              (Q, Q2, r'^MD&A Non-GAAP reconciliation of Net income', r'Transaction costs$')],
 'sev':      [(A, FY + Q1, r'^MD&A Adjusted operating profit and Segment', r'^(Employee severance charges|Other|Other \(1\))$'),
              (Q, Q2, r'^MD&A Non-GAAP reconciliation of Net income', r'Employee severance charges and other$')],
 'acq':      [(A, FY + Q1, r'^MD&A Adjusted operating profit and Segment', r'^(Acquisition integration costs|Acquisition and disposition - related costs|Legal settlement recovery|ELT transition costs)$')],
 'us':       [(A, FY + Q1, r'^MD&A Segment Results - (CARFAX|B2B) \((years|three months)', r'^U\.S\. revenue$'), (Q, Q2, r'^MD&A Segment Results - (CARFAX|B2B)$', r'^U\.S\. revenue$')],
 'intl':     [(A, FY + Q1, r'^MD&A Segment Results - (CARFAX|B2B) \((years|three months)', r'^International revenue$'), (Q, Q2, r'^MD&A Segment Results - (CARFAX|B2B)$', r'^International revenue$')],
 'oprel':    [(A, FY + Q1, r'^MD&A analysis by segment of operating-related and selling and general', r'^Operating-related expenses$')],
 'sg':       [(A, FY + Q1, r'^MD&A analysis by segment of operating-related and selling and general', r'^Selling and general expen')],
 'adj':      [(A, FY + Q1, r'^MD&A Adjusted operating profit and Segment', r'^Segment Adjusted EBITDA$'),
              (F, Q1, r'^MD&A Adjusted operating profit and Segment', r'^Segment Adjusted EBITDA$'),
              (Q, Q2, r'^MD&A Non-GAAP reconciliation of Net income', r'^Adjusted EBITDA$')],
}
out = {}; log = []
for concept, specs in SPEC.items():
    for doc, pers, secre, capre in specs:
        for r in rows:
            if r['source_doc'] != doc or r['fiscal_period'] not in pers or not re.search(secre, r['section']): continue
            li = re.sub(r'^(CARFAX|B2B) \(\d\)', r'\1', r['line_item'].strip()); li = re.sub(r'^Corporate Unallocated expense \(\d\)', 'Corporate', li); li = re.sub(r'^Total segment:', 'TotalSeg:', li)
            m = re.match(r'^(CARFAX|B2B|Corporate|Total): (.*)$', li)
            if not m or not re.search(capre, m.group(2).strip()): continue
            seg, per = m.group(1), r['fiscal_period']
            k = (concept, seg, per)
            v = float(r['value'])
            if concept in ('sev', 'acq'):   # multiple captions aggregate into one uniform bucket (sum of printed items) — logged
                if k in out and out[k]['doc'] == doc:
                    out[k]['value'] += v; out[k]['cap'] += ' + ' + m.group(2); log.append(f'SUM {k} += {v} ({m.group(2)})'); continue
            if k in out:
                if out[k]['doc'] != doc and doc == F:  # Form 10 only fills gaps the 10/A text dropped
                    continue
                if abs(out[k]['value'] - v) > 1e-9 and out[k]['doc'] == doc:
                    log.append(f'DUPLICATE-DIFF {k}: kept {out[k]["value"]} ({out[k]["page"]}), saw {v} p{r["page"]}')
                continue
            out[k] = dict(value=v, doc=doc, page=r['page'], cap=m.group(2))
            if doc == F: log.append(f'GAP-FILL from Form 10 (10/A text illegible): {k} = {v} p{r["page"]}')
with open(f'{W}/canonical/segment_pl.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['concept', 'segment', 'period', 'value', 'source_doc', 'page', 'source_caption'])
    for (c, s, p), d in sorted(out.items()): w.writerow([c, s, p, d['value'], d['doc'], d['page'], d['cap']])
open(f'{W}/canonical/segment_pl_log.txt', 'w').write('\n'.join(log) + '\n')
PER = FY + ['Q1-2025', 'Q2-2025', '6M-2025', 'Q1-2026', 'Q2-2026', '6M-2026']
for seg in SEGS:
    print('==', seg)
    for c in SPEC:
        print(f'  {c:7}', ' '.join(f"{out[(c, seg, p)]['value']:7.0f}" if (c, seg, p) in out else '      .' for p in PER))
print(len(out), 'cells;', len(log), 'log lines')
