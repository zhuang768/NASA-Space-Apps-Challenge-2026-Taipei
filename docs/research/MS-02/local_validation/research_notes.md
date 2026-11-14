# MS-02 local_validation：研究筆記（資料、判定、未知；非報告正文）

範圍：MS-02 52.75°N、168.25°E；固定範圍 52.50–53.00°N、168.00–168.50°E（行星中心座標、東經為正）。研究日 2026-11-15（Asia/Taipei）。
本檔只列條列與表格；報告正文、摘要、結論由人類撰寫。

## 0. 基準與讀取

- PR #6 head：`38b8fa0dea527b1cc47aeb02dc260e039da37122`（本輪開始時以 `git ls-remote` 與 `gh api` 核對，未變）；base 維持 `handoff/verified-data-20261114`（`f7076c9fdc77e00244ed5d6863aad2bf78cfa28f`）。
- 已讀：PR #6 報告 §8B、`claims.csv`、`footprint.csv`、`candidates.csv`、`evidence.csv`、`prior_work.csv`；PR #9（驗收，head `c206553…`）與 PR #10（整合，head `0260c51…`，`synthesis.md`）。
- 不採用：降級前的「覆土＋雷達」用途文字（PR #6 報告前段與 H2/H3 殘留）；以 §8B 與 PR #9 主張台帳 C19–C24、X04 為準。
- 環境限制（影響後述每一項「未取得」）：shell 對 PDS／ODE／USGS／HiRISE 索引等資料主機一律 CONNECT 403；`oderest` 經 WebFetch 被 robots 拒絕；HAL 被 Anubis 擋（未繞過）。見 `search_log.csv` LV-S14、S15、S18、S21、S52。
- 產出數字的程式：`derive_metrics.py`（衍生數值＋圖）、`build_tables.py`（五個表）、`verify_local_validation.py`（核對）。

## 1. 問題一：研究缺口

### 1.1 區域與地質單元（自行核對）

| 項目 | 結果 | 來源／依據 | 狀態 |
|---|---|---|---|
| 圖幅 | 在 MC-7 Cebrenia 四邊形內（30–65°N、120–180°E）；距其東界 180°E 沿緯線約 421.6 km | Wikipedia Cebrenia quadrangle（次級；LV-S05） | 取得（次級來源） |
| Arcadia Planitia | planitia 範圍約 33.9–64.2°N、165.9–210.4°E（中心 47.2°N、184.3°E）；本格在其範圍框內，距西緣沿緯線約 84.3 km | Wikipedia Arcadia Planitia（次級；LV-S06）；Gazetteer 該 planitia 頁未讀到（LV-S11、S22） | 次級來源；不可直接稱「在 Arcadia」 |
| 易混名稱 | Gazetteer 的 `Arcadia`（Feature 346）是 albedo feature，44.66°N、260°E；`Cebrenia`（Feature 1095）albedo feature 49.67°N、150°E，皆為單點，不是 planitia 範圍 | LV-S03、S04 | 取得 |
| 地質單元 | **未確定**。Tanaka 2014（SIM 3292）說明書讀到 pp.13–14，列出低地單元 lHl、AHtu、mAl、Av，但沒有給任何座標的單元；GIS 未取得 | LV-S12、S13、S40 | 未取得；不得命名單元 |
| 與已做格圖帶的位置 | Arcadia 格圖帶（Ramsdale 2019）約 186–194°E，距本格中心約 628.7 km；Utopia 格圖帶（Séjourné 2019）約 87–94°E，約 2,534.5 km | `derived_metrics.json`；圖 `fig_local_prior_work_extents.png` | 本次計算（帶寬為近似） |

### 1.2 既有研究分類（完整表：`local_prior_work.csv`）

