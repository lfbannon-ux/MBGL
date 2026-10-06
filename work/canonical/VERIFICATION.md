# Verification log — Part A (Phases 3 & 6)

## Phase 3 — independent cross-check (XBRL substitute)
SEC XBRL company-facts unavailable (sec.gov blocked by sandbox egress). Substitutes used:
1. Quartr standardized financials (`get_financials`, sourced from filings): only Q2-2026 is populated for MBGL. 6/6 matched:
   revenue 468 · operating profit 82 · net income 53 · total assets 13,060 · long-term debt 1,981 · CFO 6M-2026 189. No annual periods available.
2. Cross-document: Form 10 vs Form 10/A identical (annual + Q1); 10-Q 6M = Form 10/A Q1 + 10-Q Q2 on every IS line; 10-Q 12/31/25 comparative BS = Form 10/A; 8-K IS/BS = 10-Q.
3. Predecessor S&P Global Mobility segment revenue vs carve-out revenue: 2023 1,484 vs 1,485; 2024 1,609 vs 1,613; 2025 1,747 vs 1,750 (basis differences, see analysis/D4).

## Phase 4 — canonical guards
canon_primary.py: 0 collisions (59 identical duplicates absorbed and logged), 0 leftovers (every source row mapped or EXCLUDED with reason), 3 logged MD&A gap-fills.

## Phase 6 — recalc
LibreOffice headless recalc → 0 formula errors; 106 integrity-check cells, 0 failures. n/a checks are explained in Accounting Notes
(annual/Q1 CFO components unreadable; Q1-2025 FX unreadable).

## Outstanding (needs native filings once the network allowlist opens)
- EDGAR XBRL company-facts cross-check of ~8 headline items × every period.
- Annual CF working-capital lines (Form 10/A p.443), Q1 CF components, tax provision 2024/23 split, lease maturity table, Market Scan PPA liabilities.
