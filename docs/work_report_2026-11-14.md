# 2026-11-14 工作報告

本輪已完成一條可實際重跑的地球地形搜尋流程，並取得候選的 NASA 氣候背景。正式結果是地形篩選，不是四面向整合推薦。目前沒有足夠依據宣布哪一地點是「整體最像火星」或「較少被研究的新類比場址」。

## 本次完成的工作

- 複製 repo，基準為 `330666e`，建立 `codex/earth-analog-pipeline` 獨立分支。保留隊友既有火星讀取、地形及沙塵模組，新增地球與配對模組。
- 使用免登入 NOAA ETOPO 2022、NASA PDS MOLA 與 Natural Earth 陸地遮罩，實際下載並記錄 SHA-256、來源、單位、版本及座標基準。
- 將地球與火星轉到各自天體的局部 100×100 km 視窗、4 km 取樣間距，計算同定義的坡度與起伏特徵。地球使用平均球半徑近似，沒有直接比較絕對海拔。
- 在 60°S 至 60°N 每 2° 搜尋中心：初始陸地中心 2,897 個，286 個未達 95% 取樣陸地比例，剩 2,611 個合格視窗。這不是完整覆蓋全球每個位置的搜尋。
- 對 Jezero、Gale 及專案設計的 Arcadia 目標產出完整排序；每一目標保留最多 12 個相隔至少 300 km 的候選，共 36 個候選條目。
- 取得六個候選中心的 NASA POWER 2023–2024 月資料。每個氣象變數使用完整 24 個月並按天數加權；資料來自再分析與衍生產品，與地形排名分開。
- 完成兩種地形權重變動及 10 km 取樣間距重跑；保留完整排名、CSV、GeoJSON 足跡、來源快照、敏感度與地圖／地形比較圖。
- 建立 Earthdata 月資料查詢／下載入口，實際查到 MOD11C3、MOD13C2、GPM_3IMERGM、MOD08_M3 的 2023–2024 granules，各 24 個。修正 MOD08_M3 在 CMR 的版本識別為 `6.1`，排除查詢區間相交而混入的前一個月。

## 候選交接

以下是各目標的空間分散地形前兩名。D 是本專案定義的地形差距，越低越接近；不能解讀為百分比、整體相似度或任務成功率。

| 火星目標 | 地球中心 lat, lon | D | POWER 平均 2 m 氣溫 °C | POWER 平均降水 mm/day |
|---|---|---:|---:|---:|
| Jezero 18.44°N, 77.45°E | 57°N, 161°E | 0.1341 | -2.47 | 2.513 |
| Jezero | 13°N, 37°E | 0.1362 | 25.56 | 7.692 |
| Gale 4.59°S, 137.44°E | 39°N, 75°E | 0.2319 | 0.72 | 0.300 |
| Gale | 35°N, 75°E | 0.3459 | -1.91 | 2.108 |
| Arcadia 設計目標 40°N, 170°W | 29°N, 105°W | 0.0252 | 21.38 | 0.346 |
| Arcadia 設計目標 | 35°N, 57°E | 0.0448 | 19.31 | 0.289 |

每一候選代表約 100 km 區域，不能把中心點當成精確試驗場。所有候選標示「本專案提出、尚待驗證」，既有類比文獻、礦物、冰、後勤及許可仍未確認。避開團隊指定的熱門區域不代表證明新穎性。

Jezero 前兩名的降水背景不支持直接將其描述為乾旱類比，適合保留為地形方法參照。若隊友要先選較乾燥的區域查資料，可先研究 Arcadia 清單的 29°N, 105°W 與 35°N, 57°E；這是後續查證優先順序，尚未建立地下冰類比或綜合推薦。

完整數字：[候選交接表](../outputs/analysis/candidate_handoff.md)、[CSV](../outputs/analysis/shortlist.csv)、[含氣候的結果與來源](../outputs/analysis/results_with_context.json)。

## 敏感度結果

| 目標 | 坡度較重時前兩名保留數 | 起伏較重時保留數 | 10 km 取樣時保留數 |
|---|---:|---:|---:|
| Jezero | 1/2 | 0/2 | 1/2 |
| Gale | 2/2 | 2/2 | 1/2 |
| Arcadia | 2/2 | 1/2 | 0/2 |

權重比較使用相同候選、目標、容許差與分散規則。10 km 重跑有 2,601 個合格視窗，因遮罩取樣而略有改變；這是整體流程尺度敏感度。結果顯示目前不應宣稱推薦穩定。沒有機率、先驗或查證成本模型，未計算期望資訊價值。

## 實際驗證

- `pytest -q`：**27 passed**。含既有 8 個測試與本輪新增 19 個測試案例。
- `ruff check .`：**All checks passed**。
- `git diff --check`：通過。
- `pip check`：No broken requirements found。
- 以真實資料執行下載、兩種取樣尺度的排名、六筆氣候查詢、結果摘要及繪圖。已開啟候選地圖與 Jezero 地形圖檢查，並修正地圖註記與座標文字重疊。
- 測試涵蓋天體半徑與物理距離、跨日期變更線、已知斜率人工解、缺值不能贏得排名、候選去重、空結果、地形平均及座標、閏年月權重、氣候缺月保留 unknown、CMR 時間邊界。

