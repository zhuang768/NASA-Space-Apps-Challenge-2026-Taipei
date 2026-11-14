# MS-03 報告技術措辭獨立核對

日期：2026-11-15（Asia/Taipei）。草稿：`/tmp/ms03-new-report.md`。本次只核定點數值與語義，沒有重跑全球篩選。

|檢查|實讀／計算證據|結果與修訂|
|---|---|---|
|CRISM原label|`local_validation/crism/sources/hsp0002de65_03_if218l_trr3.lbl`及`msp00018fda_01_if214l_trr3.lbl` lines118–120|三個實際欄分別為`MRO:ATMO_CORRECTION_FLAG=OFF`、`MRO:THERMAL_CORRECTION_MODE=OFF`、`MRO:PHOTOCLIN_CORRECTION_FLAG=OFF`。|
|CRISM欄位語義|官方DPSIS v1.3.7.7 §3.4.2 TRDR keyword表，web render lines2618–2620；已open及find原文件，不只搜索摘要|ATMO定義涵蓋photometric與atmospheric correction；PHOTOCLIN僅在THERMAL=PHYSICAL_MODEL;ADR_TE有效，OFF使用DDR坡度、ON使用CRISM photoclinometry坡度。它不是獨立photometric correction flag。在本THERMAL=OFF不能把它解為已執行任何熱模型坡度選擇。草稿已改全名與語義。|
|AD1 circularity|以`AD1_recomputed_geometry.csv`185列的area_m2／perimeter_m重新計4πA/P²；每列與既有circularity欄差<1e-14|中位0.8066001368914908，6位四捨五入0.806600；草稿增定義與無因次單位。未重描原像，不稱獨立地貌真值。|
|Piqueux原生索引|本機`/tmp/nasa_shared_validation/caltech/`的Lat/Lon/Notes/TI_SI/d_m五原檔，逐檔provider MD5與原piqueux_qa一致；實讀360×720矩陣|Lat[64]=57.75、Lon[484]=242.25、d[64,484]=0.103161566、TI=215.4277344。zero-based64/484即one-based65/485。草稿正確，模型非實測。|
|Marinova2022年份|Cambridge原出版頁題名與metadata|Antarctic Science34(2),144–171，online2022-04-20；已將online日補入草稿。|
|McKay2026年份|Cambridge原出版頁題名與metadata|卷期38(2),April2026,122–134；online2025-11-27。草稿年份／online日正確。|
|SHARAD尺度|radar_diagnostics/range_support.csv及公式c/(2B)，B=10MHz、c=299792458m/s|14.9896229m為理想真空界面分離尺度；37.5ns是取樣間隔。非本格實測有效解析力、local detection limit或冰存在機率。草稿已更精確限定。|

來源與讀取範圍：

- [CRISM DPSIS v1.3.7.7](https://pds-geosciences.wustl.edu/mro/mro-m-crism-3-rdr-targeted-v1/mrocr_2101/document/crism_dpsis.htm)，§3.4.2 keyword定義中的三條欄位；沒有聲稱本次重讀全文。
- [Marinova2022原頁](https://www.cambridge.org/core/journals/antarctic-science/article/climate-and-energy-balance-of-the-ground-in-university-valley-antarctica/432141245F43EF744DD8ABDB56580A5F)，只為此核出版日期／卷期metadata；原研究Methods的先前實讀範圍維持。
- [McKay2026原頁](https://www.cambridge.org/core/journals/antarctic-science/article/summer-snow-determines-the-depth-to-icecemented-ground-under-dry-permafrost-in-antarctica/5B2E97EBA4C91035CAFCECC234A532A0)，只為此核出版日期／卷期metadata。

公開查核搜尋詞：`site:pds.nasa.gov "PHOTOCLIN_CORRECTION_FLAG"`、`site:pds-geosciences.wustl.edu "PHOTOCLIN_CORRECTION_FLAG"`、`site:pds-geosciences.wustl.edu "PHOTOCLIN_CORRECTION" "photoclinometry"`、`"10.1017/S0954102022000025" "Published online"`、`site:cambridge.org "Climate and energy balance of the ground in University Valley" "Published online"`、`site:cambridge.org "Summer snow determines" "27 November 2025"`。前兩個關鍵查核已用官方文件本體定位核實。
