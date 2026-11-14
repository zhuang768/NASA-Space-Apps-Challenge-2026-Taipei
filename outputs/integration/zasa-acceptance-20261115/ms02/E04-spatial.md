# MS-02 空間定位查核筆記（非正式報告）

- 範圍：本輪只負責 E04 九個 LiDAR 參考點的原始 UTM 交叉驗證，以及 MS-02 固定框的區域地質定位；不重做既有雷達／岩芯研究，不更動候選或遠端 repository。
- 基底：已讀最新 main `1506ede572435588eb5e64f95f24639279b77e56`；PR #22、#25 均開啟且未合併；#27 為開啟的 draft。快照在 `sources/remote_state.json`。這不是合併或 CI 就緒判定。

## E04：數值定位缺口已閉合，實地真值未閉合

- 重新核對 [Andres2020 原學位論文的全文鏡像](https://www.academia.edu/180656780/A_Periglacial_Landsystem_Analysis_in_the_Canadian_High_Arctic_A_Tool_for_Planetary_Geomorphology)，§3.3.1／Table3.1：WGS84、UTM16N。表的 Lat UTM 是 northing、Long UTM 是 easting，不能當角度。九組重轉錄與 main 完全一致。官方舊儲存庫已移轉，CORE PDF 本輪403；未宣稱重取原PDF或完成表格影像核對。
- `haughton_table31.csv` 保留九點；使用獨立 pyproj3.8.0／PROJ9.8.1 轉換 EPSG32616→4326，與 main 純 Python 結果逐點比較。最大差 **0.000220052m**；回轉殘差 **1.87e-9m**。這驗證運算一致性，並不代表實地定位有亞毫米精度。
- 九個參考點範圍為 **75.35883963–75.39368038°N，89.51057634–89.65474895°W**；點位南北跨度 **3.888996km**、平均緯度東西跨度 **4.065827km**。這是參考點跨度，不是九塊 DEM 完整外框，也不是連續研究面積。
- 依原論文§3.4.1，五個河流沉積點、三個撞擊熔融岩點、一個 Eleanor River Formation 點分開保存，不能當成單一岩性控制場。
- [Thomson2012 §2.3](https://doi.org/10.1029/2012JE004053) 的具名點距最近表列點 **16N約171.696m**。這不證明同線／同多邊形，也不證明不重疊，因為 DEM 外框與雷達線方向尚缺。不用名義河谷點的約0.22km代替實際九點查核。
- 額外品質警示：Table3.1列16N=134.93m、16AD=197.52m，§3.4.1後段文字有互換寫法；本輪不選邊、不把這兩個高度當新實測或 DEM 高程真值。定位驗證不受這個標籤衝突影響。

## MS-02：區域單元可確認，地方材料仍未知

- main 已保存從 [USGS SIM3292](https://pubs.usgs.gov/publication/sim3292) 原始資料庫擷取的 polygon，原 ZIP 記錄大小808,910,442bytes、SHA256 `ef75f059b1f2f5a47aff55e6c6e39500cf1ab65e743fabc5d463b97bc10b6541`。本輪重算的是這個固定擷取檔；**未重下載或獨立重驗整個ZIP**。
- 來源限制：保存的總體metadata描述Robinson製圖投影，不能替代個別shapefile的.prj。本輪GeoJSON以其經緯度座標與GeoJSON約定重算，並與明列Mars2000地理座標104971的服務核對；未取得原shapefile.prj。直接USGS ZIP本輪HEAD403，未繞過。若要求全鏈獨立認證，應補原檔.prj和ZIP到GeoJSON的完整重建，不能說本輪已完成。
- Shapely2.2.0／GEOS3.14.1 驗證原 polygon 有效，且完整包含 **168.00–168.50°E、52.50–53.00°N** 固定框：**OBJECTID1252，mAl = Middle Amazonian lowland unit（中亞馬遜世低地單元）**。不是只看中心點或 bbox 相交。
- 本輪另外成功重取引用同一USGS來源的 ArcGIS REST geometry及metadata；回應SHA256與 main 記錄相同。此服務 item owner為 `dasbury_storymaps`，**未確認為USGS官方營運**，只列為衍生交叉來源，不當獨立地質證據。它同樣完整包含固定框；與原polygon Hausdorff差6.84e-10度，屬座標序列小數差。
- SIM3292是 **1:20,000,000** 區域地質分類，不供應 MS-02 的覆土厚度、礦物／鹽分、冰存在、埋深或含量，也不能拿它裁定 Arcadia 地名邊界。
- 原正式報告§9的「正式地質單元未知」與「UTM未用獨立函式庫交叉驗證」可在交接中標成**已被較新查核取代**；本輪沒有替使用者改寫正式報告。

## 整合時的狀態界線

- 四個ID仍為 E01保留、E03方法參照、E02/E04原候選待補。main地方查核AV-06／AV-07早已有Liu2018與Thomson2012具名子案例；PR#25把這個界線同步進主表。`candidate_state_audit.csv`逐欄記錄，不把PR#27既有文字重列成新觀測。
- E04未升級為熱學／全區含冰量驗證場。本輪確實完成的是投影運算與區域地質定位兩項；科學完成旗標仍應為false。

## 重跑

```sh
python -m pip install pyproj==3.8.0 shapely==2.2.0
python verify_spatial.py
```

- 不連網、不執行舊程式的I/O，僅從固定原始碼AST提取舊UTM函式比較。
- 結果：`haughton_coordinate_check.csv`、`candidate_state_audit.csv`、`spatial_audit.json`；所有限定範圍assertion通過。`retrieval_receipts.json`保存本輪實際下載URL／bytes／hash。
- 欄位包含更多小數只為重現運算；不能當測量精度。JSON的1.0覆蓋分率是角度平面內的幾何包含性檢查，不是冰覆蓋率或地球—火星相似度。
