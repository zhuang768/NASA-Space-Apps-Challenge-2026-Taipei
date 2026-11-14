"""Preserve exact XML paragraph text and ordinals from MD5-verified source DOCX."""
from pathlib import Path
import argparse,hashlib,json,zipfile,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--raw-dir',type=Path,required=True);a=p.parse_args()
    assets=json.loads((HERE/'source_manifest.json').read_text())['assets'];result={}
    for asset in assets:
        if not asset['filename'].endswith('.docx'):continue
        path=a.raw_dir/asset['filename'];assert hashlib.md5(path.read_bytes()).hexdigest()==asset['expected_md5']
        with zipfile.ZipFile(path) as z:root=ET.fromstring(z.read('word/document.xml'))
        ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        paragraphs=[dict(xml_w_p_ordinal_1based=i,text=''.join(node.itertext())) for i,node in enumerate(root.findall('.//w:p',ns),1)]
        # Preserve only actual Word text runs, including empty paragraph positions.
        for row,node in zip(paragraphs,root.findall('.//w:p',ns)):row['text']=''.join(x.text or '' for x in node.findall('.//w:t',ns))
        result[asset['filename']]=dict(source_url=asset['url'],source_sha256=asset['sha256'],locator_definition='word/document.xml w:p ordinal, not a printed page number',paragraphs=paragraphs)
    (HERE/'deployment_paragraphs.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print({k:len(v['paragraphs']) for k,v in result.items()})
if __name__=='__main__':main()
