# segments_kpi — NOTES (Mobility Global Inc., MBGL)

Scope: SEG, REV_DISAGG, NONGAAP, KPI for ERA C (Form 10 / Form 10/A carve-out) and ERA S (10-Q Q2-2026, 8-K release, Q2-2026 slides).
Method: Quartr `read_document`, structured rows only. Rows: 1,868 (incl. 20 resumed rows from the prior run, Form10A p.346, kept unchanged).
Conventions: `6M-2026`/`6M-2025` = six months to June 30. A printed dash in a segment cell is recorded as 0. Parentheses are recorded as negative values. Growth %
rows are recorded only where printed. Text rows (`unit=text`) hold short verbatim definitions. Rows marked "(abridged)" or "(paraphrase)" are labelled as such.

## Source map (Quartr page numbers)
| Doc | documentId | Pages used |
|---|---|---|
| Form10A_2026-05-27 | 3603533 | Summary/KPIs 262-272; MD&A 340-361; Human capital 384-385; goodwill 367; interim Note 6/7 430-433; audited Note 6/7/8 459-463 |
| Form10_2026-05-07 | 3603535 | Business 351; MD&A non-GAAP 436-439 (comparison only) |
| 10Q_Q2-2026 | 3699447 | Note 2 p.10; Note 7 pp.14-15; MD&A pp.19-29 |
| 8K_2026-08-07 (release) | 3699450 | pp.1-3, Exhibit 4 p.8, Exhibit 5 pp.9-11 |
| Slides_Q2-2026 | 3986013 | pp.5-9, 11-14 |
Page offsets: Form 10/A Quartr page = printed page + 261 (front sections), and F-1 = p.421. Form 10 Quartr page = printed page + 340.

## Segments: definitions and how they changed
- **Two reportable segments in every document:** CARFAX and B2B. B2B has two business lines, Marketing & Sales (automotiveMastermind, Polk Auto Solutions, Market Scan, Data Studio, Recall, VIN Solutions) and Strategy & Planning (forecasting, Global Reporting, FAST, PIQ, DA stake). There is also an unallocated "Corporate" category.
- **Form 10 / Form 10/A (CODM measure = segment operating profit):** "Segment operating profit is defined as operating profit before Corporate Unallocated expense" (10/A p.347). The audited Note 8 also excludes Other income, net and Interest expense, net (p.461). The ASU 2023-07 table shows Revenue, then "segment expenses", then "other segment items" (mainly acquired-intangible amortization plus special items), giving segment OP. The 2025 realignment and the refined cost allocation were applied to all prior periods (Note 8). Goodwill is tested across 3 reporting units (p.367).
- **10-Q Q2-2026 (CODM measure = Adjusted EBITDA):** "Beginning in the second quarter of 2026, the Company changed its segment profitability measure from segment operating profit to Adjusted EBITDA and recast prior period amounts" (p.14). So the 10-Q "segment expenses" (CARFAX Q2-26 159) are **not comparable** with the 10/A "segment expenses" (CARFAX Q1-26 162). The 10/A figure excludes amortization and special items but includes depreciation and SBC. The 10-Q figure excludes D&A, SBC, transaction and severance costs.
- **CODM:** in the 10/A it was the President of S&P Global Mobility (CEO-designate). In the 10-Q it is the CEO.
- **Segment assets:** disclosed in the 10/A (interim and audited Note 8, plus D&A and capex by segment). The 10-Q states that asset information by segment is not disclosed because the CODM does not use it.

