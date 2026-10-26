"""Build deliverables/MBGL_Segments_and_Products.docx (+ .md twin).

"Mobility Global — Segments and Products: evidence from the antitrust record and expert calls".
Deterministic: all content is defined below; segment numbers are read from canonical/segment_pl.csv
and Investor Day percentages from extraction/presentations.csv.

House style: Arial, navy #1F3864 headings, banded tables (navy header, #D9E1F2 alternate rows),
quote callouts (indented italic, navy left border, light shading) with an attribution line.

QA:  python3 build_segments_products_doc.py --verify <expert_call_text_dir> <filing_src.txt>
     checks every expert quote verbatim (whitespace/quote-mark normalised) against the AlphaSense
     transcript text and its stated page, and every filing quote against the Quartr page text excerpt.
"""
import csv, glob, os, re, sys
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DOCX = f'{W}/deliverables/MBGL_Segments_and_Products.docx'
OUT_MD = f'{W}/deliverables/MBGL_Segments_and_Products.md'
NAVY = RGBColor(0x1F, 0x38, 0x64); NAVY_HEX = '1F3864'; BAND_HEX = 'D9E1F2'; QUOTE_HEX = 'EEF2F9'
GREY = RGBColor(0x59, 0x59, 0x59)
TITLE = 'Mobility Global — Segments and Products'
SUBTITLE = 'Evidence from the antitrust record and expert calls'
DATE = '26 October 2026'

# ---------------------------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------------------------
# Expert calls (AlphaSense). n -> (interview date, short role, file-id prefix, independence note)
CALLS = {
    1: ('13 Jul 2026', 'ex-CARFAX BIG sales manager, now Black Book', '0fb2bd44', 'Same person as #3; left CARFAX Jan 2024'),
    2: ('9 Jul 2026', 'ex-Cox Automotive AVP Product, now iPacket', '31405ae3', 'Independent; Cox alumnus, not at Cox for the 2025 switch'),
    3: ('3 Jul 2026', 'ex-CARFAX BIG sales manager, now Black Book', 'e7de514f', 'Same person as #1 (counted once)'),
    4: ('23 Jun 2026', 'Nissan NMAC finance manager; ex-CARFAX rep', '65d937a3', 'Independent; OEM customer, left CARFAX ~2018'),
    5: ('18 Jun 2026', 'ex-CARFAX Director, Data Acquisition', '2d7e5416', 'Independent; left ~2020; friend of CEO'),
    6: ('30 Sep 2026', 'AutoNation JLR store GM (CARFAX customer)', 'ddd64411', 'Independent; only call after the Aug-2026 guidance cut'),
    7: ('15 Jan 2026', 'Edmunds senior account executive', '31276b5b', 'Peripheral; never mentions CARFAX'),
    8: ('25 Sep 2025', 'Tire Discounters regional manager', 'c8bccf36', 'Peripheral; data contributor; one CARFAX mention'),
    9: ('10 Feb 2021', 'ex-CARFAX Director, Strategic Insights', 'b5804e99', 'Independent; 2021 baseline only'),
}
# Filing keys -> citation label
DOCS = {
    'INFO16': 'IHS Markit FY2016 10-K (Quartr 223426), Note: Litigation',
    'INFO17': 'IHS Markit FY2017 10-K (Quartr 223425), Note: Litigation',
    '10A': 'Form 10/A (Quartr 3603533)',
    '10Q': '10-Q Q2-2026 (Quartr 3699447)',
}

Q = {}  # id -> dict(kind, src, page, text)


def x(qid, call, page, text):
    Q[qid] = dict(kind='X', src=call, page=page, text=text)


def d(qid, doc, page, text):
    Q[qid] = dict(kind='D', src=doc, page=page, text=text)


# ---- expert-call quotes (verbatim, <=2 sentences) ----
x('X1a', 1, 3, "The dealer market for CARFAX is very saturated. They're going to have pretty much over 90% market share already, if not higher.")
x('X1b', 1, 3, "They call them stores, they might get 8%. Your big customers like Sonic and AutoNation, like Lithia, all the larger ones, they're in your 5%s.")
x('X1c', 1, 3, "They complain and threaten to cancel but it seems that they rarely ever do.")
x('X1d', 1, 3, "CARFAX has always been, before they do a price increase, they will typically launch something new to justify it.")
x('X1e', 1, 4, "I think we're another 12%-15%. I think that's when the cost gets pretty high.")
x('X1f', 1, 4, "They were selling cars, it was two to three days faster, and for about $200-$300 more.")
x('X1g', 1, 5, "CARFAX for police is able to respond to 70% of crashes throughout the country.")
x('X1h', 1, 5, "CARFAX has over 90,000 service shops sending them data.")
x('X1i', 1, 6, "CARFAX will typically give that away for free as long as the service shop agrees to send them all the data whenever they get somebody come into their shop.")
x('X1j', 1, 6, "It would take them years, probably three to five years to do and maybe to gain 20%-25% market share.")
x('X1k', 1, 6, "They don't have any data that a shop or a dealer would necessarily want.")
x('X1l', 1, 7, "AutoCheck is roughly half. About half the price.")
x('X1m', 1, 8, "The other 90%, it was about a 50/50 split between CARFAX and AutoCheck on who they were using on the lender side.")
x('X1n', 1, 9, "The advantage that CARFAX has is CARFAX has all the odometer readings.")
x('X1o', 1, 10, "It was taking CARFAX two to three years to onboard a new insurance company from the time they said they were interested. When I left in 2024, they had roughly half of insurance companies buying data.")
x('X1p', 1, 10, "Once they built the database up, they were going to turn around and sell it.")
x('X1q', 1, 11, "I think it's always going to be a sideshow, with the idea it could grow. It's my understanding that the data over there, it's a lot more restricted than it is in the States.")
x('X1r', 1, 7, "That said, this space, future reliability repair is saturated.")

x('X2a', 2, 2, 'I\'ve heard of, "Our price doubled," "Our price tripled," I talked to a dealer about that two weeks ago.')
x('X2b', 2, 2, "both of these companies struggle with accident severity in their reports.")
x('X2c', 2, 2, "Cox said we're going to work with Experian AutoCheck only for Autotrader.")
x('X2d', 2, 3, "I think it was a little more of like an industry statement, if that makes sense.")
x('X2e', 2, 3, "It wasn't paying Cox much anyway, because they had a reciprocal agreement going where they're putting CARFAX reports into some of Cox's B2B software for the dealers.")
x('X2f', 2, 4, "98% of them are going to say CARFAX, because they've seen the Super Bowl commercials, they've seen the race cars, the Fox, all that.")
x('X2g', 2, 4, "It might be one of the last things to go.")
x('X2h', 2, 4, 'all of their bosses are saying, "Just use AI to do it all. We don\'t need to spend any more money."')
x('X2i', 2, 5, "That's 75% of the franchise dealers, at least, are on vAuto.")
x('X2j', 2, 5, "Even though there's drama on the Autotrader side, they haven't broken it on the vAuto side yet, where then it'll pull in CARFAX data inside that application.")
x('X2k', 2, 5, "Mastermind is the, I don't know if gold standard is the right word, but they're the benchmark in the industry.")
x('X2l', 2, 6, "Every provider seems to run to about 7,000 or 8,000 dealers in the auto industry and then start to stall out, because that's half the franchise base.")
x('X2m', 2, 7, "Polk was definitely what the industry leans on for sales data.")
x('X2n', 2, 7, "the complaint is always that it's too old, it takes 90 days for them to get that.")
x('X2o', 2, 7, "they went from something like $2,500 a month to $4,800 a month to like $6,800 a month or something like that.")
x('X2p', 2, 7, "Usage is starting to run away from them.")
x('X2q', 2, 8, "AI could be the best thing possible for them, because it enables people to use their product more.")
x('X2r', 2, 8, 'The problem is if Experian comes in and says, "We can give you the source data for half the price." "Fine, I don\'t really care where it comes from."')
x('X2s', 2, 9, "That's an advantage CARFAX has, because they have some integrations with OEMs to pull stickers, and I don't believe AutoCheck does.")
x('X2t', 2, 11, "They already are a data company, but that's where they need to be, is data through API.")
x('X2u', 2, 7, "I think of them as the de facto pathway in to that data.")

x('X3a', 3, 4, "I'd say a majority of BIG's revenue is coming from insurance, and then less than 20% is auto finance.")
x('X3b', 3, 5, "banking and insurance group is going to be less than 40% and then insurance is going to be over 50% of that right now.")
x('X3c', 3, 6, "Just to give you guys an idea, insurance companies will pay anywhere from, I would say, $0.05 up to $0.25 per VIN.")
x('X3d', 3, 6, "It's roughly every year and a half, every 18 months or so, and then 3%-5%, but they're fairly custom.")
x('X3e', 3, 8, "That said, it does seem like AutoCheck is gaining some market share there, and it is mainly due, from my understanding, some dealers are starting to leave because of the price increases.")
x('X3f', 3, 14, "I don't see them losing any market share in the next five years.")
x('X3g', 3, 8, "That's why a lot of them pulled the plug and moved to AutoCheck when CARFAX stood up their used car listings.")
x('X3h', 3, 9, "I don't know how much revenue is generated off listings, but it's a large revenue generator for them.")
x('X3i', 3, 9, "The consumer group's been shrinking a lot over the years, and we can talk through that if you like.")
x('X3j', 3, 9, "I think they charge, it's on their website, like $45 or $50 to go pull your report.")
x('X3k', 3, 10, "AutoCheck has always been an add-on to the credit. Not a huge focus.")
x('X3l', 3, 12, "There's nothing exclusive about it.")
x('X3m', 3, 12, "I don't think it's extremely important.")
x('X3n', 3, 12, "the dealerships and the service shops will pay to be a preferred service center of CARFAX.")
x('X3o', 3, 13, "They charge them for it. It's big bucks.")
x('X3p', 3, 13, "They're doing lien holder. That started in 2023.")

