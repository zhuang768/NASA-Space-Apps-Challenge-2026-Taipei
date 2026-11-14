# MS-03：地球方法參照、局部資料查核與可驗證問題

Team zasa｜更新：2026-11-15（Asia/Taipei）｜本次來源基準：`234e58a8a0a0a9966e97e1b13d7ccc587cf3e8aa`

MS-03目前支持的研究成果是：**把固定火星格的熱性質、冰一致性、影像與雷達證據分開，檢查哪些資料能回答「覆土／表面邊界是否混淆冰判讀」，哪些資料仍不足以辨識地貌或地下界面。** University Valley W 保留為已知歷史界面與資料品質參照；Adventdalen AD1保留為已發表幾何／取樣方法參照。這不是兩個已成立的環境配對，也沒有證實MS-03的冰存在、實際深度、含量或基地可行性。

本報告整合已取得的局部科學包與本輪地球／雷達診斷。舊交接與原始判斷原樣保存在[歷史報告](report_history_before_completion_20261115.md)；歷史中的「只有目錄／尚未取得原像」等取得狀態不再代表現況。兩候選ID、火星範圍及原始觀測值保持不變。

共同交接提交為`f7076c9fdc77e00244ed5d6863aad2bf78cfa28f`，初始研究基準為`3cc8488577535e2fa4d146021fde51f8ff6cc667`；本輪固定查核最新已合併資料的`234e58a8a0a0a9966e97e1b13d7ccc587cf3e8aa`。各版本角色分開保留，不覆寫其他人的工作。

## 1. 固定位置與可比較的火星背景

MS-03中心為 **57.75°N、242.25°E**（−117.75°E）；範圍為57.50–58.00°N、242.00–242.50°E（−118.00至−117.50°E），以planetocentric／east-positive表達。這是名義0.5°篩選格，不是著陸橢圓、鑽孔或已調查的工程場址。[mars_reference.json](../../../outputs/research/MS-03/mars_reference.json)保留固定來源；逐數值定位在[evidence.csv](../../../outputs/research/MS-03/evidence.csv) EV01–07。

|面向／產品|固定格或所選背景值|支撐與解釋界線|
|---|---|---|
|地形：MGS MOLA|均坡0.162753°；relief 76m|坡度約3.7km基線、16 pixels/degree；64/64格心為有限值。區域平緩不證明局部無石塊、無陡坎或著陸安全。|
|熱性質：MGS TES|平均152.8077，範圍111–270 J m⁻² K⁻¹ s⁻¹ᐟ²；79/100有效格|20 pixels/degree，21個mask0格排除。熱慣量不是溫度、硬度或冰深；範圍是空間差異，不是誤差棒。|
|水冰：SWIM2|0–1m一致性平均0.910904；1–5m為0.509972|各100個原生格心。是多產品一致性指標，不能寫成91%含冰率、機率或兩深度間的實際垂向冰剖面。|
|大氣沙塵：重建CDOD|MY34平均0.098215、p95 0.173362；MY35平均0.088660、p95 0.140962|3°重建格，所選座標58.5°N、117°W；9.3µm吸收、全柱量，各669個重建sol。不是現地風、壓力、沉積或地球可見光AOD。|
|溫度情境：MRO MCS|最近格60°N、120°W；配對日夜差中位67.0547K|5°格、MY29–36、10°Ls分箱；171個day／148個night／60個配對，可能288個。是模型調整的季節背景，非候選現地溫度、同sol振幅或可直接與地球氣溫相減的量。|

這組背景使「低TI＋較強淺層SWIM一致性」值得追查，但材料、覆土、表面邊界及產品支撐不同，仍可產生歧義。不能僅靠這些摘要選定唯一冰模型。

## 2. 兩個地球候選與四面向

### MS-03-E01：University Valley weather station W

