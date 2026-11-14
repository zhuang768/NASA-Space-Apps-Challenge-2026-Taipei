#!/usr/bin/env python3
"""Export Team2's published EH2 row parser; no new measurement or inversion.

The anchored row expression and six/nine-value interpretation come from the
Team2 report at main 14be2d5b. This exporter uses its already-used PDFium path,
because local pypdf 6.14 plain extraction concatenates the printed rows.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import os
import re
import shutil
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/research/elephant_head_final"
VERSION = "MR-20261114-v3-final"
SOURCE_URL = (
    "https://static.cambridge.org/content/id/urn:cambridge.org:id:article:"
    "S0954102019000269/resource/name/S0954102019000269sup001.pdf"
)
SOURCE_SHA256 = "20fe70f574bc394f05f0c720809f80a9602ac73f6ede34d322ea816cf25590d9"
TEAM2_BASE = ROOT / "outputs/consolidated/research_main_20261114/sources/v2_14be2d5b"
TEAM2_REPORT = TEAM2_BASE / "docs/research/team2_novelty_audit.md"
TEAM2_CSV = TEAM2_BASE / "outputs/research/team2_novelty_audit.csv"
TIME1_LABEL = "Time, GMT-07:00"
TIME2_LABEL = "Local Time GMT-5:30"
PATTERN = re.compile(
    r"^(\d+)\s+(\d+/\d+/\d+ \d+:\d+)\s+(\d+/\d+/\d+ \d+:\d+)\s+(.+)$"
)
VALUES = [
    ("air_temperature_C", "Temp,AIR", "degC", "air", ""),
    ("air_RH_raw_pct", "RH,%", "percent", "air", ""),
    ("air_RH_corrected_pct", "RHice", "percent", "air", ""),
    ("ice49_temperature_C", "Temp, ice 49 cm", "degC", "ice", "49"),
    ("ice49_RH_raw_pct", "RH,%", "percent", "ice", "49"),
    ("ice49_RH_corrected_pct", "RHice", "percent", "ice", "49"),
    ("soil3_temperature_C", "Temp, 3 cm", "degC", "soil", "3"),
    ("soil3_RH_raw_pct", "RH, % raw", "percent", "soil", "3"),
    ("soil3_RH_corrected_pct", "RH_ice <0, -2", "percent", "soil", "3"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def parse_existing(pdf: Path) -> tuple[list[dict], list[dict], int]:
    """Same Team2 anchored regex/6-or-9 numeric rows, PDFium extraction engine."""
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf))
    rows, bad = [], []
    for page_index in range(len(doc)):
        page = doc[page_index]
        textpage = page.get_textpage()
        for line_index, line in enumerate(textpage.get_text_range().splitlines(), 1):
            match = PATTERN.match(line.strip())
            if not match:
                continue
            n, t1, t2, rest = match.groups()
            vals = rest.split()
            try:
                assert len(vals) in [6, 9]
                values = list(map(float, vals))
                assert all(math.isfinite(value) for value in values)
                a = datetime.strptime(t1, "%m/%d/%y %H:%M")
                b = datetime.strptime(t2, "%m/%d/%y %H:%M")
            except Exception as exc:
                bad.append({"source_page": page_index + 1, "line": line, "error": str(exc)})
                continue
            rows.append(
                dict(n=int(n), page=page_index + 1, line=line_index, t=a, t2=b,
                     v=values, tokens=vals, printed_t1=t1, printed_t2=t2,
                     source_text=line.strip())
            )
        textpage.close()
        page.close()
    pages = len(doc)
    doc.close()
    return rows, bad, pages


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf", type=Path, help="Existing exact-hash EH2 PDF; otherwise use output copy/download")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    pdf = OUT / "elephant_head_2019_supplement.pdf"
    if args.pdf:
        if sha256(args.pdf) != SOURCE_SHA256:
            raise ValueError("Input is not the pinned EH2 source")
        if args.pdf.resolve() != pdf.resolve():
            shutil.copyfile(args.pdf, pdf)
    elif not pdf.exists():
        req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
        pdf.write_bytes(urllib.request.urlopen(req, timeout=30).read())
    if sha256(pdf) != SOURCE_SHA256:
        raise ValueError("Source SHA-256 mismatch")

    rows, bad, page_count = parse_existing(pdf)
    if bad or not rows:
        raise ValueError(f"Existing parser failed: {len(rows)} rows, errors={bad}")
    # Structural checks use the parsed rows, not hard-coded target counts.
    assert [x["n"] for x in rows] == list(range(1, len(rows) + 1))
    assert len({x["t"] for x in rows}) == len(rows)
    assert all(b["t"] - a["t"] == timedelta(hours=1) for a, b in zip(rows, rows[1:]))
    assert all(x["t2"] - x["t"] == timedelta(minutes=90) for x in rows)

    annual_start, annual_stop = datetime(2017, 12, 1), datetime(2018, 12, 1)
    summer_start, summer_stop = datetime(2017, 12, 1), datetime(2018, 3, 1)
    annual = [x for x in rows if annual_start <= x["t"] < annual_stop]
    summer = [x for x in rows if summer_start <= x["t"] < summer_stop and len(x["v"]) == 9]
    if not summer or not annual:
        raise ValueError("No paired data in the existing Team2 windows")
    summary = dict(
        source_sha256=sha256(pdf), pages=page_count, records=len(rows), bad_records=bad,
        first=str(rows[0]["t"]), last=str(rows[-1]["t"]), row_ids_contiguous=True,
        hourly_first_timestamp_contiguous=True, second_timestamp_offset_minutes=90,
        timezone_status="printedoffsetconsistent_butUTCmeaning_unverified",
        records_with_3cm=sum(len(x["v"]) == 9 for x in rows),
        missing_3cm_records=sum(len(x["v"]) == 6 for x in rows),
        last_3cm=str([x for x in rows if len(x["v"]) == 9][-1]["t"]),
        annual_n=len(annual), summer_paired_n=len(summer),
        annual_air_mean_C=mean(x["v"][0] for x in annual),
        annual_ice49_mean_C=mean(x["v"][3] for x in annual),
        summer_air_mean_C=mean(x["v"][0] for x in summer),
        summer_ice49_mean_C=mean(x["v"][3] for x in summer),
        summer_soil3_mean_C=mean(x["v"][6] for x in summer),
        summer_soil3_minus_ice49_mean_C=mean(x["v"][6] - x["v"][3] for x in summer),
        RH_ice49_corrected_above100_n=sum(x["v"][5] > 100 for x in rows),
        annual_window=dict(start_inclusive=str(annual_start), stop_exclusive=str(annual_stop)),
        summer_window=dict(start_inclusive=str(summer_start), stop_exclusive=str(summer_stop)),
        summer_first_source_row=summer[0]["n"], summer_last_source_row=summer[-1]["n"],
        summer_first_source_page=summer[0]["page"], summer_last_source_page=summer[-1]["page"],
        summer_expected_hourly_records=int((summer_stop - summer_start).total_seconds() / 3600),
    )
    summary["summer_paired_coverage_fraction"] = len(summer) / summary["summer_expected_hourly_records"]

    with TEAM2_CSV.open(encoding="utf-8-sig", newline="") as handle:
        team2_row = next(row for row in csv.DictReader(handle) if row["candidate_id"] == "EARTH-002")
    reference = json.loads(team2_row["executed_evidence_qa_json"])
    compare_keys = [key for key in reference if key in summary]
    comparisons = {}
    for key in compare_keys:
        a, b = summary[key], reference[key]
        matches = math.isclose(a, b, rel_tol=0, abs_tol=1e-10) if type(a) is float else a == b
        comparisons[key] = {"reproduced": a, "team2_recorded": b, "matches": matches}
    if not all(item["matches"] for item in comparisons.values()):
        raise ValueError("Reproduction disagrees with the pinned Team2 QA; inspect without tuning")

    fields = [
        "version", "earth_candidate_id", "mars_candidate_id", "source_row", "source_page",
        "source_extracted_line_on_page", "printed_time_1_label", "printed_time_1",
        "printed_time_2_label", "printed_time_2", "time_1_nominal_iso", "time_2_nominal_iso",
        "source_numeric_count", "ice49_depth_cm", "soil3_depth_cm",
    ] + [x[0] for x in VALUES] + [
        "air_missing", "ice49_missing", "soil3_missing", "soil3_missing_reason",
        "air_RH_corrected_gt100", "ice49_RH_corrected_gt100", "soil3_RH_corrected_gt100",
        "in_annual_window_time1", "in_summer_paired_window_time1", "flags", "source_text",
    ]
    records = []
    for row in rows:
        tokens = row["tokens"] + [""] * (9 - len(row["tokens"]))
        flags = ["timezone_meaning_unverified"]
        if len(row["v"]) == 6:
            flags.append("soil3_not_printed")
        for index, prefix in [(2, "air"), (5, "ice49"), (8, "soil3")]:
            if index < len(row["v"]) and row["v"][index] > 100:
                flags.append(prefix + "_RH_corrected_gt100_retained")
        record = dict(
            version=VERSION, earth_candidate_id="EARTH-002", mars_candidate_id="I-02",
            source_row=row["n"], source_page=row["page"], source_extracted_line_on_page=row["line"],
            printed_time_1_label=TIME1_LABEL, printed_time_1=row["printed_t1"],
            printed_time_2_label=TIME2_LABEL, printed_time_2=row["printed_t2"],
            time_1_nominal_iso=str(row["t"]), time_2_nominal_iso=str(row["t2"]),
            source_numeric_count=len(row["v"]), ice49_depth_cm=49, soil3_depth_cm=3,
            air_missing=False, ice49_missing=False, soil3_missing=len(row["v"]) == 6,
            soil3_missing_reason="not_printed_in_source_6_value_row" if len(row["v"]) == 6 else "",
            air_RH_corrected_gt100=row["v"][2] > 100,
            ice49_RH_corrected_gt100=row["v"][5] > 100,
            soil3_RH_corrected_gt100=row["v"][8] > 100 if len(row["v"]) == 9 else "",
            in_annual_window_time1=annual_start <= row["t"] < annual_stop,
            in_summer_paired_window_time1=summer_start <= row["t"] < summer_stop and len(row["v"]) == 9,
            flags=";".join(flags), source_text=row["source_text"],
        )
        record.update({value[0]: token for value, token in zip(VALUES, tokens)})
        records.append(record)
    csv_path = OUT / "elephant_head_records.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
    # Roundtrip every source literal, both printed times and original row/page.
    with csv_path.open(encoding="utf-8", newline="") as handle:
        written = list(csv.DictReader(handle))
    assert len(written) == len(rows)
    for source, exported in zip(rows, written):
        assert int(exported["source_row"]) == source["n"]
        assert int(exported["source_page"]) == source["page"]
        assert exported["printed_time_1"] == source["printed_t1"]
        assert exported["printed_time_2"] == source["printed_t2"]
        assert [exported[x[0]] for x in VALUES] == source["tokens"] + [""] * (9 - len(source["tokens"]))

    definitions = {
        "version": "Mainline export version; does not change the publisher's observation date.",
        "earth_candidate_id": "Fixed EARTH-002 key; Elephant Head published station.",
        "mars_candidate_id": "I-02 research-question correspondence; no physical-equivalence claim.",
        "source_row": "Original printed # record identifier (not spreadsheet row).",
        "source_page": "One-based PDF page containing the record.",
        "source_extracted_line_on_page": "One-based PDFium extracted-text line; source_row is the printed identifier.",
        "printed_time_1_label": "Exact first printed column label; UTC interpretation unresolved.",
        "printed_time_1": "Original first printed timestamp string, unchanged.",
        "printed_time_2_label": "Exact second printed column label; UTC interpretation unresolved.",
        "printed_time_2": "Original second printed timestamp string, unchanged.",
        "time_1_nominal_iso": "Naive parsed first timestamp for within-table selection; no timezone conversion.",
        "time_2_nominal_iso": "Naive parsed second timestamp; no timezone conversion.",
        "source_numeric_count": "Six or nine printed numeric values; six means the 3 cm group is absent.",
        "ice49_depth_cm": "Nominal published 49 cm subsurface sensor depth, not a new interface estimate.",
        "soil3_depth_cm": "Nominal published 3 cm subsurface sensor depth; not satellite LST.",
        "air_missing": "True only if the air group is missing; no such parsed records in this export.",
        "ice49_missing": "True only if the 49 cm group is missing; no such parsed records in this export.",
        "soil3_missing": "True when all three 3 cm values are absent in the printed six-value record.",
        "soil3_missing_reason": "Source absence is retained; no winter infilling or zero substitution.",
        "air_RH_corrected_gt100": "Flag only; published air corrected RH retained above 100 percent.",
        "ice49_RH_corrected_gt100": "Flag only; published 49 cm corrected RH retained above 100 percent.",
        "soil3_RH_corrected_gt100": "Flag only; blank when the 3 cm group is missing.",
        "in_annual_window_time1": "First printed time in [2017-12-01, 2018-12-01); not a UTC year.",
        "in_summer_paired_window_time1": "Both depths printed and first time in [2017-12-01, 2018-03-01).",
        "flags": "Semicolon-separated export cautions; absence of a sensor flag is not calibration clearance.",
        "source_text": "Complete extracted printed record, preserved for source-row audit.",
    }
    dictionary = []
    for name in fields:
        entry = dict(column=name, printed_header="", unit="", medium="", nominal_depth_cm="",
                     missing_encoding="empty field where source value is absent", definition=definitions.get(name, ""))
        if name in {x[0] for x in VALUES}:
            _, header, unit, medium, depth = next(x for x in VALUES if x[0] == name)
            note = "Original published numeric token; no rescaling or independent recalibration."
            if "corrected" in name:
                note += " Author-corrected RH as printed; no new correction formula, clipping, or water-activity inference."
            elif "RH_raw" in name:
                note += " Original RH column, distinct from the adjacent author-corrected RH."
            if medium == "air":
                note += " Air sensor height is not specified by this table header."
            entry.update(printed_header=header, unit=unit, medium=medium, nominal_depth_cm=depth, definition=note)
        dictionary.append(entry)
    with (OUT / "data_dictionary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(dictionary[0]))
        writer.writeheader()
        writer.writerows(dictionary)

    limits = [
        "Published supplementary observations reproduced, not new field measurements or sensor recalibration.",
        "Both printed time labels are retained; their UTC/solar-time meaning remains unverified.",
        "Corrected RH above 100 percent is flagged and preserved, not clipped or treated as calibrated water activity.",
        "Missing 3 cm records remain missing; no annual 3 cm mean or winter infilling.",
        "Only same-row paired summer temperatures are plotted; serial correlation is not modeled and records are not independent replicates.",
        "No confidence intervals, causal cover effect, ice-depth/TI inversion, blind accuracy, ice mass balance, or Mars performance inference.",
        "Agreement with Team2 QA does not rule out errors in the original publisher data.",
    ]
    qa = dict(
        version=VERSION, earth_candidate_id="EARTH-002", mars_candidate_id="I-02",
        status="PASS_EXPORT_REPRODUCTION_AND_TRACEABILITY_ONLY",
        provenance=dict(source_url=SOURCE_URL, source_pdf=pdf.name, source_sha256=sha256(pdf),
                        source_bytes=pdf.stat().st_size, original_parser_and_QA="Team2",
                        current_work="Mainline export and reproduction, not original observations",
                        report_reference=str(TEAM2_REPORT.relative_to(ROOT)),
                        report_sha256=sha256(TEAM2_REPORT), csv_reference=str(TEAM2_CSV.relative_to(ROOT)),
                        csv_reference_sha256=sha256(TEAM2_CSV), parser_code="scripts/research/export_elephant_head_final.py"),
        extraction=dict(engine="pypdfium2 (existing Team2 second-engine path)",
                        pdfium_version=importlib.metadata.version("pypdfium2"), pattern=PATTERN.pattern,
                        method="Existing anchored row regex and 6/9 numeric-value interpretation, unchanged",
                        pypdf_plain_note="Local pypdf 6.14.2 plain extraction concatenates rows and yields no anchored records; not used to change or reconstruct records",
                        current_double_engine_check=False,
                        prior_Team2_double_engine_QA="Team2 reported full pypdf/PDFium row comparison; inherited with attribution, not claimed as this export's run"),
        printed_time_labels=[TIME1_LABEL, TIME2_LABEL], summary=summary,
        validation=dict(source_hash_matches=True, source_literals_roundtrip_all_records=True,
                        original_row_page_and_both_times_roundtrip=True,
                        pinned_Team2_summary_comparisons=comparisons,
                        all_summary_comparisons_match=True,
                        hard_coded_target_record_counts_or_means_used=False),
        limits=limits,
    )
    write_json(OUT / "qa.json", qa)

    os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib_elephant_head_final")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.titlesize": 17,
                         "axes.labelsize": 11, "axes.spines.top": False, "axes.spines.right": False,
                         "savefig.facecolor": "white", "figure.facecolor": "white"})
    times = [x["t"] for x in summer]
    soil = [x["v"][6] for x in summer]
    ice = [x["v"][3] for x in summer]
    diff = [a - b for a, b in zip(soil, ice)]

    def decorate(ax, title: str, ylabel: str) -> None:
        ax.set_title(title, loc="left", pad=38, fontweight="bold")
        ax.text(0, 1.045, f"01 Dec 2017 to 28 Feb 2018 | {len(summer):,} paired hourly records | published observations",
                transform=ax.transAxes, color="#4B5563", fontsize=10)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(f"First printed time ({TIME1_LABEL}); no UTC/solar-time conversion", labelpad=12)
        ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[1, 15]))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        ax.set_xlim(summer_start, summer_stop)
        # Keep the final boundary label inside the canvas.
        ax.get_xticklabels()[-1].set_horizontalalignment("right")
        ax.grid(axis="y", color="#D1D5DB", linewidth=0.55)
        ax.tick_params(axis="both", length=3, color="#9CA3AF")

    foot = ("Source: McKay et al. (2019), published supplement (QA1). Team2 parser/QA; mainline export and reproduction.\n"
            "Subsurface records, not satellite LST. No causal, ice-depth/TI, or Mars-performance inference. " + VERSION)
    fig, ax = plt.subplots(figsize=(11.5, 5.8))
    fig.subplots_adjust(left=.09, right=.98, top=.79, bottom=.25)
    ax.plot(times, soil, color="#D55E00", linewidth=.85,
            label=f"3 cm | mean {summary['summer_soil3_mean_C']:.4f} °C")
    ax.plot(times, ice, color="#0072B2", linewidth=1.1,
            label=f"49 cm | mean {summary['summer_ice49_mean_C']:.4f} °C")
    decorate(ax, "Elephant Head: summer temperatures at two depths", "Temperature (°C)")
    ax.legend(loc="lower left", frameon=True, framealpha=.96, facecolor="white", edgecolor="#D1D5DB")
    fig.text(.09, .045, foot, fontsize=8.1, color="#4B5563", linespacing=1.65)
    fig.savefig(OUT / "summer_temperatures.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11.5, 5.8))
    fig.subplots_adjust(left=.09, right=.98, top=.79, bottom=.25)
    ax.plot(times, diff, color="#6A3D9A", linewidth=.85, label="Same-row 3 cm minus 49 cm")
    ax.axhline(0, color="#6B7280", linewidth=.8, zorder=0)
    ax.axhline(summary["summer_soil3_minus_ice49_mean_C"], color="#111827", linewidth=1.1,
               linestyle=(0, (5, 3)), label=f"Descriptive mean {summary['summer_soil3_minus_ice49_mean_C']:+.4f} °C")
    decorate(ax, "Elephant Head: paired depth-temperature difference", "3 cm minus 49 cm (°C)")
    ax.legend(loc="lower left", frameon=True, framealpha=.96, facecolor="white", edgecolor="#D1D5DB")
    fig.text(.09, .045, foot, fontsize=8.1, color="#4B5563", linespacing=1.65)
    fig.savefig(OUT / "summer_temperature_difference.png", dpi=300)
    plt.close(fig)

    readme = f"""# Elephant Head final data export - {VERSION}

