# 專案資料總表

主要閱讀檔案：**[NASA_Space_Apps_2026_All_Data.xlsx](NASA_Space_Apps_2026_All_Data.xlsx)**。

這本 Excel 將專案既有的科學 CSV、JSON／GeoJSON、候選結果、研究查核、報告內容與原始檔案索引放在一起。總覽在第一頁，其餘頁籤依資料用途分類，可篩選、排序並追溯來源。

交付版採白底黑字與緊湊資料列；全部工作表名稱、標頭及可讀內容統一為英文。來源原檔仍是權威的逐字紀錄；Excel 中的英文翻譯不是原文封存，實際檔名、路徑及技術識別碼依來源保留。

## 收錄方式

- CSV 保留完整資料列、來源檔及來源列號。三份 MEDA 原始 CSV 全部保留，不在匯入時刪掉品質較差的紀錄。
- JSON／GeoJSON 除了可讀的主題表，另以欄位路徑與型別保存原值，避免摘要漏掉細節。
- 報告按來源文件與段落收入，圖片、衛星網格、HDF／NetCDF／TIFF、壓縮檔及 XML 標籤由檔案索引連回原檔。大型原檔保留原位置，不再複製一份。
- 原始資料、處理後結果、敏感度版本與人工查核分開標示。缺值保持缺值，不補成零。
- 網站、套件、Git 內部資料與憑證不收入這份科學資料總表。

## 閱讀限制

- 地球兩版皆採 **100 km 視窗**，採樣間距分別為 4 km 與 10 km。以 `run_id + candidate_id` 區分，不能只用候選編號合併。
- 火星發現原表有 **24 點**，其中 **15 點**有第一輪文獻查核，**4 點**暫留供報告。未查的九點不會標成已查。
- 現有地球排名使用地形。其他環境資料是背景，尚未形成完整四主題排名。
- POWER 的 `YYYY13` 是年值，不是第十三個月。POWER 氣溫、MEDA 亮溫、區域溫度背景及 TES 熱慣量各自保留原意義。
- 實驗性分數不是信心、百分比或登陸核准。新穎性尚未通過。
- 這是產生當下的資料快照。修改 Excel 不會重跑 Python 科學流程，也不會自動寫回原始 CSV／JSON。

## 檔案分類

| 目錄 | 內容 |
|---|---|
| 本目錄 | 唯一一份交付 Excel |
| `support/` | 匯入清單與來源對照。大型中間資料於驗證後清除 |
| `review/` | 盤點、保全比對及匯入驗證紀錄 |
| `previews/` | 工作表視覺檢查用圖片 |
| [../../docs/research/](../../docs/research/) | 研究報告及導覽 |
| [../../scripts/reporting/](../../scripts/reporting/) | 可重現的資料匯整與 Excel 產生程式 |

塵埃衍生資料保留原有 [CC-BY-SA-3.0 授權說明](../mars_profiles/LICENSE-data.md)。其他來源與授權依原始資料紀錄。

## 本輪成果與重建

已交付 24 個工作表，收錄 106 個科學來源檔、159,418 筆 MEDA 原始紀錄、35 份 JSON／GeoJSON 原值及 44 份報告內容，另列 426 項專案檔案索引。來源到資料包、資料包到 Excel 均逐格核對通過。

原生資料與科學分數沒有更動。大型原始資料表使用串流方式寫入同一本 Excel，以降低編製所需記憶體。文字欄保留日期的原始拼寫、時區與微秒。

需要依最新來源重建時，在專案根目錄依序執行：

1. `python scripts/reporting/prepare_workbook_data.py`
2. 使用 Codex 隨附 Node 執行 `scripts/reporting/build_project_workbook.mjs`。
3. 使用 Codex 隨附 Python 執行 `scripts/reporting/verify_project_workbook.py`，逐格核對並產生最終總覽顯示值。
4. 使用同一個 Node 執行 `scripts/reporting/build_project_workbook.mjs --overview-preview`。
5. 原版建立後，保全原版備份及對應的來源文字清單、完整英文翻譯映射。現有快照的三個檔案是 `review/plain_english/original_workbook.xlsx.bak`、`review/plain_english/source_strings.json` 及 `review/plain_english/translations_merged.json`；請保留這組檔案，不以新重建檔覆蓋既有備份。
6. 重現目前英文交付版時，執行 `python scripts/reporting/plain_english_workbook.py --apply`。程式預設讀取上述備份與映射，套用英文、白底黑字及緊湊列高，並寫入 `review/plain_english/verification.json` 驗證紀錄。

英文套用程式只使用已完成的映射，不會自動翻譯新增或變更的內容。若最新來源與既有快照不同，需先另外保全新原版、建立與其雜湊一致的來源清單並完成翻譯映射，再用 `--source`、`--source-strings`、`--translations` 指定新的一組檔案執行 `--apply`。

`stream_raw_sheet.py` 是作者程式自動呼叫的大型原始表寫入步驟。驗證通過後可清除 `support/workbook_data.json`、`support/workbook_base.xlsx` 及其 inspect 中間檔；原始 CSV／JSON、最終 Excel、來源雜湊與驗證紀錄仍保留。