| 類別 | 項目 | 備註 |
|---|---|---|
| 格內同用途 | 無「針對本格」研究在已執行搜尋中出現；**產品級**例外：Piqueux 2019 全球冰表深度圖（2 ppd，本格約為 1 個像元） | 像元值未取得（LP-08、ME-12） |
| 格內不同用途 | SWIM2 一致性（本格有值；區域篩選，不是局部驗證）；Tanaka 2014 地質圖（覆蓋本格；單元值未取得） | LP-05、LP-09 |
| 附近／大區域 | Bramson 2015（180–225°E、38–50°N；距 463.6 km）；Viola 2015（180–240°E；421.1 km）；Ramsdale 2019（628.7 km）；Pathare 2017 WEH（Arcadia 框 184–228°E；563.9 km；MONS 約 550 km FWHM）；Séjourné 2019（2,534.5 km）；Morgan 2025 Table 2 最近點 Site 46（46.62°N、171.88°E）389.0 km | LP-01–04、06、07、10 |
| 位置不明 | Costard 等 EPSC 2013（只讀到摘錄，無座標） | LP-13 |
| 繼承自 hand-off 稽核（本輪未重讀） | Dundas 2014/2021 點、EZMars、SWIM4MIM、MCOA、Phlegra 提案 | LP-11、LP-12 |

- 搜尋用的鍵：座標字串、區域名（Arcadia／Cebrenia／Utopia／Phlegra）、地質單元名、HiRISE 影像 ID 格式、引用鏈（Bramson→Viola→Ramsdale→Morgan）。完整字串與日期見 `search_log.csv`（LV-S01–S55）。
- 搜尋無命中**不等於**從未研究：WebSearch 不是目錄；ODE、PDS 影像／SHARAD 索引、HiRISE 累積索引（168,675,271 B）都無法在本環境查詢。

### 1.3 具體缺少的研究／觀測（判定）

| 缺口 | 判定 | 需要的資料或觀測 |
|---|---|---|
| 本格或其 0.5° 像元的冰表深度數值 | 缺（產品存在、值未取得） | Piqueux 2019 `d_m.ascii` 與 `TI_SI.ascii` 在該像元的值與擬合殘差（像元大小 2 ppd 與 3 ppd 兩頁說法不一致，未解決） |
| SHARAD 是否有軌跡穿過固定範圍、是否有反射體 | 缺 | PDS／ODE 的 SHARAD 軌跡與雷達圖；若有，需 ε 假設與近表面雜波評估（Bramson：側瓣可遮蔽 20–30 m 內反射；解析度約 8.4 m（冰中）） |
| 格內 HiRISE／CTX 影像清單與地貌 | 缺 | ODE 或 HiRISE 累積索引查詢固定範圍；目前無影像 ID |
| 光譜（CRISM／OMEGA）冰訊號或含水訊號 | 缺（未取得任何產品；僅做標題級搜尋） | CRISM 覆蓋清單與判讀 |
| 暴露冰（新撞擊坑、冰崖） | 未見（只涵蓋已繼承的點表） | 對固定範圍的新撞擊坑／重複影像檢索 |
| MONS WEH 在本格的數值 | 缺（區域圖存在，足跡約 550 km） | Pathare／Wilson 圖在該座標的值（此值也只是約 550 km 範圍平均） |
| 本格正式地質單元 | 缺 | SIM 3292 向量與固定範圍相交 |
| 與 Arcadia 區域研究（180°E 以東）的銜接 | 缺 | 沒有任何已讀研究把 168°E 帶納入；Ramsdale 與 Bramson／Viola 的西界皆在 180–186°E |

## 2. 問題二：MS-02 當地材料、覆土與冰證據（完整：`mars_ice_evidence.csv`）

### 2.1 實際取得與計算（本格；來源 hand-off main 的 `final_candidates.csv`，共享資料）

| 項目 | 值 | 單位 | 類型 | 限制 |
|---|---|---|---|---|
| MOLA 高程 平均（最小／最大） | −3898.719（−3956／−3839） | m 相對 areoid | 產品推估 | 約 3.7 km 基線；64 個原生格 |
| MOLA 坡度 平均／最大；起伏 | 0.3018／0.9253；117 | °；m | 產品推估 | 基線尺度，不是局部坡度 |
| TES 熱慣量 平均（中位；範圍；有效） | 217.269（213；177–276；93/100） | J m⁻² K⁻¹ s⁻⁰·⁵ | 產品推估 | 表層熱性質；7 格 mask=0 補值格已排除（不是 0）；不是溫度、硬度、冰量或深度 |
| SWIM2 0–1 m 平均（中位＝最小；最大） | 0.6930（0.6650；0.7845） | 無量綱 −1..1 | 產品推估 | 一致性，不是含量、機率、深度；至少半數格同值 |
| SWIM2 1–5 m 平均（中位＝最小；最大） | 0.6225（0.5；1.0） | 無量綱 −1..1 | 產品推估 | 同上；兩層共用輸入 |
| 若 1–5 m 只含 0.5 與 1.0 兩值，1.0 的占比 | 0.245（約 24.5/100 格） | 比例（假設） | 本次計算（假設） | 無逐格資料，未驗證；不得當作量測占比 |
| CDOD MY34 平均／p95；MY35 平均／p95 | 0.1254／0.2400；0.1101／0.1731 | 無量綱（9.3 µm 吸收柱） | 產品推估 | 3° 網格；不可換算覆土堆積率或覆土厚度 |
| MCS 15/03 LTST 中位；反差 | 171.27／246.31；66.83 | K | 產品推估 | 5° bin，中心距本格約 146.7 km；模式時間校正，無 QA |

