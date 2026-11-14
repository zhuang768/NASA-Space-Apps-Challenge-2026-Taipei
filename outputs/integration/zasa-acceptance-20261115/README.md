# ZASA 三點｜整合驗收與問題處置

本目錄是證據、數值查核、可重跑方法與展示工件，不是正式報告或簡報。主張界線：**三點均是火星待驗證區域，還沒有當地冰真值、三組成功配對或全球新穎性證明。**

## 主線驗收

- [MS-02 #22](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/22) 與 [#25](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/25) 已合併。97 與 86 個改動路徑逐一讀回相符；兩批分開引用，不把重疊的數值檢查當成獨立科學驗證。
- [MS-03 #26](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/26) 並未整批合併。W 氣象與雷達等 28 個已驗證原檔，加兩個說明檔，以 [16822bb](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/commit/16822bb7bb39f4661abc5af964aa464f0c6aa698) 進入主線。四份數據表重算一致；正式報告 blob `f9164ae35147f6007f486fe69cb93cc41572c2b5` 原封不動。#26 改寫的正文、整體清冊及其他未納入檔案仍在原 PR。
- [#27 證據快照](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/27) 原 32 檔可查讀，其「未合併狀態」是當時的歷史文字。草稿仍待使用者同意改狀態；不以本次新的證據或清單繞過。舊 #9／#10 整合快照已過時，不覆蓋現在結果。
- 本機 Mac 另有未提交工作，未以清理、reset 或覆蓋處理。

## 新增問題處置

| 問題 | 新驗收結果 | 仍缺／處置 |
|---|---|---|
| 三點冰存在 | [有限的原位與曝光查核](common/evidence.md) 未找到固定框內的確認觀測。 | 不支持存在或不存在。須有同址、獨立且有敏感度界線的測量。 |
| 冰深與含量 | [雷達共址](common/radar.md)：MS-02 最近分析跨軌樣本相距 562.5 m；±0.45 m 的跨軌深度可比條件，需額外假設深度變化率不超過 0.0008 m/m。 | 滿足該條件未被量測；不能用條件式熱深度、未驗證峰值或採樣間距推估真值。 |
| UV 物性／控制 | [物性來源](ms01/MS-01-material-control.md)：已區分異地物性代入、同地估計值和獨立測量。 | 仍缺同位置、已知冰量且邊界可比的有冰／無冰對照及材料 k、ρCp。 |
| UV 站位 | [站位圖核對](ms01/station_identity.md)：圖 1b 的 D 在 S 以北，偏支持 2009 部署版，原文座標寫法反向。 | 定性圖不是精定位；保留兩套，待原始 GPS＋序號 1122968／2432936 或作者更正。 |
| 站內／跨儀器時鐘 | [站內 11 組](ms01/README.md) 重算共 5,016 值，同一批讀值的共同常數偏移不影響相對相位。 | 無法辨識跨 logger、漂移或重置。沒有修正原時標。 |
| MS-02 E02 | [典藏索引](ms02/NEW_E02_EVIDENCE.md) 找到對應 GCMD→CMR 和 GTN-P 點位；未取得逐時序列。 | 不併接分隔數公里的鑽孔；仍待同址原始感測及部署資料。 |
| MS-02 E04／地質 | [獨立 GIS](ms02/E04-spatial.md)：9 個 UTM 參考點最大差 0.00022 m，確認數值回轉；兩份地質幾何皆覆蓋固定框 mAl。 | 九點不是 DEM 外框；GPR／LiDAR 是否同址仍未知，衍生 ArcGIS 重取不是另一套地質量測。 |
| MS-03 三原表 | [原表狀態](ms03/original_table_status.csv)：找出 Cohen-Zada 的確切檔案 DOI。 | 真正原表仍未拿到；所有格內成員狀態保持未知，HTTP 封鎖不是零筆。 |
| MS-03 形貌 | [像元取樣界線](ms03/DECISION.md)：AD1 典型等效直徑對應約 3.08 CTX 或 6.7 MOC 取樣，邊界定位敏感。 | 不是校準後檢出門檻，不代表無多邊形，保持形貌未知。 |
| MS-03 T1811 | [正式產品標籤](ms03/T1811_provenance.md) 指向 1.03.94；實取 CAT 7.4 程式庫不含該執行程式。 | 無法歸因殘差，需要執行設定、係數、遮罩、輸入及中間陣列。 |
| MS-03 光譜辨識上限 | [實際近鄰波段](ms03/spectral-limits/DECISION.md) 在兩組資料分別偏離名義 1525 nm 約 10.83、16.60 nm。 | 是取樣查核，不是冰指標；缺大氣／霜控制、精定位及噪音校準。 |
| MS-03 AD1 | [原研究交叉索引](ms03/crosswalk_status.json) 找到作者指引用的 2008 GPR 研究。 | 沒有確定雷達測線與熱測站坐標；保持一般方法參照。 |
| 新穎性／賽題 | [既有先例](common/novelty.md) 已覆蓋 UV、Beacon、Haughton、AD1，並核對賽題要求的新地球類比。 | 可以展示新的比較流程，不能宣告發現新類比、通過賽題或科學完成。 |

[分工與驗收門檻](WORKSTREAMS.md)｜[展示檢查](web/CHECKLIST.txt)

## 網站與正式提交是兩件事

`web/` 保存現行候選互動展示的公開資產；`deployment.json` 記錄來源快照及檔案指紋。正式站以對外實際讀回為準，Cloudflare 外部建置檢查的舊紅燈不能和預覽資料核對混為一談。

官方 Project Demo 和 Final Project 是兩個欄位；新版互動站屬 Final Project 候選。未代寫正式報告／簡報，也未替隊伍正式送出。[NASA 主辦方欄位說明](https://github.com/nasa/spaceapps/discussions/1991)。
