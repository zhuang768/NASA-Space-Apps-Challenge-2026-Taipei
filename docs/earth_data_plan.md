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
- 火星與地球沿子午線的 `1°` 分別約為 59 km 與 111 km；經向距離另隨緯度改變，不能把火星 `1°` 與地球 `0.5°` 視為各地皆相同的物理尺度。
- 以各天體座標與半徑建立相同公里範圍的視窗，確認原始資料有效尺度後再聚合。現有程式採 100×100 km 視窗、4 km 取樣，另有 10 km 敏感度分析；插值不代表新增真實細節。
- 所有網格統一格式：`xarray.DataArray`，座標 `(lat, lon)`，緯度由北到南（遞減），經度 `-180` 到 `180`。

---

## 2. 地球端資料清單（222 個檔案、12.33 GB，已於隊友本機逐檔開啟）

隊友回報以下資料已下載至其 `data/raw/earth/`（不進 Git）；NASA 資料透過 `earthaccess`，永凍土來自 ESA CCI 歸檔。逐檔檔名、位元組數、SHA-256 與讀取結果見 [earth_inventory.csv](earth_inventory.csv)（2026-11-14 於隊友本機 `.venv` 測試，222/222 開啟成功）；原始檔本身尚未交接至 repo，其他電腦取得後可用 SHA-256 比對。資料交接方式見 [data_handoff.md](data_handoff.md)。

| 面向 | 資料夾 (`data/raw/earth/`) | 資料集（Shortname） | 檔案數與容量 | 原始解析度／網格 | 關鍵變數與讀取備註 |
| --- | --- | --- | --- | --- | --- |
| **1. 地形** | `terrain/` | **`SRTMGL30`**（官方 collection **002**；實際下載識別碼待核對） | 回報 27 個 `.dem.zip`（266 MB） | 30 arc-sec（~900 m） | 隊友回報 `.DEM` 為 16-bit signed big-endian、每塊 4800×6000、無 `.HDR`，圖磚集合涵蓋 60°S–90°N。需用實際檔案大小與產品中繼資料確認邊界及維度，檔名不代表版本；按相同物理尺度計算坡度／起伏。 |
| **1. 地形（地表覆蓋）** | `terrain/landcover/` | **`MCD12C1`** (v061, 2024) | 1 個 `.hdf`（1.24 GB） | 0.05° 年平均（`3600×7200`） | `Majority_Land_Cover_Type_1`（HDF4，可由本機 `netCDF4.Dataset` 開啟）；區分裸岩／荒漠／植被。 |
| **2. 溫度** | `temperature/` | **`MOD11C3`** (v061, 2023–2024) | 24 個 `.hdf`（1.9 GB） | 0.05° 月平均（~5.6 km） | `LST_Day_CMG`／`LST_Night_CMG`，K；讀取 scale、fill 與 QA。月合成日夜值之差不是 TES 熱慣量；月合成值的年內最小／最大也不是瞬時極端溫度。HDF4 讀取依環境支援而定。 |
| **2. 溫度（日照／反照率）** | `temperature/radiation/` | **`M2TMNXRAD`** (MERRA-2, 2023–2024) | 24 個 `.nc4`（1.45 GB） | 0.5° × 0.625°（`361×576`） | `xarray` 直接讀取 `SWGDN`（入射短波輻射）、`ALBEDO`（地表反照率）、`LWGNT`；注意 MERRA-2 為再分析資料，非衛星直接觀測。 |
| **3. 水／冰（乾旱度）** | `water_ice/gpm/` | **`GPM_3IMERGM`** (v07, 2023–2024) | 24 個 `.HDF5`（444 MB） | 0.1° 月平均（`1800×3600`） | `xarray(..., group='Grid')` 讀取 `precipitation` |
| **3. 水／冰（土壤濕度）** | `water_ice/gldas/` | **`GLDAS_NOAH025_M`** (v2.1, 2023–2024) | 24 個 `.nc4`（584 MB） | 0.25° 月平均（`600×1440`） | `xarray` 直接讀取 `SoilMoi0_10cm_inst`（取代原規劃的每日 9 km 衛星觀測 `SPL3SMP_E`；注意 GLDAS 為陸面模式輸出，非衛星直接觀測，涵蓋 60°S–90°N） |
| **3. 水／冰（植被背景）** | `water_ice/ndvi/` | **`MOD13C2`** (v061, 2023–2024) | 24 個 `.hdf`（2.6 GB） | 0.05° 月平均（~5.6 km） | `CMG 0.05 Deg Monthly NDVI`，需處理 QA、scale 與 fill。僅作植被背景，尚未定義扣分規則；HDF4 讀取依環境支援而定。 |
| **3. 水／冰（永凍土）** | `water_ice/permafrost/` | **ESA CCI Permafrost** (v4.0，回報選取 2021) | 1 個 `.nc`（12 MB） | 回報 0.01° 經緯網格（`6000×36000`），25°N–85°N；需確認有效資料遮罩 | `PFR` 與 `PFR_uncertainty` 為 %，由熱模型及衛星／再分析輸入推算。產品序列涵蓋 1997–2021，隊友只回報選取 2021；PFR 是永凍土面積比例，不是地下冰含量、純度、深度或可開採性。 |
| **4. 大氣與沙塵** | `air/` | **`M2TMNXAER`** (MERRA-2, 2023–2024) | 24 個 `.nc4`（1.9 GB） | 0.5° × 0.625°（`361×576`） | `xarray` 直接讀取 `DUEXTTAU`（純沙塵消光 AOT，取代原規劃的 `MOD08_M3` 總 AOD；注意 MERRA-2 為再分析資料，非衛星直接觀測） |
| **4. 大氣與沙塵（衛星觀測 AOD）** | `air/viirs/` | **`AERDB_M3_VIIRS_SNPP`** (2022-12, 2023–2024) | 25 個 `.nc`（155 MB） | 1° × 1°（`180×360`，座標名為 `Latitude_1D`／`Longitude_1D`） | `xarray` 直接讀取 `Aerosol_Optical_Thickness_550_Land_Mean`（衛星實測 AOD，補齊 MERRA-2 再分析之外的直接觀測）。第 25 個檔 `A2022335` 為 2022 年 12 月（搜尋時間範圍重疊而納入），計算 2023–2024 平均時應排除。 |
| **4. 大氣與沙塵（風速／氣壓）** | `air/wind_pressure/` | **`M2TMNXSLV`** (MERRA-2, 2023–2024) | 24 個 `.nc4`（1.89 GB） | 0.5° × 0.625°（`361×576`） | `xarray` 直接讀取 `U10M`、`V10M`（10 m 風速）與 `PS`（地表氣壓）；注意 MERRA-2 為再分析資料 |

