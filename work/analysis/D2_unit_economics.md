# D2 — Unit economics (Mobility Global, MBGL)

Prepared 2026-10-06 by the Part D analyst. Inputs: `extraction/segments_kpi.csv`, `statements.csv`, `notes.csv`, `presentations.csv`, `acquisitions.csv`, the three transcript quote banks, `QUALITATIVE.md`, plus re-reads of Form 10/A (Quartr 3603533) pp.340-350 and 10-Q (3699447) pp.27-30.

**Tiers:** [D] disclosed · [C] computed (method stated) · [E] estimate (assumption stated) · [IR] management verbal · [X] third party · [context] general knowledge.

**Citation keys:**
- 10A = Form 10/A, 2026-05-27, Quartr page.
- 10Q = 10-Q Q2-26.
- ID = Investor Day deck 3352878, slide number. ID-T = Investor Day transcript 2026-05-12.
- Q2-T = Q2 call transcript 2026-08-07. GS-T = Goldman Sachs Communacopia 2026-09-10.
- $m unless stated.

**Ground rule:** MBGL discloses **no** price per rooftop, ARPU, churn, NRR, report unit volumes, brand-level P&L or country P&L (segments_kpi_NOTES "NOT disclosed"; presentations_NOTES "Not disclosed"). Every per-unit number below is therefore either a printed operational KPI or a [C] ratio of two printed numbers whose denominators are known to be imperfect. No per-unit P&L is constructed where none exists.

---

## Summary
1. **CARFAX is the profit engine.**
   - Segment Adj. EBITDA margin was 45.5% / 45.8% / 46.9% in FY23-25 and 49% in Q2-26 [C/D].
   - Incremental Adj. EBITDA flow-through was 49% in FY24, 58% in FY25 and 46% in 6M-26 [C].
   - Growth in 2026 is mostly price. The 10-Q attributes ~$36m of the $64m 6M-26 revenue increase to price, against ~$20m to new business [D, 10Q p.27].
2. **B2B is a mid-30s-margin business with weak flow-through.**
   - FY25 revenue rose $34m while segment Adj. EBITDA fell $6m (−18% flow-through) [C].
   - In 2026 flow-through recovered to ~50% (6M-26) [C].
   - On a GAAP operating-profit basis B2B earns a ~10% margin [D], because it carries ~$107m a year of acquired-intangible amortization against ~$608m revenue.
3. **The best dealer-level anchor available is about $17k per year of Advantage + Listings revenue per CARFAX dealer customer (~$1.4k/month) [C].** This is FY25 product mix × segment revenue ÷ ">40,000 dealer customers". It is an average across customers, not rooftops, and the numerator is a deck percentage.
4. **Capital intensity is trivially low.** Capex is 0.9-1.4% of revenue [D]; there is no capitalized-software intangible build [Inference]. The "return" problem is the purchase-price basis: FY25 NOPAT on the ~$11.7bn carve-out invested capital is ~2.2%, or ~3.9% before amortization [C]. These are not company-printed metrics.
5. **International and new products have no disclosed unit P&L.**
   - Canada (CARPROOF, bought for $459m in Dec-2015 [D]) sits inside CARFAX International revenue of $168m in FY25 [D].
   - No Germany set-up cost or break-even has been disclosed.

---

## (a) CARFAX dealer economics

