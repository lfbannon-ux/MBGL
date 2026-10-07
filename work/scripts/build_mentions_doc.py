"""Assemble transcripts/predecessor_mentions/*.md into one chronological document:
deliverables/MBGL_Predecessor_Transcript_Mentions.docx (+ .md). House style: Arial, navy headings, banded tables."""
import glob, os, re, json, collections
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = f'{W}/transcripts/predecessor_mentions'
NAVY = RGBColor(0x1F, 0x38, 0x64)
events = {e['id']: e for e in json.load(open(f'{D}/event_list.json'))}
files = sorted(glob.glob(f'{D}/*_[0-9][0-9][0-9][0-9]-*.md'), key=lambda p: os.path.basename(p).split('_')[1])

def count_mentions(txt):
    m = re.search(r'[Mm]ention count:[ \t]*(\d+)', txt)
    if re.search(r'[Mm]ention count:[ \t]*n/a', txt): return 0
    if m: return int(m.group(1))
    return len(re.findall(r'^#{2,4}\s*(?:Mention\s*)?#?\d+\b', txt, re.M))

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr(); s = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear'); s.set(qn('w:color'), 'auto'); s.set(qn('w:fill'), hexcolor); tcPr.append(s)

def add_runs(p, text, size=9.5, italic=False):
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'\1', text)  # links -> label (URL kept in md)
    for part in re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', text):
        if not part: continue
        bold = part.startswith('**') and part.endswith('**')
        t = part.strip('*').strip('`') if (bold or part.startswith('`')) else part
        r = p.add_run(t); r.bold = bold; r.italic = italic; r.font.size = Pt(size); r.font.name = 'Arial'


NOTES = [
 'Wrong-event payloads (Quartr served a different transcript; excluded, no entries): 64126 "AGM 2022" (actually a Sustainable1 ESG webinar); 609213 "Fireside chat" 2026-03-18 (actually a Market Intelligence AI-strategy webinar).',
 'IHS Markit: Quartr holds transcripts only for the Q2 FY2021 (2021-06-23) and Q3 FY2021 (2021-09-28) calls. FY2016–FY2020 and Q4 FY2021 earnings calls are listed without transcripts — not obtainable from this source.',
 'Event 620148 ("Investor Day 2026", listed under S&P Global) is Mobility Global\'s own inaugural investor day; it duplicates the MBGL quote bank (transcripts/MBGL_2026-05-12_investor-day.md). Consecutive same-speaker paragraphs were grouped into one entry.',
 'Scan method: batches read every paragraph, except eight events (24584, 20622, 65410, 165844, 223553, 393534, 673513 and part of 24584) where transcripts were too large to return inline; there mentions were located by keyword search (Mobility, CARFAX, automotive, Polk, automotiveMastermind, Market Scan, dealer, spin) plus surrounding Q&A context. Explicit mentions are captured; an indirect reference without any keyword ("the division") could be missed.',
 'Borderline entries (portfolio-review or divestiture remarks where Mobility is not named; passing "transportation" remarks pre-merger) are included and flagged as borderline inside the entry — drop them for a strict count.',
 'Quotes were checked verbatim against transcript text (programmatically where the transcript was saved locally, otherwise by eye). Transcript errors are flagged, not corrected (e.g., "$80 billion-$90 billion" deferred-tax figure, likely millions).',
]

doc = Document()
st = doc.styles['Normal']; st.font.name = 'Arial'; st.font.size = Pt(9.5)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
for s in ('Heading 1', 'Heading 2', 'Heading 3'):
    doc.styles[s].font.name = 'Arial'; doc.styles[s].font.color.rgb = NAVY
for sec in doc.sections:
    sec.left_margin = sec.right_margin = Cm(2); sec.top_margin = sec.bottom_margin = Cm(1.8)

t = doc.add_paragraph(); r = t.add_run('Mobility / CARFAX in IHS Markit and S&P Global transcripts'); r.bold = True; r.font.size = Pt(20); r.font.color.rgb = NAVY
p = doc.add_paragraph(); add_runs(p, 'Every mention, event by event (Nov 2020 – Sep 2026). Prepared 2026-10-07 from Quartr transcripts. '
    'Quotes are short verbatim extracts (≤2 sentences) with speaker and timestamp; the "Detail" text is a paraphrase of everything said in the passage. '
    'Tier: all management statements are [IR] (verbal, unaudited).', italic=True)

