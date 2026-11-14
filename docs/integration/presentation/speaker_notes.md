# Team zasa 研究展示講稿

本版 8 頁；圖表與結論沿用固定研究提交，未新增場址或資料分析。

## 1. 地球場址能幫我們回答哪些火星冰問題？

開場：我們選擇三個既定火星候選，檢查地球資料實際能支援哪些研究用途。任務目的是在投入新量測前，把可用資料、已知先例與判讀限制說清楚。

這輪完成的是既有資料分析、來源 QA 與配對適用性查核。乾覆土如何改變熱訊號、影像中的多邊形是否可比較，是研究問題；三個火星格的地下冰真值尚未取得。保留或降級指的是用途證據是否足夠，不是地點好壞排名。

本版 8 頁依使用者要求製作。正式提交頁數、表單及格式仍需隊伍向主辦確認；不宣稱本檔已滿足提交規格。

### 本頁來源

- [R01T：MS-01 熱訊號補充報告](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/docs/research/MS-01/thermal_followup.md)
- [R02：MS-02 報告，§8B 最新 Adventdalen 處置](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/docs/research/MS-02/report.md)
- [R03：MS-03 報告，最新形貌／索引查核與降級](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8fa07afac4a98096958880f6a5ece16f35abc4db/docs/research/MS-03/report.md)

## 2. 三個名義候選格，四個資料面向

三點座標使用火星 planetocentric 緯度、east-positive 經度。名義格都是 0.5° × 0.5°，這只是候選範圍，不是所有儀器解析度或有效影像範圍。MS-01 中心 56.75°N、72.75°E；MS-02 52.75°N、168.25°E；MS-03 57.75°N、242.25°E。

地形、溫度／熱性質、水／冰、大氣／沙塵保留原產品物理意義。MOLA 區域地形約 3.7 km 基線；TES 為 20 pixels/degree 產品；MCS 為 5°、MY29–36 的 03/15 LTST 彙整背景，不能稱同日振幅或站點實測；SWIM 是資料一致性，不是冰量或機率；CDOD 是 9.3 μm 柱光學厚度，MY34/35，不是沉積率。更細的共同網格不會增加原生細節。

本簡報沿用各 PR 數值與查核，未重新擷取火星網格。MS-02 原始產品存取受限，原報告依交接資料核對，不宣稱所有點均已由本輪從原始資料重算。

### 本頁來源

- [D01：三個火星點的原生資料支撐紀錄](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3cc8488577535e2fa4d146021fde51f8ff6cc667/outputs/research/mars_reselection_20261114/candidate_native_evidence.json)
- [R01T：MS-01 熱訊號補充報告](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/docs/research/MS-01/thermal_followup.md)
- [R02：MS-02 報告，§8B 最新 Adventdalen 處置](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/docs/research/MS-02/report.md)
- [R03：MS-03 報告，最新形貌／索引查核與降級](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8fa07afac4a98096958880f6a5ece16f35abc4db/docs/research/MS-03/report.md)

## 3. MS-01｜已知冰界面，如何約束熱訊號？

圖 F01 依交付 comparison.json 的四條主要剖面重繪，沒有重新擬合或重新解析原始檔。橫軸是冰界面 24 小時半振幅除以上層半振幅，無單位。點為原計算結果，橫線是逐日留一敏感度範圍，不是信賴區間。原擬合含截距、線性趨勢與 24 小時 sin/cos，溫度半振幅以 K 表示。

期間固定在原印刷時間 2010-11-07 00:00 含至 2010-11-18 00:00 不含。S/M/D 各 264 個同站共同有效逐時列，W Campbell 528 個半小時列；沒有跨站或 Campbell–HOBO 配時。M 上層探針是 1 cm。來源為作者已校準／篩選匯出，不是未處理 logger bytes。

界面分量都較小，可用於分層模型與資料品質檢查。D36 與 W42 比值不隨深度單調，跨站材料與邊界條件未控制；所有主剖面已知含冰，缺同材料無冰對照，所以不能證明冰獨有訊號或建立冰深校正。S/D 座標版本衝突仍未解，按匯出／序號辨識，不作坡向配準。W 短版與長版匯出的時標脈絡不同，未合併。MS-01 地下冰存在、深度與純度仍未知。

### 本頁來源

