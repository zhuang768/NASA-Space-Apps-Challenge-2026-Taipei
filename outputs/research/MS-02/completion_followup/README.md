# MS-02 本輪證據與分析索引

日期：2026-11-15（Asia/Taipei）。固定火星點 **52.75°N、168.25°E**；名義範圍 **52.50–53.00°N、168.00–168.50°E**。起始主線為 `521740108050ba16e406f8becb67a786179ff8bd`。

本輪已整理可核對的資料修正、來源紀錄與可重現分析。**整體科學目標仍未完成：`all_ms02_problems_resolved=false`、`scientific_completion=false`。** 缺少獨立冰真值、完整光譜處理及其他指定原件的項目仍是未解項；填入「未知」或通過程式檢查不會使它們變成完成。

本目錄是人類撰寫正式報告時使用的證據筆記。`docs/research/MS-02/report.md` 依既有要求逐位元保留，SHA-256 為 `1f603ac5a125befdd34af97c14a0c24b3a3591f2b6289a07d4ea62abf7caa0f4`。**該舊稿仍含已由本輪資料表與筆記修正的歷史敘述，不能當作目前證據狀態的權威版本。** 原稿未代寫或改寫。

## 閱讀入口

- [需求與狀態](requirements.csv)：逐項區分已交付的資料工作與尚未滿足的科學驗證。
- [新證據索引](evidence_index.csv)：把六組工作連到實際資料、程式與來源。
- [機器可讀完成狀態](completion_status.json)：保留完整未解原件清單。
- [固定版本及保存證據](base_provenance.json)：起始 SHA、固定範圍與原稿雜湊。

| 工作 | 本輪可核對結果 | 判讀界線 |
|---|---|---|
| [資料對齊](audit/audit_notes.md) | 修正54個舊欄位、新增11列；4個地球候選均具4面向紀錄；22列原始先例；14項交接數值核對通過 | 更正紀錄及衍生資料一致，不構成新獨立觀測 |
| [熱模型](thermal/thermal_notes.md) | 重核5份原檔雜湊，保留81格原生值；補讀2026公開方法、0.5°輸出與等權規則 | 約0.45m仍是條件式模型；新規則單分量不是實際SWIM像元或機率 |
| [雷達](radar_notes.md) | 194欄、54組敏感度、相對回波對齊及測線相交檢查 | 未成立獨立地下冰反射判讀；零連續支援不代表無冰 |
| [光譜](spectral_notes.md) | 912個像元無一具完整55波段；890個具有其餘54波段；22個全缺；負I/F保留 | 數值可用比例不能替代波長、品質及材料／冰判讀 |
| [影像／氫](morphology_hydrogen/notes.md) | 5景、10組重複足跡交集；MONS實際尺度與數值表來源釐清 | 名義覆蓋不等於有效影像或變化測量；本格WEH仍為null |
| [地球驗證](earth/earth_notes.md) | 來源與用途分離、CRIM非唯一性、可取得author-calibrated export／通道支援另列 | 沒有以不同測線、年份或處理版本拼出獨立冰真值；最終通道判定以該包現行紀錄為準 |

完整篩選檔為58,238列×54欄，MS-02目標唯一。23,035,176-byte整合Excel已核對遠端位元及ZIP CRC，實際有**32張工作表**；舊稿33張的說法已在現行資料紀錄更正。兩個檔案原已存在固定遠端版本，本輪未以重新上傳相同檔案冒充新資料。

## 目前仍未解決的證據需求

1. MS-02同位置、獨立的冰存在／界面深度／含量真值。
2. CRISM原55列detector-row資料、精確WA校正、場景sample/line對應與完整品質／大氣／熱／光度處理。
3. CTX實際影像校正、SPICE投影／正射、有效遮罩、局部地形與可量化的重複影像變化誤差。
4. Pathare2018 TableS1的MONS數值及適用誤差；細存儲網格不代表0.5°獨立觀測。
5. 本格熱觀測日期／數量、殘差／RMS／CI、處理階段轉製鏈與實際SWIM分量／遮罩／版本關係。公開2026方法權重已補出，逐像元發布運算尚未重建。
6. 地球案例原始資料、逐探頭校準／校時／位置關係、同位置冰與材料真值及匹配邊界控制。已校正作者export、文獻模型與合成計算有各自用途。
7. MS-02實際覆土材料／厚度／累積率；整層沙塵光學厚度無法直接換算這些量。

具體原件與影響見 `completion_status.json`。來源存取失敗、檢索無結果、未取得原件、已有數值但尚無有效科學判讀均分別保留；沒有把它們寫成「無冰」或「資料不存在」。

## 重現及驗收

六個現行檢查入口如下；它們讀取各包實際輸入／衍生表，寫入各自現行verification，保留舊歷史驗證紀錄。

```sh
python3 outputs/research/MS-02/completion_followup/audit/verify.py
python3 outputs/research/MS-02/completion_followup/earth/verify.py
python3 outputs/research/MS-02/completion_followup/radar/verify.py
python3 outputs/research/MS-02/completion_followup/spectral/verify.py
python3 outputs/research/MS-02/completion_followup/thermal/verify.py
python3 outputs/research/MS-02/completion_followup/morphology_hydrogen/verify_support.py
```

現行具名檢查共**362項**（128+83+9+122+20），地球包另有來源／雜湊／計算／export斷言，兩者分開計數。檢查通過的範圍是資料與數值重現，未替缺少的外部觀測提供證明。各包的分析重算方式及依賴在其筆記／程式說明內；熱模型分析需指定5份原始檔目錄，離線驗證可使用交付的81格摘錄。

整合manifest涵蓋本輪產物雜湊；`finalize.py`與`verify_followup.py`由整合步驟更新／執行。不要執行歷史builder覆寫現行資料。GitHub成功提交、PR內容及是否合併須由遠端回讀另外確認；本索引本身不宣稱已上傳或已合併。

補充：本輪再核對Daubar2022原始目錄1,203筆有限座標，固定MS-02格內零筆目錄撞擊點；只限目錄點位，不代表無冰、無其他撞擊或影像無覆蓋。原表欄名與經度方向已個別查核，來源與程式見 `audit/catalogue_roi_check.json`、`audit/catalogue_roi_check.py`，此檢查另外計數。
