"""Offline, dependency-free CTX nominal footprint/time support audit.

Run from any directory with Python >=3.8. Reads the pinned product_footprints.csv.
This does not register images, detect change, or classify surface morphology.
"""
import csv
import datetime as dt
import hashlib
import itertools
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "local_validation" / "product_footprints.csv"
RADIUS_M = 3396190.0
ROI = [(168.0, 52.5), (168.5, 52.5), (168.5, 53.0), (168.0, 53.0)]
BASE_SHA = "521740108050ba16e406f8becb67a786179ff8bd"


def orient(poly):
    signed = sum(a[0] * b[1] - a[1] * b[0]
                 for a, b in zip(poly, poly[1:] + poly[:1]))
    return poly if signed > 0 else list(reversed(poly))


def clip(subject, convex_clip):
    """Sutherland-Hodgman in lon/lat, matching the source WKT edge model."""
    out = subject[:]
    for a, b in zip(convex_clip, convex_clip[1:] + convex_clip[:1]):
        inp, out = out, []
        if not inp:
            break
        def side(p):
            return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
        for u, v in zip(inp, inp[1:] + inp[:1]):
            du, dv = side(u), side(v)
            iu, iv = du >= -1e-13, dv >= -1e-13
            if iu != iv:
                t = du/(du-dv)
                out.append((u[0]+t*(v[0]-u[0]), u[1]+t*(v[1]-u[1])))
            if iv:
                out.append(v)
    return out


def spherical_area(poly):
    """Exact surface integral for polygon edges linear in lon and lat.

    A = -R^2 integral(sin(phi) d(lambda)); edges follow supplied lon/lat
    segments, not great circles. The ROI edges are parallels/meridians.
    """
    terms = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        la, pa, lb, pb = map(math.radians, (a[0], a[1], b[0], b[1]))
        dp = pb-pa
        # Stable even for near-horizontal clipping edges: avoid subtracting cosines.
        h = dp/2
        mean_sine = math.sin((pa+pb)/2) * (math.sin(h)/h if h else 1.0)
        terms.append((lb-la)*mean_sine)
    return abs(math.fsum(terms))*RADIUS_M**2


def laea_area(poly):
    """Independent legacy projection reproduction, same vertices as old script."""
    l0, p0 = map(math.radians, (168.25, 52.75))
    coords = []
    for lon, lat in poly:
        l, p = map(math.radians, (lon, lat))
        k = math.sqrt(2/(1+math.sin(p0)*math.sin(p)+math.cos(p0)*math.cos(p)*math.cos(l-l0)))
        coords.append((RADIUS_M*k*math.cos(p)*math.sin(l-l0),
                       RADIUS_M*k*(math.cos(p0)*math.sin(p)-math.sin(p0)*math.cos(p)*math.cos(l-l0))))
    return abs(math.fsum(a[0]*b[1]-a[1]*b[0]
                        for a,b in zip(coords, coords[1:]+coords[:1])))/2


def read_ctx():
    rows = [r for r in csv.DictReader(SOURCE.open(encoding="utf-8-sig")) if r["catalog"] == "CTX_EDR"]
    for r in rows:
        points = [tuple(map(float, p.split())) for p in
                  re.findall(r"(-?\d+\.?\d*\s-?\d+\.?\d*)", r["footprint_wkt"])]
        assert points[0] == points[-1]
        r["poly"] = orient(points[:-1])
        # Convexity is a prerequisite for clipping, checked from actual inputs.
        v = r["poly"]
        cross = [(v[(i+1)%len(v)][0]-v[i][0])*(v[(i+2)%len(v)][1]-v[(i+1)%len(v)][1])-
                 (v[(i+1)%len(v)][1]-v[i][1])*(v[(i+2)%len(v)][0]-v[(i+1)%len(v)][0]) for i in range(len(v))]
        assert min(cross) >= -1e-12
        r["roi_poly"] = clip(r["poly"], ROI)
    assert len(rows) == 5
    return rows


