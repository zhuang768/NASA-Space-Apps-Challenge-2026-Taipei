"""Reproduce the three-candidate package; network access is opt-in."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download",action="store_true",help="Download missing checksum-pinned public inputs")
    parser.add_argument("--font",type=Path,help="Font containing Traditional Chinese glyphs for the PDF")
    parser.add_argument("--skip-report",action="store_true",help="Reproduce numerical artifacts without generating the PDF")
    args=parser.parse_args()
    commands=[
        ["scripts.download_mars","--download" if args.download else "--verify-only"],
        ["scripts.build_mars_stack"],
        ["scripts.research.mars_reselection_20261114"],
        ["scripts.research.mars_reselection_20261114","--finalize-targets","outputs/research/mars_reselection_20261114/fixed_targets.json"],
        ["scripts.research.mars_reselection_20261114","--validate"],
    ]
    if not args.skip_report:
        command=["scripts.reporting.build_mars_reselection_report"]
        if args.font: command += ["--font",str(args.font.resolve())]
        commands.append(command)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",MPLCONFIGDIR=str(ROOT/".cache/matplotlib"))
    for command in commands:
        subprocess.run([sys.executable,"-m",*command],cwd=ROOT,env=env,check=True)


if __name__ == "__main__":
    main()
