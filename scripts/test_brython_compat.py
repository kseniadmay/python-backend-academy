import subprocess, os

test_html = """<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/brython/3.13.0/brython.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/brython/3.13.0/brython_stdlib.js"></script>
</head>
<body onload="brython()">
<div id="res"></div>
<script type="text/python">
from browser import document
out = []
for mod in ['multiprocessing', 'cProfile', 'threading', 'sqlite3', 'time']:
    try:
        __import__(mod)
        out.append(f"{mod}: OK")
    except Exception as e:
        out.append(f"{mod}: ERROR ({e})")
document['res'].text = " | ".join(out)
</script>
</body>
</html>"""

html_path = os.path.abspath('brython_compat_test.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(test_html)

chrome_exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [chrome_exe, '--headless', '--no-sandbox', '--disable-gpu', '--virtual-time-budget=5000', '--dump-dom', f'file:///{html_path.replace(os.sep, "/")}']
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=20)

import re
m = re.search(r'<div id="res">(.*?)</div>', res.stdout)
if m:
    print("Brython Module Results:", m.group(1))
else:
    print("Could not find #res in output:", res.stdout[:500])

if os.path.exists(html_path):
    os.remove(html_path)
