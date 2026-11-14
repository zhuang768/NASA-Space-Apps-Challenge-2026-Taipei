# MS-03 地球類比場址研究與用途查核

Team zasa｜初版2026-11-14；最後核對2026-11-15｜PR #7研究交付

**閱讀順序：** 前段最新MS-03／AD1處置及2026-11-15時標交接為目前有效限制；「2026-11-14初版紀錄」之後保留歷史內容，已被新版取代的取得狀態不可作為現況。所有驗證通過只限列明的結構與重現檢查，未確認感測器真實時刻或偏移原因。

## 2026-11-15交接：149份標籤結果、取整假說界線與根因缺件

交接基準SHA **`8f6d3134bc5bfef6e83a4caddb1d602872d40708`**。本節整理已執行的核對，不新增下載、時間修正或因果分析。原始核對與先前交接保留於後方。615筆負經度警示已由緯度排除，舊「615筆位置未知」說法已被取代；這個已釐清事項與下列生成根因未知分開處理。

### 給主要對話：可引用結論與不能擴張的內容

> 本組取得149個重複PRODUCT_ID的149份現行公開PDS標籤，與固定索引內每個產品的兩個指令起始時間比較。78組與現行標籤的整秒floor／ceil相容，71組不相容。另有29組的兩個索引值相差超過1秒，排除「全部差異僅由同一時刻的整秒取整造成」這個受限單一解釋。這沒有確認另一個根因，也不能用78組相容結果選取時間。實際2026執行版、SQL／來源版本及建置日誌尚未取得，149組重複列的生成機制仍為unknown。

**數字的單位：** 149是產品／重複組／標籤份數，對應75個Observation ID，包含同一觀測的RED與COLOR產品，不是149次獨立觀測或獨立時鐘驗證。29組是上述71組中的子集；78、71、29不能相加作總數，也不是機率、錯誤率或準確度。

主要對話可將本輪定位為「索引來源追溯與受限假說診斷」。可說公開版本字串已核對、149份標籤已取得、單一整秒取整不足以解釋全部差異；不能說已確認SQL join bug、distinct計數、官方校時錯誤、索引已修復，或2026確實使用文件顯示的某一版。文件產生時間、影像PRODUCT_VERSION_ID與實際索引執行版本不可混用。

這些核對沒有改變MS-03固定範圍的目錄交集結果，沒有新增格內地貌或地下冰證據。AD1維持一般方法參照、退出目前具體配對；MS-03形貌維持unknown。此處HiRISE指令時間差不解除Campbell／HOBO的配時限制。

### 交接證據入口

| 連結 | 實際內容與讀取限制 |
|---|---|
| [149組逐筆比較CSV](../../../outputs/research/MS-03/morphology/evidence_followup/generator_followup/duplicate_label_time_comparison.csv) | PRODUCT_ID、原索引兩行及兩時間、實際標籤URL、大小、SHA、標籤指令時間與相容旗標。只比較指定欄位，沒有校正欄 |
| [診斷摘要JSON](../../../outputs/research/MS-03/morphology/evidence_followup/generator_followup/duplicate_label_time_summary.json) | 149／149取得、78相容、71不相容、29組大於1秒、假說定義與不可推論事項 |
| [149份來源標籤ZIP](../../../outputs/research/MS-03/morphology/evidence_followup/generator_followup/duplicate_source_labels.zip) | 實際取得的PDS `.LBL`，非生成圖片／補寫標籤。ZIP SHA256 `aaea677542b323640935f66450e9ebba825e2a534fc54fa272b50c9d6e23d34b`；逐檔SHA在CSV |
| [取得／比較程式](../../../scripts/research/MS-03/check_hirise_duplicate_label_times.py) | 只抓149個已知產品標籤；讀`MRO:OBSERVATION_START_TIME`，缺少時不以`START_TIME`代替；保留兩個索引時間，不產生校正表 |
| [公開版本與實讀範圍](../../../outputs/research/MS-03/morphology/evidence_followup/generator_followup/public_version_trace.json) | 官方文件ID、文件產生時間、來源URL／SHA與未取得材料；不是2026執行版證明 |
| [原149重複組逐欄核對](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/duplicate_product_audit.csv) | 同PRODUCT_ID僅指令起始時間不同；其他53欄包含路徑與幾何相同。保留原表行號 |
| [固定索引取得紀錄](../../../outputs/research/MS-03/morphology/evidence_followup/index_download_manifest.json) | 原表URL、168,675,271bytes、SHA256及回應標頭。完整索引未加入Git，不能稱所有原始輸入都已在GitHub |

### 已排除的假說，精確到哪裡？

假說限定為：兩個索引值都來自**同一個未改變的時刻**，唯一差別是取整到整秒的floor／ceil／nearest。這類結果最多差1秒；29組相差2或3秒，因此不能用這個假說單獨解釋全部149組。

這不排除取整曾是處理鏈中的一個步驟，也不排除不同輸入版本、其他時間處理或查詢結果差異。78組只表示對**現行標籤值**相容；71組只表示兩值無法同時符合該現行標籤的floor／ceil。現行標籤未必是當次建置輸入版本，不能據此指定原表哪一列錯誤或給替代根因下定論。

### 仍缺的決定性材料與各自用途

| 缺件 | 要取得的具體內容 | 有了才能確認什麼 |
|---|---|---|
| 實際2026執行版 | 該次建置使用的jar／class或source revision、SHA、呼叫方式與必要相依版本；能連到2026-11-03那份索引 | 確認真正執行哪一版與哪段生成邏輯，而非以Javadoc推定 |
| 實際SQL／設定與來源版本 | RDR cumulative-index查詢原文與有效設定、相關資料快照／版本，尤其149組PRODUCT_ID對應來源列及指令時間；不需要帳密 | 確認重複是否已出現在查詢輸出、在哪些欄位／版本形成；檢驗任何join／distinct假說 |
| 同次建置日誌 | 查詢回傳、分批／寫檔、實寫列數、unique ID計數及label更新紀錄；可串接205,451物理列、205,302產品與149個差異組 | 定位「取資料→寫表→計數→更新label」哪一步產生不一致，並核對是否為同一次建置 |

公開文件與現行標籤不能替代這三組材料。本聊天室未取得、未向發布方發送訊息，也未把「本次未取得」寫成官方沒有保存。主要對話若要繼續追因，可直接用此表作取得清單；本輪交接完成不代表根因已解決。

### 給GPU：可重現工作、禁用操作與解除條件

- **可以做：** 從CSV與來源ZIP重現149份檔案／產品ID核對及78／71／29統計，保留source line、兩個時間與原標籤SHA。若重抓公開URL，另存取得日期與新SHA，不能靜默覆蓋本交接快照。
- **比較欄位：** 索引`OBSERVATION_START_TIME`對標籤`MRO:OBSERVATION_START_TIME`，兩者是指令起始時間；`START_TIME`是第一影像列取得時間，不能缺值替代。原表兩列都保留，不因label較精細就直接宣布其為當次建置真值。
- **確認前不能做：** 以78組相容就自動選floor／ceil、挑第一列去重、校正索引時間或估算錯誤率；從71組不相容推定SQL bug；把29組當第三個互斥類別；把產品份數當獨立觀測樣本數；將此結果套到Campbell／HOBO配時。
- **缺件到齊後：** 先封存執行版、查詢設定、來源快照及日誌的版本／SHA；逐步比較查詢原結果、寫出的各列與label計數，定位差異首次出現的步驟。若要產生修訂表，須有可引用的重現規則、逐列處理旗標及原值保留；在證據成立前維持unknown。

**交付狀態：** 已整理供主要對話與GPU從本報告及PR #7讀取，未對外通知、未改其他人的檔案；原數據、時間、科學圖與既有配時限制不變。只推原分支，先不合併main。


## 2026-11-15生成元件追查：公開版本可核實，2026實跑版／SQL與根因仍未知

接續SHA `3321765dc0cd24316e7e12d30b4ade803fa67fcd`。這輪沿官方軟體子系統、HiVolume套件、生成元件及常數頁追查，並實得149個重複產品的原始PDS標籤。**新增可確認的公開版本線索與時間差診斷，但沒有取得2026那次建置的執行檔、SQL／設定或日誌；不能宣布149組重複列的生成原因已解決。** 615筆負經度警示已由緯度排除的結論不變，舊「615筆位置未知」仍屬已取代說法。

### 公開版本與實際執行版必須分開

