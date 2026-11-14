# MS-03 原始先例目錄續查：可讀範圍與驗證程序

日期：2026-11-15（Asia/Taipei）。查核基準：`234e58a8a0a0a9966e97e1b13d7ccc587cf3e8aa`。固定範圍為57.50–58.00°N、242.00–242.50°E，未移動場址。

本次未取得 Cohen-Zada 2024 原始資料/header、Levy 2009 全 S1 或 Dundas 2021 全 S4，三者格內成員狀態均維持 unknown。下述是原文實讀與可重現程序補充，不能標成新觀測、新原表取得或全球新穎性排除。既有 Daubar 2022 的0個格內事件點不替代這三份目錄，也不排除影像足跡相交、未收錄研究或地下冰。

## 已核對的來源身份

|來源|確實實讀|補強的定位與限制|
|---|---|---|
|[Levy等2009](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2008JE003273)，DOI10.1029/2008JE003273|出版商HTML §2¶5–8、§3¶9–11、Appendix A2¶57、Supporting Information清單|S1為按HiRISE影像編號列出的形貌組別資料；精確檔名為`jgre2606-sup-0002-ds01.txt`（刊載46.3KB）、`jgre2606-sup-0003-ds01.xls`（344.5KB）、`jgre2606-sup-0004-ds01.pdf`（397.2KB）；readme為`jgre2606-sup-0001-readme.txt`。未讀到任何S1資料列；清單大小不是本次下載驗證值。|
|[Dundas等2021](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2020JE006617)，DOI10.1029/2020JE006617|Data Availability Statement與Supporting Information清單|S4精確檔名`2020JE006617-sup-0005-Table SI-S04.csv`，刊載10.7KB。出版商明列同一補充資料USGS release DOI10.5066/P9Y8FR1R；不能當兩套獨立資料。未讀到S4資料列。|
|[Cohen-Zada等2024](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2024JE008387)，DOI10.1029/2024JE008387|§1.2、Data Availability Statement與引用資料DOI|研究用HiRISE影像，MBARS boulder maps/calibration等連至MartianBoulder Dataverse與DOI10.18738/T8/DUCOYB。DOI及論文能證明資料身份，不能證明原檔取得、完整54影像清單或本格足跡。|

Levy原文選樣為823幅HiRISE、PSP001330–006981，先順序選早期軌道，再依地理缺口補樣；不能將它視為每一個指定格都有觀測的隨機/完整普查。其形貌命名依可見地表，而地球冰楔/砂楔分類涉及地下結構；兩者不能只憑形似等同。原文另明列季節霜、雲與沙塵影響辨識。這些判準支持MS-03維持「先驗證可觀測性，後作形貌比較」，不供本格冰含量判定。

## 取得原表後應實際執行的程序

1. 儲存原始檔與readme、官方URL、下載UTC、HTTP狀態、bytes與SHA-256；驗證內容不是拒絕頁。以官方檔案checksum存在與否分開記錄，不能將自己hash寫成provider核對。
2. 依原始header/readme釐清planetocentric/geodetic、east/west、−180–180/0–360、事件點/影像中心/足跡與缺值定義；保留原值，衍生欄才轉換。沒有定義就標unknown，禁止把0當缺值或反向。
3. 對Levy S1每個唯一HiRISE產品ID取得同版官方label/footprint，做固定格的實際足跡相交；先保留多種形貌標籤與一圖多類關係。影像中心不在格內不能直接排除足跡。
4. 對Cohen-Zada逐一建立54幅影像和實際分析子區crosswalk；分開全影像足跡與boulder map有效邊界。只在可取得分析區時檢查同地同用途，不能把全幅內某角落的研究套給全幅。
5. 對Dundas S4先確認它的記錄對象和欄定義，再分開事件/暴露點membership與對應圖像footprint。不得將其他catalogue或重複release當獨立證據。
6. 對所有交集記錄逐篇核對問題、材料/深度、尺度、方法與結論，分類「直接同地同用途／部分重疊／不同用途／證據不足」。格外範例可作方法先例，不能證明本格已研究或未研究。
7. 即使三表均0交集，只能排除指定版本/選樣/邊界下的記錄。完整歷史新穎性與未出版研究仍unknown；不寫首次、從未研究、冰不存在或AD1配對成功。

## 實際存取限制

搜尋服務可讀出版商正文與附件清單，但點選Levy TXT/readme及Dundas S4的官方下載均回403。USGS DOI導向ScienceBase後不可讀；Data.gov只有metadata與landing-page連結，不是原CSV。Dataverse landing page不可讀。另試出版商supinfo路徑，搜尋服務回不可讀；不聲稱不存在。Playwright公開頁導覽長時間無回應後被中止；後續node請求亦無可用結果，因此沒有任何本輪原表bytes、hash或資料列可交付。沒有對外寄信。

逐次搜尋/來源定位在同目錄對應的`prior_search_log.csv`、`prior_source_read_log.csv`及`prior_protocol.csv`，供後續取得原件時接續。