x('X4a', 4, 3, "Mazda, for some reason, bucked the trend, and they partnered with AutoCheck for that program. Everybody else partnered with CARFAX.")
x('X4b', 4, 3, "They are more comfortable with a less robust and less expensive product.")
x('X4c', 4, 5, "The slowdown isn't because the model doesn't work, it's because they've run out of customers.")
x('X4d', 4, 5, "I think they charge $29.99 and then you can have access to that car.")
x('X4e', 4, 6, "You cannot certify a car without that.")
x('X4f', 4, 6, "Every car gets run twice.")
x('X4g', 4, 7, "There would have to be something negative or, I do not know, a 25% price increase.")
x('X4h', 4, 7, "There is precedent with Mazda already using AutoCheck, so there is a clear path for us to divest.")
x('X4i', 4, 7, "you're looking to find a recall because recalls are easy money.")
x('X4j', 4, 8, "If you want unlimited and you are just a one-rooftop store, it might just be like $999.")
x('X4k', 4, 8, "AutoCheck would come in and hit them at $799.")
x('X4l', 4, 9, "it was a couple thousand every quarter or something like that we were paying of that bill.")
x('X4m', 4, 10, "Registration data itself, I know of no other company than Polk.")
x('X4n', 4, 11, "Polk and PIN are the two pillars of sales and marketing for automotive.")
x('X4o', 4, 6, "S&P Global, the parent company, we subscribe to their automotive and global automotive insights, where they talk about trends and hot items that are coming through, whether it is sales, service parts, body shop, electric vehicle trends, hybrid trends, tariff issues, all of that.")
x('X4p', 4, 6, "We also utilize the CARFAX three-year buyback guarantee.")

x('X5a', 5, 2, "In exchange for providing this software and this process, CARFAX got the data from the accident immediately after it happened.")
x('X5b', 5, 4, "We were held hostage by these companies.")
x('X5c', 5, 4, "My best guess would be 20% would be unique, 80% would be common.")
x('X5d', 5, 7, "Very rarely would an insurance or a finance company want a full vehicle history report because they're four, five, six, eight pages long.")
x('X5e', 5, 7, "That was a concession that CARFAX had to make, is only reporting open recalls, because once they received the information that that recall had been addressed, inspected, or whatever, then that open recall record was immediately removed or shut off.")
x('X5f', 5, 9, "The margins in the vehicle history data business are crazy because in most cases, you own the data, you buy the data.")
x('X5g', 5, 10, "The dealers represent 70%-75% of the revenues that CARFAX gets, it's from dealers.")
x('X5h', 5, 10, "CARFAX is unique in getting that data.")
x('X5i', 5, 12, "For fleet, rental and lease, they probably get 70%-80% of the data. For dealer-consigned cars, which represents about 50% of the volume, they don't get that information for dealer-consigned cars directly.")
x('X5j', 5, 13, "Manheim has a deep loyalty and relationship. They actually helped found AutoCheck.")
x('X5k', 5, 15, "A lot of the CARFAX product owners, etc., they don't come from the automotive world.")
x('X5l', 5, 17, "I don't think those discussions ever took place.")
x('X5m', 5, 15, "When CARFAX launched used car listing, initially, it looked like a complete failure because they tried to do it all over, all at once, and you had to build up the inventory, build up the eyeballs, people who wanted to buy it, etc.")
x('X5n', 5, 4, "the estimatics companies are the big leaker of this data, not the insurance companies.")

x('X6a', 6, 2, "probably 40%-50% ask for it at the time of interaction when we're reviewing the car itself.")
x('X6b', 6, 3, "We pay under $5,000 a month.")
x('X6c', 6, 3, "I want to say it's been the same for at least the past two years that I can remember. We haven't had a price increase.")
x('X6d', 6, 3, "That may likely be because we're part of AutoNation.")
x('X6e', 6, 4, "I've used AutoCheck in the past at previous dealerships, and it never lasted long.")
x('X6f', 6, 4, "It's probably about 1/3 of what we're currently paying.")
x('X6g', 6, 5, "Transparently, I really wasn't aware that most of the current sites would be showing that.")
x('X6h', 6, 6, "If we get to that point, CARFAX definitely could be on the chopping block.")
x('X6i', 6, 7, "automotiveMastermind, then you have CARFAX, and then iPacket are three different companies as far as I know it.")
x('X6j', 6, 9, "The truth is I don't really know if it's added much in terms of business with that.")
x('X6k', 6, 10, "Yeah, I would probably get rid of it.")
x('X6l', 6, 10, "This month alone, it would have been 78 CARFAX listings, 60 CarGurus.")
x('X6m', 6, 11, "It's the highest volume of leads, but it's one of the lowest, if not the lowest, closing percentage of leads.")
x('X6n', 6, 11, "It's 4.29, CARFAX 1.98, CarGurus 4.54, Cars.com 3.55, Edmunds 1.88, and TrueCar 1.08.")
x('X6o', 6, 12, "No, none of our vendors have brought it up recently.")
x('X6p', 6, 13, "When it first came to the store, I want to call it six months ago, there was no real game plan.")
x('X6q', 6, 11, "I'm wondering if people are bouncing basically over to the CARFAX site to get the free listing.")

x('X7a', 7, 0, "Edmunds has a 30-day out program, so they have to give you a 30-day notice.")
x('X8a', 8, 2, "It also has built-in extensions with ALLDATA, CARFAX, and other systems like that we can go in and use and pull information from.")

x('X9a', 9, 11, "The dealers could pay twice what they're paying and would still be getting a great deal on the CARFAX vehicle history report product.")
x('X9b', 9, 11, "we could eventually out-SEO CarGurus. I don't think it's happened yet.")
x('X9c', 9, 10, "AutoCheck has something like a 10% market share with new car dealers and a 25% market share with used car dealers.")
x('X9d', 9, 11, "We knew we couldn't price as high as we felt like it was worth, and so we did a lot of intro pricing, try it free for 30 days kind of thing, and then just set up in the backend.")
x('X9e', 9, 13, "That's kind of their next growth area.")

