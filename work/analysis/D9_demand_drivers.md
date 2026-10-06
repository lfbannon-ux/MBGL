# D9 — Demand drivers: the macro series MBGL is levered to

Mobility Global (MBGL). Part D analytical layer. Prepared 2026-10-06 from Quartr sources only (SEC blocked).
Tiers: [D] disclosed · [C] computed (method stated) · [E] estimate · [IR] management verbal · [X] third party · [context] general knowledge, to be replaced by Part B series (see `market/PART_B_SERIES_PLAN.md`).

Citation shorthand used below (all links are Quartr deep links):
- **10/A p.N** = Form 10/A, documentId 3603533, `https://web.quartr.com/companies/22709?companyId=22709&documentId=3603533&documentType=report&eventId=695345&navigation=external&utm_medium=referral&utm_source=mcp&rp=N`
- MBGL quote banks: `transcripts/MBGL_2026-05-12_investor-day.md` (ID26), `..._q2-2026-earnings-call.md` (Q2-26), `..._goldman-sachs-communacopia.md` (GS26). Their URLs and timestamps are in those files.
- SPGI calls: a full link is given on each quote.

---

## 0. Bottom line

1. **Management never quantifies a macro sensitivity.** No elasticity to used-vehicle units, SAAR, dealer count, VIO, rates or insurance appears in the 10/A, the 10-Q, the Investor Day, the Q2-26 call, GS26, or 16 SPGI earnings calls (2022–25). What management does say is qualitative: the company is "relatively acyclical", has a "natural hedge" from new to used, and its transactional revenue is "non-cyclical". The only macro-linked items quantified in dollars are recall, underwriting volumes and discretionary budgets (§2). The only quantified *flow-through* to margin is recall (§2.4).
2. **Empirically, the growth rate has decoupled from the industry, except in a real shock.** Management's own chart (ID26 slide 91) shows organic growth of 9–18% in every year 2015–2025 except 2020 (−2%). Over the same years US vehicle sales growth (FRED, per the slide) ran from −15% to +13%.
   - The full-sample correlation is 0.54. Excluding 2020–21 it is −0.39, i.e. none [C].
   - **The one break is a demand-plus-dealer-liquidity shock (COVID).** It hit through dealer price relief and non-recurring recall/marketing revenue (§3).
3. **The real exposures are second-order and sit in the minority lines:**
   - B2B transactional and Planning (OEM discretionary spend, tariffs, recall timing).
   - International transactional (Canada 2026).
   - Dealer count/consolidation (structural, slow).
   - The 81% subscription base [D] is driven by **price and new-store/product adoption**, not volumes. The CFO said core 5–7% is "value plus volume … The majority of that is in value" [IR, ID26].
4. **Inference:** in Part C the right shape for a driver model is (a) price + product attach on a slowly drifting dealer-rooftop base, plus (b) a small transactional "beta" sleeve (~19% of revenue [D]) that carries the cyclicality. A regression of revenue on SAAR or used units is the wrong shape.

---

## 1. Exposure map (what is at risk to which series)

| Exposure | Size | Tier / source |
|---|---|---|
| Dealership customer group | ~60% of revenue | [D] 10/A p.299 |
| OEM customer group | ~10% of revenue | [D] 10/A p.299 |
| "Used car related" | "about 70%" (SPGI framing) | [IR] Cheung, SPGI Q1-25 / Bernstein 2025 (below) |
| Subscription / non-subscription | 81% / 19% (FY25) | [D] SPGI FY25 10-K p.61 (predecessor.csv) |
| International (non-US) | $296m / $1,747m = 17% (FY25) | [D] SPGI FY25 10-K p.61; % [C] |
| CARFAX / B2B | ~65% / ~35% | [IR] ID26 |
| Planning (Strategy & Planning) | ~9% of total | [C] slide 93 mapping, presentations_NOTES |

The "70% used" (SPGI) and "60% dealer + 10% OEM" (10/A) are **different bases**: one is market exposure, the other is customer group. Treat them as non-additive. **Inference:** the remaining ~30% of revenue comes from lenders and insurers (BIG/Financials), consumers, suppliers, financial markets and others.

---

