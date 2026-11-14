"""Descriptive University Valley known-interface comparison; no ice inversion.

Run with Python 3.11+ and numpy:
  .venv/bin/python outputs/research/MS-01/thermal_followup/analyze.py --raw-dir /tmp/ms01_uv_followup_raw
Raw files must match the source manifest. This script writes only its own folder.
"""
from pathlib import Path
from datetime import datetime,timedelta
import argparse,csv,gzip,hashlib,json
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
START=datetime(2010,11,7);END=datetime(2010,11,18)
EPOCH=datetime(2009,1,1)

# Numeric indices are zero-based and checked against the exact author header prefix.
# For S, an extra H in the late RH heading is retained as an explicit header defect.
SPECS={
 'S8':dict(filename='UniversityV_09_10_Hobo_shal8cm_data_good_only_calibrated.txt',md5='c86d19365c2deb4f1d6e71109cbb18cc',skip=2,step_minutes=60,logger='U12-008 serial 1122968',ice_m=.08,
    channels=[('upper','Shal_surf_T',2,0.),('ice','Shal_Ice8cm_T',3,.08),('below','Shal_InIce15cm_T',4,.15)],comparison='same U12 logger channels'),
 'M22':dict(filename='UniversityV_09_10_Hobo_med22cm_data_good_only_calibrated.txt',md5='71a790d5594bc89e621e3f5766c87948',skip=2,step_minutes=60,logger='U12-008 serial 2432937',ice_m=.22,
    channels=[('upper','Med_cm1_T',4,.01),('middle','Med_cm12_T',2,.12),('ice','Med_Ice22cm_T',5,.22),('below','Med_InIce27cm_T',3,.27)],comparison='same U12 logger channels; upper is 1 cm, not skin surface'),
 'D36':dict(filename='UniversityV_09_10_Hobo_deep36cm_data_good_only_calibrated.txt',md5='005d3a762723c0654aa3d4c80bebf9c2',skip=2,step_minutes=60,logger='U12-008 serial 2432936',ice_m=.36,
    channels=[('upper','Deep_surf_T',2,0.),('middle','Deep_cm10_T',3,.10),('ice','Deep_ice36cm_T',4,.36),('below','Deep_InIce42cm_T',5,.42)],comparison='same U12 logger channels'),
 'W42_Campbell':dict(filename='UniversityV_09_10_Campbell_data_good_only_calibrated.txt',md5='ae2133eac5c92c695c5f6ef93bcbbd25',skip=4,step_minutes=30,logger='Campbell CR1000 serial 28046 per author export',ice_m=.42,
    channels=[('upper','T107_surf',10,0.),('middle','T107_10cm',11,.10),('ice','T107_ice42cm',12,.42),('below','T107_InIce49cm',13,.49)],comparison='same CR1000 channels; prior W example reproduced independently'),
 'W42_HOBO':dict(filename='UniversityV_09_10_Hobo_WeatherStation_data_good_only_calibrated.txt',md5='0c138af0770ec15d4a4942a66507328f',skip=2,step_minutes=60,logger='Separate U23 T/RH loggers at each depth; not one common logger',ice_m=.42,
    channels=[('upper','Surf_T',5,0.),('middle','cm20_T',8,.20),('ice','ice42cm_T',11,.42)],comparison='cross-logger descriptive amplitude ratio only; no relative-phase interpretation')}

def parse_time(value):
    value=value.strip()
    try:return datetime.fromisoformat(value)
    except ValueError:return datetime.strptime(value,'%m/%d/%Y %H:%M')

def fit(hours,values,semi=False):
    angle=2*np.pi*hours/24
    cols=[np.ones(len(hours)),hours-hours.mean(),np.sin(angle),np.cos(angle)]
    if semi:cols += [np.sin(2*angle),np.cos(2*angle)]
    design=np.array(cols).T
    coef,_,rank,_=np.linalg.lstsq(design,values,rcond=None)
    if rank!=design.shape[1]:raise ValueError('Insufficient model rank')
    predicted=np.einsum('ij,jk->ik',design,coef)
    return dict(amplitude=np.hypot(coef[2],coef[3]),rmse=np.sqrt(np.mean((values-predicted)**2,axis=0)),
                phase=np.arctan2(coef[3],coef[2]),coefficients=coef)

