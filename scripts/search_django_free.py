import urllib.request
import json

def get_free_django():
    for page in range(1, 4):
        url = f"https://stepik.org/api/search-results?query=Django&type=course&is_paid=false&page={page}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            cids = [str(r["target_id"]) for r in data.get("search-results", []) if r.get("target_type") == "course"]
            if not cids:
                break
            curl = "https://stepik.org/api/courses?ids[]=" + "&ids[]=".join(cids)
            req2 = urllib.request.Request(curl, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req2) as resp2:
                cdata = json.loads(resp2.read().decode('utf-8'))
                for c in cdata.get("courses", []):
                    if "django" in c["title"].lower() or "веб" in c["title"].lower() or "web" in c["title"].lower():
                        print(f"ID: {c['id']} | Learners: {c['learners_count']} | Title: {c['title']}")

get_free_django()
