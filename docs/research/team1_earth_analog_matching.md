# Team 1 地球類比配對｜第一組交接

研究日期：2026-11-14（Asia/Taipei）。版本：第一組，待隊友 2 查核。本文的「新用途配對」表示重新依冰探查用途評估地球場址，不表示場址、設備或用途具有新穎性。I-02、D-03、D-04 尚未完成配對，不能將本檔當作四組完成版。

## 1. 配對表

| 固定地球候選 ID | 火星候選 ID | 地點／國家或地區 | 地球座標（北、東為正） | 具體測試用途 | 判定 |
|---|---|---|---|---|---|
| EARTH-UV-001 | I-01：54.25°N, 1.25°E | University Valley 氣象站 W 周邊，McMurdo Dry Valleys，南極洲（不列為單一主權國家） | −77.862150°, 160.710100°；文獻原值 77°51.729′S, 160°42.606′E | 以已量測的乾燥覆土—冰膠結層界面，檢查熱探針／淺層探測判讀與分段鑽採的界面辨識、樣品升溫及冰損失 | 有條件的局部「方法／材料」類比；不是整體環境、地形或資源量配對 |

ID 固定代表此地球研究場址，不隨火星對象或排序改名。座標為文獻氣象站的定位錨點，不是新核准鑽孔；文獻未在本次讀取段落明示水平 datum，不聲稱六位小數代表測量精度。新採樣須另定位、確認現況及取得許可。

## 2. 已讀資料與用途重新評估

- GitHub connector 已查核主分支完整樹及原文：`docs/site_discovery_brief.md`、`docs/mars_discovery_handoff.md`、`outputs/mars_discovery/mars_site_discovery.json`、`docs/earth_inventory.csv`、`docs/cross_reference.md`、`docs/earth_pipeline.md`、`outputs/analysis/shortlist.csv`。基準 commit：`3e3ffff3d8d0814c407eacdc0a83d8b45a5123b8`。
- 總 Excel **只讀**：`NASA_Space_Apps_2026_All_Data.xlsx`，SHA-256 `a789fcdc9c0a7e780f85b63687ad54f05b87cd6e341ecf024375dcd6fcb3f731`。其 Overview 標示資料快照為 2026-11-14 15:42:59 +08:00。
- 先前指定的 `ice_candidate_followup_2026-11-14.md` 未見於此 GitHub 快照。Excel 的 `Report Text!A475:G505` 收錄其後續報告，來源路徑為 `docs/research/ice_candidate_followup/README.md`；`File Index` 第 65 列記錄原檔 SHA-256 `dd0556061d4fb2a89b1f0bef89112ff597142016326071ac2305a55fc3cd3689`。connector 對此新版路徑回傳 404。因此本次讀到的是 **Excel 英文轉存版本**，未冒稱已查得 GitHub 原始 Markdown。
- `Ice Candidate QA!A1:BB3` 提供兩個火星點的有效格數與深淺 SWIM 背景；`Earth Candidates!A1:AV73` 提供 72 筆版本化候選。舊 ID 必須連同 analysis version 使用；同名 ID 在 4 km、10 km 取樣版本可以是不同地點。
- 舊候選來自 100 × 100 km 地形視窗，水／冰欄仍為 unknown。六個已有 POWER 背景的中心即使氣溫低，也沒有直接的淺層冰深度、純度、連續性或採樣證據。故不直接沿用既有 Jezero/Gale/Arcadia 配對，不為冰探查用途強行選入。
- University Valley 是本次依直接冰層與量測證據補入的場址。舊搜尋限定 60°S–60°N，本來沒有搜尋此極區；未被舊名單收錄不是新穎性證據。

## 3. 火星 I-01 的比較依據

| 項目 | 已有資料 | 空間／期間與限制 |
|---|---|---|
| 地形 | 坡度 0.302596°；格內起伏 76 m | 0.5°名義格，約 29.64 × 17.31 km；MOLA 16 px/degree，坡度基線約 3.7 km。不是鑽機周邊地形或石塊尺度 |
| 溫度／熱性質 | TES 熱慣量 244.709671 J m⁻² K⁻¹ s⁻½ | 本地 2007 產品；產品年份不等於所有觀測年份。沒有此候選的合格日夜／季節地表溫度；熱慣量不是溫度或硬度 |
| 水／冰 | SWIM 淺層一致性 0.354307；原生名義格 100/100 有效 | SWIM 2.0，2021 產品，多源跨時期；名義原生格約 0.05°，先聚合再插值。數值不是 35.4% 冰、機率或已確認 <1 m 冰 |
| 大氣／沙塵 | MY35 年均 9.3 μm 吸收 CDOD 0.106878 | 原始重建支撐約 3°；0.5°只是共格。無本點近地風、壓力、沉積通量或磨蝕量 |

