# Team zasa：三個火星點的共同研究結論

三點目前最有根據的共同主線是：**在不同區域熱性質與冰一致性線索下，檢查哪些觀測足以支持地下冰相關判讀，哪些仍會受材料、覆土、測區拼接與影像尺度混淆。** MS-01提供已知界面的熱響應案例；MS-02釐清覆土、鑽孔與雷達是否構成同址證據鏈；MS-03界定現有影像是否足以支持形貌配對。這些是可追溯的研究問題與資料適用性結果，尚未證明三個新穎、未被研究的火星場址，也沒有完成三個成功的地球環境配對。

本輪直接整合三份已交付研究，沒有新增場址、外部文獻搜尋、現地量測或物理模型。各地球來源的閱讀深度沿原組明列範圍，摘要不升格為全文證據。四面向的未知會保留；候選降級不等於否定該火星點的研究問題。

## 固定來源與採用規則

開始核對後固定以下版本。MS-03已比任務提供的3321765…更新，故採8f6d313…的最新生成元件／149標籤補充。後續若有更新，應另外比較，不靜默更換本交付的來源。

| 來源 | 本輪實際使用完整 SHA | 基底／用途 |
|---|---|---|
| 執行開始時 origin/main | `3cc8488577535e2fa4d146021fde51f8ff6cc667` | 整合分支起點與共同Mars原生格數據 |
| [PR #6](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/6) | `38b8fa0dea527b1cc47aeb02dc260e039da37122` | `handoff/verified-data-20261114`；來源分支只讀 |
| [PR #7](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/7) | `8f6d3134bc5bfef6e83a4caddb1d602872d40708` | `main`；來源分支只讀 |
| [PR #8](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/8) | `b4b6929e890018668ef4faa9a74128a4ce5aa8df` | `main`；來源分支只讀 |

優先順序是「各報告明列有效的最新補充／處置 → 對應新證據與資料狀態 → 保留的歷史段落」。遇到沒有明確取代關係的差異則列入後方判定帳，不自行填補。來源表中採集失敗／成功只指該組、該版本、該檔；不能泛稱所有人都無資料或所有原始資料皆已取得。

PR #6的基底是交接分支，與另兩份不同。本整合從固定main建立，僅引用其內容，沒有合併／改基底，也沒有把交接分支其他檔案帶進本PR。42個取得的文字來源均重建出與固定Git tree相同的bytes及Git blob SHA；這是來源版本核對，不是42次獨立物理驗證。

## 三點比較總表

| 火星點／中心與名義範圍 | 具體問題 | 地球候選及最新處置 | 本隊增加的內容 | 目前研究價值與限制 |
|---|---|---|---|---|
| MS-01：56.75°N，72.75°E；56.50–57.00°N，72.50–73.00°E | 在本三點中較高的TES熱慣量與正SWIM一致性並存時，哪些熱響應仍可由材料／覆土解釋，哪些需要獨立冰界面證據？ | MS-01-E01 University Valley W/S/M/D：保留，限定熱傳與可辨識性；MS-01-E02 central Beacon Valley：保留可選文獻補充；原始序列待證 | 新增本次固定短窗四站描述性重算、同logger衰減及留一日敏感度、來源行欄交付、S/D座標與時間欄位問題，以及MS-01可支持／不可支持的判讀。 | 以已知界面剖面檢查熱傳模型與訊號多解，防止把產品共現誤作冰的因果證明。 沒有同材料同forcing無冰控制、獨立UV k/ρCp或MS-01冰真值；站間材料／日照／陰影／風與探針條件不受控；不反演MS-01冰深／含冰量。 |
| MS-02：52.75°N，168.25°E；52.50–53.00°N，168.00–168.50°E | 在較低緯度、正冰一致性及區域沙塵背景下，如何避免把覆土、季節與不同測區的雷達／冰證據拼成同址探冰結論？ | MS-02-E01 University Valley：保留，限定熱響應參照；MS-02-E02 middle Beacon Valley：待補證據；MS-02-E03 Adventdalen：降為一般方法參照；CS-1子過程仍可引用；MS-02-E04 Haughton River Valley：待補證據 | 新增岩芯／鑽孔／雷達的證據足跡查核、CS-1與ADE距離、引用層級與數字適用期修正；撤回跨場址拼接及由CDOD換覆土沉積率的主張。 | 將風成覆土、季節熱響應與冰線索分開，查明哪些地球證據具有同址、同年、相同深度的驗證鏈。 雷達測線位置與多邊形溝槽的獨立冰真值未得；摘要模型介電常數未證實為實測；MS-02材料、覆土、冰深與正式地質單元未知。 |
| MS-03：57.75°N，242.25°E；57.50–58.00°N，242.00–242.50°E | 低TES熱慣量與較強近表層SWIM一致性並存時，現有影像能否辨識足以比較的多邊形邊界？哪些材料／界面解釋仍需保留？ | MS-03-E01 University Valley W：保留為已知方法／歷史資料參照；MS-03-E02 Adventdalen AD1 / Act-IWS：降為一般方法參照，退出具體MS-03配對 | 新增固定MS-03範圍的影像覆蓋／品質／尺度適用性查核、AD1既有向量重算與刊載數字重現、索引異常與149標籤診斷、UV作者匯出QA與分檔時標限制。 | 先檢查取樣尺度與可觀測性是否允許形貌類比，避免從目錄零命中或模糊影像推成形貌不存在／有冰。 MS-03格內多邊形、成因與地下冰仍未知；無可用Mars多邊形樣本作分布比較；索引執行版／SQL與重複根因未知；不同地球logger同步仍未核實。 |

位置與格界：[MARS_SELECTION]的sites[id].center/bounds；同一MS-03位置也可寫−117.75°E，格界−118至−117.5°E。上述一律轉為0–360°東經；這是表示法一致化，沒有移動取樣格。候選處置與用途依各點下節來源。可機讀總表為[comparison.csv](../../../outputs/integration/science/comparison.csv)，**一列一個火星點，共三列**；八個原候選保留完整ID於earth_candidates_json，不按谷名合併。

## 四面向：已核實產品摘要與可比性

下表統一使用共同final_candidates.csv的原生格欄位，不用stack_*近值替代。本輪轉錄並核對既有摘要，未重新擷取全部Mars原始產品。所有三點的MOLA坡度均有64/64有限格，兩SWIM分區各100/100；有限值不代表全部為直接量測或皆無偏。

| 火星點 | MOLA均坡 °／高差 m | TES夜間TI／有效格 | SWIM 0–1m／1–5m一致性 | MY34／35 CDOD均值 | MY34／35 CDOD p95 |
|---|---:|---:|---:|---:|---:|
| MS-01 | 0.287207／76 | 325.1557；73/100 | 0.639225／0.647482 | 0.119264／0.107535 | 0.222456／0.180147 |
| MS-02 | 0.301845／117 | 217.2690；93/100 | 0.692987／0.622499 | 0.125384／0.110066 | 0.240015／0.173120 |
| MS-03 | 0.162753／76 | 152.8077；79/100 | 0.910904／0.509972 | 0.098215／0.088660 | 0.173362／0.140962 |

數值來源：[MARS_CSV]，candidate_id=MS-01/MS-02/MS-03；欄mola_slope_deg_mean、mola_relief_m、TES_TI_mean/valid_cells、SWIM_0_1m_mean、SWIM_1_5m_mean、dust_my34/my35_mean_cdodtot及p95_cdodtot。完整精度在CSV，顯示值按上表位數四捨五入。定義與原始產品URL見[MARS_METADATA]的units_periods_and_support及sources；單點證據定位另見[MS01_EVIDENCE] EV-001–014、[MS02_EVIDENCE] EV-001–012、[MS03_EVIDENCE] MS03-EV01–07。

| 面向 | 量、期間、深度／高度與尺度 | 本輪可說與不能外推 |
|---|---|---|
| 地形 | MOLA MEGDR約16px/degree；坡度約3.7km基線，區域格中心高差；MGS mapping，精確源日期依原標籤 | 三點粗尺度地形摘要不同；沒有共同尺度Earth DEM與米級障礙真值，不能判通行／著陸安全。 |
| 熱性質 | TES約20px/degree；TI單位J m⁻² K⁻¹ s⁻½；排mask0後73/93/79格；觀測起訖未列，2007為建檔年 | TI是產品反演的熱性質，非溫度、硬度或冰量；不能與地球點測T、土樣k或κ直接相減。 |
| 水／冰 | SWIM2 2021多儀器跨期綜合；0.05°為輸出格距；0–1m與1–5m是敏感分區，原儀器支撐不同 | 無單位一致性，非機率／冰量／冰層上下界；兩分區共享來源，TES與SWIM也不能算完全獨立互證。 |
| 大氣／沙塵 | MY34/35各669個重建sol；所選3°格的9.3μm吸收整柱光學厚度，無單位 | 僅區域背景；不能換算當地風、壓力、沉積率、覆土厚度或設備失效機率。 |
| 溫度背景 | MCS衍生校時產品MY29–36；5°格、10°Ls分箱、03/15LTST；共同配對分箱MS-01/02/03為69/75/60（各最多288） | 缺QA、樣本數及誤差，不是當地實測、同sol日振幅或全年氣溫；不與Earth MAAT／地下溫度相減。 |

因此三點是不同觀測背景下的問題案例。MS-01在本三點產品摘要內TI較高；MS-02緯度較低、MY34 p95較高；MS-03均坡較低、近表層一致性較高但深層分區較低。這些比較只限本三個固定格與產品定義，不是全球排名、顯著性檢定、資源量或工程性能結論。[MARS_CSV]；[MARS_SELECTION]

## 各點的地球驗證用途與本次貢獻

### MS-01：以已知界面剖面檢查熱傳模型與訊號多解，防止把產品共現誤作冰的因果證明。

**可檢驗問題：** 在本三點中較高的TES熱慣量與正SWIM一致性並存時，哪些熱響應仍可由材料／覆土解釋，哪些需要獨立冰界面證據？ 這是待驗問題，不能預寫為冰已存在或某材料已造成訊號。

| 候選ID／位置與範圍 | 最新處置與能驗證什麼 | 限制 |
|---|---|---|
| MS-01-E01 University Valley W/S/M/D；W錨點−77.86215°,160.71010°E；S/D座標版本衝突；四個離散站及名義探針剖面，站間不補為連續測區 | 保留，限定熱傳與可辨識性。已知8/22/36/42cm界面下的熱波響應及資料品質檢查 | S/D定位未解；不同站不是控制冰深實驗；不能證明MS-01有冰。[MS01_THERMAL]（§2,§3,§6）；[MS01_STATIONS]（S8/M22/D36/W42_Campbell） |
| MS-01-E02 central Beacon Valley；約−77.8166667°,160.65000°E；文獻僅到角分；單一多邊形剖面與鄰孔；完整邊界／逐孔GPS未知 | 保留可選文獻補充；原始序列待證。乾覆土下塊狀冰、土樣密度／比熱及界面模型假設的補充對照 | 本輪無新逐時序列比較，非UV結論不可替代的必要條件。[MS01_THERMAL]（§6）；[MS01_EVIDENCE]（EV-021–029） |

**先例與實際新增：** Marinova2022已研究同谷能量收支、振幅／相位與熱參數／冰深敏感度；Liu2018已有Beacon剖面與模型。 [MS01_PRIOR]（PW-U1;PW-B1）；[MS01_DELTA]（source_id=U1;B1）。新增本次固定短窗四站描述性重算、同logger衰減及留一日敏感度、來源行欄交付、S/D座標與時間欄位問題，以及MS-01可支持／不可支持的判讀。 [MS01_THERMAL]（§1–6）；[MS01_AMPLITUDES]（station=S8/M22/D36/W42_Campbell;role=ice）；[MS01_INTERPRETATION]（OBS-01–08）。

MS-01補充已用固定印刷日期[2010-11-07 00:00,2010-11-18 00:00)作OLS：截距＋線性趨勢＋24h正弦／餘弦。比值為界面／上層的24h**半振幅**，非max−min；S/M/D各264共同有效列，W Campbell528列，無補值。界面比值依序為**0.45097、0.08774、0.02063、0.02526**。[MS01_AMPLITUDES] station/role=ice與amplitude_to_upper_ratio；[MS01_THERMAL] §1–3。

觀測支持各剖面日週期分量向下衰減；沒有相同材料、相同forcing的無冰控制，均質無冰導熱也可衰減，故不能驗證冰偵測特異性。M上層是1cm，其餘近表面；站間日照／陰影／風、材料與接觸不同，正規化振幅沒有控制這些因素。D36與W42比值也不是按冰深嚴格排序。留一日範圍只表窗口敏感度，不是信賴區間。這是描述性重算／應用，不是新的熱傳方法或MS-01冰深反演。[MS01_INTERPRETATION] OBS-01–04/07；[MS01_DELTA] U1。

Beacon在本點只作另一種界面型態與材料約束的可選文獻對照。本輪沒有其原始逐時比較，也沒有證成UV與Beacon的聯合驗證；其特定場址不是本輪UV結論不可替代的必要輸入。[MS01_THERMAL] §6。

### MS-02：將風成覆土、季節熱響應與冰線索分開，查明哪些地球證據具有同址、同年、相同深度的驗證鏈。

**可檢驗問題：** 在較低緯度、正冰一致性及區域沙塵背景下，如何避免把覆土、季節與不同測區的雷達／冰證據拼成同址探冰結論？ 這是待驗問題，不能預寫為冰已存在或某材料已造成訊號。

| 候選ID／位置與範圍 | 最新處置與能驗證什麼 | 限制 |
|---|---|---|
| MS-02-E01 University Valley；谷錨點約−77.8667°,160.7500°E，不是W探針精孔；谷底站群與原文熱剖面；未取得測區polygon | 保留，限定熱響應參照。覆土、季節邊界與已知冰膠結界面的耦合 | 同名谷資料不等於MS-02真值或沉積史；年摘要不能直接比MCS。[MS02_CANDIDATES]（candidate_id=MS-02-E01）；[MS02_REPORT]（§8B「與University Valley各自解決的問題」） |
| MS-02-E02 middle Beacon Valley；本組未萃取可核對座標；本組摘要級來源，尚未建立與MS-01中央谷剖面的一對一對照 | 待補證據。只保留埋冰過程的候選線索 | 足跡對應未完成前，不能套用MS-01所讀剖面升級本候選。[MS02_CANDIDATES]（candidate_id=MS-02-E02） |
| MS-02-E03 Adventdalen；CS-1:78.201°N,15.840°E；ADE:78.1722°N,16.0613°E；雷達未知；不同岩芯／鑽孔／雷達範圍；不是單一共址測區 | 降為一般方法參照；CS-1子過程仍可引用。僅CS-1支援風成覆土累積與同生冰的地球過程；雷達只作方法參考 | CS-1與ADE約5.97km；無證據把三組結果組成同址雷達偵冰。[MS02_REPORT]（§8B）；[MS02_CLAIMS]（C7/C9）；[MS02_FOOTPRINT]（各足跡列） |
| MS-02-E04 Haughton River Valley；約75.37°N,−89.53°E（西經89.53°）河谷錨點；九個局部LiDAR格／河谷測區，不是撞擊中心 | 待補證據。可供圖案地形／融化深度與測區代表性的方法比較 | 缺本站含冰量與地溫序列；不能把其他北極場址GPR移入。[MS02_CANDIDATES]（candidate_id=MS-02-E04）；[MS02_PRIOR]（PW-07/PW-14/PW-15） |

**先例與實際新增：** Marinova2022已有UV能量／熱過程；Hauber2011已有Adventdalen與Mars形貌類比；Rasmussen2023已有CS-1沉積／冰史；Brighi的WISDOM用途已有先例，但本組主要讀摘要。 [MS02_PRIOR]（PW-02/PW-04/PW-05/PW-06/PW-18–20）；[MS02_REPORT]（§7,§8B）。新增岩芯／鑽孔／雷達的證據足跡查核、CS-1與ADE距離、引用層級與數字適用期修正；撤回跨場址拼接及由CDOD換覆土沉積率的主張。 [MS02_REPORT]（§8B）；[MS02_CLAIMS]（C1–C9）；[MS02_FOOTPRINT]（FP-01/FP-03及雷達列）。

最新足跡查核把CS-1（78.201°N,15.840°E）、ADE（78.1722°N,16.0613°E）與無座標的WISDOM測線分開。前兩者距離約**5.97km**是MS-02既有球面計算；取芯日期未萃取、ADE鑽孔為2017年3月、雷達為2022年3月，不能因同谷或深度範圍重疊便視為同址實驗。[MS02_REPORT] §8B範圍表；[MS02_FOOTPRINT] 各列；[MS02_VERIFICATION] earth_coordinates_and_conversions.E03_Adventdalen_anchor_separations_km。

CS-1有岩芯含冰量／冷凍構造及年代證據，能支持該點覆土與同生冰的過程。雷達約1.5m反射是摘要中的作者解釋，未取得同測線獨立冰真值；冰洞的3D真值屬另一地形。介電常數是模型輸入，不能稱本站已量得。本整合保留「CS-1子過程」與「整體候選降級」兩層結論，沒有將UV或MS-01資料用來補成同址雷達驗證。[MS02_CLAIMS] C1/C5–C9；[MS02_REPORT] §8B。

### MS-03：先檢查取樣尺度與可觀測性是否允許形貌類比，避免從目錄零命中或模糊影像推成形貌不存在／有冰。

**可檢驗問題：** 低TES熱慣量與較強近表層SWIM一致性並存時，現有影像能否辨識足以比較的多邊形邊界？哪些材料／界面解釋仍需保留？ 這是待驗問題，不能預寫為冰已存在或某材料已造成訊號。

| 候選ID／位置與範圍 | 最新處置與能驗證什麼 | 限制 |
|---|---|---|
| MS-03-E01 University Valley W；W錨點−77.86215°,160.71010°E；W歷史剖面；作者處理後長版Campbell/HOBO分開使用 | 保留為已知方法／歷史資料參照。來源QA、分檔時間欄位限制與已知界面資料需求 | 作者處理匯出已得；未處理logger／原校準碼／時鐘紀錄仍缺；禁止跨儀器配時或冰反演。[MS03_REPORT]（2026-11-15時標交接及2010描述）；[MS03_UV_QA]（records）；[MS03_CLOCK]（regime_offsets_hours;correction_applied） |
| MS-03-E02 Adventdalen AD1 / Act-IWS；事件起點78.184°N,15.913°E；metadata78.184–78.188°N,15.913–15.933°E；185個已發表向量；事件範圍不是感測器位置或連續冰真值 | 降為一般方法參照，退出具體MS-03配對。既有幾何重現與影像取樣尺度檢查 | 未獲可可靠追描的格內Mars邊界，形貌與地下冰保持未知。[MS03_CANDIDATES]（candidate_id=MS-03-E02）；[MS03_GEOMETRY]（n;metrics.equivalent_circle_diameter_m.median）；[MS03_OBSERVABILITY]（Equivalent-circle diameter;Available sampling） |

**先例與實際新增：** Marinova2022已有UV熱傳用途；Ulrich2011已用AD1與Mars作定量地貌類比，185個向量及刊載統計屬既有資料。 [MS03_PRIOR]（MS03-PW01/MS03-PW04/MS03-PW08）；[MS03_REPORT]（形貌補充：原刊Tables2–4核對與降級）。新增固定MS-03範圍的影像覆蓋／品質／尺度適用性查核、AD1既有向量重算與刊載數字重現、索引異常與149標籤診斷、UV作者匯出QA與分檔時標限制。 [MS03_REPORT]（2026-11-15最新補充及形貌／時標交接）；[MS03_OBSERVABILITY]（各metric列）；[MS03_INDEX]（decision）；[MS03_DUPLICATES]（149標籤診斷）。

AD1的**185個**已發表向量有效幾何重算，中位等效圓直徑**18.484785m**。以所用CTX示例**6.09m/pixel**換算約**3.04pixels**；這是取樣說明，不是校準檢出閾值。沒有可靠的格內Mars邊界樣本，不能比較兩地多邊形分布，也不能將AD1值或0填成Mars真值。[MS03_GEOMETRY] n、metrics.equivalent_circle_diameter_m.median；[MS03_OBSERVABILITY] Equivalent-circle diameter/Available sampling。

固定任務索引的205451物理列中，205302個唯一產品、149個額外重複列已對應；615筆原警示為負經度格式檢核問題，均有有效緯度且可排除本格，舊「615筆位置未知」已被取代。已核的固定索引格內bbox交集為0，仍不能推出未發布／未列入觀測都無覆蓋，更不能推出多邊形不存在。[MS03_INDEX]；[MS03_REPORT] 最新正式交接。

最新又取得149份現行產品標籤；78組與整秒floor/ceil相容，71組不相容，29組兩索引時間差超過1秒。這僅排除「同一時刻只作整秒取整」是全部差異唯一原因的受限假說，2026執行版、SQL／設定與生成根因仍未知。公開文件版本不等於實際執行版，本整合不把這項資料追溯成果寫成新地貌發現。[MS03_DUPLICATES]；[MS03_VERSIONS]；[MS03_REPORT] 最前段生成元件追查。

UV的作者處理長版匯出已取得，仍缺未處理logger、原校準碼與時鐘記錄。2010 HOBO同列20/42cm描述只表示作者合併匯出上的同列資料，不證明不同logger真正同步；不能把其差值當傳熱真值。長版Campbell在2012年時間欄位差變化也未被自動校正。[MS03_UV_QA] records；[MS03_CLOCK]；[MS03_REPORT] 時標交接。

## 三點共同結論與達成程度

**共同結論：地球已知場址讓本隊把「可能相似」改寫成有範圍、有真值條件及可辨識性界線的問題；目前最強的新增成果是描述性重算、證據足跡與來源適用性查核。** 這些工作可以排除不受支持的推論，尚不能從Mars粗尺度產品唯一識別材料／冰，或證明多邊形成因。

三點共用University Valley、SWIM與TES，不構成三套獨立真值。UV驗證的是已知界面下的響應／方法限制；Adventdalen與AD1查核則顯示同谷證據與可辨識影像的重要性。覆土／材料、冰界面、表面邊界與幾何取樣仍須分開。地球極區氣候、大氣、雪／水汽補給與Mars條件也未等效化，不能移植地球冰深、k／κ、昇華率或沉積率。[MS01_THERMAL] §4–6；[MS02_CLAIMS] C7–C9；[MS03_OBSERVABILITY] Cause/ground ice。

| 原目標／問題 | 本輪可確認的完成內容 | 仍不能確認 |
|---|---|---|
| 三個明確Mars研究範圍 | 三點座標、格界與同定義產品摘要已固定 | 非實地孔位、著陸橢圓、局部材料或冰真值。[MARS_SELECTION]；[MARS_METADATA] |
| 每點找至少兩個有據可查的Earth候選 | 已提出並逐項處置2／4／2個候選，保留完整ID | 不代表每點都有兩個成立的具體配對；MS-02 E03、MS-03 E02降級。[MS01_CANDIDATES]；[MS02_CANDIDATES]；[MS03_CANDIDATES] |
| 地形、熱、水冰、大氣沙塵比較 | 有共同產品背景、地球過程證據與逐面向未知 | 缺共同尺度DEM、同定義沙塵及本地真值，無整體相似度排名。[MARS_METADATA]；[MS01_REPORT]；[MS02_REPORT]；[MS03_REPORT] |
| 同場址同用途先例與本隊差異 | 已找到UV及AD1直接／重疊先例；本次新增重算／稽核與適用性判讀 | 未完成全球新穎性排除；未查到指定點研究不等於從未研究。[MS01_PRIOR]；[MS02_PRIOR]；[MS03_PRIOR] |
| 三個研究不足／被忽略的火星區域 | 可交付三個界線清楚、值得進一步驗證的研究問題 | 尚未證明三點均研究不足或從未被研究；共同基準亦標not_globally_novelty_cleared。[MARS_CSV]；[MARS_SELECTION] |
| 地球驗證能否證明Mars地下冰／工程可行 | 已辨清哪些熱／雷達／形貌推論不成立或證據不足 | 無本地冰深、含量、連續性、採冰能耗、承載或設備性能結果；不作資源／著陸結論。[MS01_THERMAL]；[MS02_CLAIMS]；[MS03_OBSERVABILITY] |

## 報告差異與待統籌判定帳

以下同時區分「明確被新補充取代的歷史文字」「量或範圍不同」與「真正仍未知」。採用規則不代表修改原研究者成果，亦不把所有差異視作數字錯誤。

| ID／類型與差異 | 本整合採用方式 | 尚待判定或原稿同步事項／來源 |
|---|---|---|
| I01：歷史狀態與新版補充不一致。MS-01候選主表仍稱S/M/D待下載 | 共同結論採已核hash及264有效列的新補充；原候選表保留歷史，不回寫他人成果。 | 來源表是否另行整理由統籌決定；不影響固定短窗結果。 [MS01_CANDIDATES]（E01.available_data/next_step）；[MS01_THERMAL]（§1–3） |
| I02：同一報告用途敘述寬於最新處置。MS-02前段及候選用途仍提覆土＋雷達，與§8B降級不同 | 採§8B限定；不引用H1/H2編號錯位或同址雷達已成立的措辭。 | 原稿措辭修訂歸原作者／統籌；本輪不補雷達真值。 [MS02_REPORT]（§5/§6對照§8B）；[MS02_CANDIDATES]（E01.disposition_reason;E03.testable_physical_processes）；[MS02_CLAIMS]（C7/C9） |
| I03：歷史enum與取得狀態不同。MS-03 E01字串仍帶pending_raw_series，但data_status說處理後匯出已取得 | 明寫作者處理匯出已得，未處理logger／原碼與時鐘記錄未得；不籠統寫原時序全未取。 | enum是否更新由統籌決定；不能把已得匯出當未處理真值。 [MS03_CANDIDATES]（E01.disposition/data_status）；[MS03_REPORT]（2026-11-15時序取得與時標交接） |
| I04：同名候選、不同用途與閱讀範圍。Beacon在MS-01保留補充、MS-02待證；UV／Adventdalen也不是同名即可同孔 | 保留完整候選ID及各自處置；不按谷名合併、套座標或自動升級。 | 跨來源精確範圍對應未完成，留待統籌判定是否可共用。 [MS01_THERMAL]（§6）；[MS02_CANDIDATES]（E01–E04）；[MS03_CANDIDATES]（E01/E02） |
| I05：匯出檔／時期不同，來源關係未知。W短版與長版時間欄位差不同 | 按檔／期間保留限制；不平均、不校時、不跨logger join，也不因2012長檔問題否定2010短窗全部數字。 | 真正對時與生成鏈未知，需原碼與logger紀錄；本輪不追查。 [MS01_THERMAL]（§2時標；short09_10）；[MS03_CLOCK]（long09_13 offsets−1/−5h;2012boundary）；[MS03_CLOCK_SEARCH]（root_cause=unknown） |
| I06：未經本輪核定的定義與數值。MS-02 EV-018約2560h同時水活度與溫度雙閾值 | 列待核定，不納入共同關鍵結論；另外兩組未交付同定義雙閾值核算，不能由其他溫度統計補證。 | 需核對原文圖說、量的定義、年／深度與實測／模型別；本輪未重查原文。 [MS02_EVIDENCE]（EV-018;p161 Fig6）；[MS02_REPORT]（§8 E01） |
| I07：定義差異，非已證實數字錯誤。原生格摘要與stack摘要不可混欄比較 | 三點總表統一原生格欄；保留stack是另一定義，不以同名近值相互替代。 | 不重做原始網格；共同數字的來源一致性不等於獨立真值。 [MARS_CSV]（native SWIM/TES/MOLA columns vs stack_*）；[MS02_VERIFICATION]（checks;expected_scale_differences_not_errors） |
| I08：測站座標版本衝突仍未解。UV的2009部署與2022論文把S/D具名座標對調；MS-02另用谷錨點 | S/D按匯出與serial辨識；谷錨點與W孔位分開；不做未核對的坡向／陰影歸因。 | 哪版位置正確未知，本輪不代原作者修正。 [MS01_STATIONS]（S8/D36 paper vs deployment2009）；[MS02_CANDIDATES]（E01 coordinate/boundary_basis） |
| I09：舊警示已釐清，根因仍未知。MS-03舊615筆位置未知與新版緯度排除不同 | 採新版：615筆有有效緯度且可排除本格；149額外列數量已對應，生成根因仍未知。 | 不能延伸成完整觀測無覆蓋、已修正官方表、已知SQL根因或形貌不存在。 [MS03_INDEX]（legacy_flagged_rows;flagged_latitude_intersections;all_raw_rows_roi_bbox_intersections;decision）；[MS03_REPORT]（最新生成元件追查；正式交接）；[MS03_DUPLICATES]（149/78/71/29及causal_interpretation） |

## 交付與驗證範圍

本文件、[comparison.csv](../../../outputs/integration/science/comparison.csv)與[manifest.json](../../../outputs/integration/science/manifest.json)構成本輪交付。機讀研究卡、完整來源hash／章節索引與必要製作／驗證程式置於相同science目錄。CSV的source_refs_json與候選內refs保留具體列／欄／JSON key／頁段；source_index.json將其解析為完整commit permalink。資料類型以既有實測／作者處理觀測、產品推估、團隊重算與研究假設區分，不將來源指向替代成新測量。

驗證僅涵蓋42來源的bytes／Git blob／SHA-256、三點座標格界與數字轉錄、三列CSV、八候選與降級、引用定位、既有衰減比／AD1取樣示例的一致性及本次輸出hash。沒有重新執行三組全部原始資料流程、原文全文重查、感測器校準或實地真值驗證。原組PASS按其原範圍保留，不升格成獨立物理證明。結果見verification.json；有本次固定來源快取時可額外核對原表。

```sh
python3 outputs/integration/science/build.py
python3 outputs/integration/science/verify.py --source-cache /path/to/source-cache
python3 outputs/integration/science/build.py --manifest-only
python3 outputs/integration/science/verify.py --check-manifest
```

本輪從執行開始時固定origin/main建立integration/research-synthesis，只提交docs/integration/science/與outputs/integration/science/。來源分支保持只讀，未合併main、不改他人成果、不要求隊友展開下一輪。原始實測／產品及文獻仍歸原來源，沙塵衍生數值的原授權條件沿源保留（見MS-01來源說明）；本輪不替專案重新授權。

## 固定來源連結

以下均為本輪固定commit；上文方括號連到確切檔案，具體定位文字保留於各處與機讀研究卡。外部DOI及作者實讀頁段仍以各組evidence/prior_work為準。

- **MARS_CSV**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3cc8488577535e2fa4d146021fde51f8ff6cc667/outputs/research/mars_reselection_20261114/final_candidates.csv)；PR main，`outputs/research/mars_reselection_20261114/final_candidates.csv`。
- **MARS_METADATA**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3cc8488577535e2fa4d146021fde51f8ff6cc667/outputs/research/mars_reselection_20261114/candidate_native_evidence.json)；PR main，`outputs/research/mars_reselection_20261114/candidate_native_evidence.json`。
- **MARS_SELECTION**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3cc8488577535e2fa4d146021fde51f8ff6cc667/outputs/research/mars_reselection_20261114/selected_targets.json)；PR main，`outputs/research/mars_reselection_20261114/selected_targets.json`。
- **MS01_AMPLITUDES**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/amplitudes.csv)；PR 8，`outputs/research/MS-01/thermal_followup/amplitudes.csv`。
- **MS01_CANDIDATES**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/candidates.csv)；PR 8，`outputs/research/MS-01/candidates.csv`。
- **MS01_DELTA**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/prior_work_delta.csv)；PR 8，`outputs/research/MS-01/thermal_followup/prior_work_delta.csv`。
- **MS01_EVIDENCE**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/evidence.csv)；PR 8，`outputs/research/MS-01/evidence.csv`。
- **MS01_INTERPRETATION**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/interpretation_table.csv)；PR 8，`outputs/research/MS-01/thermal_followup/interpretation_table.csv`。
- **MS01_PRIOR**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/prior_work.csv)；PR 8，`outputs/research/MS-01/prior_work.csv`。
- **MS01_REPORT**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/docs/research/MS-01/report.md)；PR 8，`docs/research/MS-01/report.md`。
- **MS01_STATIONS**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/station_metadata.csv)；PR 8，`outputs/research/MS-01/thermal_followup/station_metadata.csv`。
- **MS01_THERMAL**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/docs/research/MS-01/thermal_followup.md)；PR 8，`docs/research/MS-01/thermal_followup.md`。
- **MS02_CANDIDATES**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/candidates.csv)；PR 6，`outputs/research/MS-02/candidates.csv`。
- **MS02_CLAIMS**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/claims.csv)；PR 6，`outputs/research/MS-02/claims.csv`。
- **MS02_EVIDENCE**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/evidence.csv)；PR 6，`outputs/research/MS-02/evidence.csv`。
- **MS02_FOOTPRINT**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/footprint.csv)；PR 6，`outputs/research/MS-02/footprint.csv`。
- **MS02_PRIOR**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/prior_work.csv)；PR 6，`outputs/research/MS-02/prior_work.csv`。
- **MS02_REPORT**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/docs/research/MS-02/report.md)；PR 6，`docs/research/MS-02/report.md`。
- **MS02_VERIFICATION**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/verification.json)；PR 6，`outputs/research/MS-02/verification.json`。
- **MS03_CANDIDATES**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/candidates.csv)；PR 7，`outputs/research/MS-03/candidates.csv`。
- **MS03_CLOCK**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/uv_w/campbell_clock_audit.json)；PR 7，`outputs/research/MS-03/uv_w/campbell_clock_audit.json`。
- **MS03_CLOCK_SEARCH**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/uv_w/clock_search_followup.json)；PR 7，`outputs/research/MS-03/uv_w/clock_search_followup.json`。
- **MS03_DUPLICATES**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/evidence_followup/generator_followup/duplicate_label_time_summary.json)；PR 7，`outputs/research/MS-03/morphology/evidence_followup/generator_followup/duplicate_label_time_summary.json`。
- **MS03_GEOMETRY**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/AD1_geometry_summary.json)；PR 7，`outputs/research/MS-03/morphology/AD1_geometry_summary.json`。
- **MS03_INDEX**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/evidence_followup/index_anomalies/resolution_summary.json)；PR 7，`outputs/research/MS-03/morphology/evidence_followup/index_anomalies/resolution_summary.json`。
- **MS03_OBSERVABILITY**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/observability_comparison.csv)；PR 7，`outputs/research/MS-03/morphology/observability_comparison.csv`。
- **MS03_PRIOR**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/prior_work.csv)；PR 7，`outputs/research/MS-03/prior_work.csv`。
- **MS03_REPORT**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/docs/research/MS-03/report.md)；PR 7，`docs/research/MS-03/report.md`。
- **MS03_UV_QA**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/uv_w/qa.json)；PR 7，`outputs/research/MS-03/uv_w/qa.json`。
- **MS03_VERSIONS**：[固定檔案](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/evidence_followup/generator_followup/public_version_trace.json)；PR 7，`outputs/research/MS-03/morphology/evidence_followup/generator_followup/public_version_trace.json`。

