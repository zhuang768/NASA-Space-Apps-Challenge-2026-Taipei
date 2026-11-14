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
.venv/bin/python scripts/download_mars.py      # 若尚未有檔：下載火星資料到 data/raw/mars（約 380 MB，免登入）
.venv/bin/python scripts/build_mars_stack.py   # 產出 data/processed/mars_stack_0p5deg.nc
.venv/bin/python scripts/score_mars_selftest.py
.venv/bin/python scripts/quicklook_mars.py
.venv/bin/python scripts/check_upload.py
.venv/bin/ruff format . && .venv/bin/ruff check .
.venv/bin/python -m pytest
```

## 隊友協作與資料取得

請先閱讀 [CONTRIBUTING.md](CONTRIBUTING.md)：包含協作者邀請、各作業系統的資料下載指令、分支上傳方式與常見錯誤處理。
`data/raw/mars/` 與 `data/processed/`（約 390 MB）已進版控，clone 即可用。
`data/raw/earth/`（約 7.6 GB）仍不進 git，請用雲端交接，見 `docs/data_handoff.md`。

## 架構

- `analog/pds.py`：讀取 PDS3 格式的全球網格影像，統一成北到南、東經 -180 到 180 的 `xarray.DataArray`。
- `analog/mars.py`：火星資料的網址、下載與載入。
- `analog/terrain.py`：可跨行星比較的地形量（坡度、區塊統計）。
- `analog/swim.py`、`analog/dust.py`：SWIM 2.0 地下水冰與 Montabone 沙塵氣候讀取。
- `analog/stack.py`、`analog/score.py`、`analog/sites.py`：0.5 度共同網格、參考場址特徵與相似度評分。
- `scripts/`：下載、建堆疊與檢查用的腳本。
- `docs/`：簡報架構（`presentation_outline.md`）、類比極限（`mars_limits.md`）、地球端資料規劃（`earth_data_plan.md`）與跨行星對照表（`cross_reference.md`）。
- `data/raw/mars/`、`data/processed/`：火星原始與處理後網格（進版控）。`data/raw/earth/` 不進版控。

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

隊友回報已下載約 7.6 GB 地球資料至其 `data/raw/earth/`：`SRTMGL30`（官方 collection 002，實際下載識別碼待確認）、`MOD11C3`、`GPM_3IMERGM`、`GLDAS_NOAH025_M`、`MOD13C2`、`M2TMNXAER`，以及選取 2021 年的 ESA CCI Permafrost v4.0。這批原始檔與讀取紀錄尚未透過 repo 交接；依表格預期為 148 個，與先前回報開啟 145 個的範圍有差異，尚待核對，不能直接宣稱完整性已驗證。規格與限制見 `docs/earth_data_plan.md`、`docs/cross_reference.md`，交接方式見 `docs/data_handoff.md`。

MODIS 地表溫度與 TES 熱慣量、地球乾濕條件與 SWIM 地下冰一致性均不是同一物理量；NDVI 不代表生命存在與否，永凍土面積比例也不是可開採冰量。這些面向先作分開的證據描述，尚未整合為四面向相似度分數。

## 尺度對齊

沿子午線，火星與地球的 1 度分別約為 59 km 與 111 km；經度方向的距離還會隨緯度改變，因此地球 0.5 度不是火星 1 度的通用等價網格。現有分析以各天體半徑建立 100×100 km 視窗，採 4 km 點距並做 10 km 尺度敏感度比較。取樣與插值不代表新增真實解析度。

## AI 工具使用紀錄

提交時必須說明 AI 工具的用途，請在這裡持續記錄。

- 2026-11-13：使用 Cursor（Claude）整理挑戰說明與資料來源、建立專案骨架、撰寫火星資料的下載與讀取程式及測試。
- 2026-11-14：使用 Gemini 整理 2026 挑戰規範與評分重點、確定聚焦地球與火星類比（排除月球）、整併四大主題與子題，撰寫「地球無法複製的火星條件」、7 頁簡報架構、地球端資料下載規劃與跨行星對照表（`docs/`），並下載分類地球端四大面向資料：2023–2024 兩年全球網格（`MOD11C3`、`GPM_3IMERGM`、`GLDAS_NOAH025_M`、`MOD13C2`、`M2TMNXAER`）、地形 `SRTMGL30`，以及 2021 年北半球 `ESA CCI Permafrost v4.0`。
- 2026-11-14：隊友回報使用 Claude Code 協助授權 Earthdata 資料中心、建立 Python 3.12 環境、監看下載及開啟 145 個資料檔。此為隊友環境的紀錄；與清單推算 148 個的差異、實際檔案及讀取紀錄尚待核對。
- 2026-11-14：使用 OpenAI Codex 核對官方規格，修正 SRTMGL30 版本、資料計數狀態、永凍土／NDVI 解釋、跨行星配對與 HDF4 環境限制。本次文件修正未使用 C2C。
- 2026-11-14：使用 Cursor（Claude）完成火星四面向堆疊與相似度自我測試，並將 `data/raw/mars/` 與 `data/processed/` 納入版控以便隊友直接取得。

## 地球管線與第一輪實際結果（2026-11-14）

已加入免登入 ETOPO 地形篩選、NASA POWER 候選氣候背景、Earthdata 月資料清單與下載入口。
本輪是 **terrain-only regional screening**，尚未完成四面向綜合相似度。

- 方法與執行：[docs/earth_pipeline.md](docs/earth_pipeline.md)
- 原始資料下載與交接：[docs/data_handoff.md](docs/data_handoff.md)
- 候選交接：[outputs/analysis/candidate_handoff.md](outputs/analysis/candidate_handoff.md)
- 完整工作回報：[docs/work_report_2026-11-14.md](docs/work_report_2026-11-14.md)
- 數值結果與來源：`outputs/analysis/results_with_context.json`
- 權重及尺度敏感度：`outputs/analysis/sensitivity.json`

AI 使用紀錄補充：2026-11-14，OpenAI Codex 協助本輪地球資料程式、方法說明、測試及工作報告。
已嘗試 Codex with ChatGPT 規劃審查，但工作區讀取服務失敗，未取得其獨立程式審查。
所有候選數值來自下載資料與公開 API，未以 AI 生成地形或補造缺值。

