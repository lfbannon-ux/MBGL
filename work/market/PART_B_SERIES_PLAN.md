# Part B — public series plan (fetch once the network allowlist opens)

Purpose: replace every [context] figure in `analysis/D9_demand_drivers.md` with fetched data. The data feeds the driver regressions and the stress cases (Part C).
Status: **nothing fetched yet.** FRED, BEA, Census, BLS, the Fed and third-party sites are not reachable today, and Quartr is the only source.

## Rules for the fetch

- Save raw downloads to `raw/market/<source>/` with fetch date and URL. Write a tidy CSV to `market/series.csv` with columns: `series_id, source, date, value, unit, sa_flag, freq, basis_label, fetched_utc, url`.
- **Basis labels.** Official statistics are [X-official]. Third-party press releases and indices are [X-3P]. Company-produced industry data (MBGL/SPGI Mobility press releases) is [X-co]. Say on every series whether it is SA, NSA or SAAR.
- **Calendar alignment.** Aggregate to calendar years (SPGI/MBGL, Dec FYE). For the 2015–21 overlap also aggregate Dec–Nov years (IHS Markit Nov FYE).
- **ID checks.** IDs marked "verify" are from memory. Confirm them on the FRED series page before use, and record any substitute.

## A. New-vehicle sales (SAAR) — confirms the slide-91 "Industry Growth" footnote (FRED, SA annual)

| Series | ID / URL | Freq | Basis | Use |
|---|---|---|---|---|
| Total vehicle sales, SAAR | FRED `TOTALSA` — https://fred.stlouisfed.org/series/TOTALSA | M | [X-official] BEA via FRED, SAAR, mn units | Reproduce slide 91 industry growth; episode dating |
| Light-weight vehicle sales: autos + light trucks | FRED `ALTSALES` | M | [X-official] SAAR | Light-vehicle SAAR (core comparator) |
| Lightweight auto / light truck sales | FRED `LAUTOSA`, `LTRUCKSA` (verify) | M | [X-official] SAAR | Mix |
| Heavy truck sales | FRED `HTRUCKSSAAR` | M | [X-official] SAAR | Excluded from comparator |
| Auto inventory/sales ratio | FRED `AISRSA` | M | [X-official] SA | Chip-shortage inventory trough 2021–22 |
| Motor-vehicle assemblies | FRED `MVAAUTLTTS` (verify) | M | [X-official] Fed G.17, SAAR | Production (Planning demand proxy) |
| BEA auto & truck unit sales detail | BEA NIPA underlying detail, Table 7.2.5S — https://apps.bea.gov/iTable/?reqid=19&step=4&isuri=1&nipa_table_list=2079&categories=underlying (verify link); also BEA "Motor Vehicle" xlsx at https://www.bea.gov/news/glance (verify) | M | [X-official] | Cross-check of TOTALSA |

## B. Used-vehicle transactions and prices

| Series | ID / URL | Freq | Basis | Use |
|---|---|---|---|---|
| Used car dealers, retail sales ($) | FRED `MRTSSM44112USN` (Census MRTS, NSA; verify) — https://www.census.gov/retail/index.html | M | [X-official] NSA $ (value, not units) | Used-dealer revenue proxy |
| Motor vehicle & parts dealers retail sales | FRED `RSMVPD` | M | [X-official] SA $ | Dealer-health proxy |
| CPI used cars & trucks | FRED `CUSR0000SETA02` | M | [X-official] BLS SA index | Used-price episode (2021–22 spike) |
| CPI new vehicles | FRED `CUSR0000SETA01` | M | [X-official] BLS SA index | Affordability / new–used price gap |
| Manheim Used Vehicle Value Index | https://site.manheim.com/en/services/consulting/used-vehicle-value-index.html (monthly press release; history PDF/xlsx if public) | M | [X-3P] Cox Automotive, mix/mileage/SA adjusted | Wholesale price cycle; Jan-22 peak |
| Cox Automotive used-vehicle retail & total sales estimates | https://www.coxautoinc.com/market-insights/ (used-vehicle inventory and sales posts; annual "used-vehicle sales" estimates) | M/Q/A | [X-3P] estimates | **Used retail units, the main D9 driver.** No official unit series exists |
| Kelley Blue Book ATP / incentives | https://www.coxautoinc.com/market-insights/ (KBB ATP monthly release) | M | [X-3P] | New ATP; incentive % of ATP (OEM spend proxy) |
| Edmunds used-vehicle reports (fallback) | https://www.edmunds.com/industry/insights/ | Q | [X-3P] | Cross-check of used units and prices |

