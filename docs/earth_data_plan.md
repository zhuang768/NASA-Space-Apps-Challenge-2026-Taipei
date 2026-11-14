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

## 2. 地球端已下載之 Core 資料清單（2023–2024 兩年完整網格，共 ~7.6 GB）

以下資料已透過 `earthaccess` 下載並分類至 `data/raw/earth/`（不進 Git）：

| 面向 | 資料夾 (`data/raw/earth/`) | 資料集（Shortname） | 檔案數與容量 | 原始解析度／網格 | 關鍵變數與讀取備註 |
| --- | --- | --- | --- | --- | --- |
| **1. 地形** | `terrain/` | **`SRTMGL30`** (v003) | 27 個 `.dem.zip`（266 MB） | 30 arc-sec（~900 m） | `*.DEM`（16-bit signed big-endian 整數高程，需重採樣至 ~3–4 km 算 `slope_deg`/`relief`） |
| **2. 溫度** | `temperature/` | **`MOD11C3`** (v061, 2023–2024) | 24 個 `.hdf`（1.9 GB） | 0.05° 月平均（~5.6 km） | MODIS Terra LST 日夜地表溫度（HDF4 格式，Python 讀取需 `pyhdf`） |
| **3. 水／冰（乾旱度）** | `water_ice/gpm/` | **`GPM_3IMERGM`** (v07, 2023–2024) | 24 個 `.HDF5`（444 MB） | 0.1° 月平均（`1800×3600`） | `xarray(..., group='Grid')` 讀取 `precipitation` |
| **3. 水／冰（土壤濕度）** | `water_ice/gldas/` | **`GLDAS_NOAH025_M`** (v2.1, 2023–2024) | 24 個 `.nc4`（584 MB） | 0.25° 月平均（`600×1440`） | `xarray` 直接讀取 `SoilMoi0_10cm_inst`（取代高達 467 GB 的每日 `SPL3SMP_E`） |
| **3. 水／冰（植被扣分）** | `water_ice/ndvi/` | **`MOD13C2`** (v061, 2023–2024) | 24 個 `.hdf`（2.6 GB） | 0.05° 月平均（~5.6 km） | MODIS Terra NDVI（HDF4 格式，Python 讀取需 `pyhdf`） |
| **4. 大氣與沙塵** | `air/` | **`M2TMNXAER`** (MERRA-2, 2023–2024) | 24 個 `.nc4`（1.9 GB） | 0.5° × 0.625°（`361×576`） | `xarray` 直接讀取 `DUEXTTAU`（純沙塵消光 AOT，比 9 GB 的 `MOD08_M3` 更精準且輕量） |

> [!NOTE]
> **格式讀取備註**：`GPM_3IMERGM`、`GLDAS_NOAH025_M` 與 `M2TMNXAER` 皆已實測可用 `xarray` 直接開啟；`MOD11C3` 與 `MOD13C2` 為 NASA HDF4 格式（內建 `rasterio` wheel 未包含 HDF4 驅動），程式端載入時需安裝 `pyhdf`（或透過 HDF4 工具轉換）。

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
