import glob
import json

for f in glob.glob(r'C:\Users\fury6\.gemini\antigravity\brain\*\.system_generated\logs\transcript.jsonl'):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as log:
            for line in log:
                if 'USER_INPUT' in line and 'баз' in line.lower():
                    obj = json.loads(line)
                    cnt = obj.get('content', '')
                    if 'верни' in cnt.lower() or 'базу' in cnt.lower():
                        print(f"--- MATCH in {f} ---")
                        print(cnt)
    except:
        pass
