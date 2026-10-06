# D3 — Group decomposition, corporate wedge, standalone normalized net income

Prepared 2026-10-06 by the Part D analyst. Sources: `extraction/segments_kpi.csv`, `statements.csv`, `notes.csv`, `presentations.csv`, transcript quote banks, and a re-read of 10-Q (Quartr 3699447) pp.27-30.

**Tiers:** [D] disclosed · [C] computed · [E] estimate · [IR] management verbal · [X] third party.

**Keys:**
- 10A = Form 10/A, 2026-05-27, Quartr page.
- 10Q = 10-Q Q2-26.
- ID = Investor Day deck 3352878 (slide). ID-T / Q2-T / GS-T = transcripts dated 2026-05-12 / 2026-08-07 / 2026-09-10.
- $m.

**Two bases, never mixed:**
- **Basis 1, Form 10/A segment operating profit:** after acquired-intangible amortization and special items; before Corporate Unallocated, Other income and interest. The 10-Q MD&A also prints segment OP for Q2/6M (p.24-25), so Basis 1 can be extended to Q2.
- **Basis 2, Adjusted EBITDA:** the 10/A "Segment Adjusted EBITDA" for FY / Q1 and the 10-Q Note 7 Adj. EBITDA (the new CODM measure from Q2-26) for Q2 / 6M.
  - The two Adj. EBITDA definitions differ in wording (10 vs 6 exclusions; segments_kpi_NOTES).
  - They tie numerically for Q1-26: 10-Q 6M − Q2 equals 10/A Q1 for CARFAX 140, B2B 49 and Corporate −5.

---

## Summary
1. **Segment profit identities hold in every period on both bases** [D/C]. On Basis 2, CARFAX supplies ~75% of Adj. EBITDA (536 of 711 in FY25). Corporate Unallocated is a small wedge: $16-22m a year before specials.
2. **The real corporate cost is in the S&P Global allocations, not in "Corporate".**
   - Allocations were $89m / $90m / $112m in FY23-25 [D], or ~$100m in FY25 excluding $12m of allocated stand-up costs.
   - They are mostly pushed into the segment lines.
   - The standalone add-on is guided at ~150bp of FY25 revenue (≈$26m, "high end of $20-25m") [IR]. That implies a run-rate corporate cost base of ~$126m [C] and a reset FY25 margin of ~39.1% [IR].
3. **The $2.0bn notes carry $110.6m a year of cash coupon** (5.53% weighted) [C]. The printed pro forma interest is $114m including fee and OID amortization [D]. This lifts interest from $13m (carve-out) to ~8.5x that level.
4. **Standalone normalized net income [C] is ~$165-180m on a FY25 base and ~$210m on a FY26 run-rate.**
   - The dividend is **$70.8m** a year [C]: $0.06 × 4 × 294.8m. That is **34-43%** of those figures, not 25%.
   - A 25% payout requires normalized NI of **~$283m**.
   - That figure is reached only by (i) a definition that adds back part of the after-tax acquired-intangible amortization, or (ii) earnings around FY28.
   - **Management's "25% of normalized net income" is not reproducible from disclosed data.** The dividend is still small against estimated standalone FCF of ~$365m (~19%) [C].

---

## 1. Segment + segment − Corporate = combined profit

### Basis 1, operating profit (10/A segment OP; 10-Q MD&A OP for Q2/6M)
| Period | CARFAX OP | B2B OP | Corporate Unallocated | = Total OP | Printed total | Source |
|---|---|---|---|---|---|---|
| FY2023 | 210 | 61 | (32) | 239 | 239 | 10A p.352, 461-462 |
| FY2024 | 259 | 69 | (30) | 298 | 298 | 10A p.352, 461 |
| FY2025 | 322 | 62 | (45) | 339 | 339 | 10A p.352, 461 |
| Q1-2025 | 77 | 14 | (7) | 84 | 84 | 10A p.348, 431 |
| Q1-2026 | 89 | 5 | (13) | 81 | 81 | 10A p.348, 431 |
| Q2-2025 | 89 | 16 | (9) | 96 | 96 | 10Q p.25 |
| Q2-2026 | 101 | 3 | (22) | 82 | 82 | 10Q p.24 |
| 6M-2025 | 166 | 30 | (16) | 180 | 180 | 10Q p.25 |
| 6M-2026 | 190 | 8 | (35) | 163 | 163 | 10Q p.25 |

**Below-the-line bridge to net income [D]**