# ---- primary-document quotes (verbatim, <=2 sentences) ----
d('D16a', 'INFO16', 80, "The complaint alleges, among other things, that, in violation of antitrust laws, CARFAX entered into exclusive arrangements regarding the sale of CARFAX vehicle history reports with certain auto manufacturers and owners of two websites providing classified listings of used autos and light trucks.")
d('D16b', 'INFO16', 80, "On October 25, 2013, the plaintiffs served a second amended complaint with similar allegations purporting to name approximately 469 auto dealers as plaintiffs, and counsel for plaintiffs indicated that there may be additional claimants.")
d('D16c', 'INFO16', 80, "On September 30, 2016, the District Court granted CARFAX's motion for summary judgment, dismissing all claims in the complaint. The plaintiffs filed their notice of appeal on October 28, 2016.")
d('D17a', 'INFO17', 79, "The court has stayed the case pending the outcome of the appeal of the first case described above.")
d('A263a', '10A', 263, "CARFAX has established and continues to expand a superior data estate comprised of more than 38 billion vehicle history records from more than 177,000 sources through symbiotic data partnerships with automotive industry participants including more than 92,000 dealers and service shops, 6,300 police agencies and 36 OEMs as of December 31, 2025.")
d('A263b', '10A', 263, "Advantage: A dealer subscription product that provides CARFAX Vehicle History Reports and related insights (e.g., accident, service/maintenance, ownership, valuations and recalls) that dealers use to acquire the right inventory, price accurately with history-based valuation and build buyer confidence at point of sale.")
d('A263c', '10A', 263, "Every vehicle listing includes a free CARFAX report, history-based value and verified reviews.")
d('A263d', '10A', 263, "CARFAX For Life: A dealer subscription product that drives service retention and loyalty by providing their customers with access to CARFAX Car Care.")
d('A263e', '10A', 263, 'Banking & Insurance Group ("BIG"): Our data and analytics products for lenders and insurers that customers integrate into their workflows.')
d('A264a', '10A', 264, 'automotiveMastermind: A specialized sales and marketing platform for automotive dealers and OEM programs utilizing advanced predictive analytics and proprietary "Behavior Prediction Scores" ("BPS").')
d('A264b', '10A', 264, "The data is used daily across OEMs from product planners to sales operations.")
d('A264c', '10A', 264, "As of December 31, 2025, approximately 10,500 dealerships utilized this pricing engine which integrates with major dealer software providers and online shopping marketplaces.")
d('A265a', '10A', 265, "Key differentiators include a daily-updated VIN database with over 13 billion vehicle owner records as of December 31, 2025, vehicle filtering to exclude non-service vehicles, and comprehensive analytics for campaign effectiveness.")
d('A265b', '10A', 265, "Built by a 195-expert global analyst team and powered by AI-enabled forecasting systems, coverage includes over 145 sales country markets, over 85,000 vehicle variants, approximately 990 production plants across over 50 countries, and over 2,900 supplier plant locations across more than 80 countries as of December 31, 2025.")
d('A296a', '10A', 296, "While we have experienced data quality issues, to date none of these issues have had a material impact on our operations or financial results.")
d('A297a', '10A', 297, "Our competitors are deploying AI in ways that could materially reduce demand for our products and services (for example, by deploying AI in ways that make collection and processing of information relatively inexpensive or free or by leveraging AI to build products and services that compete with our products and services).")
d('A298a', '10A', 298, "Third parties could also use our data with AI tools to create their own insights and potentially supplant our products and services.")
d('A298b', '10A', 298, "We are likely to continue to modify our pricing models for both existing and new products and solutions so that our prices for our offerings reflect the value those offerings are providing to customers.")
d('A299a', '10A', 299, "Additionally, competing products from internet search engine providers, such as those that provide dealer and vehicle pricing and other information directly in search results or decreases in customer use of search engines, for example, as a result of the continued development of AI technology, could also adversely impact traffic to our websites.")
d('A299b', '10A', 299, "As of December 31, 2025, we derived approximately 60% and 10% of our revenue from our dealership and OEM customer groups, respectively. Our contracts with dealers and OEMs do not contain contractual obligations requiring them to maintain its relationship with us beyond the initial term.")
d('A300a', '10A', 300, "Specifically, for CARFAX, we are investing in consumer brand advertising to raise unaided awareness, drive more direct traffic and high quality leads to Car Listings, and expand the Car Care audience.")
d('A301a', '10A', 301, "If such agreements are not sufficiently robust or enforceable, or if counterparties fail to honor them, we would not be able to maintain the exclusivity of our data sets and the competitiveness of our products and solutions may decrease.")
d('A301b', '10A', 301, "Outside of the U.S., we are more likely to compete against vendors that may differentiate themselves based on local advantages in language, market knowledge, existing relationships with customers and content applicable to that jurisdiction.")
d('A302a', '10A', 302, "Further, relationships with our partners with whom we currently have a cooperative relationship could shift over time, as we, or they, develop products and solutions that compete with each other.")
d('A302b', '10A', 302, "Our business also depends on access to our vast network of data providers, and the costs of access to data have increased and may continue to increase.")
d('A303a', '10A', 303, "We believe CARFAX Europe is poised to expand its presence by entering new, high-potential markets such as Germany and France.")
d('A304a', '10A', 304, "Some of our suppliers are also our competitors, and from time to time they negotiate to change the terms of the data and services that they supply to us in order to gain an advantage in the marketplace, which could materially harm our business.")
d('A304b', '10A', 304, "In addition, the consolidation of our third-party data suppliers has reduced the number of firms we partner with, which has impacted the size of our third-party data supplier base for certain products and solutions and resulted in an increase in fees charged by certain of our third-party data supplier partners.")
d('A340a', '10A', 340, "Segment revenue is primarily driven by the number of dealer locations enrolled in dealer subscription products (Advantage, Car Listings, and CARFAX For Life), the average monthly price per location on each product, and the number of BIG customers and their average monthly price per customer.")
d('A340b', '10A', 340, "Strong consumer recognition also reinforces credibility with dealers and supports pricing power and retention across our product suite.")
d('A341a', '10A', 341, "Examples include CARFAX dealer products (Advantage vehicle history, Car Listings, CARFAX For Life), BIG minimums with usage tiers, B2B Marketing & Sales solutions (automotiveMastermind, Market Reporting, Market Scan API priced by dealer rooftops) and Planning Solutions (vehicle & supply chain forecasting, powertrain and technology, global reporting).")
d('A380a', '10A', 380, "CARFAX operates a consumer-pull, dealer-monetization model by first building trust and demand with consumers.")
d('A380b', '10A', 380, "OEM CPO relationships and marketplace/dealer management system integrations deepen adoption and the Lifetime Dealer initiative bundles Advantage, Car Listings and CARFAX For Life, leverages OEM co-op funds (marketing funds reimbursing dealers' approved advertising expenses) and creates clear upsell paths such as Premium Listings and Sell My Car.")
d('A380c', '10A', 380, "Internationally, CARFAX leads with a consumer-first strategy (e.g., in Spain, Italy, Poland and expansion in Canada).")
d('A381a', '10A', 381, "We believe this approach is successful because our core market reporting datasets covering registration, ownership and loyalty are widely regarded as the 'gold standard' in the industry.")
d('A381b', '10A', 381, "We believe Planning Solutions is the industry benchmark for analytics and reference data.")
d('A381c', '10A', 381, "This extensive network of more than 177,000 diversified data sources as of December 31, 2025 provides access to incident and service data, often on an exclusive basis, forming a highly difficult-to-replicate ecosystem.")
d('A382a', '10A', 382, "More recently, AI has been deployed to ingest previously challenging information, such as converting PDF content into data or analyzing vehicle images to assess accident damage.")
d('A382b', '10A', 382, "Our competitors include: (i) automotive data and analytics providers, such as J.D. Power and Cox Automotive; (ii) data and information providers, such as Experian and Global Data; (iii) business intelligence and consulting firms who offer automotive industry expertise and provide strategic advice; and (iv) smaller niche players who may focus on specific segments of the automotive value chain.")
d('Q27a', '10Q', 27, "Revenue increased $29 million in the three months ended June 30, 2026 as compared to the three months ended June 30, 2025, and increased $64 million in the six months ended June 30, 2026 as compared to the six months ended June 30, 2025, primarily attributable to an increase in subscription revenue, driven primarily by price increases of approximately $16 million and $36 million, respectively, and continued new business growth of approximately $8 million and $20 million, respectively.")
d('Q28a', '10Q', 28, "Revenue increased $23 million in the three months ended June 30, 2026 as compared to the three months ended June 30, 2025, and increased $46 million in the six months ended June 30, 2026 as compared to the six months ended June 30, 2025, primarily attributable to an increase in subscription revenue, which was primarily driven by price increases.")
d('Q29a', '10Q', 29, "Revenue increased $6 million in the three months ended June 30, 2026 as compared to the three months ended June 30, 2025, and increased $18 million in the six months ended June 30, 2026 as compared to the six months ended June 30, 2025, primarily attributable to an increase in subscription revenue, which was primarily due to continued new business growth.")


def cite(qid):
    q = Q[qid]
    if q['kind'] == 'X':
        date, role = CALLS[q['src']][:2]
        pg = f", p.{q['page']}" if q['page'] else ''
        return f"[X, call #{q['src']}, {date}, {role}{pg}]"
    sec = {'INFO16': '', 'INFO17': ''}.get(q['src'], '')
    return f"[D, {DOCS[q['src']]} p.{q['page']}{sec}]"


# ---------------------------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------------------------
def load_seg():
    v = {}
    for r in csv.DictReader(open(f'{W}/canonical/segment_pl.csv')):
        v[(r['concept'], r['segment'], r['period'])] = float(r['value'])
    return v


def load_deck():
    out = {}
    for r in csv.DictReader(open(f'{W}/extraction/presentations.csv')):
        if r['source_doc'].startswith('InvDay') and r['page'] in ('10', '34', '57') and r['unit'] == 'pct':
            out[(r['page'], r['line_item'])] = float(r['value'])
    return out


SEG = load_seg(); DECK = load_deck()
PER = ['FY2023', 'FY2024', 'FY2025', '6M-2025', '6M-2026']
PLAB = ['FY23', 'FY24', 'FY25', '6M-25', '6M-26']


def g(c, s, p):
    return SEG.get((c, s, p))


def fm(v):
    return '—' if v is None else (f'({abs(v):,.0f})' if v < 0 else f'{v:,.0f}')


def pc(v):
    return '—' if v is None else f'{v * 100:.1f}%'


def growth(c, s, p):
    prev = {'FY2024': 'FY2023', 'FY2025': 'FY2024', '6M-2026': '6M-2025'}.get(p)
    if not prev or not g(c, s, prev):
        return None
    return g(c, s, p) / g(c, s, prev) - 1


def seg_rows():
    rows = []
    for s, lab in (('CARFAX', 'CARFAX'), ('B2B', 'B2B')):
        rows.append([f'**{lab}** revenue [D]'] + [fm(g('rev', s, p)) for p in PER])
        rows.append(['  growth y/y [C]'] + [pc(growth('rev', s, p)) for p in PER])
        rows.append(['  Adj. EBITDA [D]'] + [fm(g('adj', s, p)) for p in PER])
        rows.append(['  Adj. EBITDA margin [C]'] + [pc(g('adj', s, p) / g('rev', s, p)) for p in PER])
        rows.append(['  subscription share [C]'] + [pc(g('sub', s, p) / g('rev', s, p)) for p in PER])
        rows.append(['  international share [C]'] + [pc(g('intl', s, p) / g('rev', s, p)) for p in PER])
    rows.append(['**Corporate** Adj. EBITDA [D]'] + [fm(g('adj', 'Corporate', p)) for p in PER])
    rows.append(['**Total** revenue [D]'] + [fm(g('rev', 'Total', p)) for p in PER])
    rows.append(['  Adj. EBITDA [D] / margin [C]'] + [f"{fm(g('adj', 'Total', p))} / {pc(g('adj', 'Total', p) / g('rev', 'Total', p))}" for p in PER])
    rows.append(['  CARFAX share of revenue [C]'] + [pc(g('rev', 'CARFAX', p) / g('rev', 'Total', p)) for p in PER])
    return rows


