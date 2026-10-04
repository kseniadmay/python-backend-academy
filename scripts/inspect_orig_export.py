import zipfile

orig_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNoteExport_Fury-Inf_md_2026-09-24_06-38_FIXED.zip'
with zipfile.ZipFile(orig_zip) as z:
    for n in z.namelist()[:20]:
        print('FILE:', n)
        lines = z.read(n).decode('utf-8', errors='ignore').splitlines()[:5]
        for l in lines:
            print('  ', repr(l))
