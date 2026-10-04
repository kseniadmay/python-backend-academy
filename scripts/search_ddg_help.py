import urllib.request
import urllib.parse
import json

# Let's search using a public search endpoint
url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote("site:help.remnote.com markdown import")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
try:
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8', errors='ignore')
        import re
        links = re.findall(r'<a class="result__url"[^>]*href="([^"]+)"', html)
        snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
        for l, s in zip(links[:5], snippets[:5]):
            print('URL:', l.strip())
            print('SNIPPET:', re.sub(r'<[^>]+>', '', s).strip())
            print('---')
except Exception as e:
    print('Error:', e)
