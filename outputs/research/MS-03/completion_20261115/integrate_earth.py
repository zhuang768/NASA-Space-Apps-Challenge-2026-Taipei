#!/usr/bin/env python3
"""Idempotently append the MS-03 Earth supplement without changing prior values.

Usage: python3 /tmp/ms03-integrate-earth.py /path/to/repository
The three *_append.csv inputs must be in outputs/research/MS-03/completion_20261115/.
All inputs and collisions are checked before the four tables/sources are written.
"""
import csv
import io
import json
from pathlib import Path
import sys

SOURCE_METADATA = {
    "CEW1": {
        "url": "https://doi.org/10.5281/zenodo.10553882",
        "locator": "Fixed version10553882; UniversityV_09_10_Campbell_data_good_only_calibrated.txt; second-row headers and third-row units; earth_input_receipt.json",
        "read_scope": "Provider fixed-version listing and MD5 re-read; existing original short-export bytes independently SHA256/MD5 checked; all17705 rows parsed;16032 rows selected for11 complete months; no new download, untouched logger or clock-alignment claim",
        "access_date_taipei": "2026-11-15",
        "related_existing_source_id": "U4",
        "dataset_doi": "10.5281/zenodo.10553882",
        "source_file_sha256": "c46d93e3dd07c6c91d700a814214716f00caa0d5cc3a520f8969ce0af63ecafd",
        "source_file_md5": "ae2133eac5c92c695c5f6ef93bcbbd25",
    },
    "CEW2": {
        "url": "https://doi.org/10.1017/S0954102022000025",
        "locator": "Meteorological measurements paragraphs on heights/instruments; Energy balance pressure paragraph after Eq6",
        "read_scope": "Publisher HTML named Methods paragraphs and constant-pressure assumption re-read; no full-paper review or independent sensor calibration claimed;05103/05013 spelling difference retained",
        "access_date_taipei": "2026-11-15",
        "related_existing_source_id": "U1",
    },
    "CEW3": {
        "url": "https://doi.org/10.1017/S0954102025100448",
        "locator": "Environmental data: W coordinates/data-source; Discussion / Extrapolating up and down University Valley: surface boundary, approximations and one-year representativity; TableII caption",
        "read_scope": "Named primary publisher HTML sections and publication metadata read; USGS70273131 used to crosscheck publication year; direct same-W same-process precedent classified; no independent model reproduction, full-paper review or new clock evidence",
        "access_date_taipei": "2026-11-15",
        "related_existing_source_id": "U5",
        "authors": ["Christopher P. McKay", "Margarita M. Marinova", "Kaj E. Williams", "Michael T. Mellon"],
        "title": "Summer snow determines the depth to ice-cemented ground under dry permafrost in Antarctica",
        "year": 2026,
        "online_publication_date": "2025-11-27",
        "journal": "Antarctic Science",
        "volume": 38,
        "issue": 2,
        "pages": "122–134",
        "doi": "10.1017/S0954102025100448",
    },
    "CEA2": {
        "url": "https://doi.org/10.1002/ppp.1985",
        "locator": "Sections2,3.1 Instrumentation,3.2 Thermal parameters,4.1 Snow/thermal/hydrological regimes",
        "read_scope": "Named publisher HTML sections re-read; hourly records,0.02m surface-temperature definition and snow-camera limitations; exact TR1-TR3 to AD1GIS correspondence unproved; no raw sensor supplement acquired",
        "access_date_taipei": "2026-11-15",
        "related_existing_source_id": "A2",
    },
}

CANDIDATE_UPDATES = {
    "MS-03-E01": {
        "disposition": "retain_known_interface_and_data_quality_method_reference",
        "data_status": "2026-11-15: W author-processed long Campbell/HOBO exports acquired and checked; short09_10 Campbell rehashed against providerMD5;16032 rows for2010Jan-Nov summarized without clock conversion or joining; unprocessed logger/calibration/clock-operation records remain unavailable. MS03 original MOC imagery, local CRISM excerpts/MRDR and same-track USRDR/clutter evidence acquired; local ice, depth/content and morphology remain unconfirmed; not a successful quantified Earth-Mars pair.",
        "next_step": "Use W as a historical interface and data-quality reference; retain separate file clocks and unresolved author intervention flags. Obtain independent logger clock/calibration records before any cross-instrument join or thermal inversion. Require scientifically qualified local material/ice evidence before an MS03 interpretation; acquired imagery/spectra/radar are not independent ice truth.",
    },
    "MS-03-E02": {
        "data_status": "2026-11-15: published AD1 GIS185 polygons and geometry reproduction retained. MS03 original MOC imagery and inspected windows, local CRISM excerpts/MRDR, and same-track USRDR plus clutter-simulation bytes acquired; no reliable closed Mars polygon sample or independent local ice truth established. AD1 remains general-method reference only; morphology, ice depth/content and spectral/radar scientific interpretation unresolved. TR1-TR3 thermal/snow monitoring not geometrically registered to AD1; no exact AD1 temperature or dust value invented.",
    },
}

