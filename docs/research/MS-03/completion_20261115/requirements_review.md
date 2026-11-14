> 本檔是固定基準234e58a8的整合前審查紀錄；其中P1–P4文件缺口已由本輪主報告、來源對照與完整索引修正。目前驗收以 outputs/research/MS-03/completion_20261115/requirement_audit.csv 為準；科學未知仍保留。

# MS-03 獨立驗收：234e58a8a0a0a9966e97e1b13d7ccc587cf3e8aa

核對日期：2026-11-15（Asia/Taipei）。驗收對象是既定 MS-03 研究交付，與「所有科學未知都已解決」分開判定。此稽核沒有變更來源檔或使用驗證綠燈代替科學證據。

## 權威範圍

- 原始任務：本機 `docs/prompts/MS-03.txt`，實際全文已讀。固定遠端 main 的同路徑返回404，因此不能聲稱提示詞已存於該遠端版本。
- 固定 main：`234e58a8a0a0a9966e97e1b13d7ccc587cf3e8aa`。
- 實讀：主報告521行、candidates 2列、evidence 32列、prior_work 8列、search_log 45列、頂層manifest、local_validation README/analysis_summary、CRISM QA、official_resources README、bd1500 results、original_tables_followup README、gap_completion README/gap_status，以及新增radar_diagnostic_summary。
- 檔數比較由固定 Git tree 的三個MS-03專用目錄計算；不含其他點或shared_validation中MS-03平鋪副本。

## 原始要求逐項判定

|要求|當前權威證據|判定與必要修正|
|---|---|---|
|固定火星位置／界線|candidates.mars_id、manifest.mars_coordinates、mars_reference；57.75N/242.25E、57.50–58.00N/242.00–242.50E|符合；保持planetocentric/east-positive，名義格非著陸區。|
|至少兩個有據地球候選、範圍、具體用途|candidates E01 W點、E02 AD1；GIS185多邊形及UTM33N bbox|已提出2候選。E01只能稱單站錨點，無擅設radius；E02起始事件座標不能寫成sensor或bbox中心。兩候選不等於兩個已成立的火星配對。|
|兩候選四面向|E01 EV08–13/19–24；E02 EV14–18/25/29；MS03 EV01–07|四面向均有證據或明示unknown。W地形只有點位/現地描述，不應叫已完成共同尺度坡度比較；AD1熱/雪是未證同址的區域context。數據缺口符合原文「沒有可比較的數據就標未知」。|
|每數值定位、單位、期間、支撐、品質|evidence完整17欄無空欄；manifest.sources；各局部retrieval/source_read_log|主要可追溯；儀器在個別文字中，不是每列都有獨立instrument欄。宜建立source crosswalk，將歷史來源與local evidence明確連結。|
|同地同用途先例、分類、方法差異|prior_work PW01–08；search45列；Ulrich2011 Table3/4重現|原始兩候選已查；地球代理會補McKay2026同W站直接先例。不可因沒查到特定MS03論文就聲稱全球新穎。|
|候選處置、下一步、可/不可外推|candidates disposition/reason/next_step、gap_status6列|處置合理，但E01 enum仍pending_raw_series且描述已取得；E02仍只寫CTX，未納MOC。應修正現行機讀狀態。|
|SWIM/TI/MCS/坡度不得誤解|EV01/03–07限制；report相關段落|符合。Piqueux0.103161566m是條件熱模型，不是實測冰深；SHARAD採樣間隔不能當15m以下界面真值。|
|6項指定交付、來源hash及未解缺口|report/candidates/evidence/prior/search/manifest存在|檔案存在，但有效內容未完整匯入後續科學包，需下列P1–P4修正。|
|只改自己目錄、分支/PR、不合main|PR7及後續已由先前授權合併；本次尚未發佈|本次應以目前main另開補充分支/PR，因原研究分支/PR已合併。只寫MS03專用路徑，不直接合main。|
|座標/單位/缺值/引文核對|既有validators及本次獨立檔內容查核|可驗證格式/重現；不能藉test pass證明冰、成因、時鐘或novelty。|

## 必須修正的有效現況整合問題

### P1：主報告完全未包含後續局部科學證據

在固定main主報告，`local_validation`、`MOC`、`CRISM`、`SHARAD`、`MRDR`、`Daubar`均出現0次；主文開頭仍是8f6d313版本的149標籤交接。現行main卻已取得MOC、原始mapping光譜、MRDR、同軌雷達/雜波和目錄原表查核。

修正：保留原報告原樣到history，新report以有效現況取代一輪輪交接。列出每項真正獲得的證據、支撐範圍及未知，連到對應README/表/原始byte範圍。

### P2：頂層manifest覆蓋範圍未向後續擴展

