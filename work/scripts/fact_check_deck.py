#!/usr/bin/env python3
"""QA (a): re-read every number in deck_content.json and compare with its source.

* Direct facts (canonical/primary.csv, extraction/segments_kpi.csv, predecessor.csv,
  presentations.csv, notes.csv) are matched row-by-row on their locator.
* Computed facts are re-evaluated from their formula and compared at the stated rounding.
* Analysis-file facts: the quoted evidence string must appear verbatim in the cited file.
* Quotes: each must appear verbatim in the cited transcript quote bank.
* Chart series: every plotted value is a fact id (checked above).
* Untraced numbers: numbers in visible slide text that do not match any fact on that slide
  (review aid; years, slide/page refs and list counters are skipped).
Exit code 1 on any mismatch.
"""
import csv
import json
import math
import re
import sys

ROOT = "/home/user/MBGL/work"
doc = json.load(open(f"{ROOT}/deliverables/deck_content.json"))
F = doc["facts"]

_cache = {}


def rows(path):
    if path not in _cache:
        _cache[path] = list(csv.DictReader(open(f"{ROOT}/{path}")))
    return _cache[path]


def num(s):
    s = str(s).strip().replace(",", "")
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()%")
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def close(a, b, tol=1e-6):
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b)))


def check_direct(fid, f):
    src, loc, val = f["source"], f["locator"], f["value"]
    if src == "canonical/primary.csv":
        cand = [r for r in rows(src) if r["canon_key"] == loc["canon_key"] and r["period"] == loc["period"]]
        got = [num(r["value"]) for r in cand]
        return ("OK" if any(close(g, val) for g in got) else ("MISMATCH" if cand else "NO_ROW")), got
    if src in ("extraction/segments_kpi.csv", "extraction/predecessor.csv", "extraction/notes.csv"):
        cand = [r for r in rows(src) if r["line_item"] == loc["line_item"] and r["fiscal_period"] == loc["fiscal_period"]
                and ("page" not in loc or r["page"] == loc["page"]) and ("source_doc" not in loc or r["source_doc"] == loc["source_doc"])]
        if isinstance(val, str) and "text_contains" not in loc:
            ok = any(r["value"].strip() == val for r in cand)
            return ("OK" if ok else ("MISMATCH" if cand else "NO_ROW")), [r["value"][:40] for r in cand]
        if "text_contains" in loc:
            ok = any(loc["text_contains"] in r["value"] for r in cand)
            return ("OK" if ok else ("MISMATCH" if cand else "NO_ROW")), [r["value"][:80] for r in cand]
        got = [num(r["value"]) for r in cand]
        return ("OK" if any(close(g, val) for g in got) else ("MISMATCH" if cand else "NO_ROW")), got
    if src == "extraction/presentations.csv":
        cand = [r for r in rows(src) if r["page"] == loc["page"] and loc["line_item_contains"] in r["line_item"]
                and ("fiscal_period" not in loc or r["fiscal_period"] == loc["fiscal_period"])]
        if "list_index" in loc:
            got = []
            for r in cand:
                labels = r["line_item"].split(":", 1)[1].split(" / ")
                got.append(num(labels[loc["list_index"]]))
        elif isinstance(val, str):
            got = [r["value"] for r in cand]
            return ("OK" if any(g.strip() == val for g in got) else ("MISMATCH" if cand else "NO_ROW")), got
        else:
            got = [num(r["value"]) for r in cand]
        return ("OK" if any(close(g, val) for g in got) else ("MISMATCH" if cand else "NO_ROW")), got
    return "UNKNOWN_SOURCE", []


def eval_formula(expr):
    ids = sorted(F.keys(), key=len, reverse=True)
    out = expr
    for k in ids:
        out = re.sub(r"(?<![A-Za-z0-9_])" + re.escape(k) + r"(?![A-Za-z0-9_])", f"({float(F[k]['value'])!r})", out) \
            if not isinstance(F[k]["value"], str) else out
    return eval(out, {"__builtins__": {}}, {})


def check_computed(fid, f):
    v = eval_formula(f["formula"])
    d = f.get("decimals", 1)
    ok = round(v, d) == round(float(f["value"]), d) or abs(v - float(f["value"])) <= 0.5 * 10 ** (-d) + 1e-9
    return ("OK" if ok else "MISMATCH"), [round(v, d + 2)]


def check_analysis(fid, f):
    path = f"{ROOT}/{f['source']}"
    try:
        txt = open(path).read()
    except FileNotFoundError:
        return "NO_FILE", []
    return ("OK" if f["locator"]["evidence"] in txt else "EVIDENCE_NOT_FOUND"), [f["locator"]["evidence"][:60]]


results = {}
for fid, f in F.items():
    if f["source"] == "computed":
        st, got = check_computed(fid, f)
        kind = "computed"
    elif f["source"].endswith(".md"):
        st, got = check_analysis(fid, f)
        kind = "analysis"
    else:
        st, got = check_direct(fid, f)
        kind = "direct"
    results[fid] = (kind, st, got)

