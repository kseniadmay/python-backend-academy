import urllib.request
import urllib.parse
import re

queries = [
    'site:help.remnote.com markdown import',
    'site:help.remnote.com importing from obsidian',
    'site:help.remnote.com backlinks references import'
]

for q in queries:
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            links = re.findall(r'<a class="result__url"[^>]*href="([^"]+)"', html)
            snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
            print('QUERY:', q)
            for l, s in zip(links[:3], snippets[:3]):
                print('  URL:', l.strip())
                print('  SNIPPET:', re.sub(r'<[^>]+>', '', s).strip())
    except Exception as e:
        print('Error:', e)
