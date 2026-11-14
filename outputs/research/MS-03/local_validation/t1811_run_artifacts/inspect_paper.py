"""Read an original author-deposited PDF; retain locators/hashes, not full text."""
from pathlib import Path
import hashlib,json
from pypdf import PdfReader,__version__
O=Path(__file__).resolve().parent
p=O/'sources/seelos2024_overview.pdf';b=p.read_bytes();record=json.loads((O/'sources/caltech_record.json').read_text())
f=record['files']['entries']['1-s2.0-S0019103523001896-main.pdf']
assert hashlib.md5(b).hexdigest()==f['checksum'].split(':')[1] and len(b)==f['size']
r=PdfReader(p);read=[]
for page,locator in [(24,'Fig21; sections6.4-6.6'),(25,'section6.6; Fig22; Fig23 caption'),(26,'sections6.7-6.11'),(32,'Data availability')]:
    s=r.pages[page-1].extract_text()
    read.append(dict(pdf_page_1based=page,printed_page=page,locator=locator,extracted_text_sha256=hashlib.sha256(s.encode()).hexdigest(),scope='complete indicated page text read; pages24-26 additionally rendered and visually checked'))
assert '6.8.' in r.pages[25].extract_text()
result=dict(source_url='https://authors.library.caltech.edu/records/h6pv6-fhf02',doi='10.1016/j.icarus.2023.115612',pdf_sha256=hashlib.sha256(b).hexdigest(),provider_md5_verified=True,pdf_pages=len(r.pages),pypdf_version=__version__,record_file_count=record['files']['count'],record_related_identifiers=record.get('metadata',{}).get('related_identifiers'),read_pages=read,
    embedded_file_count=len(r.attachments),T1811_text_hits=sum(p.extract_text().upper().count('T1811')for p in r.pages),
    fig23_support=dict(latitude_N=[17.0,19.5],longitude_E=[76.0,79.0],region='Jezero',RGB_nm=[716,599,534],both_autostretched=True,overlaps_fixed_MS03_roi=False,usable_MS03_BD1500_pre_post_pair=False),
    actual_coefficients_or_run_files_obtained=False,license='CC BY-NC-ND4.0; original PDF local-only, not republished or altered')
(O/'paper_read_scope.json').write_text(json.dumps(result,indent=2)+'\n')
