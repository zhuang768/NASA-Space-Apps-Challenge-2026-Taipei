# MS-02：重複影像幾何與 MONS 支援尺度筆記

日期：2026-11-15 Asia/Taipei。這是可重現的資料筆記，並非正式報告正文。基準 `521740108050ba16e406f8becb67a786179ff8bd`，固定範圍仍為 52.50–53.00°N、168.00–168.50°E。

## 實際完成的計算

使用既有原始目錄足跡、時間、入射角與太陽黃經，重新計算 5 景 CTX 的個別覆蓋及 10 組交集；沒有使用未驗證的 JPEG 配準。`analyze_support.py` 完全離線、僅需 Python 標準函式庫。

- 五景名義聯集覆蓋全部 ROI；名義上至少兩期覆蓋也達全部 ROI，至少三期約 **68.240%**、至少四期約 **5.122%**。這是目錄幾何，不是已通過定位、曝光、雲塵或解析度 QA 的有效像元比例。
- D01（2012-06-09）與 J02（2016-04-13）名義交集約 **247.508 km²，46.553% ROI**，基線 **1403.543 地球日**，入射角差 **2.20°**、太陽黃經差 **14.22°**；可作後續同季節影像準備的具體一組資料，尚不能聲稱已可量測變化。
- J02 與 V16（2024-12-31）交集約 **366.613 km²，68.955% ROI**，但太陽黃經差 **113.05°**；亮度或陰影差異不能直接解釋為覆土或冰變化。
- 最長影像時間跨度由 G23 的 2012-05-12 至 V16 的 2024-12-31，約 **4615.496 地球日**。並非全格每個像元都擁有此最長基線。

幾何方法：以火星半徑 3,396,190 m，將經緯度線性邊的球面面積積分與凸多邊形交集結合，得 ROI **531.671871 km²**。既有程式採 LAEA 投影後直線頂點面積 **531.665374 km²**；差異是邊界近似，並非更換範圍。獨立實作重現既有 5 個 LAEA 覆蓋比例的最大誤差為 **2.54×10⁻¹⁴**。輸出的原始浮點比例可能超出 1 約 10⁻¹⁴，屬計算捨入。

`verify_support.py` 用 1000×1000 格點及 cos(緯度) 面積權重、直接半平面判斷，獨立核對每對交集與多期覆蓋，20 項檢查通過。這只驗證幾何計算，不能驗收形貌、覆土累積率、冰存在或冰量。

## MONS：補清實際尺度與正確數值來源

[Pathare et al. 2018](https://doi.org/10.1016/j.icarus.2017.09.031) 的原文已讀 §3.1、§5 與 Appendix pp114–115。儀器 FWHM 約 550 km；其採用的 N=16 球諧反演有縱向半波長 11.25°，以論文半徑3390 km換算約 **665.625 km**。半波長與 FWHM 定義不同。細網格不代表細空間資訊，兩層 WEH 也依賴覆土模型。

原文明確將 N16 全球數值列於 **Supplemental Table S1**，未反卷積結果列於 **S2**。本輪未取得表格，不能給 MS-02 的 Wup、Wdn、D 或誤差；這些欄位維持 null。未從彩色圖取值，也未倒算 SWIM 一致性當冰含量。`mons_scale_constraints.json` 分開記錄文獻尺度與本格缺值。

## 已查的可行資料途徑與仍缺證據

| 項目 | 本輪取得／查核 | 尚未完成 |
|---|---|---|
| 原始 CTX 五景 | 目錄足跡與時間已作精確交集 | EDR 輻射校正、SPICE 相機投影、有效遮罩、同物件配準與變化誤差 |
| Caltech CTX V01 | [官方產品說明](https://murray-lab.caltech.edu/CTX/V01/TilePages/)說明4°tile及原始來源 seam／tie-point 圖。固定格依命名落在 E168_N52 | 該tile的datasheet／GeoTIFF未取得，未宣稱已讀影像。拼接圖本身也不是兩期變化序列 |
| USGS ISIS 方法 | [ctxcal](https://isis.astrogeology.usgs.gov/dev/Application/presentation/Tabbed/ctxcal/ctxcal.html)、[cam2map](https://isis.astrogeology.usgs.gov/dev/Application/presentation/Tabbed/cam2map/cam2map.html) 明確提供輻射校正及依SPICE投影 | 沒有把四角插值定位包裝成相機模型，也未聲稱執行ISIS |
| MONS數值 | 原論文與正確補充表目標已識別 | ScienceDirect回403；SWIM開啟回523；CDN候選位址未能取得。僅證明本環境這些嘗試失敗，不證明公開資料不存在 |
| PDS neutron products | [NS特殊產品](https://pds-geosciences.wustl.edu/missions/odyssey/grsspecial.html)與[IDND說明](https://ode.rsl.wustl.edu/mars/pagehelp/Content/Missions_Instruments/Mars_Odyssey/GRS/Derived%20Data%20Sets%20from%20Individual%20Investigators/IDND.htm)已辨別 | 這些是中子通量或校正計數序列，不能冒充Pathare兩層WEH數值表 |

因此本輪解決了「是否有重複觀測幾何、哪些配對具體可用、MONS實際尺度與目標來源」；**已校正局部形貌／定量變化、覆土累積率及本格 WEH 數值仍未完成**。不能用此筆記宣稱 MS-02 所有科學缺口已關閉。

重現：先執行 `python3 analyze_support.py`，再執行 `python3 verify_support.py`（後者需 numpy）。來源 URL 與逐次嘗試分類見 `source_attempts.csv`；其中 CDN 副檔名及 tile 個別網址是依命名規則構造的候選位址，不是已核實存在的檔案。
