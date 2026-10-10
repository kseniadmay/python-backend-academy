# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
import time
from PIL import Image

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
brain_dir = r"C:\Users\fury6\.gemini\antigravity\brain\d689245c-f3a9-498f-b883-ee4a97e4b9bc"
live_png = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\live_skill_111.png"

# Делаем скриншот с небольшой задержкой для отработки hash-роутинга
subprocess.run([
    chrome_path,
    "--headless=new", "--disable-gpu", "--window-size=1440,900",
    f"--screenshot={live_png}",
    "file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/academy.html#/python/skill/1.1.1"
])

# Crop
img = Image.open(live_png)
crop = img.crop((260, 0, 1420, 320))
crop_png = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\live_skill_111_crop.png"
crop.save(crop_png)

# Copy to brain
shutil.copyfile(live_png, os.path.join(brain_dir, "live_skill_111.png"))
shutil.copyfile(crop_png, os.path.join(brain_dir, "live_skill_111_crop.png"))

print("Captured live_skill_111 screenshot!")
