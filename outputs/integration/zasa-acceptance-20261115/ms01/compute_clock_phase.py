#!/usr/bin/env python3
"""MS-01 same-logger amplitude/phase and clock-origin diagnostic, NOT an ice/material inversion.
Python 3 + numpy + matplotlib. --download reacquires author processed exports.
Fixed 2010-11-07 <= printed time < 2010-11-18; no clock repair or cross-logger join.
"""
import argparse,csv,datetime as dt,hashlib,json,pathlib,urllib.request,os
os.environ.setdefault("MPLCONFIGDIR","/tmp/ms01-matplotlib")
os.environ.setdefault("XDG_CACHE_HOME","/tmp/ms01-cache")
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent
P=24.; OMEGA=2*np.pi/P
START=dt.datetime(2010,11,7); END=dt.datetime(2010,11,18)
SPECS={
 'S8':('shal8cm',2,['Shal_surf_T','Shal_Ice8cm_T','Shal_InIce15cm_T'],[0.,.08,.15]),
 'M22':('med22cm',2,['Med_cm1_T','Med_cm12_T','Med_Ice22cm_T','Med_InIce27cm_T'],[.01,.12,.22,.27]),
 'D36':('deep36cm',2,['Deep_surf_T','Deep_cm10_T','Deep_ice36cm_T','Deep_InIce42cm_T'],[0.,.10,.36,.42]),
 'W42_Campbell':('Campbell',4,['T107_surf','T107_10cm','T107_ice42cm','T107_InIce49cm'],[0.,.10,.42,.49])}
def fit(t,y,semi=False):
 a=t*OMEGA
 cols=[np.ones(len(t)),t-t.mean(),np.sin(a),np.cos(a)]
 if semi: cols += [np.sin(2*a),np.cos(2*a)]
 X=np.column_stack(cols); c,_,rank,_=np.linalg.lstsq(X,y,rcond=None)
 assert rank==X.shape[1]
 return np.hypot(c[2],c[3]),np.arctan2(c[3],c[2]),np.sqrt(np.mean((y-X@c)**2,axis=0))
def diagnostic(t,y,semi=False):
 A,phi,rmse=fit(t,y,semi)
 R=A/A[0]; q=-np.log(R)
 lag=(phi[0]-phi)/OMEGA
 # Circular discrepancy avoids asserting an unwrapped travel time.
 discrepancy=(lag-q/OMEGA+12)%24-12
 return A,R,q,(lag+12)%24-12,discrepancy,rmse
