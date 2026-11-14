import pathlib,csv,json,collections,datetime
import numpy as np
import openpyxl
P=pathlib.Path(__file__).parent;S=P/'sources';O=P/'derived'
r=list(csv.DictReader(open(S/'gtnp1505/alt_dataset_1505_alt_grid-transect.csv')));g=collections.defaultdict(list)
for x in r:g[x['date']].append(float(x['alt']))
out=[dict(date=d,n=len(v),mean_cm=float(np.mean(v)),median_cm=float(np.median(v)),min_cm=min(v),max_cm=max(v),stdev_cm=float(np.std(v,ddof=1)),site='UNISCALM N3',source='https://data.gtn-p.org/view/alt-ds/1505')for d,v in sorted(g.items())]
with(O/'uniscalm_by_date.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=out[0]);w.writeheader();w.writerows(out)
w=openpyxl.load_workbook(S/'Adventdalen_data.xlsx',data_only=True);o=list(w['Overview'].values);head=list(o[0]);coremeta=[];cores=[]
for i,row in enumerate(o[1:],2):
 if not row[0]:continue
 x={str(k):v.isoformat()if isinstance(v,datetime.datetime)else v for k,v in zip(head,row)if k};x.update(source_sheet='Overview',source_row=i,source_url='https://doi.org/10.5281/zenodo.11187360');coremeta.append(x)
for sheet in w:
 if not sheet.title.startswith('Core_'):continue
 for i,row in enumerate(list(sheet.values)[1:],2):
  if not isinstance(row[1],(int,float))or not isinstance(row[2],(int,float)):continue
  cores.append(dict(core=sheet.title[5:],sample_type=row[0],upper_depth_cm=row[1],lower_depth_cm=row[2],sample_length_cm=row[3],VIC_vol_percent=row[4],EIC_vol_percent=row[5],PIC_vol_percent=row[6],grain_type=row[7],source_sheet=sheet.title,source_row=i,flag_VIC_outside_0_100=isinstance(row[4],(int,float))and not(0<=row[4]<=100),source_url='https://doi.org/10.5281/zenodo.11187360'))
for name,rows in [('adventdalen_2023_core_overview.csv',coremeta),('adventdalen_2023_core_samples.csv',cores)]:
 with(O/name).open('w')as f:wr=csv.DictWriter(f,fieldnames=rows[0]);wr.writeheader();wr.writerows(rows)
print('UNISCALM:',len(r),'records',len(g),'dates, annual means',min(x['mean_cm']for x in out),max(x['mean_cm']for x in out));print('new cores',len(coremeta),'segments',len(cores),'VIC out of range',sum(x['flag_VIC_outside_0_100']for x in cores));print('metadata cols',head)
