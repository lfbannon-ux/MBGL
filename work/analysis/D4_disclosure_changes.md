# D4 — Disclosure changes and red flags: Mobility Global (MBGL)

Prepared 2026-10-06 by the Part D analyst. It follows `analysis/D_SPEC.md`.

**Tiers**
- **[D]** disclosed
- **[C]** computed (method stated)
- **[E]** estimate
- **[IR]** management verbal
- **[X]** third party
- **[context]** general knowledge

**Doc keys (Quartr ids)**
- F10 = Form 10, 2026-05-07 (3603535)
- 10A = Form 10/A, 2026-05-27 (3603533)
- 10Q = 10-Q Q2-26, 2026-08-07 (3699447)
- 8K = Q2 release (3699450)
- ID-deck = Investor Day slides, 2026-05-12 (3352878)
- Q2-deck = 3986013
- SPGI-xx = S&P Global earnings slides (company 3977)
- SPGI10K-FYxx and INFO10K-FYxx = predecessor 10-Ks, as listed in `extraction/predecessor_NOTES.md`

Pages are Quartr pages.

**Scoring.** For each item, the "Unflattering?" column asks whether the change coincided with the metric it affects turning worse. The answer is **Yes**, **No** (the change is neutral or hurts the company's optics), or **Mixed**.

---

## 0. Summary: the red flags that matter, ranked

| # | Change | Vintage | Coincided with metric turning unflattering? |
|---|---|---|---|
| 1 | **Growth attribution relabelled.** Form 10/A attributes Q1-26 subscription growth to "new business growth" ($26m) plus "improved contract terms". The 10-Q's 6M figures imply that Q1 was mostly **price** (~$20m) with only ~$12m of new business. | 10A (May-27) → 10Q (Aug-7) | **Yes.** New business fell to ~$8m in Q2 [D], the same quarter the FY guide was cut. |
| 2 | **Segment profit measure switched** from segment operating profit to Adjusted EBITDA, with prior periods recast. | 10Q p.14 | **Yes.** B2B segment OP fell −62% in Q1-26 and −81% in Q2-26 [D/C]. B2B Adj. EBITDA shows +8% [D]. |
| 3 | **FY26 guide basis switched** from organic constant currency (7.5–9%) to reported (6.9–7.7%). | ID → Q2-deck | **Yes.** On a like-for-like basis the cut is ~0.9–1.6 pt [C], not the 0.6–1.3 pt the headline implies. |
| 4 | **Adjusted EBITDA definition** shrank from 10 to 6 exclusions. Item (6) became a catch-all ("and other costs that are not representative…"). The Q2 deck still prints the 10-item text. | F10/10A → 10Q/8K; Q2-deck stale | **Mixed.** The 2026 periods have no acquisition or legal items, but the catch-all widens discretion. |
| 5 | **SPGI-era Mobility margin target dropped.** SPGI's 41–43% adjusted operating margin target for 2025/26 was missed (FY25: 39.9%). MBGL replaced it with "+50 bp/yr from a reset ~39.1% base". | SPGI Investor Day 2022 → MBGL ID 2026 | **Yes.** |
| 6 | **NRR removed** from the Investor Day deck before presentation. Management admitted this on stage. | ID 2026-05-12 | Unknown. "Great number" per management [IR], but not shown. |
| 7 | **Business-line revenue in dollars dropped.** SPGI printed Dealer/Manufacturing/Financials every quarter. MBGL prints only CARFAX/B2B, with business-line % for FY25 only. Organic constant-currency growth also stopped being printed. | SPGI-Q1-26 → MBGL Q2-26 | **Yes.** Manufacturing was the weak line (−3% Q3-25, +1% Q4-25 [IR]). |

---

## 1. Adjusted EBITDA definition: 10 exclusions → 6

| Document (vintage) | Exact short wording | Source |
|---|---|---|
| F10 (May-7) and 10A (May-27), identical | "(1) interest … (6) employee severance charges, (7) acquisition integration costs, (8) acquisition and disposition-related costs, (9) legal settlement recovery and (10) other non-operational and/or non-recurring expenses." | 10A p.357; F10 p.436 |
| 10Q Note 7 (Aug-7) | "(5) transaction costs related to the stand-up of the Spin Business … and (6) employee severance charges and other costs that are not representative of the underlying economics of the periods presented." | 10Q p.14 |
| 8K Exhibit 5 (Aug-7) | Same 6-item text as the 10Q. | 8K p.11 |
| Q2-deck slide 12 (Aug-7) | **Still the 10-item Form 10 text**, printed next to a 6-line reconciliation. | Q2-deck p.12 |

- **What changed.** Items (7)–(10) were removed. Item (6) widened from "employee severance charges" to severance "and other costs that are not representative of the underlying economics". The reconciliation line is now captioned "Employee severance charges and other". It was 9 in Q2-25 and 2 in Q2-26 [D] (10Q p.15).
- **Unflattering?** Mixed.
  - The deleted items had no 2026 activity, so the deletion itself is cosmetic.
  - The new catch-all is the real change. A single "and other" bucket replaces four named buckets, so future add-backs are less itemised.
  - The deck/10-Q mismatch on the same day is a control-quality flag, not a numbers flag.
- **10/A-only measures that disappeared in the 10-Q:**
  - Adjusted operating profit (8 items, including "ELT transition costs").
  - "Segment Adjusted EBITDA" (10 items) (10A p.358).
  - Neither appears in the 10Q.
  - ELT transition costs were excluded from Adjusted OP but were not a named item in the 10-item Adjusted EBITDA list. In FY25 they net to 0: B2B (5) and Corporate +5 [D] (10A p.350).

## 2. Segment profit measure: segment OP → Adjusted EBITDA (recast)

**Wording by vintage**
- **10A:** "Segment operating profit is defined as operating profit before Corporate Unallocated expense." The CODM measure is segment OP (10A p.347, p.461).
- **10Q:** "Beginning in the second quarter of 2026, the Company changed its segment profitability measure from segment operating profit to Adjusted EBITDA and recast prior period amounts accordingly" (10Q p.14).

**What the old measure would have shown** (10Q MD&A still prints per-segment GAAP OP inside the reconciliation):

| Segment OP, $m | Q1-25 | Q1-26 | Q2-25 | Q2-26 | 6M-25 | 6M-26 | Source |
|---|---|---|---|---|---|---|---|
| CARFAX | 77 [D] | 89 [D] | 89 [D] | 101 [D] | 166 [D] | 190 [D] | 10A p.348; 10Q p.24–25 |
| B2B | 14 [D] | 5 [D] (−62% printed) | 16 [D] | 3 [D] (−81% [C]) | 30 [D] | 8 [D] (−73% [C]) | same |
| B2B Adj. EBITDA (new measure) | — | 49 [D] | 49 [D] | 53 [D] (+8%) | 93 [D] | 102 [D] (+10%) | 10Q p.14, 24–25 |

- **Why B2B OP collapsed.** Stand-up transaction costs were booked **in the B2B segment**: $13m in Q1-26 (10A p.347 fn1), $20m in Q2-26 and $33m in 6M-26 [D] (10Q p.24–25). Amortization (~$26–27m a quarter) is unchanged [D].
- **Unflattering?** **Yes.** The measure switch coincides exactly with the quarter in which B2B segment OP went to ~zero.
  - The measure is economically defensible: it strips one-off spin costs.
  - However, it also strips ~$105m a year of acquired-intangible amortization from B2B (107 in FY25 [D], 10A p.352). That amortization is the cost of aM, Polk and Market Scan.
  - It also removes segment OP, which had already shown B2B −12% in FY25 [D] (10A p.352).
- **Inference:** booking separation transaction costs in B2B rather than Corporate is an allocation choice, and it is not explained in the text read.

**Related changes in the 10-Q**
- **Segment assets.** Disclosed in the 10A (interim and audited Note 8, with D&A and capex by segment; 10A p.459–463). The 10Q says: "Asset information by segment is not disclosed because this information is not used by the CODM…" (10Q p.15). Flattering? Neutral. The asset base is ~$8.8bn of goodwill [D] (10A p.367), so segment ROIC can no longer be tracked.
- **CODM.** The 10A names the "President of S&P Global Mobility". The 10Q names "the Chief Executive Officer, who was previously the President of S&P Global Mobility" (10Q p.14). Same person; no flag.
- **"Segment expenses".** The 10A figure includes depreciation and SBC. The 10Q figure excludes D&A, SBC, transaction and severance costs. CARFAX Q1-26 162 (10A) and Q2-26 159 (10Q) **are not comparable** (`segments_kpi_NOTES.md`).

## 3. Growth attribution: "new business" (10/A) vs "price" (10-Q). New red flag.

**Wording by vintage**
- **10A, Q1-26:** revenue rose "due to continued new business growth and solid underwriting volumes of $26 million and $2 million, respectively, and the remaining increase driven by improved contract terms" (10A p.347).
- **10A, FY25:** "continued new business growth and solid underwriting volumes of $76 million and $13 million, respectively, and the remaining increase driven by improved contract terms" (10A p.349–350).
- **10A, FY24:** the same wording with $80m and $17m. "Contract terms" is not mentioned (10A p.350).
- **10Q, Q2/6M-26:** "driven primarily by price increases of approximately $16 million and $36 million, respectively, and continued new business growth of approximately $8 million and $20 million, respectively" (10Q p.27).
- **10Q, CARFAX:** "primarily driven by price increases". **10Q, B2B:** "primarily due to continued new business growth" (10Q p.28–29).

**Arithmetic [C]: implied Q1 = 6M − Q2**
- Price ≈ $36m − $16m = **$20m**.
- New business ≈ $20m − $8m = **$12m**.
- The 10A, 10 weeks earlier, attributed **$26m** of the same quarter to new business, and only the residual to "improved contract terms". The residual is ≈ $35m − 28m ≈ $7m on total revenue, or ≈ $1m on subscription ($29m subscription increase [C]).

**Interpretation**
- Either Q1 was re-attributed, or the two filings define "new business" differently. **Inference:** the Form 10 vocabulary ("new business growth", "improved contract terms") appears to have absorbed price.
- **FY25 under the 10A wording [C]:** subscription +$123m = new business $76m + underwriting $13m + residual ~$34m.
- **Same implication for SPGI-era commentary.** SPGI stopped naming price as a Dealer driver after Q4-23 and attributed 2024–25 growth to "new business growth" (see D7).
- **Unflattering?** **Yes.** The 10-Q split shows new business of only ~$8m in Q2 (~1.8 pt of growth [C]), versus price ~$16m (~3.6 pt [C]). That is the quarter growth slowed to 6.6% reported [C] and guidance was cut.
- **Honest qualifier:** both filings say "approximately", and neither defines the terms. A PDF read or management confirmation is needed before asserting a restatement.

## 4. FY2026 revenue guide: organic constant currency → reported basis

| Vintage | Exact wording | Basis | Source |
|---|---|---|---|
| SPGI Q4-25 deck, 2026-02-10 | Mobility "7.5 % to 9 %" under "Organic, Constant Currency Revenue Growth" | OCC | SPGI-Q4-25 p.26 |
| SPGI Q1-26 deck, 2026-04-28 | "7.5 % to 9 %" previous = current | OCC | SPGI-Q1-26 p.24 |
| MBGL ID, 2026-05-12 | "You saw we just reaffirmed guidance for 2026 at 7.5%-9%." Slide 90: "2026E 7.5-9% organic cc". | OCC | [Investor Day : Calderone : 2026-05-12 : [8007.2s](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=8007.2)]; ID-deck p.90 |
| MBGL Q2, 2026-08-07 | "we are lowering our full year revenue guidance to 6.9%-7.7% growth"; $1,870–1,885m | Reported | [Q2 call : Eager : 2026-08-07 : [243.34s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=243.34)]; Q2-deck p.9 |

**Like-for-like [C]**
- 1H FX benefit is ~$5m [IR], and no 2H FX is assumed [D] (Q2-deck p.9).
- On that basis, the new guide in OCC terms ≈ ($1,870–5)/1,750 − 1 = **6.6%** to ($1,885–5)/1,750 − 1 = **7.4%**.
- The OCC cut is therefore ~**0.9–1.6 pt**. The headline comparison (7.5–9 vs 6.9–7.7) implies 0.6–1.3 pt.
- The `TARGETS_TIMELINE.md` "−60/−130 bp" understates the cut for the same reason.

**Unflattering?** **Yes.**
- **Organic growth stopped being printed.** SPGI printed "Mobility Organic Constant Currency Revenue Growth" on every 2025 Mobility slide (e.g. "+10%" Q1/Q2-25, "+8%" Q3/Q4-25; SPGI-Q1-25 p.23, SPGI-Q2-25 p.18, SPGI-Q3-25 p.17, SPGI-Q4-25 p.22). MBGL's Q2 deck prints only the FX benefit (~$1m Q2, ~$5m 1H [D]; Q2-deck p.5).
- **Spoken organic figures are ambiguous.** The call says "approximately 7% organic" [IR]. For 1H, "Including the impact of FX, we grew approximately 6.8%" is ambiguous; ex-FX 1H ≈ 6.9% [C].
- The basis switch happened when OCC growth fell below the old floor: Q1-26 ≈ 7.4% [C] and Q2-26 ≈ 6.4% [C] (see D10).

## 5. Q2-2025 Adjusted EBITDA: 186 (ID-deck) vs 188 (Q2-deck / 10-Q)

| Line, Q2-25 ($m) | ID-deck p.112/114 (May-12) | 10Q p.15 / Q2-deck p.13 (Aug-7) |
|---|---|---|
| Net income | 65 [D] | 65 [D] |
| Interest | 3 [D] | 4 [D] |
| Tax | 27 [D] | 27 [D] |
| D&A | 78 [D] | 77 [D] |
| SBC | 4 [D] | 4 [D] |
| Non-recurring / Transaction + severance & other | 10 [D] (one line) | 2 + 9 = 11 [D] |
| **Adjusted EBITDA** | **186** | **188** |

- **Q1-25 recast [C].** 6M-25 is 357 [D] (10Q) less Q2-25 188 = **169**, against **170** on the ID-deck. Q1-25 moved down 1 and Q2-25 moved up 2. 1H-25 is 356 → 357.
- **Explanation.** None is printed. The arithmetic differences are interest 3→4, D&A 78→77 and add-backs 10→11. **Inference:** this is re-rounding plus the new item-(6) catch-all.
- **Unflattering? No; it works against the company.** A higher Q2-25 base lowers reported growth:
  - Q2-26 growth 202/188 = **7.4%** [C] vs 202/186 = 8.6%.
  - Q2 margin expansion +40 bp [IR] vs ~+80 bp on the old base [C].
- **FY25 Adj. EBITDA of $711m [D]** (10A) has not been republished on the 6-item definition. Whether FY25 changes on recast is unknown.

## 6. EPS for carve-out periods

- **F10/10A:** "Net earnings per share data has not been presented in the combined financial statements because Mobility did not operate as a separate legal entity with its own capital structure" (10A p.446 annual; p.428 interim; F10 p.524/506).
- **10Q:** prints EPS for all four periods: Q2-26 $0.18, Q2-25 $0.22, 6M-26 $0.37, 6M-25 $0.42 [D]. The footnote says 294,821,320 shares "was used to calculate both basic and diluted earnings per share for the three and six months ended June 30, 2026 and 2025… There were no shares outstanding as of June 30, 2025" (10Q p.11).
- **Basis is stated**, which resolves the earlier statements_NOTES flag. Diluted = basic, so the unvested RSUs are ignored [D].
- **Unflattering? No.** The comparison shows EPS down −18% [C], so printing it does not flatter. It is a methodology inconsistency only: a pre-spin period gets per-share data the Form 10 said could not exist.

## 7. One-time stand-up costs: 75–100 → ~100 → 75–110

| Vintage | Wording | Source |
|---|---|---|
| ID-deck slide 97 / ID call (May-12) | "~$75-100M over 12-18 months" (fn: INTERNAL DATA); "$75 million-$100 million of cash over the first 12-18 months" | ID-deck p.97; [Investor Day : Calderone : 2026-05-12 : [8612.03s](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=8612.03)] |
| Q2 call / Q2-deck (Aug-7) | "approximately $100 million in one-time cash costs… approximately half of this incurred in 2026"; "roughly 50% … capitalized" | [Q2 call : Calderone : 2026-08-07 : [1344.91s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1344.91)]; Q2-deck p.9 |
| 10Q MD&A (Aug-7) | non-recurring stand-alone/TSA transition costs "$75 million to $110 million" | 10Q p.23 |

- **Unflattering? Yes, mildly.** On the same day the call moved to the top of the old range and the 10-Q **raised the ceiling** to $110m.
- **The ~50% capitalisation is new at Q2.** It moves roughly half of the cost out of the P&L and out of FCF-before-capex optics.
- **Already expensed as "transaction costs" (pre-spin) [D]:** $21m in FY25 and $57m in 6M-26, $78m in total (10A p.350; 10Q p.17). It is **not stated** whether these sit inside or outside the ~$100m.
- **Inference:** two definitions ("transaction costs" excluded from Adj. EBITDA vs "one-time stand-up cash") coexist, and investors cannot reconcile them.

## 8. Standalone run-rate cost: "$20–25M" → "high end" → 150 bp

- **ID-deck p.96:** "~$20-25M in run-rate costs … compared to historic SPGI allocations".
- **Q2 call:** "reducing full year margins by approximately 150 basis points relative to our fiscal year 2025 baseline … This equates to the high end of the $20 million-$25 million range" [Q2 call : Calderone : 2026-08-07 : [1221.31s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1221.31)].
- **Check [C]:** 1.50% × FY25 revenue of $1,750m [D] = **$26.3m**, above the top of the range. On FY26 guided revenue (~$1,878m midpoint) it is ~$28m.
- **GS conference:** "75 basis points of it this year and then the full 150 next year"; "probably not going to get to the full 50 basis point expansion target until 2028" [GS : Calderone : 2026-09-10 : [1642.34s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1642.34)].
- **Unflattering? Yes.** The units switched from dollars to basis points when the dollar figure would have exceeded the range. The margin-expansion start date also slipped to 2028.

## 9. Medium-term margin target: SPGI 41–43% → MBGL "+50 bp/yr after reset"

- **SPGI Investor Day 2022-12-01:** "S&P Global Mobility … 2025/2026 Target Model: 7 %-9 % Annual Organic Revenue Growth; 41 %-43 % Adjusted Operating Profit Margin" ([SPGI ID-2022 deck p.79](https://web.quartr.com/companies/3977?companyId=3977&documentId=95359&documentType=slide&eventId=44944&navigation=external&utm_medium=referral&utm_source=mcp&sp=79)).
- **Delivered:**
  - FY25 revenue +8.6% [D]: target met.
  - FY25 adjusted operating margin **39.9%** [D] ([SPGI-Q4-25 p.6](https://web.quartr.com/companies/3977?companyId=3977&documentId=2795238&documentType=slide&eventId=393534&navigation=external&utm_medium=referral&utm_source=mcp&sp=6)): **missed by 110–310 bp** [C].
- **MBGL framework (ID 2026):** "~50bps annual margin expansion target" after a "standalone reset" (ID-deck p.30/96). The base is reset to "39.1-ish%" (GS).
- **Unflattering? Yes.**
  - The absolute-level target that was being missed disappears.
  - It is replaced by a rate-of-change target from a lower, re-measured base, and the measure changes from SPGI adjusted OP margin to MBGL Adjusted EBITDA margin. The EBITDA measure is higher for the same business; see §12.
- **2026 division margin guidance.** SPGI's 2026 deck dropped division margin guidance (only an enterprise "10 to 35 bps") (SPGI-Q4-25 p.25–26), although it had given Mobility margin ranges every year 2023–2025.

## 10. Net revenue retention removed from the Investor Day deck

- **Wording:** "We actually had an NRR number in the presentation early on. We pulled it." … "meaningfully north of 100%" [Investor Day : Calderone : 2026-05-12 : [10177.24s](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=10177.24)].
- **Filings:** no NRR, gross retention, churn or ARPU in F10, 10A or 10Q (`segments_kpi_NOTES.md`).
- **Unflattering?** Unknown. Management's stated reason is replicability. The 10A names "average monthly price per location" as the CARFAX revenue driver (10A p.340) but never prints it.

## 11. Disclosures printed by predecessors that MBGL does not print

| Disclosure | Last predecessor print | MBGL status | Unflattering? |
|---|---|---|---|
| Business-line revenue $ (Dealer / Manufacturing / Financials & Other), quarterly | SPGI every quarter through Q1-26, e.g. Q4-25 Dealer $274m (+10%), Manufacturing $91m (+1%), Fin & Other $80m (+11%) [D] ([SPGI-Q4-25 p.22](https://web.quartr.com/companies/3977?companyId=3977&documentId=2795238&documentType=slide&eventId=393534&navigation=external&utm_medium=referral&utm_source=mcp&sp=22)) | Replaced by CARFAX/B2B segments. B2B business-line split given only as % of FY25 (ID-deck p.93, 34). | **Yes.** Manufacturing (Polk planning, recall) was the weak line: −3% Q3-25 [IR] (SPGI-Q3-25 call), +1% Q4-25. |
| Organic constant-currency growth by division | SPGI 2025 slides (Mobility +10/+10/+8/+8%) | Not printed; only FX $ | **Yes** (see §4) |
| Recurring revenue % / TTM adjusted margin | SPGI 2022 slides ("Recurring revenue as % of revenue" 78.3% Q4-22) [D] | "Subscription" % (81–82%) [D]; no TTM margin | No; definitional |
| Division margin guidance | SPGI 2023–25 | MBGL guides only FY Adj. EBITDA $ (~40%) | Neutral |
| Transportation "recurring revenue organic growth" | INFO10K FY2016–21 (10/10/11/10/3/18%) [D] | n/a. Scope differs (P0 includes Maritime & Trade) | n/a |
| CARFAX record / source counts | INFO FY2021 "more than 27 billion records … more than 130,000 data sources" [D] | Still printed: 38bn+ records, 177,000+ sources [D] (10A p.263) | No (continued) |
| Car Care users | SPGI Q1-25: "approximately 46 million users" [IR] | 53m+ [D] (10A p.263). Goal "150 million" US+Canada (ID) became US "north of 100 million" (GS). | Mixed; goal reframed |

## 12. S&P Global 10-K Mobility segment vs Form 10/A carve-out, FY2023–25: every difference explained

| $m | FY23 SPGI | FY23 10A | Δ | FY24 SPGI | FY24 10A | Δ | FY25 SPGI | FY25 10A | Δ |
|---|---|---|---|---|---|---|---|---|---|
| Revenue | 1,484 [D] | 1,485 [D] | +1 | 1,609 [D] | 1,613 [D] | +4 | 1,747 [D] | 1,750 [D] | +3 |
| Subscription | 1,169 | 1,170 | +1 | 1,299 | 1,303 | +4 | 1,422 | 1,426 | +4 |
| Non-subscription | 315 | 315 | 0 | 310 | 310 | 0 | 325 | 324 | −1 |
| U.S. | 1,223 | 1,224 | +1 | 1,325 | 1,329 | +4 | 1,451 | 1,454 | +3 |
| International | 261 | 261 | 0 | 284 | 284 | 0 | 296 | 296 | 0 |
| Segment OP (SPGI) / total segment OP (10A) | 260 | 271 | +11 | 312 | 328 | +16 | 378 | 384 | +6 |
| Corporate Unallocated (10A only) | — | (32) | | — | (30) | | — | (45) | |
| OP (SPGI segment vs carve-out total) | 260 | 239 | −21 | 312 | 298 | −14 | 378 | 339 | −39 |
| Amortization of acquired intangibles | 301 | 295 | −6 | 303 | 296 | −7 | 303 | 296 | −7 |
| Total D&A | 314 | 307 | −7 | 317 | 309 | −8 | 320 | 310 | −10 |
| "Adjusted" margin | 38.8% adj. OP [D] | 40.3% Adj. EBITDA [C] 598/1,485 | | 39.0% | 40.8% [C] 658/1,613 | | 39.9% | 40.6% [D] | |

Sources: SPGI10K-FY2025 p.61, 119–122 (FY23–25 columns identical in the FY23 and FY24 10-Ks per predecessor_NOTES); 10A p.349, 352, 440, 285; SPGI adjusted margins from SPGI-Q4-23 p.16, SPGI-Q4-24 p.12 and SPGI-Q4-25 p.6.

**Explanations**

1. **Revenue +1/+4/+3 sits entirely in U.S. subscription.** The carve-out reports "Data sharing revenues" from S&P Global of **$3m in each year** [D] (10A p.465). SPGI eliminates this on consolidation, where intersegment revenue is printed as nil.
   - Quarterly check: SPGI Mobility Q1-26 $454m vs MBGL $455m; Q2-25 $438m vs $439m; Q1-25 $420m vs $420m [D] (SPGI decks; 10Q).
   - Residual −2 (FY23) and +1 (FY24) is rounding [C].
2. **Amortization is 6–7 lower in the carve-out.** Not explained in the documents read. **Inference:** SPGI's segment charge includes amortization on intangibles that S&P Global retained or recognised at parent level and that were not pushed down to the carve-out. Depreciation also differs by 1/1/3 [C].
3. **Segment OP is higher in the carve-out (+11/+16/+6), but total OP is lower (−21/−14/−39).** The carve-out moves some costs out of segments into a "Corporate Unallocated" line of $32m/$30m/$45m [D]. That line includes FY25 transaction costs of $12m, severance of $5m and ELT costs of $5m [D] (10A p.350 fn3). The 10A also says the 2025 "refinement of segment cost allocation methodologies" was applied to all periods (10A p.349).
   - Bridge [C]: SPGI OP + amortization difference + revenue difference − Corporate Unallocated = 235/293/343, against carve-out OP 239/298/339.
   - Residual +4/+5/−4 = other allocation differences. The carve-out's corporate allocations from the parent were $89m/$90m/$112m [D] (10A p.465), against SPGI's own internal charging. They are not separately reconcilable.
4. **The adjusted margin measure changed** from SPGI adjusted OP margin (after depreciation and SBC, before amortization) to MBGL Adjusted EBITDA (before depreciation and SBC).
   - On the same business, MBGL's measure is **+1.5/+1.8/+0.7 pt higher** [C].
   - Add-backs that are not in SPGI's adjusted OP: depreciation $12m/$13m/$14m and SBC $20m/$28m/$22m [D] (10A p.440; Note 6). These are partly offset by the extra corporate allocations in the carve-out.
   - **Inference:** a "~40%" MBGL Adjusted EBITDA margin is roughly equivalent to ~38–39% on the SPGI basis [E] (assumes ~$15–30m gap persists). The 41–43% SPGI target in §9 is therefore even further away.
5. **FY24 growth is printed 8% (SPGI) vs 9% (10A).** 1,609/1,484 = 8.4% vs 1,613/1,485 = 8.6% [C]; rounding at the boundary. ID-deck slide 90 labels 8.6% as "Organic Growth". It is reported growth. Organic would be ≈ 8.8% [C] (ex Market Scan +$3m, Catalyst −$5m [D] 10A p.350), so the label understates slightly.

## 13. Smaller items

| Item | Vintages | Unflattering? |
|---|---|---|
| **TAM source unnamed.** "according to an independent third-party consulting firm" ($75–81bn) (10A p.266 = F10 p.345). ID-deck: "2025 ESTIMATES FROM INDEPENDENT THIRD-PARTY CONSULTING FIRM; MIDPOINT OF RANGES" ($78bn) (ID-deck p.27). Never named in any document read. The CARFAX TAM is cited as $26bn by the CEO and $60bn on slide 71 (core+extended vs total). | F10 → ID | Neutral, but unverifiable [X unnamed] |
| **Payment to SPGI.** "approximately $1.9 billion" (10A p.278, 321) → "$2.0 billion dividend" (10Q p.12, 18) | 10A → 10Q | Mildly: more debt-funded cash leaving |
| **Leverage target.** "target gross leverage ratio of 2.5 times or below" (ID) → "2.5x-ish" (GS); actual gross 2.7x [IR] | ID → GS | Yes, wording softened while above target |
| **Dividend payout.** "20%-25% of net income" (ID) → "pegged at 25% of GAAP net income", "normalized" (GS). $0.06 × 4 × 294.8m ≈ $71m ≈ 32% of FY25 NI of $220m [C]. | ID → GS | Yes: "normalized" undefined |
| **Medium term.** "2028 and beyond" (ID Q&A) → "That's really when the medium-term targets, in our mind, start" (GS) | ID → GS | Yes: clock reset |
| **Headcount.** "over 3,400 FTEs" (10A p.268) vs ~3,522 (10A p.384) vs "3,500" (GS) | — | No |

---

## Honest counters

- **Most changes have benign explanations.**
  - Spin-offs routinely move to Adjusted EBITDA segment measures.
  - They drop parent-era business lines and stop presenting parent-format organic growth.
  - The 10-item → 6-item definition simply removes empty categories.
- **Several changes cut against the company.**
  - The Q2-25 recast (186 → 188) *lowers* reported growth.
  - Printing carve-out EPS *shows* a −18% decline.
  - The 10-Q's new price/new-business split *volunteered* that growth is mostly price. That is more candid than the Form 10's euphemism ("improved contract terms").
- **The B2B segment OP collapse is mostly one-off spin costs** ($33m 6M-26 [D]). On the Adjusted EBITDA measure B2B grew +10% 6M [D], which is the economically fairer view of run-rate profit.
- **Unproven items.**
  - The new-business vs price discrepancy (§3) rests on subtracting "approximately" figures. It could reflect a definitional clarification rather than a re-attribution.
  - The SPGI–carve-out amortization gap (§12.2) is unexplained in the text read, not shown to be wrong.
- **Management did not hide the guide cut.** The CEO stated it in the first ~4 minutes of the Q2 call.
- **The reported-basis guide carries only ~$5m (~0.3 pt) of banked 1H FX** [C], and no 2H FX is assumed [D]. So the basis switch inflates the new number only modestly. The bigger issue is losing a comparable organic series.