- 三個MS03專用目錄有536檔。
- 頂層manifest.outputs只列94檔，且0條local_validation。
- local_validation有441檔；頂層manifest本身亦未列入自身hash（此點正常，避免自引用）。總共442條未進頂層outputs。
- 已列94檔與固定tree沒有size衝突；不能把這個覆蓋問題錯報成已證明hash損毀。

修正：頂層列明歷史manifest的scope；新增完整當前文件inventory或串接各子manifest，含本次基準SHA與來源hash。驗證實際檔案hash，區分retained與ignored/可重取/未取得。不能說原始大型全球影像、未取得的logger和三份原表已全部在GitHub。

### P3：機讀表停在舊階段

- evidence只有32列，沒有MOC/MRDR/CRISM/SHARAD局部證據；search_log45列只到149標籤。
- E01 disposition `retain_known_method_reference_pending_raw_series` 與已取得作者處理匯出矛盾；改為明示processed export已得、未處理logger/校時缺件未得。
- E02 data_status以3CTX/0HiRISE為主，未提MOC，應更新，仍維持general-method disposition。
- EV28保留已取代615列狀態並指EV30，歷史允許，但要明確active/superseded，不讓機讀下游把615當unknown locations。
- EV22同列HOBO差值應在該列限制明文加入不同logger真實同步未獨立證實；不是只在報告遠處說明。

修正：追加/索引新證據與各輪search/read log，保留歷史列與來源；明確當前狀態，不覆寫原始數值。

### P4：來源ID與頂層source catalog不完全連結

EV26/27/28/29/30/31/32使用MOR1/2/4/5/9/11，不在頂層manifest.sources。各列有直接URL與locator，並非所有引文都斷；但頂層source lookup不完整。U5目前只作W資料庫identity bridge，沒有直接先例分類。

修正：將MOR與各LV/GAP來源串入source crosswalk，保留read_scope/date/license；地球新先例需按實讀範圍新增prior row與search/read記錄。

## 科學仍未解與可執行驗證protocol

|未知|可執行protocol|成立條件／仍不成立時的輸出|
|---|---|---|
|Mars閉合多邊形是否可量測|對固定格內原像製作預先固定取樣網格；記錄PSF/曝光/壓縮/照度與配準誤差；兩位盲判者獨立描邊，量測重複性；將AD1原像按實際sampling與噪音降級作辨識測試|若邊界無重現性，輸出不可辨識及檢出限制，不能填0或用AD1替代Mars。現有3MOC窗不足以作全格普查。|
|光譜差值根因及冰檢出|先取得producer1.03.94實際設定/優化係數與同源前後中間陣列；逐stage定位差值。另以同模式/季節/幾何控制、雲霜及儀器mask、已知光譜端元/噪音注入，事先定義檢出/誤報率|無執行材料不能精確歸因；無QA/控制不能用負BD作無冰結論。既有SIS只解釋AL公式不必等於SU，不解釋本格每個殘差。|
|地下反射界面與冰深/量|核對原始USRDR/GEOM/同軌clutter時間支撐、有效帶寬與表面追蹤；在獨立pass重現同一候選反射；枚舉地形/旁瓣/電離層/處理假說；若有可信delay，再以明列介電假設傳播不確定度|全crop argmax不作界面；觀測/模型power不相減；沒有可靠reflector保留unknown。15m真空range resolution不能獨立核實0.10m條件模型界面。|
|三原表同址成員|取得Cohen-Zada原data+headers、Levy全S1、Dundas全S4；以原座標/命名與影像ID查footprint；分開point與影像面積；retain失敗HTTP|Daubar1203事件0格內點僅是該表結果，不代替三原表；缺表維持unknown。|
|W logger真實時間與跨儀器同步|取得原始W logger、校準.m/.xls/.CR1及2012時鐘操作紀錄；逐步重現處理與印出時標；以獨立時鐘/事件證明修正，再分別核HOBO時基|先保留同檔描述；不能自動平移4h、cross-join、估lag/diffusivity或轉Mars冰深。|
|全球新穎性|公開可重跑keyword/coordinate/影像ID策略，逐篇閱讀與引用定位；把已讀先例的同址/用途/尺度/方法差異寫出|有限搜尋不形成全球排除證明；不許首次/最佳主張。|

## 可作與不可作的完成宣告

原始任務已明文允許證據不足、unknown及待補證據交付。因此兩候選、四面向、先例、處置、資料與驗證完整整理後，可以說「MS-03既定研究交付已整理並驗收」。它不要求偽造兩個成功配對或把每個物理未知變成已知。

目前證據不能說「所有MS-03科學問題均已解決」：冰存在/深度/含量、格內可量測多邊形、MRDR每像素執行歸因、W同步與三原表成員仍有實質缺件。完成文件與計算QA不會補出這些真值。最新使用者的廣義全解要求因此仍未獲證實，不能因停工或推PR就勾成科學全解。