## 2. Driver-by-driver: management's stated relationship, lags, sensitivity, flow-through

### 2.1 Used-vehicle retail transactions
- **Stated relationship [D]:** "when new vehicle sales experience a slowdown due to recession risks or credit tightening, we often observe a corresponding increase in used vehicle transactions. This shift directly supports the demand for our core products, such as CARFAX Vehicle History Reports and our related dealer solutions." (10/A p.382)
- **Volume link denied [IR]:** "Our business model is not directly associated with number of transactions. As long as people are buying used cars, servicing used cars, then we have a business" (Tavernier, SPGI Investor Day 2022, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3779438&documentType=transcript&eventId=44944&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=9931.79)).
- **Resilience claim [IR]:** "Dealer revenue benefits from its higher exposure to the used car market, which is generally more resilient for the cycle than the new car market." (Aboaf, SPGI Q1-25, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3781865&documentType=transcript&eventId=314678&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1572.24))
- **Mechanism:** CARFAX revenue is driven by "the number of dealer locations enrolled in dealer subscription products … the average monthly price per location on each product, and the number of BIG customers and their average monthly price per customer" (10/A p.340) [D]. That definition has no transaction term. Pay-per-report consumer revenue is the only directly unit-linked item, and it is not sized.
- **Lag:** none stated. **Inference:** the effect runs through dealer profitability and renewals (monthly to multi-year subscriptions), so a lag of 2–4 quarters is likely. The exception is Canada, where transactional lines responded within the quarter (Q2-26).
- **Sensitivity / flow-through: none quantified.**

### 2.2 New-vehicle SAAR
- **Stated relationship [D]:** "Seasonality and cyclicality are inherent characteristics of the automotive industry, with global light vehicle sales naturally subject to fluctuations based on macroeconomic conditions, consumer confidence and credit availability." (10/A p.382) This sits alongside the claim of resilience "through various business cycles".
- **Where it bites [D]:** "Marketing & Sales … designed to enhance new vehicle sales" and aM is aimed at the "new car market" (10/A p.341). Planning subscription revenue is "generated from products that provide data and insight on future vehicle sales and production" (10-Q p.23).
- **Counter-cyclical claim [IR]:** "The point of this chart is we are not just counter-cyclical, we're relatively acyclical." (Calderone, ID26)
- **Lag / sensitivity: none quantified.** The investor chart (slide 91) is the only SAAR comparison management has offered. It is used to argue *above-market* growth, not to give a beta.

### 2.3 Dealer count / consolidation
- **Stated relationship [D]:** "When dealers consolidate, the products and solutions they previously purchased separately are often purchased by the combined entity, leading to loss of revenue." Also: "further proliferation of automotive manufacturer direct-to-consumer sales models could result in a decline in the number of U.S. dealers and consolidation in buying power." (10/A p.299)
- **Base [D/IR]:** >40,000 dealer customers (10/A p.340). aM has 3,200 dealers (ID26). Franchise dealers are "highly pinned"; the opportunity is in independents (Eager, Q2-26).
- **Lag / sensitivity: none quantified.** No rooftop count history, churn or NRR is disclosed. NRR was "pulled" from the deck; it is "meaningfully north of 100%" (ID26) [IR].
- **Inference:** consolidation is a slow structural drag on the rooftop count. It is offset by attach: an average of 1.5–2 products per dealer, with the target being "three or four or five" (ID26, Q2-26).

### 2.4 OEM marketing / discretionary spend (incl. recall)
- **Stated relationship [D]:** transactional revenue is "non-cyclical in nature — and that are usually tied to underlying business metrics such as OEM marketing spend or safety recall activity" (10/A p.341; repeated in 10-Q p.23).
- **Quantified items [D]** (10/A p.350, segments_kpi.csv):
  - Lower recall activity: −$15m FY24, −$3m FY25.
  - Lower marketing services: −$2m FY24.
  - "Tightening of discretionary budgets": −$2m FY25.
  - Recall revenue of ~$1m slipped from Q2-26 into H2 pending a court order (Q2-26 slides p.8).
