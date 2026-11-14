"""Inventory and cross-reference checks; no physical parameter calculation."""
from pathlib import Path
from html.parser import HTMLParser
import csv,hashlib,json,re,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent;P=O.parent;S=O/'sources'
def sha(b):return hashlib.sha256(b).hexdigest()
def table(name,rows):
    with (O/name).open('w',encoding='utf-8-sig',newline='')as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def local_tag(e):return e.tag.split('}')[-1]
def items(root,name):return [(e.text or '').strip() for e in root.iter() if local_tag(e)==name]
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,t,a):
        if t=='a':self.links.append(dict(a).get('href',''))
def main():
    inventory=list(csv.reader((S/'collection_data_mrdr_inventory.csv').open(newline='')))
    assert len(inventory)==7056 and all(len(x)==2 for x in inventory)
    hits=[x for x in inventory if ':t1811_' in x[1]]
    assert len(hits)==4
    table('T1811_inventory_members.csv',[dict(member_status=a,lidvid=b,source_url='https://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-multispectral-v1/mrocr_3201/mrdr/collection_data_mrdr_inventory.csv') for a,b in hits])
    bundle=ET.parse(S/'bundle_crism_mrdr.xml').getroot()
    members=[]
    for e in bundle.iter():
        if local_tag(e)=='Bundle_Member_Entry':members.extend(items(e,'lid_reference'))
    collection=ET.parse(S/'collection_data_mrdr.xml').getroot()
    assert items(collection,'records')==['7056']
    all_refs=[];products=[]
    labels=[('AL',P/'production_history/sources/T1811_AL_PDS4.xml'),('SU',P/'production_history/sources/T1811_SU_PDS4.xml'),('DE',S/'T1811_DE.xml'),('WV',S/'T1811_WV.xml')]
    for kind,path in labels:
        root=ET.parse(path).getroot();lid=items(root,'logical_identifier')[0]
        assert any(lid+'::1.0'==x[1] for x in hits)
        names=items(root,'file_name');versions=items(root,'program_version')
        products.append(dict(product_family=kind,logical_identifier=lid,source_path=str(path.relative_to(P)),source_sha256=sha(path.read_bytes()),file_names_json=json.dumps(names),software_versions_json=json.dumps(versions),file_role='delivered product + label/header metadata; not a stage-paired intermediate'))
        for e in root.iter():
            tag=local_tag(e)
            if tag in ['lid_reference','lidvid_reference','reference_type','program_version','program_stop_date_time']:
                all_refs.append(dict(product_family=kind,xml_tag=tag,value=(e.text or '').strip(),source_path=str(path.relative_to(P))))
    table('T1811_product_files.csv',products);table('T1811_label_references.csv',all_refs)
    # Reuse the previously acquired, pinned original index; extract exact records.
    old=P/'official_resources/sources/mrdr_index_index.tab';b=old.read_bytes();lbl=(S/'index.lbl').read_text()
    recbytes=int(re.search(r'RECORD_BYTES\s*=\s*(\d+)',lbl)[1]);n=int(re.search(r'FILE_RECORDS\s*=\s*(\d+)',lbl)[1])
    assert len(b)==recbytes*n
    cols=[]
    for m in re.finditer(r'OBJECT\s*=\s*COLUMN\b(.*?)END_OBJECT\s*=\s*COLUMN',lbl,re.S):
        z=m[1];cols.append(dict(name=re.search(r'\bNAME\s*=\s*([^\r\n]+)',z)[1].strip().strip('"'),start_byte=int(re.search(r'\bSTART_BYTE\s*=\s*(\d+)',z)[1]),bytes=int(re.search(r'\bBYTES\s*=\s*(\d+)',z)[1])))
    selected=[];excerpt=b''
    for i in range(n):
        row=b[i*recbytes:(i+1)*recbytes]
        if b't1811_' in row.lower():
            excerpt+=row
            for c in cols:
                v=row[c['start_byte']-1:c['start_byte']-1+c['bytes']].decode('ascii').strip().strip('"')
                selected.append(dict(record_0based=i,byte_offset=i*recbytes,field=c['name'],value=v))
    assert len(excerpt)==4*recbytes
    (S/'T1811_original_index_records.tab').write_bytes(excerpt)
    table('T1811_index_fields.csv',selected)
    listing=Links();listing.feed((P/'production_history/sources/listing_mrocr_3201_mc03.html').read_text())
    files=[x for x in listing.links if '/t1811_' in x]
    assert len(files)==15
    result=dict(starting_main_sha='fee734610c6bacc57880eaaba1a1301f09fdd4d6',roi='57.50..58.00N;242.00..242.50E;planetocentric/east-positive',
        bundle_members=members,data_inventory_records=len(inventory),T1811_members=4,T1811_physical_listing_files=len(files),T1811_file_urls=files,
        index_source=dict(path=str(old.relative_to(P)),bytes=len(b),sha256=sha(b),record_bytes=recbytes,records=n,selected_records_0based=sorted(set(x['record_0based']for x in selected)),excerpt_sha256=sha(excerpt)),index_column_count=len(cols),
        inventoried_run_configuration='not_identified_in_checked_bundle',inventoried_optimization_coefficients='not_identified_in_checked_bundle',inventoried_pre_post_arrays='not_identified_in_checked_bundle',
        global_absence_claim=False,source_five_strips_are_complete_optimization_network='unknown',
        reproducible_stage_replay=False,quantitative_residual_cause='unknown',corrected_values_generated=False)
    (O/'inventory_audit.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