### Printed anchors
| Anchor | Value | Date | Tier / source |
|---|---|---|---|
| CARFAX dealer customers | >40,000 | 12/31/25 | [D] 10A p.263, 340; 10Q p.19 |
| Revenue driver definition | "number of dealer locations enrolled … the average monthly price per location on each product, and the number of BIG customers and their average monthly price per customer" | 10/A 2026-05-27 | [D] 10A p.340 (neither driver is quantified) |
| CARFAX segment revenue FY23 / FY24 / FY25 | 928 / 1,039 / 1,142 | FY | [D] 10A p.355 |
| CARFAX subscription share | 81% (FY23-25); 81% Q2-26 | FY / Q | [D] 10A p.355; 10Q p.28 |
| FY25 CARFAX product mix: Advantage / Financial-Consumer-Other / Listings / International | 38% / 26% / 22% / 15% (sums to 101%) | FY25 | [D-deck] ID 57 (unaudited marketing figure) |
| Products per dealer | "1.5" (ID); "between one and a half and two" (Q2) | 2026-05-12; 2026-08-07 | [IR] |
| Dealer-presented reports | 28m+/month; consumer "show me" ~2m/month | FY25 / YE2024 survey | [D-deck] ID 67; [X] survey |
| Dealer ROI claim | 10-15x (2023 Economic Model of Advantage study) | 2023 | [IR]/[X] ID 68 |
| Lifetime Dealer Program sign-ups | 1,600 since Q4-25 | 2026-05-12 | [IR] ID 73 |
| Lifetime outcomes | +19ppt return-for-service yr-1; +16ppt OEM brand loyalty; 293 Car Care cars serviced/month per avg Lifetime dealer; 14 OEMs allow co-op dollars | 2026-05-12 | [IR] ID 73 |

### Computed per-dealer ratios (FY25)
| Ratio | Value | Method | Caveat |
|---|---|---|---|
| CARFAX segment revenue ÷ dealer customers | **≤$28.6k/yr (~$2.4k/mo)** [C] | 1,142 ÷ 40,000 | Upper bound. The numerator includes BIG (lenders/insurers), consumer pay-per-report and international. ">40,000" makes it a ceiling. |
| Advantage + Listings revenue | **~$685m** [C] | (38% + 22%) × 1,142 | Deck % on audited revenue |
| … per dealer customer | **~$17.1k/yr (~$1.4k/mo)** [C] | 685 ÷ 40,000 | Customers ≠ rooftops (filing driver is "locations"). Also includes some Canada dealers if International is not fully separated in the mix. |
| Advantage alone per dealer customer | **~$10.8k/yr (~$0.9k/mo)** [C] | 0.38 × 1,142 = 434 ÷ 40,000 | Assumes every dealer customer takes Advantage ("You have to have Advantage" [IR] Q2-T) |
| Revenue per product-subscription | **~$8.6-11.4k/yr** [C] | 685 ÷ (40,000 × 1.5-2.0) | Products-per-dealer is a verbal [IR] figure |
| Lifetime penetration | **~4%** of dealer customers [C] | 1,600 ÷ 40,000 | Sign-ups, not paying conversions |

### Price escalators
- **2026: price is the main driver, and now quantified.** "price increases of approximately $16 million and $36 million" (Q2 and 6M) versus "continued new business growth of approximately $8 million and $20 million" [D, 10Q p.27]. For CARFAX: "primarily driven by price increases" [D, 10Q p.28].
  - [C] Price = 36 ÷ 859 = **~4.2pts** of 6M-26 total growth. New business = 20 ÷ 859 = ~2.3pts. FX ≈ 5 ÷ 859 = 0.6pts. The total is 7.4%.
  - This matches the CFO's "the majority of that is in value" for the 5-7% core ([ID-T 10629.67s](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=10629.67)).
- **Timing:** "The preponderance of our pricing actions take effect early in the year" ([Q2-T 1167.77s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1167.77)) [IR]. No contractual escalator percentage is disclosed.
- **The CFO rejects a fixed-escalator reading:** "this is not as simple as saying … every year we're going to increase price by 3%, 4%, 5%" ([ID-T 10222.16s](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=10222.16)) [IR].
- **Disclosure change (feed D4).** The Form 10/A does not use the word "price". It attributes FY25 subscription growth to "new business growth" ($76m), "underwriting volumes" ($13m) and "the remaining increase driven by improved contract terms" [D, 10A p.349-350].
  - [C] The residual is 1,426 − 1,303 − 76 − 13 = **$34m**, about 2.6% of FY24 subscription revenue.
  - The 10-Q now labels price ≈ 4% of revenue in a half-year. Either 2026 pricing stepped up, or the 10/A "new business" bucket contained price. The two disclosures are not comparable.

