"""Available-window hourly surface-RHi support, not full-paper snow reproduction.

python3 inspect_uv_surface_support.py --input /path/to/UniversityV_09_10_Hobo_WeatherStation_data_good_only_calibrated.txt[.gz]
Preserves printed time. Does not resample, infill, join loggers or infer snow truth.
"""
from pathlib import Path
from datetime import datetime,timedelta
from collections import Counter
import argparse,csv,gzip,hashlib,io,json,math
HERE=Path(__file__).resolve().parent
MD5='0c138af0770ec15d4a4942a66507328f'
URL='https://zenodo.org/records/10553882/files/UniversityV_09_10_Hobo_WeatherStation_data_good_only_calibrated.txt?download=1'
def main(path):
 raw=path.read_bytes();raw=gzip.decompress(raw) if path.suffix=='.gz' else raw
 assert hashlib.md5(raw).hexdigest()==MD5
 rows=list(csv.reader(io.StringIO(raw.decode())));header=[x.strip() for x in rows[0]];data=rows[2:]
 assert header[6]=='Surf_RHIce' and len(header)==14 and all(len(r)==14 for r in data)
 times=[datetime.strptime(r[0].strip(),'%m/%d/%Y %H:%M') for r in data]
 assert len(data)==8625 and len(set(times))==len(times)
 assert all((b-a).total_seconds()==3600 for a,b in zip(times,times[1:]))
 start,stop=datetime(2009,11,1),datetime(2010,3,1)
 records=[];offsets=Counter()
 for line,(r,t) in enumerate(zip(data,times),3):
  delta=(datetime(2009,1,1)+timedelta(days=float(r[1]))-t).total_seconds()/3600
  offsets[round(delta,2)]+=1
  if start<=t<stop:
   rh=float(r[6]);valid=math.isfinite(rh)
   records.append({'source_text_line_1based':line,'printed_timestamp':r[0].strip(),'decimal_day_original':r[1].strip(),'surface_RH_ice_percent':rh if valid else '', 'finite':valid,'ge98_percent':valid and rh>=98})
 valid=[r for r in records if r['finite']];high=sum(r['ge98_percent'] for r in valid)
 text=io.StringIO(newline='');w=csv.DictWriter(text,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
 (HERE/'uv_surface_RH_available_summer.csv.gz').write_bytes(gzip.compress(text.getvalue().encode(),mtime=0))
 result={'scope':'Available-window hourly surface-RHi sample support; not independently observed snow or full-paper reproduction','source_file':'UniversityV_09_10_Hobo_WeatherStation_data_good_only_calibrated.txt','source_url':URL,'source_decoded_bytes':len(raw),'source_decoded_md5':hashlib.md5(raw).hexdigest(),'source_decoded_sha256':hashlib.sha256(raw).hexdigest(),'source_level':'existing author-calibrated export reused; not new remote download or raw logger','data_rows':len(data),'header':header,'raw_time_label':rows[1][0].strip(),'printed_time_start':str(times[0]),'printed_time_stop':str(times[-1]),'native_cadence_seconds':3600,'decimal_minus_printed_hours_rounded_counts':{str(k):v for k,v in offsets.items()},'time_policy':'Original printed labels retained; +1h decimal discrepancy is not repaired or declared UTC offset. No cross-logger join.','surface_RH_channel':'Surf_RHIce, zero-based column6, percent relative to ice; separate from Campbell air RH','paper_rule_source':'McKay2026 DOI10.1017/S0954102025100448; Variation in snow days and Fig6','paper_nominal_window_start':str(start),'paper_nominal_window_stop_exclusive':str(stop),'paper_cadence_seconds':1800,'paper_nominal_days':120,'paper_reported_approximately_equivalent_days':24,'available_window_start':str(datetime.strptime(records[0]['printed_timestamp'],'%m/%d/%Y %H:%M')),'available_window_stop_inclusive':str(datetime.strptime(records[-1]['printed_timestamp'],'%m/%d/%Y %H:%M')),'expected_hourly_samples_full_nominal_window':2880,'available_hourly_samples':len(records),'finite_surface_RH_samples':len(valid),'missing_surface_RH_samples':len(records)-len(valid),'uncovered_nominal_window_hourly_positions':2880-len(records),'ge98_percent_sample_count':high,'ge98_percent_fraction_of_finite_available_samples':high/len(valid),'nominal_hourly_sample_equivalent_days':high/24,'equivalent_day_divisor':24,'equivalent_day_qualification':'Count-based hourly-sample equivalent only; not integrated continuous snow-cover duration. The paper48-samples/day divisor is not applied to hourly records.','RH_over100_N':sum(r['surface_RH_ice_percent']>100 for r in valid),'RH_below0_N':sum(r['surface_RH_ice_percent']<0 for r in valid),'full_paper_snow_days_reproduced':False,'infilled_or_resampled':False,'cannot_compare_directly_reason':'November2009 and December1-9 absent; hourly author export differs from paper30min surface series; version/resampling and timing provenance not recovered. No missing days set to zero or extrapolated.'}
 (HERE/'uv_surface_RH_support.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result,indent=2,allow_nan=False))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);main(ap.parse_args().input)
