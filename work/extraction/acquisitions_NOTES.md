# acquisitions_NOTES — extraction agent #6

**Output:** `extraction/acquisitions.csv` (191 rows).
- Schema: `deal_order, deal_label, section, line, order, value, unit, source_doc, page`.
- Pages are Quartr pages.
- **Method:** values were taken from Quartr `read_document`; only structured rows were written.

## Deals and sources
| # | Deal | Preliminary | Final |
|---|---|---|---|
| 1 | CARPROOF (2015-12-24) | INFO_10K_FY2016 (223426) p.61 | INFO_10K_FY2017 (223425) p.64 (no longer labelled preliminary; values unchanged) |
| 2 | automotiveMastermind (2017-09-25) | INFO_10K_FY2017 p.62–63 | INFO_10K_FY2018 (223424) p.64–65 |
| 3 | Market Scan (2023-02-16) | not presented | Form10A p.452–453 = Form10 p.530–531 (identical) |
| 4 | Catalyst for Aftersales (divested Aug-2023) | — | Form10A p.350, 447, 453 |
| 5 | Separation consideration to S&P Global (2026) | Form10A p.321, 338 (expected / pro forma) | 10Q_Q2-2026 p.11–12, 17 (actual) |
| 6 | Context only, not a deal: Note 3 goodwill and intangibles roll-forward | — | Form10A p.454, 367 |

## Footing checks
- **CARPROOF:** foots in both documents (506.9 − 47.7 = 459.2).
- **aM:** both the preliminary and final tables foot (493.8 − 48.9 = 444.9; 486.1 − 42.0 = 444.1).
  - From preliminary to final, goodwill fell from 370.7 to 363.0, deferred taxes from 42.9 to 36.2 and current liabilities from 4.6 to 4.4.
- **Market Scan:** assets foot (253), and 253 − 39 = 214 net assets. The intangibles foot (10 + 81 + 6 = 97).

## Flags
1. **Market Scan liabilities don't foot.** The printed liability lines (2 + 22 + 1 + 25 + 9) sum to **59**, but the printed total is **39**.
   - The Form 10 and 10/A texts are identical, so this is not something the amendment introduced.
   - It is probably a single misprint or text corruption: unearned revenue 2 vs 22, or DTL 5 vs 25. A PDF is needed to resolve it.
   - Rows are recorded as printed.
2. **Market Scan consideration vs net assets.** Total consideration is $223m ($214m cash + $9m contingent), but net assets acquired are $214m. The $9m contingent consideration appears as an assumed liability inside the PPA, so net assets equal cash consideration. Recorded as printed.
3. **aM PPA covers two deals.** The tables combine aM with Macroeconomic Advisers (MEA, a small IHS research firm), and only the "Total" column is printed. aM-only PPA is not disclosed.
4. **aM consideration was restated between 10-Ks.**
   - FY2017 10-K: about $433m, including an estimated $44m contingent payment.
   - FY2018 10-K: about $432m, including $43m contingent.
   - Both are recorded. The estimate for the remaining 22% (treated as compensation, not purchase consideration) fell from $200–225m (preliminary) to $150–175m (Q3-2018).
5. **CARPROOF finalization.** The FY2017 10-K says finalization of the 2016 deals cut intangibles by about $80m and deferred taxes by $66m, and raised goodwill by $20m. However, the CARPROOF column is unchanged, so these changes sit in the Markit/OPIS columns.
6. **Separation payment amount differs.** The 10/A expected "approximately $1.9 billion" (p.278, 321; pro forma APIC −1,900). The 10-Q reports a **"$2.0 billion dividend"** (p.12, 18). The 10/A says the amount "may vary based on our existing cash position". Both are recorded.
7. **Market Scan acquisition cash outflow.** The FY2023 acquisition cash outflow is not separately legible in the Quartr cash-flow text. Investing outflow of $(230)m is stated to be "primarily" Market Scan (p.362) and is recorded only as context.

## Not disclosed / not available
- **Not disclosed:** a Catalyst sale price; the NGC (~35%) and Digital Automotive (~25%) stake cost or carrying values; any Mobility-level IHS Markit/S&P merger PPA (goodwill of 8,845 is presented without a deal split).
- **Not available:** the R.L. Polk 2013 acquisition terms, because IHS Inc. 10-Ks are not in Quartr (see predecessor_NOTES).
- **Out of scope:** the A&D (Jane's) divestiture belongs to the Transportation segment, not Mobility; it is captured in predecessor.csv.
