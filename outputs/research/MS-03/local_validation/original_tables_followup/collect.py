"""Retrieve public source bytes only; never treat an error page as a data table.

Usage: python3 collect.py requests.json
The request list records why each public endpoint was followed. No credentials,
CAPTCHA handling, or private author communications are used.
"""
import concurrent.futures
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request
import urllib.parse

HERE = Path(__file__).resolve().parent

def retrieve(item):
    record = dict(item)
    record['retrieved_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    request = urllib.request.Request(item['url'], headers={'User-Agent': 'Team-zasa-public-research/1.0', **item.get('headers', {})})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read(20_000_001)
            record.update(http_status=response.status, final_url=response.url,
                          content_type=response.headers.get('Content-Type', ''))
            if len(data) > 20_000_000:
                record['status'] = 'too_large_not_retained'
                return record
    except urllib.error.HTTPError as error:
        data = error.read(100_000)
        record.update(http_status=error.code, final_url=error.url,
                      content_type=error.headers.get('Content-Type', ''),
                      error=str(error), error_body_retention_limit_bytes=100_000,
                      response_body_may_be_truncated=(len(data) == 100_000))
    except Exception as error:
        record.update(status='transport_error', error=str(error))
        return record
    record.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    final = urllib.parse.urlsplit(record.get('final_url', ''))
    if final.hostname == 'accounts.google.com':
        record['final_url'] = urllib.parse.urlunsplit((final.scheme, final.netloc, final.path, '', ''))
        record['final_url_query_omitted'] = 'Unnecessary sign-in-flow query identifiers omitted from research log; requested public URL retained.'
    path = HERE / 'responses' / item['output']
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    record['file'] = str(path.relative_to(HERE))
    record['status'] = 'response_retained_not_yet_content_validated'
    return record

if __name__ == '__main__':
    requests_path = Path(sys.argv[1])
    requests = json.loads(requests_path.read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(retrieve, requests))
    destination = HERE / (requests_path.stem + '_retrievals.json')
    destination.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    for row in results:
        print(row['id'], row.get('http_status', row['status']), row.get('bytes', ''), row.get('content_type', ''))
