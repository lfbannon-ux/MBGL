# D6 — Value Proposition, Competitive Advantage, Barriers to Entry: Mobility Global (MBGL)

Prepared 2026-10-06 by the Part D analyst. It uses the tiers and source keys defined in `D1_moat.md`.

**Tiers:** [D] disclosed · [C] computed · [E] estimate · [IR] management verbal · [X] third party · [context] general knowledge.

**Revenue by customer group (FY25)**

| Basis | Dealers | OEM | OEM & supplier | Financial / consumer / other | Source |
|---|---|---|---|---|---|
| Filing | ~60% | ~10% | — | — | 10A p.299 [D] |
| Investor Day deck | 62% (B2B + CARFAX) | — | 20% | 18% | PRES s.10/93 [IR] |

**[C]** On the deck basis the FY25 split is roughly: dealers ≈ $1,085m, OEM & supplier ≈ $350m, financial/consumer/other ≈ $315m.

**Economic unit:**
- CARFAX: the dealer rooftop subscription. Revenue = enrolled locations × price per location, plus BIG (Banking & Insurance Group) customers × price [10A : 340].
- B2B: the OEM or enterprise contract.

Price per rooftop, location counts over time, ARPU and churn are **not disclosed** [segments_kpi_NOTES]. The unit economics below are therefore qualitative, apart from the products-per-dealer figure.

---

## 1. Value proposition by customer segment

