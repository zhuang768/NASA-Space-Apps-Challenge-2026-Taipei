# MS-02 CRISM 逐波段／逐像元品質補查

這份資料筆記供人類撰寫報告使用；沒有改寫正式報告。固定基準為 `521740108050ba16e406f8becb67a786179ff8bd`，固定範圍仍是52.50–53.00°N、168.00–168.50°E。

已對既有 `crism_roi.npz` 的全部55×912值重算數值支援、缺值與負值；Git blob SHA-1核對為 `c4cf29f4a9c86bbd48a268eaf47920d417b0b6fd`。不是重新從全球產品定位抽取，也沒有外推未覆蓋區域。

| 檢查 | 實際結果 | 解讀 |
|---|---|---|
| 全部值 | 50,160；數值可用48,060，即95.813397% | 只是既有numeric mask規則；不是光譜科學有效率 |
| band0（0起算） | 全部912值為65535 | 全波段缺測；無法由此表判明原因，不能稱為真實零反射 |
| 完整55波段光譜 | 0／912像元 | 不能將整體95.8%寫成95.8%光譜已完整可判讀 |
| 除band0後54波段 | 890像元有全部54個數值；22像元全部缺測 | 未填補、未內插；890也不是礦物檢出數 |
| 負I/F | 43值，全部在band9；占890個有數值像元4.83146% | 保留原值與旗標，沒有截成零；未認定為吸收帶、冰或特定校正錯誤 |
| 支援範圍 | 52.9249916–52.9999886°N；168.2478638–168.4997711°E | 只是912個像元中心的邊界，位於固定格北側子區；不是本格完整面積覆蓋率 |

`band_quality.csv`提供55波段的數值個數、65535數、負值與分位數；`pixel_quality.csv`提供912像元的原座標、可用波段數與旗標。波長、detector row、材料類別沒有證據可填，維持空值／unclassified。

原始PDS標籤明列本景為 `MSP0001565D_01_IF213L_TRR3`，2010-01-08T23:15:04.702至23:16:04.631；`MRO:ATMO_CORRECTION_FLAG`、`MRO:THERMAL_CORRECTION_MODE`、`MRO:PHOTOCLIN_CORRECTION_FLAG`均OFF，空間與光譜重採樣也OFF。HDF軟體與濾波參數為N/A，不能用版本3概括宣稱本景已完成所有雜訊濾除。這些是標籤狀態，不是本輪已執行校正的結果。

官方[CRISM SIS v1.3.7.7](https://pds-geosciences.wustl.edu/mro/mro-m-crism-2-edr-v1/mrocr_0001/document/crism_dpsis.htm) §3.4與label keyword table說明：TRDR的波長需對應WA校正圖與所選detector row；資料有跨軌光譜smile。不能依band序號等間隔指定波長。[PDS TRDR primer](https://ode.rsl.wustl.edu/mars/pagehelp/Content/Missions_Instruments/Mars%20Reconnaissance%20Orbiter/CRISM/CRISM%20Product%20Primer/CRISM%20TRDR.htm)所稱radiometrically calibrated I/F，不能直接替代地表大氣與光度校正。

精確缺件已從標籤定位：`CDR450924300802_WA0300010L_3.IMG`及其label；原IF影像record49501起的55個大端16-bit detector row（110bytes）；ROI回到原影像sample／line的對應；科學品質mask與可驗證的smile、大氣／熱／光度處理。既有npz只有I/F、lat、lon、numeric_valid，未保留sample／line／row table，不能單靠它完成逐像元波長配對。

本輪有實際嘗試取得精確WA、IF與DDR：`acquire.py`使用8秒連線／12秒wall-clock上限及大小界線，四個請求均因執行環境DNS `Errno8`未取得，原錯誤見`retrievals.json`。官方SIS可透過網頁檢索讀取，WA／WV／SW直接web open則無法存取；不能把工具無法取回當成PDS沒有資料。其他MS-03研究的WA檔案時間與ID不同，本輪只參考下載方法，沒有借用數值。

新增9項驗證只證明此數值品質盤點與固定輸入一致。光譜材料辨識缺口仍未關閉；沒有材料／礦物／地表冰的科學分類，且表面光譜本身不能直接驗證約0.45m地下模型冰界面。

重現：先執行`spectral/analyze.py`，再執行`spectral/verify.py`。取得精確原始檔與校正後，應保留原mask與sample／line／detector-row對應，再做有依據的波長、品質與校正處理；不能把這次QA通過改寫為已證實本格有冰。
