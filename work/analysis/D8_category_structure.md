# D8 — Category Structure: Mobility Global (MBGL)

Prepared 2026-10-06 by the Part D analyst. It uses the tiers and source keys defined in `D1_moat.md`.

**Tiers:** [D] disclosed · [C] computed · [E] estimate · [IR] management verbal · [X] third party · [context] general knowledge.

---

## 1. Why this format wins its niche

**The format:** a neutral, VIN-keyed data utility.
- It **collects** from many fragmented contributors.
- It **brands** the output to consumers.
- It **sells** access to the concentrated professional buyers in between: dealers, OEMs and lenders.
- It **distributes** through other companies' applications rather than owning the transaction.

| Structural feature | Why it wins | Evidence | Tier |
|---|---|---|---|
| **A fragmented supply side** (92k shops, 6,300 police agencies, DMVs, OEMs) | No contributor has enough data alone to be useful, so the aggregator captures the value of combining it. Contributors are paid in kind (give-get) rather than cash. | 177k sources; give-get, "often on an exclusive basis" [10A : 381] | [D] |
| **A fragmented, trust-starved demand side** (consumers buying a ~$28k used car with an information gap) | The VHR resolves an information asymmetry between dealer and buyer. A *third-party, neutral* brand is worth more than the dealer's own claims. | "When the stakes are high, people have questions." [[ID : Fredericks](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=6142.49)]. The 10/A lists "brand trust and independence" as a basis of competition [10A : 382]. | [IR] / [D] |
| **The payer is not the user** | The consumer gets the report free, while the dealer pays a subscription. Price sensitivity is muted because the fee is tiny relative to vehicle gross. | "The cost of the CARFAX report as a percent of that continues to decline." [ID : Fredericks]. 81% subscription [D]. | [IR] / [D] |
| **Neutral, application-agnostic positioning** | MBGL does not own the marketplace, the DMS or the lending decision. Every software vendor can integrate it without competing with it. This maximises distribution (95 integrations). | "Our differentiation comes from the combo of that brand and data, not the application itself." [[GS : Eager](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=798.69)] | [IR] |
| **A cumulative, time-indexed asset** | Value grows with the age and coverage of the archive. Late entrants are permanently behind. | Records 17bn → 38bn (FY16→FY25), ~9.3%/yr [C, D1] | [D] / [C] |
| **Regulated data custody** (DPPA, GLBA) | Compliance infrastructure and a track record with DMVs are a moat for registration data | DPPA "embedded in our culture and operations" [10A : 343] | [D] |
| **Lifecycle breadth with different competitors at each stop** | No single rival matches the whole chain, but each stop is contested | "We see different competitors at each one of those stops around the life cycle." [[GS : Eager](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=707.5)] | [IR] |

**Inference: the niche is narrow but deep.**
- The format wins where *a neutral record plus a trusted brand* matters: vehicle history, registration-based measurement, and recall.
- It does not automatically win where the incumbent owns the consumer *transaction*. In listings, MBGL is the newest of four players with <10% share. It has not won the transaction.

---

## 2. What the company explicitly does NOT do

