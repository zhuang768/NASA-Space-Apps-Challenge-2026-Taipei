"""Refresh own evidence tables and bullet notes. No network/Git mutations."""
from pathlib import Path
import csv,json,hashlib,datetime as dt,subprocess
O=Path(__file__).resolve().parent;L=O.parent;ROOT=O.parents[4];START='ddd04cfcb5ea810d73304b1cf6ae064c1f77a1c5'
def write(name,data):
 with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=data[0].keys(),lineterminator='\n');w.writeheader();w.writerows(data)
def dump(name,data): (O/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
readlog=[]
def source(i,url,loc,scope,support,limit):readlog.append(dict(source_id=i,url_or_doi=url,source_locator=loc,actually_read=scope,supports=support,limits=limit,date_taipei='2026-11-15'))
source('GAP-S01','https://zenodo.org/records/6604912','original XLSX sheet1 rows1–1204; author record file checksum/license','Actual metadata and all1203 cached data rows; raw cell references preserved by parser','Original catalogue identity; dated-impact point membership; original ice flags','Not all fresh impacts or image footprints; not Dundas2021 S4')
source('GAP-S02','https://doi.org/10.1029/2021JE007145','§§2–2.1, Supporting Information/Data Availability','Selected publisher HTML method paragraphs and data linkage, not a complete independent re-review of paper','Dated-before/after and resolving-HiRISE selection restrictions','A no-hit filtered catalogue cannot establish local ice absence')
source('GAP-S03','https://www.uahirise.org/PSP_007561_1290','Image metadata: centred latitude −50.602°, east longitude305.990°','Actual author image page metadata; not a local MS-03 observation','Independent cardinal-coordinate orientation check for conflicting XLSX E/N header suffixes','Image centre is not identical to impact position; this product lies outside MS-03 and supplies no local ice evidence')
source('GAP-S04','https://planetarydata.jpl.nasa.gov/img/data/mgs/moc/rdr/mgscim_1548/s17006/s1700607_na.lbl','IMAGE and IMAGE_MAP_PROJECTION; QUALITY_ID; processing NOTE','Complete label and actual original IMG pixels decoded, PDS checksum verified','Exact 2006 observation, native 3.000339463 m projected grid, projection and producer QA','RDR resampling does not create native detail; no absolute geolocation uncertainty or PSF calibration supplied here')
source('GAP-S05','https://oderest.rsl.wustl.edu/live2/?target=mars&ihid=MGS&iid=MOC-NA%2FWA&pt=NASDP&query=product&results=mf&output=json&westernlon=242&easternlon=242.5&minlat=57.5&maxlat=58&limit=1000','S17/00607 Footprint_geometry; original file links','Actual JSON product and dense footprint; explicit 0–360 east geometry','Catalogue intersection, product identity and scope context','Footprint is not pixel QA or proof of identifiable polygons; C0 field is not used as east-positive geometry')
source('GAP-S06','https://planetarydata.jpl.nasa.gov/img/data/mgs/moc/rdr/mgscim_1548/catalog/DSMAP.CAT','POLAR STEREOGRAPHIC block and Snyder1987 reference','Original catalogue projection description; no detailed pixel-origin equations in this short catalogue','Projection class; IMG/LBL offsets and spherical radius used explicitly in own code','Valid nonzero pixel bounds can be narrower than producer footprint bounds')
source('GAP-S07','https://pds-geosciences.wustl.edu/missions/mro/CAT_v7_4_codeonly.zip','SummaryParams2014/crism_summary_bd1500_2.pro lines7–17; crism_sumutil_band_depth.pro lines47–57; crism_sumutil_single.pro lines32–100','Actual ZIP and selected source functions; code hashes/member names retained; IDL not executed','Multispectral two-band-depth definition; actual wavelength continuum; hyper-only kernel branching','Not proof CAT7.4 is the MRDR1.03.94 production binary or same execution path')
source('GAP-S08','https://pds-geosciences.wustl.edu/missions/mro/crism_summary_parameter_reference.pdf','July2026 PDF pp1–2,5','Selected original parameter pages; no whole-document review claimed','BD1500_2/ICER1_2 documented parameter context','Parameter sign or magnitude without calibrated QA is not an ice classification')
source('GAP-S09','https://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v2/mrosh_2101/document/edr_to_usrdr.csv','Exact four matched EDR basenames among six earlier Italian products','Complete correspondence CSV parsed by exact token matching','Mapped IDs, not guessed Italian/US ID equivalence','No match here is not archive-wide data absence')
source('GAP-S10','https://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v2/mrosh_2101/document/rgram_processing.htm','SHARAD characteristics; geometry description; native sample intervals','Selected actual HTML sections, encodingcp1252','GEOM planetocentric/east-positive; .0375us sampling;10MHz/15m vacuum range resolution','Sampling is not resolution; material resolution depends on dielectric model and not local truth')
source('GAP-S11','https://pds-geosciences.wustl.edu/mro/urn-nasa-pds-mro_sharad_simulations/document/userguide.pdf','PDF pp3,5–11,20 (printed2,4–10,19); §§1–3 and Appendix B example','Selected original text including source-data limitations and sample indexing example','Same-USRDR dimensional alignment; geodetic return latitude; zero-based range rows; model-only travel timing; no power subtraction','Unmodeled clutter and non-calibrated simulated amplitude; simulation not independent observation')
source('GAP-S12','https://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v2/mrosh_2101/data/rgram/s_0462xx/s_04624502_rgram.img','rows2182–2450 zero-based; official GEOM columns2185–2249 one-based','Actual original HTTP206 bytes, paired exact observation sim XML/combined-array bytes, geom and return rows','Real 2016 radar/clutter pixels, 65 in-cell centre positions and native-grid QA','Not all scattering inside cell; no validated subsurface pick, dielectric inversion or ice-fraction calculation')
source('GAP-S13','https://api.sciencebase.gov/catalog/item/5f99f0b8d34e198cb786e8e7?format=json','Exact alternate official API request','HTTP404 only; no science table','Records a new access attempt','No TableS4 or membership result')
source('GAP-S14','https://dataverse.tdl.org/api/datasets/:persistentId/?persistentId=doi:10.18738/T8/DUCOYB','Exact native Dataverse DOI request','HTTP403 only; no science table','Records a new access attempt','No data/header bytes or membership result')
source('GAP-S15','https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2008JE003273','Supporting Information list and exact S1 PDF download; historical AGU auxiliary URL','Actual support-list text; PDF and old endpoint HTTP403; web fetch failure retained in search log','Identity of alternate S1 representation and failed access','No S1 data rows or whole-footprint exclusion')
write('source_read_log.csv',readlog)
q=[]
def gap(i,topic,done,state,unknown,nextstep,owner,src):q.append(dict(gap_id=i,topic=topic,completed_this_round=done,state=state,remaining_unknown=unknown,next_required_evidence=nextstep,handoff_owner=owner,source_ids=src))
gap('GAP01','Morphology / AD1','Acquired official MOC RDR; checked PDS checksum/projection and three fixed native-DN tiles','new_pixels_obtained_morphology_unknown','No reliable closed polygon boundary set; full-cell feature survey and effective detectability not established','Actual higher-resolution in-cell imagery or independently validated boundaries plus matched-scale uncertainty protocol','Main + human image interpreter; GPU only after validated boundaries','GAP-S04;GAP-S05;GAP-S06')
gap('GAP02','Spectral QA','Verified official CAT multispectral path; computed actual-wavelength, float32/64, legacy-parameter and ICER algebra diagnostics','partial_hypotheses_tested_no_ice_detection','Producer execution/root cause, cloud/frost/instrument mask and detection sensitivity unknown','Verified production pipeline/normalization relationship; independent same-mode controls and documented science QA','Main + GPU + instrument expertise','GAP-S07;GAP-S08')
gap('GAP03','Independent subsurface evidence','Verified EDR/USRDR mapping, four actual centre tracks, same-observation 65-column echo/clutter subset','radar_pixels_and_model_obtained_ice_unknown','No defensible subsurface reflector, local dielectric, depth or fraction','Validate surface/clutter/radar artefacts and reflector picks across independent suitable passes; any local depth model must state assumptions','Main + radar specialist / GPU','GAP-S09;GAP-S10;GAP-S11;GAP-S12')
gap('GAP04','Prior-work catalogue membership','Parsed1203 author-catalogue events; zero point records in fixed cell; tried three alternate official target-table routes','one_bounded_catalogue_checked_three_originals_still_missing','Cohen-Zada54 image footprints, LevyfullS1, DundasfullS4 membership unknown','Actual originals and original header definitions; image footprints separately from event-point membership','Main / literature evidence owner','GAP-S01;GAP-S02;GAP-S03;GAP-S13;GAP-S14;GAP-S15')
gap('GAP05','Research difference','Separated archival QA/observability additions from ice/genesis claims and prior established methods','bounded_integration_contribution_only','No exhaustive historical novelty clearance or new physical result','Human decision on archival reproducibility/observability framing; no first-site claim','Main / human author','GAP-S01;GAP-S04;GAP-S07;GAP-S12')
gap('GAP06','UV timing','Preserved existing block; exact calibration filename query yielded no usable source in this search','unresolved_no_clock_join','Original .m/.xls/.CR1, unprocessed2012 logger and clock/deployment records absent','Named originals or author deployment/clock documentation; no inferred four-hour correction','Main / data owner; GPU join remains disabled','Existing UV clock handoff; search_log.csv')
write('gap_status.csv',q)
# Membership evidence is separately testable, with exact IDs and point/footprint distinctions.
import csv as _csv
cross=list(_csv.DictReader((O/'sources/edr_to_usrdr.csv').open()));tracks=[]
for old in ['0796502','1768301','4624502','5476301','6059201','5882501']:
 key=f'e_{old}_001_ss19_700_a';matches=[r['US RDR Basename'] for r in cross if key in [v.strip() for v in r['EDR Basename(s)'].split(';')]]
 assert len(matches)<=1
 count='';first='';last='';geomfile=''
 if matches:
  geomfile='sources/'+matches[0]+'_geom.tab';g=list(_csv.reader((O/geomfile).open()));ins=[r for r in g if 57.5<=float(r[2])<=58 and 242<=float(r[3])%360<=242.5];count=len(ins)
  if ins:first=ins[0][0].strip();last=ins[-1][0].strip()
 tracks.append(dict(italian_product_id='R_'+old+'_001_SS19_700_A',US_crosswalk_basename=matches[0] if matches else '',strict_GEOM_centre_hits=count,first_column_1based=first,last_column_1based=last,geom_source=geomfile,scope='actual GEOM planetocentric centres; not full radar scattering footprint' if matches else 'not found in this downloaded crosswalk; archive-wide availability unknown'))
write('radar_track_membership.csv',tracks)
e=[]
def ev(i,kind,val,unit,period,scale,extent,src,limit):e.append(dict(evidence_id=i,candidate_id='MS-03',evidence_type=kind,value=val,units=unit,period=period,resolution_or_scale=scale,effective_extent=extent,ice_presence='unknown',actual_ice_depth_m='',ice_fraction='',source_ids=src,limitations=limit))
ev('GAP-ICE01','original_author_catalogue_and_this_point_query','1203 records;0 point hits','impact points','Daubar2022 release6604912','individual dated events; image footprints not tested','fixed cell impact coordinates only','GAP-S01;GAP-S02;GAP-S03','Zero membership does not imply no exposed ice or absence from broader Dundas S4')
ev('GAP-ICE02','orbital_image_and_this_native_pixel_QA','9272742 nonzero ROI pixel centres','resampled map pixel centres','2006-04-08T00:22:40.473–00:22:50.285 UTC','3.000339463m projected grid, not PSF','partial strip and three fixed512x512 review windows','GAP-S04;GAP-S05;GAP-S06','Texture visible; no reliable closed polygon geometry or ice proof')
ev('GAP-ICE03','parameter_implementation_calculation','0.019347334519968284 max absolute residual','dimensionless','source2006–2014; MRDR production2023-07-18','180.4662m map grid;13169 strict source centres','fixed cell strict source-centre subset','GAP-S07;GAP-S08','Not a detection threshold or confirmed processing error; root cause and cloud/frost QA unknown')
ev('GAP-ICE04','radar_measurement_and_surface_model','65 actual in-cell GEOM centres;269 range rows each','radargram samples; model arbitrary power','2016-06-07T22:23:51.611–22:24:01.059 UTC','.0375us sampling;15m vacuum resolving power','centres in cell; off-nadir sources may be outside','GAP-S09;GAP-S10;GAP-S11;GAP-S12','No validated subsurface reflector; model not independent observation; do not subtract powers or convert unpicked returns to ice depth')
write('mars_ice_evidence.csv',e)
write('local_prior_work.csv',[dict(prior_work_id='GAP-PW01',candidate_id='MS-03',title='Daubar et al.2022 New Craters on Mars: An Updated Catalog',url_or_doi='https://doi.org/10.1029/2021JE007145 ; https://doi.org/10.5281/zenodo.6604912',scope_class='global_catalogue_with_zero_fixed_cell_impact_point_members',source_locator='paper§§2–2.1; original sheet1rows2–1204',same_use='dated new-impact census including ice flag; not an MS-03 analogue validation',overlap_status='no impact-point membership in this bounded catalogue; full image footprints not tested',research_difference='fixed-cell reproducible membership and selection-dependence audit, not new crater/ice discovery',limitations='Dated/resolving-HiRISE inclusion differs from Dundas2021S4; no full prior-work clearance',source_ids='GAP-S01;GAP-S02;GAP-S03')])
write('analog_validation.csv',[dict(earth_id='MS-03-E02',site='Adventdalen AD1',disposition='general_method_reference_only',new_support='actual MOC strip and three fixed review tiles; still no reliable Mars closed boundaries',comparison='not performed; unknown, not0',shared_genesis_or_ice='unknown',restriction='No AD1 number copied into Mars; new image pixels do not automatically restore specific pairing',source_ids='GAP-S04;GAP-S05;GAP-S06'),dict(earth_id='MS-03-E01',site='University Valley W',disposition='known_interface_and_quality_reference_only',new_support='no new Earth raw timing files acquired',comparison='Campbell–HOBO join disabled',shared_genesis_or_ice='not inferred for Mars',restriction='No Earth depth or temperature used to invert MS-03 depth; four-hour offset cause unresolved',source_ids='Existing MS-03 timing handoff')])
# Log actual retrievals, preserving every historical row as an exact byte prefix.
req=json.loads((O/'retrievals.json').read_text());logs=[]
for r in req:
 logs.append(dict(log_id='LV-GAPREQ-'+r['id'],date_taipei='2026-11-15',platform='direct official/author public HTTP',query_or_url=r['url'],status=str(r.get('http_status',r['status'])),actual_read_scope=r['source_basis'],result=('Actual response retained locally/where licensed; see content audit and source_read_log. HTTP success is not science acceptance.' if r.get('bytes') else 'No requested scientific payload obtained; not zero membership.'),spatial_basis='MS-03 fixed cell; source type/selection and centre-vs-footprint scope handled explicitly'))
extra=[('LEVYWEB','publisher web open/click','https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2008JE003273','SupportingInformation links153/155','S1 TXT/PDF fetch failure; support list read, no table acquired'),('EXACTFILES','web search','"2020JE006617" "TableS4" download ; "Cohen-Zada" "DataSet1.tab" ; "Levy" "jgre2606" ds01 ; "University_Valley_Met_Station_Calibration"','Search results and actual publisher methods where relevant','No new original target table or calibration program obtained; no exhaustive repository exclusion')]
for i,platform,query,scope,result in extra:logs.append(dict(log_id='LV-GAPSEARCH-'+i,date_taipei='2026-11-15',platform=platform,query_or_url=query,status='bounded search completed',actual_read_scope=scope,result=result,spatial_basis='No coordinate-only absence claim; original-table membership unresolved'))
write('search_log.csv',logs)
logpath=L/'search_log.csv'
with logpath.open(encoding='utf-8-sig',newline='') as f:rd=csv.DictReader(f);fields=rd.fieldnames;old=list(rd)
seen={r['log_id'] for r in old}
with logpath.open('a',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writerows([r for r in logs if r['log_id'] not in seen])
visual=dict(review_date_taipei='2026-11-15',actually_opened=['MOC_detail_1_native_DN.png','MOC_detail_2_native_DN.png','MOC_detail_3_native_DN.png','F-GAP01_MOC_in_cell_review.png','F-GAP02_spectral_implementation_QA.png','F-GAP03_same_track_radar_clutter.png'],MOC=dict(scope='three fixed512x512windows, not whole-cell complete feature census',observed='fine mottled/textured surface and broad tonal contrasts; no confidently traced closed polygon network in these reviewed windows',not_concluded=['absence of polygons','absence/presence of ice','effective spatial resolving power','full-strip quality qualification']),radar=dict(scope='same observation cropped269x65pixels; no quantitative inversion',observed='Observed signal has repeated curved bands and a low-power zone; model image has different structure. Cause and relation to real subsurface unknown.',not_concluded=['physical cause of curved bands or low-power zone','validated subsurface reflector','ice depth or fraction','all observed features reproduced by model']),figure_QA='Explicit east-positive footprint fixed; legend/footer and radar caption clipping corrected after actual opening; final images reopened.')
dump('visual_review.json',visual)
notes=ROOT/'docs/research/MS-03/local_validation/research_notes.md';text=notes.read_text();heading='## 2026-11-15：MS-03 全缺口逐項補查（MOC／同軌雷達／CAT／撞擊坑原表）'
section='''
- 起始 main：`ddd04cfcb5ea810d73304b1cf6ae064c1f77a1c5`；隔離分支 `codex/ms03-gap-completion-20261115`；保留其他人的工作與以下歷史查核。
- [本輪資料與重現方式](../../../../outputs/research/MS-03/local_validation/gap_completion/README.md)；[逐項缺口／交接表](../../../../outputs/research/MS-03/local_validation/gap_completion/gap_status.csv)；[原始來源實讀範圍](../../../../outputs/research/MS-03/local_validation/gap_completion/source_read_log.csv)。
- 本輪為資料、方法、表格、圖與條列筆記；不代寫正式報告、摘要、結論或簡報。

|項目|本輪確實取得／完成|仍不可推論|
|---|---|---|
|格內影像|MOC `S1700607_NA` 原始 RDR IMG／LBL；2006-04-08；完整檔案 SHA256 與 PDS 像素 checksum 核對；9,272,742個非零格內中心；3個固定512×512視窗實際開啟|3.00034m是投影網格，非實測解析力；沒有可靠閉合多邊形資料，不能說不存在；AD1維持方法參照|
|既有冰暴露目錄|作者 Daubar2022 `6604912` 原 XLSX、provider MD5及CC-BY-4.0；1,203筆事件、固定格內0筆事件座標|只排除該目錄的事件點；不是影像足跡零相交、不是無冰／無研究，也不能代替Dundas2021 S4|
|雷達中心線核對|官方 EDR→USRDR 對照、4條實際GEOM；`S_00796502`中心線0筆格內，`S_04624502`／`S_06059201`／`S_05882501`分別65／64／65筆|目錄足跡相交不保證中心線在格內；沒有對應列的兩條不代表官方完全無資料|
|格內雷達＋雜波|取得`S_04624502_RGRAM`及同觀測combined simulation原始bytes；2016-06-07；65個格內中心、269個原始range rows；有圖和來源|模型不是獨立觀測，強度不能相減；無可信地下反射層pick、介電反演、冰深／含量；回波形狀差異原因未知|
|光譜殘差|取得官方CAT7.4 source，核對multispectral分支；13,169個嚴格來源中心；float32/64差最大約1.26e−7，遠小於原參數殘差最大0.0193473|已排除精度差單獨解釋，未找到真正根因；舊BD1500是不同參數，不能拿來取代BD1500_2；雲霜／儀器QA及檢出界限仍未知|
|三份原始表|本輪再試ScienceBase alternate API、TDL native API、Levy S1 PDF及歷史AGU入口，實際404／403|仍未取得Cohen-Zada原資料／headers、Levy全S1、Dundas全S4；格內成員未知，不填0|
|UV時標|保留原始檔缺件與配時禁令；精確校準檔名搜尋未取得可用程式|未修正四小時差、未和HOBO配時、未用Earth數字反推Mars冰深|

- [MOC影像／固定視窗圖](../../../../outputs/research/MS-03/local_validation/gap_completion/F-GAP01_MOC_in_cell_review.png)；[CAT參數QA圖](../../../../outputs/research/MS-03/local_validation/gap_completion/F-GAP02_spectral_implementation_QA.png)；[同軌雷達／雜波圖](../../../../outputs/research/MS-03/local_validation/gap_completion/F-GAP03_same_track_radar_clutter.png)。
- MOC只實際判讀3個固定視窗：可見細碎紋理與大尺度明暗，未建立可重現的閉合多邊形邊界；不能把全格或全影像寫成已完成地貌普查。原始DN與遮罩crop保留，沒有增強或生成研究影像。
- 原始XLSX的B／C括號方位單位寫反，未悄悄改來源；按Latitude／Longitude變數名稱解析，另以官方`PSP_007561_1290`中心約−50.602°N、305.990°E核對方向。該產品在格外，只作欄位方向查核，不作本格證據。
- 雷達使用GEOM的planetocentric／east-positive座標選中心；`rtrn`的SpacecraftLat是geodetic，沒有混用。官方guide PDF p20／printed19範例確認Column減1、NadirLine直接作零起算row。
- 原始雷達資料與模型網格相容不等於冰已確認。圖內觀測有彎曲重複紋理與低功率帶；本輪未查明其物理／處理原因，未將它們命名為冰層。模型的90km跨軌地形與128ppd來源也可能漏雜波；不能以「模型沒有」證明地下。
- SHARAD 0.0375µs是採樣間隔，10MHz對應15m真空range resolution；不是本格淺冰深真值。現有圖不提供約0.10m熱模型界面的獨立深度驗證，也未宣稱任何薄冰都絕對不可偵測。
- CAT source是可讀實作參照，沒有執行IDL或取得MRDR producer1.03.94的實際執行回條。參數資料與albedo可能經不同正規化是待查假說，未當根因。
- 完整取得／失敗紀錄：[52次HTTP請求](../../../../outputs/research/MS-03/local_validation/gap_completion/retrievals.json)；HTTP200／206仍需內容與科學品質核對。原有搜尋log逐列保留並追加，前輪來源未刪。

|對象|可以直接接續|仍需補件／決定|暫停的分析|
|---|---|---|---|
|主要對話／人類作者|採「固定格資料追溯、QA與可觀測性檢查」定位；使用新增圖與結構表，明列未知|決定是否值得啟用雷達專業判讀與同模式光譜控制；三原表或作者提供原件；新穎性只作有限搜尋結果|首次場址／首次類比、已證實地下冰、冰量、AD1具體幾何類比|
|GPU|可讀相同USRDR／simulation原始range bytes、GEOM與欄位；用現有MRDR原bytes重現殘差|科學使用前處理surface／artefact／clutter與QA，若無可靠pick保留unknown；沒有冰ground truth不自行設threshold|不相減模型power、不把range row直接轉冰深、不追描無可靠邊界、不跨Campbell／HOBO自動配時|
|地球配對／隊友1|AD1仍一般方法參照；UV仍已知界面與資料QA參照，無新候選|有可靠格內Mars邊界才設一致取樣／尺度比較；獨立材料／地下觀測才能討論成因|不把Earth多邊形或深度填入MS-03未知，不宣稱量化最像|

- 本輪實際新增的是固定格的原始影像／雷達取得與檢查、可重跑目錄查詢和參數診斷；沒有新增獨立冰真值，未完成歷史完整的新穎性排除。
- 下方各輪紀錄保留；「尚無同軌雜波／只有目錄」等舊取得狀態，僅適用其當時材料，由本節與新表補充；未將舊unknown改成不存在。

'''
if heading not in text:
 text=text.replace('# MS-03 — local validation evidence notes\n','# MS-03 — local validation evidence notes\n\n'+heading+'\n'+section,1);notes.write_text(text)
# Original tables and analogue rows remain historical records; new tables are linked above.
# Manifest covers retained new deliverables, not ignored optional local bodies.
files=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',str(O.relative_to(ROOT))],cwd=ROOT,text=True).splitlines();entries=[]
for n in sorted(set(files)):
 p=ROOT/n
 if p.is_file() and p.name not in ['manifest.json','validation.json','validation_retained_only.json']:
  raw=p.read_bytes();entries.append(dict(path=str(p.relative_to(ROOT)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
dump('manifest.json',dict(task='MS-03 gap-completion evidence; no formal report',starting_sha=START,branch='codex/ms03-gap-completion-20261115',roi=dict(lat_min=57.5,lat_max=58,lon_east_min=242,lon_east_max=242.5,latitude='planetocentric'),disposition=dict(morphology='unknown',AD1='general_method_reference_only',ice_independently_confirmed=False,actual_ice_depth_m=None,ice_fraction=None,campbell_hobo_aligned=False),actual_http_attempts=len(req),files=entries,optional_ignored_inputs='Full MOC IMG/compressed IMQ, CAT archive/code, publisher HTML/PDF; retained validation never requires them',publication='GitHub records actual PR/head/merge status; this script does not publish'))
# Refresh only affected parent-manifest hashes; preserve all previous provenance fields.
p=L/'manifest.json';m=json.loads(p.read_text());m['gap_completion_supplement']='gap_completion/manifest.json';m['gap_completion_starting_sha']=START
for x in m['files']:
 f=ROOT/x['path']
 if f.exists():raw=f.read_bytes();x.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('Refreshed tables, preserved historical rows, appended new search IDs, and linked bullet notes.')