Published source observations, original parser and QA: McKay et al. (2019) supplementary table and Team2. This package is the mainline's export and reproduction of that work, not original field measurements, a new parser, or independent sensor calibration.

- Source: {SOURCE_URL}
- Original PDF: `elephant_head_2019_supplement.pdf`; SHA-256 `{SOURCE_SHA256}`.
- Team2 frozen evidence: `{TEAM2_REPORT.relative_to(ROOT)}` and the EARTH-002 `executed_evidence_qa_json` in its companion CSV; source main `14be2d5b`.
- Fixed correspondence: EARTH-002 -> I-02 for research-question organization, not a physical-equivalence or ice-resource validation.

## Contents and reproduced results

`elephant_head_records.csv` contains all {len(rows):,} printed records, one row per original record, with source PDF page/row and extraction-line number, both unchanged printed time strings/labels, nominal parsed times without timezone conversion, all nine original numeric tokens where printed, explicit 3 cm missingness, and retained RH flags. `data_dictionary.csv` documents every column, original header, units and nominal depth. Empty numeric fields mean absent source values, never zero.

The table spans {summary['first']} to {summary['last']} on the first printed time axis. The 3 cm group has {summary['records_with_3cm']:,} records and {summary['missing_3cm_records']:,} missing records; its final printed record is {summary['last_3cm']}. No 3 cm annual mean or winter fill is produced.

