import urllib.request
import json
import re

url = 'https://forum.remnote.io/search.json?q=empty+line+spacing+between+rem'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        topics = data.get('topics', [])
        print("Topics for empty line spacing:", len(topics))
        for t in topics[:10]:
            print(f"- {t.get('title')} (ID: {t.get('id')})")
except Exception as e:
    print("Error:", e)