第一次新增氣候測試有兩例因測試替身的檔名不符合下載介面而失敗；已修正測試資料位置並重跑。最終 27 例通過。仍有兩個 affine 矩陣乘法的 PendingDeprecationWarning，未影響這次結果，後續更新套件時可處理。

## 遇到的問題與處理

1. 使用者目前沒有 Earthdata 帳號。保留四種月產品的真實清單與受保護下載入口，改以免登入 ETOPO 與 NASA POWER 完成能執行的流程。**未下載或解碼受保護 MODIS/GPM 原始檔，也未驗證授權下載。**
2. NOAA 大檔單線下載緩慢並逾時。透過 HTTP Range 分段下載，核對回應區間與總長度後組合成功，再記錄 SHA-256。repo 的一般下載入口仍使用原有串流下載方法，慢速連線可能需要較長時間。
3. 不限制版本的環境安裝出現套件相依回溯。改用已實測版本完成環境，保存 `requirements-lock.txt`。
4. TES 熱慣量／MODIS 溫差、SWIM／地球乾旱度、Mars CDOD／地球 AOD 的物理定義不同，因此沒有硬湊四面向總分。
5. 使用 [Codex with ChatGPT skill](/Users/clark/.codex/skills/codex-with-chatgpt/SKILL.md) 嘗試規劃審查；原對話已達容量上限，替代對話的工作區讀取持續失敗。本機健康檢查後仍失敗，故**沒有取得 ChatGPT 獨立程式審查**，也沒有把其失敗當成審查通過。這輪程式、資料與驗證由 Codex 在本機執行。

## 官方與未確認資訊

2026-11-14 已在官網直接讀到完整 Details 與 Resources：Objectives 允許對應 Moon **or** Mars，支持本輪聚焦火星；要求以資料說明有用的類比與限制，並呈現新候選。資源頁列 Earthdata Search、Worldview、PDS、LRO/Diviner、CSA、ESA 與 JAXA。

來源：[官方題目](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/)、[官方資源分頁](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources)。

7 頁／30 秒與 11/15 23:59 截止為本次隊友交接資訊，本輪未從提交規範頁獨立核實，應依台北主辦方正式通知確認。AI 紀錄已在 README 補上本輪 Codex 使用情況。

## 接下來的工作

| 狀態 | 項目 |
|---|---|
| 已完成 | 本輪地球地形搜尋、候選足跡與排序、來源紀錄、NASA 氣候背景、權重與尺度敏感度、上述測試與圖表 |
| 已完成 | 月資料清單查詢及下載程式；清單查詢已實測 |
| 示範／設計假設 | 地形權重與容許差、Arcadia 目標中心；尚未校準成任務工程門檻 |
| 待確認 | 候選是否已有類比研究、場址地質／礦物、任務適用性、季節、許可、進入方式與授權方案 |
| 尚未完成 | 有效 Earthdata 帳號下載、MODIS/GPM QA 解碼、跨星球同物理量配對與四面向整合 |
| 尚未完成 | 未知證據翻轉分析、正式場址深入報告、7 頁簡報、互動前端、部署與提交 |
| 尚未完成 | ChatGPT 獨立程式審查；repo 尚無 LICENSE，需團隊決定適用的開源授權 |

下一個最值得投入的工作是先決定一個明確的任務測試問題，再從上述乾燥候選查地質與既有研究；同時申請 Earthdata 帳號，補上真正同物理量的環境比較。只要氣候或地質證據不支持，就應排除或縮小類比主張。

本輪已推送獨立分支 `codex/earth-analog-pipeline`，並建立[草稿 PR #1](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/1)供隊友審查。尚未合併主分支、部署或提交參賽作品。

## 後續資料上傳與 GitHub 查驗

依使用者指示，本次後續作業沒有使用 C2C。GitHub plugin 已實際成功讀取主分支完整 `analog/dust.py`。已整合隊友主分支 `d9d121b` 的最新文件，保留其地球資料規格。

[資料 Release](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/releases/tag/terrain-inputs-2026-11-14)已發布，包含本輪實際取得的原始輸入包及 `SHA256SUMS.txt`。資料包 491,292,776 bytes，GitHub 回報附件狀態 uploaded；伺服器 SHA-256 與本機一致。另已解讀資料包並核對其中 ETOPO、Natural Earth、MOLA 影像與標籤共四個來源檔的 SHA-256。

這個資料包不包含隊友文件另記載的約 7.6 GB MODIS/GPM/GLDAS/MERRA-2 等地球原始檔。檢查當時的分支、Release、Actions artifacts 與 Issue/PR 未找到那批檔案或交接連結；文件註明其位於不進 Git 的 `data/raw/earth/`。尚需隊友提供實際資料位置，不能把文件清單當成原始資料已可取得。

下載、校驗與解壓指令見 [data_handoff.md](data_handoff.md)。分析程式與結果仍在 PR #1，未合併主分支、未部署、未提交參賽作品。
