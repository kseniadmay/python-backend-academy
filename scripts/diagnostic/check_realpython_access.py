import urllib.request
import re

url = "https://realpython.com/quizzes/queue-in-python/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8')
    print("Page title:", re.findall(r'<title>(.*?)</title>', html))
    print("Locked / Member / Premium mentions:")
    for m in re.findall(r'(member|membership|unlock|sign in|free account|start quiz)', html, re.I):
        print(" -", m)
