import urllib.request
import json
import re

def search_ddg(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract links and snippets
            results = re.findall(r'<a class="result__snippet[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
            if not results:
                # alternative pattern
                results = re.findall(r'<a class="result__url"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
            print(f"Results for '{query}':")
            # find result-snippet
            snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
            titles = re.findall(r'<a class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL)
            for i, (t_url, title) in enumerate(titles[:5]):
                snip = snippets[i] if i < len(snippets) else ""
                clean_title = re.sub(r'<[^>]+>', '', title)
                clean_snip = re.sub(r'<[^>]+>', '', snip)
                print(f"[{i+1}] {clean_title}\nURL: {t_url}\n{clean_snip}\n")
    except Exception as e:
        print("Error:", e)

search_ddg("site:help.remnote.com markdown import")
search_ddg("RemNote markdown flashcards syntax >>")
search_ddg("RemNote import markdown numbered list")
