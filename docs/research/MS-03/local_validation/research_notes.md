# MS-03 — local validation evidence notes

## 2026-11-15：CRISM 格內光譜新增資料與條列判定

- 本輪起始 SHA：`778af696c654a191fe2a720f24d9f30ebd7d247b`；已連線核對原分支，沒有隊友未同步更新。固定範圍未變。
- 新資料：[CRISM 資料、方法與來源](../../../../outputs/research/MS-03/local_validation/crism/README.md)；[QA／光譜圖](../../../../outputs/research/MS-03/local_validation/crism/F-CRISM01_pixel_QA_spectra.png)。
- 本節取代前輪「只有CRISM標籤、未取得任何cube」的取得狀態；前輪紀錄保留於下方及 `crism/previous_catalogue_status.json`。本輪取得局部原始cube位元組，非完整全條帶光譜。

|觀測|實際取得／格內定位|基本數值與校準檢查|尚未確認|
|---|---|---|---|
|HSP0002DE65_03_IF218L_TRR3|2014-02-10 17:28:23.764至17:31:23.693 UTC；Ls88.051829；154通道；原始列628至762（零起算）；1350個DDR格內中心|966個中心通過實際採樣1300至2200nm通道的有限值、非65535、WA場景波長及正I/F檢查；384個診斷錨點對應校準非場景樣本|雲霜、大氣與儀器殘差、最終科學有效性、冰吸收檢出率|
|MSP00018FDA_01_IF214L_TRR3|2010-05-25 09:48:43.578至09:51:43.515 UTC；Ls95.410373；55通道；原始列2434至2582；9056個DDR格內中心|8516個中心通過相同基本檢查；540個診斷錨點對應校準非場景樣本|同上；不能把基本通過比例稱格內有效面積或無冰比例|

- 證據層次：已由「目錄相交／標籤取得」前進到「取得局部光譜、逐像素定位、波長與缺值檢查」；**未前進到冰存在確認**。
- 原始網址、逐次請求UTC、HTTP206 byte ranges、SHA256、失敗紀錄：`crism/retrievals.json`。原始DDR整檔取得後，保留14個backplane所需列的逐段原始位元組與偏移；不是自造定位或原始連續檔案。
- 座標：DDR實際存帶負號東經，程式明確modulo360。依SIS §3.2.1，IR定位代表約2300nm；不同波長keystone與絕對定位誤差未校正，不能保證每個1.5µm像素完整足跡在格內。
- 尺度：10倍空間合併；格內相鄰跨軌中心距離中位數187.80／187.44m（本輪球面計算，R3396190m）；不是PSF實測或裂隙可辨識尺度。
- 原始TRR3與標籤指定WA3的detector-row表完全相符；波長以原通道／每列實際值保存。沒有套用均勻波長軸、填補缺值或插值補通道。
- 1.5µm附近採樣不連續；原文Table3-3的BD1500_2高光譜5／11／5 kernel沒有直接套在稀疏mapping資料上。本輪未計算標準冰指數；若另採mapping-mode定義，需記錄定義、通道近似與驗證，不能宣稱mapping資料原理上完全不能計算指數。
- 原始光譜曲線保留凹陷；大氣、熱、光度與光譜重採樣旗標均OFF。圖中的空間5至95百分位是資料分散，不是信賴區間或檢出門檻；未把凹陷命名為冰。
- 判定表：

|問題|本輪狀態|依據／缺口|
|---|---|---|
|格內可取得光譜嗎？|已確認兩組局部光譜|有原始I/F bytes、DDR與WA，非只有目錄|
|有效像素完整覆蓋整格嗎？|未知|只呈現DDR中心與基本檢查；未建立逐波段足跡、完整面積或雲霜品質遮罩|
|能確認地表冰嗎？|unknown|大氣／雲霜／儀器殘差與冰吸收判別未完成；沒有校準過的檢出或陰性界限|
|能確認地下冰深或含量嗎？|unknown|光學表面／大氣訊號不能單獨量測覆土下的冰深、連續性或含量|
|AD1能恢復具體形貌配對嗎？|不能，維持降級|約188m中心間距光譜資料不能提供可靠閉合Mars邊界|
|可以與UV時序配時或反演嗎？|沒有執行，限制維持|不涉及Campbell／HOBO時標修正，不用地球數值推MS-03冰深|

