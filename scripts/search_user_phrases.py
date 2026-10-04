import glob
import json

for f in glob.glob(r'C:\Users\fury6\.gemini\antigravity\brain\*\.system_generated\logs\transcript.jsonl'):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as log:
            for line in log:
                if 'USER_INPUT' in line and ('баз' in line.lower() or 'верни' in line.lower()):
                    try:
                        obj = json.loads(line)
                        cnt = obj.get('content', '')
                        if any(w in cnt.lower() for w in ['баз', 'верни', 'архив']):
                            print(f"Transcript: {f.split('/')[-1]}")
                            print(f"Content: {cnt[:200]}")
                            print('-'*40)
                    except:
                        pass
    except Exception as e:
        pass
