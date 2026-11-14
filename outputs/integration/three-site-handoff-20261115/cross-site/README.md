# 三點共用｜證據尺度與模型相依性查核

- `python3 reproduce.py` 以三個固定範圍重新計算 `cross_site_checks.csv`，不需要第三方套件。三份 `*_source` 來自 [固定研究基準 1506ede](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/tree/1506ede572435588eb5e64f95f24639279b77e56/outputs/research) 的原始提交內容。
- 同一球形火星半徑 3,396.19 km 計算面積及球面中心距。MCS 背景格中心相距 127.9／146.7／150.1 km；MY34 沙塵格中心相距 78.1／17.3／50.3 km。這是格中心偏離量，不是足跡、位置誤差或資料失效判定。
- MCS 有效日夜配對為 69／75／60 組，各除以 288 個預期年季配對，約 24.0%／26.0%／20.8%。這是專案背景產品篩選後的完整度；不能冒充 Piqueux 原始觀測或連續現地時序。
- [Piqueux 模型原生格](https://doi.org/10.22002/D1.1316) 輸出條件式深度 0.427／0.450／0.103 m。熱慣量不是硬度；深度不是直接量測；三格沒有獨立冰存在、深度、含量真值。
- 按 [Sizemore 2026 圖 2／§3.3](https://www.astroexplorer.org/details/psjae7b38f2b) 與 [SWIM 作者團隊章節 §2.2.2、§2.3.1](https://nathaniel.putzig.com/publications/Putzig_and_Morgan_et_al_2023_preprint.pdf) 做明示假設情境。只取 PQ19 的已建模冰格分項：(C_{PQ}=clamp((0.50-d)/0.20,0,1))。得到 0.365／0.250／1.000。若套用三個熱分項等權且全部齊備、使用 0–1 m 公式，名目 PQ19 項為 0.051／0.035／0.139。這只是兩個已公布公式串接的試算，不重建歷史 SWIM2 格網，未驗證當地遮罩、重投影或權重。
- 在同一假設下把輸入深度上下擾動 5 cm，MS-01／02 的名目合成項各變動 ±0.034722，MS-03 未出 0.30 m 飽和區所以不變；這是敏感度示例，**不是深度誤差、信賴區間或比較冰量的依據**。1–5 m 式沒有直接 PQ19 熱項；兩深度層仍含共享地形與雷達分項。
- [2019 年 7 月會議版本](https://www.hou.usra.edu/meetings/ninthmars2019/pdf/6027.pdf) 明載 3 ppd、低 TI 遮罩 120、Phoenix 模型範例 12 cm；[12 月正式論文](https://doi.org/10.1029/2019GL083947) 範例 8 ± 2 cm、遮罩 100，[11 月 Caltech v1 資料](https://data.caltech.edu/records/ym7fc-x0r93) 為 2 ppd。版本差異可引用，但無法重建 3→2 ppd 轉製或推定原因。
