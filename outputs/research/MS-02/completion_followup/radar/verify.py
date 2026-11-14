"""Independent checks of the diagnostic table against delivered ROI inputs."""
from pathlib import Path
import csv,hashlib,json,math
import numpy as np

P=Path(__file__).resolve().parent
I=P.parents[1]/'local_validation/radar_roi'
d=json.loads((P/'diagnostics.json').read_text())
r=list(csv.DictReader((P/'trace_diagnostics.csv').open()))
s=list(csv.DictReader((P/'threshold_sensitivity.csv').open()))
checks=[]
def check(name,ok):
    checks.append(dict(check=name,pass_=bool(ok)))
    assert ok,name

check('exactly194_delivered_columns',len(r)==194)
check('three_noise_quantiles_two_windows_three_browse_cuts_per_orbit',len(s)==54)
known={
 '00464501':'1b4dfd0a83cf37e90e8af93c97e00abfdc7b4cf5',
 '01983502':'ecc7431a6234bce63d7a180a83334b3be37f31d3',
 '02004601':'8bb7a060774d5c042fabcbd9d70cbda7306756ac'}
lines={}
for orbit,gitsha in known.items():
    data=(I/('s_'+orbit+'.npz')).read_bytes()
    check(orbit+'_exact_original_git_blob',hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==gitsha)
    z=np.load(I/('s_'+orbit+'.npz'));p=z['power'].astype(float)
    rr=[x for x in r if x['orbit']==orbit]
    peak=p.argmax(axis=0)
    check(orbit+'_peak_rows_recomputed',np.array_equal(peak,[int(x['observed_strongest_row0']) for x in rr]))
    check(orbit+'_reported_columns_match_input',np.array_equal(z['source_columns_1based'],[int(x['source_column_1based']) for x in rr]))
    check(orbit+'_roi_bounds',np.all((z['latitude']>=52.5)&(z['latitude']<=53)&(z['longitude']>=168)&(z['longitude']<=168.5)))
    check(orbit+'_noise_quantile_recomputed',np.allclose(np.quantile(p[200:1000],.999,axis=0),[float(x['pre_echo_q999']) for x in rr],rtol=1e-12))
    check(orbit+'_no_pass_claim',all('not accepted' in x['classification'] for x in rr))
    order=np.argsort(z['latitude'])
    lat=z['latitude'][order];lon=z['longitude'][order]
    check(orbit+'_strictly_monotone_latitude',np.all(np.diff(lat)>0))
    lines[orbit]=(lat,lon)
    for t in [x for x in s if x['orbit']==orbit]:
        start=int(t['noise_row_start0']);stop=int(t['noise_row_stop_exclusive0']);q=float(t['empirical_noise_quantile'])
        noise_cut=np.quantile(p[start:stop],q,axis=0)
        source_rows=peak[None,:]+np.arange(30,301)[:,None]
        sampled=p[source_rows,np.arange(p.shape[1])[None,:]]
        hit=sampled>noise_cut[None,:]
        check(orbit+'_sensitivity_count_'+str(start)+'_'+str(q)+'_'+t['simulated_browse_dn_threshold'],int(hit.sum())==int(t['above_noise_samples']))
for pair in d['track_pairs']:
    a,b=pair['orbit_a'],pair['orbit_b']
    la,xa=lines[a];lb,xb=lines[b]
    low=max(la.min(),lb.min());high=min(la.max(),lb.max())
    knots=np.unique(np.r_[la[(la>=low)&(la<=high)],lb[(lb>=low)&(lb<=high)],low,high])
    dx=np.interp(knots,la,xa)-np.interp(knots,lb,xb)
    # Independent algorithm: for strictly monotone latitude polylines, the
    # longitude difference is piecewise-linear on the union of latitude knots.
    intersection=(np.min(dx)<=0<=np.max(dx))
    check(a+'_'+b+'_intersection_independent_latitude_knots',intersection==(pair['piecewise_linear_track_intersection_count']>0))
check('045m_is_subsample_not_resolved',d['model045m_delay_samples']<1 and math.isclose(d['nominal_ice_range_resolution_m'],299792458/(2e7*math.sqrt(3.15))))
check('no_amplitude_subtraction',d['amplitude_subtraction_performed'] is False)
check('unvalidated_detector_explicit',d['thresholds_not_validated'] is True)
out=dict(status='pass',check_count=len(checks),checks=checks,
    scope='Input hashes, table calculations and geometry only; does not verify ice or detector sensitivity')
(P/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status=out['status'],check_count=out['check_count'])))
