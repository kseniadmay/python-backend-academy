import urllib.request
import json
import re

for tid in [4990, 8301, 4716, 3547]:
    url = f"https://forum.remnote.io/t/{tid}.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            title = data.get('title')
            posts = data.get('post_stream', {}).get('posts', [])
            print(f"=== Topic {tid}: {title} ===")
            for p in posts[:3]:
                raw = p.get('cooked', '')
                clean = re.sub(r'<[^>]+>', ' ', raw)
                clean = re.sub(r'\s+', ' ', clean).strip()
                user = p.get('username')
                print(f"Post by {user}:\n{clean[:500]}\n")
    except Exception as e:
        print(f"Error {tid}:", e)