> [!NOTE]
> **數量與讀取狀態**：原始批次為 `27 + 5×24 + 1 = 148` 個；先前回報的 145（及更早的 144）是 Claude Code 驗證時的加總錯誤，當時各資料夾實際已逐檔開啟全部檔案。加上新增子資料集 `25 + 24 + 24 + 1 = 74` 個，共 **222 個、12.33 GB（十進位）**，全部開啟成功，逐檔紀錄見 [earth_inventory.csv](earth_inventory.csv)。容量以十進位 GB／MB 計。
> - `GPM_3IMERGM`（需 `group='Grid'`）、`GLDAS_NOAH025_M`、`M2TMNXAER` 與 ESA CCI Permafrost 可用 `xarray` 直接開啟，並帶有 lat/lon 座標。
> - `MOD11C3` 與 `MOD13C2` 為 HDF4-EOS。隊友回報其環境可用 `netCDF4.Dataset(path)` 開啟；這需要底層 netCDF-C 編譯支援 HDF4 SD，不能保證其他 wheel 或電腦也可讀。應以同一原始檔測試實際環境；若不支援，再使用具 HDF4 支援的讀取器或經驗證的轉檔工具。
> - MODIS CMG 檔案**沒有 lat/lon 變數**，需自行建立 0.05° 網格（3600×7200）：lat 由 89.975 遞減至 −89.975，lon 由 −179.975 遞增至 179.975（皆為格點中心）。
> - 隊友回報 `SRTMGL30` zip 只有 `.DEM`、無 `.HDR`，其中 `W020N40` 為大寫。可用檔名協助定位，但仍要核對中繼資料、位元組數與缺值定義。

