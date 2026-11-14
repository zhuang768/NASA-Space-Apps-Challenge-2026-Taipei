"""Reacquire fixed public inputs with byte and checksum validation (stdlib only).

If Zenodo returns 403, use the record's ordinary browser download controls and
place the named files in --raw-dir, then rerun this check. No credential required.
"""
from pathlib import Path
import argparse,hashlib,json,os,tempfile,urllib.request

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-dir',type=Path,required=True)
    args=parser.parse_args();args.raw_dir.mkdir(parents=True,exist_ok=True)
    entries=json.loads((HERE/'source_manifest.json').read_text())['assets']
    for entry in entries:
        target=args.raw_dir/entry['filename']
        if target.exists():
            data=target.read_bytes()
            if hashlib.md5(data).hexdigest()!=entry['expected_md5']:raise SystemExit('Refusing different existing file: '+str(target))
            print('Already verified: '+target.name);continue
        try:
            request=urllib.request.Request(entry['url'],headers={'User-Agent':'Team-zasa-research-data-verification/1.0'})
            with urllib.request.urlopen(request,timeout=30) as response:data=response.read()
        except Exception as error:
            raise SystemExit(f'Could not download {entry["filename"]}: {error}. Use https://zenodo.org/records/10553882 and preserve the exact original file.') from error
        if len(data)!=entry['bytes'] or hashlib.md5(data).hexdigest()!=entry['expected_md5'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
            raise SystemExit('Downloaded response does not match the published input: '+entry['filename'])
        with tempfile.NamedTemporaryFile(dir=args.raw_dir,delete=False) as f:
            f.write(data);tmp=Path(f.name)
        os.replace(tmp,target);print('Downloaded and verified: '+target.name)

if __name__=='__main__':main()
