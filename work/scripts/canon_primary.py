"""Phase 4 — guarded canonical transform for primary statements (IS/CI/BS/CF).
Sources: Form 10/A statements (annual + Q1) and 10-Q Q2-2026 statements (Q2, 6M, 6/30/26 BS + comparatives).
Guards: collision (same key/period, different value -> ABORT; identical -> absorbed + logged);
leftover (every source row must map or be explicitly EXCLUDED with a reason)."""
import csv, re, sys, collections, os
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(f'{W}/extraction/statements.csv')))

PRIMARY_DOCS = {'Form10A_2026-05-27', '10Q_Q2-2026'}
# (statement, section regex, caption regex) -> canonical key. Order matters only for documentation.
MAP = [
 # Income statement
 ('IS', r'Statements of (Income|Operations)', r'^Revenue$', 'IS.revenue'),
 ('IS', r'Statements of (Income|Operations)', r'^Operating-related expenses$', 'IS.oprel'),
 ('IS', r'Statements of (Income|Operations)', r'^Selling and general expenses$', 'IS.sg'),
 ('IS', r'Statements of (Income|Operations)', r'^Depreciation$', 'IS.dep'),
 ('IS', r'Statements of (Income|Operations)', r'^Amortization of intangibles$', 'IS.amort'),
 ('IS', r'Statements of (Income|Operations)', r'^Total expenses$', 'IS.totexp'),
 ('IS', r'Statements of (Income|Operations)', r'^Operating profit$', 'IS.op'),
 ('IS', r'Statements of (Income|Operations)', r'^Other income, net$', 'IS.other'),
 ('IS', r'Statements of (Income|Operations)', r'^Interest expense, net$', 'IS.int'),
 ('IS', r'Statements of (Income|Operations)', r'^Income before (taxes on income|provision for income taxes)$', 'IS.pbt'),
 ('IS', r'Statements of (Income|Operations)', r'^Provision for (taxes on income|income taxes)$', 'IS.tax'),
 ('IS', r'Statements of (Income|Operations)', r'^Net income$', 'IS.ni'),
 ('IS', r'Statements of (Income|Operations)', r'Net income per common share: Basic', 'IS.eps_b'),
 ('IS', r'Statements of (Income|Operations)', r'Net income per common share: Diluted', 'IS.eps_d'),
 ('IS', r'Statements of (Income|Operations)', r'Weighted.*[Bb]asic', 'IS.wso_b'),
 ('IS', r'Statements of (Income|Operations)', r'Weighted.*[Dd]iluted', 'IS.wso_d'),
 ('IS', r'Comprehensive Income', r'^Net income$', 'CI.ni'),
 ('IS', r'Comprehensive Income', r'^Foreign currency translation adjustments$', 'CI.fx'),
 ('IS', r'Comprehensive Income', r'^Comprehensive income$', 'CI.ci'),
 # Balance sheet
 ('BS', r'Balance Sheets', r'^Cash and cash equivalents$', 'BS.cash'),
 ('BS', r'Balance Sheets', r'^Due from related parties[,\s-]+current$', 'BS.duefrom_c'),
 ('BS', r'Balance Sheets', r'^Accounts receivable, net', 'BS.ar'),
 ('BS', r'Balance Sheets', r'^Prepaid and other current assets$', 'BS.prepaid'),
 ('BS', r'Balance Sheets', r'^Total current assets$', 'BS.tca'),
 ('BS', r'Balance Sheets', r'^Buildings and leasehold improvements$', 'BS.ppe_bldg'),
 ('BS', r'Balance Sheets', r'^Equipment and furniture$', 'BS.ppe_eq'),
 ('BS', r'Balance Sheets', r'^Total property and equipment$', 'BS.ppe_gross'),
 ('BS', r'Balance Sheets', r'^Less: accumulated depreciation$', 'BS.ppe_acc'),
 ('BS', r'Balance Sheets', r'^Property and equipment, net', 'BS.ppe_net'),
 ('BS', r'Balance Sheets', r'^Right of use assets$', 'BS.rou'),
 ('BS', r'Balance Sheets', r'^Goodwill$', 'BS.gw'),
 ('BS', r'Balance Sheets', r'^Other intangible assets[,\s-]+net$', 'BS.intang'),
 ('BS', r'Balance Sheets', r'^Due from related parties\s*[–-]\s*non-current$', 'BS.duefrom_nc'),
 ('BS', r'Balance Sheets', r'^Other non-current assets$', 'BS.onca'),
 ('BS', r'Balance Sheets', r'^Total assets$', 'BS.ta'),
 ('BS', r'Balance Sheets', r'^Accounts payable$', 'BS.ap'),
 ('BS', r'Balance Sheets', r'^Due to related parties\s*-\s*current$', 'BS.dueto_c'),
 ('BS', r'Balance Sheets', r'^Accrued compensation', 'BS.accomp'),
 ('BS', r'Balance Sheets', r'^Unearned revenue$', 'BS.unearned'),
 ('BS', r'Balance Sheets', r'^Other current liabilities$', 'BS.ocl'),
 ('BS', r'Balance Sheets', r'^Total current liabilities$', 'BS.tcl'),
 ('BS', r'Balance Sheets', r'^Long-term debt$', 'BS.ltd'),
 ('BS', r'Balance Sheets', r'^(Lease liabilities - non-current|Operating lease liabilities)$', 'BS.lease_nc'),
 ('BS', r'Balance Sheets', r'^Deferred tax liability', 'BS.dtl'),
 ('BS', r'Balance Sheets', r'^Due to related parties\s*[–-]\s*non-current$', 'BS.dueto_nc'),
 ('BS', r'Balance Sheets', r'^Other non-current liabilities$', 'BS.oncl'),
 ('BS', r'Balance Sheets', r'^Total liabilities$', 'BS.tl'),
 ('BS', r'Balance Sheets', r'^Parent company investment$', 'BS.npi'),
 ('BS', r'Balance Sheets', r'^Accumulated other comprehensive', 'BS.aoci'),
 ('BS', r'Balance Sheets', r'^Total equity$', 'BS.te'),
 ('BS', r'Balance Sheets', r'^Total liabilities and equity$', 'BS.tle'),
 # Cash flow
 ('CF', r'Cash Flows - Operating', r'^Net income$', 'CF.ni'),
 ('CF', r'Cash Flows - Operating', r'^Depreciation$', 'CF.dep'),
 ('CF', r'Cash Flows - Operating', r'^Amortization of intangibles$', 'CF.amort'),
 ('CF', r'Cash Flows - Operating', r'^Provision for losses on accounts receivable$', 'CF.prov'),
 ('CF', r'Cash Flows - Operating', r'^Deferred income taxes$', 'CF.deftax'),
 ('CF', r'Cash Flows - Operating', r'^Stock-based compensation$', 'CF.sbc'),
 ('CF', r'Cash Flows - Operating', r'^Restructuring and other$', 'CF.restr'),
 ('CF', r'Cash Flows - Operating', r'^Other$', 'CF.other'),
 ('CF', r'Cash Flows - Operating', r'^Accounts receivable$', 'CF.wc_ar'),
 ('CF', r'Cash Flows - Operating', r'^Due from related parties$', 'CF.wc_duefrom'),
 ('CF', r'Cash Flows - Operating', r'^Prepaid and other current assets$', 'CF.wc_prepaid'),
 ('CF', r'Cash Flows - Operating', r'^Accounts payable and accrued expenses$', 'CF.wc_ap'),
 ('CF', r'Cash Flows - Operating', r'^Due to related parties$', 'CF.wc_dueto'),
 ('CF', r'Cash Flows - Operating', r'^Unearned revenue$', 'CF.wc_unearned'),
 ('CF', r'Cash Flows - Operating', r'^Other current liabilities$', 'CF.wc_ocl'),
 ('CF', r'Cash Flows - Operating', r'^Net change in other assets and liabilities$', 'CF.wc_other'),
 ('CF', r'Cash Flows - Operating', r'^Cash provided by operating activities$', 'CF.cfo'),
 ('CF', r'Cash Flows - Investing', r'^Capital expenditures$', 'CF.capex'),
 ('CF', r'Cash Flows - Investing', r'^Acquisitions, net of cash acquired$', 'CF.acq'),
 ('CF', r'Cash Flows - Investing', r'^Proceeds from loan to related parties$', 'CF.loan_rp'),
 ('CF', r'Cash Flows - Investing', r'^Proceeds from dispositions$', 'CF.disp'),
 ('CF', r'Cash Flows - Investing', r'^Purchases of equity investments$', 'CF.eqinv'),
 ('CF', r'Cash Flows - Investing', r'^Cash used for investing activities$', 'CF.cfi'),
 ('CF', r'Cash Flows - Financing', r'^Proceeds from issuance of Senior Notes$', 'CF.notes'),
 ('CF', r'Cash Flows - Financing', r'^Net transfers to Parent$', 'CF.parent'),
 ('CF', r'Cash Flows - Financing', r'^Payments related to loan from related parties$', 'CF.loan_pay'),
 ('CF', r'Cash Flows - Financing', r'^Contingent consideration payments$', 'CF.contingent'),
 ('CF', r'Cash Flows - Financing', r'^Cash (provided by \(used for\)|used for) financing activities$', 'CF.cff'),
 ('CF', r'Cash Flows( - Total)?$', r'^Effect of exchange rate changes on cash$', 'CF.fx'),
 ('CF', r'Cash Flows( - Total)?$', r'^Net change in cash', 'CF.chg'),
 ('CF', r'Cash Flows( - Total)?$', r'^Cash.* at beginning of', 'CF.beg'),
 ('CF', r'Cash Flows( - Total)?$', r'^Cash.* at end of', 'CF.end'),
 ('CF', r'Supplemental$', r'Interest$', 'CF.sup_int'),
 ('CF', r'Supplemental$', r'Income taxes$', 'CF.sup_tax'),
 ('CF', r'Supplemental non-cash', r'Canada Carfax Loan', 'CF.sup_canloan'),
 ('CF', r'Supplemental non-cash', r'Accrued debt issuance costs', 'CF.sup_debtcost'),
]
# Fallbacks: MD&A cash-flow overview fills ONLY gaps (statement page text unreadable). Logged.
FALLBACK = [('CF', r'MD&A Cash Flow Overview', r'^Investing activities$', 'CF.cfi'),
            ('CF', r'MD&A Cash Flow Overview', r'^Financing activities$', 'CF.cff')]
