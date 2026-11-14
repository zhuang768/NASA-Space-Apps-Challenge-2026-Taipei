# 地球資料管線與配對方法

本輪完成的是區域地形篩選與 NASA 地球氣候背景查詢。四大面向保留在研究架構中，但尚未形成可比較的四面向數值模型。

## 執行

從 repo 根目錄執行。已在 Python 3.12 的獨立環境實測；大檔下載需要時間與約 1 GB 可用空間。

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt -e ".[dev]"
.venv/bin/python scripts/download_earth.py
.venv/bin/python -c 'from analog import mars; mars.download("mola_topography")'
.venv/bin/python scripts/rank_analogs.py
.venv/bin/python scripts/enrich_candidates.py
.venv/bin/python scripts/plot_analogs.py
.venv/bin/python scripts/rank_analogs.py --spacing-km 10 --output outputs/analysis_scale10km
.venv/bin/python scripts/summarize_run.py
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
```

`requirements-lock.txt` 記錄本次實際環境版本，沒有私人 repo 安裝網址或登入資料。原始下載位於被 git 忽略的 `data/raw/`；小型結果、來源紀錄與候選足跡位於 `outputs/analysis/`。下載中斷留下的 `.part` 不會作為完成資料使用。

## 本輪使用的資料

| 資料 | 取得與用途 | 單位、尺度及限制 |
|---|---|---|
| [NOAA ETOPO 2022](https://www.ncei.noaa.gov/products/etopo-global-relief-model) surface v1 | 免登入全球地形，實際下載 465,969,062 bytes | 原始 60 arcsec、EPSG:9518，WGS84 水平與 EGM2008 高程，m；先 2×2 平均到 120 arcsec |
| [NASA PDS MOLA](https://pds-geosciences.wustl.edu/mgs/urn-nasa-pds-mgs_mola_topography_derived/meg016/megt90n000eb.lbl) | 實際下載影像及標籤，產品版本 2.0 | 16 px/degree，IAU2000、planetocentric、東經正向；3396 km 球半徑，m 相對火星 areoid |
| [Natural Earth land](https://www.naturalearthdata.com/downloads/110m-physical-vectors/110m-land/) | 免登入陸地遮罩，下載檔 VERSION 為 4.1.0 | 1:110 million；不保證排除所有內陸水體或準確描述海岸 |
| [NASA POWER](https://power.larc.nasa.gov/docs/services/) | 六個候選中心的 2023–2024 月資料，免登入，原始 JSON 留存 | MERRA2/POWER，再分析與衍生資料；氣象網格 0.5° lat × 0.625° lon，不是場址實測或 4 km 觀測 |

來源清單保存 URL、SHA-256、檔案大小、版本、期間、座標與單位。來源快照見 `outputs/analysis/source_metadata/`；完整參數及本輪來源見 `results.json`。MOLA 標籤指出無量測格有插值，赤道附近軌跡間可能存在最長約 12 km 缺口。因此 4 km 是分析取樣間距，不能稱為真實有效解析度。

## 物理尺度與搜尋範圍

1. 搜尋中心覆蓋 60°S 至 60°N、全球經度，每 2° 一個中心，排除海洋中心及團隊指定的 Atacama、Iceland、Hawaii 方框。極區與 McMurdo 已因緯度範圍排除。這是全球中低緯帶的稀疏搜尋，不是全球每一位置的完整搜尋；100 km 視窗之間存在未搜尋空隙。
2. 每個視窗為局部球面方位等距座標中的 100×100 km 正方形。地球球半徑採 6,371,008.8 m，火星依 MOLA 標籤採 3,396,000 m；各自反算經緯度，不混用天體距離。地球 WGS84 以平均球半徑近似，在本輪區域尺度仍有橢球近似誤差。
3. 在 x、y 各 -50 至 +50 km 每 4 km 取樣，共 26×26 點。對來源網格做雙線性取樣，跨經度邊界正確循環。這是共同物理取樣，不代表兩種感測器具有完全一致的點擴散函數或有效解析度。
4. 用粗陸地多邊形檢查取樣點，至少 95% 在陸地；任何 DEM 缺值使該視窗不參與排名。陸地比例只是遮罩取樣比例。
5. 原始海拔只在各自視窗內計算高差，不跨天體比較絕對海拔。來源垂直基準差異沒有被當成場址相似特徵。

## 配對定義

每個視窗的地形向量為坡度中位數、坡度第 90 百分位、起伏量（最高減最低）。坡度使用共同取樣格的內部中心差分，4 km 點距對應 8 km 差分跨度；它不反映石塊、輪胎接觸、細小坡面或著陸風險。

```text
D = .25 × |slope_median_E − slope_median_M| / 1 degree
  + .25 × |slope_p90_E − slope_p90_M| / 2 degrees
  + .50 × |relief_E − relief_M| / 500 m
