import urllib.request
import json

def get_stepik_courses(query):
    url = f"https://stepik.org/api/search-results?query={query}&type=course&is_paid=false&page_size=10"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get("search-results", [])
            print(f"Results for '{query}': {len(results)}")
            course_ids = [str(r["target_id"]) for r in results if r.get("target_type") == "course"]
            if course_ids:
                courses_url = f"https://stepik.org/api/courses?ids[]=" + "&ids[]=".join(course_ids)
                req2 = urllib.request.Request(courses_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req2) as resp2:
                    cdata = json.loads(resp2.read().decode('utf-8'))
                    for c in cdata.get("courses", []):
                        print(f"ID: {c['id']} | Title: {c['title']} | Learners: {c['learners_count']} | Rating: {c['review_summary']}")
    except Exception as e:
        print(f"Error for {query}:", e)

print("--- Django Courses ---")
get_stepik_courses("Django")
print("\n--- FastAPI Courses ---")
get_stepik_courses("FastAPI")
print("\n--- Bash Linux Courses ---")
get_stepik_courses("Linux")
print("\n--- SQL Courses ---")
get_stepik_courses("SQL")
