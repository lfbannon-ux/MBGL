# D15 — CARFAX price as a share of dealer gross profit, compared with dealer-pays classifieds (notes)

Prepared 2026-10-26 for the MBGL (Mobility Global) research. This file holds source notes and calculations. It is not a finished analysis.

**Tiers**
- **[D]**: disclosed in a filing, release or deck, with a Quartr link.
- **[IR]**: a management statement on a call or at an investor day.
- **[X]**: expert call, cited as in `X_expert_calls.md`.
- **[C]**: my arithmetic on [D], [IR] or [X] inputs.
- **[E]**: my estimate or assumption.
- **[context]**: web-search snippet only; the primary source was not opened. nada.org was blocked by the proxy (403 / DNS).

**Headline [C]**
- **CARFAX Advantage** (the VHR subscription) costs about **0.7–1.6% of a typical franchised rooftop's used-vehicle front-end gross**. Including F&I it is **≈0.25–0.6%**, or **≈$11–24 per used retail unit**. This uses the $999–$2,000/month expert anchors on AutoNation and Group 1 rooftop economics.
- **The full CARFAX dealer bundle** (Advantage + Listings + For Life, ≤$5,000/month) is **≈3.5–4.9%** of used front-end gross, **≈1.4–1.75%** including F&I, or **≈$56–76 per unit**.
- **The US marketplaces** each cost **≈1.8–2.6%** of the same used front-end gross: CarGurus ≈$2.7k/month, Cars.com ≈$2.5k/month. TrueCar costs ≈1%.
- **Auto Trader UK** says it takes **5–7% of UK retailers' used-car sales gross profit**, or £90–120 per used car sold [IR, 2022].
- **Comparison:** CARFAX's core VHR price is roughly **half of one US marketplace subscription** and **about one-fifth of Auto Trader's take**, measured against the same gross. Only the full bundle reaches classifieds-level take.

---

## A. Dealer economics

### A1. AutoNation (AN), FY2025 and Q2-26 [D]

