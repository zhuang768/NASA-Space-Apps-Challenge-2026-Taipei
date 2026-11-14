# Team 1 地球類比場址與用途配對

## 備案增補：EARTH-003，2026-11-14

本次只新增 **Linnaeus Terrace 的 LT 歷史溫度站 → I-02**，固定 ID `EARTH-003`，定位為**尚未啟用的檔案資料方法備案**。EARTH-UV-001 及 EARTH-002 的原資料列、用途與查核狀態完整保留；Elephant Head 仍是 GPU 優先工作。以下是本輪更新，後面的前次報告作版本化紀錄保留。

### 版本核對與最新需求

開始時為 main，工作區乾淨，`git pull --ff-only` 顯示與遠端一致，基準 `cf72039a4bdfb94666c8df176de41eefd55f30ee`。主分支尚無 `docs/research/main_research_requirements.csv`；本輪 fetch 找到主要對話分支 `codex/mars-research-mainline-20261114`，只讀取其 commit `9e5c49ea7b4d7272972e7d409e6a298e6ef3da4a` 的[需求單](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/9e5c49ea7b4d7272972e7d409e6a298e6ef3da4a/docs/research/main_research_requirements.csv)與[研究卡](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/9e5c49ea7b4d7272972e7d409e6a298e6ef3da4a/docs/research/main_mars_research_cards.md)，沒有合併或修改他人文件。需求單 SHA-256 `89fe4d295856c09edeaabd8a32b6e63fcb5cbc1ea3fe762e211eb6a773ccfaf3`；研究卡 `4ca4f38ef53a6326ed3d779e0c47669fb0ea00c557a0200a69229f0b7763a784`。

採用 **MR-20261114-v1** 的暫定研究設計：先做已發表資料的熱響應描述與驗證需求規劃；研究覆土如何造成冰界面判讀歧義。沒有獨立真值、控制與儀器規格，不能報盲判準確度或因果效應；冰損失為附屬模組。所有門檻仍 `not_defined`。該分支需求不是「已整合 main 的正式定案」。其中 T1-09 要求先補 EH 協定，本輪依使用者較新的指示，只備妥一個備案，**不啟用第二組計算、不改主題**。

已重讀本報告、候選 CSV、選點 brief、Team 2 的報告與 CSV、Mars discovery JSON。main 的 Team 2 尚無 EARTH-002 新回覆，故保留待 QA／查核狀態；UV 已知用途對照不變。未還原舊排名，未重新開啟總 Excel，未將檔案清單當作原始 raster。

### 為什麼保留這個備案

它有直接的歷史剖面與同站深度溫度量測，且官方小型 ASCII 原始檔已實際取得，適合在需要時評估深度熱響應。其價值是**不同深度支撐與資料取得路徑**，不是少有人研究。它位於 McMurdo Dry Valleys，屬已知冰穩定性研究站；如果展示必須以新場址為主，它不能直接承擔該主張。

本輪證據搜尋只沿用前次 Linnaeus Terrace 線索，查詢 `McKay Mellon Friedmann 1998 soil temperature stability ice cemented ground Linnaeus Terrace 25 cm data coordinates` 及 `"Soil temperatures and stability of ice-cemented ground" pdf McKay 1998`。未展開大量地點搜尋，也未進行隊友 2 的系統性新穎性查核。

### 固定身份、範圍與資料證據

| 欄位 | 本輪紀錄 |
|---|---|
| 地球／火星 ID | `EARTH-003 → I-02`，作 EARTH-002 的研究用途備案；不表示定量最相似，亦可供 I-01 問題規劃參考 |
| 名稱、別名與地區 | Linnaeus Terrace；LT；GGD6；Upper Wright Valley，Asgard Range，McMurdo Dry Valleys，南極洲 |
| 原座標 | LT1 site LT：77°36′S、161°05′E；換算北東為正 **−77.6°、161.083333333°**。目錄經度 161.083°為較短表示，不另建新地點 |
| 定位慣例與限制 | 原 guide 明列 `Geodetic datum: none`，不能自行指定 WGS84。角分座標只是歷史 point anchor，不表示轉換後九位小數精度；未提供水平誤差 |
| 代表範圍 | 同站感測剖面；沒有調查多邊形、周邊半徑或新採樣區。不外推到整個 Terrace |
| 地下結構 | LT2 作者摘要報冰膠結界面 **25 cm**；LT1 記錄挖坑至冰層並用錘鑽安裝地下感測器。此為歷史直接場地工作，非現在的獨立留出真值 |
| 四面向：地形 | LT1 站點表的平坦／脊狀／砂質等定性欄位；未有同物理尺度 DEM、數值坡度或局部安全檢查。表內 bedrock 勾選不代表所有覆土是完整基岩 |
| 四面向：溫度 | LT1 深度 0、17、23、40 cm；10 分鐘取樣、30 分鐘平均。僅原始檔取得與樣本列核對，無新統計 |
| 四面向：水／冰 | 歷史界面可作已知剖面參照；純度、連續性、厚度、當前冰況、可採量與鑽採性能 unknown |
| 四面向：大氣／沙塵 | 原格式列 air T/RH、日照；沒有取得地下 RH、站點風壓或沉積／磨蝕量，不配對沙塵耐受測試 |

LT1 guide 記錄 1993 部署，儲存期 1994-01-06 至 1995-01-16；目錄名義期間為 1994 年。實際原始檔起訖、缺列與有效數尚未抽取，不能先稱完整全年。guide 的深度精度為 ±0.03 m；23 cm 與文獻 25 cm 界面僅差 2 cm，不能將該感測器當作精確、全程確定的純乾土控制。這個限制會影響分層判讀。

LT1 的局部時間缺 UTC offset，RH 在低於 15% 時有偏差提醒。未確認校準／RH 基準前不改值；也不把零深度接觸式溫度與軌道 LST 當同一觀測。上述都是方法與品質文件資訊，不是本專案新量測。

