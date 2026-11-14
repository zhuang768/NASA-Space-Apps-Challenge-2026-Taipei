"""Inventory original/downloaded and versioned derivatives; excludes self-referential hashes."""
from pathlib import Path
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3]
rows=[]
for root in [P,R/'docs/research/MS-02/local_validation']:
 for f in sorted(root.rglob('*')):
  if not f.is_file() or '__pycache__' in f.parts or f.name in ['manifest.json','revision_verification.json','statistics_summary.md']:continue
  rel=str(f.relative_to(R));ignored=subprocess.run(['git','check-ignore','-q',rel],cwd=R).returncode==0
  rows.append(dict(path=rel,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),storage='local_only' if ignored else 'git_deliverable',role='downloaded_source' if 'sources' in f.parts else 'derived_or_method'))
manifest=dict(schema_version=2,task='MS-02 fixed-ROI local validation; evidence only',date_local='2026-11-15',timezone='Asia/Taipei',
 start_head='c309675fbe713a8548a75abf29b54e64217768f9',preserved_remote_head='ef5eb162b1df0919b8d6dd780782896188607b2c',user_known_old_head='38b8fa0dea527b1cc47aeb02dc260e039da37122',
 branch='research/ms-02-earth-analogs',base='handoff/verified-data-20261114',base_sha='f7076c9fdc77e00244ed5d6863aad2bf78cfa28f',pr=6,
 fixed_roi=dict(south=52.5,north=53,west_east_positive=168,east_east_positive=168.5,coordinate_system='planetocentric; Mars sphere3396190m'),
 audit_reads={'PR9':'c206553fc681328d214cbbcd508d3c5b1391e200','PR10':'0260c511d9fce6be12d3460a69e474f333160cbf'},
 acquisition='acquisition_log.jsonl; actual requests including errors; source ZIP hash in geology_archive_provenance.json',
 storage_policy='Large originals, copyrighted full articles and intermediate extracted text remain local-only; labels/catalogs/ROI numerical derivatives and source hashes are committed. Missing local-only data after clone may be reacquired by exact source URL; no claim all source bytes reside in Git.',
 reproduction=['extract_geology.py ZIP_PATH','analyze_products.py','analyze_radar.py','analyze_crism.py','analyze_workbooks.py','revise_evidence.py','finalize_records.py','build_revision_manifest.py','verify_revision.py','build_statistics.py'],
 dependencies=['Python3.9+','numpy','shapely','pyproj','pyshp','matplotlib','Pillow','openpyxl'],
 historical_scripts='build_tables.py, derive_metrics.py, build_manifest.py and historical verifiers reflect earlier snapshot; do not run to overwrite revised evidence',
 excluded_self_hashes=['manifest.json','revision_verification.json','statistics_summary.md'],files=rows)
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('manifest files',len(rows),'versioned bytes',sum(x['bytes'] for x in rows if x['storage']=='git_deliverable'))
