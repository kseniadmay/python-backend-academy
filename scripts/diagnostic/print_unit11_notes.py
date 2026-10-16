import zipfile

remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'
with zipfile.ZipFile(remnote_python_zip) as z:
    for n in z.namelist():
        if 'Юнит 1.1' in n and 'Конспекты' in n:
            print(n)
