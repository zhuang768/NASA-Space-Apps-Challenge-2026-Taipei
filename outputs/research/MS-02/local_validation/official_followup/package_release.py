import pathlib,shutil,json,hashlib,csv,zipfile,datetime
P=pathlib.Path(__file__).parent;root=P/'release';rel='outputs/research/MS-02/local_validation/official_followup';R=root/rel;R.mkdir(parents=True,exist_ok=True);(R/'sources').mkdir(exist_ok=True);(R/'derived').mkdir(exist_ok=True)
for p in (P/'derived').iterdir():
 if p.suffix!='.npy':shutil.copy2(p,R/'derived'/p.name)
for p in P.glob('*.py'):shutil.copy2(p,R/p.name)
for p in P.glob('retrievals_*.json'):shutil.copy2(p,R/p.name)
for p in (P/'sources').iterdir():
 if p.suffix in ['.lbl','.hdr']or p.name in ['mrr_map.cat','ctx_esri.json','wisdom2026.html','active2026.html','wisdom_hal.json','brighi_thesis.json','zenodo_groundice.json','Adventdalen_data.xlsx']or p.name.endswith(('_sim.xml','_rtrn.csv'))or(p.name.startswith('ctx_')and p.name.endswith('_L12.png')):shutil.copy2(p,R/'sources'/p.name)
shutil.copytree(P/'sources/gtnp1505',R/'sources/gtnp1505',dirs_exist_ok=True)
with zipfile.ZipFile(R/'sources/catalogues_and_themis_headers.zip','w',zipfile.ZIP_DEFLATED)as z:
 for pat in ['CRISM_*.json','THEMIS_*.json','*.header']:
  for p in (P/'sources').glob(pat):z.write(p,p.name)
notes=root/'docs/research/MS-02/local_validation/official_followup_notes.md';notes.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/'official_followup_notes.md',notes)
# inherited observed arrays stay in their original directory; retain pinned-input provenance
inputs=[]
for id in ['00464501','01983502','02004601']:
 p=P/'sources'/f's_{id}.npz';b=p.read_bytes();inputs.append(dict(path=f'outputs/research/MS-02/local_validation/radar_roi/s_{id}.npz',ref='1aea666cd3f227a296218362317a0d5ad989129d',sha256=hashlib.sha256(b).hexdigest(),git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
(R/'inherited_inputs.json').write_text(json.dumps(inputs,indent=2))
for name in ['radar_follow.py','diagnostics.py','plot_followup.py']:
 p=R/name;s=p.read_text();s=s.replace("np.load(S/f's_{id}.npz')","np.load((S/f's_{id}.npz') if (S/f's_{id}.npz').exists() else P.parent/'radar_roi'/f's_{id}.npz')");p.write_text(s)
readme='''# MS-02 official-source follow-up

- Scope: fixed 52.50–53.00 N, 168.00–168.50 E. Data/methods/bullet notes only; no formal report.
- Read `docs/research/MS-02/local_validation/official_followup_notes.md` for limits and the eight-item status table. This release does not claim every scientific gap is closed.
- Offline data: `derived/thermal_common_grid.npz`, source row-block ZIP, CRISM albedo and geometry NPZ, numerical radar clutter and aligned arrays, five CTX samples, UNISCALM raw CSV and 2023 core source workbook. NaNs are missing values, never zero ice.
- Units/epochs/URLs: individual CSVs, retained PDS labels and source metadata. `thermal_pairs.csv` is b minus a. Display-grid cells are not independent native pixels.
- Decompress `sources/catalogues_and_themis_headers.zip` into `sources/` before running acquisition/extraction. Original observed radar NPZs are reused from sibling `../radar_roi/`; hashes and pinned source commit are in `inherited_inputs.json`.
- Reproduce: `fetch_sources.py`, `get_products.py`, `thermal_extract.py`, `spectral_extract.py`, `geometry_extract.py`, `radar_follow.py`, `ctx_tiles.py`, `earth_analyze.py`, `diagnostics.py`, `thermal_sensitivity.py`, `plot_followup.py`. Acquisition scripts require network and some endpoints are blocked. `earth_analyze.py` uses read-only openpyxl; processing uses numpy/scipy/matplotlib/Pillow. No new workbook is authored.
- All numeric-coverage/geometry filters are documented analysis choices, not official scientific validation flags. Radar selection parameters are exploratory; no peak is classified as ice. Corrected MRDR4 is an alternate product, not a claim that the old TRDR calibration is repaired. CTX beta01 is explicitly uncontrolled.
- Failed access: competition resources 503; PSI/Elsevier supplementary tables 403 or HTML error body; HAL full PDFs 403; Murray site/KML 503. HTTP200 alone is not accepted as successful scientific data acquisition. File suffix probes at Elsevier do not establish actual supplement URLs.
- Data attribution: NASA/PDS/ASU/JHU-APL; NASA/JPL/MSSS/Caltech Murray Lab/Esri CTX; GTN-P UNISCALM, Ole Humlum (CC BY 4.0); Wendt 2024, DOI10.5281/zenodo.11187360; Brighi et al., DOI10.5194/epsc2026-988 (CC BY4.0). Original metadata is retained.
'''
(R/'README.md').write_text(readme)
# source file fingerprints, including source paper retained only locally (no rehosting required)
source=[]
for p in sorted((P/'sources').rglob('*')):
 if p.is_file()and p.suffix not in ['.b64','.npy']:
  b=p.read_bytes();source.append(dict(local_source_path=str(p.relative_to(P)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),retained_in_release=(R/p.relative_to(P)).exists()))
(R/'source_fingerprints.json').write_text(json.dumps(source,indent=2))
files=[]
for p in sorted(root.rglob('*')):
 if p.is_file():b=p.read_bytes();files.append(dict(path=str(p.relative_to(root)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(R/'manifest.json').write_text(json.dumps(dict(scope=dict(lat_min=52.5,lat_max=53,lon_east_min=168,lon_east_max=168.5),baseline_main='1aea666cd3f227a296218362317a0d5ad989129d',publication_parent='826780f0b270eebe9b6f2f64b8ba1ac5ddcc8177',files=files,limitations='Not all gaps closed; no direct local ice existence/depth/content claim; no formal report authored'),indent=2))
print(len(files)+1,'files',sum(x['bytes']for x in files),'bytes')
