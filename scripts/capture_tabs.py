# -*- coding: utf-8 -*-
import subprocess

with open('mockup_skill_1_1_1.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# 1. Capture Underline (already default)
subprocess.run([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new', '--disable-gpu', '--window-size=1440,900',
    r'--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\tab_style_1_underline.png',
    'file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_skill_1_1_1.html'
])

# 2. Capture Stepper
s2 = orig.replace('id="tabs-variant-underline" class="tabs-variant-block"', 'id="tabs-variant-underline" class="tabs-variant-block" style="display:none;"')
s2 = s2.replace('id="tabs-variant-stepper" class="tabs-variant-block" style="display:none;"', 'id="tabs-variant-stepper" class="tabs-variant-block"')
with open('mockup_skill_1_1_1.html', 'w', encoding='utf-8') as f:
    f.write(s2)

subprocess.run([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new', '--disable-gpu', '--window-size=1440,900',
    r'--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\tab_style_2_stepper.png',
    'file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_skill_1_1_1.html'
])

# 3. Capture Milestones
s3 = orig.replace('id="tabs-variant-underline" class="tabs-variant-block"', 'id="tabs-variant-underline" class="tabs-variant-block" style="display:none;"')
s3 = s3.replace('id="tabs-variant-milestones" class="tabs-variant-block" style="display:none;"', 'id="tabs-variant-milestones" class="tabs-variant-block"')
with open('mockup_skill_1_1_1.html', 'w', encoding='utf-8') as f:
    f.write(s3)

subprocess.run([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new', '--disable-gpu', '--window-size=1440,900',
    r'--screenshot=C:\Users\fury6\OneDrive\Python_Backend_Academy\design_mockups\tab_style_3_milestones.png',
    'file:///C:/Users/fury6/OneDrive/Python_Backend_Academy/mockup_skill_1_1_1.html'
])

# Restore default
with open('mockup_skill_1_1_1.html', 'w', encoding='utf-8') as f:
    f.write(orig)

# Copy to design_mockups
with open('design_mockups/mockup_skill_1_1_1.html', 'w', encoding='utf-8') as f:
    f.write(orig)

print("All 3 tab shots successfully captured!")
