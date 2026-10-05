import urllib.request, sys
for u in ['https://www.remnote.com/notes']:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            print(u, 'Status:', resp.status)
    except Exception as e:
        print(u, 'Result:', e)
print('[OK] RemNote endpoint check finished')
