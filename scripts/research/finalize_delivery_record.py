"""Finalize the fixed-scope MR-v3 evidence records; no scientific recalculation."""
import argparse
import collections
import csv
import hashlib
import json
import posixpath
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'outputs/consolidated/research_main_20261114'
VERSION = 'MR-20261114-v3-final'
ARCHIVE = ROOT / 'outputs/consolidated/backups/All_Data_before_MR_v3_a789fcdc9c0a.xlsx.bak'
WORKBOOK = ROOT / 'outputs/consolidated/NASA_Space_Apps_2026_All_Data.xlsx'
EH = ROOT / 'outputs/research/elephant_head_final'
NS = {'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def fingerprint(path):
    b = Path(path).read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
            'git_blob_sha': hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()}


def cell_values(path, requested):
    out = {}
    with zipfile.ZipFile(path) as z:
        book = ET.fromstring(z.read('xl/workbook.xml'))
        rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sheet in book.find('x:sheets', NS):
            name = sheet.get('name')
            if name not in requested:
                continue
            target = rels[sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
            part = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            root = ET.fromstring(z.read(part))
            for cell in root.iter('{%s}c' % NS['x']):
                addr = cell.get('r')
                if addr in requested[name]:
                    out[name, addr] = (cell.get('t'), cell.findtext('x:v', namespaces=NS),
                                       ''.join(cell.find('x:is', NS).itertext()) if cell.find('x:is', NS) is not None else None)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source-main', default='ab1da697ad2093ca8185d29932e3fc5b85e7f80b')
    ap.add_argument('--publication-commit')
    ap.add_argument('--workbook-remote-verified', action='store_true')
    ap.add_argument('--workbook-upload-blocked', action='store_true')
    args = ap.parse_args()
    now = datetime.now(ZoneInfo('Asia/Taipei')).isoformat()
    e = read(BASE / 'evidence.json')
    m = read(BASE / 'source_manifest.json')
    qa = read(EH / 'qa.json')
    summary = qa['summary']
    wqa = read(ROOT / 'outputs/consolidated/review/main_v3/verification.json')
    assert wqa['status'] == 'PASS' and wqa['all_original_worksheet_cells_preserved']
    assert fingerprint(WORKBOOK)['sha256'] == wqa['output_sha256']
    assert qa['validation']['all_summary_comparisons_match']
    for f in read(EH / 'manifest.json')['files']:
        assert fingerprint(ROOT / f['path'])['sha256'] == f['sha256'], f['path']

    req = ROOT / 'docs/research/main_research_requirements.csv'
    rows = list(csv.DictReader(req.open()))
    old = list(csv.DictReader((BASE / 'history/MR-20261114-v2/docs/research/main_research_requirements.csv').open()))
    assert len(rows) == 27 == len({r['requirement_id'] for r in rows})
    assert [r['requirement_id'] for r in rows] == [r['requirement_id'] for r in old]
    for a, b in zip(rows, old):
        for key in ['requirement_zh', 'requirement_en', 'priority']:
            assert a[key] == b[key]
        assert a['threshold_value'] == '' and a['threshold_status'] == 'not_defined'
        assert a['version'] == VERSION
        if a['requirement_id'] == 'MAIN-02':
            a['current_status'] = 'accepted_workbook_and_two_page_summary'
    with req.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

    requested = collections.defaultdict(set)
    for c in e['checks']:
        requested[c['sheet']].add(c['cell'])
    av, nv = cell_values(ARCHIVE, requested), cell_values(WORKBOOK, requested)
    assert len(av) == 44 and av == nv
    validation = {'version': VERSION, 'status': 'PASS', 'requirement_ids': 27,
                  'duplicate_ids': 0, 'v1_v2_requirement_history_preserved': True,
                  'undefined_thresholds_empty': True, 'retained_key_cells_rechecked': 44,
                  'original_worksheet_parts_preserved': 24, 'workbook_sheet_count': 32,
                  'EH_records': summary['records'], 'EH_valid_3cm': summary['records_with_3cm'],
                  'EH_summer_paired': summary['summer_paired_n'],
                  'EH_summer_mean_difference_C': summary['summer_soil3_minus_ice49_mean_C'],
                  'source_row_spot_checks_with_page_trace': [1, 73, 2232, 2646, 2647, 4500, 8922],
                  'two_figures_visually_checked': True, 'English_summary_pages': 2,
                  'science_limits_retained': True, 'workbook_QA_path': 'outputs/consolidated/review/main_v3/verification.json',
                  'reader_QA_path': 'outputs/consolidated/review/main_v3/reader_qa.json',
                  'validation_scope': 'Final artifacts and inherited references; no reranking, new measurements or new literature searches.'}
    write(BASE / 'final_validation.json', validation)

    e['version'] = VERSION; e['checked_taipei'] = now; e['status'] = 'PASS_FIXED_SCOPE_FINAL_ARTIFACTS'
    e['archive_workbook_sha256'] = fingerprint(ARCHIVE)['sha256']
    e['workbook_sha256'] = fingerprint(WORKBOOK)['sha256']
    e['verification_provenance'] = 'MR-v1 source comparisons inherited; 44 retained workbook cells rechecked against original snapshot; no raw Mars raster rerun.'
    e['receipt_main'] = args.source_main
    e['inherited_source_main_MRv2'] = e.get('inherited_source_main_MRv2', e.get('source_main'))
    e['source_main'] = args.source_main
    e['mainline_EH_reproduction'] = {'status': 'accepted', 'original_observations': 'McKay et al. published supplement',
                                   'original_parser_QA': 'Team2', 'export_and_artifact_checks': 'mainline',
                                   'GPU_acceleration_claimed': False, 'qa_path': 'outputs/research/elephant_head_final/qa.json',
                                   'summary': summary, 'engine': qa['extraction']}
    e['completion_classes']['B'] = {'status': 'accepted_CSV_dictionary_QA_two_figures',
                                   'original_QA_owner': 'Team2', 'current_export_owner': 'mainline', 'pending_required_artifacts': []}
    e['completion_classes']['C']['status'] = 'received_review_closed_with_known_limits'
    e['completion_classes']['C']['pending'] = []
    e['completion_classes']['C']['unresolved_limits_no_new_tasks'] = ['1998 full text and25/45 citation cause',
                                                                  'unassigned alternative EZ boundaries', 'new site/use/distinct scientific difference not established']
    pair = next(p for p in e['earth_pairings'] if p['earth_candidate_id'] == 'EARTH-002')
    pair.update(pair_status='archival_delivery_accepted_physical_equivalence_unvalidated', mainline_CSV_delivered=True,
                mainline_QA_delivered=True, two_descriptive_figures_delivered=True)
    e['backup_decision'] = 'Linnaeus Terrace not activated; unresolved limits archived. No additional work requested this round.'
    e['final_validation_path'] = 'outputs/consolidated/research_main_20261114/final_validation.json'
    write(BASE / 'evidence.json', e)

    m['version'] = VERSION; m['checked_taipei'] = now
    m.setdefault('MRv2_remote_main_at_start', m.get('remote_main_at_start'))
    m.setdefault('MRv2_remote_source_main', m.get('remote_source_main'))
    m.setdefault('MRv2_remote_source_tree', m.get('remote_source_tree'))
    m['remote_main_at_start'] = '501d6454624108cf7b7e7f8ad572540bc7f774eb'
    m['remote_source_main'] = args.source_main
    m['remote_source_tree'] = None
    m['remote_source_tree_note'] = 'Source references are pinned by commit and per-file Git blob; no stale earlier tree SHA is used.'
    m['current_receipt_main'] = args.source_main
    m['raw_access_boundary'] = 'Mainline re-read only the same-hash EH supplement using the existing Team2 method. Mars native-grid results inherited. Team2 subsequent closeout received; no new source search.'
    m['history']['MR-20261114-v2'] = {'published_commit': '501d6454624108cf7b7e7f8ad572540bc7f774eb',
                                   'local_archive': 'outputs/consolidated/research_main_20261114/history/MR-20261114-v2/'}
    for f in m['source_files']:
        src = f['source_path']
        if src == str(WORKBOOK.relative_to(ROOT)):
            f.update(source_path=str(ARCHIVE.relative_to(ROOT)), original_path=src, read_path=str(ARCHIVE.relative_to(ROOT)),
                     role='archival_workbook_local_backup', remote_ref=None, publication_scope='local_backup_only; original cells retained in final workbook')
        elif src in ['outputs/research/ice_candidate_followup/native_audit.json', 'docs/research/ice_candidate_followup/README.md']:
            f['read_path'] = str((BASE / 'sources/final_local_science' / src).relative_to(ROOT))
            f['publication_snapshot_path'] = f['read_path']
        elif src in ['docs/research/team2_novelty_audit.md', 'outputs/research/team2_novelty_audit.csv']:
            path = BASE / 'sources/final_ab1da697' / src
            f.update(read_path=str(path.relative_to(ROOT)), remote_ref=args.source_main,
                     url='https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/' + args.source_main + '/' + src,
                     **fingerprint(path))
        assert fingerprint(ROOT / f['read_path'])['sha256'] == f['sha256'], f['source_path']
    m['source_version_discrepancies'] = ['Team2 final closeout received atab1da697; novelty remains uncleared and no further searches assigned.',
                                      'EH reproduction uses frozen14be2d5b QA/parser inputs; later closeout is received separately.',
                                      'Workbook source_mapping records bundle-capture hashes; artifact manifest records final hashes.']
    m['original_EH_QA_inputs'] = [str((BASE / 'sources/v2_14be2d5b' / p).relative_to(ROOT)) for p in
                               ['docs/research/team2_novelty_audit.md', 'outputs/research/team2_novelty_audit.csv']]
    m['excel_refresh'] = {'updated_this_round': True, **fingerprint(WORKBOOK), 'local_backup': str(ARCHIVE.relative_to(ROOT)),
                          'original_sheet_parts_retained': 24, 'new_sheets': 8, 'MEDA_records_retained': 159418,
                          'known_styles_child_order_fixed': 4, 'large_grids_included': False,
                          'QA_path': 'outputs/consolidated/review/main_v3/verification.json'}
    m['final_artifact_manifest'] = 'outputs/consolidated/research_main_20261114/final_artifact_manifest.json'
    m['final_stop_rule'] = 'Fixed-scope acceptance complete; no further sites, experiments, literature search or teammate tasks.'
    write(BASE / 'source_manifest.json', m)

    artifacts = [ROOT / p for p in ['docs/research/main_mars_research_cards.md', 'docs/research/main_project_synthesis.md',
                 'docs/research/main_research_requirements.csv', 'docs/research/final_research_summary_en.md',
                 'outputs/research/final_research_summary_en.pdf', 'scripts/research/export_elephant_head_final.py',
                 'scripts/research/finalize_delivery_record.py', 'scripts/reporting/update_main_workbook.py',
                 'scripts/reporting/build_main_update.mjs', 'scripts/reporting/build_final_research_summary.py']]
    artifacts += list(EH.iterdir()) + [WORKBOOK, BASE / 'final_validation.json']
    artifacts += [ROOT / 'outputs/consolidated/review/main_v3' / p for p in
                  ['verification.json', 'reader_qa.json', 'merge_manifest.json', 'source_mapping.json', 'before_inventory.json']]
    artifacts += [ROOT / 'outputs/consolidated/previews/main_v3' / p for p in ['Overview.png', 'EH Summary.png']]
    artifacts += [ROOT / f['read_path'] for f in m['source_files'] if f['read_path'].startswith(str(BASE.relative_to(ROOT)) + '/sources/')]
    artifacts += [ROOT / p for p in m['original_EH_QA_inputs']]
    artifacts = sorted(set(artifacts))
    records = [{'path': str(p.relative_to(ROOT)), **fingerprint(p)} for p in artifacts]
    if args.workbook_upload_blocked:
        next(r for r in records if r['path'] == str(WORKBOOK.relative_to(ROOT)))['remote_publication'] = 'not_uploaded_connector_request_limit; accepted_local_artifact'
    write(BASE / 'final_artifact_manifest.json', {'version': VERSION, 'files': records,
          'exclusions': ['local archival backup; inherited sheets preserved in new workbook', 'temporary support and rendering files',
                         'mutable evidence/source/delivery metadata have no self-hash'], 'no_large_raw_grids': True})
    d = {'version': VERSION, 'updated_taipei': now, 'scope': 'fixed_archival_QA_descriptive_reproduction_and_evidence_requirements',
         'main_case': 'I-02/EARTH-002', 'content_acceptance': 'complete', 'required_artifact_gaps': [],
         'original_novelty_goal_completed': False, 'science_groups_physically_validated': False,
         'previous_MRv2_PR3_merged': True, 'previous_MRv2_merge_commit': 'b35a01ded4d03132cea8ef141e0864dcf4ca39cc',
         'previous_MRv2_receipt_commit': '501d6454624108cf7b7e7f8ad572540bc7f774eb',
         'source_main': args.source_main, 'research_branch': 'codex/mars-research-mainline-20261114',
         'local_main_synced': False, 'other_local_work_preserved': True,
         'excel_updated': True, 'excel_sha256': fingerprint(WORKBOOK)['sha256'],
         'excel_local_backup': str(ARCHIVE.relative_to(ROOT)), 'requirements_count': 27,
         'EH': {'records': summary['records'], 'valid_3cm': summary['records_with_3cm'], 'summer_paired': summary['summer_paired_n'],
                'CSV_dictionary_QA_two_figures_accepted': True, 'original_QA_owner': 'Team2', 'export_reproduction_owner': 'mainline'},
         'English_summary_pages': 2, 'scientific_limits_retained': True, 'future_experiments_executed': False,
         'known_limits_closed_no_further_tasks': True,
         'publication_commit': args.publication_commit, 'workbook_remote_verified': args.workbook_remote_verified,
         'integrated_into_main': bool(args.publication_commit and args.workbook_remote_verified),
         'research_documents_integrated_into_main': bool(args.publication_commit),
         'remote_artifact_gaps': [str(WORKBOOK.relative_to(ROOT))] if args.workbook_upload_blocked else [],
         'remote_upload_blocker': 'GitHub connector rejects request bodies above16MiB;23,035,176-byte workbook requires larger base64 body. CLI path unavailable; browser upload not completed.' if args.workbook_upload_blocked else None,
         'remote_delivery_status': 'verified_complete' if args.publication_commit and args.workbook_remote_verified else ('limited_workbook_upload_blocked' if args.workbook_upload_blocked else 'publication_in_progress'),
         'task_delivery_label': '本輪完整交付完成' if args.publication_commit and args.workbook_remote_verified else ('本輪限制版交付完成' if args.workbook_upload_blocked else '本機完整驗收完成；遠端發布尚待驗證'),
         'artifact_manifest': str((BASE / 'final_artifact_manifest.json').relative_to(ROOT)),
         'validation': validation, 'stop_after_necessary_acceptance_repairs': True}
    write(BASE / 'delivery_status.json', d)
    print(json.dumps({'version': VERSION, 'artifacts': len(records), 'workbook_sha256': d['excel_sha256'],
                      'local_acceptance': 'PASS', 'remote_delivery': d['remote_delivery_status']}))


if __name__ == '__main__':
    main()