### Listings vs vehicle-history reports
| | Advantage (VHR) | Listings |
|---|---|---|
| FY25 revenue [C] | ~434 (38%) | ~251 (22%) |
| Market / share | VHR "doesn't even represent 40%" of CARFAX [IR] ID-T | US listings ">$3 billion", "not even at 10%" [IR] GS-T |
| Reconciliation | — | 251 ÷ 3,000 = **8.4%** [C], consistent with the "<10%" claim |
| Usage anchor | ~28m report views/month [D] 10A p.263 → ~$1.29 of Advantage revenue per view [C] (434 ÷ 336m) | ~23m monthly unique visitors [D] → ~$10.9 Listings revenue per MUV per year [C] |
| 2026 developments | Homegrown bundled into the base subscription (no price) [IR] GS-T | Showroom: first premium listing, paid add-on, launched Q2-26; "expect CARFAX Showroom to drive higher revenue per dealer" ([Q2-T 367.81s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=367.81)) [IR] |

**Lifetime bundle failure (the 2026 unit-economics event).**
- The bundle needed "two yeses", from the sales GM and the service manager ([Q2-T 3411.03s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=3411.03)).
- Rep incentives rewarded waiting for both ([GS-T 913.53s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=913.53)).
- Products went back to à-la-carte selling in June 2026 [IR].
- Fewer than half of franchise Advantage dealers take Service Loyalty [IR] Q2-T.
- *Inference:* the cross-sell lever (1.5 → 3-5 products) is real but slower than planned. No conversion or price-uplift data is disclosed.

**Advertising is the main variable cost of the dealer model.**
- Group advertising expense was 134 / 152 / 176 in FY23-25 [D, 10A p.450]. That is 9.0% / 9.4% / 10.1% of revenue [C].
- *Inference:* this is mostly CARFAX (brand and traffic), but the segment split is not disclosed.
- The 10/A flags that customer-acquisition cost "is rising as major advertising platforms … dial up their monetization" [D, 10A p.343].

## (b) Consumer report economics
- **Model:** consumer pay-per-report sits in CARFAX non-subscription revenue [D, 10A p.341]. CARFAX non-subscription was 180 / 196 / 215 in FY23-25 [D]. The line also contains other transactional items, so consumer report revenue alone is **not disclosed**.
- **Volumes and price:** no unit volumes, consumer price or conversion are disclosed. [context] The CARFAX consumer list price is a single-report retail price in the tens of dollars. It is not used in any computation here.
- **Main channel is free-via-dealer:** "the dealer makes it available at no charge online and in their showroom" ([ID-T 9483.13s](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=9483.13)) [IR].
  - *Inference:* consumer reports are mainly a demand-creation device for the dealer subscription, not a P&L line.
- **Financial / Consumer / Other** was 26% of CARFAX in FY25, about **$297m** [C]. It mixes BIG (lenders and insurers; driver = BIG customers × monthly price [D]), consumer and Car Care.
  - BIG "underwriting volumes" added $13m (FY25) and $17m (FY24) of subscription revenue [D, 10A p.349-350].
  - In FY24, "strong performance from insurance products" added $17m [D, 10A p.356].
  - 17 of the top 20 banks and insurers are customers [D].
- **No consumer CAC, LTV or payback data exists in any source.**

## (c) B2B contract economics
| Anchor | Value | Date | Tier |
|---|---|---|---|
| OEM coverage | 100% of top-40 global OEMs; 94 of top-100 suppliers; 100% of top-10 investment banks | 12/31/25 | [D] 10A p.265, 341 |
| OEM users | ~6,000 | 2026-05-12 | [IR] ID-T |
| Customer concentration | No customer ≥10% of revenue (FY23-25) or of A/R | FY25 | [D] 10A p.448 |
| Customer-type mix | ~60% dealerships, ~10% OEMs (10/A "as of" 12/31/25); deck: Dealer 62%, OEM & Supplier 20%, Financial/Consumer/Other 18% | FY25 | [D] 10A p.299; [D-deck] ID 10 |
| B2B revenue FY23 / FY24 / FY25 | 557 / 574 / 608; subscription 76% → 80% → 82% | FY | [D] 10A p.356 |
| Business lines | Marketing & Sales 74% (~$450m [C]); Strategy & Planning 26% (~$158m [C]) | FY25 | [D-deck] ID 34 |
| automotiveMastermind | 3,200 dealers [IR] ID-T; 56k+ users, 14x ROI, 650k attributed sales [D-deck] ID 48; "growing at double digits" [IR] | 2025 / 2026-05-12 | — |
| aMM pricing / revenue | **Not disclosed** | — | — |
| Market Scan | ~10,500 dealerships (priced by rooftop) | 12/31/25 | [D] 10A p.264, 341 |
| US dealers using B2B | 11K | FY25 | [D-deck] ID 42 |
| Contract terms | No obligation beyond initial term; generally invoiced annually in advance; RPO $78m (12/31/25) → $102m (6/30/26) | — | [D] 10A p.299, 447; 10Q p.10 |

