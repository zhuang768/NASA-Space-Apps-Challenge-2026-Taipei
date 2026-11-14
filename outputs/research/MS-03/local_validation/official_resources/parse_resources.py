"""Read resourcesTabContent from acquired Next flight strings; no site scripts executed."""
from pathlib import Path
from html.parser import HTMLParser
import re,json,csv,urllib.parse
O=Path(__file__).resolve().parent;raw=(O/'sources/challenge_resources.html').read_text();chunks=[]
for m in re.finditer(r'self\.__next_f\.push\((\[.*?\])\)</script>',raw,re.S):
 a=json.loads(m[1]);chunks.extend([a[1]] if len(a)>1 and isinstance(a[1],str) else [])
s=''.join(chunks);ref=re.search(r'"resourcesTabContent":"\$([^" ]+)"',s)[1];m=re.search(re.escape(ref)+r':T([0-9a-fA-F]+),',s);n=int(m[1],16);fragment=s[m.end():].encode()[:n].decode();assert fragment.endswith('</p>') and 'NASA Planetary Data System' in fragment
class A(HTMLParser):
 def __init__(self):super().__init__();self.rows=[];self.url=None;self.parts=[]
 def handle_starttag(self,t,a):
  if t=='a':self.url=dict(a).get('href');self.parts=[]
 def handle_data(self,d):
  if self.url:self.parts.append(d)
 def handle_endtag(self,t):
  if t=='a' and self.url:
   u=urllib.parse.urlsplit(self.url);q=urllib.parse.parse_qsl(u.query,keep_blank_values=True);canonical=urllib.parse.urlunsplit((u.scheme,u.netloc,u.path,urllib.parse.urlencode([(k,v) for k,v in q if not k.startswith('utm_')]),u.fragment));self.rows.append(dict(resource_name=''.join(self.parts),exact_listed_url=self.url,canonical_without_tracking=canonical,source='https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/?tab=resources',source_locator='resourcesTabContent -> $'+ref+' flight text; anchor href',retrieved_date_taipei='2026-11-15'));self.url=None
p=A();p.feed(fragment)
with (O/'resources_links.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=p.rows[0].keys());w.writeheader();w.writerows(p.rows)
(O/'resource_chain.json').write_text(json.dumps(dict(starting_sha='44c2e03b8617c7bb536ad712b85f4716dd190d7c',official_resources_verified=True,read_method='urllib HTTP200 HTML; decoded Next flight text length, no scripts executed; web reader initially failed',flight_reference=ref,fragment_utf8_bytes=n,resource_names=[x['resource_name'] for x in p.rows],selected_gateway='NASA Planetary Data System (PDS)',chain=['official challenge resourcesTabContent','https://pds.nasa.gov/','PDS Geosciences Node','https://pds-geosciences.wustl.edu/missions/mro/crism.htm','official CRISM derived products and ODE lookup'],limits='Official list supplies PDS gateway; it does not specifically name the local products, certify this analysis or supply pixel quality for MS-03.'),indent=2)+'\n');print('Verified',len(p.rows),'actual resource links')
