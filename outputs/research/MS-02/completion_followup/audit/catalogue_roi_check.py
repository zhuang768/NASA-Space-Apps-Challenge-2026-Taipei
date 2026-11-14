"""Bounded MS-02 membership check of the original Daubar2022 Table S1.

Read-only input; standard library only. No source/other-site/old-report write.
The output is a catalogue point query, never an ice-absence conclusion.
Usage: python3 catalogue_roi_check.py --source /path/to/Daubar_2022_catalog_tableS1.xlsx
"""
from pathlib import Path
import argparse
from collections import Counter
import hashlib,json,math,zipfile
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
EXPECTED_MD5='4d1b49c2e62785a1b4efb73b2040de4d'
EXPECTED_SHA256='393ed99a157a7e68a77fc3adf332939ea368a15f2b7ac2589cb701e4f82291f6'
EXPECTED_GIT_BLOB='b7d23e5ddea1592403dc3733aa76764413e918a4'
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def read_rows(path):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None,'XLSX member CRC failure'
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            shared=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)]
        records=[]
        for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('m:sheetData/m:row',NS):
            item={}
            for cell in row.findall('m:c',NS):
                typ=cell.get('t');value=cell.find('m:v',NS)
                text=value.text if value is not None else ''
                if typ=='s':text=shared[int(text)]
                elif typ=='inlineStr':text=''.join(cell.find('m:is',NS).itertext())
                item[''.join(c for c in cell.get('r') if c.isalpha())]=text
            records.append((int(row.get('r')),item))
    return records


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=ROOT/'outputs/research/MS-03/local_validation/gap_completion/sources/Daubar_2022_catalog_tableS1.xlsx')
    args=ap.parse_args();raw=args.source.read_bytes()
    md5=hashlib.md5(raw).hexdigest();sha256=hashlib.sha256(raw).hexdigest()
    gitsha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert md5==EXPECTED_MD5 and sha256==EXPECTED_SHA256 and gitsha==EXPECTED_GIT_BLOB,'Source differs from the provider-matched original'
    records=read_rows(args.source);header=records[0][1]
    assert records[0][0]==1
    assert header['B']=='Latitude (deg E, centric)' and header['C']=='Longitude (deg N)'
    assert header['H']=='Ice-exposing impact'
    data=[];invalid=[]
    for rowno,r in records[1:]:
        try:
            lat=float(r['B']);lon_source=float(r['C'])
            assert math.isfinite(lat) and math.isfinite(lon_source)
            assert -90<=lat<=90 and 0<=lon_source<360
        except (KeyError,ValueError,AssertionError):
            invalid.append(rowno);continue
        # Variable names + centric qualifier are preserved. Parenthetical E/N
        # suffixes conflict; official observation orientation independently checked.
        lon_east=lon_source%360
        member=52.5<=lat<=53.0 and 168.0<=lon_east<=168.5
        data.append({'source_excel_row':rowno,'HiRISE_observation_id':r.get('A',''),
                     'latitude_deg_planetocentric':lat,'longitude_deg_east_0_360':lon_east,
                     'ice_exposing_flag_original':r.get('H',''),'reference_original':r.get('T',''),
                     'inside_fixed_roi':member})
    assert not invalid and len(data)==1203
    first=data[0]
    assert first['HiRISE_observation_id']=='PSP_007561_1290'
    # This loose, explicit orientation check is not an accuracy or same-point claim.
    assert abs(first['latitude_deg_planetocentric']-(-50.602))<0.02
    assert abs(first['longitude_deg_east_0_360']-305.990)<0.02
    hits=[r for r in data if r['inside_fixed_roi']]
    ice_hits=[r for r in hits if r['ice_exposing_flag_original'].strip().lower()=='y']
    possible_hits=[r for r in hits if r['ice_exposing_flag_original'].strip().lower()=='possible']
    result={
      'check_scope':'Daubar2022 original catalogue impact-point membership only',
      'source_doi':'10.5281/zenodo.6604912','paper_doi':'10.1029/2021JE007145',
      'source_url':'https://zenodo.org/records/6604912/files/Daubar_2022_catalog_tableS1.xlsx?download=1',
      'source_repo_path':'outputs/research/MS-03/local_validation/gap_completion/sources/Daubar_2022_catalog_tableS1.xlsx',
      'source_bytes':len(raw),'source_md5':md5,'provider_advertised_md5':EXPECTED_MD5,
      'provider_md5_matched':True,'source_sha256':sha256,'source_git_blob_sha1':gitsha,
      'source_license':'CC-BY-4.0 per author release metadata',
      'original_headers':header,
      'coordinate_handling':{
        'latitude':'Column B, named Latitude and marked centric; retained as planetocentric, no geodetic conversion',
        'longitude':'Column C, named Longitude; east-positive orientation checked against official HiRISE first-row observation, normalized modulo360; no west-positive flip',
        'header_issue':'Original B/C parenthetical E/N suffixes conflict with variable names; original headers retained unedited',
        'orientation_check_source':'https://www.uahirise.org/PSP_007561_1290',
        'orientation_check_read':'Official page latitude(centered)-50.602deg; longitude(East)305.990deg; read2026-11-15',
        'source_first_row_impact_point':[first['latitude_deg_planetocentric'],first['longitude_deg_east_0_360']],
        'check_limit':'An observation centre is not the exact catalogue impact point. Difference used only to reject swapped columns/west-positive orientation, not to assign location accuracy.'},
      'fixed_roi':{'south_deg_N':52.5,'north_deg_N':53.0,'west_deg_E':168.0,'east_deg_E':168.5,'inclusive_bounds':True},
      'worksheet':'Sheet1','source_data_rows':len(data),'source_excel_row_range':[2,1204],
      'invalid_coordinate_rows':invalid,
      'source_latitude_range':[min(r['latitude_deg_planetocentric'] for r in data),max(r['latitude_deg_planetocentric'] for r in data)],
      'source_longitude_east_range':[min(r['longitude_deg_east_0_360'] for r in data),max(r['longitude_deg_east_0_360'] for r in data)],
      'original_ice_flag_counts':dict(sorted(Counter(r['ice_exposing_flag_original'] for r in data).items())),
      'in_cell_catalogue_point_count':len(hits),'in_cell_ice_exposing_y_count':len(ice_hits),
      'in_cell_possible_ice_exposing_count':len(possible_hits),'hits':hits,
      'interpretation':'No impact point from this bounded2022 source falls in fixedMS-02. This neither establishes no ice nor establishes no crater/study or no overlapping HiRISE image.',
      'selection_limit':'Dated new-impact catalogue with before/after and crater-resolving HiRISE constraints; not an exhaustive local exposure/geomorphology inventory and not a replacement for other catalogues.',
      'ice_presence':'unknown','ice_depth_m':None,'ice_fraction':None,
      'independent_local_ice_truth_gap_closed':False,'all_ms02_problems_resolved':False,
      'checks_passed':['original provider MD5 and two additional hashes','XLSX CRC','original headers and ice flag present','1203 finite valid coordinate rows','independent official cardinal orientation cross-check','fixed inclusive ROI point selection; original flags retained']}
    (HERE/'catalogue_roi_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['source_bytes','source_sha256','source_data_rows','in_cell_catalogue_point_count','in_cell_ice_exposing_y_count','in_cell_possible_ice_exposing_count','independent_local_ice_truth_gap_closed']},indent=2))

if __name__=='__main__':main()
