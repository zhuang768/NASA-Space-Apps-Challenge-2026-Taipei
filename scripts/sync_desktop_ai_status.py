"""Update only the GPT section of the original Desktop coordination file.

Run in the user's Mac Terminal when the Codex workspace cannot write to Desktop.
Use --preview to inspect the replacement without writing anything.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="Only display the GPT section")
    parser.add_argument("--handoff", action="store_true", help="Sync the Matching handoff status")
    args = parser.parse_args()

    project = Path(__file__).resolve().parents[1]
    target = project.parent / "AI_STATUS.md"
    brief_name = "mars_discovery_handoff.md" if args.handoff else "site_discovery_brief.md"
    brief = project / "docs" / brief_name
    if not target.is_file() or not brief.is_file():
        print("找不到桌面 AI_STATUS.md 或交接文件；沒有修改任何檔案。")
        return 1

    content = target.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?ms)^## GPT\n.*?(?=^## |\Z)", content))
    if len(matches) != 1:
        print("桌面檔案必須恰好有一個 ## GPT 區塊；沒有修改任何檔案。")
        return 1

    timestamp = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M")
    doing = (
        "idle — Matching handoff ready: 15 reviewed; novelty unchecked; "
        "ice conditional, dust context; firm-ground claim dropped"
        if args.handoff
        else "idle — 已同步使用者選點方向：新穎／少研究、特定用途、"
        "排除已知同用途場址、不要求整體最高分"
    )
    label = "Matching → Reporting handoff" if args.handoff else "完整選點原則"
    section = (
        "## GPT\n"
        f"- Doing: {doing}\n"
        f"- Files: [{label}]({brief.relative_to(target.parent).as_posix()})\n"
        f"- Updated: {timestamp} (Asia/Taipei)\n"
    )
    if args.preview:
        print("預覽：尚未寫入桌面原檔。")
        print(section)
        return 0

    match = matches[0]
    replacement = content[: match.start()] + section + content[match.end() :]
    try:
        with target.open("r+", encoding="utf-8") as stream:
            if stream.read() != content:
                print("協作檔剛被更新，沒有修改；請重新執行一次。")
                return 1
            stream.seek(0)
            stream.write(replacement)
            stream.truncate()
    except PermissionError:
        print("此執行環境禁止寫入桌面。請在 Mac 的終端機執行本指令。")
        return 1

    if target.read_text(encoding="utf-8") != replacement:
        print("讀回內容與寫入內容不同，可能有另一個 AI 同時更新；請檢查檔案。")
        return 1
    print(f"已同步：{target}")
    print("僅更新 ## GPT；Cursor 區塊及其他內容均保留。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
