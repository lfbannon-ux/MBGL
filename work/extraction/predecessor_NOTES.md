# predecessor_NOTES — SEG_PRED (eras P1 and P0)

Output: `extraction/predecessor.csv` (597 rows, statement=SEG_PRED). Source: Quartr `read_document`, structured rows only. Pages are Quartr page numbers.
Each 10-K's comparative columns are kept as separate rows under that 10-K's `source_doc`. Nothing is substituted across documents.
Text rows (`unit=text`) are short summaries or quotes of no more than 2 sentences.

## Source map
| source_doc | Quartr id | Key pages |
|---|---|---|
| SPGI_10K_FY2025 | 2802490 | 43 (expenses by segment), 60–62 (Mobility MD&A + spin), 118 (restructuring), 119–123 (Note 12) |
| SPGI_10K_FY2024 | 1839960 | 40–41, 56–57, 113–117 |
| SPGI_10K_FY2023 | 318736 | 43, 58–59, 117–121 |
| SPGI_10K_FY2022 | 214376 | 42, 57–58, 118–121 |
| INFO_10K_FY2021 | 223420 | 13–14, 73–79, 137–139 (Note 20) |
| INFO_10K_FY2020 | 223421 | 12, 78–84, 145–146 |
| INFO_10K_FY2019 | 223422 | 9–10, 40–43, 63, 80–81 |
| INFO_10K_FY2018 | 223424 | 9–10, 42–44, 64, 84–85 |
| INFO_10K_FY2017 | 223425 | 9, 40–43, 83 |
| INFO_10K_FY2016 | 223426 | 9–10, 37–40, 60, 80, 83–84 |

## P1: S&P Global "Mobility" segment (Dec FYE)
- **Scope:** automotive only. Business lines are Dealer (CARFAX, automotiveMastermind, Market Scan), Manufacturing (forecasts, Polk-heritage marketing and recall) and Financial (lenders and insurers). These lines are first named in the FY2023 10-K. The FY2022 10-K gives no line breakdown.
- **Inclusion date:** FY2022 covers only Mar 1–Dec 31, 2022 ("acquired in connection with the merger with IHS Markit on February 28, 2022"). FY2022 is therefore a ~10-month period. The FY2023 +30% growth is printed but not organic.
- **Measure:** segment operating profit is GAAP-based and after D&A. It includes amortization of acquired intangibles: $241m (2022), $301m (2023), $303m (2024 and 2025). It also includes severance, merger costs and similar items, listed in footnotes and captured as "Operating profit includes:" rows. SPGI prints no adjusted segment profit in the 10-K.
- **ASU 2023-07:** first presented in the FY2024 10-K, with 2022–2023 recast as "segment expenses" and "other segment items". This is a presentation change only; revenue and OP are unchanged.
  - Tie-out: revenue − segment expenses − other segment items = OP for 2022–2025.
  - Tie-out: operating-related + S&G + D&A = revenue − OP in every doc.
  - Other segment items ≈ intangibles amortization + listed special items, within ±1 rounding (2023: 315 vs 316; 2022: 234 vs 235).
- **Restatement (FY2024 → FY2025 10-K):** the 2024 Mobility operating-related/S&G split moved from 469/511 to 487/493. The total of 980 is unchanged. This was a company-wide reclassification (MI and Ratings moved too). Both versions are kept.
  - No other Mobility figure changed between consecutive 10-Ks: revenue, sub/non-sub, US/Intl, OP, D&A, capex and total assets all agree.
  - The FY2024 doc lacks a 2022 restructuring row. The FY2022 plan Mobility charge of $2m comes from the FY2023 doc.
- **Wording drift:** "majority of the top North American dealerships" (FY2025) vs "majority of North American dealerships" (earlier). Non-subscription is described as "Transactional sales" (FY2025) vs "One-time transactional sales" (earlier). In the FY2025 10-K, Commodity Insights is renamed Energy (not Mobility).
- **Acquisitions and divestitures:** Market Scan (Feb-2023, not material). No Mobility disposition is printed. FY2025 has $7m of "disposition-related costs" in Mobility OP, with no transaction named.
- **Spin:** "On April 29, 2025, we announced that our Board of Directors decided to pursue a full separation of our Mobility segment…" It is described as tax-free, with completion expected mid-2026 (FY2025 p62).
- **Dashes:** Mobility intersegment revenue is printed "-" and is recorded as 0. 2021 and 2020 columns printed "$ -" (pre-merger) were not recorded.

