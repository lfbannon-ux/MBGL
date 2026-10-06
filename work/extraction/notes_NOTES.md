# notes.csv — extraction notes (agent #2, notes)

Sources (Quartr read_document, structured rows only; no page text copied):
- Form10A_2026-05-27 (doc 3603533): interim Q1-2026 condensed notes p.427–437; annual FY2023–FY2025 notes p.445–468 (F-25..F-47, Sched. II S-1); Separation agreements p.326–328; Capitalization p.331; pro forma + notes p.332–339; Description of Certain Indebtedness / contractual obligations p.362–365.
- 10Q_Q2-2026 (doc 3699447): statements p.4–8, notes p.9–18, MD&A liquidity/debt p.30–31.
- Form10 (3603535) p.532–535 read only to try to repair the corrupted tax table; it carries the identical corruption (no restatement seen between Form 10 and 10/A in goodwill/tax notes).

Period labels: Q1-2026 = 3M to 2026-03-31; Q2-2026 = 3M to 2026-06-30; 6M-xxxx = six months. Opening equity balance (Jan 1 2023) is labelled FY2022 / 2022-12-31.

## Footing checks (all pass unless listed under Flags)
- PCI roll-forward FY23–FY25, Q1-26, Q1-25, Q2-26, Q2-25: foot. PCI components tables (annual 3 yrs, Q1, Q2, 6M) foot to printed net; Q1+Q2 = 6M on every line.
- AOCI roll-forward foots. Goodwill by segment (5,912 + 2,933 = 8,845, flat FY23–FY25). Intangibles cost / accumulated amortization / net by class all foot (net FY25 3,789; FY24 4,085).
- DTA/DTL FY25 and FY24 foot (78 − 1,079 = (1,001); 60 − 1,156 = (1,096)).
- ETR 2025 percent column foots to 32.5%; 2024 (26.8%) and 2023 (27.3%) foot.
- 2025 tax provision (federal 110/(62), foreign 30/(12), state 56/(16), total 106) foots, and deferred total (90) ties to the CF deferred-tax line.
- Leases Q1-26 maturity table foots (28 − 3 = 25 = 6 + 19). Contractual obligations FY25 foot (109).
- Pro forma cash adjustment (1,997 − 16 − 3 − 1,900 = 78), APIC adjustment (= 9,927), capitalization (actual 11,810, PF 11,908) foot. 10-Q debt table: 2,000 − 19 = 1,981.
- Related-party tables foot. RSU roll 107 + 50 − 52 − 36 + 21 = 90 (thousand awards).

## Flags: corrupted or non-footing prints
1. **Tax provision table (p.455)** is badly corrupted for 2024/2023. I recorded only federal current (103/90), federal deferred (−64/−59), total federal 2024 (39) and totals (76/61). The foreign and state splits for 2024/2023 are not recorded. They are present as fragments only ("45 (26) 45", "56 56 51 (29)", "22 19") and can't be mapped reliably.
2. **ETR 2025 amounts:** "502 1.5" is read as $5 / 1.5% (UK valuation allowance; 5/326 = 1.5%). Amounts for Other foreign jurisdictions (0.7%) and cross-border (−0.1%) are not legible, so only percents are recorded (the implied amounts are 2 and 0, and the amount column then foots to 106). Mapping the leaf rows to the Canada and UK sub-captions is positional.
3. **Valuation allowance** is not legible in the DTA table. The implied (5) is confirmed by Schedule II p.468, which is recorded. DTA "Losses and other carryforwards" for FY24 is not printed (implied 0). There is a stray "226" in the text.
4. **UTB roll-forward (p.458):** the end balances 2/5/4 are confirmed by text. The begin 2023 (3), the additions 2024/2023 (1/1) and the 2025 settlements (−3) come from a positional read of corrupted text. 2025 does not foot: 5 − 3 = 2 only if 2025 additions = 0, which isn't printed. Interim 3/31/26 UTB = 3.
5. **Market Scan PPA:** liabilities print as 2 + 22 + 1 + 25 + 9 = 59, but the printed total is 39. Net assets 253 − 39 = 214 ties to the cash consideration, so the "Unearned revenue 22" is probably a corrupted "2". Recorded as printed.
6. **Annual lease maturity table (p.464)** is corrupted ("72222"). Only 2026 = 7 and PV = 18 are recorded (18 = 7 current + 11 non-current). The total undiscounted payments and imputed interest are not recorded. Contractual-obligations operating leases total 19 (p.365). ROU obtained in exchange ("— 2") could not be assigned to a year.
7. **2025 income-tax payments by jurisdiction (p.457)** are garbled ("25 15 1 35 $26"). Only the total (26) is recorded.
8. **Q1-26 related-party table:** the data-sharing expenses row prints nothing (total expenses = corporate allocations 28/22). It is treated as nil and not recorded.
9. **401(k):** 6M-2025 is printed as 12, but Q1-25 (7) + Q2-25 (6) = 13. Recorded as printed. 6M-2026 13 = 8 + 5.
10. **SBC:** the FY note shows expense 22/28/20 (2025/24/23), matching the PCI SBC component. The annual CF line looks like "22 22 28" in the flattened text, which may be a misalignment. Flag for the statements agent.
11. Form10A p.363 says the Company "expects that the outstanding loan *receivable* will be transferred by S&P Global to the Company" for the Canada Carfax Loan, which is a payable. Wording is kept as printed. The 10-Q confirms it was contributed 2026-06-25 and eliminated (non-cash 230).

