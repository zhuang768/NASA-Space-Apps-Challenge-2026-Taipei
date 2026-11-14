# 可重跑數值交付｜2026-11-14

**目前完成：EARTH-002 的逐列交付、QA 接收和描述圖；EARTH-UV-001 的溫度對照亦保留。實際使用 Mac CPU，沒有 GPU 加速或模型訓練。**

目前研究需求採 **MR-20261114-v2 @ `f6d4c181d9739fe5c74b1c573b59414d63d6ec8e`**。沿用 Team1 固定候選、point anchor 與原用途文字。Team1 部分 requirement 欄仍是舊 provisional 值，轉接層保留，沒有代改隊友檔案或視為協定版本已一致。

## 最主要交付：EARTH-002 → I-02

Elephant Head 站點錨點：**-79.820216667°N、-83.314333333°E**，datum 未聲明，沒有新試驗區範圍。

| 檔案 | 用途 |
|---|---|
| [station_observations.csv.gz](EARTH-002/station_observations.csv.gz) | 8922 筆逐時資料；原頁／頁內列／印刷列號、雙時標、九個溫濕度欄與缺值旗標。解壓後為 CSV |
| [earth_candidate_features.csv](EARTH-002/earth_candidate_features.csv) | 120 筆月統計：九個原變數及同列 3–49 cm 溫差；有效數、預期數、涵蓋率、單位、來源 |
| [window_summaries.csv](EARTH-002/window_summaries.csv) | 同窗口夏季配對、完整年度 air／49 cm 描述；沒有 3 cm 全年平均 |
| [reference_comparison.csv](EARTH-002/reference_comparison.csv) | 對照 Team2 既有均值與原論文 Table II，不把重現稱新效應 |
| [qa_report.json](EARTH-002/qa_report.json)、[page_qa.csv](EARTH-002/page_qa.csv) | 108 頁匯出／抽樣核對、缺測、時間限制、來源及程式雜湊、實際環境 |
| [data_dictionary.json](EARTH-002/data_dictionary.json) | 單位、深度、RH 定義、原始時間欄與來源頁列定義 |
| [inputs_manifest.csv](EARTH-002/inputs_manifest.csv) | 實際原始來源、期間、座標支撐、檔案狀態與雜湊 |
| [paired_summer 圖](EARTH-002/figures/EARTH-002_paired_summer.png) | 同站、同列、共同有效夏季兩深度序列與差值 |
| [monthly_coverage 圖](EARTH-002/figures/EARTH-002_monthly_coverage.png) | 明確呈現 3 cm 冬季缺資料；0% 表示無觀測，不是 0°C |

