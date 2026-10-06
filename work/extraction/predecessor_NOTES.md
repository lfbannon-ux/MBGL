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
