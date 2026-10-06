# MBGL research stack — engagement status

Company: Mobility Global Inc. (NYSE: MBGL; the brief's "MGBL" is a typo). It was spun off from S&P Global ("S&P Global Mobility"): Form 10 filed 2026-05-07, 10/A filed 2026-05-27. Brands: CARFAX, automotiveMastermind, Polk Automotive Solutions, Market Scan.

## Decisions (user-confirmed 2026-10-06)
- Network: sec.gov / data.sec.gov / efts.sec.gov / files.quartr.com / web.archive.org are blocked. The user will allowlist them; until then the source is the Quartr MCP only.
- Predecessor history: S&P Global "Mobility" segment FY2022–25 and IHS Markit "Transportation" segment FY2016–21 go on a separate tab. They are segment-level only and never merged into the carve-out figures.
- Part E: house style; no templates supplied.
- Transcripts: quote banks (short verbatim quotes + citations) instead of full-text archives, because bulk verbatim reproduction is refused.
- No expert-call folder was supplied, so the expert-call summary is skipped.

## Known limitations
- No XBRL cross-check while SEC is blocked. Verification is cross-document instead (Form 10 vs 10/A vs 10-Q vs 8-K).
- Quartr page text flattens tables and sometimes corrupts digits (8-K pp.7-10, 10-Q pp.4,5,7).
- No native PDFs, so there is no filings zip yet.

## Stage log (2026-10-06)
| Part | State | Output |
|---|---|---|
| A model | DONE (Quartr-only); XBRL check + ~8 unreadable cells pending network | deliverables/MBGL_Historical_Model.xlsx, PART_A_SUMMARY.md, canonical/VERIFICATION.md |
| B market | BLOCKED (FRED/BEA/Census/BLS denied) — plan written | market/PART_B_SERIES_PLAN.md |
| C voice | DONE: 3 events (204 verified quotes), targets timeline; no expert calls supplied | transcripts/ |
| D analysis | DONE: D1–D12 + SYNTHESIS + K_session_tables | analysis/ |
| E documents | DONE: research doc (54pp, 82 [TO COLLECT]), deck (23 slides, 422 facts fact-checked; NOT opened in real PowerPoint — no COM on Linux) | deliverables/ |

## Next when network opens
1. EDGAR: confirm CIK, pull native Form 10/10-A/10-Q + XBRL company-facts → Phase 3 cross-check; fill CF working-capital lines, tax split, lease table, Market Scan PPA.
2. Part B workbook per PART_B_SERIES_PLAN.md; replace [context] industry figures; re-run D1/D9 share arithmetic.
3. Rebuild workbook/doc/deck via scripts (deterministic).
4. Q3-2026 earnings (2026-11-06): extend model, transcripts, guidance tracker.
