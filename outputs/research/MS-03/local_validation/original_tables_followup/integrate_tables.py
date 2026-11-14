# -*- coding: utf-8 -*-
"""Append this bounded acquisition supplement; retain earlier rows and identifiers."""
from pathlib import Path
import csv
import json
import subprocess

FUP = Path(__file__).resolve().parent
P = FUP.parent
ROOT = FUP.parents[4]
INTEGRATION_BASE = 'fbfa780cf587a0787739200898e80b4d27fea8d1'

def read(name):
    with (P/name).open(encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)

def write(name, fields, rows):
    # Preserve each published primary CSV's newline convention.
    original = subprocess.check_output(['git','show',INTEGRATION_BASE+':outputs/research/MS-03/local_validation/'+name], cwd=ROOT)
    ending = '\r\n' if b'\r\n' in original else '\n'
    with (P/name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator=ending)
        w.writeheader()
        w.writerows(rows)

def append_text(row, field, text):
    if text not in row[field]:
        row[field] += text

fields, rows = read('local_prior_work.csv')
for r in rows:
    if r['prior_work_id'] == 'LV-PW08':
        append_text(r, 'actually_read', '；2026-11-15補查另取得父子DataCite metadata、作者公開首頁及MBARS程式庫清單；原表與欄位說明仍未取得')
        append_text(r, 'evidence_path', '; original_tables_followup/metadata/cz_parent.json; original_tables_followup/metadata/cz_data.json; original_tables_followup/metadata/cz_headers.json; original_tables_followup/table_acquisition.csv')
        append_text(r, 'limitations', '；檔案DOI已確認但不等於讀取資料；不將相關Hood清單直接視為同一54影像')
    if r['prior_work_id'] == 'LV-PW05':
        r['source_locator'] = r['source_locator'].replace('§3 impact discussion', '§4 impact discussion')
        append_text(r, 'actually_read', '；2026-11-15補查實取官方USGS資料頁、正確Data Catalog入口及AIS XML；AIS與既有FGDC位元組相同，沒有新增觀測列')
        append_text(r, 'evidence_path', '; original_tables_followup/source_column_notes.csv; original_tables_followup/table_acquisition.csv; original_tables_followup/requests_round3_retrievals.json')
        append_text(r, 'limitations', '；TableS4的Yes(CTX)缺HiRISE彩色確認；CRISM ice?的x是無適當資料，不是陰性')
new = dict(
    prior_work_id='LV-PW10', candidate_id='MS-03',
    title='Levy, Head & Marchant 2009 thermal contraction polygon classification; full Data Set S1 not acquired',
    year='2009', url_or_doi='https://doi.org/10.1029/2008JE003273',
    scope_class='regional_or_unknown_sample_overlap',
    purpose_relation='相關多邊形辨識、分類與冰成因研究已有先例；完整原表是否包含固定格仍未知',
    source_extent='原文§2：30–80度南北緯，共823幅HiRISE（413北／410南）；這是文獻調查數，不是本次取得資料列數',
    source_locator='publisher HTML §§2–3, Table1 note, Appendix A; Supporting Information catalogue Data Set S1',
    actually_read='實讀HTML所列段落與附件清單；沿Colgate官方師資頁讀作者lab/research頁；未取得S1資料列或全文PDF；舊別名網址HTTP200實為登入頁',
    overlap_status='full_image_catalogue_roi_membership_unknown',
    research_gap_or_difference='待完整S1及readme、影像ID與官方足跡核對；未取得表格不是格內零命中；Table1型式範例不是全調查清單',
    limitations='TXT及替代XLS公開下載均403；已讀作者頁未提供指定原表；不以緯度分布、地名或舊索引結果推定本格形貌；分類不直接量測冰深或含量',
    evidence_path='original_tables_followup/table_acquisition.csv; original_tables_followup/requests_round1_retrievals.json; original_tables_followup/requests_round2_retrievals.json; original_tables_followup/content_checks.json',
    search_date_taipei='2026-11-15')
if not any(r['prior_work_id'] == new['prior_work_id'] for r in rows):
    rows.append(new)
write('local_prior_work.csv', fields, rows)