## Non-GAAP definition differences (important)
- **Adjusted EBITDA, Form 10 and Form 10/A (identical text):** 10 exclusions. They add acquisition integration costs, acquisition/disposition costs, legal settlement recovery and "other non-operational and/or non-recurring". Interest is called "interest", not "interest expense, net".
- **Adjusted EBITDA, 10-Q / 8-K Exhibit 5:** 6 exclusions. Item (6) is "employee severance charges and other costs that are not representative of the underlying economics". The acquisition and legal-recovery items are dropped, because the Q2-2026 periods have none of them.
- **Q2 slides p.12 still print the 10-item Form 10 definition** while showing the 6-line reconciliation. The slide definition was not updated to match.
- **Form 10/A only:** Adjusted operating profit, Segment Adjusted EBITDA (operating-profit based, with an 8-item list that includes ELT transition costs) and margins. "ELT transition costs" are excluded from Adjusted OP / Segment Adj EBITDA but do not appear in the 10-item Adjusted EBITDA list. FY2025 B2B shows a (5) ELT benefit and Corporate shows +5 (net 0).
- **NI-based vs OP-based Adjusted EBITDA (Form 10/A):** these normally tie. However, FY2024 segment columns cross-foot to 659 against a printed total of 658, and FY2023 segment columns sum to 597 against a printed total of 598. The FY2023 total column also does not foot (OP 239 + 295 + 17 + 9 + 4 = 564 vs printed Adj OP 565; Amortization total printed 295 vs 190 + 106 = 296). These look like rounding or Other-income effects. They are recorded as printed and not fixed.
- **Free cash flow:** the definition is the same everywhere (CFO less capex). The 10/A and 10-Q add "Capital expenditures include purchases of property and equipment and additions to technology projects".
- **Revenue labels:** filings use "Subscription / Non-subscription". The slides use "Subscription / Transactional", with the same values (e.g. CARFAX Q2-26 60 = non-subscription).

## Tie-outs performed (all pass unless listed)
- 10-Q Note 7: CARFAX + B2B + Corporate equals Total for revenue, segment expenses and Adj EBITDA in all 4 periods. Revenue minus segment expenses equals Adj EBITDA for each segment.
- 10-Q MD&A per-segment OP-to-Adj EBITDA reconciliations foot in every column. NI-to-Adj EBITDA (Note 7) foots: 202 / 188 / 386 / 357.
- 10-Q segment U.S./International revenue sums to the total U.S./International figures. Subscription plus non-subscription equals the total by segment.
- Form 10/A ASU 2023-07 tables (Q1-26, Q1-25, FY25, FY24, FY23): Revenue − segment expenses − other items = segment OP. Segment OP − Corporate = OP: 81 / 84 / 339 / 298 / 239.
- Form 10/A Q1 segment OP plus 10-Q Q2 segment OP equals the 10-Q 6M figures (CARFAX 89 + 101 = 190; B2B 5 + 3 = 8; Corp −13 − 22 = −35; 6M-25 also ties). Form 10/A Q1 geography plus 10-Q Q2 equals 6M.
- Segment revenue sums to combined revenue in every document and period.

## Corrupted text / flags
1. **8-K Exhibit 5 (pp.9-10):** the add-back lines are corrupted ("1ŏ01", "6130", "8 2 2 1", "7356", "INN to", "212", "3263", "5531", "555", "324"). Only the clean OP, Adj EBITDA and margin rows by segment were recorded from the 8-K. Use the 10-Q pp.24-25 reconciliation, which is clean and foots.
2. **8-K Exhibit 4 Q2-2026 block (p.8):** text is corrupted ("888", "662"). Values were recorded where they foot uniquely in both directions: OpRel 68/66/134; S&G 93/60/22/175; D&A 50/27/77; totals 211/153/22/386. The section caption flags this.
3. **8-K Exhibit 4 D&A split vs the 10-Q reconciliation:** Q2-2025 shows CARFAX 49 / B2B 28, but the 10-Q reconciliation gives amortization + depreciation of 50 / 27. 6M-2025 shows 99 / 56 vs 100 / 55. Totals agree (77 / 155) and segment OP agrees. These are recorded as printed, as a release inconsistency.
4. **Slides p.13, 6M-2025 stock-based compensation:** printed 6, but the 10-Q and the cash-flow statement show 9. The slide column foots to 354, not the printed 357. SBC is recorded as printed (6) and flagged here. The transaction-costs row also contains a stray extra "40" in the text; 6M-2025 transaction costs are recorded as 2, which matches the 10-Q.
5. **Form 10/A NI-to-Adj EBITDA (p.358):** add-back rows are corrupted (the Form 10 text p.437 is identical). Clean rows (NI, interest, tax, D&A, Adj EBITDA, margins) are recorded. SBC (4/5/22/28/20) and transaction costs (Q1-26 21, FY25 21) are recorded only after cross-checking against the segment tables (pp.359-360) and audited Note 6 (SBC 22/28/20). Severance, integration, legal and Other rows of the NI reconciliation were not recorded.
6. **Form 10/A segment table Q1-2026 (p.359):** B2B Segment Adj EBITDA (49) and B2B SBC are missing from the 10/A text. They appear in the Form 10 text (p.438: B2B 49, SBC 3) and were recorded under Form10_2026-05-07. Q1-26 B2B depreciation (1) is not legible in either document and was not recorded. FY2025 "Other (1)" by segment is ambiguous ("1 2"), so only the Total (2) was recorded. The CARFAX FY2025 OP margin is absent from the text (it is 28% in the MD&A segment table p.355).
7. **Audited Note 7 restructuring by segment:** partly corrupted. Only the legible values were recorded.

