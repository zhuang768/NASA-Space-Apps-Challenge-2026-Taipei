# ZASA｜三點研究補證據與交接

**研究證據包，不是正式報告或簡報。** 基準為 [main 快照 1506ede](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/commit/1506ede572435588eb5e64f95f24639279b77e56)；MS-02 最新未合併補件另列確切版本。沒有修改既有研究正文、隊友分支、公開站或競賽表單。

| 點位 | 本輪新完成 | 可用處置 | 不能宣稱／下一個必要證據 |
|---|---|---|---|
| [MS-01](ms01/README.md) | 實取作者工作簿並核驗 MD5；與同作者 TXT 的 91,618 個可用值零不符。另實取 68 站地面冰深原表，位置 A 同報告精度有三個坑深 40/44/44 cm；位置 B 無同座標量測，最近 70.2 m 的站均深 10.8 cm。 | University Valley 保留為熱傳與訊號可辨識性案例；另外的地面深度測量偏支持 2009 部署版 S/D 配置，但不改站標。Beacon 的加水實驗為材料敏感性參照。 | 還缺 GPS 與序號確證、原始校時紀錄、同孔物性及可比冰／無冰控制。重複匯出一致不是獨立觀測。 |
| [MS-02](ms02/MS02_HAUGHTON_EVIDENCE.md) | 核實遠端已有獨立目錄。Haughton 原研究在同一測線以雷達＋取冰芯建立地面方法對照；濕覆土干擾需開挖；重新估算示例雷達尺度。另核對 [Beacon 原研究](ms02/MS02_BEACON_EVIDENCE.md) 的短期昇華值是模型結果。 | Haughton／Beacon 保留為方法參照，不升為 Mars 成功配對。A/B 兩批補件可分別查閱，不混算通過數或來源。 | 真值、完整校正與現地尺度不足；不同位置與不同工作條件不能當同站控制。Haughton 已有地面冰類比文獻，不能稱全球新用途。 |
| [MS-03](ms03/README.md) | 以原產品配合正式查詢驗證高解析覆蓋。五個 CTX 已審視窗口約 2.06% 固定框面積；MOC 三個窗口約 1.28–1.29%，保留有效條帶約 15.13–15.21%。查核三個 HiRISE 地圖產品家族固定框零命中，有附近陽性對照。 | 形貌目前只能做取樣與尋找候選地標，AD1 保留一般方法參照。 | 非全域搜尋；兩種覆蓋率不能相加，也不是偵測力。仍不能測可靠的全框多邊形或以光譜／雷達反演冰深，原始輸入與時鐘缺口仍在。 |
| [三點尺度／相依性](cross-site/README.md) | 三點統一重算背景格中心距、有效配對、條件式深度轉換與 ±5 cm 假設敏感度。 | 三點都是待檢驗區域；釐清局部資料和粗背景、相依模型、獨立真值之間的差異。 | 沒有三組驗證地球配對、已證實火星冰，也沒有無先例／新地點的證據。當次新增的是可重算的比較流程及具體限制。 |

## 倉庫、版本及展示

- [主線研究索引（固定 SHA）](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/1506ede572435588eb5e64f95f24639279b77e56/outputs/research/README.md)；[地球來源私有 Release](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/releases/tag/earth-raw-inputs-2026-11-14)。隊友需要現有私有庫權限；ESA 原件仍按來源下載。
- 未合併 [MS-02 PR #22](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/22)＝`4145ec5c586511df4813590cf1a7197fa26ff8c0`；[PR #25](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/25)＝`57143ab5b6d59f3ada0d203a53c01e4aadefc297`。97 與 86 個改動路徑的交集為空，但科學主張有重疊，應並列釐清依據。MS-03 PR [#23](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/23)／[#24](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/24) 與共用 [#20](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/20) 已合併。舊整合 PR [#9](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/9)／[#10](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/10) 有衝突，不覆蓋。
- [離線網站預覽](engineering/index.html) 不會自動連網或顯示私人資料；需下載後用瀏覽器開啟，GitHub 檔案頁不等於展示網站。只呈現已查過的三候選篩選表，不包含未合併補件，不是正式 Demo。公開站的部署標記仍是舊版 [e84da75](https://nasa-space-apps-challenge-2026-taipei.ziz81503.workers.dev/deployment.json)。官方網站設定曾有意從主線移走，Cloudflare 遠端建置失敗；本機工作樹未動，無法確認本機每一筆未提交內容都在遠端。
- [正式送出檢查](SUBMISSION_CHECKLIST.md)：**台北時間 11/15 23:59**。先以有限主張定稿，完成公開可讀的 Demo 和 Final Project 連結，再由隊伍確認官方 Project → Submit。沒有驗證 Submitted；本資料包及 PR 都不算投稿。

所有新增摘要按「來源實讀／重算／推論」分開。若把本資料包作為定稿引用，請保持 commit 與原始來源鎖定並保留授權標註。
