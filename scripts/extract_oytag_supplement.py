"""Extract published parent-sample coordinates from the verified zircon supplement.

Optional reader: pip install xlrd==2.0.1. Raw supplement is not redistributed.
"""

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from shapely.geometry import Point, Polygon

from analog.provenance import write_json

URL = "https://ars.els-cdn.com/content/image/1-s2.0-S1367912011001878-mmc1.xls"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    try:
        import xlrd
    except ImportError as exc:
        raise SystemExit("Optional reader required: pip install xlrd==2.0.1") from exc
    book = xlrd.open_workbook(args.input)
    assert book.sheet_names() == ["ZirconData"], "Inspect a changed supplement before extraction"
    sheet = book.sheet_by_name("ZirconData")
    assert sheet.nrows == 912 and sheet.ncols == 17
    assert "U-Pb" in str(sheet.cell_value(0, 0))
    root = Path(__file__).resolve().parents[1]
    candidate_path = root / "outputs/analysis/results_with_context.json"
    candidate = next(
        c
        for c in json.loads(candidate_path.read_text())["candidates"]["gale"]
        if c["candidate_id"] == "gale-01"
    )
    polygon = Polygon(candidate["footprint"])
    metadata_rows = [i for i in range(sheet.nrows) if "Latitude:" in sheet.row_values(i)]
    records = []
    for j, row_no in enumerate(metadata_rows):
        row = sheet.row_values(row_no)
        lat, lon = row[row.index("Latitude:") + 1], row[row.index("Longitude:") + 1]
        stop = metadata_rows[j + 1] if j + 1 < len(metadata_rows) else sheet.nrows
        ids = [
            str(sheet.cell_value(i, 0))
            for i in range(row_no + 1, stop)
            if re.match(r"^PMR-\d+-\d+$", str(sheet.cell_value(i, 0)))
        ]
        families = {re.match(r"^(PMR-\d+)-\d+$", i)[1] for i in ids}
        assert len(families) == 1 and -90 <= lat <= 90 and -180 <= lon <= 180
        records.append(
            {
                "parent_sample_id": families.pop(),
                "latitude_deg": lat,
                "longitude_deg": lon,
                "sample_type": row[0].split(":", 1)[1].strip(),
                "metadata_excel_row": row_no + 1,
                "source_sheet": sheet.name,
                "inside_candidate_polygon": polygon.covers(Point(lon, lat)),
                "same_gypsum_outcrop_link": "not established",
                "coordinate_datum": "not stated in metadata row",
            }
        )
    assert len(records) == 10 and len({r["parent_sample_id"] for r in records}) == 10
    output = root / "outputs/research/oytag_supplement_coordinates.csv"
    with output.open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    write_json(
        root / "outputs/research/oytag_supplement_metadata.json",
        {
            "source_doi": "10.1016/j.jseaes.2011.04.020",
            "url": URL,
            "source_title": sheet.cell_value(0, 0),
            "source_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
            "source_bytes": args.input.stat().st_size,
            "sheet": sheet.name,
            "dimensions": [sheet.nrows, sheet.ncols],
            "coordinate_groups": len(records),
            "candidate_input_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
            "data_type": "zircon U-Pb analyses with parent-rock coordinates; not gypsum mineralogy",
            "not_proven": [
                "GPS instrument or coordinate datum",
                "gypsum layer sample ID",
                "same-outcrop XRD",
                "FigDR1 map",
            ],
            "coordinates_csv": output.name,
            "inside_count": sum(r["inside_candidate_polygon"] for r in records),
        },
    )
    print(
        f"{len(records)} coordinate groups extracted; {sum(r['inside_candidate_polygon'] for r in records)} in candidate"
    )
    print("Zircon parent coordinates are not gypsum GPS or mineral evidence")


if __name__ == "__main__":
    main()
