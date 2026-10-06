#!/usr/bin/env python3
"""Authoring source for the Part E research deck content.

Emits work/deliverables/deck_content.json. Every number shown on a slide is a
registered fact with its source file and row/section locator; the per-slide
`notes` field is generated from those facts so the deck's speaker notes carry
the full audit trail. build_deck.py renders the JSON; fact_check_deck.py
re-reads every fact against the canonical / extraction CSVs.
"""
import json
import os

ROOT = "/home/user/MBGL/work"
OUT = os.path.join(ROOT, "deliverables", "deck_content.json")

FACTS = {}


def _add(fid, **kw):
    assert fid not in FACTS, fid
    FACTS[fid] = kw
    return fid


# ---- fact constructors -------------------------------------------------------
def P(fid, label, value, key, period, tier="D", unit="usd_m"):
    """canonical/primary.csv row (canon_key, period)."""
    return _add(fid, label=label, value=value, unit=unit, tier=tier,
                source="canonical/primary.csv",
                locator={"canon_key": key, "period": period})


def S(fid, label, value, line_item, period, tier="D", unit="usd_m", page=None, doc=None):
    """extraction/segments_kpi.csv row (line_item, fiscal_period[, page, source_doc])."""
    loc = {"line_item": line_item, "fiscal_period": period}
    if page:
        loc["page"] = str(page)
    if doc:
        loc["source_doc"] = doc
    return _add(fid, label=label, value=value, unit=unit, tier=tier,
                source="extraction/segments_kpi.csv", locator=loc)


def PR(fid, label, value, line_item, period, tier="D", unit="usd_m", text_contains=None):
    loc = {"line_item": line_item, "fiscal_period": period}
    if text_contains:
        loc["text_contains"] = text_contains
    return _add(fid, label=label, value=value, unit=unit, tier=tier,
                source="extraction/predecessor.csv", locator=loc)


def PP(fid, label, value, page, contains, period=None, tier="D", unit="usd_m", list_index=None):
    loc = {"page": str(page), "line_item_contains": contains}
    if period:
        loc["fiscal_period"] = period
    if list_index is not None:
        loc["list_index"] = list_index
    return _add(fid, label=label, value=value, unit=unit, tier=tier,
                source="extraction/presentations.csv", locator=loc)


def N(fid, label, value, line_item, period, tier="D", unit="usd_m"):
    return _add(fid, label=label, value=value, unit=unit, tier=tier,
                source="extraction/notes.csv",
                locator={"line_item": line_item, "fiscal_period": period})


def C(fid, label, value, formula, tier="C", unit="usd_m", decimals=1, method=""):
    """Computed from other facts; fact_check re-evaluates the formula."""
    return _add(fid, label=label, value=value, unit=unit, tier=tier,
                source="computed", formula=formula, decimals=decimals, method=method)


def A(fid, label, value, tier, src, section, evidence, unit=""):
    """Analysis-file fact (no direct CSV row). fact_check confirms `evidence`
    appears verbatim in the cited file."""
    return _add(fid, label=label, value=value, unit=unit, tier=tier,
                source=src, locator={"section": section, "evidence": evidence})


# =============================================================================
# FACTS
# =============================================================================
# --- carve-out P&L / cash (canonical) ---
for per, v in [("FY2023", 1485), ("FY2024", 1613), ("FY2025", 1750), ("6M-2025", 859), ("6M-2026", 923),
               ("Q1-2025", 420), ("Q1-2026", 455), ("Q2-2025", 439), ("Q2-2026", 468)]:
    P(f"rev_{per}", f"Revenue {per}", v, "IS.revenue", per)
for per, v in [("FY2023", 239), ("FY2024", 298), ("FY2025", 339), ("6M-2025", 180), ("6M-2026", 163)]:
    P(f"op_{per}", f"Operating profit {per}", v, "IS.op", per)
for per, v in [("FY2023", 163), ("FY2024", 208), ("FY2025", 220), ("6M-2025", 123), ("6M-2026", 108)]:
    P(f"ni_{per}", f"Net income {per}", v, "IS.ni", per)
for per, v in [("FY2023", 393), ("FY2024", 427), ("FY2025", 485), ("6M-2025", 233), ("6M-2026", 189)]:
    P(f"cfo_{per}", f"Cash from operations {per}", v, "CF.cfo", per)
for per, v in [("FY2023", -18), ("FY2024", -15), ("FY2025", -24), ("6M-2025", -8), ("6M-2026", -12)]:
    P(f"capex_{per}", f"Capex {per}", v, "CF.capex", per)
P("tax_FY2025", "Tax provision FY25", 106, "IS.tax", "FY2025")
P("int_FY2025", "Interest expense, net FY25", 13, "IS.int", "FY2025")
P("amort_FY2025", "Amortization of acquired intangibles FY25", 296, "IS.amort", "FY2025")
P("sbc_FY2025", "Stock-based compensation FY25", 22, "CF.sbc", "FY2025")
P("sbc_FY2024", "Stock-based compensation FY24", 28, "CF.sbc", "FY2024")
P("sbc_FY2023", "Stock-based compensation FY23", 20, "CF.sbc", "FY2023")
P("cash_Q2", "Cash at 6/30/26", 186, "BS.cash", "Q2-2026")
P("ltd_Q2", "Long-term debt (carrying) at 6/30/26", 1981, "BS.ltd", "Q2-2026")
P("eps_6M26", "Diluted EPS 6M-26 (10-Q)", 0.37, "IS.eps_d", "6M-2026", unit="usd_per_share")
P("eps_6M25", "Diluted EPS 6M-25 (10-Q)", 0.42, "IS.eps_d", "6M-2025", unit="usd_per_share")

# --- Adj. EBITDA / FCF (segments_kpi) ---
for per, v, pg in [("FY2023", 598, 358), ("FY2024", 658, 358), ("FY2025", 711, 358), ("Q1-2025", 169, 358), ("Q1-2026", 184, 358)]:
    S(f"ae_{per}", f"Adj. EBITDA {per}", v, "Adjusted EBITDA", per, page=pg)
for per, v in [("6M-2025", 357), ("6M-2026", 386), ("Q2-2025", 188), ("Q2-2026", 202)]:
    S(f"ae_{per}", f"Adj. EBITDA {per}", v, "Adjusted EBITDA", per, page=15)
for per, v, pg in [("FY2023", 375, 361), ("FY2024", 412, 361), ("FY2025", 461, 361), ("6M-2025", 225, 26), ("6M-2026", 177, 26)]:
    S(f"fcf_{per}", f"Free cash flow {per}", v, "Free cash flow", per, page=pg)

# --- segments ---
for seg in ("CARFAX", "B2B"):
    for per, v in {"CARFAX": [("FY2023", 928), ("FY2024", 1039), ("FY2025", 1142), ("6M-2025", 564), ("6M-2026", 610)],
                   "B2B": [("FY2023", 557), ("FY2024", 574), ("FY2025", 608), ("6M-2025", 295), ("6M-2026", 313)]}[seg]:
        S(f"{seg.lower()}_rev_{per}", f"{seg} revenue {per}", v, f"{seg}: Revenue", per)
for seg, vals in {"CARFAX": [("FY2023", 422), ("FY2024", 476), ("FY2025", 536)],
                  "B2B": [("FY2023", 191), ("FY2024", 203), ("FY2025", 197)]}.items():
    for per, v in vals:
        S(f"{seg.lower()}_ae_{per}", f"{seg} Segment Adj. EBITDA {per}", v, f"{seg}: Segment Adjusted EBITDA", per)
S("corp_ae_FY2025", "Corporate Adj. EBITDA FY25", -22, "Corporate: Segment Adjusted EBITDA", "FY2025")
for seg, vals in {"CARFAX": [("6M-2025", 272), ("6M-2026", 293)], "B2B": [("6M-2025", 93), ("6M-2026", 102)]}.items():
    for per, v in vals:
        S(f"{seg.lower()}_ae_{per}", f"{seg} Adj. EBITDA {per}", v, f"{seg}: Adjusted EBITDA", per)
S("carfax_op_FY2025", "CARFAX segment OP FY25", 322, "CARFAX: Segment operating profit", "FY2025")
S("b2b_op_FY2025", "B2B segment OP FY25", 62, "B2B: Segment operating profit", "FY2025")
S("corp_unalloc_FY2025", "Corporate Unallocated FY25", 45, "Total: Corporate Unallocated expense (3)", "FY2025")
S("sub_FY2025", "Subscription revenue FY25", 1426, "Total: Subscription", "FY2025")
S("intl_FY2025", "International revenue FY25", 296, "International", "FY2025", page=463)

# --- KPIs (segments_kpi) ---
S("k_sources", "Contributory network sources (more than)", 177000, "Contributory network sources (more than)", "FY2025", unit="count")
S("k_records", "CARFAX vehicle history records (more than)", 38e9, "CARFAX vehicle history records (more than)", "FY2025", unit="count")
S("k_dealers", "CARFAX dealer customers (over)", 40000, "CARFAX dealer customers (over)", "FY2025", unit="count")
S("k_shops", "Dealers and service shops in data network (more than)", 92000, "CARFAX dealers and service shops in data network (more than)", "FY2025", unit="count")
S("k_police", "Police agencies", 6300, "Police agencies (data partnerships)", "FY2025", unit="count")
S("k_oem_src", "OEMs (data partnerships)", 36, "OEMs (data partnerships)", "FY2025", unit="count")
S("k_cpo", "OEM CPO programs", 36, "OEM Certified Pre-Owned programs (data sources)", "FY2025", unit="count")
S("k_daily", "Records added daily (approx.)", 6e6, "Average records added daily (approximately)", "FY2025", unit="count")
S("k_txn", "Transaction records (more than)", 13e9, "Transaction records (more than)", "FY2025", unit="count")
S("k_vins", "Unique VINs tracked (approx.)", 832e6, "Unique VINs tracked (approximately)", "FY2025", unit="count")
S("k_attr", "Data attributes per vehicle", 2000, "Data attributes per vehicle (more than)", "FY2025", unit="count")
S("k_muv", "Monthly unique visitors (US)", 23e6, "Monthly average unique visitors to CARFAX U.S. website and apps (approximately)", "FY2025", unit="count")
S("k_views", "Monthly VHR views", 28e6, "Monthly average CARFAX vehicle history report views (more than)", "FY2025", unit="count")
S("k_carcare", "Car Care consumers", 53e6, "Car Care consumer audience (more than)", "FY2025", unit="count")
S("k_aware", "In-market awareness", 96, "CARFAX average in-market awareness (survey of in-market consumers)", "FY2025", unit="pct")
S("k_top40", "Top-40 carmakers served", 100, "Share of top 40 global carmakers served", "FY2025", unit="pct")
S("k_top100sup", "Top-100 suppliers served", 94, "Share of top 100 automotive suppliers served", "FY2025", unit="pct")
S("k_banks", "Top-20 banks/insurers using data", 17, "Top 20 banks and insurers using data (printed 17 of the top 20)", "FY2025", unit="count")
S("k_mktscan", "Dealerships using Market Scan", 10500, "Dealerships using Market Scan pricing engine (approximately)", "FY2025", unit="count")
S("k_underwrite_FY25", "Underwriting volumes contribution FY25", 13, "Subscription revenue increase from solid underwriting volumes", "FY2025")
S("k_underwrite_FY24", "Underwriting volumes contribution FY24", 17, "Subscription revenue increase from solid underwriting volumes", "FY2024")
S("k_nb_FY25", "New business growth FY25 (10/A)", 76, "Subscription revenue increase from continued new business growth", "FY2025")
S("k_nb_Q1_10A", "Q1-26 new business growth per 10/A", 26, "Subscription revenue increase from continued new business growth", "Q1-2026")
S("k_price_Q2", "Price increases Q2-26 (approx.)", 16, "Revenue increase from price increases (approximately)", "Q2-2026")
S("k_price_6M", "Price increases 6M-26 (approx.)", 36, "Revenue increase from price increases (approximately)", "6M-2026")
S("k_nbq_Q2", "New business Q2-26 (approx.)", 8, "Revenue increase from continued new business growth (approximately)", "Q2-2026")
S("k_nbq_6M", "New business 6M-26 (approx.)", 20, "Revenue increase from continued new business growth (approximately)", "6M-2026")
S("k_fx_6M", "FX benefit 6M-26 (~)", 5, "Foreign exchange benefit to revenue (~)", "6M-2026")
S("g_rev_lo", "FY26 revenue guide low", 1870, "Revenue - low end", "FY2026E")
S("g_rev_hi", "FY26 revenue guide high", 1885, "Revenue - high end", "FY2026E")
S("g_ae_lo", "FY26 Adj. EBITDA guide low", 745, "Adjusted EBITDA - low end", "FY2026E")
S("g_ae_hi", "FY26 Adj. EBITDA guide high", 760, "Adjusted EBITDA - high end", "FY2026E")
S("g_gr_lo", "FY26 revenue growth guide low", 6.9, "Revenue Growth - low end", "FY2026E", unit="pct")
S("g_gr_hi", "FY26 revenue growth guide high", 7.7, "Revenue Growth - high end", "FY2026E", unit="pct")
S("g_onetime", "One-time spin costs (~)", 100, "One-time spin-related costs total (~)", "FY2026E")
S("g_int_2H", "2H-26 interest expense (~)", 55, "Second half 2026 interest expense (~)", "FY2026E")
S("div_q", "Quarterly dividend per share", 0.06, "Quarterly cash dividend per share (initiated)", "Q2-2026", unit="usd_per_share")
S("rpo_FY25_q2", "RPO 6/30/26", 102, "Remaining performance obligations (aggregate transaction price)", "6M-2026")

# --- notes.csv: senior notes ---
N("n29", "5.050% notes due 2029 principal", 650, "5.050% senior notes due 2029 - principal", "Q1-2026")
N("n31", "5.450% notes due 2031 principal", 650, "5.450% senior notes due 2031 - principal", "Q1-2026")
N("n36", "6.050% notes due 2036 principal", 700, "6.050% senior notes due 2036 - principal", "Q1-2026")
N("n29c", "2029 coupon", 5.05, "5.050% senior notes due 2029 - coupon", "Q1-2026", unit="pct")
N("n31c", "2031 coupon", 5.45, "5.450% senior notes due 2031 - coupon", "Q1-2026", unit="pct")
N("n36c", "2036 coupon", 6.05, "6.050% senior notes due 2036 - coupon", "Q1-2026", unit="pct")
N("n_total", "Senior notes aggregate principal", 2000, "senior notes aggregate principal amount", "Q1-2026")

# --- predecessor ---
PRED_REV = [("FY2014", 662.6), ("FY2015", 758.4), ("FY2016", 892.8), ("FY2017", 991.6), ("FY2018", 1160.2),
            ("FY2019", 1246.1), ("FY2020", 1151.6), ("FY2021", 1354.4)]
PRED_AE = [("FY2014", 234.3), ("FY2015", 282.7), ("FY2016", 353.3), ("FY2017", 408.6), ("FY2018", 479.3),
           ("FY2019", 520.9), ("FY2020", 514.7), ("FY2021", 645.0)]
for per, v in PRED_REV:
    PR(f"p_rev_{per}", f"IHS Transportation revenue {per}", v, "Revenue - Transportation", per)
for per, v in PRED_AE:
    PR(f"p_ae_{per}", f"IHS Transportation Adj. EBITDA {per}", v, "Adjusted EBITDA - Transportation", per)
for per, v in PRED_REV:
    ae = dict(PRED_AE)[per]
    C(f"p_m_{per}", f"IHS Transportation Adj. EBITDA margin {per}", round(ae / v * 100, 1),
      f"p_ae_{per}/p_rev_{per}*100", unit="pct", method="Adj. EBITDA / revenue")
for per, v in [("FY2022", 1142), ("FY2023", 1484), ("FY2024", 1609), ("FY2025", 1747)]:
    PR(f"spgi_rev_{per}", f"SPGI Mobility revenue {per}", v, "Revenue", per)
for per, txt in [("FY2016", "17 billion records"), ("FY2018", "20 billion records"), ("FY2019", "23 billion records"),
                 ("FY2021", "27 billion records")]:
    PR(f"rec_{per}", f"CARFAX VH records {per} (bn)", float(txt.split()[0]), "CARFAX data scale (printed)", per,
       unit="bn", text_contains=txt)
