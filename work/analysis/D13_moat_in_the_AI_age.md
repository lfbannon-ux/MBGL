# D13: Competitive advantage and the AI age, from every transcript (2020-11 to 2026-09)

**Corpus.** 68 transcribed events: 3 Mobility Global events (Investor Day 2026-05-12, Q2-26 call 2026-08-07, Goldman Sachs 2026-09-10), 2 IHS Markit calls (2021) and 63 S&P Global events.
- 236 relevant passages, each with a verbatim quote and a Quartr link, sit in the evidence files:
  - `AI_evidence_MBGL_investor_day.md` (116)
  - `AI_evidence_MBGL_Q2_GS.md` (36)
  - `AI_evidence_predecessors.md` (84)
- **Tiers:** management statements are [IR]; analyst assertions are [X]. Lines marked **Inference:** are my judgement. Quotes are verbatim, at most 2 sentences.

## 1. What management says the advantage is

| Pillar | Management's words | Who / when |
|---|---|---|
| Proprietary, contractual data network | "Every one of those 177,000 sources are contractual relationships that are slow to replicate." | Morehouse, Investor Day 2026 |
| Depth built over time | "It's a relationship by relationship, shop by shop, dealer by dealer, police agency by police agency, ground truth built over 40 years. Good luck trying to replicate it." | Fredericks (CARFAX), Investor Day 2026 |
| Embeddedness / switching costs | "We're so embedded in these systems that the switching cost is just too high. It's way too high." | Morehouse, Investor Day 2026 |
| Brand + data, not the app | "We have been application agnostic for decades, where our differentiation comes from the combo of that brand and data, not the application itself." | Eager (CEO), Goldman Sachs 2026-09-10 |
| Positioning vs rivals | "If we do typically see that, the competitors, it's a low-cost alternative to what we're providing and a very different product." | LaFeir (B2B), Investor Day 2026 |
| Parent's view at the spin | "This data and technology is deeply entrenched in the workflows of mobility customers, creating a very strong competitive moat…" | Cheung (S&P Global CEO), spin call 2025-04-29 |

**Supporting numbers (as stated) [IR]:**
- 177,000 sources; 38bn CARFAX records; 13bn B2B transaction records; ~800m VINs.
- More than 90% of revenue from proprietary data.
- 40 of 40 top OEMs; 36 OEMs require CARFAX for certified pre-owned (CPO); 40,000+ dealers.
- 53m Car Care users; 54m monthly visits.
- NRR "meaningfully north of 100%".

**How the language changed (predecessor era):**
- "Critical must-have products" (IHS Markit, Jun 2021).
- "Other people could do this, but they'll have to invest a lot of time and effort to replicate what we have." (Tavernier, S&P Global Investor Day, Dec 2022): the only on-record concession that the data is replicable.
- "Fairly unique" (Peterson, May 2024).
- "Hard to recreate" (Jun 2024).
- "Very strong competitive moat" (Apr 2025).

The claims got stronger over time; the evidence offered for them did not.

## 2. What management says about AI

**The thesis [IR]:** models are becoming a commodity, but decision-grade, VIN-level proprietary data and a trusted brand are not. AI is therefore framed as an *accelerant*, not a threat.
- "AI is not replacing the need for a company like ours. It's actually creating a global demand for our data because the data we provide is decision-grade." (Morehouse, Investor Day)
- "We have decision-grade data, VIN-level data, global data that allows us to provide these services to customers in a trustworthy way that public AI can't do." (Morehouse, Investor Day)
- "As AI generates more intelligence from our data, the value of our data only grows." (Eager, Q2-26 call)
- "When I think of AI impacting our business, I really do think about it as an accelerant for our business." (Eager, Goldman Sachs)
- **Brand in "data overload":** provenance and trust become more valuable when information is abundant (Eager, Goldman Sachs). This was asserted with no usage data.

**The four "AI engines" (Investor Day):**
1. **Productivity.** Engineering productivity rose 10–15% last year and "four to five times that" in Q1-26; 84% of chat/email queries are deflected to AI.
2. **Data amplification.** Service-record decoding runs at 99.5% production accuracy; accident records are ingested within two hours.
3. **Supercharged core products.** Behavior Prediction Score: +10% loyalty. Data Studio: +40% close rates. FAST forecasting: 90% of workflow automated.
4. **New products and channels.** Exposing data to customers' AI agents via MCP: "We're designing infrastructure to monetize those agents." Also VIN-level future reliability, offered as an opportunity only.

