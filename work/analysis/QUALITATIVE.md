# QUALITATIVE — Mobility Global Inc. (NYSE: MBGL)

Extraction agent #7. Prepared 2026-10-06.

**Tiers and source keys**
- Every fact is tier **[D]**: printed in a filing and cited by source doc and Quartr page (`p.`). Items marked **[D-flag]** are printed but odd or inconsistent; the flag explains why.
- **10A** = Form 10/A, filed 2026-05-27 (Quartr 3603533). The information statement starts at p.256. Printed page = Quartr page − 261.
- **F10** = Form 10, filed 2026-05-07 (3603535). Its front sections sit 79 Quartr pages after the 10/A.
- **10Q** = 10-Q Q2-2026 (3699447).
- **INFO16/17/18** = IHS Markit 10-Ks: FY2016 (223426), FY2017 (223425), FY2018 (223424).
- **PRED** = `extraction/predecessor_NOTES.md`.
- Deal numbers are in `extraction/acquisitions.csv`, with flags in `extraction/acquisitions_NOTES.md`.

---

## 1. Business description by brand

**Group** [D]
- MBGL describes itself as an automotive data, solutions and insights provider. It reports two segments, CARFAX and B2B. B2B has two business lines: Marketing & Sales and Strategy & Planning (10A p.262, 340).
- **Scale at 12/31/25:**
  - more than 177,000 data sources;
  - more than 40,000 dealer customers;
  - customers include the top 40 global automakers, which cover 96% of global production;
  - more than 38bn vehicle history records;
  - more than 13bn transaction records;
  - about 832m unique VINs;
  - more than 2,000 attributes per vehicle;
  - more than 80m rows of actively updated data (10A p.262, 268).
- **Heritage:** Polk dates to 1870, giving "more than 100 years" of data stewardship and more than 30 years of ownership data (10A p.268).
- **Financials:** FY25 revenue $1.75bn (+8.5%) and net income $220m (+5.8%). Q1-26 revenue $455m (+8.1%) (10A p.262).
- **Market estimates:**
  - Management estimates the global auto market at about $8.0tn, split $3.2tn new light vehicles, $2.8tn used, $1.3tn maintenance and repair, and $0.7tn medium/heavy commercial vehicles (10A p.266).
  - A third party estimates TAM at $75–81bn, split $13–15bn core, $25–27bn extended core and $37–39bn adjacencies (10A p.266).
- **Revenue model:** primarily subscription. Subscription revenue was $1,426m (81%) in FY25, against $324m (19%) non-subscription (10A p.349).

**CARFAX (segment)** [D]
- **Awareness:** 96% in-market awareness, 85% mascot recognition and 50% unaided awareness, per a survey (10A p.263, 268).
- **Data sources:** more than 38bn records from more than 177,000 sources, including more than 92,000 dealers and service shops, 6,300 police agencies and 36 OEMs (36 OEM CPO programs) (10A p.263, 270). About 6m records are added per day (10A p.270).
- **Audience:** more than 53m Car Care consumers; about 23m monthly average unique visitors (U.S.); more than 28m monthly average VHR views (10A p.263).
- **Products:** Advantage (vehicle history reports), Car Listings (launched 2014), CARFAX For Life (launched 2019), and BIG (Banking & Insurance Group, serving lenders and insurers). New products are Premium Listings and Sell My Car. CARFAX uses a B2B2C model (10A p.263, 271).
- **Revenue drivers:** enrolled dealer locations × price per location, plus BIG customers × price (10A p.340).
- **Geography:**
  - The U.S. and Canada are established markets.
  - In Europe, CARFAX has launched in Spain and Italy with a consumer-first strategy; it also names Poland. Germany and France are targeted (10A p.264, 271, 380).
- **Investment:** CARFAX holds about 35% of New General Company (NGC) (10A p.264).
- **Advertising expense:** $176m in FY25, $152m in FY24 and $134m in FY23 (10A p.450).

