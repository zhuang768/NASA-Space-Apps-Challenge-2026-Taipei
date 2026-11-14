# MS-03 完整研究交付與本輪重現入口

閱讀[目前報告](../../../../docs/research/MS-03/report.md)、[逐條驗收](requirement_audit.csv)、[完整檔案清單](file_inventory.csv)及[科學未解問題](open_questions.csv)。原研究要求明文允許資料不足時記為未知；本交付沒有把文件完成等同所有科學問題已解決。

本輪把原先分散的 MOC、CRISM、MRDR、SHARAD及目錄查核接回主報告與機讀證據，更新兩候選取得狀態與先例。W仍是已知界面／資料QA參照，AD1仍是一般幾何方法參照，沒有升為成功火星配對。

## 新增可重現資料

- [W五指標摘要](earth_atmosphere_summary.csv)、[55列月表](earth_atmosphere_monthly.csv)：同一作者處理短檔中，2010-01-01至2010-12-01（不含）的16,032列、11個完整月。沒有12月，不稱全年，不配HOBO或長版時標。
- [W無損保留原件與來源](earth_raw/README.md)：CC0作者處理匯出，gzip解壓後與固定Zenodo原bytes的SHA256／MD5一致；不是未處理logger。
- [兩候選四面向表](earth_four_dimensions.csv)、[新先例引文](earth_new_prior_citation.json)：2026文章與同W資料用途直接重疊；原來源曾用於身份追溯，本輪擴大查核實際用途，沒有主張首次發現文獻。
- [雷達峰值診斷](radar_diagnostics/README.md)：65個格內中心；crop argmax有大跳動，沒有依據直接當地下反射層；採樣間距與頻寬理論尺度分開。無功率相減、校時或冰深反演。
- [全部搜尋紀錄入口](search_log_index.csv)、[保留逐列搜尋紀錄](all_search_records.csv)：保存來源表、行號、原ID與完整JSON；重複記錄有標記，總列數不是獨立搜尋或成功請求數。
- [來源對照](source_crosswalk.csv)、[原研究要求](original_research_instructions.txt)、[固定共同輸入](shared_input_verification.json)。共同Excel與186份歷史補充已由原還原程式核驗；舊配對僅作背景。

## 從專案根目錄重現

Python標準庫足以重現W與交付索引；雷達分析另需NumPy，重畫圖另需Matplotlib。

```bash
python3 outputs/research/MS-03/completion_20261115/earth_atmosphere.py
python3 outputs/research/MS-03/completion_20261115/earth_validate.py
python3 outputs/research/MS-03/completion_20261115/radar_diagnostics/analyze.py
python3 outputs/research/MS-03/completion_20261115/build_delivery_index.py . --strict
```

`integrate_earth.py`與`integrate_local_evidence.py`用唯一ID更新原表，沒有改動原始觀測陣列。`refresh_parent_manifest.py`保存歷史manifest、固定共同輸入並更新頂層入口。索引程式只驗證資料關係、來源身份、實際bytes及文件路徑；不校準科學檢出能力。既有其他子套件的驗證仍以各自明列範圍為準。

完整原始大檔並非全部隨本輪重複附上。既有Git檔案均保留在固定來源樹；本次未能從連線下載的檔案明列`remote_tree_reference_only`，其繼承SHA256不標為重算。乾淨Git clone可取得既有已提交檔案；未公開logger、執行係數及未取原表則仍是真正缺件。

## 發布與完成界線

[發布收據](publication_receipt.json)在發布後記錄實際分支、資料commit、PR與讀回結果；離線驗證內`not_verified_by_offline_builder`只表示程式不連GitHub。頂層manifest與收據排除自身雜湊循環，理由逐項列明。

目前仍不能證實本地冰存在／深度／含量、可比較的Mars閉合多邊形、精確光譜執行歸因、跨logger同步或全球新穎性。下一個可執行程序及禁止的推論在報告與未解表中，沒有用0、任意位移或擬合代替未知。
