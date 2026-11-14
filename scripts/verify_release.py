#!/usr/bin/env python3
"""Verify the published evidence package using only the Python standard library."""
from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/research/mars_reselection_20261114"


def main():
    manifest = json.loads((ROOT / "release_manifest.json").read_text())
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        content = path.read_bytes()
        assert len(content) == entry["bytes"], entry["path"]
        assert hashlib.sha256(content).hexdigest() == entry["sha256"], entry["path"]
    rows = list(csv.DictReader((OUT / "final_candidates.csv").open()))
    assert [r["candidate_id"] for r in rows] == ["MS-01", "MS-02", "MS-03"]
    assert [r["input_review_id"] for r in rows] == ["A", "D", "C"]
    assert all("not_globally_novelty_cleared" in r["final_selection_status"] for r in rows)
    sites = json.loads((OUT / "selected_targets.json").read_text())["sites"]
    expected = [(56.75, 72.75), (52.75, 168.25), (57.75, -117.75)]
    assert [(s["center"]["lat"], s["center"]["lon"]) for s in sites] == expected
    assert (OUT / "mars_three_candidates_report_zh.pdf").read_bytes().startswith(b"%PDF-")
    assert (OUT / "candidate_map.png").read_bytes().startswith(bytes([137, 80, 78, 71]))
    for path in ROOT.rglob("*.md"):
        if any(x in path.parts for x in [".git", ".venv", ".cache", "data"]):
            continue
        for link in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            if "://" in link or link.startswith(("#", "mailto:")):
                continue
            target = link.split("#", 1)[0]
            if target:
                assert (path.parent / target).exists(), (str(path.relative_to(ROOT)), target)
    for old in ["web", "outputs/analysis", "outputs/analysis_scale10km", "outputs/matching_handoff", "outputs/compute", "outputs/consolidated", "outputs/research/elephant_head_final"]:
        assert not (ROOT / old).exists(), old
    print(f"PASS: {len(manifest['files'])} immutable files; three selected targets; links and artifact signatures.")


if __name__ == "__main__":
    main()
