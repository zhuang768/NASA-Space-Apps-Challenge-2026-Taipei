# Team 2: Same-purpose research and novelty audit

Team zasa. Review date: **2026-11-14, Asia/Taipei**. Phase 1 repository baseline: `3e3ffff`; Phase 2 main baseline: `263269a`. Scope: literature and proposal checks for I-01, I-02, D-03 and D-04, followed by the supplied Earth candidate EARTH-UV-001. No new site selection, Earth pairing, environmental validation or ranking.

## 2026-11-14：主要對話、GPU與隊友1的直接交接

交接基準：main `bc9fe3c`；研究需求沿用暫定 `MR-20261114-v1`。以下三份可分別閱讀／轉貼。**文件發布不代表已傳送到其他對話、取得收件確認或完成對方工作。**先前查核與QA紀錄完整保留於下方。

### 共用資料與可重跑QA連結

- [固定版本：Team 2報告、QA說明及重跑程式](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/bc9fe3c/docs/research/team2_novelty_audit.md)：見「五項延伸工作」的第2節與「重跑方式與數值來源」。
- [固定版本：候選查核CSV與完整QA結果](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/bc9fe3c/outputs/research/team2_novelty_audit.csv)：`candidate_id=EARTH-002`，欄位 `executed_evidence_qa_json`。這是QA摘要，不是完整tidy時序；其他列的該欄空白不表示零或QA失敗。
- [固定版本：Team 1候選與資料需求](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/bc9fe3c/outputs/research/team1_earth_analog_candidates.csv)：`earth_candidate_id=EARTH-002`，含來源與原GPU需求。
- [原始108頁EH補充資料PDF](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0954102019000269/resource/name/S0954102019000269sup001.pdf)；SHA-256 `20fe70f574bc394f05f0c720809f80a9602ac73f6ede34d322ea816cf25590d9`。
- [McKay et al.2019原始論文](https://www.nasa.gov/wp-content/uploads/2019/09/mckay_etal_2019_dry_permafrost_ellsworth_land21.pdf)：Methods、Appendix及Table II（PDF p.5）。
- [主線需求分支固定版本](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/9e5c49ea7b4d7272972e7d409e6a298e6ef3da4a/docs/research/main_research_requirements.csv)：記錄實際採用的版本，不冒稱已在main整合。

### 給主要對話：研究定位與待決事項

**Team 2交付版本：main `bc9fe3c`，EARTH-002 → I-02。**

Elephant Head的108頁補充資料已完整轉錄，共8,922筆逐時紀錄。兩套PDF引擎逐列比對列號、第一時間與數值一致；重算年均與夏季均溫，四捨五入至0.1°C後與原論文Table II一致。這支持原印刷時標下的熱響應描述與既有分析重現，不能代表原感測器重新校準、獨立真值或場址適用性通過。

目前已完成資料轉錄QA、均溫重現、研究先例整合及驗證需求草案。新盲判、覆土受控實驗、採樣升溫、冰質量收支、地球到火星性能驗證仍未完成。覆土影響熱響應、跨場址機制比較與受控加熱已有研究，不以此稱新發現。

**主要對話下一步：**

1. 將本階段定位為「重現、資料QA整合與驗證需求設計」。
2. 若要新的科學分析，先明定問題、輸入及結果量，再評估現有資料是否足夠；不因QA成功直接宣稱新貢獻。
3. 決定是否啟用Linnaeus備案；25／45cm矛盾尚未解，不自行選成唯一真值。
4. 未取得獨立真值與可識別控制前，不報準確度、因果、冰損失或火星性能。協定草案仍待主線審查，不是已定案實驗。

### 給GPU：接續QA與可重跑交付

**對象：EARTH-002／Elephant Head → I-02。** Team 2實際執行的結果如下；請獨立重跑後再記GPU自己的驗證狀態。

| 項目 | 已執行結果 |
|---|---|
| 原始補充資料 | 108頁，8,922筆；完整列號且第一時標逐時連續 |
| 第一印刷時標 | 2017-11-28 00:00至2018-12-04 17:00 |
| 第二印刷時標 | 全部比第一時標晚90分鐘；UTC／太陽時定義仍待獨立核實 |
| 3cm通道 | 2,646筆；最後2018-03-18 05:00，後續保持缺值 |
| 年窗口 | 第一時標2017-12-01含至2018-12-01不含，8,760筆 |
| 夏季配對窗口 | 第一時標2017-12-01含至2018-03-01不含，2,160筆 |

**GPU下一步：**

1. 從上列原始網址重取PDF，核對hash，依報告內程式重跑，交付自己的版本、命令與差異檢查；不把Team 2結果直接標為GPU已驗證。
2. 產出帶來源頁碼／列號、兩個原時間欄、單位、深度及缺值的tidy table和資料字典。現在CSV裡的QA摘要不能取代完整時序。
3. 查明兩個印刷時標的實際定義；未核實前不轉UTC／太陽時，不做跨資料集時刻配準。
4. 保留raw與corrected RH。49cm corrected RH有2,807筆超過100%，須檢查原校準脈絡並標記，不能默默裁切或直接當成水活性。
5. QA後製作共同有效夏季的3cm／49cm溫度與配對溫差圖，標明期間、有效N、缺值與限制。這些圖尚未由本次交接製作。

限制：不計3cm全年均值、不補冬季、不用兩深度唯一反演冰深／TI；逐時紀錄不是獨立樣本數。RH衍生量要先確認基準，這組表不能給出採樣冰損失。資料取得／解析成功不等於科學適用性全部通過。

### 給隊友1：場址證據與用途修訂

**對象：EARTH-002／Elephant Head。** 保留原ID、錨點、用途與修訂歷史。新QA支持將已知剖面作描述性方法參照，未完成新界面偵測，也未證明與I-02的冰深、材料或熱性質相等。

既有先例保留：Site 3鄰近站點已有分層採土、鑽冰芯與低溫保存；10cm分層採土不等於10cm受控分段鑽冰，保存溫度不等於鑽進時樣品升溫。完整聯合流程與新試驗範圍仍資料不足。

**隊友1下一步：**

1. 分清歷史監測點、既有採樣點與提議試驗區；沒有可靠範圍就保留point anchor，不自行補半徑。
2. 建立位置—日期—深度—方法對照，不把不同年代／位置的45或49cm移作同一真值。
3. 盤點可取得的覆土粒徑、密度、孔隙率、含水／冰量及熱性質；分開實測與模型採用值，缺件寫unknown。
4. 說明是否有同位、同期且獨立於判讀輸入的界面真值。公開歷史49cm不能同時作擬合答案與盲測留出答案。
5. 若仍提議冰損失模組，先確認初始／回收冰量、樣品溫度、處理時間與質量校核是否可量測；缺件則維持未啟用，不報損失結果。

本輪不用再找新場址或重跑排名。先回覆現有場址能支持哪些研究、哪些仍不可執行；Team 2在收到具體範圍與協定後才能續查完整同用途先例。

**發布與檢查：** 以上交接整理自已執行QA及既有查核；僅增補Team 2報告，未改其他人的狀態或文件。各方回覆請帶固定ID、採用版本、來源與未完成項；尚無接收確認。

---

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

### 3. 新增實質方法先例：受控加熱不是空白領域

LTA9：Mellon et al.2025 [Humidity Enhancement in Dry Permafrost](https://doi.org/10.1089/ast.2024.0148)，出版者摘要已讀；並實讀作者[LPSC2056兩頁摘要](https://www.hou.usra.edu/meetings/lpsc2025/pdf/2056.pdf)，Experiment／Model／Results。原研究已做受控熱脈衝、不同土壤材料、T/RH陣列與數值模擬，結果量是濕度／水活性；不能把「控制材料與加熱、量溫濕度」稱為我們的新方法。該實驗不是LT新鑽孔，也不是盲判冰界面或採樣冰量收支的直接先例。期刊全文的所有細節與補充未完整查讀，不能認證完整協定沒有重複。

| 擬議差異 | 證據判斷 | 現有資料能否執行 |
|---|---|---|
| QA後重現EH均溫與深度熱差 | 本輪已執行，屬重現與資料整合 | 可以，範圍如上 |
| 25／45cm衝突與層位不確定性帳 | 可查證的資料追溯成果；未解決成因 | 可以記錄，不可選成唯一真值 |
| 覆土／濕度影響熱響應或冰穩定性 | LTA3／LTA5／LTA6已有實質研究 | 可重現脈絡，不能主張新機制 |
| 控制土樣與熱輸入，測T/RH | LTA9已有方法先例 | 新實驗未執行，不能宣稱原創 |
| 加入獨立真值是否降低特定方法的冰界面誤差 | 尚缺演算法、輸入、可用真值及試驗控制 | 現有EH兩深度表不足；仍是研究提案 |
| 控溫是否減少採樣冰損失 | UV控溫與EH取樣組成已有；本組缺冰質量收支 | 不能由熱濕表回答，需新實驗 |

因此不保證新穎性。可交付貢獻是可重現的QA、來源／量測限制及有缺件清單的驗證設計；新的科學分析差異尚未完成。

### 4. 獨立真值與覆土材料：可用性核對

| 項目 | 已知與可用範圍 | 還缺什麼 |
|---|---|---|
| LT25／45cm | 歷史來源衝突；GGD6安裝紀錄支持局部結構 | 1998全文、同剖面／年代核對；不是現代獨立真值 |
| UV W42cm | 已公開的歷史界面與站點觀測 | 不能把公開42cm拿來擬合後再報盲測；新測區、同期獨立真值未知 |
| EH49cm | 原感測器安裝界面；既有Site3取樣先例已確認 | 不同年45cm或監測站49cm不可互換；未知新試驗區與獨立留出資料 |
| 覆土材料 | 已有定性岩性／砂質與文獻模型參數 | 三站同位置同時期粒徑、密度、孔隙率、含冰量與校準熱性質尚不完整；模型採用值不是新測值 |
| 正負控制 | 已知有冰剖面可作參照 | 無冰樣本及偵測限、標籤獨立性未建立，不能報誤判率 |

這些資料足以定義缺口，不足以完成新盲判或因果實驗。沒有以地名、低溫或SWIM補成真值；也沒有將三個非同期場址當成已控制其他因素的實驗組。

### 5. 驗證協定草案 v0.1（未執行、未由主線定案）

本草案供MR-20261114-v1審查，不替團隊選購儀器、設定合格線或啟動出隊。當前可交付的是資料研究；以下為後續實驗的可檢查規格。

1. **問題與結果量先固定：** 分開「已知剖面熱響應描述」與「界面深度預測」。後者先定可用輸入、演算法及版本；不得以歷史界面答案選參數後回稱盲測。
2. **量測系統：** 候選方案為可校準、多深度接觸式溫度探針＋獨立物理剖面／取芯確認；它不等於TES。若主線選GPR等方法，須另列介電參數、頻率、解析度及偵測限。深度間距、設備範圍與樣本數依目標誤差和儀器規格訂定，本輪留空。
3. **範圍與材料紀錄：** 每試驗單元保留座標／datum／誤差、剖面圖、採樣深度與日期；覆土厚度、粒徑、密度、孔隙與含水／冰量逐項記來源。無法控制的材料、日照、溫濕度及接觸差異必須列為混雜因素。
4. **獨立真值與盲判：** 同位、相容時間的物理界面紀錄由獨立標記者保存；模型先固定再揭露。校準／開發和留出單元分開；時間相鄰樣本不可當獨立隨機樣本擴大N。缺真正留出資料則只報重現，不報新準確度。
5. **覆土控制：** 在可行實驗單元中先固定冰幾何、邊界熱輸入及儀器接觸，再按預先規劃改變覆土條件；測量差異而非假定相等。需要無冰正確標籤對照才能報誤判率；隨機化、重複與樣本數待功效／儀器要求評估，不能編造通過門檻。
6. **報告方式：** 深度偏差／絕對誤差、失敗與缺值、量測不確定度及有效支撐分開；不報無模型的95%信心。若無法辨識覆土與冰因素，結果就是不可辨識，不能轉成地下無冰。
7. **冰損失附屬模組：** 先有初始／回收冰質量、樣品溫度時間序列、處理時間、容器／空白及校核方法，才做質量收支；總回收質量、鑽頭溫度、保存設定不能替代。缺任一必要觀測則不啟用結果模組。
8. **火星轉移：** Earth可先驗證測量流程；低壓CO₂、重力、輻射與熱邊界差異須另建模型／環境驗證。沒有這些證據就不報I-01／I-02冰量、能耗或性能。

**可完成與外部依賴：** 已完成來源續查、EH全表轉錄QA／均溫重現、更新文獻差異矩陣、真值／材料可用性表及協定草案。尚未取得1998全文、未核實UTC定義、未取得新獨立真值／材料控制，也未做實驗；這些缺件不會因使用者要求持續工作而變成已完成。需要合法全文存取或新外部資料／量測，以及主線對協定作實際選擇。沒有替其他隊友回填完成狀態。

### 重跑方式與數值來源

以下程式以Python `pypdf`讀原始補充PDF；`p`改為實際下載路徑，結果輸出在記憶體。以相同hash重取原檔即可重跑。程式中的斷言只驗證結構與兩時標差，不等於感測器科學校準。跨引擎複核另外用`pypdfium2`逐列對比全部數值，已執行通過；不以均值相符代替完整轉錄比對。

```python
import logging,re,json,hashlib
from datetime import datetime,timedelta
from statistics import mean
from collections import Counter
logging.getLogger('pypdf').setLevel(logging.ERROR)
from pypdf import PdfReader
p='/tmp/team1_earth_002/elephant2019sup.pdf';r=PdfReader(p);rows=[];bad=[]
pat=re.compile(r'^(\d+)\s+(\d+/\d+/\d+ \d+:\d+)\s+(\d+/\d+/\d+ \d+:\d+)\s+(.+)$')
for page,obj in enumerate(r.pages,1):
 for line in obj.extract_text().splitlines():
  m=pat.match(line.strip())
  if not m:continue
  n,t1,t2,rest=m.groups();vals=rest.split()
  try:
   assert len(vals) in [6,9];v=list(map(float,vals));a=datetime.strptime(t1,'%m/%d/%y %H:%M');b=datetime.strptime(t2,'%m/%d/%y %H:%M')
  except Exception:bad.append([page,line]);continue
  rows.append(dict(n=int(n),page=page,t=a,t2=b,v=v))
assert not bad
assert [x['n'] for x in rows]==list(range(1,8923))
assert len({x['t'] for x in rows})==len(rows)
assert all(b['t']-a['t']==timedelta(hours=1) for a,b in zip(rows,rows[1:]))
assert all(x['t2']-x['t']==timedelta(minutes=90) for x in rows)
annual=[x for x in rows if datetime(2017,12,1)<=x['t']<datetime(2018,12,1)]
summer=[x for x in rows if datetime(2017,12,1)<=x['t']<datetime(2018,3,1) and len(x['v'])==9]
result=dict(source_sha256=hashlib.sha256(open(p,'rb').read()).hexdigest(),parser='pypdf + anchored rowregex;6or9numericvalues; no imputation/clipping',pages=len(r.pages),records=len(rows),bad_records=bad,first=str(rows[0]['t']),last=str(rows[-1]['t']),row_ids_contiguous=True,hourly_first_timestamp_contiguous=True,second_timestamp_offset_minutes=90,timezone_status='printedoffsetconsistent_butUTCmeaning_unverified',records_with_3cm=sum(len(x['v'])==9 for x in rows),last_3cm=str([x for x in rows if len(x['v'])==9][-1]['t']),annual_n=len(annual),summer_paired_n=len(summer),annual_air_mean_C=mean(x['v'][0] for x in annual),annual_ice49_mean_C=mean(x['v'][3] for x in annual),summer_air_mean_C=mean(x['v'][0] for x in summer),summer_ice49_mean_C=mean(x['v'][3] for x in summer),summer_soil3_mean_C=mean(x['v'][6] for x in summer),summer_soil3_minus_ice49_mean_C=mean(x['v'][6]-x['v'][3] for x in summer),RH_ice49_corrected_above100_n=sum(x['v'][5]>100 for x in rows),limits=['NoUTC/solartimeconversion','Noannual3cmmean','Noice-depth/TIinversion','Noindependenttruthvalidation','Noice-massbalance','Digitizedpublisherdata;not sensorrecalibration'])

print(json.dumps(result, indent=2))
```

本輪QA完整結果另存在CSV的 `executed_evidence_qa_json`（EARTH-002列），包含來源hash、窗口、有效數、均值與限制。其餘既有資料不改；不把原作者表格當我們的新觀測。新增來源LTA9與QA1只在本節定義；保留之前所有查核紀錄。

---

## 2026-11-14：1998全文／作者公開稿續查

本次接續 main `cf00e25`，只補取全文路徑，不重做其他候選或統計。**仍未取得可核實的1998全文，25／45cm原因維持 insufficient_data；不下引用錯誤定論。**

- 新查 LTA7：[OpenAlex DOI紀錄](https://api.openalex.org/works/https://doi.org/10.1017/S0954102098000054)。實際讀取JSON：`is_oa=false`、`oa_status=closed`、`oa_url=null`、`any_repository_has_fulltext=false`；列出出版者及PubMed位置，均無PDF URL。這只是該索引的存取紀錄，不能證明所有作者稿都不存在。
- 新查 LTA8：[共同作者Friedmann的FSU官方頁](https://www.bio.fsu.edu/faculty-friedmann.php)，Selected Publications的1998條目。可確認書目；該條目沒有全文連結，沒有深度資料，不用來解決矛盾。此為頁面條目核對，不是FSU整個典藏的完整排除。
- 新搜尋未取得能證明25／45差異成因的原稿或勘誤。保留LTA2作者摘要25cm、LTA3後續轉述45cm與LTA6表格25cm；未把索引的非開放狀態當成科學結論。

搜尋日期2026-11-14（Asia/Taipei），實際查詢：`"McKay" "1998" "Soil temperatures and stability" pdf -site:researchgate.net -site:academia.edu`；`"S0954102098000054" manuscript fulltext`；`"Linnaeus" "45" "25" "erratum"`。無關天文Linnaeus勘誤未採用。已知出版者全文限制與NASA無下載狀態沿用上一輪紀錄，沒有把重複失敗算成新證據。

下一個可結案的證據是合法取得1998期刊pp.31–38、作者稿／原始剖面圖，或明確勘誤／作者書面說明；取得後逐項確認站點、年代、深度定義及45cm來源。在此之前，不能正式把45cm刪改成25cm，也不能推論冰層變化。本輪未向作者或圖書館發訊息，未改Team1資料。

---

## 2026-11-14：EARTH-003 接收、25／45 cm 來源鏈與 MR-v1 比較

本輪基準 main `409a2e77dbeb741486901f840da3643180bed2ac`，開始時工作區乾淨；保留 `01142ca` 的 Elephant Head 組成先例與所有火星範圍排除。只補本節與 CSV 的 EARTH-003，不重搜 EH 或重算 GIS。

**結論：25／45 cm 的矛盾已定位到來源，但原因尚未釐清。現階段主線適合稱「既有研究重現、來源與 QA 整合、後續驗證需求設計」，尚無已證實的新科學分析差異或新實驗結果。**

### 身份、版本與兩層範圍

接收 Team 1 main `409a2e77dbeb741486901f840da3643180bed2ac` 的 `EARTH-003 → I-02`（候選 CSV 第4列）：Linnaeus Terrace／LT／GGD6，歷史站點 77°36′S、161°05′E，即 −77.6°、161.083333333°（北東為正）。只有 point anchor，沒有新試驗區；guide 明列 datum `none`，不指定 WGS84。配對、ID 與座標未改。

主線三檔 `main_mars_research_cards.md`、`main_research_requirements.csv`、`main_project_synthesis.md` 於本輪 main 均未整合；實讀 `origin/codex/mars-research-mainline-20261114` commit `9e5c49ea7b4d7272972e7d409e6a298e6ef3da4a` 的 MR-20261114-v1，不修改其文件。需求仍為暫定設計、門檻未定。研究分兩層：

- **A：已發表資料 QA、熱響應描述與驗證需求。** 可立即比對既有文獻，不等待未來硬體。
- **B：未來盲判／覆土控制／新取芯與冰損失實驗。** 組成方法有先例；完整新協定仍資料不足，不能由本次未找到證明從未做過。

Team 1 CSV SHA-256 `cb45ebafe1d7e43506462bdc467b402bc6f2446cea3c1d0f7b2ee52468ef107a`；需求 CSV 的 branch 版本 SHA-256 `89fe4d295856c09edeaabd8a32b6e63fcb5cbc1ea3fe762e211eb6a773ccfaf3`。本輪只讀交接中的 raw 取得紀錄，沒有代替 GPU 解析原始時序或產生統計。

### 25／45 cm：各來源實際說了什麼

| 來源／實讀定位 | 數值與性質 | 同站／同年判斷及限制 |
|---|---|---|
| LTA2，1998 原論文出版者及 NASA 作者摘要 | 25 cm，描述 1994 年歷史冰膠結界面；不是我們反演的深度 | 本次可追到的最早期刊來源。全文未取得，不能宣稱檢查完原始剖面／圖表或所有調查點 |
| LTA1，1998 CAPS 原作者指南，printed pp.2–5（PDF pp.3–6） | 0／17／23／40 cm 感測器，23 cm 稱在冰層上方；挖坑到界面後向冰層鑽孔 15 cm | 與 GGD6／同一引用文獻有明確連結；guide 儲存期為1994–1995。40−15=25 cm 是與安裝敘述一致的解讀，不是另一筆獨立界面量測 |
| LTA4，2009 作者研究之摘要 | 25 cm；雪再現與冰穩定性解釋 | 沿用 LT 背景做機制研究，不是新的同站深度監測。只讀摘要 |
| EHA1，2019 Introduction PDF p.1（既有來源重用） | 25 cm，引用 McKay et al.1998 | 後續轉述，非2019新量測LT；未重搜EH |
| LTA3，2022 Introduction printed p.144／PDF p.1 | **45 cm**，明文引用1998研究 | 本次鏈中最早核實到45cm的位置；引用同一作者、年份、地區／高度，沒有另述新LT調查年、座標或剖面 |
| LTA6，2026 Table I printed p.124／PDF p.3 | 25 cm，再引用1998研究 | 同一歷史文獻的比較值，不是2026新量測LT；不能拿兩篇出版年份當冰層變化時序 |

**已釐清的是來源性質與引用關係，未釐清的是差異成因。** 現有證據較直接支持「25cm是1998作者報告值」，而45cm是後來轉述；但沒有原全文／明確勘誤，不能正式判定45cm必是筆誤，也不能排除未讀的不同剖面或其他脈絡。這些只是待查可能性，不是等權或已證實解釋。本次查詢未找到能確認成因的勘誤；不宣稱不存在勘誤。

資料處理應保留 `reported_depth_cm=25, source=LTA2` 與 `quoted_depth_cm=45, source=LTA3`，附 `conflict_unresolved`。若主線要用其中一值作模型幾何，須記採用理由、限制及敏感度設計；本次不替主線選定「唯一正確真值」。兩值都不是現況或新實驗留出答案。

**23cm層位限制：** guide 深度誤差為 ±0.03m，與25cm只差2cm；原文的「在冰上方」是安裝描述，不能升級成精確、全年、無誤差的純乾土分類。不能把這個誤差寫成常態分布、95%信心，不能在25／45未解時擅自重分層；交GPU保留名義深度與來源限制，不代算。

### 文獻比較：問題、控制、真值與已回答內容

下表 A 是當前檔案研究；B 是尚未執行的實驗設計。`真值`需分清現地結構、擬合資料、獨立留出驗證；有現地深度不代表做過盲測。EHA、U編號沿用舊來源，本輪不重做其搜尋。

| 原始來源／範圍 | 問題、資料與考慮的變因 | 真值、方法與結果／已回答什麼 | 對A／B的差異判斷與實讀限制 |
|---|---|---|---|
| LTA1／LTA2：LT歷史站點 | 多深度溫度與氣象；地下冰穩定性 | 現地安裝／歷史界面；年溫與水汽平衡推論。不是獨立盲測 | **A有同用途**：描述溫度與冰穩定性已有研究。LTA2僅摘要；熱性質方法細節不能冒稱原文已讀 |
| LTA4：LT及UV／Beacon背景 | 雪再現與覆土下冰能否維持；理論＋現地背景 | 雪頻率可解釋穩定深度；模型假設不是隨機覆土實驗 | A泛稱「表面條件影響地下冰」已有答案；B精確驗證未能判定。僅作者摘要 |
| LTA5：UV模型區域 | 薄雪補水、表層鹽脫水；氣象驅動土雪模型 | 情境模型顯示雪與鹽可產生不同穩定性效應；不是取芯保冰量測 | A機制／敏感度已有先例；摘要不能確立完整控制、誤差或驗證切分。未取得全文 |
| LTA3：UV W及其他實測站，2009–2013背景 | 能量平衡／熱擴散；多深度T/RH與氣象；albedo、粗糙度、濕度及感測器干擾 | 現地界面支持剖面，量測亦用於模型約束；三種擴散率方法，季節變化與含濕導熱相關；未見本組所需的盲判留出 | **A問題實質重疊**，多深度溫差／擴散率與覆土影響不是新題。B未定。讀Methods、模型與Appendix相關全文段落，不等於所有補充與引文已讀 |
| EHA1：EH監測站，既有查核 | 乾覆土、冰界面、T/RH、水汽與棲地 | 挖溝與站點感測；提供局部結構與自然環境解釋 | A為已有觀測／相關研究；不等於盲判工程測試。沿用既有PDF方法查核 |
| EHA2：EH Site1／3，既有查核 | 微生物目的的分層土樣、取芯與保存 | 已有取樣組成；並非鑽進升溫曲線／初末冰量收支 | B組成先例保留。新試驗區未定就不能判同範圍完整協定；不重搜 |
| LTA6：UV／EH主序列及LT文獻比較 | 夏季雪、表面水汽與熱波相位如何維持冰界面 | 以原序列／模型比較機制；LT無地下RH；雪事件變更的模型結果已有 | A跨場址比較與表層—地下機制**已有實質答案**；B不由此完成。讀Environmental data、Table I、Results及相關Discussion段落 |
| U2／U3：UV舊鑽孔與方法，既有查核 | 分段鑽採、鑽頭溫控與相變控制 | 已執行方法組成；與W新試驗區不等同 | B分段／控溫不是新方法；U3仍僅摘要，不擴張舊讀取聲明 |

LTA3定位：printed pp.145–151（PDF pp.2–8）方法／參數，Appendix printed pp.165–171（PDF pp.22–28），尤其pp.166、169、171 的方法比較與限制。它也指出導熱率、密度、熱容量沒有獨立量測，且感測器配置會限制反推；**「需要更多材料觀測／更合適層位」也已有研究依據**。本組若只把該建議重新列清單，應標資料整合，不稱新方法。此處不是把已有模型內的參數擬合認作本組需要的留出測試。

### 五個層次的判定與目前可檢查的差異

1. **觀測／製圖：** LT、UV、EH 已有現地量測；本輪沒有新增觀測。
2. **相關研究：** 三地熱／水汽／冰穩定性已有研究，不能說未研究。
3. **相同用途組成：** 熱響應描述、熱物性估計、模型敏感度已有；UV鑽採控溫與EH取樣先例保留。
4. **同範圍、同問題與結果量：** 對LT歷史剖面的溫度／冰穩定性描述，A層 `same_use_exists`；對跨站自然機制亦有明確先例。但新問題若是「特定演算法的盲判誤差」，它需要別的結果量，不能由已有描述表直接判重複或判新穎。
5. **完整未來協定：** B層 `insufficient_data`。新試驗範圍、儀器、輸入、覆土控制、獨立真值及結果量未定，無法完成同範圍同用途查核。

**當前工作定位：** 重現已有熱描述／機制脈絡，加上來源追溯、數據QA與證據限制整合。具體可檢查的交付差異是25／45引用衝突帳、深度不確定性與量測量／模型可用性的清單；這是本專案的資料治理交付，**未證明是文獻首創或新的科學發現**。目前沒找到已完成、有數據支持的新分析差異。若想研究判讀誤差如何隨覆土改變，須另定演算法、可識別控制與獨立評估；現有多站非同期序列本身不足以證因果。

### 可直接採用的措辭、撤回主張與交接

**A．報告可用文案：**

> 本專案以已發表的南極乾覆土—冰膠結地層研究作參照，整理資料來源、品質與熱響應的解讀限制，並提出火星候選I-01／I-02後續驗證所需的獨立冰證據與控制條件。這一階段屬重現、資料整合及驗證需求設計；未完成新盲判、覆土受控實驗、採樣冰量收支或火星性能驗證。Linnaeus歷史冰深的25／45cm引述尚未完全釐清。

**B．應撤回／避免：** 首次發現覆土影響熱響應、首次比較UV／EH／LT、全新聯合方法、三地已受控比較、25cm是當前真值、45cm證明冰層變深、已確認23cm為純乾層、已驗證I-02冰或資源量。不能以把已知方法串成長句作原創性證據。

**C．主要對話需決定：** 接受本階段為重現／QA整合與驗證設計，或另定可測的新結果量；若用LT深度作模型輸入，先訂衝突處理規則；決定是否有理由啟用備案GPU（本輪不啟用）。要做B層則先補完整協定與資料可行性，不自行加門檻。

**D．隊友1需補：** 歷史LT資料與原全文／現場剖面連結；任何新試驗區、datum與誤差；覆土粒徑／密度／水冰狀態的實際可取得性；真值的同位／同期／獨立性；原有三站用途版本如何對應MR-v1。已知缺件就寫unknown，不能用公開歷史答案充當盲測。

### 本輪來源、取得範圍與搜尋限制

| 編號 | 原始來源／網址 | 本輪讀取範圍 |
|---|---|---|
| LTA1 | [GGD6作者指南](https://nsidc.org/sites/default/files/20ggd6-userguide-v001.pdf) | 全指南，printed pp.2–5／PDF pp.3–6 的方法、siteLT、精度；歷史1998 CAPS文字、guide更新2021 |
| LTA2 | [1998 DOI](https://doi.org/10.1017/S0954102098000054)；[NASA NTRS](https://ntrs.nasa.gov/citations/20040089259) | 出版者HTML作者摘要已讀；NTRS摘要。PDF請求回傳HTML存取頁，**不是原始PDF全文**。未取得補充資料或勘誤 |
| LTA3 | [Marinova et al.2022 PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/432141245F43EF744DD8ABDB56580A5F/S0954102022000025a.pdf/climate-and-energy-balance-of-the-ground-in-university-valley-antarctica.pdf) | 28頁PDF已取得，實讀上列方法／模型／Appendix段落；不是新現地資料 |
| LTA4 | [McKay2009 DOI](https://doi.org/10.1017/S0954102008001508) | 出版者摘要，2008線上／2009卷期；未取得完整模型／補充 |
| LTA5 | [Williams et al.2018出版者頁](https://www.cambridge.org/core/journals/antarctic-science/article/effects-of-snow-and-salt-on-ice-table-stability-in-university-valley-antarctica/62069847A335AEDFDACD88EFF144C46F) | 作者摘要，2017線上／2018卷期。PMC遇驗證；EuropePMC XML回500，沒有把indexed全文片段當作已讀全文 |
| LTA6 | [McKay et al.2026 PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5B2E97EBA4C91035CAFCECC234A532A0/S0954102025100448a.pdf/summer-snow-determines-the-depth-to-ice-cemented-ground-under-dry-permafrost-in-antarctica.pdf) | 13頁PDF已取得；2025-11-27線上、2026卷38，Environmental data／Table I／Results／相關Discussion；未宣稱全引文鏈完成 |

LTA3 PDF SHA-256 `3090b004f5d633897e447eb9b58d7e3ab9ab32f47f56d18c50b2331bc0a6e1a1`；LTA6 `749416df3b1c3de64dacf02040817382ba05e711469f9dd4a386230b16cb9915`。未提交原始PDF；未處理GPU時序。

搜尋日期2026-11-14（Asia/Taipei）。新查詢：`"McKay" "1998" "Linnaeus" filetype:pdf soil temperatures stability`；`"Climate and energy balance" "45 cm" Linnaeus`；`"S0954102098000054" pdf`；`"Soil temperatures and stability" site:nasa.gov`；`"Linnaeus" "45 cm" ice McKay`；`"Linnaeus" "45 cm" "corrigendum"`；`"Snow recurrence sets" filetype:pdf McKay`；`"The effects of snow and salt on ice table stability" cambridge`。另直接讀取已知原始來源與MR-v1三檔。

此為有界的來源與問題查核，不是所有資料庫／歷年提案完整排除。原1998全文、明確勘誤、全部補充與後續引文仍缺。沒有取得新的幾何，不改火星交集結果。文獻A層比較已完成；B層缺件如上，不等待B才交付A。

驗證：新增EARTH-003一列，保留原6列與45欄，追加3個明確的版本／結構欄（舊列留空）；來源ID、固定座標與Team1原用途比對；JSON可解析；舊報告全文保留。OpenAI Codex協助來源核對與撰寫，沒有新增實驗、統計或科學通過結果。

---

## 2026-11-14 新版交接：已知用途、待查缺口與 EARTH-002

本段以最新 main `cf72039` 的 Team 1 版本 `TEAM1-ICE-REDO-v1`（`EARTH-002 → I-02`，`EARTH-UV-001 → I-01`）更新交接；下方舊階段敘述保留為當時紀錄。研究需求 `TEAM1-PROVISIONAL-ICE-v1 / 2026-11-14` 尚待主要對話定案；`docs/research_requirements.csv` 仍是較早的綜合需求，不能當作新冰探查規格。清理提交 `5901362` 已包含在此 main 歷史中；總 Excel 不是本輪新配對的交付證據。本次只改本報告與 Team 2 CSV。

### 隊友 1 選點可用的已知用途簡表

| 地點／區域 | 已知研究或測試用途、原始來源 | 已取得範圍 | 與目前用途相近及已確定重複的部分 | 尚不能判定；給新候選的提醒 |
|---|---|---|---|---|
| University Valley，W 站與山谷 | W 站冰界面及氣象監測 [U1]；Icebreaker 火星類比鑽探、短段取樣及控溫 [U2–U3]；樣品處理 [U5] | U1 的 W 點位；U2 另一鑽孔點約離 W 2.13 km；U5 未定位到 W | 山谷尺度的火星類比鑽探和分段、控溫用途已有先例；W 點的冰界面也已量測 | `EARTH-UV-001` 的「周邊」未畫範圍；盲判、獨立取芯誤差與冰質量收支的完整聯合流程未證實。保留為已知用途對照，不能稱首次鑽探 |
| Elephant Head，Mount Dolence 北側監測站／Site 3 | 壕溝確認冰界面與熱濕監測 [EHA1]；Site 1/3 分層採土、鑽取冰芯與低溫保存 [EHA2]；與 UV 的冰界面機制比較 [EHA3] | 監測站點位；EHA1 明載站點在 Site 3 的 10 m 內；EHA2 的 Site 1、3 座標，兩點約 0.3 km；無新試驗區 | 冰界面已有直接真值；Site 3 附近已有分層採樣及鑽冰芯。跨 UV/EH 的自然機制比較已做過 | 現有原文未顯示盲判深度誤差、鑽採時樣品升溫或初末冰量收支。不可把「10 cm 分層採土」改述為「10 cm 分段鑽冰」，也不能以低溫保存代替升溫量測；需界定新試驗區 |
| I-01／I-02 火星名義格 | SWIM 冰一致性製圖與冰資源探索區先例 [N1–N3, P1–P5] | 兩個 0.5° 名義格；已查 I-MIM 初始 RZ、已釋出的 SWIM4MIM RZ 及兩個 ASU 圓；其他替代 EZ／ROI 未取得完整幾何 | 廣域冰探查與資源評估已有研究；上述具名受查範圍與兩格不重疊 | 未取得所有替代 EZ／ROI 與後續提案的原始邊界及用途對照。不得從已查的不重疊推成所有提案均不重疊；低溫及 SWIM 指標不證明可挖冰 |
| D-03 Hellas／D-04 Elysium 周邊 | 已有區域沙塵與地表變化研究 [N6–N9] | 區域研究；候選格與研究／任務完整範圍的交集仍有缺口 | 已研究區域與沙塵背景，不能稱發現全新沙塵區 | 隊友 1 尚未交新地球 ID、範圍與測試用途；先等交接，不自行配對 |

狀態整理：既有四個火星格的區域文獻與已查幾何結果屬**已完成、沒有新疑點**；若得到完整替代 EZ／ROI 資料或新提案，才更新那些範圍結論。`EARTH-UV-001` 的山谷先例已完成，確切 W 周邊範圍仍待 Team 1。`EARTH-002` 已收到並於下方逐項查核。D-03／D-04 的新地球候選待 Team 1；儀器、深度、誤差、冰損失門檻與正式聯合流程待主要對話。

### EARTH-002 → I-02：新候選逐項查核

**交接身份與問題。** 固定 ID `EARTH-002`；Elephant Head monitoring station／Elephants Head Permafrost Site，Mount Dolence 北側，南極洲。Team 1 的地球錨點 `−79.820216667°, −83.314333333°`（北、東為正，原始文獻 `79°49.213′S, 83°18.860′W`）；火星 I-02 `53.75°N, 42.25°E` 為 planetocentric／東經。地球文獻未報水平 datum 或定位誤差。新測試區只有已發表站點錨點，無半徑、多邊形或鑽孔；不得用站點與 Site 3 的 10 m 既有關係冒充新試驗範圍。用途版本 `TEAM1-PROVISIONAL-ICE-v1 / 2026-11-14`：盲判乾覆土下冰膠結界面並以獨立真值驗證，接著受控分段採樣，分開量測樣品升溫與冰質量損失；屬**提議、未執行**。查核 Team 1 §8 四項問題，尤其分清觀測、取樣、工程驗證與整套流程。

| 層次／組成部分 | 讀到的原始證據與範圍 | 本次判定 |
|---|---|---|
| A. 站點與冰界面研究 | [EHA1] 2016 年在 Elephant Head 四處以挖溝定冰界面；監測站在 Site 3 的 10 m 內，長期感測器置於 49 cm 界面。[EHA3] 已研究本站與 UV 冰界面受夏季積雪、熱及水汽影響的機制 | `related_research_exists`；本站不是未研究場址，UV–EH 自然機制比較也已有先例 |
| B1. 分層土樣、冰芯與冷藏 | [EHA2] 2020 年在 Site 1／Site 3 每 10 cm 分層以無菌勺取乾凍土，在 30／45 cm 見冰界面，以手持電鑽及鑽石取芯鑽頭取得 13／3 cm 冰芯，現地、運輸、實驗室維持 −20°C。Site 3 的發表座標與 EHA1 的 Site 3 相同，而站點在 Site 3 10 m 內 | **站點鄰近尺度的用途組成先例已確認**；先前 Team 1 僅從 EHA2 摘要得知微生物用途，現在讀到全文方法，應補記分層與取芯。這不是受控分段鑽進、鑽頭／樣品升溫曲線或冰損失量測 |
| B2. 盲判界面與獨立真值 | [EHA1] 壕溝與 [EHA2] 採樣提供已知界面；兩者所讀方法未述隱藏真值、固定盲判演算法、預先登記誤差／漏判／誤判 | 已有**真值測定**，本次未找到**盲判驗證**；不能把文獻沒提到直接寫成從未執行 |
| B3. 升溫、冰損失與完整流程 | [EHA2] 的 −20°C 是保存條件，不是鑽進時樣品溫度；[EHA1] 的冰界面長期水汽穩定性，[EHA3] 的冰界面機制也不是回收冰芯初末質量量測 | 本次未找到可驗證的升溫曲線、初末冰量或完整聯合流程；`complete_joint_protocol_status=insufficient_data` |
| C. 相同範圍、相同完整用途 | EHA1 明載站點與舊 Site 3 的距離關係；EHA2 重用 Site 3 座標，但未提供鑽孔的精確位置或新提議試驗區 | **既有取芯活動可能與提議站點周邊高度接近**，不能說沒有同址先例；完整同範圍同用途仍 `insufficient_data`，不設定無來源的半徑 |

**可保留的研究差異（待證實，不是新穎性結論）：** 將已有實測界面當獨立真值，在明定場址、儀器與輸入後，先盲判界面深度與漏誤判，再同一試驗設計量測分段取芯的樣品溫度、處理時間、初末含冰量及質量變化。這些輸出會回答「探查方法的誤差」與「採樣是否保存冰」，與 EHA1 的熱濕平衡、EHA2 的微生物取樣、EHA3 的自然形成機制所報量測不同；是否有未查到的同流程研究仍未排除。站點可作**待設計的方法參照候選**，不稱已證實新研究場址或已可施工。與 I-02 的關係僅是方法問題：不得由 Elephant Head 冰芯推算火星格內冰深、可採量、能耗或安全性。

**查核與存取紀錄。** 2026-11-14（Asia/Taipei）查詢公開網頁及出版者／NASA 原文，詞組：`"Elephant Head" Antarctica ice cemented drilling sampling core ice loss blind detection`；`"Elephant Head" "ice-cemented" drilling sampling Mars analog`；`"Elephants Head" permafrost site ice probe borehole thermophysical experiment`；`"Elephant Head" "ice table" thermal probe McKay sampling`；`"Elephant Head" Antarctica "drill" "ice" Mars 2021 2022 2023`；`"Elephant Head" "ice-cemented" "radar" Antarctica`；`"Elephant Head" Antarctica "ice loss" sampling`；`"Elephant Head" Antarctica "blind" "ice" probe`。實際讀到 EHA1 NASA 原文 PDF 的 Methods、Table I、Discussion；EHA2 作者原文 PDF 的 Site description／field sampling／Figure 1，檔案由 Semantic Scholar 鏡像取得並核對出版者 DOI；EHA3 出版者 PDF 的方法及結論。EHA2 出版者 HTML 開啟失敗，PMC 直接開啟遇瀏覽器驗證；未以搜尋摘要代替原文。未完整查 ADS／Scopus、所有後續引文、所有會議摘要、EHA2 補充資料及未公開野外紀錄；故「未找到」只限本次所列查詢與可讀材料。

| 來源 | 原始文獻與本次支持範圍 |
|---|---|
| EHA1 | McKay et al. (2019), [Dry permafrost over ice-cemented ground at Elephant Head](https://www.nasa.gov/wp-content/uploads/2019/09/mckay_etal_2019_dry_permafrost_ellsworth_land21.pdf)，Methods、Table I、Discussion；2016 挖溝、2017–2018 站點量測及 Site 3／站點位置。 |
| EHA2 | Wood et al. (2024), [Active microbiota persist in dry permafrost and active layer from Elephant Head](https://doi.org/10.1093/ismeco/ycad002)，[可讀原文 PDF](https://pdfs.semanticscholar.org/6702/fb238f8ae546875a33f0e1348cf9807ac160.pdf)，Methods pp.2–3／Figure 1；2020 分層土樣、鑽冰芯及保存條件。原研究目的是微生物學，不是儀器盲判或冰損失工程驗證。 |
| EHA3 | McKay et al. (2026，2025-11-27 線上發表), [Summer snow determines the depth to ice-cemented ground under dry permafrost in Antarctica](https://doi.org/10.1017/S0954102025100448)，[出版者 PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5B2E97EBA4C91035CAFCECC234A532A0/S0954102025100448a.pdf/summer-snow-determines-the-depth-to-ice-cemented-ground-under-dry-permafrost-in-antarctica.pdf)，結果及結論；UV–EH 機制比較，非新取芯實驗。 |

**交接。** 隊友 1：將 EHA2 的 Site 3 分層／取芯先例加入 `EARTH-002` 自己的來源核對，明確標示「取芯已做；升溫與冰質量收支未驗證」，並提供預定試驗區、儀器與量測流程；可保留候選作方法參照，也可修訂用途，不能以新 ID 隱藏先例。主要對話：可說「利用已研究的乾覆土—冰界面場址，設計盲判探查與採樣保冰性的聯合驗證」，**不可說**首次在 Elephant Head 發現冰、首次取芯、首次與 UV 比較、已證實完整流程新穎、I-02 有可挖冰或地球測試能直接預測火星性能。正式用途、誤差／損失指標與是否實作由主要對話決定。GPU 若只處理既有熱濕時序，可用於背景與 QA；那組表不能代替新流程的樣品升溫和初末冰量觀測。

CSV 沿用原有 45 欄，新增 `EARTH-002` 一列而未改欄名。此列 `classification=related_research_exists` 表示站點有研究；`site_level_same_use_status=related_research_exists` 表示相近的取樣／取芯**方法組成**已做，但 EHA2 的微生物研究目的不同；`exact_site_same_use_status=insufficient_data` 與 `complete_joint_protocol_status=insufficient_data` 表示新試驗區及完整用途尚不能判定。這些欄位是不同層次，不是分數或新穎性保證。原有 `EARTH-UV-001` 山谷尺度 `same_use_exists` 結論保留，不移用到 EARTH-002。

### 目前真正未完成的查核

1. **EARTH-002／EARTH-UV-001 的精確範圍：** Team 1 需提供試驗圖、半徑或多邊形，以及規劃鑽孔與歷史 Site 3／UV 鑽孔的關係；目前只能說站點錨點與已知採樣點的關係，不能判定整套流程的同範圍重複。
2. **用途版本：** 主要對話需定儀器、探測深度、盲判輸入與真值、分段採樣方法、樣品溫度及冰損失量測、決策門檻。定版後才檢索是否有完全相同的方法研究；EHA2 的補充資料和後續引文也是具體可查缺口。
3. **I-01／I-02 未覆蓋的火星提案：** 需取得 Head et al. 替代 EZ／資源 ROI 的原始幾何和名稱對應，以及 MarsGIS 的完整 EZ／ROI 圖層；得到資料才做相同座標慣例下的交集。P1–P3 已確定的分離結果不重算。也需核對後續具名冰探查目標，避免把目前搜尋未找到寫成沒有提案。
4. **D-03／D-04：** 等 Team 1 固定 ID、地點、座標、範圍、用途版本、來源及具體查核問題；目前沒有可逐項審查的新地球交接。

Latest ice-footprint results are in the dated follow-up immediately below. Earlier sections remain as the audit history.

## Ice-purpose footprint follow-up, 2026-11-14

This follow-up uses main `74c7ed6` and retains the earlier audit below. Only unfinished I-01/I-02 proposal-extent checks were extended. Purpose: **subsurface ice characterization and preliminary resource assessment research**. The fixed planetocentric, east-positive nominal cells remain **I-01: 54.00–54.50°N, 1.00–1.50°E** and **I-02: 53.50–54.00°N, 42.00–42.50°E**. These are project screening cells, not proposed drill footprints.

**Both candidates remain `insufficient_data` for the overall exact-site, same-purpose proposal question.** Several inspected targeting footprints are now confirmed separate from both cells. No same-footprint, same-purpose hit was confirmed in this follow-up. The unresolved alternative-EZ inventory prevents novelty clearance.

### Results by inspected footprint

| Inspected object and purpose | I-01 | I-02 | Evidence and boundary of conclusion |
|---|---|---|---|
| I-MIM 2022 initial reconnaissance zone: ice survey and resource assessment | Confirmed inspected footprint does not overlap | Confirmed inspected footprint does not overlap | P1, printed p.152 / PDF page 160: the entire initial RZ is restricted to ±40° latitude and maximum 0 km elevation. Both cells are entirely north of that band. This excludes the specified priority RZ only; it does not exclude future high-latitude observations or every mission objective. |
| Released SWIM4MIM notional reconnaissance-zone geometry: future orbital buried-ice targeting | Confirmed inspected footprint does not overlap | Confirmed inspected footprint does not overlap | P2: downloaded provider SHP/SHX/PRJ and README; actual polygon intersections are empty. Released geometry reaches only 51.217655°N. Do not equate this download automatically with the engineering-clipped I-MIM map. |
| ASU catalog “Deuteronilus Mensae”: represented 100 km EZ circle | Confirmed inspected footprint does not overlap | Confirmed inspected footprint does not overlap | P3 stores radius 100 km at approximately 23.20, 39.10. N2 already establishes ice/resource purpose for the primary EZ. The complete catalog circle is well south of both cells. This reuses the primary proposal's earlier purpose check. |
| ASU catalog “Deuteronilus Mensae 2”: represented 100 km EZ circle | Confirmed inspected footprint does not overlap | Confirmed inspected footprint does not overlap | P3 stores radius 100 km at 22, 41; even the northern edge is below 42.70° in the stated spherical calculation. The catalog provides no source citation establishing which Figure 2 marker or resource ROI this entry represents. Its individual purpose linkage remains insufficient. |
| Other alternative Deuteronilus EZs / associated resource ROIs in N2 Figure 2 | Extent or purpose insufficient; unresolved | Extent or purpose insufficient; unresolved | Original figure inspected in P4. It locates alternatives with similar objectives, but does not provide a coordinate table or full resource-ROI polygons. The two ASU entries do not establish completeness or a one-to-one crosswalk. |
| NASA MarsGIS full EZ / science-and-resource ROI inventory | Extent or purpose insufficient; unresolved | Extent or purpose insufficient; unresolved | P5 identifies a GIS product, but no public downloadable full layer was obtained. A software catalog description cannot substitute for the actual footprint data. |

The existing Protonilus and primary Deuteronilus checks remain in the historical record; no new regional geology or candidate matching was performed. “Confirmed separate” applies to each named representation above, never to every prior proposal in that region.

### Geometry, provenance and reproducibility

P2 is a released targeting polygon, distinct from the broad SWIM consistency-map coverage. The ancillary README describes notional lowest-latitude buried-ice targeting and refers to Morgan et al. (2025), section 7, DOI [10.3847/PSJ/ad9b24](https://doi.org/10.3847/PSJ/ad9b24). Publisher full access was restricted; the downloaded README and geometry support the intersection result independently. The provider does not identify in the ancillary attributes whether this is the filtered or unfiltered figure variant; that identity remains unverified.

- Accessed 2026-11-14. Provider lists reconnaissance product update **2025-08-05 09:13:41**. This is a provider timestamp, not an independently verified collection version.
- File `SWIM4MIM_RZ_GIS.shp`, SHA-256 `d652283966a46b93979010d4ffcd28171bd05d9e006f2857a36e4557f5209796`; inner ancillary ZIP SHA-256 `e2963b9a02966d1db83e0c8c4128708e195977079b96a935060ddf9f41445429`.
- PRJ: `Mars2000_equicylindrical_clon0`, spherical Mars radius **3,396,190 m**, Plate Carrée, central longitude 0°, false easting/northing 0, metre units. No Earth CRS or Earth distance formula was used.
- One valid MultiPolygon, five parts, 10,764 vertices. No DBF was supplied in the retrieved archive; no region names or feature attributes were inferred.
- Inverse-projected bounds: approximately **−179.999989 to 179.999989° longitude, −57.217651 to 51.217655° latitude**. Whole-cell north/south exclusion independently agrees with polygon intersection. Longitude wrapping cannot affect this latitude-based exclusion.
- Both `intersects` results are false and intersection areas are zero. Projected areas/distances are not reported as geodesic physical measurements. These calculations say nothing about ice abundance, accessibility or absence.

Minimal reproduction after downloading and extracting P2 (Python packages `pyshp`, `shapely`):

```python
from math import pi
import shapefile
from shapely.geometry import shape, box

stem = "SWIM4MIM_RZ_Ancillary/SWIM4MIM_RZ_GIS"
r = shapefile.Reader(shp=stem + ".shp", shx=stem + ".shx")
g = shape(r.shapes()[0].__geo_interface__)
assert g.is_valid
m = 3396190.0 * pi / 180.0  # metres per degree in the supplied PRJ
for site, lat, lon in [("I-01", 54.25, 1.25), ("I-02", 53.75, 42.25)]:
    cell = box((lon-.25)*m, (lat-.25)*m, (lon+.25)*m, (lat+.25)*m)
    print(site, g.intersects(cell), g.intersection(cell).area)
# I-01 False 0.0; I-02 False 0.0
```

P3's XML explicitly supplies a `Radius` field and `RadiusKm` geometry units, so these checks use complete represented circles rather than distances to unbounded centers. For a spherical circle, its northern bound is center latitude plus `100000 / 3396190 * 180/pi` degrees: **40.788°** and **42.688°**, respectively. The catalog latitude convention is not explicit; adding a conservative 0.5° convention allowance still leaves both circles south of 43.2°N and both candidate cells north of 53.5°N. Longitude orientation is therefore immaterial to this exclusion. Stored longitudes agree approximately with the primary N2 center, but a normalized all-ROI longitude overlay was not performed. The 0.5° allowance is an audit robustness check, not a provider accuracy specification. No editable JMARS layer was changed or saved back to its provider.

P3 file `2015_proposed_exp_zones.jlf` SHA-256: `51b371b8fc0dff5d00be2d9a2470ee9c59d0eda19cf752294d1d75ee2f79704e`. The tutorial session is dated 2016-02-09; this is a catalog snapshot, not proof of the complete current proposal inventory.

### Additional primary-source register

| Ref | Source and inspected material | What it supports / access limit |
|---|---|---|
| P1 | [I-MIM MDT final report, 31 August 2022](https://science.nasa.gov/wp-content/uploads/2023/10/i-mim-mdt-final-report-31-aug-2022-final-hi-qual-copy-tagged.pdf), §6.1.1, printed p.152, Figure 6.1 | Explicit initial-RZ bounds. The figure's black circles are illustrative, randomly positioned prospective TAIs, not actual selected targets. Local PDF SHA-256 `17d0212d4a7727a392153766ea41c9112909c1b3d3243e507f9c52b78c986778`. |
| P2 | [SWIM4MIM provider page](https://swim.psi.edu/SWIM4MIMProducts.php), [ancillary selection download](https://swim.psi.edu/SWIM4MIMProducts.php?RZ-Ancillary=True&DL-Sel=True), bundled README and SHP/SHX/PRJ | Actual released notional targeting extent. Download redirects to a temporary ZIP; retain hashes above to identify this snapshot. Broader mapping is a separate product. |
| P3 | [ASU JMARS2035 description](https://jmars.asu.edu/jmars2035/), [saved session](https://jmars.mars.asu.edu/static/saved-sessions/2035_tutorial.jmars), [original proposed-EZ XML layer](https://jmars.mars.asu.edu/static/saved-layers/mars2035/2015_proposed_exp_zones.jlf) | Catalog circle radii and centers. Read as XML, without executing serialized session objects. The second entry lacks a proposal/ROI cross-reference. |
| P4 | [NASA-hosted 2015 abstract collection](https://www.nasa.gov/wp-content/uploads/2015/06/mars-c-abstracts_in_order_of_presentation10242015_0.pdf), Head abstract 1033, PDF pp.55–56 / printed pp.49–50; same abstract as [N2](https://www.hou.usra.edu/meetings/explorationzone2015/pdf/1033.pdf) | Figure 2 visually inspected. Alternative locations and shared objectives are established; exact individual boundaries remain unavailable. No claim that the whole collection was reviewed. |
| P5 | [NASA MarsGIS software catalog, LAR-19183-1](https://software.nasa.gov/software/LAR-19183-1) | Leads to the potentially fuller GIS inventory; actual full EZ/ROI geometry not obtained. No access request or message sent. |

### Follow-up query log and remaining evidence

All additional searches: 2026-11-14, Asia/Taipei. Exact representative queries are retained here; landing pages, downloaded source contents and figure inspection determine conclusions, rather than search snippets.

| Group | Exact queries | Result and limit |
|---|---|---|
| Q10, reconnaissance footprints | `International Mars Ice Mapper reconnaissance zones 2022 report boundaries latitude`; `"SWIM4MIM" "RZ" shapefile`; `"ad9b24" "RZs" "boundaries"` | P1 and P2 obtained; published targeting boundaries can now be distinguished from mapping coverage. |
| Q11, alternative exploration / resource zones | `Mars exploration zones GIS shapefile 2015 human landing sites Deuteronilus alternative`; `"Deuteronilus" "exploration zone" "Figure 2" alternatives`; `"Head" "Deuteronilus" site:nasa.gov "2015" "pdf"`; `"MarsGIS" "FeatureServer"`; `"MarsGIS" "arcgis.com"` | P3/P4 inspected; P5 remains a catalog lead. No verified public full MarsGIS endpoint found in this search. |
| Q12, additional regional planning lead | `"Multi-criteria Overlay Analysis for Identifying Preferred Exploration Zones on Mars" pdf`; `"ade30e" "50°" "mask"` | Located [2025 paper DOI](https://doi.org/10.3847/PSJ/ade30e) and [Zenodo v1](https://zenodo.org/records/15854213). Publisher full access restricted; 140.8 MB analysis archive not downloaded. No footprint exclusion or candidate-purpose conclusion is based on this lead. |

Remaining evidence: a full alternative-EZ/resource-ROI polygon inventory with coordinate metadata and original-proposal crosswalks; the specific purpose and provenance of the ASU second entry; and any later named ice-survey/resource targets that include either whole cell or a documented subarea. Regional names, marker dots and unverified search-result summaries cannot close those gaps. Previously documented observation/mapping and regional science remain established and are not promoted to site proposals.

Permitted wording: “Neither nominal candidate cell intersects the inspected I-MIM initial RZ or the released SWIM4MIM notional RZ geometry. The inspected ASU Deuteronilus circles are also separate. This bounded search has not verified an overlapping same-purpose proposal; alternative-ROI coverage remains incomplete.” Do not claim “never studied,” “first ice-resource site,” “outside all exploration proposals,” “no ice,” or that SWIM mapping itself proves a new targeted proposal. D-03/D-04 remain unchanged references. No additional Earth candidates were audited; further Earth checks wait for Team 1's new list.

Follow-up verification: downloaded P2 geometry read successfully; validity, both exact cell intersections and an independent latitude-bound check agreed. P3 radius units and the two stored records were inspected. CSV retains all five prior records and all original fields, adding dated structured checks only for I-01/I-02. Only the two Team 2 deliverables changed.

## Decision for Team 1 (prior audit, retained)

**All four Mars candidates have related prior research. No exact-footprint, same-purpose Mars site proposal was verified in this bounded search. None is cleared as new or understudied.** These statements describe different checks: regional research is established; exact proposal overlap remains unresolved.

| ID | Classification | Exact-site / same-purpose result | Handoff |
|---|---|---|---|
| I-01 | Related research exists | No verified proposal hit; proposal inventory incomplete | Retain only as a conditional shallow-ice research candidate. Prior SWIM mapping covers this sector; that mapping coverage is distinct from a targeting reconnaissance-zone footprint (see the follow-up). |
| I-02 | Related research exists | No verified proposal hit; proposal inventory incomplete | Same treatment. The inspected Deuteronilus and Protonilus exploration zones are geographically separate. |
| D-03 | Related research exists | No verified dust-observation or equipment-test site proposal in this nominal cell | Existing eastern Hellas geological mapping encompasses the nominal coordinates. Keep as a context reference; withdraw any unstudied-terrain claim. |
| D-04 | Related research exists | No verified exact-cell operations proposal; published dust-study footprints remain unresolved | Cerberus/Elysium dust sources, sinks and surface changes are established research topics. Keep as a context reference; withdraw any newly identified dusty-region claim. |

Classification vocabulary: `same_use_exists` = 已有相同用途, requiring both compatible footprint and explicit purpose; `related_research_exists` = 已有相關研究; `not_found_in_this_search` = 本次搜尋未找到, always bounded by the logged search; `insufficient_data` = 資料不足. A related-research classification does not establish an exact same-use proposal. The exact-site proposal status remains `insufficient_data` for the four Mars candidates. This is not a claim that no such proposals exist. The Earth review below distinguishes a verified valley-scale use precedent from an unresolved exact station/vicinity footprint.

**Phase 2: first supplied Earth candidate reviewed.** Git fetch found `outputs/research/team1_earth_analog_candidates.csv` on `team1/earth-analog-first-case-2026-11-14` at `5efa19766342a5a9ab24fcbbe3dbf02ed05805a6`, not on main. It contains only **EARTH-UV-001 → I-01**. University Valley already has Mars-analog drilling, depth-segmented sampling and thermal-control research. This is a material same-use precedent for Team 1 to assess. Exact overlap with station W and the complete proposed interface-detection/ice-loss protocol is unverified. Earth candidates for I-02, D-03 and D-04 are **waiting for Team 1's list additions**. No older Jezero/Gale/Arcadia Earth matches were substituted.

## Phase 2: EARTH-UV-001 → I-01

### Fixed input and source identity

Read both Team 1 files directly from the fetched commit, without checking out, merging or modifying that branch:

- [Candidate CSV at the reviewed commit](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/5efa19766342a5a9ab24fcbbe3dbf02ed05805a6/outputs/research/team1_earth_analog_candidates.csv), SHA-256 `4a901e4bc2625dc516018cb468a35fdecf5574736b378545448059020db12e8b`.
- [Team 1 research handoff at the reviewed commit](https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/5efa19766342a5a9ab24fcbbe3dbf02ed05805a6/docs/research/team1_earth_analog_matching.md), SHA-256 `dc25c4d609ed5b9332567758c25680e14b1b1fb332cac4cb9c9ab6356ea9c5f4`.

ID **EARTH-UV-001**, associated Mars ID **I-01**. Site: **University Valley meteorological station W vicinity**, Antarctica. Earth anchor **−77.862150°, 160.710100°E**, retained exactly as supplied. This is a station reference, not a specified new borehole. No polygon or vicinity radius was supplied; the inspected coordinate passage does not state the horizontal datum.

Original CSV purpose, unchanged: `辨識乾覆土下冰膠結界面；驗證分段取樣升溫與冰損失。研究提議，尚未執行。` English reading: identify the ice-cemented interface below dry overburden and evaluate heating and ice loss during segmented sampling; proposed research, not performed. The handoff additionally proposes blind probe interpretation followed by physical sampling. No new pairing or replacement site is proposed here.

### Finding: substantial use precedent, exact joint protocol unresolved

**Anchor-level classification: related research exists. Valley-level component-use status: same use exists. Complete protocol at the W-station vicinity: insufficient data. Novelty is not cleared.**

| Part of Team 1's proposed use | Existing work actually supports | Spatial / methodological boundary |
|---|---|---|
| Dry overburden and an independently known ice interface | Marinova et al. (2022) locate the meteorological station at the supplied coordinate and instrument the 42 cm boundary [U1]. | Direct station-level study. This establishes earlier characterization, not blind interface-detection accuracy or current conditions. |
| Mars-analog segmented drilling and temperature control | Paulsen et al. (2011) report a 2010 University Valley field trial through dry soil into ice-cemented ground, using 10 cm sampling intervals and bit-temperature feedback [U2]. | Explicit same-use components at the named valley. Reported drill coordinates differ from W; no borehole overlap is inferred. |
| Sampling while limiting phase changes | Zacny et al. (2013) explicitly describe short sampling bites intended to prevent thawing/phase changes [U3]. | Publisher abstract supports the engineering purpose. Full paper access was restricted; this is not an exact-W experiment or a measured ice-loss curve. |
| Automated drilling and sample transfer | Glass et al. (2013) discuss University Valley among field sites and integrated operations [U4]. | Its detailed 2012 results are from Haughton; Antarctic repetition is described as planned in the Results section. Do not transfer those outcomes to W. |
| Delivery yield and sublimation-related sample handling | Steel et al.'s 2017 NASA Ames abstract uses University Valley soil in laboratory sample-delivery tests [U5]. | Prepared dry/frozen material in a chamber, not a W-station field test. Sublimation-related clogging is listed as further work, not a demonstrated completed ice-loss experiment. |

The original task is therefore partly an established experimental use of this valley. A new label or the association with I-01 does not establish a new site or first use. Conversely, the inspected literature does not prove that the full combination of blind interface detection, ground-truth depth error and a quantified sample ice-mass balance has already been executed at W. The correct result is a component-level use overlap with an unresolved complete-protocol check.

### Footprint and coordinate check

U2 reports its ice-cemented-ground drill at **77°51.891′S, 160°48.029′E**, converted to **−77.864850°, 160.800483°E**. The W anchor is **77°51.729′S, 160°42.606′E** [U1]. A spherical-Earth haversine check, **R = 6,371 km**, gives an approximate separation of **2.13 km**. This calculation uses the printed coordinates; it does not resolve their unreported datums, possible transcription issues, or field-survey accuracy.

This demonstrates that the published coordinate strings are different. It does not establish whether the earlier borehole is inside Team 1's undefined “vicinity,” nor whether a new experimental plot overlaps older work. Do not move EARTH-UV-001 to the U2 borehole or transfer the station's 42 cm interface to it. Formal footprint clearance requires Team 1 to define a plot/polygon or radius and prior studies' actual sampling extents.

### Research differences worth specifying, subject to Team 1's decision

These are proposed refinements within the supplied use, not established new methods:

1. Define the **blind detection protocol** and held-out ground truth: who predicts the boundary, which observations are withheld, and how depth errors and missed boundaries are measured. The station study is a reference dataset, not proof of this new protocol's accuracy.
2. Separate **bit temperature, recovered-sample temperature and ice mass loss**. An above-freezing limit or a subzero bit reading does not quantify retained ice. Specify initial/final ice measurements, handling time, repeatability and a closed mass balance before reporting ice-loss results. Review U3's full text and later sample-delivery work before calling this protocol novel.
3. State which unresolved **I-01 measurement requirement** the test would inform. No inspected source established a specific historical I-01 ↔ W pairing, but that bounded non-finding cannot establish novelty. Earth field results still require environmental modeling/chamber validation before any Mars performance inference.

**Team 1 action requested:** treat University Valley as a known Mars drilling/sampling analog. Decide whether to retain it as a validation/reference site with a precisely specified additional question, or propose a different candidate through Team 1's own process. Keep EARTH-UV-001 unchanged while that decision is pending. This audit does not select a replacement or certify the site unsuitable.

**Prohibited claims:** first Mars drilling analog in University Valley; previously unused dry-soil/ice-cemented site; first segmented thermal-control sampling; confirmed full-protocol novelty; previous field tests at the exact W borehole; measured ice loss or drilling performance at I-01. No number in Team 1's climate/environment extraction was reprocessed or independently validated by this literature audit.

### Earth sources and inspected scope

Search/access date: **2026-11-14, Asia/Taipei**. Source IDs U1–U5 belong to this audit; Team 1's E1/E5 labels are retained only in its own files.

| Ref | Original source | Material inspected / actual support |
|---|---|---|
| U1 | Marinova et al. (2022), [Climate and energy balance of the ground in University Valley, Antarctica](https://doi.org/10.1017/S0954102022000025) | Public full-text Introduction and Methods, meteorological measurements. Independently checked station coordinate and interface instrumentation. No claim of blind boundary testing. |
| U2 | Paulsen et al. (2011), [Field testing of the Icebreaker Mars drill in the Antarctic, LPSC 1901](https://www.lpi.usra.edu/meetings/lpsc2011/pdf/1901.pdf) | Both pages, especially the first field-test section. Explicit valley, drill location and thermal/segmented-sampling procedure. Includes a separate massive-ice trial; it is not the W plot. |
| U3 | Zacny et al. (2013), [Reaching 1 m Deep on Mars: The Icebreaker Drill](https://journals.sagepub.com/doi/10.1089/ast.2013.1038), doi:10.1089/ast.2013.1038 | Publisher abstract and contents only. Short bites and phase-change control are explicit; full text/PDF unavailable. Related to U2's hardware program, not an independent field campaign count. |
| U4 | Glass et al. (2013), [Planetary-prototype drilling and sample acquisition tests at analog sites, LPSC 1334](https://www.lpi.usra.edu/meetings/lpsc2013/pdf/1334.pdf) | Both pages, Field Test Sites and Results. Distinguishes Haughton results from planned Antarctic repetition. |
| U5 | Steel et al. (2017), **Testing A Sample Delivery System for Planetary Surface Missions**, [NASA Ames Jamboree 2017 abstract collection](https://ntrs.nasa.gov/api/citations/20200001147/downloads/20200001147.pdf?attachment=true), printed p. 92 / PDF page 93, PS.1 | Downloaded public NASA PDF and extracted this abstract locally after web-section requests timed out. Material provenance, sample handling and further-work section inspected. NTRS accession year 2020 is not the 2017 meeting year. University Valley material does not establish W provenance. |

### Earth search log and remaining scope

The following exact queries were submitted on 2026-11-14 (Asia/Taipei):

| Group | Queries | Outcome |
|---|---|---|
| Q07 | `University Valley Antarctica Icebreaker drilling ice sampling heating sublimation 2013`; `University Valley station W ice cemented soil drilling Icebreaker 42 cm` | U1/U2/U4 and the existing U3 lead. |
| Q08 | `"University Valley" "ice loss" drill`; `"University Valley" "drill" "77" "51"`; `"University Valley" "thermal" "probe" ice table drilling sample heating` | Located explicit field-drill context and further thermophysical work; no exact-W full protocol verified. |
| Q09 | `"Reaching 1 m Deep on Mars" PMC`; `"University Valley" "thermal probe" "ice" drilling`; `"University Valley" "sublimation" "Icebreaker" samples loss` | U3 publisher record and U5 laboratory-delivery precedent. |

Directly opened Team 1's U1/U3 DOI leads, U2/U4 abstracts, and U5 NASA PDF. U3 DOI/PDF requests timed out; its publisher HTML abstract was accessible. PubMed returned only a footer and supplied no usable abstract in this session. A snow/salt ice-stability lead at `PMC7430506` returned a browser check on direct access; it was not used to establish a completed sampling experiment. A separate NASA water-rich mission PDF returned 403. Search excerpts/secondary news were not used as proof of full-paper or exact-site inspection.

This is a bounded public-web review of one supplied candidate. No exhaustive ADS/Scopus search, full U3 methods/supplement review, later citation-chain review, or spatial intersection of every historical borehole was completed. The absence of a supplied vicinity polygon and a completed mass-balance protocol limits the exact-use conclusion. University Valley and Beacon Valley are related search contexts, not interchangeable experimental coordinates.

CSV schema update: four original Mars rows are retained; one Earth row is appended with `candidate_id=earth_candidate_id=EARTH-UV-001`, `mars_candidate_id=I-01`. Earth coordinates occupy the explicit `earth_lat_deg`/`earth_lon_east_deg` fields; Mars planetocentric and nominal-box fields are blank for that row. `site_level_same_use_status=same_use_exists` records the valley-level precedent, while `classification=related_research_exists` and `exact_site_same_use_status=insufficient_data` describe the unresolved W-vicinity footprint. `verified_same_use_hit_found` remains an exact-footprint flag, not the valley-level status.

## Inputs and completed checks reused

Read the current repository copies of [site_discovery_brief.md](../site_discovery_brief.md), [mars_discovery_handoff.md](../mars_discovery_handoff.md), [mars_discovery_novelty_checks.csv](../mars_discovery_novelty_checks.csv), and [mars_discovery_search_scope.json](../mars_discovery_search_scope.json). The original 15-row review already covered literal coordinate queries, regional precedents, Protonilus and InSight center distances, and the D-01/D-02 Utopia monitoring-circle overlap. Those are inherited checks, not new discoveries in this audit.

The requested filename `ice_candidate_followup_2026-11-14.md` was not found in the current checkout. The supplied `NASA_Space_Apps_2026_All_Data.xlsx` contains its apparent successor as an English rendering of **`docs/research/ice_candidate_followup/README.md`**, in `Report Text!A475:G505`, with supporting search records in `JSON Source Records!A20680:H20730`. Read all these records. They document native-grid QA, the nominal 2015 latitude/radius envelope, Luzzi et al.'s AP-1/AP-8/AP-9 checks, Protonilus ice-exposing craters, and unresolved actual proposal footprints. These checks were reused without rerunning data processing. The original Markdown is authoritative and is absent from this checkout; the workbook is a supplied snapshot, not a replacement original.

Workbook identity: snapshot `2026-11-14T15:42:59.879915+08:00` (`Overview!A4`); SHA-256 `a789fcdc9c0a7e780f85b63687ad54f05b87cd6e341ecf024375dcd6fcb3f731`. `Earth Candidates` contains 72 versioned rows: 36 for `earth_100km_sample4km` and 36 for `earth_100km_sample10km`. These are older Jezero/Gale/Arcadia results, not 72 independent new analog sites. The workbook was read only and was not copied into Git.

## Spatial interpretation

The stored Mars centers use planetocentric latitude and east-positive longitude. For the Mars audit, a **nominal cell** means center ±0.25° in both axes, inferred from the documented 0.5° grid. It is not a landing ellipse or a verified instrument footprint. The Earth anchor has separate coordinate fields and no assumed cell footprint.

| ID | Latitude bounds, degrees | East longitude bounds, degrees | Search labels, not certified site boundaries |
|---|---:|---:|---|
| I-01 | 54.00 to 54.50 | 1.00 to 1.50 | Northern plains / Vastitas Borealis; eastern Acidalia context; Ismenius Lacus context |
| I-02 | 53.50 to 54.00 | 42.00 to 42.50 | Northern plains / Ismenius Lacus; Lyot, Protonilus and Deuteronilus regional terms |
| D-03 | -46.50 to -46.00 | 82.50 to 83.00 | Eastern Hellas Planitia / basin floor and rim |
| D-04 | 7.50 to 8.00 | 154.00 to 154.50 | Elysium Planitia / Cerberus plains and classical Cerberus albedo feature |

Slope/relief cell support, interpolated SWIM support, and the dust layer's native 3° support are different. In particular, a dust study outside a nominal 0.5° cell may still overlap the broader atmospheric context. No native dust-contribution polygon was reconstructed here. No complete GIS overlay of study/ROI/landing polygons was completed.

Center distances below are geometric calculations, using a Mars sphere of radius **3,396 km** and the haversine formula `2R atan2(sqrt(a), sqrt(1-a))`, where `a = sin²(Δlat/2) + cos(lat1) cos(lat2) sin²(Δlon/2)`. They are rounded context checks; source datum differences were not rigorously transformed. They cannot exclude uninspected alternative sites or extended ROIs.

## Candidate findings

### I-01: 54.25°N, 1.25°E

- **Already observed/studied:** SWIM's published 2019 reconnaissance domain includes this sector [N1]. This establishes prior ice-resource mapping context, not a local independent ice detection. Reusing its product does not make this a newly discovered ice deposit.
- **Proposal check:** the inspected Deuteronilus exploration zone explicitly combines science and ice-resource use [N2]. Its center, 39.11°N, 23.199°E, is approximately **1,255.5 km** away; the stated primary circle has a 100 km radius. Its alternative EZs in Figure 2 were not digitized. The inherited Protonilus separation is approximately 1,939.6 km [N3].
- **Scope correction:** Orgel et al.'s Acidalia geomorphological survey is a 300 km strip centered on **22.5°W**, extending 20°N to 84°N [N4]. That regional citation does not establish imagery interpretation or ice landforms at 1.25°E. No local landform was assigned from it.
- **Possible research difference:** compare follow-up observations needed here with I-02, where the existing descriptors show similar ice consistency and slope but different TI. A documented comparison of missing evidence could add value. This is a proposed question, not a novelty finding or extraction-performance result.
- **Cannot claim:** first ice-resource proposal, an unstudied area, confirmed shallow ice, extractable water, or a suitable crewed base. The inherited nominal 2015 envelope exclusion also reflects historical latitude constraints [N5].

### I-02: 53.75°N, 42.25°E

- **Already observed/studied:** the same published SWIM reconnaissance domain applies [N1]. The specific candidate selection is a project interpretation of an existing reconnaissance product.
- **Proposal check:** the already reviewed Protonilus proposal is at **42.187°N, 48.062°E**, approximately **722.5 km** away, with resources/ROIs described around its habitation zone [N3]. The newly inspected primary Deuteronilus circle is approximately **1,158.2 km** away [N2]. These named proposals are not this nominal cell. Their existence establishes a related ice-resource use in the wider region, not exact duplication.
- **Remaining uncertainty:** no complete set of alternative Deuteronilus sites, later prospecting proposals or their actual ROI polygons was obtained. Nearby Lyot/Ismenius search terms did not establish an exact same-use proposal. The already checked Protonilus ice-exposing craters remain separate observations, not measurements at I-02.
- **Possible research difference:** test which observation would resolve the ambiguity between surface thermophysical context and the inferred subsurface ice resource at this specific cell, using I-01 as a comparison. Any Earth experiment must wait for Team 1's explicit pairing and use.
- **Cannot claim:** the Protonilus EZ, a validated alternative to it, first ice-prospecting site, independent confirmation from multiple SWIM depth maps, or demonstrated lower drilling cost.

### D-03: 46.25°S, 82.75°E

- **Already studied:** the USGS SIM 3096 publication record describes mapping of **37.5°S to 47.5°S, 270°W to 280°W** [N6], equivalent to 80°E to 90°E. The nominal candidate box is numerically inside that published extent. This is geological mapping coverage, not a dust-test recommendation. The full sheet/pamphlet could not be retrieved, so no unit or landform was assigned to this cell. Astropedia's indexed geometry appears to show only one northern quadrangle; it was not substituted for the publication's four-quadrangle extent.
- **Dust footprint check:** Szwast et al.'s Hellas dust/albedo ROI is **31°S to 53°S, 54°E to 82°E** [N7, §5.3/Figure 9]. The nominal cell begins at 82.5°E and is outside that particular ROI, despite sharing the basin name. The coarser atmospheric support may overlap; its seasonal result was not transferred to D-03.
- **Proposal check:** Rice et al.'s eastern Hellas human-exploration proposal has a **200 km diameter** zone near **40°S, 104°E**, approximately **987.3 km** away [N8]. Its purpose includes geological/ice-resource exploration, not an equipment dust-tolerance test at D-03.
- **Possible research difference:** define this eastern-basin cell as an explicit contrast in a seasonal dust-column/terrain comparison, then check the difference against local transport observations. Neither such a result nor an unclaimed prior use is established yet.
- **Cannot claim:** unstudied Hellas terrain, a new dust source/hotspot, locally measured deposition/abrasion, equipment suitability, or a safe operating surface.

### D-04: 7.75°N, 154.25°E

- **Already studied:** Geissler [N9, §4.4] examines dust deposition/erosion in classical Cerberus around **10°N, 205°W = 155°E**, approximately **140.4 km** from D-04. The study covers an extended feature, not just that center; a center mismatch cannot exclude overlap. Its actual changed-surface polygon was not obtained.
- **Closely related research purpose:** the 2018 Elysium study [N10] proposes relating dust sources/sinks to terrain types using thermal-image differences. Thus, comparing dust and terrain in Elysium already has methodological precedent. Its exact image/ROI overlap with D-04 remains unverified. This is an abstract describing work and next steps, not a completed validation of D-04.
- **Further prior work:** Wolfe et al. [N11] combine diurnal EMIRS temperatures and modeling to constrain dust redistribution over an Elysium ROI. The inspected text/Figure 2 caption does not provide a usable numeric D-04 polygon. None of its regional dust-thickness estimates is assigned to this point.
- **Operations-footprint check:** Yao et al.'s Tianwen-1 monitoring circle is centered at **17°N, 107°E**, radius **2,000 km** [N12]. D-04 is approximately **2,782.8 km** away, so its nominal cell is outside that circle. This excludes only that monitoring footprint, not all Elysium operations studies. The earlier InSight site separation is inherited from the handoff; its observations are not ground truth here.
- **Possible research difference:** explicitly separate atmospheric column dust from surface dust transport for this candidate and compare their seasonal behavior. That physical distinction is established in prior work; a contribution would require a new, reproducible candidate-specific result.
- **Cannot claim:** first dust/terrain study, newly discovered dusty region, InSight-validated conditions here, or proved absence of prior operational interest.

## Sources and what was actually inspected

All access/search dates below are 2026-11-14 (Asia/Taipei). References identify author research or official records, not agency endorsement of these candidates. Broadly relevant works found in search results were not treated as exact-site evidence.

| Ref | Source | Inspected material and supported scope |
|---|---|---|
| N1 | Putzig, Morgan & SWIM team (2022), [LPSC abstract 2443](https://www.hou.usra.edu/meetings/lpsc2022/pdf/2443.pdf) | Two-page abstract, Introduction/Motivation. Stated 2019 domain: 0 to 60°N and 0 to 225°E, 290 to 360°E; resource reconnaissance supports future missions. Domain membership is not local detection or a selected landed site. |
| N2 | Head et al. (2015), [Deuteronilus EZ, abstract 1033](https://www.hou.usra.edu/meetings/explorationzone2015/pdf/1033.pdf) | Both pages, primary EZ center and Figure 1 radius. Same broad resource purpose at a separate primary zone; Figure 2 alternatives remain unresolved. |
| N3 | Gallegos & Newsom (2015), [Protonilus EZ, abstract 1053](https://www.hou.usra.edu/meetings/explorationzone2015/pdf/1053.pdf) | Existing checked lead reopened for spatial comparison; both pages, proposed center and ROI discussion. No claim that its resources extend to either ice candidate. |
| N4 | Orgel et al. (2019), [doi:10.1029/2018JE005664](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2018JE005664) | §2.1 study-area definition. Narrows the geographic relevance of an inherited Acidalia citation. |
| N5 | Hoffman & Bussey (2016), [NASA NTRS 20160001040](https://ntrs.nasa.gov/citations/20160001040) | Official abstract reopened; full-paper nominal-envelope analysis inherited from the supplied follow-up. 47 workshop proposals, ±50° criterion and approximately 100 km EZ definition do not constitute a complete modern site inventory. |
| N6 | Bleamaster & Crown (2010), [USGS SIM 3096](https://doi.org/10.3133/sim3096), [publication record](https://pubs.usgs.gov/publication/sim3096), [Astropedia record](https://astrogeology.usgs.gov/search/map/mars_geologic_map_of_mtm_40277_45277_40272_and_45272_quadrangles_eastern_hellas_planitia_region) | Indexed official publication abstract/metadata returned the full stated extent and 1:1,000,000 map scale. Direct pages and attempted pamphlet access returned 403. Extent comparison only; full map and coordinate-reference details unverified. |
| N7 | Szwast, Richardson & Vasavada (2006), [doi:10.1029/2005JE002485](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2005JE002485) | Full-text abstract and Hellas §5.3/Figure 9 text. Explicit ROI bounds enable a nominal-box exclusion; basin-wide phenomena are not cell measurements. |
| N8 | Rice et al. (2015), [Eastern Hellas EZ, abstract 1038](https://www.hou.usra.edu/meetings/explorationzone2015/pdf/1038.pdf) | Entire one-page abstract; center, diameter and resource purpose. Regional proposal at a different location. |
| N9 | Geissler (2005), [doi:10.1029/2004JE002345](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2004JE002345) | §4.4/Figure 9 caption. Cerberus surface-change research near D-04; no digitized deposit or image polygon. |
| N10 | Kozdon et al. (2018), [LPSC abstract 2514](https://www.hou.usra.edu/meetings/lpsc2018/pdf/2514.pdf) | Both pages: Elysium ROI rationale, methods and proposed follow-up. Direct regional precedent for dust/terrain comparison; no numeric local polygon validated. |
| N11 | Wolfe et al. (2023), [doi:10.1029/2023JE007794](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023JE007794) | Abstract, §§2.2, 3.1, 4.1, Figure 2 caption and data-availability statement. Regional dust/thermal work, with uncertainties permitting zero net change. Exact D-04 support remains unchecked; original EMIRS products were not downloaded. |
| N12 | Yao et al. (2020), [doi:10.1029/2020EA001242](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020EA001242) | Figure 1 caption and §2.2: numeric monitoring circle, distinct from preferred landing areas. |

## Search log

Public-web search, 2026-11-14 (Asia/Taipei). Queries are grouped below but each string was submitted separately. Search output was screened for original papers, NASA/USGS records and formal abstracts. Commercial hits, games, Wikipedia, fictional Ares III material and unsupported aggregation pages were excluded. A failed literal query is not evidence of absence.

| Group | Candidate / purpose | Exact submitted queries |
|---|---|---|
| Q01 | I-01 and northern-plains resources | `Mars "54" "1" Acidalia ice exploration zone landing site`; `site:hou.usra.edu explorationzone2015 "Acidalia"`; `Mars "54" "0" "ice" landing site Acidalia`; `site:hou.usra.edu/meetings/explorationzone2015 "Acidalia" ice`; `Mars ice "Acidalia" "0" "55"`; `Mars Acidalia eastern northern plains ice ISRU landing exploration zone Cydnus`; `"54" "1" "ice" "Acidalia" ISRU`; `"Acidalia" "ice" "landing" "site" -site:wikipedia.org -site:researchgate.net` |
| Q02 | I-02 and regional ice proposals | `Mars "53" "42" ice exploration site Deuteronilus Protonilus`; `site:hou.usra.edu explorationzone2015 "ice" "Deuteronilus"`; `Mars "53.75" "42.25"`; `Mars "54" "42" "ice" Vastitas`; `Mars Lyot northern plains ice prospecting Ismenius human landing site`; `site:hou.usra.edu "Ismenius" "ice" "exploration"`; `"53" "42" "ice" "Mars" landing`; `"Ismenius" "ice" "landing" site:hou.usra.edu` |
| Q03 | Ice-method / proposal leads | `"Mars Water Ice Prospecting" "pdf" NASA`; `"Subsurface water ice mapping" "0" "60" "2021"` |
| Q04 | D-03, Hellas | `Mars Hellas "82" dust storms landing site`; `"Hellas" "explorationzone2015"`; `"Mars" "82.75" dust`; `Hellas basin dust monitoring terrain landing site study eastern floor`; `"Geologic map" "Eastern Hellas" "37.5" "47.5"`; `"Hellas" "dust" "46" "83" study`; `"Hellas" "dust" "82" "46" Mars operations` |
| Q05 | D-04, Elysium/Cerberus | `Mars "154" "8" Elysium dust landing site`; `"Elysium" "explorationzone2015"`; `"Mars" "154.25" dust`; `Elysium Cerberus plains dust monitoring deposition study landing site 150 east`; `"Elysium" "dust" "154" study` |
| Q06 | Explicit surrounding-area queries | `Mars northern plains Vastitas Borealis eastern Acidalia shallow ice prospecting site 50 60 north 0 10 east`; `Mars Lyot Ismenius Lacus northern plains 50 60 north 40 east ice resource landing proposal`; `Mars eastern Hellas Planitia dust column terrain operations 40 50 south 80 90 east site`; `Mars Cerberus Elysium Planitia 5 10 north 150 160 east dust monitoring operations proposal` |

Q01/Q02 returned regional leads, including N1/N2/N4 and a 2025 Acidalia rampart-crater abstract; no exact same-use site was verified. Q03 returned Phlegra-focused prospecting reports and SWIM; Phlegra reports were screened as different-region leads and were not used to assign a site overlap. Q04 returned N6/N7/N8. Q05/Q06 returned N9/N10/N11/N12. Literal coordinate results were often unrelated numerical matches. The source table records what was inspected beyond search output.

Additional bounded source inspection: Deuteronilus 1033, Protonilus 1053, Eastern Hellas 1038, Ismenius Cavus 1027 and Apollinaris Sulci 1043 abstracts were opened. The latter two did not establish overlap with these candidates. LPSC 2025 abstract 2282 was inspected as regional cryosphere research; its individual crater polygons were not checked. The 2024 Tianwen-3 paper `10.1029/2024EA003634` was reopened as a dust-operations precedent; no new exact candidate overlap was established. SWIM pilot and northern-hemisphere product pages were reviewed for domain context, without treating different releases as interchangeable. No complete workshop abstract inventory, ADS/Scopus search, non-English review, instrument-image catalog search or systematic citation chaining was performed.

Access limitations: the 2015 program page could not be retrieved; USGS SIM 3096 and Astropedia direct access returned 403; the 2011 USGS mapping abstract-volume request timed out; a NASA-hosted Cerberus landing abstract request timed out; a Hellas dust-dynamics publisher page returned 403. The USGS mirror of Geissler failed, but publisher full text was accessible. Wolfe publisher access initially failed and succeeded on retry. These failures were not interpreted as absent prior work. No conclusions depend on inaccessible full-map units or unseen supplements.

## Remaining work and handoff checklist

- [x] Reuse the prior 15-point review and supplied ice follow-up instead of presenting them as new work.
- [x] Check all four fixed Mars IDs with regional names, surrounding-area terms and use keywords.
- [x] Separate observations, regional research and explicit site proposals; record source scope and access failures.
- [x] Record nominal boxes and bounded spatial comparisons; no novelty clearance from center mismatch.
- [ ] Obtain actual alternative EZ/ROI, changed-surface and EMIRS ROI geometry where overlap is unresolved. Normalize coordinate conventions before formal intersections.
- [ ] Complete a broader modern same-use proposal inventory before any first-use or understudied claim.
- [ ] Team 1 to evaluate the regional purpose precedents, particularly the Elysium dust/terrain precedent. No exact duplicate requiring automatic replacement is established; keep/change decisions belong to Team 1.
- [x] Read Team 1's first candidate from its uploaded branch and audit EARTH-UV-001 under its original ID, coordinates and purpose.
- [ ] **Team 1 decision pending:** University Valley has existing drilling/segmented thermal-control use. Retain as a known reference with a precise additional protocol, or revise through Team 1's process. W-vicinity bounds and exact full-protocol overlap remain unresolved.
- [ ] **Waiting for Team 1 additions:** Earth candidates for I-02, D-03 and D-04 in `outputs/research/team1_earth_analog_candidates.csv`. Require fixed IDs, coordinates, footprints, intended tests and original evidence links.

Companion machine-readable file: [team2_novelty_audit.csv](../../outputs/research/team2_novelty_audit.csv), four Mars records and one Earth record. `novelty_cleared=false` is a research status, not a rejection of the candidate's future usefulness.

Verification: the original four Mars IDs/coordinates were checked against the repository novelty CSV and supplied workbook. Phase 2 checks cover the appended Earth record against the pinned Team 1 CSV, exact preservation of its purpose text, distinct Earth/Mars coordinate fields, unchanged prior Mars findings, CSV structure, source-reference completeness and local report links. Numeric distances were independently calculated as described above. Only the two Team 2 deliverables were written. No `analog/`, ranking, Team 1 file, total workbook, README or website change was made. OpenAI Codex assisted literature screening, geometric context calculations and reporting; every external scientific claim is tied to the inspected source scope above.
