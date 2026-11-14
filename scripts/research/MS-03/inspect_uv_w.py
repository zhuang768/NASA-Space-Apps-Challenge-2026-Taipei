"""Acquire pinned author-calibrated W-station exports and perform bounded QA.
No PDF transcription, UTC conversion, gap filling, TI/ice inversion or Mars fit.
"""
from pathlib import Path
import argparse,csv,datetime as D,gzip,hashlib,io,json,math,statistics,urllib.request,collections
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'outputs/research/MS-03/uv_w'
FILES={
'UniversityV_09_13_Campbell_data_all_calibrated.txt':'333b498382376f3bb034e68862bede70',
'UniversityV_09_13_Hobo_WeatherStation_data_good_only_calibrated.txt':'22932fdef50cac1b372b06100392c2fe',
'University Valley Campbell notes Dec 2010.pdf':'608feb1d54fa3c2de4265f1d3f96d8b5',
'University Valley weather station data check 2011-2013.docx':'1212e1db8ba61a5a84c54cd80ae4d9cc',
'UnivValley_Dec2009Deployment_HoboInfo.docx':'7a1d6353d30d724a0512ffb24db36401',
'UnivValley_HoboInfo_Dec2010_Update.docx':'b8eb8ad431f094898dfc2d984e0f5c04'}
def sha(b):return hashlib.sha256(b).hexdigest()
def when(s):
 for fmt in ['%m/%d/%Y %H:%M','%Y-%m-%d %H:%M:%S']:
  try:return D.datetime.strptime(s.strip(),fmt)
  except ValueError:pass
 raise ValueError(s)
def finite(s):
 v=float(s);return v if math.isfinite(v) else None

