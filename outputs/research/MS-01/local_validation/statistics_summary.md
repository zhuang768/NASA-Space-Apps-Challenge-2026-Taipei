# MS-01 統計彙整（僅計數與數值；非報告正文）

目標：MS-01，56.75°N、72.75°E（56.50–57.00°N、72.50–73.00°E，約 29.6 × 16.2 km）

## 檔案列數

| 檔案 | 資料列 |
|---|---|
| mars_ice_evidence.csv | 4 |
| local_prior_work.csv | 6 |
| analog_validation.csv | 9 |
| search_log.csv | 17 |
| product_inventory.csv | 335 |
| catalogue_summary.csv | 15 |
| scale_gap_resolution.csv | 8 |

## ODE 目錄（nominal 足跡；不是有效像元）

| 資料集 | 查詢數 | 面相交 | 線相交 | 觀測組 |
|---|---|---|---|---|
| CRISM_MTRDR | 0 | 0 | 0 | 0 |
| CRISM_TRDR | 207 | 207 | 0 | 54 |
| CTX_EDR | 4 | 4 | 0 | 4 |
| HIRISE_RDR | 0 | 0 | 0 | 0 |
| HIRISE_RDRV11 | 0 | 0 | 0 | 0 |
| SHARAD_RDR | 6 | 0 | 6 | 6 |
| SHARAD_USGEOM |  |  |  |  |
| SHARAD_USGEOMV2 | 6 | 0 | 6 | 6 |
| SHARAD_USRDR |  |  |  |  |
| SHARAD_USRDRV2 | 6 | 0 | 6 | 6 |
| THEMIS_IRBTR | 34 | 34 | 0 | 34 |
| THEMIS_IRPBT1 | 8 | 8 | 0 | 8 |
| THEMIS_IRPBT2 | 17 | 17 | 0 | 17 |
| THEMIS_IRPBT4 | 12 | 12 | 0 | 12 |
| THEMIS_IRRDR | 35 | 35 | 0 | 35 |

## 尺度缺口判定

| id | 主題 | 狀態 |
|---|---|---|
| SG-01 | terrain | Answered at 3.7 km only |
| SG-02 | thermal | Answered as cell-scale descriptor; local material unknown |
| SG-03 | water-ice | Existence = evidence insufficient; depth = model only; content unknown |
| SG-04 | atmosphere-dust | Answered as column context only; cover unknown |
| SG-05 | local material | CANNOT be answered |
| SG-06 | cover (overburden) | CANNOT be answered |
| SG-07 | morphology | CANNOT be answered |
| SG-08 | neighbourhood representativeness | Answered as regional context; does not resolve SG-05-07 |

## 周邊（±2°）

81 個 0.5° 格；thermal_inertia 平均 304.279（257.964–340.212）；relief 平均 115.457（23.0–876.0）；ice_shallow 平均 0.492（0.228–0.735）；dust_my34_mean 平均 0.114（0.107–0.12）；slope 平均 0.381（0.105–3.448）

