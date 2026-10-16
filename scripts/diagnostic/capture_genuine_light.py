import os
import subprocess

mockup_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\2b320042-cd74-466b-b716-1ee73a7ff7f2"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
academy_html = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"

with open(academy_html, "r", encoding="utf-8") as f:
    text = f.read()

# Принудительно выставляем светлую тему во всем коде файла
light_text = text.replace(
    'document.documentElement.setAttribute(\'data-theme\', \'dark\');',
    'document.documentElement.setAttribute(\'data-theme\', \'light\');'
).replace(
    'state.theme = \'dark\';',
    'state.theme = \'light\';'
).replace(
    '<html lang="ru">',
    '<html lang="ru" data-theme="light">'
)

light_path = os.path.join(mockup_dir, "full_screen_light_mirror.html")
with open(light_path, "w", encoding="utf-8") as f:
    f.write(light_text)

png_path = os.path.join(brain_dir, "full_screen_light_mirror.png")
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,960",
    f"--screenshot={png_path}",
    f"file:///{light_path.replace(os.sep, '/')}#/python/skill/1.1.1"
], check=True)

print("Saved REAL light theme screenshot:", png_path)
