import urllib.request
import re

url = 'https://help.remnote.com/en/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8')
        articles = re.findall(r'href="(/en/articles/[^"]+)"[^>]*>([^<]+)', html)
        for u, t in articles:
            print(u, t.strip())
except Exception as e:
    print(e)