| Product / activity | Reason (as stated) | Commentary | Source | Tier |
|---|---|---|---|---|
| **Owning the end application / software layer** | "Application agnostic for decades"; "We're not a software company, right?" | Keeps MBGL neutral and maximises integrations. It also gives up software-style pricing and sits behind DMS gatekeepers. | [GS : Eager 798.69s]; [[ID : Calderone](https://web.quartr.com/companies/22709?companyId=22709&documentId=3659313&documentType=transcript&eventId=676565&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=10177.24)] | [IR] |
| **Scraped, public or synthetic data as the core** | "The data we have isn't scraped, it's not publicly available, and it's not synthetic." | This is the moat claim. It is partly qualified by the 10/A's own reliance on public DMV data [10A : 381]. | [ID : Morehouse 6809.36s] | [IR] |
| **Charging most consumers directly for reports** | "The typical scenario is the dealer makes it available at no charge" | The B2B2C model: the consumer is the demand engine, the dealer is the payer | [ID : Fredericks 9483.13s]; [10A : 380] "consumer-pull, dealer-monetization model" | [IR] / [D] |
| **Fixed price escalators** | "Not as simple as saying … every year we're going to increase price by 3%, 4%, 5%." | Price is tied to added value (Homegrown and SMS offers are folded into base subscriptions "to accrue benefit … in subsequent years" [GS : Calderone]). It is less mechanical than a contract escalator. | [ID : Calderone 10222.16s] | [IR] |
| **Bundle-only selling (Lifetime program)** | Abandoned in June 2026. It needed "two yeses", and the rep incentives were wrong. | A failed packaging model: see §3 | [Q2 : Eager 1811.22s, 3411.03s]; [GS : Eager 913.53s] | [IR] |
| **Ad-cluttered listings / monetising at the expense of the consumer experience** | "You will see things on other listing sites that you do not see on ours"; "testing our way into … opportunities to make sure that we do not see a drop in consumer experience" | Protects the trust asset, but caps listings yield in the near term | [GS : Eager 1178.28s] | [IR] |
| **Aftersales business (Catalyst for Aftersales)** | Sold Aug-2023 at a loss of under $1m; −$5m revenue effect in FY24 | Exited a non-core adjacency | [10A : 350, 447, 453] | [D] |
| **Material M&A, near term** | No M&A in the first 6–12 months; tuck-ins only, nothing meaningful near term | Capital goes to dividends and buybacks (≥75% of FCF) | [ID : Calderone 8825.42s]; [Q2 1445.65s]; [GS : Calderone 2012.25s] | [IR] |
| **Buybacks before 2027** | "Give things time to settle"; leverage starts at 2.7x gross | — | [ID : Calderone 8825.42s] | [IR] |
| **Contracts that lock customers in beyond the initial term** | Dealer and OEM contracts carry no obligation beyond the initial term | Renewal risk is structural. RPO was only $78m at FY25 and $102m at 6/30/26 [D], which is small against $1.75bn of revenue. | [10A : 299, 447]; [10Q : 10] | [D] |
| **Publishing NRR / retention KPIs** | NRR was drafted into the deck, then "pulled" | A disclosure choice. Feed D4. | [ID : Calderone 10177.24s] | [IR] |
| **Exclusive data licensing with former parent S&P** | Cross-licences are *non-exclusive*, multiyear and arm's-length, and "not material" | MBGL does not keep exclusivity over data shared with SPGI | [10A : 328]; [10Q : 18] | [D] |
| **Hedging FX historically** | No hedges until a USD/CAD forward on 2026-07-01 | Minor. Shown for completeness. | [10A : 365]; [10Q : 31] | [D] |
| **Robotaxi / AV as a core market** | ~6m robotaxis by 2035 in a ~1.6bn fleet, framed as small | Not a strategic priority. It is framed as a source of data demand. | [ID : Eager 10707.85s] | [IR] |

**Inference:** the consistent pattern is **neutrality and capital-light data custody**.
- MBGL does not own the transaction (vehicle sale, loan, repair) or the application, and it does not take inventory or credit risk.
- Its departures from this pattern have been weaker: Listings, which competes with marketplaces; the bundle push; Aftersales, which was exited.

---

## 3. Inversion: failed or former models and peers, and the insight each carries

| Model / peer | What happened | Insight for MBGL | Tier |
|---|---|---|---|
| **Conglomerate parent (IHS → IHS Markit → S&P Global)** | Mobility sat inside three successive information conglomerates. The CEO says investment went to S&P's "core divisions". CARFAX Germany was pulled forward from 2027 to Jul-2026 once MBGL was independent. | **Inference:** the moat was under-invested, not over-exploited, which supports the standalone thesis. It also means the data is that IHS/S&P held the moat for ~13 years without monetising adjacencies faster. | [[GS : Eager](https://web.quartr.com/companies/22709?companyId=22709&documentId=4152674&documentType=transcript&eventId=725748&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=168.1)] [IR]; [PRED] [D] |
| **IHS Markit "Transportation" (auto + Maritime & Trade + Jane's AD&S)** | A broad "transportation" bundle. AD&S was sold for ~$470m in Dec-2019. Auto grew from ~80% to >90% of the segment. | Scope that is narrow around automotive outgrew broad transportation. Category focus beats breadth across verticals. | [D] PRED |
| **Five siloed businesses → "One Mobility Global"** | CARFAX, Polk, aM, Market Scan and Planning ran with separate HR, finance and systems. Integration is about halfway through, with ~2 years to go. | Cross-sell value (aM 3,200 dealers × CARFAX 40k) was left unrealised. **Inference:** it is upside, but execution risk is live (see the bundle). | [IR] ID / Q2 |
| **The CARFAX "Lifetime" bundle GTM (Q4-25 → Jun-26)** | Sold Advantage + Listings + Service Loyalty as one package. Sales cycles lengthened because two dealer buyers had to agree. Reversed in June, and the FY26 guide was cut to 6.9–7.7%. | Dealer purchasing is departmental. The moat gives pricing power on *one* product. It does not compel adoption of a suite. | [IR] Q2 / GS |
| **Catalyst for Aftersales (sold Aug-2023)** | A small aftersales software business was exited | Aftersales is now re-attacked via Car Care (53m consumers) rather than shop software, which fits the "no application" pattern | [D] 10A |
| **CARFAX Listings (2014→)** | Still a challenger after 12 years; <10% of a $3bn+ market | Brand plus data does not displace a two-sided marketplace's liquidity. Moats are category-specific. | [IR] / [C] |
| **Dealer antitrust challenge (2013–2017)** | ~469 dealers attacked exclusivity; CARFAX won summary judgment | The legal-attack route against a contribution network has failed once. Regulators have not intervened (no material proceedings, 10A p.385). | [D] |
| **Experian AutoCheck (peer)** | A durable #2 with comparable title and auction data | **Inference:** what decides the category is the brand plus service-record breadth, not raw title data | [context] / [IR] |
| **NMVTIS / NICB free or cheap checks (government)** | Exist but have stayed niche | Free data that covers *part* of the question does not substitute for a trusted, complete answer | [context] |
| **Listings and lead-gen peers that struggled** (e.g., TrueCar's lead-fee model; online used-car retailers such as Vroom and Shift that exited or failed, 2023–24) | Models that took transaction or inventory risk, or depended on paid lead flow, proved fragile in the 2022–23 rate shock | MBGL's refusal to own transactions and inventory is the reason it grew +10% organic in 2022 while industry units fell −8% [C, D1 §4] | [context] / [C] |
| **Planning/forecasting low-cost alternatives (GlobalData/LMC)** | Persist at lower price points | The B2B planning niche is contestable. Analyst depth sustains it, not network effects. | [IR] |

---

## Disclosures that stopped or changed (for D4)

- NRR was removed from the Investor Day deck.
- The Lifetime bundle was emphasised at Investor Day (1,600 sign-ups) and then de-emphasised after June 2026.
- The Car Care target changed from 150m (US+Canada) to ">100m" (US).
- The segment profit measure changed from OP to Adj. EBITDA in Q2-26 [segments_kpi_NOTES].

## Honest counters

1. **"Neutral utility" may be a description of constraint, not strategy.** MBGL does not own applications or transactions partly because others (Cox, CDK, the marketplaces) already do. Those owners could squeeze its access, and some of its suppliers are its competitors [10A : 304].
2. **The format's best evidence is old.** The structural advantages were mostly built before 2013 under Polk/CARFAX. Under IHS and S&P, the newer extensions (Listings, Europe, Aftersales, bundles) have a mixed record.
3. **The inversion peers are illustrative, not controlled comparisons.** TrueCar, Vroom and Shift are [context] general knowledge and differ in model. Their failures do not prove MBGL's model is safe.
4. **AI-native answer engines could recreate the "neutral trusted answer" role** at the consumer interface without owning MBGL's data, as long as dealers or OEMs supply alternative data. The 10/A concedes the risk [10A : 297–299]. The structural argument in §1 assumes that the trusted answer must carry the CARFAX brand. That assumption is untested.