### 判讀與配對限制

- NASA 官方 SRTMGL30 目錄列 collection `002`，並註明未隨 SRTM V3 更新；原文件的 `v003` 已更正。實際取得的檔案仍需核對 collection ID，不能只改標籤就宣稱原始檔版本已驗證。
- NDVI 只用於植被背景，低值或負值可能涉及水、雪或品質問題，不能證明無生命。必須套用 QA 與地表遮罩。
- GPM 降水與 GLDAS 表層土壤水分描述地球乾濕條件，不能直接等同或相減於 SWIM 地下冰一致性。SWIM 分數也不是冰含量或機率。
- MODIS 日夜溫度差與 TES 熱慣量的量綱不同；需取得相同物理量或驗證轉換模型，再進行定量配對，不能直接推論地面硬度。
- MERRA-2 `DUEXTTAU` 是 550 nm 沙塵光學厚度。與火星 CDOD 比較前，仍需對齊波長、氣壓正規化、季節與時間尺度；不能因兩者都量沙塵就直接視為等量。
- 現有正式結果仍為地形篩選；四面向綜合分數尚未完成，未知條件保留未知。

來源：[NASA SRTMGL30 官方目錄](https://cmr.earthdata.nasa.gov/search/collections.umm_json?short_name=SRTMGL30)、[ESA/CEDA 永凍土 v4.0](https://catalogue.ceda.ac.uk/uuid/93444bc1c4364a59869e004bf9bfd94a/)、[Unidata HDF4 編譯支援](https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html)。

---

## 3. 地球端免登入即可開始的工作（現在就能做）

在等待或註冊 Earthdata Login 的同時，地球端負責人可以先完成以下三件事：

1. **準備 Earthdata Login 帳號（供 `earthaccess` 使用）**
   - 前往 [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov/) 註冊帳號（免費，約 2 分鐘）。
   - 註冊後在帳號設定中勾選授權 `NASA GESDISC DATA ARCHIVE` 與 `LP DAAC` 應用程式（下載 GPM、GLDAS、MODIS、SRTMGL30 必備）。
   - 本機設定 `~/.netrc` 或執行 `earthaccess.login()` 即可無縫讓隊友的 Python 管線下載。

2. **用免登入工具先篩選與預覽候選類型**
   - **[NASA Worldview](https://worldview.earthdata.nasa.gov/)**：完全免登入。先開啟以下圖層，視覺巡檢「高沙塵＋極度乾燥＋低植被」的非傳統區域（例如：中亞阿爾泰／柴達木盆地／吉爾吉斯高寒荒漠、伊朗盧特沙漠、澳洲內陸鹽沼、非洲納米比／提貝斯提高原、南美普納高原等，避開 Atacama / 冰島 / 夏威夷 / McMurdo）：
     - *Corrected Reflectance (True Color)*
     - *Aerosol Optical Depth (MODIS)*
     - *Land Surface Temperature (Day/Night)*
     - *Vegetation Index (NDVI)*
   - **[NASA Mars Trek](https://trek.nasa.gov/mars/)**：完全免登入。預先熟悉要對照的火星目標區截圖（如 Jezero Crater、Arcadia Planitia、Gale Crater、Arsia Mons 天窗）。

3. **建立簡報與場址分析的「定性子題」資料夾／清單**
   - 等相似度排名一出，就能直接把 Top 1–2 場址的 Worldview 截圖、Mars Trek 截圖與四大面向子題（礦物、洞穴、極端生物文獻）填入 後續依最新研究問題製作的展示文案（舊簡報已移除）。

---

## 4. 下一步檢查清單（取得 Earthdata Login 後）

- [ ] 確認 `earthaccess` 登入成功（可交給隊友 A 跑全球地球下載腳本）
- [ ] 確認全球相似度地圖產出並挑出 Top 1–2 個「非熱門」候選場址
- [ ] 擷取 Top 1–2 場址的 **NASA Worldview** 圖層截圖（真彩色、LST、AOD、NDVI）
- [ ] 擷取對應火星目標區的 **NASA Mars Trek** 截圖
- [ ] 完成 `docs/site_deep_dive.md` 深入分析並填入 7 頁簡報