CFX25 = g('rev', 'CARFAX', 'FY2025'); B2B25 = g('rev', 'B2B', 'FY2025')
MIX = {k: DECK[('57', f'CARFAX REVENUE BY PRODUCT & INTERNATIONAL - {k}')] for k in ('Advantage', 'Listings', 'Financial / Consumer / Other', 'International')}
MS = DECK[('34', 'B2B REVENUE BY BUSINESS LINE - Marketing & Sales')]; SP = DECK[('34', 'B2B REVENUE BY BUSINESS LINE - Strategy & Planning')]
CUST = {k: DECK[('10', f'REVENUE BY CUSTOMER TYPE - {k}')] for k in ('Dealer ( B2B & CARFAX )', 'OEM & Supplier', 'Financial / Consumer / Other')}


def usd(pct, base):
    return f'~${pct / 100 * base:,.0f}m'


# ---------------------------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------------------------
BOTTOM_LINE = (
    f"Mobility Global is two businesses with different economics. **CARFAX** ({pc(CFX25 / g('rev', 'Total', 'FY2025'))} of FY25 revenue; "
    f"Adj. EBITDA margin {pc(g('adj', 'CARFAX', 'FY2025') / CFX25)}) grew 8–12% a year in FY24–6M-26, and the 10-Q says that growth is \"primarily driven by price increases\". "
    f"**B2B** ({pc(B2B25 / g('rev', 'Total', 'FY2025'))}; margin {pc(g('adj', 'B2B', 'FY2025') / B2B25)}) grows 3–6%, mostly from new business [D/C]. "
    "The primary documents and the experts agree on what CARFAX sells: a dealer-paid report that consumers ask for by name. "
    "The experts add four things the filings do not say. Dealer penetration is close to complete. "
    "List price increases of \"up to 5%-8%\" fall mainly on smaller dealers, and one large-group store has been flat for two years. "
    "AutoCheck is 20–67% cheaper. And the marketplaces that once showed CARFAX exclusively, the conduct challenged and cleared in Maxon v. CARFAX (2013–18), have moved to AutoCheck since CARFAX became their listings rival. "
    "The courts treated CARFAX's lead as consumer preference, not contractual foreclosure. "
    "The 2026 evidence still fits that view for Advantage, but not for Listings: at the one dealer that measured it, Listings brings the most leads and converts them at 1.98%. "
    "The thinnest evidence is on B2B Strategy & Planning, International and AI, where no expert speaks with first-hand authority."
)

SOURCE_NOTE = [
    "**\"Direct documents\".** Quotes come from the primary texts themselves, not from our summaries: the nine AlphaSense expert-call transcripts (read in full; the AI-generated \"Smart Summary\" is ignored because it overstates the transcript at least eight times, per analysis/X_expert_calls.md §1b), the Mobility Global Form 10/A and Q2-2026 10-Q, and the IHS Markit FY2016/FY2017 10-K litigation notes (Quartr page text). Every quote is verbatim, at most two sentences, and was checked by script against its source (Appendix).",
    "**Court opinions were not retrieved.** Court websites are blocked by network policy. The court history is therefore given \"as reported in secondary coverage (court opinion not retrieved)\", from research_notes/CARFAX challengers beyond AutoCheck/us_platforms_and_antitrust.md §5 and the challengers report. Only the 10-K litigation notes are primary.",
    "**Expert-call limits.** Nine calls come from eight people; #1 and #3 are the same person and count once. Of the six who speak substantively about CARFAX, four are ex-CARFAX staff (#1/#3, #4, #5, #9), and their knowledge ends between 2018 and January 2024. The core calls ran June–September 2026. #7 (Jan 2026) and #8 (Sep 2025) are peripheral, and #9 (Feb 2021) is a baseline. Only #6, a single AutoNation luxury store, post-dates the 7 Aug 2026 guidance cut. Expert numbers are unaudited and do not change any [D] figure.",
    "**Tags.** [D] filing text or figure · [C] our computation from [D] · [D-deck] Investor Day deck, 12 May 2026 (Quartr 3352878), unaudited · [IR] management on a call · [X] expert call, third-party, unaudited. **Inference:** marks our judgement. **Archive check** compares the evidence with earlier work files (validates / updates / contradicts).",
]

# Segment description table
SEG_DESC = [
    ['**CARFAX**', 'Advantage (dealer vehicle-history reports); Car Listings; CARFAX For Life (service loyalty, Car Care); Banking & Insurance Group (BIG); consumer pay-per-report; Canada and Europe',
     '40,000+ dealer customers; consumers (53m+ Car Care users); lenders and insurers (17 of top 20) [D, 10/A p.263, 380]',
     f"FY25 ${CFX25:,.0f}m. Mix [D-deck, slide 57]: Advantage {MIX['Advantage']:.0f}% ({usd(MIX['Advantage'], CFX25)} [C]), Financial/Consumer/Other {MIX['Financial / Consumer / Other']:.0f}% ({usd(MIX['Financial / Consumer / Other'], CFX25)}), Listings {MIX['Listings']:.0f}% ({usd(MIX['Listings'], CFX25)}), International {MIX['International']:.0f}% (sums to 101%)",
     'Price: "primarily driven by price increases" [D, 10-Q p.28]'],
    ['**B2B – Marketing & Sales**', 'automotiveMastermind; Polk Auto Marketing Solutions (market reporting, audiences, measurement); Market Scan; Data Studio; VIN Solutions; Recall',
     'OEMs, dealers (11k US dealers use B2B [D-deck]), lenders, media platforms, DMVs, insurers',
     f"{MS:.0f}% of B2B ({usd(MS, B2B25)} [D-deck, slide 34 / C])", 'B2B: "primarily due to continued new business growth" [D, 10-Q p.29]'],
    ['**B2B – Strategy & Planning**', 'Vehicle & Supply Chain Forecasting; Global Reporting; FAST; PIQ; ~25% stake in Digital Automotive',
     '100% of top-40 carmakers, 94% of top-100 suppliers, 100% of top-10 investment banks [D, 10/A p.265]',
     f"{SP:.0f}% of B2B ({usd(SP, B2B25)} [D-deck / C])", 'Not split from B2B in filings'],
    ['**Corporate**', 'Unallocated costs (stand-alone public-company functions)', '—', f"Adj. EBITDA −${abs(g('adj', 'Corporate', 'FY2025')):,.0f}m FY25 [D]", '—'],
]

MONEY = [
    "**CARFAX dealer products** are monthly subscriptions per location. The filing names the drivers:",
    ('Q', 'A340a'),
    "**BIG** sells data fields to lenders and insurers on one-year contracts with monthly minimums, billed per VIN [X, #3]; the filing's phrase is \"BIG minimums with usage tiers\" [D, 10/A p.341]. **Consumer reports** are pay-per-report and transactional.",
    "**B2B** is 82–83% subscription: OEM and dealer-group enterprise agreements, dealer-rooftop APIs (Market Scan) and planning datasets, plus transactional campaigns, VIN pulls and Recall outreach [D, 10/A p.341].",
    "**Price versus volume.** The only quantified split in any filing:",
    ('Q', 'Q27a'),
    f"Price was therefore about 56% of 6M-26 revenue growth ($36m of $64m) [C]. Customer types [D-deck, slide 10]: dealers {CUST['Dealer ( B2B & CARFAX )']:.0f}%, OEMs & suppliers {CUST['OEM & Supplier']:.0f}%, financial/consumer/other {CUST['Financial / Consumer / Other']:.0f}%. The 10/A gives dealers ~60% and OEMs ~10% [D, 10/A p.299].",
]

