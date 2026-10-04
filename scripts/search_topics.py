import urllib.request
import json

queries = ['numbered list', 'flashcard import', 'quote import', 'markdown flashcard']

for q in queries:
    url = f"https://forum.remnote.io/search.json?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            topics = data.get('topics', [])
            print(f"=== Query: {q} (found {len(topics)}) ===")
            for t in topics[:5]:
                print(f"  - {t.get('title')} (ID: {t.get('id')})")
    except Exception as e:
        print("Error:", e)