PR("src_FY2016", "CARFAX sources FY16", 100000, "CARFAX data scale (printed)", "FY2016", unit="count", text_contains="100,000 data sources")
PR("src_FY2021", "CARFAX sources FY21", 130000, "CARFAX data scale (printed)", "FY2021", unit="count", text_contains="130,000 data sources")

# --- presentations ---
PP("pp_dealer", "Revenue by customer type: Dealer (deck)", 62, 10, "Dealer ( B2B & CARFAX )", "FY2025", unit="pct")
PP("pp_oem", "Revenue by customer type: OEM & Supplier (deck)", 20, 10, "OEM & Supplier", "FY2025", unit="pct")
PP("pp_fin", "Revenue by customer type: Financial/Consumer/Other (deck)", 18, 10, "Financial / Consumer / Other", "FY2025", unit="pct")
PP("pp_adv", "CARFAX mix: Advantage", 38, 57, "PRODUCT & INTERNATIONAL - Advantage", "FY2025", unit="pct")
PP("pp_fco", "CARFAX mix: Financial/Consumer/Other", 26, 57, "PRODUCT & INTERNATIONAL - Financial", "FY2025", unit="pct")
PP("pp_list", "CARFAX mix: Listings", 22, 57, "PRODUCT & INTERNATIONAL - Listings", "FY2025", unit="pct")
PP("pp_intl", "CARFAX mix: International", 15, 57, "PRODUCT & INTERNATIONAL - International", "FY2025", unit="pct")
PP("pp_ms", "B2B line: Marketing & Sales", 74, 34, "BUSINESS LINE - Marketing & Sales", "FY2025", unit="pct")
PP("pp_sp", "B2B line: Strategy & Planning", 26, 34, "BUSINESS LINE - Strategy & Planning", "FY2025", unit="pct")
PP("pp_media", "Media investment since 2000", 1500, 18, "Media Investment Since 2000", "2000-2025")
PP("pp_showme", "'Show me the CARFAX' per month", 2e6, 67, "Number of times per month consumers walk", "2024", unit="count")
PP("pp_integr", "Dealer integrations", 95, 66, "Dealer : Integrations", "2026", unit="count")
PP("pp_conv_FY2023", "FCF conversion FY23 (deck)", 63, 111, "Free cash flow % Conversion", "FY2023", unit="pct")
PP("pp_conv_FY2024", "FCF conversion FY24 (deck)", 63, 111, "Free cash flow % Conversion", "FY2024", unit="pct")
PP("pp_conv_FY2025", "FCF conversion FY25 (deck)", 65, 111, "Free cash flow % Conversion", "FY2025", unit="pct")
PP("pp_onetime_FY25", "Non-recurring adjustments FY25", 40, 111, "Non - Recurring Adjustments", "FY2025")
PP("pp_gross_lev", "Gross leverage LTM Q1-26 (deck)", 2.8, 115, "Gross Leverage Ratio", "LTM-Q1-2026", unit="x")
ORG = [10, 11, 14, 11, 10, -2, 18, 10, 9, 9, 9]
IND = [6, 0, -2, 1, -1, -15, 4, -8, 13, 2, 2]
for i, yr in enumerate(range(2015, 2026)):
    PP(f"org_{yr}", f"Mobility organic growth {yr} (s.91, mapping inferred)", ORG[i], 91, "Mobility Organic Growth", unit="pct", list_index=i)
    PP(f"ind_{yr}", f"Industry (FRED) growth {yr} (s.91, mapping inferred)", IND[i], 91, "Industry Growth", unit="pct", list_index=i)

# --- computed ---
C("c_rev_cagr", "Revenue CAGR FY23-25", 8.6, "((rev_FY2025/rev_FY2023)**0.5-1)*100", unit="pct")
C("c_ae_cagr", "Adj. EBITDA CAGR FY23-25", 9.0, "((ae_FY2025/ae_FY2023)**0.5-1)*100", unit="pct")
C("c_fcf_cagr", "FCF CAGR FY23-25", 10.9, "((fcf_FY2025/fcf_FY2023)**0.5-1)*100", unit="pct")
for per in ["FY2023", "FY2024", "FY2025", "6M-2025", "6M-2026", "Q2-2026"]:
    pass
for per, v in [("FY2023", 40.3), ("FY2024", 40.8), ("FY2025", 40.6), ("6M-2025", 41.6), ("6M-2026", 41.8)]:
    C(f"c_m_{per}", f"Adj. EBITDA margin {per}", v, f"ae_{per}/rev_{per}*100", unit="pct")
for per, v in [("FY2023", 62.7), ("FY2024", 62.6), ("FY2025", 64.8), ("6M-2025", 63.0), ("6M-2026", 45.9)]:
    C(f"c_conv_{per}", f"FCF conversion {per}", v, f"fcf_{per}/ae_{per}*100", unit="pct", method="FCF / Adj. EBITDA")
for per, v in [("FY2023", 25.3), ("FY2024", 25.5), ("FY2025", 26.3)]:
    C(f"c_fcfm_{per}", f"FCF margin {per}", v, f"fcf_{per}/rev_{per}*100", unit="pct")
for per, v in [("FY2023", 1.2), ("FY2024", 0.9), ("FY2025", 1.4), ("6M-2026", 1.3)]:
    C(f"c_capint_{per}", f"Capex / revenue {per}", v, f"-capex_{per}/rev_{per}*100", unit="pct")
C("c_1h_growth", "1H-26 revenue growth", 7.5, "(rev_6M-2026/rev_6M-2025-1)*100", unit="pct")
C("c_q2_growth", "Q2-26 revenue growth", 6.6, "(rev_Q2-2026/rev_Q2-2025-1)*100", unit="pct")
C("c_q1_growth", "Q1-26 revenue growth", 8.3, "(rev_Q1-2026/rev_Q1-2025-1)*100", unit="pct")
C("c_cfo_yoy", "CFO 6M y/y", -18.9, "(cfo_6M-2026/cfo_6M-2025-1)*100", unit="pct")
C("c_p_rev_cagr", "IHS Transportation revenue CAGR FY14-21", 10.8, "((p_rev_FY2021/p_rev_FY2014)**(1/7)-1)*100", unit="pct")
C("c_p_ae_cagr", "IHS Transportation Adj. EBITDA CAGR FY14-21", 15.6, "((p_ae_FY2021/p_ae_FY2014)**(1/7)-1)*100", unit="pct")
C("c_carfax_share", "CARFAX share of FY25 revenue", 65.3, "carfax_rev_FY2025/rev_FY2025*100", unit="pct")
C("c_sub_share", "Subscription share FY25", 81.5, "sub_FY2025/rev_FY2025*100", unit="pct")
C("c_intl_share", "International share FY25", 16.9, "intl_FY2025/rev_FY2025*100", unit="pct")
for seg in ("carfax", "b2b"):
    for per in ("FY2023", "FY2024", "FY2025"):
        r = FACTS[f"{seg}_ae_{per}"]["value"] / FACTS[f"{seg}_rev_{per}"]["value"] * 100
        C(f"c_{seg}_m_{per}", f"{seg.upper()} Adj. EBITDA margin {per}", round(r, 1), f"{seg}_ae_{per}/{seg}_rev_{per}*100", unit="pct")
    r = FACTS[f"{seg}_ae_6M-2026"]["value"] / FACTS[f"{seg}_rev_6M-2026"]["value"] * 100
    C(f"c_{seg}_m_6M-2026", f"{seg.upper()} Adj. EBITDA margin 6M-26", round(r, 1), f"{seg}_ae_6M-2026/{seg}_rev_6M-2026*100", unit="pct")
