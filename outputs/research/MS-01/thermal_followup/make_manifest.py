"""Hash this bounded follow-up after running analysis, plot and validation."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def main():
    paths=[p for p in HERE.iterdir() if p.is_file() and p.name!='manifest.json']+[ROOT/'docs/research/MS-01/thermal_followup.md']
    files=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(paths)]
    payload=dict(schema='MS01-KNOWN-INTERFACE-FOLLOWUP-v1',starting_sha='33f78ed986b0c39585dc4224b5f68bd6a7e9bed7',original_mars_baseline_sha='3cc8488577535e2fa4d146021fde51f8ff6cc667',branch='research/ms-01-earth-analogs',pr=8,research_date_taipei='2026-11-15',sources='source_manifest.json',sources_read_scope='sources.json',files=files,hash_exclusion='Only this manifest excludes itself; root MS01 manifest additionally hashes this file.',findings=['Known-interface profiles attenuate24h component; this is not unique ice identification.','UV retained for heat-transfer and identifiability checks; S/D coordinate crosswalk unresolved.','Beacon is optional literature-level massive-ice/material contrast; no new raw comparison.'],contribution='Descriptive reproduction/application plus source QA and MS01 evidence interpretation; no new mechanism, field discovery, inverse model or Mars ice proof.',unresolved_gaps=['No same-material same-forcing ice-free control','No independent UV k/rho/Cp, complete local energy boundary or per-probe footprint','S/D coordinates swapped between2009 note and2022 paper','Historical cross-logger clocks unknown; W HOBO decimal-day offset~1hour','Oblique probe geometry and surface contact/exposure uncertainties','Beacon raw hourly series not acquired; no dual-site validation','MS01 local ice truth/material and matched multitemporal forcing remain unknown'],scope='Only docs/research/MS-01 and outputs/research/MS-01; no main merge or teammate work modification.')
    (HERE/'manifest.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n');print({'followup_hashed_files':len(files)})
if __name__=='__main__':main()