錨點 **−77.86215°、160.71010°E**，來自Marinova等2022的站點文字座標換算。研究範圍是該歷史氣象站及各自註明的感測剖面；原站點文字未交代座標datum／誤差，沒有增設半徑，也不把同谷其他鑽孔當成W。[candidates.csv](../../../outputs/research/MS-03/candidates.csv) E01；[2022原文](https://doi.org/10.1017/S0954102022000025) Meteorological measurements／Table II。

|面向|已取得的證據|能回答與仍缺什麼|
|---|---|---|
|地形|歷史站在岩質谷底；站點錨點和部署說明可追溯|可界定資料來自哪個點；沒有共同尺度DEM坡度／障礙調查，不能與MOLA數值作匹配分數。EV08。|
|溫度／熱性質|作者校準匯出Campbell 55,346列、HOBO 27,553列；歷史探頭深度0、10、20、42、49cm，不代表每種變數都在每個深度；Campbell 30分鐘、Onset 60分鐘|可檢查同檔缺值及有限窗口描述；不是未處理logger或獨立校準，沒有可與TES等同的地球TI。2010 HOBO同列20／42cm有效8,759對，差值平均−0.244125°C只屬作者合併檔描述，不證明不同logger真實同步或傳熱因果。EV10、13、19–23。|
|水／冰|部署記錄把42cm視為歷史界面；已有雪／鹽及表面水汽控制研究|可規劃「界面、覆土與表面邊界分開量測」的實驗；不是現在的獨立冰真值，也不能把42cm移植到MS-03。EV09、12、24。|
|大氣／沙塵|本輪重核同一短版Campbell檔，取印出時間2010-01-01至2010-12-01（不含），16,032列、11個完整月；氣溫平均−25.4289°C、風速2.76548m/s，五個大氣／輻射欄均有有限值|測高分別為氣溫／RH 1.2m、風1.08m、日照1.27m；各單位、基準與逐月值見新表。沒有12月，不能稱全年；未轉UTC、不與長版拼接；風速不是沙塵代理。82.8kPa在原論文是模型假設，非實測。|

原始W公開版本為Zenodo [10.5281/zenodo.10553882](https://doi.org/10.5281/zenodo.10553882)。本輪短檔MD5與provider一致；雜湊、原URL、欄位及方法在[earth_input_receipt.json](../../../outputs/research/MS-03/completion_20261115/earth_input_receipt.json)、[大氣期間摘要](../../../outputs/research/MS-03/completion_20261115/earth_atmosphere_summary.csv)、[逐月統計](../../../outputs/research/MS-03/completion_20261115/earth_atmosphere_monthly.csv)。有限值不等於沒有儀器或作者處理誤差。

**處置：保留為歷史界面／邊界條件與資料品質參照。** 長版Campbell在2012-10-28邊界有−1h至−5h的日期欄差變化，伴隨8個全通道NaN列；作者QA記述補入8點／4小時，但原始logger、校準碼及操作紀錄未取得，不能據此直接平移4小時。短版的同檔統計不解除長版限制；Campbell與HOBO仍不配時、不估跨儀器lag／diffusivity。[clock audit](../../../outputs/research/MS-03/uv_w/campbell_clock_audit.json)；[地球補充](completion_20261115/earth_evidence.md)。

### MS-03-E02：Adventdalen AD1／Act-IWS

metadata事件起點 **78.184°N、15.913°E**，事件外框78.184–78.188°N、15.913–15.933°E。這不是溫度感測器位置或幾何中心。真正測繪範圍來自PANGAEA既有185個多邊形，WGS84／UTM33N bbox為[520884.4169, 8679090.0993, 521340.9904, 8679522.0092]m；metadata外框不是連續地下冰範圍。[原資料10.1594/PANGAEA.921087](https://doi.org/10.1594/PANGAEA.921087)；candidates E02。

|面向|已取得的證據|能回答與仍缺什麼|
|---|---|---|
|地形|185個既有有效向量重算；等效圓直徑中位18.484785m、無因次circularity（4πA/P²）中位0.806600；原刊13個四捨五入統計與重算一致|可檢查既有幾何方法、尺度與取樣；不是新測繪或獨立真值。原刊報導20cm orthoimage取樣，原像精度未重新驗證。EV14、25、29。|
|溫度／熱性質|Adventdalen 2005–2017監測研究有三trough、雪與熱條件，active layer約0.8–1.0m；表面溫度測法為0.02m深、通常每小時|尚無可將TR1–TR3／GPR感測線逐點註冊到AD1 GIS的證據，只列區域情境；AD1現地溫度及TI未知，不複製機場或他站數值。EV16、18。|
|水／冰|原資料是active ice-wedge site的多邊形網路|既有場址解釋支持過程參照，卻不提供每個polygon下的深度、純度或連續冰量；不能從裂縫形貌單獨推冰。EV15。|
|大氣／沙塵|監測文獻記錄風再分配雪與雪絕熱；相機無完整極夜雪記錄|可設計雪／水分混淆控制；該濕凍土情境不是Mars CO₂稀薄大氣或乾UV的等效條件，無AD1現地dust column／沉積量。EV17。|

**處置：一般方法參照，退出目前具體MS-03形貌配對。** 在6.09m/pixel的所用CTX例中，18.484785m僅約3.04pixels，這只是取樣比值，不是校準檢出門檻。新增MOC原像提高可用資料量，但目前仍無可重現的格內閉合多邊形樣本；不能作兩地分布比較、推相同成因或填入0值。[幾何摘要](../../../outputs/research/MS-03/morphology/AD1_geometry_summary.json)；[尺度比較](../../../outputs/research/MS-03/morphology/observability_comparison.csv)；[四面向來源表](../../../outputs/research/MS-03/completion_20261115/earth_four_dimensions.csv)。

## 3. 同地同用途先例與本隊差異

|候選／來源|分類與實際讀取範圍|與本次用途的關係|
|---|---|---|
|W：Marinova等2022，10.1017/S0954102022000025；online 2022-04-20|直接先例；Methods、Table II、thermal diffusivity及Appendix相關部分|已用同W站多深度觀測與熱模型研究地下熱性質歧義；不能稱首次使用此站或新機制。PW01。|
|W：McKay等2026，10.1017/S0954102025100448；online 2025-11-27|本輪補入的直接先例；Environmental data、Discussion／Extrapolating及出版metadata；並非全文重審|同W座標、同資料來源，直接研究夏雪、表面水汽邊界與冰桌穩定。其一年代表長期、RH辨雪與簡化衰減等假設必須保留。本次並未獨立重做物理驗證。CEW3。|
|W：雪／鹽穩定研究，10.1017/S0954102017000402|部分重疊；本次僅讀作者機構abstract|支持需分開控制雪補給及鹽作用；不聲稱掌握全文所有實驗細節。PW02。|
|AD1：Ulrich等2011，10.1016/j.geomorph.2011.07.002及PANGAEA|直接先例；原刊pp199–201、203–204，Tables2–4；185向量與13項刊載精度重現|已做AD1–Mars定量地貌類比。本文具名Mars影像在本MS-03格外，只排除這些影像，不是全球先例排除。PW04／08。|
|Adventdalen：Matsuoka等2018，10.1002/ppp.1985；2025 WISDOM會議摘要|部分重疊；前者§2、§3.1–3.2、§4.1，後者作者摘要|熱／雪／開裂與雷達歧義的方法已有先例；精確AD1同址關係未證實，不能把同谷等同同儀器剖面。PW05／06。|

完整分類、搜尋平台／詞／日期、頁段與未知保留在[prior_work.csv](../../../outputs/research/MS-03/prior_work.csv)、[search_log.csv](../../../outputs/research/MS-03/search_log.csv)及[本輪地球實讀紀錄](../../../outputs/research/MS-03/completion_20261115/earth_source_read_log.csv)。

本隊可主張的差異是：**對固定MS-03格做來源追溯、真實資料取得、座標／產品QA、既有地球資料重算及可觀測性診斷。** 不是新場址發現、新冰機制或已成立的新類比。限定搜尋與幾份目錄不能證明全球從未研究。

## 4. 火星局部資料：實際新增了什麼

|資料／定位|已完成的查核|不能由此推出|
|---|---|---|
|[熱模型原生格](../../../outputs/research/MS-03/local_validation/piqueux_native_cell.csv)，DOI10.22002/D1.1316|原生0-based row64／col484、中心57.75N/242.25E；條件模型深度0.103161566m，上層TI215.4277344 J m⁻² K⁻¹ s⁻¹ᐟ²|不是實測冰深或獨立冰確認；與TES產品定義/支撐不同，不能把兩TI差值解為材料變化。封存格2ppd與論文3ppd生成鏈仍有限制。|
|[USGS地質交集](../../../outputs/research/MS-03/local_validation/analysis_summary.json)|原始AHv多邊形包含固定格；原始shape／坐標定義與交集保留|全球地質單元不是本地材料、冰量或鑽孔真值。|
|[MOC原像／QA](../../../outputs/research/MS-03/local_validation/gap_completion/moc_summary.json)|S1700607_NA，2006-04-08；完整PDS checksum／projection核對；9,272,742個非零格內中心，實際開啟3個固定512×512窗|3.00034m是投影網格，非有效解析力；3窗不等於全格地貌普查。尚無可靠閉合邊界，亦不能說多邊形不存在。|
|[原始CRISM mapping](../../../outputs/research/MS-03/local_validation/crism/qa.json)|2014-02-10 HSP0002DE65與2010-05-25 MSP00018FDA；DDR／WA原件匹配；取樣1300–2200nm通道的數值/校準合格中心分別966/1,350、8,516/9,056|不是全格面積覆蓋或最終科學QA。原label的`MRO:ATMO_CORRECTION_FLAG=OFF`、`MRO:THERMAL_CORRECTION_MODE=OFF`；前者由SIS定義涵蓋photometric與atmospheric correction。`MRO:PHOTOCLIN_CORRECTION_FLAG=OFF`是photoclinometry坡度來源選擇，僅physical thermal分支有效，非獨立photometric旗標。雲／霜／儀器殘差未解；原始光譜凹陷不命名為冰。|
|[MRDR v4／原始byte範圍](../../../outputs/research/MS-03/local_validation/official_resources/README.md)|T1811 AL/SU/DE/WV，6 albedo bands、3參數、6溯源欄；原生projection半徑3,381,164.4m、網格180.4662m；13,284映射格心，嚴格來源中心在格內13,169，排除115個邊界remap|5條來源觀測跨2006–2014，非單一新觀測或原始光譜的獨立確認；負BD1500_2不證明無冰。數值格心不等於獨立樣本或光學footprint完整位於格內。|
|[CAT／MRDR殘差](../../../outputs/research/MS-03/local_validation/bd1500_audit/results.json)、[歷史流程](../../../outputs/research/MS-03/local_validation/production_history/README.md)、[執行缺件](../../../outputs/research/MS-03/local_validation/t1811_run_artifacts/README.md)|嚴格13,169中心，公式值減官方值中位+0.000711422、maxabs0.019347335，均無因次；受檢float32/64差約1.35×10⁻⁷。歷史SIS已記錄parameter計算後再做summary優化；產品label記producer1.03.94|浮點差單獨不足以解釋所見殘差；AL公式不必保持SU關係。但沒有該run設定／係數／成對中間陣列，不能逐像素歸因、判官方錯誤或調值強迫吻合。較窄GAP運算式的1.26×10⁻⁷與此不是同一實驗。|
|[同軌SHARAD／雜波](../../../outputs/research/MS-03/local_validation/gap_completion/radar_summary.json)|S_04624502_RGRAM，2016-06-07；65個格內GEOM中心、269個原始range rows及同觀測combined simulation。另3條實際GEOM的格內中心數為0、64、65；目錄footprint與中心線分開|模型非獨立觀測；不能相減power。0.0375µs採樣間隔不是range resolution；10MHz以c/(2B)換算的理論真空界面分離尺度為14.9896m，非本格實測解析力或檢出機率，不能作0.10m條件界面的獨立深度驗證。未有可信地下reflector／介電反演／含量。|
|[本輪雷達峰值診斷](../../../outputs/research/MS-03/completion_20261115/radar_diagnostics/radar_diagnostic_summary.json)|65個crop全域最大值相對模型nadir為−67至185samples，43個在前、22個在後；64對相鄰column中13對跳動>10samples、10對>100，最大絕對跳207samples|這些是描述門檻，非檢出判準；crop argmax不是已驗證表面／地下界面。變化原因不能唯一歸為地質、電離層、旁瓣、clutter或處理。未作校時、功率相減或delay轉本地冰深。|
|[目錄原表狀態](../../../outputs/research/MS-03/local_validation/original_tables_followup/table_acquisition.csv)、[Daubar核對](../../../outputs/research/MS-03/local_validation/gap_completion/daubar2022_summary.json)|Daubar2022作者XLSX 1,203個事件，固定格內0個事件點；原標頭E/N括號差異有獨立產品方向檢查，未改原檔|只排除該目錄點，非影像足跡零相交、無冰或無研究。Cohen-Zada原data／headers、Levy全S1、Dundas全S4未取得時，成員維持unknown，不能填0或互相替代。|

上述CRISM欄位語義依[官方DPSIS v1.3.7.7 §3.4.2的TRDR keyword定義](https://pds-geosciences.wustl.edu/mro/mro-m-crism-3-rdr-targeted-v1/mrocr_2101/document/crism_dpsis.htm)；label保留的PHOTOCLIN字樣不能改稱photometric，也不能在THERMAL=OFF時把它解為已選用某種熱模型坡度。

圖像可直接查閱[MOC固定視窗](../../../outputs/research/MS-03/local_validation/gap_completion/F-GAP01_MOC_in_cell_review.png)、[光譜QA](../../../outputs/research/MS-03/local_validation/gap_completion/F-GAP02_spectral_implementation_QA.png)、[同軌雷達／雜波](../../../outputs/research/MS-03/local_validation/gap_completion/F-GAP03_same_track_radar_clutter.png)及[峰值索引診斷](../../../outputs/research/MS-03/completion_20261115/radar_diagnostics/F-RAD01_peak_index_diagnostic.png)。顯示拉伸不改原始陣列，也不提供新物理真值。

HiRISE固定索引的205,451物理列／205,302唯一產品與149個額外重複列已對應。舊615筆「位置未知」其實是負經度格式旗標，均可由有效緯度排除；固定表內bbox交集為0。149現行label診斷有78組整秒floor/ceil相容、71不相容，其中29組差>1s，只排除「全部差異唯一來自同時刻取整」；實際生成版／SQL／根因未明。這項資料追溯已與地貌證據分開，不再把已解的615旗標當研究阻塞。[resolution_summary](../../../outputs/research/MS-03/morphology/evidence_followup/index_anomalies/resolution_summary.json)；[149組摘要](../../../outputs/research/MS-03/morphology/evidence_followup/generator_followup/duplicate_label_time_summary.json)。

本輪另補[三原表的精確附件與實讀範圍](completion_20261115/prior_followup.md)、[14筆搜尋紀錄](../../../outputs/research/MS-03/completion_20261115/prior_search_log.csv)與[7步空間／用途查核程序](../../../outputs/research/MS-03/completion_20261115/prior_protocol.csv)。原表仍未取得，精確檔名及可讀文章不是原始成員表，不能填0；研究選樣與影像中心／足跡也分開處理。

## 5. 剩餘問題與可執行的驗證程序

|問題|下一個具體程序|判定門檻與失敗時輸出|
|---|---|---|
|能否做AD1–MS-03形貌比較？|固定格內原像以事先指定的空間網格抽樣；逐窗記曝光／壓縮／照度及配準誤差；兩位獨立判讀者描邊並算重複性；用AD1原像按Mars sampling與噪音降級做辨識試驗|先證明邊界在同一尺度可重現，才比較分布；否則輸出不可辨識／檢出限制，不填0、不搬格外影像。|
|光譜能否提供冰證據？|取得producer1.03.94設定、優化係數與同源stage前後陣列，逐stage重演殘差；另用同模式／季節／幾何控制、雲霜及儀器mask、已知端元與噪音注入測靈敏度|未取得run材料就保留數值歸因unknown；沒有獨立QA／檢出與誤報率，不能定冰threshold或把負值當無冰。|
|雷達是否有可信地下界面？|先核有效帶寬、原始delay／surface追蹤及同軌clutter；在獨立pass重現候選反射，逐一評估旁瓣／地形／電離層／處理假說；只有可信delay才按明列介電模型傳播深度誤差|crop argmax與模型不合不構成界面；沒有可靠pick維持unknown。模型強度不相減，也不以SHARAD解像力驗證10cm界面。|
|先例目錄是否在本格？|取得三份指定原表與header；保留原ID／缺值／座標慣例，分開事件點與影像中心；以官方footprint另算影像交集|失敗HTTP／metadata不是原表；未取得維持unknown。即使0命中也只排除該表，不放行全球新穎性。|
|W能否跨logger作熱反演？|取得原始W logger、校準.m／.xls／.CR1、2012操作時鐘紀錄，重現每步作者處理；以獨立時基證明修正，再分別核HOBO|沒有獨立時鐘證據不移4h、不跨儀器join；先保留有限同檔描述。即使時標成立，仍需k、密度、熱容、界面與表面條件才能做限定反演。|

地球的重力、大氣密度／成分、對流、雪／水汽供給及鹽作用與火星不同。本研究可設計要量哪些控制量，不能把地球冰深、融化／昇華率、機械承載或設備性能直接移植到MS-03。

## 6. 資料、重現與完成界線

[本輪重現入口](../../../outputs/research/MS-03/completion_20261115/README.md)包含[完整檔案清單](../../../outputs/research/MS-03/completion_20261115/file_inventory.csv)、[驗收表](../../../outputs/research/MS-03/completion_20261115/requirement_audit.csv)、[全部搜尋紀錄入口](../../../outputs/research/MS-03/completion_20261115/search_log_index.csv)及[發布收據](../../../outputs/research/MS-03/completion_20261115/publication_receipt.json)。檔案存在、實際取得、雜湊重算與繼承來源分開標記。W短版作者匯出的無損gzip原件隨本輪附上，兩支氣象程式可離線重現5列期間摘要與55列月表。

六項核心交付為本報告及[candidates](../../../outputs/research/MS-03/candidates.csv)、[evidence](../../../outputs/research/MS-03/evidence.csv)、[prior_work](../../../outputs/research/MS-03/prior_work.csv)、[search_log](../../../outputs/research/MS-03/search_log.csv)、[manifest](../../../outputs/research/MS-03/manifest.json)。新增分析保留在MS-03專用目錄；來源URL／DOI、讀取頁段、儀器／欄位、期間、單位、支撐、缺值與hash以相應CSV／子manifest為準。歷史Excel與舊I-01/I-02配對只作背景，未套到本格。

原始大檔有的只保留精確byte excerpts與公開重取方式；未取得的原表／logger維持缺件，不能稱「所有全球原始資料已上傳」。子套件的validation驗證來源與重現範圍，並不驗證地下冰或類比性能。

**既定研究交付**可以按「兩候選、四面向、先例、處置、可追溯資料及未知」逐項驗收，原任務也明文允許證據不足如實交付。**所有科學問題均已解決**則尚不成立：本地冰真值、可量測多邊形、光譜執行歸因、跨logger同步與缺失原表成員仍不能由目前觀測證實。文件完備、推送成功或檢查通過不會把這些未知變成已知。