原始 PDF SHA-256：`20fe70f574bc394f05f0c720809f80a9602ac73f6ede34d322ea816cf25590d9`，108 頁、1,165,179 bytes。來源：[EH2 出版者附表](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0954102019000269/resource/name/S0954102019000269sup001.pdf)；量測方法／單位：[EH1 NASA 存檔](https://www.nasa.gov/wp-content/uploads/2019/09/mckay_etal_2019_dry_permafrost_ellsworth_land21.pdf)，本輪讀 Methods p.2、Table II p.5，SHA-256 `1d64eb94184a5e4fd7e8e0985a23a8c9a6e35ad2626f268ad8a3a80ffc21b6db`。觀測期 2017–2018、出版 2019、取得 2026-11-14 分開記錄。

沿用 **Team2 @ `bc9fe3c0f352632a7117dbdab24df21b7450738e`** 的 parser、8922 筆全表雙引擎 QA 與均溫摘要。該成果屬 Team2；本交付補成可重跑程式、逐列匯出、每頁抽查與圖。原 parser 摘錄、來源 QA 摘錄及版本資訊保存在 `inputs/`，未改原查核結論。

本輪匯出驗收：8922 個印刷列號連續，第一時標從 **2017-11-28 00:00 至 2018-12-04 17:00** 每小時連續，第二時標全部晚 90 分鐘；未轉 UTC。3 cm 有 2646 筆，最後為 **2018-03-18 05:00**，後續 6276 筆保留缺值。49 cm 修正 RH 有 2807 筆高於 100%，保留原值並標記。

| 第一印刷時標窗口 | 數量 | 本輪重現均值 |
|---|---:|---:|
| 夏季：2017-12-01 含至 2018-03-01 不含；3 cm | 2160 | -5.3553°C |
| 同一夏季窗口；49 cm | 2160 | -8.6302°C |
| 同列 3 cm 減 49 cm | 2160 對 | +3.2749°C |
| 論文年：2017-12-01 含至 2018-12-01 不含；air | 8760 | -20.2940°C |
| 同一論文年；49 cm | 8760 | -19.2370°C |

這些是**已發表資料的描述重現**，與 Team2 摘要一致，五項原 Table II 均溫四捨五入至 0.1°C 亦一致。N 是時間支撐，非獨立重複試驗數。現有資料不能驗證新冰界面偵測、鑽進升溫、保冰率、覆土因果效應或火星設備性能；已公開 49 cm 是歷史安裝位置資訊，不能同時當擬合答案與新盲測真值。

## 補充對照：EARTH-UV-001 → I-01

W 錨點：-77.86215°N、160.7101°E。來源是作者校準並篩選過的封存資料，不是未加工 logger bytes：[Zenodo 10553882](https://zenodo.org/records/10553882)，檔名 `UniversityV_09_10_Campbell_data_good_only_calibrated.txt`。

原檔 2,673,975 bytes，MD5 `ae2133eac5c92c695c5f6ef93bcbbd25` 與作者檔案頁一致，SHA-256 `c46d93e3dd07c6c91d700a814214716f00caa0d5cc3a520f8969ce0af63ecafd`。封存發布 2024-01-23，本輪下載／校驗 2026-11-14。原檔實際從 2009-12-04 19:30 至 2010-12-08 15:30，共 17705 筆半小時紀錄；氣溫全部有值，四個土溫通道各有 297 筆作者檔中的 NaN，位於初期。

分析窗口固定 2010 年：各通道 **16400／17520** 筆；1–11 月完整，12 月只有 **368／1488（24.73%）**。不產生 W 全年平均。84 筆月結果包含五個溫度通道與兩組同列深度差；土表是接觸式量測，未與 MODIS／TES 混用。

交付：[數值表](EARTH-UV-001/earth_candidate_features.csv)、[逐筆資料](EARTH-UV-001/station_observations.csv.gz)、[QA](EARTH-UV-001/qa_report.json)、[圖](EARTH-UV-001/figures/EARTH-UV-001_temperature_coverage.png)、[輸入與缺檔清單](EARTH-UV-001/inputs_manifest.csv)。本項延續原先 W 最小案例，**不把它當成 MR-v2 已改派 EH2 的 GPU-08 結案證據**。

## 環境、範圍及剩餘缺口

- 執行位置：Mac 的隔離副本 `/tmp/nasa-compute-20261114`，避免改動原專案約 50 個既有修改。僅將新 `scripts/compute/`、`outputs/compute/` 及對應 `data/raw/earth/` 複製回專案；不覆蓋隊友文件、總 Excel、`analog/` 或網站。
- 實際 Python 為專案既有 `.venv/bin/python` 3.12.15；numpy 2.5.4、matplotlib 3.11.2。PDF 讀取額外使用暫存隔離的 pypdf 7.1.0、pypdfium2 5.15.2，不修改原 venv。詳細套件／CPU／來源檔案雜湊見 [runtime/local_inventory.json](runtime/local_inventory.json) 及各 QA。
- 此次運算是 **Mac CPU／binary64**，非 AUP GPU。此次流程未使用 Apple GPU 後端；Mac 環境未找到 ROCm／torch／cupy；沒有加速倍數。每階段時間寫在 QA，單次計時僅描述此次執行，不作效能基準。
- AUP 舊工作根目錄曾實際確認為 `/home/jovyan/mars-analog-test`；它沒有 `.git`，保有舊 Mars JSON 與三張圖。本輪再次開啟時顯示斷線，Hub 顯示 stopped；已嘗試重啟 CPU，但尚未完成此次雲端執行／套件／cgroup／GPU 盤點，不能把畫面中的主機記憶體當分配額度。未重跑或恢復舊地球排名，也不將舊副本整批放回 main。
- 15 項正確性檢查涵蓋缺值／scale／offset／fill／閏年預期筆數、單月資料無年均、共同有效配對、時間差、重複／衝突、檔案校驗、座標綁定，以及下一個候選透過 CSV／profile 接入。[測試紀錄](runtime/tests.log)。測試 fixture 僅在暫存目錄，非真實觀測。
- MERRA-2 SLV/AER 2023–2024 各 24 個月、MOD11C3.061 24 個月的真正原檔／可追溯裁切未交至此案例，無重新抽取的值。W manifest 列出檔名模式、變數、單位與來源，保留 Team1 數字為外部既有結果。MR-v2 將這些放在主分析後，並非 EH2 交付阻礙。
- 無可用局部 DEM／新測區範圍、現代獨立冰界面真值或 I-01/I-02 合格溫度序列；不補零、不用冷溫或 TI 推冰深。MOLA／TES／SWIM 既有 QA 按 MR-v2 重用，沒有重算。EARTH-003 Linnaeus Terrace 保持未啟用。

## 主要對話如何使用

可接收 GPU-01／08 的 EH2 來源與 metadata、GPU-09 逐列表與轉錄驗收、GPU-10 同列夏季描述圖與有效支撐。用語限定「出版資料可重現／既有站點熱響應描述」。未知時區、感測器校準限制與候選用途版本差異必須隨結果保留；新穎性與未來實驗仍由主要對話及 Team1／2 決定。

執行方式與候選欄位契約見 [scripts/compute/README.md](../../scripts/compute/README.md)。Git 分支為 `compute/candidate-extraction-20261114`；本交付不自行合併 main，最終 commit／PR 以 GitHub 回報為準。程式與小型結果可進 Git，下載的原始 PDF／站點檔保留於 `data/raw/earth/`，以 manifest 和 checksum 重取。