- [R01T：MS-01 熱訊號補充報告](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/docs/research/MS-01/thermal_followup.md)
- [D02：UV 固定窗口結果、有效列與敏感度](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/outputs/research/MS-01/thermal_followup/comparison.json)
- [P01：Marinova et al. 2022（原始研究）](https://doi.org/10.1017/S0954102022000025)
- [P02：UV 作者校準／篩選資料，固定 Zenodo v1](https://zenodo.org/records/10553882)

## 4. MS-02｜用途可保留，證據不能跨點拼接

MS-02 保留 University Valley 為乾燥覆土下冰膠結層與季節熱響應的過程參照。這是用途支持，不是定量最相似，也不是 MS-02 地下冰證明。

Adventdalen 降為一般方法參照。F02 是依交付 footprint.csv 與報告 §8B 整理的證據範圍表，沒有新量測或新距離計算。CS-1：78.201°N、15.840°E，0–3.22 m 岩芯，有 OSL 年代、含冰量與冰構造；記錄涵蓋約 3000 年，取芯日期未萃取。ADE：78.1722°N、16.0613°E，2017 年 3 月鑽孔 13 m / 9 m，研究孔隙水化學及凍結結構。兩錨點間 5.97 km 沿用 MS-02 原計算。

WISDOM 的 2022 年 3 月多邊形溝槽測線未取得座標，只有摘要層級；約 1.5 m 反射是作者解釋，缺該溝槽獨立冰真值。Longyearbreen 冰洞真值屬另一地形，不能挪用。未知座標不等於已確認不重疊，但不能視為同址。

保留 CS-1 覆土堆積與同生冰的地球過程證據；雷達驗冰的具體配對證據不足。沙塵光學厚度不能轉成覆土厚度或堆積率。原報告早段部分假設已由 §8B 降級取代；未採用未核實的水活度與 2560 h 聯合門檻。

### 本頁來源

- [R02：MS-02 報告，§8B 最新 Adventdalen 處置](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/docs/research/MS-02/report.md)
- [D03：Adventdalen 證據範圍表](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/outputs/research/MS-02/footprint.csv)
- [P03：Rasmussen et al. 2023 作者稿，§§3.2–3.5／5.4](https://backend.orbit.dtu.dk/ws/files/329047704/1_s2.0_S0277379123001853_main.pdf)
- [P04：Rotem et al. 2023，§§2–3](https://tc.copernicus.org/articles/17/3363/2023/)
- [P05：Brighi et al. 2025，WISDOM 摘要，僅摘要](https://meetingorganizer.copernicus.org/EPSC-DPS2025/EPSC-DPS2025-710.html)

## 5. MS-03｜有目錄覆蓋，形貌仍無法確認

F03 依已交 CTX 足跡重新排版，保留原局部影像像素；未重算幾何或新增判讀。左為火星名義格 57.50–58.00°N、242.00–242.50°E 與三個 CTX 目錄足跡；中為 D01_027566_2370_XN_57N117W 的局部原生 EDR。AD1 只以已交幾何摘要作取樣尺度說明，不與火星影像混用座標。

三個 CTX 產品拍攝日期為 2010-07-25、2012-06-13、2025-01-31，名義取樣 6.08–6.11 m/pixel。原圖中的局部原生影像為 2012-06-13，6.09 m/pixel，未完成精定位／正射，存在條帶與低對比。目錄足跡聯集涵蓋名義格，不代表整格有效像素或可辨識細節均已核實。

AD1 GIS 共 185 個有效多邊形，EPSG:32633，等效直徑中位 18.485 m。源文影像為 2008 年 HRSC-AX，2009 年為現地工作／資料目錄脈絡，原 raster 未取得，本輪不聲稱已做地球影像 QA。18.5 m 除以 6.09 m/pixel 約 3.04 像素，只示意取樣，不是偵測閾值。

受查 ODE 與任務索引沒有找到可直接支援格內判讀的有效 HiRISE 紀錄，不構成完整歷史無覆蓋。AD1 退出目前有證據支持的具體配對，保留一般已知方法參照。現有證據既不能確認相似，也不能確認不同或不存在。成因及地下冰還需同位材料／層序、精定位影像與獨立地下結構證據。

### 本頁來源

- [R03：MS-03 報告，最新形貌／索引查核與降級](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8fa07afac4a98096958880f6a5ece16f35abc4db/docs/research/MS-03/report.md)
- [D04：MS-03 影像產品、日期、足跡及品質](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8fa07afac4a98096958880f6a5ece16f35abc4db/outputs/research/MS-03/morphology/image_inventory.csv)
- [D05：AD1 幾何摘要](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8fa07afac4a98096958880f6a5ece16f35abc4db/outputs/research/MS-03/morphology/AD1_geometry_summary.json)
- [P06：Ulrich et al. 2011，既有 Svalbard–Mars 比較](https://doi.org/10.1016/j.geomorph.2011.07.002)
- [P07：AD1 既有 GIS 資料集](https://doi.pangaea.de/10.1594/PANGAEA.921087)

## 6. 前人已做什麼？本隊實際增加什麼？

University Valley 已有觀測、熱傳模型與火星類比研究；Adventdalen／AD1 已有火星形貌比較及雷達方法工作。這些不是本隊首次提出。

MS-01 增加固定窗口、逐站／逐通道 QA 與已交熱振幅比較；MS-02 增加出處、位置、時間、深度的共址稽核，修正把不同點拼成聯合驗冰的主張；MS-03 增加固定候選格的影像可辨識性檢查與原始 AD1 GIS 幾何核對。這些屬重現、資料整合與適用性查核，可追溯而可檢查。

我們沒有新場址發現、新的火星冰觀測、受控辨識效能或全球完整新穎性排除。相同方法組成已有先例，不能把較長的方法描述稱全新流程。

### 本頁來源

- [R01T：MS-01 熱訊號補充報告](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/docs/research/MS-01/thermal_followup.md)
- [R02：MS-02 報告，§8B 最新 Adventdalen 處置](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/docs/research/MS-02/report.md)
- [R03：MS-03 報告，最新形貌／索引查核與降級](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8fa07afac4a98096958880f6a5ece16f35abc4db/docs/research/MS-03/report.md)
- [P01：Marinova et al. 2022（原始研究）](https://doi.org/10.1017/S0954102022000025)
- [P06：Ulrich et al. 2011，既有 Svalbard–Mars 比較](https://doi.org/10.1016/j.geomorph.2011.07.002)

## 7. 三點比較：可支持的用途與下一筆關鍵證據

三點沒有總體相似度排名。保留或降級只針對已提出用途及當下證據。MS-01 的 UV 是已知剖面方法參照，但不能唯一歸因；MS-02 UV 保留，Adventdalen 僅 CS-1 地球過程證據可用；MS-03 AD1 不保留為具體形貌配對，形貌仍未知。

下一筆關鍵證據是研究缺口，不是本隊已取得成果，也不是正式期望資訊價值計算。MS-01 需要同材料無冰對照與邊界條件；MS-02 需要精確測線、同位獨立冰真值；MS-03 需要格內可精定位且能辨識邊界的影像及品質檢查。即使未來形貌相近，也不能直接推出相同成因或冰量。

共同限制：地球與火星材料、輻射、大氣、重力與日照條件不同；溫度不等於熱慣量，SWIM 不是冰量，柱光學厚度不是沉積率。不同尺度支撐不直接相減、拼接或排名。Campbell 與 HOBO 校時仍未確認，跨 logger 配時／相位結論禁用。

### 本頁來源

- [R01T：MS-01 熱訊號補充報告](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/docs/research/MS-01/thermal_followup.md)
- [R02：MS-02 報告，§8B 最新 Adventdalen 處置](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/docs/research/MS-02/report.md)
- [R03：MS-03 報告，最新形貌／索引查核與降級](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8fa07afac4a98096958880f6a5ece16f35abc4db/docs/research/MS-03/report.md)
- [D01：三個火星點的原生資料支撐紀錄](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/3cc8488577535e2fa4d146021fde51f8ff6cc667/outputs/research/mars_reselection_20261114/candidate_native_evidence.json)

## 8. 目前的價值：讓下一步研究有可檢查的起點

收束：完成的是三個固定候選的用途與資料適用性檢查。UV 可支援熱傳資料重現及模型 QA；Adventdalen 證據不能跨點拼成雷達驗冰；MS-03 形貌未知，AD1 降級。把不足說清楚，可以避免把後續工作建立在不成立的聯合證據上。

後續驗證需求已列明，沒有在本輪執行新實驗。團隊現在可稱資料整合、QA、重現與研究需求設計；不能稱新場址、首次類比、偵測準確度或火星冰已證實。

待確認：S/D 位置來源衝突；W 不同匯出版本與 Campbell/HOBO 歷史時標；Adventdalen 雷達測線／真值及僅摘要來源；MS-03 格內有效像素與更細影像。本 8 頁展示稿仍需確認正式提交格式。所有研究 PR 作為各自固定 SHA 輸入，不代表已合併或主線最終科學驗收。

### 本頁來源

- [R01T：MS-01 熱訊號補充報告](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/b4b6929e890018668ef4faa9a74128a4ce5aa8df/docs/research/MS-01/thermal_followup.md)
- [R02：MS-02 報告，§8B 最新 Adventdalen 處置](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/38b8fa0dea527b1cc47aeb02dc260e039da37122/docs/research/MS-02/report.md)
- [R03：MS-03 報告，最新形貌／索引查核與降級](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/8fa07afac4a98096958880f6a5ece16f35abc4db/docs/research/MS-03/report.md)
