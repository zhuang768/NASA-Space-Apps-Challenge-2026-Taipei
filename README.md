# Mars Analog Finder

NASA Space Apps Challenge 2026 Taipei — Team zasa。挑戰題目：
[Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/)。

目標：用開放資料在地球上找出與火星地點條件相近的類比場址，並說明哪裡像、哪裡不像。

## 安裝

需要 Python 3.11 以上。

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

## 指令

```bash
.venv/bin/python scripts/download_mars.py    # 下載火星資料到 data/raw/mars（約 110 MB，免登入）
.venv/bin/python scripts/quicklook_mars.py   # 產生 outputs/figures/mars_quicklook.png
.venv/bin/ruff format . && .venv/bin/ruff check .
.venv/bin/python -m pytest
```

## 架構

- `analog/pds.py`：讀取 PDS3 格式的全球網格影像，統一成北到南、東經 -180 到 180 的 `xarray.DataArray`。
- `analog/mars.py`：火星資料的網址、下載與載入。
- `analog/terrain.py`：可跨行星比較的地形量（坡度、區塊統計）。
- `scripts/`：下載與檢查用的腳本。
- `data/`：下載與處理後的資料，不進版控，用腳本重建。

## 資料來源

| 天體 | 資料 | 來源 | 解析度 | 登入 |
| --- | --- | --- | --- | --- |
| 火星 | MGS MOLA 地形（MEGDR） | NASA PDS Geosciences Node | 16 像素／度（3.7 km） | 不需要 |
| 火星 | MGS TES 夜間熱慣量 | NASA PDS Geosciences Node | 20 像素／度（3.0 km） | 不需要 |
| 火星 | SWIM 2.0 地下水冰一致性（淺層 <1 m、深層 1–5 m） | SWIM（NASA 資助，swim.psi.edu） | 20 像素／度，涵蓋南北緯 60 度 | 不需要 |
| 火星 | 沙塵柱光學厚度氣候（MY34 全球沙塵暴年、MY35 平常年；TES/THEMIS/MCS 觀測） | Montabone et al. v2，LMD | 3 度 | 不需要 |

比較面向（與隊友定案，分為四大主題與子項目）：

1. **地形（Terrain）**：坡度與粗糙度、登陸／探測車通行性；子題包含**地質礦物**（玄武岩、黏土、硫酸鹽、碳酸鹽、二氧化矽）與**地下洞穴／熔岩管**（輻射與溫差遮蔽）。
2. **溫度（Temperature）**：地表高低溫與日夜溫差；子題包含**熱慣量**（裸岩 vs. 鬆軟塵土）、**日照／紫外線與輻射**。
3. **水／冰（Water / Ice）**：乾旱度與土壤含水；子題包含**現代地下水冰／永凍土**（ISRU 資源）與**古水文／適居性與極端生物**（NDVI 低植被指標）。
4. **大氣與沙塵（Air）**：懸浮沙塵與沙塵暴（影響太陽能與設備）；子題包含**風力與風蝕地形**（沙丘、雅丹）及**大氣成分與氣壓**（0.6 kPa CO₂）。
- **地球無法複製的限制**（0.38 g 重力、低氣壓、強輻射與高氯酸鹽土壤等）將於各場址分析中明確標註。

地球端資料尚未加入程式管線，預計搭配 NASA Earthdata（NASADEM、MODIS LST/AOD/NDVI、EMIT、GPM、SMAP）、CSA RADARSAT、ESA Sentinel/CCI Permafrost 與 JAXA G-Portal（部分需 Earthdata Login）。

## 尺度對齊

火星的 1 度約 59 km，地球的 1 度約 111 km。比較兩個行星時用實際距離對齊，不是用度數：
火星 1 度的網格大約對應地球 0.5 度的網格。

## AI 工具使用紀錄

提交時必須說明 AI 工具的用途，請在這裡持續記錄。

- 2026-11-13：使用 Cursor（Claude）整理挑戰說明與資料來源、建立專案骨架、撰寫火星資料的下載與讀取程式及測試。
- 2026-11-14：使用 Gemini 整理 2026 挑戰規範與評分重點、確定聚焦地球與火星類比（排除月球），並將所有地球與火星資料來源整併為四大主題（地形、溫度、水／冰、大氣與沙塵）與對應子題及限制條件。