## Restatements / differences across documents
- **Form 10 vs Form 10/A:** the MD&A non-GAAP pages (Form 10 pp.436-439 vs 10/A pp.357-360) carry identical figures and definitions. Customer KPIs (Form 10 p.351 vs 10/A p.272) are identical. No restatement was observed in the pages compared. The full Form 10 F-pages were not re-extracted.
- **Form 10/A vs 10-Q comparatives (6M-2025, Q2-2025):** consistent with the 10/A Q1 data (see tie-outs). The prior-period segment measure was recast to Adjusted EBITDA, which is a new measure rather than a restatement of segment OP.
- **Employees:** the Summary gives "over 3,400 FTEs" at 12/31/2025 (p.268). Human Capital gives about 3,522 FTE at 3/31/2026 (p.384).

## Guidance (8-K and slides, both dated August 7, 2026)
- FY2026: Revenue $1,870–1,885m (growth 6.9%–7.7%); Adj EBITDA $745–760m; margin ~40%.
- Basis: carve-out 1H plus consolidated 2H. No forward reconciliation is given. No incremental net FX is assumed for 2H.
- Slide assumptions: about 150bps run-rate standalone cost impact (about half felt in 2026); $50m of about $100m one-time spin costs in 2H cash flow (about 50% capitalized); 2H interest about $55m; first $60m interest payment in Q4; GAAP tax rate 28–31%; cash taxes $80–90m higher; average shares 295–297m.
- The release says medium-term targets were "reiterated", but the targets themselves are not printed in the release or slides. They are presumably in the Investor Day deck 3352878, which was not extracted.

## NOT disclosed (in the sources read)
- Revenue by brand or product (CARFAX sub-lines; automotiveMastermind; Polk; Market Scan; Recall; Planning Solutions). Only segment-level revenue is given; B2B business-line revenue (Marketing & Sales vs Strategy & Planning) is not.
- Organic or constant-currency growth. Only the FX benefit is given (~$1m Q2-26, ~$5m 1H-26, slides p.5). Acquisition/disposition effects are given only for FY2024 (Market Scan +$3m, Catalyst −$5m).
- Customer counts beyond "more than 40,000 dealer customers". Not disclosed: revenue retention or NRR (described only qualitatively), ACV, ARR, ARPU/price per location, BIG customer count, dealer location counts by product, churn.
- Recurring-revenue %, other than the subscription share (81–82% of total).
- Geography beyond U.S. / International. No country or regional revenue is given; the 10/A says no foreign country exceeds 10% of revenue.
- Segment-level net income, interest or tax. Segment assets in the 10-Q.
- A reconciliation of forward-looking non-GAAP guidance.
- Quarterly data before Q1-2025, and 9M or Q3 data (not yet filed at these sources).
