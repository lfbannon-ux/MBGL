# D1 — Moat: Mobility Global (MBGL)

Prepared 2026-10-06 by the Part D analyst. Follows `analysis/D_SPEC.md`.

**Tiers:** [D] disclosed · [C] computed (method stated) · [E] estimate (assumption stated) · [IR] management verbal · [X] third party · [context] general knowledge, not from the filings.

**Source keys**
- **10A** = Form 10/A (Quartr 3603533). Page numbers are Quartr pages.
- **10Q** = 10-Q Q2-26 (3699447).
- **INFOyy** = IHS Markit 10-K for FY20yy. **SPGIyy** = S&P Global 10-K for FY20yy.
- **ID / Q2 / GS** = Investor Day 2026-05-12 (event 676565), Q2-26 call 2026-08-07 (704668), Goldman Sachs Communacopia 2026-09-10 (725748).
- **PRES s.N** = Investor Day deck slide N (doc 3352878; `extraction/presentations.csv`). This is a management marketing figure, not audited.
- **PRED** = `extraction/predecessor.csv` and its NOTES file.

---

## 1. The moat in one sentence

**MBGL owns the only VIN-level vehicle record that a dealer can hand to a consumer. That record is built over decades through give-get contributions from about 177,000 sources and backed by a brand consumers ask for by name, and its cost to replicate keeps rising as the archive ages.**

The dealer pays for the consumer's trust. The contributors keep sending data because they get value back. Every year of history that a newcomer did not collect is lost to that newcomer for good.

Polk registration and ownership data is a second, related moat on the B2B side: DMV-sourced, governed by the DPPA, and the "gold standard" for OEM market reporting. It is the same pattern of a regulated, slow-to-assemble archive. But it has a credible low-cost substitute (Experian), and its growth is lower (§4).

---

## 2. Architecture of the moat: each element with its strongest evidence

