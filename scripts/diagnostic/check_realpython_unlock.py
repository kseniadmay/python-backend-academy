import urllib.request
import re

url = "https://realpython.com/quizzes/queue-in-python/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8')
    # find snippet around unlock
    for m in re.finditer(r'unlock', html, re.I):
        start = max(0, m.start() - 150)
        end = min(len(html), m.end() + 150)
        snippet = re.sub('<[^<]+?>', ' ', html[start:end])
        print("Snippet:", " ".join(snippet.split()))
