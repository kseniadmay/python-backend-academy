import os

with open('design_mockups/full_screen_light_mirror.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make variant 1: airy soft (без капсулы, невесомые капли, мягкая окантовка)
v1_html = content

# Make variant 2: capsule soft (деликатная полупрозрачная капсула-трекер)
v2_html = content.replace(
    '<div class="dots-necklace" id="radar-dots-necklace"',
    '<div class="dots-necklace dots-necklace--capsule" id="radar-dots-necklace"'
).replace(
    '</style>',
    """  .dots-necklace--capsule {
    display: inline-flex !important;
    width: auto !important;
    padding: 6px 16px !important;
    border-radius: 999px !important;
    background: rgba(15, 23, 42, 0.035) !important;
    border: 1px solid rgba(15, 23, 42, 0.06) !important;
    gap: 8px !important;
  }
  :root[data-theme="dark"] .dots-necklace--capsule {
    background: rgba(255, 255, 255, 0.035) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
  }
</style>"""
)

with open('design_mockups/full_screen_v1_airy.html', 'w', encoding='utf-8') as f:
    f.write(v1_html)

with open('design_mockups/full_screen_v2_capsule.html', 'w', encoding='utf-8') as f:
    f.write(v2_html)

print('Generated full_screen_v1_airy.html and full_screen_v2_capsule.html')
