from pathlib import Path
import csv,json,hashlib,collections,datetime,math
import numpy as np
import argparse
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description='Independent positional source and OLS audit')
parser.add_argument('--raw-dir',type=Path,required=True)
args=parser.parse_args()
ROOT=args.raw_dir
start=datetime.datetime(2010,11,7);end=datetime.datetime(2010,11,18);epoch=datetime.datetime(2009,1,1)
config={
'D':('deep36cm',[(2,'surface',0),(3,'soil10cm',.1),(4,'ice36cm',.36),(5,'inice42cm',.42)],4,2),
'M':('med22cm',[(4,'soil1cm',.01),(2,'soil12cm',.12),(5,'ice22cm',.22),(3,'inice27cm',.27)],5,4),
'S':('shal8cm',[(2,'surface',0),(3,'ice8cm',.08),(4,'inice15cm',.15)],3,2),
'W_HOBO':('WeatherStation',[(5,'surface',0),(8,'soil20cm',.2),(11,'ice42cm',.42)],11,5),
}
result={ 'scope':'Independent positional CSV/time/count/harmonic audit, no time correction or cross-logger joins', 'primary_start_inclusive':start.isoformat(),'primary_end_exclusive':end.isoformat(),'model':'T=intercept+linear_hours+sin(2pi hours/24)+cos(2pi hours/24); half-amplitude sqrt(a^2+b^2)','stations':{}}

def parse(x):
 try:return datetime.datetime.strptime(x.strip(),'%m/%d/%Y %H:%M')
 except ValueError:return datetime.datetime.fromisoformat(x.strip())

def summary_float(a):
 a=np.asarray(a,dtype=float); finite=np.isfinite(a)
 return {'finite':int(finite.sum()),'missing_or_nonfinite':int((~finite).sum()),'mean':float(np.mean(a[finite])) if finite.any() else None,'min':float(np.min(a[finite])) if finite.any() else None,'max':float(np.max(a[finite])) if finite.any() else None}

for site,(token,channels,ice_idx,upper_idx) in config.items():
 p=ROOT/f'UniversityV_09_10_Hobo_{token}_data_good_only_calibrated.txt'
 data=p.read_bytes(); rows=list(csv.reader(data.decode().splitlines()));header=[x.strip() for x in rows[0]];units=[x.strip() for x in rows[1]];rr=rows[2:]
 width_counts=collections.Counter(map(len,rr));assert len(width_counts)==1,(site,width_counts)
 ncols=len(rr[0]);times=[parse(r[0]) for r in rr];nums=np.array([[float(s.strip()) for s in r[1:]] for r in rr]);deltas=[(b-a).total_seconds()/60 for a,b in zip(times,times[1:])]
 decimal_offset_hr=np.array([(float(r[1])-(t-epoch).total_seconds()/86400)*24 for r,t in zip(rr,times)])
 select=np.array([start<=t<end for t in times]);idx=np.flatnonzero(select);tt=np.array([(t-start).total_seconds()/3600 for t in times])[select]
 station={'file':str(p),'bytes':len(data),'md5':hashlib.md5(data).hexdigest(),'sha256':hashlib.sha256(data).hexdigest(),'data_rows':len(rr),'header_field_count':len(header),'unit_field_count':len(units),'data_row_width_counts':dict(width_counts),'header_fields':header,'unit_fields':units,'first_datetime':times[0].isoformat(),'last_datetime':times[-1].isoformat(),'duplicate_datetime_count':len(times)-len(set(times)),'time_step_minutes_counts':dict(collections.Counter(deltas)),'decimal_minus_printed_hours':summary_float(decimal_offset_hr),'numeric_column_missing_counts':{f'index_1based_{j+2}':int((~np.isfinite(nums[:,j])).sum()) for j in range(ncols-1)},'primary_printed_rows':int(select.sum()),'channels':[]}
 channel_indices=[j for j,_,_ in channels]
 common=np.isfinite(nums[select][:,[j-1 for j in channel_indices]]).all(axis=1)
 station['primary_common_valid_rows']=int(common.sum());station['primary_missing_rows']=int((~common).sum());station['primary_expected_hour_rows']=264
 used_t=tt[common];design=np.column_stack([np.ones(len(used_t)),used_t,np.sin(2*np.pi*used_t/24),np.cos(2*np.pi*used_t/24)])
 fits={}
 for j,label,depth in channels:
  vals=nums[select,j-1];z=vals[common]
  coef,*_=np.linalg.lstsq(design,z,rcond=None)
  residual=z-design@coef;amp=math.hypot(coef[2],coef[3])
  row={'csv_index_1based':j+1,'header':header[j],'nominal_depth_m_from_header':depth,'label':label,'full_file':summary_float(nums[:,j-1]),'primary_individual_valid':int(np.isfinite(vals).sum()),'joint_fit_n':len(z),'half_amplitude_K':amp,'residual_RMSE_K':float(np.sqrt(np.mean(residual**2))),'slope_K_per_h':float(coef[1]),'fit_intercept_C':float(coef[0]),'window_min_C':float(z.min()),'window_max_C':float(z.max())}
  fits[j]=row;station['channels'].append(row)
 station['ice_to_upper_half_amplitude_ratio']=fits[ice_idx]['half_amplitude_K']/fits[upper_idx]['half_amplitude_K']
 station['upper_reference_header']=header[upper_idx];station['ice_reference_header']=header[ice_idx]
 station['cautions']=[]
 if site=='S':station['cautions'].append('Header 11 vs units/data 10 due split trailing RH-like label; only temperature columns3–5 interpreted; trailing columns not silently DictReader-aligned.')
 if site=='M':station['cautions'].append('Upper reference is nominal1cm, not surface0cm; channel order is12cm,27cm,1cm,22cm.')
 if site=='W_HOBO':station['cautions'].append('Temperature/RH probes are not declared one common logger; raw printed-grid co-occurrence is not validated cross-logger timing. DecimalDay differs printed DateTime by about+1hour; neither silently corrected.')
 station['cautions'].append('Times retained as author printed GMT+13 header; absolute historical clock accuracy not validated. No gapfill, phase-to-solar-time or Mars transfer.')
 result['stations'][site]=station
out=HERE/'independent_audit.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:{'rows':v['data_rows'],'first':v['first_datetime'],'last':v['last_datetime'],'header_unit_data':(v['header_field_count'],v['unit_field_count'],v['data_row_width_counts']),'primary_rows':v['primary_printed_rows'],'primary_common_valid':v['primary_common_valid_rows'],'ratio':v['ice_to_upper_half_amplitude_ratio'],'channels':[{'name':c['header'],'valid':c['primary_individual_valid'],'amp':c['half_amplitude_K'],'rmse':c['residual_RMSE_K']} for c in v['channels']],'decimal_offset_minmax':(v['decimal_minus_printed_hours']['min'],v['decimal_minus_printed_hours']['max'])} for k,v in result['stations'].items()},ensure_ascii=False,indent=2))
