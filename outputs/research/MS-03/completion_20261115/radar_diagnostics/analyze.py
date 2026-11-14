"""Bounded peak-index diagnostics, never reflector picks or an ice classifier."""
from pathlib import Path
import argparse, csv, hashlib, json, math
import numpy as np

PINNED_MAIN = '234e58a8a0a0a9966e97e1b13d7ccc587cf3e8aa'
EXPECTED_INPUT_SHA256 = 'ac36e98d8af635bf1078ac7689005e490b09f2d765a7e60aa170a24b266c095c'
OUT = Path(__file__).resolve().parent

def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w=csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator='\n')
        w.writeheader(); w.writerows(rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path)
    a=p.parse_args()
    source=a.input or OUT.parent.parent/'local_validation/gap_completion/radar_local_arrays.npz'
    raw=source.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    assert digest==EXPECTED_INPUT_SHA256, 'Input changed: inspect the scientific revision before updating the checksum.'
    x=np.load(source);obs=x['observed'];sim=x['simulated'];r=x['row_0based'];col=x['column_1based'];n=x['nadir'];first=x['first']
    assert obs.shape==sim.shape==(269,65)
    assert np.isfinite(obs).all() and np.isfinite(sim).all() and (obs>=0).all() and (sim>=0).all()
    # A maximum index is only a descriptive statistic over this cropped delay window.
    imax=np.argmax(obs,axis=0);smax=np.argmax(sim,axis=0)
    peak=r[imax];speak=r[smax];off=peak-n
    rows=[]
    for i,c in enumerate(col):
        nd=int(n[i]-r[0]);fr=int(first[i]-r[0]);assert 0<=nd<len(r) and 0<=fr<len(r)
        # Model-nadir power rank is a crop-relative rank, not an SNR or confidence.
        rank=100*float(np.count_nonzero(obs[:,i]<=obs[nd,i]))/len(r)
        rows.append(dict(column_1based=int(c),observed_crop_max_row_0based=int(peak[i]),
          model_nadir_row_0based=int(n[i]),model_first_return_row_0based=int(first[i]),
          simulated_crop_max_row_0based=int(speak[i]),
          observed_crop_max_minus_model_nadir_samples=int(off[i]),
          observed_crop_max_minus_model_nadir_us=float(off[i]*.0375),
          max_row_change_from_previous_column_samples=None if i==0 else int(peak[i]-peak[i-1]),
          model_nadir_observed_crop_percentile=rank,
          interpretation='descriptive_indices_only; not_surface_or_subsurface_pick'))
    write_csv(OUT/'radar_pick_diagnostic.csv',rows)
    d=np.diff(peak)
    summary=dict(pinned_main=PINNED_MAIN,input_path='outputs/research/MS-03/local_validation/gap_completion/radar_local_arrays.npz',
      input_sha256=digest,product_id='S_04624502_RGRAM',columns=65,adjacent_column_pairs=64,
      source_rows_0based=[int(r[0]),int(r[-1])],source_columns_1based=[int(col[0]),int(col[-1])],
      observed_max_minus_model_nadir_sample_quantiles=dict(zip(['min','q25','median','q75','max'],map(float,np.percentile(off,[0,25,50,75,100])))),
      observed_max_before_at_after_model_nadir=[int(sum(off<0)),int(sum(off==0)),int(sum(off>0))],
      observed_adjacent_max_jump_samples_min_max=[int(d.min()),int(d.max())],
      observed_adjacent_max_abs_jump_gt10_count=int(sum(abs(d)>10)),
      observed_adjacent_max_abs_jump_gt100_count=int(sum(abs(d)>100)),
      jump_thresholds='10 and100 samples are descriptive thresholds, not detection criteria',
      observed_max_at_crop_edge_count=int(sum((peak==r[0])|(peak==r[-1]))),
      simulated_max_minus_model_nadir_sample_quantiles=dict(zip(['min','q25','median','q75','max'],map(float,np.percentile(speak-n,[0,25,50,75,100])))),
      simulation_is_model_not_independent_observation=True,
      conclusion='Global crop argmax is not an independently validated surface or subsurface track. Large index changes and model disagreement cannot be uniquely assigned to geology, processing, ionosphere, sidelobes or clutter here.',
      inference_limits=['No time alignment or correction','No amplitude subtraction','No delay-to-local-depth conversion','No inferred dielectric constant','No calibrated SNR or detection limit','No ice presence/absence result'])
    (OUT/'radar_diagnostic_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    # Ideal bandwidth-limited support: no claim to a calibrated local impulse response.
    c=299792458.;B=10e6;dt=.0375e-6;h=.10
    support=[]
    for eps,scope in [(1.,'vacuum reference'),(3.15,'illustrative pure-water-ice assumption; not MS-03 measurement')]:
        speed=c/math.sqrt(eps)
        support.append(dict(relative_permittivity_assumed=eps,assumption=scope,
          sample_interval_ns=dt*1e9,one_way_distance_per_sample_m=speed*dt/2,
          bandwidth_MHz=B/1e6,ideal_one_way_bandwidth_resolution_m=speed/(2*B),
          trial_interface_depth_m=h,trial_round_trip_delay_ns=2*h/speed*1e9,
          trial_delay_samples=2*h/(speed*dt),
          bandwidth_resolution_divided_by_trial_depth=speed/(2*B*h),
          scope='homogeneous nondispersive nonmagnetic medium; separability scale only; not detection probability'))
    write_csv(OUT/'range_support.csv',support)
    # Separate independent coding path verifies all maxima and delays, not scientific truth.
    manual=np.array([int(r[max(range(len(r)),key=lambda j:float(obs[j,i]))]) for i in range(65)])
    checks=dict(input_hash=digest==EXPECTED_INPUT_SHA256,all65_maxima_independently_recomputed=bool(np.array_equal(manual,peak)),
      no_source_mutation=hashlib.sha256(source.read_bytes()).hexdigest()==digest,
      first_row_missing_previous_jump=rows[0]['max_row_change_from_previous_column_samples'] is None,
      negative_delay_retained=bool(np.any(off<0)),positive_delay_retained=bool(np.any(off>0)),
      vacuum_bandwidth_resolution_near15m=abs(support[0]['ideal_one_way_bandwidth_resolution_m']-15)<.02,
      counts_partition65=sum(summary['observed_max_before_at_after_model_nadir'])==65,
      no_depth_column_in_peak_table=not any('depth' in k for k in rows[0]))
    assert all(checks.values())
    (OUT/'validation.json').write_text(json.dumps(dict(checks=checks,passed=len(checks),scientific_validation=False),indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