**Computed ratios (all upper bounds or illustrative) [C]**
- **OEM revenue ≈ 10% × 1,750 = ~$175m.** Divided by 40 top OEMs, that is **≤~$4.4m per OEM per year**. This is a ceiling: the 10% includes non-top-40 OEMs and is a rounded filing percentage.
- **OEM & Supplier ≈ 20% × 1,750 = ~$350m** [C, deck %]. Divided by (40 OEMs + 94 suppliers), that is ~$2.6m per named enterprise customer. The denominator understates the customer count.
- **B2B dealer revenue** (aMM, Market Scan, Polk dealer products) is ≲ $400m [C]. Method: dealer share 62% × 1,750 = 1,085, less CARFAX Advantage + Listings ~685, less some CARFAX International dealer revenue. Divided by ~11K US B2B dealers, that is ≤~$36k per dealer per year.
  - *Inference:* this is a very loose bound. It cannot be decomposed into aMM vs Market Scan.
- **RPO is small relative to revenue.** RPO / FY25 subscription revenue = 78 ÷ 1,426 = 5.5% [C]. *Inference:* contracts are mostly ≤12 months, or RPO excludes cancellable terms. Either way, multi-year lock-in is not evidenced in the accounting.
- **NRR:** management pulled NRR from the deck and called it "meaningfully north of 100%" ([ID-T 10177.24s](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=10177.24)) [IR]. **No number exists.** This is a disclosure that stopped before it started (feed D4).
- **B2B underlying subscription growth:** ~6% in 1H-26, with a goal of "high single digits" ([Q2-T 2695.93s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=2695.93)) [IR]. Printed: 6M-26 B2B subscription +8%; Q2 +6% [D, 10Q p.29].

## (d) Incremental margin / flow-through by segment [C]
Method: Δsegment profit ÷ Δsegment revenue, year over year, using `segments_kpi.csv`. The **OP basis** is Form 10/A segment operating profit (after acquired-intangible amortization and special items). The **Adj. EBITDA basis** is 10/A "Segment Adjusted EBITDA" for FY / Q1 and 10-Q Adj. EBITDA for Q2 / 6M. The two Adj. EBITDA definitions tie for Q1-26 (10-Q 6M − Q2 = 10/A Q1 for every segment). The bases are kept separate.

| Period (vs PY) | Segment | ΔRev | ΔOP | OP flow-through | ΔAdj. EBITDA | Adj. EBITDA flow-through | Adj. EBITDA margin PY → CY |
|---|---|---|---|---|---|---|---|
| FY24 | CARFAX | 111 | 49 | 44% | 54 | 49% | 45.5% → 45.8% |
| FY25 | CARFAX | 103 | 63 | 61% | 60 | 58% | 45.8% → 46.9% |
| Q1-26 | CARFAX | 23 | 12 | 52% | 10 | 43% | 47.3% → 47.0% |
| Q2-26 | CARFAX | 23 | 12 | 52% | 11 | 48% | 49.1% → 49.0% |
| 6M-26 | CARFAX | 46 | 24 | 52% | 21 | 46% | 48.2% → 48.0% |
| FY24 | B2B | 17 | 8 | 47% | 12 | 71% | 34.3% → 35.4% |
| FY25 | B2B | 34 | −7 | −21% | −6 | **−18%** | 35.4% → 32.4% |
| Q1-26 | B2B | 12 | −9 | n/m (transaction costs 13) | 5 | 42% | 30.3% → 31.2% |
| Q2-26 | B2B | 6 | −13 | n/m (transaction costs 20) | 4 | 67% | 32.7% → 34.0% |
| 6M-26 | B2B | 18 | −22 | n/m | 9 | 50% | 31.5% → 32.6% |
| FY24 | Total | 128 | 59 | 46% | 60 | 47% | 40.3% → 40.8% |
| FY25 | Total | 137 | 41 | 30% | 53 | 39% | 40.8% → 40.6% |
| 6M-26 | Total | 64 | −17 | n/m | 29 | 45% | 41.6% → 41.8% |

