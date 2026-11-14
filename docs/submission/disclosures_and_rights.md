# 授權建議、引用與AI揭露

狀態：待全隊確認。使用者要求先提供建議，本輪沒有新增根目錄LICENSE，也沒有代表其他貢獻者授權。

## 原創程式的建議

建議全隊在確認貢獻權利後，將原創程式採Apache-2.0。理由是可公開再使用、保留授權通知與修改紀錄，並有明確專利條款。這是建議，不是已生效的專案授權，也不保證解決所有第三方相容性問題。

確認後才加入原文LICENSE、必要NOTICE及套件metadata，載明授權範圍。論文、衛星圖像、第三方資料和套件不因根目錄LICENSE自動改成Apache-2.0。[官方條款](https://www.spaceappschallenge.org/legal/)要求的公開使用與第三方權利需一起核對。

## 第三方內容登記

| 類別 | 已有紀錄 | 提交前動作 |
|---|---|---|
| Montabone沙塵及其衍生部分 | [既有CC-BY-SA3.0說明](../../outputs/mars_profiles/LICENSE-data.md)與作者／DOI | 保留原通知、署名與修改說明；核對實際分發範圍，不統一套Apache |
| MOLA／TES／SWIM／MEDA | [火星來源](../../outputs/mars_profiles/profiles.json)、[MEDA](../mars_temperature.md) | 按各產品規範署名，確認再分發條件；不因NASA資助一律宣稱公有領域 |
| ETOPO／Natural Earth／POWER | [地球來源](../../outputs/analysis/source_metadata/public_sources.json)、[方法](../earth_pipeline.md) | 提交圖表標產品與期間；保留來源、處理及授權條款 |
| 隊友Earthdata／ESA資料 | [222檔清單](../earth_inventory.csv) | 資料尚未全數在當前分析QA；由提供者補各產品引用及分發條款 |
| 原始論文與補充資料 | 既有研究報告的DOI及事實摘錄 | 不貼受保護全文／原圖；必要時使用自行重繪的事實示意，明示非原始實測地圖 |
| 前端與Python套件 | web/package-lock.json、requirements-lock.txt | release前產生實際依賴授權清單，保留必要notice；本輪未完成逐套件審查 |
| 展示截圖／底圖／照片／字體 | 最終素材尚未凍結 | 每張記source URL、product/layer、view日期、credit、授權；人物與logo使用依條款核對 |

## AI使用紀錄草稿

以下根據repo紀錄，必須由各成員核對實際工具、模型、日期與用途，不能冒稱每個工具皆由本輪執行。

| 工具 | repo記載用途 | 驗證狀態 |
|---|---|---|
| OpenAI Codex | 程式、資料處理、測試、來源查核、研究與文件整理 | 本輪實際使用；科學結論仍以來源及計算為依據 |
| Antigravity | 隊友記載用於web前端、資料轉接、build與瀏覽器驗證 | 隊友回報；本輪未重跑介面 |
| Cursor／Claude | 舊文件記載程式、環境與測試協助 | 實際模型／工作範圍待使用者核對 |
| Claude Code | 隊友記載Earthdata環境與開檔 | 待成員核對 |
| Gemini | 舊文件記載研究整理與簡報規劃 | 待成員核對，不把AI對規則的解釋當官方證據 |

英文揭露草稿：

> We used OpenAI Codex to assist with code, data-processing checks, source review, and documentation. Other team-reported tools include Antigravity, Cursor/Claude, Claude Code, and Gemini; their final uses will be confirmed by the contributing members before submission. Quantitative results come from identified datasets and explicit calculations. AI-generated explanations are not treated as scientific measurements or official NASA guidance.

提交前須將英文中的待確認內容換成確認後清單。若沒有用某工具，刪除該工具，不為完整性保留。

## 分工欄位

| 成員姓名 | 實際貢獻 | 使用工具 | 本人核對 |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |

姓名／隊伍欄位依使用者要求留空，未把舊文件中的Team zasa視為帳戶已確認。