| Period | Total OP | Other income | Interest, net | Pre-tax | Tax | Net income | Source |
|---|---|---|---|---|---|---|---|
| FY2023 | 239 | 2 | (17) | 224 | (61) | 163 | 10A p.440 |
| FY2024 | 298 | 1 | (15) | 284 | (76) | 208 | 10A p.440 |
| FY2025 | 339 | 0 | (13) | 326 | (106) | 220 | 10A p.440 |
| Q2-2026 | 82 | — | (7) | 75 | (22) | 53 | 10Q p.4 |
| 6M-2026 | 163 | — | (10) | 153 | (45) | 108 | 10Q p.4 |

### Basis 2, Adjusted EBITDA
| Period | CARFAX | B2B | Corporate | = Sum | Printed total | Note |
|---|---|---|---|---|---|---|
| FY2023 | 422 | 191 | (16) | 597 | 598 | Printed footing break (segments_kpi_NOTES) |
| FY2024 | 476 | 203 | (20) | 659 | 658 | Printed footing break |
| FY2025 | 536 | 197 | (22) | 711 | 711 | |
| Q1-2025 | 130 | 44 | (5) | 169 | 169 | |
| Q1-2026 | 140 | 49 | (5) | 184 | 184 | B2B 49 from Form 10 p.438 |
| Q2-2025 | 142 | 49 | (3) | 188 | 188 | Investor Day deck showed 186 → **recast** to 188 (presentations_NOTES) |
| Q2-2026 | 153 | 53 | (4) | 202 | 202 | 10Q p.14 |
| 6M-2025 | 272 | 93 | (8) | 357 | 357 | |
| 6M-2026 | 293 | 102 | (9) | 386 | 386 | |

Segment Adj. EBITDA margins [C]:
- CARFAX: 45.5% / 45.8% / 46.9% (FY23-25); 48.0% (6M-26).
- B2B: 34.3% / 35.4% / 32.4%; 32.6% (6M-26).
- Corporate as % of group revenue: 1.1% / 1.2% / 1.3%; 1.0% (6M-26).

### Basis 1 → Basis 2 walk by segment, FY2025 [D, 10A p.359; 10A p.350 footnotes]
| | CARFAX | B2B | Corporate | Total |
|---|---|---|---|---|
| Segment OP | 322 | 62 | (45) | 339 |
| + Acquired-intangible amortization | 189 | 107 | — | 296 |
| + Special items (severance, transaction, ELT, legal, other) | 3 [C, residual] | 14 (13 + 9 − 5 − 3) | 23 (12 + 5 + 5 + 1) | 40 |
| = Adjusted OP | 514 | 183 | (22) | 675 |
| + Depreciation + SBC | 22 [C, residual] | 14 [C, residual] | 0 | 36 |
| = Segment Adj. EBITDA | 536 | 197 | (22) | 711 |

Note: the 2026 special items sit heavily in **B2B**, not Corporate. Transaction costs in 6M-26 were B2B $33m and Corporate $24m [D, 10Q p.25]. B2B GAAP OP of $8m in 6M-26 therefore understates the segment's economics.

## 2. The Corporate / unallocated wedge

| Wedge component | FY23 | FY24 | FY25 | Q1-25 | Q1-26 | Q2-25 | Q2-26 | 6M-25 | 6M-26 | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| Corporate Unallocated (OP basis) | 32 | 30 | 45 | 7 | 13 | 9 | 22 | 16 | 35 | 10A p.352, 348; 10Q p.24-25 |
| … of which special items | 16 | 10 | 23 | 2 | 8 | 6 | 18 | 8 | 26 | 10A p.359-360; 10Q p.24-25 |
| Corporate Adj. EBITDA (recurring wedge) | (16) | (20) | (22) | (5) | (5) | (3) | (4) | (8) | (9) | same |
| **Corporate allocations from S&P Global (total, all lines)** | 89 | 90 | 112 | 22 | 28 | 24 | 36 | 46 | 64 | 10A p.434, 465; 10Q p.16 |
| … of which allocated stand-up / transaction costs | n/d | n/d | ~12 | — | ~7 | ~2 | ~15 | ~2 | ~22 | 10A p.435, 466; 10Q p.17 |
| … of which severance in allocations | | | | | | | 2 | | 2 | 10Q p.16 |
| **Allocations ex one-time [C]** | 89 | 90 | ~100 | 22 | ~21 | ~22 | ~19 | ~44 | ~40 | [C] |
| Allocations ex one-time as % of revenue [C] | 6.0% | 5.6% | 5.7% | 5.2% | 4.6% | 5.0% | 4.1% | 5.1% | 4.3% | [C] |