Excel QA 記錄：MOLA 64/64 有效；TES 93/100、7 個填充值排除；深層 SWIM 重取樣值 0.529793。這是既有 QA 的轉存記錄，本次未重跑火星管線；深淺 SWIM 共享輸入，不能算兩份獨立冰確認。來源：[GitHub 交接](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3e3ffff3d8d0814c407eacdc0a83d8b45a5123b8/docs/mars_discovery_handoff.md)、[原始 discovery JSON](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3e3ffff3d8d0814c407eacdc0a83d8b45a5123b8/outputs/mars_discovery/mars_site_discovery.json)、Excel `Ice Candidate QA` 第 2 列。

## 4. 地球配對證據、年份、解析度與缺漏

| 面向 | 地球可用證據 | 來源、年份、解析度 | 配對意義與缺漏 |
|---|---|---|---|
| 地形 | 岩質谷底的 W 站；約 1677 m 高程 | E1，2022 出版；現地站點，2009–2013 觀測 | 可布置界面探測剖面；沒有與火星相同尺度重算的坡度／起伏，不主張地形數值相等。絕對高程基準也不跨天體比較 |
| 現地溫度 | 文獻平均氣溫 −23.4°C；有表面、10、42、49 cm 溫度記錄 | E1；氣象系統 30 分鐘、另一組溫濕度感測器 60 分鐘；點測量 | 可測熱訊號與冰界面的關係。表面溫度有長段缺測及異常剔除；不能與 2023–2024 月資料當成同期驗證 |
| 水／冰 | W 站冰膠結界面在 42 cm；另有不同界面深度的測站 | E1 現地探針安裝深度；E2（2013）谷內調查報告 0–98 cm 冰膠結土深度範圍，屬離散調查，不是全谷連續冰圖 | 直接支持「乾覆土之下存在冰膠結層」的局部方法類比；不外推整個場址的冰量、純度、連續性或可開採量 |
| 地表溫度補充 | 桌面 MOD11C3.061：嚴格 QC 下日間 0/24、夜間 1/24 個月可保留；不產生年均或日夜差 | E4；2023–2024 月合成，0.05°；所選格中心 −77.875°, 160.725° | 品質篩選不足，不代表該地完全沒有觀測。網格混合谷地、坡面與冰雪；夜間唯一保留值 233.8 K 不是年均或極值 |
| 大氣 | 桌面 MERRA-2：PS 78,685 Pa；T2M 239.170 K；U10M +10.727、V10M +2.351 m/s | E3；2023–2024，24/24 月有效，按月天數加權；0.5° × 0.625°，最近格中心 −78°, 160.625° | 再分析背景，不是 W 站實測。T2M 與文獻氣溫時期、高度、支撐範圍不同；風分量不是平均風速或陣風 |
| 沙塵 | 同格 MERRA-2 DUEXTTAU = 0.002139，24/24 月有效 | E3；2023–2024 月資料，550 nm 沙塵消光光學厚度，再分析 | 不能直接與火星 9.3 μm 吸收 CDOD 相減；沒有本地沉積／磨蝕量，不配對沙塵耐受測試 |

**桌面資料的使用邊界：**本組實際開啟並抽取 24 個 MOD11C3、24 個 MERRA-2 SLV、24 個 MERRA-2 AER 檔。MODIS 關閉自動縮放後檢查原值 7500–65535、`QC == 0`，乘 0.02 得 K；這是全部品質位元均為最佳類別的保守篩選。MERRA-2 依檔內座標取最近格，遵守填充值遮罩，以 2023–2024 各月天數加權；不插值成站點實測。原始檔全部只讀。

SRTMGL30 本批範圍未涵蓋此南極緯度；ESA CCI Permafrost 本批為北半球產品，不能用其缺值推論此地無永凍土。GLDAS 本批緯度範圍不包含本站。GPM 降水、NDVI、VIIRS 氣膠與 MERRA 輻射資料不提供本站地下冰深度真值；本組未將它們計入冰存在證據，也未宣稱已完成這些產品的本站 QA。資料存在、可開啟和支持特定用途是不同層次。

## 5. 具體可測試什麼

以下為 **Team 1 提議的測試設計**，不是已執行結果，也不表示文獻已驗證這個火星點：

1. 在經重新確認的乾覆土—冰膠結層剖面，先做盲判熱探針／淺層探測，再用實際取芯界面深度驗證。記錄界面深度誤差、漏判、誤判與有效剖面長度，不能把低溫當成標準答案。
2. 固定鑽頭、轉速、推力與每段進尺，分段記錄扭矩、功率、鑽進速率、樣品溫度、回收質量與採樣前後含冰量。可檢查乾土進入冰膠結土時的辨識與取樣損失；功率單獨不能轉為冰含量或硬度。
3. 用已知界面深度、粒徑、密度與含冰量樣品，檢查熱訊號反演的多解性。未建立可信熱物性模型前，不把本站設定為 TES 熱慣量 244.71 的等效材料。

