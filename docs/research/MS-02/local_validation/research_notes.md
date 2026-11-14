- **2026-11-14 官方資料補充入口**：[新增條列筆記](official_followup_notes.md)。本頁下方為前輪快照；本次新增 9 景 THEMIS 共址亮溫、CRISM MRDR4 與幾何欄位、數值雷達雜波及地表對齊、五塊 CTX 地理定位樣區、UNISCALM 968 筆測值與 2023 岩芯原始資料。更新後的八項狀態、資料與品質限制以補充筆記和 `outputs/research/MS-02/local_validation/official_followup/` 為準；仍未確認當地冰存在、深度或含量。

# MS-02 local_validation — 證據、方法與待決事項

- 用途：人類撰寫正式報告的資料筆記；不是報告正文、摘要或結論。
- 固定範圍：52.50–53.00°N、168.00–168.50°E；中心52.75°N、168.25°E；行星中心緯度、東經為正。未更動範圍。
- 本輪日期：2026-11-15 Asia/Taipei（下載紀錄使用 UTC，部分為11月14日）。

## 基準與閱讀範圍

| 項目 | 核對結果 |
|---|---|
| 起始遠端完整 SHA | `c309675fbe713a8548a75abf29b54e64217768f9`；已不同於使用者已知的 `38b8fa0dea527b1cc47aeb02dc260e039da37122` |
| 工作中新增遠端提交 | `cdcf3baaa0342a852cc4f6060f3d8fb048dcce53`：統計彙整與 builder；已 fast-forward 保留 |
| 原分支／PR | `research/ms-02-earth-analogs`／[#6](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/6) |
| 第二次保留遠端提交 | `ef5eb162b1df0919b8d6dd780782896188607b2c`：瀏覽器ODE盤點；已fast-forward，保留其清單與LV-S56–60；本輪實際檔案驗證另列 |
| 不變的 base | `handoff/verified-data-20261114`；`f7076c9fdc77e00244ed5d6863aad2bf78cfa28f` |
| 原資料已讀 | report §8B、claims、footprint、candidates、evidence、prior_work；既有 local_validation 與統計表 |
| 驗收／整合已讀 | [PR9](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/9) `c206553fc681328d214cbbcd508d3c5b1391e200`；[PR10](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/10) `0260c511d9fce6be12d3460a69e474f333160cbf`；其引用的舊 PR6 SHA 不代表本輪產品狀態 |
| Excel | 完整巡覽 repo 彙整活頁簿32張表、逐列計數／MS-02 字串盤點，見 `workbook_inventory.csv`；MEDA/Jezero、舊 I-01/I-02、Elephant Head 等不得移用為本格量測 |
| 無法識別的使用者來源 | 本對話沒有附百度帳號、下載連結或額外 Excel 附件；沒有宣稱已取得這些未提供來源。以 repo 可辨識活頁簿為界 |
| 禁止沿用 | 降級前 Adventdalen「覆土＋雷達」鏈、H2/H3 舊敘述；詳 `claim_corrections.csv` |

## 1. 位置與既有研究

| 判定 | 證據／方法 | 限制 |
|---|---|---|
| 正式圖幅：MC-7 Cebrenia | USGS I-1140 原圖30–65°N、180–240°W，即120–180°E | 圖幅名不等於地貌單元名 |
| 全格在 mAl（Middle Amazonian lowland unit） | SIM3292 原始 shapefile；OBJECTID1252；Mars2000球半徑3396190m；相交面積比例1.0 | 1:20,000,000全球圖；不能推出局部礦物、覆土厚度或現在含冰量 |
| 不直接稱 Arcadia Planitia | Gazetteer Feature348 的 MDIM2.1 多邊形不與固定範圍相交；MDIM2.0 舊矩形則相交 | 名稱邊界為近似；不能只用 bounding box。原「距西緣84km」停止引用 |
| MDIM2.1 圖形間距約7.69km | 火星球面局部等積投影、ROI與多邊形距離；`geography_check.json` | 近似圖形的幾何距離，不是精確地貌分界距離 |
| ROI面積約531.665km² | 同一投影計算；`analyze_products.py` | 直線多邊形邊界近似；不用地球半徑 |

- 來源：[SIM3292](https://doi.org/10.3133/sim3292)、[I-1140](https://pubs.usgs.gov/imap/1140/plate-1.pdf)、[Gazetteer](https://planetarynames.wr.usgs.gov/Feature/348)；下載hash與實讀欄位見 manifest、search_log。
- 搜尋鍵：完整座標、Cebrenia／Arcadia／Phlegra、mAl／Middle Amazonian lowland unit、五個 CTX ID、SHARAD 00464501、Piqueux／Tanaka／Skinner 引用鏈；歷史搜尋55筆保留並標記為前輪。

| 類別 | 本輪處置 | 不能推論 |
|---|---|---|
| 格內同用途 | Piqueux2019全球熱反演產品的本格像元已取得；用途為淺冰表深度估計 | 不是針對本格的獨立地面驗證研究 |
| 格內不同用途 | SIM3292地質分類、SWIM篩選一致性、已定位軌道產品 | 覆蓋不等於已完成相同研究問題 |
| 附近／大區域 | 原 Bramson、Viola、Ramsdale、Séjourné、MONS、暴露冰點表的範圍限制保留；新增 Skinner2012 mAl引用鏈 | 不移植180°E以東研究的深度／含量至168°E；Skinner只讀摘要與地圖引用，不能宣稱其局部樣區含本格 |
| 位置不明 | Costard摘要，以及僅由檢索結果不能定位的項目 | 沒找到不能證明從未研究 |

- `local_prior_work.csv` 的 `review_state` 區分本輪重讀、前輪繼承；未把繼承的全文閱讀冒充本輪重讀。
- 研究缺口的具體定義：缺「格內同一位置的覆土材料／厚度、冰真值與季節熱觀測或雷達」配套驗證；不再寫成「完全沒有產品／從未研究」。

## 2. 已取得的火星資料與品質

| 資料 | 本次取得與計算 | 時期／解析度／敏感深度 | 品質與未知 |
|---|---|---|---|
| Piqueux2019 | 全部5個檔案；row74 col336（0起算）：模型深度0.4499824941m、乾層TI188.2415009 J m⁻² K⁻¹ s⁻½ | 2019-11-27 archive；0.5°像元恰等於ROI；季節熱敏感約6cm–1m | 非缺值−32768；真實深度未驗證；沒有本格殘差或CI；不可把論文最佳情況約20%直接當本格誤差棒；檔案2ppd與論文3ppd原因未解 |
| CTX | 5個EDR目錄足跡＋5張browse；名義聯集覆蓋100%ROI | 2012-05-12至2024-12-31；原生約6.08–6.15m/px；browse降採樣不同；只看表面 | 已看browse；未做EDR校正、正射或有效像元面積；低對比影像不能證明沒有多邊形、冰崖或新撞擊坑 |
| SHARAD | 3個原始power陣列、標籤、定位表、表面clutter模擬browse；格內64+65+65=194欄；均finite且非零 | 2007-07-24、2010-10-20、2010-11-05；posting460m；sample0.0375µs；20MHz、10MHz頻寬 | 194欄不是194獨立解析單元；第1800列是areoid不是地表；完整delay圖有表面回波；未認定地下反射體、未反演介電常數 |
| CRISM | 177目錄記錄中59為IF科學產品（49S、10L）；取得全部IF標籤；其中1個L立方體＋配套DDR | MSP0001565D，2010-01-08；55bands×900lines×64samples；survey約200m；光學表面 | 格內912像元中心／50160光譜值；2100值為65535；數值可用95.8134%不等於科學有效率；含負I/F；波長／壞band／大氣／光度校正不足，不能判礦物或冰 |
| HiRISE | ODE RDR4、RDRV11成功查詢為0；EDR空間查詢不支援 | 查詢日期與類型限定 | 錯誤不是零；不是任務全期無資料或無冰證明 |
| MONS | 原資料的粗尺度背景＋Pathare2018文章PDF；本格WEH數值仍未取得 | 約550km FWHM；近表層氫、分層模型，非0.5°獨立觀測 | 氫不等於獨立確認H₂O冰；不得以SWIM neutron consistency替代WEH；SWIM頁本輪亦有timeout紀錄 |
| TES／SWIM／CDOD／MCS | repo交接數據保留；來源依賴與原生格限制見CSV | TES93/100有效；SWIM兩層是產品深度標籤；CDOD3°；MCS5° | 沒有把這些背景資料重新包裝成新量測 |

- 熱資料來源：[資料DOI](https://doi.org/10.22002/D1.1316)、[方法§2–3](https://doi.org/10.1029/2019GL083947)；地層冰為模型假設，岩石／塊石可造成混淆；不能辨別孔隙冰與塊狀冰。
- SHARAD解析度計算：c/(2B)≈15m自由空間；除以√3.15≈8.45m冰中（介電常數為假設）。0.0375µs取樣間隔對應5.62m自由空間，不是系統解析度；不可能用此產品直接驗證0.45m冰表。
- `fig_sharad_observed_clutter.png`：完整3600列與對應格內欄位；觀測power顯示用dB、模擬為browse灰階；幅度不可直接相減或定量比值。未做盲測／自動偵測率試驗。
- `fig_verified_footprints.png`：原地質單元、Gazetteer近似界線、CTX足跡、SHARAD測線。聯集面積是名義支援，不是無雲／無塵／有效像元覆蓋。
- `crism_roi.npz` 保留未作光譜解釋的樣本與numeric mask；DDR的TI來自其他產品，不能當CRISM獨立熱測量。

### 冰存在、深度、含量分開判定

| 問題 | 直接證據 | 間接線索 | 模型／假設 | 判定與未知 |
|---|---|---|---|---|
| 存在 | 本格未取得獨立冰真值；軌道power／I/F是直接觀測，但不是直接冰確認 | 本格季節熱模型、SWIM一致性；mAl區域成因描述 | 熱模型下層假設冰；mAl成因為解釋 | 間接支持增加；實際存在仍證據不足；不判無冰 |
| 深度 | 無本格鑽探／暴露界面／經驗證反射體 | 熱季節差異 | 兩層模型給0.4499824941m | 可引用「產品模型值約0.45m」；真實深度與本格CI未知 |
| 含量 | 無本格含冰量實測／獨立介電反演 | SWIM、氫背景不能直接給本格冰量 | 熱模型下層物性；雷達介電常數若使用須另假設 | 缺值保留；不填百分比、不填機率 |
| 覆土／材料 | 地質單元已定位；尚無局部粒徑／礦物／累積率真值 | TI、CTX表面外觀 | 乾層熱模型，不唯一 | 0.45m只是條件性模型乾層厚度；CDOD不能換算堆積率 |

### 來源依賴

- SWIM綜合 N/T/G/RS/RD：氫、熱、影像地貌、雷達表面／地下輸入；不是五次獨立確認。
- Piqueux MCS/THEMIS 與SWIM熱資料屬共享資料家族；未取得逐像元輸入權重，不能聲稱完全相同或完全獨立。
- MOLA既是地形背景，又參與SHARAD定位／clutter、CRISM DDR與熱模型邊界；交叉一致不能重複計票。
- TES本格TI217.27與Piqueux乾層TI188.24估計對象、時段、模型不同；不直接求差判成冰。
- 地質圖的「dust+ice」解釋與區域文獻引用鏈不算本格新觀測。

## 3. 地球配對的驗證程度

| 案例 | 本輪獨立核對 | 保留／提升的精確用途 | 不可跨越的限制 |
|---|---|---|---|
| University Valley W站 | Marinova2022完整PDF、TableII、p162 Fig6與附錄；42cm界面；約15cm是0°C活動層 | 保留已知界面＋季節熱響應 | 不能把15cm當全部乾覆土；部分導熱係數依賴外來密度／比熱；無雷達用途 |
| CS-1 | Rasmussen2023 PDF p5 §3.2：2019年9月取芯；2022年8月露頭20mNE另列 | 風成覆土累積＋同生冰子過程 | 0.35cm/yr為峰值，不是長期平均或火星堆積率；質量冰含量不是vol% |
| ADE | 78.1722N16.0613E；2017年3月資料維持原範圍 | 一般凍土結構參照 | 與CS-1約5.97km，不接同址鏈 |
| WISDOM Adventdalen | Brighi摘要仍無可定位測線與同測線獨立冰真值 | 一般雷達方法參照 | Longyearbreen冰洞3D真值不能移接；模型ε不當實測ε |
| Wendt2026／2023岩芯 | 版本DOI10.5281/zenodo.11187360原Excel；12站UTM33N轉WGS84；各層數值QA | 各岩芯位置的獨立地面資料，非WISDOM驗證 | E6 5–10cm VIC108.9293、PIC101.2191vol%超物理區間，保留旗標；未知雷達位置不能拼接 |
| Beacon：Liu2018具名測站 | §2–3.3、Table1、Fig2；77°49′S160°39′E；約30cm乾層與已知冰界面 | 限縮提升為熱模型材料參數與界面子案例 | 深部井在相鄰多邊形；導熱係數為半經驗估計；未下載原時間序列；不提升整個谷名 |
| Haughton：Thomson2012具名測線 | §2.3、3.1–3.3；75°22′06″N89°31′33″W；3m線、450MHz、CMP焦點1.5m處約1m岩芯 | 限縮提升為同測線GPR＋獨立岩芯介電方法子案例，補足WISDOM缺的真值設計 | 雷達穿透濕活動層受阻後挖除約0.9m；不能說驗證未擾動覆土下冰，也不能驗證軌道SHARAD；Table1類型彙整不當本點含冰量 |

- [University Valley](https://doi.org/10.1017/S0954102022000025)、[Rasmussen全文](https://backend.orbit.dtu.dk/ws/files/329047704/1_s2.0_S0277379123001853_main.pdf)、[Wendt原資料](https://doi.org/10.5281/zenodo.11187360)、[Beacon](https://doi.org/10.1029/2017JF004535)、[Haughton](https://doi.org/10.1029/2012JE004053)。
- 沒有新增谷名候選、沒有全球相似度排名；Beacon/Haughton僅以自行核對的特定研究補明確缺口。

## 4. 驗收／整合的主張修正與禁用

- 權威修正清單：`claim_corrections.csv`；只提出對原報告、PR9、PR10的修正要求，沒有改寫正式稿或他人成果。
- C19/C20/C21/C24：CS-1/ADE/WISDOM不可同址串接；約1.5m雷達反射不代表已獨立驗證冰；ε輸入與量測分離；H2/H3舊用途禁用。
- C22：峰值沉積率限制保留；C23：60–100cm與UNISCALM≥1m為不同時期／來源，仍未調和。CS-1取芯日期另由未知更新為2019年9月。
- I06／EV-018：原文p162為2560h/年溫度門檻累積；溫度來自記錄，water activity由冰／水飽和蒸氣壓比計算；不是兩個量均直接量測，也不是能量模型模擬時數。不得移植為MS-02可居住性；Fig6年化，不自行指定某完整曆年。
- I08：University Valley S/D座標跨文獻交換問題維持未解；不用名稱自動配對感測器。
- MCS日夜順序修正：day246.3053K、night171.2721K；66.8305K是配對差的中位數，不是兩個中位數相減；來源量與QA未重處理，不當地表／地下溫度。
- 舊SWIM「若只有兩值則24.5/100格」推論撤回：平均／極值無法證明二值分布，更不是實測格數。

## 5. 尚缺與待人類決定

| 缺口 | 已做的工作／影響 | 最小下一步 |
|---|---|---|
| 本格冰真值 | 已有條件性熱深度，但無獨立確認 | 暴露冰重複影像、可定位獨立反射體或原位驗證 |
| SHARAD冰層解釋 | 有原始power與clutter；未做可信反射挑選 | 表面對齊、噪音／側瓣門檻、地形clutter驗證、跨軌一致性；不以0.45m作已知真值 |
| 光譜表面材料 | 有1個L科學樣本，尚無完整光譜處理 | 波長、壞band／像元、大氣／光度校正，與同位置影像比較 |
| 實際覆土累積率 | CDOD無法回答；無變化測量 | 定量重複影像／原位沉積觀測 |
| MONS格內WEH | 文章取得，數值格未取得 | 下載原WEH與誤差／PSF；仍只作粗尺度氫背景 |
| 土壤粒徑／礦物／冰含量 | 全球地質分類已取得但不能代替 | 可辨識材料的當地觀測；保留缺值 |
| 地球原始驗證資料 | UV/Beacon/Haughton文獻用途已限縮；Wendt有原表 | 雷達原始線與岩芯物性剖面共同座標，未擾動覆土對照 |
| 人類論點選擇 | 證據支持寫「模型估約0.45m」，不支持寫「已證實0.45m有冰」 | 人類決定是否採用此條件性估計及兩個限縮地球子案例 |

## 6. 重現與檔案管理

- 主資料：`mars_ice_evidence.csv`、`local_prior_work.csv`、`analog_validation.csv`、`search_log.csv`、`manifest.json`。
- 新分析：`analyze_products.py`、`analyze_radar.py`、`analyze_crism.py`、`analyze_workbooks.py`；需要 numpy/shapely/pyproj/pyshp/matplotlib/Pillow/openpyxl。
- `acquisition_log.jsonl`逐次保存URL、UTC、HTTP／錯誤、bytes、SHA256；HTTP200的ODE錯誤body仍標錯誤，不當成功產品。
- 原始大檔與完整文章在本機 `sources/`；`.gitignore`只排除本輪大陣列／GIS／文章全文與中間抽取，沒有刪除。Git交付小型目錄、標籤、ROI陣列、衍生表與圖；manifest明列local-only與已納入Git的差別。
- 熱圖原檔Notes標示all rights reserved，Git交付本格／小鄰域衍生值、來源與hash，沒有重新散布全球原圖。
- 舊 `build_tables.py`／`derive_metrics.py`／原verifiers是前輪快照；保留歷史，但不得重跑覆蓋新表。本輪以 `verify_revision.py`為檢查入口；`build_statistics.py`依新表更新計數。
- 下載未取得、檢索無命中、產品未分類、無法有效判讀四種狀態分開保存；均不當無冰或無既有研究的證明。

## 遠端並行盤點差異（保留、不混算）

- `ode_coverage_query.csv`與LV-S56–60來自ef5eb16的瀏覽器清單；沒有冒充本輪重跑瀏覽器。
- 該清單CRISM383筆含TRDR/MRDR4/DDR/VRDR等不同產品，不是383次獨立光譜觀測；其TRDR180與本輪REST177筆差異尚未調和，不能相加。
- 該清單SHSIMU=0已被本輪取得的3個SHSIMU產品與對應browse反證；原清單保留並新增修正欄，不再引用「無clutter產品」。
- 新清單另提示THEMIS等產品；本輪未逐一取得，並未將未下載誤記為無觀測。

- 最後保留遠端 `79a36344fc4f815f4fcca6d0ddb446efe6ba4080` 的 `ctx_product_metadata.csv`（D01瀏覽器metadata）；本輪另有全部5景REST足跡與browse。合併保留雙方提交，沒有強推；原「足跡未核實」僅適用該遠端先前閱讀狀態。

