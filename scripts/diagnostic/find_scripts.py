import urllib.request, re

req = urllib.request.Request('https://www.remnote.com', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as r:
    h = r.read().decode('utf-8')
    scripts = re.findall(r'<script.*?</script>', h, re.DOTALL)
    print('Found script blocks:', len(scripts))
    for s in scripts[:5]:
        print('=== SCRIPT ===')
        print(s[:500])
