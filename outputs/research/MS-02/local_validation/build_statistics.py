#!/usr/bin/env python3
"""Current descriptive counts; no scientific validity inference and no historical verifier side effects."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
rows=[]
for f in ['local_prior_work.csv','mars_ice_evidence.csv','analog_validation.csv','search_log.csv','claim_corrections.csv','product_footprints.csv','workbook_inventory.csv','wendt_core_locations.csv','wendt_quality_flags.csv']:
 rows.append((f,len(list(csv.DictReader((P/f).open(encoding='utf-8-sig'))))))
v=json.loads((P/'revision_verification.json').read_text());m=json.loads((P/'manifest.json').read_text())
s=['# MS-02 當前資料盤點（非報告正文）','','- 日期：2026-11-15；保留遠端基準：`'+m['preserved_remote_head']+'`。','- 原版統計可由該提交取得；下表更新到本輪證據。','','| 檔案 | 資料列 |','|---|---:|']
s+=['| '+f+' | '+str(n)+' |' for f,n in rows]
s+=['','- CTX：5個名義足跡、5張browse。','- CRISM：177筆目錄含59個IF科學產品；取得1組L科學立方體＋DDR，ROI912像元中心。','- SHARAD：3條段，194個posting欄，並非194獨立觀測單元。','- 熱模型：ROI一個0.5°像元；約29.636km南北 ×17.938km東西。','- 驗證：`verify_revision.py` '+str(v['checks_count'])+'項通過；包括'+str(v['hashed_files_verified'])+'個檔案hash。','- 檢查通過只代表數據／來源／範圍一致，不是冰驗證通過。','- 舊verification.json是歷史結果，不當本輪檢查。','']
(P/'statistics_summary.md').write_text('\n'.join(s));print('Statistics updated')
