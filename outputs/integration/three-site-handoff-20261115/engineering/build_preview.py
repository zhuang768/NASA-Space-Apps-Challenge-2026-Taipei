#!/usr/bin/env python3
"""Build an offline, dependency-free evidence preview. No deployment hooks."""
import csv
import hashlib
import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMIT = "1506ede572435588eb5e64f95f24639279b77e56"
BLOB = "2371ade1c27087efaa165acb98b7541266eaa606"
SOURCE = ROOT / "final_candidates.csv"
raw = SOURCE.read_bytes()
if hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() != BLOB:
    raise SystemExit("CSV does not match the pinned git blob; refuse to generate.")
rows = list(csv.DictReader(raw.decode().splitlines()))
assert [r["candidate_id"] for r in rows] == ["MS-01", "MS-02", "MS-03"]

def val(row, key, places):
    x = float(row[key])
    assert math.isfinite(x)
    return f"{x:.{places}f}"

def card(r):
    ident = escape(r["candidate_id"])
    lat, lon = val(r,"lat",2), val(r,"lon_east_0_360",2)
    desc = [
        ("MOLA · mean slope", f"{val(r,'mola_slope_deg_mean',3)}°", "Regional surface measure"),
        ("MOLA · relief", f"{val(r,'mola_relief_m',0)} m", "Range within the cell"),
        ("TES · thermal inertia", f"{val(r,'TES_TI_mean',1)} J m⁻² K⁻¹ s⁻½", f"{r['TES_TI_valid_cells']} of {r['TES_TI_native_cells']} source cells"),
        ("SWIM · shallow consistency", val(r,"SWIM_0_1m_mean",3), "Index; not an ice probability"),
        ("SWIM · deeper consistency", val(r,"SWIM_1_5m_mean",3), "Index; not measured ice depth"),
        ("MY35 · mean dust CDOD",val(r,"dust_my35_mean_cdodtot",3), "Regional optical-depth context"),
    ]
    metrics = "".join(f'<div class="metric"><dt>{escape(k)}</dt><dd>{escape(v)}<small>{escape(q)}</small></dd></div>' for k,v,q in desc)
    return f"""<article id="{ident}" aria-labelledby="{ident}-heading">
<p class="eyebrow">Retained research candidate</p><h2 id="{ident}-heading">{ident}</h2>
<p class="coord">{lat}°N &nbsp; {lon}°E <span>east-positive 0–360°</span></p>
<p class="scope">Nominal grid footprint: {val(r,"north_south_km",1)} × {val(r,"east_west_km",1)} km</p>
<dl>{metrics}</dl>
</article>"""
cards = "".join(card(r) for r in rows)
page = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ZASA | Mars evidence preview</title>
<meta name="description" content="Offline snapshot of three Mars regional research candidates from the frozen ZASA screening table.">
<style>
:root{color-scheme:dark;--bg:#101418;--card:#182128;--line:#34434c;--text:#f0f6f7;--muted:#c2d2d7;--accent:#96ebd1;--warm:#ffc9a3}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 system-ui,sans-serif}a{color:var(--accent)}a:focus-visible{outline:2px solid var(--accent);outline-offset:4px}main{max-width:1250px;margin:auto;padding:clamp(16px,4vw,60px)}header{padding:0 0 22px;border-bottom:1px solid var(--line);margin-bottom:24px}h1,h2{margin:.2em 0;line-height:1.12}h1{font-size:clamp(2rem,5vw,4rem)}h2{font-size:2rem}.eyebrow,.stamp{font-size:.8rem;text-transform:uppercase;letter-spacing:.12em;font-weight:700;color:var(--accent)}.stamp{color:var(--warm)}.lede{max-width:67ch;color:var(--muted)}nav{display:flex;flex-wrap:wrap;gap:.7rem}nav a{padding:.38rem .7rem;border:1px solid var(--line);border-radius:7px;text-decoration:none}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,310px),1fr));gap:16px}article,aside{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px}aside{border-left:4px solid var(--warm);margin:21px 0}.coord{font:700 .96rem/1.45 ui-monospace,monospace}.coord span,small,.scope,footer{color:var(--muted)}.coord span,small{display:block;font:.78rem/1.45 system-ui,sans-serif}dl,.metric,dd{margin:0}.metric{padding:.52rem 0;border-top:1px solid var(--line)}dt{color:var(--muted);font-size:.84rem}dd{font-weight:700}small{font-weight:400}footer{overflow-wrap:anywhere}
</style></head><body><main>
<header><p class="eyebrow">ZASA / evidence snapshot</p><h1>Mars candidates</h1>
<p class="stamp">Offline engineering preview • source commit __SHORT__ • not deployed</p>
<p class="lede">Three retained Mars windows from the pinned candidate table. This is a data viewer, not a formal report or a new ranking. Later branch evidence and unmerged follow-ups are not included.</p>
<nav aria-label="Jump to candidate"><a href="#MS-01">MS-01</a><a href="#MS-02">MS-02</a><a href="#MS-03">MS-03</a></nav></header>
<section class="cards" aria-label="Candidate data cards">__CARDS__</section>
<aside><strong>Interpretation boundary</strong><br>These regional metrics are not site-scale ground truth. SWIM is a consistency index, not an ice quantity, depth, or probability; TES thermal inertia is not temperature. No globally novel site, confirmed ice resource, landing safety, or excavation suitability is asserted.</aside>
<footer>Snapshot source: <code>__COMMIT__</code> · Pinned candidate table Git blob: <code>__BLOB__</code>.</footer>
</main></body></html>"""
for old, new in {"__SHORT__":COMMIT[:7],"__COMMIT__":COMMIT,"__BLOB__":BLOB,"__CARDS__":cards}.items():
    page=page.replace(old,new)
(ROOT / "index.html").write_text(page,encoding="utf-8")
