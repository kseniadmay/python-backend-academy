import urllib.request
import urllib.parse
import re

url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote('site:help.remnote.com markdown import')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'href="(https://help\.remnote\.com[^"]+)"', html)
        seen = set()
        for m in matches:
            if m not in seen:
                seen.add(m)
                print(m)
except Exception as e:
    print('Error:', e)
