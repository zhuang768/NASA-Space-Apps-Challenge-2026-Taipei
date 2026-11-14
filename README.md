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
.venv/bin/python scripts/profile_mars.py --strict  # 火星目標特徵、來源與逐 sol 沙塵序列
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
| 火星 | MY34／MY35 沙塵重建場；兩份 v2.5 檔案標示觀測輸入為 MRO/MCS | Montabone et al. v2.5，LMD | 原生 3 度；9.3 μm 吸收光學厚度 | 不需要 |

比較面向（與隊友定案，分為四大主題與子項目）：

1. **地形（Terrain）**：坡度與粗糙度、登陸／探測車通行性；子題包含**地質礦物**（玄武岩、黏土、硫酸鹽、碳酸鹽、二氧化矽）與**地下洞穴／熔岩管**（輻射與溫差遮蔽）。
2. **溫度（Temperature）**：地表高低溫與日夜溫差；子題包含**熱慣量**（裸岩 vs. 鬆軟塵土）、**日照／紫外線與輻射**。
3. **水／冰（Water / Ice）**：乾旱度與土壤含水；子題包含**現代地下水冰／永凍土**（ISRU 資源）與**古水文／適居性與極端生物**（NDVI 低植被指標）。
4. **大氣與沙塵（Air）**：懸浮沙塵與沙塵暴（影響太陽能與設備）；子題包含**風力與風蝕地形**（沙丘、雅丹）及**大氣成分與氣壓**（0.6 kPa CO₂）。
- **地球無法複製的限制**（0.38 g 重力、低氣壓、強輻射與高氯酸鹽土壤等）將於各場址分析中明確標註。

隊友回報已下載約 12 GB 地球資料至其 `data/raw/earth/`（含最新補齊的四大面向子資料集）：`SRTMGL30`（官方 collection 002）＋`MCD12C1` 2024 地表覆蓋（地形）、`MOD11C3`＋`M2TMNXRAD` 輻射與反照率（溫度）、`GPM_3IMERGM`＋`GLDAS_NOAH025_M`＋`MOD13C2`＋2021 年 ESA CCI Permafrost v4.0（水／冰與永凍土／植被）、`M2TMNXAER`＋`AERDB_M3_VIIRS_SNPP` 衛星 AOD＋`M2TMNXSLV` 風速與氣壓（大氣與沙塵）。這批原始檔與讀取紀錄尚未透過 repo 交接；規格與限制見 `docs/earth_data_plan.md`、`docs/cross_reference.md`，交接方式見 `docs/data_handoff.md`。

MODIS 地表溫度與 TES 熱慣量、地球乾濕條件與 SWIM 地下冰一致性均不是同一物理量；NDVI 不代表生命存在與否，永凍土面積比例也不是可開採冰量。這些面向先作分開的證據描述，尚未整合為四面向相似度分數。

## 尺度對齊

沿子午線，火星與地球的 1 度分別約為 59 km 與 111 km；經度方向的距離還會隨緯度改變，因此地球 0.5 度不是火星 1 度的通用等價網格。現有分析以各天體半徑建立 100×100 km 視窗，採 4 km 點距並做 10 km 尺度敏感度比較。取樣與插值不代表新增真實解析度。

## AI 工具使用紀錄

提交時必須說明 AI 工具的用途，請在這裡持續記錄。

- 2026-11-13：使用 Cursor（Claude）整理挑戰說明與資料來源、建立專案骨架、撰寫火星資料的下載與讀取程式及測試。
- 2026-11-14：使用 Gemini 整理 2026 挑戰規範與評分重點、確定聚焦地球與火星類比（排除月球）、整併四大主題與子題，撰寫「地球無法複製的火星條件」、7 頁簡報架構、地球端資料下載規劃與跨行星對照表（`docs/`），並下載分類 2023–2024 兩年地球端四大面向全球資料（`SRTMGL30`、`MCD12C1`、`MOD11C3`、`M2TMNXRAD`、`GPM_3IMERGM`、`GLDAS_NOAH025_M`、`MOD13C2`、`ESA CCI Permafrost v4.0`、`M2TMNXAER`、`AERDB_M3_VIIRS_SNPP`、`M2TMNXSLV`），同步備份至本機桌面並更新對照文件。
- 2026-11-14：隊友回報使用 Claude Code 協助授權 Earthdata 資料中心、建立 Python 3.12 環境、監看下載及開啟 145 個資料檔。此為隊友環境的紀錄；與清單推算 148 個的差異、實際檔案及讀取紀錄尚待核對。
- 2026-11-14：使用 OpenAI Codex 核對官方規格，修正 SRTMGL30 版本、資料計數狀態、永凍土／NDVI 解釋、跨行星配對與 HDF4 環境限制。本次文件修正未使用 C2C。
- 2026-11-14：使用 Cursor（Claude）完成火星四面向堆疊與相似度自我測試，並將 `data/raw/mars/` 與 `data/processed/` 納入版控以便隊友直接取得。
- 2026-11-14：OpenAI Codex 接入並核對上傳的 10 個火星來源檔、修正 SWIM 座標與聚合倍率、沙塵欄位及缺值評分，匯出目標特徵與交接文件；本輪未使用 C2C，地球端處理由隊友負責。

## 火星端交接

