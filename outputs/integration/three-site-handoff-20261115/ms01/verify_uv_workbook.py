#!/usr/bin/env python3
"""Re-download four Zenodo v1 observations exports and compare published workbook with text.
Requires Python and openpyxl; no workbook editing, time correction, joins across instruments,
or material interpretation. Optionally supply cached inputs with --inputs.
"""
import argparse, collections, csv, datetime as dt, hashlib, json, math, pathlib, urllib.parse, urllib.request
from openpyxl import load_workbook

SOURCES = {
    'hobos.xlsx':('UV 2009_2011 All Hobos.xlsx','7ab4bf2692ef83c5a3d4a5347b8a71c8'),
    'shal8.txt':('UniversityV_09_13_Hobo_shal8cm_data_good_only_calibrated.txt','b5aed600dbdfc30d44c96720ddf34ae4'),
    'med22.txt':('UniversityV_09_13_Hobo_med22cm_data_good_only_calibrated.txt','87a4f1d870b50c3e8cb508d827d35cee'),
    'deep36.txt':('UniversityV_09_13_Hobo_deep36cm_data_good_only_calibrated.txt','ce95463da241db7209c49b07ff4772df'),
}
MAP = [('S8','shal8.txt',0,2,3),('M22','med22.txt',5,4,5),('D36','deep36.txt',10,2,4)]
parser=argparse.ArgumentParser()
parser.add_argument('--inputs',type=pathlib.Path,required=True)
parser.add_argument('--output',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent)
args=parser.parse_args()
args.inputs.mkdir(exist_ok=True,parents=True); args.output.mkdir(exist_ok=True,parents=True)
sources={}
for short,(name,expected) in SOURCES.items():
    path=args.inputs/short
    url='https://zenodo.org/records/10553882/files/'+urllib.parse.quote(name)+'?download=1'
    if not path.exists():
        with urllib.request.urlopen(url,timeout=30) as opened:
            path.write_bytes(opened.read())
    b=path.read_bytes()
    md5=hashlib.md5(b).hexdigest()
    if md5!=expected: raise ValueError(f'{name}: MD5 mismatch')
    sources[short]={'url':url,'bytes':len(b),'provider_md5':expected, 'sha256':hashlib.sha256(b).hexdigest()}
workbook=load_workbook(args.inputs/'hobos.xlsx', read_only=True, data_only=False)
assert len(workbook.sheetnames)==1
sheet=workbook.active
rows=list(sheet.values)
def num(item):
    try:
        n=float(item)
        return n if math.isfinite(n) else None
    except (TypeError,ValueError):
        return None
result=[]; all_differences=[]
for station,src,start,tupper,tice in MAP:
    values={}
    with (args.inputs/src).open(newline='') as f:
        reader=csv.reader(f); header=next(reader); units=next(reader)
        assert units[0]==rows[1][start]=='GMT+13:00'
        if station=='M22':
            assert header[tupper]=='Med_cm1_T'
        source_time_minmax=[]
        for rownum,row in enumerate(reader,3):
            if not row or not row[0].strip(): continue
            when=dt.datetime.strptime(row[0].strip(),'%m/%d/%Y %H:%M')
            assert when not in values
            values[when]=(num(row[tupper]), num(row[tice]),rownum)
            dd=dt.datetime(2009,1,1)+dt.timedelta(days=float(row[1]))
            source_time_minmax.append((dd-when).total_seconds())
    cells=[(row[start],num(row[start+1]),num(row[start+2]),i,row[start+3])
           for i,row in enumerate(rows[2:],3) if isinstance(row[start],dt.datetime)]
    assert len({t for t,*_ in cells})==len(cells)
    intervals=collections.Counter((b[0]-a[0]).total_seconds() for a,b in zip(cells,cells[1:]))
    both=sum(1 for _,a,b,*_ in cells if a is not None and b is not None)
    match=[0,0]; miss=[0,0]; diff=[0,0]; xlsx_only=0; maxabs=[0.,0.]
    for when,a,b,i,_ in cells:
        if when not in values:
            xlsx_only+=1; continue
        ta,tb,line=values[when]
        for j,(work,txt) in enumerate(((a,ta),(b,tb))):
            if work is None and txt is None: miss[j]+=1
            elif work is not None and txt is not None and work==txt: match[j]+=1
            else:
                diff[j]+=1
                if work is not None and txt is not None: maxabs[j]=max(maxabs[j],abs(work-txt))
                all_differences.append({'station':station,'printed_time':when.isoformat(), 'channel':['upper','ice_interface'][j], 'xlsx_row':i,'text_line':line,'xlsx_value_c':work,'text_value_c':txt})
    used={row[0] for row in cells}
    result.append(dict(station=station, workbook_upper=rows[0][start+1],workbook_interface=rows[0][start+2], workbook_timestamps=len(cells),
        xlsx_start=cells[0][0].isoformat(), xlsx_last=cells[-1][0].isoformat(), workbook_non_hour_steps=sum(n for a,n in intervals.items() if a!=3600),
        workbook_numeric_pairs=both, workbook_no_numeric_pair=len(cells)-both, text_timestamps=len(values),
        text_first=min(values).isoformat(),text_last=max(values).isoformat(),xlsx_unmatched_date=xlsx_only,text_unmatched_date=len(set(values)-used), text_extra_numeric_pairs=sum(1 for t in set(values)-used if all(v is not None for v in values[t][:2])),
        upper_equal=match[0],interface_equal=match[1],upper_both_missing=miss[0],interface_both_missing=miss[1],
        upper_difference=diff[0],interface_difference=diff[1],upper_max_abs_delta_c=maxabs[0],interface_max_abs_delta_c=maxabs[1],
        txt_decimal_minus_printed_min_s=min(source_time_minmax),txt_decimal_minus_printed_max_s=max(source_time_minmax),
        saturation_formula_rows=sum(isinstance(row[-1],str) and row[-1].startswith('=') for row in cells)))
assert all(r['workbook_timestamps']==r['upper_equal']+r['upper_both_missing']+r['upper_difference']+r['xlsx_unmatched_date'] for r in result)
assert all(r['workbook_timestamps']==r['interface_equal']+r['interface_both_missing']+r['interface_difference']+r['xlsx_unmatched_date'] for r in result)
with (args.output/'university_valley_workbook_comparison.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(result[0])); w.writeheader(); w.writerows(result)
with (args.output/'university_valley_workbook_differences.csv').open('w',newline='') as f:
    fields=['station','printed_time','channel','xlsx_row','text_line','xlsx_value_c','text_value_c']
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(all_differences)
facts={'sources':sources,'worksheet':sheet.title,'worksheet_count':len(workbook.sheetnames),
       'worksheet_size':[sheet.max_row,sheet.max_column],
       'formulas_vapour_example':rows[2][3], 'formula_first_year_summary':rows[2][19],
       'w_ac_ad_label':rows[0][28:30], 'w_ac_ad_nonempty_cell_rows':[i for i,row in enumerate(rows,1) if any(x is not None for x in row[28:30])],
       'w_ac_ad_header_and_summary':[row[28:30] for row in rows[:6]],
       'printed_time_basis':'GMT+13:00 as labelled in both processed exports, not verified physical time',
       'notes':'Row matching is workbook-vs-text for each station only; not synchronizing stations or loggers.'}
(args.output/'university_valley_workbook_provenance.json').write_text(json.dumps(facts,indent=2)+'\n')
print(json.dumps(result,indent=2))
