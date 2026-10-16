import subprocess
import shutil
import os
import time
from PIL import Image

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
test_html = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\test_screenshot_cards.html"
cards_png = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\live_skill_111_cards.png"
cards_crop_png = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\live_skill_111_cards_crop.png"

loader_html = """<!DOCTYPE html>
<html>
<head>
<script>
  try {
    const s = JSON.parse(localStorage.getItem('academy_state_v1') || '{}');
    if(!s.readingPositions) s.readingPositions = {};
    s.readingPositions['1.1.1'] = { tab: 'cards', fId: 'Ф-001', cardIdx: 0, updatedAt: Date.now() };
    localStorage.setItem('academy_state_v1', JSON.stringify(s));
  } catch(e){}
  window.location.replace('../academy.html#/python/skill/1.1.1');
</script>
</head>
<body>Redirecting to cards...</body>
</html>
"""

with open(test_html, "w", encoding="utf-8") as f:
    f.write(loader_html)

# Run chrome with slight delay
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    f"--screenshot={cards_png}",
    f"file:///{test_html.replace(os.sep, '/')}"
])

# Crop
if os.path.exists(cards_png):
    img = Image.open(cards_png)
    crop = img.crop((260, 0, 1420, 600))
    crop.save(cards_crop_png)
    shutil.copyfile(cards_png, os.path.join(brain_dir, "live_skill_111_cards.png"))
    shutil.copyfile(cards_crop_png, os.path.join(brain_dir, "live_skill_111_cards_crop.png"))
    print("Cards screenshot saved successfully!")
else:
    print("Failed to save screenshot")
