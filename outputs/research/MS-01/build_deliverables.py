"""Build MS-01 evidence tables. No network calls; edits only this researcher's outputs."""
from pathlib import Path
import csv, hashlib, json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'outputs/research/MS-01'
DATE = '2026-11-14'
BASE = '3cc8488577535e2fa4d146021fde51f8ff6cc667'
REPO = 'https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei'

SOURCES = {
 'M1': dict(url='https://pds-geosciences.wustl.edu/mgs/urn-nasa-pds-mgs_mola_topography_derived/meg016/', title='MOLA MEGDR 16 pixels/degree', read_scope='本機IMG/LBL及基準原生統計；本次重提取', period='label START 1997-09-15T19:10:00; STOP 2001-06-30T11:10:40; 個別格觀測日期未知', resolution='1/16 degree; 約3.7 km南北/坡度基線', depth='surface topography', extent='56.5–57N,72.5–73E內64原生格中心'),
 'M2': dict(url='https://pds-geosciences.wustl.edu/mgs/mgs-m-tes-5-timap-v1/mgst_9001/data/', title='TES night thermal inertia 2007 product and infill mask', read_scope='本機IMG/LBL、原始遮罩；本次重提取', period='START/STOP N/A; 2007-01-30為產品製作日', resolution='1/20 degree; 約3 km南北', depth='熱反演有效深度依週期/材料；非固定鑽深', extent='MS-01名義格100原生格；mask=0剔27，保留73'),
 'M3': dict(url='https://swim.psi.edu/SWIM2Products.php', title='SWIM2.0 combined ice consistency', read_scope='提供者Global Composite及兩深度GeoTIFF；本次重提取', period='2021-02-24產品；多儀器跨期，非同時觀測', resolution='0.05 degree網格；各儀器有效解析度更粗且不同', depth='0–1m / 1–5m敏感深度分區，非冰層上下界', extent='MS-01名義格各100格中心'),
 'M4': dict(url='https://doi.org/10.1029/2019JE006111', title='Montabone dust climatology; local files MY34/MY35 v2.5', read_scope='基準metadata及本機NetCDF重提取；未重審整篇方法文', period='MY34及MY35，各669重建sol', resolution='3x3 degree; 重建每日', depth='9.3 micrometre absorption total atmospheric column', extent='最近原生座標55.5N72E；非MS-01局地站'),
 'M5': dict(url='https://doi.org/10.5281/zenodo.17947556', title='Wang/Jin MCS time-adjusted temperature', read_scope='基準metadata及本機NetCDF重提取；不另聲稱原論文全文重審', period='MY29–36; Ls每10degree;03/15 LTST', resolution='5x5 degree', depth='校時衍生地表溫度；非氣溫/地下溫度', extent='最近原生座標55N75E；格中心/邊界語意未確認'),
 'U1': dict(url='https://doi.org/10.1017/S0954102022000025', title='Marinova et al. 2022 Climate and energy balance of the ground in University Valley', read_scope='出版社全文Methods/Meteorological measurements、Thermal diffusivity、Results/Model validation、Fig1與Appendix', period='2009-12部署至2013-01-31；各sensor有效期不同', resolution='Campbell30min; Onset60min; 點測', depth='air1.2m; wind1.08m; solar1.27m; ground0,0.10,0.42,0.49m', extent='W/S/M/D四站；非全谷平均'),
 'U2': dict(url='https://doi.org/10.1002/2016JF004054', title='Fisher et al. 2016 Ground surface temperature and humidity...', read_scope='原始全文摘要、§2、邊界條件與REGO模擬；不採其衝突經度', period='文內2010–2011站資料與理想化模擬；非本次新量測', resolution='點測/一維模型', depth='土面及冰表；隨剖面', extent='University Valley；精孔座標與本候選尚未逐孔配準'),
 'U3': dict(url='https://doi.org/10.1017/S0954102017000402', title='Williams et al. 2018 (online2017) The effects of snow and salt...', read_scope='PMC作者全文Introduction/Methods/Results；座標163.758E衝突不採', period='氣象驅動及理想化積雪/鹽情境', resolution='一維數值模型；不是全谷測值', depth='可變覆土厚度', extent='University Valley過程模型'),
 'U4': dict(url='https://doi.org/10.1017/S0954102025100448', title='McKay et al. 2026 Summer snow determines the depth...', read_scope='原始PDF pp122–134；特讀pp130 TableII、p132 Mars及雪日定義', period='University部分主分析2009-12–2010-12；shallow註腳2011', resolution='半小時事件加總雪日/一維年平均模型', depth='W冰表0.42m；其他測站與模式深度區分', extent='University Valley測站及模擬up/down-valley；另有Elephant Head，未移植'),
 'U5': dict(url='https://doi.org/10.5281/zenodo.10553882', title='NASA University Valley field datasets, Zenodo v1 2024', read_scope='提供者檔名/MD5清單；本機原作者processed calibrated txt核對MD5後本次重算', period='本次只用UniversityV_09_10_Campbell_data_good_only_calibrated.txt內實際時間範圍', resolution='名義30min; 缺值保留；時區未明', depth='T107_surf/10cm/ice42cm/InIce49cm; air1.2m', extent='W站，非S/M/D、非2013全序列'),
 'B1': dict(url='https://doi.org/10.1029/2017JF004535', title='Liu et al. 2018 Thermal Regime and Properties...', read_scope='出版社全文§2–5、Table1/2、Figs2/5/6；原始逐時檔未取得', period='1999–2011 hourly; 土樣實驗與模型物性', resolution='逐時點溫/一維模型/土樣', depth='0.02,0.10,0.20,0.30,0.45,0.60m；鄰多邊形孔4,9,14,19.6m', extent='中央谷單一polygon穩定部與鄰孔；出版概略錨點到分，無精孔GPS'),
 'B2': dict(url='https://doi.org/10.1002/2014JF003415', title='Liu et al. 2015 Enhanced model of sublimation...', read_scope='出版社全文§2、Table1、§3–4及資料聲明；原始檔未取得', period='1999–2011; camera2009-01–2011-01', resolution='T/RH10sec→hourly; camera3h;1D模型', depth='覆土0.30m；EC0.05m；測溫0.02–0.60m', extent='中央谷剖面，距polygon trough5.9m；不假設與2003/2006同孔'),
 'B3': dict(url='https://www.arlis.org/docs/vol1/ICOP/55700698/Pdf/Chapter_160.pdf', title='Putkonen, Sletten & Hallet 2003 Atmosphere/ice energy exchange...', read_scope='原始3頁pp913–915 §2–5/Figs1–2；root取逾時，協作研究者成功讀取', period='一年記錄，文未明確曆起訖', resolution='點測/雙層熱模型', depth='約0.30m覆土；氣象sensor高度未列', extent='mid-valley(-77.84,160.60)及lower(-77.80,160.71)另站'),
 'B4': dict(url='https://doi.org/10.1017/S0954102006000460', title='Kowalewski et al. 2006 Quantifying low rates of summertime sublimation...', read_scope='出版社摘要及作者稿Methods/Results pp1–8（正式pp421–428）', period='2004-11-18–12-29南極夏季', resolution='15min點測/水汽擴散模型', depth='0.50m覆土；近地2cm濕度', extent='中央谷17m polygon中心附近另站，無共用逐孔GPS'),
 'G1': dict(url='https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/mars-atmosphere-equation-english/', title='NASA Glenn Mars atmosphere', read_scope='Atmosphere of Mars 段；僅全球定性背景', period='一般行星背景；非MS-01觀測期', resolution='全球定性', depth='atmosphere', extent='Mars/Earth整體；不用來代填本站氣壓/風')
}
RESOLUTIONS={
 'M1':('跨軌合成；格內觀測時刻/時間解析度未知','1/16 degree；約3.7km南北；坡度同基線'),
 'M2':('夜間觀測合成；確切時間解析度未知','1/20 degree；約3km南北'),
 'M3':('跨儀器/跨期合成；無單一時間解析度','0.05 degree輸出格距；原儀器有效解析度不同'),
 'M4':('每火星年669個等距重建sol','3x3 degree'),
 'M5':('Ls10degree bins；名義03/15 LTST；MY29–36','5x5 degree；非現地站'),
 'U1':('Campbell30min/Onset60min；依sensor','W/S/M/D離散點測；非面平均'),
 'U2':('站點記錄/理想化模型各異；本文未統一','點柱/一維模型；無面解析度'),
 'U3':('重複一年氣象強迫的time-marching模型；非觀測解析度','一維土柱模型；非面測量'),
 'U4':('半小時事件加總等效雪日/年平衡模型','測站點柱及假設土柱；非面平均'),
 'U5':('名義30min；缺值保留；時區未明','W站單一土柱/氣象sensor；非面平均'),
 'B1':('逐時測溫；物性實驗/模型無觀測cadence','單一polygon剖面及鄰孔；土樣，非面平均'),
 'B2':('air/RH10s→hourly；camera3h；EC hourly','中央谷點剖面及相片視場；視場邊界未取得'),
 'B3':('一年記錄；文未統一列出觀測cadence','mid/lower兩個離散站；非同孔'),
 'B4':('15min；短夏季2004-11-18–12-29','單一17m polygon內點測'),
 'G1':('不適用，全球定性背景','不適用，全球定性背景')}
