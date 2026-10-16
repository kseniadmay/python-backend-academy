import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_html = os.path.join(root, 'academy.html')
etalon_path = os.path.join(root, 'Эталоны', 'Эталоны.html')

shutil.copy2(academy_html, etalon_path)
print(f"Copied {academy_html} -> {etalon_path} ({os.path.getsize(etalon_path)} bytes)")
