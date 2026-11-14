# 合併就緒檢查

驗收日 2026-11-15（Asia/Taipei）。本檔只記錄事實與建議，**未改任何 PR 的 base、未合併、未帶入無關檔案**。

## 1. 基底與關係

| PR | base | head（完整 SHA） | GitHub mergeable | 備註 |
|---|---|---|---|---|
| #8 MS-01 | `main` (`3cc8488577535e2fa4d146021fde51f8ff6cc667`) | `b4b6929e890018668ef4faa9a74128a4ce5aa8df` | true／unstable | 51 檔、+13,244／−0 |
| #6 MS-02 | **`handoff/verified-data-20261114`** (`f7076c9fdc77e00244ed5d6863aad2bf78cfa28f`) | `38b8fa0dea527b1cc47aeb02dc260e039da37122` | true／unstable | 15 檔、+1,737／−0 |
| #7 MS-03 | `main` | `8fa07afac4a98096958880f6a5ece16f35abc4db` | true／clean | 95 檔、+29,909／−0（相對 main，head 前進後仍是此數） |

`unstable`＝非必要檢查未通過。三個 PR **與 main 和 handoff 本身**的 `Workers Builds: nasa-space-apps-challenge-2026-taipei` 皆為 failure，故不是這幾個 PR 造成；原因屬部署設定，本輪未調查。

**PR #6 與 main 的關係：** handoff 分支相對 main **只多 2 個新增檔**：`outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx` 與 `outputs/research/mars_reselection_20261114/screened_pool.csv.gz`；main 不含它們。handoff 分支目前**沒有**對 main 的 PR（開放 PR 為 #1、#2、#5、#6、#7、#8）。因此 PR #6 合併後，內容只進 handoff，**不會自動進 main**。

## 2. 路徑與重疊

- 每個 PR 的檔案全為「新增」，且都在自己的目錄：`docs/research/MS-0x/`、`outputs/research/MS-0x/`、（MS-01 另有 `outputs/research/MS-01/` 內腳本；MS-02 `scripts/research/ms02_earth_analogs/`；MS-03 `scripts/research/MS-03/`）。
- 三者兩兩**無共同路徑**；與 handoff 的 2 個檔也無重疊。（`audit_checks.py` F-paths／F-overlap）
- 大小（相對 main 新增的 git blob 位元組）：MS-01 約 1.6 MB；MS-02 約 31.5 MB（為相對 main 新增的 blob 總量，17 檔＝PR 自身 15 檔＋handoff 2 檔（xlsx 與篩選池））；MS-03 約 7.7 MB（含 `polygons_Act-IWS_source.zip`、`duplicate_source_labels.zip`）。

## 3. 整合相依

1. **PR #6 需要 handoff 的兩個檔**：`verify_ms02.py` 與 MS-02 manifest 引用 xlsx 與 `screened_pool.csv.gz`。在 main 單獨執行會失敗（已在 PR #6 head 自帶 handoff 的 worktree 內通過）。
2. **MS-03 manifest** 同樣列出這 2 個路徑，驗證時標為「不在 repo」；這兩項要等 handoff 進 main 才能全部核對。
3. 三份報告引用 `outputs/research/mars_reselection_20261114/` 的共用檔，這些已在 main，無相依問題。
4. 合併順序沒有路徑衝突；但**內容層面**請見下節。

## 4. 建議順序（供決定者參考，本審查未執行）

1. 先決定 handoff 的去向：若要讓 PR #6 的驗證在 main 可重跑，需要先把 handoff 的 2 個檔帶進 main（另開 PR，由資料負責人決定），或在 PR #6 描述寫明依賴。**本審查不更改 PR #6 的 base。**
2. PR #7、PR #8 各自對 main，可任意順序合併（無重疊）。
3. 合併前須先處理審查報告 §7 的「阻擋引用」句：C37（MS-03 報告後段舊文）屬於文件內容，需 MS-03 作者在其報告修正或加醒目標註；本審查**未修改他人檔案**。
4. 合併前建議 MS-01 作者補 Campbell 時標偏移句（C07），MS-02 作者清理 H2／H3／比較表中的 E03 殘留（C24）。

## 5. 授權與署名

MS-03 帶入第三方檔（PANGAEA 921087 的 Act-IWS 多邊形 zip、HiRISE PDS 標籤、Ulrich 等 2011 的讀取記錄）。其 README 載明來源與授權；合併或轉用圖表時須保留署名。MS-02 的 PANGAEA 數值檔未下載（403）。本審查未做法律授權判斷。

## 6. 未能驗證

- Workers Builds 失敗原因。
- 三個 PR 在「合併到 main 之後」的整合建置（未做合併試驗，也不合併 main 到審查分支）。
- 授權文字的法律效力。
