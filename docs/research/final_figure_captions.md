# Final research text and figure captions · Team zasa

Status: **ready for the main conversation's acceptance, 2026-11-14 (Asia/Taipei); checked against main `e84da75`.** Part 1 is public-facing English text. Part 2 (Traditional Chinese) records versions, the number and attribution check, requested figure edits and open items. Figure review rows are in [`final_figure_review.csv`](final_figure_review.csv).

---

# Part 1 · Public text (English)

## A. Research summary

Mars candidate I-02 (53.75°N, 42.25°E) is a low-slope screening cell with a shallow-ice consistency indicator; the indicator is not a confirmed deposit and gives no independent depth, purity or extractability. Before any new measurement is designed, we ask what published ground observations can and cannot say about thermal response above an ice-cemented layer. We keep one anchor case, the Elephant Head monitoring station in Ellsworth Land, Antarctica (McKay et al., 2019), because its published hourly table and quality-check record allow a traceable, descriptive reproduction. University Valley remains a known-use comparison and Linnaeus Terrace an inactive archival backup; all three sites have prior research.

What we completed is data organisation, not new measurement. The 108-page published supplement was parsed into 8,922 hourly rows with source-page provenance, and the reported means were reproduced from that table with a CPU-only export. In the common summer window (1 December 2017 to 1 March 2018, first printed clock), 2,160 hourly pairs show a 3 cm soil temperature averaging −5.36 °C and a 49 cm ice-table probe averaging −8.63 °C: a same-row mean difference of +3.27 °C.

These results do not establish equivalence with Mars, ice depth or quantity, extractability, interface-detection accuracy, a cover effect, ice loss or equipment performance. Novelty is not cleared.

## B. Figure captions

**Figure F01. Case context: Mars candidate I-02 and the Elephant Head station anchor.** Left, the Mars screening cell for I-02 (planetocentric latitude, east-positive longitude), centred at 53.75°N, 42.25°E and spanning 53.5–54°N, 42–42.5°E, about 29.64 × 17.52 km; the panel shows 52.75–54.75°N, 40.75–43.75°E. The cell is a regional screening support, not a borehole, landing ellipse or instrument footprint. Right, a south-polar coordinate locator (60–90°S; longitude east-positive, 0° at top) with the Elephant Head monitoring station, Ellsworth Land, Antarctica, at 79.820216667°S, 83.314333333°W (79°49.213′S, 83°18.860′W as published; datum and positioning error not stated). This is a single published point: no test-area radius, polygon or trial plot is defined, and the marker size is symbolic. The panels differ in kind and scale, a regional cell tens of kilometres across against one station, and no common distance scale is implied. The Earth site is paired with I-02 as a research-purpose reference for describing thermal response and the evidence still needed, not as a best match, an equivalent or a newly discovered site. No imagery, terrain or ice data are shown. Sources: MR-20261114-v2 I-02 research card (Mars cell); McKay et al. (2019), Methods and Fig. 1, doi:10.1017/S0954102019000269 (Earth coordinates).

**Figure F02. Elephant Head: temperatures at two depths.** Hourly temperature (°C) at one published station (EARTH-002; 79.820216667°S, 83.314333333°W): a sensor at 3 cm depth in dry loose material (teal) and the installed probe at the 49 cm ice table (orange; the ice-table depth is a historical installation value). The window runs from 1 December 2017 (inclusive) to 1 March 2018 (exclusive) on the first printed time axis, labelled “GMT-07:00”, and contains 2,160 same-row hourly pairs, all valid at both depths. Over the window the 3 cm series averages −5.3553 °C (range −21.13 to +17.75 °C) and the 49 cm series −8.6302 °C (range −14.00 to −5.23 °C); both means agree with the published Table II values at one decimal (−5.4 and −8.6 °C). Values are plotted as published, without smoothing, filling, resampling or time-zone conversion. The meaning of the two printed clocks (the second runs 90 minutes later) is unverified. The 3 cm sensor logged 2,646 hourly values and stopped on 18 March 2018, so there is no winter or annual 3 cm series. N counts hourly records, which are autocorrelated, not independent replicates. The 3 cm series is subsurface soil temperature, not land-surface skin temperature and not Mars thermal inertia. Observations: McKay et al. (2019), EH2 supplement. Transcription and full-table QA: Team 2. Reproducible export (CPU only): compute commit 14f6550. Rendering: Team 1.

