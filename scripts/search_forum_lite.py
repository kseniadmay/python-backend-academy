import urllib.request
import urllib.parse
import re

query = 'site:forum.remnote.io import markdown links'
url = 'https://lite.duckduckgo.com/lite/'
data = urllib.parse.urlencode({'q': query}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        tds = re.findall(r'<td class="result-snippet">(.*?)</td>', html, re.DOTALL)
        links = re.findall(r'<a class="result-link" href="([^"]+)">([^<]+)</a>', html)
        print('Found results:', len(links))
        for (u, t), s in zip(links[:5], tds[:5]):
            print('TITLE:', t.strip())
            print('URL:', u)
            print('SNIPPET:', re.sub(r'<[^>]+>', '', s).strip())
            print('-' * 40)
except Exception as e:
    print('Error:', e)
