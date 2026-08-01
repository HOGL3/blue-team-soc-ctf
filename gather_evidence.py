import urllib.request
import urllib.error
import re
from html.parser import HTMLParser

BASE_URL = "http://127.0.0.1:8001"

class StaticParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'link' and 'href' in attrs_dict:
            href = attrs_dict['href']
            # Only track CSS files or explicit stylesheet links
            if attrs_dict.get('rel') == 'stylesheet' or href.endswith('.css'):
                self.assets.append({'url': href, 'type': 'CSS'})
        elif tag == 'script' and 'src' in attrs_dict:
            self.assets.append({'url': attrs_dict['src'], 'type': 'JS'})
        elif tag == 'img' and 'src' in attrs_dict:
            self.assets.append({'url': attrs_dict['src'], 'type': 'Image'})

try:
    req = urllib.request.Request(BASE_URL)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
except Exception as e:
    print(f"Failed to fetch homepage: {e}")
    exit(1)

parser = StaticParser()
parser.feed(html)

print("--- NETWORK REQUEST EVIDENCE ---\n")

for asset in parser.assets:
    url = asset['url']
    if url.startswith('/'):
        full_url = BASE_URL + url
    elif not url.startswith('http'):
        full_url = BASE_URL + '/' + url
    else:
        full_url = url
        
    try:
        req = urllib.request.Request(full_url)
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            headers = dict(response.info())
            print(f"[SUCCESS] {asset['type']} loaded: {url} (Status: {status})")
    except urllib.error.HTTPError as e:
        print(f"--- FAILED REQUEST ---")
        print(f"URL: {full_url}")
        print(f"Status Code: {e.code}")
        print(f"Resource Type: {asset['type']}")
        print(f"Response Headers: {dict(e.headers)}")
        body = e.read().decode('utf-8')[:200]
        print(f"Response Body (truncated):\n{body}\n----------------------")
    except Exception as e:
        print(f"[ERROR] Failed to connect to {full_url}: {e}")

print("\n--- END OF EVIDENCE ---")