def read_csv(path):
    with path.open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        fields=reader.fieldnames
        rows=list(reader)
    if not fields or len(fields)!=len(set(fields)):
        raise ValueError(f"Invalid headers: {path}")
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError(f"Malformed row: {path}")
    return fields,rows

def csv_text(fields,rows):
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=fields)
    writer.writeheader();writer.writerows(rows)
    return stream.getvalue()

def main():
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python3 ms03-integrate-earth.py REPOSITORY_ROOT")
    root=Path(sys.argv[1]).resolve()
    target=root/'outputs/research/MS-03'
    package=target/'completion_20261115'
    sources_path=target/'sources.json'
    sources=json.loads(sources_path.read_text(encoding='utf-8'))
    if not isinstance(sources,dict) or not all(isinstance(v,dict) for v in sources.values()):
        raise ValueError('sources.json must retain its source-ID dictionary structure')
    original_sources=json.loads(json.dumps(sources))
    for sid,metadata in SOURCE_METADATA.items():
        if sid in sources and sources[sid]!=metadata:
            raise ValueError(f'Source ID collision differs from this supplement: {sid}')
        sources.setdefault(sid,metadata)
    writes={}
    counts={}
    for base,append,idfield in [
        ('evidence.csv','earth_evidence_append.csv','evidence_id'),
        ('prior_work.csv','earth_prior_append.csv','prior_id'),
        ('search_log.csv','earth_search_append.csv','search_id')]:
        path=target/base
        fields,old=read_csv(path)
        newfields,new=read_csv(package/append)
        if fields!=newfields:
            raise ValueError(f'Append header/order mismatch: {append}')
        original_old=[dict(r) for r in old]
        existing={row[idfield]:row for row in old}
        if len(existing)!=len(old):
            raise ValueError(f'Duplicate existing IDs: {base}')
        seen=set()
        added=0
        for row in new:
            rid=row[idfield]
            if not rid or rid in seen:
                raise ValueError(f'Empty or duplicate append ID: {append}: {rid}')
            seen.add(rid)
            if 'source_id' in row:
                sid=row['source_id']
                if sid not in sources or sources[sid]['url']!=row['source_url']:
                    raise ValueError(f'Append source URL mismatch: {rid}: {sid}')
            if 'source_ids' in row:
                for sid in filter(None,row['source_ids'].split(';')):
                    if sid not in sources:
                        raise ValueError(f'Unknown search source ID: {rid}: {sid}')
            if rid in existing:
                if existing[rid]!=row:
                    raise ValueError(f'Existing row ID has different values; not overwritten: {rid}')
            else:
                old.append(row);existing[rid]=row;added+=1
        assert old[:len(original_old)]==original_old
        writes[path]=csv_text(fields,old)
        counts[base]=dict(original=len(original_old),appended=added,final=len(old))
    path=target/'candidates.csv'
    fields,candidates=read_csv(path)
    original_candidates=[dict(r) for r in candidates]
    byid={r['candidate_id']:r for r in candidates}
    if len(byid)!=len(candidates) or not set(CANDIDATE_UPDATES).issubset(byid):
        raise ValueError('Expected unique E01 and E02 candidates')
    for cid,updates in CANDIDATE_UPDATES.items():
        for key,value in updates.items():
            if key not in fields:raise ValueError(f'Missing candidate column {key}')
            byid[cid][key]=value
    for before,after in zip(original_candidates,candidates):
        allowed=set(CANDIDATE_UPDATES.get(before['candidate_id'],{}))
        assert all(before[key]==after[key] for key in fields if key not in allowed)
    assert all(sources[sid]==metadata for sid,metadata in original_sources.items())
    writes[path]=csv_text(fields,candidates)
    writes[sources_path]=json.dumps(sources,ensure_ascii=False,indent=2)+'\n'
    # No writes occur until every file, ID, URL and allowed-field check above passes.
    for path,content in writes.items():
        with path.open('w',encoding='utf-8',newline='') as stream:
            stream.write(content)
    print(json.dumps(dict(status='passed',tables=counts,sources_added=[k for k in sources if k not in original_sources],candidate_changes={k:list(v) for k,v in CANDIDATE_UPDATES.items()},preservation='All prior evidence/prior/search row values and existing source entries unchanged; candidate changes restricted to explicitly listed text fields'),ensure_ascii=False))

if __name__=='__main__':main()