EXCLUDE = [  # (doc regex, statement, section regex, reason)
 (r'.', 'IS', r'SUMMARY', 'Summary table duplicates the statements (verified equal by extraction agent)'),
 (r'.', 'BS', r'SUMMARY', 'Summary table duplicates the statements'),
 (r'.', 'CF', r'SUMMARY', 'Summary table duplicates the statements'),
 (r'.', 'CF', r'MD&A Free cash flow', 'Non-GAAP FCF table -> Adjusted/Non-GAAP tab'),
 (r'.', 'CF', r'MD&A Cash Flow Overview', 'Duplicate presentation; used only as logged gap-fill fallback'),
 (r'.', 'EQ', r'.', 'Equity roll-forward -> Equity tab (separate build)'),
 (r'.', 'NONGAAP', r'.', 'Non-GAAP -> Adjusted/Non-GAAP tab'),
 (r'.', 'PROFORMA', r'.', 'Pro forma -> own tab; never merged with historical'),
]
period_end = {}
out = {}; log = []; leftovers = []; cmap = []
def norm(s): return re.sub(r'\s+', ' ', s).strip()
for r in rows:
    doc, st, sec, cap = r['source_doc'], r['statement'], r['section'], norm(r['line_item'])
    if doc not in PRIMARY_DOCS:
        continue
    key = None
    for (s, secre, capre, k) in MAP:
        if st == s and re.search(secre, sec) and re.search(capre, cap):
            key = k; break
    if key is None:
        ex = [x for x in EXCLUDE if re.search(x[0], doc) and x[1] == st and re.search(x[2], sec)]
        if ex:
            cmap.append((doc, st, sec, cap, 'EXCLUDE', ex[0][3])); continue
        leftovers.append((doc, st, sec, cap, r['fiscal_period'])); continue
    cmap.append((doc, st, sec, cap, key, ''))
    p = r['fiscal_period']; period_end[p] = r['period_end']
    v = float(r['value'])
    if (key, p) in out:
        prev = out[(key, p)]
        if abs(prev['value'] - v) > 1e-9:
            sys.exit(f'COLLISION ABORT {key} {p}: {prev} vs {doc} p{r["page"]} {v}')
        log.append(f'absorbed identical {key} {p}={v} from {doc} p{r["page"]} (kept {prev["doc"]} p{prev["page"]})')
        continue
    out[(key, p)] = dict(value=v, doc=doc, page=r['page'], cap=cap, unit=r['unit'])
