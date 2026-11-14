"""Reproducibly locate disclosed CAT functions; preserve raw code locally, inventory in Git."""
from pathlib import Path
import zipfile,json,hashlib
O=Path(__file__).resolve().parent;z=zipfile.ZipFile(O/'sources/CAT_v7_4_codeonly.zip');wanted=['crism_summary_bd1500_2.pro','crism_sumutil_band_depth.pro','crism_sumutil_single.pro','mro_crism_lookupwv.pro','crism_summary_icer1_2.pro','compute_summary_params_cev.pro'];out=[];flowmatches=[];nread=0
for info in z.infolist():
 if info.filename.endswith(('.pro','.txt','.md')):
  b=z.read(info);nread+=1
  if b'crism_mapping_execute_flow' in b.lower():flowmatches.append(info.filename)
 if any(info.filename.endswith('/'+w) for w in wanted):
  b=z.read(info);dest=O/'sources/cat_selected'/info.filename;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);lines=b.decode('latin1').splitlines();out.append(dict(member=info.filename,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),crc32=info.CRC,zip_member_time=info.date_time,source_url='https://pds-geosciences.wustl.edu/missions/mro/CAT_v7_4_codeonly.zip',match_line_numbers=[i+1 for i,x in enumerate(lines) if any(w in x.lower() for w in ['function ','img=0.5','(wc-wl)','mro_crism_lookupwv','keyword_set(hyper)','img=(img2','bd1500_2'])]))
(O/'disclosed_source_inventory.json').write_text(json.dumps(dict(members=out,readable_members_scanned=nread,production_flow_text_matches=flowmatches,production_flow_filename_matches=[n for n in z.namelist() if 'crism_mapping_execute_flow' in n.lower()],scope='This fetched CAT archive only, not all author material. No claim that production source is globally unavailable.'),indent=2)+'\n');print('Inventoried',len(out),'functions;',nread,'readable members scanned; production name matches',len(flowmatches))