fields, rows = read('mars_ice_evidence.csv')
for r in rows:
    if r['evidence_id'] == 'LV-ICE08':
        append_text(r, 'source_locator', '; TableS4 exact field definitions (FGDC eainfo/detailed); independent official AIS metadata route')
        append_text(r, 'limits', '; 2026-11-15 alternate official catalog/AIS yielded metadata only, not TableS4 rows; Yes(CTX) and CRISM x must retain original semantics')
        append_text(r, 'evidence_path', '; original_tables_followup/table_acquisition.csv; original_tables_followup/source_column_notes.csv; original_tables_followup/content_checks.json')
write('mars_ice_evidence.csv', fields, rows)

fields, rows = read('search_log.csv')
existing = len(rows)
ids = {r['log_id'] for r in rows}
classes = {r['request_id']:r['classification'] for r in json.loads((FUP/'content_checks.json').read_text())['checks']}
for f in sorted(FUP.glob('requests_round*_retrievals.json')):
    for q in json.loads(f.read_text()):
        identifier = 'LV-TABREQ-' + q['id']
        if identifier in ids:
            continue
        rows.append(dict(log_id=identifier, date_taipei='2026-11-15',
                         platform='public author/official repository endpoint; '+q['route_basis'],
                         query_or_url=q['url'], status=str(q.get('http_status', q['status'])),
                         actual_read_scope=classes[q['id']],
                         result='Original target table not acquired; see original_tables_followup/'+f.name+' and content_checks.json',
                         spatial_basis='No original rows/usable geometry received; MS-03 fixed-cell membership unknown, not zero'))
        ids.add(identifier)
queries = [
    ('S01', 'Web search', '"10.18738/T8/DUCOYB" "Data"; "DUCOYB/J9K4HL"', 'Dataset identity and linked original-paper results; no original table rows exposed'),
    ('S02', 'Web search', '"jgre2606-sup-0002-ds01"; "Levy" "ds01.xls" Mars', 'Publisher attachment list identifies TXT/XLS/PDF versions, not acquired data'),
    ('S03', 'Web search', '"TableS4.csv" "Dundas"; "Dundas" "5f99f0b8d34e198cb786e8e7"', 'Official release/catalogue metadata found; table not acquired'),
    ('S04', 'Web search', '"Levy" "2008JE003273" site:brown.edu; "2008JE003273" site:planetary.brown.edu', 'No exact original-table download found in these results; not complete author-history search'),
    ('S05', 'Web search', '"Cohen-Zada" Mars data site:github.com; "Cohen-Zada" Mars data site:geo.tamu.edu', 'No exact original-table mirror found in inspected results; unrelated names excluded'),
    ('S06', 'Web search', '"2008JE003273" site:figshare.com; "2020JE006617" site:figshare.com; "2024JE008387" site:figshare.com', 'No exact original table found; separate API DOI filters retained in request log'),
    ('S07', 'Publisher HTML', 'https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2008JE003273', 'Actually read §§2–3, Table1 note, Appendix A and attachment inventory via web; TXT/XLS/PDF advertised, not downloaded table'),
    ('S08', 'Official faculty page to author lab', 'https://www.colgate.edu/about/directory/jlevy -> https://sites.google.com/colgate.edu/levy/research', 'Actual public author pages read; no specified S1 attachment link on these pages'),
    ('S09', 'USGS official web', 'https://www.usgs.gov/data/locations-and-properties-ice-exposing-scarps-and-new-impact-craters-mid-latitudes-mars', 'Release title/DOI/CC0 link read; release landing page not original TableS4'),
    ('S10', 'Browser availability', 'in-app research browser unavailable', 'Browser creation failed; no browser page viewed or login performed; public APIs/HTML used instead'),
]
for suffix, platform, query, result in queries:
    identifier = 'LV-TABSEARCH-' + suffix
    if identifier in ids:
        continue
    rows.append(dict(log_id=identifier, date_taipei='2026-11-15', platform=platform,
                     query_or_url=query, status='bounded_inspection_record', actual_read_scope=result,
                     result='No new original target-table acquisition from this inspection',
                     spatial_basis='No complete original-table membership test; fixed cell unchanged'))
    ids.add(identifier)
write('search_log.csv', fields, rows)
print('Existing search records preserved:', existing, '; new records:', len(rows)-existing)
