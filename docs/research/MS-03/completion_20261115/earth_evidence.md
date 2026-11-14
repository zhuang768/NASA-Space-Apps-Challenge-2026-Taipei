# MS-03 地球證據補充（2026-11-15）

固定來源版本為 main `234e58a8a0a0a9966e97e1b13d7ccc587cf3e8aa`。本補充保留 MS-03-E01／E02 的原候選 ID、座標與處置，補齊可取得的大氣描述及直接先例；不把一般方法參照升為已成立的火星配對。

## 本輪真正補上的資料

W 的既有短版作者處理匯出，已重新核對 SHA256 與 Zenodo 頁列的 MD5 `ae2133eac5c92c695c5f6ef93bcbbd25`。同一檔案有兩種日期字串格式，本程式明確解析兩者；17,705 列印出時刻均為連續 30 分鐘、沒有重複。僅取 **2010-01-01 00:00 至 2010-12-01 00:00（不含）**，得到 **16,032 列、11 個完整月份**。五個大氣／輻射欄都無非有限值；輸出 5 列期間摘要及 55 列逐月統計。不補 12 月，不稱全年平均，不與長版匯出混用。[CEW1]

資料表保留氣溫、相對水／相對冰的 RH、日照、風速各自的單位和來源欄位。這能檢查 W 點自身的邊界條件，不能與火星粗格 MCS 或 CDOD 直接相減。沒有新的沙塵柱量或沉積率；風速也不是沙塵代理量。作者已校準處理，未提供的逐列處理旗標不能由本次摘要補出。[CEW1]

2022 原文 Methods 將氣溫／RH、風速、日照測高分別列為 1.2、1.08、1.27 m；氣壓 **82.8 kPa 是模型假設，非實測**。風速儀型號在同一原文不同段落分別寫 05103／05013，本補充保留此差異。風速 0 值不能證明真正無風；樣本數不能消除系統誤差。[CEW2]

## 補查到的直接先例

Christopher P. McKay、Margarita M. Marinova、Kaj E. Williams、Michael T. Mellon（2026）的 *Summer snow determines the depth to ice-cemented ground under dry permafrost in Antarctica*，Antarctic Science **38**(2), 122–134，DOI [10.1017/S0954102025100448](https://doi.org/10.1017/S0954102025100448)，online 2025-11-27。原文 Environmental data 明列同一 W 座標及相同 University Valley 資料來源；研究夏雪、水汽邊界和冰桌穩定。因此這是 **同地、同邊界過程的直接先例**，不能把本隊「覆土／表面邊界造成冰判讀歧義」說成首次。[CEW3]

其 Discussion／Extrapolating 模型假設必須保留：一年資料代表長期、以表面 RH 門檻辨識雪事件、以簡化衰減估計界面。它不能解除本資料的時標問題，也不能證明 MS-03 有冰。新增的是本次固定格資料適用性與原始匯出 QA；並非獨立重做該物理驗證。[CEW3]

## 兩候選四面向與用途

逐面向精確引用、期間與缺值在 [earth_four_dimensions.csv](../../../../outputs/research/MS-03/completion_20261115/earth_four_dimensions.csv)，簡表在 [earth_comparability.csv](../../../../outputs/research/MS-03/completion_20261115/earth_comparability.csv)。W 為點位：−77.86215°、160.71010°E，不能加上任意半徑。AD1 的 metadata 外框與 185 個既有向量仍是測繪支持範圍，不是感測器座標、連續地下冰範圍或實驗場邊界。

W 可用來規劃「已知歷史界面、覆土與表面邊界需分開量測」的控制。若要反演，還要獨立 k、密度、熱容、時標與表面條件；本輪沒有計算熱慣量、導熱率、相位延遲或冰深。Campbell／HOBO 不配時，短／長版不拼接。

AD1 可作已發表幾何方法與取樣尺度參照。Matsuoka et al. 2018 的 TR1–TR3 監測研究有明確熱／雪測法，但尚未取得能將這些感測器逐點註冊到 AD1 GIS 的證據。因此其熱與雪資料只能列為 **Adventdalen 監測情境**，不能填入「AD1 現地溫度」。原文 Methods 將表面溫度定義為 0.02 m 深、通常每小時紀錄；相機不提供完整極夜雪紀錄。[CEA2]

現有 MS-03 火星影像仍沒有可靠閉合邊界樣本，所以 AD1 維持一般方法參照。沒有地球／火星共同尺度地形或同定義沙塵數據，不算整體相似度。實際冰深、冰量、承載、採冰與基地可行性維持未知。

## 重現與來源

```bash
python3 outputs/research/MS-03/completion_20261115/earth_atmosphere.py
python3 outputs/research/MS-03/completion_20261115/earth_validate.py
```

程式預設讀取已隨交付保存的 [earth_raw/](../../../../outputs/research/MS-03/completion_20261115/earth_raw/README.md) 無損 gzip，不依賴其他本機原件或網路。2,673,975 bytes 的作者處理短版原件經 gzip 壓成 506,804 bytes（mtime=0、空檔名標頭）；解壓的原始 bytes／換行／時標逐位元一致。保留 CC0 來源署名及壓縮前後 hash；沒有校時、編輯數值或重新校準。

原始公開 URL、雜湊與欄位在 [earth_input_receipt.json](../../../../outputs/research/MS-03/completion_20261115/earth_input_receipt.json)；來源原讀範圍在 [earth_source_read_log.csv](../../../../outputs/research/MS-03/completion_20261115/earth_source_read_log.csv)，搜尋詞與日期在 [earth_search_log.csv](../../../../outputs/research/MS-03/completion_20261115/earth_search_log.csv)。原資料保存、統計與重現程式一起交付；未取得的 logger 原件與時標紀錄仍維持缺件。

- CEW1：Marinova（資料收集者），Zenodo [10.5281/zenodo.10553882](https://doi.org/10.5281/zenodo.10553882)，固定短版 Campbell 檔；既有本機 bytes 重新核驗。
- CEW2：Marinova et al. 2022，[10.1017/S0954102022000025](https://doi.org/10.1017/S0954102022000025)，Meteorological measurements；Energy balance pressure paragraph；未聲稱全文重審。
- CEW3：McKay et al. 2026，[10.1017/S0954102025100448](https://doi.org/10.1017/S0954102025100448)，Environmental data；Discussion／Extrapolating；來源年份另用 USGS 原作者機構紀錄互核。
- CEA2：Matsuoka et al. 2018，[10.1002/ppp.1985](https://doi.org/10.1002/ppp.1985)，§2、§3.1–3.2、§4.1；未下載補充感測器原時序。