## C. Dealer count / consolidation

| Series | ID / URL | Freq | Basis | Use |
|---|---|---|---|---|
| NADA Data (annual): franchised dealership count, dealer financials, gross profit | https://www.nada.org/nadadata | A (+ mid-year) | [X-3P] trade association | Rooftop base; consolidation trend; dealer profitability (retention driver per SPGI Q1-23) |
| Automotive News dealer census / Haig Report (public summaries) | https://www.autonews.com/ ; https://haigpartners.com/haig-report/ (quarterly; public summary) | A/Q | [X-3P] | Buy-sell deal counts (consolidation pace) |
| Census County Business Patterns, NAICS 44111/44112 establishments | https://www.census.gov/programs-surveys/cbp.html (API: `api.census.gov/data/<yr>/cbp`) | A | [X-official] | Independent (44112) vs franchise (44111) establishment counts |
| Public dealer groups' store counts | Quartr 10-Ks: AutoNation, Lithia, Penske, Group 1, Sonic, Asbury | A | [D] company filings | Consolidation share of rooftops |

## D. OEM marketing / incentive spend and recall activity

| Series | ID / URL | Freq | Basis | Use |
|---|---|---|---|---|
| OEM advertising expense | GM, Ford, Stellantis, Toyota 10-K/20-F notes (via Quartr) | A | [D] company filings | Direct OEM marketing spend proxy (no public aggregate exists) |
| Incentive spend per unit | J.D. Power / GlobalData monthly forecast releases — https://www.jdpower.com/business/press-releases ; KBB incentives % ATP (above) | M | [X-3P] | OEM discretionary spend proxy |
| NHTSA recalls: campaigns and vehicles affected | https://www.nhtsa.gov/nhtsa-datasets-and-apis (recalls flat file `FLAT_RCL.zip` at https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL.zip — verify) | daily → A | [X-official] | Recall-revenue driver (−$15m FY24) |
| US ad spend (auto category) | Public summaries only (Kantar/Vivvix, MediaRadar) — likely paywalled | Q | [X-3P] | Optional |

## E. Vehicles in operation and average age

| Series | ID / URL | Freq | Basis | Use |
|---|---|---|---|---|
| S&P Global Mobility "average age of vehicles in US" press releases (2014–2025) | https://press.spglobal.com/ (search "average age" / "vehicles in operation"); post-spin: https://mobilityglobal.com (newsroom; verify) | A (~May) | [X-co] company's own TIP/Polk data | VIO count and average age history; check against slide 70 labels |
| Auto Care Association factbook (VIO) | https://www.autocare.org/data-and-information | A | [X-3P] (sourced from S&P/Polk) | Cross-check |
| FHWA registered vehicles (MV-1) | https://www.fhwa.dot.gov/policyinformation/statistics.cfm | A | [X-official] | Independent VIO check |
| Vehicle miles traveled | FRED `TRFVOLUSM227NFWA` | M | [X-official] NSA | Service-lifecycle / Car Care demand |
| Canada VIO | StatCan Table 23-10-0308-01 (vehicle registrations; verify) | A | [X-official] | International whitespace (slide 75 ~28M) |

## F. Auto lending