C("c_carfax_g24", "CARFAX growth FY24", 12.0, "(carfax_rev_FY2024/carfax_rev_FY2023-1)*100", unit="pct")
C("c_carfax_g25", "CARFAX growth FY25", 9.9, "(carfax_rev_FY2025/carfax_rev_FY2024-1)*100", unit="pct")
C("c_b2b_g24", "B2B growth FY24", 3.1, "(b2b_rev_FY2024/b2b_rev_FY2023-1)*100", unit="pct")
C("c_b2b_g25", "B2B growth FY25", 5.9, "(b2b_rev_FY2025/b2b_rev_FY2024-1)*100", unit="pct")
C("c_carfax_g6m", "CARFAX growth 6M-26", 8.2, "(carfax_rev_6M-2026/carfax_rev_6M-2025-1)*100", unit="pct")
C("c_b2b_g6m", "B2B growth 6M-26", 6.1, "(b2b_rev_6M-2026/b2b_rev_6M-2025-1)*100", unit="pct")
# flow-through (Adj. EBITDA basis)
C("ft_carfax_FY24", "CARFAX flow-through FY24", 48.6, "(carfax_ae_FY2024-carfax_ae_FY2023)/(carfax_rev_FY2024-carfax_rev_FY2023)*100", unit="pct")
C("ft_carfax_FY25", "CARFAX flow-through FY25", 58.3, "(carfax_ae_FY2025-carfax_ae_FY2024)/(carfax_rev_FY2025-carfax_rev_FY2024)*100", unit="pct")
C("ft_carfax_6M", "CARFAX flow-through 6M-26", 45.7, "(carfax_ae_6M-2026-carfax_ae_6M-2025)/(carfax_rev_6M-2026-carfax_rev_6M-2025)*100", unit="pct")
C("ft_b2b_FY24", "B2B flow-through FY24", 70.6, "(b2b_ae_FY2024-b2b_ae_FY2023)/(b2b_rev_FY2024-b2b_rev_FY2023)*100", unit="pct")
C("ft_b2b_FY25", "B2B flow-through FY25", -17.6, "(b2b_ae_FY2025-b2b_ae_FY2024)/(b2b_rev_FY2025-b2b_rev_FY2024)*100", unit="pct")
C("ft_b2b_6M", "B2B flow-through 6M-26", 50.0, "(b2b_ae_6M-2026-b2b_ae_6M-2025)/(b2b_rev_6M-2026-b2b_rev_6M-2025)*100", unit="pct")
# per-dealer anchors
C("c_adv_list", "Advantage + Listings revenue FY25", 685.2, "(pp_adv+pp_list)/100*carfax_rev_FY2025", decimals=1)
C("c_per_dealer", "Advantage + Listings per dealer customer ($k/yr)", 17.1, "c_adv_list/k_dealers*1000", unit="usd_k", decimals=1)
C("c_adv_dealer", "Advantage per dealer customer ($k/yr)", 10.8, "pp_adv/100*carfax_rev_FY2025/k_dealers*1000", unit="usd_k", decimals=1)
C("c_carfax_dealer", "CARFAX revenue per dealer customer, upper bound ($k/yr)", 28.6, "carfax_rev_FY2025/k_dealers*1000", unit="usd_k", decimals=1)
# pricing
C("c_q1_price", "Q1-26 implied price", 20, "k_price_6M-k_price_Q2", decimals=0)
C("c_q1_nb", "Q1-26 implied new business", 12, "k_nbq_6M-k_nbq_Q2", decimals=0)
C("c_q1_drev", "Q1-26 revenue increase", 35, "rev_Q1-2026-rev_Q1-2025", decimals=0)
C("c_q2_drev", "Q2-26 revenue increase", 29, "rev_Q2-2026-rev_Q2-2025", decimals=0)
C("c_6m_drev", "6M-26 revenue increase", 64, "rev_6M-2026-rev_6M-2025", decimals=0)
C("c_q1_other", "Q1-26 other", 3, "c_q1_drev-c_q1_price-c_q1_nb", decimals=0)
C("c_q2_other", "Q2-26 other", 5, "c_q2_drev-k_price_Q2-k_nbq_Q2", decimals=0)
C("c_6m_other", "6M-26 other", 8, "c_6m_drev-k_price_6M-k_nbq_6M", decimals=0)
C("c_price_pts_6m", "Price points of 6M growth", 4.2, "k_price_6M/rev_6M-2025*100", unit="pct")
C("c_nb_pts_6m", "New business points of 6M growth", 2.3, "k_nbq_6M/rev_6M-2025*100", unit="pct")
C("c_price_pts_q2", "Price points of Q2 growth", 3.6, "k_price_Q2/rev_Q2-2025*100", unit="pct")
C("c_price_pts_q1", "Price points of Q1 growth", 4.8, "c_q1_price/rev_Q1-2025*100", unit="pct")
C("c_price_share_6m", "Price share of 6M revenue increase", 56.3, "k_price_6M/c_6m_drev*100", unit="pct")
# notes / interest
C("c_coupon", "Annual cash coupon on notes", 110.6, "n29*n29c/100+n31*n31c/100+n36*n36c/100")
C("c_wtd_coupon", "Weighted coupon", 5.53, "c_coupon/n_total*100", unit="pct", decimals=2)
# normalized NI bridge (FY25 base) - D3 section 4
C("b_op", "Operating profit (bridge)", 339, "ni_FY2025+tax_FY2025+int_FY2025", decimals=0)
C("b_taxint", "Tax + net interest add-back", 119, "tax_FY2025+int_FY2025", decimals=0)
A("b_onetime", "One-time items added back", 40, "D", "analysis/D3_group_decomposition.md", "section 4 (A1)", "One-time items (A1) | 40")
A("b_standalone", "Standalone increment (150bp x FY25 revenue)", 26, "C", "analysis/D3_group_decomposition.md", "section 4 (A2)", "Standalone increment (A2) | (26)")
A("b_interest", "Run-rate interest", 110, "C", "analysis/D3_group_decomposition.md", "section 4 (A4)", "Run-rate interest (A4) | (110)")
A("b_tax", "Tax @ 29.5%", 72, "E", "analysis/D3_group_decomposition.md", "section 4 (A5)", "Tax @ 29.5% (A5) | (72)")
C("b_norm_op", "Standalone normalized OP", 353, "b_op+b_onetime-b_standalone", decimals=0)
C("b_pretax", "Standalone pre-tax", 243, "b_norm_op-b_interest", decimals=0)
C("b_ni", "Standalone normalized NI FY25 base", 171, "b_pretax-b_tax", decimals=0)
A("b_ni_fy26", "Standalone normalized NI FY26 run-rate", 209, "C", "analysis/D3_group_decomposition.md", "section 4 FY26 run-rate variant", "NI ≈ 209")
A("shares", "Shares outstanding (m)", 294.82132, "D", "analysis/D3_group_decomposition.md", "section 5 (10Q p.11)", "294,821,320", unit="m")
C("c_eps_norm", "Standalone normalized EPS FY25 base", 0.58, "b_ni/shares", unit="usd_per_share", decimals=2)
C("c_eps_fy26", "Standalone normalized EPS FY26 run-rate", 0.71, "b_ni_fy26/shares", unit="usd_per_share", decimals=2)
C("c_eps_carve", "Illustrative carve-out EPS FY25", 0.75, "ni_FY2025/shares", unit="usd_per_share", decimals=2)
C("c_div", "Annual dividend ($m)", 70.8, "div_q*4*shares", decimals=1)
C("c_payout_fy25", "Payout on FY25-base normalized NI", 41.4, "c_div/b_ni*100", unit="pct")
C("c_payout_fy26", "Payout on FY26 run-rate NI", 33.9, "c_div/b_ni_fy26*100", unit="pct")
C("c_int_share", "Interest / standalone normalized OP", 31.2, "b_interest/b_norm_op*100", unit="pct")
C("c_int_share_co", "Interest / carve-out OP", 3.8, "int_FY2025/op_FY2025*100", unit="pct")
C("c_div_needed", "NI needed for 25% payout", 283, "c_div/0.25", decimals=0)
A("c_fcf_standalone", "Standalone FCF estimate", 365, "C", "analysis/D3_group_decomposition.md", "section 5", "~$365m")
C("c_div_fcf", "Dividend / standalone FCF", 19.4, "c_div/c_fcf_standalone*100", unit="pct")
# guidance arithmetic
C("c_2h_m_lo", "Implied 2H-26 margin low", 37.9, "(g_ae_lo-ae_6M-2026)/(g_rev_lo-rev_6M-2026)*100", unit="pct")
C("c_2h_m_hi", "Implied 2H-26 margin high", 38.9, "(g_ae_hi-ae_6M-2026)/(g_rev_hi-rev_6M-2026)*100", unit="pct")
C("c_2h25_m", "2H-25 margin", 39.7, "(ae_FY2025-ae_6M-2025)/(rev_FY2025-rev_6M-2025)*100", unit="pct")
C("c_occ_lo", "FY26 guide in OCC terms, low", 6.6, "((g_rev_lo-k_fx_6M)/rev_FY2025-1)*100", unit="pct")
C("c_occ_hi", "FY26 guide in OCC terms, high", 7.4, "((g_rev_hi-k_fx_6M)/rev_FY2025-1)*100", unit="pct")
C("c_q1_occ", "Q1-26 OCC growth (FX ~$4m)", 7.4, "((rev_Q1-2026-4)/rev_Q1-2025-1)*100", unit="pct")
C("c_standalone_bp", "150bp of FY25 revenue", 26.3, "0.015*rev_FY2025")
C("c_sbc3", "SBC at 3% of FY26 guide midpoint", 56.3, "0.03*c_rev_mid")
C("c_sbc4", "SBC at 4% of FY26 guide midpoint", 75.1, "0.04*c_rev_mid")
C("c_sbc_pct", "SBC / revenue FY25", 1.3, "sbc_FY2025/rev_FY2025*100", unit="pct")
C("c_ae_mid", "FY26 Adj. EBITDA guide midpoint", 752.5, "(g_ae_lo+g_ae_hi)/2")
C("c_rev_mid", "FY26 revenue guide midpoint", 1877.5, "(g_rev_lo+g_rev_hi)/2")
# moat
C("c_rec_cagr", "VH records CAGR FY16-25", 9.3, "((k_records/1e9/rec_FY2016)**(1/9)-1)*100", unit="pct")
C("c_src_cagr", "Sources CAGR FY16-25", 6.5, "((k_sources/src_FY2016)**(1/9)-1)*100", unit="pct")
A("ad_FY2023", "Advertising expense FY23", 134, "D", "analysis/QUALITATIVE.md", "section 1 CARFAX (10A p.450)", "$134m in FY23")
A("ad_FY2025", "Advertising expense FY25", 176, "D", "analysis/QUALITATIVE.md", "section 1 CARFAX (10A p.450)", "$176m in FY25")
C("c_ad_growth", "Ad expense growth FY23-25", 31.3, "(ad_FY2025/ad_FY2023-1)*100", unit="pct")
C("c_rev_growth_2y", "Revenue growth FY23-25", 17.8, "(rev_FY2025/rev_FY2023-1)*100", unit="pct")
C("c_ad_int", "Ad expense / revenue FY25", 10.1, "ad_FY2025/rev_FY2025*100", unit="pct")
C("c_org_mean", "Mean organic growth 2015-25", 9.9, "(org_2015+org_2016+org_2017+org_2018+org_2019+org_2020+org_2021+org_2022+org_2023+org_2024+org_2025)/11", unit="pct")
C("c_ind_mean", "Mean industry growth 2015-25", 0.2, "(ind_2015+ind_2016+ind_2017+ind_2018+ind_2019+ind_2020+ind_2021+ind_2022+ind_2023+ind_2024+ind_2025)/11", unit="pct")
# analysis-sourced items
A("a_corr", "Correlation organic vs industry (all / ex-2020-21)", "0.54 / -0.39", "C", "analysis/K_session_tables.md", "D9_demand_drivers", "corr 0.54 (all), -0.39 ex-2020/21")
A("a_gross_lev", "Gross leverage at spin", 2.7, "IR", "transcripts/TARGETS_TIMELINE.md", "Leverage row", "Gross 2.7x, net 2.4x", unit="x")
A("a_net_lev", "Net leverage", 2.4, "IR", "transcripts/TARGETS_TIMELINE.md", "Leverage row", "net 2.4x", unit="x")
A("a_spgi_m25", "SPGI Mobility adj. OP margin FY25", 39.9, "D", "analysis/D10_guidance_vs_execution.md", "section 1 scorecard", "**39.9%** [D]", unit="pct")
A("a_spgi_target", "SPGI 2025/26 margin target", "41-43%", "D", "analysis/D10_guidance_vs_execution.md", "section 1 scorecard", "**41–43%** adj. OP margin")
A("a_alloc_FY25", "S&P Global allocations FY25", 112, "D", "analysis/D3_group_decomposition.md", "section 2", "| 89 | 90 | 112 |")
A("a_txn_6M_b2b", "B2B transaction costs 6M-26", 33, "D", "analysis/D4_disclosure_changes.md", "section 2", "$33m in 6M-26")
A("a_b2b_op_q2", "B2B segment OP Q2-26", 3, "D", "analysis/D3_group_decomposition.md", "section 1 Basis 1", "| Q2-2026 | 101 | 3 | (22) | 82 |")
A("a_sbc_step", "SBC step-up to 3-4% of revenue", "3-4%", "IR", "transcripts/TARGETS_TIMELINE.md", "Stock-based comp row", "From ~1% to 3–4%")
A("a_ceo_tdc", "CEO 2026 target TDC", 4.50, "C", "analysis/D5_incentives.md", "section 2.4", "**$4.50m [C]**", unit="usd_m")
A("a_cfo_tdc", "CFO 2026 target TDC", 5.05, "C", "analysis/D5_incentives.md", "section 2.4", "**$5.05m [C]**", unit="usd_m")
A("a_cfo_onetime", "CFO one-time awards", 5.93, "C", "analysis/D5_incentives.md", "section 2.4", "**$5.93m [C]**", unit="usd_m")
A("a_eager_sct", "Eager FY25 SCT total", 6444004, "D", "analysis/D5_incentives.md", "section 2.1", "**$6,444,004**", unit="usd")
A("a_eager_sti", "Eager FY25 STI payout", 120.0, "C", "analysis/D5_incentives.md", "section 2.2", "**120.0%**", unit="pct")
A("a_fred_sti", "Fredericks FY25 STI payout", 129.2, "C", "analysis/D5_incentives.md", "section 2.2", "**129.2%**", unit="pct")
A("a_psu", "2023-25 PSU payouts", "182-184%", "C", "analysis/D5_incentives.md", "section 2.3", "about **182%**")
A("a_ltip", "LTIP share reserve", 14, "D", "analysis/D5_incentives.md", "section 3.1", "14% of shares outstanding", unit="pct")
A("a_ltip_sh", "LTIP reserve shares (m)", 41.3, "C", "analysis/D5_incentives.md", "section 3.1", "about **41.3m shares**", unit="m")
A("a_carfax_psu_band", "CARFAX PSU threshold-target spread", 4.5, "C", "analysis/D5_incentives.md", "section 2.3", "only 4.5%", unit="pct")
A("a_sbc_ramp", "SBC at 3-4% of FY26 revenue ($m)", "56-75", "C", "analysis/D5_incentives.md", "section 4", "about **$56-75m a year**")
A("a_fy28_rev", "FY28 plan revenue", 2220, "E", "analysis/D11_premortem.md", "Base for magnitudes", "**$2,220m**")
A("a_fy28_ae", "FY28 plan Adj. EBITDA", 870, "E", "analysis/D11_premortem.md", "Base for magnitudes", "**$870m**")
A("a_pm1", "Bear case 1 EBITDA gap", 105, "E", "analysis/D11_premortem.md", "table row 1", "**~$105m Adj. EBITDA")
A("a_pm2", "Bear case 2 EBITDA gap", "30-55", "E", "analysis/D11_premortem.md", "table row 2", "**~$30–55m of EBITDA**")
A("a_pm3", "Bear case 3 EBITDA cost", "35-40", "E", "analysis/D11_premortem.md", "table row 3", "**~$35–40m (~5% of EBITDA)**")
A("a_pm4", "Bear case 4 EBITDA gap", 35, "E", "analysis/D11_premortem.md", "table row 4", "**~$35m of EBITDA**")
A("a_pm5", "Bear case 5 EBITDA hit", 45, "E", "analysis/D11_premortem.md", "table row 5", "**−$45m of EBITDA (~6%)**")
A("a_pm6", "Bear case 6 GAAP pre-tax", "55-75", "E", "analysis/D11_premortem.md", "table row 6", "**~$55–75m of GAAP pre-tax**")
A("a_pm8", "Bear case 8 EBITDA", "20-30", "E", "analysis/D11_premortem.md", "table row 8", "**~$20–30m of EBITDA**")
A("a_pm10", "Bear case 10 SBC cost", 50, "E", "analysis/D11_premortem.md", "table row 10", "**+$50m a year**")
A("a_pm7", "Leverage sensitivity per $50m EBITDA", "0.15-0.2x", "C", "analysis/D11_premortem.md", "table row 7", "≈0.15–0.2x of leverage")
A("a_pm11", "International start-up losses", "10-20", "E", "analysis/D11_premortem.md", "table row 11", "~$10–20m a year")
A("a_beat_years", "Years organic beat industry", "10 of 11", "C", "analysis/D1_moat.md", "section 4.1", "In ten of eleven years")
A("a_recurring_2020", "2020 recurring organic growth", 3, "D", "analysis/D1_moat.md", "section 4.2", "**recurring organic +3%**", unit="pct")
A("a_new_biz_drop", "New business Q1 -> Q2", "12 -> 8", "C", "analysis/K_session_tables.md", "D7_pricing", "| New business | ~12 [C] (10A said 26) | ~8 [D] | ~20 [D] |")

# --- additional traced facts (text numbers) ---
A("a_filing_mix", "Filing customer mix: dealers / OEMs", "60 / 10", "D", "analysis/QUALITATIVE.md", "section 2 (10A p.299)", "about **60%** of revenue came from dealerships and **10%** from OEMs")
PP("pp_carfax_seg", "CARFAX share of revenue (deck)", 65, 10, "REVENUE BY SEGMENT - CARFAX", "FY2025", unit="pct")
PP("pp_b2b_seg", "B2B share of revenue (deck)", 35, 10, "REVENUE BY SEGMENT - B2B Solutions", "FY2025", unit="pct")
A("a_carproof", "CARPROOF price", 459, "D", "analysis/QUALITATIVE.md", "section 11 (INFO16 p.60)", "$459.2m net of cash", unit="usd_m")
A("a_mktscan", "Market Scan price", 223, "D", "analysis/QUALITATIVE.md", "section 1 (10A p.452)", "Acquired 2023-02-16 for $223m", unit="usd_m")
A("a_am78", "automotiveMastermind stake acquired", 78, "D", "analysis/QUALITATIVE.md", "section 1 (INFO17 p.62)", "78% for about $432", unit="pct")
PR("p_auto80", "Automotive share of Transportation FY16", 80, "Segment description (summary)", "FY2016", unit="pct", text_contains="about 80 percent")
PR("p_auto90", "Automotive share of Transportation FY21", 90, "Segment description (summary)", "FY2021", unit="pct", text_contains="more than 90 percent")
A("a_fy22_10m", "FY22 SPGI period length (months)", 10, "D", "analysis/SYNTHESIS.md", "caveats", "FY22 is a ~10-month SPGI period")
A("a_alloc100", "S&P allocations in carve-out (~$m)", 100, "C", "analysis/SYNTHESIS.md", "caveats", "The carve-out includes ~$100m of S&P allocations")
A("a_excl", "Adj. EBITDA exclusions 10 -> 6", "10 -> 6", "D", "analysis/SYNTHESIS.md", "caveats", "shrank from 10 to 6 exclusions")
A("a_lfl", "Like-for-like growth step-down", "~10% (2015-22) / ~8.5% / ~7%", "C", "analysis/SYNTHESIS.md", "Inference", "growth has stepped down from ~10% (2015–22) to ~8.5% (2023–25) to ~7% (2026)")
A("a_bear_frame", "Bear framing: 6-7% grower, ~39% margin, 2.7x", "6-7 / 39 / 2.7", "C", "analysis/D11_premortem.md", "section 2 inference", "6–7% grower with ~39% margins and 2.7x leverage")
A("a_txn57", "Stand-up transaction costs 6M-26", 57, "D", "analysis/QUALITATIVE.md", "section 9 (10Q p.17)", "$21m in Q1-26, $57m in 6M-26", unit="usd_m")
C("c_ni_6m_yoy", "Net income 6M y/y", -12.2, "(ni_6M-2026/ni_6M-2025-1)*100", unit="pct")
C("c_growth_ratio", "CARFAX vs B2B revenue growth FY23-25 (x)", 2.5, "(carfax_rev_FY2025/carfax_rev_FY2023-1)/(b2b_rev_FY2025/b2b_rev_FY2023-1)", unit="x")
C("c_margin_gap", "CARFAX minus B2B Adj. EBITDA margin FY25 (pt)", 14.5, "c_carfax_m_FY2025-c_b2b_m_FY2025", unit="pt")
C("c_mix_sum", "CARFAX product mix total", 101, "pp_adv+pp_fco+pp_list+pp_intl", unit="pct", decimals=0)
C("c_cpn29", "2029 notes cash coupon", 32.8, "n29*n29c/100")
C("c_cpn31", "2031 notes cash coupon", 35.4, "n31*n31c/100")
C("c_cpn36", "2036 notes cash coupon", 42.4, "n36*n36c/100")
N("n_pay19", "10/A approximate payment to S&P Global", 1900, "approximate cash payment to S&P Global from senior notes proceeds (printed as approximately $1.9 billion)", "Q1-2026")
A("a_revolver", "Revolver size", 500, "D", "analysis/QUALITATIVE.md", "section 9 (10A p.363)", "$500m, signed 2026-05-06", unit="usd_m")
A("a_cov", "Revolver max net leverage", "3.50x / 4.00x", "D", "analysis/QUALITATIVE.md", "section 9", "maximum net leverage 3.50x (4.00x step-up)")
A("a_cov_ae", "Adj. EBITDA / interest", 6.5, "C", "analysis/D3_group_decomposition.md", "section 3", "711 / 110 = 6.5x", unit="x")
A("a_cov_op", "Normalized OP / interest", 3.2, "C", "analysis/D3_group_decomposition.md", "section 3", "353 / 110 = 3.2x", unit="x")
A("a_dtl", "Cash tax above provision", "89 / 12 yrs", "IR", "transcripts/TARGETS_TIMELINE.md", "DTL row", "~$89M/yr above provision for 12 yrs")
A("a_dppa", "DPPA custodianship", "three decades", "D", "analysis/QUALITATIVE.md", "section 4", "in place for over three decades")
A("a_am3200", "automotiveMastermind dealers", 3200, "IR", "analysis/D2_unit_economics.md", "(c)", "3,200 dealers [IR]", unit="count")
A("a_products", "Products per dealer", "1.5-2", "IR", "analysis/D2_unit_economics.md", "(a)", '"between one and a half and two"')
PP("pp_roi", "Claimed dealer ROI", "10-15x", 68, "ROI (printed 10-15x)", "2023", unit="text")
PP("pp_turn", "Faster inventory turn (claimed)", 9, 68, "Faster inventory turn", "2023", unit="pct")
S("k_analysts", "Forecasting analyst team", 195, "Forecasting analyst team (experts)", "FY2025", unit="count")
A("a_payout_rng", "Payout on standalone normalized NI", "34-44%", "C", "analysis/SYNTHESIS.md", "finding 4", "is actually 34–44%")
A("a_fred_metric", "Fredericks STI metric", 100, "D", "analysis/D5_incentives.md", "section 2.2", "**100% CARFAX U.S. EBITA**", unit="pct")
A("a_fred_beat", "CARFAX U.S. EBITA vs target", 102.6, "C", "analysis/D5_incentives.md", "section 2.2", "102.6% of target", unit="pct")
A("a_psu_floor", "CARFAX PSU floor", 50, "D", "analysis/D5_incentives.md", "section 2.3", "(the floor is 50%)", unit="pct")
A("a_sev", "CEO CIC severance multiple", 2, "D", "analysis/D5_incentives.md", "section 3.4", "2× (base + target bonus)", unit="x")
A("a_lfl_cut", "Like-for-like FY26 cut (pt)", "0.9-1.6", "C", "analysis/D4_disclosure_changes.md", "section 4", "~**0.9–1.6 pt**")
A("a_head_cut", "Headline FY26 cut (pt)", "0.6-1.3", "C", "analysis/D4_disclosure_changes.md", "section 4", "0.6–1.3 pt")
A("a_reset", "Reset margin base", 39.1, "IR", "analysis/D4_disclosure_changes.md", "section 9", "39.1-ish%", unit="pct")
A("a_50bp", "Margin expansion target (bp/yr)", 50, "IR", "analysis/D4_disclosure_changes.md", "section 9", "~50bps annual margin expansion target", unit="bp")
A("a_nrr", "NRR description", 100, "IR", "analysis/D4_disclosure_changes.md", "section 10", '"meaningfully north of 100%"', unit="pct")
A("a_mfg", "Manufacturing growth Q3-25", -3, "IR", "analysis/D4_disclosure_changes.md", "section 0", "−3% Q3-25", unit="pct")
A("a_2h_growth", "Implied 2H-26 revenue growth", "6.3-8.0", "C", "analysis/D10_guidance_vs_execution.md", "section 3", "**+6.3%** | **+8.0%**")
A("a_recast", "Q2-25 Adj. EBITDA recast", "186 -> 188", "D", "analysis/D3_group_decomposition.md", "section 1", "186 → **recast** to 188")
A("a_cut1pt", "FY26 cut like-for-like (~pt)", 1, "C", "analysis/SYNTHESIS.md", "honest counters", "The FY26 cut is ~1pt like-for-like", unit="pt")
A("a_12m", "Recovery period after 2020 (months)", 12, "D", "analysis/D11_premortem.md", "section 3", "recovery came within 12 months", unit="months")
C("c_fcf_cover", "Standalone FCF / dividend (x)", 5.2, "c_fcf_standalone/c_div", unit="x")
A("a_canon", "Canonical cells / collisions", "390 / 0", "D", "deliverables/PART_A_SUMMARY.md", "verification counts", "390 primary cells; 0 collisions")
A("a_quartr6", "Quartr Q2-26 cross-check", "6 of 6", "D", "deliverables/PART_A_SUMMARY.md", "verification counts", "matched 6 of 6")
A("a_lev50", "Leverage per $50m EBITDA shortfall", "0.15-0.2x", "C", "analysis/D11_premortem.md", "table row 7", "$50m of EBITDA shortfall is ≈0.15–0.2x")
S("k_recall_FY24", "Lower recall activity FY24", -15, "Lower recall activity (non-subscription)", "FY2024")
C("c_nonsub_share", "Non-subscription share FY25", 18.5, "(rev_FY2025-sub_FY2025)/rev_FY2025*100", unit="pct")
A("a_25claim", "Management dividend claim: 25% of normalized GAAP NI", 25, "IR", "transcripts/TARGETS_TIMELINE.md", "Dividend row", "25% of normalised GAAP NI", unit="pct")
A("a_150bp", "Standalone cost ~150bp (high end)", 150, "IR", "transcripts/TARGETS_TIMELINE.md", "Standalone run-rate cost row", "~150bp of margin vs FY25 = **high end**", unit="bp")
A("a_reset_mo", "Reset period 12-18 months", "12-18", "IR", "transcripts/TARGETS_TIMELINE.md", "Margin expansion row", "after a 12–18-month reset")
A("a_sleeve19", "Transactional sleeve share", 19, "D", "analysis/D9_demand_drivers.md", "section 0", "sleeve (~19% of revenue [D])", unit="pct")
A("a_lev50m", "EBITDA shortfall step", 50, "C", "analysis/D11_premortem.md", "table row 7", "Every $50m of EBITDA shortfall", unit="usd_m")
A("a_rpo78", "RPO at 12/31/25", 78, "D", "analysis/D2_unit_economics.md", "(c)", "RPO / FY25 subscription revenue = 78 ÷ 1,426 = 5.5%", unit="usd_m")
C("c_rpo_ratio", "RPO / FY25 subscription revenue", 5.5, "a_rpo78/sub_FY2025*100", unit="pct")
G = [("g23r", "6.5–8.5% (Feb-23)"), ("g23r2", "9.0–10.0% (Q3-23)"), ("g23m", "38.5–39.5% (Q1-23)"), ("g24r", "8.5–10.0% (Feb-24)"),
     ("g24r2", "8.0–8.5% (Q3-24, pos.)"), ("g24m", "38.5–39.0% (Q3-24)"), ("g25r", "7.0–8.5% (Feb-25)"), ("g25r2", "↑ 8–9% (Q3-25)"),
     ("g25m", "39.5–40% (Q3-25)"), ("ga23m", "**38.8%** [D]"), ("ga24m", "**39.0%** [D]"), ("ga23r", "**+10%** [D]"), ("ga25r", "**8.6%** [D]"),
     ("gmiss", "missed by 110–310 bp"), ("gsa", "$20–25m (ID)"), ("got", "$75–100m (ID)"), ("got2", "$75–110m (10Q)"), ("glev", "≤2.5x target")]
