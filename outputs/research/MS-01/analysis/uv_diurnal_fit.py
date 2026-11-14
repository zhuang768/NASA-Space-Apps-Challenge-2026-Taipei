"""Descriptive 24 h attenuation example for University Valley, not a Mars inversion.

Requires numpy. From repository root run:
    python3 outputs/research/MS-01/analysis/uv_diurnal_fit.py
The input is the published, calibrated/good-only Campbell file from Zenodo
10.5281/zenodo.10553882. A restored legacy-snapshot copy is accepted as fallback.
No gap filling, Earth/Mars temperature subtraction, or ice-depth fit is performed.
"""
import argparse
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
REL = Path('data/raw/earth/university_valley/UniversityV_09_10_Campbell_data_good_only_calibrated.txt')
EXPECTED_MD5 = 'ae2133eac5c92c695c5f6ef93bcbbd25'


def analyze(source):
    data = source.read_bytes()
    assert hashlib.md5(data).hexdigest() == EXPECTED_MD5, 'Input differs from Zenodo v1 calibrated/good-only file'
    # The same warm interval examined by Marinova et al. (2022), p.153.
    # These are file timestamps; their timezone is not established here.
    start = datetime(2010, 11, 7)
    end = datetime(2010, 11, 18)
    lines = data.decode().splitlines()
    header = [s.strip() for s in next(csv.reader([lines[1]]))]
    columns = ['T107_surf', 'T107_10cm', 'T107_ice42cm', 'T107_InIce49cm']
    indices = [header.index(c) for c in columns]
    rows = []
    for row in csv.reader(lines[4:]):
        try:
            time = datetime.fromisoformat(row[0])
        except ValueError:
            time = datetime.strptime(row[0], '%m/%d/%Y %H:%M')
        if not start <= time < end:
            continue
        values = np.array([float(row[j]) for j in indices])
        if np.isfinite(values).all():
            rows.append((time, values))
    times = [t for t, _ in rows]
    assert len(times) == len(set(times)), 'Duplicate common-valid timestamps'
    assert times == sorted(times), 'Input is not chronologically ordered'
    hours = np.array([(t-start).total_seconds()/3600 for t in times])
    expected = int((end-start).total_seconds()/1800)
    assert len(rows) == expected == 528, 'Warm interval incomplete; revisit sampling and fit'
    assert np.allclose(np.diff(hours), .5), 'Sampling is not a continuous 30 min sequence'
    observations = np.array([v for _, v in rows])
    angle = 2*np.pi*hours/24
    design = np.array([np.ones(len(hours)), hours-hours.mean(), np.sin(angle), np.cos(angle)]).T
    coefficients, _, rank, _ = np.linalg.lstsq(design, observations, rcond=None)
    assert rank == 4
    # Element-wise sum avoids BLAS warnings on some host builds.
    residual = observations - np.sum(design[:, :, None]*coefficients[None, :, :], axis=1)
    try:
        relpath = str(source.relative_to(ROOT))
    except ValueError:
        relpath = str(source)
    result = {
        'source_file': relpath,
        'source_md5': hashlib.md5(data).hexdigest(),
        'source_sha256': hashlib.sha256(data).hexdigest(),
        'source_doi': '10.5281/zenodo.10553882',
        'source_version': 'v1, 2024-01-23',
        'source_columns': columns,
        'data_kind': 'this-study calculation from published processed in-situ measurements',
        'start_inclusive': start.isoformat(),
        'end_exclusive': end.isoformat(),
        'timestamp_timezone': 'not established from file; no absolute local-time phase interpretation',
        'common_valid_samples': len(rows),
        'expected_half_hour_samples': expected,
        'spatial_support': 'University Valley weather-station soil column, -77.86215,160.7101; no area average',
        'model': 'T=intercept+linear_time+bsin*sin(2*pi*t/24h)+bcos*cos(2*pi*t/24h)',
        'method': 'Ordinary least squares; amplitude=sqrt(bsin^2+bcos^2), not peak-to-peak',
        'limits': ['descriptive fit only; residuals include weather/other frequencies',
                   'uncertainty not estimated; no significance claim',
                   'cannot infer MS-01 ice depth or thermal inertia',
                   'surface sensors may have wind exposure and radiative bias'],
        'values': []
    }
    for j, (column, depth) in enumerate(zip(columns, [0, .1, .42, .49])):
        result['values'].append({
            'column': column,
            'depth_m': depth,
            'min_C': float(observations[:, j].min()),
            'max_C': float(observations[:, j].max()),
            'diurnal_amplitude_K': float(np.hypot(coefficients[2, j], coefficients[3, j])),
            'linear_trend_K_per_h': float(coefficients[1, j]),
            'residual_rmse_K': float(np.sqrt(np.mean(residual[:, j]**2)))
        })
    return result


def main():
    default_source = ROOT / REL
    if not default_source.exists():
        default_source = ROOT / 'outputs/handoff/legacy_snapshot' / REL
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=default_source)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    result = analyze(args.source.resolve())
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(f'Verified source MD5 and {result["common_valid_samples"]} common-valid samples; wrote {args.output}')


if __name__ == '__main__':
    main()
