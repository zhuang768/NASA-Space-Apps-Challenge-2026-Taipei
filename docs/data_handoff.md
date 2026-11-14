# 資料交接

## 本輪實際取得的檔案

本輪可交接的是 ETOPO 2022 地球地形、MOLA 火星地形、Natural Earth 陸地遮罩，以及 NASA POWER 氣候 JSON，約 480 MB 原始資料。資料包不含帳號、密碼、token、`.netrc` 或 `.env`。

下載附件位於專案的 `terrain-inputs-2026-11-14` Release。依使用者指示，分析結果、程式與文件修正改為直接整合至 `main`，原草稿 PR #1 已關閉；Release 附件內容與校驗碼保持不變。

```bash
# 從 repo 根目錄執行，使用自己的 GitHub 登入存取私人 repo
mkdir -p data/downloads
gh release download terrain-inputs-2026-11-14 --repo zhuang768/NASA-Space-Apps-Challenge-2026-Taipei --dir data/downloads
cd data/downloads
shasum -a 256 -c SHA256SUMS.txt
cd ../..
mkdir -p data/raw
tar -xzf data/downloads/spaceapps-terrain-inputs-2026-11-14.tar.gz -C data/raw
```

資料包頂層為 `earth/` 與 `mars/`，解壓後對應管線使用的 `data/raw/earth/` 與 `data/raw/mars/`。若既有同名檔，請先比對 SHA-256，再決定是否解壓覆寫。來源與原始檔校驗碼在資料包的 `earth/public_sources.json` 及 repo `outputs/analysis/results.json`；資料包校驗碼另在 Release 的 `SHA256SUMS.txt`。

`earth/power/` 包含六個候選的月氣候資料，另含一筆 33°N, 87°E 的連線檢查資料；連線檢查未進入排名。地形原始檔只提供資料取得依據；候選仍是未驗證的區域地形候選。

## GitHub 文件提到的另外一批資料

主分支 `d9d121b` 的 `docs/earth_data_plan.md` 與 `docs/cross_reference.md` 記載隊友已下載約 7.6 GB 地球資料：SRTMGL30、MOD11C3、GPM_3IMERGM、GLDAS_NOAH025_M、MOD13C2、M2TMNXAER，另列 ESA CCI Permafrost。這是隊友文件的說明，尚未由本輪原始檔查驗。

2026-11-14 本輪檢查當時的主分支完整檔案樹、分支清單、Releases、Actions artifacts 及 Issue/PR，尚未找到那批原始檔或附件連結。文件明確註記 `data/raw/earth/` 不進 Git，因此 `git pull` 只會取得清單與規格，不會取得另外 7.6 GB。

若隊友的原始檔尚在其電腦，需另外提供可存取的資料包或儲存位置，再核對檔名、數量、SHA-256、期間、版本與 QA。這個 Release 沒有包含尚未取得的那批檔案，也沒有聲稱已完成它們的四面向分析。

## 本輪作業方式

依使用者最新指示，本次上傳與整合沒有使用 C2C。既有報告保留前一輪曾嘗試但未成功的審查紀錄。