for gid, ev in G:
    A(f"a_{gid}", f"Guidance scorecard: {ev}", ev.replace("*", "").replace(" [D]", ""), "D", "analysis/D10_guidance_vs_execution.md", "section 1 scorecard", ev)

# =============================================================================
# QUOTES (verbatim; fact_check verifies each string appears in transcripts/*.md)
# =============================================================================
QUOTES = {
    "q_archive": {"text": "some of that data that's seven years old, 12 years old, 15 years old just doesn't exist anymore anywhere else.",
                  "who": "Bill Eager (CEO), Q2-26 call, 2026-08-07", "file": "transcripts/MBGL_2026-08-07_q2-2026-earnings-call.md"},
    "q_sources": {"text": "Every one of those 177,000 sources are contractual relationships that are slow to replicate.",
                  "who": "Jeremy Morehouse (Head of AI Office), Investor Day, 2026-05-12", "file": "transcripts/MBGL_2026-05-12_investor-day.md"},
    "q_cpo": {"text": "In the CPO area, we have 36 OEMs that will not certify a car without a CARFAX report",
              "who": "Scott Fredericks (President, CARFAX), Investor Day, 2026-05-12", "file": "transcripts/MBGL_2026-05-12_investor-day.md"},
    "q_brandz": {"text": "You want to put in brand Z in front of them, the dealer loses confidence with the consumer.",
                 "who": "Scott Fredericks (President, CARFAX), Investor Day, 2026-05-12", "file": "transcripts/MBGL_2026-05-12_investor-day.md"},
    "q_value": {"text": "The majority of that is in value.",
                "who": "Matt Calderone (CFO), Investor Day, 2026-05-12, on core 5-7% growth", "file": "transcripts/MBGL_2026-05-12_investor-day.md"},
    "q_cars": {"text": "Cars continue to go up. The cost of the CARFAX report as a percent of that continues to decline.",
               "who": "Scott Fredericks (President, CARFAX), Investor Day, 2026-05-12", "file": "transcripts/MBGL_2026-05-12_investor-day.md"},
    "q_timing": {"text": "The preponderance of our pricing actions take effect early in the year",
                 "who": "Matt Calderone (CFO), Q2-26 call, 2026-08-07", "file": "transcripts/MBGL_2026-08-07_q2-2026-earnings-call.md"},
    "q_nrr": {"text": "We actually had an NRR number in the presentation early on. We pulled it.",
              "who": "Matt Calderone (CFO), Investor Day, 2026-05-12", "file": "transcripts/MBGL_2026-05-12_investor-day.md"},
    "q_software": {"text": "We're not a software company, right?",
                   "who": "Matt Calderone (CFO), Investor Day, 2026-05-12", "file": "transcripts/MBGL_2026-05-12_investor-day.md"},
    "q_2028": {"text": "So we're probably not going to get to the full 50 basis point expansion target until 2028.",
               "who": "Matt Calderone (CFO), Goldman Sachs Communacopia, 2026-09-10", "file": "transcripts/MBGL_2026-09-10_goldman-sachs-communacopia.md"},
    "q_cut": {"text": "we are lowering our full year revenue guidance to 6.9%-7.7% growth for the year.",
              "who": "Bill Eager (CEO), Q2-26 call, 2026-08-07", "file": "transcripts/MBGL_2026-08-07_q2-2026-earnings-call.md"},
    "q_twoyes": {"text": "You're, in essence, getting two yeses in order to put those products in versus selling them à la carte, where you need to get to one yes.",
                 "who": "Bill Eager (CEO), Q2-26 call, 2026-08-07", "file": "transcripts/MBGL_2026-08-07_q2-2026-earnings-call.md"},
    "q_acyclical": {"text": "The point of this chart is we are not just counter-cyclical, we're relatively acyclical.",
                    "who": "Matt Calderone (CFO), Investor Day, 2026-05-12", "file": "transcripts/MBGL_2026-05-12_investor-day.md"},
    "q_firewall": {"text": "the majority of it's sitting behind a firewall or a paywall somewhere.",
                   "who": "Bill Eager (CEO), Goldman Sachs Communacopia, 2026-09-10", "file": "transcripts/MBGL_2026-09-10_goldman-sachs-communacopia.md"},
}

# =============================================================================
# SLIDES
# =============================================================================
NAVY, TEAL, BLUE, LTEAL, GREY, AMBER, RED = "1F3864", "0E7C86", "2E75B6", "7FC4CB", "8C8C8C", "C9861A", "B0413E"

SLIDES = []


def slide(**kw):
    SLIDES.append(kw)


# 1 ---------------------------------------------------------------- title
slide(layout="title", kicker="PART E RESEARCH DECK",
      title="Mobility Global (MBGL): a wide-moat vehicle-data utility being priced for a growth rate it no longer prints",
      subtitle="CARFAX + B2B carve-out from S&P Global (spin 2026-07-01). Financials as originally reported, USD millions unless stated.",
      meta=["Prepared 2026-10-06", "Evidence tiers: [D] disclosed  [C] computed  [E] estimate  [IR] management verbal",
            "Built from analysis/SYNTHESIS.md, D1-D12, canonical/primary.csv and extraction/*.csv"],
      chips=[{"value": "$1,750m", "label": "FY25 revenue [D]"}, {"value": "40.6%", "label": "FY25 Adj. EBITDA margin [C]"},
             {"value": "$461m", "label": "FY25 free cash flow [D]"}, {"value": "6.9-7.7%", "label": "FY26 revenue growth guide [D]"}],
      sources=["analysis/SYNTHESIS.md", "deliverables/PART_A_SUMMARY.md", "canonical/primary.csv", "extraction/segments_kpi.csv"],
      fact_ids=["rev_FY2025", "ae_FY2025", "c_m_FY2025", "fcf_FY2025", "g_gr_lo", "g_gr_hi"])

# 2 ---------------------------------------------------------------- executive summary
slide(layout="content", kicker="EXECUTIVE SUMMARY",
      title="The CARFAX moat is real and widening, but growth is now price-led and the margin story keeps resetting",
      elements=[
          {"type": "cards", "box": [0.45, 1.5, 8.35, 5.15], "cols": 1, "rows": 5, "gap": 0.1, "title_size": 12.5, "body_size": 11,
           "items": [
               {"title": "1  Growth is mostly price, and new business is fading", "tag": "D/C",
                "body": "Price was ~$36m of the $64m 6M-26 revenue increase (~4.2pt of 7.5% growth); new business fell from ~$12m (Q1) to ~$8m (Q2). The Form 10/A had called Q1 growth \"new business\"."},
               {"title": "2  The CARFAX moat is wide and widening; B2B's is moderate", "tag": "D/C",
                "body": "177k+ sources and 38bn+ records (records +9.3%/yr since FY16); organic growth beat industry units in 10 of 11 years. B2B grew +3.1% / +5.9% with -18% FY25 flow-through."},
               {"title": "3  The margin narrative keeps resetting", "tag": "D/C/IR",
                "body": "SPGI's 41-43% target was missed (39.9% FY25); standalone and one-time costs drifted to the top of their ranges; +50bp/yr expansion now starts in 2028."},
               {"title": "4  The spin changes earnings power, not cash power", "tag": "C",
                "body": "Interest rises from $13m to ~$110m (~31% of normalized OP). Standalone normalized NI is ~$171m vs $220m carve-out; the dividend is ~41% of it but only ~19% of FCF."},
               {"title": "5  Disclosure retreated as metrics weakened; pay is loosely tied to performance", "tag": "D",
                "body": "NRR pulled, organic growth no longer printed, segment measure switched the quarter B2B OP fell to $3m. PSUs became time-vested RSUs; no TSR metric; insiders <1%."},
           ]},
          {"type": "panel", "box": [9.05, 1.5, 3.85, 5.15], "fill": "EEF3F8"},
          {"type": "text", "box": [9.25, 1.62, 3.5, 0.4], "size": 13, "bold": True, "color": NAVY, "text": "Bottom line"},
          {"type": "bullets", "box": [9.25, 2.05, 3.5, 3.0], "size": 11.5, "items": [
              {"text": "Likeliest loss: a slow de-rating of a 6-7% grower with ~39% margins and 2.7x gross leverage, not a moat collapse [Inference]."},
              {"text": "Like-for-like growth has stepped down: ~10% (2015-22) to 8.6% (FY23-25) to ~7% (FY26 guide)."},
              {"text": "What would change our mind: printed dealer-location, retention and price-per-location KPIs."},
          ]},
          {"type": "kpis", "box": [9.25, 5.1, 3.5, 1.4], "cols": 2, "value_size": 20, "items": [
              {"value": "8.6%", "label": "FY23-25 CAGR", "tier": "C"},
              {"value": "6.9-7.7%", "label": "FY26 guide (cut Aug-7)", "tier": "D"},
          ]},
      ],
      sources=["analysis/SYNTHESIS.md", "analysis/D1_moat.md", "analysis/D3_group_decomposition.md", "analysis/D4_disclosure_changes.md",
               "analysis/D5_incentives.md", "analysis/D7_pricing.md", "extraction/segments_kpi.csv (10Q p.27)", "canonical/primary.csv"],
      fact_ids=["a_50bp", "a_lfl", "a_bear_frame", "c_q1_drev", "k_price_6M", "c_6m_drev", "c_price_pts_6m", "c_1h_growth", "c_q1_nb", "k_nbq_Q2", "k_sources", "k_records", "c_rec_cagr",
                "a_beat_years", "c_b2b_g24", "c_b2b_g25", "ft_b2b_FY25", "a_spgi_target", "a_spgi_m25", "int_FY2025", "b_interest",
                "c_int_share", "b_ni", "ni_FY2025", "c_payout_fy25", "c_div_fcf", "a_b2b_op_q2", "c_rev_cagr", "g_gr_lo", "g_gr_hi", "a_gross_lev"])