| Segment (≈ share of revenue) | What they care about | What MBGL offers | Evidence | Tier |
|---|---|---|---|---|
| **Dealers** (~60–62%; 40k+ dealer customers) | Turning used inventory faster at better gross; consumer trust at the point of sale; service-lane retention; lead flow; pricing and payment accuracy | **CARFAX Advantage** (VHR; under 40% of CARFAX revenue); **Car Listings**; **CARFAX For Life / Car Care** service loyalty; Premium Listings / Showroom; Sell My Car; **automotiveMastermind** BPS (Behavior Prediction Scores) for sales targeting (3,200 dealers); **Market Scan** payments engine (~10,500 dealers); Polk dealer KPIs | Management-claimed 10–15x ROI, ~9% faster turn, ~5% more gross (2023 internal study) [PRES s.68]. Lifetime program: +19pt service retention, +16pt brand loyalty, 1,600 sign-ups [PRES s.73]. ~2m "Show me the CARFAX" requests a month [X survey]. aM: "90% of key decision makers" see it as needed (Teneo 2021, n=1,257) [X]. Dealers average **1.5–2 products** [[Q2 : Calderone](https://web.quartr.com/companies/22709?companyId=22709&documentId=4111696&documentType=transcript&eventId=704668&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=2647.85)]. | [IR] / [X] / [D] |
| **OEMs and suppliers** (~10% OEM per filing; ~20% OEM & supplier per deck) | Volume, share and loyalty measurement; incentive efficiency; recall reach; production, supply-chain and tariff planning; CPO program integrity | Polk market reporting ("gold standard"); audiences and closed-loop measurement; **Recall** (13bn+ owner records); **Data Studio** clean room + **Enterprise EyeQ** incentives; **Planning Solutions** forecasts (195 analysts, 145+ markets, 85k variants); **FAST**, **PIQ**; CARFAX in **36 OEM CPO programs** | 100% of the top-40 OEMs; 94% of the top-100 suppliers (98% of the top 40) [10A : 380]. Data Studio: +40% close rate, +10% sales, ~10% incentive reduction (case studies) [PRES s.50 / ID]. FAST: 90% workflow automation, "4x" forecast quality [ID : LaFeir]. OEM/supplier subscriptions grew in the hardest years [ID : LaFeir]. | [D] / [IR] |
| **Lenders, insurers and others** (part of the ~18% bucket; CARFAX BIG; VIN Solutions; DMVs, tolling agencies, parts retailers) | Collateral valuation and underwriting risk; claims and fraud; VIN decoding at scale; regulatory-grade data handling (DPPA, GLBA) | **CARFAX BIG** (history-based valuations: 250m VH-based valuations), **VIN Solutions** real-time APIs, registration-based data under the DPPA | 17 of the top-20 banks and insurers use the data [10A : 380]. "~50% loan default risk reduction" (management study) [PRES s.68]. Subscription growth includes "solid underwriting volumes", +$13m FY25 / +$17m FY24 [D 10A : 349]. | [D] / [IR] |
| **Consumers** (indirect: dealer-provided reports are free to the consumer; some direct report purchases; 53m Car Care users) | Avoiding a lemon at a ~$28k average used price; service reminders and cost estimates; resale value | The VHR (usually free via the dealer), Car Care app, valuations, Listings with history attached | 96% awareness, 92% VHR CSAT [10A : 263; PRES s.68]. "The typical scenario is the dealer makes it available at no charge" [[ID : Fredericks](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=9483.13)]. 23m monthly US unique visitors [10A : 380]. | [D] / [IR] / [X] |

**Inference: how the four sides connect.**
- The consumer is the *source of pricing power* but mostly not the *payer*.
- The dealer pays because consumers trust the brand.
- The OEM pays for CARFAX indirectly: CPO mandates and co-op dollars from 14 OEMs.
- Lenders pay because the same record de-risks collateral.
- One dataset is monetised four ways. That is the core of the value proposition.

---

## 2. Competitive advantage: where it comes from and how large it is

| Source of advantage | Evidence | Tier | Size / durability judgment |
|---|---|---|---|
| **Data scale and age** (see D1 §2) | 177k sources, 38bn records, ~6m added a day | [D] | Large; widening at ~9%/yr in records [C, D1] |
| **Brand-driven demand** | 96% awareness; $1.5bn media since 2000; ad expense $176m FY25 | [D] / [IR] | Large but costly. Ad spend grew faster than revenue FY23→25 (+31% vs +18%) [C] |
| **Embedded distribution** | 95 dealer integrations; 17 of the top-20 FIs; 36 CPO programs; Market Scan in 10,500 dealers | [D-pres] / [D] | Medium–large. Switching means unpicking workflows: "We're so embedded in these systems that the switching cost is just too high." [ID : Morehouse] |
| **Profitability as proof** | FY25 Adj. EBITDA margin 40.6% [IR GS]. CARFAX segment OP margin 23% → 25% → 28% (FY23→25, after amortization) [D 10A : 355]. | [D] / [IR] | **[C]** A rising CARFAX margin alongside ~10% growth is consistent with pricing power. B2B is not separately evidenced. |
| **Cross-sell headroom** | 1.5–2 products per dealer vs a stated potential of "three or four or five"; <50% of franchise Advantage dealers use Service Loyalty; B2B "<50%" penetrated at the top-40 OEMs [IR] | [IR] | This is the growth engine behind core 5–7%. **Inference:** it is a lever, not a moat. The 2026 bundle failure shows the lever has friction. |

---

## 3. Barriers to entry

### 3.1 Entry-cost stack: what a new vehicle-history entrant would have to assemble

**[E]** throughout. These are order-of-magnitude judgments built from MBGL's own disclosed spend and counts. They are not quotes.

| Layer | What it takes | Anchor evidence | Rough cost / time [E] | Rising? |
|---|---|---|---|---|
| 1. Contribution contracts | Tens of thousands of give-get deals with shops, dealers, police agencies, OEMs and DMVs, some exclusive | 177k sources, growing ~6.5%/yr [C]. "Slow to replicate" [IR]. | Years to reach critical mass. The cost is mostly the value-exchange product that must be built first (MBGL uses Car Care traffic for shops). | **Yes.** Source count up 77% FY16→FY25 [C] |
| 2. Historical archive | Records from as far back as the 1980s (the VHR dates to 1984) | 38bn records; "data that's … 15 years old just doesn't exist anymore anywhere else" [IR] | **Cannot be bought.** Only partially licensable from title and auction sources. | **Yes, by definition** |
| 3. Public / DMV data | Purchase fees plus DPPA compliance infrastructure | DMV cost is "significant relative to potential monetization" [10A : 381–382]. DPPA liquidated damages of $2,500 per individual [10A : 312–314, 383–384]. | Material fixed cost, before any revenue | Likely yes. Data fees are rising: "have increased and may continue to increase" [10A : 302] |
| 4. Brand | Consumer awareness to the point where buyers ask for it at the dealer | $1.5bn of media since 2000. Ad expense $134m → $176m (FY23→25) [D]. | **[E]** ≥$1bn and ≥10 years to approach parity. The incumbent's run-rate spend alone is ~$176m/yr. | **Yes.** CAC is rising as platforms "dial up their monetization" [10A : 343] |
| 5. OEM CPO mandates | Persuading OEMs to accept a second VHR standard | 36 programs mandate CARFAX [IR] | Relationship- and time-bound | Stable |
| 6. Workflow integrations | Integrations into DMS, CRM, listings and lender systems | 95 dealer and 36 CPO integrations [PRES s.66] | Moderate, but DMS gatekeepers can block access [10A : 304] | Mixed |
| 7. Data science / AI | Decoding unstructured service records | 100+ data scientists; 99.5% decoding accuracy [IR] | **Falling.** Off-the-shelf AI lowers this layer for everyone [10A : 297]. | **No, falling** |

**Net judgment [Inference]**
- Layers 1–4 have risen over the last decade.
- Layer 7 has fallen, which helps entrants *process* data but not *obtain* it.
- The binding constraint is access, not processing. So barriers have **risen on balance** for the VHR franchise.
- For B2B planning, barriers are **flat to falling**: GlobalData and Experian already offer "low-cost alternative[s]", and AI lowers forecasting labour costs.

### 3.2 Failed or weak entrants and challengers

| Challenger | What happened | Insight | Tier |
|---|---|---|---|
| Dealer antitrust suit (~469 dealers, 2013) | Challenged CARFAX exclusive arrangements; CARFAX won summary judgment 2016-09-30; appealed; new complaint Jan-2017 | Exclusivity in contribution and distribution survived a coordinated legal attack. The final outcome is not in the sources [gap]. | [D] INFO16 p.80 |
| Experian AutoCheck | Long-standing #2 VHR. Management's framing implies it is the alternative a dealer could "put in front of" a consumer ("brand Z") | Data parity on title and auction records is not enough without consumer pull | [IR] / [context] |
| NMVTIS-based low-cost report providers | Government title data sold cheaply by approved providers | Title-only data is commoditised. The service and accident archive is the moat. | [context] |
| GlobalData / LMC; Experian (registration) | Persist as "low-cost alternative[s]" in planning and B2B | B2B is contestable at the low end. MBGL competes on breadth plus analysts. | [IR] |
| MBGL's own Listings (launched 2014) | After 12 years it is still the "newest of the four" with <10% of a $3bn+ market | The CARFAX brand does **not** carry over automatically into adjacent categories with entrenched incumbents | [IR] / [C] |
| MBGL Europe (Spain, Italy, Poland; Germany Jul-2026) | Consumer-first entry; "strong double-digit" growth but transactional revenue missed in Q2-26 | Shows what it costs MBGL itself to rebuild the network from zero abroad. That is the same barrier an entrant faces in the US. | [IR] |

---

## Table persisted to K_session_tables.md

The entry-cost stack and the segment value table are appended under "D6_value_prop".

## Honest counters

1. **The value proof is mostly the company's own studies.** ROI, turn, gross, default reduction and Data Studio lifts all come from internal or commissioned research. There are no audited unit economics: no ARPU, retention or churn.
2. **Some dealer value is defensive rather than incremental.** Dealers may pay because consumers expect the report, not because it raises gross. **Inference:** that is a strong moat but a weak "value creation" story. If consumer expectations shift (AI-generated summaries; free OEM histories), willingness to pay could fall quickly.
3. **Barriers to *processing* are falling** (AI), and the 10/A admits that IP protection against AI use of its data is uncertain [10A : 298].
4. **Rising ad spend could signal brand fatigue, not brand strength.** Ad spend rose +31% FY23→25 against +18% revenue [C].
5. **B2B's value proposition is not evidenced in growth** (+3%, +6%). Low-cost alternatives exist. Its barriers may be overstated by the "gold standard" language.
6. **The customer mix is inconsistent across documents:** dealer 60% vs 62%, OEM 10% vs OEM & supplier 20%. The segment-level analysis depends on which basis is used.