- **Margin flow-through (the only one quantified):** "For Mobility, given our expectations for softer revenue from the recall business, we now expect margins in the division to be slightly lower in the range of 38.5%-39.5%, down 50 basis points from prior guidance." (Peterson, SPGI Q2-24, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2727355&documentType=transcript&eventId=188627&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1759.98)) [IR]
  - Also: "it's actually a very high margin business … when we do see that loss and slowdown in recall, that actually does impact margins fairly significantly." (Craig, SPGI Q2-24, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2727355&documentType=transcript&eventId=188627&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=3434.45)) [IR]
  - **[C]:** a ~$15m recall shortfall against the 50bp guide cut on ~$1.6bn implies roughly $8m of EBITDA impact, i.e. a decremental margin of about 50% or more. This assumes the cut was driven entirely by recall.
- **Recall is not controllable:** "We can create demand in a lot of places. We can't create demand for recall." (Calderone, ID26)
- **OEM incentives as a tailwind [IR]:** "We also expect Mobility to continue to benefit from Dealerships and OEMs, increasing their incentive spend on new vehicles as affordability is hampered by rising rates." (Steenbergen, SPGI Q3-23, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3750202&documentType=transcript&eventId=85482&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1501.85))

### 2.5 Vehicles in operation / average age
- **Disclosed or shown [D]:**
  - 1.5B+ global VIO (Investor Day slide 12; "Mobility Global estimates").
  - US VIO ~292M and Canada ~28M (slide 75; region mapping inferred).
  - US average age is at an "all-time high" of 12 years. The chart labels 10.0/10.7/11.2/12.0/12.5 for 2010–2030 (slide 70; mapping inferred, 2030 projected).
  - [context] SPGI Mobility's own press releases put US average age at about 12.5–12.8 years in 2023–25. That is above the 12.0 label for 2025, so either the basis differs or the label mapping is wrong. Verify in Part B.
- **Stated relationship:** VIO is framed as TAM and whitespace ("1.5 billion vehicles that are on the road", Eager, ID26). Car Care and service retention monetise the parc: "Shops … lose 22%, 23% of the vehicles that they work on" every year (Eager, ID26).
- **Lag / sensitivity: none quantified.** **Inference:** an older, larger parc lengthens the service lifecycle (Car Care, Service Loyalty) and raises the number of used-vehicle resales per vehicle lifetime. This is a slow secular tailwind, not a cyclical driver.

### 2.6 Auto lending (rates, terms, credit availability)
- **Stated relationship [D]:** "the availability and cost of credit are factors affecting consumer confidence, which is a driver of vehicle sales for our consumer customers and dealer customers" (10/A p.295).
- **Datapoint [IR]:** "We're seeing over 20% of car loans at 84 months now. This is a rising trend." (LaFeir, ID26)
- **Financial-institution exposure [D]:** 17 of the top 20 banks and insurers use MBGL data (10/A p.272). "Banking & Insurance Group" pricing uses minimums with usage tiers (10/A p.341). That makes it partly volume-linked.
- **Lag / sensitivity: none quantified.**

### 2.7 Insurance (underwriting volumes / premiums)
- **Quantified [D]:**
  - "Solid underwriting volumes" added +$17m (FY24) and +$13m (FY25) to subscription revenue, and +$2m in Q1-26.
  - FY24 CARFAX: "strong performance from insurance products" +$17m (10/A pp.349, 356).
- **Stated relationship [IR]:** Financials & Other grew 11–18% in 2024–25 on "strong underwriting volumes and market share growth" (Craig, SPGI Q4-24, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2560751&documentType=transcript&eventId=249213&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1495.74)).
  - 2022: "tempered by slowing consumer activity and persistent low volumes across auto sales" (Steenbergen, SPGI Q2-22, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3104752&documentType=transcript&eventId=26055&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1980.94)).
  - 2025: possible tariff pull-forward, "a little bit of that in the financial, to the extent that people were buying new cars ahead of the tariffs" (Cheung, SPGI Q2-25, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2222025&documentType=transcript&eventId=339947&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=2824.15)).
- **Inference:** this is the most volume-sensitive subscription line. Underwriting volumes track policy shopping, which rose with the 2023–24 premium spike [context], and new-vehicle sales. The quantified tailwind has faded: $17m in FY24, $13m in FY25 and $2m in Q1-26 [D].
- **Rising premiums as a risk to affordability:** "rising auto insurance rates" (10/A p.295).