## P0: IHS Markit "Transportation" segment (Nov 30 FYE)
- **Scope is broader than Mobility:**
  - Automotive was about 80% of segment revenue (FY2016/17), about 84% (FY2018), approximately 85% (FY2019) and "more than 90 percent" (FY2020/21).
  - Maritime & Trade was included throughout.
  - Aerospace, Defense & Security (Jane's) was included until its sale on Dec 2, 2019. The deal was ~$470m to Montagu; held for sale at 11/30/2019 (goodwill $87.7m, assets $115.3m). It caused the −6pt acquisitive effect in FY2020.
  - Automotive revenue in $ is never printed.
- **Measure:** segment Adjusted EBITDA (non-GAAP). It excludes D&A, stock comp, restructuring, acquisition-related costs and aM performance compensation, among others. The definition wording drifts: "restructuring charges" (FY2019) vs "restructuring and impairment charges" (FY2021).
- **No segment-level revenue split:** no recurring/non-recurring dollar split and no D&A or capex by segment is printed in any INFO 10-K. Only consolidated transaction-type tables exist. The segment proxies are the narrative "Transportation recurring revenue organic growth" % and the organic/acquisitive/FX bridges.
- **Restatements across consecutive 10-Ks:** none for Transportation. Revenue, Adj. EBITDA and total assets agree for every overlapping year. The FY2018 margin is printed as 41% (whole %) in the FY2018 doc and as 41.3% in FY2019/20. Printed "- %" bridge cells are recorded as 0.
- **Acquisitions:**
  - CARPROOF (Dec 24, 2015; ~$459.2m net of cash).
  - automotiveMastermind (Sep 25, 2017; ~$432m for 78%, with the remaining 22% treated as compensation, est. $150–175m). aM performance compensation was $54.1m (FY2018) and $9.9m (FY2017), excluded from Adj. EBITDA.
  - A Transportation goodwill acquisition of $9.0m in FY2019 is not named.
- **Goodwill rollforwards foot:** 1,299.1 → 1,361.4 → 1,671.1 → 2,055.6 → 2,031.6 → 1,953.1 → 1,961.2 → 1,964.0.
- **CARFAX and Polk:** CARFAX record counts are printed each year (17bn/100k sources in FY2016, rising to 27bn/130k in FY2021). US ownership records are also printed (5bn → 12bn). The only Polk references are the 2013 CARFAX antitrust suit "prior to our acquisition of R.L. Polk & Co." (~469 dealers) and a note that repayment began in 2014 of the borrowings used to fund the Polk acquisition (FY2016 p43). No deal value is printed.

## IHS Inc. pre-2016
Quartr has no IHS Inc. filings. Company 6412 lists 10-Ks only from FY2016, and "IHS" (12916) is the unrelated IHS Holding towers company. The 2013 Polk/CARFAX acquisition facts are **not available** from Quartr.

## Non-comparability (P0 vs P1): no growth rate across the boundary
1. Scope differs: P0 includes M&T, and AD&S until FY2019; P1 is automotive only.
2. The fiscal year differs: Nov 30 vs Dec 31.
3. The measure differs: Adj. EBITDA, pre-D&A and stock comp, vs GAAP-based OP after $241–303m PPA amortization from the S&P/IHS merger.
4. P1 FY2022 is a 10-month period.
5. Dec 2021–Feb 2022 is in neither era.
6. The PPA step-up affects P1 only.

## Not disclosed
- SPGI: Mobility business-line revenue, adjusted segment margin, and segment goodwill (the goodwill table was not extracted).
- INFO: Transportation recurring/non-recurring $, D&A, capex, Automotive vs M&T $, and CARFAX standalone revenue.

## IHS Markit deep extraction (2026-10-07)
This pass appended 1,000 rows (CSV now 1,597 rows) under `statement=SEG_PRED`. Each source's comparatives stay under that source's own `source_doc`. No existing row was altered. The duplicate key is (source_doc, fiscal_period, section, line_item) and no key repeats.
Slide values are whole $m, as printed. Slide pages are text-extractable tables, so no number was read off a chart.

### Sources and pages
| source_doc | Quartr id | Rows | Pages used |
|---|---|---|---|
| INFO_8K_Q2-FY2021 | 109729 | 204 | 1–2 (summary, transaction type, growth bridge), 8–9 (supplemental revenue by segment × transaction type), 11 (segment Adj. EBITDA and margin) |
| INFO_10Q_Q2-FY2021 | 474120 | 97 | 17 (Note 2: A&D, aM), 19 (Note 3), 26 (restructuring by segment), 33–34 (Note 16), 35, 41, 43, 46 (MD&A) |
| INFO_10Q_Q3-FY2021 | 474119 | 135 | 18 (Note 2/3), 26, 33–35 (Note 16), 36, 42, 44, 47 |
| INFO_Slides_Q2-FY2021 | 4776 | 116 | 4 (quarterly revenue by segment: recurring and non-recurring), 5 (quarterly organic growth), 7 (quarterly Adj. EBITDA and margin) |
| INFO_Slides_Q3-FY2021 | 3229 | 133 | 3 (guidance text), 4, 5, 7 |
| INFO_10K_FY2021 … FY2016 | 223420/21/22/24/25/26 | 315 | Item 1 Transportation pages, Employees, MD&A transaction-type tables, FY2017 Note segment table (p82–83) |

### Key new series
- **Transportation recurring vs non-recurring revenue in $.** This is the first segment-level split. The 8-K gives Q2-FY2021, Q2-FY2020, 6M-FY2021 and 6M-FY2020 to one decimal: 261.6 + 82.5 = 344.1, and 508.2 + 147.6 = 655.8. The slides add quarterly data for Q1-FY2020 to Q3-FY2021 plus FY2020 (879 recurring + 273 non-recurring = 1,152).
  - In the IHS Markit taxonomy, Transportation "recurring" is entirely recurring fixed. Recurring variable is 100% Financial Services.
- **Quarterly Transportation revenue, Adj. EBITDA and margin, Q1-FY2020 to Q3-FY2021.** Source is the slides, plus 10-Q comparatives for Q2/Q3 FY2020.
- **Quarterly Transportation organic growth by type.** Covers recurring, non-recurring and total.
  - Q2-FY2020, Q3-FY2020, FY2020 and Q3-FY2021 sit in "Normalized" columns; the caption carries that tag.
  - Footnote (1) gives the reported figures for Q2-FY2020 including the impact of cancelled events: non-recurring −37%, total −18%. For FY2020 they are −16% and −2%.
- **Quarter and YTD organic/acquisitive/FX bridges:** Q2-FY2021 39/0/2, 6M-FY2021 20/0/2, Q3-FY2021 15/0/1, 9M-FY2021 18/0/2.
- **Consolidated revenue-by-transaction-type tables, FY2014–FY2021,** for context. Section names include "(consolidated)".
- **Item 1 KPI drift, FY2016 → FY2021:**

| Item | FY2016 | FY2021 |
|---|---|---|
| Light-vehicle forecast coverage | more than 98% | 99% |
| Model variants forecast | nearly 40,000 | more than 50,000 |
| Vehicle systems/components forecast | more than 100 | more than 150 |
| U.S. ownership records | 5bn | nearly 12bn |
| Vehicles covered | 740m | 790m |
| U.S. households covered | 200m | 250m |

  - U.S. ownership records were 7bn from FY2017 to FY2020.
  - CARFAX records and sources over time: 17bn/100k (FY2016), 19bn/110k (FY2017), 20bn/112k (FY2018), 23bn/112k (FY2019), 25bn/112k (FY2020), 27bn/130k (FY2021).
  - M&T statistics and AD&S statistics (FY2016–18) were also captured.
- **Other items:**
  - Consolidated headcount, which has no segment split: 12,500 → 13,000 → 14,900 → 15,500 → 16,000 → 16,000.
  - aM performance-award cost: $10m (FY2017), $54m (FY2018) and $42m (FY2019). Of an estimated $60–65m for the remaining interests, $44.7m had been recognized by 5/31/21 and $48.3m by 8/31/21.
  - Transportation restructuring liability: $3.9m (5/31/21) and $1.6m (8/31/21).

### Ties performed (all pass unless noted)
- **8-K segment sums.** Revenue segments sum to the total for all 4 columns. Adj. EBITDA (four segments plus shared services) sums to the total for all 4 columns. Margins recompute exactly from revenue and Adj. EBITDA.
- **8-K transaction type.** Transportation recurring + non-recurring = segment revenue in all 4 columns. Recurring fixed + variable + non-recurring = total revenue.
- **10-Q Q3 Note 16.** Segment sums tie to the totals. Q3 also ties to the Q2 YTD figures: YTD + Q3 = 9M, both 655.8 + 347.4 = 1,003.2 and 317.4 + 167.1 = 484.5. The same holds for the prior year (540.4 + 298.9 = 839.3; 219.6 + 153.6 = 373.2).
- **Slides.** All segment/total and recurring + non-recurring = total ties hold within ±1 (rounding to whole $m).
  - Summing quarters to FY2020 gives revenue 1,151 vs 1,152 printed, recurring 880 vs 879, non-recurring 272 vs 273, and Adj. EBITDA 515 (exact).
- **Implied quarters agree with the slides within rounding.** These are differences of printed figures and were not recorded:

| Quarter | Implied revenue | Implied Adj. EBITDA | Slide |
|---|---|---|---|
| Q1-FY2020 | 297.2 | 118.0 | 297 / 118 |
| Q4-FY2020 | 312.3 | 141.5 | 312 / 141 |
| Q1-FY2021 | 311.7 | 146.7 | 312 / 147 |

  - Q4-FY2021 is not printed anywhere on Quartr. The implied figures are 1,354.4 − 1,003.2 = 351.2 revenue and 645.0 − 484.5 = 160.5 Adj. EBITDA (derived only, not recorded).
- **Does not tie:**
  - The 6M-FY2021 Transportation bridge is 20 + 0 + 2 = 22 against a printed total of 21. This is printed rounding, recorded as printed.

### Corrupted or garbled text
- **Q2 slides p4:**
  - "26222" appears for the Q1-FY2021 non-recurring block. The Financial Services value of 26 comes from the Q3 deck, and the column sum of 121 confirms it.
  - A stray "77" sits beside the Q3-FY2020 non-recurring values. Transportation is 72, confirmed three ways: the Q3 deck prints 72, the column sum is 124, and 10-Q revenue 298.9 − recurring 227 ≈ 72.
- **Q3 slides:** "1.152" and "1.073" are decimal-for-comma corruptions, recorded as 1,152 and 1,073. The deck also prints the typo "IHS Marklt".
- **8-K p2:** the segment growth-bridge table is scrambled. The YTD FX figure (2) was taken from the 10-Q p41 bridge, which is cleanly ordered. Release rows hold only values that are unambiguous.
- **8-K p9:** the caption for the "Total non-recurring revenue" row is lost in the page split. The values are recorded with a caption that says so.

### Inconsistencies between documents (both kept as printed)
- **Q4-FY2020 organic growth:** Transportation recurring is 5% in the Q2 deck and 6% in the Q3 deck. Financial Services total organic is 5% vs 6%. No other cell changed between the two decks.
- **FY2019 recurring variable organic growth:** 4% in the tables of the FY2019 and FY2020 10-Ks, but 6% in the FY2020 10-K narrative (row captioned accordingly).
- **A&D sale price:** "approximately $470 million" in the FY2019 10-K vs "approximately $466 million" in the FY2021 10-Qs, which is presumably the final figure.
- **Whole-% margins in the 10-Q MD&A vs one-decimal margins in the release** are recorded as separate rows: Q2-FY2021 50% vs 49.6%, Q2-FY2020 42% vs 41.8%.

### What is NOT disclosed or available
- **Quartr coverage.** For INFO, Quartr holds only the Q2 and Q3 FY2021 10-Qs, the Q2 FY2021 8-K and the Q2/Q3 FY2021 slides, besides the six 10-Ks.
  - There are no quarterly releases or slides before Q2-FY2021, so there is no quarterly segment data before Q1-FY2020. The slides' history starts at Q1 20.
  - There are no Q4-FY2021 or Q1-FY2021 filings.
- **10-Ks:**
  - No segment-level recurring/non-recurring $ appears in any 10-K or 10-Q. Only the release and slides give it, for FY2020–Q3 FY2021.
  - No quarterly segment table appears. The quarterly data in the FY2016/17/20 10-Ks is consolidated revenue, net income and EPS only.
  - Segment stock-based compensation, D&A and capex are not printed.
  - Geography by segment is not printed: the U.S./U.K./RoW table is consolidated.
  - Automotive vs M&T vs A&D revenue is never given in $; only the automotive % of segment revenue appears.
  - CARFAX standalone revenue, customer counts and Transportation headcount are not printed.
- **10-Qs:** neither interim 10-Q prints segment total assets or segment goodwill.
- **Slides:** the slides print no Transportation sub-business KPIs (automotive, CARFAX, aM, recall, maritime). The commentary appears only as MD&A narrative.
- **Guidance:** guidance is consolidated only.
