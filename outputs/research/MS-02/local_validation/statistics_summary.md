# MS-02 統計彙整（僅計數與核對結果；非報告正文）

目標：MS-02，52.75°N、168.25°E；branch research/ms-02-earth-analogs；HEAD `ef5eb162b1df0919b8d6dd780782896188607b2c`

## 1. 檔案與列數

| 檔案 | 資料列 |
|---|---|
| candidates.csv | 4 |
| claims.csv | 9 |
| evidence.csv | 61 |
| footprint.csv | 9 |
| prior_work.csv | 20 |
| search_log.csv | 65 |
| local_validation/local_prior_work.csv | 14 |
| local_validation/mars_ice_evidence.csv | 25 |
| local_validation/analog_validation.csv | 9 |
| local_validation/search_log.csv | 60 |
| local_validation/scale_gap_resolution.csv | 8 |


## 2. 證據表 evidence.csv（61 列）

依候選：
| candidate | 列數 |
|---|---|
| MS-02-E03 | 20 |
| MS-02 | 12 |
| MS-02-E04 | 12 |
| MS-02-E01 | 11 |
| MS-02-E02 | 6 |

依面向：
| facet | 列數 |
|---|---|
| 水/冰 | 26 |
| 地形 | 14 |
| 熱性質 | 11 |
| 大氣/沙塵 | 10 |

依證據類型（取第一個詞）：
| 類型 | 列數 |
|---|---|
| 文獻 | 22 |
| 實測 | 21 |
| 產品推估 | 10 |
| 未知 | 7 |
| 本文推導 | 1 |


## 3. 主張 claims.csv

| claim_id | 狀態 |
|---|---|
| C1 | 支持 (僅 CS-1) |
| C2 | 部分支持 (峰值期，非長期平均) |
| C3 | 數量級一致，非同址同年 |
| C4 | 支持 (ADE 結構；與 CS-1 相距 ~6.0 km，與雷達無關) |
| C5 | 作者結論；無獨立冰真值 |
| C6 | 未證實 |
| C7 | 不成立 (不能當同址) |
| C8 | 不可轉換 |
| C9 | 證據不足 |


## 4. 足跡 footprint.csv 幾何狀態

| 狀態 | 數 |
|---|---|
| stated | 4 |
| unknown | 4 |
| bbox stated; site outlines not obtained | 1 |


## 5. 先例 prior_work.csv 分類

| 分類 | 數 |
|---|---|
| 部分重疊 | 9 |
| 用途不同 | 9 |
| 證據不足 | 2 |


## 6. 地球候選處置

| id | 處置 |
|---|---|
| MS-02-E01 | 保留 |
| MS-02-E02 | 待補證據 |
| MS-02-E03 | 降為一般方法參照 |
| MS-02-E04 | 待補證據 |


## 7. local_validation 先例（14 列）

| 分類 | 數 |
|---|---|
| 附近／大區域 | 9 |
| 格內不同用途 | 2 |
| 格內同用途(全球產品；值未取得) | 1 |
| 位置不明 | 1 |
| (none found) | 1 |


## 8. 尺度缺口判定

| id | 主題 | 狀態 |
|---|---|---|
| SG-01 | terrain | Answered at 3.7 km only |
| SG-02 | thermal | Answered as cell-scale descriptor; local material unknown |
| SG-03 | water-ice | Existence = insufficient evidence; depth/content unknown |
| SG-04 | atmosphere-dust | Answered as column context only; cover unknown |
| SG-05 | local material | CANNOT be answered |
| SG-06 | cover (overburden) | CANNOT be answered |
| SG-07 | morphology | CANNOT be answered |
| SG-08 | neighbourhood representativeness | Answered as regional context; does not resolve SG-05-07 |


## 9. MS-02 格尺度數值（來源 hand-off main 共享資料）

| 項目 | 值 |
|---|---|
| 格大小 km (EW×NS) | 29.636 × 17.938（約 531.6 km²） |
| MOLA 平均 m | -3898.719 |
| MOLA 坡度 平均/最大 ° | 0.3018/0.9253 |
| MOLA 起伏 m | 117.0 |
| TES TI 平均/中位/範圍/標準差 | 217.269/213.0/177.0–276.0/18.246 |
| TES 有效格 | 93/100 |
| SWIM 0–1 m 平均 | 0.693 |
| SWIM 1–5 m 平均 | 0.6225 |
| CDOD MY34 平均/p95 | 0.1254/0.2400 |
| CDOD MY35 平均/p95 | 0.1101/0.1731 |
| 最近 Morgan 2025 冰點 km | 389.0 (Site 46) |
| 距 Bramson/Viola/Ramsdale/Séjourné km | 463.6/421.1/628.7/2534.5 |


## 10. 核對結果（本次重跑）

| 腳本 | 結果 | 摘要 |
|---|---|---|
| local_validation/verify_local_validation.py | PASS | PASS changes only under local_validation dirs |
| local_validation/verify_scale_gap.py | PASS | {"passes": 3, "fail": []} |
| verification.json（原 PR 腳本） | PASS | 14 checks |

