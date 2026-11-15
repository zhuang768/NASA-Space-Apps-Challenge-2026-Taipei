#!/usr/bin/env python3
"""Independent Askja trace-registration failure/sensitivity experiment.
Run: python3 recompute_sensitivity.py /path/to/ms02_alternative_research OUTPUT
Standard library only. Public USGS DOI 10.5066/P9QATARQ CC0.
This does NOT register B7 to a raw trace or classify material.
"""
import csv,json,math,struct,sys,pathlib,datetime,hashlib
B=pathlib.Path(sys.argv[1]); O=pathlib.Path(sys.argv[2]);O.mkdir(parents=True,exist_ok=True)
line='ICE192__030';raw=B/'Askja_GPR_2019_raw'; ppath=B/'Ice_Thickness_2019_Picks_csv'/(line+'_pk_es.csv')
buf=(raw/(line+'.DZT')).read_bytes(); n=struct.unpack_from('<H',buf,4)[0];bits=struct.unpack_from('<H',buf,6)[0]; spm=struct.unpack_from('<f',buf,14)[0];rg=struct.unpack_from('<f',buf,26)[0];off=1024*struct.unpack_from('<H',buf,2)[0];nt=(len(buf)-off)//(bits//8*n)
picks=list(csv.DictReader(ppath.open())); assert len(picks)==nt
assert [int(r['trace']) for r in picks] == list(range(nt)), 'trace field must be continuous and zero based'

def writecsv(name,rows):
 with (O/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

gps=[];scan=None
for s in (raw/(line+'.DZG')).read_text().splitlines():
 if s.startswith('$GSSIS,'):scan=int(s.split(',')[1])
 if s.startswith('$GPGGA,'):
  a=s.split(',');lat=float(a[2][:2])+float(a[2][2:])/60;lon=-(float(a[4][:3])+float(a[4][3:])/60)
  gps.append(dict(trace=scan,lat=lat,lon=lon,utc=a[1],quality=a[6],hdop=a[8]))
gps=list({r['trace']:r for r in gps}.values()); gps.sort(key=lambda r:r['trace'])
def dist(a,b):
 r=6371008.8;p,q=math.radians(a['lat']),math.radians(b['lat']);d=p-q;dl=math.radians(a['lon']-b['lon']);return 2*r*math.asin(math.sqrt(math.sin(d/2)**2+math.cos(p)*math.cos(q)*math.sin(dl/2)**2))
cumulative=0
for i,g in enumerate(gps):
 if i:cumulative+=dist(gps[i-1],g)
 g['cumulative_GPS_segment_length_m']=cumulative;g['odometer_station_m']=g['trace']/spm
writecsv('raw_GPS_support.csv',gps)
rows=[];vrows=[]
top=next(k for k in picks[0] if k.startswith('TephraBase_IceTop') and k.endswith('sample'));thick=next(k for k in picks[0] if k.startswith('srf_TephraBase') and k.endswith('thick'))
for direction in ['forward','reverse']:
 for offset in [-10,-5,0,5,10]:
  station=29+offset
  t=round(station*spm) if direction=='forward' else (nt-1)-round(station*spm)
  row=dict(direction_hypothesis=direction,origin_offset_hypothesis_m=offset,paper_station_quoted_m=29,raw_trace_candidate_zero_based=t,within_raw_profile=0<=t<nt,assigned_B7_trace='NA',note='HYPOTHETICAL mapping; not accepted registration')
  if 0<=t<nt:
   p=picks[t];sf=float(p['srf_sample']);tp=float(p[top]) if p[top] else None;dt=(tp-sf)*rg/n if tp is not None else None
   row.update(raw_top_amp_signed_int32=struct.unpack_from('<i',buf,off+4*(t*n+int(tp)))[0] if tp is not None else None,published_top_amp=float(p[next(k for k in p if k.startswith('TephraBase_IceTop') and k.endswith('amp'))]) if tp is not None else None,candidate_odometer_m=t/spm,rawGPS_bracketed=gps[0]['trace']<=t<=gps[-1]['trace'],surface_sample=sf,published_top_pick_sample=tp,top_relative_TWT_ns=dt,published_interpretation_depth_m=float(p[thick]) if p[thick] else None)
   if dt is not None:
    for v in [.06,.08,.10,.12,.14,.16,.168]:
     vrows.append(dict(direction_hypothesis=direction,origin_offset_hypothesis_m=offset,raw_trace_candidate_zero_based=t,top_relative_TWT_ns=dt,assumed_velocity_m_per_ns=v,inferred_depth_m=.5*v*dt,quoted_B7_depth_m=.62,difference_from_quoted_B7_m=.5*v*dt-.62,material_truth='NA',note='Velocity is sensitivity scenario; B7 association unverified'))
  else:row.update(raw_top_amp_signed_int32=None,published_top_amp=None,candidate_odometer_m=None,rawGPS_bracketed=None,surface_sample=None,published_top_pick_sample=None,top_relative_TWT_ns=None,published_interpretation_depth_m=None)
  rows.append(row)
assert all(r['raw_top_amp_signed_int32']==r['published_top_amp'] for r in rows if r.get('published_top_pick_sample') is not None)
writecsv('registration_hypotheses.csv',rows);writecsv('velocity_sensitivity.csv',vrows)
meta=dict(executed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),line=line,total_traces=nt,samples_per_trace=n,bits=bits,traces_per_m=spm,time_window_ns=rg,sample_interval_ns=rg/n,odometer_profile_extent_m=(nt-1)/spm,unique_raw_GPS_fixes=len(gps),raw_GPS_trace_min=gps[0]['trace'],raw_GPS_trace_max=gps[-1]['trace'],raw_GPS_coverage_fraction_of_traces=(gps[-1]['trace']-gps[0]['trace']+1)/nt,raw_GPS_polyline_length_m=cumulative,raw_GPS_odometer_extent_m=(gps[-1]['trace']-gps[0]['trace'])/spm,trial_hypotheses=len(rows),inbounds_hypotheses=sum(r['within_raw_profile'] for r in rows),velocity_depth_scenarios=len(vrows),B7_raw_trace='NA',status='registration unresolved; sensitivity executed; no independent ice classification',random_uncertainty='Not estimated; no repeated B7 location observations',systematic_uncertainty='File crosswalk, origin, direction, antenna-GPS offset, borehole coordinates absent/unresolved. Hypothesis spread is not a confidence interval.',input_sha256={str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [raw/(line+'.DZT'),raw/(line+'.DZG'),raw/(line+'.DZX'),ppath]})
(O/'summary.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2));print(json.dumps(rows,indent=2))
