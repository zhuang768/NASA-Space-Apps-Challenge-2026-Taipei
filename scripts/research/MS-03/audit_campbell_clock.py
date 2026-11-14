"""Audit printed Campbell time fields only; never correct or join instrument clocks."""
import argparse,csv,datetime as dt,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--raw-dir',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[3];out=root/'outputs/research/MS-03/uv_w'
f=a.raw_dir/'UniversityV_09_13_Campbell_data_all_calibrated.txt'
assert hashlib.md5(f.read_bytes()).hexdigest()=='333b498382376f3bb034e68862bede70'
with f.open() as h: rows=list(csv.reader(h))[4:]
def date(s):
 for fmt in ('%Y-%m-%d %H:%M:%S','%d-%b-%Y %H:%M:%S','%m/%d/%Y %H:%M'):
  try:return dt.datetime.strptime(s,fmt)
  except ValueError:pass
 raise ValueError(s)
base=dt.datetime(2009,1,1);times=[date(r[0]) for r in rows]
off=[round((float(r[1])-(t-base).total_seconds()/86400)*24,2) for r,t in zip(rows,times)]
changes=[i for i in range(1,len(rows)) if off[i]!=off[i-1]]
assert len(changes)==1;i=changes[0];j=i
while rows[j][2].strip()=='NaN':j+=1
assert j-i==8 and off[i-1]==-1 and off[i]==-5
assert rows[i-1][2]=='33305' and rows[j][2]=='33314'
assert (times[i]-times[i-1]).total_seconds()==270*60
assert all(all(v.strip()=='NaN' for v in r[2:]) for r in rows[i:j])
fields=['source_line_1based','printed_timestamp','decimal_day_original','record_original','decimal_minus_printed_hours_rounded','air_temperature_C_original']
with (out/'campbell_clock_boundary.csv').open('w',newline='') as h:
 w=csv.writer(h);w.writerow(fields)
 for k in range(i-3,j+3):w.writerow([k+5,rows[k][0],rows[k][1],rows[k][2],off[k],rows[k][4]])
result=dict(version='MS03-Campbell-clock-audit-v1',date='2026-11-15',source_doi='10.5281/zenodo.10553882',source_md5=hashlib.md5(f.read_bytes()).hexdigest(),rows=len(rows),offset_definition='24*(decimal_day - naive printed-time days since 2009-01-01);not a UTC offset',change_source_line_1based=i+5,last_before=rows[i-1][:3],first_after=rows[i][:3],first_record_after_nan_block=rows[j][:3],nan_rows=j-i,printed_boundary_step_minutes=270,decimal_boundary_step_minutes=(float(rows[i][1])-float(rows[i-1][1]))*1440,regime_offsets_hours=[-1,-5],interpretation='Four-hour field discrepancy begins at the eight-row NaN insertion documented by author QA; exact generating code and correct time basis remain unverified.',correction_applied=False,hobo_read_or_aligned=False,required_evidence=['University_Valley_Met_Station_Calibration_all.m and dependencies','unprocessed Campbell logger files around 2012-10-28','2012 clock/reset/download deployment log and export time-vector convention'])
(out/'campbell_clock_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: one offset transition; eight all-channel NaN rows; RECORD33305->33314; no clock correction or HOBO input.')
