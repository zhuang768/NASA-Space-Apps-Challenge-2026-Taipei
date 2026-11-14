"""Build the bounded three-target synthesis from frozen, source-located cards.

No external downloads, new science calculation, ranking or source-branch edits.
Run from any working directory: python3 outputs/integration/science/build.py
"""
from pathlib import Path
import argparse,csv,hashlib,json,re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REPORT=ROOT/'docs/integration/science/synthesis.md'
DATA=json.loads((HERE/'research_cards.json').read_text())
SOURCES=json.loads((HERE/'source_index.json').read_text())['sources']
BY_ID={s['source_id']:s for s in SOURCES}

def references(refs):
    return '；'.join(f"[{r['source_id']}]（{r['locator']}）" for r in refs)

def pretty_bounds(c):
    b=c['bounds'];return f"{b['south']:.2f}–{b['north']:.2f}°N，{b['west']:.2f}–{b['east']:.2f}°E"

def write_comparison():
    output=[]
    for c in DATA['cards']:
        refs=c['mars_refs']+c['prior_refs']+c['contribution_refs']+[r for e in c['candidates'] for r in e['refs']]
        row=dict(mars_id=c['mars_id'],latitude_deg_n=c['center_latitude_n'],longitude_deg_e_0_360=c['center_longitude_e'],
                 south_deg_n=c['bounds']['south'],north_deg_n=c['bounds']['north'],west_deg_e_0_360=c['bounds']['west'],east_deg_e_0_360=c['bounds']['east'],coordinate_definition=c['coordinate_definition'],
                 **c['metrics'],metric_kind=c['metric_kind'],terrain_support='MOLA16px/degree;about3.7km slope baseline;64 native centres;mapping/interpolated product,not local obstacles',
                 thermal_support='TES20px/degree;mask0 excluded;observation start/end not supplied;2007 is product creation,not observing year;TI unit J m^-2 K^-1 s^-0.5',
                 water_ice_support='SWIM2 2021;0.05degree output grid;multi-instrument/time support;0–1m/1–5m sensitivity zones;unit1 consistency,not ice fraction/probability;shared inputs',
                 dust_support='MY34/MY35;669 reconstructed sols each;3degree selected cell;9.3micrometre absorption total-column optical depth;unit1;not deposition/wind/pressure',
                 MCS_support='MY29–36;5degree nearest grid;10degreeLs bins;03/15LTST model-time-adjusted;QA/count/error absent;contrast not same-sol daily amplitude',
                 research_question=c['question'],earth_candidates_json=json.dumps(c['candidates'],ensure_ascii=False,separators=(',',':')),
                 validation_use=c['validated_use'],prior_work=c['prior'],team_contribution=c['contribution'],limitations=c['limits'],disposition=c['disposition'],
                 source_refs_json=json.dumps(refs,ensure_ascii=False,separators=(',',':')),
                 source_versions_json=json.dumps(dict(main=DATA['main_baseline_sha'],research_prs={str(p['pr']):p['head'] for p in DATA['source_prs']}),separators=(',',':')))
        output.append(row)
    with (HERE/'comparison.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,list(output[0]),lineterminator='\n');w.writeheader();w.writerows(output)

def write_report():
    lines=["# Team zasa：三個火星點的共同研究結論",'',
    '三點目前最有根據的共同主線是：**在不同區域熱性質與冰一致性線索下，檢查哪些觀測足以支持地下冰相關判讀，哪些仍會受材料、覆土、測區拼接與影像尺度混淆。** MS-01提供已知界面的熱響應案例；MS-02釐清覆土、鑽孔與雷達是否構成同址證據鏈；MS-03界定現有影像是否足以支持形貌配對。這些是可追溯的研究問題與資料適用性結果，尚未證明三個新穎、未被研究的火星場址，也沒有完成三個成功的地球環境配對。','',
    '本輪直接整合三份已交付研究，沒有新增場址、外部文獻搜尋、現地量測或物理模型。各地球來源的閱讀深度沿原組明列範圍，摘要不升格為全文證據。四面向的未知會保留；候選降級不等於否定該火星點的研究問題。','',
    '## 固定來源與採用規則','',
    '開始核對後固定以下版本。MS-03已比任務提供的3321765…更新，故採8f6d313…的最新生成元件／149標籤補充。後續若有更新，應另外比較，不靜默更換本交付的來源。','',
    '| 來源 | 本輪實際使用完整 SHA | 基底／用途 |','|---|---|---|',
    f"| 執行開始時 origin/main | `{DATA['main_baseline_sha']}` | 整合分支起點與共同Mars原生格數據 |"]
    for p in DATA['source_prs']:
        lines.append(f"| [PR #{p['pr']}]({p['url']}) | `{p['head']}` | `{p['base']}`；來源分支只讀 |")
    lines += ['',
    '優先順序是「各報告明列有效的最新補充／處置 → 對應新證據與資料狀態 → 保留的歷史段落」。遇到沒有明確取代關係的差異則列入後方判定帳，不自行填補。來源表中採集失敗／成功只指該組、該版本、該檔；不能泛稱所有人都無資料或所有原始資料皆已取得。','',
    'PR #6的基底是交接分支，與另兩份不同。本整合從固定main建立，僅引用其內容，沒有合併／改基底，也沒有把交接分支其他檔案帶進本PR。42個取得的文字來源均重建出與固定Git tree相同的bytes及Git blob SHA；這是來源版本核對，不是42次獨立物理驗證。','',
    '## 三點比較總表','',
    '| 火星點／中心與名義範圍 | 具體問題 | 地球候選及最新處置 | 本隊增加的內容 | 目前研究價值與限制 |','|---|---|---|---|---|']
    for c in DATA['cards']:
        candidate_text='；'.join(f"{e['candidate_id']} {e['name']}：{e['disposition']}" for e in c['candidates'])
        lines.append(f"| {c['mars_id']}：{c['center_latitude_n']:.2f}°N，{c['center_longitude_e']:.2f}°E；{pretty_bounds(c)} | {c['question']} | {candidate_text} | {c['contribution']} | {c['research_value']} {c['limits']} |")
    lines += ['',
    '位置與格界：[MARS_SELECTION]的sites[id].center/bounds；同一MS-03位置也可寫−117.75°E，格界−118至−117.5°E。上述一律轉為0–360°東經；這是表示法一致化，沒有移動取樣格。候選處置與用途依各點下節來源。可機讀總表為[comparison.csv](../../../outputs/integration/science/comparison.csv)，**一列一個火星點，共三列**；八個原候選保留完整ID於earth_candidates_json，不按谷名合併。','',
    '## 四面向：已核實產品摘要與可比性','',
    '下表統一使用共同final_candidates.csv的原生格欄位，不用stack_*近值替代。本輪轉錄並核對既有摘要，未重新擷取全部Mars原始產品。所有三點的MOLA坡度均有64/64有限格，兩SWIM分區各100/100；有限值不代表全部為直接量測或皆無偏。','',
    '| 火星點 | MOLA均坡 °／高差 m | TES夜間TI／有效格 | SWIM 0–1m／1–5m一致性 | MY34／35 CDOD均值 | MY34／35 CDOD p95 |','|---|---:|---:|---:|---:|---:|']
    for c in DATA['cards']:
        m=c['metrics'];lines.append(f"| {c['mars_id']} | {m['mola_slope_deg_mean']:.6f}／{m['mola_relief_m']:.0f} | {m['TES_TI_mean']:.4f}；{m['TES_TI_valid_cells']}/100 | {m['SWIM_0_1m_mean']:.6f}／{m['SWIM_1_5m_mean']:.6f} | {m['dust_my34_mean_cdodtot']:.6f}／{m['dust_my35_mean_cdodtot']:.6f} | {m['dust_my34_p95_cdodtot']:.6f}／{m['dust_my35_p95_cdodtot']:.6f} |")
    lines += ['',
    '數值來源：[MARS_CSV]，candidate_id=MS-01/MS-02/MS-03；欄mola_slope_deg_mean、mola_relief_m、TES_TI_mean/valid_cells、SWIM_0_1m_mean、SWIM_1_5m_mean、dust_my34/my35_mean_cdodtot及p95_cdodtot。完整精度在CSV，顯示值按上表位數四捨五入。定義與原始產品URL見[MARS_METADATA]的units_periods_and_support及sources；單點證據定位另見[MS01_EVIDENCE] EV-001–014、[MS02_EVIDENCE] EV-001–012、[MS03_EVIDENCE] MS03-EV01–07。','',
    '| 面向 | 量、期間、深度／高度與尺度 | 本輪可說與不能外推 |','|---|---|---|',
    '| 地形 | MOLA MEGDR約16px/degree；坡度約3.7km基線，區域格中心高差；MGS mapping，精確源日期依原標籤 | 三點粗尺度地形摘要不同；沒有共同尺度Earth DEM與米級障礙真值，不能判通行／著陸安全。 |',
    '| 熱性質 | TES約20px/degree；TI單位J m⁻² K⁻¹ s⁻½；排mask0後73/93/79格；觀測起訖未列，2007為建檔年 | TI是產品反演的熱性質，非溫度、硬度或冰量；不能與地球點測T、土樣k或κ直接相減。 |',
    '| 水／冰 | SWIM2 2021多儀器跨期綜合；0.05°為輸出格距；0–1m與1–5m是敏感分區，原儀器支撐不同 | 無單位一致性，非機率／冰量／冰層上下界；兩分區共享來源，TES與SWIM也不能算完全獨立互證。 |',
    '| 大氣／沙塵 | MY34/35各669個重建sol；所選3°格的9.3μm吸收整柱光學厚度，無單位 | 僅區域背景；不能換算當地風、壓力、沉積率、覆土厚度或設備失效機率。 |',
    '| 溫度背景 | MCS衍生校時產品MY29–36；5°格、10°Ls分箱、03/15LTST；共同配對分箱MS-01/02/03為69/75/60（各最多288） | 缺QA、樣本數及誤差，不是當地實測、同sol日振幅或全年氣溫；不與Earth MAAT／地下溫度相減。 |','',
    '因此三點是不同觀測背景下的問題案例。MS-01在本三點產品摘要內TI較高；MS-02緯度較低、MY34 p95較高；MS-03均坡較低、近表層一致性較高但深層分區較低。這些比較只限本三個固定格與產品定義，不是全球排名、顯著性檢定、資源量或工程性能結論。[MARS_CSV][MARS_SELECTION]','',
    '## 各點的地球驗證用途與本次貢獻','']
    for c in DATA['cards']:
        lines += [f"### {c['mars_id']}：{c['research_value']}",'',f"**可檢驗問題：** {c['question']} 這是待驗問題，不能預寫為冰已存在或某材料已造成訊號。",'',
        '| 候選ID／位置與範圍 | 最新處置與能驗證什麼 | 限制 |','|---|---|---|']
        for e in c['candidates']:
            lines.append(f"| {e['candidate_id']} {e['name']}；{e['position']}；{e['scope']} | {e['disposition']}。{e['verified_use']} | {e['limit']}。{references(e['refs'])} |")
        lines += ['',f"**先例與實際新增：** {c['prior']} {references(c['prior_refs'])}。{c['contribution']} {references(c['contribution_refs'])}。",'']
        if c['mars_id']=='MS-01':
            lines += ['MS-01補充已用固定印刷日期[2010-11-07 00:00,2010-11-18 00:00)作OLS：截距＋線性趨勢＋24h正弦／餘弦。比值為界面／上層的24h**半振幅**，非max−min；S/M/D各264共同有效列，W Campbell528列，無補值。界面比值依序為**0.45097、0.08774、0.02063、0.02526**。[MS01_AMPLITUDES] station/role=ice與amplitude_to_upper_ratio；[MS01_THERMAL] §1–3。','',
            '觀測支持各剖面日週期分量向下衰減；沒有相同材料、相同forcing的無冰控制，均質無冰導熱也可衰減，故不能驗證冰偵測特異性。M上層是1cm，其餘近表面；站間日照／陰影／風、材料與接觸不同，正規化振幅沒有控制這些因素。D36與W42比值也不是按冰深嚴格排序。留一日範圍只表窗口敏感度，不是信賴區間。這是描述性重算／應用，不是新的熱傳方法或MS-01冰深反演。[MS01_INTERPRETATION] OBS-01–04/07；[MS01_DELTA] U1。','',
            'Beacon在本點只作另一種界面型態與材料約束的可選文獻對照。本輪沒有其原始逐時比較，也沒有證成UV與Beacon的聯合驗證；其特定場址不是本輪UV結論不可替代的必要輸入。[MS01_THERMAL] §6。','']
        elif c['mars_id']=='MS-02':
            lines += ['最新足跡查核把CS-1（78.201°N,15.840°E）、ADE（78.1722°N,16.0613°E）與無座標的WISDOM測線分開。前兩者距離約**5.97km**是MS-02既有球面計算；取芯日期未萃取、ADE鑽孔為2017年3月、雷達為2022年3月，不能因同谷或深度範圍重疊便視為同址實驗。[MS02_REPORT] §8B範圍表；[MS02_FOOTPRINT] 各列；[MS02_VERIFICATION] earth_coordinates_and_conversions.E03_Adventdalen_anchor_separations_km。','',
            'CS-1有岩芯含冰量／冷凍構造及年代證據，能支持該點覆土與同生冰的過程。雷達約1.5m反射是摘要中的作者解釋，未取得同測線獨立冰真值；冰洞的3D真值屬另一地形。介電常數是模型輸入，不能稱本站已量得。本整合保留「CS-1子過程」與「整體候選降級」兩層結論，沒有將UV或MS-01資料用來補成同址雷達驗證。[MS02_CLAIMS] C1/C5–C9；[MS02_REPORT] §8B。','']
        else:
            lines += ['AD1的**185個**已發表向量有效幾何重算，中位等效圓直徑**18.484785m**。以所用CTX示例**6.09m/pixel**換算約**3.04pixels**；這是取樣說明，不是校準檢出閾值。沒有可靠的格內Mars邊界樣本，不能比較兩地多邊形分布，也不能將AD1值或0填成Mars真值。[MS03_GEOMETRY] n、metrics.equivalent_circle_diameter_m.median；[MS03_OBSERVABILITY] Equivalent-circle diameter/Available sampling。','',
            '固定任務索引的205451物理列中，205302個唯一產品、149個額外重複列已對應；615筆原警示為負經度格式檢核問題，均有有效緯度且可排除本格，舊「615筆位置未知」已被取代。已核的固定索引格內bbox交集為0，仍不能推出未發布／未列入觀測都無覆蓋，更不能推出多邊形不存在。[MS03_INDEX]；[MS03_REPORT] 最新正式交接。','',
            '最新又取得149份現行產品標籤；78組與整秒floor/ceil相容，71組不相容，29組兩索引時間差超過1秒。這僅排除「同一時刻只作整秒取整」是全部差異唯一原因的受限假說，2026執行版、SQL／設定與生成根因仍未知。公開文件版本不等於實際執行版，本整合不把這項資料追溯成果寫成新地貌發現。[MS03_DUPLICATES]；[MS03_VERSIONS]；[MS03_REPORT] 最前段生成元件追查。','',
            'UV的作者處理長版匯出已取得，仍缺未處理logger、原校準碼與時鐘記錄。2010 HOBO同列20/42cm描述只表示作者合併匯出上的同列資料，不證明不同logger真正同步；不能把其差值當傳熱真值。長版Campbell在2012年時間欄位差變化也未被自動校正。[MS03_UV_QA] records；[MS03_CLOCK]；[MS03_REPORT] 時標交接。','']
    lines += ['## 三點共同結論與達成程度','',
    '**共同結論：地球已知場址讓本隊把「可能相似」改寫成有範圍、有真值條件及可辨識性界線的問題；目前最強的新增成果是描述性重算、證據足跡與來源適用性查核。** 這些工作可以排除不受支持的推論，尚不能從Mars粗尺度產品唯一識別材料／冰，或證明多邊形成因。','',
    '三點共用University Valley、SWIM與TES，不構成三套獨立真值。UV驗證的是已知界面下的響應／方法限制；Adventdalen與AD1查核則顯示同谷證據與可辨識影像的重要性。覆土／材料、冰界面、表面邊界與幾何取樣仍須分開。地球極區氣候、大氣、雪／水汽補給與Mars條件也未等效化，不能移植地球冰深、k／κ、昇華率或沉積率。[MS01_THERMAL] §4–6；[MS02_CLAIMS] C7–C9；[MS03_OBSERVABILITY] Cause/ground ice。','',
    '| 原目標／問題 | 本輪可確認的完成內容 | 仍不能確認 |','|---|---|---|',
    '| 三個明確Mars研究範圍 | 三點座標、格界與同定義產品摘要已固定 | 非實地孔位、著陸橢圓、局部材料或冰真值。[MARS_SELECTION][MARS_METADATA] |',
    '| 每點找至少兩個有據可查的Earth候選 | 已提出並逐項處置2／4／2個候選，保留完整ID | 不代表每點都有兩個成立的具體配對；MS-02 E03、MS-03 E02降級。[MS01_CANDIDATES][MS02_CANDIDATES][MS03_CANDIDATES] |',
    '| 地形、熱、水冰、大氣沙塵比較 | 有共同產品背景、地球過程證據與逐面向未知 | 缺共同尺度DEM、同定義沙塵及本地真值，無整體相似度排名。[MARS_METADATA][MS01_REPORT][MS02_REPORT][MS03_REPORT] |',
    '| 同場址同用途先例與本隊差異 | 已找到UV及AD1直接／重疊先例；本次新增重算／稽核與適用性判讀 | 未完成全球新穎性排除；未查到指定點研究不等於從未研究。[MS01_PRIOR][MS02_PRIOR][MS03_PRIOR] |',
    '| 三個研究不足／被忽略的火星區域 | 可交付三個界線清楚、值得進一步驗證的研究問題 | 尚未證明三點均研究不足或從未被研究；共同基準亦標not_globally_novelty_cleared。[MARS_CSV][MARS_SELECTION] |',
    '| 地球驗證能否證明Mars地下冰／工程可行 | 已辨清哪些熱／雷達／形貌推論不成立或證據不足 | 無本地冰深、含量、連續性、採冰能耗、承載或設備性能結果；不作資源／著陸結論。[MS01_THERMAL][MS02_CLAIMS][MS03_OBSERVABILITY] |','',
    '## 報告差異與待統籌判定帳','',
    '以下同時區分「明確被新補充取代的歷史文字」「量或範圍不同」與「真正仍未知」。採用規則不代表修改原研究者成果，亦不把所有差異視作數字錯誤。','',
    '| ID／類型與差異 | 本整合採用方式 | 尚待判定或原稿同步事項／來源 |','|---|---|---|']
    for i in DATA['issues']:
        lines.append(f"| {i['id']}：{i['classification']}。{i['topic']} | {i['decision']} | {i['unresolved']} {references(i['sources'])} |")
    lines += ['',
    '## 交付與驗證範圍','',
    '本文件、[comparison.csv](../../../outputs/integration/science/comparison.csv)與[manifest.json](../../../outputs/integration/science/manifest.json)構成本輪交付。機讀研究卡、完整來源hash／章節索引與必要製作／驗證程式置於相同science目錄。CSV的source_refs_json與候選內refs保留具體列／欄／JSON key／頁段；source_index.json將其解析為完整commit permalink。資料類型以既有實測／作者處理觀測、產品推估、團隊重算與研究假設區分，不將來源指向替代成新測量。','',
    '驗證僅涵蓋42來源的bytes／Git blob／SHA-256、三點座標格界與數字轉錄、三列CSV、八候選與降級、引用定位、既有衰減比／AD1取樣示例的一致性及本次輸出hash。沒有重新執行三組全部原始資料流程、原文全文重查、感測器校準或實地真值驗證。原組PASS按其原範圍保留，不升格成獨立物理證明。結果見verification.json；有本次固定來源快取時可額外核對原表。','',
    '```sh','python3 outputs/integration/science/build.py','python3 outputs/integration/science/verify.py --source-cache /path/to/source-cache','python3 outputs/integration/science/build.py --manifest-only','python3 outputs/integration/science/verify.py --check-manifest','```','',
    '本輪從執行開始時固定origin/main建立integration/research-synthesis，只提交docs/integration/science/與outputs/integration/science/。來源分支保持只讀，未合併main、不改他人成果、不要求隊友展開下一輪。原始實測／產品及文獻仍歸原來源，沙塵衍生數值的原授權條件沿源保留（見MS-01來源說明）；本輪不替專案重新授權。','',
    '## 固定來源連結','',
    '以下均為本輪固定commit；上文方括號連到確切檔案，具體定位文字保留於各處與機讀研究卡。外部DOI及作者實讀頁段仍以各組evidence/prior_work為準。','']
    used={r['source_id'] for c in DATA['cards'] for r in c['mars_refs']+c['prior_refs']+c['contribution_refs']+[r for e in c['candidates'] for r in e['refs']]}
    used.update(r['source_id'] for i in DATA['issues'] for r in i['sources'])
    used.update(['MS03_UV_QA','MS03_VERSIONS','MS01_REPORT','MS02_VERIFICATION'])
    # Bare reference labels also get human-readable entries and definitions.
    for sid in sorted(used):
        s=BY_ID[sid];lines.append(f"- **{sid}**：[固定檔案]({s['url']})；PR {s['pr_number'] if s['pr_number'] is not None else 'main'}，`{s['path']}`。")
    lines.append('')
    for s in SOURCES:lines.append(f"[{s['source_id']}]: {s['url']}")
    report='\n'.join(lines)+'\n'
    # Adjacent shortcuts otherwise become a full-reference link to the next ID.
    report=re.sub(r'\]\[(?=[A-Z0-9_]+\])',']；[',report)
    REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(report,encoding='utf-8')

def write_manifest():
    paths=[REPORT]+[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json']
    files=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(paths)]
    result=dict(schema='ZASA-FINAL-SCIENCE-SYNTHESIS-v1',team='zasa',date_taipei=DATA['date_taipei'],main_baseline_sha=DATA['main_baseline_sha'],branch=DATA['branch'],source_prs=DATA['source_prs'],
                scope='Read completed fixed research only; no new site, literature search or physical validation; no source branch mutation or main merge',
                source_index='outputs/integration/science/source_index.json',source_files=42,source_byte_exact_matches=42,comparison_grain='one Mars target per row;3 rows;8 scoped candidate IDs in nested JSON',
                data_kind_policy='Measurements and author-processed exports remain Earth observations;Mars products remain inferences;prior team reprocessing is attributed;this integration copies/compares sources and labels hypotheses.',
                units={'mola_slope_deg_mean':'degree at~3.7km baseline','mola_relief_m':'m,nominal native centres','TES_TI_mean':'J m^-2 K^-1 s^-0.5','SWIM_0_1m_mean':'dimensionless consistency,not fraction/probability','SWIM_1_5m_mean':'dimensionless consistency,not fraction/probability','dust_*_cdodtot':'dimensionless9.3micrometre absorption column optical depth','MCS_paired_contrast_median_K':'K,MY/Ls paired bins,not daily amplitude'},
                latest_dispositions={c['mars_id']:{e['candidate_id']:e['disposition'] for e in c['candidates']} for c in DATA['cards']},issues=DATA['issues'],
                unmet_goals=['Global novelty/understudied status not established for all3 targets','Not3 confirmed environmental matches or2successful matches per target','No local Mars ice/material truth or unique thermal attribution','No same-forcing/material ice-free control or co-located Adventdalen radar truth','MS03 local morphology unknown;catalogue completeness/rootcause unknown','Per-export clock and UVS/Dposition conflicts unresolved'],
                files=files,hash_scope='All own deliverables including verification.json;only this manifest and __pycache__ excluded.',
                preservation='Remote branch created from pinned main via GitHub API;shared dirty checkout not switched/reset;only science paths published.',
                stop='Deliver this synthesis and PR;do not expand research or wait for other integration streams.')
    (HERE/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'report':str(REPORT),'comparison_rows':len(DATA['cards']),'hashed_files':len(files)},ensure_ascii=False))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--manifest-only',action='store_true');a=p.parse_args()
    if not a.manifest_only:write_comparison();write_report()
    write_manifest()
if __name__=='__main__':main()
