# Team 2: Same-purpose research and novelty audit

Team zasa. Review date: **2026-11-14, Asia/Taipei**. Phase 1 repository baseline: `3e3ffff`; Phase 2 main baseline: `263269a`. Scope: literature and proposal checks for I-01, I-02, D-03 and D-04, followed by the supplied Earth candidate EARTH-UV-001. No new site selection, Earth pairing, environmental validation or ranking.

## 2026-11-14：五項延伸工作、EH全表QA與驗證協定草案

本輪依使用者「全部都做」指示，把前述五項工作推進到目前證據允許的程度。沒有改GPU程式或輸出；數值複核由本輪執行，不能歸為GPU隊友已交付。只更新Team2兩檔，歷史「尚未解析全表」保留為當時紀錄，以下為新狀態。

### 1. 1998全文與25／45cm：外部證據仍缺

再查 `"S0954102098000054" "pdf" McKay Mellon Friedmann`、`"Linnaeus Terrace" "45 cm" corrigendum correction Marinova`、`"Soil temperatures and stability" "McKay" author manuscript full text`，並篩查NASA相關原稿線索。仍只取得摘要／引用，未取得合法可核實的1998全文或勘誤。無新的成因證據，不重複把25cm來源較早改寫成「已證明45cm錯誤」。**此項未結案**；所需外部證據是原文pp.31–38、作者稿或明確更正。沒有冒用機構存取、繞過存取限制或向他人發訊息。

### 2. Elephant Head：108頁原始表完整抽取與雙引擎複核

來源QA1：[EH2019原始補充PDF](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0954102019000269/resource/name/S0954102019000269sup001.pdf)，SHA-256 `20fe70f574bc394f05f0c720809f80a9602ac73f6ede34d322ea816cf25590d9`。先用pypdf抽取整份108頁，僅接受「列號＋兩個日期時間＋6或9個數值」的完整列；第二次用PDFium抽取，**逐一比對全部8922筆的列號、第一時間與數值完全相同**。沒有插補、濕度裁切或時區轉換。這是出版資料轉錄／一致性QA，不是重新校準原感測器或獨立現地驗證。

| 實際執行的檢查 | 結果與適用範圍 |
|---|---|
| 列數與列號 | 8922筆；1–8922完整，無重複或缺號；符合資料列格式的紀錄無解析失敗 |
| 第一印刷時標 | 2017-11-28 00:00 至2018-12-04 17:00，逐時連續；無重複時間 |
| 第二印刷時標 | 全部比第一時標晚90分鐘；與標頭所列兩個GMT偏移一致，但其UTC／當地太陽時意義仍未獨立核實 |
| 3cm通道 | 2646筆，最後為2018-03-18 05:00；之後缺失保持缺失，未產生3cm全年均值 |
| 年窗口 | 依第一印刷時標2017-12-01含至2018-12-01不含，8760筆；不是已轉UTC的窗口 |
| 夏季共同有效窗口 | 同時標2017-12-01含至2018-03-01不含，2160筆；各深度同一列配對 |
| 修正RH異常提醒 | 49cm的corrected RH有2807筆大於100%；保留原作者數值及校準脈絡，不默默裁成100%，不將其當未經校準的水活性 |

描述性結果（°C，從已發表表格重算，**不是新量測**）：

| 窗口與量 | 本輪均值 | EHA1 Table II PDF p.5所列 | 核對 |
|---|---:|---:|---|
| 年air | −20.2940 | −20.3 | 四捨五入至0.1°C一致 |
| 年49cm | −19.2370 | −19.2 | 一致 |
| 夏air | −10.3409 | −10.3 | 一致 |
| 夏49cm | −8.6302 | −8.6 | 一致 |
| 夏3cm | −5.3553 | −5.4 | 一致 |
| 夏3cm減49cm配對均差 | +3.2749，N=2160 | 未將其當新效應驗證 | 僅描述兩已知深度，不能唯一反演冰深或TI |

**可用性結論：** 可支援原印刷時標下的共同期間深度溫差描述與原表重現。UTC／太陽時對齊、RH衍生水汽／棲地指標、新界面偵測、因果效應與火星性能不因本次QA而通過。序列自相關未建模，8760筆不是8760個獨立樣本；不提供虛構信賴區間。跨引擎相同能排查轉錄差異，不能排除原作者檔案中的錯誤。

