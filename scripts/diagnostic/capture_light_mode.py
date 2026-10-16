import os
import subprocess

mockup_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\2b320042-cd74-466b-b716-1ee73a7ff7f2"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
academy_html = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"

# Создадим html-обертку, которая установит в localStorage правильный ключ состояния
wrapper_path = os.path.join(mockup_dir, "capture_light_theme_wrapper.html")
with open(wrapper_path, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <script>
    try {
      const cur = JSON.parse(localStorage.getItem('pba_academy_state') || '{}');
      cur.theme = 'light';
      localStorage.setItem('pba_academy_state', JSON.stringify(cur));
      localStorage.setItem('theme', 'light');
    } catch(e){}
    window.location.replace('../academy.html#/python/skill/1.1.1');
  </script>
</head>
<body></body>
</html>
""")

light_png = os.path.join(brain_dir, "live_skill_111_light_mode.png")
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1200,900",
    f"--screenshot={light_png}",
    f"file:///{wrapper_path.replace(os.sep, '/')}"
], check=True)

print("Saved light mode screenshot:", light_png)