**automotiveMastermind** (B2B, Marketing & Sales) [D]
- A dealer and OEM sales and marketing platform built on proprietary Behavior Prediction Scores (BPS), integrating CRM and DMS data. It includes Enterprise EyeQ (EEQ), a private-offer incentive tool launched in 2021 (10A p.264, 271).
- Acquired by IHS Markit on 2017-09-25 (78% for about $432–433m; the remaining 22% was treated as compensation) (INFO17 p.62; INFO18 p.64).

**Polk Automotive Solutions / Polk Auto Marketing Solutions** (B2B, Marketing & Sales) [D]
- Provides KPIs (market share, volume, loyalty, defection), audiences and closed-loop measurement, built on billions of transaction records (10A p.264).
- Related offerings:
  - **Recall:** a daily VIN database of more than 13bn owner records (10A p.265).
  - **VIN Solutions:** real-time APIs serving DMVs, parts retailers, insurers and tolling agencies (10A p.265).
- **Naming drift [D-flag]:** the filings use "Polk Auto Marketing Solutions" (p.264), "Polk Auto Solutions" (p.267, 341) and "Polk Automotive Solutions" (p.268).

**Market Scan** (B2B, Marketing & Sales) [D]
- Real-time pricing and payments engine delivered via APIs and dealer software, including Automotive Payments as a Service (APaaS). About 10,500 dealerships used it at 12/31/25 (10A p.264, 381).
- Acquired 2023-02-16 for $223m (10A p.452).

**Data Studio** (B2B, Marketing & Sales) [D]
- A clean-room platform for OEM and dealer first-party data. Early deployments showed 98% participation (10A p.264–265).

**Strategy & Planning** (B2B) [D]
- **Penetration:** serves 100% of the top 40 carmakers, 94% of the top 100 suppliers (98% of the top 40) and 100% of the top 10 investment banks (10A p.265, 268).
- **Vehicle & Supply Chain Forecasting:**
  - 195-person analyst team;
  - more than 145 country markets;
  - more than 85,000 vehicle variants;
  - about 990 production plants;
  - more than 2,900 supplier plant locations;
  - more than 680 technologies;
  - more than 4,400 suppliers (10A p.265).
- **Other products:** Global Reporting (100 countries), FAST (scenario tool) and PIQ (procurement; covers 60% of vehicle value) (10A p.265–266).
- **Investment:** about 25% stake in Digital Automotive (DA, Germany), with a right of first refusal on the remaining 75% (10A p.266).

**Divested** [D]
- Catalyst for Aftersales, described as "our focused automotive aftersales business", was sold in August 2023. The loss was under $1m and it reduced FY24 revenue growth by $5m (10A p.350, 447, 453).

## 2. Customer concentration [D]

- **By customer group:** "As of December 31, 2025," about **60%** of revenue came from dealerships and **10%** from OEMs (10A p.299; identical in F10 p.378).
  - **[D-flag]** The filing states a revenue share "as of" a balance-sheet date.
- **By customer:** no single customer was 10% or more of gross A/R at 12/31/25 or 12/31/24, and none exceeded 10% of revenue in FY25, FY24 or FY23 (10A p.448).
- **Contract terms:** dealer and OEM contracts carry no obligation beyond the initial term (10A p.299).
- **Financial institutions:** 17 of the top 20 banks and insurers use MBGL data (10A p.272).
- **Multi-year billing:** generally invoiced annually in advance (10A p.447).
- **Remaining performance obligations (RPO):** $78m at 12/31/25 (10A p.447) and $102m at 6/30/26 (10Q p.10).

## 3. Geography [D]

| Period | U.S. $m | Intl $m | U.S. % | Intl % | Source |
|---|---|---|---|---|---|
| FY2023 | 1,224 | 261 | 82% | 18% | 10A p.349 |
| FY2024 | 1,329 | 284 | 82% | 18% | 10A p.349 |
| FY2025 | 1,454 | 296 | 83% | 17% | 10A p.349 |
| Q1-2026 | 376 | 79 | 83% | 17% | 10A p.346 |
| Q2-2026 | 389 | 79 | — | — | 10Q p.15 |
| 6M-2026 | 765 | 158 | — | — | 10Q p.15 |

