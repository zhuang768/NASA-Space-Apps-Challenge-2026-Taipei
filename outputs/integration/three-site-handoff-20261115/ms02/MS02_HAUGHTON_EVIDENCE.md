# MS-02 E04 Haughton 補證據 / 供撰寫者查核

- 固定火星範圍：52.50–53.00°N、168.00–168.50°E，中心 52.75°N、168.25°E。未改候選範圍或研究全部成功配對的標準。
- [Main 的 MS-02 資料](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/tree/fee734610c6bacc57880eaaba1a1301f09fdd4d6/outputs/research/MS-02) 有獨立資料夾；[PR #22](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/pull/22) 的 4145ec5c586511df4813590cf1a7197fa26ff8c0 是額外的官方資料跟進，查核時開啟、未合併。沒有修改遠端。
- 本頁補的是該資料表 E04「沒有 Haughton 冰量、無地溫監測」的現有查核缺口。不能把以下子場址混成一個穿透完整地層的試驗。

| 證據 | 位置與尺度 | 實際量測、可保留的用途 | 限制 |
|---|---|---|---|
| [Thomson et al. (2012), §§2.3, 3.1–3.3, 4.1, 5.2](https://doi.org/10.1029/2012JE004053) | Haughton 撞擊熔融岩平台，75.36833333°N、89.52583333°W；3 m 雷達線，中點約 1 m 岩芯 | 450 MHz 地面雷達、同線取冰芯、5 cm 切段熔融並稱重。完整活動層上的初步雷達觀測受訊號損失限制，研究團隊懷疑濕覆土是原因；清挖至冰面之後才測冰的介電性。可當「已知有冰，但覆土會妨礙探測」的方法案例。 | 3.65–3.90 是論文對所測冰楔的彙整範圍，不是整條 Haughton Valley，更不是火星介電常數。挖開之後的成績不能證明穿透完整覆土。本文沒有取得逐層原始 radargram 和岩芯原表。表 1 是理論混合模型及參考冰量，不可當成實測 Haughton 全域冰含量。 |
| [Zacny et al. (2012), p. 290, Fig. 3/8；作者機構發布全文](https://publications.ri.cmu.edu/storage/publications/pub_files/2012/4/97-earth_space2012.pdf) | Drill Hill Station 1，75.42086111°N、89.76025°W，165 m；距上列冰楔約 8.79 km | 深鑽在 0.65 m 遇冰；同點另有三種貫入儀分析與 10 cm 地溫 14°C 的單次記錄。支持以侵入式真值校驗局部探測，而非直接外推。 | 貫入反應亦受土壤強度和含水、位置與操作施力影響；不是地溫時序、非 Thomson 雷達測線，非整個谷地。 |
| [Knightly et al. (2019), Field Results/Figs. 1–2](https://www.hou.usra.edu/meetings/lpsc2019/pdf/2181.pdf)；[2018 companion abstract](https://www.hou.usra.edu/meetings/amazonian2018/pdf/4020.pdf) | 撞擊坑西北邊緣下方的濕多邊形地；2017 夏季連續 27 天，土壤約 1 分鐘、氣象約 5 分鐘 | 起始活動層界面約 0.45 m 深，觀測期該深度平均 2.01°C、含水率 37.42%。區內樣品摘要平均導熱率 0.6711 W m⁻¹ K⁻¹、體積熱容 1.6200×10⁶ J m⁻³ K⁻¹。可當濕季節融化的反例，不能當作冷乾火星環境。 | 會議摘要及圖，並未取得完整時鐘校正、原始時間序列或精確站點座標。四個額外樣區的材料平均值不能視為同址探針物性；起始界面也不等於 27 天不變的冰深。 |
| [Andres (2020), Ch. 3](https://ir.lib.uwo.ca/etd/7528/)，[原作者 LPSC 摘要](https://www.hou.usra.edu/meetings/lpsc2019/pdf/2103.pdf) | 既有 MS-02 E04 河谷 LiDAR 範圍；repo 表列位置 75.37°N、89.53°W | 局地多邊形／條紋形貌的比較用材料，不能代替別處雷達或地下真值。 | 名義 E04 點到 Thomson 點約 0.22 km 並不代表某一具名 LiDAR 測塊、量測時間、個別多邊形或岩性同址。 |

## 重算與判定

- `python ms02_haughton_audit.py > ms02_haughton_calculations.csv`；僅標準函式庫。地球站位距離用球面大圓距離 R=6,371.0088 km；距離是資料點座標比較，不是地貌邊界。
- [SHARAD 原始儀器論文 §2](https://doi.org/10.1029/2006JE002745) 與 [NASA PDS](https://pds.nasa.gov/ds-view/pds/viewContext.jsp?identifier=urn%3Anasa%3Apds%3Acontext%3Ainstrument%3Asharad.mro)：20 MHz 中心、10 MHz 頻寬，自由空間約 15 m 名目垂直分辨。示例假設介電常數 3.65–3.90（不是火星實測），名目分辨 7.59–7.85 m，0.44998 m 介面雙程時間約 5.74–5.93 ns。公式 Δz=c/(2B√εr)，Δt=2d√εr/c。0.45 m 是熱模型條件值，不是雷達測得；名目分辨與 PR #22 的 37.5 ns 數位取樣步長須分開。這只能限制表面回波與淺界面的直接分辨性，不能宣稱雷達完全不受淺層影響。
- 以摘要的區內平均 k、體積熱容 Cv 換算，濕 Haughton 的 k/Cv≈0.4143 mm²/s、√(kCv)≈1043 J m⁻² K⁻¹ s⁻½，Knightly 對照的 Phoenix TECP 平均輸入換算約 0.08095 mm²/s 與 299 J m⁻² K⁻¹ s⁻½。皆是對摘要平均值的衍生量，非對樣本熱慣量取平均，不與 MS-02 遙測像元當成同類觀測，亦不是「誤差」。
- **裁決：保留 E04 為局部已知冰與濕覆土的地面雷達／鑽測方法證據。** 想論證地球與火星的熱環境吻合或同型冰分布，仍不支持。既有 Haughton 就此用途並非未研究：Thomson 2012 為雷達和取芯門檻，[Barfoot et al. (2010)](https://doi.org/10.1016/j.pss.2009.09.021) 是既有 Devon Island 機器人勘冰類比，Knightly 2018/2019 做過濕多邊形類比；目前不主張全球新用途。可新增的狹義貢獻是對 MS-02 固定框的尺度與失效條件對照。
- **剩餘阻礙：** MS-02 火星真值（冰存在、埋深、含量、覆層成分）仍未觀測；MS-02 實際可用的獨立證明需同框受控高解析度形貌與／或更淺層探測、材料及界面約束。地球方面未取得 Haughton 完整 27 日原檔、同址多感測器鏈、全區冰量或乾濕成對控制。不能用不同地點的地溫、冰深、LiDAR 或濕度拼成一個控制實驗。
