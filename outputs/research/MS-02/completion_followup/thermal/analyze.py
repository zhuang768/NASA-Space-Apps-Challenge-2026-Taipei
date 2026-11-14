"""MS-02 native thermal product support audit; no inversion or uncertainty fit.

Usage: python3 analyze.py --source-dir /path/to/shared_validation/inputs
Source files are the five-file CaltechDATA release doi:10.22002/D1.1316.
Only 81 native sample values are exported; no global source is redistributed.
"""
import argparse
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RADIUS_M = 3396190.0
EXPECTED_MD5 = {
    'Lat.ascii': '9b70d4b2f0297594ce7e02494cf8564b',
    'Lon.ascii': 'c60b8ff5f8b0bc603c92967862ad7431',
    'Notes.txt': '931c03a665d02755470be11becf7841b',
    'TI_SI.ascii': '267810eb52f6c053dd2adefe4dc2010a',
    'd_m.ascii': '080dd616a822fa74f20f4c923a1d79f1',
}


def write_csv(name, rows):
    with (ROOT / name).open('w', newline='', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def area(south, north, west, east):
    return RADIUS_M ** 2 * math.radians(east - west) * (
        math.sin(math.radians(north)) - math.sin(math.radians(south)))


def published_pq19_consistency(depth_m):
    """2026 paper sec3.3 rule, NOT independently acquired SWIM release pixel."""
    return min(1.0, max(0.0, (0.5 - depth_m) / 0.2))


def run(source_dir):
    arrays, receipts = {}, []
    for name, expected in EXPECTED_MD5.items():
        path = source_dir / name
        compressed = not path.exists()
        if compressed:
            path = source_dir / (name + '.gz')
        raw = gzip.decompress(path.read_bytes()) if compressed else path.read_bytes()
        md5 = hashlib.md5(raw).hexdigest()
        assert md5 == expected, (name, md5, expected)
        receipts.append(dict(name=name, source_url='https://data.caltech.edu/api/records/ym7fc-x0r93/files/' + name + '/content',
                             decoded_bytes=len(raw), md5=md5, sha256=hashlib.sha256(raw).hexdigest(),
                             expected_md5=expected, checksum_pass=True))
        if name.endswith('.ascii'):
            arrays[name] = np.loadtxt(io.BytesIO(raw))
    lat, lon = arrays['Lat.ascii'], arrays['Lon.ascii']
    depth, ti = arrays['d_m.ascii'], arrays['TI_SI.ascii']
    assert depth.shape == ti.shape == (len(lat), len(lon)) == (360, 720)
    assert np.allclose(np.diff(lat), -0.5) and np.allclose(np.diff(lon), 0.5)
    r = int(np.flatnonzero(lat == 52.75)[0])
    c = int(np.flatnonzero(lon == 168.25)[0])
    cells = []
    for rr in range(r - 4, r + 5):
        for cc in range(c - 4, c + 5):
            d, t = float(depth[rr, cc]), float(ti[rr, cc])
            valid = math.isfinite(d) and math.isfinite(t) and d != -32768 and t != -32768
            cells.append(dict(row_zero_based=rr, column_zero_based=cc, latitude_deg_N=float(lat[rr]),
                              longitude_deg_E=float(lon[cc]), conditional_depth_m=d,
                              dry_layer_TI_J_m_minus2_K_minus1_s_minushalf=t,
                              both_valid=valid, chebyshev_cell_radius=max(abs(rr-r),abs(cc-c)),
                              spherical_cell_area_m2=area(lat[rr]-0.25, lat[rr]+0.25, lon[cc]-0.25, lon[cc]+0.25),
                              PQ19_component_by_published_2026_rule=published_pq19_consistency(d) if valid else None))
    write_csv('native_cells_9x9.csv', cells)
    summaries = []
    for radius in (0, 1, 2, 4):
        selected = [x for x in cells if x['chebyshev_cell_radius'] <= radius]
        valid = [x for x in selected if x['both_valid']]
        for field in ('conditional_depth_m', 'dry_layer_TI_J_m_minus2_K_minus1_s_minushalf'):
            values = np.asarray([x[field] for x in valid])
            weights = np.asarray([x['spherical_cell_area_m2'] for x in valid])
            mean = np.average(values, weights=weights)
            sd = np.sqrt(np.average((values-mean)**2, weights=weights))
            centre = depth[r,c] if field == 'conditional_depth_m' else ti[r,c]
            summaries.append(dict(window_side_cells=2*radius+1, quantity=field,
                                  nominal_N=len(selected), valid_N=len(valid),
                                  minimum=float(values.min()), maximum=float(values.max()),
                                  median=float(np.median(values)), unweighted_mean=float(values.mean()),
                                  area_weighted_mean=float(mean), area_weighted_population_SD=float(sd),
                                  centre_value=float(centre), centre_minus_area_weighted_mean=float(centre-mean),
                                  interpretation='spatial variation of released conditional model; NOT error/CI/independent observations'))
    write_csv('spatial_support_summary.csv', summaries)
    geometry = dict(
        radius_m=RADIUS_M, coordinate_convention='planetocentric latitude; east-positive longitude',
        row_zero_based=r, column_zero_based=c, centre_latitude_deg_N=float(lat[r]), centre_longitude_deg_E=float(lon[c]),
        south_deg_N=52.5, north_deg_N=53.0, west_deg_E=168.0, east_deg_E=168.5,
        exact_spherical_cell_area_km2=area(52.5,53,168,168.5)/1e6,
        north_south_meridian_length_km=RADIUS_M*math.radians(0.5)/1000,
        east_west_parallel_length_at_centre_km=RADIUS_M*math.cos(math.radians(52.75))*math.radians(0.5)/1000,
        nominal_output_spacing_deg=0.5, paper2019_MCS_observation_binning_spacing_deg=1/3,
        paper2026_PQ19_native_output_spacing_deg=0.5,
        paper2026_output_spacing_locator='Sizemore2026 sec3.1/4.1 and Figure4 caption; upsampled BF08 and SWIM23 to PQ19 0.5deg grid',
        ratio_of_degree_cell_areas_2ppd_to_3ppd=2.25,
        same_pixel_conclusion='published 2019 3ppd MCS observation bins and released2ppd output refer to different supports/stages; 2026 explicitly confirms PQ19 output0.5deg; exact processing-stage lineage remains unverified',
        finite_depth=float(depth[r,c]), dry_layer_TI=float(ti[r,c]),
        model_depth_exceeds_0p30m_sensitivity_context=bool(depth[r,c]>0.3),
        PQ19_component_by_published_2026_rule=published_pq19_consistency(float(depth[r,c])),
        rule_status='reimplementation of 2026 sec3.3 scalar rule on published PQ19 depth; not a retrieved SWIM2 pixel or combined value or ice probability',
        combined_thermal_consistency=None,
        combined_missing_reason='local BF08 and SWIM23 depth/components plus exact release identity/masks absent',
        published_thermal_component_weights={'PQ19':1/3,'BF08':1/3,'SWIM23':1/3},
        published_weights_source='Sizemore2026 sec3.3; publication scheme is now known; actual per-pixel implementation/version mapping still unverified',
        sensitivity_context_source='Sizemore2026 DOI10.3847/PSJ/ae7b38 abstract and Figure13; broad sensitivity limitation, not MS02 calibrated error',
        local_observation_count=None, local_RMS_K=None, local_depth_CI_m=None,
        unavailable_diagnostics_reason='not supplied in five-file release; source3ppd stage product/transformation and per-cell measurements/residuals absent; published thermal weights now known but local components/masks/release implementation not verified',
        source_md5_pass_N=len(receipts), source_md5_total_N=len(EXPECTED_MD5),
    )
    (ROOT/'support_audit.json').write_text(json.dumps(geometry,indent=2)+'\n')
    (ROOT/'source_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
    print(json.dumps({'MD5_pass':len(receipts),'centre_row_col':[r,c],
                      'area_km2':geometry['exact_spherical_cell_area_km2'],
                      'cells_exported':len(cells),'summary_rows':len(summaries)}))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-dir', required=True, type=Path)
    run(parser.parse_args().source_dir)