- **B2B mix:** B2B is 79% U.S. and 21% international (Q2-26 and 6M-26) (10Q p.29).
- **Pre-tax income:** domestic $276m vs foreign $50m in FY25 (FY24: 225 vs 59; FY23: 184 vs 40) (10A p.455).
- **Footprint:** regions are North America, EMEA and APAC (10A p.262).
- **FX exposure:** the main exposures are CAD, EUR and GBP, with no hedges historically (10A p.365). A USD/CAD forward was entered on 2026-07-01, running to 9/30/26, against the Canada Carfax Loan (10Q p.31).
- **Subsidiaries:** Exhibit 21 lists 39 subsidiaries across the U.S., Canada, Germany, Spain, Italy, the Netherlands, Poland, Sweden, the UK, Ireland, France, Australia, Malaysia, India, China, Japan and Mexico (10A p.255).

## 4. Data sources and supply dependencies [D]

**Contributors**
- CARFAX draws on dealers, service shops, police agencies, OEM CPO programs and governments. The relationships are reciprocal "give-get" arrangements, often exclusive (10A p.263, 381).
- Commercial third-party data is "often under exclusive rights" (10A p.381).
- **DMVs:**
  - State DMVs are named as data suppliers; access is governed by the DPPA, "in place for over three decades" (10A p.343).
  - DMV public data is described as a high barrier to entry because of its cost (10A p.381–382).
  - DMVs are also VIN Solutions *customers* (10A p.265).
- **Marketing & Sales inputs:** consumer credit, OEM, dealer and lending transactions, inventory, pricing and incentives, and demographics (10A p.296).
- **Strategy & Planning inputs:** reciprocal relationships with OEMs, suppliers and financial institutions (10A p.296).
- **OEMs:** 36 OEMs contribute to CARFAX, and OEM co-op funds support the Lifetime Dealer program (10A p.263, 380).

**Supplier risk (as disclosed)**
- Data supplier consolidation has reduced the number of partners and raised fees. Some suppliers can cancel on short notice, and some are competitors (10A p.304).
- Data access costs "have increased and may continue to increase" (10A p.302).

**Infrastructure**
- A "significant amount" of computing runs on a third-party cloud provider, which is not named (10A p.305).
- The business relies on third-party AI model providers (10A p.297).

**S&P Global data licences after the spin**
- **Planned terms (10/A):** commercial agreements give mutual **non-exclusive** rights to each party's data products, for internal use and derived-data creation. Terms are multiyear and arm's-length, and the company calls them "not material to us" (10A p.328).
- **Status at 10-Q:** the agreements were entered into, per the 10-Q, which names "other commercial arrangements" (10Q p.18).
- **Historical data sharing:** related-party data-sharing revenue was $1m in Q2-26 and $2m in 6M-26 (10Q p.16).

## 5. Competition (as named) [D]

- Competitors are named only in Business (10A p.382):
  - (i) automotive data and analytics: **J.D. Power, Cox Automotive**;
  - (ii) data and information providers: **Experian, Global Data**;
  - (iii) BI and consulting firms (unnamed);
  - (iv) niche players (unnamed).
- The risk factors name no competitors (10A p.301).
- Chinese OEM expansion is flagged as making deeper penetration of "certain OEMs" harder, given MBGL's U.S. base (10A p.343).
- Search engines and AI are cited as competitive risks to traffic (10A p.297, 299).

## 6. Legal proceedings and regulation [D]