Sources: 10A p.355-356, 359-360; 10Q p.14, 24-25. Segment Adj. EBITDA margins are [C] from printed $ (printed % agree within rounding).

**Reading**
- **CARFAX:** incremental Adj. EBITDA margins of ~45-58% sit at or just above the segment average, so margin is roughly flat to slightly up. *Inference:* price-led growth (≈100% incremental margin) is being reinvested in advertising and "strategic investments" (10Q p.27-28 cites higher advertising and promotion as the offset).
- **B2B FY25 is the anomaly.**
  - Operating-related expenses rose 11% (232 → 258) and S&G 9% (162 → 177) on 6% revenue growth [D, 10A p.350].
  - FY25 B2B S&G also absorbed $13m of severance, $9m of transaction costs, a $5m ELT benefit and a $3m legal recovery [D]. These are excluded from Segment Adj. EBITDA, so the −18% is an underlying cost step, not a special item.
  - The 2025 refined cost-allocation methodology was applied to all periods (10A p.349), so the drop is not an allocation discontinuity *within* the 10/A.
  - It may become one *going forward*: "We're going to see a slight reallocation of costs between CARFAX and B2B" ([GS-T 1694.2s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1694.2)). The segment baseline will be reset in the next 1-2 quarters (feed D4).
- **The OP basis is dominated by fixed amortization.** CARFAX ~189-190 and B2B ~106-107 a year [D] are flat, so OP flow-through is mechanically higher than the operating reality on growth years.

## (e) Capex & capitalized software intensity
| | FY23 | FY24 | FY25 | 6M-25 | 6M-26 |
|---|---|---|---|---|---|
| Capex [D] | 18 | 15 | 24 | 8 | 12 |
| Capex / revenue [C] | 1.2% | 0.9% | 1.4% | 0.9% | 1.3% |
| CARFAX capex / B2B capex [D] | 9 / 9 | 10 / 5 | 15 / 9 | n/d | n/d (segment capex dropped in 10-Q) |
| Depreciation (excl. acquired amortization) [D] | 12 | 13 | 14 | 7 | 7 |
| Capex / depreciation [C] | 1.5x | 1.2x | 1.7x | 1.1x | 1.7x |
| FCF [D] / FCF conversion (FCF / Adj. EBITDA) | 375 / 63% | 412 / 63% | 461 / 65% | 225 / 63% [C] | 177 / 46% [C] |

Sources: 10A p.361, 463; 10Q p.7; 8-K p.10; ID 108/111.

- **Capitalized software is not separately disclosed.** Capex "include[s] purchases of property and equipment and additions to technology projects" [D, 10A/10Q non-GAAP definitions].
  - Acquired "Databases and software" intangibles have an unchanged cost of $1,077m for FY23-25 [D, 10A p.454], and gross PP&E is only ~$100m [D, 10A p.424].
  - *Inference:* MBGL does not build a material capitalized-software asset. Development cost runs through the P&L (S&G "includes … research and development" [D, 10A p.345]; the R&D amount is not extracted). Reported FCF is therefore not flattered by capitalization, unlike many data peers.
