import zipfile
import re

remnote_python_zip = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\RemNote_Python.zip'

with zipfile.ZipFile(remnote_python_zip) as z:
    for n in z.namelist():
        if '01. Структуры данных' in n:
            text = z.read(n).decode('utf-8')
            lines = text.splitlines()
            
            # Посмотрим, как вставлять H1 и пустые буллеты
            new_lines = []
            new_lines.append('# К-001. Структуры данных Python_ list, dict, set')
            new_lines.append('- ')
            
            for l in lines:
                # Если встречаем заголовок ##, перед ним проверяем пустой буллет
                if l.startswith('- ##') or l.startswith('##'):
                    if new_lines and new_lines[-1] != '- ':
                        new_lines.append('- ')
                    new_lines.append(l if l.startswith('- ') else f'- {l}')
                else:
                    new_lines.append(l)
            
            sample_result = '\n'.join(new_lines[:35])
            print('SAMPLE TRANSFORMED NOTE:')
            print(sample_result)
            break