The existing Team2 summer window is first printed time >= 2017-12-01 and < 2018-03-01: {len(summer):,} same-row paired records ({summary['summer_paired_coverage_fraction']:.1%} of the nominal hourly window), source rows {summer[0]['n']}--{summer[-1]['n']}, PDF pages {summer[0]['page']}--{summer[-1]['page']}. Mean 3 cm temperature is {summary['summer_soil3_mean_C']:.10f} degC; mean 49 cm temperature is {summary['summer_ice49_mean_C']:.10f} degC; mean paired 3-minus-49 cm difference is {summary['summer_soil3_minus_ice49_mean_C']:+.10f} degC. Both final PNGs show all paired hourly values, without smoothing or confidence bands.

The reference annual window is first printed time >= 2017-12-01 and < 2018-12-01: {len(annual):,} records. Mean air is {summary['annual_air_mean_C']:.10f} degC and mean 49 cm is {summary['annual_ice49_mean_C']:.10f} degC. These and the summer means reproduce Team2's recorded QA; no target record count or mean is used to alter the extraction.

## Reproduction and checks

Run from the repository root:

```sh
python3 scripts/research/export_elephant_head_final.py --pdf outputs/research/elephant_head_final/elephant_head_2019_supplement.pdf
```

Dependencies: Python with `pypdfium2` and `matplotlib`. The row expression and six/nine-value interpretation are Team2's existing parser. Its already-used PDFium extraction path is selected because local pypdf 6.14.2 plain extraction concatenates rows. This export does not claim a fresh double-engine check. It verifies the exact source hash, contiguous original IDs, hourly first timestamps, 90-minute difference between printed times, all CSV numeric tokens/row/page/time fields after roundtrip, and dynamically compares its computed summary with the pinned Team2 QA JSON. `qa.json` contains the checks, values and limits; `manifest.json` contains final file hashes. Failed checks stop export rather than tuning data to expected totals.