**Interpretation**
- *Inference:* the allocations (~$100m) are 4-5x the Corporate Unallocated recurring wedge (~$22m). Most S&P Global allocated cost is therefore embedded in the CARFAX and B2B segment expense lines. Segment margins are "post-allocation", not "pre-corporate".
- Management will "reallocate" some costs into corporate over the next 1-2 quarters (GS-T 1694.2s). Expect reported Corporate to widen and segment margins to rise mechanically from Q3/Q4-26 (feed D4).

**Standalone vs allocated vs one-time: three distinct things**

| Layer | Amount | Tier | Treatment |
|---|---|---|---|
| (i) Historical allocations (recurring) | ~$100m (FY25 ex one-time) | [C] from [D] | Already in carve-out P&L and Adj. EBITDA |
| (ii) Incremental standalone run-rate vs allocations | "$20 million-$25 million in run rate expense" ([ID-T 8463.17s](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=8463.17)). Re-stated as "approximately 150 basis points" of FY25 margin = "the high end" ([Q2-T 1221.31s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1221.31)) | [IR] | Recurring; hits Adj. EBITDA. [C] 150bp × FY25 revenue 1,750 = **$26.3m**; × FY26 guide midpoint 1,877.5 = $28.2m (just above the stated range). Phasing: ~75bp in 2026, 150bp in 2027 ([GS-T 1642.34s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1642.34)) |
| … printed subset | Pro forma "autonomous entity" S&G +$12m (new office rent 9 + incremental TSA 3), FY25 | [D] 10A p.339 | *Inference:* this is a subset of (ii), not additive |
| (iii) SBC step-up | from "1% range" to "3%-4%" of revenue ([ID-T 8519.49s](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=8519.49)) | [IR] | Excluded from Adj. EBITDA but a GAAP cost. [C] +$31-48m a year at FY25 revenue (3-4% × 1,750 − 22). **Not** inside the 150bp |
| (iv) One-time stand-up costs | Pre-spin transaction costs recognized: FY25 21; Q1-26 21; Q2-26 36 (cumulative **$78m** through 6/30/26) [D]. Post-spin guide: ~$100m one-time cash, ~half in 2026, ~50% capitalized [IR]; 10-Q range "$75 million to $110 million" [D, 10Q p.23] | [D]/[IR] | Non-recurring; excluded from Adj. EBITDA and from normalized NI below. *Inference:* overlap between the $78m recognized and the ~$100m guide is not stated |

**Margin reset check [C].**
- FY25 Adj. EBITDA margin was 40.6% (711 / 1,750). Less 150bp gives ~39.1%, which matches "resetting 2025 to 39.1-ish%" [IR GS-T].
- FY26 guidance ($745-760m on $1,870-1,885m) implies a 2H-26 margin of **37.9-38.9%** against 39.7% in 2H-25 [C]. Method: (guide − 6M-26 386) ÷ (guide revenue − 923).
- That is ~80-180bp lower. It is consistent with ~150bp of 2H standalone cost (half-year phasing of the 75bp full-year) plus seasonal advertising.

## 3. Pro forma interest burden on the $2.0bn notes
| Tranche | Principal | Coupon | Annual cash coupon [C] |
|---|---|---|---|
| 5.050% 2029 | 650 | 5.050% | 32.8 |
| 5.450% 2031 | 650 | 5.450% | 35.4 |
| 6.050% 2036 | 700 | 6.050% | 42.4 |
| **Total** | **2,000** | **5.53% weighted** | **110.6** |

Sources: 10Q p.11; 10A p.337.

| Measure | Value | Tier |
|---|---|---|
| Pro forma FY25 interest on notes incl. OID / fee amortization | 114 (weighted 5.74%) | [D] 10A p.338 |
| Less removal of Canada Carfax Loan interest | (14) → net PF adjustment +100; PF interest 113 | [D] 10A p.335, 338 |
| Guided 2H-26 interest expense | ~55 (annualized ~110) | [IR] Q2-T 1555.86s |
| First cash coupon (Q4-26) | ~60, covering accrual from 2026-05-29 | [IR]; [C] 2,000 × 5.53% × ~0.55yr ≈ 61 |
| Interest income offset | Cash $186m at 6/30/26 [D] × ~4% [E] ≈ 7 | [E] |
| Run-rate net interest used below | **~110** | [C/E] |
| Coverage: FY25 Adj. EBITDA / interest | 711 / 110 = 6.5x | [C] |
| Coverage: standalone normalized OP / interest | 353 / 110 = 3.2x | [C] |
| Gross leverage | 2.7x at spin; 2.8x on LTM Q1-26 (ID 115); target ~2.5x via EBITDA growth (no prepayable debt) | [IR]/[D-deck] |