Cost realism: "We can't just throw all this at an LLM. I think it's very expensive." (Morehouse). The company builds bespoke models and claims "nearly a decade" of machine learning.

**Predecessor era:** AI appears only four times, all about efficiency or distribution:
- Autopilot internal LLM tool, Jul 2023;
- Mobility data on the S&P Marketplace as an "early opportunity", Nov 2023;
- Mobility benefiting from S&P's AI and extraction tools, Jun 2024;
- the GenAI Car Fox video, Oct 2024.

## 3. What is quantified, and what is not

| Quantified [IR] | Never quantified |
|---|---|
| Operational AI metrics: 99.5% accuracy, 84% deflection, 4–5x engineering productivity, 100+ data scientists (later "hundreds"), 25m AI-generated videos/month | AI revenue, or AI's share of growth |
| Customer-outcome claims: +10% loyalty, +40% close rates, 10–15x dealer ROI | AI cost savings in $ or bp. The 50bp/yr margin target is not attributed, and AI savings are "reinvested" near term (CFO, Goldman Sachs) |
| Data-scale metrics (sources, records, VINs) | Any MCP/agent or data-licensing revenue, or any customer using it |
| | Retention/NRR as a number; contract length or exclusivity ("It's a mix"); share vs AutoCheck |
| | Share of CARFAX consumer traffic arriving via search or AI assistants vs direct/dealer-embedded |

**Disclosure pattern [C]:** none of the Investor Day AI numbers recur at the Q2 call or at Goldman Sachs. The data-rights line ("The data we have isn't scraped, it's not publicly available, and it's not synthetic.", Morehouse, Investor Day) was replaced by "the majority of it's sitting behind a firewall or a paywall somewhere", which says nothing about contracts or exclusivity.

## 4. Questions not asked, and questions not answered

**Never raised by any analyst, and never volunteered by management, in all 68 events:**
- AI search and chatbots sitting between car shoppers and CARFAX (54m monthly visits; "Show me the CARFAX").
- LLMs reproducing vehicle-history content from dealer-posted reports.
- Licensing data to AI companies.
- OEM telematics/connected-car data competing with the contributor network.

The last of these was flagged in 2021: "There are still some significant question marks around access to VIN level data, who owns that data, which will have to play out over the next two or three years." (Tavernier, IHS Markit Q2 FY21). No later event revisits it.

**Asked but not answered:**

| Analyst (event) | Question | Answer given |
|---|---|---|
| Unnamed (Investor Day) | How does CARFAX compete with AutoCheck? | "We don't compete with anyone directly across that entire thing." |
| Meuler, Baird (Investor Day) | Metrics vs AutoCheck; is Polk registration data public? | No metrics. Answered with secrecy and "what we wrap around it". |
| Kaplan, Morgan Stanley (Investor Day) | How exclusive are the source contracts? | "It's a mix." No terms given. |
| Kramm, UBS (Investor Day) | NRR | The NRR slide was withdrawn; no number given. |
| Bhatia, Morningstar (Q2-26 call) | Marketplaces switching to AutoCheck | Not confirmed, denied or sized. Answer: "pockets of increased competition". |
| Bhatia, Morningstar (Q2-26 call) | Customer acquisition cost | No number; answer pivoted to AI efficiency. |
| Tong, Goldman Sachs | Can AI make the applications easier to build? | Answered only obliquely, via "application agnostic". |
| Tong, Goldman Sachs | How much of the margin target comes from AI? | No figure; savings reinvested. |

**Tone shift, May → Sep 2026:**
- From "switching cost is way too high" to admissions: competitors are "very good", there are "pockets of increased competition", and CARFAX is "the new kid on the block" in Listings and Service Loyalty.
- The Q2 guidance cut was blamed on go-to-market execution, not on competition or AI.

**S&P Global's stance:** its "AI + proprietary data" identity (Investor Day 2025) is stated only for the four divisions it kept. No statement places Mobility inside or outside that frame. The spin rationale given was customer and portfolio fit: dealers are a customer base S&P can't cross-sell to.

**Inference:** this does not show S&P saw AI risk in Mobility. It does mean the "proprietary data wins in the AI age" thesis was never applied to this asset by its previous owner on the record.

