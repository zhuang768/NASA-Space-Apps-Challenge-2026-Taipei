# 最終輪證據與主張驗收報告

Team zasa｜NASA Space Apps 2026｜驗收日期 2026-11-15（Asia/Taipei）｜本報告只核對，不開新研究、不新增網站、不修改他人檔案。

## 1. 驗收對象（完整 SHA）

| 項目 | PR／分支 | 驗收時 head（完整 SHA） | 備註 |
|---|---|---|---|
| MS-01 | PR #8 | `b4b6929e890018668ef4faa9a74128a4ce5aa8df` | 與任務所列相同 |
| MS-02 | PR #6（base=`handoff/verified-data-20261114`） | `38b8fa0dea527b1cc47aeb02dc260e039da37122` | 與任務所列相同 |
| MS-03 | PR #7 | `8fa07afac4a98096958880f6a5ece16f35abc4db` | **任務所列為 `3321765d…`；PR 已前進 2 個 commit**（`8f6d3134`、`8fa07afa`，2026-11-14T17:39Z／17:44Z，即台北 11-15 01:39／01:44）。依「以遠端最新為準」改驗新 head，新增內容已逐項納入（§6） |
| main | `main` | `3cc8488577535e2fa4d146021fde51f8ff6cc667` | 未變 |
| handoff | `handoff/verified-data-20261114` | `f7076c9fdc77e00244ed5d6863aad2bf78cfa28f` | 未變 |

三個 head 均用 `git ls-remote` 與 `gh api` 兩種方式確認；每個 head 以 read-only worktree 取出核對。

## 2. 結論摘要

- **自動化核對**：`audit_checks.py` 共 25 項 PASS、0 項 FAIL、4 項 INFO（錨點距離、處置傾印、檔案大小、措辭掃描；INFO 為記錄，不是通過宣告）。
- **既有驗證器重跑**：4 個重跑結果為 exit 0（MS-01 `validate_deliverables.py`、MS-02 `verify_ms02.py`、MS-03 `validate.py`、MS-03 `validate_morphology.py`）；1 個**無法重跑**（MS-01 `thermal_followup/validate.py`），見 §5。**這 4 個 exit 0 只代表各組自己的結構與重現檢查通過，不是科學結論的 PASS。**
- **主張台帳**：`outputs/integration/audit/claim_ledger.csv` 共 49 列：可引用 6、可引用但須帶已明列限制 29、需要修正文句 7、阻擋引用 7。
- **沒有發現**：三份報告的火星數值與主 repo 共用資料不一致、manifest 雜湊不符、跨 PR 路徑重疊、或把 SWIM／熱慣量／衰減寫成冰量或唯一冰訊號的未否定語句（掃描為啟發式，僅供輔助，已逐條人工覆核）。

## 3. 通過項目（實際重算）

1. **座標與格尺寸**：以 Mars 半徑 3,396,000 m 重算三點格尺寸（29.64×16.25／17.94／15.81 km），與報告印出值一致；MS-03 的 242.25°E 與 −117.75° 互換一致。
2. **數值**：三份報告引用的 35 個數值（MOLA、TES、SWIM、CDOD、MCS）與主 repo 的 `final_candidates.csv` 及 `candidate_native_evidence.json` 一致；原生檔與 final 表彼此一致；有效格數／bin 數（73/100、93/100、79/100；161/145/69、75/288、171/148/60）一致。
3. **距離**：MS-02 的 MCS bin 距格 146.7 km、塵格 17.3 km，重算一致（這是已明列限制，見 §4）。
4. **University Valley W 站座標**：DMS 轉十進位 −77.86215、160.7101 一致。
5. **Adventdalen 錨點**：ADE、CS-1、AD1 三處錨點兩兩距離重算（ADE–CS-1 5.97 km；AD1 與 ADE 約 3.5–3.6 km；AD1 與 CS-1 約 2.5 km；AD1 GIS 外包框中心經 UTM33N 逆算，與事件起點相差 0.34 km）。ADE 在 MS-02 所引 PANGAEA 八場址外包框南側約 1.1 km 處。
6. **MS-01 獨立重算**：以 numpy 對 PR #8 已入庫的分析窗紀錄（`primary_temperature_records.csv.gz`，非 Zenodo 原始檔）重做 24 h 諧波 OLS，18 筆振幅最大差 2.13e-14 K。
7. **MS-03 新增診斷**：自交付的 149 列比較 CSV 重算得 78／71／29，與其 JSON 摘要一致；29 組全部屬於 71 組不相容群；distinct 觀測 ID 為 75。**只驗證 CSV 與規則的內部一致，未重新連線下載 149 份標籤。**
8. **manifest**：MS-01 74/74、MS-02 14/14、MS-03 100/100（含新增檔）SHA-256 全部相符；MS-03 manifest 另有 2 個路徑不在本 repo（xlsx 與 `screened_pool.csv.gz`，屬 handoff 分支）。
9. **路徑與範圍**：每個 PR 只新增自己目錄的檔案，三者互不重疊；PR #6 與 handoff 相對 main 的差異只有 2 個新增檔。

