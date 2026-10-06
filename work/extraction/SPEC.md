# EXTRACTION SPEC — Mobility Global Inc. (NYSE: MBGL)

## Entity & eras (to be confirmed from filings; agents must verify, not assume)
- Registrant: Mobility Global Inc. (Delaware), spin-off of S&P Global's Mobility division. Form 10-12B filed 2026-05-07, 10-12B/A 2026-05-27.
- ERA C (carve-out / combined): combined financial statements of S&P Global Mobility as presented in the Form 10/A (expected FY2023–FY2025 IS/CF, FY2024–FY2025 BS; plus unaudited interim). Basis: carve-out with corporate allocations from S&P Global — every allocation is a judgment of the parent; record it.
- ERA S (standalone): 10-Q Q2 2026 and later filings.
- ERA P1 (predecessor segment, S&P Global "Mobility" segment): SPGI 10-K FY2022–FY2025 (Dec FYE). Segment-level only.
- ERA P0 (predecessor segment, IHS Markit "Transportation" segment): INFO 10-K FY2016–FY2021 (Nov 30 FYE). Segment-level only; scope differs from Mobility (verify what it contained). NON-COMPARABLE with P1 — no growth rate across the P0/P1 boundary.
- Predecessor eras are a separate statement family (statement=SEG_PRED); they never overwrite or fill carve-out cells.

## Golden rules
1. As originally reported: values from the document named in source_doc, primary column. Comparatives from a later doc are recorded as separate rows (source_doc differs) — never substituted.
2. Never fabricate: not printed → no row. Odd print → keep verbatim, flag in notes.
3. Every row carries source_doc + page (Quartr page number, as in the text/ file headers).
4. Units as printed: state `usd_m` (millions), `usd_k`, `usd`, `usd_per_share`, `pct`, `shares_m`, `count`, `text`. Parentheses → negative value, record sign as printed in line_item context.
5. Self-verify before writing: BS foots (assets = liabilities + equity/net parent investment), IS ties to net income, CF rolls to change in cash, note tables foot to printed totals. A printed table that doesn't foot → note it, don't fix it.
6. Checkpoint: write CSV rows to disk as you go.

## Long-CSV schema (one file per agent: extraction/{topic}.csv)
source_doc,page,statement,fiscal_period,period_end,section,line_item,value,unit,is_subtotal,order_index
- source_doc: e.g. Form10A_2026-05-27, Form10_2026-05-07, 10Q_Q2-2026, SPGI_10K_FY2024, INFO_10K_FY2019
- statement: IS, BS, CF, EQ, NOTE_<topic>, SEG, SEG_PRED, REV_DISAGG, NONGAAP, KPI, PRES, PROFORMA
- fiscal_period: FY2025, FY2024, H1-2026, Q2-2026, 6M-2025 ... ; period_end ISO date
- line_item: VERBATIM caption (keep Quartr spacing artefacts normalised only by collapsing whitespace)

## Notes file per agent: extraction/{topic}_NOTES.md
Per-period source refs; caption oddities; restatements observed (Form 10 vs Form 10/A vs 10-Q comparatives); what is NOT disclosed.

## Text sources
work/text/*.txt — `=== PAGE n === url` headers. Tables are flattened by Quartr; read carefully, columns appear in print order.

## REVISED SOURCE METHOD (2026-10-06)
Full-text mirroring of Quartr documents into text/ was blocked (bulk verbatim reproduction refused). Agents therefore read
Quartr `read_document` directly and write ONLY structured extracted rows (numbers + verbatim captions) with page refs.
Do NOT copy whole pages/paragraphs to disk. Short verbatim quotes (≤2 sentences) are allowed in notes where needed for audit.
Quartr page text flattens tables and sometimes corrupts digits (e.g. "1ŏ01") — when a figure looks corrupted, cross-check it
against another presentation of the same number (summary table, MD&A, release, comparative column) and flag it; never guess.
Known docs (Quartr documentId): Form10A 3603533 (472pp, filed 2026-05-27); Form10 3603535 (filed 2026-05-07);
10-Q Q2-2026 3699447 (199pp); 8-K Q2-2026 release 3699450 (11pp); Q2-2026 slides 3986013 (15pp); Investor Day slides 3352878 (116pp).