| Metric | FY2025 | Q2-26 (Q2-25) | Source |
|---|---|---|---|
| Used retail units (total) | 269,558 | 64,521 (69,736) | [Q4-25 8-K p.6](https://web.quartr.com/companies/4007?companyId=4007&documentId=2762057&documentType=report&eventId=395846&navigation=external&utm_medium=referral&utm_source=mcp&rp=6); [Q2-26 8-K p.5](https://web.quartr.com/companies/4007?companyId=4007&documentId=3668693&documentType=report&eventId=659151&navigation=external&utm_medium=referral&utm_source=mcp&rp=5) |
| Used retail units at franchised stores (Domestic 74,625 + Import 91,443 + Premium Luxury 74,597) | **240,665** | — | [Q4-25 8-K p.8](https://web.quartr.com/companies/4007?companyId=4007&documentId=2762057&documentType=report&eventId=395846&navigation=external&utm_medium=referral&utm_source=mcp&rp=8). The remainder (~28.9k) is "Other", mainly AutoNation USA. |
| Used GPU (retail, front-end) | **$1,555** | $1,582 ($1,622) | Q4-25 8-K p.6; Q2-26 8-K p.5 |
| F&I per vehicle retailed (new + used blended) | **$2,769** | $2,799 ($2,712) | same |
| New GPU | $2,564 | $2,381 ($2,785) | same |
| Total variable ops GP per vehicle retailed | $4,819 | $4,777 | same |
| Retail used vehicle GP | $419.2m | $102.1m | Q4-25 8-K p.6 |
| F&I GP | $1,464.4m | $357.6m | same |
| Total gross profit | $4,948.5m | $1,231.1m | [Q4-25 8-K p.2](https://web.quartr.com/companies/4007?companyId=4007&documentId=2762057&documentType=report&eventId=395846&navigation=external&utm_medium=referral&utm_source=mcp&rp=2) |
| Used retail GPU as % of revenue | 5.8% | 5.5% | Q4-25 8-K p.7; Q2-26 8-K p.6 |
| Stores (franchises) | **245 stores** (323 franchises) at 31-Dec-25 | 246 (327) at 30-Jun-26 | [10-K p.3](https://web.quartr.com/companies/4007?companyId=4007&documentId=2814377&documentType=report&eventId=395846&navigation=external&utm_medium=referral&utm_source=mcp&rp=3); [Q2-26 10-Q p.8](https://web.quartr.com/companies/4007?companyId=4007&documentId=3668694&documentType=report&eventId=659151&navigation=external&utm_medium=referral&utm_source=mcp&rp=8) |

Derived values [C]:
- **Used retail units per store:** 240,665 ÷ 245 = **982 a year, or ≈82 a month**. The year-end store count is used, so this is slightly low.
- **Used front-end gross per store:** 82 × $1,555 = **≈$127k a month**.
- **Used variable gross per unit including F&I:** $1,555 + $2,769 = **$4,324**. This assumes used units earn the blended F&I PVR [E]; AN does not split F&I between new and used.
- **Used variable gross per store including F&I:** ≈**$354k a month**.
- **Total GP per store:** $4,948.5m ÷ 245 ÷ 12 = **≈$1.68m a month**. This is an upper bound because AN USA and corporate are in the numerator.

### A2. Group 1 Automotive (GPI), US segment, FY2025 [D]

| Metric | FY2025 | Source |
|---|---|---|
| US used retail units | 155,510 | [Q4-25 8-K p.13 (US operating data)](https://web.quartr.com/companies/11694?companyId=11694&documentId=2688048&documentType=report&eventId=398337&navigation=external&utm_medium=referral&utm_source=mcp&rp=13) |
| US used retail GPU | **$1,582** (2024: $1,629) | same |
| US F&I PRU | **$2,466** | same |
| US new GPU | $3,423 | same |
| US used retail gross margin | 5.2% | same |
| US total GP | $2,809.9m | same |
| US dealerships | **145** (plus 109 in the UK) at 31-Dec-25 | [10-K p.5](https://web.quartr.com/companies/11694?companyId=11694&documentId=2821968&documentType=report&eventId=398337&navigation=external&utm_medium=referral&utm_source=mcp&rp=5) |
| Consolidated used GPU, FY25 (US + UK) | $1,478 | [8-K p.2](https://web.quartr.com/companies/11694?companyId=11694&documentId=2688048&documentType=report&eventId=398337&navigation=external&utm_medium=referral&utm_source=mcp&rp=2) |

Derived values [C]:
- **Used retail units per US store:** 155,510 ÷ 145 = **1,072 a year, or ≈89 a month**.
- **Used front-end gross:** ≈**$141k a month**.
- **Used gross including F&I:** $4,048 per unit, ≈**$362k a month**.
- **US total GP per store:** ≈**$1.61m a month**.

Lithia was not pulled. The two groups give a consistent range for large-group rooftops.

### A3. NADA industry context [context]
- **Dealer count:** 16,972 franchised light-vehicle dealers at mid-2025 and 16,990 at full-year 2025 (NADA Data, via search snippets; [nada.org/media/4694](https://www.nada.org/media/4694)).
- **H1-25 volume:** franchised dealers sold **6.74m used vehicles**. Average used selling price was **$28,602**.
  - Per dealership that is ≈397 in the half, or **≈66 a month** [C].
  - The snippet does not say whether this count is retail only, so wholesale may be included.
- **Average new sold per dealership:** 477 in H1-25 ([Digital Dealer summary](https://digitaldealer.com/news/dealerships-still-thriving-even-amid-a-turbulent-year-nada/168193/)).
- **Not obtained:** NADA used gross per unit, used gross as % of sales, and average total dealership gross. This is a **gap**.
- **Secondary benchmark:** Haig Report puts the public-group average used gross per retailed vehicle at $1,668 (Q2-25) and $1,528 (Q3-25) ([Haig Partners](https://haigpartners.com/resources/used-vehicle-profits-steady-in-q2-2025-what-it-means-for-dealers-planning-their-next-move/)) [context]. That is consistent with AN and GPI.
- **NADA-derived rooftop [E]:** 66 used units a month × AN GPU $1,555 = **≈$103k a month front-end**. Using AN's $4,324 including F&I, it is **≈$286k a month**. A typical NADA rooftop is smaller than a public-group store, so this is the more conservative denominator.

---

## B. Dealer-pays classifieds: per-dealer spend

### B1. CarGurus [D]
| Metric | Q4-25 | Q2-26 (latest) | Source |
|---|---|---|---|
| US paying dealers | 26,049 (+5% y/y) | 26,151 (+3%) | [Q4-25 8-K p.2](https://web.quartr.com/companies/6015?companyId=6015&documentId=2874071&documentType=report&eventId=401325&navigation=external&utm_medium=referral&utm_source=mcp&rp=2); [Q2-26 8-K p.2](https://web.quartr.com/companies/6015?companyId=6015&documentId=3671663&documentType=report&eventId=662781&navigation=external&utm_medium=referral&utm_source=mcp&rp=2) |
| Total paying dealers | 34,409 | 34,629 | same |
| US QARSD (quarterly) | **$7,938** (+8%; Q4-24 $7,337) | **$8,134** (+8%; Q2-25 $7,533) | same; [Q2-26 10-Q p.29](https://web.quartr.com/companies/6015?companyId=6015&documentId=3671664&documentType=report&eventId=662781&navigation=external&utm_medium=referral&utm_source=mcp&rp=29) |
| International QARSD | $2,413 | $2,568 | same |
| Consolidated QARSD | $6,616 | $6,771 | same |
| **US monthly equivalent** [C] (QARSD ÷ 3) | **≈$2,646** | **≈$2,711** | |

- QARSD is a quarterly metric with no annual equivalent. Q4-25 is used as the FY25 exit rate.
- CarGurus' paying dealers include independents, so the franchised-dealer average is likely higher than this [E].

### B2. Cars.com (Cars Commerce) [D]
| Metric | FY2025 | Q4-25 | Q2-26 (latest) | Source |
|---|---|---|---|---|
| ARPD (monthly) | **$2,460** (2024: $2,483, −1%) | $2,472 (flat y/y) | **$2,500** (+3% y/y; Q2-25 $2,435) | [10-K p.32](https://web.quartr.com/companies/11183?companyId=11183&documentId=2939316&documentType=report&eventId=412428&navigation=external&utm_medium=referral&utm_source=mcp&rp=32); [Q2-26 8-K p.1](https://web.quartr.com/companies/11183?companyId=11183&documentId=3672509&documentType=report&eventId=662363&navigation=external&utm_medium=referral&utm_source=mcp&rp=1) |
| Dealer customers | 19,544 (31-Dec-25, +2%) | — | 19,343 | same |

- **Definition caveat** ([Q2-26 8-K p.2](https://web.quartr.com/companies/11183?companyId=11183&documentId=3672509&documentType=report&eventId=662363&navigation=external&utm_medium=referral&utm_source=mcp&rp=2)): ARPD is Dealer revenue, excluding digital advertising services and DealerClub, divided by average dealer customers.
- Dealer revenue includes Dealer Inspire websites, AccuTrade trade and appraisal, and media. **ARPD is therefore more than marketplace listings**, and the listings-only figure is lower.
- The 10-K ([p.33](https://web.quartr.com/companies/11183?companyId=11183&documentId=2939316&documentType=report&eventId=412428&navigation=external&utm_medium=referral&utm_source=mcp&rp=33)) attributes the FY25 −1% to "customer and product mix".

### B3. TrueCar (taken private; last public data Q3-25) [D]
- **Dealers at 30-Sep-25:** 8,225 franchise and 2,794 independent, 11,019 in total ([Q3-25 8-K p.1–2](https://web.quartr.com/companies/11929?companyId=11929&documentId=2238745&documentType=report&eventId=371949&navigation=external&utm_medium=referral&utm_source=mcp&rp=1)).
- **Q3-25 dealer revenue:** $40.393m ([10-Q p.22](https://web.quartr.com/companies/11929?companyId=11929&documentId=2246092&documentType=report&eventId=371949&navigation=external&utm_medium=referral&utm_source=mcp&rp=22)).
- **Monetization:** $491 of total revenue per unit sold through TrueCar ([10-Q p.33](https://web.quartr.com/companies/11929?companyId=11929&documentId=2246092&documentType=report&eventId=371949&navigation=external&utm_medium=referral&utm_source=mcp&rp=33)). This is per TrueCar-attributed sale, not per dealer unit.
- **Monthly dealer revenue per dealer [C]:** $40.393m ÷ 3 ÷ 11,019 = **≈$1,222**. The period-end dealer count is used.

### B4. Auto Trader Group (UK) [D] / [IR]
| Metric | FY26 (yr to Mar-26) | FY25 | FY24 | Source |
|---|---|---|---|---|
| ARPR (£ per retailer forecourt per month) | **£2,995** (+5%, +£141) | £2,854 (+5%) | £2,721 (+12%) | [FY26 AR p.7](https://web.quartr.com/companies/3633?companyId=3633&documentId=3516127&documentType=report&eventId=411876&navigation=external&utm_medium=referral&utm_source=mcp&rp=7); [FY26 results slides p.8](https://web.quartr.com/companies/3633?companyId=3633&documentId=3354376&documentType=slide&eventId=411876&navigation=external&utm_medium=referral&utm_source=mcp&sp=8) |
| Average retailer forecourts | **13,942** (−0.5%; H2 −1.7%) | 14,013 | 13,783 | same |
| Retailer revenue | £501.1m | £480.0m | £450.0m | [FY26 AR p.23](https://web.quartr.com/companies/3633?companyId=3633&documentId=3516127&documentType=report&eventId=411876&navigation=external&utm_medium=referral&utm_source=mcp&rp=23) |
| H1-26 ARPR (Apr–Sep 25) | £2,994 (+5%) | | | [H1-26 slides p.6](https://web.quartr.com/companies/3633?companyId=3633&documentId=2241094&documentType=slide&eventId=358084&navigation=external&utm_medium=referral&utm_source=mcp&sp=6) |

No FY27 interim (H1 to Sep-26) was available at the time of writing; it is due in Nov-26.

**Auto Trader's own price-to-gross statements:**
- **Take of retailer gross profit** (Investor Day 2022 slide 26; [slide](https://web.quartr.com/companies/3633?companyId=3633&documentId=80811&documentType=slide&eventId=33455&navigation=external&utm_medium=referral&utm_source=mcp&sp=26)) [IR]:
  - The headline is "We take 3.5-4.5% of retailer gross profit in sales".
  - **Used sales: 5–7%**. Used sales plus aftersales: 3–4%. Total across new, used and aftersales: 2.5–3%. FY18–FY22 range, excluding FY21.
  - The sales director says the same on the call: "Over that period, the amount of revenue that we benefit from in used cars has been between 5% and 7%" ([transcript 40:50](https://web.quartr.com/companies/3633?companyId=3633&documentId=3135931&documentType=transcript&eventId=33455&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=2450.54)).
- **Revenue per car sold:** **£90–£120 per used car sold** (estimate), at a 70% margin, which is about £75 of profit per car ([Investor Day slide 89](https://web.quartr.com/companies/3633?companyId=3633&documentId=80811&documentType=slide&eventId=33455&navigation=external&utm_medium=referral&utm_source=mcp&sp=89)) [IR].
- **CEO, H1-24 call:** "a 10 times return on investment and a GBP 120 or so pound cost per sale" ([transcript](https://web.quartr.com/companies/3633?companyId=3633&documentId=3660610&documentType=transcript&eventId=121306&navigation=external&utm_medium=referral&utm_source=mcp&targetTime=3932.29)) [IR].
- **UK used-car retailer economics** ([FY25 AR p.9](https://web.quartr.com/companies/3633?companyId=3633&documentId=1961346&documentType=report&eventId=253783&navigation=external&utm_medium=referral&utm_source=mcp&rp=9)) [D]:
  - Gross percentage margins have stayed "between nine and eleven percent" for 10 years.
  - The average advertised used car price is "over £17,000".
  - The company has grown revenue "without meaningfully increasing our take-rate".
- **Derived UK figures [C]:**
  - Used gross per car is about £1,530–1,870.
  - £90–120 ÷ £1,530–1,870 = **≈4.8–7.8%**, consistent with the stated 5–7%.
  - ARPR £2,995 ÷ £90–120 implies ≈25–33 cars sold per forecourt a month. Treat this as an estimate.
- **Limitation:** Auto Trader's percentages use **UK** retailer gross; the US figures in this file use US franchised-group gross. Auto Trader's "sales gross profit" may include some finance commission; the slide does not say. Like-for-like, compare the 5–7% with the US **front-end** column.

---

## C. CARFAX dealer spend (archive anchors)

| Anchor | Value | Tier / source |
|---|---|---|
| Single rooftop, unlimited Advantage | **~$999/month**; capped tiers from $250 | [X, #4] Nissan FSM and ex-CARFAX rep; `X_expert_calls.md` §Price points (l.86) |
| Typical dealer spend | "**a couple thousand dollars a month**" | [X, #2] ex-Cox AVP (l.86) |
| Usage true-ups | One appraisal-heavy dealer: ~$2,500 → $4,800 → ~$6,800/month | [X, #2] (l.82) |
| AutoNation JLR White Plains bundle (Advantage + Listings + For Life) | **< $5,000/month**, flat for about 2 years (group deal) | [X, #6] (l.79) |
| Advantage + Listings revenue per dealer customer | **≈$1.4k/month** ($685m ÷ >40,000) | [C] `D2_unit_economics.md` l.56 |
| Advantage alone per dealer customer | **≈$0.9k/month** ($434m ÷ >40,000) | [C] D2 l.57 |
| Upper bound (all CARFAX segment revenue ÷ dealers) | ≤$2.4k/month | [C] D2 l.54 |
| Advantage per car sold (D14) | ≈$7–13 | [C] `D14_price_to_value.md` l.17 |
| Listings revenue | ≈$251m (22% of CARFAX) | [C] D2 / D14 l.20 |
| Price trend | ≈4–5% annual rises; "another 12%-15%" headroom; flat at AN for 2 years | [X, #1], [X, #6] |

The D2 per-dealer figures are averages across >40,000 dealer customers, independents included. They are not per franchised rooftop.

---

## D. Calculations

**Formulas**
- Used front-end gross per month = used retail units a month × used retail GPU.
- Used gross including F&I = units × (used GPU + F&I PVR). The blended F&I PVR is applied to used units [E].
- Share = vendor monthly spend ÷ dealer monthly gross.
- Per unit = vendor monthly spend ÷ used retail units a month.
- Monthly vendor spend: CarGurus = US QARSD ÷ 3. Cars.com = ARPD. TrueCar = quarterly dealer revenue ÷ 3 ÷ dealers.

**Rooftop denominators [C]**

| Rooftop | Used units/mo | Used front-end GP/mo | Used GP incl. F&I/mo | Total store GP/mo |
|---|---|---|---|---|
| AN franchised (FY25) | 81.9 | $127.3k | $354.0k | ≈$1.68m (upper bound) |
| GPI US (FY25) | 89.4 | $141.4k | $361.8k | ≈$1.61m |
| NADA-volume rooftop [E] (66/mo × AN per-unit gross) | 66.2 | $102.9k | $286.2k | n/a |

**Comparison table [C]**

The range in each column runs GPI → AN → NADA-volume rooftop. A larger rooftop gives a lower %.

| Vendor | Monthly spend per dealer | Per used unit | % of used front-end GP | % of used GP incl. F&I | What the dealer gets | Pricing trend |
|---|---|---|---|---|---|---|
| **CARFAX Advantage**, single rooftop unlimited [X #4] | $999 | $11–15 | **0.71–0.97%** | 0.28–0.35% | VHRs for appraisal and merchandising, CARFAX badges and links on listings; trust and compliance (CPO mandate) | ≈4–5%/yr list rises [X #1]; flat at AN group [X #6]; usage true-ups [X #2] |
| CARFAX Advantage, average per dealer customer [C, D2] | ≈$900 | $10–14 | 0.64–0.87% | 0.25–0.31% | same | — |
| CARFAX Advantage + Listings, average [C, D2] | ≈$1,400 | $16–21 | 0.99–1.36% | 0.39–0.49% | + leads from CARFAX Listings (closes at 1.98% [X #6]) | Listings: no price lever (D14) |
| CARFAX "couple thousand" [X #2] | ≈$2,000 | $22–30 | 1.41–1.94% | 0.55–0.70% | Advantage, likely with add-ons | — |
| **CARFAX full bundle** at an AN luxury store [X #6] | ≤$5,000 (ceiling) | $56–76 | **3.54–4.86%** | 1.38–1.75% | Advantage + Listings + For Life (service retention) | Flat about 2 yrs |
| **CarGurus** US, Q2-26 [D] | ≈$2,711 (QARSD $8,134 ÷ 3) | $30–41 | **1.92–2.63%** | 0.75–0.95% | Leads and connections, deal ratings, prominence; one marketplace | US QARSD **+8% y/y** (Q2-26 and Q4-25) |
| **Cars.com**, Q2-26 [D] | $2,500 (FY25 $2,460) | $28–38 | **1.77–2.43%** | 0.69–0.87% | Marketplace leads + websites + trade/appraisal + media (wider than listings) | ARPD **+3% y/y** Q2-26; FY25 −1% |
| **TrueCar**, Q3-25 [D] | ≈$1,222 | $14–19 | 0.86–1.19% | 0.34–0.43% | Pay-per-sale-style leads from affinity programs ($491/unit monetization) | Dealer count falling; taken private |
| **Auto Trader UK**, FY26 [D] / [IR] | £2,995 ARPR | £90–120 per used car sold (company estimate) | **5–7% of UK used sales GP** (company, FY18–22); my check gives 4.8–7.8% | 3–4% incl. aftersales (company) | Dominant marketplace (>75% of minutes, 11x the nearest rival) + data and pricing tools + Deal Builder | ARPR **+5%** FY26, +5% FY25, +12% FY24 |

**Shares of total store gross [C]** (AN, ≈$1.68m a month):
- CARFAX $999 ≈ **0.06%**.
- CARFAX $5,000 bundle ≈ 0.30%.
- CarGurus ≈ 0.16%.
- Cars.com ≈ 0.15%.

**Marketplace stack [C]:**
- A rooftop paying both CarGurus and Cars.com spends ≈$5.2k a month, or ≈**4.1%** of AN-rooftop used front-end gross.
- Autotrader.com (Cox, private) and Facebook come on top of that.
- On these averages, CARFAX Advantage is ≈20–35% of the marketplace subscriptions a dealer pays.

### Interpretation (Inference)
1. **Price share.** On a like-for-like basis (vendor spend ÷ used front-end gross), CARFAX Advantage takes **≈0.7–1.6%**. A single US marketplace takes ≈1.8–2.6%. Auto Trader UK, a near-monopoly classifieds business, takes 5–7%.
   - This supports D14's view that Advantage has **pricing headroom** relative to dealer economics.
   - The [X #1] figure of "another 12–15%" headroom would move Advantage from about 0.8% to about 0.9% of used front-end gross. That is still well below marketplace take.
2. **Why the gap may persist.** Classifieds sell leads with a measurable ROI. Auto Trader cites a 10x ROI; the dealer at [X #6] tracks close rates. Advantage sells trust and compliance, and a cheaper substitute exists (AutoCheck at 50–80% of the price [X]).
   - The constraint on Advantage pricing is therefore substitution, not dealer affordability.
3. **The full CARFAX bundle** (≈3.5–4.9%) is comparable to one or two marketplaces. Listings is the weak part of it on value per closed sale (D14).
4. **Pricing momentum.** CarGurus +8%, Auto Trader +5% and Cars.com +3% (FY25 −1%), against CARFAX at ≈4–5% list and flat for a large group.

## Data gaps and caveats
- **NADA Data figures** (used GPU, used units per dealership, total dealership gross) were not retrieved because nada.org is blocked. The only NADA figure is 66 used units a month from search snippets [context], and it may include wholesale.
- **AN F&I** is new/used blended. Used-specific F&I is probably lower, so the "% including F&I" figures may be slightly understated.
- **Customer mix:** classifieds' per-dealer averages (QARSD, ARPD) cover franchised and independent dealers, as does CARFAX's $0.9–1.4k. Franchised rooftops likely pay more than average on each platform, so the % of franchised-rooftop gross for the averages is probably **understated** for both CARFAX and the classifieds.
- **Cars.com ARPD** includes websites, trade/appraisal and media, so it is not pure listings.
- **CarGurus QARSD** is a marketplace-subscription metric (continuing operations); I did not re-check the 10-K definition for which products it includes.
- **Auto Trader's 5–7%** dates from 2022 (FY18–22). It has said since that the take rate has not risen meaningfully (FY25 AR). There is no FY26 refresh of the percentage, and no Auto Trader UK used GPU disclosure beyond "9–11%" of a £17k+ price.
- **AN store denominator** uses the 245 stores at year-end, not an average. Group 1 has 145 US stores and divested some during the year.
- **CARFAX prices** are expert anchors [X], not disclosed figures. The $5,000 bundle is a ceiling ("< $5,000") at one luxury store.
- **Lithia and other groups** were not pulled; AN and GPI give the range.