- **Maintenance vs growth capex: not stated.**
- **One-time stand-up spending will roughly double near-term capex.** About $100m of one-time spin costs, "roughly 50% of these one-time costs will be capitalized" ([Q2-T 1344.91s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1344.91)) [IR]. [C] That is ~$50m of capitalized stand-up spend over 2026-27, against $24m of FY25 capex.
- **6M-26 FCF conversion fell to 46% [C]** (FCF 177 ÷ Adj. EBITDA 386), from 63% in 6M-25. Working capital and $57m of transaction costs (mostly cash) drove the decline [D, 10Q p.30].

## (f) International expansion unit
| Anchor | Value | Tier / source |
|---|---|---|
| CARPROOF (Canada) acquisition | 2015-12-24, $459.2m net of cash; goodwill 330.0, intangibles 168.3 | [D] IHS FY2016 10-K p.60-61 (acquisitions.csv) |
| Canada Carfax Loan (intra-group funding) | CAD 403m, 6.0%, 2018; $230m at 12/31/25; contributed and eliminated 2026-06-25 | [D] 10A p.363; 10Q p.17 |
| CARFAX International revenue FY23 / FY24 / FY25 | 137 / 155 / 168 (+13% / +9%) | [D] 10A p.355 |
| CARFAX International revenue Q2-26 / 6M-26 | 47 (+9%) / 92 (+12%) | [D] 10Q p.28 |
| CARFAX International mix | 15% of CARFAX; "Canada is the largest established international business" | [D] 10A p.355; [IR] GS-T |
| Group foreign pre-tax income FY23 / FY24 / FY25 | 40 / 59 / 50 | [D] 10A p.455 (includes B2B international) |
| UK valuation allowance charge | $5m in FY25 ETR | [D] 10A p.456 |
| VIO: US / Canada / EMEA | ~292m / ~28m / ~506m | [D-deck] ID 75 |
| Germany | Launched early July 2026 vs a plan of "the beginning of 2027" by reusing the CARFAX US platform; plus Italy, Spain, Poland; France targeted | [IR] Q2-T, [GS-T 119.5s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=119.5) |
| Europe performance | "strong double-digit growth, but our transactional revenue in the quarter lagged expectations" | [IR] [Q2-T 1069.83s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1069.83) |
| International contribution to MT growth | 1-2pts of the 7.5-10% | [IR] GS-T 457.2s |

**Computed / inferred**
- **Mature case (Canada).**
  - CARFAX International revenue of $168m (FY25) is **0.37x** the 2015 CARPROOF price ($459m) [C]. The numerator includes Europe and ten years of organic growth.
  - CARFAX International revenue per Canadian VIO is ≤$6.0 (168 ÷ 28m), against US CARFAX revenue per US VIO of $3.3 (974 ÷ 292m) [C].
  - *Inference:* this hints that Canada monetizes at or above US intensity per vehicle (a "market leader in Canada" [IR]). However, the numerator contains Europe, so the true Canada figure is lower. **No Canada revenue, margin, payback or IRR is disclosed.**
- **Germany / Europe launch:** **no set-up cost, operating loss, headcount or break-even timing is disclosed in any source read.**
  - The only cost signals are indirect: the $5m UK valuation allowance (*inference:* some European or UK entity is loss-making; entity and segment not identified) and the EUR 10m Europe Carfax Loan (repaid 2025-11-30) [D].
  - An international contribution of 1-2pts of growth equals **~$18-38m a year** of incremental revenue on the FY26 guide midpoint [C]. No margin is attached.

## (g) New-product economics (AI, Car Care, Showroom)
| Product | Printed anchors | Economics disclosed? |
|---|---|---|
| Car Care / CARFAX for Life / Service Loyalty | 53m+ consumers [D]; goal 150m US+CA (ID) → ">100 million" US (GS) [IR]; 293 serviced cars per month per Lifetime dealer [IR] | No revenue, no price. Monetized via dealer service-marketing subscriptions inside "Financial/Consumer/Other" or Advantage bundles [Inference] |
| Showroom (premium listing) | Launched Q2-26, paid add-on [IR] | No price, no uptake |
| Homegrown, AMM SMS offers | Included in base subscription "to support future price capture" [IR] GS-T 627.8s | Zero direct revenue by design |
| FAST / PIQ / Data Studio | "all four of them are in their early stages" [IR]; Data Studio 40% close-rate lift, 10% incentive reduction (case studies) [D-deck] ID 50 | No revenue |
| AI productivity | 100+ data scientists; 84% of customer queries deflected; 10-15% engineering lift in 2025, 4-5x in Q1-26 [IR] ID-T | Savings "we've been reinvesting most of that" ([GS-T 1809.58s](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1809.58)) [IR]. No $ quantified |
| New products in growth algorithm | 1-2pts of MT growth = ~$18-38m a year [C] | — |