### 2.8 Tariffs / trade (2025–26)
- **Stated relationship [D]:** "rising vehicle prices, potentially due to tariffs, can lead to shifts in demand … and changes in the relative demand for new versus used vehicles" (10/A p.342). Also: "The increased importance of used vehicle history reports in a tariff-affected market also underscores the value of our CARFAX offerings" (10/A p.342).
- **Evidence [IR]:**
  - SPGI Manufacturing revenue: +1% (Q1-25), +3% (Q2-25), −3% (Q3-25), +1% (Q4-25), "as tariffs and related uncertainty weighed on consulting" (Aboaf, SPGI Q3-25, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3802116&documentType=transcript&eventId=369174&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1582.16)).
  - FY26 guide: "only modest growth until we see more concrete signs of acceleration" (Aboaf, SPGI Q4-25, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3758741&documentType=transcript&eventId=393534&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=2199.96)).
  - MBGL Q2-26: "modest delays in Planning Solutions projects due to the uncertain macroeconomic environment" (Calderone, Q2-26).

### 2.9 International auto activity (new in 2026)
- [IR] "softer automotive activity outside the U.S. weighed on transactional revenue this quarter" (Eager, Q2-26). "Canadian auto market's been tough. Our planning business felt the impact." (Calderone, Q2-26)
- **Explicit sensitivity: none.** H2 guidance assumes "We're not assuming any improvement in the macro" (Calderone, Q2-26).

---

## 3. Predecessor-era empirical evidence vs industry episodes

**Basis warnings:**
- Era rules: see `extraction/predecessor_NOTES.md`.
- 2015–21 is IHS Markit Transportation, Nov FYE. The slide-91 series is "adjusted to exclude other businesses". The INFO series is the reported segment, which includes M&T and AD&S.
- 2022–25 is SPGI Mobility, Dec FYE. FY22 covers 10 months. FY23 +30% is not organic.
- The slide footnote says the series is "NOT prepared on a consistent basis".
- **Inference (year mapping):** slide 91's labels were extracted in print order without a year mapping. The 11 industry labels (6/0/(2)/1/(1)/(15)/4/(8)/13/2/2) match [context] US total vehicle sales growth 2015–2025 one-for-one in chronological order (2020 −15%, 2022 −8%, 2023 +13%). The organic labels are therefore read in the same order. Verify against the image.

| FY | MBGL organic (slide 91) [D chart; mapping Inference] | INFO Transportation organic, reported [D] | INFO recurring organic [D] | US vehicle sales growth (FRED via slide 91) [D chart] | Episode [context] | What management said |
|---|---|---|---|---|---|---|
| 2015 | 10% | 9% | 11% | 6% | Cycle peak build | Used-car penetration, recall (INFO narrative) |
| 2016 | 11% | 10% | 10% | 0% | Plateau ~17.5M | "used-car penetration, new-car technology/regulatory/digital-marketing demand, recall" |
| 2017 | 14% | 10% | 10% | (2%) | SAAR roll-over; aM acquired Sep-17 | used-car offerings, strong recall |
| 2018 | 11% | 11% | 11% | 1% | | used-car offerings, new-car innovation |
| 2019 | 10% | 8% | 10% | (1%) | | same |
| 2020 | **(2%)** | (2%) | 3% | **(15%)** | COVID: dealer closures, sales halt Mar–May 2020 | "temporary dealer price relief, paused new sales, cancellations … lower recall and marketing non-recurring revenue" (INFO FY20/21 10-K) |
| 2021 | **18%** | 16% | 18% | 4% | Chip shortage; used prices spike | "dealer-facing offerings (CARFAX, automotiveMastermind) rebounding" |
| 2022 | 10% | n/a (SPGI 10-month) | — | (8%) | Chip shortage, inventory trough, used peak (Manheim Jan-22) then rates rise | see §4 |
| 2023 | 9% | SPGI +30% reported (inorganic) | sub +32% (inorganic) | 13% | Normalisation; UAW strike 15 Sep–30 Oct 2023 | Q3-23 +10%, Q4-23 +9%; **no strike commentary found** |
| 2024 | 9% | SPGI +8% | sub +11%, non-sub (2%) | 2% | Recall slump; CDK ransomware outage Jun-24 | recall (−$15m); "Even with the CDK outage, still, we see strong growth" |
| 2025 | 9% | SPGI +9% (carve-out +8.5%) | sub +10%, non-sub +5% | 2% | Tariffs (Apr-25 onward), pull-forward | Manufacturing ~flat; Dealer +10–11% |
| 2026 H1 | 7.4% reported (Q1 8.1%, Q2 7%) [D/IR] | — | sub +7%, transactional +5% (Q2) | [context] modest | Canada weak; GTM bundle misstep | guide cut to 6.9–7.7% |

