# 隊友協作與上傳

## 先確認協作者權限

儲存庫：https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei

擁有者在儲存庫的 **Settings → Collaborators → Add people** 邀請隊友的 GitHub 帳號。
隊友必須接受邀請，並使用受邀的同一個帳號登入 GitHub 或開發工具。
加入競賽隊伍並不會自動取得這個儲存庫的權限。

## 第一次取得程式和資料

```bash
git clone https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei.git
cd NASA-Space-Apps-Challenge-2026-Taipei
python3 -m venv .venv
```

macOS / Linux：

```bash
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python scripts/download_mars.py
```

Windows PowerShell（需已安裝 Python 3.11 以上，建立環境時可使用 `py -3 -m venv .venv`）：

```powershell
.venv\Scripts\python.exe -m pip install -e ".[dev]"
.venv\Scripts\python.exe scripts\download_mars.py
```

`data/` 不放進 Git。下載腳本會取得目前列出的火星資料（約 365 MB），已有的檔案會跳過。
這個下載流程仍需要可連到各資料來源的網路；腳本出錯時請保留完整錯誤訊息。
衍生資料由對應的處理腳本重建。

## 提交程式

在最新的 `main` 上建立自己的分支，例如 `git switch -c teammate/terrain`。
若本機已有未提交的修改，先保留好修改，再切換或同步分支。

```bash
python3 scripts/check_upload.py
git status
git add <本次修改的程式檔案路徑>
git diff --cached --stat
git commit -m "Describe the change"
git push -u origin HEAD
```

Windows 可將上面的 `python3` 改成 `py -3`。
上傳後在 GitHub 建立 Pull Request，將分支的變更合併到 `main`。

## 依錯誤訊息處理

| 現象或訊息 | 處理方式 |
| --- | --- |
| 資料沒有出現在 GitHub，但程式有上傳 | `data/` 被刻意忽略；執行下載腳本取得資料。 |
| `403`、`Permission denied`、`Write access ... not granted` | 確認協作者邀請已接受、登入的是受邀帳號；SSH 使用者另外檢查金鑰。 |
| `401`、`Authentication failed` | 開發工具重新登入 GitHub；使用 gh CLI 時執行 `gh auth login`。HTTPS Git 不使用帳號密碼驗證，需使用工具登入、權杖或 SSH。 |
| 網頁指出檔案過大 | 網頁每檔上限 25 MiB；25–100 MiB 的檔案改用 Git。專案原始資料優先透過下載腳本取得。 |
| `GH001` 或檔案超過 100 MiB | 不要反覆重推。檢查待推送提交是否含大型檔案，選擇移除該提交中的大檔、外部資料來源或 Git LFS；只刪掉工作區檔案未必能移除提交中的大檔。 |
| `non-fast-forward`、`fetch first` | 遠端已有其他提交。保留本機修改並同步、解決衝突，或推送自己的新分支；不要使用 force push 覆蓋隊友。 |
| 分支保護或必須使用 Pull Request | 推送自己的分支並建立 Pull Request。 |
| `push protection`、`secret detected` | 從待推送提交移除憑證；若已外洩，撤換該憑證。不要繞過保護。 |

本機檢查工具不連線 GitHub，也不能證明隊友有寫入權限。需要進一步診斷時，提供 GitHub 帳號、上傳方式與錯誤訊息；不要提供密碼或權杖。