def write_csv(name,rows):
 with (HERE/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--download',action='store_true');args=parser.parse_args()
 manifest=json.loads((HERE/'inputs/source_manifest.json').read_text())
 old={(r['station'],r['column']):r for r in csv.DictReader((HERE/'inputs/amplitudes.csv').open())}
 result=[]; checks=[]; loo=[]; used=[];max_old=0.;shift_err=0.
 for station,(key,skip,names,depths) in SPECS.items():
  a=next(a for a in manifest['assets'] if key in a['filename']);path=HERE/'inputs'/a['filename']
  if args.download or not path.exists():path.write_bytes(urllib.request.urlopen(a['url'],timeout=60).read())
  b=path.read_bytes();assert hashlib.md5(b).hexdigest()==a['expected_md5'];assert hashlib.sha256(b).hexdigest()==a['sha256']
  used.append(dict(filename=path.name,url=a['url'],bytes=len(b),md5=hashlib.md5(b).hexdigest(),sha256=hashlib.sha256(b).hexdigest(),retrieval='Python urllib fresh download for this follow-up; processed author data, not original logger binary'))
  raw=list(csv.reader(b.decode('utf-8-sig').splitlines()));header=[v.strip() for v in raw[1 if skip==4 else 0]]
  idx=[header.index(n) for n in names];times=[];yy=[]
  for r in raw[skip:]:
   try:when=dt.datetime.fromisoformat(r[0].strip())
   except ValueError:when=dt.datetime.strptime(r[0].strip(),'%m/%d/%Y %H:%M')
   y=[float(r[j]) for j in idx]
   if START<=when<END and np.isfinite(y).all():times.append(when);yy.append(y)
  assert len(times)==len(set(times))
  t=np.array([(w-START).total_seconds()/3600 for w in times]);y=np.array(yy)
  assert len(t)==(528 if station=='W42_Campbell' else 264)
  assert np.allclose(np.diff(t),.5 if station=='W42_Campbell' else 1.)
  d=diagnostic(t,y); semi=diagnostic(t,y,True);days=np.floor(t/24).astype(int)
  trials=[diagnostic(t[days!=day],y[days!=day]) for day in np.unique(days)]
  # Same rows shifted in clock origin, not shifted selection/window; no physical correction.
  for shift in [-13,-5,-1,.371,1,5,13]:
   ds=diagnostic(t+shift,y)
   e=float(max(np.max(np.abs(ds[1]-d[1])),np.max(np.abs(ds[4]-d[4]))));shift_err=max(shift_err,e)
   checks.append(dict(station=station,common_clock_origin_shift_h=shift,max_ratio_or_circular_hour_difference=e))
  for j,n in enumerate(names):
   max_old=max(max_old,abs(d[0][j]-float(old[station,n]['amplitude_K'])))
   if j==0:continue
   dis=np.array([s[4][j] for s in trials])
   result.append(dict(station=station,upper=names[0],lower=n,upper_depth_m=depths[0],lower_depth_m=depths[j],common_n=len(t),amplitude_ratio=d[1][j],negative_log_amplitude_ratio=d[2][j],measured_lag_mod24_h=d[3][j],homogeneous_predicted_lag_h=d[2][j]/OMEGA,circular_measured_minus_predicted_h=d[4][j],leave_one_day_discrepancy_min_h=dis.min(),leave_one_day_discrepancy_max_h=dis.max(),with_12h_nuisance_discrepancy_h=semi[4][j],lower_amplitude_K=d[0][j],lower_residual_rmse_K=d[5][j],interpretation='Descriptive discrepancy only; not significance test, ice detection, true delay, or diffusivity estimate'))
   for day,s in zip(np.unique(days),trials):loo.append(dict(station=station,lower=n,excluded_printed_date=(START+dt.timedelta(days=int(day))).date().isoformat(),amplitude_ratio=s[1][j],circular_discrepancy_h=s[4][j]))
 # Ideal synthetic transfer test: phase attenuation relation and sign.
 t=np.arange(264,dtype=float)
 synthetic=np.column_stack([np.cos(OMEGA*t),np.exp(-1.3)*np.cos(OMEGA*t-1.3)])
 exact_error=float(abs(diagnostic(t,synthetic)[4][1]))
 assert max_old<1e-10 and shift_err<1e-10 and exact_error<1e-10
 write_csv('amplitude_phase_consistency.csv',result);write_csv('leave_one_day_diagnostics.csv',loo);write_csv('clock_origin_invariance.csv',checks)
 provenance=dict(main_sha='1506ede572435588eb5e64f95f24639279b77e56',reviewed_pr27_sha='3186fca5f968322a7bdaaed83c41d870a1d68c6f',inputs=used,window=[START.isoformat(),END.isoformat()],same_logger_only=True,primary_processed_temperature_values=sum((528 if s=='W42_Campbell' else 264)*len(v[2]) for s,v in SPECS.items()),prior_amplitude_max_abs_delta_K=max_old,clock_origin_invariance_max_numerical_error=shift_err,ideal_synthetic_discrepancy_h=exact_error,formula_reference='https://doi.org/10.1029/2002JB002351 section 3.1 equations in paragraph 10',notes=['No new field observations; new diagnostic of existing observations.','No phase between separate U23 loggers or between stations.','Common constant offset only; clock drift, reset, channel delay and calibration are not verified.','LODO bounds are sensitivity ranges, not confidence or sensor uncertainty intervals.'])
 (HERE/'verification.json').write_text(json.dumps(provenance,indent=2)+'\n')
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,ax=plt.subplots(figsize=(9,5.6));labels=[r['station']+' '+str(int(round(r['lower_depth_m']*100)))+' cm' for r in result]
 x=np.arange(len(result));v=np.array([r['circular_measured_minus_predicted_h'] for r in result]);lo=np.array([r['leave_one_day_discrepancy_min_h'] for r in result]);hi=np.array([r['leave_one_day_discrepancy_max_h'] for r in result])
 # Ranges are plotted as segments, since full-data value need not be inside LODO extrema.
 ax.hlines(x,lo,hi,color='#237a89',linewidth=3,label='Leave-one-day-out range (not CI)');ax.scatter(v,x,color='#132d46',zorder=3,label='Full fixed 11-day window');ax.axvline(0,color='grey',ls='--')
 ax.set_yticks(x,labels);ax.invert_yaxis();ax.set_xlabel('Circular phase discrepancy: measured - homogeneous prediction (hours)');ax.set_title('University Valley: same-logger amplitude/phase diagnostic');ax.legend(loc='best',fontsize=8);ax.grid(axis='x',alpha=.15)
 fig.text(.5,.01,'Known-ice sites; printed clocks; not an ice test, physical travel time, or thermal-property inversion.',ha='center',fontsize=8);fig.tight_layout(rect=[0,.04,1,1]);fig.savefig(HERE/'amplitude_phase_consistency.png',dpi=180);fig.savefig(HERE/'amplitude_phase_consistency.svg');plt.close(fig)
 print(json.dumps(provenance,indent=2));print('Computed',len(result),'within-logger pairs')
if __name__=='__main__':main()
