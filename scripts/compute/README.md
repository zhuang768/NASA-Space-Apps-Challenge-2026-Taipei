# 候選資料抽取與 QA

統一入口：`pipeline.py --candidate-id ID`。候選 ID、座標與用途由 Team1 CSV 提供；資料產品／來源、格式、觀測期間、變數與座標綁定由 `source_profiles.json` 提供。科學用途、新穎性與候選保留決定仍由對應負責人維護。

## 執行

在專案根目錄執行，Python 3.11 以上：

```sh
python3 -m venv /tmp/zasa-compute-venv
/tmp/zasa-compute-venv/bin/python -m pip install -r scripts/compute/requirements.txt
/tmp/zasa-compute-venv/bin/python scripts/compute/download_inputs.py --source-id EH2-2019-PUBLISHED-SUPPLEMENT
/tmp/zasa-compute-venv/bin/python scripts/compute/download_inputs.py --source-id UV-W-CAMPBELL-2009-2010
MPLCONFIGDIR=/tmp/zasa-compute-mpl /tmp/zasa-compute-venv/bin/python scripts/compute/pipeline.py --candidate-id EARTH-002
MPLCONFIGDIR=/tmp/zasa-compute-mpl /tmp/zasa-compute-venv/bin/python scripts/compute/pipeline.py --candidate-id EARTH-UV-001
/tmp/zasa-compute-venv/bin/python -m unittest discover -s scripts/compute -p 'test_*.py' -v
```

原始資料不加入 Git。若一般 HTTP 下載遇到來源站限制，程式會停止；可從官方網址正常下載，再用以下指令核對原始位元組，不匯入 HTML 錯誤頁或複製網頁數字：

```sh
/tmp/zasa-compute-venv/bin/python scripts/compute/download_inputs.py --source-id UV-W-CAMPBELL-2009-2010 --import-file /absolute/path/to/UniversityV_09_10_Campbell_data_good_only_calibrated.txt
```

所有輸入／輸出路徑預設相對於程式所在專案根目錄，支援 `--root`、`--candidates`、`--profiles`、`--output`。在 AUP 必須先用 `pwd` 找到實際根目錄，不能貼 Mac 路徑。

```sh
python3 scripts/compute/inventory.py --root /actual/project/root --output /actual/project/root/outputs/compute/runtime/inventory.json
```

## 輸入契約

Team1 原欄全部保留，包括研究版本不一致的原值。轉接層僅增加下列別名：

| 契約欄位 | Team1 原欄 |
|---|---|
| earth_candidate_id / mars_candidate_id | 同名，必填且 Earth ID 不重複 |
| site_name | earth_site_name |
| latitude_deg | earth_lat_deg；北正南負 |
| longitude_east_deg | earth_lon_east_deg；東正西負，保留原值 |
| anchor_description | coordinate_basis |
| intended_test | test_purpose |
| evidence_sources | source_urls |
| 需求版本／日期 | requirements_version；無此欄時至少有 review_date |

`site_extent_type`、`site_extent_description`、datum 等原欄也保留。僅有站點座標時必須標示 point anchor；不生成任意半徑、試驗區或新鑽孔。候選與來源的 Earth/Mars ID、經緯度都須相符，不能把 W 站序列搬給別的座標。

下一個候選以新的 CSV 列與來源 profile 接入，不修改核心抽取程式。已測試不同 ID、座標及原自訂欄保留。現有 adapter 支援 Campbell TOA5 與此次 EH2 PDF；其他產品不能僅改 ID 就假裝支援，需有官方定義、實際檔案及專屬格式轉接。EARTH-003 未啟用。

## QA 與處理邊界

- W：原檔 MD5；TOA5 20 欄與單位；兩種時間字串格式；decimal day 與日期交叉核對；半小時格；重複／衝突；NaN 與儀器範圍遮罩。資料已由作者校準，使用 identity scale/offset，不二次校準。無可恢復的原始 QA bit 或作者刪除紀錄。
- EH：沿用 Team2 `bc9fe3c0` 的列號＋雙日期＋6/9 數值正則與欄位次序。新匯出保留 source_page、source_page_row、source_text_line、published_row_id。採出版表中 degC／% 值，不再次套用 RH 修正。
- EH 每頁首／中／末以 PDFium 檢查 pypdf 匯出，共 324 筆，兩時標和數值一致；沿用 Team2 已完成的全 8922 筆雙引擎 QA，明確保留歸屬。另視覺檢查原 PDF 第 1／54／108 頁。
- 完整月／部分月／無有效資料分開報，observed_mean 僅描述現有觀測；不插補、沒有適合度門檻。W 不算全年統計；EH 不算 3 cm 全年統計。
- 深度差只用同列共同有效溫度相減；3 cm 是地下土溫。地面探針不是衛星 LST、氣溫或 TES 熱慣量；不能用溫差反推冰深／TI／取樣冰損失。
- 所有日期均維持來源原時標。W 的 UTC offset 不明；EH 保留 `Time, GMT-07:00`、`Local Time GMT-5:30`，相差 90 分鐘不能自行解釋為已核實 UTC／太陽時。
- EH 修正 RH >100% 原值保留並標記，不裁切、不用它自動產生水活性／宜居性判定。每小時 N 不是獨立樣本數，不產生虛構信賴區間。

每次執行的 `qa_report.json` 記錄來源／候選 CSV／profile／程式 SHA-256、套件、數值精度及計時。CPU 單次計時不代表 GPU 加速；無 GPU 運算或比較時 speedup 為 null。

結果、來源清單、現存缺口與研究主線對照見 [outputs/compute/README.md](../../outputs/compute/README.md)。