- GPU／主要對話下一步（未完成，需決定是否啟用）：建立具來源的mapping-mode大氣／光度校正與有效像素流程；檢查雲與季節霜、壞點／條紋與光譜微笑殘差；以已知光譜或控制觀測校準檢出限制，再決定是否計算冰吸收指標。未驗證前，保留unknown。
- 本輪僅處理兩條較低入射角、北半球夏季L-detector mapping觀測，不代表已檢查全部12個L-detector IF產品或排除所有季節。
- 原始來源實讀：PDS DPSIS v1.3.7.7（2024-11-05）§§2.5.1至2.5.3、3.2.1、3.4.1、3.9.1／AppendixE及Table3-3相關段；兩份TRR3、兩份DDR1與兩份WA3標籤的欄位。完整HTML取得不等於所有章節均已閱讀。
- 新增資料／圖／方法及QA詳見 `crism/manifest.json`、`crism/validation.json`；既有26項檢查另保留。未執行的冰偵測與大氣校正不得列通過。

## 前輪歷史紀錄（起始SHA 8fa07af；CRISM取得狀態由上節更新）

- 查核日期：2026-11-15（Asia/Taipei）。本檔為資料與條列研究筆記，非正式報告。
- 固定範圍：57.50–58.00°N、242.00–242.50°E；planetocentric、east-positive。未移動範圍。
- 起始 PR #7 SHA：`8fa07afac4a98096958880f6a5ece16f35abc4db`。
- 已讀驗收 PR #9：`c206553fc681328d214cbbcd508d3c5b1391e200`；整合 PR #10：`0260c511d9fce6be12d3460a69e474f333160cbf`。PR #10 使用較早 MS-03 版本，不等於本輪新增資料已驗收。
- 資料表、程式、圖與取得紀錄：[local_validation](../../../../outputs/research/MS-03/local_validation/)。

## 2026-11-15 補查：三份原始表的作者／官方入口

- 本次起始 SHA：`778af696c654a191fe2a720f24d9f30ebd7d247b`；使用獨立本機副本，未改動原副本尚未提交的 CRISM 工作。
- 交付歷史：首次交付時依「先不要推 PR」保留在本機。使用者後續授權推送並直接合併；發布核對時 PR #7 已合併，因此本補查另以後續 PR 提交。
- 本次整合基準：最新 main `08d2740a23694a54bcc11cabf7120114d2e120fc`；分支 `codex/ms03-original-tables-followup`。保留已合併的 CRISM 資料、判定與查詢紀錄；實際發布／合併狀態以 GitHub 後續 PR 為準。
- [逐表取得狀態](../../../../outputs/research/MS-03/local_validation/original_tables_followup/table_acquisition.csv)、[公開入口／內容核對](../../../../outputs/research/MS-03/local_validation/original_tables_followup/content_checks.json)、[重跑與後續取得步驟](../../../../outputs/research/MS-03/local_validation/original_tables_followup/README.md)。先前失敗紀錄仍保留；本次另存 29 次公開請求。

