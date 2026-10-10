import csv, hashlib, os, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

BASE = 'https://wikileaks.org/vault8/'
ROOT = os.path.dirname(os.path.abspath(__file__))
seen_pages, files, rows = set(), set(), []

def get(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=45) as r:
        return r.read()

def links(url, data):
    text = data.decode('utf-8', 'replace')
    return {urljoin(url, x) for x in re.findall(r'href="([^"]+)"', text)
            if not x.startswith(('#','mailto:','javascript:'))}

def crawl(page, bucket):
    if page in seen_pages: return
    seen_pages.add(page)
    try: data = get(page)
    except Exception as e:
        print('PAGE_FAIL', page, e, file=sys.stderr); return
    for u in links(page, data):
        if not u.startswith('https://wikileaks.org/vault8/'): continue
        path = urlparse(u).path
        if path.endswith('/'):
            # The WikiLeaks repository index exposes nested paths from the root page;
            # avoid recursively fetching every directory page.
            continue
        elif '/document/repo_hive/' in path:
            files.add(('Hive-Repository', u))
        elif '/document/hive-log/' in path:
            files.add(('Hive-Development-Logs', u))

crawl(BASE, '')
for start, bucket in [('https://wikileaks.org/vault8/document/repo_hive/', 'Hive-Repository'),
                      ('https://wikileaks.org/vault8/document/hive-log/', 'Hive-Development-Logs')]:
    crawl(start, bucket)

def download_one(item):
    bucket, url = item
    name = os.path.basename(urlparse(url).path)
    destdir = os.path.join(ROOT, bucket); os.makedirs(destdir, exist_ok=True)
    dest = os.path.join(destdir, name)
    try:
        if not os.path.exists(dest) or os.path.getsize(dest) == 0:
            with open(dest, 'wb') as f: f.write(get(url))
        h = hashlib.sha256(); size = 0
        with open(dest, 'rb') as f:
            for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk); size += len(chunk)
        return {'Project':bucket,'File':name,'Bytes':size,'SHA256':h.hexdigest().upper(),'Source':url,'Status':'OK'}
    except Exception as e:
        return {'Project':bucket,'File':name,'Bytes':0,'SHA256':'','Source':url,'Status':str(e)}

with ThreadPoolExecutor(max_workers=16) as pool:
    futures = [pool.submit(download_one, item) for item in sorted(files)]
    for i, future in enumerate(as_completed(futures), 1):
        rows.append(future.result())
        if i % 100 == 0: print('Downloaded', i, 'of', len(futures), flush=True)

with open(os.path.join(ROOT,'manifest.csv'),'w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['Project','File','Bytes','SHA256','Source','Status']); w.writeheader(); w.writerows(rows)
print('Pages=%d Files=%d OK=%d Failed=%d' % (len(seen_pages),len(rows),sum(r['Status']=='OK' for r in rows),sum(r['Status']!='OK' for r in rows)))
