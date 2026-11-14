# 提交準備與官方查核

日期：2026-11-14；本輪時鐘查核為台北12:50，已過官方答覆所述週六09:00。團隊實際所屬場次仍留空。依使用者要求，帳戶欄位不代填，授權只提供建議。完整正式指南未取得，以下英文內容為可審查草稿，不是已提交作品。

## 官方確認程度

| 來源 | 本輪狀態 | 採取行動 |
|---|---|---|
| [2026年度頁](https://www.spaceappschallenge.org/2026/) | 前輪取得可見全文，列出11/14至11/15本地時段 | 以隊伍帳戶顯示核對適用時區及截止，不自行推定台北地方細則 |
| [GO-Team答覆 #1827](https://github.com/nasa/spaceapps/discussions/1827) | 本輪直接讀取；開工時段、事前研究與來源引用說明 | 本輪在11/14台北中午工作；過往工作歷史保留，不改寫為全在競賽內完成 |
| [Navigator答覆 #1973](https://github.com/nasa/spaceapps/discussions/1973) | 本輪直接讀取：英文、7頁以內或30秒內、公開展示連結、AI揭露及本地截止 | 準備七頁英文文案；不把討論答覆當完整表單規格 |
| [本題](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/) | 直接web仍timeout；前輪HTTP200只見標題；本輪官方搜尋回傳有題目簡介 | 完整Details／Resources仍未核實，Mars-only仍待確認 |
| [Resources](https://www.spaceappschallenge.org/resources/)／[Taipei](https://www.spaceappschallenge.org/2026/local-events/taipei/) | 直接web502，前輪可見內容不足 | 不再重複搜尋冒充已找到指南；等待有效指南／帳戶內容 |
| [條款](https://www.spaceappschallenge.org/legal/) | 前輪公開全文已讀；本輪webtimeout | 原創開源與第三方權利分開處理；資格、授權及影像人物使用仍由隊伍核對 |

只有完整頁面或已讀答覆支持的內容列為已確認。搜尋摘要不升格為完整題目；指南預定11/13發布不代表已取得。

## 題目適配

目前有Earth與Mars的真實資料、由程式提出候選及地圖／工具原型，對應已讀簡介的主要工作方向。但簡介提及Earth、Moon、Mars資料，完整要求未核實，不能保證Mars-only足夠。本輪先完成可共用的研究／提交說明，不擅自補Moon資料或改變策略。

給主辦／Navigator的提問草稿（未發送）：

> Our team is addressing “Identify Earth Locations that Analog the Permanent Moon Base Locations and Mars.” We use Earth and Mars open data to identify and characterize terrestrial analog candidates for a Mars-focused geological reconnaissance use case. Does this challenge permit a Mars-only implementation, or is an implemented lunar comparison and use of Moon data required? Could you point us to the complete 2026 challenge requirements and submission guide applicable to Taipei?

## 帳戶／提交欄位

| 欄位 | 內容 |
|---|---|
| Registered team name | |
| Team page URL | |
| Selected challenge confirmed | |
| Event and applicable timezone | |
| Official guide URL/version | |
| Final project page URL | |
| Public demo URL | |
| Public slide/video URL | |
| Submission owner | |
| Submitted status and timestamp | |

隊名在repo曾寫Team zasa，但不當作帳戶已核對。正式欄位名稱與字數限制未知；英文文案貼入前需按實際表單調整。

## 英文提交文案草稿

### Project name
TerraMatch Mission Lab

### One-sentence summary
A reproducible terrain-screening workflow that proposes Earth analog candidates for Mars research and shows the evidence and unresolved conditions behind each comparison.

### Project description
TerraMatch Mission Lab helps researchers decide which Earth regions merit closer investigation as partial Mars analogs. We compare Earth and Mars terrain in 100 km windows using planetary radii, a common sampling scheme, and an explicit distance based on slope statistics and relief.

The existing run evaluated 2,611 eligible Earth windows within a sparse search between 60°S and 60°N. It generated terrain shortlists for Gale, Jezero and a project-defined Arcadia target. Environmental data and published geological evidence are presented separately from the terrain ranking. Missing information remains unknown.

Our contribution is a traceable screening and review workflow: candidate footprints, source records, transparent assumptions, sensitivity comparisons, and explicit limits on what the data can establish. The current release does not provide a validated four-theme score, landing-safety assessment, resource estimate, or field-access approval. Mars-only challenge eligibility still requires confirmation.

### NASA and other open data used
NASA MGS MOLA supplies the Mars terrain used in the ranking; NOAA ETOPO supplies Earth terrain, with Natural Earth used for the land mask. NASA POWER provides limited Earth environmental context for six shortlisted target–candidate records. MGS TES thermal inertia, SWIM ice consistency and Montabone dust products supply separate Mars context. Jezero MEDA brightness-temperature data remain provisional because the conservative quality requirements are not satisfied. Product identifiers, hashes and processing details are linked from the repository; products in the teammate Earth inventory are not represented as fully integrated analysis.

### Results and limitations
The completed result is a regional terrain shortlist, not a whole-planet similarity percentage. The three Earth candidates discussed in the existing research report correspond to two Mars targets. Geological links remain partial; a regional reference comparison confirms that terrain distance alone cannot establish environmental or mineralogical suitability. Resampling does not create detail, and the data do not resolve wheel-scale hazards. Gravity, atmospheric pressure and radiation remain major limits of natural Earth analogs.

### Next steps
Validate the mission requirements, obtain compatible quality-controlled environmental summaries, test a larger independent reference set, and verify any outcrop-specific material claims before planning field experiments.

### Code and methods
https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei

Original-code license: pending team confirmation. Third-party material retains its own applicable terms. This project is not endorsed or certified by NASA.

## 展示製作與送出順序

1. 先核對完整題目／指南與Mars-only；未回覆時保留待確認，不自行寫「符合所有規則」。
2. 依[七頁英文文案](slides_en.md)製作PDF，加入實際截圖及可讀引用；本輪尚未產出完成PDF／影片。
3. 全隊核對姓名、貢獻與[AI紀錄](disclosures_and_rights.md)，確認授權。不要把待確認欄位原樣當最終提交。
4. 指定release commit，驗證公開repo／展示／PDF的匿名存取。Cloudflare workflow存在不代表已部署。
5. 依實際表單填入文案、資料與引用；檢查儲存結果，完成SUBMIT後確認狀態與時間。

[最後未完成清單](remaining_checklist.md)逐項交接。沒有在本輪登入、發送問題、接受條款或代替隊長提交。
