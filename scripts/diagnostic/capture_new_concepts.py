# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
from PIL import Image

brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with open("mockup_skill_1_1_1.html", "r", encoding="utf-8") as f:
    base_html = f.read()

# Make sure tabs-variant-underline is display:none by default when stories is selected
base_html = base_html.replace(
    'id="tabs-variant-underline" class="tabs-variant-block"',
    'id="tabs-variant-underline" class="tabs-variant-block" style="display:none;"'
)

# 1. CAPTURE CONCEPT 1: Stories Header (Zero-Tabs)
# It has stories-track displayed and all tabs-variant-block hidden
with open("mockup_skill_1_1_1.html", "w", encoding="utf-8") as f:
    f.write(base_html)

subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\concept_1_stories_header.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_skill_1_1_1.html"
])

# 2. CAPTURE CONCEPT 2: Bottom Control Dock
# Bottom dock is visible, stories-track is hidden, default-progress-track is visible, all tabs-variant-block hidden
html_dock = base_html.replace(
    'id="bottom-control-dock" class="bottom-control-dock" style="display:none;"',
    'id="bottom-control-dock" class="bottom-control-dock" style="display:flex;"'
)
html_dock = html_dock.replace(
    '<option value="stories" selected>',
    '<option value="stories">'
).replace(
    '<option value="bottomdock">',
    '<option value="bottomdock" selected>'
)
html_dock = html_dock.replace(
    'id="stories-track"',
    'id="stories-track" style="display:none;"'
).replace(
    'id="default-progress-track" style="display:none;"',
    'id="default-progress-track"'
)

with open("mockup_skill_1_1_1.html", "w", encoding="utf-8") as f:
    f.write(html_dock)

subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\concept_2_bottom_dock.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_skill_1_1_1.html"
])

# 3. CAPTURE CONCEPT 3: Continuous Unified Flow
html_cont = base_html.replace(
    '<option value="stories" selected>',
    '<option value="stories">'
).replace(
    '<option value="continuous">',
    '<option value="continuous" selected>'
)
# Make all stages visible
html_cont = html_cont.replace(
    'id="stage-cards" class="stage-view" style="display:none;"',
    'id="stage-cards" class="stage-view"'
).replace(
    'id="stage-code" class="stage-view" style="display:none;"',
    'id="stage-code" class="stage-view"'
)

with open("mockup_skill_1_1_1.html", "w", encoding="utf-8") as f:
    f.write(html_cont)

subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    r"--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\concept_3_continuous.png",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_skill_1_1_1.html"
])

# Restore base HTML
with open("mockup_skill_1_1_1.html", "w", encoding="utf-8") as f:
    f.write(base_html)

with open("design_mockups/mockup_skill_1_1_1.html", "w", encoding="utf-8") as f:
    f.write(base_html)

print("Captures completed! Now cropping and copying...")

for name in ["concept_1_stories_header", "concept_2_bottom_dock", "concept_3_continuous"]:
    src = f"design_mockups/{name}.png"
    if os.path.exists(src):
        # copy full
        shutil.copyfile(src, os.path.join(brain_dir, f"{name}.png"))
        
        # crop header/tabs area or bottom
        img = Image.open(src)
        if name == "concept_2_bottom_dock":
            # crop bottom dock area (x: 260 to 1420, y: 720 to 900)
            crop_bottom = img.crop((260, 680, 1420, 890))
            crop_bottom.save(f"design_mockups/{name}_crop.png")
            crop_bottom.save(os.path.join(brain_dir, f"{name}_crop.png"))
        else:
            # crop top area (x: 260 to 1420, y: 0 to 220)
            crop_top = img.crop((260, 0, 1420, 220))
            crop_top.save(f"design_mockups/{name}_crop.png")
            crop_top.save(os.path.join(brain_dir, f"{name}_crop.png"))

print("All screenshots and crops prepared!")
