# 地球端資料整理與下載規劃（對應火星端管線）

本文件整理**地球端**如何對齊隊友 A 在 `analog/` 已完成的火星資料，讓你在取得 **Earthdata Login** 後能立刻接軌，並在還沒取得帳號前先完成準備與免登入資料預覽。

> [!IMPORTANT]
> **分工邊界**：`analog/`、`scripts/`、`tests/` 由隊友 A 與 Cursor 維護，這裡只整理規格與下載步驟，不更動程式碼。

---

## 1. 火星端已完成什麼（我們要對齊的目標）

檢視 repo 最新進度（截至 `ccf4e07`），火星端已具備四個面向的資料模組：

| 面向 | 火星端檔案 (`analog/`) | 資料產品 | 原始解析度 | 涵蓋範圍 | 單位／數值 |
| --- | --- | --- | --- | --- | --- |
| **1. 地形** | `analog/mars.py` + `terrain.py` | MGS MOLA (`megt90n000eb.img`) | 16 px/deg（~3.7 km） | 全球 | 公尺 → 轉成 `slope_deg`、`relief` |
| **2. 溫度** | `analog/mars.py` | MGS TES 夜間熱慣量 (`global_ti_night_2007.img`) | 20 px/deg（~3.0 km） | 全球 | `J m⁻² K⁻¹ s⁻⁰·⁵`（5–5000） |
| **3. 水／冰** | `analog/swim.py` | SWIM 2.0 地下水冰一致性 (`SWIM2_c0_1.tif`, `SWIM2_c1_5.tif`) | 20 px/deg | **±60° 緯度** | `-1`（無冰證據）到 `+1`（強冰證據） |
| **4. 大氣與沙塵** | `analog/dust.py` | Montabone v2.5 沙塵柱光學厚度（MY35 平常年、MY34 全球沙塵暴年） | 3°（~177 km） | 全球 | 年平均 `mean_cdod`（無因次） |

**對齊規則（來自 `README.md`）：**
- 火星 `1° ≈ 59 km`，地球 `1° ≈ 111 km`。
- 空間尺度對齊：以實際地面距離為準（火星 `1°` 網格 ≈ 地球 `0.5°` 網格；MOLA 3.7 km 對應地球 ~3–4 km 粗網格聚合）。
- 所有網格統一格式：`xarray.DataArray`，座標 `(lat, lon)`，緯度由北到南（遞減），經度 `-180` 到 `180`。

---

## 2. 地球端 Core 資料清單（進程式計算用）

| 面向 | 地球端資料 | Earthdata Shortname 參考 | 原始解析度 | 轉成什麼指標去比火星 | 是否需要 Earthdata Login |
| --- | --- | --- | --- | --- | --- |
| **1. 地形** | **NASADEM**（或免登入替代：Copernicus GLO-30 / ETOPO 2022） | `NASADEM_HGT` (v001) | ~30 m（需降採樣至 ~3–4 km 算坡度/起伏） | `slope_deg`（度）、`relief`（m） | NASADEM 需登入；**ETOPO / Copernicus 部分可免登入** |
| **2. 溫度** | **MODIS LST**（Terra/Aqua 地表溫度） | `MOD11C3`（月平均 0.05° ≈ 5.6 km）或 `MOD11A2`（8 日 1 km） | ~1–5.6 km | **日夜溫差（ΔT）**、年均高／低溫（作為熱慣量與極端溫度代理） | 是（Earthdata Login） |
| **3. 水／冰（乾旱度）** | **GPM IMERG** 降水 ＋ **SMAP** 土壤濕度 | `GPM_3IMERGM`（月平均 0.1°） / `SPL3SMP_E`（9 km） | ~9–11 km | 年均降水量（越低越乾旱）、表層含水量 | 是（Earthdata Login） |
| **3. 水／冰（植被扣分）** | **MODIS NDVI** | `MOD13C2`（月平均 0.05° ≈ 5.6 km） | ~5.6 km | NDVI 越接近 0 或負值代表越荒蕪、少植被（類比無植物火星地表） | 是（Earthdata Login） |
| **4. 大氣與沙塵** | **MODIS AOD**（氣膠光學厚度） | `MOD08_M3`（月平均 1°）或 `MCD19A2`（1 km） | 1° 或 1 km | 年平均 AOD（對照火星 `mean_cdod`） | 是（Earthdata Login） |

> [!TIP]
> **給程式端的關鍵省時建議**：做「全球粗網格相似度評分」時，直接抓 **L3 月平均／全球網格產品**（如 `MOD11C3` 0.05°、`MOD13C2` 0.05°、`GPM_3IMERGM` 0.1°、`MOD08_M3` 1°），檔案只有幾十到幾百 MB，比抓 1 km 每日切片快 100 倍！

---

## 3. 地球端免登入即可開始的工作（現在就能做）

在等待或註冊 Earthdata Login 的同時，地球端負責人可以先完成以下三件事：

1. **準備 Earthdata Login 帳號（供 `earthaccess` 使用）**
   - 前往 [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov/) 註冊帳號（免費，約 2 分鐘）。
   - 註冊後在帳號設定中勾選授權 `NASA GESDISC DATA ARCHIVE` 與 `LP DAAC` 應用程式（下載 GPM、MODIS、NASADEM 必備）。
   - 本機設定 `~/.netrc` 或執行 `earthaccess.login()` 即可無縫讓隊友的 Python 管線下載。

2. **用免登入工具先篩選與預覽候選類型**
   - **[NASA Worldview](https://worldview.earthdata.nasa.gov/)**：完全免登入。先開啟以下圖層，視覺巡檢「高沙塵＋極度乾燥＋低植被」的非傳統區域（例如：中亞阿爾泰／柴達木盆地／吉爾吉斯高寒荒漠、伊朗盧特沙漠、澳洲內陸鹽沼、非洲納米比／提貝斯提高原、南美普納高原等，避開 Atacama / 冰島 / 夏威夷 / McMurdo）：
     - *Corrected Reflectance (True Color)*
     - *Aerosol Optical Depth (MODIS)*
     - *Land Surface Temperature (Day/Night)*
     - *Vegetation Index (NDVI)*
   - **[NASA Mars Trek](https://trek.nasa.gov/mars/)**：完全免登入。預先熟悉要對照的火星目標區截圖（如 Jezero Crater、Arcadia Planitia、Gale Crater、Arsia Mons 天窗）。

3. **建立簡報與場址分析的「定性子題」資料夾／清單**
   - 等相似度排名一出，就能直接把 Top 1–2 場址的 Worldview 截圖、Mars Trek 截圖與四大面向子題（礦物、洞穴、極端生物文獻）填入 `docs/presentation_outline.md` 第 4 頁。

---

## 4. 下一步檢查清單（取得 Earthdata Login 後）

- [ ] 確認 `earthaccess` 登入成功（可交給隊友 A 跑全球地球下載腳本）
- [ ] 確認全球相似度地圖產出並挑出 Top 1–2 個「非熱門」候選場址
- [ ] 擷取 Top 1–2 場址的 **NASA Worldview** 圖層截圖（真彩色、LST、AOD、NDVI）
- [ ] 擷取對應火星目標區的 **NASA Mars Trek** 截圖
- [ ] 完成 `docs/site_deep_dive.md` 深入分析並填入 7 頁簡報
