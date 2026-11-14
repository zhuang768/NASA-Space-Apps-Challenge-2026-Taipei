"""Compile acquisition/search provenance and supersession ledger. Idempotent."""
import csv,json,hashlib,datetime
from pathlib import Path
P=Path(__file__).resolve().parent

def save(name,rows):
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (P/name).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def main():
 logs=[json.loads(l) for l in (P/'acquisition_log.jsonl').read_text().splitlines() if l.strip()]
 for r in logs:
  for k in ['url','final_url']:
   if 'X-Amz-' in r.get(k,''):r[k]=r[k].split('?')[0]
 (P/'acquisition_log.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in logs))
 old=[r for r in csv.DictReader((P/'search_log.csv').open(encoding='utf-8-sig')) if r['search_id'].startswith('LV-')]
 for r in old:r['review_state']='prior-round historical search; failures not current blanket access claims'
 extra=[
 ('Web search','"52.75" "168.25" Mars ice','no relevant local paper in returned results; irrelevant matches excluded','results only; not evidence of never studied','LP-14'),
 ('Web search','"D01_027516_2328" ice','no relevant paper identified','result list only; footprint established separately in ODE','LP-14'),
 ('Web search','"G23_027160_2321" OR "J02_045529_2335" OR "K01_053836_2341" OR "V16_086396_2333"','no relevant paper identified','result list only; no never-studied claim','LP-14'),
 ('Web search','"Mars" "168" "53" "Cebrenia" ice','irrelevant/historical matches excluded','result list only','LP-14'),
 ('Web search','"00464501" "ice" Mars','irrelevant skating record excluded','result list only; orbit not confirmed literature use','LP-14'),
 ('Web search + USGS','"mAl" "Middle Amazonian lowland" ice Skinner','Skinner2012 DOI10.1130/G33513.1; regional mapping','USGS abstract; SIM3292 Middle Amazonian citation chain; not full article','LP-15'),
 ('Publisher web','https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019GL083947','method and limits read; archive5files acquired','sections2–3; 2-layer model;6cm–1m;3ppd text vs2ppd archive','LP-08;ME-12'),
 ('Publisher web','https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2012JE004053','specific Haughton co-located GPR/core study','2.3;3.1–3.3;4;5.2; excavation0.9m caveat; no raw field arrays','AV-07'),
 ('Publisher web','https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2017JF004535','specific Beacon thermal/material study','2;3.1–3.3;Table1;Fig2; adjacent deep polygon separated','AV-06'),
 ('Primary PDF','https://doi.org/10.1017/S0954102022000025','full PDF text extracted; p162 rendered and visually checked','TableII p153;Fig6/p162;Appendix;measuredT/derivedaw;42cm interface','AV-01;I06'),
 ('Primary PDF','https://backend.orbit.dtu.dk/ws/files/329047704/1_s2.0_S0277379123001853_main.pdf','22-page primary PDF read; core date resolved','3.2 p5 September2019;4.2;5.4;Fig13','AV-02;CS1-DATE'),
 ('Primary data','https://doi.org/10.5281/zenodo.11187360','all16sheets inspected;12cores exported','Overview;Core_*;README drawing UTM33N;two out-of-range fields','AV-05'),
 ('Web fetch','https://swim.psi.edu/LPSCProducts.php','timeout on retry; earlier partial page inspection not WEH data acquisition','neutron consistency is not rawWEH; source unavailable on retry','ME-11'),
 ('Repository Excel','outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx','all32sheets and rows inventoried','workbook_inventory.csv; older contexts not local observations','scope inventory'),
 ('USGS original GIS','https://pubs.usgs.gov/sim/3292/downloads/sim3292_database.zip','ZIP downloaded and shapefile extracted; ROI inside OBJECTID1252 mAl','originalshp/dbf/prj;1:20M;Mars2000sphere;geography_check.json','ME-17'),
 ('USGS Gazetteer','https://planetarynames.wr.usgs.gov/Feature/348','MDIM2.1 actual polygon vsMDIM2.0 rectangle tested','HTML WKT geometry25330 vs348; approximate boundary','ME-18')]
 for i,(platform,q,out,read,used) in enumerate(extra,1):old.append(dict(search_id=f'R-S{i:03}',date='2026-11-15',platform=platform,query_or_url=q,purpose='bounded source validation',outcome=out,pages_or_extent_read=read,used_in=used,review_state='executed this round'))
 for i,r in enumerate(logs,1):
  outcome=r.get('error','HTTP '+str(r.get('status'))+'; bytes='+str(r.get('bytes')))
  dest=P/'sources'/r['name']
  if dest.exists() and dest.suffix=='.json':
   try:
    d=json.loads(dest.read_text()).get('ODEResults',{});
    if d:outcome+='; ODE status='+str(d.get('Status'))+'; count='+str(d.get('Count'))
   except (ValueError,AttributeError):pass
  old.append(dict(search_id=f'R-A{i:03}',date=r.get('retrieved_utc',''),platform='direct HTTPS request',query_or_url=r['url'],purpose=r['name'],outcome=outcome,pages_or_extent_read='Downloaded bytes; analysis use only as listed in evidence/manifest; not every downloaded page interpreted',used_in='acquisition_log.jsonl',review_state='executed this round'))
 save('search_log.csv',old)
 corrections=[
 ('GEO','PR6 local_notes;PR10','地質單元未知；Arcadia bbox位置','已被取代','mAl全格；MC7Cebrenia；MDIM2.1不相交','ME-17;ME-18','原始GIS/Gazetteer','人類更新正式稿'),
 ('ACCESS','PR6 description/local_notes','PDS/ODE/USGS一律無法下載','已被取代','本輪實際取得目錄、原始雷達、熱模型、光譜、GIS；個別失敗另列','acquisition_log.jsonl','HTTP+hash','人類更新正式稿'),
 ('C20','PR9 ledger;PR6 claims','CS1/ADE/WISDOM為同址冰雷達驗證鏈','禁止引用','三組分址；未知測線不能接真值','AV-02..05;AV-09','CS1/ADE座標與WISDOM摘要','保持降級'),
 ('C21','PR9 ledger','WISDOM介電常數當獨立實測','禁止引用','標模型輸入；未取得同線獨立真值','AV-04','原摘要／§8B','保持降級'),
 ('C22','PR9 ledger','0.35cm/yr作長期平均或火星覆土率','禁止引用','峰值期；CS1風成覆土與同生冰子過程','AV-02','Rasmussen2023 §5.4/Fig13','保留限制'),
 ('CS1-DATE','PR6 description','CS1取芯時間未知','修正','September2019；2022年8月露頭另址20mNE','AV-02','Rasmussen2023 §3.2 p5','人類更新'),
 ('C23','PR9 ledger','60–100cm活動層與UNISCALM>=1m拼成單值','禁止引用','不同來源/時期未調和；不得由CS1取芯日期解決此差異','AV-03','PR9 C23; Rotem引用與UNISCALM','保持限制'),
 ('C24/H2/H3','PR6 report early sections;PR9','降級前覆土＋雷達用途','禁止引用','只能按最新§8B及此local_validation範圍','AV-09','三組足跡','人類清除殘留，不改正式稿'),
 ('I06/EV-018','PR10 unresolved;PR6 evidence','2560h當雙變量實測或純能量模型時數','修正','記錄T累積年化時數；aw是冰/水蒸氣壓比計算；不推MS02可居住性','AV-01','Marinova2022 p162 Fig6 (rendered)','人類精確標量測/計算'),
 ('I08','PR10 unresolved','UniversityValley S/D跨文獻座標混用','保持未解','本輪只以W站界面/熱資料；不移接S/D','AV-01','TableI/歷史交接','需原始station metadata'),
 ('UV-COVER','PR6 inherited uses','15cm活動層當乾覆土總厚度','禁止引用','W站冰表42cm；15cm為0C等溫面活動層估計','AV-01','TableII/pp152–153','人類修正'),
 ('MCS-ORDER','local_notes ME10;PR9 context','15/03日夜值顛倒','修正','day246.3053K night171.2721K；paired median66.8305K另統計','ME-10','final_candidates.csv named fields','不當當地地表/地下溫度'),
 ('SWIM-BINARY','oldlocal ME06','24.5/100格之假設比例','撤回','平均與極值不能建立二值分布；空值保留','ME-06','統計識別限制','禁止當觀測占比或冰量'),
 ('ICE-DEPTH','PR6/local_notes;PR10','本格熱深度值未取得','修正','模型像元0.4499824941m；真實深度未知','ME-12;MV-02','Caltechrow74col336','可引用須連模型假設'),
 ('BEACON','PR6 E02','整個Beacon候選升級','不支持整體升級','僅Liu2018特定位置熱材料子案例','AV-06','primary2–3.3','人類決定是否採用子案例'),
 ('HAUGHTON','PR6 E04','雷達穿透未擾動覆土已驗證','禁止引用','Thomson2012挖除約0.9m後同測線GPR/core方法子案例','AV-07','primary3.1–3.3','不能併原河谷/gully鏈')]
 save('claim_corrections.csv',[dict(claim_id=a,affected_record=b,old_or_prohibited_claim=c,disposition=d,replacement_or_limit=e,evidence=f,locator=g,human_action=h) for a,b,c,d,e,f,g,h in corrections])
 # Align additional scale-gap rows, preserving unrelated context rows.
 rows=list(csv.DictReader((P/'scale_gap_resolution.csv').open(encoding='utf-8-sig')))
 for r in rows:
  if r['id']=='SG-06':r.update(finest_data_in_repo_or_excel='Piqueux2019 conditional two-layer thermal model',cell_value='model drylayer0.4499824941m',limit='not direct overburden thickness; accumulation rate/material unknown',status='Conditional model available; actual cover unvalidated',minimum_data_needed='independent interface/material observation')
  if r['id']=='SG-07':r.update(finest_data_in_repo_or_excel='5CTXbrowse images with nominal footprints',cell_value='nominalunion100%ROI',limit='lowcontrast/variable downsampling; no calibrated morphometry/change analysis',status='Images acquired; local morphology not quantitatively classified',minimum_data_needed='calibrated orthorectified repeat imaging/DTM')
 save('scale_gap_resolution.csv',rows)
if __name__=='__main__':main()
