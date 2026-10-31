import shutil

src = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"
dst = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\standards\standards.html"

shutil.copyfile(src, dst)
print("Copied academy.html -> standards/standards.html successfully!")