## 4. 特別核對

**SWIM 一致性不是冰量或機率。** 三份報告皆標為無量綱一致性、且兩層（0–1 m、1–5 m）共用輸入。MS-03 兩層為 0.911／0.510，落差**不得**解讀為冰深、冰量或冰減少。→ 台帳 C04、C15、C29（已明列限制）。

**熱慣量不是溫度或硬度；粗網格不是局部量測。** TES 值為格內有效格統計；MS-01 有 27 格、MS-03 有 21 格因補值或遮罩排除，**排除不等於量測為 0**。MOLA 坡度為約 3.7 km 基線尺度。MCS 為 5° bin、模式時間校正、無 QA 與計數欄，且 bin 中心與候選格不同。→ C02、C03、C06、C14、C17、C28、C31。

**衰減／雷達反射不是唯一冰訊號；unknown 不是不存在。** MS-02 引述的 GPR 約 1.5 m 反射（ε≈3.2）僅為摘要層級作者結論，ε 為模型輸入，無獨立冰真值（C21）。MS-03 格內多邊形形貌為 unknown：報告明寫「證據不足，不是確認不存在」，也不補零、不代入 AD1 數值（C34）。HiRISE 索引無相交只代表固定版本索引內無相交，不代表所有觀測皆無覆蓋（C35）。

**MS-02 Adventdalen 與 MS-03 AD1 的降級一致。** MS-02-E03 為「降為一般方法參照」，MS-03-E02 為 `downgrade_general_method_reference_not_specific_MS03_pair`，方向一致、均保留固定 ID。**但兩者用的是不同錨點**：ADE 鑽孔、CS-1 岩芯、AD1（Act-IWS）互不同址（§3 第 5 項）。聯合報告不得把三者寫成「同一個 Adventdalen 場址」（X04）。

**重現既有研究不是新發現。** MS-01 報告自己寫明「已找到直接同場址同用途研究…不主張新場址、新機制或全球首次配對」；MS-03 報告寫明 AD1 的 185 個多邊形重算與原刊 13 項統計一致只是重現／溯源檢查；MS-02 第四輪「沒有新量測」。三份新增的是出處稽核、適用性查核與限制整理（X03、C11、C32）。

## 5. 無法驗證的內容（逐項原因，沒有複製 PASS）

| 項目 | 原因 |
|---|---|
| MS-01 `thermal_followup/validate.py` 重跑 | 需要 Zenodo 原始 HOBO／Campbell 檔（以 `--raw-dir` 指定）；本環境無該檔且對 Zenodo 連線不通（HEAD 請求無回應，先前下載亦被拒）。已記錄 `FileNotFoundError`。**以獨立 OLS 重算 18 筆振幅作為替代，使用 PR #8 已入庫的 `primary_temperature_records.csv.gz`（團隊自己萃取的分析窗紀錄）；它驗證「振幅由這批紀錄算出」，不驗證這批紀錄與 Zenodo 原始檔一致，也不等同於重跑原始檔雜湊驗證。** |
| MS-03 `validate.py` 的 W 站雜湊 | 腳本自述只核對「本機有的」來源雜湊；本環境未取得全部原始檔，exit 0 不涵蓋沒有的檔。 |
| MS-03 149 份標籤本身 | 未重新連網下載；只驗證 CSV 與其規則的內部一致。 |
| MS-02／MS-03 引用的論文內容 | 本輪不開新研究；論文只讀到各組報告自稱的範圍（多為摘要或部分內文）。 |
| MS-03 根因（索引重複列為何生成） | 2026 實跑版、SQL、建置日誌均未取得；各組報告自標 unknown，本驗收維持 unknown。 |
| PR 的 CI | 三個 PR、main、handoff 的 `Workers Builds` 檢查**同樣失敗**，故非這三個 PR 引入；失敗原因屬部署設定，本輪未調查。 |

環境：Python 3.13.18、numpy 2.5.3（MS-03 驗證另裝 pyshp、shapely、pyproj、matplotlib）、Linux 6.18.44。

## 6. MS-03 head 前進後的新增內容

新增兩個 commit 只動 MS-03 自己的目錄（13 個檔案：報告、evidence、manifest、README、`generator_followup/` 四檔、`handoff_status.json`、search_log、sources、validation、1 支腳本）。**沒有改任何火星數值、AD1 降級、形貌 unknown 或 Campbell／HOBO 配時禁用。** 新增主張為 149 份標籤診斷，已列入台帳（C41–C44）。注意該節的「基準 SHA」`8f6d3134…` 寫於報告內，而下方舊節仍寫「接續 SHA `3321765…`」——兩者是同一份報告的時序層次，不是衝突。

## 7. 問題分類與可直接採用的替換句

### 阻擋引用（不得進入聯合報告或簡報）