|原始表|本次確認的證據|尚未取得／空間判定|
|---|---|---|
|Cohen-Zada 2024 `Data Set 1.tab`＋欄位說明|DataCite 父子紀錄確認資料檔 DOI [`J9K4HL`](https://doi.org/10.18738/T8/DUCOYB/J9K4HL)、欄位說明 DOI [`E4MMUE`](https://doi.org/10.18738/T8/DUCOYB/E4MMUE)；另有 `SI_Revised.pdf`。已讀 Hood 公開首頁及其 MBARS 程式庫完整六項檔案清單，未在這些頁面找到指定原表|Dataverse 公開資料、匯出及 OAI 入口均為 CloudFront 403。**只有 metadata，沒有原表資料列**；54 幅研究影像與本格的實際關係仍 unknown，不將 Hood 的其他表直接當作同一清單|
|Levy 2009 Data Set S1|原文 Supporting Information 列有 `jgre2606-sup-0002-ds01.txt`，並有同表 XLS／PDF 版本；實讀原文 §§2–3、Appendix A 與附件清單。沿 Colgate 官方師資頁讀取作者公開實驗室及研究頁|TXT／替代 XLS 下載仍 HTTP403；已讀作者頁未提供指定附件。推測的舊站網址回 HTTP200，實為 **Google Drive 登入頁**，沒有讀到其內容。完整影像／分類表未取得；格內關係 unknown|
|Dundas 2021 `TableS4.csv`|成功取得 [USGS 正式資料頁](https://www.usgs.gov/data/locations-and-properties-ice-exposing-scarps-and-new-impact-craters-mid-latitudes-mars)、[Data Catalog 正確冒號 ID 入口](https://data.usgs.gov/datacatalog/data/USGS%3A5f99f0b8d34e198cb786e8e7)及其列出的 [AIS XML](https://www1.usgs.gov/pir/api/identifiers/USGS:5f99f0b8d34e198cb786e8e7)。AIS 位元組與既有 FGDC 完全相同，可確認欄位定義，但不是觀測表|ScienceBase 單筆／搜尋／檔案入口及 publisher CSV 仍 HTTP403。`TableS4.csv` 未取得；不能計數格內暴露冰，也不能作完整清單排除。誤用底線 ID 的另一個 Data Catalog 嘗試回404，與正確冒號入口分開記錄|

- 三份原表皆 **未取得**；沒有執行資料列篩選或新的足跡交集，命中數留空，**不是零命中**。也沒有新增可改變冰存在、實際冰深或冰含量判定的資料。
- 已保存取得的 [DataCite metadata](../../../../outputs/research/MS-03/local_validation/original_tables_followup/metadata/)；父紀錄文字稱 xlsx/docx，但格式清單列兩份 TSV 與一份 PDF。這只確認典藏描述，不能冒稱已驗證實際檔案格式、資料列或精度。
- 已抽出 [USGS Table S4 九項欄位定義](../../../../outputs/research/MS-03/local_validation/original_tables_followup/source_column_notes.csv)。其中 `Yes (CTX)` 缺 HiRISE 彩色確認；`CRISM ice? = x` 代表沒有適當資料，不能改成未探測到冰。
- Figshare 以三篇原文 DOI 作 `resource_doi` 精確查詢，均回空清單；只說明該入口／條件的結果，不是跨平台或歷史完整排除。作者頁查找也只涵蓋實際讀到的頁面與程式庫；未寄信或存取私人檔案。
- 資料到手後須先核對原始座標、缺值、ID 與欄位說明；點位置及影像足跡分開判定，不能只用中心在格外排除整張影像。沒有可靠足跡時保留 unknown，不能以地區名稱、大區研究範圍或索引零命中代替原表核對。
- **目前可說：** 三份指定表的來源與缺件已具體化；本次公開入口補查尚未取得原始資料列，固定格內成員關係未能確認。
- **目前不能說：** 三份表都不含 MS-03、本格從未研究、本格沒有多邊形／冰、AD1 已完成具體定量配對。AD1 維持一般方法參照，MS-03 形貌維持 unknown；不跨 Campbell／HOBO 配時。

以下保留先前已完成分析及查核紀錄；本次補查不代表其 PR 驗收狀態改變。

## 判定與變化

|問題|本輪取得／計算|判定與限制|
|---|---|---|
|格內有無既有同用途資料？|Piqueux 2019 公開原始矩陣，中心 57.75N/242.25E；原生 0.5°格與本範圍一致|已有格內地下冰熱模型產品；不能宣稱從未研究或首次提出|
|冰是否存在？|條件式熱模型、既有 SWIM 正一致性|仍無本輪獨立局部真值；產品依賴不能當多次獨立確認|
|實際冰深？|存檔模型 `d=0.103161566 m`，展示僅約 0.10 m|假設下模型值，非實測深度；實際深度 unknown|
|冰含量／可採量？|未取得格內經驗證的含量反演|unknown；不得從一致性或熱模型換算|
|地質單元？|USGS 原始 GIS：OBJECTID 1264，AHv，完整包含固定格|Amazonian and Hesperian volcanic；1:20,000,000 區域分類，非局部礦物或覆土剖面|
|多邊形／裂隙？|五個事前指定位置的 CTX 拼接顯示圖，逐張檢視|未取得可可靠追描的完整邊界；形貌 unknown，非不存在|
|雷達可用性？|6 條 ODE 格內相交軌跡；其中一段原始 RDR 256 筆座標核對|僅幾何取得成功，回波尚未判讀；非冰層探測結果|
|AD1 配對？|沒有新增可靠 Mars 邊界|維持降級，一般方法參照；不做幾何分布相似度|
|UV 配對？|本輪未新增或修正地球時序|僅已知界面、方法與資料品質參照；不跨 Campbell／HOBO 配時|

## 原始來源、實讀範圍與數據

- **LV-PW01 / LV-ICE01–02：Piqueux et al. 2019**。
  - 論文：[10.1029/2019GL083947](https://doi.org/10.1029/2019GL083947)；實讀 publisher HTML 方法／討論 §§2–3、圖 2–4 圖說及資料取得段落；不聲稱讀取全文 PDF。
  - 原始資料：[CaltechDATA v1.0, D1.1316](https://data.caltech.edu/records/ym7fc-x0r93)，發布 2019-11-27。
  - 已取得 Lat、Lon、d_m、TI_SI、Notes 五檔；與提供者 MD5 全部相符。原始矩陣 360 緯度列×720 經度欄；本次讀取零起算 row64/column484，非重新擬合。
  - 上覆材料模型熱慣量：215.4277344 J m⁻² K⁻¹ s⁻½；非地球溫度或地下冰含量。
  - 存檔座標為 **2 ppd**，論文方法寫 **3 ppd**；未取得兩者轉製說明。依實際存檔座標取值，不插值假裝 3 ppd。
  - Notes 的矩陣方向與 TI 單位排印需與座標長度、論文物理單位分別核對；詳見 `piqueux_qa.json`。
  - 模型下層假設為冰；材料、孔隙率、膠結、表層熱性質與邊界條件有歧義。離散查找深度不支持原始小數位精度；不分辨孔隙冰與塊狀冰。
  - 每格觀測時段及 QA 未提供；原始 MCS 約 7 km 支撐不能等同格內均一，存檔格約 30×16 km。與其他熱資料／SWIM 有輸入依賴。
- **LV-PW02 / LV-ICE10：Tanaka et al. 2014**。
  - [USGS SIM3292](https://doi.org/10.3133/sim3292)；[原始 GIS ZIP](https://pubs.usgs.gov/sim/3292/downloads/sim3292_database.zip)；[DMU p1 AHv 條目](https://pubs.usgs.gov/sim/3292/pdf/sim3292_dmu_with_locality_images.pdf)。
  - HTTP Range 取得原 ZIP 目錄與 SHP/SHX/DBF/PRJ 四個成員，逐一核對 CRC32，非鏡像圖層替代原件；未下載完整約 809 MB ZIP。
  - 以原始有效多邊形判定完整包含固定格。Mars_2000 sphere 半徑 3396190 m；−180..180 經度與 east-positive 轉換留在程式。
  - DMU 的 AHv type locality 不在本格；不得搬用其現地性質。區域底圖不排除薄覆蓋層。
- **LV-ICE11：CTX 原始來源與局部可辨識性**。
  - [Caltech Murray Lab V01 E-120_N56](https://murray-lab.caltech.edu/CTX/V01/TilePages/E-120_N56.html)；實際取得作者 KML 階層、原始 seam map 與五張 level13 PNG。
  - 原始產品：`D01_027566_2370_XN_57N117W`（2012-06-13，約 6.09 m）；`G01_018718_2370_XN_57N118W`（2010-07-25，約 6.08 m）。NW 拼接樣本涉及兩日期。
  - 中央與四象限固定錨點；每塊 256×256，完整 KML 邊界在固定格內。顯示網格約 5.41–5.45 m，不能新增原影像細節。
  - 五張均非空、alpha 不透明；**不等於科學有效像素 QA 全通過**。絕對定位誤差、雲霜、輻射與裂隙辨識率未校準。
  - 已逐張看過：有斑駁紋理與小型坑狀構造；無可靠完整裂隙／多邊形邊界可追描。局部樣本不能代表整格不存在。
  - [影像判讀圖](../../../../outputs/research/MS-03/local_validation/F-LV01_CTX_samples.png)：包含方位、範圍、來源日期與尺度限制。
- **LV-ICE05–07：ODE 實際格內幾何查詢**。
  - [官方 API](https://oderest.rsl.wustl.edu/live2/)；完整請求、日期、原回應、產品 URL／ID／WKT 在 `retrievals.json`、`search_log.csv`、`observation_inventory.csv`。
  - CRISM：168 個產品、44 個 observation IDs；56 個 IF 產品，其中 12 個 L detector IF；數量不是獨立冰探測次數。已取得兩份原始 PDS label，尚未取得 cube／DDR／有效像素與光譜冰吸收分析。
  - THEMIS IRBTR：35 個相交產品；UTC 起始範圍 2003-05-05 至 2018-09-04；非連續觀測或完整季節曲線。未下載科學 cube，不能提出新局部熱反演。
  - SHARAD RDR：6 條實際相交 LineString；是抽樣星下點，不是波束足跡。初次 USRDR 是無效產品類別查詢，不是零覆蓋。
  - 原始 `R_1768301_001_SS19_700_A`：2010-05-05，record5822 bytes；Range 取得零起算 57227–57482 共256列，1490432 bytes；依原始 FMT 的 little-endian float64 與 UTC 欄獨立解碼。
  - 256/256 星下點落格內，含連續超取樣，不是256次獨立觀測。未評估 SNR、表面雜波、介電參數或地下反射層；沒有冰層陰性判定。
  - [幾何與支撐圖](../../../../outputs/research/MS-03/local_validation/F-LV02_observation_support.png)；原始位元組、座標 CSV 與 QA 可重跑。
- **LV-ICE03–04：SWIM2 原生資料重現**。
  - [官方 SWIM2](https://swim.psi.edu/SWIM2Products.php)；本機原始 GeoTIFF SHA 與已交付版本一致。每產品格內100個原生中心有效，依 cos(latitude) 加權；兩組平均約0.910904及0.509972。
  - 只是舊產品取樣重現，非新增觀測。深度組別不是實測分層；一致性不是機率、冰量或冰深。熱、雷達與地貌依賴見證據表。

## 既有研究的實際空間範圍與缺口

|來源|實際核對|可用分類|尚缺|
|---|---|---|---|
|Piqueux 2019|公開原生格恰好覆蓋固定格|格內相同冰探查用途的模型產品|獨立局部真值、每格 QA、2/3 ppd 轉製鏈|
|Cohen-Zada 2024，10.1029/2024JE008387|原文 §§1.2、2、4.3.2–5，圖1/5及資料段落；研究50–70N、大區域含本格|附近／大區域冰與地貌研究|54個HiRISE研究影像的逐幅格內關係；Texas Dataverse API403，不能用大區域推定本格有高解析圖|
|Dundas 2021，10.1029/2020JE006617|Table1、撞擊／資料段落及官方 FGDC；列有S1–S4檔名|已讀個案在其他緯度；完整清單格內關係未知|ScienceBase及publisher附件403；完整CSV未取得，不作全清單排除或格內暴露冰主張|
|Courville 2026，10.3847/PSJ/ae8904|官方LPSC2026 1792 p1方法與結果、作者摘要|60S–60N區域模型框架|IOP HTTP200實為CAPTCHA，不是全文；未取得本格後驗／體積；不得引用為本格冰量|
|Gregg & Schiff 2020 LPSC2299|原摘要與圖1；兩個具名CTX原始足跡完整不相交|已核對的具名圖為格外案例|只排除這兩影像，不宣稱排除全文所有範圍|
|Ulrich 2011 AD1|沿用先前已核對的兩幅火星比較影像與原表|既有火星比較用途、格外案例|不能代替MS-03格內邊界；本輪沒有新同尺度幾何|

- 來源與讀取範圍逐筆保留於 `local_prior_work.csv`；查詢詞／平台／取得時間於 `search_log.csv`。未使用「座標無命中＝從未研究」推論。
- 具體資料工作差異：原始熱模型格值定位、原始地質 GIS 包含關係、固定局部 CTX 樣本可辨識性、雷達原始座標 QA、產品依賴／缺件盤點。
- 尚無證據支持：新地下冰發現、新多邊形發現、全球首創方法、AD1 與 MS-03 成因相同。
- 外形即使未來可量測，仍需獨立冰／熱／物性資料、排除乾縮／構造／侵蝕等成因、共同尺度與選樣協定，才討論成因類比。

## 交接與待人類決定

- 主要對話：是否以「已發表冰模型的局部追溯與觀測可驗證性」定位 MS-03；不要稱未研究場址或新冰資源發現。
- GPU：可接手取得 CRISM cube+DDR、THEMIS科學像素與季節QA；先判有效格內像素，再決定分析。雷達如啟用，需完整有效段、雜波模擬、SNR與介電假設，不從本次幾何CSV推冰深。
- AD1：維持一般方法參照；沒有格內可信完整邊界，不建立 Mars polygon 表、不算分布相似度、不填0。
- UV：保留已知界面／儀器品質參照。作者處理後長時序與未取得的原 logger、校準程式／部署校時紀錄分清；Campbell四小時變化原因仍未知，不與HOBO自動配時。
- 不新增地球場址：目前瓶頸為 Mars 局部可觀測性與獨立真值；更換地球點不補足這些缺件。
- 驗收資料的措辭待人類修訂（本輪未改其檔）：PR9 C31 的 MCS「大氣反差」應核對作者[Surface Temperatures record](https://zenodo.org/records/17947556)及 `tsurf_correct`，不能把地表產品稱大氣；C39 的 raw pending 須區分已取得處理後時序與未取得原 logger；C37 歷史強 AD1 敘述不得覆蓋本輪降級。
- 舊「615筆位置未知」已被既有查核取代；本輪未重做索引生成器、SQL、149組標籤診斷，也未把它們計為新增研究。

## 可重現性與本輪檢查

- 執行方式、依賴、原始檔取得／Git內外區別：見輸出目錄 `README.md`。
- 數據、來源、原始位元組及 PNG 雜湊：見 `manifest.json`、`retrievals.json`、各 QA JSON。
- CSV 使用 UTF-8 BOM；讀取以 `utf-8-sig`。`dependencies_json` 為可解析 JSON。
- 兩張最終 PNG 已實際開啟檢查；修正先前座標／來源註記重疊，NW保留兩日期。圖不是地下冰探測圖。
- 自動檢查結果以 `validation.json` 為準；未執行的後續光譜、雷達回波與跨儀器配時分析不列通過。