# 3 ---------------------------------------------------------------- business at a glance
slide(layout="content", kicker="BUSINESS AT A GLANCE",
      title="A $1.75bn VIN-keyed data utility: 81% subscription, two-thirds CARFAX, and roughly 60% paid for by dealers",
      elements=[
          {"type": "kpis", "box": [0.45, 1.5, 7.6, 2.3], "cols": 4, "value_size": 24, "items": [
              {"value": "$1,750m", "label": "FY25 revenue", "tier": "D"},
              {"value": "$711m", "label": "FY25 Adj. EBITDA (40.6%)", "tier": "D/C"},
              {"value": "$461m", "label": "FY25 free cash flow", "tier": "D"},
              {"value": "81%", "label": "Subscription share", "tier": "C"},
              {"value": "177k+", "label": "Data sources", "tier": "D"},
              {"value": "38bn+", "label": "Vehicle history records", "tier": "D"},
              {"value": "40k+", "label": "CARFAX dealer customers", "tier": "D"},
              {"value": "17%", "label": "International revenue", "tier": "C"},
          ]},
          {"type": "panel", "box": [0.45, 4.0, 7.6, 2.65], "fill": "F2F2F2"},
          {"type": "text", "box": [0.65, 4.08, 7.2, 0.35], "size": 12.5, "bold": True, "color": NAVY, "text": "Two segments, one dataset"},
          {"type": "bullets", "box": [0.65, 4.45, 7.25, 2.15], "size": 11.5, "items": [
              {"head": "CARFAX (65% of revenue):", "text": " Advantage vehicle-history reports, Listings, Car Care / For Life, and BIG for lenders and insurers. FY25 segment Adj. EBITDA margin 46.9%."},
              {"head": "B2B (35%):", "text": " automotiveMastermind, Polk audiences and recall, Market Scan, and Strategy & Planning forecasts. FY25 margin 32.4%."},
              {"head": "Model is B2B2C:", "text": " the consumer creates the demand; the dealer pays. Dealers ~60% and OEMs ~10% of revenue per the filing."},
          ]},
          {"type": "chart", "box": [8.3, 1.5, 4.6, 5.15], "chart": "doughnut", "title": "FY25 revenue by customer type (deck basis)", "tier": "D",
           "categories": ["Dealer (B2B & CARFAX)", "OEM & supplier", "Financial / consumer / other"],
           "series": [{"name": "Share", "facts": ["pp_dealer", "pp_oem", "pp_fin"]}], "number_format": "0\"%\"",
           "colors": [NAVY, TEAL, LTEAL], "legend": "bottom",
           "note": "Filing basis differs: dealers ~60%, OEMs ~10% (10A p.299)."},
      ],
      sources=["canonical/primary.csv", "extraction/segments_kpi.csv (10A p.262-263, 358-361, 462-463)", "extraction/presentations.csv (ID s.10)", "analysis/QUALITATIVE.md §1-3"],
      fact_ids=["a_filing_mix", "pp_carfax_seg", "pp_b2b_seg", "rev_FY2025", "ae_FY2025", "c_m_FY2025", "fcf_FY2025", "sub_FY2025", "c_sub_share", "k_sources", "k_records", "k_dealers",
                "intl_FY2025", "c_intl_share", "c_carfax_share", "c_carfax_m_FY2025", "c_b2b_m_FY2025", "pp_dealer", "pp_oem", "pp_fin"])

# 4 ---------------------------------------------------------------- history / eras
slide(layout="content", kicker="HISTORY",
      title="Three corporate parents since 2013: every change of owner breaks the comparability of the numbers",
      elements=[
          {"type": "timeline", "box": [0.45, 1.5, 12.45, 3.2],
           "eras": [
               {"label": "IHS / IHS Markit: Transportation segment (FY14-FY21, Nov FYE)", "start": 2013.0, "end": 2022.15, "color": GREY},
               {"label": "S&P Global: Mobility segment (FY22-FY25)", "start": 2022.15, "end": 2026.0, "color": BLUE},
               {"label": "MBGL", "start": 2026.0, "end": 2027.0, "color": TEAL},
           ],
           "start": 2013.0, "end": 2027.0,
           "events": [
               {"x": 2013.0, "date": "2013", "label": "IHS buys R.L. Polk, incl. CARFAX", "pos": "up", "level": 1},
               {"x": 2015.95, "date": "Dec-2015", "label": "CARPROOF (Canada), $459m", "pos": "down", "level": 1},
               {"x": 2016.55, "date": "Jul-2016", "label": "IHS / Markit merger", "pos": "up", "level": 1},
               {"x": 2017.7, "date": "Sep-2017", "label": "automotiveMastermind (78%)", "pos": "down", "level": 2},
               {"x": 2019.9, "date": "Dec-2019", "label": "Aerospace & Defense sold", "pos": "up", "level": 1},
               {"x": 2022.15, "date": "Feb-2022", "label": "S&P Global / IHS Markit merger", "pos": "down", "level": 1},
               {"x": 2023.12, "date": "Feb-2023", "label": "Market Scan acquired ($223m)", "pos": "up", "level": 1},
               {"x": 2025.33, "date": "Apr-2025", "label": "Spin announced", "pos": "down", "level": 2},
               {"x": 2026.4, "date": "May-2026", "label": "Form 10/A; $2.0bn notes issued", "pos": "up", "level": 1},
               {"x": 2026.5, "date": "Jul-1-2026", "label": "Distribution; NYSE: MBGL", "pos": "down", "level": 1},
           ]},
          {"type": "table", "box": [0.45, 4.85, 12.45, 1.8], "font_size": 10.5, "col_widths": [2.0, 3.1, 3.6, 3.75],
           "columns": ["Series", "Period / basis", "Why it is not comparable", "Where used in this deck"],
           "rows": [
               ["IHS Transportation [D]", "FY14-FY21, Nov FYE, IHS Adj. EBITDA", "Includes Maritime & Trade; Jane's to 2019; automotive ~80% to >90%", "Slide 7 only (separate chart)"],
               ["SPGI Mobility [D]", "FY22 (~10 months) to FY25, adj. OP margin", "Different margin measure; FY22 partial year", "Guidance scorecard (slide 15)"],
               ["Carve-out [D]", "FY23-FY25 + 6M, Form 10/A and 10-Q", "Includes ~$100m of S&P allocations; Adj. EBITDA definition changed Q2-26", "Core financial slides"],
           ]},
      ],
      sources=["analysis/QUALITATIVE.md §11", "deliverables/PART_A_SUMMARY.md (structural breaks)", "extraction/predecessor_NOTES.md", "analysis/SYNTHESIS.md (caveats)"],
      fact_ids=["a_carproof", "a_mktscan", "a_am78", "n_total", "p_auto80", "p_auto90", "a_fy22_10m", "a_alloc100", "a_excl", ])

# 5 ---------------------------------------------------------------- segments & mix
slide(layout="content", kicker="SEGMENTS & REVENUE MIX",
      title="CARFAX is two-thirds of revenue and grew ~2.5x faster than B2B over FY23-25, at a ~15pt higher margin",
      elements=[
          {"type": "chart", "box": [0.45, 1.5, 6.1, 4.0], "chart": "column_stacked", "title": "Revenue by segment, $m", "tier": "D",
           "categories": ["FY23", "FY24", "FY25"],
           "series": [{"name": "CARFAX", "facts": ["carfax_rev_FY2023", "carfax_rev_FY2024", "carfax_rev_FY2025"], "color": NAVY},
                      {"name": "B2B", "facts": ["b2b_rev_FY2023", "b2b_rev_FY2024", "b2b_rev_FY2025"], "color": LTEAL}],
           "number_format": "#,##0", "legend": "bottom", "label_pos": "ctr"},
          {"type": "chart", "box": [6.8, 1.5, 6.1, 2.55], "chart": "bar", "title": "CARFAX FY25 revenue by product (deck, sums to 101%)", "tier": "D",
           "categories": ["Advantage (VHR)", "Financial / consumer / other", "Listings", "International"],
           "series": [{"name": "% of CARFAX", "facts": ["pp_adv", "pp_fco", "pp_list", "pp_intl"], "color": TEAL}],
           "number_format": "0\"%\"", "legend": "none", "label_pos": "outEnd", "reverse": True},
          {"type": "table", "box": [6.8, 4.2, 6.1, 1.35], "font_size": 10, "col_widths": [1.3, 1.2, 1.2, 1.2, 1.2],
           "columns": ["Segment", "Growth FY24", "Growth FY25", "Growth 6M-26", "Adj. EBITDA margin FY25"],
           "rows": [["CARFAX", "+12.0%", "+9.9%", "+8.2%", "46.9%"], ["B2B", "+3.1%", "+5.9%", "+6.1%", "32.4%"]],
           "tier": "C"},
          {"type": "callout", "box": [0.45, 5.7, 12.45, 0.95], "size": 11.5,
           "text": "B2B is 74% Marketing & Sales (aM, Polk audiences, Market Scan) and 26% Strategy & Planning [D, deck s.34]. Revenue by brand, product or B2B line is not in the filings. CARFAX margin rose from 45.5% to 48.0% (6M-26); B2B's fell from 35.4% to 32.4% in FY25 [C]."},
      ],
      sources=["extraction/segments_kpi.csv (10A p.359-361, 461-462; 10Q p.14)", "extraction/presentations.csv (ID s.34, s.57)", "analysis/D2_unit_economics.md (d)"],
      fact_ids=["c_growth_ratio", "c_margin_gap", "c_mix_sum", "carfax_rev_FY2023", "carfax_rev_FY2024", "carfax_rev_FY2025", "b2b_rev_FY2023", "b2b_rev_FY2024", "b2b_rev_FY2025",
                "pp_adv", "pp_fco", "pp_list", "pp_intl", "c_carfax_g24", "c_carfax_g25", "c_carfax_g6m", "c_b2b_g24", "c_b2b_g25", "c_b2b_g6m",
                "c_carfax_m_FY2025", "c_b2b_m_FY2025", "pp_ms", "pp_sp", "c_carfax_m_FY2023", "c_carfax_m_6M-2026", "c_b2b_m_FY2024"])

# 6 ---------------------------------------------------------------- financial history carve-out
slide(layout="content", kicker="FINANCIAL HISTORY: CARVE-OUT",
      title="Carve-out revenue compounded 8.6% and Adj. EBITDA 9.0% over FY23-25, with the margin flat at ~40-42%",
      elements=[
          {"type": "chart", "box": [0.45, 1.5, 7.4, 4.3], "chart": "column", "title": "Revenue and Adj. EBITDA, $m (carve-out, company definition)", "tier": "D",
           "categories": ["FY23", "FY24", "FY25", "6M-25", "6M-26"],
           "series": [{"name": "Revenue", "facts": ["rev_FY2023", "rev_FY2024", "rev_FY2025", "rev_6M-2025", "rev_6M-2026"], "color": NAVY},
                      {"name": "Adj. EBITDA", "facts": ["ae_FY2023", "ae_FY2024", "ae_FY2025", "ae_6M-2025", "ae_6M-2026"], "color": TEAL}],
           "number_format": "#,##0", "legend": "bottom", "label_pos": "outEnd", "gap": 60},
          {"type": "chart", "box": [8.1, 1.5, 4.8, 4.3], "chart": "line", "title": "Adj. EBITDA margin, %", "tier": "C",
           "categories": ["FY23", "FY24", "FY25", "6M-25", "6M-26"],
           "series": [{"name": "Adj. EBITDA margin", "facts": ["c_m_FY2023", "c_m_FY2024", "c_m_FY2025", "c_m_6M-2025", "c_m_6M-2026"], "color": TEAL}],
           "number_format": "0.0", "legend": "none", "label_pos": "t", "y_min": 36, "y_max": 44},
          {"type": "callout", "box": [0.45, 5.95, 12.45, 0.7], "size": 11,
           "text": "GAAP operating profit is only $339m (FY25) because ~$296m/yr of IHS Markit purchase amortization is pushed down. 6M-26 net income fell to $108m (-12%) on $57m of stand-up transaction costs. Q2-26 measure: 6 exclusions vs 10 at FY [D]."},
      ],
      sources=["canonical/primary.csv (IS.revenue)", "extraction/segments_kpi.csv (10A p.358 Adj. EBITDA recon; 10Q p.15 Note 7)", "deliverables/PART_A_SUMMARY.md"],
      fact_ids=["c_ni_6m_yoy", "a_txn57", "a_excl", "rev_FY2023", "rev_FY2024", "rev_FY2025", "rev_6M-2025", "rev_6M-2026", "ae_FY2023", "ae_FY2024", "ae_FY2025", "ae_6M-2025", "ae_6M-2026",
                "c_m_FY2023", "c_m_FY2024", "c_m_FY2025", "c_m_6M-2025", "c_m_6M-2026", "c_rev_cagr", "c_ae_cagr", "op_FY2025", "amort_FY2025",
                "ni_6M-2026", "ni_6M-2025"])

# 7 ---------------------------------------------------------------- predecessor
slide(layout="content", kicker="FINANCIAL HISTORY: PREDECESSOR (NON-COMPARABLE)",
      title="The IHS-era Transportation segment compounded revenue 10.8% to FY21, but on a broader scope that cannot be spliced to the carve-out",
      elements=[
          {"type": "banner", "box": [0.45, 1.45, 12.45, 0.42], "text": "NON-COMPARABLE SERIES: IHS Markit Transportation segment, Nov FYE, includes Maritime & Trade (and Jane's to 2019); IHS Adj. EBITDA definition. Do not splice to slides 6 and 8.", "fill": "FBEFD9", "color": "7A4E00"},
          {"type": "chart", "box": [0.45, 2.0, 7.4, 3.9], "chart": "column", "title": "IHS Transportation revenue and Adj. EBITDA, $m (FY14-FY21)", "tier": "D",
           "categories": ["FY14", "FY15", "FY16", "FY17", "FY18", "FY19", "FY20", "FY21"],
           "series": [{"name": "Revenue", "facts": [f"p_rev_FY20{y}" for y in range(14, 22)], "color": GREY},
                      {"name": "Adj. EBITDA", "facts": [f"p_ae_FY20{y}" for y in range(14, 22)], "color": "4F6D8F"}],
           "number_format": "#,##0", "legend": "bottom", "label_pos": "outEnd", "gap": 50, "label_size": 8},
          {"type": "chart", "box": [8.1, 2.0, 4.8, 3.9], "chart": "line", "title": "IHS Adj. EBITDA margin, %", "tier": "C",
           "categories": ["FY14", "FY15", "FY16", "FY17", "FY18", "FY19", "FY20", "FY21"],
           "series": [{"name": "Margin", "facts": [f"p_m_FY20{y}" for y in range(14, 22)], "color": "4F6D8F"}],
           "number_format": "0.0", "legend": "none", "label_pos": "t", "y_min": 30, "y_max": 50},
          {"type": "callout", "box": [0.45, 6.0, 12.45, 0.68], "size": 11,
           "text": "Revenue CAGR 10.8%, Adj. EBITDA CAGR 15.6% [C]. The 47.6% FY21 margin does not mean margins later \"fell\" to ~40%: scope, FYE, allocations and definitions all differ. SPGI Mobility then printed $1,142m (FY22, ~10 months) to $1,747m (FY25) [D]."},
      ],
      sources=["extraction/predecessor.csv (INFO 10-K FY2016-FY2021 segment notes; SPGI 10-K FY2022-25 Mobility table)", "extraction/predecessor_NOTES.md", "analysis/SYNTHESIS.md (caveats)"],
      fact_ids=[f"p_rev_FY20{y}" for y in range(14, 22)] + [f"p_ae_FY20{y}" for y in range(14, 22)] + [f"p_m_FY20{y}" for y in range(14, 22)] +
               ["c_p_rev_cagr", "c_p_ae_cagr", "spgi_rev_FY2022", "spgi_rev_FY2025"])

# 8 ---------------------------------------------------------------- FCF
slide(layout="content", kicker="FREE CASH FLOW",
      title="Cash conversion of 63-65% is structural, but 1H-26 fell to 46% as spin costs and working capital hit",
      elements=[
          {"type": "chart", "box": [0.45, 1.5, 7.0, 4.25], "chart": "column", "title": "Free cash flow, $m (CFO less capex)", "tier": "D",
           "categories": ["FY23", "FY24", "FY25", "6M-25", "6M-26"],
           "series": [{"name": "Free cash flow", "facts": ["fcf_FY2023", "fcf_FY2024", "fcf_FY2025", "fcf_6M-2025", "fcf_6M-2026"], "color": NAVY}],
           "number_format": "#,##0", "legend": "none", "label_pos": "outEnd", "gap": 70},
          {"type": "chart", "box": [7.7, 1.5, 5.2, 2.6], "chart": "line", "title": "FCF conversion (FCF / Adj. EBITDA), %", "tier": "C",
           "categories": ["FY23", "FY24", "FY25", "6M-25", "6M-26"],
           "series": [{"name": "Conversion", "facts": ["c_conv_FY2023", "c_conv_FY2024", "c_conv_FY2025", "c_conv_6M-2025", "c_conv_6M-2026"], "color": AMBER}],
           "number_format": "0", "legend": "none", "label_pos": "t", "y_min": 30, "y_max": 75, "major_unit": 15},
          {"type": "table", "box": [7.7, 4.25, 5.2, 1.5], "font_size": 10, "col_widths": [1.6, 0.9, 0.9, 0.9, 0.9],
           "columns": ["", "FY23", "FY24", "FY25", "6M-26"],
           "rows": [["CFO, $m", "393", "427", "485", "189"], ["Capex, $m", "(18)", "(15)", "(24)", "(12)"], ["Capex / revenue", "1.2%", "0.9%", "1.4%", "1.3%"]],
           "tier": "D/C"},
          {"type": "callout", "box": [0.45, 5.9, 12.45, 0.78], "size": 11,
           "text": "FCF margin 25.3% to 26.3% (FY23-25) [C]; there is no capitalized-software asset, so FCF is not flattered. Standalone FCF ~$365m after after-tax interest and standalone costs [C/E], before ~$100m of one-time stand-up cash (about half capitalized) [IR]."},
      ],
      sources=["extraction/segments_kpi.csv (10A p.361 FCF recon; 10Q p.26)", "canonical/primary.csv (CF.cfo, CF.capex)", "extraction/presentations.csv (ID s.111)", "analysis/D2_unit_economics.md (e)", "analysis/D3_group_decomposition.md §5"],
      fact_ids=["fcf_FY2023", "fcf_FY2024", "fcf_FY2025", "fcf_6M-2025", "fcf_6M-2026", "c_conv_FY2023", "c_conv_FY2024", "c_conv_FY2025", "c_conv_6M-2025",
                "c_conv_6M-2026", "pp_conv_FY2023", "pp_conv_FY2024", "pp_conv_FY2025", "cfo_FY2023", "cfo_FY2024", "cfo_FY2025", "cfo_6M-2026",
                "capex_FY2023", "capex_FY2024", "capex_FY2025", "capex_6M-2026", "c_capint_FY2023", "c_capint_FY2024", "c_capint_FY2025", "c_capint_6M-2026",
                "c_fcfm_FY2023", "c_fcfm_FY2025", "c_fcf_standalone", "b_interest", "g_onetime"])

