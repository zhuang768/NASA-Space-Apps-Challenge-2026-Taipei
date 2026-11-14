#!/usr/bin/env python3
"""Promote pinned local-validation results into the MS-03 evidence registry.

Only descriptions/metadata are added. No observational array, coordinate,
timestamp, ice depth or optical parameter is corrected by this program.
"""
from pathlib import Path
import csv, hashlib, json

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'outputs/research/MS-03'
HERE=Path(__file__).resolve().parent
PIN='234e58a8a0a0a9966e97e1b13d7ccc587cf3e8aa'
URL='https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/'+PIN+'/'

def read(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);rows=list(reader)
    return reader.fieldnames,rows

def write(path,fields,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(rows)

def main():
    fields,rows=read(OUT/'evidence.csv')
    sources=json.loads((OUT/'sources.json').read_text())
    additions=[]
    def add(n,theme,metric,value,unit,period,depth,resolution,support,kind,file,locator,limits):
        sid='MS03C'+str(n).zfill(2);eid='MS03-LV-C'+str(n).zfill(2)
        path='outputs/research/MS-03/local_validation/'+file
        url=URL+path
        sources[sid]={'url':url,'locator':locator,'read_scope':'Full named retained calculation/QA record; upstream original sources and exact byte hashes remain in its package. This is project analysis, not a second independent observation.','access_date_taipei':'2026-11-15','source_kind':kind}
        row=dict(evidence_id=eid,candidate_id='MS-03',theme=theme,metric=metric,value=json.dumps(value,ensure_ascii=False,separators=(',',':')) if not isinstance(value,str) else value,unit=unit,period=period,measurement_depth_or_height=depth,resolution=resolution,spatial_support=support,evidence_type=kind,source_id=sid,source_url=url,source_locator=locator,read_scope=sources[sid]['read_scope'],status='bounded_result_not_ice_confirmation',limitations=limits)
        assert set(row)==set(fields)
        additions.append(row)
    add(1,'water_ice','conditional_native_model_interface',{'model_depth_m':0.103161566,'upper_regolith_TI':215.4277344},'m;J m-2 K-1 s-0.5','published2019 archived model','conditional interface;not measured','archived2pixels/degree;row64 col484 zero-based','native centre57.75N242.25E','published_model_locally_extracted','piqueux_native_cell.csv','candidate_id=MS-03;row_0based=64;column_0based=484; DOI10.22002/D1.1316','Model estimate is not independent ice confirmation, measured depth, abundance or TES equivalence; archived2ppd/paper3ppd chain remains bounded.')
    add(2,'terrain','MOC_retained_image_support',{'nonzero_in_cell_pixel_centres':9272742,'review_windows':3,'window_pixels':[512,512]},'count;pixel','2006-04-08T00:22:40.473 to00:22:50.285UTC','optical surface','3.000339463m map grid;not effective resolving power','S1700607_NA;fixed MS03 ROI;3 fixed windows only','archival_processed_image_and_derived_count','gap_completion/moc_summary.json','roi_valid_nonzero_pixel_centres;tiles;original_dimensions;source_sha256','No reliable closed Mars polygon dataset;no whole-cell feature census or absence result;original RDR already destriped/histogram-scaled/map-projected.')
    add(3,'water_ice','CRISM_numeric_calibration_centres',{'HSP_pass':966,'HSP_in_cell':1350,'MSP_pass':8516,'MSP_in_cell':9056},'count','HSP2014-02-10;MSP2010-05-25','surface/atmospheric optical signal;not buried ice interface','sampled1300-2200nm mapping channels;no interpolation','DDR-centre masks of two specific mapping observations','derived_numeric_and_calibration_QA','crism/qa.json','products;mask counts;matching DDR and WA calibration;original label flags','Not final cloud/frost/instrument QA, independent samples or whole-cell area coverage. ATMO_CORRECTION_FLAG covers atmospheric/photometric processing; PHOTOCLIN_CORRECTION_FLAG is a distinct slope-source control, not a photometric flag. No ice presence/absence inference.')
    add(4,'water_ice','MRDR_parameter_formula_residual',{'strict_centres':13169,'median_calculated_minus_official':0.0007114219669,'max_absolute_difference':0.01934733452},'1;count','source observations2006-2014;T1811 produced2023-07-18','optical processed mosaic;not subsurface interface','180.4662m native map grid;source centres strictly inside ROI','T1811 MRDR4 strict subset;115 boundary remaps excluded','derived_parameter_non_equivalence_diagnostic','bd1500_audit/results.json','strict subset BD1500_2 residual;production_history/README.md and t1811_run_artifacts/README.md','Summary-stage optimization is documented, but exact producer1.03.94 run settings/coefficients/paired intermediates are unavailable. No value correction, error attribution or ice threshold.')
    add(5,'water_ice','same_observation_radar_clutter_support',{'in_cell_GEOM_centres':65,'range_rows':269,'row_sampling_us':0.0375,'bandwidth_MHz':10},'count;us;MHz','2016-06-07T22:23:51.611 to22:24:01.059UTC','radar return;no validated subsurface pick','37.5ns sampling;ideal c/(2B)=14.9896m vacuum separation scale;not local detection performance','S_04624502;original rows2182-2450;columns2185-2249 one-based','archival_radar_and_same_track_clutter_model','gap_completion/radar_summary.json','array_shape;strict_roi_centre_count;row_sampling_us;source_inputs','Clutter is a model, not independent observation;no power subtraction;off-nadir scattering can be outside ROI;no dielectric inversion, measured depth or ice amount.')
    add(6,'water_ice','bounded_new_impact_catalogue_membership',{'catalogue_events':1203,'in_cell_event_points':0},'count','Daubar2022 author catalogue;individual periods retained in original rows','impact event coordinate;not image footprint','catalogue point support;coordinate header orientation checked','fixed MS03 ROI against this exact inclusion-defined catalogue','original_catalogue_point_membership_calculation','gap_completion/daubar2022_summary.json','total_records;ROI membership;source MD5;DOI10.5281/zenodo.6604912','Zero points is not zero image overlaps, no ice, no prior research or a replacement for Dundas2021 TableS4;other original tables remain unavailable.')
    # Use actual JSON keys, rather than guessed labels, in the catalogue locator.
    additions[-1]['source_locator']='rows;point_hits;original_headers;original_ice_flag_counts;source_sha256; DOI10.5281/zenodo.6604912'
    sources['MS03C06']['locator']=additions[-1]['source_locator']
    old={r['evidence_id']:r for r in rows}
    for row in additions:
        if row['evidence_id'] in old:
            if old[row['evidence_id']]!=row:
                assert row['evidence_id']=='MS03-LV-C06' and all(old[row['evidence_id']][k]==v for k,v in row.items() if k!='source_locator')
                old[row['evidence_id']]['source_locator']=row['source_locator']
        else:rows.append(row)
    write(OUT/'evidence.csv',fields,rows)
    (OUT/'sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
    write(HERE/'local_evidence_append.csv',fields,additions)
    source_rows=[dict(source_id=k,source_url=v['url'],source_locator=v.get('locator','unknown'),read_scope=v.get('read_scope','unknown'),access_date_taipei=v.get('access_date_taipei','unknown'),license=v.get('license','not specified in this registry')) for k,v in sorted(sources.items())]
    write(HERE/'source_crosswalk.csv',list(source_rows[0]),source_rows)
    records=[];index=[];seen={}
    for path in sorted(OUT.rglob('*search*log*.csv')):
        if path.name in {'all_search_records.csv','search_log_index.csv'}:continue
        header,table=read(path);rel=path.relative_to(ROOT).as_posix()
        index.append(dict(path=rel,stored_rows=len(table),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),columns_json=json.dumps(header,separators=(',',':'))))
        for n,row in enumerate(table,2):
            raw=json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':'));digest=hashlib.sha256(raw.encode()).hexdigest();rid='SREC-'+hashlib.sha256((rel+':'+str(n)).encode()).hexdigest()[:16]
            records.append(dict(record_id=rid,source_path=rel,source_csv_line=n,original_search_id=row.get('search_id',row.get('id','')),record_sha256=digest,exact_duplicate_of=seen.get(digest,''),original_row_json=raw));seen.setdefault(digest,rid)
    write(HERE/'all_search_records.csv',list(records[0]),records)
    write(HERE/'search_log_index.csv',list(index[0]),index)
    print(json.dumps({'evidence_rows':len(rows),'local_evidence_rows':len(additions),'sources':len(sources),'search_tables':len(index),'stored_search_rows':len(records)}))

if __name__=='__main__':main()