[MS02_REPORT]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/docs/research/MS-02/report.md
[MS02_CANDIDATES]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/candidates.csv
[MS02_EVIDENCE]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/evidence.csv
[MS02_PRIOR]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/prior_work.csv
[SOURCE_05]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/manifest.json
[MS02_VERIFICATION]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/verification.json
[MS02_CLAIMS]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/claims.csv
[MS02_FOOTPRINT]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/footprint.csv
[SOURCE_09]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/search_log.csv
[MS03_REPORT]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/docs/research/MS-03/report.md
[MS03_CANDIDATES]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/candidates.csv
[MS03_EVIDENCE]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/evidence.csv
[MS03_PRIOR]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/prior_work.csv
[SOURCE_14]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/manifest.json
[SOURCE_15]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/validation.json
[SOURCE_16]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/mars_reference.json
[SOURCE_17]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/README.md
[MS03_OBSERVABILITY]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/observability_comparison.csv
[MS03_GEOMETRY]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/AD1_geometry_summary.json
[MS03_INDEX]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/evidence_followup/index_anomalies/resolution_summary.json
[MS03_HANDOFF]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/evidence_followup/index_handoff/handoff_status.json
[MS03_DUPLICATES]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/evidence_followup/generator_followup/duplicate_label_time_summary.json
[MS03_VERSIONS]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/morphology/evidence_followup/generator_followup/public_version_trace.json
[MS03_CLOCK]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/uv_w/campbell_clock_audit.json
[MS03_CLOCK_SEARCH]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/uv_w/clock_search_followup.json
[MS03_UV_QA]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8f6d3134bc5bfef6e83a4caddb1d602872d40708/outputs/research/MS-03/uv_w/qa.json
[MS01_REPORT]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/docs/research/MS-01/report.md
[MS01_THERMAL]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/docs/research/MS-01/thermal_followup.md
[MS01_CANDIDATES]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/candidates.csv
[MS01_EVIDENCE]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/evidence.csv
[MS01_PRIOR]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/prior_work.csv
[SOURCE_32]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/manifest.json
[SOURCE_33]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/sources.json
[MS01_AMPLITUDES]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/amplitudes.csv
[MS01_INTERPRETATION]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/interpretation_table.csv
[MS01_DELTA]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/prior_work_delta.csv
[MS01_STATIONS]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/station_metadata.csv
[SOURCE_38]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/source_manifest.json
[SOURCE_39]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/verification.json
[MARS_CSV]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3cc8488577535e2fa4d146021fde51f8ff6cc667/outputs/research/mars_reselection_20261114/final_candidates.csv
[MARS_SELECTION]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3cc8488577535e2fa4d146021fde51f8ff6cc667/outputs/research/mars_reselection_20261114/selected_targets.json
[MARS_METADATA]: https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3cc8488577535e2fa4d146021fde51f8ff6cc667/outputs/research/mars_reselection_20261114/candidate_native_evidence.json