# fallbacks
for r in rows:
    if r['source_doc'] not in PRIMARY_DOCS: continue
    for (s, secre, capre, k) in FALLBACK:
        if r['statement'] == s and re.search(secre, r['section']) and re.search(capre, norm(r['line_item'])):
            p = r['fiscal_period']
            if (k, p) not in out:
                out[(k, p)] = dict(value=float(r['value']), doc=r['source_doc'], page=r['page'], cap=norm(r['line_item']) + ' [MD&A fallback]', unit=r['unit'])
                log.append(f'FALLBACK {k} {p}={r["value"]} from MD&A Cash Flow Overview {r["source_doc"]} p{r["page"]} (statement cell unreadable in Quartr text)')
if leftovers:
    for l in leftovers: print('LEFTOVER', l)
    sys.exit('LEFTOVER ABORT')
os.makedirs(f'{W}/canonical', exist_ok=True)
with open(f'{W}/canonical/primary.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['canon_key', 'period', 'period_end', 'value', 'unit', 'source_doc', 'page', 'source_caption'])
    for (k, p), d in sorted(out.items()):
        w.writerow([k, p, period_end.get(p, ''), d['value'], d['unit'], d['doc'], d['page'], d['cap']])
with open(f'{W}/canonical/primary_caption_map.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['source_doc', 'statement', 'section', 'caption', 'canon_key_or_EXCLUDE', 'reason'])
    for c in sorted(set(cmap)): w.writerow(c)
with open(f'{W}/canonical/primary_merge_log.txt', 'w') as f:
    f.write('\n'.join(log) + '\n')
print('canonical cells', len(out), '| absorbed/fallback log lines', len(log), '| caption map', len(set(cmap)))
