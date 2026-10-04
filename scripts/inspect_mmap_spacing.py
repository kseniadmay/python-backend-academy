map_path = r'C:\Users\fury6\OneDrive\Документы\Обучение Python\Python_Backend_Academy_Mastery_Map.md'

with open(map_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('First 40 lines of Mastery Map:')
for i, l in enumerate(lines[:40], 1):
    print(f'{i:2d}: {repr(l)}')
