"""Inspect a known author-calibrated export; never replace surface RH with air RH.

python3 inspect_uv_support.py --input /path/to/UniversityV_09_10_Campbell_data_good_only_calibrated.txt[.gz]
The released text's MD5 pins this analysis. Source is Zenodo v1 10553882.
"""
from pathlib import Path
from datetime import datetime
from collections import Counter
import argparse,csv,gzip,hashlib,io,json,math,statistics
HERE=Path(__file__).resolve().parent
EXPECTED_MD5='ae2133eac5c92c695c5f6ef93bcbbd25'
SOURCE_URL='https://zenodo.org/records/10553882/files/UniversityV_09_10_Campbell_data_good_only_calibrated.txt?download=1'
def parse_time(s):
 s=s.strip()
 try:return datetime.strptime(s,'%m/%d/%Y %H:%M'),'US_month_day'
 except ValueError:return datetime.fromisoformat(s),'ISO'
def quantile(xs,q):
 xs=sorted(xs);f=(len(xs)-1)*q;i=int(f);j=min(i+1,len(xs)-1)
 return xs[i]+(f-i)*(xs[j]-xs[i])
def main(path):
 raw=path.read_bytes();raw=gzip.decompress(raw) if path.suffix=='.gz' else raw
 md5=hashlib.md5(raw).hexdigest();assert md5==EXPECTED_MD5
 rows=list(csv.reader(io.StringIO(raw.decode())))
 header=[v.strip() for v in rows[1]];data=rows[4:]
 assert len(header)==20 and all(len(r)==20 for r in data)
 assert header[8]=='WS_ms' and header[5]=='RH_wrt_water' and header[6]=='RH_wrt_WaterIce'
 times=[];formats=Counter();winds=[];records=[]
 for line,r in enumerate(data,5):
  t,fmt=parse_time(r[0]);times.append(t);formats[fmt]+=1
  v=float(r[8]);finite=math.isfinite(v)
  if finite:winds.append(v)
  records.append({'source_text_line_1based':line,'printed_timestamp':r[0].strip(),'timestamp_format':fmt,'wind_ms':v if finite else '', 'raw_wind_field':r[8].strip()})
 assert len(data)==17705 and len(set(times))==len(times)
 output=io.StringIO(newline='');w=csv.DictWriter(output,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
 (HERE/'uv_wind_records.csv.gz').write_bytes(gzip.compress(output.getvalue().encode(),mtime=0))
 start,end=datetime(2009,11,1),datetime(2010,3,1)
 selected=[t for t in times if start<=t<end]
 result={'source_file':'UniversityV_09_10_Campbell_data_good_only_calibrated.txt','source_url':SOURCE_URL,'source_level':'previous author-calibrated export reused and rehashed; not unprocessed logger; no new remote acquisition','source_decoded_bytes':len(raw),'source_decoded_md5':md5,'source_decoded_sha256':hashlib.sha256(raw).hexdigest(),'data_rows':len(data),'header':header,'timestamp_format_counts':dict(formats),'printed_time_start':str(min(times)),'printed_time_stop':str(max(times)),'printed_time_duplicate_count':len(times)-len(set(times)),'sampling_interval_seconds_counts':{str(k):v for k,v in sorted(Counter((b-a).total_seconds() for a,b in zip(times,times[1:])).items())},'timestamp_interpretation':'Original printed labels; no UTC assignment, interpolation, clock correction or cross-logger join.','paper_summer_window_start':str(start),'paper_summer_window_stop_exclusive':str(end),'rows_in_paper_summer_window':len(selected),'observed_summer_start':str(min(selected)),'observed_summer_stop':str(max(selected)),'surface_RH_available_in_this_export':False,'RH_channel_support':'Campbell207 air RH at1.2m per Marinova2022 Meteorological measurements; surface RH was separate Onset U23 at60min.','snow_proxy_equivalent_days':None,'snow_proxy_missing_reason':'No surface RH channel in this export and November2009 absent; do not substitute air RH, repeat missing days or resample hourly Onset to30min without documented provenance.','wind_height_m':1.08,'wind_unit':'m/s','wind_valid_finite_N':len(winds),'wind_missing_N':len(data)-len(winds),'wind_min':min(winds),'wind_max':max(winds),'wind_mean':statistics.mean(winds),'wind_median':statistics.median(winds),'wind_p95_linear':quantile(winds,.95),'wind_below_1ms_instrument_threshold_N':sum(v<1 for v in winds),'wind_negative_N':sum(v<0 for v in winds),'wind_over_100ms_N':sum(v>100 for v in winds),'wind_interpretation':'Descriptive available-export distribution, not annual climatology or Mars transfer; below-threshold records retained, not independently verified calm winds.'}
 (HERE/'uv_export_support.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result,indent=2,allow_nan=False))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);main(ap.parse_args().input)