# Product sections: (letter, title, intro, quotes, assessment, archive[list])
PRODUCTS = [
    ('a', 'CARFAX dealer vehicle-history subscriptions (Advantage)',
     f"Advantage is ~{MIX['Advantage']:.0f}% of CARFAX revenue [D-deck], about {usd(MIX['Advantage'], CFX25)} in FY25 [C].",
     ['A263b', 'Q28a', 'X1a', 'X4c', 'X1b', 'X1c', 'X6c', 'X1e', 'X4j', 'X1l', 'X4k', 'X6f', 'X6e', 'X3e', 'X3f'],
     "Penetration is effectively complete, so growth is price on a base that \"rarely\" cancels. "
     "But price realisation is uneven: list increases land hardest on small groups, while a large-group store reports two flat years. "
     "AutoCheck's discount is wide (20–67%), yet the switching evidence is anecdotal and runs both ways. The same person (#1/#3) says AutoCheck is \"gaining\" and that CARFAX will lose no share.",
     ["**Validates** analysis/D7_pricing.md §1: the 10-Q puts price at ~56% of 6M-26 growth. Also validates X_expert_calls.md §3 rows 1–2.",
      "**Updates** D7 §3, which assumes price applies across the base. The experts split it by cohort: small groups ~8%, large groups 4–5% or flat [X, #1, #6].",
      "**Validates** D2_unit_economics.md (a), dealer spend ≤$2.4k/month [C]. The experts give $999 for a single rooftop and under $5,000 for a three-product bundle."]),
    ('b', 'Consumer reports and brand demand',
     "No consumer-report revenue is disclosed. It sits inside CARFAX non-subscription revenue ($215m in FY25) together with BIG transactional revenue [D, 10/A p.355].",
     ['A380a', 'A300a', 'X2f', 'X6a', 'X3i', 'X3j', 'X4d', 'X1f'],
     "Consumer reports are a small, transactional line that one insider calls shrinking. Their economic job is to create the demand that dealers pay for. "
     "The evidence for brand pull is strong but qualitative, and the two price points conflict ($45–50 against $29.99). "
     "No expert was asked whether AI answer engines divert report traffic, although the 10/A flags it (§k).",
     ["**Validates** D1_moat.md §2 row 2: 96% in-market awareness and 28m+ report views a month [D].",
      "**Resolves** the price conflict toward #3: the challengers report cites a $44.99 CARFAX report (via VinAudit's comparison). #4's $29.99 is likely stale.",
      "**Gap:** consumer revenue and volume remain undisclosed (D2 (b))."]),
    ('c', 'OEM certified pre-owned (CPO) programs',
     "36 OEM CPO programs contribute data and mandate the report [D, 10/A p.263]. The 2013 complaint targeted exactly these arrangements (§d).",
     ['A380b', 'X4e', 'X4f', 'X4p', 'X4a', 'X4h', 'X4g', 'X4l', 'X4b'],
     "CPO is a distribution mandate more than a revenue line. The OEM's own bill is small, and the value accrues through dealer subscriptions and the buyback guarantee. "
     "Mazda shows that exit is feasible. The trigger an OEM manager names is a breach or about a 25% price increase, which is well above current increases.",
     ["**Validates** D1_moat.md §2 row 3 (36 CPO mandates; \"will not certify a car without a CARFAX report\" [IR]).",
      "**Consistent with the court record** (secondary coverage): the district court found the CPO agreements short-term or terminable. #4 likewise says the system is not \"super difficult to de-link\".",
      "**Gap:** no brand-by-brand CPO list and no CPO revenue."]),
    ('d', 'CARFAX Listings and marketplace relationships',
     f"Listings is ~{MIX['Listings']:.0f}% of CARFAX revenue ({usd(MIX['Listings'], CFX25)} [D-deck/C]). It is the product that turned the marketplaces from distribution partners into competitors.",
     ['D16a', 'A263c', 'A302a', 'X3g', 'X2c', 'X2e', 'X2d', 'X6g', 'X6o', 'X6l', 'X6m', 'X6n', 'X6q', 'X9b', 'X9d'],
     "There are two separate effects. "
     "(1) **Distribution.** The marketplaces' exit removes the channel the 2013 plaintiffs called decisive (they alleged 75% foreclosure). In 2026 dealer sites and carfax.com carry the report, and the post-switch dealer had not noticed the change. "
     "(2) **Listings economics.** High lead volume with a low close rate suggests that many leads are report-seekers, so Listings revenue is at risk when contracts renew. A GM would cut Listings and For Life before Advantage [X, #6, p.12]. All lead data comes from one store.",
     ["**Validates** reports/CARFAX challengers beyond AutoCheck.md (\"Marketplaces, not startups, were the real challenge\") and D13 §3 (\"the newest of the four\" [IR]).",
      "**Updates** D2 (a) Listings: lead quality is a new risk (X_expert_calls.md §3 row 12).",
      "**Unresolved:** whether Cox's arrangement is exclusive. The June 2025 press release says \"co-brand\", while #2 says \"AutoCheck only\" second-hand (X row 10).",
      "**Contradicted on dating:** #3 dates the marketplace exits to the Listings launch \"six or seven years ago\". The archive's dated sources (dual-provider opening in 2013–14, exits in 2025–26) stand."]),
    ('e', 'Car Care, the service-shop data network, and CARFAX For Life',
     "92,000+ dealers and service shops contribute records, and Car Care has 53m+ users [D, 10/A p.263].",
     ['A263d', 'X1h', 'X1i', 'X8a', 'X5h', 'X3n', 'X3o', 'X9e', 'X6j', 'X6k'],
     "The service network is the core data asset: it supplies the odometer and service records that AutoCheck lacks. "
     "It runs on a give-get exchange, not on payment. "
     "Dealer monetisation through For Life is contested: one GM barely uses it and would cut it first. White-label Car Care sold to dealer groups and insurers (\"big bucks\") is unquantified.",
     ["**Contradicts** D6 §1 (+19pt service retention [IR]), with n=1 (X row 20).",
      "**Validates** D2 (a): the Lifetime bundle went back to à-la-carte selling in June 2026, and fewer than half of franchise Advantage dealers take Service Loyalty [IR].",
      "**Validates** D1 §2 row 1 (give-get network) [D]."]),
    ('f', 'Banking & Insurance Group (lenders, insurers)',
     "BIG is not split out. It sits in \"Financial/Consumer/Other\", " + f"{MIX['Financial / Consumer / Other']:.0f}% of CARFAX ({usd(MIX['Financial / Consumer / Other'], CFX25)} [D-deck/C]).",
     ['A263e', 'X3a', 'X3b', 'X3c', 'X5d', 'X1n', 'X1o', 'X1m', 'X3k', 'X3d', 'X1p', 'X3p'],
     "Insurance underwriting is the one place where experts see new-customer growth: about half of insurers are live, with a 2–3-year onboarding queue. "
     "Lending is a commodity split ~50/50 with AutoCheck. "
     "This rests on one person (#1/#3), whose knowledge ends in January 2024. "
     "Inference: insurance revenue is probably ~$100–150m (BIG <40% of ~$1bn, insurance >50% of BIG).",
     ["**Contradicts (weakly)** D9 §2.7: the underwriting-volume tailwind fell from +$17m to +$13m to +$2m [D, 10/A p.347–350]. Reconciliation: the filing measures volume from existing insurers, while the expert describes new insurers onboarding (X row 16).",
      "**Validates** D7 §2 (\"BIG minimums with usage tiers\" [D]) and adds a cadence: 3–5% every ~18 months [X, #3]."]),
    ('g', 'Data sources and the quality of accident and collision data',
     "The filing calls the network \"often\" exclusive and hedges that exclusivity is contractual.",
     ['A263a', 'A381c', 'A301a', 'X1g', 'X5a', 'X5c', 'X5b', 'X3l', 'X5i', 'X5j', 'X2b', 'A296a', 'A304a', 'X1j', 'X1k'],
     "The proprietary core is narrower than \"often exclusive\" suggests. It consists of police reports (by contract) and service and odometer records (by give-get). Collision data is mostly common, and dealer-consigned auction data sits with AutoCheck. "
     "Rebuilding the core is uneconomic rather than impossible: rivals have \"no data\" to offer in exchange. "
     "Accident-severity accuracy is a reputational exposure and a buyback-guarantee exposure that the filing does not size.",
     ["**Validates** D1 §2 row 1 and management's \"It's a mix\" [IR]. Adds the first split: ~20% of collision data unique (X row 7).",
      "**Validates** D11 #8 (data-supply squeeze): the filing's own supplier-consolidation language matches #5's \"held hostage\" (X row 25).",
      "**New:** accident-severity misgrading appears only in the expert evidence (X §4 risk 5)."]),
    ('h', 'International (Canada / CARPROOF, Europe / Germany)',
     f"CARFAX international revenue was ${g('intl', 'CARFAX', 'FY2025'):,.0f}m in FY25 ({pc(g('intl', 'CARFAX', 'FY2025') / CFX25)} of segment). In 6M-26 it grew {pc(growth('intl', 'CARFAX', '6M-2026'))}, against {pc(growth('us', 'CARFAX', '6M-2026'))} in the U.S. [D/C]. "
     "Canada came from the CARPROOF acquisition (Dec 2015, ~$459.2m net of cash) [D, IHS Markit FY2016 10-K p.60–61, via research_notes/.../primary_sources.md].",
     ['A380c', 'A303a', 'A301b', 'X1q'],
     "Only one expert comments on International, and only in passing (\"sideshow\"). No expert covers Canada or Germany first-hand. "
     "The filing's own risk language (local rivals, restricted data) matches that view. Evidence gap.",
     ["**Validates** D11 #11 (International an opaque drag) and X row 23.",
      "**Context from the challengers report:** CARFAX launched in Germany on 1 Jul 2026 with mobile.de. carVertical reported €75.8m of revenue in 2025 (company-sourced), probably larger than CARFAX Europe, which is undisclosed."]),
    ('i', 'B2B Marketing & Sales: automotiveMastermind, Polk audiences, Market Scan, Recall',
     None,
     ['A264a', 'X2k', 'X2l', 'X6p', 'X6i', 'X5l', 'A381a', 'A264b', 'X2m', 'X4m', 'X4n', 'X2n', 'A264c', 'A265a', 'X5e'],
     "Polk registration data has the strongest corroboration in the whole record: two independent users know no alternative. "
     "automotiveMastermind is respected, but its adoption appears to stall at around 7–8k dealers, and selling it takes in-store effort. "
     "Separate sales forces confirm cross-sell friction. No expert speaks to Market Scan or Data Studio. "
     "Recall's value lies in dealer service revenue, which is limited because only open recalls are shown.",
     ["**Updates** D1 §3, which called the Polk moat \"medium\" with a low-cost substitute. Per the challengers report, management's \"low-cost alternative\" referred to planning, not Polk, and the experts support that correction (X row 15).",
      "**Validates** D11 #2/#4 (cross-sell friction) and D6 §2 (X row 14). D2 records aM at 3,200 dealers [IR]."]),
    ('j', 'B2B Strategy & Planning: forecasting and registration data',
     None,
     ['A381b', 'A265b', 'X4o'],
     "There is effectively no independent evidence here: one OEM user confirms the subscription and nothing more. "
     "At the Investor Day, management conceded a \"low-cost alternative\" on the planning side [IR] (primary_sources.md Q3). Evidence gap. Treat the 26% of B2B (~$158m) as unexamined.",
     ["**Validates** the challengers report correction: the low-cost competitor sits in Planning.",
      "**Gap:** no expert on GlobalData/LMC, S&P Global (the former parent, now a licensor), or forecasting churn."]),
    ('k', 'AI-related product use',
     None,
     ['A382a', 'X2o', 'X2p', 'X2q', 'X2t', 'X2r', 'X2h', 'X2g', 'A297a', 'A298a', 'A299a'],
     "The only product-level AI evidence is about usage. Automated appraisals multiply report pulls on old, uncapped contracts, so re-tiering is upside if CARFAX prices it and a churn trigger toward cheaper source data if it does not. "
     "It rests on one competitor alumnus's anecdotes. "
     "The filing's search and answer-engine traffic risk is untested by any expert.",
     ["**Updates** D13 §6: no analyst in 68 events asked about AI assistants, and no expert addressed them either.",
      "**Updates** D7 §3: AI monetisation is unquantified [IR]. The experts suggest some of what reads as \"price\" may be usage true-ups (X §4 risk 1)."]),
]

