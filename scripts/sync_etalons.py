import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_html = os.path.join(root, 'academy.html')
etalon_root = os.path.join(root, 'Эталоны.html')
etalon_folder = os.path.join(root, 'Эталоны', 'Эталоны.html')

for target in [etalon_root, etalon_folder]:
    shutil.copy2(academy_html, target)
    print(f"Copied {academy_html} -> {target} ({os.path.getsize(target)} bytes)")
