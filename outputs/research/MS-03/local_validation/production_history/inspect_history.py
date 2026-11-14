"""Inspect acquired documentation and metadata, never change spectral values.

Run with system Python after acquire.py. HTML text is decoded as Windows-1252;
style/script contents are omitted. Offsets refer to normalized visible text.
"""
from pathlib import Path
from html.parser import HTMLParser
import csv, hashlib, json, re, xml.etree.ElementTree as ET

O = Path(__file__).resolve().parent
S = O / 'sources'

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('style', 'script'): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('style', 'script'): self.skip -= 1
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def visible(path):
    p = Text(); p.feed(path.read_text(encoding='cp1252'))
    return ' '.join(' '.join(p.parts).split())

def sha(b): return hashlib.sha256(b).hexdigest()
def table(name, rows):
    with (O / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
    docs = []
    for filename, version, date, source_id in [
        ('historical_dpsis_20220930.htm', '1.3.7.6', '2022-06-22', 'PH-S01'),
        ('official_dpsis.htm', '1.3.7.7', '2024-11-05', 'PH-S02')]:
        b = (S / filename).read_bytes(); text = visible(S / filename)
        assert 'Version ' + version in text
        start = text.index('8. Reconciliation of Inter-strip Residuals')
        end = text.index('9. VNIR to IR Sensor Space Transform', start)
        section = text[start:end].strip()
        assert 'applied a second time' in section and '1-51 in Table 3-12' in section
        assert 'MRRAL multiband image' in text and 'BD1500_2' in text
        docs.append(dict(source_id=source_id, file='sources/'+filename,
            document_version=version, document_date=date, sha256=sha(b),
            read_scope='title/version; Appendix P3 sections 6-8, 11, 13; Table 3-12 BD1500_2 row',
            normalized_text_method='HTMLParser cp1252; omit style/script; collapse whitespace',
            section8_start_offset=start, section8_end_offset=end,
            section8_character_count=len(section), section8_sha256=sha(section.encode()),
            exact_production_flow_name_present='crism_mapping_execute_flow' in text,
            brief_quote='the optimization procedure is applied a second time'))
    (O/'history_sections.json').write_text(json.dumps(docs, indent=2)+'\n')

    ns = {'p':'http://pds.nasa.gov/pds4/pds/v1', 'proc':'http://pds.nasa.gov/pds4/proc/v1'}
    products = []
    for k in ['AL', 'SU']:
        path = S / ('T1811_'+k+'_PDS4.xml'); root = ET.parse(path).getroot()
        # Namespace version is declared by the XML; use local tag names rather
        # than infer a schema URI from the software's version string.
        fields = {}
        for e in root.iter():
            tag = e.tag.split('}')[-1]
            if tag in ['name','program_version','program_stop_date_time','creation_date_time','file_name']:
                if tag != 'name' or (e.text or '').strip() == 'crism_mapping_execute_flow':
                    fields.setdefault(tag, []).append((e.text or '').strip())
        assert fields['program_version'] == ['1.03.94']
        assert fields['name'] == ['crism_mapping_execute_flow']
        products.append(dict(product_family=k, source_file='sources/'+path.name,
            sha256=sha(path.read_bytes()), inspected_fields=fields,
            runtime_settings_obtained=False, intermediate_arrays_obtained=False,
            label_migration_is_not_observation_time=True))
    (O/'product_metadata.json').write_text(json.dumps(products,indent=2)+'\n')
    q=json.loads((O.parent/'bd1500_audit/results.json').read_text())
    result=dict(starting_main_sha='826780f0b270eebe9b6f2f64b8ba1ac5ddcc8177',
        historical_snapshot_utc='2022-09-30T18:58:40Z',
        section8_identical_across_read_versions=docs[0]['section8_sha256']==docs[1]['section8_sha256'],
        documented_summary_optimization_precedes_product_creation=True,
        exact_1_03_94_source_obtained=False, execution_settings_obtained=False,
        normalization_coefficients_obtained=False, paired_pre_post_data_obtained=False,
        quantitative_attribution='unknown', local_ice_presence='unknown',
        local_ice_depth_m='unknown', local_ice_fraction='unknown',
        original_scientific_values_changed=False, fitted_correction_applied=False,
        prior_numbers_reference='../bd1500_audit/results.json',
        prior_strict_residual_unchanged=q['cat64_minus_official_strict'],
        production_runtime_executed=False)
    (O/'results.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__': main()