**[C] Statistics** (slide-91 series, 2015–25, n=11):
- Mean organic growth 9.9% (sd 4.8) vs industry 0.2% (sd 7.2).
- Correlation 0.54 and OLS beta 0.36 on the full sample.
- Excluding 2020–21: correlation −0.39, beta −0.11.
- Lag-1 correlation −0.32.
- Spread over industry: +4 to +18pt in every year except 2023 (−4pt, when SAAR rebounded +13%).

**Reading:**
1. The positive correlation comes **entirely** from the 2020/2021 V. **Inference:** this is an episode in which dealer liquidity was stressed and the business gave price relief. It is not a gradual volume elasticity.
2. In the 2022 inventory trough (−8% SAAR), growth held at 10%. SPGI explicitly credited the used-car shift: "The used car market completely took off … the Mobility business, kept growing … In fact, benefited tremendously from it." (Peterson, Stifel 2024, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2700773&documentType=transcript&eventId=199854&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1454.88))
3. In the 2023 SAAR rebound (+13%) growth did **not** accelerate (9%). That is consistent with the "acyclical" claim: weak upside capture as well as weak downside.
4. Recurring organic growth stayed positive (+3%) even in 2020. The drawdown sat in non-recurring revenue (recall/marketing) and in temporary dealer price relief.
5. **Inference:** this is the template for a stress case. Hold subscription at low-single-digit growth with price concessions, cut transactional 20–40%, and recover in 12 months.

---

## 4. SPGI-era management commentary on Mobility drivers (2022–2025)

Quarterly Mobility growth by business line, as stated on SPGI calls [IR] (SPGI business lines: Dealer / Manufacturing / Financials & Other):

| Qtr | Total | Dealer | Manufacturing | Fin. & Other | Cited driver |
|---|---|---|---|---|---|
| Q1-22 | 10% | n/a | n/a | n/a | "strength in planning solutions and used car offerings" ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3142482&documentType=transcript&eventId=20622&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1642.54)) |
| Q2-22 | 7% | 10% | 3% | 3% | "relatively flat … OEM spend on marketing"; "persistent low volumes across auto sales" ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3104752&documentType=transcript&eventId=26055&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1980.94)) |
| Q3-22 | n/a | 10% | n/a | 9% | "strong demand for CARFAX as dealerships' profitability remains high. Marketing initiatives … remain muted" ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3288784&documentType=transcript&eventId=27407&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1317.24)) |
| Q4-22 | 9% | 9% | 8% | n/a | Polk Automotive Solutions, "conclusion of several major recall deals" ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3733338&documentType=transcript&eventId=40414&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1573.36)) |
| Q1-23 | 10% (~1pt Market Scan) | 10% | 11% | n/a | "price increases and new store growth"; recall ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3774204&documentType=transcript&eventId=52966&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1373.78)) |
| Q2-23 | 10% | 12% | 5% | 9% | "continued benefit of price increases"; "elevated recall" ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3774723&documentType=transcript&eventId=65410&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1601.21)) |
| Q3-23 | 10% | 13% | 4% | 9% | "price realization"; "favorable pricing environment" in Financials ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3750202&documentType=transcript&eventId=85482&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1443.6)) |
| Q4-23 | 9% | double-digit (4th qtr) | n/a | n/a | — ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2808001&documentType=transcript&eventId=119328&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1622.29)) |
| Q1-24 | n/a | 12% | (3%) | 12% | recall and marketing one-time revenue down ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3779678&documentType=transcript&eventId=165844&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1112.89)) |
| Q2-24 | 8% (9% ex-Aftersales) | 11% | (1%) | n/a | recall; guide cut to 8–9% ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2727355&documentType=transcript&eventId=188627&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1265.14)) |
| Q3-24 | 9% | 10% | 2% | 12% | subscription "low double digits", despite CDK ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2621748&documentType=transcript&eventId=223553&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=3235.36)) |
| Q4-24 | 9% | 10% | 1% | 18% | insurance underwriting volumes, share gains ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2560751&documentType=transcript&eventId=249213&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1495.74)) |
| Q1-25 | n/a | 11% | 1% | 11% | used-car resilience; A&P lifted Car Care to ~46M ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3781865&documentType=transcript&eventId=314678&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1572.24)) |
| Q2-25 | 10% | 11% | 3% | n/a | "sensitivity to tariff-related uncertainty" ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2222025&documentType=transcript&eventId=339947&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1446.48)) |
| Q3-25 | 8% | 10% | (3%) | 12% | tariffs weighed on consulting ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3802116&documentType=transcript&eventId=369174&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1582.16)) |
| Q4-25 | 8% | 10% | 1% | 11% | "tariffs and regulatory uncertainty weighed on demand for consulting and lower recalls" ([link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3758741&documentType=transcript&eventId=393534&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1717.17)) |