| Series | ID / URL | Freq | Basis | Use |
|---|---|---|---|---|
| Motor vehicle loans outstanding (owned & securitized) | FRED `MVLOAS` (Fed G.19; verify) | Q | [X-official] NSA $ | Credit availability |
| Finance rate, new auto 60-month, commercial banks | FRED `RIFLPBCIANM60NM` (verify) | Q | [X-official] | Affordability |
| Finance rate, new auto 72-month / finance companies | Fed G.19 release tables — https://www.federalreserve.gov/releases/g19/current/ | M/Q | [X-official] | Term extension |
| Auto delinquency (90+ days) | NY Fed Household Debt & Credit Report — https://www.newyorkfed.org/microeconomics/hhdc | Q | [X-official] | Lender stress |
| Senior Loan Officer Survey: auto-loan standards | FRED `STDSAUTO` (verify) | Q | [X-official] | Credit tightening (10/A risk factor) |
| Experian State of the Automotive Finance Market (84-month share, avg payment) | https://www.experian.com/automotive/auto-credit-webinar-form (registration wall) | Q | [X-3P] | Verify LaFeir's ">20% of car loans at 84 months" |
| Fed funds / 2y Treasury | FRED `FEDFUNDS`, `DGS2` | M/D | [X-official] | Rate regime |

## G. Insurance

| Series | ID / URL | Freq | Basis | Use |
|---|---|---|---|---|
| CPI motor vehicle insurance | FRED `CUSR0000SETE` | M | [X-official] BLS SA index | Premium spike 2023–24 (shopping → underwriting volumes) |
| LexisNexis Insurance Demand Meter (shopping / new policies) | https://risk.lexisnexis.com/insurance (quarterly public summary) | Q | [X-3P] | Underwriting-volume proxy for BIG/Financials (+$17m/+$13m) |
| J.D. Power insurance shopping study | https://www.jdpower.com/business/press-releases | A | [X-3P] | Cross-check |

## H. International (Canada, Germany, Italy, Spain) and FX

| Series | ID / URL | Freq | Basis | Use |
|---|---|---|---|---|
| Canada new motor vehicle sales | StatCan Table 20-10-0001-01 — https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2010000101 | M | [X-official] | 2026 Canada softness (Q2-26 call) |
| Canada used vehicle (fallback) | DesRosiers / AutoTrader.ca price index public releases | M | [X-3P] | CARFAX Canada transactional proxy |
| Germany new registrations and used-car ownership transfers ("Besitzumschreibungen") | KBA — https://www.kba.de/DE/Statistik/Fahrzeuge/fahrzeuge_node.html | M | [X-official] | CARFAX Germany TAM (launched Jul-26) |
| Italy used transfers (passaggi di proprietà) | ACI / UNRAE — https://www.aci.it/ ; https://unrae.it/ | M | [X-official]/[X-3P] | Italy |
| Spain used sales | ANFAC / Ganvam — https://anfac.com/ | M | [X-3P] | Spain |
| Global LV production/sales | OICA — https://www.oica.net/production-statistics/ | A | [X-3P] | Planning-solutions context |
| CAD/USD, USD/EUR | FRED `DEXCAUS`, `DEXUSEU` | D | [X-official] | FX (~$5m 1H-26 benefit) |

## I. Company-side series to pair (already in Quartr; for the regressions)

- Slide 91 organic growth (re-read the image to confirm the year mapping), INFO Transportation organic/recurring bridges, SPGI Mobility revenue by year and quarter, MBGL CARFAX/B2B subscription/transactional by quarter (`extraction/*.csv`).
- SPGI quarterly earnings supplements: Dealer / Manufacturing / Financials growth to fill the n/a cells in D9 §4 (SPGI IR site, needs allowlist).

## Priority order (if fetch budget is limited)

1. `TOTALSA`, `ALTSALES`, `CUSR0000SETA02`, `CUSR0000SETE`, `AISRSA` (FRED).
2. Cox used retail sales estimates and the Manheim index.
3. NADA dealer count and dealer gross profit.
4. NHTSA recall file.
5. S&P/MBGL VIO and age releases.
6. G.19 / NY Fed lending.
7. StatCan and KBA.
8. The rest.
