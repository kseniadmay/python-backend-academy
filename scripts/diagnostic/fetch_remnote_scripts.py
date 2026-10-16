import urllib.request, re

req = urllib.request.Request('https://www.remnote.com', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8')
        scripts = re.findall(r'src="([^"]+\.js)"', html)
        print('Found scripts on remnote.com:', len(scripts))
        for s in scripts:
            print(' ', s)
except Exception as e:
    print(e)
