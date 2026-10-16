import urllib.request
import re

url = "https://realpython.com/quizzes/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8')
        print("Real Python Status:", resp.status)
        quizzes = re.findall(r'<a[^>]+href="(/quizzes/[^"]+)"[^>]*>(.*?)</a>', html)
        print("Quizzes found:", len(quizzes))
        for q in quizzes[:5]:
            print("Quiz:", q)
except Exception as e:
    print("Real Python error:", e)