# 9 ---------------------------------------------------------------- capital structure
slide(layout="content", kicker="CAPITAL STRUCTURE POST-SPIN",
      title="$2.0bn of notes lift interest from $13m to ~$110m a year: earnings power changes, cash cover does not",
      elements=[
          {"type": "table", "box": [0.45, 1.5, 7.3, 2.3], "font_size": 11, "col_widths": [2.5, 1.5, 1.5, 1.8],
           "columns": ["Senior notes (issued 2026-05-29)", "Principal, $m", "Coupon", "Annual cash coupon, $m"],
           "rows": [["5.050% due 2029", "650", "5.050%", "32.8"], ["5.450% due 2031", "650", "5.450%", "35.4"],
                    ["6.050% due 2036", "700", "6.050%", "42.4"], ["Total / weighted", "2,000", "5.53%", "110.6"]],
           "bold_last": True, "tier": "D/C"},
          {"type": "kpis", "box": [8.0, 1.5, 4.9, 2.3], "cols": 2, "value_size": 22, "items": [
              {"value": "2.7x", "label": "Gross leverage at spin (target ~2.5x)", "tier": "IR"},
              {"value": "2.4x", "label": "Net leverage", "tier": "IR"},
              {"value": "$186m", "label": "Cash at 6/30/26", "tier": "D"},
              {"value": "$500m", "label": "Revolver, undrawn (to 2031)", "tier": "D"},
          ]},
          {"type": "chart", "box": [0.45, 4.0, 6.0, 2.65], "chart": "bar", "title": "Net interest as % of operating profit", "tier": "C",
           "categories": ["Carve-out FY25 ($13m / $339m)", "Standalone normalized (~$110m / $353m)"],
           "series": [{"name": "Interest / OP", "facts": ["c_int_share_co", "c_int_share"], "color": NAVY}],
           "number_format": "0.0\"%\"", "legend": "none", "label_pos": "outEnd", "reverse": True},
          {"type": "bullets", "box": [6.7, 4.0, 6.2, 2.65], "size": 11.5, "items": [
              {"head": "Use of proceeds:", "text": " $2.0bn dividend to S&P Global (the 10/A had said ~$1.9bn) [D]."},
              {"head": "Covenants:", "text": " revolver max net leverage 3.50x (4.00x step-up); notes not prepayable, so deleveraging relies on EBITDA growth [D/IR]."},
              {"head": "Coverage:", "text": " FY25 Adj. EBITDA / interest ~6.5x; standalone normalized OP / interest ~3.2x [C]."},
              {"head": "Tax:", "text": " ~$89m/yr cash tax above provision for ~12 years (IHS DTL) [IR]."},
          ]},
      ],
      sources=["extraction/notes.csv (10A p.337)", "canonical/primary.csv (BS.cash, BS.ltd, IS.int)", "analysis/D3_group_decomposition.md §3", "transcripts/TARGETS_TIMELINE.md", "analysis/QUALITATIVE.md §9"],
      fact_ids=["c_cpn29", "c_cpn31", "c_cpn36", "n_pay19", "a_revolver", "a_cov", "a_cov_ae", "a_cov_op", "a_dtl", "n29", "n31", "n36", "n29c", "n31c", "n36c", "n_total", "c_coupon", "c_wtd_coupon", "a_gross_lev", "a_net_lev", "cash_Q2", "ltd_Q2",
                "int_FY2025", "op_FY2025", "c_int_share_co", "c_int_share", "b_norm_op", "b_interest", "pp_gross_lev"])

# 10 --------------------------------------------------------------- moat architecture
slide(layout="content", kicker="MOAT ARCHITECTURE",
      title="Six interlocking moat elements; the decades-deep archive is the one a rival cannot buy",
      elements=[
          {"type": "cards", "box": [0.45, 1.5, 8.2, 5.15], "cols": 2, "rows": 3, "gap": 0.15, "title_size": 12.5, "body_size": 12,
           "items": [
               {"title": "Give-get data network", "tag": "D", "body": "177k+ sources, many exclusive; ~6m records added a day; 92k+ dealers and shops, 6,300 police agencies, 36 OEMs."},
               {"title": "An archive that cannot be rebuilt", "tag": "IR", "body": "38bn+ records. Old service history \"just doesn't exist anymore anywhere else\", per CEO Bill Eager."},
               {"title": "Two-sided brand", "tag": "D", "body": "96% in-market awareness; ~2m \"Show me the CARFAX\" requests a month [X]; $1.5bn of media since 2000."},
               {"title": "OEM lock-in", "tag": "D/IR", "body": "36 OEM CPO programs require the report; 100% of the top-40 carmakers buy MBGL data."},
               {"title": "Workflow embedding", "tag": "D", "body": "95 dealer-tool integrations; 17 of the top-20 banks and insurers; Market Scan in ~10,500 dealerships."},
               {"title": "Polk registration data (B2B)", "tag": "D", "body": "DMV-sourced under the DPPA; 13bn+ transaction records. Moderate moat: Experian and GlobalData offer low-cost alternatives."},
           ]},
          {"type": "chart", "box": [8.9, 1.5, 4.0, 3.15], "chart": "column", "title": "CARFAX VH records, bn", "tier": "D",
           "categories": ["FY16", "FY18", "FY19", "FY21", "FY25"],
           "series": [{"name": "Records", "facts": ["rec_FY2016", "rec_FY2018", "rec_FY2019", "rec_FY2021", "k_records"], "scale": [1, 1, 1, 1, 1e-9], "color": TEAL}],
           "number_format": "0", "legend": "none", "label_pos": "outEnd", "gap": 60},
          {"type": "panel", "box": [8.9, 4.8, 4.0, 1.85], "fill": "EEF3F8"},
          {"type": "bullets", "box": [9.05, 4.88, 3.75, 1.75], "size": 11, "items": [
              {"head": "Verdict:", "text": " wide moat in CARFAX, moderate in B2B [Inference]."},
              {"head": "Widening:", "text": " records +9.3%/yr and sources +6.5%/yr FY16-25 [C]."},
              {"head": "Weak spot:", "text": " ad spend +31% vs revenue +18% (FY23-25) [C]."},
          ]},
      ],
      sources=["analysis/D1_moat.md §2, §6", "extraction/segments_kpi.csv (10A p.262-272)", "extraction/predecessor.csv (INFO 10-K FY16/18/19/21 data scale)", "extraction/presentations.csv (ID s.18, s.66, s.67)", "transcripts/MBGL_2026-08-07_q2-2026-earnings-call.md"],
      fact_ids=["k_sources", "k_daily", "k_shops", "k_police", "k_oem_src", "k_records", "k_aware", "pp_showme", "pp_media", "k_cpo", "k_top40", "pp_integr",
                "k_banks", "k_mktscan", "k_txn", "rec_FY2016", "rec_FY2018", "rec_FY2019", "rec_FY2021", "c_rec_cagr", "c_src_cagr", "src_FY2016",
                "c_ad_growth", "c_rev_growth_2y", "ad_FY2023", "ad_FY2025"],
      quote_ids=["q_archive"])

# 11 --------------------------------------------------------------- data network flow diagram
slide(layout="content", kicker="DATA NETWORK",
      title="One VIN-level record, fed by 177k contributors and monetized four ways",
      elements=[
          {"type": "flow", "box": [0.45, 1.5, 12.45, 4.65],
           "left_title": "DATA CONTRIBUTORS (give)",
           "left": [
               {"title": "Dealers and service shops", "stat": "92,000+ in the network [D]"},
               {"title": "Police agencies", "stat": "6,300+ data partnerships [D]"},
               {"title": "OEMs (CPO programs)", "stat": "36 contribute data [D]"},
               {"title": "DMVs / governments", "stat": "DPPA custodian for over three decades [D]"},
           ],
           "center_title": "CARFAX / POLK ARCHIVE",
           "center": ["177,000+ sources [D]", "38bn+ vehicle history records [D]", "13bn+ transaction records [D]", "~832m unique VINs [D]", "2,000+ attributes per vehicle [D]", "~6m records added a day [D]"],
           "right_title": "WHO PAYS / USES (get)",
           "right": [
               {"title": "Dealers", "stat": "40,000+ CARFAX customers; ~60% of revenue [D]"},
               {"title": "Consumers", "stat": "~23m monthly visitors; 28m+ report views/mo [D]"},
               {"title": "OEMs and suppliers", "stat": "100% of top-40 carmakers; ~10% of revenue [D]"},
               {"title": "Lenders and insurers", "stat": "17 of top-20; underwriting +$13m FY25 [D]"},
           ],
           "feedback": "Give-get loop: shops receive Car Care traffic (53m+ users) and dealers receive consumer trust in return for their records"},
          {"type": "quote", "box": [0.45, 6.2, 12.45, 0.5], "quote": "q_sources", "size": 11},
      ],
      sources=["extraction/segments_kpi.csv (10A p.262-272, 340, 349)", "analysis/QUALITATIVE.md §1-4", "analysis/D1_moat.md §2", "transcripts/MBGL_2026-05-12_investor-day.md"],
      fact_ids=["a_filing_mix", "a_dppa", "k_shops", "k_police", "k_oem_src", "k_sources", "k_records", "k_txn", "k_vins", "k_attr", "k_daily", "k_dealers", "k_muv", "k_views",
                "k_top40", "k_banks", "k_underwrite_FY25", "k_carcare"],
      quote_ids=["q_sources"])

# 12 --------------------------------------------------------------- value prop
slide(layout="content", kicker="VALUE PROPOSITION BY CUSTOMER",
      title="The consumer creates the pricing power; the dealer, OEM and lender pay for it",
      elements=[
          {"type": "table", "box": [0.45, 1.5, 12.45, 4.45], "font_size": 10.5, "col_widths": [1.75, 1.45, 3.0, 3.25, 3.0],
           "columns": ["Customer", "Share of revenue", "What they care about", "What MBGL sells", "Evidence (tier)"],
           "rows": [
               ["Dealers (40k+ CARFAX customers)", "~60% filing; 62% deck", "Inventory turn and gross; consumer trust at the point of sale; service retention",
                "Advantage VHR, Listings, Car Care / For Life, Showroom; aM (3,200 dealers); Market Scan (~10,500)",
                "Claimed 10-15x ROI, ~9% faster turn (2023 internal study) [IR]; 1.5-2 products per dealer [IR]"],
               ["OEMs and suppliers", "~10% OEM filing; 20% OEM & supplier deck", "Share, loyalty, incentive efficiency; recall reach; production planning",
                "Polk reporting and audiences; Recall; Data Studio; Planning forecasts (195 analysts); CARFAX in 36 CPO programs",
                "100% of top-40 carmakers, 94% of top-100 suppliers [D]"],
               ["Lenders and insurers", "Part of 18% (deck)", "Collateral value, underwriting risk, fraud; VIN decoding at scale",
                "CARFAX BIG valuations; VIN Solutions APIs; DPPA-governed data",
                "17 of top-20 banks and insurers [D]; underwriting +$17m FY24, +$13m FY25 [D]"],
               ["Consumers (mostly not payers)", "Small: pay-per-report, not disclosed", "Avoiding a bad used car; service reminders; resale value",
                "VHR (usually free via the dealer); Car Care app; Listings",
                "96% awareness [D]; 53m+ Car Care users [D]; ~23m monthly US visitors [D]"],
           ], "tier": "D/IR"},
          {"type": "callout", "box": [0.45, 6.05, 12.45, 0.62], "size": 11,
           "text": "One dataset monetized four ways. Caveat: most value proof (ROI, turn, default reduction) comes from company studies; no ARPU, retention or churn is disclosed."},
      ],
      sources=["analysis/D6_value_prop.md §1", "extraction/segments_kpi.csv (10A p.263-272, 349)", "extraction/presentations.csv (ID s.10, s.68)", "analysis/K_session_tables.md (D6)"],
      fact_ids=["a_filing_mix", "a_am3200", "a_products", "pp_roi", "pp_turn", "k_analysts", "k_dealers", "pp_dealer", "pp_oem", "pp_fin", "k_mktscan", "k_top40", "k_top100sup", "k_banks", "k_underwrite_FY24", "k_underwrite_FY25",
                "k_aware", "k_carcare", "k_muv", "k_cpo"])

# 13 --------------------------------------------------------------- unit economics
slide(layout="content", kicker="UNIT ECONOMICS",
      title="Margins and flow-through are disclosed; price per rooftop, retention and churn are not",
      elements=[
          {"type": "chart", "box": [0.45, 1.5, 6.6, 3.9], "chart": "column", "title": "Incremental Adj. EBITDA flow-through (ΔAdj. EBITDA / Δrevenue), %", "tier": "C",
           "categories": ["FY24", "FY25", "6M-26"],
           "series": [{"name": "CARFAX", "facts": ["ft_carfax_FY24", "ft_carfax_FY25", "ft_carfax_6M"], "color": NAVY},
                      {"name": "B2B", "facts": ["ft_b2b_FY24", "ft_b2b_FY25", "ft_b2b_6M"], "color": AMBER}],
           "number_format": "0", "legend": "bottom", "label_pos": "outEnd", "gap": 80, "y_min": -30, "y_max": 90},
          {"type": "kpis", "box": [0.45, 5.55, 6.6, 1.1], "cols": 3, "value_size": 18, "items": [
              {"value": "~$17.1k", "label": "Advantage + Listings per dealer customer / yr", "tier": "C"},
              {"value": "~$10.8k", "label": "Advantage alone per dealer customer / yr", "tier": "C"},
              {"value": "<=$28.6k", "label": "All CARFAX revenue per dealer (upper bound)", "tier": "C"},
          ]},
          {"type": "twocol", "box": [7.3, 1.5, 5.6, 5.15],
           "left_title": "Disclosed", "left_color": TEAL,
           "left": ["Segment revenue, Adj. EBITDA, subscription split", "Dealer customer count (40k+, a floor)", "Price vs new-business $ (10-Q, from Q2-26)",
                    "Capex 0.9-1.4% of revenue", "RPO $78m at FY25 (~5.5% of subscription revenue); $102m at 6/30/26"],
           "right_title": "Not disclosed", "right_color": RED,
           "right": ["Price per location (the 10/A's own revenue driver)", "Enrolled locations over time", "NRR (pulled), gross retention, churn",
                     "Report volumes, consumer price", "Brand / country P&L; Europe losses"]},
      ],
      sources=["extraction/segments_kpi.csv (10A p.359-360; 10Q p.10, 14)", "extraction/presentations.csv (ID s.57)", "analysis/D2_unit_economics.md (a), (c), (d)", "analysis/K_session_tables.md (D2)"],
      fact_ids=["a_rpo78", "c_rpo_ratio", "ft_carfax_FY24", "ft_carfax_FY25", "ft_carfax_6M", "ft_b2b_FY24", "ft_b2b_FY25", "ft_b2b_6M", "c_per_dealer", "c_adv_dealer", "c_carfax_dealer",
                "c_adv_list", "k_dealers", "rpo_FY25_q2", "sub_FY2025", "c_capint_FY2024", "c_capint_FY2025"])

