import os
import subprocess
import time

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\2b320042-cd74-466b-b716-1ee73a7ff7f2"
academy_html = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"

out_png = os.path.join(brain_dir, "live_skill_111_applied_v1a.png")

# Снимем страницу #/python/skill/1.1.1
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1200,900",
    f"--screenshot={out_png}",
    f"file:///{academy_html.replace(os.sep, '/')}#/python/skill/1.1.1"
], check=True)

print("Saved screenshot of live academy.html:", out_png)
