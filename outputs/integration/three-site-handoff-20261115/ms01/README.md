# MS-01｜University Valley 作者活頁簿查核（條列證據）

固定火星範圍：56.50–57.00°N、72.50–73.00°E；以下是地球資料完整性查核，不是火星量測或正式報告。

- **已完成 X08：** 從 [Zenodo 作者固定 v1](https://zenodo.org/records/10553882) 實取 [UV 2009_2011 All Hobos.xlsx](https://zenodo.org/records/10553882/files/UV%202009_2011%20All%20Hobos.xlsx?download=1)，1,767,387 bytes，作者 MD5 `7ab4bf2692ef83c5a3d4a5347b8a71c8` 核符；SHA256 及三個同期來源匯出的獨立雜湊列於 provenance JSON。前版 [PR #20／缺件表](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/main/outputs/research/shared_validation/missing_artifacts.csv) 記錄的取得障礙，本次已排除。
- **來源與數字：** 只有一張工作表。分站按同標示印刷日期和數值，比較工作表 A:C/F:H/K:M 與作者相同資料集的 2009–2013 校準篩選 TXT；逐個對照兩溫度欄，區分數值、雙缺值和無對應日期，不跨站／儀器配時。所有工作表日期都能在各自 TXT 找到，交集溫度數值與缺值完全相符（0 項不符，涵蓋 91,618 個可用數值）。相符是**同資料重複核對**，不是獨立觀測。
- **有效配對與空缺：** S8 19,575／27,371（7,796 缺雙讀值）；M22 8,749／8,749（上層 **1 cm**，非地表）；D36 17,485／17,486。TXT 多出的可用配對僅 S/M/D 2／1／1 筆；大量額外名義時標不等於新有效觀測。來源精確起迄及欄名見 CSV。
- **不是獨立含水量控制：** D3／I3／N3 是以各站冰界面溫度代入指數式的飽和水氣莫耳濃度，不是獨立水氣感測或冰體積量測。AC／AD 只有 42 cm W42 引述摘要（列 1–6，來源標 Marinova et al. 2022），不是 W42 逐時時間序列。
- **沒解決的事：** 兩份地球整理檔的時標都標 GMT+13，TXT 小數日與印刷時間僅 ±2.88 秒；這是輸出內部算術一致，不驗證絕對時鐘或各 logger 同步。這本沒有可消解 S／D 原始 GPS/serial 衝突的新記錄，也沒有原 Campbell/U23 校時日誌、獨立 UV 材料 k／ρCp／含冰量，或同材料、同邊界無冰控制。維持 [Marinova 2022](https://doi.org/10.1017/S0954102022000025) 及 [McKay 2026](https://doi.org/10.1017/S0954102025100448) 的來源鏈差異，不能用工作簿取代原件。

## MS-01 研究取捨

- **University Valley：保留**為已知冰膠結地層的熱傳及訊號辨識限制案例。11 天站內有效資料與既有振幅結果可用，但不是盲測冰探測或新用途宣稱。[PR #8](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/8) 的舊工作不重算。
- **Beacon Valley：補充材料對照。** 同一個 Beacon 土樣，乾燥到約 10 wt% 加水條件的熱擴散率由 0.191 到 0.736 mm²/s（3.85 倍）；更濕樣本下降。這可支持「含水與材料會改變熱訊號」，不是冰量，也不等於同孔位／相同環境與 University Valley 的控制。[Levy & Schmidt 2016，補表 1](https://doi.org/10.1017/S0954102016000201)
- **火星端：** 既有 Piqueux 2 ppd 原生格約 0.427 m 是有條件熱模型，不是冰真值。熱模型輸入與 SWIM 含相依，不能把分數當機率。[PR #20](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/20)。
- **可用新增觀測 QA（本次前已執行）：** [CRISM TOD 原始產品目錄](https://pds-geosciences.wustl.edu/mro/mro-m-crism-3-rdr-targeted-v1/mrocr_2102/trdr/2008/2008_191/tod0000b701/) 的 WA/TRR3 438 個探測器列配對一致，DDR 502/768 像元中心在框內但最近距中心 7.87 km，未校正 apparent I/F 亦有異常值；不可據此判冰。[USGS Casius 100 m COG](https://registry.opendata.aws/nasa-usgs-themis-mosaics/) 的同格網日夜裁切皆 296×296 且無 NoData，但 DN 是定性亮度，並非溫度或熱慣量；同格網不證明實際地標配準。
- **主張護欄：** 不宣稱冰實際存在、深度、含量或其不存在；不宣稱獨立冰量驗證、UV／Beacon 對 Mars 的成功配對、文獻首次使用或沒有既有研究。披露既有 [Heldmann 等：高海拔乾谷作火星地下冰類比](https://doi.org/10.1016/j.pss.2013.05.019)；可表述團隊的具體增量為固定 MS-01 的來源相依、尺度和不可辨識性查核。

## 重現

`python3 verify_uv_workbook.py --inputs /tmp/ms01-zenodo --output /tmp/ms01-results`（Python 3＋openpyxl）。
從固定 Zenodo v1 下載並校驗四個原件，只讀取；不重存試算表、不配時、不改 GitHub。


## 站位 X04：新增深度調查佐證，尚不能改標

- **另取實體深度資料：** [Marinova 等 2013](https://doi.org/10.1017/S095410201200123X) 的 [出版社 ZIP](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S095410201200123X/resource/name/S095410201200123X.zip)，5,595 bytes，SHA256 `773e68eb9fc63c4c1e7c771a057d2507ad0f2a237f4b1cb8f3b544bc32537517`，ZIP CRC 通過。本輪讀 003 University Valley 原始表及 005 說明；68 個調查位置，含 6 列「未抵達冰」的深度下限，**不是無冰位置**。原始地點平均由該列實測深度不加權重算並核符。另有 [USAP-DC 館藏](https://www.usap-dc.org/view/dataset/609529)；該處列出的檔案 MD5 與出版社 ZIP 內檔案不同，未取得該館檔案，不聲稱位元等同。
- **位置 A**（−77.8597333°, 160.7169833°；2009 部署 D36、2022/2026 論文 S8）：與出版社表第 22 行數值在六位小數四捨五入一致，三個 pit 40、44、44 cm，作者平均 **42.7 cm**（SD 2.3）；這比較符合偏深環境，而非名義 8 cm。近鄰不是一樣深：例如約 60.5 m 的另一測點平均 22.8 cm。
- **位置 B**（−77.8657667°, 160.7286667°；2009 部署 S8、2022/2026 論文 D36）：沒有同座標深度表記錄；最近約 **70.2 m**、平均 **10.8 cm**（第 7 行三個 pit 8.5／15／9 cm），距 ≤102 m 的 4 個位置平均介於 8.3–11.3 cm。這比較符合偏淺環境。
- **位置 M**（兩版一致）：與第 14 行座標在六位小數一致，作者 5 個量測均值 **24.2 cm**，和 M22 名義位置的環境相符，但不將調查平均換成探針深度。W 在這個調查表沒有同座標深度；最近約 49.5 m、平均 27.7 cm，不可換成 W42 的井深。
- **判定：偏向 2009 部署版，不等於已證實。** 這是另外的實地深度觀測，不是獨立團隊的 GPS 核驗；文章作者有重疊，調查表沒列 logger 序號或站名。地表條件可在短距離內變動，近鄰不可取代同井。四捨五入匹配是座標數字一致，不代表釐米 GPS 精度；來源 datum／定位誤差未證實。保留 S/D 雙版本、按實際檔與序號分析，直到取得原始 GPS、部署示意、帶序號定位或作者勘誤，不按單一版本做地形或陽照歸因。
- **重現：** `python3 verify_uv_survey.py --archive /tmp/ms01-marinova2013.zip --output /tmp/ms01-results`。用半徑 6,371,008.8 m 球面距離，每錨點列 5 個最近測點，見 `university_valley_coordinate_crosscheck.csv`；ZIP/表雜湊、行數和限制見 `university_valley_coordinate_provenance.json`。
