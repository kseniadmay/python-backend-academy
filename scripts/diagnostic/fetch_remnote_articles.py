import urllib.request
import re

articles = [
    "https://help.remnote.com/en/articles/6330674-notes-on-remnote-importers",
    "https://help.remnote.com/en/articles/7898005-importing-notes",
    "https://help.remnote.com/en/articles/9252072-how-to-import-flashcards-from-text",
    "https://help.remnote.com/en/articles/6025481-creating-flashcards",
    "https://help.remnote.com/en/articles/9216774-multi-line-list-set-flashcards"
]

for url in articles:
    print("=" * 60)
    print("FETCHING:", url)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract title and article body
            title_m = re.search(r'<title>(.*?)</title>', html)
            title = title_m.group(1) if title_m else ""
            print("TITLE:", title)
            # Find article body or main content
            article_m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
            body = article_m.group(1) if article_m else html
            # Strip tags to get text
            text = re.sub(r'<[^>]+>', ' ', body)
            text = re.sub(r'\s+', ' ', text).strip()
            print("CONTENT PREVIEW:\n", text[:2000])
            print("\n")
    except Exception as e:
        print("ERROR:", e)