| ID | 內容 | 原因 |
|---|---|---|
| C10 | 把地球站點（University Valley）結果當 MS-01 溫度預測、冰深或可採性 | 站點結果不可外推 |
| C20 | 「Adventdalen 支持風成覆土下可偵冰」 | MS-02 自己的 C9 判定證據不足：沒有單一地點同時有覆土堆積、冰真值與雷達 |
| C37 | MS-03 報告後段（約 345、387–403 行）舊文「保留條件式地貌與濕凍土對照」 | 被最新降級取代；該報告頂端雖標為歷史，單獨摘錄會誤導 |
| C38 | 把 AD1 事件座標 78.184°N、15.913°E 當感測器位置 | 它是 A1 事件起點，不是感測器 |
| C43 | 把 149 組重複列寫成「已確認 SQL join bug／distinct／官方校時錯誤／索引已修復」 | 根因 unknown |
| C44 | 把 HiRISE 指令時間差套到 Campbell／HOBO 配時 | 不同儀器；報告明禁 |
| X01 | 把三點的 SWIM／TI／CDOD／MCS 互相排序或算相似度 | 單位、解析度、輸入不同，無共同權重 |

### 需要修正文句（可引用，但原句須替換）

| ID | 問題 | 替換句 |
|---|---|---|
| C07 | Campbell 時標偏移（十進位日與印刷時間差，2012-10-28 為 −1 h→−5 h）依資料窗而異，MS-01 的 2010 窗需明說 | 「University Valley W 站 2010 年 11 天窗口的 24 h 諧波振幅（表面 8.38、10 cm 3.89、42 cm 0.21、49 cm 0.13 K）為地球站點實測重算；Campbell 時標偏移依資料窗而異，絕對相位不作引用。」 |
| C09 | Beacon Valley 座標只在 MS-01 | 「引用 Beacon Valley 時，座標以 MS-01 報告列出者為準；MS-02 未獨立查核。」 |
| C18／X02 | MS-02 的 University Valley 錨點為谷級，非 W 站；三份報告同用一個來源 | 「MS-02 對 University Valley 的引用為谷級對照；站點層級數值以 MS-01 的 W 站為準。三份報告引用同一 University Valley 資料，不構成獨立多地點驗證。」 |
| C21 | GPR 反射是摘要層級作者解讀 | 「Brighi 等摘要報告多邊形溝槽約 1.5 m 處有雷達反射；這是作者解讀，本隊未取得獨立冰真值，不作冰深或含冰量證據。」 |
| C22 | 0.35 cm/yr、2900 g m⁻² yr⁻¹ 為峰值／摘要值 | 「CS-1 岩芯堆積率多為 0.05–0.25 cm/yr，0.35 cm/yr 僅峰值期；地球速率不可換算為火星覆土堆積。」 |
| C23 | 活動層 60–100 cm 與 ≥1 m 不同期 | 「活動層深度因年份與來源而異（Rotem 引用 60–100 cm；UNISCALM ≥1 m），未調和，不引為單一值。」 |
| C24 | MS-02 降級後 H2／H3／比較表仍寫「E03 可測」 | 「H2／H3 中的 E03 僅指 CS-1 岩芯的過程類比；雷達偵測部分為一般方法參照，非本候選證據。」 |

### 已明列限制（報告已寫，聯合報告引用時須同帶）

SWIM 為一致性（C04、C15、C29）；熱慣量為表層熱性質（C03、C14、C28）；坡度為格尺度（C02）；CDOD 為 3° 柱光學厚度（C05、C16、C30）；MCS bin 與格不同、MS-02 距 146.7 km（C06、C17、C31）；AD1 重算為重現（C32）；3.04 像素非偵測門檻（C33）；形貌 unknown（C34）；HiRISE 索引限制（C35）；149 為產品份數（C42）；78/71/29 不可相加（C41）；PR #6 依賴 handoff（X05）；第三方授權（C40）。

## 8. 聯合報告與簡報可用／不可用句

**可用：** 「三個候選的圖層數值來自同一份已驗證的共用資料；各指標僅描述格尺度的軌道衍生量，無綜合分數、無相似度百分比。」「地球對照為既有研究的整理與適用性查核，本隊沒有新場址或新機制發現。」「Adventdalen 僅作一般方法參照；岩芯、鑽孔、雷達三組證據不同址。」「MS-03 格內形貌未知（unknown），不等於不存在。」

**不可用：** 任何「X 最像火星」、「此處有冰／冰深 N m」、「SWIM 顯示冰量高」、「Adventdalen 證明覆土下可偵冰」、「MS-03 沒有多邊形」、「索引 bug 已查明」。

## 9. 重現方式

```
python3 -I outputs/integration/audit/scripts/audit_checks.py --repo <repo> --main <main@3cc8488> --ms01 <PR8 head> --ms02 <PR6 head> --ms03 <PR7 head>
python3 outputs/integration/audit/scripts/build_ledger.py
```
各驗證器重跑輸出在 `outputs/integration/audit/reruns/`，每份最後一行為 exit code。