for sid,v in SOURCES.items():
    v['accessed_date']=DATE
    v['temporal_resolution'],v['spatial_resolution']=RESOLUTIONS[sid]

def write_csv(name, rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2)+'\n')
    candidates=[
      dict(candidate_id='MS-01-E01',name='University Valley W/S/M/D station network',latitude=-77.86215,longitude=160.7101,coordinate_basis='W=77°51.729S 160°42.606E; U1 Methods',coordinate_precision='出版到0.001 arcmin；datum未列，不作GPS精度聲稱',scope='W/S/M/D站點及其最小經緯外包框（索引用，非連續實測面積）',south=-77.8657666667,north=-77.8597333333,west=160.7101,east=160.7286666667,boundary_basis='U1四站座標；站間未量測不補值；不把全谷1.5km當同一樣本',purpose='覆土深度/材料與地表—冰面熱波的可辨識性；表面與大氣水汽邊界差異',available_data='U5公開校正序列；本次核對MD5並重算W站部分年與11天熱波；其餘僅文獻',disposition='保留',rationale='冰表層位已知且有多深度同步溫度；可作方法驗證，非整體氣候等價',next_step='下載S/M/D同期間序列，核對時區與sensor QA；同時窗/相同forcing交叉驗證多層熱模型',limits='無共同尺度坡度、無本站AOD；冰表8–42cm不能推成火星1–5m冰深；長極晝夜與火星日週期不同',source_ids='U1;U2;U3;U4;U5'),
      dict(candidate_id='MS-01-E02',name='Central Beacon Valley instrumented polygon',latitude=-77.8166666667,longitude=160.65,coordinate_basis='B1 §2:77°49S160°39E',coordinate_precision='出版僅到arcmin；是概略定位，非精孔GPS；datum未列',scope='B1單一多邊形內測溫剖面及鄰近多邊形深孔',south='',north='',west='',east='',boundary_basis='B1 §2/Fig1；邊界多邊形與逐孔GPS未公布；不自設半徑或以整谷代替',purpose='乾覆土—塊狀冰界面傳熱、物性誤設與雪事件對冰保存模型的影響',available_data='B1/B2公開全文與表；GCMD原始資料入口回502，本次未下載逐時資料',disposition='保留（原始序列待補）',rationale='埋冰界面與物性已報導，與E01不同冰形態可檢查模型假設；資料取用較弱',next_step='追查GCMD資料遷移ID/新目錄並取逐時檔、逐孔GPS；重現B1熱相位與剖面',limits='谷名概略座標有160/161E衝突；無共同尺度DEM/AOD；不能外推MS-01冰純度、形成史或昇華率',source_ids='B1;B2;B3;B4')]
    write_csv('candidates.csv',candidates)
    ev=[]
    def add(cid,dimension,quantity,value,unit,sid,locator,kind,limit,**overrides):
        src=SOURCES[sid]
        row=dict(evidence_id=f'EV-{len(ev)+1:03}',candidate_id=cid,dimension=dimension,quantity=quantity,value=value,unit=unit,source_id=sid,source_url=src['url'],locator=locator,data_kind=kind,observation_period=src['period'],depth_height=src['depth'],temporal_resolution=src['temporal_resolution'],spatial_resolution=src['spatial_resolution'],representative_extent=src['extent'],uncertainty='未另提供/未另估，詳限制',comparability_and_limit=limit,accessed_date=DATE)
        row.update(overrides);ev.append(row)
    add('MS-01','terrain','mean_elevation',-3700.9141272608,'m areoid','M1','final_candidates.csv:MS-01/mola_elevation_m_mean; LBL START/STOP','產品推估＋本次重算','MOLA格含產品插值；64/64有限不是64次直接雷射；不得跟地球海拔作壓力相等推論')
    add('MS-01','terrain','mean_slope',0.287206803314722,'degree','M1','MS-01/mola_slope_deg_mean','本次計算（產品DEM梯度）','約3.7km基線；非米級坡度/安全')
    add('MS-01','terrain','relief',76,'m','M1','MS-01/mola_relief_m;max=-3661,min=-3737','本次計算','僅名義格內格中心max-min，非整個連續地形真值')
    add('MS-01','thermal','night_thermal_inertia_mean',325.1557373608713,'J m^-2 K^-1 s^-0.5','M2','MS-01/TES_TI_mean;mask_zero=27;valid=73/100','產品反演＋本次重算','287–373；不是溫度或硬度；空間支持不同於土樣k/c；非當地實測')
    add('MS-01','water_ice','SWIM_0_1m_consistency',0.6392249220197742,'1','M3','MS-01/SWIM_0_1m_mean;100/100','多源產品推估＋本次重算','一致性非冰量/機率；熱與中子等共享來源',depth_height='0–1m敏感分區')
    add('MS-01','water_ice','SWIM_1_5m_consistency',0.647481749755862,'1','M3','MS-01/SWIM_1_5m_mean;100/100;positive99','多源產品推估＋本次重算','非獨立互證；min0/max1是產品值而非冰層孔隙率',depth_height='1–5m敏感分區')
    for year,mean,p95 in [('34',0.11926438338687068,0.22245603501796724),('35',0.10753491588259848,0.18014705479145052)]:
        add('MS-01','atmosphere_dust',f'MY{year}_dust_mean',mean,'1','M4',f'MS-01/dust_my{year}_mean_cdodtot','重建產品＋本次重算','9.3μm吸收整柱；不可與地球可見AOD/RH/落塵速率直接相減',observation_period=f'MY{year}；669/669重建sol')
        add('MS-01','atmosphere_dust',f'MY{year}_dust_p95',p95,'1','M4',f'MS-01/dust_my{year}_p95_cdodtot','本次計算（重建產品）','p95非暴風或設備失效機率',observation_period=f'MY{year}；669/669重建sol')
    add('MS-01','thermal','MCS_populated_day_median',247.47932050390625,'K','M5','MS-01/MCS_populated_day_median_K;161/288bins','校時產品推估＋本次重算','15 LTST；QA/樣本數/不確定度未知；不能與地球全年氣溫平均比',depth_height='surface-derived temperature')
    add('MS-01','thermal','MCS_populated_night_median',173.72867814892578,'K','M5','MS-01/MCS_populated_night_median_K;145/288bins','校時產品推估＋本次重算','03 LTST；不同缺測季節；非當地實測',depth_height='surface-derived temperature')
    add('MS-01','thermal','MCS_paired_contrast_median',63.53643660583495,'K','M5','MS-01/MCS_paired_contrast_median_K;69/288 paired','本次計算（衍生bins）','同MY/Ls仍非同sol；非每日振幅，亦不等於兩個個別中位數相減')
    add('MS-01','water_ice','actual_ice_depth_purity_continuity','unknown','unknown','M3','SWIM2產品限制；無現地真值','未知','不得從一致性直接反推')
    add('MS-01-E01','terrain','station_elevations','W1677;S1684;M1661;D1697','m a.s.l.','U1','Methods/Meteorological measurements; Fig1','文獻場址觀測','不同站點海拔不等於共同DEM高差；未計同尺度坡度')
    add('MS-01-E01','water_ice','ice_table_depths','W0.42;S0.08;M0.22;D0.36','m','U1','Methods/Meteorological measurements','實測層位（原文）','只代表各站；不是全谷冰深分布，更非MS-01真值')
    add('MS-01-E01','thermal','dry_soil_thermal_diffusivity',6.9e-7,'m^2 s^-1','U1','Methods/Thermal diffusivity; Appendix','觀測約束推估','適用-5至-25°C；較冷時隨溫度變；非TES_TI',depth_height='W乾覆土0–0.42m',temporal_resolution='多深度溫度擬合後物性；無獨立觀測cadence',uncertainty='方法與溫度依賴；此值無單一誤差條')
    add('MS-01-E01','atmosphere_dust','air_mean_temperature',-23.4,'degree_C','U1','Abstract; Results collected weather data/TableII','實測摘要（原文）','地球空氣1.2m與MCS地表5°不同定義，禁止直接差值排名',depth_height='air1.2m')
    add('MS-01-E01','atmosphere_dust','site_AOD_dust_deposition_pressure','unknown','unknown','U5','檔案表頭無相應欄','未知','無資料不填0；wind資料只能作本站地球表面熱通量邊界')
    add('MS-01-E01','water_ice','ice_depth_if_summer_snow_days_14_or_40','0.66;0.17','m','U4','p130 TableII down-valley/up-valley','模式情境推估','非實測地點值；14/40是等效雪日，非實際降雪事件數；不代入火星',observation_period='2009–2010驅動的變動情境',depth_height='model equilibrium interface')
    add('MS-01-E02','terrain','polygon_diameter','10–20','m','B1','§2 Geologic Setting','文獻形貌觀測','MS-01 MOLA不解析這尺度；本次未知MS-01是否具同形貌')
    add('MS-01-E02','water_ice','dry_cover_at_profile',0.30,'m','B1','§2 Geologic Setting;Fig1','實測層位（原文）','已知塊狀冰是對照類型；不證明MS-01塊狀冰')
    add('MS-01-E02','thermal','soil_heat_capacity','580–690','J kg^-1 K^-1','B1','§3.1.2/3.2;Fig2a','土樣實驗實測','0.10m土樣，-50至+10°C；測量日期未列；不是火星值',depth_height='0.10m土樣',observation_period='實驗日期未列；與1999–2011氣候記錄不同',temporal_resolution='實驗溫度掃描；非逐時氣候cadence',spatial_resolution='0.10m層位取得的土樣；非面平均')
    add('MS-01-E02','thermal','soil_conductivity','0.22–0.27','W m^-1 K^-1','B1','§3.1.3/3.2;Fig2b','半經驗模型推估','-47.9至+7.5°C範圍；空氣孔隙氣體與火星不同；不是原位直接量測',observation_period='2018論文所報告物性模式範圍；無量測期',depth_height='0.10m層位代表土樣模型',temporal_resolution='不適用，物性模型',spatial_resolution='代表土樣物性；非面平均')
    add('MS-01-E02','thermal','model_soil_bulk_density',1650,'kg m^-3','B1','§3.2;Table1','實驗約束後採用的模型參數','3層實驗1620–1750；端點非同一樣本/時刻，不製造誤差加權分數',observation_period='土樣實驗日期未列；模型採用值',depth_height='1–5、10–15、25–30cm土樣約束',temporal_resolution='不適用，模型物性參數',spatial_resolution='三層土樣約束；非面平均')
    add('MS-01-E02','thermal','thermistor_calibration_accuracy',0.02,'degree_C','B1','§2 Geologic Setting','儀器校正規格','不含代表性/孔位/模型誤差',depth_height='土0.02–0.30m/冰0.45–0.60m及鄰深孔',observation_period='儀器校正；日期未列',temporal_resolution='不適用，校正規格',spatial_resolution='單一探針規格，非面解析度')
    add('MS-01-E02','water_ice','model_sublimation_rate',0.11,'mm a^-1','B2','Abstract;§4 Summary','模式推估','1999–2011平均；含積雪/融雪；非直接冰損實測，不能外推火星')
    add('MS-01-E02','atmosphere_dust','air_RH_sampling','10s measured; hourly averaged','time','B2','§2.2 Field Data Collection','實測方法（原文）','原始序列未取得；RH對水需轉對冰；不是9.3μm整柱光學厚度',depth_height='air; sensor height not specified')
    add('MS-01-E02','atmosphere_dust','site_AOD_dust_deposition_pressure','unknown','unknown','B2','§2.2/資料聲明未提供已取得對應序列','未知','不把區域乾旱/強風當成火星沙塵相同')
    uv=json.loads((OUT/'analysis/uv_diurnal_fit.json').read_text())
    for v in uv['values']:
        add('MS-01-E01','thermal','24h_harmonic_half_amplitude_'+v['column'],v['diurnal_amplitude_K'],'K','U5','txt column '+v['column']+'; analysis/uv_diurnal_fit.py;uv_diurnal_fit.json','本次計算（已公開實測序列）','OLS含線性趨勢；528共同樣本；無振幅不確定度，非max-min；只示範衰減，不能反演MS-01冰深',observation_period='2010-11-07 00:00 inclusive – 2010-11-18 00:00 exclusive；時區未核明',depth_height=str(v['depth_m'])+' m below surface',uncertainty='未估計振幅信賴區間；residual RMSE='+str(v['residual_rmse_K'])+' K')
    write_csv('evidence.csv',ev)

    prior=[]
    def p(pid,cid,sid,cls,scope,question,data,method,diff):
        prior.append(dict(prior_id=pid,candidate_id=cid,source_id=sid,source_url=SOURCES[sid]['url'],classification=cls,read_locator=SOURCES[sid]['read_scope'],prior_scope=scope,prior_question=question,prior_data=data,prior_method=method,this_work_difference=diff,novelty_limit='有限檢索；已有直接或部分先例；未查到MS-01配對不等於從未研究',accessed_date=DATE))
    p('PW-U1','MS-01-E01','U1','直接先例','相同W/S/M/D網絡','冰表深度與能量收支/熱參數','2009–2013多深度氣象','能量收支模型及參數敏感度','本次僅重算W站短窗熱波與部分年QA，評估MS-01缺什麼觀測；未重現原3年模型')
    p('PW-U2','MS-01-E01','U2','直接先例','同谷與明列W站方法座標；精孔仍待配準/概略經度衝突','surface vs air水汽邊界對冰深的影響','站測及理想化強迫','REGO一維水汽模型','本次將邊界不確定性列為MS-01假設；不重跑REGO、不認領新水汽機制')
    p('PW-U3','MS-01-E01','U3','部分重疊','同谷；模式用途相近','雪補給與鹽脫水對冰表穩定性','站氣象＋假設鹽/雪','time-marching土壤/雪模型','本次無MS-01鹽/雪真值，不把模型假設變成當地結論')
    p('PW-U4','MS-01-E01','U4','直接先例','含相同University測站','夏雪造成地表水汽增強/冰深變化','既有年循環及情境','水汽平衡敏感度','本次保留其火星外推限制；明確指出2026已研究相同機制，無新穎性聲稱')
    p('PW-B1','MS-01-E02','B1','直接先例','主錨點中央谷polygon及鄰孔','乾土/冰導熱率與熱剖面','1999–2011小時溫度/土樣物性','FDM/FVM一維導熱及敏感度','本次不重跑原模型；比較TI與地面物性尺度，提出MS-01材料—冰界面可辨識性驗證')
    p('PW-B2','MS-01-E02','B2','部分重疊','中央谷0.30m剖面，同研究群但原文概略經度衝突','雪/融雪對埋冰昇華影響','12年氣象/EC＋2年相片','一維水汽擴散及200ka延伸','本次只採機制/資料需求，無MS-01昇華率或年代外推')
    p('PW-B3','MS-01-E02','B3','部分重疊','mid/lower另兩站','薄碎屑熱交換','一年未列曆期觀測/針探與實驗','雙層熱模型','非B1同孔；本次不平均0.2/0.3/0.4不同來源k')
    p('PW-B4','MS-01-E02','B4','部分重疊','另個17m polygon/0.50m覆土','夏季昇華的濕度/雪敏感度','2004短夏季15min站測','水汽模型','本次改為MS-01觀測可辨識性；不以短夏季代全年，也不宣稱同精孔')
    write_csv('prior_work.csv',prior)
    searches=[]
    def s(cid,platform,q,result,read=''): searches.append(dict(search_id=f'SR-{len(searches)+1:03}',date=DATE,candidate_id=cid,platform=platform,query=q,result=result,read_scope=read,limitation='有限網頁/文獻檢索，非全球完整文獻庫或新穎性證明'))
    s('MS-01','GitHub REST API','GET branches/main','base='+BASE,'branch commit/tree SHA')
    s('MS-01','GitHub REST API','GET contents/docs/TEAM_START.md?ref=main','404；本機有，但未發布')
    s('MS-01','GitHub REST API','GET contents/outputs/handoff?ref=main','404；再核對recursive tree確認缺件')
    s('MS-01-E01','web search engine2','University Valley Antarctica dry permafrost ice table thermal properties McKay Marinova 2013 2016','U1/U2/U3/U4候選線索','後以原始全文核對')
    s('MS-01-E02','web search engine2','Beacon Valley Antarctica debris covered buried ice thermal vapor diffusion Mars analog sublimation Kowalewski 2006','B2/B3/B4候選線索','後以原始全文核對')
    s('MS-01-E01','web search engine1','"Climate and energy balance of the ground in University Valley" data Zenodo','U1/U5','全文Methods、站座標；Zenodo MD5')
    s('MS-01-E02','web search engine1','"Atmosphere/ice energy exchange" Beacon Valley Putkonen 2003','B3','3頁原始PDF；root open逾時、協作研究者成功')
    s('MS-01','web search engine1','SWIM 2.0 ice consistency not ice abundance thermal inertia 2021','M3與SWIM原理頁','產品Composite及共享資料/歧義')
    s('MS-01-E01','web search engine1','"University Valley" "56.75" "72.75" thermal ice','未確認此MS-01明確配對文獻','不是從未研究證明')
    for q,res in [
      ('"Beacon Valley" "Quantifying low rates" 2006 PDF','B4摘要/作者稿'),
      ('"An enhanced model" "2014JF003415" Beacon Valley','B2全文'),
      ('"Atmosphere/ice energy exchange" Beacon Valley 2003','B3全文'),
      ('"Beacon Valley" thermal ice data repository Liu Sletten 1999 2011','B1/B2資料聲明'),
      ('"Beacon Valley" "160.580" polygons 2008 Levy','Levy2008搜尋片段；未全文採用'),
      ('"Beacon Valley" "56.75" "72.75"','未保留明確配對來源'),
      ('"Beacon Valley" "thermal inertia" Mars ice regolith','無新增主來源'),
      ('"2017JF004535" data Beacon Valley repository','B1全文；GCMD入口502')]: s('MS-01-E02','web search engine1',q,res,'詳prior_work與sources')
    s('MS-01','web search engine1','site.science.nasa.gov mars facts atmosphere carbon dioxide thin','NASA官方氣體/低壓定性背景','使用G1；不以全球值代填本站')
    for q,res in [('University Valley Antarctica "Climate and energy balance" 2021','U1出版年校正為2022'),('"University Valley" "2016JF004054"','U2全文'),('"University Valley" "163.758" "160"','U1/U2/U3座標衝突')]:s('MS-01-E01','web search engine1',q,res,'Methods/站點座標/相關模型')
    for sid,locator in [('U1','Methods/Results/Appendix，PDF p153 TableII/III'),('U2','§1/2/4.1'),('U3','Meteorological/model/TableI/Discussion'),('U4','pp129–130 TableII；pp132–133 Mars'),('U5','Files/MD5')]:s('MS-01-E01','直接開原始來源',SOURCES[sid]['url'],'讀取成功',locator)
    write_csv('search_log.csv',searches)

if __name__=='__main__':main()