# quotes
qres = {}
for qid, q in doc["quotes"].items():
    txt = open(f"{ROOT}/{q['file']}").read()
    qres[qid] = q["text"] in txt

# chart series reference only registered facts
chart_refs, missing_refs = 0, []
for s in doc["slides"]:
    for el in s.get("elements", []):
        for ser in el.get("series", []):
            for fid in ser["facts"]:
                chart_refs += 1
                if fid not in F:
                    missing_refs.append((s["n"], fid))
        for st in el.get("steps", []):
            chart_refs += 1
            if st["fact"] not in F:
                missing_refs.append((s["n"], st["fact"]))


# untraced numbers in visible text
def visible_text(s):
    out = [s.get("title", ""), s.get("subtitle", "")]
    out += [c.get("value", "") + " " + c.get("label", "") for c in s.get("chips", [])]

    def walk(o):
        if isinstance(o, str):
            out.append(o)
        elif isinstance(o, list):
            for i in o:
                walk(i)
        elif isinstance(o, dict):
            for k, v in o.items():
                if k in ("box", "series", "steps", "facts", "colors", "color", "fill", "tier", "tag", "quote", "type", "chart",
                         "number_format", "label_pos", "col_widths", "point_colors", "x", "level", "pos", "start", "end",
                         "left_color", "right_color"):
                    continue
                walk(v)
    for el in s.get("elements", []):
        walk(el)
    return " ".join(out)


SKIP = re.compile(r"^(19|20)\d\d$")


def fact_forms(fids):
    vals = set()
    for fid in fids:
        v = F[fid]["value"]
        if isinstance(v, str):
            for t in re.findall(r"-?\d+(?:\.\d+)?", v):
                vals.add(round(abs(float(t)), 2))
            continue
        v = abs(float(v))
        for x in (v, v / 1e9, v / 1e6, v / 1e3, v * 100, v / 100):
            for d in (0, 1, 2):
                vals.add(round(x, d))
            vals.add(round(x, 2))
            vals.add(float(math.floor(x)))
    return vals


untraced = {}
for s in doc["slides"]:
    txt = visible_text(s)
    txt = re.sub(r"\d{4}-\d{2}-\d{2}", " ", txt)
    txt = re.sub(r"\b(10/A|10-Q|10-K|8-K|Form 10|DEF 14A|S-8)", " ", txt)
    txt = re.sub(r"\d+/\d+/\d+", " ", txt)
    txt = re.sub(r"\b(19|20)\d\d-\d\d\b", " ", txt)
    txt = re.sub(r"(?i)\b(FY|Q|H|s\.|p\.|slide|slides|ID|1H|2H|6M|Q1|Q2|Q3|Q4)\s?-?\d+(-\d+)?", " ", txt)
    txt = re.sub(r"(\d)-(\d)", r"\1 \2", txt)
    txt = re.sub(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d+(-\d+)?", " ", txt)
    txt = re.sub(r"\b(top|Top)[- ]\d+", " ", txt)
    txt = re.sub(r"\b\d+\s+of\s+(the\s+)?(top-)?\d+", " ", txt)
    forms = fact_forms(s.get("fact_ids", []))
    bad = []
    for m in re.finditer(r"(?<![A-Za-z])-?\d[\d,]*(?:\.\d+)?", txt):
        tok = m.group(0)
        if SKIP.match(tok.lstrip("-")):
            continue
        v = num(tok)
        if v is None:
            continue
        v = abs(v)
        if v in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) and re.match(r"\s*(\)|  |[A-Z])", txt[m.end():m.end() + 2] or ""):
            continue  # list counters like "1  Growth..."
        if round(v, 2) in forms or round(v, 1) in forms or round(v) in forms:
            continue
        bad.append(tok)
    if bad:
        untraced[s["n"]] = bad

# report
n_ok = sum(1 for k, (_, st, _) in results.items() if st == "OK")
by_kind = {}
for k, (kind, st, _) in results.items():
    by_kind.setdefault(kind, [0, 0])
    by_kind[kind][0] += 1
    by_kind[kind][1] += st == "OK"
print(f"FACTS: {len(results)} total, {n_ok} OK")
for kind, (t, ok) in by_kind.items():
    print(f"  {kind:9s}: {ok}/{t} OK")
bad = {k: v for k, v in results.items() if v[1] != "OK"}
for k, (kind, st, got) in bad.items():
    print(f"  !! {k} [{kind}] {st}: deck={F[k]['value']} source={got}")
print(f"QUOTES: {sum(qres.values())}/{len(qres)} verbatim in transcripts")
for q, ok in qres.items():
    if not ok:
        print(f"  !! quote {q} not found verbatim")
print(f"CHART VALUES: {chart_refs} plotted values, all from registered facts: {not missing_refs} {missing_refs or ''}")
print(f"UNTRACED NUMBERS (visible text not matched to a slide fact; review): {sum(len(v) for v in untraced.values())}")
for n, toks in sorted(untraced.items()):
    print(f"  slide {n}: {' '.join(toks)}")
sys.exit(1 if bad or not all(qres.values()) or missing_refs else 0)
