import glob
import json
import re

for f in glob.glob(r'C:\Users\fury6\.gemini\antigravity\brain\*\.system_generated\logs\transcript.jsonl'):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as log:
            for line in log:
                if 'remote-debugging-port' in line or 'chrome.exe' in line.lower():
                    try:
                        obj = json.loads(line)
                        calls = obj.get('tool_calls', [])
                        for c in calls:
                            cmd = c.get('CommandLine', '')
                            if 'chrome' in cmd.lower() or 'debug' in cmd.lower():
                                print(f"Found in {f.split('/')[-1]}: {cmd[:150]}")
                    except:
                        pass
    except:
        pass