### 2.2 分項證據狀態

| 證據類型 | 取得情況 | 直接／間接 | 說明 |
|---|---|---|---|
| 影像（HiRISE／CTX） | 未取得：ODE robots 拒絕、shell 403、索引過大（LV-S15、S19、S21） | — | 無影像 ID，無法判地貌 |
| 熱 | 取得 TES TI（共享資料）；Piqueux 冰表深度圖未取得 | TI：間接（表層材料）；Piqueux：模型 | Piqueux 輸入為 MCS＋THEMIS |
| 雷達（SHARAD） | 未取得 | — | 無軌跡、無反射體資訊；Séjourné（Utopia 帶，47–78°N）曾**未**偵測到反射，作者說可能是冰太淺或雷達穿透不足，兩者無法區分 |
| 光譜 | 未取得 | — | 未見任何格內偵測；未見不等於無 |
| 氫（MONS） | 區域圖存在；本格值未取得 | 間接 | 足跡約 550 km FWHM；本格面積約為其圓面積的 0.22% |
| 暴露冰 | 最近已知點 389.0 km；格內無 | 間接（區域脈絡） | 只涵蓋繼承點表 |
| 大區域研究 | Bramson：冰層底深度眾數 42 m、平均 51 m（ε=2.5）；Viola：過量冰層多在約 15–20 m 內；皆在 180°E 以東 | 區域、他處 | 不可搬到本格 |

### 2.3 判定（冰存在／深度／含量分開）

| 問題 | 判定 | 直接證據 | 間接線索 | 模型假設 | 未知 |
|---|---|---|---|---|---|
| 冰是否存在 | **證據不足**（非「無冰」） | 無 | 區域性：SWIM 一致性為正（100/100 格）、MONS 區域 W_dn>10% 帶延伸至 Arcadia（約 45°N、150°W；Pathare Sec.4.1）、東側研究的覆土與過量冰 | SWIM 組合式 Ci；二層／三層 WEH 模型 | 格內是否有冰 |
| 冰深度 | **unknown** | 無 | 無本格值 | Piqueux 二層擬合（未取得）；SHARAD ε 假設（未取得） | 深度；現有資料對 0.5–15 m 解析不佳（Morgan p.6） |
| 冰含量 | **unknown** | 無 | 無本格值 | WEH 閾值 25 wt%＝過量冰（Pathare Eq.6），無本格 WEH 值 | 含量；SWIM 不是含量 |

### 2.4 共享輸入與不可宣稱

- SWIM Ci 由 N（MONS）、T（TES＋THEMIS 季節視熱慣量）、G（CTX 格圖地貌）、RS／RD（SHARAD）五項平均而成（Morgan 2021 pp.3–4）；0–1 m 與 1–5 m 兩層共用輸入；**本格不知道五項各自的值**，只有合成值。
- TES TI（ME-03）與 SWIM 的 T 輸入屬同一資料族；MONS 同時進 SWIM 的 N 與 Pathare WEH；以上不可當作獨立確認。
- 不得宣稱：SWIM＝含冰量或機率；CDOD＝覆土堆積率或厚度；TI＝溫度或硬度；0.5 m 解析度的 SHARAD 雜波或未見反射＝無冰；MONS 約 550 km 平均＝本格值；Arcadia 東側研究結果＝MS-02。

## 3. 問題三：地球配對驗證程度（完整：`analog_validation.csv`）

