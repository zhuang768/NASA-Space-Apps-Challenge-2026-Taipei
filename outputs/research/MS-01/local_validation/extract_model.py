"""Extract existing Piqueux2019 author-product values;not a new ice retrieval."""
from pathlib import Path
import argparse,csv,hashlib,json
import numpy as np
HERE=Path(__file__).resolve().parent
EXPECTED={'d_m.ascii':'080dd616a822fa74f20f4c923a1d79f1','TI_SI.ascii':'267810eb52f6c053dd2adefe4dc2010a','Lat.ascii':'9b70d4b2f0297594ce7e02494cf8564b','Lon.ascii':'c60b8ff5f8b0bc603c92967862ad7431','Notes.txt':'931c03a665d02755470be11becf7841b'}
URL='https://data.caltech.edu/records/ym7fc-x0r93'
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',type=Path,required=True);a=p.parse_args()
    hashes=[]
    for name,md5 in EXPECTED.items():
        b=(a.inputs/name).read_bytes();assert hashlib.md5(b).hexdigest()==md5,name
        hashes.append(dict(filename=name,bytes=len(b),md5=md5,sha256=hashlib.sha256(b).hexdigest(),url='https://data.caltech.edu/api/records/ym7fc-x0r93/files/'+name+'/content'))
    lat=np.loadtxt(a.inputs/'Lat.ascii').ravel();lon=np.loadtxt(a.inputs/'Lon.ascii').ravel()
    depth=np.loadtxt(a.inputs/'d_m.ascii');ti=np.loadtxt(a.inputs/'TI_SI.ascii')
    assert depth.shape==ti.shape==(len(lat),len(lon))==(360,720)
    assert np.allclose(np.diff(lat),-.5) and np.allclose(np.diff(lon),.5)
    ii=np.flatnonzero((lat>=56.5)&(lat<57));jj=np.flatnonzero((lon>=72.5)&(lon<73));assert len(ii)==len(jj)==1
    i,j=int(ii[0]),int(jj[0]);assert lat[i]==56.75 and lon[j]==72.75
    rows=[]
    for y in range(i-1,i+2):
        for x in range(j-1,j+2):
            valid=bool(np.isfinite(depth[y,x]) and depth[y,x]!=-32768)
            rows.append(dict(row0=y,column0=x,latitude_n=float(lat[y]),longitude_e=float(lon[x]),depth_model_m=float(depth[y,x]) if valid else None,
                 upper_dry_TI=float(ti[y,x]) if np.isfinite(ti[y,x]) and ti[y,x]!=-32768 else None,depth_valid=valid,is_roi_cell=(y==i and x==j),
                 data_kind='Existing author two-layer thermal-model inference;this run indexes/extracts,no new retrieval',source_url=URL,source_doi='10.22002/D1.1316',source_version='1.0;published2019-11-27',
                 period='MCS multi-year seasonal analysis in2019paper;exact input years/counts for this cell not supplied',spatial_support='0.5degree output cell;not in-situ point;native observations/coadds have other support',
                 depth_definition='Model depth to assumed frozenH2O lower layer,not independently detected interface',uncertainty='No cell-specific error/QA or confidence interval supplied;do not attach global best-case estimate as localCI',
                 TI_unit='J m^-2 K^-1 s^-1/2 perpaper;Notes prints J m^2,retained as source metadata issue'))
    with (HERE/'piqueux_model_patch.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    core=next(r for r in rows if r['is_roi_cell'])
    result=dict(dataset_url=URL,dataset_doi='10.22002/D1.1316',paper_doi='10.1029/2019GL083947',files=hashes,shape_rows_columns=list(depth.shape),lat_order='89.75to−89.75 descending',lon_order='.25to359.75 ascending',output_ppd=2,fill=-32768,
                roi_cell=core,cell_bounds=dict(south=56.5,north=57,west=72.5,east=73),
                metadata_limits=['Paperdescribes3ppd;downloadedv1filesandcoordinates2ppd;not silently treated as same raster','720x360 source dimensions interpreted as widthxheight and checked against360rows720columns','NotesTIunitprintspositive m^2;paperphysicalunitnegative exponent;no numericconversion performed'],
                interpretation_limits=['Conditional existing thermalmodel value,not local ice existence/depth/abundance truth','Lowerlayer ice assumption,possible competentrock/boulders/materialalternatives and errorlimits remain','No evidence here of massive vs pore ice or ice fraction','Do not use0.427m coincidence withUV0.42m as validation','Thermal inputs overlap other ice evidence;dependency must be explicit'])
    (HERE/'piqueux_model_extraction.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'row0':i,'column0':j,'depth_model_m':core['depth_model_m'],'dry_TI_model':core['upper_dry_TI'],'valid':core['depth_valid'],'source_hashes':len(hashes)},indent=2))
if __name__=='__main__':main()