Interest takes **~31%** of standalone normalized pre-interest operating profit [C] (110 ÷ 353). In the carve-out it took 4% (13 ÷ 339).

## 4. Bridge: carve-out net income → standalone normalized net income [C]

**Assumptions** (each stated; base case in bold)
- A1. One-time items: FY25 "Non-Recurring Adjustments" of 40 [D, ID 111; components in 10A p.350/359] are added back.
- A2. Standalone increment = **150bp × FY25 revenue = 26.3** [IR→C]. It is assumed to include the PF rent and TSA of 12 (no double count).
- A3. SBC is held at the FY25 $22m in the base case. A scenario steps it to 3% of revenue [IR→E].
- A4. Interest = **110** run-rate (range 107-114) [C/E]. Canada loan interest is eliminated.
- A5. Tax rate: FY25 actual 32.5% [D]; **FY26 guide midpoint ~29.5%** (28-31% slide; 28-30.5% call) [IR]; medium-term 25-27% [IR].
- A6. Acquired-intangible amortization of ~296 a year stays in GAAP NI (it is "normalized GAAP").
- A7. The DTL cash-tax effect (~$89m a year above the provision) affects cash, not NI.

| Step | FY25 base | Source / tier |
|---|---|---|
| Carve-out net income | 220 | [D] 10A p.440 |
| + Tax | 106 | [D] |
| + Interest, net (carve-out, incl. Canada loan) | 13 | [D] |
| − Other income | 0 | [D] |
| = Operating profit | 339 | [D] |
| + One-time items (A1) | 40 | [D-deck] |
| = Normalized carve-out OP | 379 | [C] |
| − Standalone increment (A2) | (26) | [IR→C] |
| = **Standalone normalized OP** | **353** | [C] |
| − Run-rate interest (A4) | (110) | [C/E] |
| = Pre-tax | 243 | [C] |
| − Tax @ 29.5% (A5) | (72) | [E] |
| = **Standalone normalized NI, FY25 base** | **~171** | [C] |

**Sensitivity** (NI; payout = $70.8m ÷ NI)

| | Tax 26% | Tax 29.5% | Tax 32.5% |
|---|---|---|---|
| Interest 107 | 182 (39%) | 173 (41%) | 166 (43%) |
| Interest 110 | 180 (39%) | **171 (41%)** | 164 (43%) |
| Interest 114 | 177 (40%) | 168 (42%) | 161 (44%) |

Further cases:
- **SBC at 3% of revenue (A3 scenario):** NI ≈ 150 → payout 47%.
- **Cross-check to the company-printed pro forma.**
  - The Form 10/A pro forma FY25 NI is **139** [D, 10A p.335]. It includes the notes interest and the +12 AEA, but also the 40 of one-time costs, at a ~35% PF tax rate.
  - [C] Adding back one-time costs after tax (40 × 0.675) and deducting the remaining standalone increment ((26 − 12) × 0.675) gives **~156**.
  - The bridge above (164 at the same 32.5% tax) is consistent within ~$8m. The gap is the PF's higher marginal tax on adjustments.
- **FY26 run-rate variant [C/E].**
  - Guide-midpoint Adj. EBITDA is 752.5. Deduct the remaining 75bp not yet in 2026 (14) to get 738.
  - Then deduct D&A 310 [D run-rate: 6M-26 155], SBC 22 and interest 110 to get 296 pre-tax.
  - At 29.5% tax → **NI ≈ 209**; payout 34%.
- **FY27 illustrative [E].**
  - Assumes Adj. EBITDA +7.5% → ~794, SBC 3% of revenue (~61), interest 107 and tax 26%.
  - **NI ≈ 234**; payout 30%.
- **"Adjusted NI" (ex acquired amortization) [C].** Adding back 296 × (1 − 26%) = 219 to the base gives **~390**. The payout is then **18%**.

## 5. Testing the "25% of normalized net income" dividend claim
**The claim, as it evolved:**
- **Investor Day:** "a dividend payout ratio of 20%-25% of net income" ([ID-T 8777.15s](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=8777.15)).
- **GS:** "We pegged at 25% of GAAP net income." ([GS-T 1917.37s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1917.37)) and "we call it a normalized GAAP net income" ([GS-T 1966.97s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1966.97)).
- **Not printed in the 10-Q.** It states only the intention to pay $0.06 a quarter [D, 10Q p.30].

