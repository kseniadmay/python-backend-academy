import urllib.request
import re

for u in ['https://www.remnote.com/notes', 'https://app.remnote.com']:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as resp:
            print(u, 'Status:', resp.status)
            html = resp.read().decode('utf-8', errors='ignore')
            scripts = re.findall(r'src="([^"]+\.js[^"]*)"', html)
            print('  Scripts:', len(scripts))
            for s in scripts[:5]:
                print('   ', s)
    except Exception as e:
        print(u, 'Error:', e)