**Figure F03. Elephant Head: paired temperature difference.** The same-row difference T(3 cm) − T(49 cm), in °C, for the 2,160 hourly pairs of Figure F02 (1 December 2017 inclusive to 1 March 2018 exclusive; first printed time, label “GMT-07:00”; no time-zone conversion). Positive values mean the 3 cm sensor was warmer than the 49 cm probe in that hour. The dashed line is the descriptive window mean, +3.2749 °C, which equals the difference of the two means in Figure F02 (−5.3553 − (−8.6302)). The hourly difference ranges from −8.22 to +23.89 °C, so a warmer mean does not mean a warmer 3 cm layer at every hour. N = 2,160 hourly records are autocorrelated rather than independent, and no confidence interval is given. The difference describes two observed depths at one historical station. It does not give ice depth, ice quantity, extractability, an effect of cover, sampling-related heating or equipment performance, and it is not evidence about Mars. Observations: McKay et al. (2019), EH2 supplement. Transcription and full-table QA: Team 2. Reproducible export (CPU only): compute commit 14f6550. Rendering: Team 1.

## C. Limitations

1. **Historical Earth stations are references, not demonstrated equivalents.** Elephant Head, University Valley and Linnaeus Terrace are published sites with their own conditions. Their measurements do not show that either Mars candidate shares their ice, materials, thermal properties or environment.
2. **A temperature difference cannot give ice depth, ice quantity or extractability.** Two depths at one station describe thermal response only; they do not identify an interface, support a cover-effect claim, or predict drilling or equipment performance on Mars.
3. **A new site, a new use and a distinct scientific difference are not established.** All three Earth sites have prior research, including monitoring, ice-stability modelling, drilling, stratified sampling and temperature-controlled handling at specified scales. Our contribution is source tracing, quality-checked reproduction and documentation of limits; novelty is not cleared.

---

# Part 2 · 核對與交接（繁體中文，內部）

## 採用的版本

| 項目 | 版本 | 狀態 |
|---|---|---|
| main | `e84da75d905ad43f260e74307752946862200dae`（先前讀 `ab1da69`、`e9554f1`） | 寫完時的最新 main；含 MR-20261114-v3-final 英文摘要與 `outputs/research/elephant_head_final/`（README、qa.json、manifest.json、records、兩張主線 PNG） |
| 數值交付（計算） | `compute/candidate-extraction-20261114` @ `14f65509bbf3358a50ef866c65e2b5d42fe8c467`（PR #5） | 只讀自分支，**未進 main**，無新提交；`outputs/compute/README.md` 仍只在此分支；主要對話尚未確認接受 |
| 正式 EH 包（主線） | main `e84da75`；`qa.json` 狀態 `PASS_EXPORT_REPRODUCTION_AND_TRACEABILITY_ONLY`；manifest 版本 MR-20261114-v3-final | 主線重新匯出與重現，不是新觀測；本次已與其 qa.json 逐項比對 |
| 圖片（隊友 1） | `reporting/team1-final-figures` @ `08cb74af411f3f529951c8f49c0c40a576e1fa20` | 只讀；其後只有 README 提交 `c1117eb`（分支頭仍是 `c1117eb`，寫完時再確認過，圖檔未變）。PNG SHA-256：F01 `95fc9fc5…430b4c`、F02 `45af1fcc…cf29`、F03 `0ebf1b18…fa43`，皆與其 manifest 相符 |
| EH 全表轉錄與 QA | Team 2 @ `bc9fe3c0f352632a7117dbdab24df21b7450738e` | 原解析與全表 QA 歸 Team 2 |
| 原始資料 | McKay 等 (2019) EH2 補充 PDF，SHA-256 `20fe70f5…5590d9`，1,165,179 bytes，108 頁 | 原作者觀測；計算分支的 manifest 已記錄 |