[官方constant-values頁](https://pirlwww.lpl.arizona.edu/software/HiRISE/Java/constant-values.html)的ID欄實際讀到：

| 元件 | 公開文件ID所載版本／時間 | 可確認與限制 |
|---|---|---|
| Index_Builder | 2.18／2016-04-07 23:07:15 | 是公開文件中的類別識別值，未與2026-11-03輸出建立執行鏈 |
| IndexBuilder | 1.3／2017-02-16 21:17:07 | 同上，不能因文件近期產生就稱此版已實跑，也不能斷言它未被使用 |
| HiVolume | 2.21／2017-02-16 21:20:27 | 文件說明GUI可更新／重建PDS索引，沒有給本次操作紀錄 |
| PDS_Release | 1.9／2025-02-13 20:57:27 | 其他發布元件的ID，不能拿來當IndexBuilder版本 |

頁面註解記載Javadoc 1.8.0_442於`Mon Oct 26 12:11:03 MST 2026`產生。這是**文件產生時間**，不是程式編譯／部署或索引建置時間。索引54欄中的`PRODUCT_VERSION_ID`描述影像產品版本，也不是索引生成器版本；該索引沒有SQL、生成器build hash等可直接接回實跑版本的欄位。

[版本、文件SHA與實讀範圍](../../../outputs/research/MS-03/morphology/evidence_followup/generator_followup/public_version_trace.json)保留來源連結與限制。已沿[官方軟體子系統頁](https://pirlwww.lpl.arizona.edu/software/HiRISE/)、HiVolume package／class及IndexBuilder文件追查，未在本次已讀公開頁面取得生成方法實作、實際RDR查詢SQL或部署設定。`PDS_Release`文件出現的SQL LIKE跳脫輔助函式，並不等於RDR生成器的SELECT／JOIN／DISTINCT查詢。沒有登入HiCat後端或存取非公開設定，也沒有以其他同名資料庫專案補作來源。

### 149份產品標籤：可排除單一取整解釋，仍無法選定真值

全部149個重複PRODUCT_ID的現行公開`.LBL`已取得，未改原索引；逐一讀`MRO:OBSERVATION_START_TIME`與兩個索引`OBSERVATION_START_TIME`比較。這是**同一種指令起始時間欄位**的來源對照；沒有拿第一影像列的`START_TIME`冒充指令時間，也沒有把它當獨立時鐘真值。

| 本輪實際檢查 | 結果 | 正確解讀 |
|---|---:|---|
| 標籤取得／可讀 | 149／149 | 都有可讀的MRO:OBSERVATION_START_TIME；網址、大小、SHA逐筆保存 |
| 兩個索引時間都落在現行標籤時間的floor／ceil整秒值 | 78組 | 僅為與該取整規則相容，不能證實原程式做了取整或任選其中一筆 |
| 兩值無法同時落在上述兩個整秒值 | 71組 | 相對現行標籤不相容，原因仍可能涉及不同來源版本或其他處理；未確認是哪一種 |
| 兩索引值相差超過1秒 | 29組 | 若唯一差異只是把同一時刻作整秒floor／ceil／nearest，兩值最多差1秒。因此這29組排除該受限的「唯一原因」假說；不排除取整曾參與其他階段 |

[149組逐筆比較CSV](../../../outputs/research/MS-03/morphology/evidence_followup/generator_followup/duplicate_label_time_comparison.csv)、[診斷摘要與假說界線](../../../outputs/research/MS-03/morphology/evidence_followup/generator_followup/duplicate_label_time_summary.json)、[原標籤ZIP](../../../outputs/research/MS-03/morphology/evidence_followup/generator_followup/duplicate_source_labels.zip)及[取得／比較程式](../../../scripts/research/MS-03/check_hirise_duplicate_label_times.py)可重現。現行產品標籤未必是當次索引生成使用的輸入版本，所以71組不相容不能直接命名為SQL join bug或資料庫多版本bug。

### 本輪能下的結論與仍缺的決定性證據

**已知：** 公開文件ID與文件產生時間可追溯；149份標籤實際取得；全部差異不能只用同一時刻的整秒取整單獨解釋。**仍未知：** 哪個IndexBuilder執行版產生2026輸出、實際查詢SQL／設定，以及149組資料如何在生成鏈中分叉。公開文件與輸出模式不能代替執行證據。

若要把根因變成可確認，需要同一次建置可串起的三組材料：①執行jar／class或source revision及雜湊；②實際RDR累積索引查詢與設定、相關資料版本／快照；③寫出與計數日誌，可對照205,451物理列、205,302產品及149個差異組。由此逐步重現「查詢結果→寫表→計數→更新label」，才可判定重複發生在哪一步。這些材料本次未取得；不以未找到推定官方未保存，也未發送對外詢問。

**交接：** 主要對話可引用「版本線索及受限假說已有核對，2026執行鏈與根因仍未知」；GPU保留149組時間欄與來源旗標，不以78組相容就選值、不覆寫原表、不把本輪推定轉成通用校時。AD1降級、MS-03形貌unknown、Campbell／HOBO配時禁用均維持。PR #7先不合併main。


## 2026-11-15正式交接：HiRISE索引已釐清事項、未知與新增證據

交接基準SHA `c6f9b93aa9ff5a471a8f67fbdf40f0922e508b84`，來源仍固定為168,675,271bytes／SHA256 `d58cf52657371f6a7e65ef4dc687fdd2f9c70e276f7755853e27971f17df4126`的任務索引。**舊說法「615筆位置未知／615筆無定位」已被本交接取代。** 舊檔案與當時判斷保留供追溯，不作目前狀態。

### 已釐清與仍未知

| 問題 | 目前狀態 | 證據與界線 |
|---|---|---|
| 615筆為何被標invalid？ | **已釐清：本組0–360°格式檢核將負經度標為警示** | 615筆均有有效緯度且不在57.50–58.00°N；來源標籤抽核也確有負經度。不是615筆缺失定位。[逐列重新分類](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/negative_longitude_reclassification.csv) |
| 205,451與205,302的數量差？ | **數量已釐清：149組重複產品各多1列** | 205,302個unique PRODUCT_ID；每組僅OBSERVATION_START_TIME不同，其他53欄相同，包括圖檔路徑及幾何。[149組核對](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/duplicate_product_audit.csv) |
| 這兩項問題是否藏了格內紀錄？ | **固定索引內影響已核對，沒有發現漏列** | 讀完205,451列，未依label count截斷；305列緯度相交紀錄的經度查核均不相交。無須把615筆負值強制轉換，也未選擇重複時間真值。[305列](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/latitude_eligible_rows.csv)、[整體判斷](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/resolution_summary.json) |
| 現行鄰近產品標籤是否改變判斷？ | **本輪新核對：所選10產品／5次觀測均不相交** | 在上述緯度相交列中，另選與237–247.5°E相交的產品作鄰近抽核，10份原標籤全取得、均不進入指定格。[下載、雜湊、標籤邊界](../../../outputs/research/MS-03/morphology/evidence_followup/index_handoff/neighbour_label_check.json)。5°緩衝是本輪設計取樣，不是保證涵蓋最大定位誤差；未核對所有產品標籤 |
| 哪個官方元件負責建立索引？ | **本輪新取得公開元件文件；實際2026執行版未知** | 官方[Index_Builder](https://pirlwww.lpl.arizona.edu/software/HiRISE/Java/HiRISE/HiCat/HiVolume/Index_Builder.html)說明建立PDS索引表並更新標籤記錄數；[IndexBuilder](https://pirlwww.lpl.arizona.edu/software/HiRISE/Java/HiRISE/HiCat/HiVolume/IndexBuilder.html)也列RDR寫出介面。這是文件，不是取得方法實作、部署紀錄或SQL。[實讀範圍](../../../outputs/research/MS-03/morphology/evidence_followup/index_handoff/generator_documentation_reading.json) |
| 為何生成149組重複列、標籤如何計數？ | **仍未知：只確認輸出對應，未確認生成機制** | 尚缺實際執行版、SQL／設定與生成日誌。不能以unique數恰好等於label宣告，就稱已證實distinct計數、資料庫join bug或取整bug。原始physical ROWS不一致仍未被修復 |
| 是否所有HiRISE都沒拍到本格？是否沒有多邊形？ | **仍未知，不能由目錄結果推出** | 未發布、未列入或來源幾何錯誤仍不能完整排除；未取得足以量測的格內HiRISE影像。現有CTX局部與取樣尺度不足以確認AD1式網路，不能作整格不存在判斷 |

### 給主要對話：可直接引用與下一步

> 針對固定版本HiRISE累積索引，先前615筆警示已釐清為負經度格式檢核問題，全部可用緯度排除MS-03。149個額外列來自重複產品ID，空間欄位相同，未在本次完整列讀取中造成MS-03相交產品漏列；另核對10份鄰近產品原標籤也均不相交。這些是索引適用性與資料追溯結果，不是「所有觀測皆無覆蓋」或「格內沒有多邊形」的證明。AD1仍為一般方法參照，退出目前具體配對，MS-03形貌保持unknown。

主要對話應將總結中的「615筆仍待定位」改為「已由緯度排除；其餘未知是上游生成與目錄完整性」。目前不必為這615列等待定位補件。若要追上游根因，需要索引發布方提供該次建置的程式revision、實際SQL／設定、重複產品來源資料版本與記錄數計算日誌；本聊天室沒有發信或取得回覆。若要恢復具體類比配對，需要可清楚辨識完整邊界且精定位的格內影像，而不是更多格外照片或調整名義格。

不得把文件寫成已確認全球首次、已證明所有HiRISE無覆蓋、已修正官方索引、已完成幾何獨立真值驗證，或已看到多邊形／地下冰。新取得的元件文件只縮小了應查證的位置，沒有解決其執行機制。

### 給GPU：可用輸入、操作界線與後續條件

1. 先核對固定來源SHA與每列821bytes，讀完整實表，不以LABEL ROWS截斷。原表未修改，大表仍只在本機暫存，GitHub交付的是查核結果、來源與程式。
2. 將舊`HiRISE_invalid_bbox_rows.csv`視為歷史strict-format警示，讀[重新分類表](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/negative_longitude_reclassification.csv)取代「位置未知」。先用有效緯度排除；負經度不能自動當NaN。涉及跨零、極區或其他格時，需另核對慣例，不把本格排除規則當通用投影修復。
3. 若未來需要去重，同PRODUCT_ID的幾何、路徑、版本及時間差必須先比較；保留來源行號與差異旗標。本輪沒有去重覆寫原表，也沒有任選指令時間或產生校正檔。
4. 可重跑[索引異常核對程式](../../../scripts/research/MS-03/audit_hirise_index_anomalies.py)及[鄰近標籤查核程式](../../../scripts/research/MS-03/check_hirise_neighbour_labels.py)。後者只檢查已定義的10產品，不是全局檢索或有效像素驗證。來源變動時先保留新舊版本，不將原SHA成果靜默更新成最新結果。
5. 形貌分析入口仍是[覆蓋／判讀圖](../../../outputs/research/MS-03/morphology/MS03_AD1_coverage_interpretation.png)、[可辨識性比較表](../../../outputs/research/MS-03/morphology/observability_comparison.csv)及[方法說明](../../../outputs/research/MS-03/morphology/README.md)。沒有格內可可靠追描的網路，就不產生Mars面積／圓度／相似度分數，不把AD1值或零值填入unknown。
6. 即使未來形貌相近，成因與冰判讀仍需同位材料／層序、重訪／立體地形與獨立地下結構證據。此處HiRISE指令時間差與地球Campbell／HOBO分開；既有配時禁用維持。

**交接狀態：** 已備妥供主要對話與GPU從PR #7讀取，未對外發送訊息，未改其他人的檔案。這輪已把「鄰近現行標籤是否仍在格外」及「公開生成元件的職責」補成有來源的結果；執行版／SQL根因、未列入觀測完整性及格內地貌仍待真正資料。不能用交接完成代替科學未知已解決。先不合併main。


## 2026-11-15續查：615筆格式警示與149列計數差的影響已釐清

接續SHA `115576b51e1a7c89d2d9cd75ae667d4da4ad96c0`，使用原已取得的HiRISE累積索引固定SHA256 `d58cf52657371f6a7e65ef4dc687fdd2f9c70e276f7755853e27971f17df4126`。**這兩個異常未在實際取得的索引內隱藏MS-03相交紀錄；未發布／未列入產品或來源幾何錯誤仍不在可排除範圍。** AD1維持降級，MS-03格內形貌維持unknown，沒有新增影像判讀或地下冰證據。

### 615筆的原因：本組檢核過嚴，不能稱為615筆缺失定位

前輪將經度限定0–360°，把含負經度的615列標成invalid bbox。此次全列核對發現：615列的target均為MARS、緯度均為有效數值；其中500列兩個經度值皆負，115列原值跨零。**原先「無效邊界」是本組格式檢核未通過，不能直接當成來源產品無定位。** 這裡不替全部產品強制轉換經度。

以緯度先做篩選，615列全部與57.50–58.00°N不相交，無須依賴經度換算即可排除本格。最近一列`ESP_019584_2365_RED`的索引緯度55.9312–56.0484°N，距本格南界仍約1.4516緯度度。已實得其原始PDS標籤，確認planetocentric、east-positive、緯度約55.931191646–56.048363042°N，且標籤本身確實使用負經度，支持其在本格外的判斷。

另取跨零`TRA_000846_2475_RED`、極區`PSP_010545_2700_RED`及重複產品樣本`PSP_001460_1425_RED`的原標籤，均在本格緯度外。極區樣本的索引與現行標籤邊界有小差異，未強行調和，兩者仍遠離本格；不能把這4份抽核寫成615份標籤全部核實。

來源與輸出：[四份原標籤及下載URL／雜湊](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/product_label_downloads.json)、[615列重新分類](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/negative_longitude_reclassification.csv)。舊的`HiRISE_invalid_bbox_rows.csv`保留為歷史警示清單，以本節重新分類為準，不再將其全部列為「位置仍未知」。

### 筆數差：實表有149組重複產品ID，生成原因仍未知

| 核對項目 | 實際結果 |
|---|---|
| 實表物理列數／每列大小 | 205,451列；每列821bytes，檔案168,675,271bytes |
| 不重複PRODUCT_ID | 205,302個，恰等於標籤宣告ROWS／FILE_RECORDS |
| 重複組 | 149個PRODUCT_ID各出現2次，形成149個額外列；不是把RED與COLOR誤算成重複 |
| 每組不同欄位 | 54個欄位中只有`OBSERVATION_START_TIME`不同；`START_TIME`、圖檔路徑及空間欄位相同 |
| 兩列指令起始時間差（第二減第一） | −2秒10組、−1秒88組、+1秒32組、+2秒4組、+3秒15組；未任選其中一個為真值 |

例如`PSP_001460_1425_RED`位於原表391／392行，同一產品的指令起始時間為05:26:24與05:26:25。其原標籤`MRO:OBSERVATION_START_TIME`為05:26:24.519，但這一例不能解釋其他全部重複列，也不能把1–3秒差異統稱為已證實的取整規則或實際校時。

**數量差已由149個額外重複列完整對應；標籤如何生成仍未確認。** 標籤宣告的physical ROWS仍不符合實表，不將「恰等於unique ID數」寫成已讀過官方生成程式或證實採distinct計數。帶`Cache-Control:no-cache`重取的標籤與前次逐位元相同；表格HEAD的大小、ETag及Last-Modified也與前次取得紀錄一致，單次重新請求沒有消除差異。

本次搜尋官方[ERRATA](https://hirise-pds.lpl.arizona.edu/PDS/ERRATA.TXT)中的duplicate／index／start-time等字詞，閱讀2012 INDEX Table Updates等相關段落，未找到專門解釋這149組紀錄的文字；未取得上游索引生成程式，不宣稱已確定是發布、資料庫或快取bug。[重複組逐欄核對](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/duplicate_product_audit.csv)、[標籤重新取得紀錄](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/label_refresh.lbl.retrieval.json)、[表格HEAD核對](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/table_header_recheck.json)保留可追溯依據。

### 是否可能因此漏掉MS-03格內影像？

本組實際解析全部205,451列，**沒有依標籤的205,302截斷讀取，也沒有先去重而捨棄不同幾何。** 全表緯度欄皆有效；305列的緯度與本格相交，它們的經度原值均在0–360°，逐列範圍查核仍為0筆MS-03 bbox交集。[305列檢查表](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/latitude_eligible_rows.csv)包括原行號，可人工抽核。615個負經度警示列全部先由緯度排除；149組重複列的幾何完全相同，不會因保留哪一組而改變本次範圍結果。

**可說：** 對這份固定索引，先前615筆格式警示與149個額外列已完成範圍影響核對，沒有發現因這兩項問題而漏列的MS-03相交產品。**不能說：** 所有HiRISE觀測都未拍過MS-03、所有原始幾何都經獨立驗證、表格發布原因已完全解決，或格內沒有多邊形。目錄無交集仍不是地貌不存在證明。

### 給主要對話與GPU的更新

- **主要對話：** 以上結果取代後方「615筆仍位置未知、筆數差尚無數量解釋」的舊狀態；保留AD1一般方法參照與既有形貌未知結論。現在不必僅因這615列而等待定位補件，但未發布／未列入觀測的完整性仍未知。
- **GPU：** 先讀完整實表並驗證821bytes與SHA；先核對緯度，再處理經度慣例，不能以負值直接標成缺失定位，也不能依LABEL ROWS提前停止。本次不改原表、不選取或校正重複列時間、不生成新影像或重新配對。若未來需要去重，先核對同PRODUCT_ID的路徑、版本、幾何與時間差，保留兩個來源行號與差異旗標；不默認第一筆正確。

[可重跑程式](../../../scripts/research/MS-03/audit_hirise_index_anomalies.py)與[完整判斷JSON](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/resolution_summary.json)已交付。此處HiRISE UTC欄位差異與地球Campbell／HOBO問題分開處理，既有配時限制維持，PR #7先不合併main。


## 2026-11-15交接初版（115576b；索引異常狀態以上段續查為準）

交接基準SHA `5154b9b2c58057b8719ed0d6297374ad03086da0`，接續既有形貌分析起始SHA `7b3c865e85ffeb4db81277ef34e9c3f4a318fc9f`。本節補讀原始論文及任務端索引，整理主要對話與GPU可直接引用的處置；原查核紀錄保留。範圍固定57.50–58.00°N、242.00–242.50°E，planetocentric／east-positive。

### 給主要對話：處置與可直接使用的敘述

> MS-03-E02（Adventdalen AD1）保留固定ID，降級為一般已知方法參照，退出目前有證據支持的具體配對。MS-03已有CTX目錄覆蓋，但已檢查影像不足以確認可與AD1量測比較的多邊形／裂隙網路。這是證據不足，不是確認地貌不存在，也尚無法判定兩地有相似或不同的形貌分布。

降級原因有三個：①AD1中位等效直徑18.485m，在CTX名義6.09m像素僅約3.04像素，不能可靠描繪同尺度邊界；②現有CTX browse降採樣或壓縮、局部原生EDR有低對比及條帶，且未精定位／正射，未完成全格原生像素判讀；③本次ODE及新增任務端索引均未找到可直接支援格內判讀的有效HiRISE產品紀錄。後者仍有版本與無效邊界限制，不能稱完整歷史無覆蓋。

| 可以說 | 不能說 |
|---|---|
| 三筆CTX的目錄角點聯集涵蓋名義格；實際可用細節與有效像素覆蓋未全面核實 | 全格已完成高解析度判讀、100%可辨識覆蓋，或格內不存在裂隙／多邊形 |
| 已檢查D01原生局部，未辨識出可可靠追描的閉合網路；火星尺寸與形狀維持unknown | 已證明與AD1形貌相近／不同，或把SWIM正一致性、低坡度當成看見多邊形 |
| AD1既有185polygon的重算與原刊多個統計量在刊載精度一致 | 這是新量測、獨立真值驗證，或首次AD1火星類比 |
| 2011論文明確使用另一組Utopia Planitia HiRISE影像，該具名影像不涵蓋MS-03 | 已完整排除所有文獻對MS-03的研究，因此本組全球首創 |
| 本輪增加固定MS-03範圍的覆蓋、資料品質、可辨識尺度與適用性查核 | 已完成Mars polygon偵測、地下冰鑑定、成因或資源評估 |

**主要對話下一步：** 在總結、研究卡或展示中同步採「一般方法參照、非當前具體配對」，保留ID及降級理由；圖說須區分「目錄足跡」「局部實際像素」與「地球既有GIS」。本聊天室只提供交接，沒有修改其他對話文件或網站，也沒有發送外部通知。若後續取得能清楚辨識完整邊界且精定位的格內影像，再重新評估；即使形狀相近，成因與地下冰仍需同位材料／層序、立體或重訪影像及獨立地下結構證據，不能用外觀直接推導冰楔、冰深、含量或可採性。

### 這輪新增的證據與讀取範圍

| 新證據 | 實際查核結果 | 能支持與不能支持的內容 |
|---|---|---|
| [HiRISE任務端RDR累積索引](https://hirise-pds.lpl.arizona.edu/PDS/INDEX/RDRCUMINDEX.TAB)及[原標籤](https://hirise-pds.lpl.arizona.edu/PDS/INDEX/RDRCUMINDEX.LBL) | 實際下載168,675,271bytes、SHA256 `d58cf52657371f6a7e65ef4dc687fdd2f9c70e276f7755853e27971f17df4126`；表頭Last-Modified為2026-11-03。205,451列均為821bytes；204,836列有效bbox未與指定格相交；615列無效bbox另存未定。標籤宣告205,302列，與實表不一致，未自行修正 | 提供獨立於ODE查詢介面的任務產品清單補查；不是對無效列、未發布產品或完整歷史的排除。[結果JSON](../../../outputs/research/MS-03/morphology/evidence_followup/HiRISE_independent_index_check.json)、[無效列](../../../outputs/research/MS-03/morphology/evidence_followup/HiRISE_invalid_bbox_rows.csv)、[取得紀錄](../../../outputs/research/MS-03/morphology/evidence_followup/index_download_manifest.json) |
| [Ulrich等2011作者公開稿](https://awi-test.eprints-hosting.org/24005/1/Ulr2011a.pdf)，[DOI](https://doi.org/10.1016/j.geomorph.2011.07.002) | 實得PDF4,448,816bytes／21頁（含封面）；重點讀印刷pp.199–201、203–204，§§2、3.1–3.3、表2–4。表3 AD1 N=185；表4與本組13項重算統計在原刊四捨五入精度一致 | 支持資料身份、定義與既有同用途先例；不是整篇全文審查、原始HRSC影像QA或新場址發現。[讀取／雜湊紀錄](../../../outputs/research/MS-03/morphology/evidence_followup/author_paper_reading.json)、[逐項核對表](../../../outputs/research/MS-03/morphology/evidence_followup/AD1_published_table_crosscheck.csv) |
| 原論文§3.2與任務索引的具名影像對照 | 論文將火星製圖限制於`PSP_001938_2265`、`PSP_002439_2265`及1m DEM；任務索引RED／COLOR的bbox約45.858–46.184°N、92.002–92.211°E，均在MS-03之外 | 確認這篇論文的具名火星影像不等於本格；只限此論文／此影像清單。[索引原列](../../../outputs/research/MS-03/morphology/evidence_followup/published_Mars_image_index_rows.csv) |

原論文§3.2另記載HRSC-AX orthoimages名義20cm/pixel；這輪仍未取得原raster，不能把文獻規格寫成影像品質已驗證。文中影像取得期間為2008年，2009是現地工作／資料目錄campaign脈絡，須分開記。原文p.200有疑似N/E互置的數字，不直接作合法座標或靜默修正；上述排除採具名產品的實際任務索引邊界。

### 給GPU：固定輸入、禁用推論與後續啟用條件

| 交接資產 | 可做的工作與界線 |
|---|---|
| [覆蓋／判讀圖PNG](../../../outputs/research/MS-03/morphology/MS03_AD1_coverage_interpretation.png)／[PDF](../../../outputs/research/MS-03/morphology/MS03_AD1_coverage_interpretation.pdf) | 圖A是目錄足跡；B是單一D01局部、顯示伸展且未正射；C是AD1 GIS。各面板尺度分開，不當作共同解析度的形貌匹配證據 |
| [幾何／可辨識性表](../../../outputs/research/MS-03/morphology/observability_comparison.csv)、[AD1逐polygon表](../../../outputs/research/MS-03/morphology/AD1_recomputed_geometry.csv)、[摘要](../../../outputs/research/MS-03/morphology/AD1_geometry_summary.json) | 可重現AD1向量幾何與像素取樣比；MRR長寬不等於論文largest/smallest diameter，L/W也不是原論文W/L。Mars量保持unknown，不補零或用AD1數值代入 |
| [影像清單](../../../outputs/research/MS-03/morphology/image_inventory.csv)、[取得清單](../../../outputs/research/MS-03/morphology/acquisition_manifest.json)、[D01裁切來源](../../../outputs/research/MS-03/morphology/native_crop_provenance.json) | 可核對產品、原始位元組、名義尺度與近似定位；JPEG原尺寸不等於原生有效細節，8bit DN非已校準反射率，不做跨日期光度比較 |
| [新增任務索引查核](../../../outputs/research/MS-03/morphology/evidence_followup/HiRISE_independent_index_check.json)與[原刊統計核對](../../../outputs/research/MS-03/morphology/evidence_followup/AD1_published_table_crosscheck.csv) | 可重跑範圍檢查與刊載精度核對；完整索引只在本機暫存，依URL與SHA重取，不把「GitHub有摘要」寫成「GitHub有完整原始索引」 |
| [方法與重跑說明](../../../outputs/research/MS-03/morphology/README.md) | 保留原檔、來源與起始SHA；本次沒有要求重跑全球排名或啟動新的大型處理 |

**目前不能做：** 從現有CTX推算MS-03 polygon面積、圓度、尺度分布或類比得分；將格外HiRISE移用；把目錄足跡當有效像素mask；把未辨識到當不存在；從形狀、SWIM或坡度推導成因／冰量；跨天體使用地球CRS算距離。3像素僅是AD1中位尺寸除以CTX名義取樣，不是經校準的偵測閾值。

**若後續資料補齊，啟用順序：** ①先核對格內足跡、有效像素、投影與品質，完成精定位／必要正射；②清楚定義可辨識閉合邊界與遮罩、邊界不確定度，在兩地共同可觀測尺度重新取樣並說明資訊損失；③建立可覆核的人工標註／辨識QA，才量測同一定義的幾何並比較選樣偏差；④保留形貌與成因／冰真值分離，取得獨立證據後另作解釋。若未達條件，維持降級，無須為湊配對而補值或另找地點。

**時標與交接狀態：** Campbell偏移原因仍unknown，HOBO深度logger同步未獨立驗證，既有配時禁用維持。本輪形貌工作不依賴配時，也不解除限制。交接已寫入此報告與PR #7供讀取；未更動主要對話、GPU輸出、總Excel或網站，先不合併main。


## 2026-11-15形貌查核初版（5154b9b；原論文取得狀態以上段補證據為準）

起始SHA `7b3c865e85ffeb4db81277ef34e9c3f4a318fc9f`；只查57.50–58.00°N、242.00–242.50°E。**目前沒有足夠影像證據確認格內存在能與AD1量測比較的多邊形／裂隙網路。MS-03-E02降級為一般已知方法參照，退出本輪有證據支持的具體配對；不刪ID，也不宣稱格內不存在這些地貌。** 下方舊的「條件式形貌對照」由本節處置更新取代。

交付：[影像覆蓋／判讀圖PNG](../../../outputs/research/MS-03/morphology/MS03_AD1_coverage_interpretation.png)、[PDF](../../../outputs/research/MS-03/morphology/MS03_AD1_coverage_interpretation.pdf)、[幾何／可辨識性比較表](../../../outputs/research/MS-03/morphology/observability_comparison.csv)。[完整方法、可重跑指令與限制](../../../outputs/research/MS-03/morphology/README.md)包含來源授權、原檔範圍及影像顯示處理。

### 實際查詢與取得的影像

[ODE官方介面](https://ode.rsl.wustl.edu/mars/pagehelp/Content/Additional_Resources/ODE_REST_API.htm)指定MRO、範圍及limit1000，CTX/EDR回傳3筆；HiRISE/RDRV11與舊RDR均回傳0。查詢原JSON保存；無效產品型別與不支援定位的EDR錯誤不當作零覆蓋。USGS獨立足跡查詢403，因此沒有第二份成功的負面確認。這是本次目錄查詢結果，不能寫成HiRISE永遠沒有拍攝過或完整歷史排除。

| 產品ID／日期（UTC起始） | 名義像素／角度 | 足跡與實際取得／品質 |
|---|---|---|
| G01_018718_2370_XN_57N118W／2010-07-25 00:47:00.535 | 6.08m；入射49.96°、出射0.09° | 目錄角點約覆蓋格45.5%；JPEG505×5222，相對原5056×52224降約10倍，不當作6m細節 |
| D01_027566_2370_XN_57N117W／2012-06-13 11:22:48.171 | 6.09m；入射49.79°、出射0.10° | 目錄約82.5%；除縮圖外，實際取得1024列原生8bit EDR位元組，檢查1024×1024像素局部：有色調起伏、坑狀特徵及條帶，沒有可靠可追描的閉合裂隙網；低對比、尺度及定位限制使其不能作全格不存在判斷 |
| V17_086802_2374_XN_57N118W／2025-01-31 23:25:39.163 | 6.11m；入射51.73°、出射0.09° | 目錄約55.0%；JPEG5056×52224雖維持原尺寸，但檢查局部有明顯壓縮區塊／量化，不能把尺寸當作可靠原生細節 |
| PSP_006864_2380_RED／2008-01-13 07:42:38.542 | 0.5m/map pixel；此列僅核對原始標籤，未取得其科學影像 | CTX備註提到的鄰近HiRISE；標籤最東241.837518391°E，小於242°E，**確定在格外，不得移作格內影像** |

[逐產品清單含完整WKT足跡與來源URL](../../../outputs/research/MS-03/morphology/image_inventory.csv)、[下載及雜湊](../../../outputs/research/MS-03/morphology/acquisition_manifest.json)。三CTX角點足跡聯集覆蓋名義格，約466.9km²（Mars球半徑3389500m局部LAEA近似）；這只表示目錄空間支撐，**不是有效像素、無雲／無霜或足以辨識的覆蓋率**。未評估全格所有原生像素。

D01原生樣本保存原DN及確切HTTP byte range；圖中僅作1–99%線性顯示伸展（DN88–104），未校準、去條帶、插值或正射。0起算列36000–37023、欄600–1623，用目錄角點雙線性定位約落在242.201–242.423°E、57.664–57.779°N；未用SPICE相機模型精定位，不能作精確地貌邊界。CTX原index角點是areographic，本組使用ODE的planetocentric轉換角點；兩者未混用。圖內明示非北向上、未量測Mars多邊形。[裁切來源與顯示處理](../../../outputs/research/MS-03/morphology/native_crop_provenance.json)可重現。

### AD1實際GIS幾何與共同可觀測尺度

只讀已取得ZIP中的`polygons_Act-IWS.*`，明確排除同包`polylines_Act-IWS.*`；EPSG32633、平面公尺，185個有效polygon。重算A、P、等效圓直徑√(4A/π)、圓度4πA/P²、最小旋轉矩形長寬與L/W；未改邊界。矩形長寬不是原論文largest/smallest diameter定義，沒有冒稱重現其全部統計。

| 量 | AD1本輪重算 | MS-03 |
|---|---|---|
| 面積中位數 | 268.361m² | unknown，未追描 |
| 等效圓直徑 | 中位18.485m；範圍8.054–50.828m | unknown |
| 圓度中位數 | 0.8066 | unknown，低解析度邊界不可比較 |
| 旋轉矩形L/W中位數 | 1.2768 | unknown |

[逐polygon結果](../../../outputs/research/MS-03/morphology/AD1_recomputed_geometry.csv)及[定義／摘要](../../../outputs/research/MS-03/morphology/AD1_geometry_summary.json)。AD1等效直徑若投到6.09m像素，約1.32–8.35像素，中位3.04像素；降採樣CTX browse中位更不足1像素。這是尺度可辨識性說明，沒有設立已驗證的偵測門檻；大polygon可能在良好影像中較易辨認，也不代表本輪已看到。未取得原HRSC-AX raster解析度與邊界誤差，不把GIS小數位當觀測精度。保留所有185polygon，未重查原研究的邊界截切與樣本選擇，不作區域隨機抽樣推論。

### 用途先例、實際新增分析與處置

[PANGAEA921087官方metadata](https://doi.org/10.1594/PANGAEA.921087)明載Act-IWS=AD1，並說明資料用於Svalbard與western Utopia Planitia火星多邊形的定量地貌比較；原[Ulrich等2011論文](https://doi.org/10.1016/j.geomorph.2011.07.002)是既有先例。本輪實讀metadata及GIS，未取得原論文全文／火星影像清單，不能宣稱完整排除過去對MS-03同格的比較。

**本輪新增的是MS-03固定範圍的適用性查核**：實際影像目錄／足跡、排除格外HiRISE、AD1可重算幾何與CTX取樣尺度檢查，以及有依據的降級。沒有新增火星polygon偵測、量化形貌相似度或新成因證據。兩地「可辨識的形貌差異」目前也無法成立；已確認的是資料尺度與品質差異。

即使之後形貌相近，仍須有格內高解析度且精定位的影像／立體地形、不同季節重訪、材料與層序／地形脈絡，以及獨立地下結構證據，才可討論熱收縮、冰楔或地下冰。雷達需說明穿透、介電性與解析歧義；現地量測／取芯需與影像同位且有獨立真值。SWIM正一致性、低坡度與多邊形外觀都不能單獨給出冰深、純度、連續性或資源量。

**處置：降級、退出目前具體配對；保留固定ID與已知方法用途。** 若日後取得合格格內影像，再另行評估；本輪不等待另外兩人，也不擴大找新場址。下方Campbell／HOBO的配時禁用限制完全維持，本次工作不使用其時間。


## 2026-11-15 PR #7最後核對

已通讀整份報告與交接，並核對本分支資料連結。修正初版取得狀態的閱讀界線，以及「同一HOBO」可能暗示共用時鐘的用詞：兩深度數值僅按作者合併匯出檔同列描述，各深度logger同步未獨立驗證。另說明QA的gaps只代表印刷時間欄間距。QA文字及輸出程式已同步，數值資料、窗口、統計與Campbell邊界均未改。

報告相對檔案連結全部存在；六個固定來源的metadata MD5與下載清單一致，六個下載URL的HEAD請求均回應HTTP200。這只確認本次連結可達，不是重新驗證感測器或時鐘。既有驗證程式與Campbell邊界核對程式實際重跑通過；完整結果見[validation.json](../../../outputs/research/MS-03/validation.json)。Campbell根因維持unknown；跨儀器配時、推定四小時校正及未驗證同步的相位／熱擴散率分析均未放行。

## 2026-11-15交接：主要對話與GPU的Campbell時標處理界線

交接基準為本分支`79072555dd90e78c3810d9e1d2ac5ec8f970c3b8`，適用MS-03／MS-03-E01 University Valley W站；原始來源固定為[Zenodo10553882](https://zenodo.org/records/10553882)。本節整理已完成查核，沒有新增分析或時間修正。後方各輪查核紀錄保留。

### 給主要對話：研究定位與缺件取得

**可直接引用的結論：** Campbell校準匯出的小數日與印刷日期，在2012-10-28補入8列NaN的邊界，欄位差由約−1小時變成−5小時。作者QA文件記載曾補8筆／4小時，但實際校準程式、補列前原始檔及2012當次時鐘紀錄尚未取得。因此只確認欄位不一致及其與補列的關聯，四小時偏移原因與正確時間仍為unknown。−1／−5小時不是已確認時區。

| 優先缺件 | 需要的具體內容 | 用來解決什麼 | 目前狀態 |
|---|---|---|---|
| 校準與補列程式 | `University_Valley_Met_Station_Calibration_all.m`實際執行版本、相依檔、輸入清單及執行順序；部署筆記另提及的`University_Valley_Met_Station_Calibration.xls` | 核對日期／小數日向量如何建立、8列如何插入，以及是否同時更新兩欄 | 尚未取得；本次公開搜尋未找到，不能稱作者未保存 |
| 未處理Campbell資料 | W站CR1000原始匯出，保留標頭、原TIMESTAMP、RECORD及所有通道；至少涵蓋2012-10-28異常前後、對應RECORD33305與33314及鄰列 | 區分logger本身跳時與後處理時間向量錯位，核對補列前後資料 | 尚未取得；`all_calibrated.txt`不能代替 |
| 2012操作／時鐘紀錄 | 該站當次下載、重設、手動校時、電腦時區及自動校時設定；相關部署日誌／LoggerNet記錄（若有） | 確認是否發生真實時鐘調整，以及方向與時間基準 | 尚未取得；2010活動紀錄不能回推2012 |
| logger程式與時間定義 | 實際部署的`UniversityValley_MetStation.CR1`版本及後續更動；小數日起算、印刷日期時區／夏令時間與取樣時間意義 | 讓校準輸出能回接到原始時鐘，而不是靠曲線對齊猜測 | 尚未取得；2009初始紐西蘭時間設定不足以解決2012問題 |

**主要對話下一步：** 將上表作為向資料持有人取得檔案的清單；接收時記錄檔名、來源、版本、雜湊與存取條件。本聊天室沒有發送作者聯絡。缺件未補齊時，保留W站為有時標限制的歷史資料方法參照；既有HOBO站內描述可保留原標示，不能寫成已完成Campbell／HOBO聯合驗證。不要將暫未查明原因寫成已證實程式bug、夏令時間或logger故障。

### 給GPU：可用輸入、禁用分析與解除條件

| 可讀取的既有成果 | 用途與必要限制 |
|---|---|
| [來源下載清單](../../../outputs/research/MS-03/uv_w/download_manifest.json) | 固定版本、六檔MD5／SHA-256及下載URL；來源是作者校準／篩選後匯出，不是原始logger位元資料 |
| [Campbell原列邊界CSV](../../../outputs/research/MS-03/uv_w/campbell_clock_boundary.csv)及[clock audit JSON](../../../outputs/research/MS-03/uv_w/campbell_clock_audit.json) | 50810行：06:00／RECORD33305；50811–50818行：10:30至14:00，全通道NaN；50819行：14:30／33314。行號含4行標頭；不含建議校正時間 |
| [來源追查紀錄](../../../outputs/research/MS-03/uv_w/clock_search_followup.json)、[搜尋日誌](../../../outputs/research/MS-03/search_log.csv) | 可知哪些資料實際取得、哪些只讀metadata、哪些未找到；不據此推定未知根因 |
| [整體QA](../../../outputs/research/MS-03/uv_w/qa.json)、[HOBO溫度整理表](../../../outputs/research/MS-03/uv_w/hobo_W_temperatures.csv.gz)、[2010站內摘要](../../../outputs/research/MS-03/uv_w/earth_only_2010_summary.csv) | 保留作者時間欄與既有單儀器描述；HOBO標頭的GMT+13也不能自行當成全部歷史校時已確認 |

**現在可以做：** 重現欄位／RECORD／NaN與來源雜湊核對，保留原始欄位、資料列順序及缺值；沿用已交付的HOBO2010年同列20／42cm描述，清楚標成原印刷時間窗口；各深度由不同HOBO logger記錄，原檔同列不等於本組已核實同步，不用這個數值差作相位或傳熱真值。這些工作不解除跨儀器配時限制。本次交接沒有新增計算需求。

**確認前暫停：**

- Campbell與HOBO任何逐時join、最近時間配對、跨儀器溫差、偏差校準或用其中一台補另一台缺值。
- 以互相關、日峰值或曲線相似性選擇平移量；直接平移四小時、指定哪個時間欄正確、轉UTC／當地太陽時。
- 混合兩儀器計算相位差、傳熱時延、熱擴散率，或用尚未配準資料重現論文跨感測器結果。
- 將Campbell邊界的270分鐘日期跳躍換算為已確認的真實缺測時長，或將補列後的時間當可靠真值。
- 依賴尚未確認的Campbell實際時間，建立與軌道過境、日照或火星資料同步的驗證；既有溫差也不能用來反演冰深、冰量或設備性能。

**取得缺件後的工作順序：** ①先封存原檔及版本；②獨立核對原TIMESTAMP／RECORD與部署紀錄；③逐步重現作者校準與補列，確認偏移究竟在哪一步出現；④若證據支持修正，另輸出有原欄、修正欄、逐列旗標與規則版本的衍生表，保留原檔；⑤將仍有歧義的列標unknown，交主要對話確認修正適用範圍與獨立時間依據。即使Campbell問題解決，仍須確認HOBO自身時間基準後，才能另行設計與驗證配時；不得只因兩曲線接近就放行。

**本輪交接狀態：** 文件與連結已整理；未產生校正時序、跨儀器配對、物理參數新結果或作者回覆。PR #7保留開啟，由主要對話後續決定合併。

## 2026-11-15追加搜尋：原碼、原始logger與2012操作紀錄仍未取得

本節接續`ab31a3d`，保留前輪邊界核對及全部歷史紀錄。本次有新增作者活動紀錄與版本查核，**仍不足以確認四小時偏移原因**。不改任何時間欄，不與HOBO配時，也不新增跨儀器統計。

| 追查路徑 | 實際取得／讀取範圍 | 結果與限制 |
|---|---|---|
| [作者Zenodo版本介面](https://zenodo.org/api/records/10553882/versions)及[latest](https://zenodo.org/api/records/10553882/versions/latest) | 兩個API實際讀取；versions回傳10553882一筆，latest仍為10553882 | 本次沒有找到另一個公開版本補上原碼或2012紀錄；不推論沒有私存資料 |
| 同固定版本的[2010 activities summaries.pdf](https://zenodo.org/records/10553882/files/2010%20activities%20summaries.pdf) | 實際下載1,108,938bytes，MD5 `d2184a3cb5941a62c9ff5079289ca766`符合來源；14頁文字抽取檢索，重點讀pp.5、8–9 | p.5 University Valley段記錄2009–2010資料下載與電腦過冷造成的重複連線問題，未提供2012-10-28時鐘或補列紀錄。這不能解釋四小時變化 |
| 同PDF的站點歸屬核對 | pp.8–9連讀 | p.9「station program was not changed」承接p.8 **Pearse Valley**，不能誤作University Valley W站未改程式的證據 |
| [2022原論文](https://doi.org/10.1017/S0954102022000025) | 出版者HTML的Meteorological measurements、Supplemental material、Author contributions | 作者說明Marinova負責logger程式、部署及取回資料；文中資料典藏方向為NSIDC，補充資料為Fig.3每日氣象數值。這些段落未提供所需`.m`、原始W logger檔或2012校時紀錄；不以論文曾比較儀器推定本組可直接配時 |
| [USAP-DC 609529](https://www.usap-dc.org/view/dataset/609529) | 官方metadata與公開檔案清單，未下載數值檔 | 清單為四谷地下冰深度調查，並非W站CR1000原始時序或時鐘操作紀錄，不作替代輸入 |
| 精確／作者與站點名稱補搜 | 2026-11-15；完整查詢記在search_log Q23–Q28 | 本次未找到可取得的校準程式、原始W站logger檔或2012校時紀錄。搜尋結果含其他站點與無關同名資料，均不採用；沒有進行作者聯絡，也不聲稱全面排除 |

本輪取得與搜尋紀錄見[clock_search_followup.json](../../../outputs/research/MS-03/uv_w/clock_search_followup.json)。新PDF原檔只留本機暫存，沒有提交大型原檔。原資料版本10553882、既有55,346列Campbell與HOBO描述結果均維持原樣。

**研究判斷維持unknown**：前輪證據已確認「欄位差改變」與「8列NaN補列」在同一邊界；本輪沒有拿到能重現該處理的原碼及前處理檔，因此無法把處理錯位假說提升成已證實原因。2010下載斷線也不能回推為2012異常原因。

接續工作只需針對缺件：實際執行的校準`.m`與相依檔、2012-10-28前後未處理CR1000檔、2012當次下載／重設／時鐘紀錄，以及時間向量生成規則。若持有人提供後，再比較補列前後輸出與RECORD；在此之前，停止重複無新線索的泛搜，保留原時標及跨儀器配時禁用狀態。

## 2026-11-15續查：Campbell −1／−5小時差異與作者補列紀錄

本節接續`89ff46f`，只查時間欄處理。**四小時差異與作者記載的8筆NaN補列，在匯出檔中發生於同一邊界；尚未取得校準程式，根因與正確時刻仍未確認。** 保留兩個原時間欄，不修正、不轉UTC或太陽時、不與HOBO配時。這裡的−1／−5小時是「小數日減印刷日期」的欄位差，並非已確認時區。

### 原列證據與可重現核對

輸入仍為[Zenodo固定版本10553882](https://zenodo.org/records/10553882)的`UniversityV_09_13_Campbell_data_all_calibrated.txt`，MD5 `333b498382376f3bb034e68862bede70`。全55,346列僅找到一次偏移轉換；本組為檢查欄位差，以naive 2009-01-01作計算基準（未獨立驗證作者起算慣例），偏移四捨五入至0.01小時，以容納小數日列印精度。

| 原檔實體行（含4行標頭） | 原日期欄 | 原小數日 | RECORD | 可確認內容 |
|---|---|---|---|---|
| 50810 | 2012-10-28 06:00:00 | 1396.2083 | 33305 | 邊界前最後一列，欄位差約−1小時 |
| 50811–50818 | 2012-10-28 10:30:00至14:00:00 | 1396.2292至1396.3750 | 全NaN | 連續8列，RECORD及全部感測欄皆NaN；欄位差約−5小時 |
| 50819 | 2012-10-28 14:30:00 | 1396.3958 | 33314 | 有效RECORD恢復，偏移仍約−5小時 |

邊界日期欄跨270分鐘，小數日僅跨約30.096分鐘（四位小數造成的列印捨入）；RECORD由33305至33314。這些證據確認兩個時間表示在補列邊界後不一致，**無法單憑匯出檔決定應修日期欄或小數日**，也不能把270分鐘逕稱為真實缺測時間。

核對輸出：[原列邊界表](../../../outputs/research/MS-03/uv_w/campbell_clock_boundary.csv)、[機器可讀查核](../../../outputs/research/MS-03/uv_w/campbell_clock_audit.json)。[核對程式](../../../scripts/research/MS-03/audit_campbell_clock.py)只讀Campbell檔，不接受HOBO輸入；沒有產生校正時序。

### 作者程式、部署紀錄與取得限制

- **作者QA正文已讀**：同紀錄中的`University Valley weather station data check 2011-2013.docx`，段落開頭「There is some weird missing data in Oct 2012」記載缺8筆／4小時，作者補入缺少時間並將感測欄設NaN。正文另明確指名`University_Valley_Met_Station_Calibration_all.m`用於校準與移除表面尖峰。它未交代補列程式、每列日期或時鐘修正方式；不能據此宣稱已讀到程式或確認某行bug。DOCX封裝未含嵌入附件。
- **部署PDF已讀**：`University Valley Campbell notes Dec 2010.pdf` p.1記載2009-12-02設定logger為紐西蘭當地時間，並提到與當地標準太陽時間差一小時。這是初始部署脈絡，不能解釋2012年的四小時突變；本輪未找到2012年該次校時／重設／下載操作紀錄。PDF另提及`University_Valley_Met_Station_Calibration.xls`與`UniversityValley_MetStation.CR1`，尚未取得。
- **固定版本清單已核對**：[API](https://zenodo.org/api/records/10553882)列28檔，沒有`.m`、`.CR1`或`.xls`檔（有另一份`.xlsx` HOBO表，不能當作所需Campbell程式）。這只限定該版本清單，不代表作者其他地方從未公開。
- **2026-11-15補搜**：精確查詢`"University_Valley_Met_Station_Calibration_all.m"`與`"UniversityValley_MetStation.CR1"`，本次搜尋未找到可取得原碼。未向作者發信，也未將無結果寫成完整排除。

### 目前判斷與交接

**可說**：時標四小時差異與已記載的補NaN操作具有直接邊界對應；資料處理造成時間向量錯位是值得優先查證的假說。**不能說**：已證實是夏令時間、logger跳時、MATLAB特定bug，或將某段平移四小時就已完成校準。

需要主要對話／資料持有人提供：①實際執行的`University_Valley_Met_Station_Calibration_all.m`及相依版本；②2012-10-28前後未處理Campbell檔；③當次logger時鐘、下載與重設紀錄；④小數日起算及時間向量建立規則。取得後才可逐步重現補列，決定修正哪個欄位。GPU暫不跨儀器join；HOBO原有2010年站內描述維持原樣，不能用其曲線相似性代替時標真值。

## 2026-11-15續查：W站時序已取得，先完成地球站內描述

本節接續研究commit `89deea4`，更新E01資料可取得性；下方2026-11-14「尚未取得時序」保留為初版紀錄，以本節及新版候選表為準。E02、MS-03科學數值與原先例判定均未改，也未合併main。

### 取得的資料、版本與身份

沿後續原論文Environmental data（printed p.124）的明確資料連結，找到[Zenodo概念紀錄10553881](https://zenodo.org/records/10553881)，API實際指向固定版本 **[10553882](https://zenodo.org/records/10553882)，DOI `10.5281/zenodo.10553882`**。metadata將資料連到Marinova等2022論文、授權列CC0。這是作者保存的校準／篩選後觀測匯出，不是未處理的logger位元資料。

六個選定檔案已實際下載，全部符合來源MD5；下載URL、大小與SHA-256完整記在[download_manifest.json](../../../outputs/research/MS-03/uv_w/download_manifest.json)。原始檔留在本機暫存，提供可重取程式，未把十多MB原檔重複提交。

| 實際取得的檔案 | 內容與本輪讀取 |
|---|---|
| `UniversityV_09_13_Campbell_data_all_calibrated.txt` | 8,535,365bytes；55,346筆，多深度與氣象匯出；完整解析做結構／缺值檢查，未做跨時標合併 |
| `UniversityV_09_13_Hobo_WeatherStation_data_good_only_calibrated.txt` | 2,522,735bytes；27,553筆，表面／20／42cm溫濕度；本輪只整理溫度與原始時標 |
| `University Valley Campbell notes Dec 2010.pdf` | 10頁原部署／校準說明已讀；pp.1–2可核對W站座標、名義探針位置與logger設定 |
| `University Valley weather station data check 2011-2013.docx` | 已讀正文；說明表面通道問題、移除尖峰／填NaN與一個Campbell42cm點曾插值，不能把匯出檔當全未改動的原始觀測 |
| `UnivValley_Dec2009Deployment_HoboInfo.docx`、`UnivValley_HoboInfo_Dec2010_Update.docx` | 已讀正文；其餘D／S站命名和座標存在需另核對的脈絡，本輪不啟用那些站，也不拿它們補W缺值 |

另核對出版者2022補充連結，但下載403；原文說明該補充是Fig.3每日氣象平均，不是地下完整時序。NSIDC-0529是冰界面深度調查，也不能替代W溫度。完整搜尋／讀取紀錄已追加到search_log與sources。

### QA發現與保守處理

| 項目 | 本輪實際檢查 | 影響與處理 |
|---|---|---|
| HOBO列與時標 | 2009-12-10 00:00至2013-01-31 00:00；27,553列，無重複，全部相鄰列60分鐘 | 保留原列與`GMT+13:00`標頭；未轉UTC／太陽時，也未宣稱已確認所有歷史校時 |
| HOBO欄名問題 | 首行14個欄名片段，單位及全部資料列為11欄 | 依單位、欄名片段與部署說明明列位置映射；20cm為第6欄、42cm第9欄（均1起算），不直接用錯位DictReader讀取 |
| HOBO有效數 | 表面8,799；20cm27,553；42cm27,550 | 表面缺值多，不產生三年完整表面年均；NaN保持缺值，不重複七日來湊全年 |
| Campbell時標 | 日期格式前後不同但可解析，無重複；2012-10-28 06:00至10:30有270分鐘跳躍 | 同處小數日相對日期欄由約−1小時改為−5小時。不能直接將它當實際缺測4小時或擅自校時；不跨儀器逐時join |
| 作者既有處理 | 校準／移除值／NaN／插值紀錄存在，但逐列介入旗標不完整 | 本輪未重新校準或再插值；作者`good_only`不等於本組完成感測器獨立驗證。已指出的單點插值屬Campbell，不指認為HOBO某一點 |

[完整QA](../../../outputs/research/MS-03/uv_w/qa.json)與[逐月涵蓋表](../../../outputs/research/MS-03/uv_w/monthly_coverage.csv)可供接續檢查。QA的gaps與step_minutes僅為印刷日期欄相鄰列間距；不是已確認的真實停機／缺測時間。月表中的calendar expected只表示名義時距的日曆格數，不保證各儀器已校到同一真實時刻。

### 能先做的分析：2010年作者HOBO合併匯出檔的20／42cm描述

設計窗口固定為**原HOBO日期欄2010-01-01含至2011-01-01不含**，不是火星同季節窗口。數值直接來自作者匯出，無填值、重採樣、去尖峰或新校準；本輪計算只作地球站內描述。

| 量（°C） | 有效N／名義8760小時 | 本輪均值 | 最小／最大 |
|---|---:|---:|---:|
| 20cm溫度 | 8760／8760 | −24.974049 | −41.618／−2.859 |
| 42cm溫度 | 8759／8760 | −24.730885 | −36.783／−9.816 |
| **同列20cm減42cm** | 8759／8760 | **−0.244125** | −7.076／+8.580 |

此處「配對」只表示作者合併匯出檔的同列欄位，不表示已核實不同深度HOBO logger的時鐘同步。數值差用各列有效配對計算，不用兩個不同有效數的均值相減。1筆缺失保留；N為觀測支撐，不是獨立樣本數，未報信賴區間。結果見[earth_only_2010_summary.csv](../../../outputs/research/MS-03/uv_w/earth_only_2010_summary.csv)，全HOBO溫度匯出含來源行號、原字串、NaN空值及名義深度，見[hobo_W_temperatures.csv.gz](../../../outputs/research/MS-03/uv_w/hobo_W_temperatures.csv.gz)。沒有畫成冰深或準確度結果。

### 對MS-03可以與不可以比較什麼

| 比較問題 | 本輪狀態 | 結論界線 |
|---|---|---|
| 同一地球站點合併匯出檔的兩深度同列差與可用期間 | **已可描述** | 上表只描述作者匯出檔同列數值；各深度logger同步未獨立驗證，不等於真實同時刻溫差、新界面偵測或因果歸因 |
| 哪些深度／時距／缺值資料適合檢查熱傳模型輸入 | **可作資料需求比較** | W有點位分層時序，MS-03目前只有不同物理尺度的產品；據此整理缺件，不保證新方法 |
| 振幅衰減、相位與熱擴散率重現 | **尚未執行** | 應先確認各深度logger時間基準與同步、感測器耦合、校準、窗口及作者處理；在此之前不做相位或熱擴散率重現，也不從年均差反推熱慣量 |
| W站溫度與MS-03 MCS作數值相減／相似度 | **不可成立** | 地下20／42cm與模型校時地表粗格不是同量；MCS偏至60°N、120°W且QA／季節支撐不足 |
| W站分層和SWIM兩深度地圖一對一對應 | **不可成立** | 地球已定位探針不代表火星界面；兩SWIM一致性圖不是實際垂直剖面 |
| TES熱慣量、冰含量、可採性或火星設備性能 | **仍未知** | 沒有相同物理支撐、獨立冰真值或跨環境驗證，不以此時序補成符合 |

E01從「原時序未取得」更新為「已有來源可重取的時序及初步地球站內QA／描述」。仍是已有用途的方法參照；新穎性與MS-03局部冰況沒有因此通過。

### 重跑與尚缺證據

```sh
python3 scripts/research/MS-03/inspect_uv_w.py
python3 scripts/research/MS-03/validate.py
```

第一個程式預設把六個固定MD5原檔放到已忽略的 `data/raw/earth/MS-03/uv_w_10553882/`；實際本輪執行使用`--raw-dir /tmp/uv_w_10553882`。程式輸出只放MS-03專用目錄，無API憑證。完整網址與固定版本已記錄，不依賴本機私有資料。

還缺：Campbell時鐘更動歷史、作者逐列處理旗標／校準程式、感測器獨立校驗，以及MS-03真正局部冰／材料／溫度證據。本輪沒有替作者推定時鐘原因，沒有聯絡作者或自動擴大至其他谷地。PR #7更新後仍由統籌審查，不合併main。

---

本研究保留兩個**已有研究的方法參照**：University Valley W站作乾覆土熱判讀參照；Adventdalen Act-IWS／AD1作冰楔地貌與季節凍融的條件式對照。沒有證明哪一地「最像火星」，也沒有發現新場址。兩者回答不同的驗證需求，不合併成一個具備全部條件的天然火星環境。

## 2026-11-14初版紀錄（取得狀態已由前段2026-11-15更新取代）

以下保留當時判斷。E01「原時序未取得」僅屬歷史狀態；目前已取得作者校準匯出，未取得的是未處理logger原檔、校準原碼及2012校時紀錄。下文原先的分析建議受前段配時禁用條件約束。

## 初版：版本與資料是否真正取得

未收到指定共同SHA，因此依指示以開始時 `origin/main` **`3cc8488577535e2fa4d146021fde51f8ff6cc667`** 建立 `research/ms-03-earth-analogs`，使用獨立worktree，保留原圖片分支。本輪沒有合併main或改其他人的文件。

已讀共同套件的 `report.md`、`selected_targets.json`、`final_candidates.csv`、`candidate_native_evidence.json`、`all_data_usage.csv`。`docs/TEAM_START.md`與`scripts/restore_team_data.py`在此基準不存在；沒有聲稱執行還原腳本。

兩個大型檔不在上述main，但已從遠端交接分支 `handoff/verified-data-20261114`，固定commit **`f7076c9fdc77e00244ed5d6863aad2bf78cfa28f`** 的Git物件實際取回並逐位元核對：

| 來源路徑 | 實得bytes／SHA-256 | 實際檢查及用途 |
|---|---|---|
| `outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx` | 23,035,176；`157a108a08b8ca32ca52b40f3e9e80536431125cecfb838aa21223a933ac1175` | XLSX ZIP各項CRC／workbook.xml存在；未逐格驗證科學內容。本輪數字不取自歷史Excel |
| `outputs/research/mars_reselection_20261114/screened_pool.csv.gz` | 7,702,846；`7c5559e40fca9fa304b7799e4490bfb4ff0d55ea0a02819c53f432377462ff92` | gzip與CSV解析成功，58,238列、54欄；未重跑排名／新篩選 |

大型檔保存在暫存目錄，不重複提交。路徑、來源commit與取得狀態見[manifest](../../../outputs/research/MS-03/manifest.json)。檔案可讀不等於其全部內容已經科學驗證。舊I-01／I-02配對不作MS-03證據；本輪重新讀取文獻及新火星格的實際欄位。

## MS-03：只沿用已核對的原生格結果

中心57.75°N、242.25°E（西經117.75°）；名義範圍57.5至58°N、242至242.5°E，約29.64 × 15.81 km。沿用planetocentric／east-positive；這是篩選單元，不是冰藏邊界、鑽孔或著陸區。

| 面向 | 實際欄位與支撐 | 解讀邊界 |
|---|---|---|
| 地形 | 原生平均坡度0.1627532209°，高差76m；MOLA64/64有限格，約3.7km坡度基線 | 不表示米級平坦、無石塊或所有格都是雷射直接量測；未取得觀測密度遮罩 |
| 熱性質 | TES平均152.80772587767 J m⁻² K⁻¹ s⁻½，範圍111至270；79/100有效，排除21個mask0格 | 不是溫度／硬度；空間範圍不等於儀器誤差；2007為建檔年，觀測起訖未列 |
| 水／冰 | SWIM原生0–1m均值0.9109040236；1–5m均值0.5099723018 | 一致性無單位，非含冰量、機率或真實分層；兩產品共享輸入 |
| 大氣／沙塵 | MY34／35 CDOD均值0.0982145182／0.0886603747；p95 0.1733616889／0.1409617454；各669重建sol | 原生3°，選取58.5°N、117°W；9.3µm吸收總柱，非當地風速、氣壓或沉積率 |
| 溫度背景 | MCS選格60°N、120°W；5°網格，MY29–36，10°Ls季節座標。日171、夜148、配對60／288；配對對比中位數67.054737899K | 模型校時衍生值；QA／每bin樣本數／不確定度缺失；季節配對不等於同sol，不能當日夜振幅或地面實測 |

數值由[原生C紀錄](../../../outputs/research/mars_reselection_20261114/candidate_native_evidence.json)與final_candidates交叉核對，完整來源URL及量測支撐另存[mars_reference.json](../../../outputs/research/MS-03/mars_reference.json)及[evidence.csv](../../../outputs/research/MS-03/evidence.csv)。沒有重跑原始影像或全球管線。MEDA位於Jezero，不移植到本格。

**可檢驗假設：** 在這種熱慣量與近表層線索組合下，表層材料、含濕狀態與界面位置是否會產生難以區分的熱訊號？若局部影像出現多邊形，哪些獨立結構量測能避免把形態直接當成冰？本格是否有多邊形、局部冰深與材料都未知，假設尚未驗證。

## 候選與四面向比較

| 固定ID／位置與範圍依據 | 地形 | 溫度／熱性質 | 水／冰 | 大氣／沙塵 | 處置 |
|---|---|---|---|---|---|
| **MS-03-E01：University Valley W**；−77.862150°、160.710100°E。U1原DMS換算；歷史站點錨點，datum／誤差未聲明，不加半徑 | 岩質谷底站點；沒有與Mars同物理尺度的坡度核對 | U1多深度站點紀錄可支援熱傳方法比較；沒有匹配尺度Earth熱慣量，不能與TES直接相減 | 有已定位歷史乾覆土／冰膠結界面；不代表當前冰況或火星格 | 站點有風／T-RH；塵柱與沉積資料未取得。地球空氣熱交換無法直接代表火星 | 保留**已知乾覆土方法參照**；原時序未取得，暫不能宣稱完成新熱分析 |
| **MS-03-E02：Act-IWS／AD1**；78.184°N、15.913°E為A1事件起點，不是感測器。事件經緯範圍78.184至78.188°N、15.913至15.933°E；實際GIS185個polygon與外包框另記CSV | 有實際取得的多邊形網路GIS；不是整區冰覆蓋。MS-03局部形態未確認 | A2有該谷地熱濕／裂隙監測，但尚未證明感測點與每個AD1polygon同位；不移用區域氣象數值 | 冰楔／季節活動層提供不同幾何及濕度條件的對照；不能作乾覆土均勻冰層等價物 | 雪與風重分布是必要干擾；雪不等於火星沙塵，無本候選當地塵柱量測 | 保留**條件式地貌與濕凍土對照**；排除作已證實熱環境匹配或資源估計 |

兩地的共同價值是分清「有冰的物理結構」與「可觀測熱／形態訊號」之間的條件；並未定量證明二者或MS-03環境等效。地球低重力、低壓CO₂、輻射和完整火星熱季節均不能由天然場址重現。地方高程不跨天體相減；沒有權重或相似度百分比。

### E01的資料與可執行工作

重新讀U1的Meteorological measurements、Thermal diffusivity及Appendix；站點、深度與取樣間隔列於證據表。U2作者摘要支持雪／鹽邊界條件的既有模型脈絡。本輪沒有取得原始T-RH時序，不能冒稱已完成新QA、重算擴散率或證明新機制。

下一個可執行步驟是取得有明確欄位／時標／缺值的原序列，先重現已發表窗口，再將材料參數、界面位置與熱邊界的可辨識性列成預先定義的問題。若要評估準確度，需另有與建模輸入獨立的同位真值；歷史答案不能同時拿來調參與盲測。尚未執行任何新實驗。

### E02的實際資料取得與範圍

已從[PANGAEA921087](https://doi.org/10.1594/PANGAEA.921087)下載Act-IWS原始ZIP（57,636bytes，SHA-256 `c75e7568c9fbfc67898f64e9c18681e5dc7e24a1ec272ceafa12c51377b8054e`），核對ZIP完整性、185個polygon、DBF欄位與PRJ的WGS84／UTM33N。原檔附來源保留於[專用目錄](../../../outputs/research/MS-03/polygons_Act-IWS_source.zip)，CC BY4.0，須署名Ulrich、Härtel、Hauber（2020）。本輪只做檔案結構與座標支撐核對，未重算地貌統計。

`Act-IWS`與`IWS`是不同檔，不能把資料庫八個場址總包範圍或IWS範圍換成AD1邊界。事件範圍、原始polygon及其外包框也不等於新測區或連續冰界面。APGC是metadata；原始資料依PANGAEA事件與實取檔案判讀。

下一步先查MS-03局部影像是否真有可比地貌；沒有就保留AD1為一般方法對照，不硬配。若要加熱響應，需取得AD1感測器位置／原序列並核對與GIS是否同位。A3的原始地震資料需向作者索取，本輪沒有聯絡；A6另有公開資料入口，但2023鑽芯與AD1的關係未核實，不拿來補成本候選真值。

## 同場址、同用途先例及可能差異

| 候選／來源與實讀範圍 | 分類 | 已回答或執行的部分 | 這輪還能提出什麼／不能說什麼 |
|---|---|---|---|
| E01／U1，出版者方法及Appendix | **直接先例** | 同W站熱描述及參數判讀問題已有研究 | 本輪為MS-03證據需求整理，沒有新熱機制；不能稱首次覆土熱判讀 |
| E01／U2，USGS作者摘要 | **部分重疊** | 雪與鹽的冰穩定性模型已有 | 只讀摘要，不作完整方法排除；不能宣稱首次控制表層條件 |
| E01／U3，原始兩頁會議摘要 | **用途不同** | 谷地已有鑽採與鑽頭控溫，但具名鑽孔不是W站 | 不移用鑽採性能或把同一谷地當同孔；本輪不以鑽探創新立題 |
| E02／A1、A7，原資料及原論文摘要 | **直接先例** | 相同AD1資料已有火星地貌比較用途 | 以新火星ID重命名不構成新貢獻；本格地貌尚未知 |
| E02／A2，監測方法／結果相關段落 | **部分重疊** | 熱濕、雪與裂隙關係已有多感測器研究 | 未核實其感測座標與AD1網路的精確對照，不能稱已同位聯合分析 |
| E02／A4，作者會議摘要location／Results | **部分重疊** | Adventdalen已有WISDOM地層反射歧義研究 | 未取得trace幾何；不能宣稱首次在此谷地用雷達辨冰，也不能判定與AD1同範圍完整重複 |
| E02／A6，方法與資料可用性 | **用途不同** | 另組谷地鑽芯／InSAR研究提供真值對照類型 | 未核實同址，不移作AD1冰含量或MS-03凍融真值 |

因此本輪的具體差異是**面向MS-03的證據支撐與缺口帳**，不是已完成的新物理分析。未找到同一個MS-03標籤，不表示從未有人研究同問題。精確的新演算法、測區、輸入、真值、結果量均未定義，完整新穎性無法判定。

搜尋平台、實際查詢詞、日期與讀取限制見[search_log.csv](../../../outputs/research/MS-03/search_log.csv)；來源ID與完整讀取範圍見[sources.json](../../../outputs/research/MS-03/sources.json)。2011作者稿下載回傳Anubis拒絕頁，PMC回傳瀏覽器檢查；沒有把它們當全文。搜尋為有限公開來源查核，未完整查Scopus／所有引文及未公開試驗。

## 給統籌的處置與完成程度

- **已完成：** 新MS-03原生格／尺度核對；兩個固定ID候選；四面向證據與未知；用途先例分類；大型共同檔實際取回檢查；AD1原始GIS取得及結構核對；可解析交付與專用檢查程式。
- **保留：** E01作優先乾覆土方法參照；E02作有條件的地貌／濕凍土對照，不評選全環境優勝者。
- **排除的主張：** 新場址、全球首次、91%含冰、SWIM深度差就是冰剖面、低TI就是鬆軟或有冰、兩地已證明類比成功、地球流程直接給火星鑽採效能。
- **待補：** MS-03局部影像及獨立冰／材料證據；候選中心溫度及QA；Earth原時序和AD1精確感測器對照。這些是後續有條件工作，不以本輪完成度掩蓋。

本輪不修改排名、總Excel、網站或其他研究文件；無新場址發現、現地量測、因果或性能驗證。完成提交與PR後停止，由統籌決定後續取捨。