# Coverage table
doc.add_heading('Coverage', level=1)
p = doc.add_paragraph(); add_runs(p, 'Scope: all IHS Markit (INFO) and S&P Global (SPGI) events with a transcript on Quartr from the SPGI–IHS Markit merger announcement '
    '(2020-11-30) to 2026-09-14. IHS Markit: Quartr holds transcripts only for the Q2 and Q3 FY2021 calls; its FY2016–FY2020 and Q4 FY2021 earnings-call events carry no transcript. '
    'SPGI events before Nov 2020 are excluded (S&P Global did not own the business). Mobility Global’s own events are in transcripts/MBGL_*.md.')
rows = []
for f in files:
    txt = open(f).read(); base = os.path.basename(f)
    co, date, eid = base[:-3].split('_')[0], base.split('_')[1], int(base[:-3].split('_')[-1])
    e = events.get(eid, {})
    rows.append((date, co, e.get('title', ''), e.get('type', ''), count_mentions(txt), f))
missing = [e for e in events.values() if not any(r[5].endswith(f"_{e['id']}.md") for r in rows)]
tbl = doc.add_table(rows=1, cols=5); tbl.style = 'Table Grid'
for i, h in enumerate(['Date', 'Company', 'Event', 'Type', 'Mentions']):
    c = tbl.rows[0].cells[i]; c.text = ''; add_runs(c.paragraphs[0], f'**{h}**', 8.5); shade(c, '1F3864')
    for rr in c.paragraphs[0].runs: rr.font.color.rgb = RGBColor(255, 255, 255)
for k, (date, co, title, typ, n, _) in enumerate(rows):
    cells = tbl.add_row().cells
    for i, v in enumerate([date, co, title, typ, str(n)]):
        cells[i].text = ''; add_runs(cells[i].paragraphs[0], v, 8.5)
        if k % 2: shade(cells[i], 'D9E1F2')
p = doc.add_paragraph(); add_runs(p, f'Events covered: {len(rows)} · total mentions: {sum(r[4] for r in rows)}' +
    (f' · NOT COVERED: {", ".join(str(m["id"]) for m in missing)}' if missing else ''), 9, italic=True)

doc.add_heading('Coverage notes', level=1)
for n_ in NOTES:
    p = doc.add_paragraph(style='List Bullet'); add_runs(p, n_, 9)

# Body: one section per event, chronological; render the agent markdown
md_out = ['# Mobility / CARFAX in IHS Markit and S&P Global transcripts', '', '## Coverage notes', ''] + ['- ' + n_ for n_ in NOTES] + ['']
for date, co, title, typ, n, f in rows:
    txt = open(f).read()
    md_out.append(txt); md_out.append('\n---\n')
    doc.add_page_break() if n >= 8 else None
    doc.add_heading(f'{date} · {co} · {title} ({n} mentions)', level=1)
    in_table = False
    for line in txt.splitlines():
        s = line.rstrip()
        if not s.strip() or s.startswith('---'): continue
        if s.startswith('# '): continue  # file title replaced by our heading
        if s.startswith('|'):
            if re.match(r'^\|\s*:?-+', s): continue
            p = doc.add_paragraph(); add_runs(p, ' · '.join(c.strip() for c in s.strip('|').split('|')), 8.5); continue
        m = re.match(r'^(#{2,4})\s+(.*)', s)
        if m:
            doc.add_heading(re.sub(r'[*`]', '', m.group(2)), level=min(3, len(m.group(1)))); continue
        m = re.match(r'^(\s*)[-*]\s+(.*)', s)
        if m:
            p = doc.add_paragraph(style='List Bullet' if not m.group(1) else 'List Bullet 2'); add_runs(p, m.group(2)); continue
        m = re.match(r'^>\s?(.*)', s)
        if m:
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(0.8); add_runs(p, m.group(1), italic=True); continue
        p = doc.add_paragraph(); add_runs(p, s)

os.makedirs(f'{W}/deliverables', exist_ok=True)
doc.save(f'{W}/deliverables/MBGL_Predecessor_Transcript_Mentions.docx')
open(f'{W}/deliverables/MBGL_Predecessor_Transcript_Mentions.md', 'w').write('\n'.join(md_out))
print('events', len(rows), 'mentions', sum(r[4] for r in rows), 'missing', [m['id'] for m in missing])