| ID | 證據 | 判定 | 與 PR #6 head 比較 | 依據 | 升級所需 |
|---|---|---|---|---|---|
| AV-01 | University Valley（E01） | **保留**（用途限縮：已知冰膠結界面深度＋季節熱響應；不含覆土堆積、雷達、塵率） | 判定不變；用途寫窄 | 站點多深度溫度與冰膠結層頂 42 cm（Marinova 2022）；谷級錨點與 W 站相距 1.06 km；2009 與 2022 的 S/D 站座標互換未解（PR #10 I08） | 不適用 |
| AV-02 | Adventdalen CS-1 岩芯 | **保留為子過程**（風成覆土累積＋同生冰） | 不變 | 岩芯本身是含冰量真值；78.201°N、15.840°E | 不適用 |
| AV-03 | ADE 鑽孔 | 一般方法參照 | 不變 | 78.1722°N、16.0613°E；與 CS-1 相距 5.97 km | — |
| AV-04 | WISDOM 多邊形溝槽雷達 | **一般方法參照（不升級）** | 不變 | 無座標、無同線獨立冰真值；ε=3.2／≥7 為模型輸入；本輪新查 EPSC2026-890、EGU25-9766 皆無場址／真值資料；HAL 被擋 | WISDOM 測線座標＋同線開挖／岩芯冰觀測 |
| AV-05 | Adventdalen 2023 岩芯＋InSAR（Wendt 等 2026） | 新增來源；**不接成雷達鏈** | 新增 | 12 個岩芯 0.63–2.02 m、2023 年 4–5 月；**未用 GPR**；Zenodo 10.5281/zenodo.11187359（未下載） | 岩芯座標與 WISDOM 測線座標並做重疊計算 |
| AV-06 | Beacon Valley（E02） | **待補證據（不升級）** | 不變 | 本格 PR 無座標；搜尋僅出 Mullins 冰川與一篇不可讀的學士論文；未開到含雷達與獨立冰深的 Beacon 論文 | 自行核對座標＋覆土厚度／冰深真值 |
| AV-07 | Haughton 多邊形溝槽（E04） | **待補證據（不升級）** | 不變；新讀到「GPR 與淺鑽確認多邊形溝槽有冰」一句 | 無座標、深度、ε、活動層、共線說明；覆土非風成粉砂 | 同線 GPR 深度＋ε 與鑽探深度的數值 |
| AV-08 | 新增候選 | **無新增** | — | 沒有任何地點在本輪可自行核對資料與範圍而補足缺口；不做全球排序 | — |
| AV-09 | CS-1→ADE→WISDOM 串接 | **不成立**（不得寫成同址驗證鏈） | 不變 | 相距 5.97 km；年份：鑽孔 2017-03、雷達 2022-03、Wendt 岩芯 2023-04/05；雷達無座標 | — |

## 4. 本輪判定變化

- 無候選層級的處置變化（E01 保留；E02、E04 待補；E03 維持降級）。
- 變化的是**描述界線**：E01 用途限縮；E03 拆為 CS-1（保留子過程）、ADE（方法參照）、WISDOM（方法參照）；新增 Adventdalen 岩芯來源（AV-05）但不接鏈；Haughton 新增一句已讀內容但不升級。
- MS-02 位置：由「Cebrenia 四邊形內、是否 Arcadia 未確認」更新為「MC-7 內；在 Arcadia Planitia 範圍框（次級來源）內靠西緣約 84 km；未見任何研究的範圍涵蓋 168°E」。地質單元仍未確認。

## 5. 未知（本輪無法取得，原因見 search_log）

- 格內：冰是否存在、深度、含量；SHARAD 軌跡與反射；HiRISE／CTX 影像 ID 與地貌；CRISM 光譜；暴露冰；Piqueux 像元值；MONS 本格值；地質單元。
- 地球：WISDOM 測線座標與同線冰真值；Wendt 岩芯座標；Beacon 座標與資料；Haughton 數值。
- 來源間：Piqueux 像元大小（2 ppd 對 3 ppd）；Morgan 2021 研究區經度字面（「290°E to 225°E」）有歧義；Ramsdale 格圖帶經度界為近似。

## 6. 待人類決定

- 報告是否沿用 MS-02 的地理描述：「Cebrenia（MC-7）內，近 Arcadia Planitia 西緣；單元未確認」，而非「Arcadia」。
- 報告 H2／H3、場址比較表與「E03 可測」的殘留措辭（PR #9 C24）是否改寫；本輪**未修改**正式報告。
- 是否把 E03 在候選表拆成 CS-1／ADE／WISDOM 三列。
- 報告是否保留「SWIM 1–5 m 中位 0.5、最大 1.0」的呈現；本輪補充的 0.245 為假設，建議不寫入正文。
- 是否在能連線的環境補取：Piqueux `d_m`、SHARAD 軌跡、ODE 影像清單、SIM 3292 GIS、Wendt Zenodo 資料（需要時另開補件任務）。
- PR #10 I06：EV-018（約 2560 h 雙閾值）本輪未核對，仍待核定。