| # | Element | Strongest evidence | Tier | How it locks in |
|---|---|---|---|---|
| 1 | **Data contribution network**: dealers, 92k+ service shops, 6,300 police agencies, 36 OEMs, DMVs and governments | 177,000+ sources and 38bn+ VH records at 12/31/25. "Long-standing 'give-get' relationships … often on an exclusive basis, forming a highly difficult-to-replicate ecosystem" [10A : 381]. About 6m records are added per day [10A : 270]. | [D] | Contributors get value back (for example, Car Care traffic for shops). Each source is a separate contract. "Every one of those 177,000 sources are contractual relationships that are slow to replicate." [[ID : Morehouse : 2026-05-12](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=6770.59)] |
| 1a | — growth of the network over time | Sources grew from 100k+ (FY16) to 112k+ (FY18/19), 130k+ (FY21) and 177k+ (FY25). Records grew from 17bn (FY16) to 20bn, 23bn, 27bn and 38bn. | [D] INFO16 p.10; INFO18 p.10; INFO19 p.10; INFO21 p.14; 10A p.263 | **[C]** Record CAGR FY16→FY25 = (38/17)^(1/9) − 1 ≈ **9.3%/yr**. Source CAGR ≈ **6.5%/yr**. The gap between MBGL and any entrant widens every year. |
| 1b | — the archive cannot be rebuilt | "Some of that data that's seven years old, 12 years old, 15 years old just doesn't exist anymore anywhere else." [[Q2 : Eager : 2026-08-07](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=3497.87)] | [IR] | Time cannot be bought. **Inference:** this is the single hardest element to copy. |
| 1c | — DMV and public data | State DMV data "presents a high barrier to entry for new competitors due to the significant cost relative to potential monetization" [10A : 381–382]. DPPA custodianship "in place for over three decades" [10A : 343]. DMVs are also *customers* of VIN Solutions [10A : 265]. | [D] | Cost plus compliance plus reciprocity. Public data is not the same as cheap data. |
| 2 | **Two-sided brand, consumer pull plus dealer monetization** | 96% in-market awareness and 85% mascot recognition [10A : 263]. About 2m "Show me the CARFAX" requests a month (third-party survey, YE24) and 28m+ dealer-shown reports a month [PRES s.67]. $1.5bn media spend since 2000 [PRES s.18]. Advertising expense was $134m / $152m / $176m in FY23 / 24 / 25 [10A : 450]. | [D] / [X] / [IR] | The consumer asks for the brand by name, so a dealer cannot swap in a rival: "You want to put in brand Z in front of them, the dealer loses confidence with the consumer." [[ID : Fredericks : 2026-05-12](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=9459.13)] |
| 2a | — dealer economics | Management claims 10–15x dealer ROI, ~9% faster turn and ~5% more gross (2023 internal "Economic Model of Advantage" study) [PRES s.68]. 40k+ dealer customers [10A : 262]. | [IR] / [X] | The fee is small relative to vehicle price: "The cost of the CARFAX report as a percent of that continues to decline." [[ID : Fredericks](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=9410.41)] |
| 3 | **OEM relationships** | 36 OEM CPO programs "will not certify a car without a CARFAX report" [[ID : Fredericks](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=5883.23)]. 100% of the top-40 OEMs and 94% of the top-100 suppliers are customers [10A : 380]. 14 OEMs allow co-op dollars for the Lifetime program [PRES s.73]. 36 OEMs contribute data [10A : 263]. | [D] / [IR] | OEMs write the standard into CPO rules, contribute data, and subsidise dealer spend. A three-way lock-in. |
| 4 | **Polk registration and ownership data** (B2B) | More than 30 years of ownership data and 13bn+ owner and transaction records [10A : 265, 268]. Core market-reporting datasets are described as "widely regarded as the 'gold standard'" [10A : 381]. Polk serves ">90% of the volume in the U.S. market" [[ID : LaFeir](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=10099.3)]. US ownership records grew from 5bn (FY16) to 7bn+ (FY17–19) and ~12bn (FY21) [INFO]. | [D] / [IR] | Market share, loyalty and defection KPIs become the shared currency between OEMs and dealers (for example, dealer sales-effectiveness scoring). **Inference:** this is a standard-setting lock-in. It is weaker than CARFAX's because there is no consumer side. |
| 5 | **Workflow embedding** | 95 dealer-tool integrations; 17 of the top 20 FIs integrated [PRES s.66]. Market Scan is in ~10,500 dealers [10A : 264, 381]. "Application agnostic for decades" [[GS : Eager](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=798.69)]. | [D-pres] / [IR] | Distribution runs through other companies' software, so the data is not exposed to any single platform losing share. |
| 6 | **Exclusivity, tested in court** | A 2013 dealer antitrust suit against CARFAX's exclusive arrangements (about 469 dealer plaintiffs) ended in summary judgment for CARFAX on 2016-09-30. It was appealed, and a new complaint followed in Jan-2017 [INFO16 : 80]. No material proceedings are pending in 2026 [10A : 385]. | [D] | **Inference:** exclusive contribution deals have survived legal challenge once. The later outcome is not in the sources read [gap]. |

**What the moat is NOT:**
- **Not exclusivity across the board.** Management called data rights "a mix" [[ID : Eager](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=9695.18)].
- **Not software.** "We're not a software company, right?" [[ID : Calderone](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=10177.24)].
- **Not proven by retention data.** Net revenue retention was "pulled" from the deck and described only as "meaningfully north of 100%" [IR]. No churn, ARPU or price-per-rooftop figure is disclosed [segments_kpi_NOTES].

---

## 3. Defensibility against each competitor class

The named competitors in the filing are J.D. Power, Cox Automotive, Experian and GlobalData [10A : 382]. Management says no one competes across the full lifecycle [[ID : Eager](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=9295.78)].

