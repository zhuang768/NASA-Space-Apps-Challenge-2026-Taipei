"""Export Team 2's EH2 transcription method with page/row provenance and QA.

Base row regex, 6/9-value interpretation and windows adopted from Team 2's
docs/research/team2_novelty_audit.md at bc9fe3c0. New work is durable tidy export,
per-page export checks, reproducible configuration and descriptive figures.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
import importlib.metadata
import json
import logging
import math
from pathlib import Path
import re
import statistics
import time

from inventory import inventory
from pipeline import digest, months, percentile, write_csv

ROW_PATTERN = re.compile(r"^(\d+)\s+(\d+/\d+/\d+ \d+:\d+)\s+(\d+/\d+/\d+ \d+:\d+)\s+(.+)$")
FIELDS = ["T_air_C", "RH_air_water_pct", "RH_air_ice_corrected_pct", "T_49cm_C",
          "RH_49cm_water_pct", "RH_49cm_ice_corrected_pct", "T_3cm_C", "RH_3cm_water_pct", "RH_3cm_ice_corrected_pct"]


def parse_page(text, page_number):
    rows, errors = [], []
    for text_line, line in enumerate(text.splitlines(), 1):
        match = ROW_PATTERN.match(line.strip())
        if not match:
            if re.match(r"^\s*\d+\s+\d+/", line):
                errors.append({"page":page_number,"text_line":text_line,"reason":"row-like line not parsed"})
            continue
        number, t1, t2, rest = match.groups()
        try:
            tokens = rest.split()
            if len(tokens) not in [6,9]:
                raise ValueError("Expected 6 or 9 numeric columns")
            values = [float(x) for x in tokens]
            if not all(math.isfinite(x) for x in values):
                raise ValueError("Nonfinite/unrecognized missing code; stop for source review")
            stamp = datetime.strptime(t1, "%m/%d/%y %H:%M")
            stamp2 = datetime.strptime(t2, "%m/%d/%y %H:%M")
        except ValueError as exc:
            errors.append({"page":page_number,"text_line":text_line,"reason":str(exc)})
            continue
        rows.append({"row_id":int(number), "source_page":page_number, "source_page_row":len(rows)+1,
                     "source_text_line":text_line,"raw_time_1":t1,"raw_time_2":t2,"timestamp":stamp,
                     "timestamp_2":stamp2,"numeric_tokens":tokens,"values":values})
    return rows, errors


def validate_rows(rows, source):
    if [r["row_id"] for r in rows] != list(range(1, source["expected_records"]+1)):
        raise ValueError("Published row IDs are missing, repeated or reordered")
    if len({r["timestamp"] for r in rows}) != len(rows):
        raise ValueError("Duplicate first printed timestamp")
    if any(b["timestamp"]-a["timestamp"] != timedelta(hours=1) for a,b in zip(rows,rows[1:])):
        raise ValueError("First printed time not hourly contiguous")
    if any(r["timestamp_2"]-r["timestamp"] != timedelta(minutes=90) for r in rows):
        raise ValueError("Changed relation between two original printed clocks")


def read_eh(path, source):
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    from pypdf import PdfReader
    import pypdfium2 as pdfium
    if digest(path) != source["expected_sha256"]:
        raise ValueError("EH2 SHA-256 differs from Team1/Team2 handoff")
    reader = PdfReader(path)
    if len(reader.pages) != source["expected_pages"]:
        raise ValueError("Wrong PDF page count")
    rows, page_qa = [], []
    second_engine = pdfium.PdfDocument(str(path))
    first_header = reader.pages[0].extract_text().splitlines()[:2]
    try:
        for page_number, page in enumerate(reader.pages,1):
            parsed, errors = parse_page(page.extract_text(),page_number)
            if errors or not parsed:
                raise ValueError(f"Page {page_number} export failed: {errors}")
            # Reuse Team2's full dual-engine QA; independently check first/middle/last
            # of EACH exported page, now including the second printed time as well.
            other_page = second_engine[page_number-1]
            text_page = other_page.get_textpage()
            other_rows, other_errors = parse_page(text_page.get_text_range(),page_number)
            text_page.close(); other_page.close()
            other = {r["row_id"]:r for r in other_rows}
            checked = []
            for index in sorted({0,len(parsed)//2,len(parsed)-1}):
                current = parsed[index]
                alternate = other.get(current["row_id"])
                if alternate is None or any(current[k] != alternate[k] for k in ["timestamp","timestamp_2","values"]):
                    raise ValueError(f"Page {page_number}, row {current['row_id']} cross-engine export mismatch")
                checked.append(current["row_id"])
            page_qa.append({"page":page_number,"parsed_rows":len(parsed),"first_row":parsed[0]["row_id"],
                            "last_row":parsed[-1]["row_id"],"cross_engine_sample_row_ids":checked,
                            "sample_check":"both original times and all values agree",
                            "pypdf_parse_errors":errors,"pdfium_row_parse_errors":other_errors})
            rows.extend(parsed)
    finally:
        second_engine.close()
    validate_rows(rows,source)
    return rows, {"pages":len(reader.pages),"records":len(rows),"raw_header":first_header,"page_checks":page_qa,
                  "source": "Team2 bc9fe3c0 row regex/6-or-9 columns; no new inference method",
                  "prior_full_dual_engine_QA": "Team2 reports all 8922 rows; reused as attributed result",
                  "this_export_dual_engine_check": "First/middle/last of every one of 108 pages: both times and values",
                  "cross_engine_sample_n":sum(len(p["cross_engine_sample_row_ids"]) for p in page_qa),
                  "manual_visual_review": "Rendered pages 1,54,108 inspected: first/middle/last-page structure, header, negative signs, absent 3cm triad",
                  "first_time_1":rows[0]["timestamp"].isoformat(),"last_time_1":rows[-1]["timestamp"].isoformat(),
                  "time_1_label":"Time, GMT-07:00","time_2_label":"Local Time GMT-5:30","second_clock_minus_first_minutes":90,
                  "time_status":"Printed offsets consistent; UTC/solar-time meaning unverified, no conversion",
                  "missing_code":"3cm triad omitted after final published observation; retained as missing",
                  "qa_bits":None,"scale_factor":1,"add_offset":0,"calibration":"Published temperatures and raw/corrected RH retained; no recalibration or reapplication of Appendix correction",
                  "sensor_uncertainty": "EH1 Methods: temperature accuracy +/-0.21 degC for 0..50 degC, assumed by authors below zero; systematic offsets do not shrink with N",
                  "statistical_independence":"Hourly samples are autocorrelated; N is observed support, not independent replication"}


def to_tidy(rows, candidate, source):
    tidy = []
    for r in rows:
        values = r["values"]+[None]*(9-len(r["values"]))
        row = {"earth_candidate_id":candidate["earth_candidate_id"],"mars_candidate_id":candidate["mars_candidate_id"],
               "source_id":source["source_id"],"source_sha256":source["expected_sha256"],
               "source_page":r["source_page"],"source_page_row":r["source_page_row"],"source_text_line":r["source_text_line"],
               "published_row_id":r["row_id"],"raw_time_1":r["raw_time_1"],"raw_time_2":r["raw_time_2"],
               "time_1_printed_label":"Time, GMT-07:00","time_2_printed_label":"Local Time GMT-5:30",
               "time_1_naive":r["timestamp"].isoformat(),"time_2_naive":r["timestamp_2"].isoformat(),
               "timezone_status":"unresolved; no UTC conversion"}
        for name,val in zip(FIELDS,values):
            row[name] = val if val is not None else ""
            row[name+"__status"] = "not_published" if val is None else ("above_100_retained" if "RH_" in name and val>100 else "published_finite")
        tidy.append(row)
    return tidy


def observed_stats(values):
    return {"valid_n":len(values),"observed_mean":statistics.fmean(values) if values else "",
            "observed_min":min(values) if values else "","observed_max":max(values) if values else "",
            "observed_p05":percentile(values,.05) if values else "","observed_p95":percentile(values,.95) if values else ""}


def monthly_features(rows, candidate, source, version):
    features = []
    for start,end in months(datetime.fromisoformat(source["period_start"]),datetime.fromisoformat(source["period_end_exclusive"])):
        selected = [r for r in rows if start <= r["timestamp"] < end]
        expected = int((end-start).total_seconds()/3600)
        for index,name in enumerate(FIELDS+["T_3cm_minus_49cm_C"]):
            values = [r["values"][6]-r["values"][3] for r in selected if len(r["values"])==9] if index==9 else [r["values"][index] for r in selected if len(r["values"])>index]
            stat = observed_stats(values)
            features.append({"earth_candidate_id":candidate["earth_candidate_id"],"mars_candidate_id":candidate["mars_candidate_id"],
                "site_name":candidate["site_name"],"latitude_deg":candidate["latitude_deg"],"longitude_east_deg":candidate["longitude_east_deg"],
                "spatial_support":source["spatial_support"],"horizontal_datum":source["horizontal_datum"],"requirement_version":version,
                "candidate_purpose_version":candidate.get("requirements_version"),"source_id":source["source_id"],
                "source_sha256":source["expected_sha256"],"source_path":source["path"],"metric_id":name,
                "source_columns":"T_3cm_C;T_49cm_C" if index==9 else name,
                "operation":"same-row subtraction" if index==9 else "published value; identity scale",
                "unit":"percent" if "RH_" in name else "degC", "period_start":start.isoformat(),"period_end_exclusive":end.isoformat(),
                "time_axis":"first printed time, original label GMT-07:00; UTC unresolved", "native_interval_minutes":60,
                "output_interval":"calendar month; observed samples", "expected_n":expected,"timestamp_n":len(selected),
                **stat,"missing_n":expected-len(values),"coverage_fraction":len(values)/expected,
                "coverage_status":"complete_calendar_support" if len(values)==expected else ("partial_calendar_support" if values else "no_valid_data"),
                "above_100_n":sum(v>100 for v in values) if "RH_" in name else "",
                "threshold_status":"not_defined","annual_3cm_statistic":"not_computed","interpolation":"none",
                "dataset_doi":source["dataset_doi"]})
    return features


def window_summaries(rows, source):
    out = []
    windows = [("summer",source["summer_start"],source["summer_end_exclusive"],[0,3,6,9]),
               ("paper_year",source["period_start"],source["period_end_exclusive"],[0,3])]
    for label,start,end,indices in windows:
        selected = [r for r in rows if datetime.fromisoformat(start) <= r["timestamp"] < datetime.fromisoformat(end)]
        for index in indices:
            name = FIELDS[index] if index<9 else "T_3cm_minus_49cm_C"
            valid = [r for r in selected if len(r["values"])>index] if index<9 else [r for r in selected if len(r["values"])==9]
            values = [r["values"][index] for r in valid] if index<9 else [r["values"][6]-r["values"][3] for r in valid]
            out.append({"window":label,"metric_id":name,"period_start":start,"period_end_exclusive":end,
                        "time_axis":"first original printed timestamp; no UTC conversion","unit":"degC",
                        "expected_n":int((datetime.fromisoformat(end)-datetime.fromisoformat(start)).total_seconds()/3600),
                        **observed_stats(values),"interpretation":"descriptive reproduction of published data; no uncertainty shrinkage or causal claim"})
    return out


def plot_eh(rows, features, candidate, source, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    summer = [r for r in rows if datetime.fromisoformat(source["summer_start"]) <= r["timestamp"] < datetime.fromisoformat(source["summer_end_exclusive"]) and len(r["values"])==9]
    fig,axes = plt.subplots(2,1,figsize=(12,7.5),sharex=True,layout="constrained")
    times = [r["timestamp"] for r in summer]
    for index,label,color in [(6,"Soil 3 cm","#cf6c24"),(3,"Published ice-table probe 49 cm","#245e98")]:
        axes[0].plot(times,[r["values"][index] for r in summer],label=label,color=color,lw=.8)
    differences = [r["values"][6]-r["values"][3] for r in summer]
    axes[1].plot(times,differences,color="#725799",lw=.8)
    axes[1].axhline(0,color="grey",ls="--",lw=.7)
    axes[0].set(ylabel="Published temperature (degC)")
    axes[1].set(ylabel="3 cm minus 49 cm (degC)",xlabel="First printed time, label GMT-07:00; UTC and solar-time meaning unresolved")
    axes[0].legend(loc="lower left")
    for ax in axes:ax.grid(alpha=.2)
    difference_label = f"{statistics.fmean(differences):+.4f} degC" if differences else "unknown (no valid pairs)"
    if not summer:
        axes[0].text(.5,.5,"No common valid observations",transform=axes[0].transAxes,ha="center")
    fig.suptitle(f"{candidate['earth_candidate_id']} / {candidate['mars_candidate_id']} | Elephant Head station point\n"
                 f"{float(candidate['latitude_deg']):.7f} deg N, {float(candidate['longitude_east_deg']):.7f} deg E | 2017-12-01 to 2018-03-01 exclusive\n"
                 f"{len(summer)} same-row hourly pairs; observed mean difference {difference_label}",fontsize=11)
    fig.supxlabel("EH2 supplement to DOI 10.1017/S0954102019000269; Team2 parser/QA reused and exported.\n"
                  "Hourly point observations; no filling, interface inversion, drilling heat/ice-loss or Mars-performance result.",fontsize=9)
    directory=output/"figures";directory.mkdir(parents=True,exist_ok=True)
    fig.savefig(directory/"EARTH-002_paired_summer.png",dpi=160);plt.close(fig)
    fields = ["T_air_C","T_3cm_C","T_49cm_C"]
    matrix = [[100*r["coverage_fraction"] for r in features if r["metric_id"]==name] for name in fields]
    labels = [r["period_start"][:7] for r in features if r["metric_id"]==fields[0]]
    fig,ax=plt.subplots(figsize=(12,3.4),layout="constrained")
    hm=ax.imshow(np.asarray(matrix),vmin=0,vmax=100,cmap="YlGnBu",aspect="auto")
    ax.set(xticks=range(len(labels)),xticklabels=labels,yticks=range(3),yticklabels=["Air +0.82 m","Soil -0.03 m","Probe -0.49 m"])
    ax.tick_params(axis="x",rotation=35)
    for j,line in enumerate(matrix):
        for i,value in enumerate(line):ax.text(i,j,f"{value:.1f}",ha="center",va="center",color="white" if value>70 else "black",fontsize=9)
    fig.colorbar(hm,ax=ax,label="Valid / expected hourly samples (%)")
    ax.set_title("EARTH-002 | Monthly temperature coverage, first printed clock\nStation point (-79.8202167 N, -83.3143333 E); nominal depths, no spatial interpolation",fontsize=11)
    fig.supxlabel("Source EH2, DOI 10.1017/S0954102019000269; 3 cm series ends 2018-03-18 05:00.\nMissing winter values retained; no annual 3 cm statistic or suitability threshold.",fontsize=9)
    fig.savefig(directory/"EARTH-002_monthly_coverage.png",dpi=160);plt.close(fig)


def run_eh(root,candidate_path,profiles_path,candidate,source,config,output):
    started=time.perf_counter();output.mkdir(parents=True,exist_ok=True);path=root/source["path"]
    manifest=[{"source_id":source["source_id"],"candidate_id":candidate["earth_candidate_id"],"filename_or_product":path.name,
               "relative_path":source["path"],"source_url":source["url"],"publication_year":2019,"retrieval_date":"2026-11-14",
               "variables":";".join(FIELDS),"units":"temperature degC; RH percent","coordinates_grid":source["spatial_support"],
               "native_interval":"hourly point readings; two printed clocks","file_status":"present" if path.is_file() else "missing",
               "bytes":path.stat().st_size if path.is_file() else "","sha256":digest(path) if path.is_file() else "",
               "expected_sha256":source["expected_sha256"],"source_level":"published supplement; temperatures and raw/corrected RH, not unprocessed logger bytes"}]
    write_csv(output/"inputs_manifest.csv",manifest)
    if not path.is_file():raise FileNotFoundError("Real EH2 PDF absent; no numeric result generated")
    t=time.perf_counter();rows,qa=read_eh(path,source);parse_seconds=time.perf_counter()-t
    t=time.perf_counter();tidy=to_tidy(rows,candidate,source);features=monthly_features(rows,candidate,source,config["requirement_version"]);summary=window_summaries(rows,source);calc_seconds=time.perf_counter()-t
    # Verify export against Team2's reported reproduction at source precision.
    comparisons=[]
    for record in summary:
        key=record["window"]+":"+record["metric_id"]
        reference=source["team2_reference_means"][key]
        has_values = record["observed_mean"] != ""
        if has_values and abs(record["observed_mean"]-reference)>0.0001:
            raise ValueError(f"Mean differs from Team2 reference beyond published 4-decimal rounding: {key}")
        comparisons.append({"window_metric":key,"this_export_mean_C":record["observed_mean"],"team2_reported_mean_C":reference,
                            "tolerance_C":0.0001,"tolerance_reason":"Team2 report rounded to 4 decimals; transcription/reproduction only, not a suitability tolerance",
                            "comparison_status":"compared" if has_values else "no_valid_data",
                            "paper_table_II_mean_C":source["paper_table_II_means"].get(key,"not_listed"),
                            "paper_one_decimal_match":round(record["observed_mean"],1)==source["paper_table_II_means"][key] if has_values and key in source["paper_table_II_means"] else "not_evaluated"})
    write_csv(output/"station_observations.csv.gz",tidy);write_csv(output/"earth_candidate_features.csv",features)
    write_csv(output/"window_summaries.csv",summary);write_csv(output/"reference_comparison.csv",comparisons)
    # Per-page support is independently machine readable in addition to the JSON.
    write_csv(output/"page_qa.csv",[{**p,"cross_engine_sample_row_ids":";".join(map(str,p["cross_engine_sample_row_ids"]))} for p in qa["page_checks"]])
    t=time.perf_counter();plot_eh(rows,features,candidate,source,output);plot_seconds=time.perf_counter()-t
    for record in manifest:record.update(observation_start=qa["first_time_1"],observation_end=qa["last_time_1"],analysis_start=source["period_start"],analysis_end_exclusive=source["period_end_exclusive"])
    write_csv(output/"inputs_manifest.csv",manifest)
    three=[r for r in rows if len(r["values"])==9]
    qa.update(valid_3cm_records=len(three),last_valid_3cm_time_1=three[-1]["timestamp"].isoformat(),
              RH_49cm_corrected_above100_n=sum(r["values"][5]>100 for r in rows),missing_3cm_records=len(rows)-len(three),
              missing_3cm_policy="omitted temperature/raw RH/corrected RH are all blank; not zero or interpolated",
              fill_scale_offset="Published finite values retained, scale=1 offset=0; no finite sentinel documented in EH2 header")
    report={"schema_version":"1.0","generated_utc":datetime.now(timezone.utc).isoformat(),"requirement_version":config["requirement_version"],
            "candidate_contract":candidate,"source_profile":source,"source_sha256":digest(path),"qa":qa,
            "candidate_csv_sha256":digest(candidate_path),"profiles_sha256":digest(profiles_path),
            "processing_code_sha256":{p.name:digest(p) for p in sorted((root/"scripts/compute").glob("*.py"))},
            "execution":{"backend":"CPU","gpu_used":False,"numeric_precision":"Python binary64 / float64","speedup":None,
                         "read_parse_page_QA_seconds":parse_seconds,"table_calculation_seconds":calc_seconds,"figures_seconds":plot_seconds,
                         "data_transfer_seconds":None,"total_seconds":time.perf_counter()-started,
                         "timing_note":"Single local run, excluding source download and dependency setup; no measured GPU comparison"},
            "environment":inventory(root,include_files=False),"policy":{"UTC_conversion":"none","RH_clipping":"none",
            "interpolation":"none","annual_3cm":"not_computed","threshold_value":None,"threshold_status":"not_defined",
            "published_49cm_interface":"context for installed sensor, not new or independent held-out ice truth",
            "purpose_version_alignment":"MR-v2 execution accepted; Team1 original provisional purpose-version strings preserved, not silently rewritten",
            "LT_backup":"not_activated","novelty_and_scientific_interpretation":"Remain Main/Team1/Team2 responsibilities"}}
    (output/"qa_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+"\n")
    (output/"data_dictionary.json").write_text(json.dumps({"fields":source["variable_dictionary"],"provenance":"source_page (1-based), source_page_row (1-based data row within page), source_text_line (pypdf extracted text line, not geometric PDF coordinate), published_row_id (printed #)","time":"Both original labels and original strings retained. Naive ISO columns are parsing conveniences, not UTC.","missing":"Empty fields and not_published flags for omitted 3cm triad; no finite missing sentinel documented in inspected header.","units":"degC and percent per EH1 Methods/Table II. Heights/depths and sensor uncertainty are historical published metadata."},indent=2)+"\n")
    print(json.dumps({"candidate":candidate["earth_candidate_id"],"rows":len(rows),"summer_pairs":summary[0]["valid_n"],"backend":"CPU","seconds":report["execution"]["total_seconds"],"output":str(output)}))
    return report
