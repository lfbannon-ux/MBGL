# statements_NOTES.md — Primary statements (extraction agent #1)

Output: `extraction/statements.csv` (1,164 rows). Units: usd_m unless the row says otherwise (EPS usd_per_share, shares shares_m).
The sign follows the print: parentheses become negative.

## Sources and pages (Quartr page numbers)
| Doc | documentId | Pages | Content |
|---|---|---|---|
| Form10A_2026-05-27 | 3603533 | 285-286 | Summary Combined Financial and Other Data (IS for Q1-26, Q1-25 and FY23-25; CF totals; BS data at 3/31/26 and 12/31/25; non-GAAP) |
| | | 334-336 | Pro forma IS Q1-2026, IS FY2025, BS 3/31/26 (statement=PROFORMA) |
| | | 361 | MD&A free cash flow and cash flow overview (used to resolve the scrambled CF) |
| | | 421 | F-index |
| | | 422-426 | Unaudited condensed IS, CI, BS, CF, EQ (Q1-2026 vs Q1-2025; BS 3/31/26 vs 12/31/25) |
| | | 440-444 | Audited IS, CI, BS, CF, EQ (FY2023-FY2025; BS 12/31/25 and 12/31/24) |
| Form10_2026-05-07 | 3603535 (546pp) | 500-504, 518-522 | Same statements. The page offset is +78 vs the 10/A |
| 10Q_Q2-2026 | 3699447 | 4-8 | IS, CI (Q2 and 6M, 2026/2025), BS (6/30/26 vs 12/31/25), CF (6M), EQ (quarterly roll-forwards) |
| 8K_Q2-2026_release | 3699450 | 5-7, 10 | IS and BS exhibits, CF Exhibit 3, FCF computation |

## Fiscal calendar as printed
- The fiscal year ends December 31.
- Annual statements: "Year Ended December 31, 2025, 2024, 2023". Interim statements: "Three Months Ended March 31", "Three/Six Months Ended June 30".
- The Form 10 auditor is Ernst & Young LLP, "auditor since 2025", report dated March 25, 2026.

## Verification
- Every BS foots, with assets = liabilities + equity: 12/31/24, 12/31/25, 3/31/26 and 6/30/26, in every source, including the pro forma BS (13,162 = 3,235 + 9,927).
- All 41 IS/CI sections tie (expenses → total, operating profit → pre-tax → net income), including both pro forma columns.
- Equity roll-forwards tie to the BS and to the CI (FX translation = change in AOCI).
- CF ties to the change in cash in every period. Annual: 11 / (20) / 5. Q1: 84 / 1. 6M: 148 / 13.
- The 10-Q 6M figures equal the 10/A Q1 figures plus the 10-Q Q2 figures on every IS line. Example: revenue 455+468=923 and 420+439=859.
- The 10-Q 12/31/25 comparative BS equals the 10/A values. Captions condense: "Property and equipment, net of accumulated depreciation", "Operating lease liabilities", "Deferred tax liability, net".
- Q1-2025 capex (5) is confirmed by 6M-2025 (8) less Q2-2025 (3) in the 8-K FCF table.

## Restatements and differences
- **Form 10 vs Form 10/A:** the annual IS, CI, BS, CF and EQ text is identical, as are the Q1 interim statements. No quiet restatement was found.
  - Text artefacts only: the 10/A Q1 CI drops the 2026 FX value "1", which the Form 10 prints. The Form 10 interim CF has an extra "11" token.
  - Both filings include Q1-2026 interim statements, even though the Form 10 was filed 2026-05-07.
- **10-Q vs Form 10/A:**
  - The statement title changed to "Statements of Operations".
  - The 10-Q prints EPS for all periods, including the carve-out comparatives: Q2-25 $0.22 and 6M-25 $0.42. The Form 10 says EPS was "not presented" because there was no capital structure. The basis is not stated; it is presumably 295m shares. Flag this.
  - The 10-Q CF caption "Other" (1) replaces "Restructuring and other".
- **8-K vs 10-Q:**
  - The IS and BS are identical.
  - The CF is titled "Condensed **Consolidated** Statements of Cash Flows", where the 10-Q says "Combined".
  - The 8-K CF collapses working capital into "Net changes in other operating assets and liabilities" (46)/(13), which equals the sum of the 10-Q lines. It labels (1) as "Restructuring and other".
  - The 6M-2025 contingent consideration (2) is missing in the 8-K text, which comes from a corrupted page. The 8-K Exhibit 4/5 pages (8-10) contain corrupted digits ("1ŏ01", "6130", "7356"). These were not used except the FCF table, which ties to the 10-Q CF.

## Gaps and judgments (NOT extracted, so no rows)
- **Annual CF (10/A p.443), working-capital lines:** "Restructuring and other" and the nine "Changes in operating assets and liabilities" lines are not recorded for any year.
  - The Quartr text is scrambled and drops values. The printed tokens sum about 27 away from the CFO tie, and brute-force placement gives no unique, plausible solution.
  - CFO (485 / 427 / 393) and every other line are recorded. A PDF is needed to fill these lines; files.quartr.com is blocked by the proxy.
- **Annual CF, contingent consideration:** recorded only for FY2024 (5). FY2025 and FY2023 are implied as (2) each from the CFF tie and are not legible.
  - The FY2025 (2) is consistent with the 10-Q 6M-2025 contingent (2).
- **Annual CF, FY2024 CFI:** the statement token is garbled. The (21) comes from MD&A p.361 and the summary p.285, recorded under those pages.
- **Q1 interim CF (p.425):**
  - Not recorded: restructuring, the working-capital lines, Q1-2025 capex/CFI/financing components, and Q1-2026 financing components.
  - Q1 totals come from MD&A p.361: CFO 54/67, CFI (6)/(5), CFF 37/(62).
  - Tokens (50), (10) and 99 cannot be attributed with confidence. The likely reading is Q1-25 net transfers (50) and loan payments (10).
  - Q1-2026 FX (1) and capex (6) are recorded.
- **Annual "Other income, net" FY2025:** blank (dash). FY2024 (1) and FY2023 (2) are printed in parentheses in the expense block, which means income. They are recorded as -1 and -2 as printed.
- **Pro forma IS:** Q1-2026 adjustment-column tax lines and the total-expense/operating-profit adjustment lines are garbled, so not recorded. They are implied by the ties: TAA tax (7), AEA tax (1).
  - Pro forma and historical columns are fully recorded.
  - The PF BS AEA +1 to other current liabilities (lease, note k) is not recorded as a separate token.
- **Stray tokens:** "228" and "278" next to PP&E, and "222222", are ignored as garble. The PP&E sub-lines are confirmed by arithmetic.

## Not disclosed
- No EPS in the Form 10 historical statements; pro forma EPS is $0.12 for Q1-26 and $0.47 for FY25, on 295m shares.
- No Q2-standalone CF statement; only 6M is given, and Q2 CFO comes from the 8-K FCF table.
- No 3/31/25 or 6/30/25 balance sheets.
- No FY2023 balance sheet except equity totals in the EQ roll-forward.
- No restricted cash at either date (10/A p.428).