# 14 --------------------------------------------------------------- group decomposition & EPS bridge
slide(layout="content", kicker="EARNINGS POWER: STANDALONE BRIDGE",
      title="Standalone normalized NI is ~$171m (~$0.58/share), not $220m, so the \"25%\" payout is really ~34-44%",
      elements=[
          {"type": "waterfall", "box": [0.45, 1.5, 8.0, 4.4], "title": "FY25 carve-out NI to standalone normalized NI, $m", "tier": "C/E",
           "steps": [
               {"label": "Carve-out NI", "fact": "ni_FY2025", "kind": "total"},
               {"label": "+ Tax, interest", "fact": "b_taxint", "kind": "up"},
               {"label": "Operating profit", "fact": "b_op", "kind": "total"},
               {"label": "+ One-time items", "fact": "b_onetime", "kind": "up"},
               {"label": "- Standalone cost", "fact": "b_standalone", "kind": "down"},
               {"label": "Normalized OP", "fact": "b_norm_op", "kind": "total"},
               {"label": "- Interest", "fact": "b_interest", "kind": "down"},
               {"label": "- Tax @29.5%", "fact": "b_tax", "kind": "down"},
               {"label": "Normalized NI", "fact": "b_ni", "kind": "total"},
           ]},
          {"type": "table", "box": [8.7, 1.5, 4.2, 2.55], "font_size": 10, "col_widths": [2.2, 1.0, 1.0],
           "columns": ["Per share (294.8m shares)", "NI $m", "EPS $"],
           "rows": [["FY25 carve-out (illustrative)", "220", "0.75"], ["Standalone normalized, FY25 base", "171", "0.58"],
                    ["Standalone FY26 run-rate", "209", "0.71"], ["10-Q printed 6M-26 EPS", "108", "0.37"]], "tier": "D/C"},
          {"type": "bullets", "box": [8.7, 4.15, 4.2, 2.5], "size": 11, "items": [
              {"head": "Dividend:", "text": " $0.06 x 4 x 294.8m = $70.8m [C]: 41% of $171m, 34% of $209m."},
              {"head": "25% payout needs", "text": " ~$283m of NI [C]: only if half the after-tax amortization is added back."},
              {"head": "Cash is fine:", "text": " dividend ~19% of ~$365m standalone FCF [C]."},
          ]},
          {"type": "callout", "box": [0.45, 6.0, 8.0, 0.68], "size": 10.5,
           "text": "FY25 Adj. EBITDA identity: CARFAX $536m + B2B $197m - Corporate $22m = $711m [D]. S&P allocations of $112m (FY25) sit mostly inside segment costs [D]."},
      ],
      sources=["analysis/D3_group_decomposition.md §1, §4, §5", "canonical/primary.csv (IS.ni, IS.tax, IS.int, IS.eps_d)", "extraction/segments_kpi.csv (10A p.359; 10Q p.14)"],
      fact_ids=["a_25claim", "a_payout_rng", "ni_FY2025", "tax_FY2025", "int_FY2025", "b_taxint", "b_op", "b_onetime", "b_standalone", "b_norm_op", "b_interest", "b_pretax", "b_tax", "b_ni",
                "b_ni_fy26", "shares", "c_eps_norm", "c_eps_fy26", "c_eps_carve", "eps_6M26", "ni_6M-2026", "div_q", "c_div", "c_payout_fy25", "c_payout_fy26",
                "c_div_needed", "c_fcf_standalone", "c_div_fcf", "carfax_ae_FY2025", "b2b_ae_FY2025", "corp_ae_FY2025", "ae_FY2025", "a_alloc_FY25"])

# 15 --------------------------------------------------------------- guidance vs execution
slide(layout="content", kicker="GUIDANCE VS EXECUTION",
      title="Revenue guides were broadly met; margin targets were repeatedly missed, and the FY26 guide was cut 3 months after reaffirmation",
      elements=[
          {"type": "table", "box": [0.45, 1.5, 7.9, 3.75], "font_size": 10, "col_widths": [1.75, 2.15, 1.3, 1.35, 1.35],
           "columns": ["Year / item", "Initial guide (to final)", "Actual", "Verdict", "Basis"],
           "rows": [
               ["FY23 revenue", "6.5-8.5% (to 9.0-10.0%)", "+10%", "Beat", "SPGI [D]"],
               ["FY23 margin", "39-40% (to 38.5-39.5%)", "38.8%", "Missed-lowered", "SPGI adj. OP"],
               ["FY24 revenue", "8.5-10.0% (to 8.0-8.5%)", "+8%", "Missed-lowered", "SPGI [D]"],
               ["FY24 margin", "39-40% (to 38.5-39.0%)", "39.0%", "Missed-lowered", "SPGI adj. OP"],
               ["FY25 revenue", "7.0-8.5% (to 8-9%)", "+8.6%", "Beat", "SPGI [D]"],
               ["FY25 margin", "39-40% (to 39.5-40%)", "39.9%", "Met", "SPGI adj. OP"],
               ["2025/26 target", "41-43% adj. OP margin", "39.9%", "Missed 110-310bp", "SPGI ID 2022"],
               ["FY26 revenue", "7.5-9% OCC (to 6.9-7.7% rep.)", "1H +7.5%", "Cut", "MBGL [D]"],
           ], "verdict_col": 3, "tier": "D/C"},
          {"type": "table", "box": [8.6, 1.5, 4.3, 3.75], "font_size": 10, "col_widths": [1.5, 1.4, 1.4],
           "columns": ["Target drift", "Investor Day (May-12)", "Now (Aug / Sep)"],
           "rows": [["Standalone cost", "$20-25m", "~150bp = ~$26m"], ["One-time cost", "$75-100m", "$75-110m; ~50% capitalized"],
                    ["+50bp/yr margin", "after 12-18m reset", "full 50bp from 2028"], ["Leverage target", "<=2.5x gross", "\"2.5x-ish\"; 2.7x actual"]],
           "tier": "IR/D"},
          {"type": "callout", "box": [0.45, 5.4, 12.45, 0.72], "size": 11,
           "text": "At the May-12 reaffirmation, Q1-26 growth ex-FX was already ~7.4%, below the 7.5% floor [C]. The new guide implies a 2H-26 Adj. EBITDA margin of 37.9-38.9% vs 39.7% in 2H-25 [C]."},
          {"type": "quote", "box": [0.45, 6.2, 12.45, 0.5], "quote": "q_2028", "size": 11},
      ],
      sources=["analysis/D10_guidance_vs_execution.md §1-3", "analysis/D4_disclosure_changes.md §4, §7-9", "transcripts/TARGETS_TIMELINE.md", "extraction/segments_kpi.csv (8-K p.3 guidance)"],
      fact_ids=["a_150bp", "a_reset_mo", "a_g23r", "a_g23r2", "a_g23m", "a_g24r", "a_g24r2", "a_g24m", "a_g25r", "a_g25r2", "a_g25m", "a_ga23m", "a_ga24m", "a_ga23r", "a_ga25r", "a_gmiss", "a_gsa", "a_got", "a_got2", "a_glev", "a_reset", "a_50bp", "a_spgi_m25", "a_spgi_target", "g_gr_lo", "g_gr_hi", "c_1h_growth", "c_standalone_bp", "g_onetime", "a_gross_lev", "c_q1_occ",
                "c_2h_m_lo", "c_2h_m_hi", "c_2h25_m", "g_rev_lo", "g_rev_hi", "g_ae_lo", "g_ae_hi", "rev_6M-2026", "ae_6M-2026"],
      quote_ids=["q_2028"])

# 16 --------------------------------------------------------------- pricing
slide(layout="content", kicker="PRICING",
      title="Price drove ~56% of 1H-26 growth; new business faded from ~$12m in Q1 to ~$8m in Q2",
      elements=[
          {"type": "chart", "box": [0.45, 1.5, 6.6, 4.3], "chart": "column_stacked", "title": "Revenue increase y/y by driver, $m", "tier": "D/C",
           "categories": ["Q1-26 (implied)", "Q2-26", "6M-26"],
           "series": [{"name": "Price", "facts": ["c_q1_price", "k_price_Q2", "k_price_6M"], "color": NAVY},
                      {"name": "New business", "facts": ["c_q1_nb", "k_nbq_Q2", "k_nbq_6M"], "color": TEAL},
                      {"name": "Other", "facts": ["c_q1_other", "c_q2_other", "c_6m_other"], "color": "BFBFBF"}],
           "number_format": "0", "legend": "bottom", "label_pos": "ctr", "gap": 70},
          {"type": "table", "box": [7.3, 1.5, 5.6, 1.6], "font_size": 10, "col_widths": [2.0, 1.2, 1.2, 1.2],
           "columns": ["Points of growth", "Q1-26", "Q2-26", "6M-26"],
           "rows": [["Price", "~4.8", "~3.6", "~4.2"], ["New business", "~2.9", "~1.8", "~2.3"], ["Total growth", "8.3%", "6.6%", "7.5%"]], "tier": "C"},
          {"type": "bullets", "box": [7.3, 3.25, 5.6, 2.55], "size": 11, "items": [
              {"head": "Vocabulary shift:", "text": " the Form 10/A credited Q1-26 to $26m of \"new business\"; the 10-Q split implies ~$12m [D/C]."},
              {"head": "CARFAX is the price engine;", "text": " B2B growth is \"primarily due to continued new business growth\" [D]."},
              {"head": "Timing:", "text": " most price lands early in the year, so 2H leans on new business [IR]."},
              {"head": "Not disclosed:", "text": " price per location, escalators, bundle pricing, AI pricing."},
          ]},
          {"type": "quote", "box": [0.45, 5.95, 6.1, 0.72], "quote": "q_cars", "size": 10.5},
          {"type": "quote", "box": [6.8, 5.95, 6.1, 0.72], "quote": "q_value", "size": 10.5},
      ],
      sources=["extraction/segments_kpi.csv (10Q p.27 revenue drivers; 10A p.347)", "canonical/primary.csv (IS.revenue)", "analysis/D7_pricing.md §1-5", "analysis/D4_disclosure_changes.md §3", "transcripts/MBGL_2026-05-12_investor-day.md"],
      fact_ids=["c_q1_nb", "c_q1_price", "k_price_Q2", "k_price_6M", "c_q1_nb", "k_nbq_Q2", "k_nbq_6M", "c_q1_other", "c_q2_other", "c_6m_other", "c_price_share_6m",
                "c_price_pts_q1", "c_price_pts_q2", "c_price_pts_6m", "c_nb_pts_6m", "c_q1_growth", "c_q2_growth", "c_1h_growth", "k_nb_Q1_10A", "c_q1_drev", "c_6m_drev"],
      quote_ids=["q_cars", "q_value"])

# 17 --------------------------------------------------------------- demand vs industry
slide(layout="content", kicker="DEMAND DRIVERS VS INDUSTRY",
      title="Organic growth beat US vehicle sales in 10 of 11 years; only the 2020-21 shock moved both",
      elements=[
          {"type": "chart", "box": [0.45, 1.5, 8.4, 4.55], "chart": "column", "title": "MBGL organic vs US vehicle sales growth, % (both as printed on Investor Day slide 91)", "tier": "D/C",
           "categories": [str(y) for y in range(2015, 2026)],
           "series": [{"name": "MBGL organic growth (deck s.91)", "facts": [f"org_{y}" for y in range(2015, 2026)], "color": NAVY},
                      {"name": "US vehicle sales growth (FRED via slide 91; not independently fetched)", "facts": [f"ind_{y}" for y in range(2015, 2026)], "color": "A6A6A6"}],
           "number_format": "0", "legend": "bottom", "label_pos": "outEnd", "gap": 60, "overlap": -10, "y_min": -20, "y_max": 25, "label_size": 8},
          {"type": "kpis", "box": [9.1, 1.5, 3.8, 2.2], "cols": 2, "value_size": 20, "items": [
              {"value": "9.9%", "label": "Mean organic, 2015-25", "tier": "C"},
              {"value": "0.2%", "label": "Mean industry, 2015-25", "tier": "C"},
              {"value": "0.54", "label": "Correlation, all years", "tier": "C"},
              {"value": "-0.39", "label": "Ex 2020-21", "tier": "C"},
          ]},
          {"type": "bullets", "box": [9.1, 3.85, 3.8, 2.2], "size": 10.5, "items": [
              {"text": "2020: organic -2% vs industry -15%; recurring revenue still +3% [D]. Damage came via price relief and recall."},
              {"text": "The cyclical sleeve is the ~19% non-subscription line: recall, OEM marketing, Planning, Canada."},
          ]},
          {"type": "callout", "box": [0.45, 6.15, 12.45, 0.52], "size": 10,
           "text": "Caveats: slide 91 is \"NOT prepared on a consistent basis\"; year mapping inferred [C]; \"industry\" is new light-vehicle sales, not used-vehicle transactions; no 2008-09 data."},
      ],
      sources=["extraction/presentations.csv (ID s.91 data labels)", "analysis/K_session_tables.md (D9, D1)", "analysis/D9_demand_drivers.md §3", "analysis/D1_moat.md §4"],
      fact_ids=["a_sleeve19", "c_nonsub_share"] + [f"org_{y}" for y in range(2015, 2026)] + [f"ind_{y}" for y in range(2015, 2026)] + ["c_org_mean", "c_ind_mean", "a_corr", "a_beat_years", "a_recurring_2020"],
      quote_ids=[])

# 18 --------------------------------------------------------------- incentives
slide(layout="content", kicker="INCENTIVES",
      title="Pay rewarded CARFAX EBITA and tenure; the spin turned performance shares into time-vested RSUs",
      elements=[
          {"type": "table", "box": [0.45, 1.5, 7.6, 4.3], "font_size": 10, "col_widths": [2.4, 3.6, 1.6],
           "columns": ["Design feature", "Evidence", "Tier"],
           "rows": [
               ["CEO FY25 total pay", "$6.44m (SCT); STI paid 120% although both revenue metrics missed target", "D / C"],
               ["CARFAX President STI", "100% CARFAX U.S. EBITA; a 2.6% beat paid 129%", "D / C"],
               ["2023-25 PSU outcomes", "~182-184% of target", "C"],
               ["CARFAX PSU band (2025)", "Threshold-to-target spread only 4.5%; 50% floor", "C"],
               ["Spin conversion", "In-flight PSUs and all 2026 PSUs became time-vested RSUs", "D"],
               ["2026 target pay", "CFO $5.05m vs CEO $4.50m; CFO one-time awards ~$5.93m", "C"],
               ["2026 LTIP", "14% reserve (~41.3m shares), liberal recycling; no metrics in plan", "D / C"],
               ["Alignment", "No TSR metric; no ownership guideline; insiders <1%", "D"],
           ], "tier": "D/C"},
          {"type": "panel", "box": [8.3, 1.5, 4.6, 4.3], "fill": "F2F2F2"},
          {"type": "text", "box": [8.5, 1.6, 4.2, 0.35], "size": 12.5, "bold": True, "color": NAVY, "text": "What to watch"},
          {"type": "bullets", "box": [8.5, 1.98, 4.25, 1.75], "size": 10.5, "items": [
              {"head": "SBC ramp:", "text": " from ~1.3% of revenue ($22m FY25) to 3-4% ($56-75m on the FY26 guide), excluded from Adj. EBITDA."},
              {"head": "Metric risk:", "text": " if pay uses Adj. EBITDA, SBC and \"other\" add-backs never reach the bonus."},
              {"head": "First proxy (~Apr-2027):", "text": " STI/PSU metrics, TSR, ownership guidelines."},
          ]},
          {"type": "chart", "box": [8.5, 3.75, 4.25, 1.98], "chart": "column", "title": "Stock-based compensation, $m", "tier": "D/C",
           "categories": ["FY23", "FY24", "FY25", "3% of FY26", "4% of FY26"],
           "series": [{"name": "SBC", "facts": ["sbc_FY2023", "sbc_FY2024", "sbc_FY2025", "c_sbc3", "c_sbc4"], "color": TEAL}],
           "number_format": "0", "legend": "none", "label_pos": "outEnd", "gap": 60, "y_max": 90, "label_size": 9, "point_colors": {"3": "A6A6A6", "4": "A6A6A6"}},
          {"type": "callout", "box": [0.45, 5.95, 12.45, 0.72], "size": 11,
           "text": "Counter: unit EBITA metrics suit a 40%+ margin data business, converting PSUs at spin is standard, and severance (CEO 2x, double trigger, no gross-up) is mid-market [E]."},
      ],
      sources=["analysis/D5_incentives.md §2-5 (10/A p.391-414; 10-Q Ex.10.17-10.18)", "canonical/primary.csv (CF.sbc)"],
      fact_ids=["a_fred_metric", "a_fred_beat", "a_psu_floor", "a_sev", "c_m_FY2025", "a_eager_sct", "a_eager_sti", "a_fred_sti", "a_psu", "a_carfax_psu_band", "a_cfo_tdc", "a_ceo_tdc", "a_cfo_onetime", "a_ltip", "a_ltip_sh",
                "sbc_FY2023", "sbc_FY2024", "sbc_FY2025", "c_sbc3", "c_sbc4", "c_sbc_pct", "a_sbc_step", "a_sbc_ramp"])

