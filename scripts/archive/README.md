# Архив разовых миграций и устаревших диагностик

В этой директории сохранены исторические скрипты миграций данных и ранней отладки интерфейса. Они зафиксированы в Git для сохранения истории изменений, но исключены из активного конвейера сборки и тестирования платформы.

---

## 📁 Структура архива

### `migrations/` — Разовые инкрементальные скрипты трансформации данных
- `apply_unit_191_atomic_quantization.py` — Атомарное квантование конспектов и задач юнита 1.9.1.
- `apply_skill_and_cards_pipeline.py` — Пайплайн привязки флеш-карточек к навыкам.
- `apply_generator_notes_fixes.py` — Корректировка форматирования генераторов конспектов.
- `apply_echelon_program_selector.py` — Внедрение селектора программ и эшелонов.
- `apply_descriptor_improvements.py`, `apply_descriptor_v2.py`, `apply_descriptor_v3.py`, `apply_descriptor_v4.py` — Итерации улучшения структуры дескрипторов задач.
- `apply_dashboard_refinement.py`, `apply_laconic_dashboard.py`, `apply_dashboard_laconic_phase2.py`, `apply_dashboard_laconic_phase3.py`, `apply_dashboard_laconic_phase4.py` — Итеративная разгрузка и лаконизация экрана дашборда.
- `apply_notes_button_styling.py` — Стилизация кнопок перехода к конспектам.

### `legacy_diagnostics/` — Специфические разовые тесты и зонды
- `test_accordion_debug.js`, `test_accordion_visual.js` — Отладка поведения и анимации аккордеона модулей.
- `test_jewels_and_accordion.js` — Проверка кликабельности самоцветов и аккордеонов.
- `deep_line_by_line_beads_audit.js` — Построчный аудит индикаторов-бусин (beads) прогресса.
- `deep_skill_audit.js` — Глубокий аудит структуры дерева навыков.

---

> [!NOTE]
> Все актуальные регрессионные тесты перенесены и централизованы в директориях [`tests/`](../../tests/) и активном корне [`scripts/`](../).
