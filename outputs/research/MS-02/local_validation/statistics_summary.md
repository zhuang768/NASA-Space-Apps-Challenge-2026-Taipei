# MS-02 當前資料盤點（非報告正文）

- 日期：2026-11-15；保留遠端基準：`ef5eb162b1df0919b8d6dd780782896188607b2c`。
- 原版統計可由該提交取得；下表更新到本輪證據。

| 檔案 | 資料列 |
|---|---:|
| local_prior_work.csv | 15 |
| mars_ice_evidence.csv | 25 |
| analog_validation.csv | 9 |
| search_log.csv | 223 |
| claim_corrections.csv | 16 |
| product_footprints.csv | 185 |
| workbook_inventory.csv | 32 |
| wendt_core_locations.csv | 12 |
| wendt_quality_flags.csv | 2 |

- CTX：5個名義足跡、5張browse。
- CRISM：177筆目錄含59個IF科學產品；取得1組L科學立方體＋DDR，ROI912像元中心。
- SHARAD：3條段，194個posting欄，並非194獨立觀測單元。
- 熱模型：ROI一個0.5°像元；約29.636km南北 ×17.938km東西。
- 驗證：`verify_revision.py` 231項通過；包括211個檔案hash。
- 檢查通過只代表數據／來源／範圍一致，不是冰驗證通過。
- 舊verification.json是歷史結果，不當本輪檢查。