# 19 --------------------------------------------------------------- red flags
slide(layout="content", kicker="RED FLAGS: DISCLOSURE CHANGES",
      title="Five of seven disclosure changes coincided with the affected metric turning worse",
      elements=[
          {"type": "table", "box": [0.45, 1.5, 12.45, 4.55], "font_size": 10, "col_widths": [3.1, 2.0, 5.3, 2.05],
           "columns": ["Change", "Vintage", "What it hid or reframed", "Coincided with weaker metric?"],
           "rows": [
               ["Growth relabelled: \"new business\" to \"price\"", "10/A (May) to 10-Q (Aug)", "10/A: Q1-26 new business $26m; 10-Q implies ~$12m, with ~$20m price", "Yes"],
               ["Segment measure: OP to Adj. EBITDA", "10-Q Q2-26", "B2B segment OP fell to $3m in Q2-26; stand-up costs ($33m 6M) booked in B2B", "Yes"],
               ["FY26 guide: organic cc to reported", "ID (May) to Q2 (Aug)", "Like-for-like cut ~0.9-1.6pt, not the 0.6-1.3pt headline", "Yes"],
               ["Adj. EBITDA definition: 10 to 6 exclusions", "10/A to 10-Q / 8-K", "New \"and other\" catch-all; Q2 deck still prints the 10-item text", "Mixed"],
               ["SPGI 41-43% margin target dropped", "SPGI ID 2022 to MBGL ID 2026", "Replaced by +50bp/yr from a reset ~39.1% base on a more generous measure", "Yes"],
               ["NRR pulled from Investor Day deck", "ID 2026-05-12", "\"Meaningfully north of 100%\"; no number in any filing", "Unknown"],
               ["Business-line $ and organic growth dropped", "SPGI Q1-26 to MBGL Q2-26", "Manufacturing (the weak line: -3% Q3-25) no longer visible", "Yes"],
           ], "verdict_col": 3, "tier": "D/C"},
          {"type": "quote", "box": [0.45, 6.15, 12.45, 0.5], "quote": "q_nrr", "size": 11},
      ],
      sources=["analysis/D4_disclosure_changes.md §0-4, §9-11", "extraction/segments_kpi.csv (10A p.347; 10Q p.27)", "transcripts/MBGL_2026-05-12_investor-day.md"],
      fact_ids=["a_lfl_cut", "a_head_cut", "a_reset", "a_50bp", "a_nrr", "a_mfg", "a_excl", "k_nb_Q1_10A", "c_q1_nb", "c_q1_price", "a_b2b_op_q2", "a_txn_6M_b2b", "a_spgi_target", "c_occ_lo", "c_occ_hi"],
      quote_ids=["q_nrr"])

# 20 --------------------------------------------------------------- pre-mortem
slide(layout="content", kicker="PRE-MORTEM",
      title="The likeliest way to lose is a slow de-rating to a 6-7% grower, not a moat collapse",
      elements=[
          {"type": "table", "box": [0.45, 1.5, 12.45, 4.5], "font_size": 10, "col_widths": [3.2, 4.6, 0.85, 0.95, 2.85],
           "columns": ["Bear case (extrapolates something already observed)", "Observed evidence", "Impact", "Likelihood", "Magnitude by FY28 [E]"],
           "rows": [
               ["1  Price lever wears out", "Price ~4.2pt of 1H-26 growth; new business $12m to $8m", "H", "M", "~$105m Adj. EBITDA (~12% of plan)"],
               ["2  Cross-sell / go-to-market keeps failing", "Lifetime bundle reversed Jun-26; 1.5-2 products per dealer", "M", "H", "~$30-55m EBITDA"],
               ["3  AI / search erode consumer traffic", "Ad spend +31% vs revenue +18% (FY23-25); CAC rising", "H", "M", "~$35-40m EBITDA"],
               ["4  B2B commoditises", "B2B +3% / +6%; FY25 flow-through -18%", "M", "H", "~$35m EBITDA"],
               ["5  Cyclical downturn (transactional + price relief)", "2020: organic -2%, dealer price relief; recall -$15m FY24", "M", "M", "~$45m EBITDA (~6%)"],
               ["6  Margin story slips again", "Target missed; costs at top of ranges; expansion pushed to 2028", "M", "H", "~$55-75m GAAP pre-tax"],
               ["7  Leverage / capital-return squeeze", "2.7x gross; interest ~31% of normalized OP", "M", "M", "$50m EBITDA miss = ~0.15-0.2x"],
               ["8  Data-supply squeeze", "10/A: supplier consolidation raised fees", "H", "L", "~$20-30m EBITDA (illustrative)"],
           ], "hml_cols": [2, 3], "tier": "E"},
          {"type": "callout", "box": [0.45, 6.1, 12.45, 0.58], "size": 10.5,
           "text": "Cases 1, 2, 4 and 6 are one cluster (growth ~6-7%, no margin expansion); magnitudes overlap and must not be summed. FY28 plan base: revenue ~$2,220m, Adj. EBITDA ~$870m [E]."},
      ],
      sources=["analysis/D11_premortem.md §1-3", "analysis/D7_pricing.md", "analysis/D2_unit_economics.md", "analysis/D3_group_decomposition.md"],
      fact_ids=["a_lev50m", "a_bear_frame", "k_recall_FY24", "a_lev50", "a_products", "a_pm1", "a_pm2", "a_pm3", "a_pm4", "a_pm5", "a_pm6", "a_pm7", "a_pm8", "a_fy28_rev", "a_fy28_ae", "c_price_pts_6m", "c_q1_nb", "k_nbq_Q2",
                "c_ad_growth", "c_rev_growth_2y", "c_b2b_g24", "c_b2b_g25", "ft_b2b_FY25", "a_gross_lev", "c_int_share"])

# 21 --------------------------------------------------------------- Q&A
slide(layout="content", kicker="MANAGEMENT Q&A",
      title="Three questions decide the thesis: dealer volume vs price, a dollar margin bridge, and AI's effect on traffic",
      elements=[
          {"type": "cards", "box": [0.45, 1.5, 12.45, 2.95], "cols": 3, "rows": 1, "gap": 0.2, "title_size": 12.5, "body_size": 12,
           "items": [
               {"title": "Q1  Price, volume, retention", "tag": "Bear case 1",
                "body": ["How did enrolled CARFAX dealer locations change in 2025 and 1H-26, what was gross revenue retention, and what share of dealers took a price increase at renewal? Will you print NRR?",
                         {"head": "Good answer: ", "text": "numbers, plus a reconciliation of the 10/A \"new business\" to the 10-Q \"price\" split."}]},
               {"title": "Q2  A dollar margin bridge", "tag": "Bear cases 6, 10",
                "body": ["Bridge FY25's $711m (10-item definition) to the FY27 base on today's 6-item definition: standalone cost, allocations replaced, reallocation, \"severance and other\". Is SBC excluded from pay metrics?",
                         {"head": "Good answer: ", "text": "dollars, and a capped \"other\" add-back."}]},
               {"title": "Q3  Traffic, ad intensity, AI", "tag": "Bear case 3",
                "body": ["What share of sessions and report views arrive via search or AI answer engines, how has cost per visitor trended, and do you license history data to any AI provider?",
                         {"head": "Good answer: ", "text": "traffic mix and cost per visitor; a concrete licensing position."}]},
           ]},
          {"type": "table", "box": [0.45, 4.65, 12.45, 2.0], "font_size": 11.5, "col_widths": [4.0, 8.45],
           "columns": ["Secondary question", "Why it matters"],
           "rows": [["Why were stand-up costs booked in B2B?", "B2B OP fell to $3m in Q2-26 as the segment measure switched [D]"],
                    ["Define \"normalized GAAP NI\" for the 25% payout", "$70.8m dividend is ~34-44% of standalone NI on our math [C]"],
                    ["What re-accelerates 2H revenue?", "Guide implies 2H +6.3-8.0% while new business was slowing [C]"]]},
      ],
      sources=["analysis/D12_management_QA.md", "analysis/D11_premortem.md", "analysis/D3_group_decomposition.md §5", "analysis/D10_guidance_vs_execution.md §3"],
      fact_ids=["a_25claim", "a_payout_rng", "a_2h_growth", "a_excl", "a_sbc_step", "ae_FY2025", "a_b2b_op_q2", "c_div", "a_sbc_step"])

# 22 --------------------------------------------------------------- honest counters
slide(layout="content", kicker="HONEST COUNTERS",
      title="The bull case is strong where it is audited: moat evidence, cash generation and revenue delivery",
      elements=[
          {"type": "cards", "box": [0.45, 1.5, 12.45, 4.4], "cols": 3, "rows": 2, "gap": 0.18, "title_size": 13, "body_size": 13,
           "items": [
               {"title": "Moat evidence is largely audited", "tag": "D/C", "body": "Revenue, margins, source and record counts are filing data; the CARFAX margin rose from 45.5% to 48.0% (6M-26)."},
               {"title": "Downturns brought price relief, not churn", "tag": "D", "body": "Recurring revenue grew +3% in 2020 while organic was -2%; recovery came within 12 months."},
               {"title": "Revenue guidance mostly met", "tag": "D/C", "body": "Two of three SPGI-era years beat the initial guide; the FY26 cut is ~1pt like-for-like."},
               {"title": "Some flags cut against the company's optics", "tag": "D", "body": "The Q2-25 recast (186 to 188) lowers growth; the 10-Q volunteered the price split; printed EPS shows the decline."},
               {"title": "B2B dip may be a one-year cycle", "tag": "C", "body": "6M-26 B2B flow-through recovered to ~50% after -18% in FY25."},
               {"title": "Cash supports the return", "tag": "C", "body": "Capex ~1% of revenue; standalone FCF ~$365m covers the dividend ~5x; no capitalized-software asset."},
           ]},
          {"type": "quote", "box": [0.45, 6.05, 12.45, 0.6], "quote": "q_firewall", "size": 11},
      ],
      sources=["analysis/SYNTHESIS.md (honest counters)", "analysis/D11_premortem.md §3", "analysis/D4_disclosure_changes.md (honest counters)", "analysis/D2_unit_economics.md", "transcripts/MBGL_2026-09-10_goldman-sachs-communacopia.md"],
      fact_ids=["a_recast", "a_cut1pt", "a_12m", "c_fcf_cover", "c_capint_FY2024", "c_carfax_m_FY2023", "c_carfax_m_6M-2026", "a_recurring_2020", "ae_Q2-2025", "ft_b2b_6M", "ft_b2b_FY25", "c_fcf_standalone", "c_capint_FY2025", "c_div_fcf"],
      quote_ids=["q_firewall"])

# 23 --------------------------------------------------------------- appendix: source limitations
slide(layout="content", kicker="APPENDIX: SOURCE LIMITATIONS",
      title="What this deck cannot see: native filings, SEC XBRL, proxy data and any used-vehicle market series",
      elements=[
          {"type": "table", "box": [0.45, 1.5, 12.45, 4.6], "font_size": 10, "col_widths": [3.0, 5.6, 3.85],
           "columns": ["Limitation", "Effect", "Mitigation in this deck"],
           "rows": [
               ["SEC (sec.gov) blocked; no XBRL cross-check", "All filing data read from Quartr page text; some tables flattened", "Canonical layer: 390 cells, 0 collisions; Quartr Q2-26 values matched 6 of 6"],
               ["Carve-out financials", "Include ~$100m of S&P allocations; pre-spin capital structure", "Standalone bridge on slide 14 [C/E]"],
               ["Investor Day slide 91 series", "\"NOT prepared on a consistent basis\"; year mapping inferred", "Labelled [C]; used only for relative growth"],
               ["Predecessor eras", "IHS scope incl. Maritime & Trade; Nov FYE; FY22 ~10 months", "Separate, labelled chart (slide 7)"],
               ["No DEF 14A yet; S-8 plan text not in Quartr", "Ownership counts flattened; future metrics unknown", "Incentive findings flagged as absence, not design"],
               ["No used-vehicle or dealer-count series (Part B blocked)", "Industry comparison uses new-vehicle sales only", "Caveat on slide 17"],
               ["Company-sourced KPIs", "ROI, awareness, \"Show me the CARFAX\", TAMs are marketing or survey figures", "Tagged [IR] / [X]; not used in computations"],
           ]},
          {"type": "callout", "box": [0.45, 6.2, 12.45, 0.48], "size": 10,
           "text": "Tiers: [D] printed in a filing or deck; [C] computed from [D] inputs; [E] estimate with stated assumption; [IR] management verbal; [X] third party."},
      ],
      sources=["deliverables/PART_A_SUMMARY.md (verification, gaps)", "canonical/VERIFICATION.md", "analysis/D_SPEC.md", "extraction/presentations_NOTES.md"],
      fact_ids=["a_canon", "a_quartr6", "a_alloc100", "a_fy22_10m", ])


# =============================================================================
# notes generation
# =============================================================================
def fmt_val(f):
    v = f["value"]
    if isinstance(v, str):
        return v
    u = f.get("unit", "")
    if u == "usd_m":
        return f"${v:,.1f}m" if abs(v) < 100 and v != int(v) else f"${v:,.0f}m" if v == int(v) else f"${v:,.1f}m"
    if u == "pct":
        return f"{v}%"
    if u == "count":
        return f"{v:,.0f}"
    if u == "usd_per_share":
        return f"${v:.2f}"
    return f"{v}"


def loc_str(f):
    src = f["source"]
    if src == "computed":
        return f"computed: {f['formula']}" + (f" ({f['method']})" if f.get("method") else "")
    loc = f.get("locator", {})
    parts = [f"{k}={v}" for k, v in loc.items()]
    return f"{src} [" + "; ".join(parts) + "]"


for i, s in enumerate(SLIDES, 1):
    s["n"] = i
    lines = [f"Slide {i}: {s['title']}", "Sources: " + "; ".join(s.get("sources", []))]
    if s.get("fact_ids"):
        lines.append("Numbers on this slide (value [tier] - source / row):")
        for fid in s["fact_ids"]:
            f = FACTS[fid]
            lines.append(f"- {f['label']}: {fmt_val(f)} [{f['tier']}] - {loc_str(f)}")
    for qid in s.get("quote_ids", []):
        q = QUOTES[qid]
        lines.append(f"Quote: \"{q['text']}\" - {q['who']} ({q['file']})")
    s["notes"] = "\n".join(lines)

doc = {"meta": {"deck": "MBGL Part E research deck", "prepared": "2026-10-06",
                "palette": {"navy": NAVY, "teal": TEAL, "blue": BLUE, "light_teal": LTEAL, "grey": GREY, "amber": AMBER, "red": RED},
                "font": "Arial"},
       "facts": FACTS, "quotes": QUOTES, "slides": SLIDES}
with open(OUT, "w") as fh:
    json.dump(doc, fh, indent=1, ensure_ascii=False)
print(f"wrote {OUT}: {len(SLIDES)} slides, {len(FACTS)} facts, {len(QUOTES)} quotes")
