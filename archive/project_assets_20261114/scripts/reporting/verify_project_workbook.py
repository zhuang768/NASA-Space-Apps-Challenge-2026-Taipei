"""Read-only verification of the delivered workbook against its source-data bundle."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/consolidated"


def same(actual, expected, kind: str) -> bool:
    if expected is None or expected == "":
        return actual is None or actual == ""
    if kind == "date":
        wanted = datetime.fromisoformat(expected).replace(tzinfo=None)
        return isinstance(actual, datetime) and abs((actual - wanted).total_seconds()) < 0.01
    if isinstance(expected, bool):
        return isinstance(actual, bool) and actual == expected
    if isinstance(expected, (float, int)):
        return isinstance(actual, (float, int)) and math.isclose(
            actual, expected, rel_tol=1e-12, abs_tol=1e-10
        )
    if str(expected).startswith("="):
        return actual == "'" + expected or actual == expected
    return actual == expected


def main() -> None:
    bundle = json.loads((OUT / "support/workbook_data.json").read_text())
    book_path = OUT / "NASA_Space_Apps_2026_All_Data.xlsx"
    book = openpyxl.load_workbook(book_path, read_only=True, data_only=False)
    checked = []
    for table in bundle["tables"]:
        sheet = book[table["name"]]
        columns = table["columns"]
        # XLSX permits missing optional dimension metadata; verify the actual rows below.
        assert sheet.max_row in (None, len(table["rows"]) + 1), (table["name"], sheet.max_row)
        assert sheet.max_column in (None, len(columns)), (table["name"], sheet.max_column)
        source_rows = iter(table["rows"])
        row_count = 0
        for row_number, row in enumerate(sheet.iter_rows(max_col=len(columns)), start=1):
            row_count = row_number
            if row_number == 1:
                assert [c.value for c in row] == [c.get("label", c["key"]) for c in columns]
                continue
            expected = next(source_rows)
            for index, (cell, value) in enumerate(zip(row, expected, strict=True)):
                assert cell.data_type != "e", (table["name"], cell.coordinate, cell.value)
                assert same(cell.value, value, columns[index].get("type", "text")), (
                    table["name"], cell.coordinate, repr(cell.value)[:100], repr(value)[:100]
                )
        assert row_count == len(table["rows"]) + 1, (table["name"], row_count)
        assert next(source_rows, None) is None
        checked.append({"sheet": table["name"], "rows": len(table["rows"]),
                        "columns": len(columns), "all_values_checked": True})
        print("PASS", table["name"], len(table["rows"]), flush=True)
    book.close()
    cached = openpyxl.load_workbook(book_path, read_only=True, data_only=True)
    counts_by_sheet = {t["name"]: len(t["rows"]) for t in bundle["tables"]}
    expected_counts = [counts_by_sheet[name] for name in [
        "火星發現候選", "火星新穎性查核", "地球視窗全量", "地球候選", "MEDA原始紀錄", "JSON原值"
    ]]
    summary_counts = [row[0] for row in cached["總覽"].iter_rows(
        min_row=7, max_row=12, min_col=2, max_col=2, values_only=True
    )]
    assert summary_counts == expected_counts, (summary_counts, expected_counts)
    overview_values = [list(row) for row in cached["總覽"].iter_rows(
        min_row=1, max_row=19, min_col=1, max_col=4, values_only=True
    )]
    (OUT / "review/final_overview_values.json").write_text(json.dumps({
        "source": book_path.name, "values": overview_values
    }, ensure_ascii=False, indent=2) + "\n")
    cached.close()

    protected = json.loads((OUT / "review/source_snapshot.json").read_text())
    authorized = {"outputs/research/ice_candidate_followup/search_scope.json"}
    changed = []
    for name, expected in protected.items():
        with (ROOT / name).open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != expected:
            changed.append(name)
    assert set(changed) <= authorized, changed
    coverage_checks = []
    for source in bundle["coverage"]:
        if source.get("sha256"):
            with (ROOT / source["path"]).open("rb") as stream:
                assert hashlib.file_digest(stream, "sha256").hexdigest() == source["sha256"]
        coverage_checks.append(source["path"])
    with book_path.open("rb") as stream:
        book_hash = hashlib.file_digest(stream, "sha256").hexdigest()
    result = {
        "file": str(book_path.relative_to(ROOT)),
        "sha256": book_hash,
        "checks": checked,
        "source_files_verified": len(set(coverage_checks)),
        "source_coverage_entries_verified": len(coverage_checks),
        "numeric_sources_unchanged": True,
        "authorized_metadata_changes": changed,
        "comparison": "All populated source-bundle cells; numeric tolerance 1e-12 relative / 1e-10 absolute",
        "engine": "openpyxl read-only, independent of authoring engine",
        "summary_counts_verified_against_written_tables": summary_counts,
    }
    (OUT / "review/verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print("PASS: all imported cells, source hashes and scientific input preservation.")


if __name__ == "__main__":
    main()
