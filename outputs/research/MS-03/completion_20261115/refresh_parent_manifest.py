#!/usr/bin/env python3
"""Refresh metadata only; keep prior manifest and input identities explicit."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
OUT=ROOT/'outputs/research/MS-03'
def digest(path):
    data=path.read_bytes();return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def main():
    path=OUT/'manifest.json';history=HERE/'parent_manifest_before_completion_20261115.json'
    if not history.exists():history.write_bytes(path.read_bytes())
    original=json.loads(history.read_text());m=json.loads(path.read_text())
    m['historical_version']=original.get('version');m['version']='MS03-completion-20261115-v1'
    m['historical_branch']=original.get('branch');m['branch']='research/ms-03-earth-analogs'
    m['initial_research_date_taipei']=original.get('research_date_taipei');m['research_date_taipei']='2026-11-15'
    m['historical_outputs']=original['outputs'];m['historical_outputs_commit']='234e58a8a0a0a9966e97e1b13d7ccc587cf3e8aa'
    m['historical_inputs']=original['inputs']
    m['inputs']=json.loads((HERE/'shared_input_verification.json').read_text())['pinned_inputs']
    m['sources']=json.loads((OUT/'sources.json').read_text())
    current=[]
    for item in original['outputs']:
        value=dict(item);p=ROOT/item['path']
        if p.exists():value.update(digest(p));value['verification']='recomputed_from_current_local_bytes'
        else:value['verification']='inherited_baseline_assertion_not_recomputed'
        current.append(value)
    for p in [HERE/'manifest.json',HERE/'file_inventory.csv']:
        if p.exists():current.append(dict(digest(p),verification='recomputed_from_current_local_bytes'))
    m['outputs']=current
    m['current_completion']={'date_taipei':'2026-11-15','baseline_main_commit':'234e58a8a0a0a9966e97e1b13d7ccc587cf3e8aa','branch':'research/ms-03-earth-analogs','report':'docs/research/MS-03/report.md','history_report':'docs/research/MS-03/report_history_before_completion_20261115.md','complete_file_inventory':'outputs/research/MS-03/completion_20261115/file_inventory.csv','manifest':'outputs/research/MS-03/completion_20261115/manifest.json','requirement_audit':'outputs/research/MS-03/completion_20261115/requirement_audit.csv','publication_receipt':'outputs/research/MS-03/completion_20261115/publication_receipt.json','legacy_outputs_scope':'Original94 outputs are retained with their baseline provenance; current full MS03 coverage is the inventory, including local_validation.','all_scientific_problems_solved':False,'unknowns':'outputs/research/MS-03/completion_20261115/open_questions.csv'}
    m['historical_data_not_transferred']=original.get('data_not_transferred')
    m['data_not_transferred']=['All global Earth raw products are not duplicated by this supplement.','Unprocessed W logger/calibration/clock records and exact MRDR producer run artifacts remain unobtained.','Specified original source tables remain limited by the documented acquisition status; no absence inferred.']
    m['gaps']=original['gaps']+['Current source-specific status and executable verification protocols are in completion_20261115/open_questions.csv and the active report; downloaded data do not establish local ice truth.']
    path.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'current_parent_outputs':len(current),'source_ids':len(m['sources']),'inputs_retained':len(m['inputs'])}))
if __name__=='__main__':main()
