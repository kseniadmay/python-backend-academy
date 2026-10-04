import urllib.request
import json

url = 'https://forum.remnote.io/search.json?q=markdown+import'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        topics = data.get('topics', [])
        print("Total topics found:", len(topics))
        for t in topics[:15]:
            print(f"- {t.get('title')} (posts: {t.get('posts_count')}) ID: {t.get('id')}")
except Exception as e:
    print("Error:", e)
