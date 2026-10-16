import os

with open('design_mockups/full_screen_v2_capsule.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Make variant 3: stacked left with capsule dots
v3_html = c.replace(
    '<div style="display:flex;justify-content:center;width:100%;">',
    '<div style="display:flex;justify-content:flex-start;width:100%;margin-top:2px;">'
)

with open('design_mockups/full_screen_v3_stacked_left.html', 'w', encoding='utf-8') as f:
    f.write(v3_html)

print('Generated full_screen_v3_stacked_left.html')
