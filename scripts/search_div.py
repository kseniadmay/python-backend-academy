import urllib.request
import json

queries = ['shift enter', 'divider markdown', 'blank line', 'horizontal rule']

for q in queries:
    url = f"https://forum.remnote.io/search.json?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            topics = data.get('topics', [])
            print(f"=== {q} ({len(topics)}) ===")
            for t in topics[:3]:
                print(f"  - {t.get('title')} (ID: {t.get('id')})")
    except Exception as e:
        print(f"Error {q}:", e)
