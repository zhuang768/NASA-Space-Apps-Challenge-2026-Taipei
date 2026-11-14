# 火星日夜溫度：MEDA 實測資料接軌

本輪先接入 Perseverance／MEDA 的 calibrated TIRS 產品，研究範圍是 Jezero 探測車附近、LMST sol 700–702 的短期觀測。下載只選這三個 sol，沒有下載完整任務資料。地球端工作仍交由隊友。

## 官方來源與物理量

- [NASA PDS MEDA 說明](https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/PERSEVERANCE/meda.html)，資料 DOI：https://doi.org/10.17189/1522849 。
- [PDS calibrated archive](https://atmos.nmsu.edu/PDS/data/PDS4/Mars2020/mars2020_meda/data_calibrated_env/sol_0660_0779/)，逐 sol 取得 CSV 與 PDS4 XML 標籤。
- 原始 XML 將 `GROUND_TEMP` 定義為 **Ground brightness temperature**，單位 kelvin；`GROUND_TEMP_UNCERTAINTY` 是其 standard deviation。`AIR_TEMP` 不作替代。
- [MEDA 儀器論文](https://doi.org/10.1007/s11214-021-00816-9)提供儀器背景。實際讀值、欄位與期間以下載產品及標籤為準。

這是紅外線地面亮溫，若要與地球 MODIS 動力地表溫度直接比較，仍需處理光譜、發射率、觀測幾何與時間配對。MEDA derived TIRS 的長波輻照度也不能直接改名為量測地表溫度。TES 熱慣量與溫度仍分開。

## 執行

```sh
.venv/bin/python -m scripts.process_mars_temperature --download
.venv/bin/python -m scripts.profile_mars --strict
```

`profile_mars --strict` 只要求核心地形／熱慣量／冰／沙塵來源齊全，不能解讀為 MEDA 品質已通過。

前者從官方目錄發現實際檔名；若同一 sol 出現多個版本，停止下載，要求人工核對。既有檔案會重用。讀取時核對標籤欄位、單位、物理量與資料列數；來源網址、LID、版本、UTC 期間、位元組數、SHA-256 寫入 `outputs/mars_temperature/summary.json`。重現時應核對已提交的 SHA-256，以免重用的本機檔案曾遭修改。

`provisional_hourly.csv` 是包含品質未知／不通過讀值的探索摘要，不是已確認可用的科學結果。`summary.json` 分列 `qualified_windows` 與 `provisional_unqualified_windows`。Mars profile 匯出將完整內容放在 `rover_temperature_context`；原本的區域 `surface_temperature` 缺值狀態保留。沒有將局部資料外插到 Arcadia、Gale 或全球網格，沒有變更相似度權重。

## 時間與品質規則

以下是專案分析假設，並非 NASA 指定的日夜標準：

- 以 LTST 字串中的 sol 分組，不能用檔名的 LMST sol 代替。sol 700 的檔案包含 LTST sol 699 晚間資料。
- 日間固定為 LTST 12:00–15:00，夜間為 00:00–03:00，右界不含。它們是時鐘區間，沒有以太陽高度判斷明暗。
- 先取每個當地小時內的中位數，再對窗口內的小時中位數取中位數。至少要有兩個小時格才能產生窗口值。這只能約束時間分布，不能證明整個窗口連續觀測。
- 只有同一 LTST sol 的兩個窗口都足夠，才輸出 sampled day–night contrast。此值不是完整日最高減最低，也未確認兩個窗口看的是同一塊地面。
- 正溫度與非負有限 uncertainty 才進探索摘要。完整品質篩選另外要求：輪子不在下視視野、低傾斜、地面足跡不在陰影、HGA 關閉、SkyCam 關閉、車體靜止，六項旗標皆為 1。這是保守的專案篩選選擇，尚需儀器專家審查。
- 任一旗標空值／未知都不算通過；逐旗標公開 good、bad、unknown 數量。不把儀器 uncertainty 轉為窗口信賴區間。

原始 sol 700 檔案有 47,774 列，其中輪子視野、HGA、SkyCam 三項旗標為空值，因此完整品質篩選後沒有合格列。程式應如實呈現 `quality_incomplete`，不能因想要日夜差數字就刪除品質要求。其他 sol 的實際統計見匯出檔。

## 仍缺什麼

1. 品質未知旗標的官方解釋或補充證據，才能決定哪些 MEDA 讀值適合正式用途。目前探索值不納入評分或確認覆蓋。
2. 足夠季節／Ls 覆蓋，以及 rover ancillary 位置、姿態、地面足跡與移動紀錄，才能審查同場配對與代表性。這次僅三個 sol，不能代表火星年度溫度。
3. 全球或指定目標區、具有明確物理定義與日夜觀測時刻的可比較溫度產品。Arcadia 仍無這批近地面資料。
4. Gale 可另接 [REMS 地面亮溫](https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/MARS/curiosity/rems_temperature.html)，須先核對該產品 confidence 與長／短期不確定度。這次未納入。
5. [TES Data Tool](https://tes.asu.edu/data_tool/)是後續軌道資料路徑；查詢需要填 email 並由服務寄回資料，本輪沒有提交查詢。THEMIS 圖像色階／DN 也沒有當成 kelvin 使用。

原始產品由 NASA PDS 提供；引用 MEDA 資料 DOI 及儀器論文，使用條件依原提供者。這份說明不將 MEDA 資料重新授權為沙塵資料使用的 CC-BY-SA。程式授權依 repo 授權檔；新增模組不另行宣稱 NASA 認證。

## AI 使用紀錄

2026-11-14：OpenAI Codex 協助尋找官方資料、實作 MEDA 下載／PDS4 驗證／時間與品質處理、接入火星報告及撰寫測試與本說明。未使用 C2C，未生成或補造溫度讀值。

## 本輪完成與驗證

已完成公開資料下載、PDS4 欄位／列數／單位核對、來源與 SHA-256 紀錄、LTST 分組、品質篩選，以及 Mars profile 匯出整合。日夜數值目前屬探索摘要；未知旗標補齊前，正式溫度比較仍未完成。

測試涵蓋未知旗標不通過、跨 sol 不配對、錯誤單位／列數拒收、小時等權避免採樣頻率偏差，以及非法時間／缺值排除。測試合成資料只留在 tests，沒有混入資料產品。

實際下載結果：3 組 CSV／XML，共 159,418 筆；UTC 2023-02-07 至 2023-02-10（各產品實際起訖與觀測間隙見 manifest）。輪子視野、HGA、SkyCam 三項旗標在全部 159,418 筆均未知；完整品質篩選後為 0 筆，正式合格窗口保持未知。

實際執行結果：`ruff check .` 通過；`pytest -q` 為 57 passed、8 個既有警告（Affine、全 NaN 分位數與陣列轉 scalar）。下載／處理指令與 `profile_mars --strict` 均完成。另核對兩份匯出的溫度內容一致（排除各次匯出時間戳），且所有區域 surface_temperature 仍保留 missing。沒有部署網站。

| 狀態 | 本輪交付 |
|---|---|
| 已完成 | 3 個 sol 的真實資料與標籤、來源紀錄、可重現處理、品質缺口與火星報告整合、測試 |
| 示範／探索 | 含未知／不通過旗標的日夜亮溫摘要，獨立標示且不進正式評分 |
| 待確認 | 缺失品質旗標的意義、足跡／姿態配對與專家審查 |
| 尚未完成 | 全球／區域可比較動力地表溫度、全年季節覆蓋、Gale REMS 與 Arcadia 溫度資料 |
