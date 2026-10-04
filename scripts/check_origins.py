import zipfile

orig_fixed_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNoteExport_Fury-Inf_md_2026-09-24_06-38_FIXED.zip'
remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

z1 = zipfile.ZipFile(orig_fixed_zip)
z2 = zipfile.ZipFile(remnote_python_zip)

c1 = sum(1 for n in z1.namelist() if '    - .' in z1.read(n).decode('utf-8', errors='ignore'))
c2 = sum(1 for n in z2.namelist() if '    - .' in z2.read(n).decode('utf-8', errors='ignore'))

print('Artifacts in RemNoteExport FIXED:', c1)
print('Artifacts in RemNote_Python.zip:', c2)