COURT_FACTS = [
    "**Case.** Maxon Hyundai Mazda et al. v. CARFAX, Inc., S.D.N.Y. No. 1:13-cv-02680-AJN (Judge Alison J. Nathan). About 120 dealers filed in April 2013, seeking $50m+ trebled. The second amended complaint (Oct 2013) named ~469 dealers [D, 10-K].",
    "**Allegations (Sherman Act §§1–2).** Exclusive deals with Autotrader.com, Cars.com and OEM CPO programs foreclosed AutoCheck. The complaint alleged that CARFAX held ~90% share and AutoCheck ~10%, that the website deals foreclosed 75% of franchised-dealer used vehicles (Autotrader alone 53% of independent-dealer vehicles), and that CPO cars were 36% of reports sold. These are allegations, not findings.",
    "**29 Sep 2014.** The motion to dismiss was largely denied. The parties then agreed that summary judgment on foreclosure alone would decide the case.",
    "**30 Sep 2016.** Summary judgment for CARFAX [D, 10-K]. As reported by CARFAX's economic consultant: the CPO agreements were short-term or terminable; AutoCheck could reach consumers through other channels; and the plaintiffs' foreclosure estimate was unreliable.",
    "**1 Jun 2018.** The Second Circuit affirmed by summary order (No. 16-3717-cv, 726 F. App'x 66). It held that plaintiffs bear the burden of showing foreclosure.",
    "**13 Jan 2017.** A follow-on suit was stayed pending the appeal [D, FY2017 10-K]. Its final disposition was not found, and no FTC or DOJ action was found. Autotrader (Sep 2013) and Cars.com (Jan 2014) had opened to AutoCheck while the suit was pending.",
]

COURTS_VS_EXPERTS = [
    ['Did marketplace exclusives foreclose AutoCheck?', 'No: AutoCheck could reach consumers through other channels.', 'The marketplaces now carry AutoCheck; it was "more of like an industry statement" [#2]; the post-switch GM had not noticed [#6].'],
    ['Did CPO exclusivity lock OEMs in?', 'No: the agreements were short-term or terminable.', 'Every OEM but Mazda still mandates CARFAX; there is "a clear path for us to divest" [#4].'],
    ['Where does dominance come from?', 'Implicitly consumer preference: some dealers that preferred AutoCheck stayed with CARFAX (per appellate commentary).', '98% would name CARFAX [#2]; 40–50% ask for it in person [#6]; AutoCheck "never lasted long" [#6].'],
    ['Where is the lock-in now?', 'Not addressed.', 'Workflow embedding: vAuto (~75% of franchise dealers) still carries CARFAX [#2]; give-get data; brand.'],
]

PRICING_TABLE = [
    ['Doctrine', 'Value-based pricing [D, 10/A p.298]; brand "supports pricing power" [D, 10/A p.340]', 'A new feature precedes each increase [#1, #3]'],
    ['Realised price', 'Price $36m of $64m 6M-26 growth (~56%) [D/C, 10-Q p.27]', 'Small groups ~8%, large groups 4–5% [#1]; AutoNation store flat 2+ yrs [#6]'],
    ['Headroom', 'Not disclosed', '"another 12%-15%" [#1]; OEM trigger ~25% [#4]; 2021: "could pay twice" [#9]'],
    ['Discount gap', 'Not disclosed', 'AutoCheck ½ [#1], −20% [#4], ⅓ of CARFAX price [#6]'],
    ['Usage', 'BIG "minimums with usage tiers" [D, 10/A p.341]', 'Dealer bills doubled or tripled after AI-driven pulls [#2]'],
    ['BIG', 'Not disclosed', '3–5% every ~18 months; insurance moving to 5–8% [#3]'],
]

EXPERT_ONLY_RISKS = [
    ('vAuto dependence.', ['X2i', 'X2j'], "If Cox broke the integration, the cost would exceed that of the Autotrader switch. The filing names Cox only as a competitor [D, 10/A p.382]."),
    ('Only ~20% of collision data is unique.', ['X5c'], "The filing's \"often on an exclusive basis\" [D, 10/A p.381] covers police and service data more than collision."),
    ('Accident-severity misgrading.', ['X2b'], "This bears on the three-year buyback guarantee [X, #4] and on the filing's data-quality risk [D, 10/A p.296]."),
    ('AI usage true-ups.', ['X2p'], "This could be upside or a churn trigger. No filing quantifies agent or API pricing."),
    ('Listings lead quality.', ['X6m'], "One store's data, but it is the only lead-to-sale figure in the record."),
    ('Auction data and Manheim.', ['X5j'], "AutoCheck holds dealer-consigned auction data (~50% of volume) [X, #5]. Unverified."),
    ('Organisation.', ['X5k'], "Silos and separate sales forces [X, #5, #6] sit behind the 2026 bundle reversal [IR, per D2]."),
]

QUESTIONS = [
    "**Price by cohort.** What share of CARFAX dealer locations are on flat multi-year group agreements? What was the 2026 price increase for independents and small groups against large groups? (Experts: ~8% for small groups against flat or 4–5% for large groups [#1, #6].)",
    "**Usage re-tiering.** How many dealer contracts were re-tiered for automated or AI-driven report pulls in 2025–26? What revenue did that add, what churn followed, and what is the agent/API price list? [#2]",
    "**Listings after the marketplace switch.** What are Listings' lead-to-sale rates against the marketplaces since the 2025–26 AutoCheck switches? What share of Listings leads start from a report view? [#6: 1.98% close rate]",
    "**vAuto.** What are the term and renewal date of CARFAX's integration in Cox's vAuto? What share of Advantage pulls originate in third-party appraisal tools? [#2]",
    "**Insurance.** How many of the top-50 U.S. insurers are live, in testing, or awaiting state approval? What was insurance growth in 2025–26 excluding underwriting volume? [#1/#3 vs D9 §2.7]",
]

PRIMARY_REGISTER = [
    ['IHS Markit 10-K FY2016', 'Quartr 223426', 'p.80 (Note: Litigation)', 'Complaint, ~469 dealers, summary judgment, appeal, Jan-2017 suit'],
    ['IHS Markit 10-K FY2017', 'Quartr 223425', 'p.79 (Note: Litigation)', 'Appeal pending; follow-on suit stayed'],
    ['Mobility Global Form 10/A (27 May 2026)', 'Quartr 3603533', 'pp.263–265, 296–304, 340–341, 380–382', 'Products, risk factors (AI, search, customers, competition, exclusivity, suppliers), business model, competition'],
    ['Mobility Global 10-Q Q2-2026', 'Quartr 3699447', 'pp.27–29', 'Price vs new-business attribution; segment drivers'],
    ['Investor Day deck (12 May 2026)', 'Quartr 3352878', 'slides 10, 34, 57', '[D-deck] revenue mix by customer, business line, CARFAX product'],
    ['Segment P&L', 'canonical/segment_pl.csv', 'Form 10/A pp.355–360, 431–463; 10-Q pp.14–29', 'Segment revenue, Adj. EBITDA, subscription, U.S./international'],
    ['Court record (secondary)', 'research_notes/CARFAX challengers beyond AutoCheck/us_platforms_and_antitrust.md §5; reports/CARFAX challengers beyond AutoCheck.md', '—', 'Court opinions not retrieved (blocked); allegations, MTD, SJ reasoning, 2nd Cir.'],
]