def write_csv(name,rows):
    with (HERE/name).open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,list(dict.fromkeys(k for r in rows for k in r)),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)

def load(path,spec):
    b=path.read_bytes();assert hashlib.md5(b).hexdigest()==spec['md5'],path
    rows=list(csv.reader(b.decode('utf-8-sig').splitlines()))
    header=[s.strip() for s in rows[1 if spec['skip']==4 else 0]]
    units=[s.strip() for s in rows[2 if spec['skip']==4 else 1]]
    records=rows[spec['skip']:]
    for _,name,i,_ in spec['channels']:assert header[i]==name,(path,header[i],name)
    times=[parse_time(r[0]) for r in records]
    values=np.array([[float(r[c[2]]) for c in spec['channels']] for r in records])
    differences=np.array([(t2-t1).total_seconds()/60 for t1,t2 in zip(times,times[1:])])
    assert len(times)==len(set(times)) and all(differences>0),'Duplicate or unordered author times'
    # Decimal days differ by a constant convention between systems; preserve, never fix.
    decimal_index=1
    offsets=np.array([((EPOCH+timedelta(days=float(r[decimal_index])))-t).total_seconds()/3600 for r,t in zip(records,times)])
    primary=np.array([START<=t<END for t in times])
    common=primary&np.isfinite(values).all(axis=1)
    hours=np.array([(t-START).total_seconds()/3600 for t in times])[common]
    sample=values[common]
    assert len(sample)>4
    model=fit(hours,sample);semi=fit(hours,sample,True)
    days=np.floor(hours/24).astype(int)
    stability=[]
    for day in np.unique(days):
        ix=days!=day
        fitted=fit(hours[ix],sample[ix])
        stability.append(fitted['amplitude'])
    stability=np.array(stability)
    all_gaps=[]
    for i,delta in enumerate(differences):
        if delta!=spec['step_minutes']:all_gaps.append(dict(before=times[i].isoformat(),after=times[i+1].isoformat(),minutes=float(delta)))
    qa=dict(filename=path.name,bytes=len(b),md5=spec['md5'],sha256=hashlib.sha256(b).hexdigest(),
            rows=len(records),header_fields=len(header),unit_fields=len(units),record_width_counts={str(n):sum(len(r)==n for r in records) for n in set(map(len,records))},
            first_printed_time=times[0].isoformat(),last_printed_time=times[-1].isoformat(),
            time_label=units[0],nominal_step_minutes=spec['step_minutes'],
            header_width_mismatch=len(header)!=len(units),header=header,unit_header=units,
            duplicate_times=0,negative_time_steps=0,non_nominal_intervals=all_gaps,
            decimal_day_minus_printed_hour_min=float(offsets.min()),decimal_day_minus_printed_hour_max=float(offsets.max()),
            decimal_day_note='Fractional day rounding retained; this arithmetic offset is not a validated timezone correction.',
            primary_rows=int(primary.sum()),common_valid_rows=int(common.sum()),expected_primary_rows=int((END-START).total_seconds()/60/spec['step_minutes']),
            sensors=[],sample_support='Known-ice sites only; no controlled ice-free material counterpart.',
            clock_limit='Printed dates only; no inter-logger clock verification or UTC conversion.')
    stats=[];export=[]
    for j,(role,name,index,depth) in enumerate(spec['channels']):
        valid=np.isfinite(values[:,j]);warm=primary&valid
        qa['sensors'].append(dict(column=name,role=role,source_index_0_based=index,depth_m=depth,valid=int(valid.sum()),missing=int((~valid).sum()),
                                  primary_finite=int(warm.sum()),whole_file_below_minus40=int((values[valid,j]<-40).sum()),
                                  primary_below_minus40=int((values[warm,j]<-40).sum())))
        phase_same_logger = not spec['comparison'].startswith('cross-logger')
        lag=(model['phase'][0]-model['phase'][j])*24/(2*np.pi)
        lag=float((lag+12)%24-12)
        stats.append(dict(column=name,role=role,depth_m=depth,common_n=len(sample),
                          amplitude_K=float(model['amplitude'][j]),amplitude_to_upper_ratio=float(model['amplitude'][j]/model['amplitude'][0]),
                          residual_rmse_K=float(model['rmse'][j]),leave_one_day_amplitude_min_K=float(stability[:,j].min()),
                          leave_one_day_amplitude_max_K=float(stability[:,j].max()),amplitude_with_12h_nuisance_K=float(semi['amplitude'][j]),
                          leave_one_day_ratio_min=float((stability[:,j]/stability[:,0]).min()),
                          leave_one_day_ratio_max=float((stability[:,j]/stability[:,0]).max()),
                          relative_lag_to_upper_h=lag if phase_same_logger else None,
                          lag_interpretation='24h harmonic modulo [-12,12); descriptive within same logger only; not absolute local solar phase' if phase_same_logger else 'not interpreted: separate U23 clocks'))
    for source_index in np.flatnonzero(common):
        record=records[source_index];time=times[source_index]
        export.append(dict(printed_timestamp=time.isoformat(),source_timestamp=record[0].strip(),source_line_1based=int(source_index+spec['skip']+1),
                           **{c[1]:float(record[c[2]]) for c in spec['channels']},
                           **{c[1]+'__source':record[c[2]].strip() for c in spec['channels']}))
    return qa,stats,export

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--raw-dir',type=Path,required=True);args=parser.parse_args()
    qas={};summaries={};exports=[];table=[];monthly=[]
    for station,spec in SPECS.items():
        path=args.raw_dir/spec['filename']
        if not path.exists() and station=='W42_Campbell':path=ROOT/'data/raw/earth/university_valley'/spec['filename']
        qa,summary,records=load(path,spec)
        qas[station]=qa;summaries[station]=summary
        for record in records:
            for role,name,_,depth in spec['channels']:
                exports.append(dict(station=station,printed_timestamp=record['printed_timestamp'],source_timestamp=record['source_timestamp'],source_line_1based=record['source_line_1based'],column=name,depth_m=depth,temperature_C=record[name],source_numeric_string=record[name+'__source'],unit='degree_C',source_filename=spec['filename']))
        for row in summary:table.append(dict(station=station,**row,logger=spec['logger'],comparison=spec['comparison']))
    payload=dict(starting_sha='33f78ed986b0c39585dc4224b5f68bd6a7e9bed7',source_doi='10.5281/zenodo.10553882',
                 start_inclusive=START.isoformat(),end_exclusive=END.isoformat(),
                 primary_window_reason='Fixed before inspecting S/M/D data; same printed-date window as prior W analysis.',
                 method='OLS intercept + centered linear trend + 24h sin/cos; half-amplitudes, no gap filling',
                 sensitivity='Leave-one-printed-day-out min/max and added 12h nuisance harmonic; neither is a confidence interval or new calibration.',
                 qa=qas,results=summaries,
                 limits=['All primary records are author-calibrated/filtered, not untouched logger bytes.',
                         'Within-station common valid samples; no cross-station or cross-instrument join.',
                         'S/D published coordinates conflict with 2009 deployment note; station keys refer to export depth and logger serial.',
                         'Material, shadowing, radiation, wind and sensor coupling are uncontrolled across sites.',
                         'No inference of MS-01 ice, depth, thermal inertia, detection accuracy or a new physical mechanism.'])
    (HERE/'comparison.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    write_csv('amplitudes.csv',table)
    write_csv('primary_temperature_records.csv',exports)
    # Deterministic compressed copy is the durable row-level handoff; plain CSV is optional scratch.
    text=(HERE/'primary_temperature_records.csv').read_bytes()
    with (HERE/'primary_temperature_records.csv.gz').open('wb') as stream:
        with gzip.GzipFile(fileobj=stream,mode='wb',filename='',mtime=0) as archive:archive.write(text)
    (HERE/'primary_temperature_records.csv').unlink()
    print(json.dumps({s:{'common':qas[s]['common_valid_rows'],'amplitudes_K':[r['amplitude_K'] for r in summaries[s]],'ice_upper_ratio':next(r['amplitude_to_upper_ratio'] for r in summaries[s] if r['role']=='ice')} for s in summaries},indent=2))

if __name__=='__main__':main()
