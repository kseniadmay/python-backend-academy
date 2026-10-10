import os
import subprocess

mockup_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\2b320042-cd74-466b-b716-1ee73a7ff7f2"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
academy_html = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"

# Создадим копию academy.html с data-theme="light" по умолчанию для прямого снимка
with open(academy_html, "r", encoding="utf-8") as f:
    text = f.read()

light_html_text = text.replace('<html lang="ru">', '<html lang="ru" data-theme="light">')
light_html_path = os.path.join(mockup_dir, "academy_live_light.html")
with open(light_html_path, "w", encoding="utf-8") as f:
    f.write(light_html_text)

light_png = os.path.join(brain_dir, "live_skill_111_light_parchment.png")
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1200,900",
    f"--screenshot={light_png}",
    f"file:///{light_html_path.replace(os.sep, '/')}#/python/skill/1.1.1"
], check=True)
print("Saved light parchment screenshot:", light_png)