- **10/A:** the company is not currently party to any material legal proceedings (10A p.385).
- **10-Q:** pending ordinary-course proceedings are "not expected to have a material adverse effect" (10Q p.16, 32).
- **Legal settlement recovery:** $3m in FY25, in B2B, with no matter named (10A p.350).
- **Tax audits:** U.S. federal audits for 2018–2024 are in process. The company is generally closed for years before 2016 (10A p.458).
- **Regulation cited:**
  - FTC CARS Rule (Dec-2023), TCPA, DPPA ($2,500 per individual liquidated damages) and GLBA;
  - GDPR and UK GDPR, Quebec Law 25, Bill C-27, PRC laws;
  - CCPA and the California CARS Act; Virginia, Colorado, Utah and Connecticut privacy laws; EU DORA; OFAC (10A p.312–314, 383–384).

## 7. Employees [D]

- More than 3,400 FTEs at 12/31/25 (10A p.268).
- About **3,522** FTE (full- and part-time) at 3/31/26: Asia ~616, U.S. and Canada 2,398, Europe 445, Latin America 63, which sums to 3,522 (10A p.384).
- 401(k) expense was $22m in FY25, $20m in FY24 and $18m in FY23 (10A p.458).

## 8. Properties [D]

- Headquarters are leased at 5860 Trinity Parkway, Suite 600, Centreville, VA (10A p.274, 385).
- **[D-flag]** The text reads "We lease office facilities at locations, of which 6 are in the U.S." The total count is missing in the Quartr text (10A p.385).
- **Leases:**
  - Remaining lease terms run 1–12 years (10A p.449).
  - Operating lease commitments are $19m and purchase obligations $90m at 12/31/25 (10A p.365).
  - Pro forma new corporate leases add $54m of right-of-use assets and $9m/yr of incremental rent (10A p.339).
  - Leases not yet commenced total $64m (2026–2037) (10Q p.16).

## 9. Separation mechanics [D]

| Item | Fact | Source |
|---|---|---|
| Announcement | S&P Global announced on 2025-04-29 | 10A p.272; PRED |
| Incorporation | "S&P Global Mobility Holding Company", Delaware, 2025-09-26; renamed Mobility Global Inc. 2026-02-05 | 10A p.274 |
| Record date | 2026-06-15 (close of business) | 10A p.256 |
| Ratio | 1 MBGL share for each SPGI share; 100% distributed pro rata | 10A p.256, 280 |
| Distribution date | 2026-07-01, before NYSE open (F10 said "after NYSE market close"; date, ratio and record date were blank in F10) | 10A p.256; F10 p.335 |
| When-issued | "MBGL WI", 2026-06-26 to 06-30 | 10A p.256 |
| Shares | ~295,077,160 expected (May-15 basis) vs **294,821,320** actual (Jun-15 basis) | 10A p.280; 10Q p.1, 11 |
| Holders of record | ~2,554 | 10A p.320 |
| Retained SPGI stake | **None**: "S&P Global retained no ownership interest" | 10A p.275; 10Q p.18 |
| Tax | Intended to qualify under §368(a)(1)(D) and §355; Davis Polk opinion; 2-year Tax Matters Agreement (TMA) restrictions (buybacks capped below 20% open-market) | 10A p.276, 294, 327 |
| Debt raised | Senior notes issued 2026-05-29: $650m 5.050% 2029, $650m 5.450% 2031, $700m 6.050% 2036; held in escrow, released 2026-06-30; carrying value $1,981m net of $(19)m; about $16.0m issuance costs | 10Q p.11–12 |
| Revolver | $500m, signed 2026-05-06, available 2026-07-01, matures 2031-07-01, +$250m accordion; maximum net leverage 3.50x (4.00x step-up); undrawn at 6/30/26 | 10A p.363–364; 10Q p.12–13 |
| Payment to parent | 10/A: "approximately $1.9 billion" cash payment, plus about $200m retained cash. 10-Q: **$2.0 billion dividend** to S&P Global as consideration **[D-flag: amount differs]** | 10A p.278, 321; 10Q p.12, 18 |
| Pro forma cap table (3/31/26) | Cash $122m → $200m; long-term debt $1,981m; related-party loan of $227m removed; 1bn authorized shares | 10A p.331 |
| Canada Carfax Loan | CAD 403m at 6.0%; $230m at 12/31/25; contributed by SPGI on 2026-06-25 and eliminated | 10A p.363; 10Q p.17 |
| Restructuring Transactions | Completed 2026-06-26 | 10Q p.9 |
| Transition Services Agreement (TSA) | IT, finance and HR, generally up to 18 months; fees at SPGI fully-loaded cost; liability capped at fees paid; pro forma incremental cost <$1m (Q1-26) and $3m (FY25) | 10A p.327–328, 339 |
| Other agreements | Separation and Distribution Agreement (SDA; uncapped cross-indemnities, non-exclusive IP cross-licences), TMA, Employee Matters Agreement (EMA); all filed via 8-K 2026-07-01 | 10A p.326; 10Q p.32 |
| Separation costs | Pre-close costs borne by SPGI, post-close by MBGL. Stand-up transaction costs: $21m in FY25 (9 B2B + 12 Corporate), $21m in Q1-26, $57m in 6M-26 | 10A p.333, 350, 347; 10Q p.17 |
| Dividend policy | $0.06/quarter; first declared Aug-2026, record 2026-08-27, paid 2026-09-10 | 10Q p.18, 30 |
| Equity awards | SPGI awards converted under the 2026 Long Term Incentive Plan (LTIP), filed on S-8 2026-07-01 | 10Q p.18, 33 |

