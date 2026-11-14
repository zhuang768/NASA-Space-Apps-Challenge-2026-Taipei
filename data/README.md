# 資料目錄

| 位置 | 內容 | 保留理由 |
|---|---|---|
| raw/mars/ | MOLA、TES 與遮罩、SWIM、MY34／MY35 沙塵 | 火星處理與測試實際輸入 |
| raw/mars/temperature/ | MEDA CSV／PDS4 XML | 亮溫探索與品質缺口追溯 |
| processed/mars_stack_0p5deg.nc | 火星描述網格 | 內部檢查輸入；非地球排名 |
| raw/earth/ | 本機地球下載（Git 忽略） | 地球搜尋／氣候背景；隊友完整批次另行交接 |

原始檔維持原始位元組，不能為縮小 repo 或美化格式改寫。來源與 checksum 見 [火星 profiles](../outputs/mars_profiles/profiles.json) 及 [溫度紀錄](../outputs/mars_temperature/summary.json)。Git 歷史不因工作區刪檔而縮小，本次沒有重寫歷史。
