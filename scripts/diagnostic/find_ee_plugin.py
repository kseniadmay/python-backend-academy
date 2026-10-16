import zipfile
import re

with zipfile.ZipFile(r'C:\Users\fury6\OneDrive\Документы\Обучение Python\PluginZip.zip') as z:
    code = z.read('index.js').decode('utf-8')

# Найдем место, где определяется команда link-current-note-to-cards или ee(Q)
pos = code.find('link-current-note-to-cards')
if pos != -1:
    print('Context around link-current-note-to-cards:')
    print(code[pos-200:pos+800])
    
# Найдем функцию ee
pos_ee = code.find('async function ee')
if pos_ee == -1:
    pos_ee = code.find('ee=async')
if pos_ee != -1:
    print('Found ee definition:')
    print(code[pos_ee:pos_ee+1000])