def run(raw):
 OUT.mkdir(parents=True,exist_ok=True);raw.mkdir(parents=True,exist_ok=True)
 meta_url='https://zenodo.org/api/records/10553882'
 if not (raw/'record.json').exists(): (raw/'record.json').write_bytes(urllib.request.urlopen(meta_url,timeout=35).read())
 meta=json.loads((raw/'record.json').read_text());assert str(meta['id'])=='10553882'
 checks=[]
 for name,md5 in FILES.items():
  item=next(x for x in meta['files'] if x['key']==name);assert item['checksum']=='md5:'+md5
  p=raw/name
  if not p.exists():p.write_bytes(urllib.request.urlopen(item['links']['self'],timeout=60).read())
  b=p.read_bytes();assert hashlib.md5(b).hexdigest()==md5 and len(b)==item['size']
  checks.append(dict(filename=name,bytes=len(b),md5=md5,sha256=sha(b),url=item['links']['self'],actually_downloaded=True,source_level='author-calibrated export or deployment/QA note;not unprocessed logger bytes'))
 (OUT/'download_manifest.json').write_text(json.dumps(dict(record_id=10553882,concept_record_id=10553881,version_doi='10.5281/zenodo.10553882',license=meta['metadata'].get('license'),metadata_sha256=sha((raw/'record.json').read_bytes()),files=checks,raw_directory=str(raw),raw_files_tracked=False),indent=2)+'\n')
 summaries={};monthly=[];hrows=[]
 base=D.datetime(2009,1,1)
 for instrument,name,skip,mapping,nominal in [
  ('Campbell','UniversityV_09_13_Campbell_data_all_calibrated.txt',4,{'T_air_C':4,'T_surface_C':10,'T10_C':11,'T42_C':12,'T49_C':13},30),
  ('HOBO','UniversityV_09_13_Hobo_WeatherStation_data_good_only_calibrated.txt',2,{'T_surface_C':2,'T20_C':5,'T42_C':8},60)]:
  source=list(csv.reader((raw/name).open()));headers=source[:skip];rr=source[skip:];width=20 if instrument=='Campbell' else 11
  assert all(len(x)==width for x in rr)
  dates=[when(x[0]) for x in rr];assert dates==sorted(dates) and len(set(dates))==len(dates)
  steps=collections.Counter((b-a).total_seconds()/60 for a,b in zip(dates,dates[1:]))
  off=[round((float(r[1])-(t-base).total_seconds()/86400)*24,2) for t,r in zip(dates,rr)]
  regimes=[]
  for t,v in zip(dates,off):
   if not regimes or regimes[-1]['offset_hours_decimal_minus_timestamp']!=v:regimes.append(dict(start=t.isoformat(),offset_hours_decimal_minus_timestamp=v))
  info=dict(file=name,headers=headers,rows=len(rr),first=dates[0].isoformat(),last=dates[-1].isoformat(),duplicates=0,step_minutes_counts=dict(steps),nominal_step_minutes=nominal,decimal_day_minus_timestamp_regimes=regimes,column_mapping_0based=mapping,series={})
  for metric,col in mapping.items():
   vals=[finite(r[col]) for r in rr];valid=[v for v in vals if v is not None]
   info['series'][metric]=dict(valid_n=len(valid),missing_n=len(vals)-len(valid),min=min(valid),max=max(valid))
   groups=collections.defaultdict(list)
   for t,v in zip(dates,vals):groups[t.strftime('%Y-%m')].append(v)
   for month,vv in groups.items():
    yy,mm=map(int,month.split('-'));start=D.datetime(yy,mm,1);end=D.datetime(yy+1,1,1) if mm==12 else D.datetime(yy,mm+1,1)
    monthly.append(dict(instrument=instrument,metric=metric,month=month,observed_rows=len(vv),finite_n=sum(x is not None for x in vv),calendar_expected_rows=int((end-start).total_seconds()/60/nominal),support='published rows;partial endpoint months;not independent samples'))
  info['gaps']=[dict(after=a.isoformat(),before=b.isoformat(),step_minutes=(b-a).total_seconds()/60) for a,b in zip(dates,dates[1:]) if (b-a).total_seconds()!=nominal*60]
  summaries[instrument]=info
  if instrument=='HOBO':
   assert len(headers[0])==14 and len(headers[1])==11 # malformed provider header retained explicitly
   assert 'cm20_T' in headers[0] and 'ice42cm_T' in headers[0]
   for line,(t,r) in enumerate(zip(dates,rr),3):
    hrows.append(dict(source_file=name,source_line=line,original_time=r[0],time_naive=t.isoformat(),decimal_day_original=r[1].strip(),time_label='GMT+13:00 per source units row;no conversion',T_surface_C='' if finite(r[2]) is None else r[2].strip(),T20_C='' if finite(r[5]) is None else r[5].strip(),T42_C='' if finite(r[8]) is None else r[8].strip(),quality='author good_only_calibrated;independent sensor validation not established'))
 def write(name,rows):
  with (OUT/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 # Deterministic compressed table, unchanged finite values, NaN becomes explicit blank.
 buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=list(hrows[0]),lineterminator='\n');w.writeheader();w.writerows(hrows)
 (OUT/'hobo_W_temperatures.csv.gz').write_bytes(gzip.compress(buf.getvalue().encode(),mtime=0))
 write('monthly_coverage.csv',monthly)
 # Design window is explicitly Earth-only;keep source clock and all finite same-row pairs.
 subset=[r for r in hrows if '2010-01-01T00:00:00'<=r['time_naive']<'2011-01-01T00:00:00']
 stats=[]
 for a,b,label in [('T20_C',None,'T20_C'),('T42_C',None,'T42_C'),('T20_C','T42_C','T20_minus_T42_C')]:
  vals=[float(r[a])-(float(r[b]) if b else 0) for r in subset if r[a]!='' and (not b or r[b]!='')]
  stats.append(dict(window_start_inclusive='2010-01-01T00:00:00',window_end_exclusive='2011-01-01T00:00:00',clock='HOBO printed GMT+13:00;not converted',metric=label,unit='degC',finite_n=len(vals),expected_hourly_n=8760,mean=statistics.fmean(vals),min=min(vals),max=max(vals),interpretation='Earth-only descriptive values in author-calibrated export;not a new mechanism,ice depth,TI or Mars similarity'))
 write('earth_only_2010_summary.csv',stats)
 qa=dict(version='MS03-UV-W-availability-v1',records=summaries,
   HOBO_header_mapping='Provider header has14 cells;units/data11;positions0time1decimal2surfaceT3surfaceRH4surfaceV5T20 6RH20 7V20 8T42 9RH42 10V42. Mapping supported by units,header fragments and Campbell deployment notes pp1-2;no silent 14-column shift.',
   author_processing='Campbell QA note reports removed surface spikes,insertedNaNs and one interpolated42cm point;not unaltered logger bytes. Per-row intervention flags/time of interpolated Campbell point not supplied;do not assume it identifies any HOBO point.',
   clock_policy='Keep clocks separate. The270min timestamp discontinuity coincides with the4h offset shift and is not classified as a physical observation gap. Campbell decimal-day offset changes from about-1h to-5h relative to printed timestamp;HOBO consistent within decimal rounding. Do not cross-join clocks or convert to UTC/solar time without correction history.',
   RH_policy='Export retains author RH basis/calibration;no RH-derived water activity or new corrections in this analysis.',
   comparative_scope='Same-W same-HOBO-depth description only. No same-time/same-quantity EarthMars comparison against coarse MCS or TES.',
   excluded=['subhourly extrema from daily means','repeated seven days as genuine independent observations','automatic outlier thresholds','cross-instrument time matching','thermal inertia/ice-depth inversion','ice quantity or equipment performance'],
   preliminary=True)
 (OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n')
 print(json.dumps({'Campbell_rows':summaries['Campbell']['rows'],'HOBO_rows':len(hrows),'year2010':stats},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--raw-dir',type=Path,default=ROOT/'data/raw/earth/MS-03/uv_w_10553882');run(p.parse_args().raw_dir)