## Limits

- Preserve `{TIME1_LABEL}` and `{TIME2_LABEL}` exactly. A consistent 90-minute offset does not resolve UTC or local solar time; neither conversion is made.
- Published corrected 49 cm RH exceeds 100% in {summary['RH_ice49_corrected_above100_n']:,} records. All values remain unchanged and flagged. No clipping, new correction formula or water-activity inference is applied.
- The 3 cm and 49 cm temperatures are subsurface point observations, not satellite LST. Air sensor height is unspecified by this table header.
- Serial correlation is not modeled: record counts are not counts of independent replicates. No confidence interval or new causal effect is claimed.
- This package does not infer ice depth, TES thermal inertia, blind-detection accuracy, sample heating, ice mass loss, or Earth-to-Mars equipment performance. Agreement with earlier QA cannot exclude errors in the original published table.

Only the final two PNG figures are supplied: `summer_temperatures.png` and `summer_temperature_difference.png`. Original data remain attributed to the authors; project code licensing is not assigned to the publisher's supplementary data.
"""
    (OUT / "README.md").write_text(readme)
    paths = [pdf, csv_path, OUT / "data_dictionary.csv", OUT / "qa.json", OUT / "README.md",
             OUT / "summer_temperatures.png", OUT / "summer_temperature_difference.png"]
    manifest = dict(version=VERSION, source_url=SOURCE_URL, source_sha256=SOURCE_SHA256,
                    authorship="Published observations: source authors; original parser/QA: Team2; this export: mainline reproduction",
                    script={"path": str(Path(__file__).resolve().relative_to(ROOT)), "sha256": sha256(Path(__file__))},
                    files=[dict(path=str(path.relative_to(ROOT)), bytes=path.stat().st_size, sha256=sha256(path)) for path in paths])
    write_json(OUT / "manifest.json", manifest)
    print(json.dumps({"output": str(OUT), "summary": summary, "CSV_columns": len(fields),
                      "Team2_comparison_count": len(comparisons), "all_match": True}, indent=2))


if __name__ == "__main__":
    main()