## 10. Risk-factor heading inventory (Form 10 vs 10/A vs 10-Q)

**Structure**
- The 10/A body has **58 headings in 5 sub-sections**, at p.287–317 (printed pp.26–56):
  - Separation: 19
  - Business & Operations: 19
  - Cybersecurity, Technology & Innovation: 8
  - Legal & Regulatory: 4
  - Common Stock: 8
- The Summary Risk Factors list is at p.283–284.

**Form 10 → 10/A**
- **Added headings:** none. **Dropped headings:** none. Headings are identical and in the same order, and every printed page break matches (F10 p.366–396 vs 10A p.287–317). [D]
- **Body edits:**
  1. **Debt risk factor** (F10 p.370 → 10A p.291): "$[blank]" becomes "$2 billion". The 10/A adds a paragraph on indenture covenants and the 3.50x/4.00x net leverage covenant.
  2. **Large-number-of-shares risk factor** (F10 p.394 → 10A p.315): blanks are filled with 295,077,160, May 15, 2026 and "less than 0.05%" director-and-officer ownership.
  3. **Index-fund risk factor** (F10 p.395 → 10A p.316): the blank becomes "approximately 29%".
  4. **Exclusive-forum risk factor** (10A p.317): adds "Moreover, these provisions may increase costs to bring a claim…". "Shareholders" becomes "Stockholders".

**10/A → 10-Q**
- The 10-Q Item 1A prints no headings and states "no material changes" from the Registration Statement (10Q p.32).

**[D-flag] Summary-vs-body inconsistencies within the 10/A**
- The summary heading reads "data network… inaccurate or unreliable data" (p.283); the body reads "data position… cannot maintain our data quality" (p.296).
- The summary reads "enhance our existing products through technology" (p.283); the body omits "through technology" (p.298).

**Selected headings by section** (abridged; full list in the 10A at the pages shown)
- **Separation:** anticipated benefits; no operating history; risks of operating within S&P Global; standalone infrastructure costs; public-company obligations; internal controls; S&P Global board discretion; indemnities; insurance; debt obligations; third-party consents; director/officer conflicts; combined post-spin value; better third-party terms; no dissenters' rights; tax-free qualification; Tax Matters Agreement indemnity; post-spin tax restrictions; accounting systems readiness (p.287–294).
- **Business & Operations:** macroeconomy; renewals/upsell; data position and quality; free information sources; AI; new products; search engines; dealer/OEM dependence; reputation; brand investment; M&A and divestitures; competition; operating costs; global operations; new-market expansion; third-party data sources; outsourcing and cloud; business continuity; talent and management transitions (p.295–306).
- **Cybersecurity, Technology & Innovation:** cyber attacks; processes and technology; AI ethics; open source; IP protection; IP disputes; networks and Internet; infrastructure failure (p.306–311).
- **Legal & Regulatory:** litigation and regulatory proceedings; privacy and data localization; legislative change; OFAC sanctions (p.311–314).
- **Common Stock:** volatility; future sales; S&P 500 index exclusion; anti-takeover provisions; exclusive forum; dilution; subordination; dividends (p.315–317).

