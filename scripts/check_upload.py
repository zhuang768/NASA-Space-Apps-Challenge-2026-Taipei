"""Check local Git upload file sizes without changing files or contacting GitHub."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIB = 1024 * 1024


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )


def main() -> int:
    result = git("ls-files", "--cached", "--others", "--exclude-standard", "-z")
    if result.returncode:
        print("無法讀取 Git 專案，請確認 Git 已安裝且專案是以 git clone 取得。")
        return 1

    files = []
    for name in set(result.stdout.split("\0")) - {""}:
        path = ROOT / name
        if path.is_file() and not path.is_symlink():
            files.append((path.stat().st_size, name))
    files.sort(reverse=True)
    oversized = [(size, name) for size, name in files if size > 100 * MIB]
    browser_large = [(size, name) for size, name in files if 25 * MIB < size <= 100 * MIB]

    print(f"檢查 {len(files)} 個已追蹤或可加入的本機檔案。")
    if files:
        size, name = files[0]
        print(f"最大檔案：{name}（{size / MIB:.2f} MiB）")
    for size, name in oversized:
        print(f"[Git 大檔阻礙] {name}：{size / MIB:.2f} MiB，超過 100 MiB。")
    for size, name in browser_large:
        print(f"[請使用 Git 上傳] {name}：{size / MIB:.2f} MiB，超過網頁的 25 MiB。")

    if git("check-ignore", "-q", "data/").returncode == 0:
        print("data/ 已依專案設計排除；請各自執行 scripts/download_mars.py 取得資料。")

    # Inspect names only; never read credential contents.
    secrets = git("ls-files", "--", ".env", ".netrc").stdout.splitlines()
    if secrets:
        print("[需要處理] 認證設定檔已被 Git 追蹤，請移出版控並檢查是否需要撤換憑證。")

    if oversized or secrets:
        print("檔案檢查未通過；請依 CONTRIBUTING.md 處理。")
        return 1
    print("本機檔案檢查通過。此檢查不涵蓋歷史提交、遠端規則或隊友帳號權限。")
    print("若仍無法上傳，請提供上傳方式與完整錯誤訊息，對照 CONTRIBUTING.md。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
