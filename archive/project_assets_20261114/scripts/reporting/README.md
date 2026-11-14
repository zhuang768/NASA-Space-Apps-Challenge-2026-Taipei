# 資料總表產生程式

- `prepare_workbook_data.py`：讀取專案現有科學資料，準備完整資料表與來源對照，不重新評分。
- `build_project_workbook.mjs`：將準備好的資料寫成同一本 Excel，設定篩選、凍結標題、格式及總覽，輸出視覺檢查與驗證紀錄。

成果放在 `outputs/consolidated/`。程式不移動大型原始資料、不改 `analog/` 的科學計算。

Excel 作者程式使用 Codex 隨附的 `@oai/artifact-tool`。優先讀取 `CODEX_PRIMARY_RUNTIME_NODE_MODULES`；此 Mac 的後備路徑為 `~/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules`。