## 現有英文摘要檢查

main 現在有主線正式英文摘要 `docs/research/final_research_summary_en.md`（MR-20261114-v3-final），以及 Team 2 的英文研究定位（`team2_novelty_audit.md`）。兩者已說清楚研究問題、三站角色、EH 數字、不能回答的問題與新穎性未成立。Part 1 的 A 是為「搭配圖片閱讀」寫的 150–250 字精簡版，數字、窗口、限制與它一致；限制 3 沿用 Team 2 內容。差異：A 另外點出『I-02 的 SWIM 指標不是已確認冰層』；主線摘要把 EH 時間標記寫為「原標記窗口」，A 與圖說寫成「第一印刷時標、意義未核實」，兩者不衝突。主線摘要用 McKay 論文表述，F02 另附 Table II 一位小數的一致性（−5.4、−8.6），是補充不是新結論。

## 數字與歸屬核對

我直接用圖片所依據的匯出檔（`station_observations.csv.gz`，SHA-256 `25389967…e6db`）再讀一次，與計算 QA 及任務基準比對。這是核對，不是新分析。

| 項目 | 任務基準 | 正式 QA／匯出 | 結果 |
|---|---|---|---|
| 原表筆數 | 8,922 | 8,922，列號 1–8922 連續；108 頁 | 一致 |
| 第一時標範圍 | — | 2017-11-28 00:00 至 2018-12-04 17:00；第二時標全部晚 90 分鐘 | 一致 |
| 3 cm 有值 | 2,646 | 2,646，最後 2018-03-18 05:00；缺值 6,276 | 一致 |
| 夏季窗口 | 2017-12-01 含至 2018-03-01 不含 | 同；最後一筆 2018-02-28 23:00 | 一致 |
| 配對數 | 2,160 | 2,160（3 cm、49 cm 皆 2,160 有效） | 一致 |
| 3 cm 均值 | −5.3553°C | −5.355300926 | 一致 |
| 49 cm 均值 | −8.6302°C | −8.630152778 | 一致 |
| 同列差均值 | +3.2749°C | +3.274851852；等於兩均值之差 | 一致 |
| 與論文 Table II | — | 夏季 3 cm −5.4、49 cm −8.6（一位小數）皆符合 | 一致 |
| 計算環境 | CPU，不宣稱 GPU | 計算分支 `gpu_used: false`，Mac arm64，Python 3.12.15，無加速倍數；主線 `qa.json` 沒有 GPU 主張 | 一致 |
| 主線正式 qa.json | 同上基準 | records 8,922；bad_records 空；3 cm 2,646；窗口 2,160（覆蓋 100%，列 73–2232、PDF 第 1–27 頁）；−5.355300926、−8.630152778、+3.274851852；年窗口 N=8,760；RH>100% 2,807；PDF SHA-256 `20fe70f5…5590d9` | 一致（與計算分支、Team 1 的 F02/F03 數值相同） |
| 雙引擎 | — | 主線 `qa.json`：`current_double_engine_check: false`，Team 2 的雙引擎比對為繼承；因此 Part 1 只說『解析並重現』，沒有寫『本次雙引擎驗證』 | 措辭已對齊 |

補充：差值範圍 −8.22 至 +23.89°C 來自匯出檔 `window_summaries.csv`，圖說用它說明「平均較暖不代表每個時刻都較暖」。49 cm 修正 RH 有 2,807 筆高於 100%，三張圖都沒有使用 RH，圖說不涉及。

歸屬已分開寫在 F02／F03 圖說：原始觀測屬 McKay 等；原解析與全表 QA 屬 Team 2；可重跑匯出屬計算分支；圖片屬隊友 1；圖說與核對屬本文件。

## 需要隊友 1 修改的項目

格式：`圖 ID | 位置 | 建議文字 | 來源／章節 | 是否阻擋`。目前**沒有阻擋項**，都是編輯性建議。我沒有修改任何圖片。

