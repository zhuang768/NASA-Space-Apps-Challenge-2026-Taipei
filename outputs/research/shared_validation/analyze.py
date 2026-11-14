"""Offline source checks and limited calculations; no Mars inversion or clock repair.

Run: MPLCONFIGDIR=/tmp/shared_mpl .venv/bin/python outputs/research/shared_validation/analyze.py
Requires numpy and matplotlib. All five Caltech files are preserved, two losslessly gzipped.
The paper 3-ppd raster is NOT reconstructed from the 2-ppd archive.
"""
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
INPUT = HERE / "inputs"
DOI = "https://doi.org/10.22002/D1.1316"
LAB = "https://doi.org/10.1029/2011JE003938"


def write_csv(name, rows):
    with (HERE / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def archive_bytes(name):
    p = INPUT / name
    return p.read_bytes() if p.exists() else gzip.decompress((INPUT / (name + ".gz")).read_bytes())


def run():
    record = json.loads((INPUT / "current_caltech_record.json").read_text())
    versions = json.loads((INPUT / "current_caltech_versions.json").read_text())
    checks = []
    for name, info in record["files"]["entries"].items():
        data = archive_bytes(name)
        checks.append({"check": "archive_md5:" + name,
                       "pass": "md5:" + hashlib.md5(data).hexdigest() == info["checksum"],
                       "detail": "uncompressed bytes=" + str(len(data))})
        assert checks[-1]["pass"], name
        assert len(data) == info["size"]
    lat = np.loadtxt(io.BytesIO(archive_bytes("Lat.ascii"))).ravel()
    lon = np.loadtxt(io.BytesIO(archive_bytes("Lon.ascii"))).ravel()
    depth = np.loadtxt(io.BytesIO(archive_bytes("d_m.ascii")))
    ti = np.loadtxt(io.BytesIO(archive_bytes("TI_SI.ascii")))
    assert depth.shape == ti.shape == (360, 720)
    assert np.allclose(np.diff(lat), -.5) and np.allclose(np.diff(lon), .5)
    assert versions["hits"]["total"] == 1 and record["metadata"]["version"] == "1.0"
    checks.append({"check": "archive_shape_coordinates_versions", "pass": True,
                   "detail": "360 latitude rows x 720 longitude columns; 0.5 degree; one listed version 1.0"})
    rows = []
    # Fixed nominal rectangles, not selected from a later geography or literature hit.
    for sid, y, x in [("MS-01", 56.75, 72.75), ("MS-02", 52.75, 168.25), ("MS-03", 57.75, 242.25)]:
        iy = np.flatnonzero(np.isclose(lat, y, atol=1e-9, rtol=0))
        ix = np.flatnonzero(np.isclose(lon, x, atol=1e-9, rtol=0))
        assert len(iy) == len(ix) == 1
        i, j = int(iy[0]), int(ix[0])
        assert depth[i, j] != -32768 and ti[i, j] != -32768
        rows.append(dict(site=sid,latitude_deg_N=y,longitude_deg_E=x,
                         south_deg_N=y-.25,north_deg_N=y+.25,west_deg_E=x-.25,east_deg_E=x+.25,
                         row_1based=i+1,column_1based=j+1,
                         conditional_depth_m=float(depth[i,j]),dry_layer_TI_J_m_minus2_K_minus1_s_minushalf=float(ti[i,j]),
                         value_type="published model product; independently re-indexed this round",
                         source_url=DOI,locator=f"d_m.ascii and TI_SI.ascii row {i+1}, column {j+1}",
                         period="13+ years MCS per paper; cell dates not supplied in five-file archive",
                         depth_basis="assumed frozen-H2O lower layer; not direct interface measurement",
                         resolution="2 ppd output; one 0.5-degree cell; observation footprint differs",
                         local_RMS_K="",local_depth_CI_m="",local_obs_count="",
                         missing_reason="not present in five released archive files; SI not downloaded",
                         transfer_3ppd="unknown; no interpolation or inferred transformation"))
    write_csv("native_model_cells.csv", rows)

    station_rows = list(csv.DictReader((INPUT / "station_metadata.csv").open()))
    # Great-circle separation is diagnostic only, not a label correction or a GPS error estimate.
    r = next(x for x in station_rows if x["station"] == "S8")
    a,b,c,d = map(float,[r["paper_latitude"],r["paper_longitude"],r["deployment2009_latitude"],r["deployment2009_longitude"]])
    dy,dx=math.radians(c-a),math.radians(d-b)
    h=math.sin(dy/2)**2+math.cos(math.radians(a))*math.cos(math.radians(c))*math.sin(dx/2)**2
    separation=6371008.8*2*math.asin(math.sqrt(h))
    write_csv("uv_coordinate_crosswalk.csv", [dict(**r,
                  coordinate_pair_separation_m=(separation if r["station"] in ["S8","D36"] else ""),
                  separation_kind="calculation on mean-radius sphere; not survey accuracy",
                  label_resolution="unresolved; use serial and channel for data identity") for r in station_rows])

    # Re-check arithmetic of a prior MS-03 audit. Original full logger export was not re-read here.
    audit=json.loads((INPUT / "outputs__research__MS-03__uv_w__campbell_clock_audit.json").read_text())
    before=float(audit["last_before"][1]); after=float(audit["first_after"][1])
    step=(after-before)*1440
    assert math.isclose(step,audit["decimal_boundary_step_minutes"],abs_tol=1e-7)
    assert audit["correction_applied"] is False
    checks.append({"check":"previous_clock_audit_arithmetic_only", "pass":True,
                   "detail":f"decimal boundary {step:.6f} min vs printed {audit['printed_boundary_step_minutes']} min; no raw re-audit/alignment"})

    lab=list(csv.DictReader((HERE/"lab_runs.csv").open()))
    vapor=[r for r in lab if r["class"]=="glass_beads_vapor"]
    assert len(vapor)==8 and all(0<=float(r["F_min_pct"])<=float(r["F_max_pct"])<=100 for r in vapor)
    f=np.arange(0, .751, .01)
    # Evaluation of a published regression, NOT new experimental points or a fit to UV/Mars.
    write_csv("published_regression_evaluation.csv",[dict(
        pore_filling_fraction=float(x),published_lambda_z_W_m_K=float(.876*x+.0752),
        source_url=LAB,locator="PDF p14 para73; Figure11",temperature_reference_K=237,
        type="this round evaluation of published regression; not new measurement",
        uncertainty="not supplied here; slope +/-0.058 is not a full prediction interval",
        applicability="500-600 micrometre glass beads; vapor runs; excludes F=1 liquid-frozen samples") for x in f])
    fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout="constrained")
    ax=axes[0]
    for r in vapor:
        t=float(r["duration_h"]);lo=float(r["F_min_pct"]);hi=float(r["F_max_pct"])
        ax.vlines(t,lo,hi,color="#28688e",lw=3);ax.scatter([t,t],[lo,hi],color="#28688e",s=16)
    ax.set(xscale="log",xlabel="Vapor deposition duration (h; logarithmic)",ylabel="Original pore volume occupied by ice (%)",
           title="A. Published ranges across sampled layers")
    ax.text(.03,.97,"Table 1: ranges are NOT confidence intervals\nIndependent ice content: sample mass loss",transform=ax.transAxes,va="top",fontsize=9)
    ax.set_ylim(-3,100);ax.grid(alpha=.2)
    ax=axes[1];ax.plot(f,.876*f+.0752,color="#b15d27",lw=2)
    ax.set(xlabel="Ice pore-filling fraction F (not bulk ice fraction)",ylabel="Vertical conductivity (W m$^{-1}$ K$^{-1}$)",
           title="B. Evaluation of a published regression")
    ax.text(.03,.97,"lambda_z = 0.876 F + 0.0752; reference 237 K\nNo new fit; no prediction interval",transform=ax.transAxes,va="top",fontsize=9)
    ax.text(.03,.05,"Glass beads, CO2 near 6 mbar\nNOT a UV or Mars ice-depth calibration\nF = 1 liquid-frozen samples excluded",transform=ax.transAxes,fontsize=9,
            bbox=dict(facecolor="white",edgecolor="none",alpha=.9))
    ax.grid(alpha=.2);fig.suptitle("Laboratory control evidence and its limits | Siegler et al. (2012), doi:10.1029/2011JE003938",fontsize=11)
    fig.savefig(HERE/"laboratory_control.png",dpi=180);fig.savefig(HERE/"laboratory_control.svg");plt.close(fig)
    result={"checks":checks,"native_cells":3,"raw_UV_time_series_recomputed":False,
            "coordinate_conflict_separation_m":separation,"clock_boundary_arithmetic_min":step,
            "laboratory_vapor_runs_transcribed":len(vapor),"new_laboratory_measurements":False,
            "new_Mars_model_fit":False,"scientific_gaps_solved_by_passing_checks":False}
    (HERE/"analysis_checks.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))


if __name__=="__main__":
    run()
