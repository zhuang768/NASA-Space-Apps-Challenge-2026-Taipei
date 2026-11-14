// Node>=20; run with a writable cache directory. No credentials required.
// Reacquire only accepted inputs, using exact successful HTTP ranges.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const dest=process.argv[2];if(!dest)throw Error('Usage: node fetch_inputs.mjs CACHE_DIR');
await fs.mkdir(dest,{recursive:true});
const scenes=JSON.parse(await fs.readFile(path.join(here,'sources/themis_receipts.json'),'utf8')).filter(x=>x.status===200);
const windows=JSON.parse(await fs.readFile(path.join(here,'sources/window_receipts.json'),'utf8')).filter(x=>x.status===206);
const receipts=[];
for(const x of [...scenes,...windows]){
 const url=x.url;const filename=x.id.endsWith('.bin')?x.id:x.id+'.IMG';
 try{
  const range=x.start===undefined?null:`bytes=${x.start}-${x.end}`;
  const response=await fetch(url,{headers:range?{Range:range}:{},signal:AbortSignal.timeout(30000)});
  if(response.status!==x.status)throw Error('Status '+response.status+' expected '+x.status);
  const data=Buffer.from(await response.arrayBuffer());
  if(data.length!==x.bytes)throw Error('Byte count changed');
  if(range&&response.headers.get('content-range')!==x.content_range)throw Error('Content-Range changed');
  await fs.writeFile(path.join(dest,filename),data);
  receipts.push({url,filename,status:response.status,bytes:data.length,retrieved_utc:new Date().toISOString()});
 }catch(e){receipts.push({url,filename,error:String(e)});}
}
await fs.writeFile(path.join(dest,'rerun_receipts.json'),JSON.stringify(receipts,null,2)+'\n');
if(receipts.some(x=>x.error))process.exitCode=1;