方法、執行與缺資料清單見 [docs/mars_pipeline.md](docs/mars_pipeline.md)，實際描述值見 [outputs/mars_profiles/handoff.md](outputs/mars_profiles/handoff.md)。`profiles.json` 含 MOLA、TES、SWIM 與 MY34／MY35 的來源、單位與品質資訊，另附六份逐 sol 沙塵 CSV。

0.5° stack 是火星內部描述網格；沙塵仍只有原生 3°尺度。內部相似度預設需要全部圖層，允許部分資料時明列 `evidence_fraction`，不是信賴度。Arcadia 內部測試不是地球選址驗證。火星地表日夜溫度與任務專用門檻仍缺，不能用熱慣量或描述值取代。

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

## 中文工作報告維護約定

依使用者要求，後續每次完成工作時，在本 README 追加繁體中文報告，記錄完成項目、實際驗證、問題、待確認事項與下一步。詳細方法或大型結果另存文件，並在此附連結。只有實際執行的檢查才能標為通過；規劃、探索結果與正式分析分開記錄。保留歷次報告，避免把前輪結果誤寫成本輪重新驗證。

## 工作報告：火星日夜亮溫接軌補記（2026-11-14）

本節補記前輪已完成的工作；對應提交為 `ee98936` 與 `1064880`。

- **已完成**：取得 Jezero／Perseverance MEDA calibrated TIRS 的 LMST sol 700、701、702，共 159,418 筆讀值與三份 PDS4 XML 標籤。加入下載、欄位／列數／單位核對、LTST 分組、品質篩選與來源校驗碼，並整合至火星報告的 `rover_temperature_context`。
- **探索結果**：日夜摘要代表探測車局部的地面亮溫，不是全球或 100 km 區域的動力地表溫度。輪子視野、HGA、SkyCam 三項品質旗標在全部讀值中皆未知；依專案保守規則，合格筆數為 0，狀態為 `quality_incomplete`。探索摘要未納入正式相似度評分。
- **前輪驗證**：57 項測試通過、8 個既有警告；Ruff 檢查通過；六個原始檔的本機與 Git 內容 SHA-256 均符合來源紀錄。這些是前輪執行結果，本次文件更新未重跑測試。
- **待確認**：缺失品質旗標的意義、觀測足跡與姿態、同場日夜配對及季節代表性。
- **尚未完成**：可與地球 LST 比較的全球／區域溫度資料、全年季節覆蓋、Gale REMS 接入與 Arcadia 溫度資料。局部亮溫尚未補齊既有區域 `surface_temperature` 的缺口。

方法與執行方式見 [火星溫度工作報告](docs/mars_temperature.md)；數值與來源見 [溫度摘要](outputs/mars_temperature/summary.json)，整合結果見 [火星目標資料](outputs/mars_profiles/profiles.json)。

## 工作報告：六階段提示詞整理（2026-11-14）

本輪已逐階段修訂並整合六份英文提示詞，最終文字已交付於對話中。六階段任務本身尚未開始執行。

| 階段 | 提示詞範圍 | 狀態 |
|---|---|---|
| Phase 1 | 工作區與 Git 狀態、資料盤點、環境／測試與重現性 | 提示詞已完成；階段未執行 |
| Phase 2 | 地球管線稽核、特徵交接格式、可行擴充與最小範圍 | 提示詞已完成；階段未執行 |
| Phase 3 | 火星資料／座標／尺度／品質稽核、目標檢查與資料缺口 | 提示詞已完成；階段未執行 |
| Phase 4 | 跨行星物理量配對、轉換方法、缺值政策與一致性檢查 | 提示詞已完成；階段未執行 |
| Phase 5 | 候選搜尋、基準比較、敏感度、深入查證與選址凍結 | 提示詞已完成；階段未執行 |
| Phase 6 | 官方提交要求核實、簡報／圖表、AI 揭露與提交準備 | 提示詞已完成；階段未執行 |

已統一的執行原則：

- 以 `VERIFIED`、`INFERRED`、`EXTERNAL`、`UNVERIFIED`、`PROPOSED` 區分證據；歷史路徑、commit、資料數與測試數不能當作當前狀態。
- 預設保留既有檔案，新腳本與輸出放入各階段獨立目錄；既有檔案修改先提出 diff，明確授權範圍除外。本次 README 更新由使用者直接授權。
- 四個主題不必強行合成分數；不同物理量、品質未知與缺資料不得被轉成確認符合。直接比較、代理模型與情境類比分開呈現。
- Phase 2 與 Phase 3 可並行，其餘依交接順序進行。開始長作業前評估時間；選址凍結後不新增科學資料或重新排名。
- 官方截止時間、頁數、影片與揭露規定仍需正式查證。提示詞中的時間屬團隊規劃；不代表規則已核實。
- 上傳、發布、標記版本與正式提交需有相應授權，並觀察實際結果後才能宣稱完成。

**本輪檢查與限制**：已逐項交叉檢查六份提示詞的階段範圍、交接、時間與授權規則。未因提示詞整理而執行資料稽核、下載、科學計算、排名、測試或提交。下一步須由使用者指定要開始的階段，再核對當時環境與剩餘時間。

AI 使用紀錄補充：OpenAI Codex 協助整理六階段提示詞，以及將工作報告補入本 README；本輪未產生新的科學結果。

