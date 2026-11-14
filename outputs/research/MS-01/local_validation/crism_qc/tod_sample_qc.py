"""Bounded CRISM sample QC only. No geolocated water-ice-band analysis.

Reads exactly the downloaded PDS4-labelled array and detector-row table.
python tod_sample_qc.py --input-dir /tmp/ms01_lv_crism --output-dir /tmp/ms01_lv_crism
"""
from pathlib import Path
import argparse,csv,hashlib,json,re,xml.etree.ElementTree as ET
import numpy as np

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input-dir',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--catalogue',type=Path,help='Optional root-acquired fixed ODE catalogue JSON')
    a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
    stem='tod0000b701_02_if204l_trr3';paths={ext:a.input_dir/f'{stem}.{ext}' for ext in ['img','lbl','xml']}
    raw={ext:path.read_bytes() for ext,path in paths.items()}
    label=raw['lbl'].decode();xml=ET.fromstring(raw['xml']);ns={'p':'http://pds.nasa.gov/pds4/pds/v1'}
    array=xml.find('.//p:Array_3D_Image',ns);assert array is not None
    dimensions=[(axis.findtext('p:axis_name',namespaces=ns),int(axis.findtext('p:elements',namespaces=ns)),int(axis.findtext('p:sequence_number',namespaces=ns))) for axis in array.findall('p:Axis_Array',ns)]
    dimensions.sort(key=lambda x:x[2]);assert [x[0] for x in dimensions]==['Line','Band','Sample']
    shape=tuple(x[1] for x in dimensions)
    assert array.findtext('p:axis_index_order',namespaces=ns)=='Last Index Fastest'
    assert array.findtext('p:Element_Array/p:data_type',namespaces=ns)=='IEEE754LSBSingle'
    offset=int(array.findtext('p:offset',namespaces=ns));missing=float(array.findtext('p:Special_Constants/p:missing_constant',namespaces=ns))
    data=np.frombuffer(raw['img'],dtype='<f4',count=int(np.prod(shape)),offset=offset).reshape(shape)
    # Separate XML/PDS3 layout control: LINE_INTERLEAVED + PC_REAL and image bytes.
    for expression in ['LINES\\s*=\\s*12','LINE_SAMPLES\\s*=\\s*64','BANDS\\s*=\\s*438','SAMPLE_TYPE\\s*=\\s*PC_REAL','SAMPLE_BITS\\s*=\\s*32','BAND_STORAGE_TYPE\\s*=\\s*LINE_INTERLEAVED']:
        assert re.search(expression,label),expression
    detector=xml.find('.//p:Table_Binary',ns);detector_offset=int(detector.findtext('p:offset',namespaces=ns));records=int(detector.findtext('p:records',namespaces=ns))
    assert offset==0 and detector_offset==data.nbytes and records==shape[1]
    row_numbers=np.frombuffer(raw['img'],dtype='>u2',count=records,offset=detector_offset)
    assert len(raw['img'])==5260*256
    finite=np.isfinite(data);is_missing=data==missing;remaining=finite&~is_missing
    spectrum_missing=is_missing.sum(axis=1)
    base='https://pds-geosciences.wustl.edu/mro/mro-m-crism-3-rdr-targeted-v1/mrocr_2102/trdr/2008/2008_191/tod0000b701/'
    source=[dict(filename=paths[ext].name,url=base+paths[ext].name,bytes=len(raw[ext]),sha256=hashlib.sha256(raw[ext]).hexdigest()) for ext in ['img','lbl','xml']]
    flags={}
    for key in ['ATMO_CORRECTION_FLAG','THERMAL_CORRECTION_MODE','PHOTOCLIN_CORRECTION_FLAG','SPATIAL_RESAMPLING_FLAG','SPECTRAL_RESAMPLING_FLAG']:
        match=re.search(r'MRO:'+key+r'\s*=\s*"([^\"]+)"',label);flags[key]=match.group(1)
    quality=dict(spectral_array_shape_line_band_sample=list(shape),spectral_array_bytes=data.nbytes,whole_file_bytes=len(raw['img']),detector_table_offset_bytes=detector_offset,detector_table_rows=records,detector_table_bytes=records*2,trailing_padding_bytes=len(raw['img'])-(detector_offset+records*2),spectral_sample_count=int(data.size),spatial_spectrum_count=shape[0]*shape[2],finite_samples=int(finite.sum()),nonfinite_samples=int((~finite).sum()),declared_missing_constant=missing,missing_constant_samples=int(is_missing.sum()),missing_constant_fraction=float(is_missing.mean()),remaining_finite_samples=int(remaining.sum()),negative_remaining_samples=int((remaining&(data<0)).sum()),remaining_over_1_samples=int((remaining&(data>1)).sum()),remaining_over_10_samples=int((remaining&(data>10)).sum()),remaining_min=float(data[remaining].min()),remaining_max=float(data[remaining].max()),remaining_quantiles={str(q):float(np.quantile(data[remaining],q)) for q in [0,.01,.5,.99,1]},spectra_with_any_missing=int((spectrum_missing>0).sum()),spectra_with_all_bands_missing=int((spectrum_missing==shape[1]).sum()),missing_bands_per_spectrum_min=int(spectrum_missing.min()),missing_bands_per_spectrum_max=int(spectrum_missing.max()),detector_row_min=int(row_numbers.min()),detector_row_max=int(row_numbers.max()),detector_rows_unique=int(len(np.unique(row_numbers))),controls='Array layout independently agrees between PDS3 LBL and PDS4 XML;finite does not mean valid:65535 is explicit missing_constant;negative/>1 counts are descriptive flags,not calibrated physical rejection thresholds.')
    output=dict(product_id=stem.upper(),date_taipei='2026-11-15',source_files=source,observation_type='TOD tracking optical depth',period_utc={'start':'2008-07-09T13:28:46.446','stop':'2008-07-09T13:28:49.383'},solar_longitude_deg=96.352471,unit='I_OVER_F;dimensionless radiometrically calibrated spectral data',depth_support='Surface/atmospheric reflected-signal product;no subsurface depth measurement',spatial_resolution_m='unknown in this check;PIXEL_AVERAGING_WIDTH=10 is not metres/pixel',pixel_averaging_width=10,calibration_flags=flags,wavelength_file_required='CDR410803692813_WA0300000L_3.IMG',wavelength_file_acquired=False,per_pixel_DDR_geolocation_acquired=False,quality=quality,interpretation_status={'ROI_water_ice_band_detection':'not evaluated','local_ice_presence':'not determined from this sample','ice_depth':'not measured','ice_abundance':'not measured'},limits=['Catalogue footprint intersection does not identify pixel coordinates or valid spectra within the ROI.','TOD is an optical-depth observation mode,not a validated surface-ice mapping experiment.','Wavelength CDR and per-pixel DDR not obtained;no wavelength-based indices or ROI spectrum assigned.','Atmospheric,thermal andphotoclinometric correction flags areOFF;these are separate from radiometric calibration.','Global cube values include explicit missing and extreme values;do not average the cube as MS01 reflectance or classify ice from those statistics.','No independent atmospheric/surface controls or repeat-scene spectral comparison performed.'])
    if a.catalogue:
        catalogue=json.loads(a.catalogue.read_text())['ODEResults']['Products']['Product']
        product=next(r for r in catalogue if r['pdsid']==stem)
        output['catalogue_metadata']={k:product.get(k) for k in ['Footprint_geometry','Footprint_souce','UTC_start_time','UTC_stop_time','Solar_longitude','Incidence_angle','Emission_angle','Description']}
        output['catalogue_metadata']['scope_note']='Root catalogue has positive ROI polygon overlap;no individual pixel geolocation has been verified.'
        output['catalogue_source']=dict(path=a.catalogue.name,sha256=hashlib.sha256(a.catalogue.read_bytes()).hexdigest())
    (a.output_dir/'sample_qc.json').write_text(json.dumps(output,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    with (a.output_dir/'sample_sources.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,list(source[0]));w.writeheader();w.writerows(source)
    with (a.output_dir/'band_qc.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['band_1based','detector_row_0based','spatial_samples','declared_missing_samples','remaining_finite_samples','negative_remaining_samples','remaining_over_1_samples'])
        for k in range(shape[1]):
            z=data[:,k,:];good=np.isfinite(z)&(z!=missing)
            w.writerow([k+1,int(row_numbers[k]),int(z.size),int((z==missing).sum()),int(good.sum()),int((good&(z<0)).sum()),int((good&(z>1)).sum())])
    print(json.dumps({'status':'QC_COMPLETE_NOT_ICE_DETECTION','quality':quality,'sources':source},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
