from test_clean_all_cards import clean_card_file, zip_path
import zipfile

with zipfile.ZipFile(zip_path) as z:
    raw = z.read('RemNote_Python/01 · 🐍 Python/Юнит 1.1 · Базовый синтаксис/📇 Карточки/Срезы.md').decode('utf-8')
cleaned = clean_card_file(raw)
for line in cleaned.splitlines()[:20]:
    print(line)
