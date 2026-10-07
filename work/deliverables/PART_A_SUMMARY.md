# Mobility Global (MBGL): Part A historical model summary

**Workbook:** `deliverables/MBGL_Historical_Model.xlsx` (26 tabs). Figures are as originally reported, in USD millions.
**Tiers:** [D] disclosed; [C] computed, with the method in the Key Metrics tab.

## The numbers

The company's own statements are carve-out financials from the Form 10/A and the 10-Q.

| | FY2023 | FY2024 | FY2025 | 2-yr CAGR [C] | 6M-2025 | 6M-2026 | y/y [C] |
|---|---|---|---|---|---|---|---|
| Revenue [D] | 1,485 | 1,613 | 1,750 | 8.6% | 859 | 923 | +7.5% |
| Operating profit [D] | 239 | 298 | 339 | 19.1% | 180 | 163 | −9.4% |
| Operating margin [C] | 16.1% | 18.5% | 19.4% | | 21.0% | 17.7% | |
| Adjusted EBITDA (company definition) [D] | 598 | 658 | 711 | 9.0% | 357 | 386 | +8.1% |
| Net income [D] | 163 | 208 | 220 | 16.2% | 123 | 108 | −12.2% |
| Cash from operations [D] | 393 | 427 | 485 | 11.1% | 233 | 189 | −18.9% |
| Capex [D] | (18) | (15) | (24) | | (8) | (12) | |

**Quarterly growth.** Revenue grew +8.3% in Q1-26 and +6.6% in Q2-26 [C]. FY2026 guidance (Aug 7, 2026) is revenue of $1,870–1,885m (+6.9–7.7%) and Adjusted EBITDA of $745–760m [D].

**Acquisition amortization.** About $296m a year of amortization from the IHS Markit merger depresses GAAP operating profit. Operating profit plus D&A gives an EBITDA margin of about 37% [C].

**Predecessor history.** This sits on the Predecessor Segments tab and is not comparable across eras.
- **IHS Markit Transportation (Nov FYE):** revenue grew from $758m (FY15) to $1,354m (FY21), a 10.1% CAGR [C]. The scope included Maritime & Trade throughout, and Aerospace & Defense until December 2019.
- **S&P Global Mobility (Dec FYE):** revenue grew from $1,484m (2023) to $1,747m (2025), an 8.5% CAGR [C]. FY2022 is only about 10 months.

## Structural breaks, in order

1. **Dec 2015:** CARPROOF acquired (Canada).
2. **Sep 2017:** automotiveMastermind acquired (78%).
3. **Dec 2019:** Aerospace & Defense sold out of IHS Markit Transportation.
4. **Feb 28, 2022:** S&P Global–IHS Markit merger. The segment becomes Mobility; the fiscal year-end moves from November to December; purchase-accounting step-up.
5. **Feb 2023:** Market Scan acquired. **Aug 2023:** Catalyst for Aftersales sold.
6. **Apr 29, 2025:** spin announced. The 2025 realignment means segments are CARFAX and B2B, recast.
7. **May 2026:** Form 10 and Form 10/A filed. $2.0bn Senior Notes issued May 29. $2.0bn dividend paid to S&P Global.
8. **Q2-2026:** the segment measure changes to Adjusted EBITDA. The Adjusted EBITDA definition narrows from 10 exclusions to 6.
9. **Jul 1, 2026:** distribution (1:1); standalone from Q3-2026.

## Genuine non-disclosures

- Revenue by brand or product, and by B2B business line.
- Organic or constant-currency growth: MBGL does not print it, although S&P Global did every quarter.
- Retention/NRR, ACV/ARR, ARPU, churn.
- Segment assets: dropped in the 10-Q.
- Transition services agreement (TSA) fees.
- Deferred-revenue roll-forward.
- A standalone Q2 cash-flow statement.

The full list is on the Accounting Notes tab (33 rows).

## Verification counts

- **Extraction:** 4,859 rows across 6 files, all self-verified for footing and ties.
- **Canonical layer:** 390 primary cells; 0 collisions (59 identical duplicates absorbed and logged); 0 leftovers; 3 gap-fills from the MD&A, logged.
- **Recalc:** 0 formula errors; 106 integrity-check cells all tie.
- **Independent check:** Quartr standardized Q2-2026 values matched 6 of 6. Annual periods aren't available there.
- **XBRL cross-check:** not done, because sec.gov is blocked (see `canonical/VERIFICATION.md`).

