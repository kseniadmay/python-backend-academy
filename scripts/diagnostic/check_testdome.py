import urllib.request
import re

url = "https://www.testdome.com/tests/django-online-test"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
# Print title and snippet
title = re.findall(r'<title>(.*?)</title>', html)
print("Title:", title)
# Look for practice or question links
links = [l for l in re.findall(r'href="([^"]+)"', html) if 'django' in l.lower() or 'question' in l.lower()]
print("Matching links count:", len(links))
for l in links[:10]:
    print(" -", l)