**Inference:** AI is currently a cost-avoidance and reinvestment story, not a revenue line. In the P&L, its only visible footprint is "strategic investments" (op-related expenses +$11m in 6M-26 [D, 10Q p.27]).

## Reconciliation to company-printed return metrics
| Printed metric | Printed | Recomputed [C] | Ties? |
|---|---|---|---|
| FCF conversion (FCF / Adj. EBITDA), FY23 / 24 / 25 | 63% / 63% / 65% (ID 108/111) | 375 / 598 = 62.7%; 412 / 658 = 62.6%; 461 / 711 = 64.8% | Yes |
| FCF margin | 25.3% / 25.5% / 26.3% (ID 97) | 25.3% / 25.5% / 26.3% | Yes |
| Capex % revenue | 1.2% / 0.9% / 1.4% (ID 97) | same | Yes |
| Dealer ROI 10-15x; aMM ROI 14x | Customer-side ROI from studies / surveys [X] | Not recomputable | n/a, customer economics, not MBGL returns |
| ROIC / ROE | **Not printed** | NOPAT FY25 = (OP 339 + one-time 40) × (1 − 32.5%) = 256 on invested capital ≈ equity 11,485 + Canada loan 230 − cash 38 = 11,677 → **2.2%**. Pre-amortization (EBITA) → **3.9%** | n/a |

*Inference:* the investment case cannot be framed as a high-ROIC compounder on the reported balance sheet.
- Goodwill (8,845) plus net acquired intangibles (3,789) exceed invested capital, because the IHS Markit / SPGI purchase-price step-ups are pushed down.
- On an incremental basis, returns are very high: capex runs at ~1% of revenue while Adj. EBITDA grows ~$50-60m a year.
- The ~4% headline return sits below the ~5.5% weighted coupon on the new notes (D3).

## Disclosures that stop or change (feed D4)
1. Price is quantified for the first time in the 10-Q (p.27). The 10/A used "new business growth" / "improved contract terms".
2. Segment capex and assets are disclosed in the 10/A but dropped in the 10-Q.
3. NRR was pulled from the Investor Day deck [IR].
4. A segment cost reallocation into corporate is flagged for the next 1-2 quarters [IR GS-T].
5. The Car Care goal was reframed from 150m US+CA to ">100m" US.
6. The B2B line split (Marketing & Sales 74% / Strategy & Planning 26%) appears only in the deck, not the filings.

## Honest counters
- **The per-dealer ratios could be materially wrong.**
  - "Dealer customers" is a ">40,000" floor, not rooftops (the filing's driver is "locations").
  - The product-mix % is a deck figure that sums to 101%.
  - If rooftops are ~1.3-1.5x customers, per-rooftop revenue would be ~$11-13k, not $17k.
- **The "price-led" reading may overstate pricing power.** The 10-Q price figure is company-level and approximate, the 10/A never used "price", and some "price" may be mix (product upgrades, Homegrown/Showroom repackaging) rather than like-for-like escalators.
- **B2B's FY25 negative flow-through may be a one-year investment** (FAST/PIQ/Data Studio build, merit) rather than structural. 2026 Adj. EBITDA flow-through is back to ~50%, and margin expanded in Q2-26 (32.7% → 34.0%).
- **The low ROIC is an accounting artefact.** It reflects pushed-down purchase prices paid by IHS/SPGI, not capital MBGL deployed. An investor buying at market value faces a different hurdle.
- **The absence of any capitalized-software asset may mean capex is under-captured** (e.g., cloud spend in opex) rather than proof of low intensity. Cloud is a "significant amount" [D, 10A p.305] and is expensed.
