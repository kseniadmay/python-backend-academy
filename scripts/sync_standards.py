import os
import shutil

_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
src = os.path.join(_ROOT, 'academy.html')
dst = os.path.join(_ROOT, 'standards', 'standards.html')

shutil.copyfile(src, dst)
print("Copied academy.html -> standards/standards.html successfully!")