| 圖 | 位置 | 建議替換 | 來源 | 類型 |
|---|---|---|---|---|
| F01 | 左下文字「Cell: 53.5–54°N × 42–42.5°E」 | `Cell: 53.5–54°N × 42–42.5°E (about 29.64 × 17.52 km)` | `main_mars_research_cards.md`，I-02 研究卡「名義單元」 | editorial |
| F01 | 最下方第二行來源／限制句 | 句尾加 `Panels show 52.75–54.75°N, 40.75–43.75°E (Mars) and 60–90°S (Earth).` | figures README「Coordinates, time and interpretation」 | editorial |
| F02、F03 | x 軸標籤 | `First printed time · label “GMT-07:00” · meaning unverified · no UTC / solar-time conversion` | 計算 `qa_report.json` 的 `time_status`；Team 2 `bc9fe3c` | editorial |
| F02、F03 | 腳註第二行 | `Transcription QA: Team 2 · export: compute 14f6550 (CPU) · unchanged hourly values; no smoothing, filling or resampling.` | 計算 README；Team 2 EH 全表 QA 段落 | editorial |
| F01–F03 | 腳註「DISPLAY EDITION · mainline final acceptance pending」 | 目前正確，請保留；主要對話確認接受後再改為正式版本標示 | figures README「Pending decisions」 | 狀態，非錯誤 |

## 通過、需修正與尚未收到

完整逐項紀錄見 `final_figure_review.csv`。摘要：

- **PASS：** ID、座標與符號慣例（含 DMS 換算與極座標幾何）、點位與單元的區別、窗口與筆數、深度與單位、差值方向與均值、不推論的限制、PNG／PDF 與 manifest 雜湊相符、使用條件已記錄。
- **NEEDS_CORRECTION（共 6 列，皆編輯性或狀態性，無阻擋）：** F01 圖中範圍與尺度差異未標在圖上；F02／F03 時標「意義未核實」與歸屬鏈未寫在圖上（4 列）；另 1 列為『主線與隊友 1 各有一套 F02/F03，需主線指定正式版』。
- **已收到（main `e84da75`）：** `final_research_summary_en.md`、`elephant_head_final/` 的 README、qa.json、manifest.json。
- **NOT_RECEIVED：** 照片或衛星影像及其拍攝日期、範圍、單張圖使用條款；實際排版寬度（無法證明小字可讀；14 吋寬縮到 6.5 吋時 9–12 pt 字約剩 4–5.6 pt，放滿版橫式投影片約縮 0.95 倍）；主要對話對 `14f6550` 的最終接受；`outputs/compute/README.md` 不在 main（只在計算分支）。
- **需主線選擇（不是錯誤）：** main 的 `elephant_head_final/` 另有兩張主線 PNG（`summer_temperatures.png`、`summer_temperature_difference.png`），與隊友 1 的 F02／F03 內容與數字相同但版面與標題不同。依分工只應有一套正式圖，請主線指定哪一套是正式版；本文件圖說以隊友 1 的 F01–F03 為準。主線 F03 的時標寫「no UTC/solar-time conversion」，沒有寫『meaning unverified』，建議同樣補上。

## 交給主線判定的矛盾與狀態

查核期間沒有發現來源之間的**科學數字矛盾**。需要主線處理的是狀態：

1. `main_project_synthesis.md`（MR-v2）寫「逐列 tidy 交付、驗收及圖表尚未收到」；這是歷史狀態。main 現在已有主線 EH 正式包，但計算分支 `14f6550` 與隊友 1 圖片分支仍未合併。請主線決定是否接受 `14f6550`、哪一套圖為正式版，再更新該狀態。
2. 兩個印刷時標的意義仍未核實，圖說已照此寫，沒有改寫成 UTC 或太陽時。
3. 新版 `final_research_summary_en.md` 與 `elephant_head_final/` 已在 main，且已與 Part 1 的摘要與數字核對（無矛盾）。main 的 commit 訊息提到『工作簿上傳限制』，屬主線狀態，我未讀其內容，不在本文件範圍。

本文件沒有新增文獻搜尋、場址搜尋、新統計或實驗，也沒有修改圖片、原始數據、總 Excel、評分程式或網站。AI 使用：Claude 協助版本核對、數字比對與文字撰寫。