## 5. Assessment: how the advantage stands in the AI age (Inference, built on [D]/[IR] evidence)

**Layer by layer:**

1. **Supply-side data network: likely strengthened by AI, if the contracts hold.**
   - Contractual, two-way exchanges with service shops, police agencies and DMVs (records tied to specific vehicles, by VIN) cannot be scraped or synthesised. AI lowers the cost of using the data (decoding, ingestion) more than the cost of getting it.
   - Weak point: contract terms, exclusivity and source churn are undisclosed ("It's a mix"). The 2021 connected-car ownership question was never answered. OEM telematics is the most plausible route to a parallel record.

2. **Consumer brand / demand-pull: the least defended layer.**
   - Dealers pay largely because shoppers ask for CARFAX.
   - If shopping moves into AI assistants, the brand has to travel inside someone else's interface. Management's answer is MCP/agent monetisation ("monetize those agents"), with no customers, revenue or partners disclosed.
   - Advertising spend grew 31% over FY23–25 against revenue +18% [C] (D1). That is consistent with rising costs to keep the brand front-of-mind, though it doesn't prove AI-driven pressure.
   - No one has asked about this risk on the record.

3. **Institutional embeddedness: robust.**
   - 36 OEM CPO mandates, DMV/insurer links and "hundreds" of integrations are rule-based, not click-based. AI changes the interface, not the requirement.
   - "Application agnostic" is a coherent defence here.

4. **B2B application layer (automotiveMastermind, Polk audiences, forecasting): most exposed.**
   - Management's own framing ("differentiation comes from … brand and data, not the application") implies applications commoditise. B2B is where management concedes "low-cost alternatives".
   - It is also where economics are already weakening: FY25 incremental Adj. EBITDA margin −17.6% [C]; B2B GAAP operating margin about 3% in 2026 [C] (Segment P&L tab).
   - AI lowers the cost for rivals and for in-house teams at OEMs to build models on purchasable data.

5. **AI as a cost lever: real but unpriced.** The operational metrics are credible and specific, but no dollar savings are given and near-term savings are reinvested. Investors are asked to take the margin benefit on trust until 2028 (the CFO said the 50bp/yr target would not be reached until 2028).

**Net view:** the advantage is strongest where it is physical and contractual (the record network, CPO mandates). It is weakest where it depends on consumer attention (brand demand-pull) and on applications (B2B). Management's AI narrative addresses the first convincingly in words, the second not at all, and the third only by redefining the moat as "brand + data". The most important unknown is how much CARFAX consumer demand flows through channels an AI assistant could intermediate. It is undisclosed and unasked.

## 6. Questions to put to management

1. **Traffic mix.** What share of the ~54m monthly CARFAX visits and report views comes direct, via dealer listings, via search, and via AI assistants? How has that mix moved since 2024? Have any AI platforms requested or licensed CARFAX data?
2. **Contracts.** What share of data sources and records come under exclusive or multi-year contracts? What is annual source churn? Has any source declined renewal citing AI/LLM use, or asked for new terms?
3. **Agents.** How many customers use the MCP/agent interface, and how is it priced? What revenue does management expect from "monetizing agents" inside the 1–2% new-products growth target?
4. **B2B.** Which automotiveMastermind/Polk products face in-house OEM or AI-native substitutes? What is B2B gross retention?

## Honest counters (evidence against my concerns)
- **AI may genuinely raise the value of proprietary data.** Ground-truth, VIN-level data built over 40 years, with two-way value exchange (shops get traffic, police get tools), is exactly what general models lack. Tavernier's 2022 concession was about time and effort, not impossibility, and AI hasn't changed the physical collection problem.
- **CARFAX use is often mandated rather than chosen.** CPO mandates, lender/insurer workflows and dealer listing integrations make many reports institutional. Even if consumers discover cars via AI, the transaction still needs a trusted, citable report. The "brand in data overload" argument has logic, even if unproven.
- **The company is acting, not just talking.** It has an AI office, bespoke models, and launched Germany early with AI-accelerated data work. The operational metrics are specific enough to be checked later.
- **Silence is not evidence of risk.** No analyst raising AI disintermediation may reflect that informed investors don't see it as material. And the guidance cut was attributed (credibly) to self-inflicted go-to-market changes, not to AI or competition.
