"""Write human-reviewed evidence tables; no inferred calibration coefficients."""
from pathlib import Path
import csv, json
from inspect_history import table
O=Path(__file__).resolve().parent
BASE='https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/'
SIS=BASE+'document/crism_dpsis.htm'
OLD='https://web.archive.org/web/20220930185840id_/'+SIS

def main():
    sources=[
      ('PH-S01',OLD,'historical_dpsis_20220930.htm','full original HTML acquired; selected sections read','SIS1.3.7.6 dated2022-06-22; AppendixP3 sections6-8,11,13; Table3-12 BD1500_2 row21','Summary-product optimization documented before T1811 production; not a build archive'),
      ('PH-S02',SIS,'official_dpsis.htm','full original HTML acquired; selected sections read','SIS1.3.7.7 dated2024-11-05; same selected sections','P3 section8 normalized text identical to2022 snapshot; later document is not execution evidence'),
      ('PH-S03',BASE+'mrdr/mc03/t1811_mrrsu_60n243_0327_4.xml','T1811_SU_PDS4.xml','complete XML parsed','proc:Software_Program; File creation_date_time','Actual product declares crism_mapping_execute_flow1.03.94; stop2023-07-18T18:12:54Z; no settings or coefficients identified'),
      ('PH-S04',BASE+'mrdr/mc03/t1811_mrral_60n243_0327_4.xml','T1811_AL_PDS4.xml','complete XML parsed','proc:Software_Program; File creation_date_time','Companion AL declares same software/version; does not expose a pre/post pair'),
      ('PH-S05','https://www.hou.usra.edu/meetings/lpsc2022/pdf/2361.pdf','not acquired as local PDF','web reader:2 pages read; shell download403','LPSC2022 abstract2361 pp1-2','Authors describe graph/least-squares interstrip optimization; no exact1.03.94 source/settings'),
      ('PH-S06','https://doi.org/10.1016/j.icarus.2023.115712','not acquired','publisher author-manuscript search excerpt only; direct open403','section2.4 excerpt; scope does not include entire paper','Related HSP framework adapted from MRDRv4; Python wrapper plus IDL/Python/Matlab; not evidence of T1811 settings'),
      ('PH-S07','https://michael-s-phillips.github.io/cv/','author_phillips_cv.html','author CV hyperlinks inspected','publication DOI and software GitHub links','Author-linked analysis software located; no production flow obtained from these link checks'),
    ]
    table('source_audit.csv',[dict(source_id=a,url=b,local_source=c,actual_read_scope=d,locator=e,support_and_limit=f,date_taipei='2026-11-15') for a,b,c,d,e,f in sources])
    stage=[
      ('PH-ST01','reflectance optimization','P3 section6','MRRAL','confirmed_documented','weighted interstrip adjustment before summary evaluation'),
      ('PH-ST02','spectral summary evaluation','P3 section7','surface summaries from MRRAL','confirmed_documented','mapping nearest detector row; same nominal formula does not replay later stages'),
      ('PH-ST03','summary-product optimization','P3 section8','surface products1-51 including BD1500_2','confirmed_documented','second optimization; actual T1811 per-product transformations unknown'),
      ('PH-ST04','projection and assembly','P3 sections10-11','MRRAL/MRRSU/MRRDE tile','confirmed_documented','traceability template controls source consistency; no new local intermediate arrays obtained'),
      ('PH-ST05','numerical replay of actual tile','T1811 execution logs/coefficients','unknown','unknown','no executable/build/configuration or paired pre/post data; no corrected values'),
    ]
    table('processing_stages.csv',[dict(stage_id=a,stage=b,source_locator=c,output_or_support=d,status=e,limits=f,source_ids='PH-S01;PH-S02' if a!='PH-ST05' else 'PH-S03;PH-S04') for a,b,c,d,e,f in stage])
    history=[
      ('MRDRv1','SIS P3 section13','TRR1; older summary definitions; interstrip residuals retained','not_a_controlled_before_pair','Different inputs/formulas; no local v1 arrays obtained; guessed3001 URLs returned404'),
      ('MRDRv3','SIS P3 section13','TRR3; MRRIF/MRRDE; no MRRAL/MRRSU','not_a_controlled_before_pair','No SU counterpart in documented v3 product set; guessed3101 URLs returned404'),
      ('MRDRv4 T1811','PDS4 actual AL/SU labels','TRR3; actual producer1.03.94;2023-07-18','final_products_only','Delivered AL/SU do not supply missing intermediate summary stage'),
      ('JCATv1.0/v1.1','public releases API','2024-09-11/2024-10-31','different_tool','Public viewer releases postdate T1811; not historical production-flow builds'),
    ]
    table('version_history.csv',[dict(version=a,locator=b,documented_properties=c,comparison_status=d,limits=e) for a,b,c,d,e in history])
    missing=[
      ('PH-A01','exact1.03.94 source/executable/build hash','unknown','actual label identifies version only; exact GitHub code query0 hits in this search','version-pinned source or executable plus dependency/build manifest'),
      ('PH-A02','T1811 runtime configuration/options','unknown','PDS labels/listings inspected; no configuration file identified','caller flags; channel selection; masks; ADR references; optimization options'),
      ('PH-A03','reflectance pre/post optimization arrays','unknown','final AL is available; not a controlled pre/post pair','same strip/pixels/channels before and after stage6; valid masks'),
      ('PH-A04','summary pre/post optimization arrays','unknown','second stage documented; intermediates not obtained','same BD1500_2 pixels before and after stage8; source assignments'),
      ('PH-A05','per-strip/per-parameter optimization coefficients','unknown','method described, local weights/gains/offsets not obtained','coefficients, anchors, overlap graph, weights, fit diagnostics'),
      ('PH-A06','execution/build logs and run database','unknown','author material describes framework; no actual run archive obtained','run identifier, code revision, parameters, tasks and checksums'),
      ('PH-A07','documented second summary optimization','confirmed_documented','2022 and2024 section8 text hashes identical','does not identify actual residual magnitude for T1811'),
      ('PH-A08','quantitative explanation of MS03 residual','unknown','existing differences retained; documentation narrows mechanism, not numerical attribution','replay actual stages against actual intermediates; no fitted correction'),
      ('PH-A09','MS03 ice presence/depth/content','unknown','processing-history evidence is not independent local ice truth','validated spectral detection and independent subsurface observations'),
    ]
    table('availability.csv',[dict(item_id=a,item=b,status=c,evidence_or_attempt=d,needed_to_resolve=e) for a,b,c,d,e in missing])
    logs=[]
    for i,r in enumerate(json.loads((O/'retrievals.json').read_text()),1):
        logs.append(dict(log_id=f'LV-PH{i:03}',date_taipei='2026-11-15',platform=r.get('method','urllib verified TLS'),query_or_url=r['url'],status=r['status'],actual_read_scope='see source_audit.csv; listings/metadata/search response only unless specified',result=r.get('error',f"{r.get('bytes')} bytes retained; retrievals.json has SHA256"),spatial_basis='global workflow metadata; T1811 actual labels; fixed MS03 ROI unchanged'))
    web=[
      ('web.search_query','"crism_mapping_execute_flow" "1.03.94"','no standalone production source identified; searched public indexed results only'),
      ('web.search_query','"crism_mapping_execute_flow" source','no executable or configuration obtained; bounded search'),
      ('web.search_query','"A first look at CRISM hyperspectral mapping mosaicked data" manuscript','author manuscript excerpt found; direct publisher403; no full-text claim'),
      ('web.open','https://www.hou.usra.edu/meetings/lpsc2022/pdf/2361.pdf','2-page original read with web reader; no binary acquired by shell'),
      ('GitHub connector','https://api.github.com/search/repositories?q=org%3AJHUAPL+crism&per_page=100','connector rejected endpoint; shell fallback recorded separately; rejection not0 results'),
    ]
    for i,(p,q,r) in enumerate(web,len(logs)+1):logs.append(dict(log_id=f'LV-PH{i:03}',date_taipei='2026-11-15',platform=p,query_or_url=q,status='searched_or_read',actual_read_scope=r,result=r,spatial_basis='software provenance; no new Mars observation'))
    table('search_log.csv',logs)

if __name__=='__main__':main()
