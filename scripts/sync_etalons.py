import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_html = os.path.join(root, 'academy.html')
etalon_path = os.path.join(root, 'Эталоны', 'Эталоны.html')
root_etalon = os.path.join(root, 'Эталоны.html')

shutil.copy2(academy_html, etalon_path)
shutil.copy2(academy_html, root_etalon)
print(f"Copied {academy_html} -> {etalon_path} ({os.path.getsize(etalon_path)} bytes)")
print(f"Copied {academy_html} -> {root_etalon} ({os.path.getsize(root_etalon)} bytes)")
