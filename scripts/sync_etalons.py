import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_html = os.path.join(root, 'academy.html')
standards_path = os.path.join(root, 'standards', 'standards.html')

os.makedirs(os.path.dirname(standards_path), exist_ok=True)
shutil.copy2(academy_html, standards_path)
print(f"Copied {academy_html} -> {standards_path} ({os.path.getsize(standards_path)} bytes)")