```

D 越小代表所定義的地形統計差距越小。1°、2°、500 m 與權重均為尚未校準的設計假設；不是任務工程門檻或統計信賴度。兩個坡度指標相關，合計占地形內部一半權重，沒有被宣稱為兩種獨立任務情境。此方法不檢查隕石坑形狀、空間排列、地質成因或礦物，統計接近不等於形態／成因相同。

完整排名與空間分散清單分開：先按 D 排序，再以至少 300 km 中心距離貪婪選取最多 12 個區域。這只是候選去重，不是互補場址最佳化。並列時依固定輸入順序處理。

Jezero 與 Gale 座標對應既有探測任務區域，不代表新選定的未來登陸區。Arcadia 40°N、170°W 是專案提出的目標中心，尚未由任務需求或 SWIM 結果驗證。

## 氣候與其他面向

NASA POWER 查詢 T2M、T2M_MAX、T2M_MIN、PRECTOTCORR、WS10M。24 個月數值按各月天數加權，包含 2024 閏年。任一月份缺失或為填充值，該變數的摘要保留 unknown。T2M 是 2 m 氣溫，T2M_MAX/MIN 摘要不是整段期間的極端最高／最低溫；日降水摘要也不是直接相加的年降水量。

氣候查詢只針對地形清單前兩名，沒有回填全球其他候選，也沒有改動地形排名。Jezero 前兩名顯示較濕的氣候，正好說明地形篩選不能直接代表整體火星類比。

- MODIS LST 日夜溫差不能直接相減於 TES 熱慣量；若要比較，應取得相同物理量，或建立有來源且經驗證的轉換模型。
- GPM 降水、SMAP 含水、NDVI 均不是 SWIM 地下冰一致性；NDVI 也不代表生命不存在。SWIM 分數不能當成冰含量或機率。
- MODIS 550 nm AOD 與火星 CDOD 在波長、粒子、氣壓及時段定義未對齊前，不能直接做等量差值。
- 光學厚度、粗地形及 POWER 氣候均不能證明礦物、洞穴、進入許可或成本。

## Earthdata 月資料入口

實測可免登入查詢 2023–2024 年四種產品，各 24 個月 granules；實際下載通常需 Earthdata Login。

```bash
.venv/bin/python scripts/download_earth.py --product lst
.venv/bin/python scripts/download_earth.py --product ndvi
.venv/bin/python scripts/download_earth.py --product precipitation
.venv/bin/python scripts/download_earth.py --product aod
# 本機設好 Earthdata 的 .netrc 後才加 --download
.venv/bin/python scripts/download_earth.py --product lst --download
```

CMR 中 MOD11C3/MOD13C2 版本為 `061`、GPM_3IMERGM 為 `07`、MOD08_M3 為 `6.1`。搜尋區間相交可能包含前一個月，程式按 granule 起始日期排除這種邊界項目。清單保存 concept ID、granule ID、資料 URL、時間範圍；有找到清單不代表下載或品質檢查完成。

這次未取得 MODIS/GPM 受保護原始檔，未執行其解碼、QA 遮罩與尺度／偏移量轉換。下載功能已寫好但尚未用有效帳號驗證。SPL3SMP_E 為每日區域後續資料，版本尚待確認，未混入月資料下載批次。不要把 9 km 網格間距當成土壤濕度的實際有效解析度。

## 敏感度與下一步

權重敏感度固定同一候選集合、目標、容許差與空間分散規則，只將權重改成 .4/.4/.2 與 .1/.1/.8。另在相同 100 km 視窗重跑 10 km 點距。尺度測試的陸地遮罩點數改變，使合格視窗略有差異，因此需同時報告數量與前兩名保留數。

下一步應先選定要驗證的任務與類比維度，檢查候選地質及既有文獻，補上同物理量環境資料，再討論四面向整合。未知項目未計分，也未當作符合。這輪尚未做未知證據翻轉模擬或資訊價值計算。