## 11. Corporate events timeline [D]

| Date | Event | Source |
|---|---|---|
| 1870 | Polk origins | 10A p.268 |
| 2013 | IHS Inc. acquires R.L. Polk (including CARFAX); deal values are not available in Quartr | PRED |
| 2014 | Car Listings launched | 10A p.271 |
| 2015-12-24 | IHS acquires CARPROOF (Canada), $459.2m net of cash | INFO16 p.60 |
| 2016-07-12 | IHS/Markit merger | INFO16 p.60 |
| 2017-09-25 | automotiveMastermind acquired (78%) | INFO17 p.62 |
| 2018-10-01 | Canada Carfax Loan (CAD 403m) from IHS Canada | 10A p.362–363 |
| 2019 | CARFAX For Life launched | 10A p.271 |
| 2019-12-02 | Aerospace & Defense sold to Montagu (Transportation segment; not Mobility) | PRED |
| 2021-02-21 | Europe Carfax Loan (up to EUR 10m to IHS Group Holdings) | 10A p.363 |
| 2021 | EEQ launched | 10A p.271 |
| 2022-02-28 | S&P Global/IHS Markit merger; Mobility becomes an SPGI segment (exchange ratio 0.2838) | 10A p.445, 459 |
| 2023-02-16 | Market Scan acquired ($223m) | 10A p.452 |
| 2023-08 | Catalyst for Aftersales disposed | 10A p.350 |
| 2025-04-29 | Separation announced | 10A p.272 |
| 2025-07-28 | CEO William W. Eager offer letter | 10A p.4 |
| 2025-09-26 | SpinCo incorporated | 10A p.274 |
| 2025-11-30 | Europe Carfax Loan repaid in full | 10A p.363 |
| 2026-01-05 | OECD guidance on U.S.-parented Pillar Two exclusion | 10A p.349 |
| 2026-02-05 | Renamed Mobility Global Inc. | 10A p.274 |
| Q1-2026 | Exits SPGI cash pooling | 10A p.345; 10Q p.10 |
| 2026-05-06 | $500m revolver signed | 10A p.363 |
| 2026-05-07 | Form 10 filed | F10 p.335 |
| 2026-05-27 | Form 10/A filed | 10A p.1 |
| 2026-05-29 | $2.0bn senior notes issued (into escrow) | 10Q p.11 |
| 2026-06-15 | Record date | 10Q p.2 |
| 2026-06-24 | Annual Incentive Plan adopted | 10Q p.33 |
| 2026-06-25 | Canada Carfax Loan contributed to MBGL | 10Q p.17 |
| 2026-06-26 | Restructuring Transactions completed; when-issued trading begins | 10Q p.9; 10A p.256 |
| 2026-06-30 | Notes escrow released | 10Q p.11 |
| 2026-07-01 | Distribution; NYSE "MBGL" listing; revolver available; Executive Severance Plan effective; S-8 and 8-K filed; USD/CAD forward entered | 10Q p.10, 12, 31–33 |
| 2026-08 | $0.06 dividend declared (record 08-27, paid 09-10) | 10Q p.18 |
| 2026-12-15 | First notes coupon | 10Q p.11 |
| 2027-10-05 | Stated maturity of the Canada Carfax Loan (intercompany since 2026-06-25) | 10A p.363; 10Q p.17 |
