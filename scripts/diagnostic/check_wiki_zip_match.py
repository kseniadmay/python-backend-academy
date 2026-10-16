import zipfile
import re

zip_path = r'C:\Users\fury6\OneDrive\Desktop\RemNote_Mastery_Import_Ready.zip'
with zipfile.ZipFile(zip_path) as z:
    all_names = z.namelist()
    map_content = z.read('Собеседования/00 · 🗺️ Карта Мастерства.md').decode('utf-8')
    
    # Ищем все ссылки [[...]]
    wiki_links = re.findall(r'\[\[(.*?)\]\]', map_content)
    print('Total wiki links in map:', len(wiki_links))
    
    # Базовые имена файлов в zip без .md
    zip_basenames = {re.sub(r'\.md$', '', name.split('/')[-1]): name for name in all_names if name.endswith('.md')}
    
    unmatched = []
    for link in wiki_links:
        if link not in zip_basenames:
            unmatched.append(link)
            
    print('Unmatched links count:', len(unmatched))
    if unmatched:
        print('Sample unmatched:', unmatched[:10])
    else:
        print('All links strictly match zip basenames!')
