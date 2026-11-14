"""Reviewed artifact decisions and reproducibility handoff, not report prose."""
from pathlib import Path
import json
from inspect_inventory import table
O=Path(__file__).resolve().parent;P=O.parent
BASE='https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/'
PAPER='https://authors.library.caltech.edu/records/h6pv6-fhf02'
def main():
    sources=[
      ('RUN-S01',BASE+'bundle_crism_mrdr.xml','sources/bundle_crism_mrdr.xml','complete XML; five Bundle_Member_Entry records','Official bundle membership; no identified run-artifact collection; not global absence'),
      ('RUN-S02',BASE+'mrdr/collection_data_mrdr_inventory.csv','sources/collection_data_mrdr_inventory.csv','all7056 inventory rows parsed; four T1811 members selected','AL/SU/DE/WV product IDs only for T1811 in checked collection'),
      ('RUN-S03',BASE+'mrdr/collection_data_mrdr.xml','sources/collection_data_mrdr.xml','complete collection XML; File_Area_Inventory/records','7056 declared rows agrees with parsed inventory'),
      ('RUN-S04',BASE+'index/index.lbl','sources/index.lbl','complete57 column definitions; original index reused by exact record','Index observation/calibration fields are not a numerical run configuration or optimization table'),
      ('RUN-S05',BASE+'mrdr/mc03/t1811_mrrde_60n243_0327_4.xml','sources/T1811_DE.xml','complete XML references and file names; AL/SU pinned labels reused','Companion traceability metadata; no actual optimizer coefficients identified'),
      ('RUN-S06',BASE+'mrdr/mc03/t1811_mrrwv_60n243_0327_4.xml','sources/T1811_WV.xml','complete XML references and file names','Wavelength table metadata; not normalization coefficients'),
      ('RUN-S07',BASE+'errata.txt','sources/errata.txt','complete notes; August11,2023 and June29,2022 releases','Release chronology; no T1811 configuration or coefficient attachment located'),
      ('RUN-S08',PAPER,'sources/seelos2024_overview.pdf','original34-page PDF acquired; pp24-26 and32 read; pp24-26 rendered/checked','Fig21 optimizer artifacts; Fig23 is Jezero VNIR illustration, not a local BD1500 pair; availability points to PDS'),
      ('RUN-S09','https://authors.library.caltech.edu/api/records/h6pv6-fhf02','sources/caltech_record.json','complete record/file metadata','One deposited file, original paper; provider size and MD5 verified'),
      ('RUN-S10','https://ntrs.nasa.gov/api/citations/77934855965157','sources/ntrs_record.json','complete metadata; downloads field','No downloadable run artifacts obtained; metadata lead redirects to publication'),
      ('RUN-S11',BASE+'document/crism_dpsis.htm','../production_history/sources/official_dpsis.htm','section2.3.4.11 and3.9 naming/archive scope; previously acquired document','ADR lookup corrections and ordinary instrument CDR coefficients are distinct from stage6/8 interstrip parameters'),
    ]
    table('source_audit.csv',[dict(source_id=a,url=b,local_path=c,actual_read_scope=d,support_and_limit=e,date_taipei='2026-11-15')for a,b,c,d,e in sources])
    evidence=[
      ('RUN-E01','T1811 archive products','confirmed_in_checked_inventory','RUN-S01;RUN-S02;RUN-S03;RUN-S05;RUN-S06','4 logical products;15 listed physical files','bundle/data collection only; no claim all public archives exhaustively searched'),
      ('RUN-E02','actual execution configuration','unknown','RUN-S04;RUN-S05;RUN-S06','not obtained','Instrument/observation metadata or software version is not a recovered run options file'),
      ('RUN-E03','actual optimization coefficients','unknown','RUN-S05;RUN-S08;RUN-S11','not obtained','Fig21 describes model artifacts but supplies no T1811 numerical coefficient array'),
      ('RUN-E04','paired local normalization arrays','unknown','RUN-S08;RUN-S09','not obtained','Fig23 before/after region17.0-19.5N,76-79E; RGB716/599/534nm; both autostretched; outside MS03'),
      ('RUN-E05','optimization dependency set','unknown','RUN-S08','five local source strips are known, full required network unknown','Request actual connected dependencies, overlap/proximity constraints and anchors; local contributors alone do not document that network'),
      ('RUN-E06','numerical stage replay','not_performed_missing_inputs','RUN-E02;RUN-E03;RUN-E04;RUN-E05','no new predicted or corrected values','Prior formula-only values remain separate; documented mechanism does not quantify local residual'),
      ('RUN-E07','local ice presence/depth/content','unknown','RUN-E06','unknown','No new independent ice truth or validated spectral detection'),
    ]
    table('artifact_status.csv',[dict(evidence_id=a,item=b,status=c,source_ids=d,value=e,limits=f)for a,b,c,d,e,f in evidence])
    needs=[
      ('RUN-N01','build and execution','version-pinned source/executable, dependency manifest, caller/options, run ID/log','T1811 producer1.03.94; actual2023-07-18 run','unknown','Do not equate public CAT/JCAT or generic config with production build'),
      ('RUN-N02','optimizer inputs','overlap/proximity samples, design matrix, weighting vector, data vector, anchor IDs and masks','reflectance and summary optimization separately; Fig21 labels are artifact types only','unknown','Request actual run dependencies; five ROI contributors do not establish full optimization inputs'),
      ('RUN-N03','optimizer outputs','actual model parameter arrays and transformations; gains/offsets if actually used; units and indexing','per source strip, channel/parameter, sensor and stage','unknown','Do not estimate coefficients from final SU by fitting'),
      ('RUN-N04','paired intermediate arrays','AL and BD1500_2 before/after each relevant stage; matching masks/wavelengths/traceability IDs','same source pixel and acquisition; enough full context to reproduce transformations','unknown','Raw TRR3 versus final AL is not isolated interstrip normalization'),
      ('RUN-N05','projection/assembly replay','GLT, stack/template inputs, source index conventions and output masks','same tile grid and actual per-pixel source ordering','unknown','Storage byte offsets and map projection offsets are not optimizer coefficients'),
    ]
    table('replay_inputs_needed.csv',[dict(request_id=a,group=b,artifacts=c,required_support=d,status=e,misuse_to_avoid=f)for a,b,c,d,e,f in needs])
    retrievals=json.loads((O/'retrievals.json').read_text());logs=[]
    for i,r in enumerate(retrievals,1):
        logs.append(dict(log_id=f'LV-RUN{i:03}',date_taipei='2026-11-15',platform='urllib verified TLS',query_or_url=r['url'],status=r['status'],actual_read_scope='source_audit.csv; acquisition is not full-text reading',result=r.get('error',str(r.get('bytes'))+' bytes; recorded SHA256'),spatial_basis='T1811 artifact metadata; fixed MS03 ROI unchanged'))
    queries=[('web.search_query','"T1811" "CRISM" normalization','no run configuration located in returned results'),('web.search_query','"crism_mapping_execute_flow" configuration coefficients','no actual run coefficients obtained'),('web.search_query','"10.1016/j.icarus.2023.115612" supplementary data','Caltech original paper record located'),('web.search_query','"T1811_MRRAL_60N243_0327_4" configuration','no T1811 configuration identified'),('web.search_query','"T1811" "MRRSU" "gain"','no local coefficient table identified'),('web.search_query','"CRISM" "mapping" "optimization" Seelos "Zenodo"','no matched production artifact identified; unrelated analysis repositories not substituted'),('web.click','Caltech file download link47','web reader failed after download redirect; cause not established; direct stableURL system download succeeded'),('local PDF read','Caltech original PDF pp24-26,32','download MD5 verified; selected complete pages read; Fig21-23 checked visually'),('local pinned index','../official_resources/sources/mrdr_index_index.tab','reused previous original index; exact4 T1811 records extracted; no physical recalculation')]
    for i,(p,q,r) in enumerate(queries,len(logs)+1):logs.append(dict(log_id=f'LV-RUN{i:03}',date_taipei='2026-11-15',platform=p,query_or_url=q,status='searched_or_read',actual_read_scope=r,result=r,spatial_basis='software/archive provenance; Jezero example explicitly outside fixed ROI'))
    table('search_log.csv',logs)
    old=json.loads((P/'bd1500_audit/results.json').read_text())
    result=dict(starting_main_sha='fee734610c6bacc57880eaaba1a1301f09fdd4d6',quantitative_attribution='unknown',stage_replay_performed=False,actual_run_settings_obtained=False,actual_coefficients_obtained=False,paired_local_pre_post_data_obtained=False,scientific_values_changed=False,fitted_correction_applied=False,ice_presence='unknown',ice_depth_m='unknown',ice_fraction='unknown',old_residual_reference='../bd1500_audit/results.json',old_strict_residual_unchanged=old['cat64_minus_official_strict'],reason='actual stage replay inputs not obtained in bounded archive/author-source checks')
    (O/'replay_readiness.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