def csv_write(name, rows):
    with (HERE/name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    rows = read_ctx()
    roi_area = spherical_area(ROI)
    legacy_area = laea_area(ROI)
    individual, pairs = [], []
    for r in rows:
        a = spherical_area(r["roi_poly"])
        individual.append(dict(product_id=r["product_id"], utc_start=r["utc_start"], utc_stop=r["utc_stop"],
                               nominal_overlap_km2=a/1e6, nominal_roi_fraction=a/roi_area,
                               incidence_deg=r["incidence_deg"], solar_longitude_deg=r["solar_longitude_deg"],
                               native_m_px=r["map_scale_m_px"], source_url=r["source_url"],
                               support_type="catalogue footprint; not validated image pixels"))
    for a,b in itertools.combinations(rows,2):
        common = clip(a["roi_poly"], b["poly"])
        area = spherical_area(common)
        elapsed = (dt.datetime.fromisoformat(b["utc_start"])-dt.datetime.fromisoformat(a["utc_start"])).total_seconds()/86400
        ls = abs(float(a["solar_longitude_deg"])-float(b["solar_longitude_deg"]))%360
        pairs.append(dict(product_a=a["product_id"], product_b=b["product_id"],
                          utc_start_a=a["utc_start"], utc_start_b=b["utc_start"],
                          elapsed_earth_days=abs(elapsed), elapsed_earth_julian_years=abs(elapsed)/365.25,
                          common_nominal_area_km2=area/1e6, common_nominal_roi_fraction=area/roi_area,
                          absolute_incidence_difference_deg=abs(float(a["incidence_deg"])-float(b["incidence_deg"])),
                          circular_solar_longitude_difference_deg=min(ls,360-ls),
                          interpretation="geometry/time support only; no image registration or detected surface change"))
    # Intersections of j polygons underpin an exact inclusion/exclusion count audit.
    sj = {j:0.0 for j in range(1,6)}
    for j in sj:
        vals=[]
        for combo in itertools.combinations(rows,j):
            p=ROI[:]
            for r in combo:p=clip(p,r["poly"])
            vals.append(spherical_area(p))
        sj[j]=math.fsum(vals)
    at_least={k:math.fsum((-1)**(j-k)*math.comb(j-1,k-1)*sj[j] for j in range(k,6))
              for k in range(1,6)}
    exact={k:at_least[k]-at_least.get(k+1,0) for k in at_least}
    csv_write("ctx_individual_support.csv",individual)
    csv_write("ctx_pair_support.csv",pairs)
    csv_write("ctx_coverage_multiplicity.csv",[
        dict(number_of_epochs=k,at_least_area_km2=at_least[k]/1e6,at_least_roi_fraction=at_least[k]/roi_area,
             exactly_area_km2=exact[k]/1e6,exactly_roi_fraction=exact[k]/roi_area,
             interpretation="catalogue nominal support, not registered usable pixels") for k in at_least])
    legacy_errors=[abs(laea_area(r["roi_poly"])/legacy_area-float(r["roi_area_fraction"])) for r in rows]
    min_time=min(r["utc_start"] for r in rows);max_time=max(r["utc_start"] for r in rows)
    result=dict(base_sha=BASE_SHA,source_path=str(SOURCE.relative_to(HERE.parents[4])),
                source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                roi_bounds_lon_lat=[168,52.5,168.5,53],sphere_radius_m=RADIUS_M,
                roi_spherical_area_km2=roi_area/1e6,legacy_laea_vertex_area_km2=legacy_area/1e6,
                geometric_model="straight source WKT segments in longitude/latitude; spherical surface integral",
                product_count=len(rows),pair_count=len(pairs),earliest_utc=min_time,latest_utc=max_time,
                nominal_union_fraction=at_least[1]/roi_area,nominal_repeat_fraction=at_least[2]/roi_area,
                maximum_legacy_fraction_error=max(legacy_errors),
                actual_valid_image_fraction=None,actual_change_rate=None,hydrogen_weh_wt_percent=None,
                uncertainties="ODE footprint approximation/rounding and effective image masks unquantified; no local WEH map fetched",
                scientific_status="nominal repeat geometry quantified; calibrated morphology/change and MONS WEH remain unclosed")
    (HERE/"support_summary.json").write_text(json.dumps(result,indent=2)+"\n")
    # Published mapping scale is a model property, never a local hydrogen value.
    mons=dict(source_doi="10.1016/j.icarus.2017.09.031",source_locator="Appendix, pp114-115, Eq A2 discussion",
              instrument_fwhm_km_approx=550,adopted_spherical_harmonic_order=16,
              longitudinal_half_wavelength_deg=360/(2*16),
              paper_radius_km=3390,
              longitudinal_half_wavelength_km=math.radians(360/(2*16))*3390,
              roi_north_south_km=math.radians(0.5)*RADIUS_M/1000,
              roi_east_west_at_center_km=math.radians(0.5)*RADIUS_M/1000*math.cos(math.radians(52.75)),
              local_weh_wt_percent=None,local_weh_uncertainty=None,local_areal_density_g_cm2=None,
              numerical_table_required="published supplemental Table S1 (N16); Table S2 for undeconvolved comparison",
              status="primary method located/read; numerical supplementary table not acquired",
              limit="N16 half-wavelength is not FWHM and is not a new local measurement; no WEH estimated from a coloured map or SWIM consistency")
    (HERE/"mons_scale_constraints.json").write_text(json.dumps(mons,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