## Known gaps (need native filings)

- Annual working-capital lines in the cash-flow statement.
- Q1 cash-flow components.
- Tax provision split for 2024/2023.
- Lease maturity table.
- Market Scan PPA liabilities (the lines sum to 59 against a printed total of 39).

## Files

- `deliverables/MBGL_Historical_Model.xlsx`
- `extraction/`: 6 long CSVs plus notes files and SPEC.md
- `canonical/`: primary.csv, caption map, merge log, accounting_notes.csv, VERIFICATION.md
- `scripts/`: canon_primary.py, build_workbook.py, verify_workbook.py
- `transcripts/`: quote banks, index.csv, TARGETS_TIMELINE.md
- `analysis/`: D1–D10, D5, QUALITATIVE, K_session_tables

## IHS Markit segment history (added 2026-10-07)

The model now has a **Segment History** tab with three eras side by side, each as originally reported, and growth computed only within an era.
- **A. IHS Markit Transportation, FY2014–21 (Nov FYE):** revenue, organic/acquisitive/FX bridge, recurring organic growth, Adj. EBITDA and margin, incremental margin, share of IHS Markit revenue, segment assets and goodwill.
- **B. S&P Global Mobility, FY2022–25:** revenue by type and region, operating profit, amortization, D&A, capex, assets.
- **C. Carve-out, FY2023–25:** linked to the IS tab, with a reconciliation to the S&P Global segment.
- **D. IHS Markit quarterly, Q1 FY2020–Q3 FY2021:** recurring/non-recurring revenue, Adj. EBITDA, organic growth by type.

**Headline figures [C, from D]:**

| IHS Markit Transportation | FY2014 | FY2019 | FY2021 |
|---|---|---|---|
| Revenue | $663m | $1,246m | $1,354m |
| Adj. EBITDA margin | 35.4% | 41.8% | 47.6% |

- **Revenue CAGR:** 10.8% over FY14–21; 13.5% over FY14–19.
- **Adj. EBITDA CAGR:** 15.6% over FY14–21.
- **Organic growth:** 8–11% a year, except FY2020 at −2%.
- **Recurring revenue:** about 76–79% of segment revenue in FY2020–21.

**Coverage and checks:**
- **Sources:** 1,000 new rows from the FY2021 10-Qs, the Q2 FY2021 8-K, the Q2/Q3 FY2021 decks and a 10-K re-sweep. `extraction/predecessor.csv` now has 1,597 rows.
- **Workbook verification:** recalc shows 0 errors and 139 integrity checks pass (10 more than before).
- **Research document:** Exhibits 8.7 and 8.8 added.

## Uniform segment P&L (added 2026-10-07)

**Segment P&L tab:** CARFAX, B2B and Corporate, with identical rows in all nine periods (FY2023–25, Q1/Q2/6M 2025–26).
- **Revenue:** subscription/non-subscription and U.S./International splits.
- **Bridge to Adjusted EBITDA:** segment operating profit plus amortization, depreciation, SBC, transaction, severance & other, and acquisition/legal/ELT items.
- **Comparison and ratios:** the built EBITDA is shown against company-reported Adjusted EBITDA, with margins, growth, incremental margins, cash operating costs, D&A % and SBC %.
- **Total:** the sum of the segments, reconciled to the IS tab.

**Why one bridge works:** both the old 10-exclusion and new 6-exclusion company definitions reduce to the same bridge, so every period sits on one basis.

**Checks:**
- All built bridges tie to reported Adjusted EBITDA, except 3 documented gaps (FY2025 "Other" split; Q1-2026 B2B depreciation).
- Revenue and operating profit tie to the IS.
- 6M = Q1 + Q2 across the definition change.
- Recalc: 0 errors; 205 integrity checks pass.

| Period | CARFAX Adj. EBITDA margin | B2B Adj. EBITDA margin |
|---|---|---|
| FY23 | 45.5% | 34.3% |
| FY24 | 45.8% | 35.4% |
| FY25 | 46.9% | 32.4% |
| 6M-26 | 48.0% | 32.6% |

[C]

**Further readings [C]:**
- CARFAX was 65% of revenue and 74% of segment Adj. EBITDA (before Corporate) in 6M-26.
- B2B's FY25 incremental margin was −17.6%.