# ---------------------------------------------------------------------------------------------
# Rendering helpers (docx + markdown in parallel)
# ---------------------------------------------------------------------------------------------
class Out:
    def __init__(self):
        self.doc = Document()
        st = self.doc.styles['Normal']; st.font.name = 'Arial'; st.font.size = Pt(9.5)
        st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
        st.paragraph_format.space_after = Pt(4)
        for s, sz in (('Heading 1', 14), ('Heading 2', 11.5), ('Heading 3', 10)):
            hs = self.doc.styles[s]; hs.font.name = 'Arial'; hs.font.color.rgb = NAVY; hs.font.size = Pt(sz)
            rf = hs.element.rPr.rFonts
            for k in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
                rf.set(qn(f'w:{k}'), 'Arial')
            for k in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
                if rf.get(qn(f'w:{k}')) is not None:
                    del rf.attrib[qn(f'w:{k}')]
            hs.paragraph_format.space_before = Pt(10 if s == 'Heading 1' else 7); hs.paragraph_format.space_after = Pt(3)
        for s in ('List Bullet', 'List Bullet 2'):
            self.doc.styles[s].font.name = 'Arial'; self.doc.styles[s].font.size = Pt(9.5)
        for sec in self.doc.sections:
            sec.left_margin = sec.right_margin = Cm(2); sec.top_margin = sec.bottom_margin = Cm(1.8)
        self._footer()
        self.md = []
        self.rendered = []

    def _footer(self):
        p = self.doc.sections[0].footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f'{TITLE} · {DATE} · page '); r.font.size = Pt(7.5); r.font.color.rgb = GREY
        r2 = p.add_run(); r2.font.size = Pt(7.5)
        for tag, txt in (('begin', None), (None, 'PAGE'), ('end', None)):
            if tag:
                e = OxmlElement('w:fldChar'); e.set(qn('w:fldCharType'), tag); r2._r.append(e)
            else:
                e = OxmlElement('w:instrText'); e.set(qn('xml:space'), 'preserve'); e.text = txt; r2._r.append(e)

    @staticmethod
    def rich(p, text, size=None, italic=False, color=None, bold=False):
        for part in re.split(r'(\*\*[^*]+\*\*)', text):
            if not part:
                continue
            b = part.startswith('**') and part.endswith('**')
            r = p.add_run(part[2:-2] if b else part)
            r.bold = b or bold; r.italic = italic
            if size: r.font.size = Pt(size)
            if color: r.font.color.rgb = color
            if part.startswith('Inference:'):
                pass
        return p

    def h(self, level, text):
        self.doc.add_heading(text, level=level); self.md += ['', '#' * (level + 1) + ' ' + text, '']

    def p(self, text, size=None, italic=False, color=None):
        para = self.doc.add_paragraph(); self.rich(para, text, size, italic, color); self.md += [text, '']
        return para

    def label(self, lab, text):
        para = self.doc.add_paragraph(); r = para.add_run(lab + ' '); r.bold = True; r.font.color.rgb = NAVY
        self.rich(para, text); self.md += [f'**{lab}** {text}', '']

    def bullets(self, items, size=None):
        for it in items:
            para = self.doc.add_paragraph(style='List Bullet'); para.paragraph_format.space_after = Pt(2)
            self.rich(para, it, size); self.md.append('- ' + it)
        self.md.append('')

    def numbered(self, items):
        for i, it in enumerate(items, 1):
            para = self.doc.add_paragraph(); para.paragraph_format.left_indent = Inches(0.25)
            para.paragraph_format.first_line_indent = Inches(-0.25)
            r = para.add_run(f'{i}.  '); r.bold = True; r.font.color.rgb = NAVY
            self.rich(para, it); self.md.append(f'{i}. {it}')
        self.md.append('')

    @staticmethod
    def _pshade_border(para):
        pPr = para._p.get_or_add_pPr()
        bdr = OxmlElement('w:pBdr'); left = OxmlElement('w:left')
        for k, v in (('val', 'single'), ('sz', '18'), ('space', '6'), ('color', NAVY_HEX)):
            left.set(qn(f'w:{k}'), v)
        bdr.append(left); pPr.append(bdr)
        shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), QUOTE_HEX)
        pPr.append(shd)

    def quote(self, qid):
        q = Q[qid]
        self.rendered.append(qid)
        para = self.doc.add_paragraph()
        pf = para.paragraph_format; pf.left_indent = Cm(0.6); pf.right_indent = Cm(0.3); pf.space_after = Pt(4); pf.keep_together = True
        self._pshade_border(para)
        r = para.add_run('“' + display(q['text']) + '”'); r.italic = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor(0x26, 0x26, 0x26)
        r.add_break(WD_BREAK.LINE)
        a = para.add_run('— ' + cite(qid)); a.font.size = Pt(7.5); a.font.color.rgb = NAVY
        self.md += [f'> *“{display(q["text"])}”*  ', f'> — {cite(qid)}', '']

    def table(self, header, rows, widths, size=8, caption=None, source=None, num_cols=()):
        if caption:
            cp = self.doc.add_paragraph(); cp.paragraph_format.keep_with_next = True; cp.paragraph_format.space_after = Pt(2)
            self.rich(cp, caption, 8.5, color=NAVY, bold=True); self.md += [f'**{caption}**', '']
        t = self.doc.add_table(rows=1 + len(rows), cols=len(header)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
        tblPr = t._tbl.tblPr; b = OxmlElement('w:tblBorders')
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            e = OxmlElement(f'w:{edge}'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4'); e.set(qn('w:space'), '0'); e.set(qn('w:color'), 'BFBFBF'); b.append(e)
        tblPr.append(b)
        tot = 6.7; s = float(sum(widths)); w_in = [tot * w / s for w in widths]
        for ri, row in enumerate([header] + rows):
            tr = t.rows[ri]; trPr = tr._tr.get_or_add_trPr(); trPr.append(OxmlElement('w:cantSplit'))
            if ri == 0:
                trPr.append(OxmlElement('w:tblHeader'))
            for ci, txt in enumerate(row):
                c = tr.cells[ci]; c.width = Inches(w_in[ci]); para = c.paragraphs[0]
                para.paragraph_format.space_after = Pt(0)
                if ri == 0:
                    shd(c, NAVY_HEX); self.rich(para, txt, size, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
                else:
                    if ri % 2 == 0:
                        shd(c, BAND_HEX)
                    self.rich(para, txt, size)
                if ci in num_cols:
                    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for ci, gc in enumerate(t._tbl.tblGrid.findall(qn('w:gridCol'))):
            gc.set(qn('w:w'), str(int(w_in[ci] * 1440)))
        self.md += ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
        self.md += ['| ' + ' | '.join(c.replace('|', '/') for c in r) + ' |' for r in rows]
        self.md.append('')
        if source:
            sp = self.doc.add_paragraph(); self.rich(sp, source, 7.5, italic=True, color=GREY); self.md += [f'*{source}*', '']
        else:
            self.doc.add_paragraph().paragraph_format.space_after = Pt(0)

    def page_break(self):
        self.doc.add_page_break()


def shd(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr(); s = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear'); s.set(qn('w:color'), 'auto'); s.set(qn('w:fill'), fill); tcPr.append(s)


def display(t):
    """Inner double quotes -> typographic single quotes for display (verification normalises all quote marks)."""
    out, open_ = [], True
    for ch in t:
        if ch == '"':
            out.append('‘' if open_ else '’'); open_ = not open_
        else:
            out.append(ch)
    return ''.join(out)


# ---------------------------------------------------------------------------------------------
def build():
    o = Out()
    # Cover
    tp = o.doc.add_paragraph(); r = tp.add_run(TITLE); r.bold = True; r.font.size = Pt(22); r.font.color.rgb = NAVY
    sp = o.doc.add_paragraph(); r = sp.add_run(SUBTITLE); r.font.size = Pt(13); r.font.color.rgb = NAVY
    o.p(f'MBGL research engagement · {DATE} · Segments overview and product-by-product evidence from primary documents', 8.5, True, GREY)
    o.md = [f'# {TITLE}', f'## {SUBTITLE}', '', f'*MBGL research engagement · {DATE}*', '']
    o.h(1, 'Bottom line')
    o.p(BOTTOM_LINE)
    o.h(2, 'What the sources are, and their limits')
    o.bullets(SOURCE_NOTE, 8.5)

    # 2 Segments
    o.page_break()
    o.h(1, '1. Segment overview')
    o.table(['$m'] + PLAB, seg_rows(), [2.3, 1, 1, 1, 1, 1], 8, caption='Table 1. Segment P&L, FY2023–FY2025 and first half [D]/[C]',
            source='Source: canonical/segment_pl.csv (Form 10/A pp.355–360, 431–463; 10-Q Q2-26 pp.14–29) [D]; growth, margins and shares [C]. Adj. EBITDA is the company definition, on one bridge across the Q2-26 definition change (deliverables/PART_A_SUMMARY.md).',
            num_cols=(1, 2, 3, 4, 5))
    o.table(['Segment / line', 'What it sells', 'To whom', 'Size', 'Growth driver (filing words)'], SEG_DESC, [1.1, 2.0, 1.6, 1.8, 1.3], 7.5,
            caption='Table 2. What each segment sells',
            source='Products: Form 10/A pp.263–265, 340–341 [D]. Business-line and product shares: Investor Day deck slides 34 and 57 [D-deck] (unaudited; the B2B line split appears only in the deck). Dollar conversions [C].')
    o.h(2, 'How the money is made')
    for it in MONEY:
        if isinstance(it, tuple):
            o.quote(it[1])
        else:
            o.p(it)
    o.label('Inference:', 'CARFAX carries the group. In 6M-26 it earned about three-quarters of segment Adj. EBITDA before Corporate [C], and its growth is mostly price on a saturated dealer base. '
            'B2B grows on volume but at lower margins, and its FY25 Adj. EBITDA fell while revenue rose [C].')

    # 3 Products
    o.h(1, '2. Products: what the documents say')
    o.p('Each product has three parts. **What the documents say** gives direct quotes from filings, the antitrust record and expert transcripts. '
        '**Assessment** is labelled Inference. **Archive check** compares the evidence with earlier work files in work/analysis and work/reports.', 8.5, True, GREY)
    for letter, title, intro, qids, assess, archive in PRODUCTS:
        o.h(2, f'({letter}) {title}')
        if intro:
            o.p(intro)
        o.label('What the documents say', '')
        if letter == 'd':
            o.p('**The antitrust record.** The only primary court-related texts are the 10-K litigation notes:', 9)
            for qid in ('D16a', 'D16b', 'D16c', 'D17a'):
                if qid != 'D16a':
                    o.quote(qid)
                else:
                    o.quote(qid)
            o.p('**Court history, as reported in secondary coverage (court opinion not retrieved):**', 9)
            o.bullets(COURT_FACTS, 8.5)
            o.p('**The filings and experts on the 2025–26 marketplace shift:**', 9)
            qids = [q for q in qids if q != 'D16a']
        for qid in qids:
            o.quote(qid)
        o.label('Assessment. Inference:', assess)
        o.label('Archive check.', '')
        o.bullets(archive, 8.5)

    # 4 Cross-cutting
    o.h(1, '3. Cross-cutting themes')
    o.h(2, 'Pricing power')
    o.table(['Lever', 'Primary documents', 'Experts'], PRICING_TABLE, [1.1, 2.8, 2.8], 8)
    o.quote('A298b')
    o.label('Inference:', 'Pricing power is real but concentrated. It is collected from smaller dealers, from BIG and from usage re-tiering more than from large groups, '
            'and the experts put the remaining runway at roughly 3–4 years of increases unless a new value-add arrives. Value-based pricing is the stated doctrine; the experts describe a feature-then-price routine.')
    o.h(2, 'Competition and exclusivity: what the courts found against what experts say now')
    o.table(['Question', 'Courts (secondary coverage; opinions not retrieved)', 'Experts, 2025–26'], COURTS_VS_EXPERTS, [1.5, 2.4, 2.8], 8)
    o.quote('A382b')
    o.label('Inference:', 'The antitrust record cuts both ways. Because the courts found that CARFAX\'s position did not depend on its exclusive contracts, losing marketplace placement in 2025–26 should not, on that logic, break Advantage, and the 2026 dealer evidence agrees. '
            'But the contested ground has moved to Listings and workflow tools, where CARFAX is the challenger (Listings) or depends on a rival (vAuto). The filing names Cox and Experian as competitors but not AutoCheck or any marketplace.')
    o.h(2, 'Risks surfaced only by experts')
    for title, qids, comment in EXPERT_ONLY_RISKS:
        seen = [q for q in qids if q in o.rendered]
        ref = ''.join(f" [X, #{Q[q]['src']}, p.{Q[q]['page']}; quoted in §2]" for q in seen)
        o.label(title, comment + ref)
        for qid in qids:
            if qid not in seen:
                o.quote(qid)

    # 5 Questions
    o.h(1, '4. Questions for management')
    o.numbered(QUESTIONS)

    # 6 Appendix
    o.page_break()
    o.h(1, 'Appendix: source register')
    rows = []
    for n, (date, role, fid, ind) in CALLS.items():
        used = sum(1 for k in set(o.rendered) if Q[k]['kind'] == 'X' and Q[k]['src'] == n)
        rows.append([f'#{n}', date, role, ind, f'{fid}-…', str(used)])
    o.table(['Call', 'Interview', 'Expert', 'Independence / limits', 'Transcript file', 'Quotes'], rows, [0.4, 0.8, 1.9, 2.0, 0.9, 0.6], 7.5,
            caption='A1. Expert calls (AlphaSense; numbering and bios per analysis/X_expert_calls.md §1)',
            source='Byte-identical duplicates of #4–#6 ignored. Nine calls, eight people; six substantive voices on CARFAX, four of them ex-CARFAX. Quote pages are AlphaSense transcript pages.')
    o.table(['Document', 'ID', 'Pages used', 'Used for'], PRIMARY_REGISTER, [1.6, 1.4, 1.6, 2.1], 7.5, caption='A2. Primary documents and secondary court record')
    ren = set(o.rendered); nx = sum(1 for k in ren if Q[k]['kind'] == 'X'); nd = len(ren) - nx
    o.p(f'**Quote verification.** {nx} expert-call quotes and {nd} primary-document quotes are used; each was checked by script '
        '(scripts/build_segments_products_doc.py --verify). Expert quotes were checked against the transcript text and its stated page, and filing quotes against the Quartr page text, ignoring only whitespace and quote-mark style. '
        'Archive files used for checks: analysis/X_expert_calls.md, D1_moat.md, D2_unit_economics.md, D6/D7/D9/D11/D13, deliverables/PART_A_SUMMARY.md, reports/CARFAX challengers beyond AutoCheck.md.', 8, True, GREY)

    os.makedirs(os.path.dirname(OUT_DOCX), exist_ok=True)
    o.doc.save(OUT_DOCX)
    open(OUT_MD, 'w').write('\n'.join(o.md).replace('\n\n\n', '\n\n') + '\n')
    used = set(re.findall(r'\b([A-Z]\w*\d\w*)\b', ''))
    print('wrote', OUT_DOCX, OUT_MD, 'quotes defined', len(Q))


# ---------------------------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------------------------
def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', "'").replace('”', "'").replace('"', "'")
    return re.sub(r'\s+', '', s)


def used_ids():
    ids = set()
    for _, _, _, qids, _, _ in PRODUCTS:
        ids |= set(qids)
    ids |= {'D16a', 'D16b', 'D16c', 'D17a', 'A340a', 'Q27a', 'A298b', 'A382b'}
    for _, qids, _ in EXPERT_ONLY_RISKS:
        ids |= set(qids)
    return ids


def verify(tdir, fsrc):
    ok = True
    # transcripts: drop page markers, footers, timestamps, speaker labels; track page per char
    texts = {}
    for n, (_, _, fid, _) in CALLS.items():
        f = glob.glob(os.path.join(tdir, fid + '*.txt'))[0]
        buf, pages, page = [], [], 0
        for line in open(f, encoding='utf-8'):
            line = line.rstrip('\n')
            m = re.match(r'^=== PAGE (\d+) ===$', line)
            if m:
                page = int(m.group(1)); continue
            if line.startswith('©') or re.match(r'^Page \d+ of \d+$', line):
                continue
            nl = norm(line)
            buf.append(nl); pages += [page] * len(nl)
        texts[n] = (''.join(buf), pages)
    fil = {}
    cur = None
    for line in open(fsrc, encoding='utf-8'):
        m = re.match(r'^### (\w+) p\.(\d+)', line)
        if m:
            cur = (m.group(1), int(m.group(2))); fil[cur] = ''; continue
        if cur:
            fil[cur] += norm(line)
    uids = used_ids(); nx = nd = 0
    for qid in sorted(uids):
        q = Q[qid]; nq = norm(q['text'])
        if q['kind'] == 'X':
            t, pages = texts[q['src']]; i = t.find(nq)
            if i < 0:
                print('FAIL X', qid, q['text'][:70]); ok = False; continue
            if q['page'] and pages[i] != q['page']:
                print('PAGE', qid, 'stated', q['page'], 'found', pages[i]); ok = False
            nx += 1
        else:
            src = fil.get((q['src'], q['page']), '')
            if nq not in src:
                print('FAIL D', qid, q['src'], q['page'], q['text'][:70]); ok = False; continue
            nd += 1
        words = len(re.findall(r'[.!?](?=\s|$)', q['text'].rstrip('"').rstrip()))
        if words > 2:
            print('LONG', qid, words)
    print(f'verified expert quotes {nx}, filing quotes {nd}, used {len(uids)} of {len(Q)} defined; ok={ok}')
    return ok


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--verify':
        sys.exit(0 if verify(sys.argv[2], sys.argv[3]) else 1)
    build()