| Competitor class | Where it overlaps | MBGL defence | Assessment | Evidence tier |
|---|---|---|---|---|
| **Experian (AutoCheck VHR; AutoCount registration data)** | Vehicle history reports (CARFAX); registration-based market share (Polk) | Brand pull ("Show me the CARFAX"), OEM CPO mandates (36), and service-shop records. **[context]:** AutoCheck's strength is title, auction and credit-bureau-adjacent data rather than service records. | **High for CARFAX; medium for Polk.** AutoCheck has existed for decades without displacing CARFAX at the consumer [context]. In registration data, Experian is the "low-cost alternative" management describes for planning and B2B [[ID : LaFeir](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=9337.39)]. Analysts at ID named "Experian AutoCheck" [ID summary]. | [D] / [IR] / [context] |
| **Cox Automotive (vAuto, KBB, Autotrader, Manheim, Dealertrack)** | Listings (Autotrader vs CARFAX Listings); valuation (KBB vs CARFAX valuations); dealer workflow | Cox is also an integration partner for distribution: the 95 integrations include large dealer-workflow tools [PRES s.66; logos not machine-read]. CARFAX valuations are VH-based (250m) [PRES s.17]. | **Medium.** In listings, MBGL is the challenger, not the incumbent: "Of the four players in that space, we're the newest of the four." [[Q2 : Eager](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=2534.08)] US listings are >$3bn with CARFAX at <10% [GS]. **Inference:** Cox is the one firm with both dealer workflow and consumer brands (KBB). It is the most capable potential VHR entrant if contribution data were obtainable. | [D] / [IR] / [context] |
| **CarGurus / Cars.com (listings marketplaces)** | Listings (CARFAX Listings is ~22% of CARFAX revenue ≈ **$251m [C]**, 22% × $1,142m, PRES s.57) | Listings depend on VHR traffic (23m monthly unique visitors; #1 US auto site by Semrush visits [X]). **[context]:** marketplaces commonly display free history-report links, which reinforces the CARFAX brand. | **Medium/low threat to the VHR moat; high competition in listings.** The marketplaces are distributors of the CARFAX report as well as rivals for listing budgets. | [D-pres] / [X] / [context] |
| **CDK / Reynolds (DMS)** | They hold the service and sales records that feed CARFAX and automotiveMastermind (aM integrates "CRM and DMS data", 10A p.264) | Many-source redundancy: 92k shops, many of them on non-DMS shop systems. | **Watch, not a direct competitor.** The 10/A warns that "Some of our suppliers are also our competitors, and from time to time they negotiate to change the terms" [10A : 304]. **[context]:** DMS vendors have historically restricted third-party data access (the 2015–2020 Authenticom litigation), and CDK had a major outage in 2024. **Inference:** DMS gatekeeping is the most plausible supply-side squeeze. | [D] / [context] |
| **J.D. Power (valuation, PIN transaction data, forecasting)** | Strategy & Planning; dealer and OEM analytics; valuation | 195-person forecasting analyst team; 30+ years as the "market-leading forecast" [10A : 265; PRES s.18]. Covers 100% of the top-40 OEMs. | **Medium.** No share data. B2B growth (+3% FY24, +6% FY25 [C]) is much slower than CARFAX's. **Inference:** this side of the business is the less defended one. | [D] / [C] |
| **GlobalData / LMC (forecasting)** | Planning Solutions | Breadth of data plus analysts; FAST self-serve | **Medium.** Management's own word for GlobalData/LMC is "low-cost alternative". Planning projects slipped in Q2-26 on macro [Q2]. | [IR] |
| **Free, government and OEM data** (NMVTIS title checks; NICB VINCheck; OEM connected-car and service data) | Basic title, salvage and theft checks; OEM-owned service histories | Free sources cover title brands and theft, not the archive of service, accident and ownership events. "The data we have isn't scraped, it's not publicly available, and it's not synthetic." [[ID : Morehouse](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=6809.36)] | **High for now.** The 10/A carries a specific risk factor on "free or relatively inexpensive information sources", amplified by AI [10A : 296–297]. **[context]:** NMVTIS reports cost a few dollars through approved providers. **Inference:** OEM connected-vehicle data is the long-dated threat. OEMs could, in principle, publish their own service histories, but 36 OEMs currently *mandate* CARFAX in CPO. | [D] / [IR] / [context] |
| **AI entrants and LLM answer engines** | Consumer research traffic (search/answer engines); cheap data processing | The data sits "behind a firewall or a paywall" [[GS : Eager](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=251.06)]. MBGL uses AI internally (99.5% decoding accuracy; 3.8bn decoded events) [IR; PRES s.83]. | **High on data, weak on traffic.** The 10/A names search and AI as threats to traffic [10A : 299] and says customer-acquisition costs are rising as ad platforms "dial up their monetization" [10A : 343]. The IP risk factor admits: "We do not yet know whether intellectual property laws … will enable us to effectively protect our data … from unintended use by AI" [10A : 298]. **Inference:** AI threatens the consumer-traffic leg of the moat, not the data leg. | [D] / [IR] |

---

## 4. Defensibility against the cycle

### 4.1 Revenue growth vs industry growth, 2015–2025

**Method [C]**
- Source is PRES s.91 (chart labels). The deck's own footnote flags the series as "NOT prepared on a consistent basis": 2014–21 is IHS Transportation adjusted to automotive, 2022 is the SPGI segment, and 2023–25 is the carve-out.
- The extraction NOTES did not assert a year mapping. I assign years as follows:
  - Revenue labels sorted ascending map to 2014 → 2025.
  - Organic and industry labels are taken in print order as 2015 → 2025.
- Validation of the mapping:
  - (a) Reported revenue growth matches the organic labels in every non-acquisition year, within ±1pt (2015, 2019, 2020, 2021, 2024, 2025). The gaps fall in CARPROOF (2016) and aM (2017–18) years, as expected.
  - (b) The industry series matches US light-vehicle SAAR history [context]: −15% in 2020, −8% in 2022, +13% in 2023.
  - (c) The automotive-only organic rates are 1–2pt above the printed IHS Transportation organic rates (9/10/10/11/8/−2/16), which is consistent with automotive being the faster-growing part [PRED].
- **"Industry" = FRED seasonally-adjusted annual figures, which is new light-vehicle sales (inference). It is not used-vehicle transactions.**

| Year | Revenue $m (s.91) | Reported growth [C] | Mobility organic (s.91) | Industry (FRED, s.91) | Gap (pt) [C] | US used-vehicle sales [context] |
|---|---|---|---|---|---|---|
| 2015 | 585 | 10.6% | 10% | 6% | +4 | rising |
| 2016 | 719 | 22.9% (CARPROOF) | 11% | 0% | +11 | ~flat/up |
| 2017 | 836 | 16.3% (aM) | 14% | (2%) | +16 | ~flat |
| 2018 | 979 | 17.1% (aM) | 11% | 1% | +10 | ~flat |
| 2019 | 1,074 | 9.7% | 10% | (1%) | +11 | ~40m units |
| 2020 | 1,052 | (2.0%) | (2%) | (15%) | **+13** | down a low-to-mid single digit |
| 2021 | 1,247 | 18.5% | 18% | 4% | +14 | up |
| 2022 | 1,351 | 8.3% | 10% | (8%) | **+18** | down ~10% |
| 2023 | 1,485 | 9.9% | 9% | 13% | **(4)** | ~flat |
| 2024 | 1,613 | 8.6% | 9% (8.6% s.90) | 2% | +7 | up slightly |
| 2025 | 1,750 | 8.5% | 9% (8.5% s.90) | 2% | +7 | ~flat/up slightly |

**Cumulative result [C]**
- 2015–25 compounded organic growth ≈ ×2.80, or **≈9.8%/yr**.
- Industry units compounded ≈ ×0.99, or **≈0%/yr**.
- Reported revenue CAGR 2014–25 ≈ **11.5%/yr**, including M&A.
- **In ten of eleven years, MBGL grew faster than the industry.** The exception is the 2023 unit rebound.

**Used-vehicle column [context]:** approximate directions only, from general knowledge (Cox Automotive-type estimates of ~36–41m units a year). These are **not** a Part B series. Part B is blocked by the network. Replace this column when Part B lands.

### 4.2 Downturn evidence

| Episode | Evidence | Tier | Read-across |
|---|---|---|---|
| **2008–09** | **No data.** Pre-2016 IHS filings are not on Quartr, and CARFAX/Polk were private before IHS bought Polk in 2013 [PRED "IHS Inc. pre-2016"]. **[context]:** US new light-vehicle sales fell ~35% from 2007 to 2009, and used-vehicle volumes fell much less. | gap / [context] | **Cannot be adjudicated.** Management's "acyclical" claim [[ID : Calderone](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=8064.02)] rests on a series that starts in 2014. |
| **2020 (COVID)** | Transportation organic −2%, but **recurring organic +3%** [D INFO20 : 80]. The decline came from "temporary dealer price relief, paused new sales, cancellations" and lower recall/marketing non-recurring revenue [D INFO20 : 78]. Adj. EBITDA fell only −1% while the margin rose from 41.8% to 44.7% [D INFO20 : 84]. Automotive organic −2% vs industry −15% [PRES s.91]. | [D] / [D-pres] | The subscription base held. The damage was confined to discretionary and transactional lines and to *price relief*. **Inference:** in a severe shock, dealers win price concessions rather than cancelling. |
| **2021 rebound** | Organic +16% (Transportation) and +18% (automotive). "Led by dealer-facing offerings (CARFAX, automotiveMastermind) rebounding" [D INFO21 : 73]. | [D] | Price relief reversed. |
| **2022–23 (chip shortage and rate shock)** | Automotive organic +10% vs industry −8% (2022). B2B OEM/supplier subscriptions "actually grew" in the hardest years [[ID : LaFeir](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=2453.79)]. FY24 non-subscription −2% with recall −$15m [D 10A : 350]. | [D] / [IR] | Recall and transactional revenue are the cyclical part, at ~19% of revenue [D]. |
| **2026 (soft ex-US)** | Q2-26: B2B transactional −4%; CARFAX Canada transactional soft; Planning projects delayed; FY26 guide cut to 6.9–7.7% [Q2]. | [IR] | Even a mild ex-US softening shows up within one quarter in the transactional ~19%. |

**Verdict [Inference]**
- MBGL is **counter-cyclical in relative terms**: it beat industry units by 13–18pt in every downturn year it has data for.
- It is **not immune in absolute terms**: −2% in 2020, plus price relief.
- The claim is credible only for downturns that look like 2020 or 2022. A 2008-type credit collapse, with dealer closures (an explicit risk factor, 10A p.299), is untested in the data.

---

## 5. Market-share arithmetic and adjudication of share claims

**Context:** there is no unit-share series. MBGL does not disclose report volumes, rooftop counts over time, or ARPU [segments_kpi_NOTES]. "Share" below therefore means share of a *TAM in dollars*, using consultant TAMs [X]. Revenue growth above market growth is mostly **price/value**, not unit share: "The majority of that is in value." [[ID : Calderone](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=10629.67)]

| Claim | Source | Arithmetic [C] | Verdict |
|---|---|---|---|
| "13% share of core" ($14bn core TAM) | PRES s.27 [X TAM, unnamed consultant, midpoint] | $1,750m / $14,000m = **12.5%** | Arithmetic **holds**, rounded up. The TAM is unverifiable and its consultant is unnamed. |
| B2B "~10% of $6bn core" | PRES s.46; [ID : LaFeir] | $608m / $6,000m = **10.1%** | **Holds.** |
| CARFAX "15% of $8bn core" | PRES s.71 | $1,142m / $8,000m = **14.3%** | **Rounded up**. Minor overstatement of ~0.7pt. |
| US listings ">$3bn, CARFAX not even at 10%" | [GS : Eager] | Listings ≈ 22% × $1,142m ≈ $251m. The 22% excludes the separate 15% international bucket on s.57, so it is mainly US. $251m / $3,000m ≈ **8.4%** at most. | **Holds.** This is a challenger position, not a moat. |
| "Polk serves >90% of US volume"; "90% of industry volume developed with our data" | [ID : LaFeir]; PRES s.42 | This is customer *coverage*: OEM brands that buy Polk, weighted by sales. It is not a revenue share. | **Mislabelled as share.** It is penetration, consistent with 100% of the top-40 OEMs. |
| "Nobody else can touch it. Our lead continues to expand there." | [[ID : Fredericks](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=9979.98)] | No competitor revenue or unit data is in the record. CARFAX revenue grew +12% (FY24) and +10% (FY25) [D] while US used volumes were roughly flat [context], which implies value capture, not proof of share gain. | **Unverified.** Directionally plausible: sources +6.5%/yr and records +9.3%/yr [C] widen the data lead. Not proven as a share gain. |
| "Market leader in Canada" | [GS : Eager] | CARPROOF was bought for $459m in 2015 [D INFO16 : 60]. No share data. | **Unverified** [IR]. |
| "#1 most visited automotive website (US)" | PRES s.65, Semrush Feb-2026 [X] | ~54m visits | **Third-party estimate.** It is a single-month snapshot. |
| Above-market growth "track record" | PRES s.91 | +10pt average gap per year 2015–25 [C, §4.1] | **Holds against new-vehicle units.** Against used units [context] the gap is similar in size. The deck compares to *new* light-vehicle sales, which flatters the claim in years when used volumes outgrew new (e.g. 2022). |

**Segment split [C]** (from 10A p.349, 355)

| Segment | FY23 revenue | FY24 revenue | FY25 revenue | Growth FY24 / FY25 |
|---|---|---|---|---|
| B2B | $557m | $574m | $608m | **+3.1% / +5.9%** |
| CARFAX | $928m | $1,039m | $1,142m | +12.0% / +9.9% |

**Inference:** B2B's growth gap over the industry is about 1–4pt in 2024–25, much thinner than CARFAX's ~8–10pt. The B2B side of the moat is holding position. It is not compounding.

---

## 6. Watch-items for erosion

| # | Watch-item | Why it matters | Signal to monitor | Current read |
|---|---|---|---|---|
| 1 | **Consumer traffic disintermediated by AI or search answers** | The brand leg (consumer pull) depends on traffic. Customer-acquisition costs are already rising [10A : 343]. | Unique visitors (23m/mo), VHR views (28m+/mo), ad expense / revenue (10.1% FY25 [C] 176/1,750) | Ad spend is up 31% FY23→25 [C] vs revenue +18%. **Amber.** |
| 2 | **Contribution-network churn or fee inflation** | Supplier consolidation has already "resulted in an increase in fees", and some suppliers can cancel on short notice [10A : 304]. | Source count (177k), cost of data in operating-related expense | **Amber.** No cost-of-data line is disclosed. |
| 3 | **DMS gatekeepers (CDK/Reynolds) or OEMs restricting service data** | "Some of our suppliers are also our competitors" [10A : 304] | Contract disputes; OEM connected-car data programs | Not disclosed [gap] |
| 4 | **OEM CPO mandates (36)** | The OEM lock-in leg | Any OEM dropping CARFAX from CPO | Stable (36) [D] |
| 5 | **Pricing power fatigue** | Core 5–7% is mostly price. The bundle GTM failed in 2026 [Q2]. | Products per dealer (1.5–2), Service Loyalty penetration (<50% of franchise Advantage dealers) | **Amber.** The GTM reversal is the first visible friction. |
| 6 | **Dealer consolidation / OEM direct-to-consumer (agency) sales** | Fewer rooftops, and purchasing gets consolidated [10A : 299] | US rooftop count [context]; Advantage enrolled locations (not disclosed) | Gap |
| 7 | **B2B commoditisation (Experian, GlobalData)** | Low-cost alternatives already exist [IR] | B2B subscription growth (~6% 1H26 vs a goal of high single digits) | **Amber.** |
| 8 | **AI and IP leakage** | Third parties "could also use our data with AI tools" [10A : 298] | Licensing terms; S&P's non-exclusive cross-licence of data [10A : 328] | **Inference:** the S&P cross-licence is a new, non-exclusive leak path, though it is described as "not material". |
| 9 | **Disclosure retreat** | NRR "pulled". The segment measure was switched to Adj. EBITDA, and segment assets were dropped [segments_kpi_NOTES]. | Whether NRR, rooftop and ARPU KPIs appear in the FY27 guide | Feed D4 |

---

## Disclosures that stopped or changed (for D4)

- NRR was drafted into the Investor Day deck, then removed [ID : Calderone].
- The data-scale KPI moved from "records/sources" printed annually in the IHS 10-Ks to a "177k" headline with inconsistent sub-counts: police agencies are given as 6K+ on one slide and 6.3K on another [presentations_NOTES].
- Dealer-coverage wording changed from "majority of North American dealerships" to "majority of the top North American dealerships" (SPGI FY25) [PRED].
- Customer-mix shares differ by basis:
  - Filing: dealers 60% / OEM 10% [10A : 299].
  - Deck: dealer 62% / OEM & supplier 20% [PRES s.10].

---

## Honest counters

1. **The cycle evidence is thin and self-selected.** The record holds two mild-to-moderate unit downturns (2020, 2022) inside a decade of rising used-vehicle prices.
   - There is no 2008–09 data.
   - The industry comparison is the company's own choice (new-vehicle units, chart labels, "not prepared on a consistent basis").
   - Relative outperformance is partly a *price* phenomenon. Price can reverse: 2020 shows dealers can extract relief.
2. **Exclusivity is not proven.** Data rights are "a mix" [IR]. Many sources are public or semi-public (DMVs, police). A deep-pocketed rival with dealer workflow access could assemble most of the record over 5–10 years. The most likely candidates are Cox, or Experian combined with a DMS vendor. Only the oldest archive would be truly lost to them.
3. **Most moat KPIs are management marketing figures.** ROI, awareness, "Show me the CARFAX" and CPO counts come from decks and surveys, not audited data. The only audited cross-check is revenue growth and margin.
4. **B2B shows little moat in its numbers.** It grew +3% and +6% while management describes "gold standard" data, and its competitors are low-cost substitutes. On this evidence, roughly a third of revenue sits behind a moderate moat, not a wide one.
5. **The 2026 guidance cut and the bundle failure** suggest that pricing and packaging power over dealers is finite. Dealers said no to buying through two decision-makers.
6. **The AI and search risk to traffic is live, and management cannot quantify it.** Rising ad spend could be the early cost of defending the consumer leg.