n/a = not stated in the retrieved passage (Quartr search snippets). Fill these from the SPGI quarterly supplements once SEC/IR access opens.

**Key SPGI-era quotes [IR]:**
- Chip shortage / low inventory (2022): "The dealers right now are in the middle of a very high demand, a low product environment. CARFAX has been benefiting across the board." (Peterson, SPGI Q2-22, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3104752&documentType=transcript&eventId=26055&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=4337.21))
- Normalisation (2023), two offsetting effects: "Maybe their margins are coming down a bit, inventory levels are going up, therefore, retention is a little bit lower. On the flip side is that there is more demand for sales and marketing products" (Steenbergen, SPGI Q1-23, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3774204&documentType=transcript&eventId=52966&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=3385.31)). **This is the one explicit SPGI admission that dealer profitability drives CARFAX retention.**
- Tariffs (2025): "We would expect … that there could be some budget pressures, for example, in dialogue with our OEM manufacturing clients. However, recall that this is largely on a subscription basis, and there we are reasonably insulated" (Cheung, SPGI Q1-25, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3781865&documentType=transcript&eventId=314678&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=3807.78))
- "With more than 70% of mobility revenue tied to the used car market and more than 80% of revenue coming from subscription products, we remain confident that … the mobility business is largely insulated from direct impact." (Cheung, SPGI Q1-25, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3781865&documentType=transcript&eventId=314678&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1066.5))
- Recall unpredictability: "The recall business is non-recurring and difficult to predict" (Peterson, SPGI Q2-24, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=2727355&documentType=transcript&eventId=188627&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1663.58))
- 2022 merger-close outlook: "on the manufacturing side, high levels of uncertainty relating to the supply chain are driving demand for our forecast offerings" (Steenbergen, SPGI Status Update 2022, [link](https://web.quartr.com/companies/3977?companyId=3977&documentId=3735411&documentType=transcript&eventId=16001&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=1634.72))

**OEM strike 2023:** Quartr full-text searches for "UAW" and "strike" across SPGI 2022–26 transcripts returned no Mobility commentary. Mobility grew +10% in Q3-23 and +9% in Q4-23 [IR]. **No visible impact and none discussed.**

---

## 5. Causes beyond the headline driver

| Cause | Evidence | Tier |
|---|---|---|
| **Price** | "majority of that is in value" (core 5–7%) (ID26). Q2-26 price added ~$16m and new business ~$8m; 6M-26 price ~$36m vs new business ~$20m (10-Q p.27). "The preponderance of our pricing actions take effect early in the year" (Q2-26). SPGI 2023: Dealer growth "driven by price increases" | [D]/[IR] |
| **Price headroom vs vehicle price** | "Cars continue to go up. The cost of the CARFAX report as a percent of that continues to decline." (Fredericks, ID26). Used ATP $28,377, new $53,192 (slide 70) | [IR]/[D] |
| **New business / product attach** | New business added +$80m (FY24) and +$76m (FY25) to subscription (10/A p.349). Products: Listings, CARFAX for Life, Car Care (53M users), Showroom, Homegrown. Avg dealer on 1.5–2 products | [D]/[IR] |
| **Go-to-market execution** | The late-2025 Lifetime bundle lengthened sales cycles and contributed to the 2026 guide cut (Q2-26, GS26). This is not macro | [IR] |
| **International** | 17% of revenue (FY25) [C]. Target +1–2pt of growth (GS26). Germany launched Jul-26. Canada transactional weak in 2026 | [D]/[IR] |
| **AI** | Framed as "an accelerant" (GS26), productivity "four to five times" (ID26). Savings mostly reinvested. Risk: free and cheap information via AI, and search-engine disintermediation (10/A pp.296, 299) | [IR]/[D] |
| **A&P spend** | SPGI Q1-25: increased A&P drove Car Care to ~46M. Q2-26: "spending modestly more on ad and promo" | [IR] |
| **M&A / divestiture** | Market Scan (+~1pt in 2023; +$3m FY24). Catalyst for Aftersales disposed (−$5m FY24) | [D] |
| **FX** | ~$5m benefit in 1H-26 | [IR] |

---

## 6. Disclosures that stop or change (feed D4)

1. **The SPGI business-line split (Dealer / Manufacturing / Financials & Other) is gone** after the spin. MBGL reports CARFAX / B2B plus subscription/transactional. The quarterly series in §4 cannot be continued, and "Manufacturing" (which carried the tariff and recall sensitivity) is no longer separately visible. B2B business-line revenue (M&S vs S&P) is not disclosed (segments_kpi_NOTES).
2. **"~70% used-car related" (SPGI 2025) is replaced by "~60% dealer / ~10% OEM customer group" (10/A).** These are different bases.
3. **INFO "Transportation recurring organic growth" ended in FY2021.** The SPGI era gives reported growth only. Carve-out organic growth starts in 2023–25 (slide 91 footnote).
4. **The "non-cyclical" label on transactional revenue first appears in the 10/A and 10-Q.** It contrasts with INFO FY2020's attribution of the decline to non-recurring revenue.
5. **NRR was in the Investor Day deck and then pulled** (ID26).

---

## Honest counters

- **The "acyclical" evidence is thin and selection-prone.** It is one cycle (2020), one series built by management (slide 91, "NOT prepared on a consistent basis"), annual Nov-FYE data set against calendar FRED, and a year mapping we inferred. n=11 cannot reject a meaningful beta, and the 2020 point alone shows the downside is real.
- **2021–22 may have flattered the base.** Record dealer gross profits during the chip shortage made price increases easy. SPGI said dealer profitability drove demand (Q3-22) and that falling dealer margins lowered retention (Q1-23).
  - [context] US franchised-dealer gross profit per unit has been normalising since 2023.
  - If dealer profitability compresses further (tariffs, rates, OEM direct sales), the price lever that drives "the majority" of core growth is the thing at risk.
  - That is a lagged macro sensitivity management does not quantify.
- **Transactional is not "non-cyclical" in practice.** Revenue tied to recall, OEM marketing, Planning consulting and Canada fell in 2020, 2024, 2025 and 2026. It is ~19% of revenue [D], carries a high decremental margin (§2.4) and accounts for most of the 2026 guide cut.
- **Insurance and lending tailwinds are fading.** The underwriting-volume contribution fell from $17m (FY24) to $13m (FY25) and then $2m (Q1-26) [D].
- **Dealer consolidation is a known negative written into the risk factors, with no counts disclosed.** A slow decline in rooftops would be invisible until it shows up in growth.
- **SPGI quotes are promotional context.** They come from a parent that was deciding whether to divest, and they are verbal [IR] rather than audited.
- **Search coverage.** The SPGI evidence comes from Quartr keyword search snippets, not full reads of all 16 calls. Some quarters' totals are n/a, and commentary in un-retrieved passages, e.g. on the strike, cannot be ruled out.
