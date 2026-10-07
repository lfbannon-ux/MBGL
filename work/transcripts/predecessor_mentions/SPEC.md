# Mention-sweep spec: Mobility / CARFAX in IHS Markit (INFO) and S&P Global (SPGI) transcripts

Load tools: ToolSearch "select:mcp__Quartr__read_transcript".

For EACH assigned event, do the following.

## 1. Read the whole transcript

Call `read_transcript(eventId, section "full")` and paginate with `nextFromTimestamp` until the end. Read every paragraph, both the prepared remarks and the Q&A.

## 2. Guard against wrong-event payloads

Confirm that the payload's company, title and date match the assignment. If they don't, record WRONG-EVENT and skip the event.

## 3. Capture every qualifying mention

A paragraph qualifies if it contains any of these:
- "Mobility"
- "CARFAX" / "Carfax"
- automotive business references that clearly refer to the unit: "automotive", "auto", "Polk", "automotiveMastermind", "aM", "Market Scan", "CARPROOF", "vehicle history", "dealer"
- for IHS Markit: "Transportation" when it means the segment
- spin, separation or "Mobility Global" references

Exclude:
- "mobility" in an unrelated sense, e.g. "upward mobility"
- "Transportation" when it means the shipping or Maritime business only. Still list it if it is the segment.
- the operator's boilerplate

## 4. Write one entry per mention

Number entries sequentially within the event. Each entry has:
- **Speaker** (name, title, firm) and **section** (Prepared / Q&A). For Q&A, give the analyst's question in your own words, one line.
- **Short verbatim quote:** at most 2 sentences, copied exactly. Pick the most informative sentence(s). Do NOT copy whole paragraphs.
- **Detail:** a thorough paraphrase in your own words of EVERYTHING said about Mobility/CARFAX in that paragraph and the immediately related turns. Include every number (growth %, margin, revenue, guidance, subscription/transaction split, CARFAX metrics, recall, dealer/OEM commentary, pricing, AI, new products, cost actions, outlook, spin details).
- **Tags:** one or more of `results`, `guidance`, `drivers`, `pricing`, `CARFAX`, `B2B/aM/Polk`, `margin/costs`, `M&A`, `spin`, `AI/product`, `risk`, `other`.
- **Link:** the Quartr timestamp URL.

## 5. Output

Write one file per event: `/home/user/MBGL/work/transcripts/predecessor_mentions/{COMPANY}_{YYYY-MM-DD}_{eventId}.md`.

The header has: company, event title, date, event type, Quartr event URL, participants (names/titles), and mention count.

After the header, write an "Event summary" in your own words, 3–6 bullets on what this event said about Mobility/CARFAX.

Then list the numbered entries.

If an event has no mentions, still write the file with "No mentions of Mobility/CARFAX or the automotive unit" and the paragraph count you scanned.

Checkpoint: write each event's file as soon as that event is done.

## 6. Verify

Re-check each quote against the transcript text so that it is verbatim.

## 7. Report

Final report under 200 words: per event, the number of mentions; any failures.