**Arithmetic [C]**
- Annual dividend = $0.06 × 4 × 294,821,320 shares [D, 10Q p.11] = **$70.8m**.
- On the guided 295-297m average diluted shares: $70.8-71.3m.
- Implied normalized NI at a 25% payout = **$283m**. At 20% = $354m.

| NI definition | NI | Payout |
|---|---|---|
| FY25 carve-out GAAP NI (pre-debt, pre-standalone) | 220 [D] | 32% |
| Form 10/A pro forma FY25 NI | 139 [D] | 51% |
| Standalone normalized, FY25 base (this file) | ~171 (161-182) [C] | 39-44% |
| Standalone normalized, FY26 run-rate | ~209 [C/E] | 34% |
| FY27 illustrative | ~234 [E] | 30% |
| NI ex after-tax acquired amortization | ~390 [C] | 18% |

**Verdict.** On every GAAP-consistent construction available from disclosed data, $0.06 a quarter is **30-51%** of standalone net income, not 25%. The claimed 25% fits only if one of two things holds:
- "Normalized" adds back roughly **one-half** of the after-tax acquired-intangible amortization. [C] 283 − 171 = 112, against 219 after-tax amortization.
- Or management is pegging to a forward year near **FY28** (*inference*: NI ≈ $280-300m if Adj. EBITDA reaches ~$870m with full standalone costs, SBC ~3% and interest ~$105m).

Management has not printed a normalized-NI reconciliation. Adjusted NI/EPS reporting starts with Q3-26 ([Q2-T 1283.73s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1283.73)). That will be the first chance to see the definition (feed D4).

**Affordability is not the issue.**
- Standalone FCF ≈ FY25 FCF 461 − after-tax interest 78 − after-tax standalone cost 19 = **~$365m** [C]. This is before ~$50m of capitalized plus ~$50m of expensed one-time cash over 2026-27 [IR].
- *Inference:* carve-out CFO already reflects current (cash) taxes. The deferred tax benefit of ~$90m is deducted in the CFO bridge [D-deck ID 108], so the $89m DTL cash drag is not an additional hit to FCF versus FY25.
- Dividend / FCF ≈ **19%**. The 75%+ FCF return target implies ~$200m+ a year of buybacks from 2027 [C].
- The gap is in **how the payout ratio is labelled**, not in cash coverage.

## Disclosures that stop or change (feed D4)
1. The segment measure switched from operating profit to Adj. EBITDA in Q2-26, with prior periods recast. Segment assets and capex were dropped.
2. Q2-25 Adj. EBITDA was recast from 186 (Investor Day) to 188 (10-Q).
3. The standalone cost was re-expressed from "$20-25m" to "~150bp, high end".
4. The dividend policy moved from "20-25% of net income" to "25% of normalized GAAP NI". The 10-Q prints only $0.06 a quarter.
5. A segment cost reallocation into Corporate is pending.
6. Adjusted NI/EPS starts in Q3-26.
7. Guidance scope is now revenue and Adj. EBITDA only; a broader FY27 guide is promised.

## Honest counters
- **The bridge may be too harsh.**
  - Interest income on the cash balance, AI-driven cost savings, and the medium-term 25-27% tax rate could each add $5-15m to NI.
  - At 26% tax and $107m interest, NI is $182m. That is still a 39% payout, so the conclusion survives, but the gap narrows.
- **"Normalized" may legitimately exclude amortization of the IHS/SPGI step-up.** Many data peers treat this as non-economic. On that basis the payout is ~18%, *below* the 20-25% range, and management would be conservative. The test above shows only that the GAAP label is wrong, not that the dividend is aggressive.
- **The 150bp standalone increment may already be offset in FY26** by allocation savings. The FY26 guide still implies ~40% margins. If so, the run-rate FY26 NI (~209) is the better base, and the payout is ~34%.
- **Allocations ≠ standalone cost.** The ~$100m "allocations" figure comes from S&P Global's methodology (revenue/headcount pro-rata). The true standalone corporate cost could be lower than allocations plus $26m if some allocated services are dropped rather than replicated.
- **The wedge table relies on approximate printed stand-up amounts.** Cross-checking on the slide footing breaks (FY23/FY24 Adj. EBITDA 597/659 vs 598/658) shows ±$1m noise in every period.