LT2 原始論文全文本輪未取得：NASA NTRS 只有作者摘要，明列無可下載全文；DOI 的 web 讀取失敗。25 cm 依作者摘要與作者資料集的現地安裝方法使用。[UV 論文 Introduction](https://www.cambridge.org/core/journals/antarctic-science/article/climate-and-energy-balance-of-the-ground-in-university-valley-antarctica/432141245F43EF744DD8ABDB56580A5F) 中出現的 Linnaeus 45 cm 引述與此處 25 cm 不一致，**不以次級引述改寫本站真值**；請隊友 2 核對是否引用誤差、不同位置或年代。沒有取得全文就保留這個缺口。

### 三個案例的用途比較

既有 UV／EH 值沿用前次 Team 1 報告，**本輪沒有重算**；新備案也只有文獻值與資料可取得性。不同年份與材料不能用來作覆土的受控因果比較。

| 比較項 | EARTH-UV-001：已知用途對照 | EARTH-002：Elephant Head，待 QA／查核 | EARTH-003：本輪備案 |
|---|---|---|---|
| 已定位地下結構 | W 歷史界面 42 cm；新試驗區未知 | 監測站歷史界面 49 cm | LT 歷史界面 25 cm；角分錨點較粗，新試驗區未知 |
| 可用觀測資料 | 既有交接的現地序列與氣候抽取；本輪未讀 raw | 108 頁 EH2 表，原交接待 GPU 恢復與 QA | 官方 `mckay.dat` ASCII 已取到；多深度溫度，尚未完整 QA |
| 可支援的研究 | 已知參照／驗證設計 | 已知剖面熱響應描述；後續獨立真值設計 | 備用多深度熱響應描述，檢查層位／深度不確定性如何限制判讀 |
| 材料／環境差異 | 沿用前次冷乾谷底背景，熱物性未等效 | 前次 EH1 為石英岩來源、少量千枚岩；有地下 RH | LT1 為砂質場地並有砂岩表面通道；沒有地下 RH，不能補 EH 同類水汽分析 |
| 主要資料缺口 | 原序列與新實驗真值／範圍需交接 | PDF 解析、兩時標、3 cm 冬季缺測 | 年代較早、實際記錄期與時區待查；23 cm 層位誤差；無新冰／材料真值 |
| 已知用途與待查項 | 山谷尺度鑽採／溫控先例已確認 | 已有環境、微生物和 UV–EH 比較；完整協定待查 | 已有冰穩定性、熱性質研究；覆土控制＋獨立真值的完整問題交 Team 2 |
| 現有資料能完成什麼 | 在來源與 QA 足夠範圍內描述既有觀測 | QA 後描述共同有效時段溫差 | 若主要對話啟用、QA 後描述表層與多深度溫差；不是界面偵測驗證 |
| 仍需新量測／實驗 | 留出真值、正負控制、覆土材料／範圍 | 同左；冰損失另須初末冰量 | 同左；無新資料就不能報盲判誤差、因果效應或冰損失 |

這三地的冰界面與雪／水汽背景已有跨場址研究（前次 EH3 包含 Linnaeus Terrace 比較脈絡）。不能把這張比較表包裝為首次配對或新機制；我們交付的是版本化資料支撐、未能識別的條件與待測協定。

### 與 MR-20261114-v1 的對照

- `ALL-01`：固定 ID、用途、版本、來源與 unknown 已保留。
- `T1-03`／`T1-05` 的精神：只將既有多深度觀測用於描述；未取得覆土粒徑、密度、含冰量與同尺度地形，不宣稱控制條件滿足或 TES 等效。
- `T1-02`／`T1-04` 的精神：25 cm 是公開歷史答案，不能同時作擬合目標及獨立留出真值；缺無冰負樣本就不報誤判率，缺盲測就不報準確度。
- `T1-08`、`MAIN-01`：冰質量收支資料尚無，附屬冰損失模組不啟用；不新增門檻。
- `T1-09`／GPU-09/10：EH 仍先做。本備案需求為 `prepared_not_activated`，由主要對話決定是否接續；不能當作已完成需求單的第二組計算。

以上是把既有需求套用到備案的可行性說明，沒有替主要對話修改需求本身。真正獨立真值與控制不足，當前結論只到描述性檔案研究與驗證設計。

### 隊友 2 查核包（待查核）

固定 `EARTH-003 / I-02 / MR-20261114-v1`，地名別名、原座標、point anchor 與範圍限制見上表；來源 LT1–LT4。請分開記錄觀測／製圖、相關科學、同用途提案和已執行實驗。

精確用途：用已知歷史界面與多深度溫度作描述性參照，評估下一步要什麼獨立真值／覆土控制，才能避免把表層效應誤判為地下冰差異。真正盲判或受控覆土試驗尚未執行，冰損失不是本輪結果。

請查：（1）本站或明確重疊範圍是否已有覆土控制＋獨立留出真值的界面判讀實驗？（2）既有熱性質反演、冰穩定性模型是否已回答我們擬提問題與反應量？（3）是否有分段採樣／樣品控溫／含冰量收支的同站先例？（4）取得 1998 全文時，核對 25 cm／45 cm 引述與實際測站／年代。每項請給範圍、控制、真值、反應量與讀取範圍；未找到僅記本次未找到。

交接內容已寫入本報告與 CSV `team2_questions_json`；未直接傳送訊息、未收到回覆。`novelty_status` 保持待隊友 2 查核，有既有研究不等於完整新協定已做，也不等於新協定有原創性。查到重複用途時改列相應對照，不靠換 ID 規避。

### GPU 備案需求（主要對話決定是否啟用）

不啟動第二條批次處理。CSV `gpu_requests_json` 提供 `GPU-EARTH-003-AVAIL` 完整規格，狀態 `not_activated_main_decision_required_EH_first`。

| 輸入／問題 | 要求 |
|---|---|
| 來源 | GGD6 v1，DOI `10.7265/tjgd-wp08`；官方 FTP `mckay.dat`，網址、hash、大小見下節；不用重新搜尋全球資料 |
| 空間與期間 | 歷史 LT 點位；guide／目錄期間不同，先報原始檔實際起訖及缺列；local time UTC offset 未知 |
| 變數與單位 | 9 欄：1994 decimal day、air T（°C）、air RH（%）、sunlight（W m⁻²）、soil surface T、17／23／40 cm T、rock surface T（後五項 °C）；RH 基準待核 |
| 啟用後第一步 | 保留行號與原時間，檢查欄序／缺值代碼／重複／間隔／校準，輸出來源 manifest、字典與各深度有效數。小數日已四捨五入，不能要求每列精確差 1/48 |
| QA 後可問 | 有哪些共同有效觀測可描述多深度熱響應、季節變化與層位不確定性？依原始有效支撐報 paired N，不插補或反演冰深／TI |
| 不能做 | 無地下 RH 就不重建地表—冰層水汽梯度；無儀器規格／真值就不報界面偵測成功率；無初末冰量就不報損失；無同期資料不作 Earth 跨站受控因果結論 |

原欄位維持 `earth_candidate_id`、`mars_candidate_id`、`test_purpose`、`site_extent_description`。若 GPU 改名仍沿用前次 §7 的欄位對照，不刪原鍵。

### 來源、實際取得與限制

| ID | 原始來源與定位 | 本輪實際讀取 |
|---|---|---|
| LT1 | [NSIDC GGD6 v1](https://nsidc.org/data/ggd6/versions/1)、[原作者資料指南](https://nsidc.org/sites/default/files/20ggd6-userguide-v001.pdf)；printed pp.2–5 / PDF pp.3–6，§1.1–1.4、site LT | metadata 與整份 7 頁 guide 已取得；讀方法／欄位／site／精度。不是新 QA，也不是期刊全文 |
| LT2 | McKay, Mellon & Friedmann (1998)，[DOI](https://doi.org/10.1017/S0954102098000054)；[NASA NTRS 20040089259](https://ntrs.nasa.gov/citations/20040089259)，作者摘要 | 作者摘要可讀，全文未取得。支持歷史冰界面與溫度／冰穩定性研究，不能引用未讀 Methods 的細節 |
| LT3 | [官方原始 ASCII](ftp://sidads.colorado.edu/pub/DATASETS/fgdc/ggd6_soiltemp_antarctica/mckay.dat)；同目錄 `README.txt` | 已實際下載 1,171,171 bytes，核對前 3 列有 9 欄，首列與 guide 範例相符；未解析全表、未算統計或有效數 |
| LT4 | [NSIDC OAI/DIF metadata](https://nsidc.org/api/dataset/metadata/v2/oai?verb=GetRecord&amp;metadataPrefix=dif&amp;identifier=GGD6.001)，identifier `GGD6.001` | XML 已讀 point bounds 與資料連結；目錄時間不是實際檔案完整性證明 |

LT3 SHA-256 `ad566f8e48b0a3542153e5f2da478f801a18c114a8c76ba3462cdcbd957d1b68`；LT1 guide SHA-256 `f76541b6f4905a3cabf6f7a3373ccd55fb9e8e8f60492bb1f93b8b88aa1fc922`。暫存於本機 `/tmp/team1_earth_003/`，不加入 Git；GPU 可從官方端重取核對。FTP 實際成功；相同目錄的 HTTPS 嘗試於 15 秒逾時。瀏覽器不支援 FTP 不代表原始檔不存在。

NSIDC 要求引用資料集及使用子集；本輪沒有把第三方資料當專案原創，也沒有將專案程式授權套到它。尚未取得原始全文、現地新量測或新試驗許可／設備資訊，不安排實地作業。

### 本輪完成度與待辦

完成：只新增一個備案；固定 ID 與 point anchor；歷史現地證據；原始檔取得與來源 manifest；三地限制比較；用途查核包；**未啟用**的 GPU 需求。保留兩個既有案例的全部 CSV 欄值與歷史紀錄。

未完成：主線需求進 main、GPU 全表 QA／數值分析、隊友 2 用途查核、現代試驗區與獨立真值／材料控制。無新準確度、因果、冰損失、資源量或新穎性結論。本輪不改網站、Excel、Team 2、GPU、analog/ 或排名。

驗證：三個 ID 唯一；原兩列逐欄不變；原 58 欄保留；座標依角分重算；I-02 引用值等於 discovery JSON；所有 JSON 交接欄可解析；原始檔／guide hash 與首列核對；僅兩個 Team 1 責任檔案修改。這些是交接一致性檢查，不是科學 QA 通過。AI：OpenAI Codex 協助來源查找、文件比對與交接撰寫。

---

## 前次交接版本：TEAM1-ICE-REDO-v1（保留）

2026-11-14，Asia/Taipei。本輪版本：`TEAM1-ICE-REDO-v1`。研究需求：`TEAM1-PROVISIONAL-ICE-v1 / 2026-11-14`，**provisional**。

本輪先交付 **EARTH-002 → I-02：Elephant Head 監測站**，定位為有條件的方法參照候選，等待 GPU 資料 QA 與隊友 2 用途查核。保留 **EARTH-UV-001 → I-01**，接受隊友 2 查核，改列已知用途對照。兩者都沒有新穎性認證；未做實地測試、未重跑排名。本輪不提出第二個新地點。

## 1. 版本、責任與資料讀取範圍

- 工作根目錄：`/Users/clark/Documents/ChatGPT/big/NASA-Space-Apps-Challenge-2026-Taipei`。開始時為 main、無未提交修改；`git pull --ff-only` 同步至 `5901362d6347c71e0d41b84ebbb35685ca7b3911`，包含清理提交 `5901362`。
- main 尚無兩份 Team 1 檔案。僅從 `origin/team1/earth-analog-first-case-2026-11-14` 的 `5efa19766342a5a9ab24fcbbe3dbf02ed05805a6` 讀取自己負責的報告與 CSV；沒有合併整個分支或還原移除的排名。CSV 原有全部欄位保留。舊報告留在本文末尾作歷史紀錄，以本輪判定為準。
- 已讀選點 brief、Mars handoff、discovery JSON、reporting cards、cross-reference，以及 Team 2 報告與 CSV。`docs/earth_inventory.csv` 的 222 筆是隊友提供的檔案清單及讀取結果；本輪解析清單，**未取得或驗證其中的地球原始 raster**。
- `docs/research/main_research_requirements.csv` 在此版本不存在。另有 `docs/research_requirements.csv`，內容仍含先前沉積／硫酸鹽等需求，不能冒充新的冰探查需求。主要對話未提供新研究卡檔案，先依使用者本輪用途設定 provisional 需求。
- 新取得：EH1 原始論文 PDF、EH2 補充資料 PDF；後者只檢查頁數、欄位及樣本頁。沒有抽取整張時間序列、重算環境統計或修改 GPU 程式。
- 舊總 Excel 本輪未重新開啟。文末舊報告的 Excel／原始檔抽取說明是先前作者的歷史紀錄，不能當作本輪已驗證。
- 修改範圍限本報告與候選 CSV。README、Team 2、GPU、排名、總 Excel、網站均不修改。

## 2. 先回應 Team 2，再選新候選

依 main 中 [Team 2 報告](team2_novelty_audit.md) 與 [CSV](../../outputs/research/team2_novelty_audit.csv)，接受以下結果：

| 項目 | Team 1 回應 | 本輪處置 |
|---|---|---|
| University Valley 已有火星類比鑽探、分段取樣與控溫先例 | 接受山谷尺度的用途先例；不因 W 站座標不同就宣稱沒有重複 | EARTH-UV-001 改為 `known_use_reference`；ID、座標、原 `test_purpose` 保留 |
| W 周邊完整聯合流程與歷史鑽孔是否重疊未明 | 接受，站點錨點不等於已劃定試驗區 | 新試驗範圍、盲判與冰質量收支仍待定，不稱完整流程新穎 |
| I-01／I-02 的某些受查調查區不重疊，但提案清單不完整 | 接受，兩點都是條件式研究候選 | 不稱已確認冰、不稱新冰資源場址 |

既有 UV 數值沿用原交接且標示為 inherited，不新增「本輪重跑通過」。主研究、已知對照與待補證據是不同角色，沒有因新增 EARTH-002 而刪除 UV 的用途先例。

## 3. Provisional 研究需求轉譯

用途：研究乾燥覆土下冰膠結界面的辨識，並評估受控分段取樣的升溫與冰損失。這是 Team 1 的研究設計建議，尚未由主要對話定案。

| 類別 | 條件 | 依據與目前狀態 |
|---|---|---|
| A 必須 | 有可定位、直接支持覆土—冰膠結界面的現地證據 | 使用者用途要求；單靠低溫、PFR 或 SWIM 不算界面真值。EH1 支持站點結構；新試驗區仍須重新確認 |
| A 必須 | 地點、時間、量測方法與來源可追溯 | 使用者證據要求；已提供原始座標與來源定位 |
| A 必須，實驗執行前 | 有獨立界面真值、材料含冰量及樣品質量量測，才能驗證誤差／損失 | 由待測問題推得的必要觀測；現有資料不完整，不能稱測試就緒 |
| B 有幫助 | 同站不同深度的溫濕度、有不同於 UV 的條件，便於檢查方法能否轉移 | EH2 可交 GPU；不是場址合格門檻 |
| C 尚無合理門檻 | 最適冰深、容許界面誤差、最大樣品升溫／冰損失、坡度及設備功率 | 等主要對話提供儀器、任務與評估規格；不自行設數字 |
| D 重要限制 | Earth 構造已量測，I-02 仍只有指標；跨天體空間與物理量不同 | 禁止把方法參照寫成確認火星資源或全面環境相似 |

主要對話待決：選熱探針、雷達或其他方法？要做到何種深度／誤差？是檔案資料研究、環境艙，還是實地構想？如何測初始／回收含冰量？這些問題尚無答案，不阻礙本次文獻與交接。

## 4. EARTH-002 的固定身份與範圍

| 欄位 | 定義 |
|---|---|
| 固定 ID | `EARTH-002`，地點變動或用途修訂須留紀錄，不隨排序更名 |
| 火星配對 | `I-02`，53.75°N、42.25°E；只作本輪行政與研究問題對應，沒有計算證明比 I-01 更相似 |
| 名稱與別名 | Elephant Head monitoring station；補充資料標題為 Elephants Head Permafrost Site；Mount Dolence 北側，Ellsworth Land／Ellsworth Mountains，南極洲 |
| 原始定位 | EH1 Methods／Fig.1：79°49.213′S、83°18.860′W；換算北東為正：`-79.820216667, -83.314333333` |
| 座標慣例 | Earth 文獻地理經緯度，西經寫為負；原文未明示水平 datum／誤差，不宣稱 EPSG:4326 或九位小數精度 |
| 證據支撐範圍 | 已發表監測站的點位與該處地下感測器。不是整個 Elephant Head 地區；不外推到鄰近研究剖面 |
| 新候選測試區 | 尚未劃定。不能以文獻「距某調查點 10 m 內」當作試驗區半徑；未畫無來源的多邊形 |
| 代表性限制 | 可交接的是明確站點錨點；尚不是已核准、可實施的取芯區。近期冰況、現場變動、許可、費用與可達性都未知 |

## 5. 環境證據卡：量測、計算與未知分開

EH1 的直接現地證據：挖溝調查定位冰界面；監測站冰膠結界面 49 cm；乾永凍層頂約 13.5 cm 是作者以夏季最高溫內插的推估，並非另一個直接探測界面。土壤主要源於石英岩，夾少量千枚岩。站高 718 m；氣溫及 49 cm 年均分別為 −20.3°C、−19.2°C。這些是文獻值，不是本專案新量測或當前場址值。定位：EH1 PDF pp.2–5，Methods、Discussion、Tables I–II。本站與鄰近 Schaefer 剖面不混用。

| 四面向 | 可用資訊與資料支撐 | 邊界與未知 |
|---|---|---|
| 地形 Terrain | EH1 Fig.1／Methods 的已定位監測站與材料描述 | 無與 MOLA 同物理尺度 DEM 計算，無鑽機周邊坡度、石塊或承載力；不跨天體比較絕對高程 |
| 溫度 Temperature | EH1／EH2：2017-11-28 起逐時 air、3 cm、49 cm 溫濕度；回收日 2018-12-04，3 cm 於 2018-03-18 停止 | 3 cm 是地下溫度，不是 LST；無完整冬季 3 cm 年均。RH 原值／冰面修正值需區分；尚無本專案數值 QA |
| 水／冰 Water/Ice | 上述定位界面與量測方式 | 沒有新測冰純度、橫向連續性、厚度、體積、可採量或鑽採性能；不能推到整個地區或 I-02 |
| 大氣與沙塵 Atmosphere & Dust | 同站有 air T/RH；再分析只列計算需求 | 本站壓力、風、沉積、磨蝕及沙塵光學厚度未抽取；不填零，不把地球壓力環境當火星 |

EH3 已將 Elephant Head 與 University Valley 的地下冰／雪水汽機制放在一起研究。EH4 的出版者摘要報告 Elephant Head 微生物研究。這些都屬既有研究；低植被或乾永凍土不能稱無生命。EH3 的比較本身不能包裝為我們的新貢獻。

EH2 實際取得為 **108 頁 PDF 表格**，不是現成 CSV。第 1 頁可見 raw 與 corrected RH 欄，以及 `GMT-07:00`、`Local Time GMT-5:30` 兩個時標。時區意義須確認後才能轉 UTC／太陽時；不先假設兩者任一是 UTC。已讀前 3 頁欄位與樣本列，沒有逐列 QA 整份補充資料。

## 6. 與 UV 的差異、研究配對與限制

| 問題 | EARTH-UV-001 | EARTH-002 | 本輪意義 |
|---|---|---|---|
| 地區與角色 | McMurdo Dry Valleys W 站；已知用途對照 | Ellsworth Land 已知研究站；待查核的方法參照候選 | 不是小幅移動 UV 座標，也不是新發現地點 |
| 界面與熱背景 | UV 既有交接的 42 cm 及冷乾環境，沿用而未重算 | EH1 上述局部剖面與 EH2 時序 | 可規劃跨場址方法檢查；不是 I-02 深度或材料的重建 |
| 已有用途 | Team 2 確認山谷尺度分段鑽探與溫控先例 | 已有 Mars 類比、熱濕與微生物研究；新精確流程交 Team 2 | 兩者都不能宣稱首次火星類比 |
| 可能值得查核的差異 | 作已知參照與基準 | 在不同已量測背景下，盲判界面誤差及獨立冰質量收支是否已有同站實驗 | 具體差異尚未證實，不能只稱「更暖／更濕」就是新方法 |

**可研究的分層流程（提案，未執行）：**

1. 先由 GPU 恢復既有時序、檢查缺值與量測深度，用共同有效夏季時段描述兩深度的熱差與變動。這能描述已知剖面的反應，不能從兩個深度唯一反演冰深。
2. 若主要對話選定儀器，再設盲判流程：隱藏界面真值，固定演算法與輸入，以獨立取芯／剖面驗證深度誤差、漏判與誤判。現有公開資料不足以完成此實驗；需要新量測／合適標準樣本與校準。
3. 分段採樣另記樣品溫度、回收質量、處理時間與初始／最後含冰量，區分鑽頭溫度、樣品升溫、冰損失。現有熱濕表不能給出冰損失或質量平衡；需獨立實驗。

I-02 的既有指標從 JSON 原值複製至候選 CSV：`purposes.isru_shallow_ice.picks[1].layers`。坡度／起伏屬區域統計、TES 是熱慣量、SWIM 是一致性、CDOD 是粗尺度柱光學厚度。**沒有合格候選日夜地表溫度、現地界面或冰純度。**本輪未重跑這些資料，也未建立四面向分數。配對價值是協助定義「怎樣探查與驗證」，不是證明兩地環境相同。

無法天然模擬：火星低壓 CO₂、0.38g、輻射、完整季節／日夜熱循環、沙塵輸運。Earth 場址結果須另用模型／環境艙處理這些條件，不能直接推算 I-02 冰量、採水率、鑽採耗能或安全性。

## 7. GPU 交接：可直接依固定 ID 接單

狀態：**需求已寫入本報告與 CSV，待 GPU 接收並執行；沒有直接訊息或收件確認，不聲稱已跑完。** 所有工作限定 `EARTH-002`，不得更動本站身份或重新跑全球排名。

| 需求 ID | 輸入、期間、支撐 | 變數／問題 | QA 與交付 |
|---|---|---|---|
| GPU-EARTH-002-01 | EH2 PDF，站點逐時資料；實際終點依表核實 | 恢復列號、兩個原時標、三深度／高度的 T、raw RH、corrected RH | 逐頁表頭、跳列、重複、缺值、時區與 RH 基準；輸出 tidy table、source page/row、字典、hash、可重跑命令；人工對首／中／末列 |
| GPU-EARTH-002-02 | 上項 QA 後；共同夏季 2017-12-01 至 2018-02-28；annual air/ice 另列 | 3 cm 與 49 cm 同時有效資料的溫度範圍／差及覆蓋率；核對 EH1 Table II | 報有效 N、期間、單位、缺值；輸出配對圖和 QA 表；不補冬季 3 cm、不反演冰深或 TI、不設合格閾值 |
| GPU-EARTH-002-03（選配） | 實際取得地球 raster 後，2023–2024 背景；按原生格支撐 | MOD11C3 day/night/QC；MERRA-2 T2M/PS/U10M/V10M/DUEXTTAU | 報 native footprint、valid N、mask、單位／縮放；不得取代舊站點實測或直接比不同波長 CDOD |

先做 01，再做 02；03 不阻擋文獻用途交接。SRTMGL30、北半球 PFR 和本批 GLDAS 若不覆蓋此緯度，就記 `out_of_coverage`，不能取鄰近北方格補足。是否需要新的南極 DEM，由具體地形問題與可用資料再決定；本輪不增加重型資料主線。

CSV `gpu_requests_json` 含來源網址、SHA-256、變數、期間、問題與交付要求。欄位對照：`earth_candidate_id→candidate_id`、`earth_lat_deg→latitude`、`earth_lon_east_deg→longitude_east`、`test_purpose→research_question`、`site_extent_description→spatial_support`。原欄不刪，轉名保留原鍵。

## 8. 隊友 2 交接：立即可查的第一個新候選

狀態：**檔案已備妥供查核，尚未收到針對 EARTH-002 的回覆。** 請沿用 ID、站點錨點和本輪 provisional 用途；不得只用區域名稱判定同地點。

- ID／座標／範圍：見 §4；站點 point，沒有假設半徑或新試驗區。
- 精確用途：見 §6 的盲判界面＋獨立真值、分段取樣＋樣品溫度及初末含冰量；兩段尚未執行，是否聯合定案仍待主要對話。
- 原始來源：EH1／EH2 是直接站點證據；EH3 已有 UV–EH 比較；EH4 是微生物用途先例。
- 請查：（1）此站／重疊範圍是否已有盲判探查與獨立界面真值？（2）是否已有分段鑽採、控溫、樣品含冰量或冰損失實驗？（3）是否完整聯合，而非不同場址的流程拼接？（4）EH3 後，尚有什麼具體研究差異值得保留？
- 請分開回填觀測／科學研究／相同用途提案／已做實驗，記錄範圍與方法。找不到只能記本次未找到。
- 回覆後 Team 1 會依 ID 接受或提出具體證據修正，再決定主研究、待補證據或已知對照。若發現重複，優先改列對照，不換 ID 隱藏先例。本輪沒有預先判定其新穎。

CSV `team2_questions_json` 提供上述完整交接包；沒有修改 Team 2 自己的文件。

## 9. 原始來源與取得紀錄

以下來源均於 2026-11-14 取得／讀取。來源識別碼只在本 Team 1 檔案使用。

| ID | 原始來源／定位 | 實際讀取範圍與用途 |
|---|---|---|
| EH1 | McKay et al. (2019), [DOI](https://doi.org/10.1017/S0954102019000269)；[NASA 原文 PDF](https://www.nasa.gov/wp-content/uploads/2019/09/mckay_etal_2019_dry_permafrost_ellsworth_land21.pdf)；Methods／Fig.1 PDF p.2、Table I p.3、Table II p.5、Appendix pp.7–8 | 完整 PDF 已取得，讀相關方法／結果與限制；站點結構和量測證據。PDF 為作者稿式頁碼 1–8，期刊卷頁為 263–270。原文標示 CC BY 4.0，使用須署名 |
| EH2 | EH1 [出版者原始補充 PDF](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0954102019000269/resource/name/S0954102019000269sup001.pdf) | 108 頁；已讀前 3 頁欄位／樣本列、檢查無內嵌附件。未逐列抽取全表；不得稱完整 QA 或生成統計 |
| EH3 | McKay et al., [Summer snow determines the depth to ice-cemented ground…](https://doi.org/10.1017/S0954102025100448)；Environmental data、Table I、Results | 出版者 HTML 相關全文段落已讀；2025-11-27 線上發表、2026 年卷 38(2),122–134。用來界定既有比較與機制研究，不把它算成新站點觀測 |
| EH4 | Wood et al. (2024), [Active microbiota persist…](https://doi.org/10.1093/ismeco/ycad002)，Abstract | 僅以出版者摘要作已研究用途提醒；未完成其採樣範圍／補充資料查核，不能移用其樣本到新鑽孔 |
| M1 | [本地 Mars JSON](../../outputs/mars_discovery/mars_site_discovery.json)、[Mars handoff](../mars_discovery_handoff.md) | JSON 原值與定義；未重新處理原始 Mars raster |
| T2 | [Team 2 報告](team2_novelty_audit.md) 與 [CSV](../../outputs/research/team2_novelty_audit.csv)，包含提交 `8d99d9f` | 接受已知 UV 用途先例及兩冰候選的有限度提案範圍查核 |

EH1 SHA-256：`1d64eb94184a5e4fd7e8e0985a23a8c9a6e35ad2626f268ad8a3a80ffc21b6db`。

EH2 SHA-256：`20fe70f574bc394f05f0c720809f80a9602ac73f6ede34d322ea816cf25590d9`。

PDF 僅在本機暫存目錄取得，沒有加入 Git；GPU 應依穩定網址重取並核對 hash。資料使用條款須隨實際採用的補充資料／產品再核對，不能將專案程式授權覆蓋第三方資料。

搜尋紀錄：`Linnaeus Terrace dry permafrost ice table borehole coordinates Antarctic depth`；`Beacon Valley ice cemented ground dry permafrost borehole 3 m coordinates`；`"Elephant Head" "McKay" "2019" ice permafrost`；`"Elephant Head" "49" "coordinates" permafrost`。前兩者作證據篩選背景，沒有指派新 ID 或宣稱系統性排名。Elephant Head 的直接證據足以先交接，未繼續湊第二個候選。系統性用途／新穎性搜尋交隊友 2。

## 10. 完成度、待辦與驗證

| 項目 | 狀態 |
|---|---|
| 同步最新 main、保留清理；讀 Team 2 結果 | 已完成 |
| 保留 EARTH-UV-001 身份並接受已知用途對照 | 已完成 |
| 新候選 EARTH-002 點位、局部現地證據與有限度用途 | 已完成文獻交接；不是新地點發現或實地驗證 |
| 主要對話最終研究需求／門檻 | 待確認，provisional |
| GPU 與隊友 2 所需內容 | 已寫入兩份可讀檔案；待接收／執行／回覆 |
| 全表數值 QA、界面盲判、分段取樣／冰質量收支 | 尚未完成；沒有捏造結果 |
| 新取芯區邊界、當前冰況、許可／設備／費用 | 未知，需獨立規劃 |
| 第二個新地點、D-03／D-04 配對 | 本輪未做 |

檢查項目：兩個固定 ID 唯一；原 UV 座標／原用途保留；原 CSV 欄位全部保留；I-02 數值逐項等於 discovery JSON；新座標換算可重算；JSON 交接欄可解析；EH1／EH2 本機 SHA-256 核對；連結與僅兩個責任檔案的修改範圍檢查。這些是文件／數據引用一致性檢查，不是場址科學適用性測試或 GPU 統計 QA。

AI 使用：OpenAI Codex 協助檔案核對、原始來源讀取、座標換算與交接整理。科學主張回到列明來源；研究設計屬建議，未取得資料的欄位保留 unknown。

---

## 歷史附錄：前次 Team 1 第一組交接（原文保留）

來源 commit `5efa19766342a5a9ab24fcbbe3dbf02ed05805a6`。以下內容是歷史紀錄；其「尚未收到隊友 2」及舊原始資料讀取敘述已由本輪 §1–2 的狀態更新。不能據此復原已移除的排名或推論本輪執行過舊抽取。

# Team 1 地球類比配對｜第一組交接

研究日期：2026-11-14（Asia/Taipei）。版本：第一組，待隊友 2 查核。本文的「新用途配對」表示重新依冰探查用途評估地球場址，不表示場址、設備或用途具有新穎性。I-02、D-03、D-04 尚未完成配對，不能將本檔當作四組完成版。

## 1. 配對表

| 固定地球候選 ID | 火星候選 ID | 地點／國家或地區 | 地球座標（北、東為正） | 具體測試用途 | 判定 |
|---|---|---|---|---|---|
| EARTH-UV-001 | I-01：54.25°N, 1.25°E | University Valley 氣象站 W 周邊，McMurdo Dry Valleys，南極洲（不列為單一主權國家） | −77.862150°, 160.710100°；文獻原值 77°51.729′S, 160°42.606′E | 以已量測的乾燥覆土—冰膠結層界面，檢查熱探針／淺層探測判讀與分段鑽採的界面辨識、樣品升溫及冰損失 | 有條件的局部「方法／材料」類比；不是整體環境、地形或資源量配對 |

ID 固定代表此地球研究場址，不隨火星對象或排序改名。座標為文獻氣象站的定位錨點，不是新核准鑽孔；文獻未在本次讀取段落明示水平 datum，不聲稱六位小數代表測量精度。新採樣須另定位、確認現況及取得許可。

## 2. 已讀資料與用途重新評估

- GitHub connector 已查核主分支完整樹及原文：`docs/site_discovery_brief.md`、`docs/mars_discovery_handoff.md`、`outputs/mars_discovery/mars_site_discovery.json`、`docs/earth_inventory.csv`、`docs/cross_reference.md`、`docs/earth_pipeline.md`、`outputs/analysis/shortlist.csv`。基準 commit：`3e3ffff3d8d0814c407eacdc0a83d8b45a5123b8`。
- 總 Excel **只讀**：`NASA_Space_Apps_2026_All_Data.xlsx`，SHA-256 `a789fcdc9c0a7e780f85b63687ad54f05b87cd6e341ecf024375dcd6fcb3f731`。其 Overview 標示資料快照為 2026-11-14 15:42:59 +08:00。
- 先前指定的 `ice_candidate_followup_2026-11-14.md` 未見於此 GitHub 快照。Excel 的 `Report Text!A475:G505` 收錄其後續報告，來源路徑為 `docs/research/ice_candidate_followup/README.md`；`File Index` 第 65 列記錄原檔 SHA-256 `dd0556061d4fb2a89b1f0bef89112ff597142016326071ac2305a55fc3cd3689`。connector 對此新版路徑回傳 404。因此本次讀到的是 **Excel 英文轉存版本**，未冒稱已查得 GitHub 原始 Markdown。
- `Ice Candidate QA!A1:BB3` 提供兩個火星點的有效格數與深淺 SWIM 背景；`Earth Candidates!A1:AV73` 提供 72 筆版本化候選。舊 ID 必須連同 analysis version 使用；同名 ID 在 4 km、10 km 取樣版本可以是不同地點。
- 舊候選來自 100 × 100 km 地形視窗，水／冰欄仍為 unknown。六個已有 POWER 背景的中心即使氣溫低，也沒有直接的淺層冰深度、純度、連續性或採樣證據。故不直接沿用既有 Jezero/Gale/Arcadia 配對，不為冰探查用途強行選入。
- University Valley 是本次依直接冰層與量測證據補入的場址。舊搜尋限定 60°S–60°N，本來沒有搜尋此極區；未被舊名單收錄不是新穎性證據。

## 3. 火星 I-01 的比較依據

| 項目 | 已有資料 | 空間／期間與限制 |
|---|---|---|
| 地形 | 坡度 0.302596°；格內起伏 76 m | 0.5°名義格，約 29.64 × 17.31 km；MOLA 16 px/degree，坡度基線約 3.7 km。不是鑽機周邊地形或石塊尺度 |
| 溫度／熱性質 | TES 熱慣量 244.709671 J m⁻² K⁻¹ s⁻½ | 本地 2007 產品；產品年份不等於所有觀測年份。沒有此候選的合格日夜／季節地表溫度；熱慣量不是溫度或硬度 |
| 水／冰 | SWIM 淺層一致性 0.354307；原生名義格 100/100 有效 | SWIM 2.0，2021 產品，多源跨時期；名義原生格約 0.05°，先聚合再插值。數值不是 35.4% 冰、機率或已確認 <1 m 冰 |
| 大氣／沙塵 | MY35 年均 9.3 μm 吸收 CDOD 0.106878 | 原始重建支撐約 3°；0.5°只是共格。無本點近地風、壓力、沉積通量或磨蝕量 |

Excel QA 記錄：MOLA 64/64 有效；TES 93/100、7 個填充值排除；深層 SWIM 重取樣值 0.529793。這是既有 QA 的轉存記錄，本次未重跑火星管線；深淺 SWIM 共享輸入，不能算兩份獨立冰確認。來源：[GitHub 交接](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3e3ffff3d8d0814c407eacdc0a83d8b45a5123b8/docs/mars_discovery_handoff.md)、[原始 discovery JSON](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3e3ffff3d8d0814c407eacdc0a83d8b45a5123b8/outputs/mars_discovery/mars_site_discovery.json)、Excel `Ice Candidate QA` 第 2 列。

## 4. 地球配對證據、年份、解析度與缺漏

| 面向 | 地球可用證據 | 來源、年份、解析度 | 配對意義與缺漏 |
|---|---|---|---|
| 地形 | 岩質谷底的 W 站；約 1677 m 高程 | E1，2022 出版；現地站點，2009–2013 觀測 | 可布置界面探測剖面；沒有與火星相同尺度重算的坡度／起伏，不主張地形數值相等。絕對高程基準也不跨天體比較 |
| 現地溫度 | 文獻平均氣溫 −23.4°C；有表面、10、42、49 cm 溫度記錄 | E1；氣象系統 30 分鐘、另一組溫濕度感測器 60 分鐘；點測量 | 可測熱訊號與冰界面的關係。表面溫度有長段缺測及異常剔除；不能與 2023–2024 月資料當成同期驗證 |
| 水／冰 | W 站冰膠結界面在 42 cm；另有不同界面深度的測站 | E1 現地探針安裝深度；E2（2013）谷內調查報告 0–98 cm 冰膠結土深度範圍，屬離散調查，不是全谷連續冰圖 | 直接支持「乾覆土之下存在冰膠結層」的局部方法類比；不外推整個場址的冰量、純度、連續性或可開採量 |
| 地表溫度補充 | 桌面 MOD11C3.061：嚴格 QC 下日間 0/24、夜間 1/24 個月可保留；不產生年均或日夜差 | E4；2023–2024 月合成，0.05°；所選格中心 −77.875°, 160.725° | 品質篩選不足，不代表該地完全沒有觀測。網格混合谷地、坡面與冰雪；夜間唯一保留值 233.8 K 不是年均或極值 |
| 大氣 | 桌面 MERRA-2：PS 78,685 Pa；T2M 239.170 K；U10M +10.727、V10M +2.351 m/s | E3；2023–2024，24/24 月有效，按月天數加權；0.5° × 0.625°，最近格中心 −78°, 160.625° | 再分析背景，不是 W 站實測。T2M 與文獻氣溫時期、高度、支撐範圍不同；風分量不是平均風速或陣風 |
| 沙塵 | 同格 MERRA-2 DUEXTTAU = 0.002139，24/24 月有效 | E3；2023–2024 月資料，550 nm 沙塵消光光學厚度，再分析 | 不能直接與火星 9.3 μm 吸收 CDOD 相減；沒有本地沉積／磨蝕量，不配對沙塵耐受測試 |

**桌面資料的使用邊界：**本組實際開啟並抽取 24 個 MOD11C3、24 個 MERRA-2 SLV、24 個 MERRA-2 AER 檔。MODIS 關閉自動縮放後檢查原值 7500–65535、`QC == 0`，乘 0.02 得 K；這是全部品質位元均為最佳類別的保守篩選。MERRA-2 依檔內座標取最近格，遵守填充值遮罩，以 2023–2024 各月天數加權；不插值成站點實測。原始檔全部只讀。

SRTMGL30 本批範圍未涵蓋此南極緯度；ESA CCI Permafrost 本批為北半球產品，不能用其缺值推論此地無永凍土。GLDAS 本批緯度範圍不包含本站。GPM 降水、NDVI、VIIRS 氣膠與 MERRA 輻射資料不提供本站地下冰深度真值；本組未將它們計入冰存在證據，也未宣稱已完成這些產品的本站 QA。資料存在、可開啟和支持特定用途是不同層次。

## 5. 具體可測試什麼

以下為 **Team 1 提議的測試設計**，不是已執行結果，也不表示文獻已驗證這個火星點：

1. 在經重新確認的乾覆土—冰膠結層剖面，先做盲判熱探針／淺層探測，再用實際取芯界面深度驗證。記錄界面深度誤差、漏判、誤判與有效剖面長度，不能把低溫當成標準答案。
2. 固定鑽頭、轉速、推力與每段進尺，分段記錄扭矩、功率、鑽進速率、樣品溫度、回收質量與採樣前後含冰量。可檢查乾土進入冰膠結土時的辨識與取樣損失；功率單獨不能轉為冰含量或硬度。
3. 用已知界面深度、粒徑、密度與含冰量樣品，檢查熱訊號反演的多解性。未建立可信熱物性模型前，不把本站設定為 TES 熱慣量 244.71 的等效材料。

E5 證明相關鑽採／樣品處理系統曾在極地類比及火星環境艙測試，提供方法依據；不能把該研究的鑽進性能移植到新鑽孔或 I-01。現地作業仍需確認許可、樣品取得與現況；本交接不安排出隊。

## 6. 相似處與不能模擬處

**證據支持的相似處：**地球場址有乾燥覆土覆蓋冰膠結土，可用來研究「先探查、再取樣驗證」的方法。I-01 的資料只支持對可能淺層冰做後續探查，因此這是對研究問題的配對，不是已知地下構造的一對一重建。

**重要差異：**地球端有現地界面證據，火星端仍是多源指標；地球站點／剖面遠小於火星格點。南極氣象、雪霜、水汽、日照季節及粒料組成都未與 I-01 配準。兩地熱慣量、冰純度、覆土連續性與力學性質尚未建立相等關係。

**不能模擬：**火星低壓 CO₂ 大氣、低重力、輻射、完整日夜／季節熱循環、火星沙塵啟動與沉積。地球現地試驗不能直接給出火星昇華損失、鑽採耗能、水產量或安全著陸結論；需獨立環境艙與模型驗證。低溫／永凍土不等於可挖冰。

## 7. 來源索引

| 來源 ID | 可查核來源／讀取範圍 | 本組使用方式 |
|---|---|---|
| E1 | Marinova et al., **2022**, [Climate and energy balance of the ground in University Valley, Antarctica](https://doi.org/10.1017/S0954102022000025)，Antarctic Science 34(2), 144–171；Methods: Meteorological measurements、Results、Fig. 1 | 站點原座標、現地溫度、冰界面、量測間隔及缺測；已讀公開全文相關段落 |
| E2 | Marinova et al., **2013**, [Distribution of depth to ice-cemented soils…](https://www.cambridge.org/core/journals/antarctic-science/article/abs/distribution-of-depth-to-icecemented-soils-in-the-highelevation-quartermain-mountains-mcmurdo-dry-valleys-antarctica/EE34F569F8E954EE4DE86125C92E3188) | 已讀出版者摘要；0–98 cm 是調查範圍，不當作 W 站當前冰深度；未取得逐點資料，不指定調查點間距 |
| E3 | [NASA GMAO MERRA-2](https://gmao.gsfc.nasa.gov/gmao-products/merra-2/)；桌面 `air/MERRA2_400.tavgM_2d_aer_Nx.202301.nc4` 至 `202412.nc4`、`air/wind_pressure/MERRA2_400.tavgM_2d_slv_Nx.202301.nc4` 至 `202412.nc4` | 本次只讀抽取的 24 月再分析；來源年份指觀測／再分析期間，不是下載日；網格、變數及單位直接讀檔 |
| E4 | MOD11C3.061，[產品 DOI](https://doi.org/10.5067/MODIS/MOD11C3.061)、[NASA/LP DAAC 使用指南](https://lpdaac.usgs.gov/documents/118/MOD11_User_Guide_V6.pdf)；桌面 `temperature/MOD11C3.A2023*.061.*.hdf`、`A2024*.061.*.hdf` | 24 月 HDF 原檔、結構 metadata、比例因子與 QC；產品 DOI 網頁本次回傳 403，未把網頁無法開啟當作檔案不可讀 |
| E5 | Zacny et al., **2013**, [Reaching 1 m Deep on Mars: The Icebreaker Drill](https://doi.org/10.1089/ast.2013.1038)；[PubMed 作者摘要](https://pubmed.ncbi.nlm.nih.gov/24303959/) | 已讀摘要的鑽採／取樣測試方法背景；不引用其性能作為本站新測試結果，不做新穎性結論 |

## 8. 隊友 2 交接狀態

- 第一組鍵值：`EARTH-UV-001` + `I-01`；配對表見 `outputs/research/team1_earth_analog_candidates.csv`。來源文獻、原有資料和本次提議分開記錄。
- 請查核相同場址、相同測試用途的既有工作，以及來源是否支持本文主張；特別注意 E5 已有鑽採方法研究。Team 1 不給新穎性結論。
- 請保留候選 ID，以此鍵值回填查核意見；如需換測站或測試用途，先記錄修訂，勿用新 ID 隱藏來源變更。
- 狀態：第一組已備妥供查核，尚未收到隊友 2 的查核結果。I-02、D-03、D-04 留待第一組交接後依原順序處理。

本次僅新增這份研究文件及候選 CSV；未修改 `analog/`、評分權重、排名、網站、總 Excel 或既有科學輸出。OpenAI Codex 協助資料讀取、來源查核與交接撰寫。
