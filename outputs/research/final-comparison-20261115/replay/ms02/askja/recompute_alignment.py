#!/usr/bin/env python3
"""Recompute Askja line-to-line alignments. These are NOT borehole alignments.
Usage: python3 recompute_alignment.py INPUT_ROOT OUTPUT_DIR
INPUT_ROOT contains Askja_GPR_2019_raw/ and Ice_Thickness_2019_Picks_csv/.
No third-party dependencies. Inputs are from USGS DOI10.5066/P9QATARQ (CC0).
Distance is spherical haversine, radius6371008.8m, using WGS84 longitude/latitude.
Trace numbers are zero based; station_m = trace/100 from DZT header.
Interpolated GPS has unreported absolute uncertainty; HDOP is NOT metres.
"""
import bisect,csv,datetime,json,math,pathlib,struct,sys
BASE=pathlib.Path(sys.argv[1]);OUT=pathlib.Path(sys.argv[2]);OUT.mkdir(parents=True,exist_ok=True)
RADIUS=6371008.8

def writecsv(name,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def gps(line):
 result=[];scan=None
 for text in (BASE/'Askja_GPR_2019_raw'/(line+'.DZG')).read_text().splitlines():
  if text.startswith('$GSSIS,'):scan=int(text.split(',')[1])
  elif text.startswith('$GPGGA,'):
   a=text.split(',');lat=float(a[2][:2])+float(a[2][2:])/60;lon=float(a[4][:3])+float(a[4][3:])/60
   result.append(dict(line=line,trace=scan,lat=lat*(-1 if a[3]=='S' else 1),lon=lon*(-1 if a[5]=='W' else 1),utc_time=a[1],fix_quality=int(a[6]),satellites=int(a[7]),hdop=float(a[8]),alt_m=float(a[9])))
 # At repeated trace zero use the final stationary fix; no extrapolation allowed.
 result={r['trace']:r for r in result}
 return [result[k] for k in sorted(result)]

def interp(rows,t):
 if not rows[0]['trace']<=t<=rows[-1]['trace']:raise ValueError('No bracketing raw GPS: '+str(t))
 i=bisect.bisect_left([r['trace'] for r in rows],t)
 if rows[i]['trace']==t:a=b=rows[i];fraction=0
 else:a,b=rows[i-1:i+1];fraction=(t-a['trace'])/(b['trace']-a['trace'])
 v={k:a[k]+fraction*(b[k]-a[k]) for k in ['lat','lon']}
 return dict(**v,bracket_lo=a['trace'],bracket_hi=b['trace'],utc_lo=a['utc_time'],utc_hi=b['utc_time'],fix_quality_lo=a['fix_quality'],fix_quality_hi=b['fix_quality'],hdop_lo=a['hdop'],hdop_hi=b['hdop'])

def distance(a,b):
 p1,p2=map(math.radians,[a['lat'],b['lat']]);dp=p2-p1;dl=math.radians(b['lon']-a['lon'])
 return 2*RADIUS*math.asin(math.sqrt(math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2))

def pickrows(line):
 with (BASE/'Ice_Thickness_2019_Picks_csv'/(line+'_pk_es.csv')).open() as f:return list(csv.DictReader(f))

def point(row):return {k:float(row[k]) for k in ['lat','lon']}
L0,L1='ICE192__030','ICE192__031';G0,G1=gps(L0),gps(L1);P0,P1=pickrows(L0),pickrows(L1)
a=interp(G0,1500);d,t,b=min((distance(a,interp(G1,t)),t,interp(G1,t)) for t in range(G1[0]['trace'],G1[-1]['trace']+1))
c=point(P0[2900]);d2,t2,row=min((distance(c,point(row)),int(row['trace']),row) for row in P1)
rows=[]
for method,source,target,separation,va,vb,note in [('raw_GGA_linear_interpolation',1500,t,d,a,b,'Both traces bracketed by raw GPS; no borehole involved'),('published_pick_coordinates',2900,t2,d2,c,point(row),'030 source outside raw GGA range0-1658; derived coordinates cannot be treated as rawGPS; no borehole involved')]:
 rows.append(dict(method=method,source_line=L0,source_trace_zero_based=source,source_station_m=source/100,target_line=L1,target_trace_zero_based=target,target_station_m=target/100,horizontal_separation_m=separation,source_lat=va['lat'],source_lon=va['lon'],target_lat=vb['lat'],target_lon=vb['lon'],ground_truth_id='',borehole_distance_m='',blind_test=False,note=note))
writecsv('alignment_rows.csv',rows)
writecsv('gps_fixes_used.csv',[r for r in G0+G1 if (r['line']==L0 and r['trace'] in [a['bracket_lo'],a['bracket_hi']]) or (r['line']==L1 and r['trace'] in [b['bracket_lo'],b['bracket_hi']])])
checks=[];heads=[]
for line,trace in [(L0,1500),(L1,t),(L0,2900),(L1,t2)]:
 buf=(BASE/'Askja_GPR_2019_raw'/(line+'.DZT')).read_bytes();ns=struct.unpack_from('<H',buf,4)[0];bits=struct.unpack_from('<H',buf,6)[0];spm=struct.unpack_from('<f',buf,14)[0];off=1024*struct.unpack_from('<H',buf,2)[0]
 assert ns==1024 and bits==32 and spm==100 and off==131072
 rs=pickrows(line);r=rs[trace]
 for ampcol in [k for k in r if k.endswith('_amp')]:
  sc=ampcol[:-4]+'_sample';si=int(float(r[sc]));v=struct.unpack_from('<i',buf,off+4*(trace*ns+si))[0];pv=int(float(r[ampcol]));checks.append(dict(line=line,trace=trace,amplitude_column=ampcol,sample=si,raw_signed_int32=v,published_csv_amplitude=pv,exact_match=v==pv))
 if not any(h['line']==line for h in heads):
  v=struct.unpack_from('<I',buf,32)[0];dt=datetime.datetime(1980+((v>>25)&127),(v>>21)&15,(v>>16)&31,(v>>11)&31,(v>>5)&63,2*(v&31))
  heads.append(dict(line=line,samples_per_trace=ns,bits=bits,traces_per_m=spm,data_offset_bytes=off,total_traces=(len(buf)-off)//(4*ns),instrument_creation_time_no_timezone=dt.isoformat(),rawGPS_maxtrace=(G0 if line==L0 else G1)[-1]['trace']))
writecsv('amplitude_checks.csv',checks);writecsv('headers.csv',heads)
(OUT/'audit_metadata.json').write_text(json.dumps(dict(distance_method='haversine',radius_m=RADIUS,trace_index_origin=0,station_rule='DZT traces_per_m; station is instrument odometer distance, not horizontal/geodesic length',no_extrapolation=True,raw_alignment_source=a,raw_alignment_target=b,uncertainty='Geo7x paper states tens-of-centimetres to metre. NMEA quality1 and HDOP0.5-0.6 are not positional error estimates. Combined borehole-to-trace uncertainty unknown because borehole coordinates absent.',B7_status='Paper B7 at29m, topice0.62m; file association unresolved, do not assign a trace or distance; B7 used in paper depth calibration and is not a blind validation'),indent=2))
print(json.dumps(rows,indent=2))

# Export interpreted depths separately; these are NOT material ground truth.
depths=[]
for line,trace in [(L0,1500),(L1,t),(L0,2900),(L1,t2)]:
 r=pickrows(line)[trace];buf=(BASE/'Askja_GPR_2019_raw'/(line+'.DZT')).read_bytes()
 ns=struct.unpack_from('<H',buf,4)[0];rg=struct.unpack_from('<f',buf,26)[0]
 top=next(k for k in r if k.startswith('TephraBase_IceTop') and k.endswith('sample'))
 base=next(k for k in r if k.startswith('IceBase') and k.endswith('sample'))
 dep=next(k for k in r if k.startswith('srf_TephraBase') and k.endswith('thick'))
 depths.append(dict(line=line,trace_zero_based=trace,surface_sample=r['srf_sample'],published_top_sample=r[top],published_base_sample=r[base],raw_header_top_relative_TWT_ns=(float(r[top])-float(r['srf_sample']))*rg/ns,published_picked_top_depth_m=r[dep],material_truth='',borehole_id='',status='Published interpretation only; not independent material label; B7 association not verified'))
writecsv('picked_depths_NOT_ground_truth.csv',depths)
assert len(checks)==12 and all(r['exact_match'] for r in checks)
assert G0[-1]['trace']==1658