## Restatements and differences between documents
- **Distribution to S&P Global:** Form 10/A pro forma (p.337) says approximately $1,900m. The 10-Q (p.12, p.18) says a $2.0bn dividend was paid. CF 6M-26: Senior Notes proceeds 1,986, net transfers to Parent (2,011). Q2 PCI cash pooling (1,886).
- **Shares:** the pro forma uses 295,077,160 (S&P shares at 2026-05-15). Actual is 294,821,320 (record date 2026-06-15), 1:1 ratio, distribution 2026-07-01.
- **RCF:** Form 10/A gives a 5-year tenor from the Initial Availability Date. The 10-Q gives maturity 2031-07-01 and adds a $250m accordion. Covenant: max total net leverage 3.50x, with a step-up to 4.00x for 4 quarters after a qualifying material acquisition. Margins: SOFR 1.0–1.625%, base rate 0–0.625%, ratings-based (Moody's/Fitch). Undrawn at 6/30/26.
- **Senior notes:** issued 2026-05-29; escrow released 2026-06-30; coupons Jun 15/Dec 15 starting 2026-12-15. Issuance costs about 16 and OID 3 (10-Q nets 19). Pro forma weighted rate 5.74%. Change-of-control put at 101%. Special mandatory redemption at 101% if escrow is not released by 2027-06-30.
- **Unrecognized RSU comp:** 18 at FY25 (1.12 yrs) vs 44 at Q1-26 (1.63 yrs), after 0.1m awards granted in Q1-26 at $441.68.
- **Not-yet-commenced leases:** 63 (FY25), 74 (Q1-26), 64 (Q2-26). Pro forma new corporate office leases: ROU 54 / liabilities 1 + 53.
- **Segment regime:** the 10-Q changes the segment measure to Adjusted EBITDA. That belongs to the SEG agent.

## Not disclosed
- No defined-benefit pension or OPEB plans; only the S&P-sponsored 401(k). Plan assets and liabilities moved to a Mobility plan in July 2026 (no amounts given).
- No deferred-revenue roll-forward table. Only the "revenue recognized from opening balance" figure (73 FY25, 38 Q1-26, 60 6M-26) and RPO (78 / 92 / 102, "majority within 12 months", with no timing buckets).
- No goodwill impairment and no goodwill change. No interim (10-Q) goodwill or intangible note.
- No OCI components other than FX translation. No reclassifications out of AOCI. No tax effect is shown.
- No TSA fee amounts are disclosed. The only figure is the pro forma incremental TSA cost (under 1 for Q1-26, 3 for FY25) and a term of up to 18 months.
- No numeric figure for legal contingencies; no accruals are quantified.
- No current/deferred split of the 2024/2023 provision by jurisdiction (corrupted). No 10-Q tax rate reconciliation. No ETR amount for the 0.7% and −0.1% lines.
- The 10-Q has no SBC award note, lease table or contractual-obligations update ("no material changes").
- The FX forward entered 2026-07-01 (USD/CAD, re the Canada Carfax Loan, terminating 2026-09-30) has no notional disclosed.