## 7. 重現與檔案

- `python3 outputs/research/MS-02/local_validation/derive_metrics.py` → `derived_metrics.json`、`fig_local_prior_work_extents.png`
- `python3 outputs/research/MS-02/local_validation/build_tables.py` → `local_prior_work.csv`、`mars_ice_evidence.csv`、`analog_validation.csv`、`search_log.csv`
- `python3 outputs/research/MS-02/local_validation/verify_local_validation.py` → `verification.json`
- 距離使用 Mars 半徑 3,396 km（格尺寸、火星距離）與地球 6,371 km（地球站點距離）；格圖帶界為本次計算，非論文所給。

## 5. 資料尺度過粗：整理與判定（表：`outputs/research/MS-02/local_validation/scale_gap_resolution.csv`，核對：`verify_scale_gap.py`，3 輪一致）

- 地形、熱性質、水／冰、大氣／沙塵：已用現有最細資料列出格內數值與限制（SG-01–04）。
- 當地材料、覆土、形貌：Excel（含 MEDA 原始紀錄，屬 Jezero 漫遊車）與 GitHub 皆無亞格（<3.7 km）資料，**無法由現有資料回答**（SG-05–07）；所需最小資料見表。
- 因此「已回答」只限於格尺度描述；三項未知維持 unknown，不推論為無冰或無覆土。
- 補（SG-08）：以 `screened_pool.csv.gz` 取本格 ±2° 的 81 個 0.5° 格比較——熱慣量 186–302（均 241.6；本格 217.3 偏低）、高差最大 542 m；顯示周邊並不均一，但仍是同一批粗產品，不能代替當地材料、覆土、形貌。`all_data_usage.csv` 也把「局部材料、冰真值、細地形」列為未取得，與本判定一致。

## 6. ODE 網頁查詢補充（2026-11-15，LV-S56–S60；表：`ode_coverage_query.csv`）

- 方式：在使用者電腦的瀏覽器操作 ODE Data Product Search 表單，座標框 52.5–53.0°N、168.0–168.5°E（未呼叫 REST 介面）。
- 取得：CTX 5 景（2012-05-12、2012-06-09、2016-04-13、2018-01-20、2024-12-31）；HiRISE 0；SHARAD 3 筆觀測（2007-07-24、2010-10-20、2010-11-05；各有 EDR＋USRDRV2 雷達圖；無雜波模擬）；CRISM 383（VRDR 6）。
- 仍未取得（不因此改變判定）：影像與雷達圖內容、CRISM 光譜、Piqueux 像元值、SIM 3292 GIS、WISDOM 座標＋同線冰真值。形貌、覆土、材料維持未知；本節只把「清單」補齊。
- 限制：ODE 對範圍框是「相交」或「包含」未核實；HiRISE 0 只代表清單無此景。
- 補（授權後在 ODE 打開產品頁）：只讀完 D01_027516_2328_XN_52N191W 的 Meta Data（範圍 51.21–53.798°N、168.06–169.41°E，6.09 m/px，入射角 47.93°；表：`ctx_product_metadata.csv`）；縮圖可見許多大小不一的小撞擊坑，僅縮圖層級，不做多邊形／裂隙／冰崖判斷。其餘 4 景與 3 條 SHARAD 未打開（ODE 頁面在視窗縮放後版面跑掉，右側面板被截）；是否覆蓋固定範圍本身尚未核實。
- 補2（同日再試）：G23_027160_2321_XN_52N192W 的 Meta Data 讀完（50.759–52.9352°N、167.34–168.56°E，6.15 m/px；ODE 註記區域「Arcadia Planitia」）；K01 只看縮圖。J02、V16 與 3 條 SHARAD 的詳細頁因 ODE 的「quick view」彈窗不穩定而未讀成；地圖上選取的一條足跡條帶看起來涵蓋查詢框，但哪一景無法確認，不作為證據。仍未判讀任何影像或雷達圖內容。
