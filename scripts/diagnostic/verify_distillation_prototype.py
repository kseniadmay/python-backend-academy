import os, sys, re, subprocess, tempfile, shutil
from pathlib import Path

def get_chrome():
    candidates = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
        os.path.expandvars(r'%PROGRAMFILES%\Google\Chrome\Application\chrome.exe'),
        os.path.expandvars(r'%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe'),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    for cmd in ('chrome', 'google-chrome', 'chromium'):
        p = shutil.which(cmd)
        if p:
            return p
    return candidates[0]

chrome_exe = get_chrome()
assert os.path.isfile(chrome_exe), f"Chrome not found at {chrome_exe}"

proto_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'design_mockups', 'style_distillation_prototype.html'))
assert os.path.isfile(proto_path), f"File not found: {proto_path}"

base_uri = Path(proto_path).as_uri()

chrome_flags = [
    chrome_exe, '--headless', '--no-sandbox', '--disable-gpu',
    '--disable-background-networking', '--disable-sync', '--disable-default-apps',
    '--allow-file-access-from-files',
    '--enable-logging=stderr', '--dump-dom'
]

print("=== VERIFYING STYLE DISTILLATION PROTOTYPE IN HEADLESS CHROME ===")
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
    cmd = chrome_flags + [f'--user-data-dir={td}', base_uri]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

    # 1. Console errors
    c_errors = [line for line in res.stderr.splitlines() if 'ERROR:CONSOLE' in line or 'Uncaught ' in line]
    if c_errors:
        print(f"[FAIL] Console errors:\n" + "\n".join(c_errors))
        sys.exit(1)
    else:
        print("[PASS] 0 console errors!")

    # 2. DOM text leaks
    dom = res.stdout
    leak_matches = re.findall(r'>\s*(undefined|null)\s*<', dom, re.I)
    if leak_matches:
        print(f"[FAIL] Visible text leak {leak_matches} found in prototype DOM")
        sys.exit(1)
    else:
        print("[PASS] 0 undefined/null text leaks!")

    # 3. Check essential sections
    for sec in ['tab-tokens', 'tab-path', 'tab-map', 'tab-tracks', 'tab-mock', 'tab-sandbox', 'tab-docs', 'tab-settings']:
        assert f'id="{sec}"' in dom, f"Missing section #{sec}"
    print("[PASS] All 8 showcase sections verified!")

    print(f"[PASS] Total rendered DOM size: {len(dom):,} chars")
