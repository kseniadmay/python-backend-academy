# Python Backend Academy (RemNote Mastery) — Облачный репозиторий проекта

Добро пожаловать в каноническую облачную директорию интерактивной образовательной платформы **Python Backend Academy**.

---

## 📂 Структура проекта

```text
Python_Backend_Academy/
│
├── academy.html                             # Главное интерактивное веб-приложение Академии (SPA, 7 модулей, 64 урока, 401 задача)
├── Практика кода — тренажёр с IDE.html      # Автономный тренажёр задач с изолированной IDE и тестами
├── HANDOVER_CONTEXT.md                      # Полная спецификация передачи контекста и архитектурные инварианты
├── PROJECT_CONTEXT.md                       # Технический паспорт проекта, матрицы мастерства и реестр навыков
├── Python_Backend_Academy_Project.zip       # Полный дистрибутивный архив проекта с исходниками
├── RemNote_Python_Mastery_FIXED.zip         # Архив канонической базы заметок и колод RemNote
│
├── RemNote_Python_Mastery_FIXED/            # Распакованная база RemNote (525 файлов Markdown):
│   ├── Модуль 01 — Основы Python (K-заметки и F-колоды)
│   ├── Модуль 02 — Web и Сети
│   ├── Модуль 03 — Архитектура бэкенда и базы данных
│   ├── Модуль 04 — Алгоритмы и структуры данных
│   ├── Модуль 05 — Базы данных и SQL
│   ├── Модуль 06 — Архитектура систем и паттерны
│   ├── Модуль 07 — DevOps, Инфраструктура и мониторинг
│   └── 🗺️ Карта Мастерства — Python Backend Junior to Middle.md
│
└── scripts/                                 # Полный комплект инструментов сборки, обогащения и тестирования:
    ├── assemble_academy.py                  # Главный сборщик монолитного academy.html
    ├── verify_academy.py                    # Быстрый валидатор синтаксиса JS и рендеринга маршрутов в Headless Chrome
    ├── test_all_401_tasks.py                # Комплексный верификатор всех 401 задач IDE, сниппетов и босс-челленджей
    ├── test_e2e_dom.js                      # E2E DOM-тестирование всех роутов, уроков и колод
    ├── build_python_mastery.py              # Парсер и генератор структур данных Python Mastery
    ├── extract_remnote_data.py              # Извлечение и нормализация заметок/карточек из базы RemNote
    ├── generate_new_lessons.py              # Генерация интерактивных уроков
    └── enrich_*.py                          # Скрипты обогащения контента по модулям 02–07
```

---

## 🚀 Быстрый запуск

### 1. Открытие платформы в браузере
Дважды кликните по файлу `academy.html` или откройте его в Google Chrome:
```powershell
Start-Process "chrome.exe" (Resolve-Path ".\academy.html")
```

### 2. Запуск E2E DOM-тестов
```powershell
node .\scripts\test_e2e_dom.js
```

### 3. Запуск верификатора Headless Chrome и JS
```powershell
python .\scripts\verify_academy.py
```

### 4. Комплексная проверка 401 задачи IDE и сниппетов
```powershell
python .\scripts\test_all_401_tasks.py
```

### 5. Пересборка проекта
```powershell
python .\scripts\assemble_academy.py
```

---

## ☁️ Синхронизация с OneDrive
Данная папка расположена в вашем личном облаке Microsoft OneDrive (`%USERPROFILE%\OneDrive\Python_Backend_Academy`). Все изменения, добавленные заметки и результаты сборки автоматически реплицируются в облако.
На вашем Рабочем столе создан ярлык: **`Python Backend Academy (Cloud)`**.
