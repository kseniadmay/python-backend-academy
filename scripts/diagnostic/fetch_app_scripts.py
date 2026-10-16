import urllib.request
import re

req = urllib.request.Request('https://www.remnote.com/app', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
        print('Found scripts:', len(scripts))
        for s in scripts:
            print(' ', s)
except Exception as e:
    print('Error:', e)