E5 證明相關鑽採／樣品處理系統曾在極地類比及火星環境艙測試，提供方法依據；不能把該研究的鑽進性能移植到新鑽孔或 I-01。現地作業仍需確認許可、樣品取得與現況；本交接不安排出隊。

## 6. 相似處與不能模擬處

**證據支持的相似處：**地球場址有乾燥覆土覆蓋冰膠結土，可用來研究「先探查、再取樣驗證」的方法。I-01 的資料只支持對可能淺層冰做後續探查，因此這是對研究問題的配對，不是已知地下構造的一對一重建。

**重要差異：**地球端有現地界面證據，火星端仍是多源指標；地球站點／剖面遠小於火星格點。南極氣象、雪霜、水汽、日照季節及粒料組成都未與 I-01 配準。兩地熱慣量、冰純度、覆土連續性與力學性質尚未建立相等關係。

**不能模擬：**火星低壓 CO₂ 大氣、低重力、輻射、完整日夜／季節熱循環、火星沙塵啟動與沉積。地球現地試驗不能直接給出火星昇華損失、鑽採耗能、水產量或安全著陸結論；需獨立環境艙與模型驗證。低溫／永凍土不等於可挖冰。

## 7. 來源索引

| 來源 ID | 可查核來源／讀取範圍 | 本組使用方式 |
|---|---|---|
| E1 | Marinova et al., **2022**, [Climate and energy balance of the ground in University Valley, Antarctica](https://doi.org/10.1017/S0954102022000025)，Antarctic Science 34(2), 144–171；Methods: Meteorological measurements、Results、Fig. 1 | 站點原座標、現地溫度、冰界面、量測間隔及缺測；已讀公開全文相關段落 |
| E2 | Marinova et al., **2013**, [Distribution of depth to ice-cemented soils…](https://www.cambridge.org/core/journals/antarctic-science/article/abs/distribution-of-depth-to-icecemented-soils-in-the-highelevation-quartermain-mountains-mcmurdo-dry-valleys-antarctica/EE34F569F8E954EE4DE86125C92E3188) | 已讀出版者摘要；0–98 cm 是調查範圍，不當作 W 站當前冰深度；未取得逐點資料，不指定調查點間距 |
| E3 | [NASA GMAO MERRA-2](https://gmao.gsfc.nasa.gov/gmao-products/merra-2/)；桌面 `air/MERRA2_400.tavgM_2d_aer_Nx.202301.nc4` 至 `202412.nc4`、`air/wind_pressure/MERRA2_400.tavgM_2d_slv_Nx.202301.nc4` 至 `202412.nc4` | 本次只讀抽取的 24 月再分析；來源年份指觀測／再分析期間，不是下載日；網格、變數及單位直接讀檔 |
| E4 | MOD11C3.061，[產品 DOI](https://doi.org/10.5067/MODIS/MOD11C3.061)、[NASA/LP DAAC 使用指南](https://lpdaac.usgs.gov/documents/118/MOD11_User_Guide_V6.pdf)；桌面 `temperature/MOD11C3.A2023*.061.*.hdf`、`A2024*.061.*.hdf` | 24 月 HDF 原檔、結構 metadata、比例因子與 QC；產品 DOI 網頁本次回傳 403，未把網頁無法開啟當作檔案不可讀 |
| E5 | Zacny et al., **2013**, [Reaching 1 m Deep on Mars: The Icebreaker Drill](https://doi.org/10.1089/ast.2013.1038)；[PubMed 作者摘要](https://pubmed.ncbi.nlm.nih.gov/24303959/) | 已讀摘要的鑽採／取樣測試方法背景；不引用其性能作為本站新測試結果，不做新穎性結論 |

## 8. 隊友 2 交接狀態

- 第一組鍵值：`EARTH-UV-001` + `I-01`；配對表見 `outputs/research/team1_earth_analog_candidates.csv`。來源文獻、原有資料和本次提議分開記錄。
- 請查核相同場址、相同測試用途的既有工作，以及來源是否支持本文主張；特別注意 E5 已有鑽採方法研究。Team 1 不給新穎性結論。
- 請保留候選 ID，以此鍵值回填查核意見；如需換測站或測試用途，先記錄修訂，勿用新 ID 隱藏來源變更。
- 狀態：第一組已備妥供查核，尚未收到隊友 2 的查核結果。I-02、D-03、D-04 留待第一組交接後依原順序處理。

本次僅新增這份研究文件及候選 CSV；未修改 `analog/`、評分權重、排名、網站、總 Excel 或既有科學輸出。OpenAI Codex 協助資料讀取、來源查核與交接撰寫。
