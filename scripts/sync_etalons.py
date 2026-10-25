import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_html = os.path.join(root, 'academy.html')
standards_path = os.path.join(root, 'standards', 'standards.html')

if not os.path.isfile(standards_path):
    raise FileNotFoundError(f'Canonical standard not found: {standards_path}')

shutil.copy2(standards_path, academy_html)
print(f"Copied {standards_path} -> {academy_html} ({os.path.getsize(academy_html)} bytes)")

