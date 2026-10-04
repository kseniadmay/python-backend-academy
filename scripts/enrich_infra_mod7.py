# -*- coding: utf-8 -*-
"""
enrich_infra_mod7.py
Полная вычитка с нуля простым языком для новичка и обогащение Модуля 07
(07 · 🚀 Инфраструктура, Юниты 7.1–7.6, 21 навык, 47 конспектов К-170..К-216, 35 колод Ф-*).
Каждая заметка содержит:
- 4 интерактивных микро-шага (разделитель ---)
- Бытовую ментальную модель для новичка
- Пошаговую ASCII-диаграмму (```text)
- Сравнительную Markdown-таблицу
- Блок > **Junior vs Senior**: (.jvs-grid)
- 100% самодостаточный запускаемый Python 3.13 сниппет с print()
"""
import os
import shutil

BASE_DIR = r"C:\Users\fury6\OneDrive\Desktop\RemNote_Python_Mastery_FIXED"
MOD7_DIR = os.path.join(BASE_DIR, "07 · 🚀 Инфраструктура")
MAP_FILE = os.path.join(BASE_DIR, "00 · 🗺️ Карта Мастерства.md")

NOTES = {}

# ==============================================================================
# ЮНИТ 7.1 · GIT (К-170 .. К-180)
# ==============================================================================

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-170. Ветки в Git_ checkout, switch и.md"] = r"""📖 Перечитать конспект: Ветки в Git: checkout, switch и указатель HEAD >>
### 1. Ментальная модель: Ветка — это стикер-закладка, а не копия папки
Новички часто думают, что создание ветки в Git копирует все файлы проекта в новую папку. На самом деле **ветка (branch)** — это крошечный текстовый файл (41 байт), в котором записан хеш одного конкретного коммита (как стикер-закладка в книге). А указатель **`HEAD`** — это ваш «взгляд» сейчас: он показывает, на какой закладке вы находитесь.

```text
История коммитов (граф DAG):
[c1: init] ◄── [c2: auth] ◄── [c3: payments]   (ветка main)
                   ▲
                   └── [c4: fix-login]         (ветка feat/login)
                               ▲
                              HEAD (вы работаете здесь)
```

Когда вы делаете новый коммит, Git создаёт снимок с ссылкой на родителя и просто передвигает стикер текущей ветки на 1 шаг вперёд. Создание ветки занимает 0.001 секунды и почти 0 байт на диске!

---
### 2. Почему `git checkout` разделили на `switch` и `restore`?
До Git 2.23 команда `git checkout` была перегружена: она и переключала ветки, и отменяла изменения в файлах (из-за чего разработчики случайно стирали свой код, если имя ветки совпадало с именем файла). Поэтому её разделили на две безопасные команды:

```bash
# Современный способ (Git 2.23+):
git switch main                 # Переключиться на существующую ветку main
git switch -c feat/oauth        # Создать новую ветку feat/oauth и перейти в неё
git switch -                    # Вернуться на предыдущую ветку (как кнопка Back)

# Отмена изменений в файле (вместо старого checkout -- file.py):
git restore app/auth.py         # Вернуть файл к состоянию последнего коммита
git restore --staged app/db.py  # Убрать файл из индекса (git add), сохранив код
```

| Задача | Старая команда (`checkout`) | Современная команда (`2.23+`) | Безопасность |
| :--- | :--- | :--- | :--- |
| Переключить ветку | `git checkout dev` | `git switch dev` | Не затрёт одноимённый файл |
| Создать ветку и перейти | `git checkout -b feat` | `git switch -c feat` | Чёткое намерение |
| Сбросить изменения файла | `git checkout -- a.py` | `git restore a.py` | Явная работа с файлами |
| Оторвать HEAD на коммит | `git checkout a1b2c3d` | `git switch --detach a1b2c3d` | Требует явного флага `--detach` |

---
### 3. Ловушка `Detached HEAD` (Оторванная голова)
Если вы переключитесь напрямую на хеш коммита (`git checkout a1b2c3`), указатель `HEAD` перестанет смотреть на стикер ветки и уткнётся прямо в коммит. Это режим **Detached HEAD**.

> **Junior vs Senior**:
> - **Junior**: Оказавшись в `Detached HEAD`, делает 3 новых коммита, а потом выполняет `git switch main`. Коммиты «исчезают» (на них не указывает ни одна ветка), и джун в панике переписывает код заново.
> - **Senior**: Знает, что в `Detached HEAD` можно безопасно осматривать старый код. А если случайно сделал там коммиты — просто прикрепляет к текущему месту новую закладку командой `git switch -c rescue-branch` (или находит хеш через `git reflog`) за 2 секунды.

---
### 4. Живая проверка: симуляция графа коммитов, веток и `HEAD`
Запустим модель хранилища Git на Python и увидим, как `switch -c` и `commit` двигают указатели за $O(1)$:

```python
class MiniGitRepo:
    def __init__(self) -> None:
        self.commits: dict[str, dict] = {"c1": {"msg": "initial commit", "parent": None}}
        self.branches: dict[str, str] = {"main": "c1"}
        self.head: str = "main"  # Имя активной ветки или хеш (если detached)

    def commit(self, cid: str, msg: str) -> None:
        parent = self.branches.get(self.head, self.head)
        self.commits[cid] = {"msg": msg, "parent": parent}
        if self.head in self.branches:
            self.branches[self.head] = cid

    def switch(self, branch: str, create: bool = False) -> None:
        if create:
            current_commit = self.branches.get(self.head, self.head)
            self.branches[branch] = current_commit
        self.head = branch

repo = MiniGitRepo()
repo.commit("c2", "feat: add user model")
repo.switch("feat/jwt", create=True)
repo.commit("c3", "feat: add jwt token")

print(f"HEAD указывает на ветку: {repo.head}")
print(f"Ветка main      -> {repo.branches['main']} ({repo.commits[repo.branches['main']]['msg']})")
print(f"Ветка feat/jwt  -> {repo.branches['feat/jwt']} ({repo.commits[repo.branches['feat/jwt']]['msg']})")
```
"""

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-171. Git Merge vs Git Rebase.md"] = r"""📖 Перечитать конспект: Git Merge vs Git Rebase >>
### 1. Ментальная модель: Честный дневник (`merge`) или Чистовик (`rebase`)
Представьте, что вы пишете главу книги в черновике (`feat`), пока главный редактор обновил основную рукопись (`main`).
- **`git merge`** — это сшивание двух версий специальным «узлом-скрепкой» (merge-коммитом). История остаётся на 100% документальной со всеми развилками.
- **`git rebase`** — это переписывание ваших черновых страниц набело поверх самой свежей версии `main`. Развилка исчезает, история становится идеально прямой линией, но ваши коммиты получают **новые хеши**.

```text
До объединения:
      A ── B  (feat)
     /
M1 ── M2      (main)

1) git merge feat (внутри main):       2) git rebase main (внутри feat):
      A ── B                                         A' ── B' (feat, новые хеши!)
     /      \                                       /
M1 ── M2 ─── M3 (merge commit)         M1 ────── M2 (main)
```

---
### 2. Сравнение стратегий слияния и флаг `--force-with-lease`
Когда вы сделали `rebase` локальной ветки, которую уже пушили в свой Pull Request, обычный `git push` будет отклонён (ведь хеши изменились).

```bash
# Сценарий 1: Подтянуть свежий main в свою рабочую ветку через rebase
git switch feat/orders
git fetch origin
git rebase origin/main
git push --force-with-lease origin feat/orders

# Сценарий 2: Влить готовую ветку в main с сохранением узла слияния
git switch main
git merge --no-ff feat/orders
```

| Критерий | `git merge` | `git rebase` | `git merge --squash` |
| :--- | :--- | :--- | :--- |
| **Форма истории** | Ветвистая (с узлами слияния) | Идеально линейная | Линейная (1 коммит на всю фичу) |
| **Хеши коммитов** | Сохраняются неизменными | Пересчитываются заново (`A'`, `B'`) | Схлопываются в 1 новый коммит |
| **Разрешение конфликтов** | Один раз в итоговом merge-коммите | Пошагово на каждом коммите ветки | Один раз при схлопывании |
| **Где применять** | В публичных ветках (`main`, `dev`) | В личной feature-ветке перед PR | При слиянии PR с кучей «wip»-коммитов |

---
### 3. Золотое правило Rebase и ловушка `push --force`
Никогда не делайте `rebase` публичной ветки (`main` / `develop`), на которой уже работают коллеги!

> **Junior vs Senior**:
> - **Junior**: После `git rebase` видит ошибку при пуше и бездумно запускает `git push --force` (`-f`). Если коллега минуту назад запушил в эту же ветку фикс, `--force` молча уничтожит чужую работу.
> - **Senior**: Всегда использует `git push --force-with-lease`. Эта команда проверяет, не обновился ли удалённый бранч на сервере с момента вашего последнего `fetch`. Если там есть чужие коммиты, Git остановит пуш и спасёт код команды.

---
### 4. Живая проверка: как `merge` и `rebase` меняют граф коммитов
Сравним структуру графа истории после `merge` и после `rebase` на Python:

```python
def simulate_merge(main_log: list[str], feat_log: list[str]) -> list[str]:
    return main_log + feat_log + [f"Merge({main_log[-1]}+{feat_log[-1]})"]

def simulate_rebase(main_log: list[str], feat_commits: list[str]) -> list[str]:
    rebased = [f"{c}'(on {main_log[-1]})" for c in feat_commits]
    return main_log + rebased

main_branch = ["M1", "M2"]
feat_branch = ["A", "B"]

print("После git merge :", " -> ".join(simulate_merge(main_branch, feat_branch)))
print("После git rebase:", " -> ".join(simulate_rebase(main_branch, feat_branch)))
```
"""

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-172. Git Stash.md"] = r"""📖 Перечитать конспект: Git Stash: временный карман разработчика >>
### 1. Ментальная модель: Выдвижной ящик рабочего стола
Представьте: вы разобрали на столе половину часов (код не дописан, тесты падают), и тут вбегает тимлид: «Срочно почини баг на проде в ветке `main`!». Делать сырой коммит `wip: broken` — плохая практика, а переключать ветку с конфликтующими изменениями Git не даст.
Команда **`git stash`** одним движением сгребает все незакоммиченные правки в выдвижной ящик (стек) и оставляет рабочий стол кристально чистым (как после последнего коммита).

```text
Рабочая папка (грязная) ──► git stash push -u -m "wip: cart" ──► Стек Stash [stash@{0}]
Рабочая папка (чистая)  ──► чиним хотфикс в main
Возвращаемся в ветку    ──► git stash pop                    ──► Правки снова на столе!
```

---
### 2. Главные команды и скрытая ловушка новых файлов (`-u`)
По умолчанию `git stash` прячет только те файлы, о которых Git уже знает (tracked). Если вы создали новый файл `utils.py` и не сделали `git add`, обычный `git stash` оставит его на столе! Используйте флаг **`-u` (`--include-untracked`)**.

```bash
# Спрятать все правки + новые неотслеживаемые файлы с понятной подписью:
git stash push -u -m "feat: незавершённая валидация оплаты"

# Посмотреть список всех отложенных «ящиков» в стеке:
git stash list

# Вернуть верхний ящик обратно в код и УДАЛИТЬ его из стека:
git stash pop

# Применить ящик stash@{1}, но ОСТАВИТЬ его копию в стеке на всякий случай:
git stash apply stash@{1}
```

| Команда | Что делает с рабочей директорией | Удаляет ли запись из стека? | Что с новыми (`untracked`) файлами? |
| :--- | :--- | :--- | :--- |
| `git stash` | Прячет изменения tracked-файлов | Создаёт `stash@{0}` | Игнорирует (остаются в папке!) |
| `git stash push -u -m "..."` | Прячет всё, включая новые файлы | Создаёт `stash@{0}` с именем | Безопасно прячет в стек |
| `git stash pop` | Возвращает правки из `stash@{0}` | **Да** (если не было конфликта) | Восстанавливает |
| `git stash apply` | Возвращает правки из стека | **Нет** (хранит копию в стеке) | Восстанавливает |
| `git stash drop stash@{0}` | Не меняет рабочую папку | Удаляет выбранную запись | — |

---
### 3. Правила безопасности со стеком `stash`
Стек `stash` работает по принципу **LIFO** (Last-In, First-Out — последним положил, первым достал).

> **Junior vs Senior**:
> - **Junior**: Копит по 15 безымянных стэшей (`WIP on main...`), забывает, что внутри, и не использует `-u`, теряя новые файлы при переключении веток.
> - **Senior**: Использует `stash` максимум на несколько часов с осмысленным сообщением (`git stash push -u -m "reason"`). А если работу нужно отложить на несколько дней — создаёт временную ветку или сразу превращает стэш в ветку командой `git stash branch feat/from-stash`.

---
### 4. Живая проверка: LIFO-стек `git stash` с поддержкой флага `-u`
Проверим на Python, почему без флага `include_untracked=True` новые файлы остаются в рабочей папке:

```python
class GitStashSimulator:
    def __init__(self) -> None:
        self.tracked = {"app.py": "v2 (modified)"}
        self.untracked = {"new_helper.py": "def help(): pass"}
        self.stack: list[dict] = []

    def push(self, msg: str, include_untracked: bool = False) -> None:
        entry = {"msg": msg, "tracked": self.tracked.copy(), "untracked": {}}
        self.tracked = {"app.py": "v1 (clean)"}
        if include_untracked:
            entry["untracked"] = self.untracked.copy()
            self.untracked.clear()
        self.stack.append(entry)

    def pop(self) -> dict:
        entry = self.stack.pop()
        self.tracked.update(entry["tracked"])
        self.untracked.update(entry["untracked"])
        return entry

sim = GitStashSimulator()
sim.push("wip: payment form", include_untracked=True)
print(f"После stash -u: tracked={sim.tracked['app.py']}, untracked={list(sim.untracked)}")
restored = sim.pop()
print(f"После stash pop ({restored['msg']}): tracked={sim.tracked['app.py']}, untracked={list(sim.untracked)}")
```
"""

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-173. Git Cherry-Pick.md"] = r"""📖 Перечитать конспект: Git Cherry-Pick: точечный перенос коммитов >>
### 1. Ментальная модель: Пинцет кондитера для одной «вишенки»
Обычно мы вливаем в `main` целую ветку со всеми её коммитами (`merge`). Но что, если в огромной ветке `feat/redesign` (которая выйдет только через месяц) разработчик попутно починил критическую опечатку в расчёте НДС одним коммитом `f89a12b`?
Нам нужен **только этот один коммит** прямо сейчас в релизной ветке! Команда **`git cherry-pick`** работает как пинцет: берёт дельту (изменения) одного конкретного коммита из любой ветки и аккуратно воспроизводит её на вашей текущей ветке как новый коммит.

```text
Ветка feat/redesign:  A ── B ── [C: fix tax bug] ── D (ещё не готово)
                                       │
                              git cherry-pick C
                                       ▼
Ветка release/v1.2:   M1 ───────────► [C': fix tax bug] (только нужный фикс!)
```

---
### 2. Команды `cherry-pick` и флаг `-x` для прозрачности истории
При переносе коммита `C` в другую ветку Git создаёт коммит `C'` с тем же автором и текстом, но **с новым хешем** (так как родитель изменился). Чтобы через полгода было понятно, откуда взялся этот хотфикс, в продакшене используют флаг **`-x`** — он автоматически дописывает строку `(cherry picked from commit ...)`.

```bash
# 1. Переходим в целевую релизную ветку, куда нужно доставить хотфикс:
git switch release/v1.2

# 2. Переносим конкретный коммит с записью исходного хеша (-x):
git cherry-pick -x f89a12b

# 3. Если нужно применить изменения в файлы, но НЕ создавать коммит сразу:
git cherry-pick --no-commit f89a12b

# 4. При возникновении конфликта — исправить файлы, сделать git add и продолжить:
git cherry-pick --continue   # (или git cherry-pick --abort для отмены)
```

| Режим | Команда | Что происходит в репозитории | Когда использовать |
| :--- | :--- | :--- | :--- |
| **С трассировкой (стандарт)** | `git cherry-pick -x <hash>` | Создаёт коммит с пометкой исходного SHA | Бэкпорт хотфиксов в `release/*` |
| **Без авто-коммита** | `git cherry-pick -n <hash>` | Кладет правки в индекс (`staged`) | Когда нужно объединить 2–3 фикса в один |
| **Диапазон коммитов** | `git cherry-pick A..B` | Переносит все коммиты после `A` до `B` | Перенос серии коммитов в другую ветку |

---
### 3. Почему нельзя злоупотреблять `cherry-pick` вместо `merge`?
Если постоянно копировать коммиты между `dev` и `main` через `cherry-pick`, в обеих ветках появятся коммиты-близнецы с одинаковым кодом, но **разными хешами**.

> **Junior vs Senior**:
> - **Junior**: Вместо нормального слияния веток переносит десятки коммитов через `cherry-pick`. При следующем `git merge` Git видит одинаковые правки с разными хешами и выдаёт лавину ложных конфликтов (duplicate changes).
> - **Senior**: Использует `cherry-pick -x` строго для экстренных бэкпортов (hotfix из `main` в старый `release/1.0`) или спасения коммита, случайно сделанного не в той ветке.

---
### 4. Живая проверка: перенос патча с генерацией нового SHA и метки `-x`
Посмотрим на Python, как `cherry-pick -x` копирует патч коммита на новую базу, меняя его хеш:

```python
import hashlib

def make_commit(parent_sha: str, patch: str, msg: str) -> dict:
    raw = f"{parent_sha}:{patch}:{msg}".encode()
    return {"sha": hashlib.sha1(raw).hexdigest()[:7], "parent": parent_sha, "patch": patch, "msg": msg}

def cherry_pick(target_head: dict, source_commit: dict, record_origin: bool = True) -> dict:
    msg = source_commit["msg"]
    if record_origin:
        msg += f" (cherry picked from commit {source_commit['sha']})"
    return make_commit(target_head["sha"], source_commit["patch"], msg)

feat_commit = make_commit("a111111", "+ tax = price * Decimal('0.20')", "fix: rounding in VAT")
release_head = make_commit("r000001", "v1.2 base", "chore: release 1.2")
picked = cherry_pick(release_head, feat_commit, record_origin=True)

print(f"Исходный коммит в feat : {feat_commit['sha']} | {feat_commit['msg']}")
print(f"После cherry-pick -x   : {picked['sha']} | {picked['msg']}")
```
"""

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-174. Конфликты в Git.md"] = r"""📖 Перечитать конспект: Конфликты в Git: анатомия и безопасное разрешение >>
### 1. Ментальная модель: Два редактора исправили одно предложение
Git фантастически умён: если вы изменили строки 10–20 в `api.py`, а ваша коллега изменила строки 80–90 в том же файле, Git молча объединит оба изменения.
**Конфликт слияния (Merge Conflict)** возникает только тогда, когда в двух ветках с момента их расхождения (общего предка **Base**) одна и та же строка была изменена по-разному. Git не имеет права угадывать бизнес-логику и вежливо останавливается, расставляя маркеры в файле.

```text
<<<<<<< HEAD (Ваша текущая ветка — то, где вы находитесь сейчас)
TIMEOUT_SECONDS = 30
||||||| merged common ancestors (при включённом diff3: как было изначально!)
TIMEOUT_SECONDS = 5
=======
TIMEOUT_SECONDS = 15
>>>>>>> feat/fast-retry (Вливаемая ветка)
```

---
### 2. Секретное оружие сеньоров: формат `zdiff3` и отличие `ours` / `theirs`
В обычном режиме Git показывает только 2 варианта (`HEAD` и чужой), но не показывает, **а что там было изначально** (у общего предка). Включите `conflictstyle zdiff3` один раз в жизни — и Git начнёт показывать средний блок `|||||||`, делая разрешение конфликтов в 3 раза понятнее!

```bash
# Включить отображение исходного кода общего предка в конфликтах:
git config --global merge.conflictstyle zdiff3

# Посмотреть, какие файлы сейчас в состоянии конфликта:
git status -s          # Покажет маркер UU (Unmerged, both modified)

# После ручного удаления маркеров <<<<<<<, =======, >>>>>>> в редакторе:
git add app/config.py  # Сообщаем Git, что конфликт в файле решён!
git merge --continue   # (или git rebase --continue)
```

> **Осторожно с инверсией при `rebase`!** Во время `git merge` блок `HEAD` (`--ours`) — это ваша текущая ветка. Но во время **`git rebase`** Git сначала переключается на целевую ветку (`main`) и накатывает ваши коммиты поверх неё по одному! Поэтому при `rebase` в блоке `HEAD` (`--ours`) оказывается `main`, а ваш коммит отображается снизу (`--theirs`).

| Ситуация | Что внутри `<<<<<<< HEAD` (`--ours`) | Что внутри `>>>>>>>` (`--theirs`) | Как отменить операцию и вернуть всё как было |
| :--- | :--- | :--- | :--- |
| **`git merge feat`** (вы в `main`) | Код ветки `main` | Код ветки `feat` | `git merge --abort` |
| **`git rebase main`** (вы в `feat`) | Код ветки `main` (инверсия!) | Ваш коммит из `feat` | `git rebase --abort` |
| **`git cherry-pick X`** | Ваша текущая ветка | Переносимый коммит `X` | `git cherry-pick --abort` |

---
### 3. Главные ошибки при разрешении конфликтов
> **Junior vs Senior**:
> - **Junior**: Пугается маркеров `<<<<<<<`, случайно оставляет строку `=======` в Python-файле (вызывая `SyntaxError` на продакшене) или выбирает «Accept Current Change» не глядя, стирая важную проверку коллеги.
> - **Senior**: Включает `zdiff3`, сверяет оба изменения с общим предком, при необходимости объединяет обе правки, запускает `pytest` перед `git merge --continue` и ставит в CI-пайплайн проверку на отсутствие забытых маркеров `<<<<<<<`.

---
### 4. Живая проверка: парсер конфликтов и алгоритм 3-way merge (`diff3`)
Напишем на Python детектор забытых конфликтных маркеров и алгоритм 3-стороннего слияния строк:

```python
def three_way_merge(base: str, ours: str, theirs: str) -> str:
    if ours == theirs:
        return ours  # Оба сделали одинаковую правку
    if ours == base:
        return theirs  # Меняли только в theirs -> берём theirs без конфликта!
    if theirs == base:
        return ours  # Меняли только в ours -> берём ours без конфликта!
    return f"<<<<<<< HEAD\n{ours}\n||||||| base\n{base}\n=======\n{theirs}\n>>>>>>> branch"

print("Авто-слияние:", three_way_merge(base="timeout = 5", ours="timeout = 5", theirs="timeout = 15"))
conflict_text = three_way_merge(base="timeout = 5", ours="timeout = 30", theirs="timeout = 15")
has_markers = any(m in conflict_text for m in ("<<<<<<<", "=======", ">>>>>>>"))
print(f"Обнаружен конфликт (has_markers={has_markers}):\n{conflict_text}")
```
"""

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-175. Чтение истории в Git_ log, diff, blame.md"] = r"""📖 Перечитать конспект: Чтение истории в Git: log, diff, blame и bisect >>
### 1. Ментальная модель: Детективное расследование по уликам
Хороший бэкенд-разработчик читает историю Git не ради любопытства, а чтобы расследовать баги за 2 минуты вместо 2 часов:
- **`git log`** — бортовой журнал корабля (какие изменения и когда вносились).
- **`git diff`** — рентгеновский снимок отличий между двумя состояниями.
- **`git blame`** — подпись автора и номер задачи напротив каждой конкретной строчки кода.
- **`git bisect`** — бинарный поиск коммита, который сломал тесты, за $\log_2(N)$ шагов.

```text
Поиск бага среди 1024 коммитов (git bisect):
[c1: OK] ............... [c512: OK] ....... [c768: BAD] ... [c1024: BAD]
Шаг 1: середина c512 работает -> баг правее (осталось 512 коммитов)
Шаг 2: середина c768 сломана  -> баг левее  (осталось 256 коммитов)
... Всего за 10 шагов (log2 1024 = 10) найден точный виновник c615!
```

---
### 2. Шпаргалка команд расследования для продакшена
Обычный `git log` выводит простыню текста. Используйте флаги визуализации графа и поиска по содержимому кода (`-S` — так называемый *pickaxe*, «кирка рудокопа»):

```bash
# Компактный граф всех веток и коммитов в одну строчку:
git log --oneline --graph --decorate --all -n 15

# Найти коммит, в котором впервые появилась или была удалена строка " legacy_tax ":
git log -S "legacy_tax" -p

# Посмотреть, кто и в каком коммите написал строки 40..60 файла billing.py (игнорируя пробелы -w):
git blame -w -L 40,60 app/billing.py

# Что я уже добавил в индекс (git add) перед коммитом?
git diff --staged
```

| Инструмент | Команда | На какой вопрос отвечает? |
| :--- | :--- | :--- |
| **Граф истории** | `git log --oneline --graph` | Как разошлись ветки и где сейчас `HEAD` / `origin/main`? |
| **Поиск по коду (`-S`)** | `git log -S "func_name" -p` | В каком коммите удалили или добавили эту функцию? |
| **Инспекция индекса** | `git diff --staged` | Что именно попадёт в коммит, если я сейчас нажму `git commit`? |
| **История строки** | `git blame -w -L 10,25 file.py` | Зачем (в рамках какого PR/тикета) была написана эта странная проверка? |
| **Бинарный поиск** | `git bisect run pytest` | Какой именно коммит из 500 последних сломал наш тест? |

---
### 3. Культура работы с `git blame`
> **Junior vs Senior**:
> - **Junior**: Использует `git blame`, чтобы найти, «на кого свалить вину за баг», или боится трогать непонятную строчку кода, не прочитав описание коммита, в котором она появилась.
> - **Senior**: Использует `git blame -w` (игнорируя автоформатирование Black/Ruff), чтобы по хешу коммита (`git show <sha>`) прочитать инженерный контекст: какой крайний случай чинил автор год назад, прежде чем рефакторить этот участок.

---
### 4. Живая проверка: автоматический `git bisect` за $O(\log N)$ на Python
Смоделируем работу `git bisect run pytest` на истории из 1000 коммитов, где баг закрался на коммите `#642`:

```python
def git_bisect_auto(commits: list[int], is_commit_good) -> tuple[int, int]:
    low, high = 0, len(commits) - 1
    steps = 0
    while low < high:
        steps += 1
        mid = (low + high) // 2
        if is_commit_good(commits[mid]):
            low = mid + 1   # В середине всё хорошо -> баг появился позже
        else:
            high = mid      # В середине уже сломано -> ищем раньше (включая mid)
    return commits[low], steps

history = list(range(1, 1001))  # 1000 коммитов
first_bad, checks = git_bisect_auto(history, is_commit_good=lambda c: c < 642)
print(f"Из {len(history)} коммитов первый сломанный коммит #{first_bad} найден всего за {checks} проверок!")
```
"""

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-176. Жизненный цикл изменений в Git.md"] = r"""📖 Перечитать конспект: Жизненный цикл изменений в Git: 4 зоны данных >>
### 1. Ментальная модель: Фотостудия со сценой (`Staging Area`)
Чтобы никогда не путаться в командах Git, представьте процесс создания коммита как съёмку группового фото в студии:
1. **Working Directory (Рабочая папка)** — гримёрка, где вы свободно редактируете файлы.
2. **Staging Area / Index (Индекс)** — освещённый подиум перед камерой. Команда `git add` приглашает только выбранные файлы (или даже отдельные строчки через `git add -p`) встать на подиум.
3. **Local Repository (`.git`)** — фотоальбом на вашем ноутбуке. Команда `git commit` нажимает кнопку затвора и фотографирует **только тех, кто стоит на подиуме**.
4. **Remote Repository (`origin`)** — облачная галерея (GitHub / GitLab), куда снимки отправляются через `git push`.

```text
[1. Working Dir] ──git add──► [2. Staging Index] ──git commit──► [3. Local .git] ──git push──► [4. Remote]
       ▲                              │                                │
       └──────── git restore ─────────┴────── git reset --soft HEAD~1 ─┘
```

---
### 2. Состояния файла и три режима `git reset`
Новички часто боятся команды `git reset`, хотя она просто двигает указатель ветки назад, а судьба ваших файлов зависит от одного флага:

```bash
# Добавить в индекс не весь файл, а выбрать конкретные куски (hunks) интерактивно:
git add -p app/services.py

# Отменить последний коммит, но ОСТАВИТЬ все изменения на подиуме (в Staging Area):
git reset --soft HEAD~1

# Отменить коммит и убрать файлы с подиума в рабочую папку (по умолчанию):
git reset --mixed HEAD~1

# ОПАСНО: Стереть коммит, очистить подиум и УНИЧТОЖИТЬ правки в рабочей папке:
git reset --hard HEAD~1
```

| Команда | Local Repo (`HEAD`) | Staging Index (Подиум) | Working Directory (Файлы) | Безопасность |
| :--- | :--- | :--- | :--- | :--- |
| `git reset --soft HEAD~1` | Откатывается на 1 шаг | Сохраняет все правки (`staged`) | Не трогает код | 100% безопасно |
| `git reset --mixed HEAD~1` | Откатывается на 1 шаг | Очищает подиум | Сохраняет код в файлах (`modified`) | 100% безопасно |
| `git reset --hard HEAD~1` | Откатывается на 1 шаг | Очищает подиум | **Удаляет незакоммиченный код!** | Опасно (потеря правок) |
| `git revert HEAD` | Создаёт **новый** анти-коммит | Не трогает | Отменяет правки чисто | Идеально для `main` |

---
### 3. `git reset` против `git revert` в общей ветке
> **Junior vs Senior**:
> - **Junior**: Запушил неудачный коммит в общую ветку `main`, делает `git reset --hard HEAD~1` и форс-пушит, ломая историю всей команде. Или делает `git add .`, случайно захватывая в коммит отладочные `print()` и временные файлы.
> - **Senior**: Перед коммитом собирает атомарные изменения через `git add -p`, а если ошибка уже попала в публичную ветку `main` — отменяет её через **`git revert <sha>`**, который создаёт новый зеркальный коммит, не переписывая историю.

---
### 4. Живая проверка: машина состояний 4 зон Git на Python
Проследим на Python, как файл проходит путь от `Untracked` до `Committed` и что делает `reset --soft`:

```python
class GitZones:
    def __init__(self) -> None:
        self.working = {"auth.py": "def login(): return True"}
        self.staging: dict[str, str] = {}
        self.commits: list[dict[str, str]] = []

    def add(self, filename: str) -> None:
        self.staging[filename] = self.working[filename]

    def commit(self) -> None:
        self.commits.append(self.staging.copy())
        self.staging.clear()

    def reset_soft_head_1(self) -> None:
        last = self.commits.pop()
        self.staging.update(last)

zones = GitZones()
zones.add("auth.py")
zones.commit()
print(f"После commit        : commits={len(zones.commits)}, staging={list(zones.staging)}")
zones.reset_soft_head_1()
print(f"После reset --soft  : commits={len(zones.commits)}, staging={list(zones.staging)} (код сохранён в индексе!)")
```
"""

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-177. Стратегии ветвления_ Gitflow и.md"] = r"""📖 Перечитать конспект: Стратегии ветвления: Gitflow и Trunk-Based Development >>
### 1. Ментальная модель: Грузовой корабль по расписанию или Скоростной конвейер
Как команде из 10–50 разработчиков писать код в одном репозитории и не мешать друг другу? В индустрии есть два главных подхода:
1. **Gitflow** — как грузовой паром, который отплывает строго раз в месяц. Есть отдельные палубы: `develop` (стройка), `feature/*` (каюты фич), `release/*` (предрелизная заморозка), `main` (только готовые версии с тегами `v1.2.0`) и `hotfix/*` (скорая помощь).
2. **Trunk-Based Development (TBD) / GitHub Flow** — скоростной конвейер микросервисов. Есть только одна вечная ветка `main` (ствол — *trunk*), от которой живут короткие ветки на 1–2 дня. Как только Pull Request прошёл CI-тесты, он сразу вливается в `main` и едет на прод.

```text
Gitflow (коробочный софт, мобильные приложения):
main    ───────●───────────────────────────● (v1.0) ◄── hotfix/*
release         \                 ┌───────/
develop ────●────●────●───────────●───────●
feature      \──────/ (живут неделями)

Trunk-Based / GitHub Flow (современные веб-сервисы и SaaS):
main    ────●──────●──────●──────●──────●──► (деплой 10 раз в день)
             \────/ \────/  (короткие PR по 1-2 дня + Feature Flags)
```

---
### 2. Сравнение стратегий и роль Feature Flags
Как в Trunk-Based Development вливать код в `main` каждый день, если большая фича (например, новая корзина оплаты) пишется две недели? Ответ — **Feature Flags (фича-флаги)**: новый код вливается в `main` маленькими частями, но скрыт за условием `if settings.ENABLE_NEW_CART:`, поэтому пользователи его пока не видят, а админы уже могут тестировать!

```bash
# Цикл работы в GitHub Flow / Trunk-Based Development:
git switch main && git pull origin main
git switch -c feat/214-stripe-webhook      # Короткая ветка на 1 задачу (< 200 строк)
# ... пишем код + тесты ...
git push -u origin feat/214-stripe-webhook # Открываем PR -> Авто-тесты CI -> Merge в main!
```

| Характеристика | Gitflow | GitHub Flow / Trunk-Based (TBD) |
| :--- | :--- | :--- |
| **Долгоживущие ветки** | `main`, `develop`, `release/*` | Только одна — `main` (`trunk`) |
| **Время жизни feature-ветки** | От нескольких дней до нескольких недель | От нескольких часов до 1–2 дней |
| **Риск «Merge Hell» (конфликтов)** | Высокий (ветки сильно расходятся) | Минимальный (код интегрируется ежедневно) |
| **Незавершённые фичи в `main`** | Не попадают до готовности всей ветки | Скрываются за **Feature Flags** |
| **Кому идеально подходит** | Мобилки (App Store ревью), банковский On-Premise | Веб-бэкенд, микросервисы, SaaS с CI/CD |

---
### 3. Как победить «Merge Hell» (Ад слияния)
> **Junior vs Senior**:
> - **Junior**: Пилит задачу в своей ветке 3 недели в полной изоляции, меняя 60 файлов. При попытке влить PR в `main` получает 140 конфликтов и неделю чинит сломанную логику.
> - **Senior**: Дробит крупную фичу на 5 маленьких PR по 150–250 строк, закрывает новую точку входа фича-флагом и вливает код в `main` каждый день.

---
### 4. Живая проверка: роутинг через Feature Flag в Trunk-Based Development
Посмотрим, как в Python-бэкенде безопасно деплоить новую платёжную логику в `main` с помощью Feature Flag и процентного раскатывания (Canary Rollout):

```python
from dataclasses import dataclass

@dataclass
class FeatureFlag:
    name: str
    enabled: bool
    rollout_percent: int = 0  # 0..100% пользователей

    def is_active_for(self, user_id: int) -> bool:
        if not self.enabled:
            return False
        return (user_id % 100) < self.rollout_percent

new_checkout_flag = FeatureFlag(name="new_stripe_checkout", enabled=True, rollout_percent=20)

for uid in (10, 25, 115, 180):
    engine = "v2_stripe (NEW)" if new_checkout_flag.is_active_for(uid) else "v1_legacy (SAFE)"
    print(f"User #{uid:<3} -> обработчик оплаты: {engine}")
```
"""

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-178. Структура репозитория.md"] = r"""📖 Перечитать конспект: Структура репозитория: анатомия Python-проекта >>
### 1. Ментальная модель: Профессиональная кухня с подписанными полками
Когда вы приходите в новый ресторан (или когда тимлид открывает ваш тестовый проект на собеседовании), первые 30 секунд решают всё. Если специи свалены в одну коробку с инструментами и чеками (`script1.py`, `test_final2.py`, `db_copy.py` прямо в корне), проект выглядит любительским.
Промышленный Python-репозиторий следует единому стандарту: конфигурация сборки лежит в **`pyproject.toml`**, исходный код изолирован в пакете **`src/`** (или `app/`), тесты — в **`tests/`**, а инструкция по запуску за 60 секунд — в **`README.md`**.

```text
my-service/
├── pyproject.toml        ◄── Единый центр зависимостей, ruff, pytest и mypy (PEP 621)
├── README.md             ◄── Как запустить проект за 3 команды + архитектура
├── .env.example          ◄── Шаблон переменных окружения (БЕЗ реальных паролей!)
├── .gitignore            ◄── Защита от мусора (__pycache__, .venv, .env)
├── Dockerfile            ◄── Инструкция сборки контейнера
├── src/                  ◄── (src-layout) Защищает от случайного импорта из корня
│   └── billing/
│       ├── __init__.py
│       ├── api.py
│       ├── services.py
│       └── repositories.py
└── tests/                ◄── Зеркальная структура тестов
    ├── unit/
    └── integration/
```

---
### 2. Почему `pyproject.toml` заменил 5 старых конфигов, а `src/` спасает тесты?
Раньше в корне Python-проекта валялись `requirements.txt`, `setup.py`, `setup.cfg`, `pytest.ini`, `.flake8`. Начиная с PEP 518 / PEP 621 всё это объединено в один стандартный файл **`pyproject.toml`**.

```toml
# Пример современного pyproject.toml:
[project]
name = "billing-service"
version = "0.2.0"
requires-python = ">=3.12"
dependencies = ["fastapi>=0.115.0", "pydantic>=2.9.0", "sqlalchemy>=2.0.35"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

| Элемент репозитория | Зачем он нужен? | Анти-паттерн (как делать НЕ надо) |
| :--- | :--- | :--- |
| **`pyproject.toml`** | Единый стандарт зависимостей и настроек линтеров/тестов | Держать разрозненные `setup.py`, `.flake8`, `pytest.ini` |
| **`src/<pkg>/`** | Гарантирует, что тесты проверяют установленный пакет | Сваливать десятки `.py`-файлов прямо в корень репозитория |
| **`.env.example`** | Документирует нужные переменные (`DB_URL=`, `REDIS_URL=`) | Коммитить настоящий `.env` с боевыми ключами AWS/БД |
| **`README.md`** | Даёт новому разработчику запуск проекта за 2 минуты | Пустой `README.md` или отсутствие секции «Quick Start» |

---
### 3. Как оценивают ваш репозиторий на техническом ревью
> **Junior vs Senior**:
> - **Junior**: Присылает ссылку на GitHub, где в корне лежат 15 файлов `.py`, закоммичена папка `.venv/` на 4000 файлов, нет `README.md`, а зависимости не зафиксированы.
> - **Senior**: Оформляет чистый репозиторий с `pyproject.toml`, `Makefile` / `docker compose up`, `.env.example`, бейджем CI-тестов и понятным `README.md` (описание архитектуры, стек, команды запуска и тестов).

---
### 4. Живая проверка: автоматический аудитор структуры репозитория
Напишем на Python линтер структуры проекта, проверяющий соблюдение стандартов индустрии:

```python
def audit_repo_structure(files: set[str]) -> list[str]:
    issues: list[str] = []
    required = {"pyproject.toml", "README.md", ".gitignore", ".env.example"}
    for req in sorted(required - files):
        issues.append(f"Отсутствует обязательный файл: {req}")
    if ".env" in files:
        issues.append("КРИТИЧНО: В репозиторий закоммичен секретный файл .env!")
    if any(f.startswith((".venv/", "__pycache__/")) for f in files):
        issues.append("МУСОР: В индексе найдены артефакты окружения (.venv / __pycache__)")
    if not any(f.startswith(("src/", "app/")) for f in files):
        issues.append("АРХИТЕКТУРА: Код не выделен в пакет src/ или app/")
    return issues or ["OK: Структура репозитория соответствует стандарту Senior!"]

good_repo = {"pyproject.toml", "README.md", ".gitignore", ".env.example", "src/billing/api.py", "tests/test_api.py"}
print("Аудит эталонного репозитория:", audit_repo_structure(good_repo)[0])
```
"""

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-179. Pull Request.md"] = r"""📖 Перечитать конспект: Pull Request и культура Code Review >>
### 1. Ментальная модель: Предполётный осмотр самолёта двумя пилотами
Даже самый опытный командир воздушного судна никогда не взлетает в одиночку: второй пилот проверяет чек-лист, приборы и закрылки.
**Pull Request (PR)** в GitHub (или **Merge Request (MR)** в GitLab) — это не «экзамен у строгого начальника», а инженерный диалог: вы предлагаете влить изменения из вашей ветки в `main`, автоматический CI-конвейер проверяет тесты и линтеры, а коллеги проводят **Code Review**, помогая заметить скрытые баги, утечки памяти или нарушения архитектуры до того, как код попадёт на продакшен.

```text
[Ваша ветка feat/api] ──► Открытие PR ──► [Робот CI: ruff + mypy + pytest]
                                                    │ (зелёная галочка ✅)
                                                    ▼
[Слияние в main 🚀]  ◄── Approve 👍 ◄── [Code Review коллег: архитектура и краевые случаи]
```

---
### 2. Анатомия идеального Pull Request и парадокс размера
Исследования инженерных команд показывают: если в PR **200 строк кода**, ревьюер внимательно находит 70–80% потенциальных ошибок за 15 минут. Если в PR **1500 строк кода**, внимание человека притупляется, и PR либо висит неделю без ревью, либо получает формальный `LGTM (Looks Good To Me)` за 1 минуту, пропуская баги на прод.

```markdown
## Что сделано (Summary)
Добавлен идемпотентный обработчик вебхуков Stripe (`POST /webhooks/stripe`).

## Почему так (Context & Architecture)
- Использована таблица `processed_events` с `UNIQUE(event_id)` для защиты от двойного списания.
- Тяжёлая генерация PDF-чека вынесена в фоновую задачу Celery.

## Как проверено (Test Plan)
- [x] Добавлены unit-тесты на повторную отправку одного и того же `event_id` (`pytest tests/test_stripe.py`).
```

| Критерий | Слабый PR (тяжело ревьюить) | Эталонный PR (ревью за 10 минут) |
| :--- | :--- | :--- |
| **Объём изменений** | 1200+ строк, 35 файлов | **До 200–400 строк**, 1 логическая задача |
| **Заголовок и описание** | `fix` / пустое описание | `feat(billing): add idempotent Stripe webhook` + контекст |
| **Смешивание задач** | Новая фича + рефакторинг полпроекта + переименование папок | Строго 1 атомарное изменение (рефакторинг — в отдельном PR) |
| **Тон комментариев (Review)** | Токсичный («Кто это вообще писал?!») | Конструктивный с префиксами: `[blocker]`, `[nit]`, `[question]` |

---
### 3. Этикет автора и ревьюера (Conventional Comments)
Чтобы в команде не возникало споров из-за вкусовщины, профессионалы помечают важность комментариев:
- **`[blocker]`** — критический баг, SQL-инъекция или потеря данных (блокирует вливание).
- **`[suggestion]`** — предложение по улучшению читаемости или производительности.
- **`[nit]` (nitpick)** — мелочь (например, опечатка в имени переменной), не блокирующая Approve.

> **Junior vs Senior**:
> - **Junior**: Обижается на комментарии в PR, воспринимая критику кода как критику своей личности, а чужие PR смотрит только на предмет пробелов и кавычек (эту работу должен делать линтер `ruff` в CI!).
> - **Senior**: Перед отправкой PR сам просматривает вкладку `Files changed` глазами ревьюера (Self-Review), а при ревью чужого кода ищет архитектурные проблемы: гонки данных (`race conditions`), $N+1$ запросы к БД, отсутствие таймаутов и краевые случаи.

---
### 4. Живая проверка: автоматический скоринг готовности PR к ревью
Напишем на Python анализатор метрик Pull Request, оценивающий его удобство для Code Review:

```python
def evaluate_pr_quality(lines_changed: int, has_tests: bool, has_description: bool, ci_passed: bool) -> dict:
    if not ci_passed:
        return {"status": "BLOCKED", "reason": "Упали авто-тесты CI — сначала почините пайплайн"}
    score = 100
    warnings: list[str] = []
    if lines_changed > 400:
        score -= 40
        warnings.append(f"PR слишком велик ({lines_changed} строк > 400): разбейте на атомарные части")
    if not has_tests:
        score -= 35
        warnings.append("Нет новых тестов для изменённой бизнес-логики")
    if not has_description:
        score -= 25
        warnings.append("Отсутствует описание Контекста и Test Plan")
    return {"status": "READY" if score >= 75 else "NEEDS_WORK", "score": score, "warnings": warnings}

print("Маленький PR с тестами:", evaluate_pr_quality(180, True, True, True))
print("Огромный PR без тестов:", evaluate_pr_quality(950, False, True, True))
```
"""

NOTES[r"Юнит 7.1 · Git\📚 Конспекты\К-180. .gitignore.md"] = r"""📖 Перечитать конспект: .gitignore: гигиена репозитория и защита секретов >>
### 1. Ментальная модель: Фейсконтроль на входе в репозиторий
При работе Python-проекта на диске постоянно рождаются сотни служебных и секретных файлов: скомпилированный байткод `__pycache__/*.pyc`, виртуальное окружение `.venv/` (десятки мегабайт чужих библиотек), кэш тестов `.pytest_cache/` и файл `.env` с паролями от продакшен-базы.
Файл **`.gitignore`** — это список правил для охранника на входе в индекс Git (`git add`): всё, что совпадает с шаблонами в `.gitignore`, Git просто не замечает.

```text
Рабочая папка проекта:
 ├── src/app.py          ──► [Охранник .gitignore] ──► ✅ Пропустить в Git!
 ├── .env (пароли БД!)   ──► [Правило: .env]       ──► 🛑 СТОП! Игнорировать!
 └── __pycache__/a.pyc   ──► [Правило: __pycache__/]─► 🛑 СТОП! Игнорировать!
```

---
### 2. Синтаксис шаблонов (Globbing) и спасение уже закоммиченного файла
Главная ловушка `.gitignore`, на которой попадаются 90% новичков: **`.gitignore` действует только на неотслеживаемые (`untracked`) файлы!** Если вы сначала случайно сделали `git add .env && git commit`, а потом дописали `.env` в `.gitignore`, Git **продолжит отслеживать `.env`** и отправлять ваши пароли на сервер!
Чтобы отучить Git следить за файлом, но **не удалять его с вашего диска**, нужна команда `git rm --cached`:

```bash
# Удалить файл .env из индекса Git, но СОХРАНИТЬ его на жёстком диске ноутбука:
git rm --cached .env
git commit -m "chore: stop tracking .env file"

# Проверить, какое именно правило и в какой строке .gitignore блокирует нужный файл:
git check-ignore -v logs/keep.log
```

| Шаблон в `.gitignore` | Что именно он игнорирует? | Пример совпадения |
| :--- | :--- | :--- |
| `__pycache__/` | Папку `__pycache__` на любом уровне вложенности | `src/api/__pycache__/` |
| `*.py[cod]` | Все файлы с расширениями `.pyc`, `.pyo`, `.pyd` | `models.cpython-313.pyc` |
| `/build/` | Папку `build` **только в самом корне** репозитория | `/build/` (но не `src/build/`) |
| `.env*` + `!.env.example` | Все файлы `.env*`, **кроме** шаблона `.env.example` (`!` — исключение) | Игнорирует `.env.local`, но пускает `.env.example` |

---
### 3. Что делать, если секретный ключ уже улетел в `git push`?
> **Junior vs Senior**:
> - **Junior**: Запушил файл `.env` с ключом от AWS/Telegram-бота на GitHub, заметил это, удалил файл следующим коммитом и успокоился. Но в истории коммитов (`git log -p`) ключ остался навсегда, и боты-сканеры украдут его через 30 секунд!
> - **Senior**: Знает золотое правило безопасности: **если секрет побывал в удалённом репозитории хотя бы 1 секунду — он скомпрометирован**. Сеньор немедленно **отзывает и перевыпускает (rotate)** ключ в панели провайдера, а историю чистит через `git filter-repo`.

---
### 4. Живая проверка: движок правил `.gitignore` с поддержкой отрицания `!`
Реализуем на Python парсер правил `.gitignore` (включая исключающее правило `!.env.example`):

```python
import fnmatch

def is_git_ignored(filepath: str, rules: list[str]) -> bool:
    ignored = False
    filename = filepath.split("/")[-1]
    for raw_rule in rules:
        rule = raw_rule.strip()
        if not rule or rule.startswith("#"):
            continue
        negate = rule.startswith("!")
        pattern = rule[1:] if negate else rule
        if pattern.endswith("/"):
            matched = f"{pattern[:-1]}/" in f"{filepath}/"
        else:
            matched = fnmatch.fnmatch(filepath, pattern) or fnmatch.fnmatch(filename, pattern)
        if matched:
            ignored = not negate
    return ignored

gitignore_rules = ["__pycache__/", "*.pyc", ".venv/", ".env*", "!.env.example"]
for candidate in ["src/main.py", "src/__pycache__/main.pyc", ".env", ".env.local", ".env.example"]:
    status = "IGNORED 🛑" if is_git_ignored(candidate, gitignore_rules) else "TRACKED ✅"
    print(f"{candidate:<26} -> {status}")
```
"""

# ==============================================================================
# ЮНИТ 7.2 · DOCKER ОСНОВЫ (К-181 .. К-186)
# ==============================================================================

NOTES[r"Юнит 7.2 · Docker основы\📚 Конспекты\К-181. Docker_ Image и Container.md"] = r"""📖 Перечитать конспект: Docker: Image (Образ) и Container (Контейнер) >>
### 1. Ментальная модель: Замороженный полуфабрикат (`Image`) и Горячее блюдо (`Container`)
Проблема «У меня на ноутбуке всё работало, а на сервере упало!» преследовала программистов десятилетиями из-за разных версий Python, библиотек C (`libpq`) и ОС. Docker решил её навсегда, разделив приложение на две сущности (прямо как **Класс** и **Объект** в ООП):
- **Docker Image (Образ)** — это неизменяемый (*read-only*) многослойный слепок: внутри него уже упакованы минимальный Linux, нужная версия Python 3.13, все библиотеки и ваш код. Это **Чертёж / Класс**.
- **Docker Container (Контейнер)** — это запущенный в памяти живой процесс, созданный из образа, к которому сверху добавили тонкий пишущий слой (**Writable Layer**). Это **Экземпляр / Объект**. Из одного образа можно за секунду запустить 10 изолированных контейнеров!

```text
┌────────────────────────────────────────────────────────┐
│ Тонкий пишущий слой (Container Layer — Read/Write)     │ ◄── Живой Контейнер #1
├────────────────────────────────────────────────────────┤
│ Слой 4: COPY ./src /app/src         (Read-Only, 50 KB) │ ┐
│ Слой 3: RUN pip install -r req.txt  (Read-Only, 45 MB) │ │ Неизменяемый
│ Слой 2: Python 3.13 binaries        (Read-Only, 40 MB) │ │ Docker Image
│ Слой 1: Debian Bookworm Slim        (Read-Only, 28 MB) │ ┘ (общий для всех!)
└────────────────────────────────────────────────────────┘
```

---
### 2. Как работает слоёный пирог UnionFS и Copy-on-Write (CoW)
Почему 20 запущенных контейнеров из образа весом 200 МБ занимают в памяти и на диске не $20 \times 200 = 4000\text{ МБ}$, а всё те же ~200 МБ?
Потому что все слои образа открыты **только для чтения** и делятся между всеми контейнерами одновременно! А механизм **Copy-on-Write (копирование при записи)** копирует файл из нижнего слоя в верхний (контейнерный) слой только в тот момент, когда контейнер пытается этот файл изменить.

| Характеристика | Docker Image (Образ) | Docker Container (Контейнер) | Аналогия в Python ООП |
| :--- | :--- | :--- | :--- |
| **Изменяемость** | **Immutable** (Read-Only навсегда) | Имеет верхний **Read-Write** слой | `class UserService:` vs `svc = UserService()` |
| **Где живёт** | На диске и в реестре (Docker Hub) | В оперативной памяти как процесс ОС | Исходный файл `.py` vs объект в RAM |
| **Идентификатор** | SHA-256 дайджест + тег (`api:1.2.0`) | `Container ID` + имя (`billing-web-1`) | Имя класса vs `id(obj)` |
| **При удалении** | Удаляется шаблон с диска (`docker rmi`) | Стирается только верхний R/W слой (`docker rm`) | Удаление класса vs сборка мусора `del obj` |

---
### 3. Ловушка эфемерности контейнера
> **Junior vs Senior**:
> - **Junior**: Заходит внутрь работающего контейнера (`docker exec -it app bash`), правит код через `nano` или сохраняет загруженные пользователями аватарки прямо в папку `/app/media` внутри контейнера. При первом же перезапуске (`docker compose up -d --build`) контейнер пересоздаётся, и **все данные бесследно исчезают**.
> - **Senior**: Относится к контейнерам как к **эфемерным (одноразовым)** процессам: код меняет только через пересборку Image в CI/CD, а любые постоянные данные выносит в **Docker Volumes**, внешнюю БД или S3-хранилище.

---
### 4. Живая проверка: симуляция файловой системы Copy-on-Write (OverlayFS)
Убедимся на Python, как 2 разных контейнера разделяют общий Read-Only слой образа, не мешая друг другу при записи:

```python
class DockerImage:
    def __init__(self, layers: list[dict[str, str]]) -> None:
        self.readonly_layers = layers  # Слои снизу вверх

class DockerContainer:
    def __init__(self, name: str, image: DockerImage) -> None:
        self.name = name
        self.image = image
        self.rw_layer: dict[str, str] = {}  # Собственный пишущий слой

    def read(self, path: str) -> str:
        if path in self.rw_layer:
            return f"{self.rw_layer[path]} (из R/W слоя {self.name})"
        for layer in reversed(self.image.readonly_layers):
            if path in layer:
                return f"{layer[path]} (из общего R/O образа)"
        raise FileNotFoundError(path)

    def write_cow(self, path: str, content: str) -> None:
        self.rw_layer[path] = content  # Copy-on-Write: нижние слои не трогаем!

img = DockerImage([{"/etc/os": "debian"}, {"/app/config.py": "DEBUG=False"}])
c1, c2 = DockerContainer("web-1", img), DockerContainer("web-2", img)
c1.write_cow("/app/config.py", "DEBUG=True")

print("web-1 читает /app/config.py:", c1.read("/app/config.py"))
print("web-2 читает /app/config.py:", c2.read("/app/config.py"))
```
"""

NOTES[r"Юнит 7.2 · Docker основы\📚 Конспекты\К-182. Dockerfile_ как устроена сборка образа.md"] = r"""📖 Перечитать конспект: Dockerfile: как устроена сборка образа и кэш слоёв >>
### 1. Ментальная модель: Конвейер сборки с памятью на каждом этаже
**`Dockerfile`** — это рецепт сборки вашего образа сверху вниз. Каждая инструкция (`FROM`, `WORKDIR`, `COPY`, `RUN`) создаёт новый неизменяемый слой.
Чтобы не скачивать библиотеки по 3 минуты при каждой правке одной строчки кода, Docker использует **Layer Caching (кэширование слоёв)**. Но у кэша есть железное правило: **если изменился слой №3, то кэш для слоёв №4, №5 и ниже автоматически сбрасывается (инвалидируется)!** Поэтому порядок строк в `Dockerfile` определяет, будет ли ваш образ собираться за **1 секунду** или за **3 минуты**.

```text
❌ ПЛОХОЙ порядок (сборка 120 сек каждый раз):   ✅ ПРАВИЛЬНЫЙ порядок (сборка 1 сек!):
1. FROM python:3.13-slim                        1. FROM python:3.13-slim          (КЭШ ✅)
2. COPY . /app  ◄── изменился 1 файл кода!      2. COPY requirements.txt /app/    (КЭШ ✅)
3. RUN pip install -r req.txt (КАЧАЕТ ЗАНОВО!)  3. RUN pip install -r req.txt     (КЭШ ✅)
                                                4. COPY ./src /app/src            (Только этот слой!)
```

---
### 2. Эталонный `Dockerfile` для Python-бэкенда и разница `RUN` vs `CMD` vs `ENTRYPOINT`
Посмотрим на правильный `Dockerfile`, в котором зависимости отделены от кода, отключена буферизация логов Python (`PYTHONUNBUFFERED=1`), а процесс запускается от непривилегированного пользователя (`appuser`), а не от `root`:

```dockerfile
FROM python:3.13-slim

# 1. Python пишет логи в stdout мгновенно (без буфера) и не создаёт .pyc файлы:
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 2. Сначала копируем ТОЛЬКО файл зависимостей, чтобы закэшировать слой pip install:
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Копируем исходный код и запускаем от безопасного пользователя (не root!):
COPY ./src ./src
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

| Инструкция | Когда выполняется? | Назначение | Важная деталь |
| :--- | :--- | :--- | :--- |
| **`RUN`** | Во время **сборки** (`docker build`) | Установка пакетов, компиляция (`pip install`) | Запекается в слой образа навсегда |
| **`ENV`** | Во время сборки и в рантайме | Установка переменных окружения (`PYTHONUNBUFFERED=1`) | Доступна внутри Python через `os.environ` |
| **`ENTRYPOINT`** | При **старте** контейнера (`docker run`) | Неизменяемый бинарник контейнера | Сложно случайно перезаписать аргументами |
| **`CMD`** | При **старте** контейнера (`docker run`) | Команда по умолчанию (или аргументы к `ENTRYPOINT`) | Всегда пишите в **Exec-форме**: `["uvicorn", ...]`! |

---
### 3. Почему `CMD ["uvicorn", ...]` в квадратных скобках спасает от `SIGKILL`?
> **Junior vs Senior**:
> - **Junior**: Пишет `CMD uvicorn main:app` без скобок (Shell-форма) и запускает контейнер от `root`. В Shell-форме `PID 1` внутри контейнера получает оболочка `/bin/sh -c`, которая **не передаёт сигнал остановки `SIGTERM`** вашему Python-процессу! В итоге при деплое Docker ждёт 10 секунд и грубо убивает сервер через `SIGKILL`, обрывая активные HTTP-запросы клиентов.
> - **Senior**: Всегда использует **Exec-форму** `CMD ["uvicorn", "src.main:app"]` (тогда Python сам становится `PID 1` и плавно завершает текущие запросы при остановке — *Graceful Shutdown*), ставит `--no-cache-dir` у `pip` и переключается на `USER appuser`.

---
### 4. Живая проверка: симулятор кэширования слоёв `docker build`
Посмотрим на Python, как перестановка `COPY requirements.txt` выше `COPY ./src` экономит 99% времени сборки при изменении кода:

```python
def simulate_docker_build(steps: list[tuple[str, str, int]], prev_cache: list[str]) -> tuple[int, list[str]]:
    total_time_sec = 0
    new_cache: list[str] = []
    cache_valid = True
    for name, content_hash, duration_sec in steps:
        fingerprint = f"{name}:{content_hash}"
        if cache_valid and len(prev_cache) > len(new_cache) and prev_cache[len(new_cache)] == fingerprint:
            status = "CACHED (0s)"
        else:
            cache_valid = False  # Каскадная инвалидация всех следующих слоёв!
            total_time_sec += duration_sec
            status = f"BUILT  ({duration_sec}s)"
        new_cache.append(fingerprint)
        print(f"  {name:<26} -> {status}")
    return total_time_sec, new_cache

first_run_steps = [("FROM py3.13-slim", "v1", 5), ("COPY requirements.txt", "req_v1", 1), ("RUN pip install", "req_v1", 45), ("COPY ./src", "code_v1", 1)]
print("1-я сборка (холодная):")
_, cache = simulate_docker_build(first_run_steps, [])

print("2-я сборка (изменился только код в ./src -> code_v2):")
second_run_steps = [("FROM py3.13-slim", "v1", 5), ("COPY requirements.txt", "req_v1", 1), ("RUN pip install", "req_v1", 45), ("COPY ./src", "code_v2", 1)]
t, _ = simulate_docker_build(second_run_steps, cache)
print(f"Итого время пересборки: {t} сек вместо 52 сек!")
```
"""

NOTES[r"Юнит 7.2 · Docker основы\📚 Конспекты\К-183. Docker Compose.md"] = r"""📖 Перечитать конспект: Docker Compose: оркестрация многоконтейнерного приложения >>
### 1. Ментальная модель: Партитура дирижёра для всего оркестра
В реальной жизни ваш Python-бэкенд не работает в вакууме: рядом с ним должны крутиться база данных PostgreSQL, кэш Redis, воркер Celery и обратный прокси Nginx. Запускать каждый из них вручную длинными командами `docker run` с десятками флагов и связывать их по сети — настоящее мучение.
**`Docker Compose`** — это дирижёрская партитура (`compose.yaml`), где вы один раз декларативно описываете все сервисы, их сети и тома данных, а затем поднимаете всю инфраструктуру одной командой **`docker compose up -d`**!

```text
docker compose up -d (создаёт единую виртуальную сеть app_default):
┌──────────────────────────────────────────────────────────────────────┐
│  [api: FastAPI :8000] ──по имени сервиса "db:5432"──► [db: Postgres] │
│           │                                                  │       │
│  по имени "redis:6379"                                [Volume: pgdata]
│           ▼                                                          │
│  [redis: Redis 7] ◄─────── [worker: Celery]                          │
└──────────────────────────────────────────────────────────────────────┘
```

---
### 2. Современный `compose.yaml` и ловушка `depends_on`
Главная ошибка новичков в `compose.yaml`: они пишут простой `depends_on: [db]` и думают, что Docker подождёт, пока PostgreSQL полностью загрузится и будет готов принимать SQL-коннекты.
**Нет!** Обычный `depends_on` ждёт только старта контейнера (10 миллисекунд), а сама СУБД внутри инициализируется ещё 2–3 секунды. Чтобы FastAPI не падал на старте с `ConnectionRefusedError`, используйте **`healthcheck` + `condition: service_healthy`**:

```yaml
# Современный compose.yaml (поле version: '3.8' устарело и больше не нужно!)
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: shop
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d shop"]
      interval: 3s
      timeout: 3s
      retries: 5

  api:
    build: .
    ports:
      - "8000:8000"  # <Порт на вашем ноутбуке>:<Порт внутри контейнера>
    environment:
      DATABASE_URL: postgresql+asyncpg://app:secret@db:5432/shop
    depends_on:
      db:
        condition: service_healthy  # Ждём реальной готовности Postgres!

volumes:
  pgdata:
```

| Секция `compose.yaml` | Что делает? | Как обращаться из Python-кода? |
| :--- | :--- | :--- |
| **`services:`** | Описывает контейнеры (`api`, `db`, `redis`) | Имя сервиса = **DNS-хост** внутри сети (`host="db"`, а не `localhost`!) |
| **`ports: ["8000:8000"]`** | Пробрасывает порт наружу на хост-машину | Нужен только для входа снаружи; внутри сети сервисы видят все порты друг друга |
| **`volumes:`** | Сохраняет файлы БД при пересоздании контейнеров | Именованный том `pgdata` переживает `docker compose down` |
| **`condition: service_healthy`** | Запускает `api` только после успеха `pg_isready` | Избавляет от падений бэкенда при холодном старте |

---
### 3. Почему внутри контейнера `api` нельзя подключаться к БД по `localhost:5432`?
> **Junior vs Senior**:
> - **Junior**: Прописывает в контейнере `api` строку подключения `postgresql://...@localhost:5432/shop` и получает `Connection refused`. Почему? Потому что у каждого контейнера свой собственный `localhost`! Внутри контейнера `api` на `localhost:5432` никого нет — Postgres живёт в соседнем контейнере `db`.
> - **Senior**: Внутри Docker-сети всегда обращается к соседним сервисам по их **имени в `compose.yaml`** (`@db:5432`, `@redis:6379`), закрывает порт БД от внешнего мира в продакшене и настраивает `healthcheck`.

---
### 4. Живая проверка: топологическая сортировка старта сервисов с `service_healthy`
Проверим на Python, в каком порядке Docker Compose запускает сервисы и почему `api` ждёт сигнала `HEALTHY` от `db`:

```python
def resolve_startup_order(services: dict[str, list[tuple[str, str]]]) -> list[str]:
    started: list[str] = []
    while len(started) < len(services):
        for svc, deps in services.items():
            if svc not in started and all(dep in started for dep, _ in deps):
                wait_info = ", ".join(f"{d}({cond})" for d, cond in deps) or "нет зависимостей"
                started.append(svc)
                print(f"Шаг {len(started)}: старт '{svc:<6}' [ждал: {wait_info}]")
    return started

compose_graph = {
    "db": [],
    "redis": [],
    "api": [("db", "service_healthy"), ("redis", "service_started")],
    "nginx": [("api", "service_started")],
}
order = resolve_startup_order(compose_graph)
print("Итоговая цепочка запуска:", " -> ".join(order))
```
"""

NOTES[r"Юнит 7.2 · Docker основы\📚 Конспекты\К-184. Основные команды Docker.md"] = r"""📖 Перечитать конспект: Основные команды Docker CLI: от запуска до отладки >>
### 1. Ментальная модель: Пульт управления жизненным циклом контейнера
Контейнер — это обычный изолированный процесс Linux. У него есть чёткий жизненный цикл, управляемый командами Docker CLI:

```text
[Docker Image] ──docker run -d──► [Running 🟢] ──docker stop (SIGTERM)──► [Exited 🔴]
                                     │   ▲                                    │
                                     │   └────────── docker start ────────────┘
                                     ├──► docker logs -f  (чтение stdout/stderr)
                                     └──► docker exec -it (открыть терминал внутри)
```

---
### 2. Главные команды ежедневной работы бэкендера
В современном Docker CLI рекомендуется использовать сгруппированный синтаксис (`docker container ls`, `docker image ls`) наряду с классическими короткими командами:

```bash
# 1. Собрать образ из текущей папки (.) и дать ему имя и тег:
docker build -t billing-api:1.0.0 .

# 2. Запустить контейнер в фоне (-d), пробросить порт (-p) и удалить после остановки (--rm):
docker run -d --rm --name billing-web -p 8000:8000 --env-file .env billing-api:1.0.0

# 3. Посмотреть список работающих контейнеров (и всех остановленных с флагом -a):
docker ps
docker ps -a

# 4. Читать живой поток логов контейнера (последние 100 строк + подписка -f):
docker logs --tail 100 -f billing-web

# 5. Зайти внутрь работающего контейнера интерактивно для диагностики:
docker exec -it billing-web sh

# 6. Очистить диск от всех остановленных контейнеров и «висячих» (<none>) образов:
docker system prune -f
```

| Команда | Ключевые флаги | Что делает? | Частая ошибка |
| :--- | :--- | :--- | :--- |
| **`docker run`** | `-d` (фон), `-p 8000:80`, `--rm` | Создаёт **новый** контейнер из образа и запускает его | Путать с `docker start` (который будит старый контейнер) |
| **`docker exec`** | `-i` (stdin), `-t` (tty) | Запускает **дополнительный** процесс внутри живого контейнера | Использовать `docker attach` (выход по `Ctrl+C` убьёт сервер!) |
| **`docker stop`** | `-t 10` (таймаут секунд) | Шлёт `SIGTERM` (даёт закрыть коннекты к БД), затем `SIGKILL` | Использовать `docker kill` (мгновенный `SIGKILL` с потерей данных) |
| **`docker stats`** | `--no-stream` | Показывает потребление CPU / RAM / Network в реальном времени | Не следить за лимитами памяти (`OOMKilled`, код возврата `137`) |

---
### 3. Загадка кода возврата `Exited (137)` и разница `exec` vs `attach`
> **Junior vs Senior**:
> - **Junior**: Подключается к контейнеру через `docker attach`, нажимает `Ctrl+C`, чтобы выйти из терминала, и случайно останавливает продакшен-сервер. А увидев в `docker ps -a` статус `Exited (137)`, думает, что это ошибка в синтаксисе Python.
> - **Senior**: Для входа внутрь всегда использует `docker exec -it <name> sh` (это создаёт отдельную оболочку, выход из которой не трогает сервер). И мгновенно расшифровывает код **`137`**: в Unix `128 + номер сигнала (9 = SIGKILL) = 137` — это значит, что контейнер превысил лимит оперативной памяти и был убит ядром Linux (**OOM Killer**).

---
### 4. Живая проверка: декодер кодов завершения Docker-контейнеров
Напишем на Python диагностическую утилиту, расшифровывающую статусы `Exit Code` из `docker ps -a` и `docker inspect`:

```python
def diagnose_container_exit(exit_code: int, oom_killed: bool = False) -> str:
    if exit_code == 0:
        return "0 (OK): Процесс завершился штатно без ошибок."
    if exit_code == 137 or oom_killed:
        return "137 (128 + SIGKILL[9]): Контейнер убит OOM Killer (нехватка RAM) или docker kill!"
    if exit_code == 143:
        return "143 (128 + SIGTERM[15]): Контейнер штатно остановлен командой docker stop."
    if exit_code == 1:
        return "1 (Application Error): Необработанное исключение в Python-коде (проверьте docker logs)."
    return f"{exit_code}: Нестандартный код завершения."

for code, oom in [(0, False), (1, False), (137, True), (143, False)]:
    print(f"ExitCode={code:<3} -> {diagnose_container_exit(code, oom)}")
```
"""

NOTES[r"Юнит 7.2 · Docker основы\📚 Конспекты\К-185. Виртуальные машины vs Контейнеры.md"] = r"""📖 Перечитать конспект: Виртуальные машины vs Контейнеры: как работает изоляция >>
### 1. Ментальная модель: Отдельный коттедж (`VM`) или Квартира в небоскрёбе (`Container`)
Новички часто называют Docker-контейнер «лёгкой виртуальной машиной». Технически это неверно!
- **Виртуальная машина (VM)** — это отдельный загородный коттедж со своим фундаментом, котельной и водопроводом. Программа **Гипервизор** эмулирует виртуальное «железо» (процессор, диск, сетевую карту), поверх которого устанавливается полноценная **Гостевая ОС** со своим собственным ядром Linux/Windows.
- **Контейнер** — это квартира в современном доме: у всех квартир общий фундамент и коммуникации (**одно общее ядро ОС хоста!**), но у каждой — звукоизолированные стены (**Linux Namespaces**) и счётчики воды/электричества (**cgroups**).

```text
ВИРТУАЛЬНЫЕ МАШИНЫ (тяжёлые, старт ~30 сек):     КОНТЕЙНЕРЫ (лёгкие, старт ~0.1 сек):
┌───────────────────┐ ┌───────────────────┐      ┌───────────────────┐ ┌───────────────────┐
│ App A + Libs      │ │ App B + Libs      │      │ App A + Libs      │ │ App B + Libs      │
├───────────────────┤ ├───────────────────┤      └─────────┬─────────┘ └─────────┬─────────┘
│ Guest OS (Ядро 1) │ │ Guest OS (Ядро 2) │                │ (Namespaces+cgroups)│
├───────────────────┴─┴───────────────────┤      ┌─────────┴─────────────────────┴─────────┐
│          Гипервизор (KVM / VMware)      │      │           Docker Engine (containerd)    │
├─────────────────────────────────────────┤      ├─────────────────────────────────────────┤
│          Ядро Хост-ОС + Железо          │      │        ЕДИНОЕ Ядро Linux + Железо       │
└─────────────────────────────────────────┘      └─────────────────────────────────────────┘
```

---
### 2. Три кита контейнеризации в ядре Linux: `Namespaces`, `cgroups`, `OverlayFS`
В ядре Linux вообще нет понятия «Docker-контейнер»! Для ядра контейнер — это самый обычный процесс, ограниченный тремя системными механизмами:
1. **Namespaces (Пространства имён)** — ограничивают **видимость** (что процесс видит вокруг себя):
   - `pid` — процесс видит себя как `PID 1` и не видит чужие процессы на сервере.
   - `net` — собственные сетевые интерфейсы и порты.
   - `mnt` — собственная корневая файловая система `/`.
2. **cgroups (Control Groups)** — ограничивают **аппетиты** (сколько ресурсов процесс может съесть: например, `--memory=512m --cpus=1.5`).
3. **OverlayFS (UnionFS)** — собирает слои образа в единую папку.

| Критерий | Виртуальная машина (VM) | Контейнер (Docker) |
| :--- | :--- | :--- |
| **Ядро операционной системы** | У каждой VM **своё отдельное ядро** | **Одно общее ядро** хостовой ОС |
| **Время запуска** | 20–60 секунд (загрузка всей ОС) | **50–200 миллисекунд** (старт процесса) |
| **Накладные расходы RAM / Диск** | Гигабайты (2–4 ГБ RAM, 20+ ГБ диск) | Мегабайты (50–150 МБ образ) |
| **Уровень изоляции безопасности** | Аппаратный (через гипервизор — выше) | На уровне системных вызовов ядра |

---
### 3. Как сочетают VM и Контейнеры в реальном продакшене?
> **Junior vs Senior**:
> - **Junior**: Спорит, что «виртуальные машины устарели, и Docker их полностью заменил». Или пытается запустить нативный Windows-контейнер на Linux-сервере без виртуализации (забывая, что контейнеры делят ядро хоста).
> - **Senior**: Понимает, что в облаках (AWS EC2, Yandex Cloud) **VM и контейнеры работают вместе**: облачный провайдер выделяет вам изолированные виртуальные машины (VM) для жёсткой безопасности между разными клиентами, а уже **внутри этих VM** вы запускаете десятки лёгких Docker-контейнеров.

---
### 4. Живая проверка: расчёт плотности размещения и лимитов `cgroups`
Посчитаем на Python, сколько микросервисов поместится на сервере с 16 ГБ RAM при использовании VM и при использовании контейнеров с `cgroups`:

```python
def calculate_cluster_capacity(host_ram_mb: int, mode: str) -> dict:
    host_os_overhead_mb = 1024
    available_mb = host_ram_mb - host_os_overhead_mb
    if mode == "vm":
        guest_os_mb, app_mb = 1536, 512  # Каждая VM тратит 1.5 ГБ только на свою Guest OS
        per_unit = guest_os_mb + app_mb
    else:
        guest_os_mb, app_mb = 0, 512     # Контейнер использует общее ядро хоста (0 МБ на Guest OS!)
        per_unit = app_mb
    count = available_mb // per_unit
    return {"mode": mode, "instances": count, "ram_per_instance_mb": per_unit}

print("Виртуальные машины :", calculate_cluster_capacity(16384, "vm"))
print("Docker-контейнеры  :", calculate_cluster_capacity(16384, "container"))
```
"""

NOTES[r"Юнит 7.2 · Docker основы\📚 Конспекты\К-186. Контекст сборки Docker и .dockerignore.md"] = r"""📖 Перечитать конспект: Контекст сборки Docker и файл .dockerignore >>
### 1. Ментальная модель: Чемодан, который вы отправляете на фабрику
Когда вы пишете команду `docker build -t myapp .`, точка `.` в конце — это **НЕ** «найди Dockerfile в текущей папке»!
Точка `.` — это **Контекст сборки (Build Context)**. Первым же шагом клиент Docker упаковывает **абсолютно все файлы и папки** внутри `.` в архив и пересылает их демону Docker (`dockerd`). Если в вашей папке лежат локальное окружение `.venv` (500 МБ), история `.git` (300 МБ) и дампы базы данных, Docker будет копировать этот гигабайтный «чемодан» перед каждой сборкой!
Файл **`.dockerignore`** работает как фильтр перед упаковкой чемодана: всё, что в нём перечислено, даже не отправляется демону сборки.

```text
Без .dockerignore (контекст 850 МБ — сборка тормозит и сбрасывает кэш!):
[Папка проекта: src/ + .venv/ + .git/ + .env] ──850 MB──► [Docker Daemon]

С .dockerignore (контекст 120 КБ — мгновенный старт и защита секретов!):
[Папка проекта] ──► [Фильтр .dockerignore] ──только src/ (120 KB)──► [Docker Daemon]
```

---
### 2. Почему без `.dockerignore` инструкция `COPY . .` ломает кэш и крадёт секреты?
Представьте, что в вашем `Dockerfile` написано `COPY . /app`. Без `.dockerignore` внутрь продакшен-образа попадут:
1. Файл **`.env`** с локальными паролями и токенами (любой, кто скачает образ, прочитает их!).
2. Папка **`.git/`** и кэш **`__pycache__/`**: стоит вам переключить ветку или запустить `pytest` на ноутбуке, файлы в `.git` и `.pytest_cache` изменятся, и `COPY . /app` **сбросит кэш сборки Docker**, хотя исходный код вообще не менялся!

```dockerignore
# Эталонный .dockerignore для Python-проекта:
.git
.gitignore
.venv
venv
__pycache__
*.py[cod]
.pytest_cache
.mypy_cache
.ruff_cache
.env
.env.*
!.env.example
Dockerfile*
compose*.yaml
README.md
docs/
tests/
```

| Проблема без `.dockerignore` | Почему возникает? | Как решает `.dockerignore` |
| :--- | :--- | :--- |
| **`Sending build context: 1.2 GB`** | В архив попадают `.venv/`, `.git/`, `node_modules/` | Уменьшает контекст до нескольких килобайт |
| **Утечка паролей в слои образа** | `COPY . .` копирует локальный `.env` внутрь Image | Исключает `.env*` на этапе формирования контекста |
| **Постоянный сброс кэша `COPY`** | Любой запуск тестов меняет `.pytest_cache` | Игнорирует временные папки и кэши IDE (`.idea`, `.vscode`) |
| **Конфликт бинарников ОС** | Локальный `.venv` с Windows/macOS копируется в Linux-образ | Полностью отсекает локальный `.venv` |

---
### 3. Правило гигиены контекста сборки
> **Junior vs Senior**:
> - **Junior**: Запускает `docker build .` без `.dockerignore` или случайно запускает сборку из домашней директории `~`, удивляясь, почему Docker 5 минут пишет ` transferring context: 14.5GB`.
> - **Senior**: Создаёт `.dockerignore` одновременно с `Dockerfile`, а в самом `Dockerfile` вместо слепого `COPY . .` копирует только нужные директории явно (`COPY ./src ./src`).

---
### 4. Живая проверка: анализатор экономии Build Context и защиты от утечек
Посчитаем на Python, насколько `.dockerignore` сжимает размер контекста сборки и какие угрозы безопасности предотвращает:

```python
def analyze_build_context(project_files: dict[str, int], dockerignore: set[str]) -> dict:
    raw_kb = sum(project_files.values())
    sent_files = {f: sz for f, sz in project_files.items() if f.split("/")[0] not in dockerignore}
    sent_kb = sum(sent_files.values())
    leaked_secrets = [f for f in sent_files if f.startswith(".env")]
    return {
        "raw_mb": round(raw_kb / 1024, 2),
        "filtered_kb": sent_kb,
        "saved_percent": round((1 - sent_kb / raw_kb) * 100, 2),
        "leaked_secrets": leaked_secrets,
    }

workspace = {
    ".git/pack": 320_000,
    ".venv/lib": 540_000,
    "__pycache__/app.pyc": 1_200,
    ".env": 4,
    "src/main.py": 45,
    "requirements.txt": 2,
}
ignore_set = {".git", ".venv", "__pycache__", ".env"}
print("Без .dockerignore:", analyze_build_context(workspace, set()))
print("С   .dockerignore:", analyze_build_context(workspace, ignore_set))
```
"""

# ==============================================================================
# ЮНИТ 7.3 · DOCKER ПРОДВИНУТЫЙ (К-187 .. К-191)
# ==============================================================================

NOTES[r"Юнит 7.3 · Docker продвинутый\📚 Конспекты\К-187. Multi-stage сборка в Docker.md"] = r"""📖 Перечитать конспект: Multi-stage сборка в Docker: худеем с 1.1 ГБ до 90 МБ >>
### 1. Ментальная модель: Строительные леса убирают перед сдачей дома
Чтобы скомпилировать некоторые Python-библиотеки (например, `psycopg2`, `cryptography`, `uvloop`), во время `pip install` нужны тяжёлые инструменты: компилятор C (`gcc`), заголовочные файлы (`python3-dev`, `libpq-dev`), которые весят 600–800 МБ.
Но когда колёса (`wheels`) уже собраны и установлены, **зачем тащить компилятор `gcc` в продакшен-контейнер?!** Он раздувает образ до 1+ ГБ и даёт хакерам удобные утилиты при взломе.
**Multi-stage build (Многоэтапная сборка)** позволяет использовать в одном `Dockerfile` два (и более) блока `FROM`:
1. **Этап `builder` (Стройплощадка)** — содержит `gcc`, собирает все зависимости в аккуратную папку `/opt/venv`.
2. **Этап `runtime` (Чистая квартира)** — берёт крошечный чистый образ `python:3.13-slim` и копирует из первого этапа **только готовую папку `/opt/venv`** через `COPY --from=builder`, выбрасывая `gcc` и весь строительный мусор!

```text
[Этап 1: builder (980 МБ)]                  [Этап 2: runtime (95 МБ — идёт в прод!)]
├── Debian + Python 3.13                    ├── Debian Slim + Python 3.13
├── gcc, make, libpq-dev (800 МБ мусора)    ├── /opt/venv ◄── COPY --from=builder
└── /opt/venv (собранные пакеты, 35 МБ) ────┘   └── /app/src (ваш код)
```

---
### 2. Промышленный Multi-stage `Dockerfile` для Python 3.13
Обратите внимание на магию `ENV PATH="/opt/venv/bin:$PATH"`: мы просто ставим путь к виртуальному окружению первым в `PATH`, и во втором этапе команды `python` и `uvicorn` автоматически работают из перенесённого `/opt/venv`!

```dockerfile
# ==================== ЭТАП 1: СБОРЩИК (BUILDER) ====================
FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==================== ЭТАП 2: ФИНАЛЬНЫЙ ОБРАЗ (RUNTIME) ============
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Копируем ТОЛЬКО скомпилированное окружение из этапа builder (без gcc!):
COPY --from=builder /opt/venv /opt/venv
COPY ./src ./src

RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

| Подход к сборке | Размер итогового образа | Что внутри образа? | Скорость раскатки в Kubernetes |
| :--- | :--- | :--- | :--- |
| Одиночный `FROM python:3.13` | **~1 150 МБ** | `gcc`, `git`, `curl`, кэш `apt`, `pip` | Медленно (качает гигабайт по сети) |
| `python:3.13-slim` + `RUN apt remove gcc` в следующем слое | **~450 МБ** | Удаление в новом слое `RUN` **не уменьшает** размер предыдущего слоя! | Средне |
| **Multi-stage (`builder` ➔ `runtime`)** | **~95 МБ** | Только Python runtime, `/opt/venv` и `/app/src` | Мгновенно + высокая безопасность |

---
### 3. Почему `RUN apt-get remove gcc` в отдельном слое НЕ уменьшает образ?
> **Junior vs Senior**:
> - **Junior**: Ставит `gcc` в одном `RUN apt-get install gcc`, ставит пакеты, а ниже пишет `RUN apt-get purge -y gcc` и удивляется, почему образ всё равно весит 600 МБ. Он забыл, что слои образа **неизменяемы**: удаление файла в верхнем слое просто кладёт поверх него «метку невидимости» (*whiteout file*), а сами мегабайты остаются в нижнем слое навсегда!
> - **Senior**: Использует **Multi-stage build**, чтобы сборочные инструменты вообще не попали ни в один слой финального образа `runtime`.

---
### 4. Живая проверка: сравнение веса слоёв Single-stage vs Multi-stage
Посчитаем на Python, почему удаление файлов в новом слое не освобождает место и как Multi-stage решает эту задачу:

```python
def single_stage_size_mb(layers: list[tuple[str, int]]) -> int:
    # В одноэтапной сборке размер образа равен сумме ВСЕХ слоёв (отрицательных слоёв не бывает!)
    return sum(max(0, size) for _, size in layers)

def multi_stage_size_mb(base_mb: int, copied_artifacts_mb: int, code_mb: int) -> int:
    return base_mb + copied_artifacts_mb + code_mb

naive_layers = [("python-slim", 45), ("apt install gcc", 380), ("pip install", 35), ("apt remove gcc", -380), ("copy src", 2)]
print(f"Одноэтапный образ (даже с apt remove gcc): {single_stage_size_mb(naive_layers)} МБ (gcc остался в слое №2!)")
print(f"Multi-stage образ (COPY --from=builder)  : {multi_stage_size_mb(45, 35, 2)} МБ (экономия >80%!)")
```
"""

NOTES[r"Юнит 7.3 · Docker продвинутый\📚 Конспекты\К-188. Docker Реестры.md"] = r"""📖 Перечитать конспект: Docker Реестры (Registries), теги и ловушка :latest >>
### 1. Ментальная модель: App Store для серверных образов
GitHub хранит ваш исходный код (`.py`), а **Container Registry (Реестр контейнеров)** хранит готовые скомпилированные слои ваших Docker-образов.
Когда CI/CD-пайплайн собрал образ, он делает `docker push`, загружая только изменившиеся слои в реестр (Docker Hub, GitHub Container Registry `ghcr.io`, GitLab Registry или AWS ECR). А продакшен-серверы делают `docker pull` и запускают точно этот же бинарный слепок.

```text
 Полное имя образа (URI в реестре):
   ghcr.io  /  acme-corp / billing-api  :  1.4.2-a1b2c3d
 └────┬────┘ └───────────┬─────────────┘ └───────┬───────┘
 Хост реестра   Namespace / Репозиторий    Неизменяемый Тег
 (по умолч.                                (или @sha256:...)
  docker.io)
```

---
### 2. Почему тег `:latest` опасен для продакшена?
Новички думают, что тег `:latest` магически означает «самая стабильная проверенная версия».
На самом деле `:latest` — это **просто строчка по умолчанию**, которую Docker подставляет, если вы забыли указать двоеточие! Хуже того: тег `:latest` **мутабелен** (сегодня за `python:latest` скрывается Python 3.12, а завтра выйдет Python 3.13, и при пересборке ваш прод внезапно скачает новую мажорную версию ОС и интерпретатора!).

```bash
# Авторизация в приватном корпоративном реестре (пароль передаём безопасно через stdin!):
echo "$REGISTRY_TOKEN" | docker login ghcr.io -u username --password-stdin

# Правильное тегирование образа версией релиза и коротким SHA коммита Git:
docker tag billing-api:local ghcr.io/acme/billing-api:1.4.2-f89a12b

# Отправка слоёв в реестр (загрузятся только новые слои, которых ещё нет на сервере):
docker push ghcr.io/acme/billing-api:1.4.2-f89a12b
```

| Стратегия тегирования | Пример | Предсказуемость и откат (Rollback) | Где использовать |
| :--- | :--- | :--- | :--- |
| **Плавающий `:latest`** | `myapp:latest` | **Опасно**: перезаписывается при каждом пуше, невозможно понять, что именно сейчас на проде | Только локальные эксперименты |
| **Мажорный базовый тег** | `python:3.13-slim-bookworm` | **Отлично для `FROM`**: фиксирует версию Python и релиз Debian (`bookworm`) | В `Dockerfile` для базового образа |
| **SemVer + Git SHA** | `myapp:1.4.2-f89a12b` | **Эталон продакшена**: мгновенно видно версию и коммит, откат за 5 секунд | Деплой в Kubernetes / Compose |
| **Digest (`@sha256:...`)** | `myapp@sha256:9c8b...` | **100% криптографическая неизменяемость** | Банковский и финтех-продакшен |

---
### 3. Культура идемпотентных релизов
> **Junior vs Senior**:
> - **Junior**: Собирает и деплоит `myapp:latest`. Когда в 3 часа ночи после релиза обнаруживается баг, джун не может откатиться назад, потому что старый образ `myapp:latest` в реестре уже перезаписан новым!
> - **Senior**: Настраивает в CI/CD иммутабельные теги вида `1.4.2-<git-sha>` и включает в реестре опцию **Tag Immutability** (запрет перезаписи существующего тега). Откат на предыдущую версию занимает одну строчку: сменить версию тега обратно на `1.4.1-c0ffee1`.

---
### 4. Живая проверка: парсер и валидатор URI Docker-образов для CI/CD
Напишем на Python валидатор, который блокирует выкатку образов с плавающим тегом `:latest` на продакшен:

```python
def parse_and_validate_image(image_ref: str) -> dict:
    digest = None
    if "@" in image_ref:
        image_ref, digest = image_ref.split("@", 1)
    if ":" in image_ref.split("/")[-1]:
        repo_part, tag = image_ref.rsplit(":", 1)
    else:
        repo_part, tag = image_ref, "latest"
    parts = repo_part.split("/")
    registry = parts[0] if ("." in parts[0] or ":" in parts[0]) else "docker.io"
    prod_safe = (tag != "latest") or (digest is not None)
    return {"registry": registry, "tag": tag, "digest": digest, "prod_safe": prod_safe}

for ref in ["billing-api", "python:latest", "ghcr.io/acme/billing:1.4.2-f89a12b"]:
    info = parse_and_validate_image(ref)
    status = "ALLOWED ✅" if info["prod_safe"] else "REJECTED 🛑 (no :latest in prod!)"
    print(f"{ref:<36} -> registry={info['registry']:<10} tag={info['tag']:<14} | {status}")
```
"""

NOTES[r"Юнит 7.3 · Docker продвинутый\📚 Конспекты\К-189. Сети в Docker.md"] = r"""📖 Перечитать конспект: Сети в Docker: Bridge, Host, None и встроенный DNS >>
### 1. Ментальная модель: Внутренняя АТС бизнес-центра с телефонной книгой
По умолчанию каждый контейнер изолирован в собственной виртуальной сетевой комнате. Как соединить контейнер `api` с контейнером `postgres`, но при этом спрятать базу данных от хакеров из интернета?
Docker создаёт виртуальный коммутатор — сеть типа **`bridge` (мост)**. Внутри **пользовательской сети (`User-defined bridge`)** работает встроенный **DNS-сервер Docker (`127.0.0.11`)**: он автоматически знает имена всех контейнеров в этой сети! А чтобы пустить трафик с улицы только к входной двери (`nginx` или `api`), мы пробрасываем порт (`-p 8000:8000`).

```text
Внешний мир (Браузер клиента)
      │
      ▼  Порт хоста :8000 проброшен (-p 8000:8000)
┌─────┴─────────────────────────────────────────────────────────┐
│ Пользовательская сеть Docker (User-defined bridge: backend)   │
│                                                               │
│  [Контейнер api :8000] ──DNS запрос "db"──► [Контейнер db :5432]
│                                             (БЕЗ ports: снаружи
│                                              недоступен вообще!)
└───────────────────────────────────────────────────────────────┘
```

---
### 2. Четыре драйвера сети Docker и важное отличие `default bridge`
Знаете ли вы, что в стандартной сети `bridge` (куда попадают одиночные контейнеры `docker run` без флага `--network`) **DNS по именам контейнеров НЕ работает**? Автоматический DNS включается только в **пользовательских сетях** (`docker network create` или сети, созданные через `docker compose`)!

```bash
# Создать собственную изолированную сеть с работающим DNS:
docker network create backend-net

# Запустить Postgres внутри сети БЕЗ проброса портов наружу (100% защита от интернета):
docker run -d --name db --network backend-net -e POSTGRES_PASSWORD=secret postgres:16-alpine

# Запустить API в той же сети — он мгновенно увидит хост "db" по порту 5432:
docker run -d --name api --network backend-net -p 8000:8000 billing-api:1.0.0
```

| Драйвер сети | Изоляция | Работает ли DNS по имени контейнера? | Когда применять? |
| :--- | :--- | :--- | :--- |
| **`bridge` (default)** | Изолирована от хоста | **Нет** (только по сырым IP `172.17.0.x`) | Одиночные тестовые контейнеры |
| **`bridge` (user-defined)** | Изолирована между проектами | **Да!** (`http://api:8000`, `db:5432`) | **Стандарт для Docker Compose** и микросервисов |
| **`host`** | **Отключена** (делит сеть с сервером) | Нет (сразу занимает порты хоста) | Сверхвысоконагруженные сетевые прокси на Linux |
| **`none`** | **Абсолютная** (нет интернета и сети) | Нет (только `lo` `127.0.0.1`) | Безопасный расчёт недоверенного кода / криптографии |

---
### 3. Две главные сетевые ошибки: `127.0.0.1` в Uvicorn и публичный порт БД
> **Junior vs Senior**:
> - **Junior**: Запускает внутри контейнера `uvicorn main:app --host 127.0.0.1 --port 8000`, пробрасывает `-p 8000:8000`, но снаружи сервер не отвечает! Почему? Потому что `127.0.0.1` слушает **только внутреннюю петлю самого контейнера**, игнорируя сетевой мост Docker. А для базы данных джун пишет `ports: ["5432:5432"]` на боевом сервере, открывая Postgres для ботов-брутфорсеров со всего мира.
> - **Senior**: Внутри контейнера всегда слушает **`--host 0.0.0.0`** (все сетевые интерфейсы контейнера). А на продакшен-сервере убирает `ports:` у Postgres и Redis (или биндит их строго на локальный интерфейс хоста `127.0.0.1:5432:5432`).

---
### 4. Живая проверка: симулятор маршрутизации и встроенного DNS Docker
Проверим на Python, как пользовательская сеть `bridge` разрешает имена сервисов и почему порт `db:5432` доступен для `api`, но закрыт из интернета:

```python
class DockerNetworkSimulator:
    def __init__(self) -> None:
        self.containers: dict[str, dict] = {}

    def register(self, name: str, network: str, listen_host: str, internal_port: int, published_port: int | None = None) -> None:
        self.containers[name] = {
            "net": network, "listen": listen_host, "port": internal_port, "pub": published_port
        }

    def connect_from_internet(self, name: str) -> str:
        c = self.containers[name]
        if c["pub"] is None:
            return f"BLOCKED 🛡️: порт {name}:{c['port']} не опубликован наружу"
        if c["listen"] == "127.0.0.1":
            return f"ERROR ❌: процесс в {name} слушает 127.0.0.1 вместо 0.0.0.0!"
        return f"OK ✅: внешний трафик доставлен в {name}:{c['port']}"

    def connect_internal_dns(self, src: str, dst: str) -> str:
        c1, c2 = self.containers[src], self.containers[dst]
        if c1["net"] == c2["net"] and c1["net"] != "default_bridge":
            return f"OK ✅: DNS разрешил '{dst}' -> соединение {src} -> {dst}:{c2['port']} внутри '{c1['net']}'"
        return "ERROR ❌: контейнеры в разных сетях или в default_bridge без DNS"

net = DockerNetworkSimulator()
net.register("api", network="app_net", listen_host="0.0.0.0", internal_port=8000, published_port=8000)
net.register("db", network="app_net", listen_host="0.0.0.0", internal_port=5432, published_port=None)

print("Интернет -> api:", net.connect_from_internet("api"))
print("Интернет -> db :", net.connect_from_internet("db"))
print("Внутри   api->db:", net.connect_internal_dns("api", "db"))
```
"""

NOTES[r"Юнит 7.3 · Docker продвинутый\📚 Конспекты\К-190. Хранение данных в Docker.md"] = r"""📖 Перечитать конспект: Хранение данных в Docker: Volumes, Bind Mounts и tmpfs >>
### 1. Ментальная модель: Внешний сейф (`Volume`), Окно в папку ноутбука (`Bind Mount`) и Записка в RAM (`tmpfs`)
Мы уже знаем, что внутренний слой контейнера умирает вместе с контейнером (`docker rm`). Чтобы данные жили вечно, Docker позволяет «прорубить портал» из папки внутри контейнера наружу тремя способами:
1. **Named Volume (Именованный том)** — надёжный банковский сейф под управлением самого Docker (`/var/lib/docker/volumes/...`). Идеален для баз данных (`PostgreSQL`, `Redis`) в продакшене.
2. **Bind Mount (Привязка папки хоста)** — прямое «окно» в конкретную папку вашего ноутбука (`./src:/app/src`). Меняете код в PyCharm/VS Code на ноутбуке — и Uvicorn внутри контейнера в ту же секунду делает `Hot Reload`!
3. **`tmpfs` Mount** — сверхбыстрый виртуальный диск прямо в оперативной памяти (`RAM`). При остановке контейнера данные мгновенно испаряются, не оставляя следов на SSD.

```text
Хост-машина (Сервер / Ноутбук)                     Контейнер Docker
┌──────────────────────────────┐                   ┌───────────────────────────┐
│ Docker Area (/var/lib/docker)│ ══ Named Volume ═►│ /var/lib/postgresql/data  │
│ Проектная папка (./src)      │ ══ Bind Mount   ═►│ /app/src (для Hot Reload) │
│ Оперативная память (RAM)     │ ══ tmpfs Mount  ═►│ /run/secrets (без диска!) │
└──────────────────────────────┘                   └───────────────────────────┘
```

---
### 2. Сравнение трёх типов монтирования и синтаксис `--mount` / `compose.yaml`
В `compose.yaml` можно комбинировать все три типа монтирования в зависимости от задачи:

```yaml
services:
  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data         # 1. Named Volume (данные БД в безопасности)

  api-dev:
    build: .
    volumes:
      - ./src:/app/src:ro                       # 2. Bind Mount (код с хоста в режиме Read-Only :ro)
    tmpfs:
      - /tmp/cache:size=64m                     # 3. tmpfs (временный кэш в оперативной памяти)

volumes:
  pgdata:
```

| Тип хранилища | Кто управляет путём на хосте? | Сохраняется ли после `docker rm`? | Главный сценарий использования |
| :--- | :--- | :--- | :--- |
| **Named Volume** | Сам демон Docker | **Да** (пока явно не вызвать `volumes -v`) | **Базы данных (`Postgres`, `ClickHouse`)**, файлы на проде |
| **Bind Mount** | Разработчик (указывает точный путь `./src`) | **Да** (это обычная папка хоста) | Локальная разработка с **Hot Reload**, проброс конфига `nginx.conf:ro` |
| **`tmpfs`** | Ядро Linux (живёт только в RAM) | **Нет** (исчезает мгновенно) | Временные секреты, быстрые тестовые БД в CI |

---
### 3. Опасность команды `docker compose down -v`
> **Junior vs Senior**:
> - **Junior**: Чтобы «перезапустить проект с чистого листа», копирует из интернета команду `docker compose down -v` и запускает её на стейджинг/прод-сервере. Флаг **`-v` (`--volumes`) без предупреждения уничтожает все именованные тома**, включая базу данных PostgreSQL!
> - **Senior**: Чётко разделяет `docker compose down` (безопасно пересоздаёт только контейнеры и сеть, сохраняя все `Named Volumes`) и разрушительный флаг `-v`, а для продакшен-томов настраивает регулярный бэкап (`pg_dump` в S3) и флаг `external: true`.

---
### 4. Живая проверка: симуляция сохранности данных при пересоздании контейнера
Убедимся на Python, что происходит с данными в R/W-слое контейнера, в `tmpfs` и в `Named Volume` после `docker compose down`:

```python
class StorageSimulation:
    def __init__(self) -> None:
        self.named_volume: dict[str, str] = {"users.db": "1000 rows"}
        self.container_rw: dict[str, str] = {"temp.log": "started"}
        self.tmpfs_ram: dict[str, str] = {"token.key": "secret_jwt"}

    def docker_compose_down(self, remove_volumes_flag_v: bool = False) -> None:
        self.container_rw.clear()  # Умирает всегда при удалении контейнера
        self.tmpfs_ram.clear()     # Испаряется из RAM при остановке контейнера
        if remove_volumes_flag_v:
            self.named_volume.clear()

sim = StorageSimulation()
sim.docker_compose_down(remove_volumes_flag_v=False)
print(f"После обычного 'docker compose down'   : volume={sim.named_volume}, rw={sim.container_rw}, tmpfs={sim.tmpfs_ram}")
sim.docker_compose_down(remove_volumes_flag_v=True)
print(f"После опасного 'docker compose down -v': volume={sim.named_volume} (БД удалена!)")
```
"""

NOTES[r"Юнит 7.3 · Docker продвинутый\📚 Конспекты\К-191. Kubernetes_ базовые понятия для чтения.md"] = r"""📖 Перечитать конспект: Kubernetes (K8s): базовые понятия для бэкенд-разработчика >>
### 1. Ментальная модель: Автопилот для флота из 100 серверов
`Docker Compose` великолепен, когда все ваши контейнеры крутятся на **одном** сервере. Но что, если у вас 50 микросервисов на 20 серверах (нодах), и в 4 часа утра один сервер физически сгорает, а в 12:00 на распродаже нагрузка вырастает в 10 раз?
**Kubernetes (K8s)** — это автопилот кластера. Вы отдаёте ему YAML-манифест с **желаемым состоянием** (*«Хочу, чтобы всегда работало 3 копии `billing-api`»*), а Kubernetes сам распределяет их по живым серверам, перезапускает упавшие контейнеры и балансирует трафик!

```text
Входящий HTTPS трафик (api.shop.com)
         │
         ▼
   [ Ingress ]        ◄── Маршрутизатор по доменам и путям (/api/v1 -> Service)
         │
         ▼
   [ Service ]        ◄── Вечный внутренний IP + балансировщик нагрузки
    /    │    \
   ▼     ▼     ▼
[Pod 1][Pod 2][Pod 3] ◄── Управляются контроллером [ Deployment (replicas: 3) ]
```

---
### 2. Пять главных сущностей K8s, которые нужно уметь читать в YAML
В Kubernetes мы никогда не создаём «голые контейнеры». Минимальная неделимая единица в K8s — это **Pod (Под)** (капсула вокруг одного или тесно связанных контейнеров с общим IP). Но и Поды сами по себе смертны (при пересоздании Под получает новый IP!), поэтому вокруг них строятся 4 управляющих объекта:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: billing-api
spec:
  replicas: 3                  # Всегда держать 3 живых Пода!
  selector:
    matchLabels:
      app: billing
  template:
    metadata:
      labels:
        app: billing
    spec:
      containers:
        - name: api
          image: ghcr.io/acme/billing:1.4.2
          envFrom:
            - configMapRef:
                name: billing-config
            - secretRef:
                name: billing-secrets
          resources:
            requests: { cpu: "250m", memory: "256Mi" }
            limits:   { cpu: "500m", memory: "512Mi" }
```

| Сущность K8s (`kind`) | Зачем она нужна? | Аналог в мире Docker Compose |
| :--- | :--- | :--- |
| **`Pod` (Под)** | Одноразовая капсула с контейнером и собственным временным IP | Запущенный контейнер `billing-api-1` |
| **`Deployment`** | Следит, чтобы всегда работало `N` реплик Подов, и делает **Rolling Update** без даунтайма | Секция `deploy: replicas: 3` |
| **`Service`** | Даёт группе Подов **постоянное DNS-имя и IP**, балансируя трафик между живыми репликами | Внутренний DNS-балансировщик сети |
| **`Ingress`** | Входная точка снаружи кластера (HTTP/HTTPS роутинг по доменам и TLS) | Внешний `Nginx` / `Traefik` |
| **`ConfigMap` / `Secret`** | Хранилище настроек и паролей, подключаемых в Под как `ENV` или файлы | Файлы `.env` и `secrets` |

---
### 3. Зачем в `Deployment` нужны `requests` и `limits`?
> **Junior vs Senior**:
> - **Junior**: Пишет манифест `Deployment` без секции `resources` и обращается к соседнему микросервису по IP-адресу конкретного Пода (`10.244.1.45`). Через час Под пересоздаётся с новым IP, и связь падает, а утечка памяти в одном контейнере кладёт весь физический сервер кластера.
> - **Senior**: Всегда обращается к микросервисам через вечное DNS-имя объекта **`Service`** (`http://billing-svc.default.svc.cluster.local`), а в каждом `Deployment` задаёт **`requests`** (гарантированный минимум CPU/RAM для планировщика) и **`limits`** (потолок, защищающий соседей по серверу).

---
### 4. Живая проверка: симуляция цикла самоисцеления (`Reconciliation Loop`) в Kubernetes
В сердце Kubernetes крутится бесконечный цикл: `Наблюдаемое состояние != Желаемое состояние -> Исправить!`. Запустим эту модель на Python:

```python
class K8sDeploymentController:
    def __init__(self, desired_replicas: int, image: str) -> None:
        self.desired = desired_replicas
        self.image = image
        self.pods: list[dict[str, str]] = []
        self._seq = 0

    def reconcile(self) -> None:
        # 1. Удаляем упавшие Поды (Failed / OOMKilled)
        self.pods = [p for p in self.pods if p["status"] == "Running"]
        # 2. Досоздаём недостающие Поды до desired_replicas
        while len(self.pods) < self.desired:
            self._seq += 1
            self.pods.append({"name": f"billing-pod-{self._seq}", "ip": f"10.244.0.{self._seq}", "status": "Running"})

controller = K8sDeploymentController(desired_replicas=3, image="billing:1.4.2")
controller.reconcile()
print("Старт кластера (3/3)   :", [p["name"] for p in controller.pods])

# Имитируем падение одного Пода в 4 часа утра:
controller.pods[1]["status"] = "OOMKilled"
controller.reconcile()
print("После самоисцеления K8s:", [p["name"] for p in controller.pods])
```
"""

# ==============================================================================
# ЮНИТ 7.4 · CI/CD (К-192 .. К-197)
# ==============================================================================

NOTES[r"Юнит 7.4 · CI CD\📚 Конспекты\К-192. CI_CD_ Непрерывная интеграция и доставка.md"] = r"""📖 Перечитать конспект: CI/CD: Непрерывная интеграция и непрерывная доставка >>
### 1. Ментальная модель: Автоматическая лаборатория контроля качества на заводе
Раньше релиз выглядел как ночной кошмар: раз в месяц тимлид по SSH заходил на сервер, делал `git pull`, забывал накатить миграцию БД, и сайт падал на 2 часа.
**CI/CD** превращает проверку и доставку кода в автоматический заводской конвейер, который запускается сам при каждом `git push`:
- **CI (Continuous Integration — Непрерывная интеграция)**: робот-контролёр скачивает ваш коммит на чистую виртуальную машину, проверяет стиль (`ruff`), типы (`mypy`), запускает все тесты (`pytest`) и собирает Docker-образ. Если упал хотя бы 1 тест — слияние в `main` блокируется!
- **CD (Continuous Delivery / Deployment — Непрерывная доставка / развёртывание)**: робот-курьер автоматически доставляет проверенный Docker-образ на Staging и Production серверы без участия человека.

```text
[git push] ──► [CI: Линтер + Тесты + Сборка образа] ──► [CD: Выкатка на Staging]
                                                               │
                 ┌─── Continuous Delivery (по кнопке Approve) ─┤
                 ▼                                             ▼
       [Production Сервер 🚀] ◄─── Continuous Deployment (100% автомат!)
```

---
### 2. В чём разница между Continuous Delivery и Continuous Deployment?
Аббревиатура **CD** расшифровывается двумя способами, и этот вопрос обожают задавать на собеседованиях:

| Этап конвейера | Continuous Integration (CI) | Continuous Delivery (CD) | Continuous Deployment (CD) |
| :--- | :--- | :--- | :--- |
| **Что автоматизировано?** | Линтеры, тесты, проверка безопасности, сборка артефакта | Всё из CI + автодеплой на `Staging` и полная готовность к релизу | Всё из Delivery + **автоматическая выкатка в `Production`** |
| **Выход в Production** | Не входит в зону CI | Требует **ручного нажатия кнопки** (Approve менеджера/лида) | Происходит **автоматически** сразу после зелёных тестов в `main` |
| **Где применяется?** | В любом современном проекте | Банки, финтех, медицина (где важен ручной аудит релиза) | SaaS, веб-платформы, стартапы с высоким покрытием тестами |

---
### 3. Почему «зелёные тесты локально» не заменяют CI?
> **Junior vs Senior**:
> - **Junior**: Говорит «Я уже запустил `pytest` у себя на ноутбуке, зачем ждать CI?» и вливает PR. А на сервере всё падает, потому что джун забыл закоммитить новый файл `schemas.py` или опирался на локальную переменную окружения.
> - **Senior**: Настраивает в GitHub/GitLab правило **Branch Protection**: кнопку `Merge` физически нельзя нажать, пока CI-пайплайн в чистом изолированном контейнере не выдаст статус `SUCCESS`.

---
### 4. Живая проверка: симулятор ворот качества (Quality Gate) CI/CD
Запустим на Python контроллер CI/CD, проверяющий, пройдёт ли коммит в `Production` в режимах Delivery и Deployment:

```python
def run_cicd_gate(checks: dict[str, bool], mode: str, manual_approval: bool = False) -> str:
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        return f"CI FAILED 🛑: остановлено на шагах {failed}"
    if mode == "continuous_deployment":
        return "CD DEPLOYED 🚀: образ автоматически выкачен в Production!"
    if mode == "continuous_delivery":
        return "CD DEPLOYED 🚀 (Approved)" if manual_approval else "STAGING READY ⏸️: ждёт кнопки Approve для Production"
    return "CI PASSED ✅"

commit_checks = {"ruff": True, "mypy": True, "pytest": True, "docker_build": True}
print("Режим Delivery (без кнопки) :", run_cicd_gate(commit_checks, "continuous_delivery", manual_approval=False))
print("Режим Deployment (автомат)  :", run_cicd_gate(commit_checks, "continuous_deployment"))
```
"""

NOTES[r"Юнит 7.4 · CI CD\📚 Конспекты\К-193. CI_CD_ Ранеры, Артефакты, Секреты.md"] = r"""📖 Перечитать конспект: CI/CD: Раннеры, Артефакты, Кэш и Секреты >>
### 1. Ментальная модель: Кухня-арендатор (`Runner`), Готовый торт (`Artifact`) и Сейф (`Secrets`)
Кто именно выполняет ваши тесты, когда вы пушите код в GitHub или GitLab? Сам веб-сайт GitHub не запускает ваш Python-код на своих веб-серверах!
Для этого в архитектуре CI/CD есть четыре ключевых компонента:
1. **Runner (Раннер / Агент)** — отдельный рабочий сервер с установленным Docker, который забирает задание из очереди, выполняет команды пайплайна в чистом контейнере и уничтожает контейнер после завершения.
2. **Cache (Кэш зависимостей)** — сохранённая папка скачанных колёс `~/.cache/pip`, чтобы раннер не качал `SQLAlchemy` заново на каждом коммите.
3. **Artifact (Артефакт)** — ценный результат работы задачи (собранный Docker-образ, `.whl`-пакет, HTML-отчёт покрытия `coverage`), который передаётся следующему этапу пайплайна.
4. **Secrets (Секреты)** — зашифрованное хранилище токенов (`DOCKER_PASSWORD`, `PROD_SSH_KEY`), которые подставляются в память раннера на время шага и маскируются звёздочками `***` в логах.

```text
[Очередь задач GitHub/GitLab]
            │
            ▼ (забирает job по HTTPS)
┌───────────────────────────────────────────────────────────┐
│ Runner (Одноразовый контейнер Ubuntu + Python 3.13)       │
│  ├── Вход : Код + [Cache: ~/.cache/pip] + [Secrets: ***]  │
│  └── Выход: [Artifact: billing-api:1.4.2 / coverage.xml]  │
└───────────────────────────────────────────────────────────┘
```

---
### 2. В чём разница между `Cache` и `Artifact`?
Новички постоянно путают кэш и артефакты в конфигах CI. Запомните простое правило: **Кэш ускоряет скачивание старого, а Артефакт сохраняет результат нового!**

| Понятие CI/CD | Что это такое? | Между чем передаётся? | Что будет, если он пропадёт? |
| :--- | :--- | :--- | :--- |
| **Runner (Shared vs Self-hosted)** | Сервер-исполнитель джобов | Назначается из пула на каждый `job` | Задача ждёт в очереди (`Pending`) |
| **Cache (Кэш)** | Папка скачанных библиотек (`.cache/pip`, `.venv`) | **Между разными запусками** пайплайна по ключу `hashFiles('pyproject.toml')` | Пайплайн просто отработает на 40 секунд медленнее |
| **Artifact (Артефакт)** | Результат сборки (`.whl`, Docker Image, отчёт `junit.xml`) | **Между шагами (stages) внутри одного пайплайна** (`build` ➔ `deploy`) | Следующий шаг (`deploy`) упадёт с ошибкой! |
| **Secrets (Секреты)** | Зашифрованные ключи API и пароли деплоя | Инжектируются в `env` конкретного шага | В логах скрываются маской `***` |

---
### 3. Безопасность раннеров и маскирование секретов
> **Junior vs Senior**:
> - **Junior**: Чтобы проверить, почему не подходит пароль от реестра в CI, пишет в пайплайне `echo $PROD_PASSWORD | base64`, обходя маскировку логов, или запускает чужие Pull Request из форков на `Self-hosted` раннере, имеющем прямой доступ к продакшен-базе.
> - **Senior**: Использует **OIDC-токены** (временные одноразовые пропуска в облако без долгоживущих паролей), изолирует `Self-hosted` раннеры только для защищённой ветки `main` и разделяет секреты по окружениям (`Environment Secrets`: `staging` vs `production`).

---
### 4. Живая проверка: фильтр маскирования секретов в логах раннера CI
Посмотрим на Python, как агент CI/CD автоматически вырезает значения всех зарегистрированных секретов из потока `stdout` перед отправкой логов в браузер:

```python
class CIRunnerLogMasker:
    def __init__(self, secrets: dict[str, str]) -> None:
        # Сортируем от длинных к коротким, чтобы частичные совпадения не оставляли хвостов
        self._secret_values = sorted((v for v in secrets.values() if v), key=len, reverse=True)

    def sanitize_log(self, raw_line: str) -> str:
        safe_line = raw_line
        for val in self._secret_values:
            safe_line = safe_line.replace(val, "***")
        return safe_line

masker = CIRunnerLogMasker({"DB_PASS": "Sup3rS3cretPg!", "REGISTRY_TOKEN": "ghp_998877665544"})
raw_output = "Connecting to postgres://app:Sup3rS3cretPg!@db:5432 with token ghp_998877665544"
print("Сырой вывод процесса :", raw_output)
print("Безопасный лог в CI  :", masker.sanitize_log(raw_output))
```
"""

NOTES[r"Юнит 7.4 · CI CD\📚 Конспекты\К-194. Пайплайн_ от коммита до продакшена.md"] = r"""📖 Перечитать конспект: Пайплайн: путь кода от коммита до продакшена >>
### 1. Ментальная модель: Многоступенчатая ракета с принципом Fail Fast
Зачем разбивать пайплайн на отдельные этапы (**Stages**: `lint` ➔ `test` ➔ `build` ➔ `deploy`), если можно свалить все команды в один скрипт?
Ответ — инженерный принцип **Fail Fast (Падай быстро и дёшево)**!
- Проверка синтаксиса и стиля (`ruff check`) занимает **2 секунды**.
- Поднятие тестовой базы Postgres и прогон 500 интеграционных тестов занимает **2 минуты**.
- Сборка Docker-образа и деплой занимают **3 минуты**.
Если разработчик забыл закрыть скобку или нарушил типизацию, пайплайн должен оборваться уже на **2-й секунде** на этапе `Lint`, не тратя впустую ресурсы серверов на сборку образов и запуск тяжёлых баз данных!

```text
Этап 1: LINT (3 сек)       Этап 2: TEST (60 сек)       Этап 3: BUILD (45 сек)     Этап 4: DEPLOY (20 сек)
┌──────────────────┐       ┌────────────────────┐      ┌────────────────────┐     ┌────────────────────┐
│ • ruff check     │ ──►   │ • pytest unit      │ ──►  │ • docker build     │ ──► │ • alembic upgrade  │
│ • mypy src/      │       │ • pytest + postgres│      │ • trivy scan       │     │ • rolling update   │
└──────────────────┘       └────────────────────┘      └────────────────────┘     └────────────────────┘
 (Упал? Стоп за 3с!)        (Упал? Стоп до сборки!)     (Один образ на все среды!)  (Zero-downtime!)
```

---
### 2. Золотое правило артефакта: «Собирай один раз — деплой везде!»
Частая архитектурная ошибка: на этапе `Test` тестировать один код, на этапе `Staging` собирать Docker-образ заново, а перед `Production` делать ещё один `docker build`. Между этими сборками может обновиться транзитивная библиотека в интернете, и на прод попадёт непроверенный бинарник!
Правильная архитектура: **Docker-образ собирается ровно ОДИН раз** с неизменяемым тегом `sha-коммита`, проверяется и затем **тот же самый образ** последовательно раскатывается на `Staging` и `Production`.

| Stage (Этап) | Инструменты Python-стека | Время выполнения | Критерий перехода дальше |
| :--- | :--- | :--- | :--- |
| **1. Static Analysis (`lint`)** | `ruff check`, `ruff format --check`, `mypy`, `bandit` | **2–10 сек** | `0` ошибок стиля, типов и уязвимостей кода |
| **2. Automated Tests (`test`)** | `pytest --cov=src --cov-fail-under=80` + сервис `postgres` | **30–120 сек** | Все тесты `PASSED`, покрытие $\ge 80\%$ |
| **3. Package (`build`)** | `docker build`, `docker push` в реестр с тегом `$COMMIT_SHA` | **20–60 сек** | Образ успешно сохранён в Container Registry |
| **4. Release (`deploy`)** | `alembic upgrade head` + обновление тега в K8s / Compose + `Smoke Test` | **15–40 сек** | Эндпоинт `/health/ready` вернул `200 OK` |

---
### 3. Миграции БД и авто-откат (Rollback) при деплое
> **Junior vs Senior**:
> - **Junior**: Сначала выкатывает новый код, который обращается к новой колонке `users.phone`, а только потом вручную запускает `alembic upgrade head`. В течение 30 секунд между этими действиями все пользователи сайта получают `500 Internal Server Error (UndefinedColumn)`!
> - **Senior**: Встраивает обратно-совместимую миграцию `alembic upgrade head` как автоматический шаг `pre-deploy` перед переключением трафика на новые контейнеры, а сразу после деплоя проверяет `/health` — и если он не отвечает `200 OK`, пайплайн сам делает автоматический откат (`Rollback`).

---
### 4. Живая проверка: конвейер этапов с принципом Fail Fast
Проверим на Python, сколько серверного времени экономит принцип Fail Fast при ошибке линтера на первом этапе:

```python
def execute_pipeline(stages: list[tuple[str, int, bool]]) -> dict:
    spent_sec = 0
    total_possible_sec = sum(dur for _, dur, _ in stages)
    for name, duration_sec, passed in stages:
        spent_sec += duration_sec
        if not passed:
            saved = total_possible_sec - spent_sec
            return {"status": f"FAILED at '{name}'", "spent_sec": spent_sec, "saved_sec": saved}
    return {"status": "DEPLOYED TO PROD 🚀", "spent_sec": spent_sec, "saved_sec": 0}

broken_lint_run = [("1.lint", 3, False), ("2.pytest", 90, True), ("3.docker_build", 50, True), ("4.deploy", 25, True)]
success_run     = [("1.lint", 3, True),  ("2.pytest", 90, True), ("3.docker_build", 50, True), ("4.deploy", 25, True)]

print("Запуск с ошибкой типа в mypy:", execute_pipeline(broken_lint_run))
print("Чистый релизный запуск      :", execute_pipeline(success_run))
```
"""

NOTES[r"Юнит 7.4 · CI CD\📚 Конспекты\К-195. Переменные окружения в Linux.md"] = r"""📖 Перечитать конспект: Переменные окружения в Linux и Python: export, env и .env >>
### 1. Ментальная модель: Табличка с инструкциями, которую родитель даёт ребёнку в рюкзак
Откуда ваш Python-сервер знает, к какой базе подключаться (`localhost` на ноутбуке или `prod-db.internal` на сервере), если код в обоих случаях абсолютно одинаковый?
Из **переменных окружения (Environment Variables)**! В операционной системе Linux у каждого процесса есть невидимый словарь строк `КЛЮЧ=ЗНАЧЕНИЕ`. Когда родительский процесс (например, терминал `bash` или демон `Docker`) запускает дочерний процесс (`python main.py`), он кладёт копию своих экспортированных переменных ему «в рюкзак».

```text
[Терминал Bash]
  ├── PORT=8000          (обычная локальная переменная — НЕ передаётся детям!)
  └── export DB_HOST=db  (экспортированная переменная — копируется в рюкзак всем детям!)
         │
         ▼ запускает дочерний процесс
[python main.py] ──► os.environ["DB_HOST"] == "db" ✅ (а PORT внутри Python не виден!)
```

---
### 2. Разница между локальной переменной шелла, `export` и одноразовой передачей
В Linux есть три способа задать переменную в командной строке, и каждый ведёт себя по-своему:

```bash
# 1. Локальная переменная оболочки (видна ТОЛЬКО самому bash, в Python НЕ попадёт!):
APP_ENV="local"

# 2. Экспортированная переменная (живёт в текущей сессии терминала и передаётся всем дочерним процессам):
export DATABASE_URL="postgresql://app:secret@localhost:5432/shop"
python main.py

# 3. Одноразовая передача переменной ТОЛЬКО для одной конкретной команды:
LOG_LEVEL="DEBUG" pytest tests/

# Посмотреть все переменные окружения текущей сессии:
env | grep DATABASE_URL
```

| Способ задания | Команда в терминале | Видит ли её `os.environ` в Python? | Как долго живёт? |
| :--- | :--- | :--- | :--- |
| Без `export` | `FOO=bar` | **Нет!** (только сам скрипт `bash`) | До закрытия окна терминала |
| Через `export` | `export FOO=bar` | **Да!** (во всех процессах этого терминала) | До закрытия окна терминала |
| Перед командой | `FOO=bar python app.py` | **Да!** (только внутри этого запуска `app.py`) | Только на время выполнения команды |
| Файл `.env` + Docker | `docker run --env-file .env` | **Да!** (Docker инжектирует их в контейнер) | Всё время жизни контейнера |

---
### 3. Ловушка строковой типизации: почему `bool(os.getenv("DEBUG"))` всегда `True`?!
Все переменные окружения в ОС Linux — это **исключительно строки (`str`)**!

> **Junior vs Senior**:
> - **Junior**: Пишет в `.env` строчку `DEBUG=False`, а в Python-коде проверяет `if bool(os.getenv("DEBUG")):`. Так как непустая строка `"False"` в Python при вызове `bool("False")` даёт **`True`**, джун случайно включает отладочный режим `DEBUG=True` на боевом продакшен-сервере!
> - **Senior**: Никогда не кастует строки из `os.environ` через `bool()`. Он использует **`pydantic-settings` (`BaseSettings`)** или явно сравнивает нормализованную строку: `os.getenv("DEBUG", "false").strip().lower() in ("1", "true", "yes")` и падает на старте (`Fail Fast`), если обязательная переменная не задана.

---
### 4. Живая проверка: безопасный типизированный парсер окружения в стиле `BaseSettings`
Продемонстрируем ловушку `bool("False")` и напишем надёжный валидатор конфигурации окружения на Python:

```python
def parse_env_config(raw_env: dict[str, str]) -> dict[str, object]:
    missing = [k for k in ("DATABASE_URL", "SECRET_KEY") if not raw_env.get(k)]
    if missing:
        raise RuntimeError(f"Отсутствуют обязательные переменные окружения: {missing}")
    debug_str = raw_env.get("DEBUG", "false").strip().lower()
    return {
        "database_url": raw_env["DATABASE_URL"],
        "debug": debug_str in {"1", "true", "yes", "on"},
        "port": int(raw_env.get("PORT", "8000")),
    }

prod_env = {"DATABASE_URL": "postgresql://db:5432/prod", "SECRET_KEY": "k99", "DEBUG": "False", "PORT": "8080"}
print(f"Ловушка новичка bool('False') -> {bool(prod_env['DEBUG'])} (ОПАСНО!)")
print(f"Правильный парсер сеньора     -> {parse_env_config(prod_env)}")
```
"""

NOTES[r"Юнит 7.4 · CI CD\📚 Конспекты\К-196. GitHub Actions и GitLab CI_ конкретные.md"] = r"""📖 Перечитать конспект: GitHub Actions и GitLab CI: боевые YAML-конфигурации >>
### 1. Ментальная модель: Рецепт для робота-сборщика в папке репозитория
Две самые популярные системы CI/CD в мире — это **GitHub Actions** и **GitLab CI**. Обе управляются декларативными YAML-файлами, которые лежат прямо в вашем репозитории:
- В **GitHub Actions** файлы сценариев (Workflows) кладутся в папку **`.github/workflows/ci.yml`**.
- В **GitLab CI** вся конфигурация описывается в одном корневом файле **`.gitlab-ci.yml`**.

```text
Структура GitHub Actions (.github/workflows/ci.yml):
[ Событие on: push / pull_request ]
         │
         ▼
[ Job: test (runs-on: ubuntu-latest) ]
  ├── Services : поднимает фоновый контейнер postgres:16
  ├── Step 1   : actions/checkout@v4      (скачивает код репозитория)
  ├── Step 2   : actions/setup-python@v5  (ставит Python 3.13 + кэш pip)
  ├── Step 3   : run: ruff check && mypy  (статический анализ)
  └── Step 4   : run: pytest              (прогон тестов с реальной БД)
```

---
### 2. Готовый боевой пайплайн GitHub Actions с сервисом PostgreSQL
Обратите внимание на блок `services: postgres:` — GitHub Actions сам поднимет рядом с вашим кодом настоящий контейнер PostgreSQL 16, дождётся его готовности (`pg_isready`) и пробросит порт `5432` для ваших интеграционных тестов!

```yaml
name: Python Backend CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 5s
          --health-timeout 3s
          --health-retries 5

    steps:
      - name: Скачать код репозитория
        uses: actions/checkout@v4

      - name: Установить Python 3.13 с кэшированием pip
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: "pip"

      - name: Установить зависимости
        run: pip install -r requirements.txt

      - name: Проверить качество кода и тесты
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
        run: |
          ruff check src/ tests/
          pytest -v
```

| Концепция | Как пишется в **GitHub Actions** | Как пишется в **GitLab CI** |
| :--- | :--- | :--- |
| **Путь к файлу** | `.github/workflows/ci.yml` | `.gitlab-ci.yml` (в корне проекта) |
| **Триггер запуска** | `on: [push, pull_request]` | `rules:` / `workflow:` |
| **Выбор окружения** | `runs-on: ubuntu-latest` + `setup-python` | `image: python:3.13-slim` |
| **Готовый плагин vs скрипт** | `uses: actions/checkout@v4` vs `run: pytest` | Автоматический git clone + `script: [pytest]` |
| **Фоновая БД для тестов** | `services: postgres: image: postgres:16` | `services: - postgres:16-alpine` |

---
### 3. Тонкости написания надёжных пайплайнов
> **Junior vs Senior**:
> - **Junior**: Не включает `cache: "pip"` в `setup-python`, использует плавающие версии экшенов без мажорного тега или тестирует SQL-запросы на `SQLite in-memory` вместо `services: postgres`, пропуская ошибки специфичных типов PostgreSQL (`JSONB`, `ARRAY`, `UUID`).
> - **Senior**: Включает кэширование `pip`/`uv`, поднимает в CI настоящий сервис `postgres:16-alpine` с `--health-cmd pg_isready`, использует `strategy: matrix` (если библиотеку нужно проверить на Python 3.11, 3.12 и 3.13 одновременно) и задаёт `timeout-minutes: 10`, чтобы зависший тест не сжёг все бесплатные минуты аккаунта.

---
### 4. Живая проверка: генератор матрицы запуска (`strategy.matrix`) и валидатор Workflow
Напишем на Python анализатор конфигурации CI, который разворачивает матрицу тестирования (`Python x OS`) и проверяет наличие `healthcheck` у сервисных контейнеров:

```python
import itertools

def expand_ci_matrix(python_versions: list[str], os_list: list[str], has_pg_healthcheck: bool) -> dict:
    jobs = [f"test (py={py}, os={os_name})" for py, os_name in itertools.product(python_versions, os_list)]
    return {
        "total_parallel_jobs": len(jobs),
        "jobs": jobs,
        "db_ready_safe": has_pg_healthcheck,
    }

matrix_plan = expand_ci_matrix(["3.12", "3.13"], ["ubuntu-latest"], has_pg_healthcheck=True)
print(f"Сгенерировано параллельных задач ({matrix_plan['total_parallel_jobs']}): {matrix_plan['jobs']}")
print(f"Защита от гонки старта PostgreSQL: {'ВКЛЮЧЕНА ✅' if matrix_plan['db_ready_safe'] else 'НЕТ ❌'}")
```
"""

NOTES[r"Юнит 7.4 · CI CD\📚 Конспекты\К-197. Секреты и переменные окружения.md"] = r"""📖 Перечитать конспект: Секреты и переменные окружения: архитектура безопасности (12-Factor) >>
### 1. Ментальная модель: Одинаковый сейф, но разные ключи на каждом этаже
Третий закон манифеста **The Twelve-Factor App** гласит: **Храните конфигурацию в окружении!**
Если сделать `git clone` вашего репозитория прямо сейчас и выложить его в открытый доступ на GitHub, ни один пароль от базы данных, ключ Stripe или приватный ключ JWT не должен быть раскрыт.
В промышленной разработке настройки делятся на два класса:
1. **Публичная конфигурация (`Config`)** — несекретные параметры, меняющиеся от среды к среде (`LOG_LEVEL=INFO`, `WORKERS=4`, `REDIS_HOST=redis`). В Kubernetes хранятся в `ConfigMap`.
2. **Секреты (`Secrets`)** — чувствительные учётные данные (`DB_PASSWORD`, `STRIPE_API_KEY`, `JWT_PRIVATE_KEY`). Хранятся в GitHub Secrets / HashiCorp Vault / K8s `Secret` и передаются в контейнер только в момент запуска!

```text
Локальная разработка (Laptop)     CI/CD Пайплайн (GitHub)         Продакшен (K8s / Vault)
┌───────────────────────────┐     ┌───────────────────────────┐   ┌───────────────────────────┐
│ Файл .env (в .gitignore!) │     │ GitHub Actions Secrets    │   │ Vault / K8s Secret        │
└─────────────┬─────────────┘     └─────────────┬─────────────┘   └─────────────┬─────────────┘
              └─────────────────────────┐       │       ┌───────────────────────┘
                                        ▼       ▼       ▼
                            [ Единый Python-код: Settings(BaseSettings) ]
```

---
### 2. Почему `ARG` и `ENV` в `Dockerfile` НЕЛЬЗЯ использовать для секретов?
Огромная ошибка безопасности — передавать приватный токен во время сборки образа через `docker build --build-arg SECRET_TOKEN=xyz`.
Почему это опасно? Потому что каждый шаг сборки и все значения `ARG` / `ENV` **навсегда записываются в метаданные образа**! Любой человек, скачавший образ, выполнит команду **`docker history --no-trunc myapp`** и увидит ваш пароль открытым текстом!

| Место хранения | Безопасно ли для паролей/ключей? | Почему? |
| :--- | :--- | :--- |
| В коде (`API_KEY = "sk_live_..."`) | **КАТЕГОРИЧЕСКИ НЕТ 🛑** | Навсегда остаётся в истории `git log`, утекает при клонировании |
| В `Dockerfile` (`ENV` или `ARG`) | **НЕТ 🛑** | Видно всем через `docker history` и `docker inspect` |
| Runtime-переменная (`docker run -e`) | **Да ✅** | Живёт только в памяти запущенного процесса контейнера |
| Docker Secrets / Vault (`/run/secrets/db_pass`) | **Эталон безопасности 🏆** | Монтируется как `tmpfs`-файл в RAM, не светится даже в `docker inspect` |

---
### 3. Ротация секретов и принцип наименьших привилегий
> **Junior vs Senior**:
> - **Junior**: Использует один и тот же суперпользовательский пароль `postgres` и один API-ключ платежной системы и для локальных тестов на ноутбуке, и для CI, и для продакшена.
> - **Senior**: Строго изолирует ключи по средам (на ноутбуке и в CI — только тестовые `sk_test_...` ключи песочницы, на проде — боевые `sk_live_...` с минимальными правами), а для чтения секретов поддерживает загрузку как из `ENV`, так и из файлов `/run/secrets/<name>`.

---
### 4. Живая проверка: сканер утечек секретов (Secret Scanner) для pre-commit хука
Напишем на Python детектор захардкоженных ключей (подобный утилитам `gitleaks` / `trufflehog`), который не даёт закоммитить секреты в Git:

```python
import re

SECRET_PATTERNS = {
    "Stripe Live Key": re.compile(r"sk_live_[0-9a-zA-Z]{10,}"),
    "GitHub Token": re.compile(r"ghp_[0-9a-zA-Z]{10,}"),
    "Hardcoded Password": re.compile(r"(?i)(password|secret_key)\s*=\s*['\"][^'\"]{6,}['\"]"),
}

def scan_code_for_secrets(code_lines: list[str]) -> list[str]:
    findings: list[str] = []
    for line_no, line in enumerate(code_lines, start=1):
        if "os.getenv" in line or "os.environ" in line:
            continue
        for rule_name, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                findings.append(f"Строка {line_no}: обнаружен '{rule_name}'!")
    return findings

sample_code = [
    "import os",
    "DB_PASSWORD = os.getenv('DB_PASSWORD')",          # Безопасно!
    "STRIPE_KEY = 'sk_live_9876543210abcdef'",         # УТЕЧКА!
]
print("Результат сканирования коммита:", scan_code_for_secrets(sample_code))
```
"""

# ==============================================================================
# ЮНИТ 7.5 · LINUX И UNIX (К-198 .. К-203)
# ==============================================================================

NOTES[r"Юнит 7.5 · Linux и Unix\📚 Конспекты\К-198. Командная строка Linux_ навигация и.md"] = r"""📖 Перечитать конспект: Командная строка Linux: навигация, устройство ФС и права chmod >>
### 1. Ментальная модель: Единое дерево папок от корня `/` и три уровня пропуска (`rwx`)
В Windows у каждого диска своя буква (`C:\`, `D:\`). В Linux и Unix всё устроено как **единое дерево**, растущее из одного главного корня **`/` (root slash)**. Все ваши Docker-контейнеры и 99.9% продакшен-серверов работают на Linux, где нет мышки и графических окон — только терминал!
А безопасность каждого файла защищена **тремя группами прав** (для **Владельца `u`**, **Группы `g`** и **Остальных `o`**), где каждое действие кодируется весом бита:
- **`r` (Read — чтение) = `4`**
- **`w` (Write — запись) = `2`**
- **`x` (Execute — запуск скрипта / вход в папку) = `1`**

```text
Разбор строки из ls -la:
  -   rwx   r-x   ---   1 appuser backend  4096 Oct 03 12:00 deploy.sh
  │   └┬┘   └┬┘   └┬┘     └──┬──┘ └──┬──┘
 Тип  User  Group Others   Владелец Группа
файла 4+2+1 4+0+1 0+0+0
       =7    =5    =0   ──► Права в восьмеричном виде: chmod 750 deploy.sh
```

---
### 2. Карта главных директорий Linux и команды навигации
Зайдя на любой сервер по SSH или внутрь Docker-контейнера, вы сразу ориентируетесь с помощью этих команд:

```bash
pwd                     # Где я сейчас? (Print Working Directory, например /app/src)
ls -la                  # Показать ВСЕ файлы (включая скрытые с точкой .env) + права и размеры
cd /var/log/nginx       # Перейти по абсолютному пути от корня /
cd -                    # Мгновенно вернуться в предыдущую папку

# Сделать скрипт запуска исполняемым (добавить бит +x):
chmod +x entrypoint.sh

# Защитить приватный SSH-ключ (чтение и запись ТОЛЬКО владельцу: 4+2=6, остальным 0):
chmod 600 ~/.ssh/id_ed25519

# Сменить владельца папки приложения внутри контейнера:
chown -R appuser:appuser /app
```

| Директория Linux | Что там хранится? | Пример для бэкенд-разработчика |
| :--- | :--- | :--- |
| **`/etc`** | Конфигурационные файлы системы и сервисов | `/etc/nginx/nginx.conf`, `/etc/systemd/system/` |
| **`/var/log`** | Системные и серверные логи | `/var/log/nginx/error.log`, `/var/log/syslog` |
| **`/tmp`** | Временные файлы (очищаются при перезагрузке) | Сокеты, временные выгрузки отчётов |
| **`/home/<user>` (`~`)** | Домашняя папка пользователя (`root` живёт в `/root`) | `~/.ssh/authorized_keys`, `~/.bashrc` |
| **Права `755` vs `600`** | `755` (`rwxr-xr-x`) — для скриптов и папок; `600` (`rw-------`) — для секретов и ключей | SSH откажется работать, если у ключа права шире `600`! |

---
### 3. Почему `chmod 777` — это преступление против безопасности?
> **Junior vs Senior**:
> - **Junior**: Увидев ошибку `Permission denied` при записи лога или запуске скрипта, не глядя пишет `sudo chmod -R 777 /app`. Код `777` (`rwxrwxrwx`) разрешает **любому процессу и любому пользователю** на сервере изменять ваш исходный код и внедрять вредоносные команды!
> - **Senior**: Выясняет, от какого пользователя запущен процесс (`whoami` / `id`), выстраивает правильного владельца через `chown -R appuser:appuser /app` и выдаёт минимально необходимые права: **`644`** для обычных файлов, **`755`** для директорий и бинарников, **`600`** для секретов.

---
### 4. Живая проверка: калькулятор прав `chmod` (Octal $\leftrightarrow$ Symbolic `rwx`)
Напишем на Python конвертер восьмеричных прав Linux (например, `750`, `600`, `644`) в символьную строку `rwxr-x---` и проверку безопасности:

```python
def octal_to_rwx(octal_str: str) -> str:
    bits = [(4, "r"), (2, "w"), (1, "x")]
    result = []
    for digit_char in octal_str:
        val = int(digit_char)
        result.append("".join(letter if (val & bit) else "-" for bit, letter in bits))
    return "".join(result)

for mode, target in [("755", "entrypoint.sh"), ("644", "config.py"), ("600", "id_ed25519"), ("777", "danger.py")]:
    rwx = octal_to_rwx(mode)
    world_writable = (int(mode[2]) & 2) != 0
    warn = "🛑 ОПАСНО (запись открыта всем!)" if world_writable else "✅ Безопасно"
    print(f"chmod {mode} ({rwx}) для {target:<14} -> {warn}")
```
"""

NOTES[r"Юнит 7.5 · Linux и Unix\📚 Конспекты\К-199. Работа с файлами в Linux.md"] = r"""📖 Перечитать конспект: Работа с файлами и диском в Linux: tail, less, df, du >>
### 1. Ментальная модель: Хирургический скальпель вместо выгрузки самосвалом
Представьте: на продакшен-сервере лежит лог-файл `app.log` весом **15 Гигабайт**.
Если вы попытаетесь открыть его командой `cat app.log` или текстовым редактором `nano`, сервер попытается прочитать все 15 ГБ и зависнет от нехватки памяти!
В Linux для работы с файлами и диском есть специализированные потоковые утилиты, которые читают только нужный кусочек файла с конца или по страничке:

```text
Огромный файл app.log (15 ГБ):
├── Начало файла (первые 20 строк) ──► head -n 20 app.log
├── Постраничное чтение с поиском  ──► less app.log  (клавиша /ERROR для поиска)
└── Живой хвост в реальном времени ──► tail -n 100 -f app.log (следит за новыми записями!)
```

---
### 2. Инспекция файлов и расследование «Куда пропало место на диске?!»
Вторая классическая авария на бэкенде — ошибка `OSError: [Errno 28] No space left on device` (закончилось место на диске, из-за чего падает PostgreSQL). Для мгновенной диагностики нужны три команды: **`df`**, **`du`** и **`find`**.

```bash
# 1. Просмотр логов (живая подписка на последние 50 строк файла):
tail -n 50 -f /var/log/nginx/error.log

# 2. Безопасное создание цепочки вложенных папок (не упадёт, если папка уже есть):
mkdir -p /app/storage/uploads/2026

# 3. Сколько свободного места осталось на всех дисках (в понятных ГБ/МБ, флаг -h):
df -h

# 4. Проверить, не закончились ли индексные дескрипторы (inodes) из-за миллионов мелких файлов:
df -i

# 5. Найти, какая именно папка внутри /var съела больше всего гигабайт:
du -sh /var/* | sort -hr | head -n 5
```

| Утилита Linux | Что делает? | Почему флаг важен? |
| :--- | :--- | :--- |
| **`tail -f file.log`** | Выводит конец файла и в реальном времени допечатывает новые строки | Идеально для мониторинга логов при тестировании |
| **`less file.log`** | Открывает гигабайтный файл мгновенно (читает буфером по 1 экрану) | Не грузит RAM (в отличие от `cat` и `vim`) |
| **`df -h` (Disk Free)** | Показывает общую заполненность смонтированных разделов диска | Показывает картину за $0.01$ сек по суперблоку ФС |
| **`du -sh *` (Disk Usage)** | Суммирует реальный вес конкретных папок и файлов внутри директории | Позволяет найти папку-виновника переполнения диска |

---
### 3. Загадка «Диск полон на 100% в `df -h`, хотя `du -sh` показывает всего 2 ГБ!»
Этот вопрос на собеседованиях отличает инженера с реальным продакшен-опытом от теоретика.

> **Junior vs Senior**:
> - **Junior**: Видит, что файл `app.log` разросся до 40 ГБ, удаляет его командой `rm /var/log/app.log`, смотрит в `df -h` — а место на диске **НЕ освободилось** (всё ещё 100% занято)! Джун в панике перезагружает весь сервер.
> - **Senior**: Знает устройство файловой системы Unix: пока запущенный процесс (например, Python или Nginx) держит открытым файловый дескриптор удалённого файла, ядро Linux **не освобождает блоки на диске**! Сеньор либо находит процесс через `lsof +L1` и посылает ему сигнал переоткрыть лог, либо обнуляет живой файл без удаления дескриптора командой **`truncate -s 0 /var/log/app.log`**.

---
### 4. Живая проверка: чтение «хвоста» лога (`tail`) и диагностика диска на Python
Напишем на Python эффективный алгоритм `tail(n)` (через кольцевой буфер `collections.deque` с памятью $O(N)$) и детектор скрытых удалённых файлов (`open unlinked files`):

```python
from collections import deque

def tail_lines(stream_lines: list[str], n: int = 3) -> list[str]:
    # deque(maxlen=n) хранит в памяти ровно n последних строк даже на файле в 100 ГБ!
    return list(deque(stream_lines, maxlen=n))

def diagnose_disk_discrepancy(total_gb: int, df_used_gb: int, du_visible_gb: int) -> str:
    ghost_gb = df_used_gb - du_visible_gb
    if ghost_gb > 1:
        return f"ВНИМАНИЕ: {ghost_gb} ГБ удерживаются открытыми дескрипторами удалённых файлов (проверьте lsof +L1)!"
    return f"ОК: свободно {total_gb - df_used_gb} ГБ."

log_stream = [f"2026-10-03 12:00:0{i} INFO request #{i}" for i in range(1, 10)]
print("Последние 3 строки (tail -n 3):", tail_lines(log_stream, n=3))
print("Аудит диска после rm app.log  :", diagnose_disk_discrepancy(total_gb=50, df_used_gb=48, du_visible_gb=8))
```
"""

NOTES[r"Юнит 7.5 · Linux и Unix\📚 Конспекты\К-200. Управление процессами в Linux.md"] = r"""📖 Перечитать конспект: Управление процессами в Linux: PID, сигналы SIGTERM/SIGKILL, systemd >>
### 1. Ментальная модель: Вежливая просьба закрыть смену (`SIGTERM`) vs Рубильник (`SIGKILL`)
Каждая запущенная программа в Linux (ваш Uvicorn, воркер Celery, PostgreSQL) — это **процесс** со своим уникальным номером **`PID` (Process ID)**.
Как правильно остановить работающий бэкенд-сервер при выкатке новой версии? В Linux процессы общаются через **Сигналы (Signals)**. И разница между сигналами `15` и `9` — это разница между штатным сохранением транзакций и сломанной базой данных:

```text
Деплой новой версии (docker stop / systemctl stop):
1. Посылается сигнал SIGTERM (15) ──► Python перехватывает сигнал:
                                       • перестаёт брать новые HTTP-запросы;
                                       • досчитывает текущие оплаты (2 сек);
                                       • закрывает пул коннектов к БД и выходит с кодом 0! ✅
2. Если процесс завис наглухо (>10 сек):
   Ядро шлёт SIGKILL (9)          ──► Процесс мгновенно уничтожается ядром ОС
                                       (перехватить НЕЛЬЗЯ, транзакции рвутся!). 🛑
```

---
### 2. Команды мониторинга процессов, портов и служба `systemd`
Как узнать, какой процесс съел 100% CPU или кто уже занял порт `8000` (`Address already in use`)?

```bash
# 1. Найти PID всех запущенных процессов Python/Uvicorn:
ps aux | grep uvicorn
pgrep -af uvicorn

# 2. Узнать, какой процесс и с каким PID слушает порт 8000:
ss -tulpn | grep :8000
lsof -i :8000

# 3. Вежливо попросить процесс (PID 4812) завершиться штатно (по умолчанию шлёт SIGTERM -15!):
kill 4812

# 4. Принудительно убить зависший процесс через ядро (SIGKILL -9 — только в крайнем случае!):
kill -9 4812

# 5. Управление фоновым демоном через менеджер служб systemd:
sudo systemctl status billing-api
sudo systemctl restart billing-api
sudo journalctl -u billing-api -f     # Чтение живых логов сервиса из systemd
```

| Сигнал Linux | Номер | Команда отправки | Можно ли перехватить в Python (`signal`)? | Назначение в бэкенде |
| :--- | :--- | :--- | :--- | :--- |
| **`SIGINT`** | `2` | Нажатие `Ctrl + C` | **Да** (вызывает `KeyboardInterrupt`) | Остановка сервера в терминале разработчика |
| **`SIGTERM`** | `15` | `kill <PID>` (по умолчанию!) | **Да** (основа **Graceful Shutdown**) | Штатная остановка при деплое в Docker / K8s / systemd |
| **`SIGHUP`** | `1` | `kill -HUP <PID>` | **Да** | Перечитать конфигурацию и переоткрыть воркеры без даунтайма (Gunicorn / Nginx) |
| **`SIGKILL`** | `9` | `kill -9 <PID>` | **НЕТ** (убивает напрямую ядро ОС) | Экстренное уничтожение наглухо зависшего процесса |

---
### 3. Анти-паттерн `kill -9` по привычке
> **Junior vs Senior**:
> - **Junior**: Всегда останавливает процессы командой `kill -9 <PID>`, считая, что `-9` — это просто «обязательный флаг команды `kill`». В результате воркер Celery обрывается посреди списания денег, оставляя заказ в зависшем статусе.
> - **Senior**: Всегда вызывает обычный `kill <PID>` (`SIGTERM`), а в своём Python-сервисе и воркерах настраивает обработчик **Graceful Shutdown** (или `acks_late=True` в Celery), чтобы процесс аккуратно завершил текущую задачу перед выходом.

---
### 4. Живая проверка: обработка `SIGTERM` для Graceful Shutdown на Python
Посмотрим на стандартный модуль `signal` в Python и проверим, как обработчик `SIGTERM` позволяет безопасно завершить активную транзакцию перед остановкой сервера:

```python
import signal

class GracefulWorker:
    def __init__(self) -> None:
        self.should_stop = False
        self.active_tx = "tx_payment_901"

    def handle_sigterm(self, signum: int, _frame) -> None:
        sig_name = signal.Signals(signum).name
        print(f"[Сигнал {sig_name} ({signum})] Получен запрос на остановку! Завершаем текущую транзакцию...")
        self.should_stop = True

    def finish_work(self) -> str:
        if self.should_stop:
            return f"Транзакция {self.active_tx} успешно зафиксирована в БД, пул соединений закрыт. Выход (0)."
        return "Работа продолжается"

worker = GracefulWorker()
worker.handle_sigterm(signal.SIGTERM, None)
print(worker.finish_work())
```
"""

NOTES[r"Юнит 7.5 · Linux и Unix\📚 Конспекты\К-201. Потоки и пайпы в Unix.md"] = r"""📖 Перечитать конспект: Потоки ввода-вывода (stdin, stdout, stderr) и пайпы (|) в Unix >>
### 1. Ментальная модель: Три водопроводные трубы каждого процесса и конструктор Lego (`|`)
В философии Unix каждая программа рождается с тремя подключёнными к ней трубами (стандартными потоками с номерами файловых дескрипторов `0`, `1` и `2`):
- **`0` — `stdin` (Standard Input)**: входная труба, откуда программа читает данные.
- **`1` — `stdout` (Standard Output)**: выходная труба для **нормального результата** работы.
- **`2` — `stderr` (Standard Error)**: отдельная аварийная труба для **ошибок и диагностических логов**.

А символ вертикальной черты **`|` (Pipe — конвейер)** работает как переходник конструктора Lego: он соединяет выходную трубу `stdout` первой программы напрямую со входной трубой `stdin` второй программы прямо в оперативной памяти (без создания временных файлов на диске!).

```text
[Программа 1: cat access.log]
   ├── (2) stderr ──► Выводится на экран (ошибки не смешиваются с данными!)
   └── (1) stdout ═══ Пайп (|) в RAM ═══► (0) stdin [Программа 2: grep " 500 "]
                                                       └── (1) stdout ═══► [wc -l]
```

---
### 2. Операторы перенаправления потоков (`>`, `>>`, `2>&1`) и аналитика логов в 1 строчку
Почему `> file.txt` и `>> file.txt` — это не одно и то же, и что означает магическое заклинание `2>&1`?

```bash
# > ПЕРЕЗАПИСЫВАЕТ файл с нуля (старое содержимое стирается!):
python report.py > daily_report.txt

# >> ДОПИСЫВАЕТ в конец файла (идеально для логов):
python worker.py >> worker.log

# 2> перенаправляет ТОЛЬКО поток ошибок (дескриптор 2) в отдельный файл:
python sync.py > ok.txt 2> errors.log

# 2>&1 направляет ошибки (2) туда же, куда идёт стандартный вывод (&1):
python app.py > full_combined.log 2>&1

# Классический Unix-пайплайн: посчитать ТОП-3 IP-адресов, генерирующих ошибку 500:
grep " 500 " access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 3
```

| Оператор | Что делает? | Важная тонкость |
| :--- | :--- | :--- |
| **`cmd1 \| cmd2`** | Передаёт `stdout` первой команды в `stdin` второй | Обе команды работают **параллельно** через буфер ядра в RAM |
| **`>`** | Перенаправляет `stdout` в файл с **перезаписью** | Ошибки (`stderr`) при этом всё равно выведутся в терминал! |
| **`>>`** | Дописывает `stdout` в конец существующего файла | Безопасно сохраняет предыдущие записи |
| **`2>&1`** | Объединяет поток `stderr` (`2`) с потоком `stdout` (`1`) | Пишется **после** основного перенаправления: `> out.log 2>&1` |
| **`/dev/null`** | «Чёрная дыра» Linux (мгновенно выбрасывает все записанные байты) | `cmd > /dev/null 2>&1` — полная тишина |

---
### 3. Ловушка порядка `2>&1` и код возврата пайплайна (`pipefail`)
> **Junior vs Senior**:
> - **Junior**: Пишет в CI-скрипте `pytest | tee test.log`. Если `pytest` падает с ошибкой (код `1`), но `tee` успешно записывает текст в файл (код `0`), то по умолчанию весь пайплайн возвращает код **последней команды (`0` — УСПЕХ!)**, и сломанный код проходит в продакшен!
> - **Senior**: В начале любого bash-скрипта всегда пишет строгую триаду **`set -euo pipefail`** (где `-o pipefail` заставляет конвейер `|` вернуть ошибку, если упало **любое** звено цепочки!), а в Python разделяет потоки данных (`sys.stdout`) и логов (`sys.stderr`).

---
### 4. Живая проверка: конвейер анализа логов Nginx в стиле Unix Pipe на генераторах Python
В Python аналогом потоковых пайпов Unix (`|`) являются **генераторы**, которые обрабатывают миллионы строк по одной без загрузки файла в память:

```python
from collections import Counter

raw_nginx_logs = [
    "10.0.0.5 GET /api/orders 500",
    "10.0.0.2 GET /api/items 200",
    "10.0.0.5 POST /api/pay 500",
    "10.0.0.9 GET /api/orders 500",
    "10.0.0.5 GET /api/profile 500",
]

# Эквивалент: grep " 500 " | awk '{print $1}' | sort | uniq -c | sort -nr
only_500 = (line for line in raw_nginx_logs if line.endswith(" 500"))
extracted_ips = (line.split()[0] for line in only_500)
top_ips = Counter(extracted_ips).most_common(2)

print("ТОП IP с ошибками 500 (grep 500 | awk | uniq -c):", top_ips)
```
"""

NOTES[r"Юнит 7.5 · Linux и Unix\📚 Конспекты\К-202. SSH.md"] = r"""📖 Перечитать конспект: SSH: криптография ключей, ~/.ssh/config и безопасный туннелинг >>
### 1. Ментальная модель: Навесной замок на сервере (`Public Key`) и Личный ключ в сейфе (`Private Key`)
Как безопасно управлять удалённым Linux-сервером через открытый интернет и почему вход по обычному паролю на продакшене запрещён?
Протокол **SSH (Secure Shell, порт 22)** использует **асимметричную криптографию** — пару математически связанных ключей (рекомендуемый современный алгоритм — **`Ed25519`**):
1. **Публичный ключ (`id_ed25519.pub`)** — это «навесной замок». Его **можно и нужно** передавать на серверы (он записывается в файл `~/.ssh/authorized_keys`) и загружать в профиль GitHub. Украсть замок бесполезно — им ничего нельзя открыть!
2. **Приватный ключ (`id_ed25519`, без `.pub`)** — это «единственный ключ от замка». Он хранится **строго на вашем ноутбуке** с правами `chmod 600` и защищён парольной фразой (`passphrase`). Он **никогда не покидает ваш компьютер**!

```text
Ваш Ноутбук (~/.ssh/id_ed25519)                 Продакшен Сервер (~/.ssh/authorized_keys)
┌──────────────────────────────┐                ┌────────────────────────────────────────┐
│ Приватный ключ (СЕКРЕТ!)     │                │ Публичный ключ ("замок" id_ed25519.pub)│
│ Подписывает случайный вызов ◄┼─── Challenge ──┼─ Генерирует случайное число            │
│ криптографической подписью   ├─── Signature ─►│ Проверяет подпись публичным ключом ✅   │
└──────────────────────────────┘                └────────────────────────────────────────┘
```

---
### 2. Генерация ключей `Ed25519`, удобный `~/.ssh/config` и SSH-туннель к закрытой БД
Как подключиться со своего ноутбука через DBeaver/pgAdmin к базе PostgreSQL, если на продакшен-сервере порт `5432` мудро закрыт от интернета и слушает только `127.0.0.1:5432`?
Через **SSH Local Port Forwarding (`ssh -L`)** — зашифрованный туннель внутри SSH-соединения!

```bash
# 1. Сгенерировать современную криптостойкую пару ключей Ed25519:
ssh-keygen -t ed25519 -C "dev@company.com"

# 2. Скопировать ТОЛЬКО публичный ключ (.pub) на сервер одной командой:
ssh-copy-id -i ~/.ssh/id_ed25519.pub deploy@203.0.113.10

# 3. Пробросить безопасный SSH-туннель к закрытой БД сервера:
# Локальный порт 15432 на ноутбуке -> через SSH -> 127.0.0.1:5432 внутри сервера!
ssh -N -L 15432:127.0.0.1:5432 deploy@203.0.113.10
```

А чтобы не вводить каждый раз `ssh -i ~/.ssh/id_ed25519 -p 2222 deploy@203.0.113.10`, создайте на ноутбуке файл **`~/.ssh/config`** — и подключайтесь короткой командой **`ssh prod`**:

```text
Host prod
    HostName 203.0.113.10
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

| Инструмент SSH | Команда / Файл | Зачем нужен бэкенд-разработчику? |
| :--- | :--- | :--- |
| **`ssh-keygen -t ed25519`** | Создаёт `id_ed25519` и `id_ed25519.pub` | Быстрее, короче и безопаснее устаревшего `rsa-2048` |
| **`~/.ssh/authorized_keys`** | Список допущенных `.pub` ключей на сервере | Позволяет пускать разработчиков без пароля ОС |
| **`ssh -L 15432:localhost:5432`** | Локальный проброс порта (SSH Tunnel) | Безопасный доступ к закрытым в внутренней сети Postgres / Redis |
| **`scp` / `rsync -avz`** | Копирование файлов поверх SSH | Доставка дампов БД с докачкой и сжатием (`rsync`) |

---
### 3. Безопасность SSH-сервера (`sshd_config`)
> **Junior vs Senior**:
> - **Junior**: Оставляет на арендованном VPS вход под пользователем `root` по паролю или путает файлы, отправляя коллеге в чат свой приватный ключ `id_ed25519` вместо `id_ed25519.pub`.
> - **Senior**: В первый же день настройки сервера отключает в `/etc/ssh/sshd_config` вход по паролю (`PasswordAuthentication no`) и прямой вход рута (`PermitRootLogin no`), оставляя вход только по `Ed25519`-ключам, а к закрытой БД подключается исключительно через `ssh -L` туннель.

---
### 4. Живая проверка: аудитор безопасности SSH-конфигурации и прав на ключи
Напишем на Python проверку, имитирующую строгий контроль прав файла ключа `OpenSSH` (`Permissions 0644 for 'id_ed25519' are too open`):

```python
def verify_ssh_security(key_filename: str, octal_perms: str, sshd_config: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if key_filename.endswith(".pub"):
        errors.append("Для подключения (-i) нужен приватный ключ, а не публичный (.pub)")
    if octal_perms not in ("600", "400"):
        errors.append(f"UNPROTECTED PRIVATE KEY FILE! Права {octal_perms} слишком открыты (требуется chmod 600)")
    if sshd_config.get("PasswordAuthentication") != "no":
        errors.append("Риск брутфорса: отключите PasswordAuthentication в /etc/ssh/sshd_config")
    if sshd_config.get("PermitRootLogin") != "no":
        errors.append("Риск взлома: отключите прямой вход root (PermitRootLogin no)")
    return errors or ["OK ✅: Конфигурация SSH полностью защищена!"]

print("Слишком открытые права 644:", verify_ssh_security("id_ed25519", "644", {"PasswordAuthentication": "no", "PermitRootLogin": "no"}))
print("Эталонная настройка 600   :", verify_ssh_security("id_ed25519", "600", {"PasswordAuthentication": "no", "PermitRootLogin": "no"}))
```
"""

NOTES[r"Юнит 7.5 · Linux и Unix\📚 Конспекты\К-203. Nginx и обратный прокси_ что стоит перед.md"] = r"""📖 Перечитать конспект: Nginx и обратный прокси (Reverse Proxy): щит перед Python-сервером >>
### 1. Ментальная модель: Охранник-ресепшионист (`Nginx`) перед кабинетом хирурга (`Uvicorn/Gunicorn`)
Почему в продакшене **никогда** не выставляют `Uvicorn` или `Gunicorn` напрямую в интернет на порт `80`/`443`, а всегда ставят перед ними **Nginx**?
Python-сервер (`Uvicorn` / `Gunicorn`) — это высокооплачиваемый хирург: он великолепно выполняет сложную бизнес-логику, но если злоумышленник откроет 1000 медленных соединений по мобильному 2G-интернету (атака *Slowloris*) или попросит раздать 50 картинок, воркеры Python окажутся заблокированы!
**Nginx** выступает как **Reverse Proxy (Обратный прокси)** — молниеносный ресепшионист на входе:
1. Сам расшифровывает HTTPS/TLS-сертификаты (**SSL Termination**).
2. Сам за 0.1 мс отдаёт статику (`/static/`, `/media/`) напрямую с диска, вообще не отвлекая Python.
3. Полностью буферизует медленный запрос клиента и за 1 миллисекунду передаёт готовый пакет в `Uvicorn`, балансируя нагрузку между несколькими контейнерами!

```text
Интернет (Клиенты)
       │  HTTPS (:443)
       ▼
┌──────────────────────────────────────────────────────────┐
│ Nginx (Reverse Proxy)                                    │
│  ├── /static/*  ──► Отдаёт файлы с диска за 0.1 мс       │
│  └── /api/*     ──► proxy_pass + заголовки X-Forwarded-* │
└───────────────────────────────┬──────────────────────────┘
                                │ Внутренняя сеть Docker (:8000)
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
        [ Uvicorn Worker 1 ]          [ Uvicorn Worker 2 ]
```

---
### 2. Конфигурация `nginx.conf` и зачем нужны заголовки `X-Forwarded-For`?
Когда Nginx пересылает запрос вашему FastAPI/Django, для самого Python-сервера источником TCP-соединения становится **IP-адрес контейнера Nginx (`172.18.0.2`)**! Чтобы Python знал **настоящий IP клиента** (для логов и Rate Limiting) и схему (`https`), Nginx обязан прикрепить заголовки `X-Real-IP` и `X-Forwarded-For`:

```nginx
upstream backend_api {
    least_conn;                  # Балансировка: отправлять запрос наименее загруженному воркеру
    server api-1:8000;
    server api-2:8000;
}

server {
    listen 80;
    server_name api.example.com;
    client_max_body_size 10M;    # Лимит размера загружаемых файлов (по умолч. всего 1 МБ -> 413!)

    location /static/ {
        alias /var/www/static/;  # Статику отдаёт сам Nginx напрямую с диска
        expires 30d;
    }

    location / {
        proxy_pass http://backend_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

| Код ошибки Nginx | Что означает? | Настоящая причина в Python-бэкенде |
| :--- | :--- | :--- |
| **`413 Request Entity Too Large`** | Файл от клиента больше лимита Nginx | По умолчанию в Nginx лимит `1M` — увеличьте `client_max_body_size 20M;` |
| **`502 Bad Gateway`** | Nginx постучался в `proxy_pass`, но дверь закрыта | Контейнер `Uvicorn`/`Gunicorn` упал или слушает `127.0.0.1` вместо `0.0.0.0` |
| **`504 Gateway Timeout`** | Nginx постучался в Python, но тот думал дольше 60 сек | Тяжёлый синхронный отчёт в ручке API — вынесите его в фоновую задачу Celery! |

---
### 3. Диагностика `502` vs `504` и подмена `X-Forwarded-For`
> **Junior vs Senior**:
> - **Junior**: При ошибке `504 Gateway Timeout` бездумно выкручивает `proxy_read_timeout 600s;` в Nginx, заставляя воркеры висеть по 10 минут, или верит заголовку `X-Forwarded-For` без настройки `--proxy-headers` и списка доверенных прокси (позволяя хакеру подделать свой IP и обойти Rate Limiter).
> - **Senior**: Мгновенно отличает `502` (Python-процесс мёртв или недоступен по сети) от `504` (Python жив, но заблокирован долгим запросом — пора выносить задачу в очередь Celery), а заголовок `X-Forwarded-For` принимает только от IP своего контейнера Nginx (`--forwarded-allow-ips`).

---
### 4. Живая проверка: симулятор Reverse Proxy Nginx с балансировкой и кодами `413`/`502`/`504`
Проверим на Python, как Nginx маршрутизирует статику и API-запросы, проставляет `X-Forwarded-For` и генерирует коды `413`, `502`, `504`:

```python
def simulate_nginx_proxy(path: str, body_mb: float, client_ip: str, backend_alive: bool, backend_time_s: float) -> dict:
    if body_mb > 10.0:
        return {"status": 413, "via": "nginx", "detail": "413 Payload Too Large (client_max_body_size=10M)"}
    if path.startswith("/static/"):
        return {"status": 200, "via": "nginx_disk_direct", "detail": f"Отдан файл {path} за 0.1 мс без Python"}
    if not backend_alive:
        return {"status": 502, "via": "nginx", "detail": "502 Bad Gateway (Uvicorn недоступен)"}
    if backend_time_s > 60.0:
        return {"status": 504, "via": "nginx", "detail": "504 Gateway Timeout (Uvicorn отвечал > 60s)"}
    headers = {"X-Real-IP": client_ip, "X-Forwarded-Proto": "https"}
    return {"status": 200, "via": "uvicorn_upstream", "headers_seen_by_python": headers}

print("Запрос статики      :", simulate_nginx_proxy("/static/app.css", 0.1, "93.184.216.34", True, 0.0))
print("Обычный API-запрос  :", simulate_nginx_proxy("/api/v1/orders", 0.5, "93.184.216.34", True, 0.05))
print("Упавший Uvicorn     :", simulate_nginx_proxy("/api/v1/orders", 0.5, "93.184.216.34", False, 0.0))
print("Зависший отчёт (95s):", simulate_nginx_proxy("/api/v1/report", 0.5, "93.184.216.34", True, 95.0))
```
"""

# ==============================================================================
# ЮНИТ 7.6 · ОЧЕРЕДИ, ТЕСТИРОВАНИЕ И МОНИТОРИНГ (К-204 .. К-216)
# ==============================================================================

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-204. Очереди задач.md"] = r"""📖 Перечитать конспект: Очереди задач (Task Queues): зачем нужна фоновая обработка >>
### 1. Ментальная модель: Пейджер в кофейне вместо стояния у кассы 10 минут
Представьте, что вы купили кофе с выпечкой, а кассир говорит: «Никуда не уходите от кассы и не моргайте 10 минут, пока печётся круассан, а вся очередь за вами пусть ждёт!». Это **синхронная обработка**.
Если в HTTP-эндпоинте `POST /orders` вы прямо внутри запроса генерируете PDF-чек (3 сек), отправляете письмо через внешний SMTP-сервер (4 сек) и шлёте запрос в 1С (5 сек), пользователь смотрит на зависший спиннер 12 секунд, а если SMTP-сервер моргнёт — вся оплата упадёт с ошибкой `500`!
**Очередь задач (Task Queue, например Celery)** работает как бариста с номером заказа:
1. Веб-сервер (`Producer`) за **15 миллисекунд** сохраняет заказ в БД, кладёт билетик задачи `send_receipt(order_id=42)` в **Брокер (Redis / RabbitMQ)** и мгновенно отвечает клиенту **`202 Accepted` («Заказ принят!»)**.
2. Отдельный фоновый процесс **Worker (`Consumer`)** забирает билетик из брокера и спокойно генерирует PDF и отправляет письмо в фоне, с автоматическими повторами (`retry`) при сбоях сети!

```text
Клиент ──POST /orders──► [FastAPI (Producer)] ──15 мс: "202 Accepted"──► Клиент счастлив!
                                  │
                     кладёт JSON-задачу: {"task": "send_pdf", "order_id": 42}
                                  ▼
                       [Брокер очереди: Redis / RabbitMQ]
                                  │
                     забирает и выполняет в фоне (с Retry при сбоях)
                                  ▼
                       [Celery Worker (Consumer)] ──► Генерация PDF + SMTP Email
```

---
### 2. Четыре участника архитектуры Celery и золотые правила фоновых задач
В экосистеме фоновых задач у каждого компонента своя строгая роль:

| Компонент | Роль в системе | Что передаётся внутри? |
| :--- | :--- | :--- |
| **Producer (Продюсер)** | Ваш веб-сервер (`FastAPI` / `Django`), вызывающий `task.delay(42)` | Только лёгкий JSON с **ID записи** (`order_id: 42`), а не гигабайтный объект! |
| **Broker (Брокер)** | Почтовый ящик задач (`Redis` или `RabbitMQ`) | Хранит очередь невыполненных сообщений до подтверждения (`ACK`) |
| **Worker (Воркер)** | Отдельный процесс Python (`celery -A app worker`), выполняющий код задачи | Сам загружает свежие данные из БД по `order_id` и делает тяжёлую работу |
| **Result Backend** | Опциональное хранилище статусов и результатов (`Redis` / `Postgres`) | Хранит `PENDING` ➔ `STARTED` ➔ `SUCCESS` / `FAILURE` по `task_id` |

---
### 3. Два смертных греха при работе с очередями: передача ORM-объектов и отсутствие Идемпотентности
> **Junior vs Senior**:
> - **Junior**: Передаёт в задачу целый ORM-объект SQLAlchemy/Django (`send_email.delay(user_obj)`) или50-мегабайтный байтовый файл (забивая память Redis и ловя `EncodeError`), а внутри задачи списывает баланс без проверки, не выполнялась ли эта задача секунду назад.
> - **Senior**: Соблюдает два железных закона очередей:
>   1. **Передавай только примитивный ID (`order_id: int`)**: пока задача лежала в очереди 5 секунд, данные в БД могли измениться, поэтому воркер сам делает `SELECT` свежей записи по ID.
>   2. **Каждая задача обязана быть идемпотентной**: из-за сетевых сбоев брокер гарантирует доставку *At-least-once* (задача может запуститься дважды!), поэтому перед отправкой чека или списанием денег воркер проверяет статус `if order.receipt_sent: return`.

---
### 4. Живая проверка: идемпотентный воркер очереди задач с экспоненциальным Retry
Запустим на Python модель очереди с брокером и убедимся, как воркер переживает временный сбой SMTP и защищается от дублей:

```python
class TaskQueueSimulator:
    def __init__(self) -> None:
        self.db_orders = {42: {"email": "user@example.com", "receipt_sent": False}}
        self.queue: list[dict] = []

    def delay(self, order_id: int) -> str:
        # Передаём ТОЛЬКО лёгкий примитивный ID!
        task = {"task_id": f"tsk-{order_id}", "order_id": order_id, "attempts": 0}
        self.queue.append(task)
        return task["task_id"]

    def process_next(self, smtp_flaky_first_time: bool = True) -> str:
        task = self.queue.pop(0)
        order = self.db_orders[task["order_id"]]
        if order["receipt_sent"]:
            return f"SKIP (Idempotent): чек для заказа #{task['order_id']} уже был отправлен ранее!"
        task["attempts"] += 1
        if smtp_flaky_first_time and task["attempts"] == 1:
            self.queue.append(task)  # Возвращаем в очередь на Retry
            return f"RETRY #{task['attempts']}: временный таймаут SMTP, задача возвращена в очередь"
        order["receipt_sent"] = True
        return f"SUCCESS: чек для заказа #{task['order_id']} отправлен с попытки #{task['attempts']}!"

tq = TaskQueueSimulator()
tq.delay(42)
print("Попытка 1 (сбой сети)  :", tq.process_next(smtp_flaky_first_time=True))
print("Попытка 2 (успех)      :", tq.process_next(smtp_flaky_first_time=True))
tq.delay(42)  # Случайный дубликат сообщения от брокера:
print("Дубликат сообщения     :", tq.process_next(smtp_flaky_first_time=False))
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-205. Очереди сообщений_ RabbitMQ и Kafka.md"] = r"""📖 Перечитать конспект: Брокеры сообщений: RabbitMQ vs Apache Kafka >>
### 1. Ментальная модель: Почтальон с удалением писем (`RabbitMQ`) vs Бортовой самописец-летопись (`Kafka`)
На каждом втором собеседовании Middle/Senior Python Backend разработчика спрашивают: **«Чем отличается RabbitMQ от Apache Kafka и когда что выбрать?»**
Разница заложена в самой физике хранения сообщения:
- **RabbitMQ (Традиционный брокер очереди, AMQP)** — это **Умный маршрутизатор (Почтальон)**. Продюсер кидает письмо в `Exchange` (сортировочный узел), тот по правилам (`Routing Key`) кладёт его в нужную очередь (`Queue`). Как только воркер прочитал письмо и сказал **`ACK` («Выполнено!»)**, RabbitMQ **навсегда удаляет это сообщение из памяти**!
- **Apache Kafka (Распределённый лог событий)** — это **Неизменяемая бухгалтерская книга (Бортовой самописец)**. Сообщения дописываются строго в конец дискового файла (**Topic / Partition**) и **НЕ удаляются после прочтения** (хранятся, например, 7 дней или 1 терабайт). Каждый сервис-читатель (**Consumer Group**) просто двигает свою личную закладку (**`Offset`** — номер прочитанной строки) и может в любой момент перемотать время назад и перечитать все события за неделю!

```text
RabbitMQ (Умный брокер, глупый консьюмер — сообщение УДАЛЯЕТСЯ после ACK):
[Producer] ──► [Exchange] ──routing_key──► [Queue] ──► [Worker] (ACK -> сообщение стерто!)

Apache Kafka (Глупый брокер, умный консьюмер — сообщения ХРАНЯТСЯ на диске):
Partition 0: [ev_0] [ev_1] [ev_2] [ev_3] [ev_4] ──► дописывается в конец (Append-only)
                       ▲             ▲
           Offset Analytics=1    Offset Billing=3 (каждая группа читает в своём темпе!)
```

---
### 2. Архитектурное сравнение: когда нужен RabbitMQ, а когда — Kafka?
Ни один из этих инструментов не «лучше» другого — они созданы для разных паттернов нагрузки:

| Критерий | RabbitMQ | Apache Kafka |
| :--- | :--- | :--- |
| **Судьба сообщения после чтения** | **Удаляется сразу** после `basic_ack` | **Хранится на диске** по `retention` (например, 7–30 дней) |
| **Повторное чтение истории (Replay)** | Невозможно (прочитанные сообщения уже стёрты) | **Да!** Любой новый сервис может вычитать события с `offset=0` |
| **Маршрутизация и приоритеты** | **Богатейшая** (`direct`, `topic`, `fanout`, `Priority Queues`, `DLQ`) | Простая (разбиение топика на партиции по хешу ключа `key`) |
| **Пропускная способность** | Десятки тысяч сообщ./сек (отлично для фоновых задач) | **Сотни тысяч — миллионы сообщ./сек** (стриминг событий, кликстрим) |
| **Гарантия порядка сообщений** | В рамках одной очереди (при 1 консьюмере) | Строгий порядок **внутри одной партиции (`Partition`)** по ключу `user_id` |
| **Идеальный сценарий** | Фоновые задачи **Celery**, отправка писем, сложный роутинг команд | Событийная шина микросервисов (**Event-Driven**), аналитика, аудит-логи |

---
### 3. Как сохранить строгий порядок событий пользователя в Kafka?
В Kafka один топик `orders` делится на несколько параллельных дорожек — **Партиций (`Partitions`)**, чтобы его могли параллельно читать несколько воркеров одной группы (`Consumer Group`).

> **Junior vs Senior**:
> - **Junior**: Отправляет в Kafka события `OrderCreated`, `OrderPaid`, `OrderShipped` с пустым ключом (`key=None`). Kafka раскидывает их по разным партициям (`P0`, `P1`, `P2`) случайным образом, и событие «Заказ доставлен» обрабатывается **раньше**, чем «Заказ создан»! А для чтения топика из 4 партиций запускает 10 консьюмеров в одной группе, не понимая, почему 6 из них простаивают без дела.
> - **Senior**: В качестве ключа сообщения в Kafka всегда передаёт **`key=str(order_id)`** (хеш `murmur2(key) % num_partitions` гарантирует, что все события одного заказа попадут строго в **одну и ту же партицию** в идеальном хронологическом порядке!). И помнит закон Kafka: число активных консьюмеров внутри одной `Consumer Group` не может превышать число партиций топика.

---
### 4. Живая проверка: сравнение удаления по `ACK` в RabbitMQ и чтения по `Offset` в Kafka
Смоделируем на Python оба брокера и убедимся, почему в Kafka два разных микросервиса (`billing` и `analytics`) могут независимо читать один поток событий и перематывать `offset` назад:

```python
class MiniRabbitQueue:
    def __init__(self) -> None:
        self.q: list[str] = []
    def publish(self, msg: str) -> None:
        self.q.append(msg)
    def consume_and_ack(self) -> str:
        return self.q.pop(0)  # Удаляется навсегда после ACK!

class MiniKafkaPartition:
    def __init__(self) -> None:
        self.log: list[str] = []
        self.offsets: dict[str, int] = {}
    def produce(self, event: str) -> None:
        self.log.append(event)  # Append-only лог
    def poll(self, group: str) -> str:
        idx = self.offsets.get(group, 0)
        event = self.log[idx]
        self.offsets[group] = idx + 1
        return event
    def seek_to_beginning(self, group: str) -> None:
        self.offsets[group] = 0  # Перемотка времени назад!

rabbit = MiniRabbitQueue()
rabbit.publish("send_email_1")
print(f"RabbitMQ: прочитано '{rabbit.consume_and_ack()}', осталось в очереди: {len(rabbit.q)}")

kafka = MiniKafkaPartition()
kafka.produce("OrderCreated#1")
kafka.produce("OrderPaid#1")
print(f"Kafka (группа billing)  : 1={kafka.poll('billing')}, 2={kafka.poll('billing')}")
print(f"Kafka (группа analytics): 1={kafka.poll('analytics')} (независимый offset!)")
kafka.seek_to_beginning("analytics")
print(f"Kafka после Replay(0)   : снова читаем '{kafka.poll('analytics')}' из истории!")
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-206. Unit vs Integration тесты и TDD_ подход.md"] = r"""📖 Перечитать конспект: Unit vs Integration тесты, пирамида тестирования и TDD >>
### 1. Ментальная модель: Проверка шестерёнки на столе (`Unit`) vs Испытание двигателя на стенде (`Integration`)
Представьте сборку автомобиля:
- **Unit-тест (Модульный тест)** — вы берёте одну изолированную функцию (например, `calculate_discount(price, promo_code)`) и проверяете её прямо в оперативной памяти **без базы данных, без сети и без диска**. Один unit-тест выполняется за **1 миллисекунду**!
- **Integration-тест (Интеграционный тест)** — вы скручиваете детали вместе и проверяете, как сервис реально сохраняет заказ в настоящую тестовую базу **PostgreSQL** и отдаёт ответ через `FastAPI TestClient`.
- **E2E-тест (End-to-End / Сквозной)** — робот открывает настоящий браузер и проходит весь путь пользователя от кнопки «Войти» до оплаты.

```text
          /\
         /  \         E2E-тесты (~5%): медленные (секунды), хрупкие, проверяют главные сценарии
        /────\
       /      \       Integration-тесты (~25%): проверяют связку API + реальная БД Postgres/Redis
      /────────\
     /          \     Unit-тесты (~70%): мгновенные (1 мс), изолированные, проверяют бизнес-логику!
    /────────────\
```

---
### 2. Паттерн `AAA` (`Arrange — Act — Assert`) и цикл `TDD` (`Red ➔ Green ➔ Refactor`)
Каждый чистый тест строится по трём абзацам **AAA**:
1. **Arrange (Подготовка)** — создаём входные данные и зависимости.
2. **Act (Действие)** — вызываем ровно одну тестируемую функцию/метод.
3. **Assert (Проверка)** — сверяем полученный результат с ожидаемым.

А методология **TDD (Test-Driven Development — Разработка через тестирование)** переворачивает привычный порядок работы в трёхшаговый цикл:
- 🔴 **Red (Красный)**: сначала пишем маленький тест на ещё не существующую фичу и убеждаемся, что он **падает**.
- 🟢 **Green (Зелёный)**: пишем минимальный код, чтобы тест **прошёл**.
- 🔵 **Refactor (Рефакторинг)**: наводим красоту и чистоту в коде под защитой зелёного теста!

| Вид тестов | Скорость 1 теста | Нужна ли БД / Сеть? | Что именно ловит? |
| :--- | :--- | :--- | :--- |
| **Unit (Модульные)** | **0.5 – 2 мс** | **Нет** (внешний мир заменён стабами/фейками) | Ошибки в формулах, краевых случаях (`0`, `None`, отрицательные суммы), правилах домена |
| **Integration (Интеграционные)** | **20 – 200 мс** | **Да** (тестовый контейнер Postgres / Redis) | Ошибки в SQL-запросах, миграциях, сериализации Pydantic и транзакциях |
| **E2E (Сквозные)** | **1 – 10 сек** | **Да** (вся система целиком) | Рассогласование фронтенда, бэкенда и внешних шлюзов |

---
### 3. Анти-паттерн «Рожок мороженого» (Перевёрнутая пирамида)
> **Junior vs Senior**:
> - **Junior**: Проверяет каждое условие `if/else` бизнес-логики только тяжёлыми запросами через HTTP + базу данных, или пишет один гигантский тест на 150 строк с 20 вызовами `assert` вперемешку. В итоге тестовый набор идёт 25 минут и падает от любого чиха.
> - **Senior**: Держит чистую доменную логику в функциях и классах без привязки к БД (покрывая её сотнями мгновенных **Unit-тестов** по принципу `AAA`), а **Integration-тестами** проверяет контракты репозиториев с настоящим PostgreSQL.

---
### 4. Живая проверка: Unit-тест по стандарту `AAA` для граничных случаев бизнес-логики
Проверим на Python функцию расчёта стоимости доставки и протестируем её по структуре `Arrange — Act — Assert`:

```python
from decimal import Decimal

def calc_delivery_fee(cart_total: Decimal, is_vip: bool) -> Decimal:
    if cart_total <= Decimal("0"):
        raise ValueError("Сумма корзины должна быть положительной")
    if is_vip or cart_total >= Decimal("3000.00"):
        return Decimal("0.00")
    return Decimal("299.00")

# Тест 1 (AAA): Бесплатная доставка от пороговой суммы 3000.00
# Arrange
total = Decimal("3000.00")
# Act
fee = calc_delivery_fee(total, is_vip=False)
# Assert
assert fee == Decimal("0.00"), f"Ожидалось 0.00, получено {fee}"

# Тест 2 (AAA): Проверка выброса ValueError на некорректной сумме
error_caught = False
try:
    calc_delivery_fee(Decimal("-50.00"), is_vip=False)
except ValueError:
    error_caught = True
assert error_caught is True

print("Все Unit-тесты по стандарту AAA (граничное значение 3000.00 и отрицательная сумма) пройдены! ✅")
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-207. pytest_ фикстуры, моки и патчи.md"] = r"""📖 Перечитать конспект: pytest: фикстуры, параметризация и правильный monkeypatch >>
### 1. Ментальная модель: Лабораторный ассистент (`fixture` с `yield`) и Каскадёр-дублёр (`Mock`)
Почему **`pytest`** стал главным стандартом тестирования в мире Python? Благодаря трём суперспособностям:
1. **Фикстуры (`@pytest.fixture`)** — это ваш лабораторный ассистент. Всё, что написано **до слова `yield`**, подготавливает пробирки перед тестом (`Setup`), сам объект после `yield` передаётся в тест по имени аргумента (через *Dependency Injection*), а всё, что написано **после `yield`**, гарантированно убирает лабораторию даже если тест упал (`Teardown`, например откатывает транзакцию БД!).
2. **Параметризация (`@pytest.mark.parametrize`)** — запускает одну тестовую функцию 10 раз с разными наборами входных данных без копипасты кода.
3. **Моки и патчи (`unittest.mock.patch` / `monkeypatch`)** — каскадёры-дублёры, которые на время теста подменяют платный SMS-шлюз или внешнее API банка, чтобы тест не списывал реальные деньги и не зависел от интернета.

```text
Жизненный цикл фикстуры с yield:
[Setup: открыть транзакцию БД] ──► yield session ──► [Выполнение test_create_user(session)]
                                                               │ (даже при падении теста!)
                                                               ▼
                                          [Teardown: session.rollback() — чистая БД!]
```

---
### 2. Времена жизни фикстур (`scope`) и Главное правило `mock.patch`: «Патчи там, где ИСПОЛЬЗУЕТСЯ!»
Самая частая ловушка на собеседованиях: допустим, в файле `app/clients.py` определена функция `send_sms()`, а файл `app/services.py` делает **`from app.clients import send_sms`** и вызывает её.
Какой путь нужно передать в `@patch(...)`, чтобы замокать отправку SMS при тестировании `services.py`?
Строго **`@patch("app.services.send_sms")`**! Почему? Потому что инструкция `from app.clients import send_sms` уже создала локальную ссылку `send_sms` внутри пространства имён модуля `app.services`. Если вы пропатчите `app.clients.send_sms`, модуль `app.services` продолжит вызывать старую настоящую функцию!

| Инструмент `pytest` | Синтаксис | Когда использовать? |
| :--- | :--- | :--- |
| **`@pytest.fixture(scope="function")`** | Выполняется заново перед **каждым** тестом (по умолчанию) | Изолированная сессия/транзакция БД, тестовый клиент |
| **`@pytest.fixture(scope="session")`** | Выполняется **1 раз** на весь запуск `pytest` | Тяжёлый старт контейнера PostgreSQL или чтение больших словарей |
| **`@pytest.mark.parametrize`** | `@pytest.mark.parametrize("inp,exp", [(1, 2), (3, 6)])` | Проверка 5–10 граничных значений одной функции |
| **`patch(..., autospec=True)`** | Подменяет внешний вызов с проверкой сигнатуры аргументов | Изоляция от внешних HTTP API, SMTP, S3 и `datetime.now()` |

---
### 3. Опасность моков без `autospec=True`
> **Junior vs Senior**:
> - **Junior**: Создаёт обычный `MagicMock()` без `autospec=True` и мокает вообще всё подряд (включая собственные функции и SQL-запросы). В реальном методе `sms_client.send(phone, text)` разработчик меняет сигнатуру на `sms_client.send(recipient_phone)`, а тест с обычным `MagicMock` **продолжает гореть зелёным**, потому что обычный мок молча принимает любые несуществующие аргументы!
> - **Senior**: Всегда использует **`autospec=True`** (или `create_autospec`) — такой мок повторяет точную сигнатуру реального класса и мгновенно упадёт с `TypeError`, если вы передадите неверные аргументы.

---
### 4. Живая проверка: фикстура с `yield` и защита сигнатуры через `create_autospec`
Убедимся на стандартной библиотеке `unittest.mock` в Python 3.13, как `create_autospec` ловит ошибку в имени аргумента, которую пропустил бы обычный `MagicMock`:

```python
from contextlib import contextmanager
from unittest.mock import MagicMock, create_autospec

class SmsGateway:
    def send_code(self, phone: str, code: str) -> bool:
        raise RuntimeError("Реальный платный SMS-шлюз не должен вызываться в тестах!")

@contextmanager
def db_session_fixture():
    tx_log = ["BEGIN"]
    try:
        yield tx_log          # Аналог yield в @pytest.fixture
    finally:
        tx_log.append("ROLLBACK")  # Гарантированный Teardown!

# Проверим защиту сигнатуры через create_autospec:
strict_mock = create_autospec(SmsGateway, instance=True)
strict_mock.send_code.return_value = True
assert strict_mock.send_code(phone="+79990001122", code="4242") is True

try:
    # Ошибка разработчика: передал несуществующий аргумент wrong_arg!
    strict_mock.send_code(wrong_arg="123")
except TypeError as exc:
    print("create_autospec поймал баг сигнатуры:", exc)

with db_session_fixture() as session:
    session.append("INSERT INTO users")
print("Жизненный цикл yield-фикстуры       :", session)
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-208. unittest_ стандартный фреймворк.md"] = r"""📖 Перечитать конспект: unittest: стандартный фреймворк тестирования из коробки >>
### 1. Ментальная модель: Классический лабораторный журнал в стиле ООП (xUnit)
Зачем учить встроенный модуль **`unittest`**, если все новые проекты пишут тесты на `pytest`?
По трём веским причинам:
1. `unittest` входит в **стандартную библиотеку Python** (работает везде без `pip install`).
2. Огромное количество корпоративных кодовых баз, стандартных тестов Django (`django.test.TestCase`) и самой стандартной библиотеки CPython написаны на классах `unittest.TestCase`.
3. Знаменитый модуль **`unittest.mock` (`Mock`, `MagicMock`, `AsyncMock`, `patch`)** — это часть пакета `unittest`, которую используют все (в том числе внутри `pytest`)!

```text
Структура класса unittest.TestCase:
┌────────────────────────────────────────────────────────────────┐
│ setUpClass(cls)     ──► 1 раз перед всеми тестами класса       │
│   ├── setUp(self)   ──► перед КАЖДЫМ методом test_*            │
│   ├── test_pay(self)──► self.assertEqual / self.assertRaises   │
│   └── tearDown(self)──► после КАЖДОГО метода test_*            │
│ tearDownClass(cls)  ──► 1 раз в самом конце                    │
└────────────────────────────────────────────────────────────────┘
```

---
### 2. Сравнение синтаксиса `unittest` и `pytest`
В `unittest` каждый тест обязан быть методом класса, унаследованного от `unittest.TestCase`, и начинаться с префикса **`test_`**, а вместо ключевого слова `assert` используются специальные методы `self.assertEqual`, `self.assertRaises`, `self.subTest`:

| Задача в тесте | Как пишется в **`unittest.TestCase`** | Как пишется в **`pytest`** |
| :--- | :--- | :--- |
| **Проверка равенства** | `self.assertEqual(actual, expected)` | `assert actual == expected` |
| **Проверка исключения** | `with self.assertRaises(ValueError): ...` | `with pytest.raises(ValueError): ...` |
| **Подготовка перед тестом** | Метод `def setUp(self):` | Фикстура `@pytest.fixture` |
| **Параметризация цикла** | Контекст `with self.subTest(val=x):` | Декоратор `@pytest.mark.parametrize` |
| **Тестирование `async def`** | Наследование от **`unittest.IsolatedAsyncioTestCase`** | Плагин `@pytest.mark.asyncio` |

---
### 3. Секретное оружие `unittest`: `self.subTest` и `IsolatedAsyncioTestCase`
> **Junior vs Senior**:
> - **Junior**: Проверяет в `unittest` список из 10 значений обычным циклом `for x in items: self.assertEqual(...)`. Как только падает 1-й элемент, весь тест прерывается, и джун не знает, работают ли остальные 9 элементов. А для тестирования асинхронных корутин городит ручной `asyncio.run()` в каждом методе.
> - **Senior**: Оборачивает тело цикла в **`with self.subTest(item=x):`** (тогда `unittest` проверит все 10 случаев и покажет отчёт по каждому упавшему параметру!), а для асинхронного кода наследуется от встроенного **`unittest.IsolatedAsyncioTestCase`** и использует **`AsyncMock`**.

---
### 4. Живая проверка: запуск `TestCase` с `subTest` и `assertRaises` в Python 3.13
Запустим полноценный тестовый набор `unittest` прямо в памяти и посмотрим на его отчёт:

```python
import unittest

def parse_Completed_age(raw: str) -> int:
    age = int(raw)
    if not (0 < age <= 120):
        raise ValueError("Некорректный возраст")
    return age

class TestAgeParser(unittest.TestCase):
    def test_valid_ages_with_subtest(self) -> None:
        for raw, expected in [("18", 18), ("45", 45), ("120", 120)]:
            with self.subTest(raw=raw):
                self.assertEqual(parse_Completed_age(raw), expected)

    def test_invalid_age_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_Completed_age("-5")

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAgeParser)
runner = unittest.TextTestRunner(verbosity=0)
result = runner.run(suite)
print(f"Выполнено тестов unittest: {result.testsRun}, Ошибок: {len(result.errors)}, Падений: {len(result.failures)} ✅")
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-209. Test coverage_ покрытие кода тестами и.md"] = r"""📖 Перечитать конспект: Test Coverage: покрытие кода тестами и иллюзия 100% >>
### 1. Ментальная модель: Ультрафиолетовый фонарик, подсвечивающий тёмные углы кода
Как понять, какие участки вашего проекта реально проверяются при запуске `pytest`, а какие ни разу даже не запускались?
Утилита **`coverage.py` (`pytest-cov`)** работает как ультрафиолетовый сканер: во время прогона тестов она записывает, на какие строчки и развилки `if/else` ступала нога интерпретатора Python, и выдаёт процент покрытия (**Code Coverage**) со списком пропущенных строк (`Missing lines`).

```text
def withdraw(balance: int, amount: int, is_frozen: bool = False) -> int:
    if is_frozen:               ◄── Ветка 1: если в тестах всегда is_frozen=False,
        raise PermissionError() ◄── эта строка останется НЕПОКРЫТОЙ (Missing)!
    return balance - amount     ◄── Ветка 2: покрыта тестом ✅
```

---
### 2. Разница между Line Coverage (по строкам) и Branch Coverage (по ветвлениям)
Почему обычное покрытие по строкам (**Line Coverage**) легко обмануть однострочным условием и почему сеньоры всегда включают флаг **`--cov-branch`**?

```bash
# Запустить pytest с проверкой покрытия пакета src, включая развилки (--cov-branch),
# показать номера пропущенных строк и уронить CI, если покрытие упало ниже 80%:
pytest --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=80
```

Посмотрите на коварный пример:
```python
def get_bonus(is_vip: bool) -> int:
    bonus = 0
    if is_vip: bonus = 100  # Однострочный if!
    return bonus
```
Если мы вызовем в тесте **только** `get_bonus(is_vip=True)`, то выполнятся все 3 строки файла — и обычный **Line Coverage покажет 100%**! Хотя случай `is_vip=False` (неявная ветка `else`) мы вообще не проверяли! А вот **Branch Coverage (`--cov-branch`)** честно покажет, что проверена только 1 из 2 веток (`50%`).

| Метрика / Настройка | Что измеряет? | Рекомендация для продакшена |
| :--- | :--- | :--- |
| **Line (Statement) Coverage** | Доля выполненных строк кода от общего числа строк | Базовый минимум, но слеп к неявным `else` |
| **Branch Coverage (`--cov-branch`)** | Доля пройденных развилок `True`/`False` в каждом `if`/`match`/`try` | **Обязательно включать** в `pyproject.toml` |
| **`--cov-fail-under=80`** | Нижний порог покрытия в CI/CD | Оптимальный баланс для бэкенда: **80–90%** (ядро оплат — **95%+**) |

---
### 3. Парадокс Гудхарта: почему 100% Coverage НЕ гарантирует отсутствие багов?
> **Junior vs Senior**:
> - **Junior**: Ради красивой цифры `100% coverage` пишет «тесты без проверок» (*Assertion-free tests*): просто вызывает функции `process_order()`, не ставя ни одного содержательного `assert`. Строчки кода выполнились, `coverage` рисует 100%, но если функция вернёт `None` вместо чека — тест даже не заметит!
> - **Senior**: Воспринимает `coverage` не как цель для накрутки, а как **инструмент поиска забытых слепых зон** (`Missing lines` в блоках `except` и граничных `if`), исключает из расчёта точки запуска и типы (`if TYPE_CHECKING:`), а качество тестов оценивает по строгости `assert`-проверок.

---
### 4. Живая проверка: трассировщик покрытия строк и веток через `sys.settrace`
Посмотрим, как под капотом работает `coverage.py` в стандартном Python: напишем собственный мини-измеритель покрытия строк и найдём слепую зону функции:

```python
import inspect

def process_payment(amount: int, currency: str) -> str:
    if amount <= 0:
        return "ERROR: invalid amount"
    if currency != "RUB":
        return "ERROR: unsupported currency"
    return f"OK: paid {amount} RUB"

def check_branch_coverage(calls: list[tuple[int, str]]) -> dict:
    results = {args: process_payment(*args) for args in calls}
    outcomes = set(results.values())
    total_branches = 3  # 1) amount<=0, 2) currency!='RUB', 3) OK
    covered = len(outcomes)
    return {
        "branch_coverage_pct": round(covered / total_branches * 100, 1),
        "tested_outcomes": sorted(outcomes),
        "blind_spots_left": total_branches - covered,
    }

print("Слабый тест (только Happy Path) :", check_branch_coverage([(100, "RUB")]))
print("Полный набор граничных тестов   :", check_branch_coverage([(100, "RUB"), (-5, "RUB"), (100, "USD")]))
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-210. Логирование в Python_ от print() к.md"] = r"""📖 Перечитать конспект: Логирование в Python: от print() к промышленному модулю logging >>
### 1. Ментальная модель: Диспетчерская вышка с фильтрами и маршрутизацией (`logging`)
Почему в продакшен-коде **категорически запрещено** использовать `print()` вместо модуля `logging`?
У `print()` нет ни времени события, ни имени модуля, ни уровня важности, его нельзя отключить одной настройкой без правки кода, и он не умеет параллельно писать важные ошибки в систему мониторинга.
Архитектура стандартного модуля **`logging`** состоит из 4 элементов, работающих как почтовая служба:
1. **`Logger` (`logging.getLogger(__name__)`)** — точка входа в вашем файле `.py`, куда код передаёт событие.
2. **`Handler` (Обработчик)** — решает, **КУДА** отправить запись (в поток терминала `StreamHandler`, во вращающийся файл `RotatingFileHandler` или по сети).
3. **`Filter` (Фильтр)** — решает, какие записи пропустить или обогатить контекстом (`request_id`).
4. **`Formatter` (Форматтер)** — решает, **КАК** будет выглядеть строка (текст для человека или **JSON** для Elasticsearch / Loki!).

```text
[logger.error("DB timeout")]
             │
             ▼
     [ Logger (__name__) ]
      /                 \
     ▼                   ▼
[StreamHandler]    [RotatingFileHandler (maxBytes=10MB)]
     │                   │
     ▼                   ▼
[JSONFormatter]    [TextFormatter]
     │                   │
  stdout (Docker)     app.log
```

---
### 2. Правильное создание логгера и `Structured Logging (JSON)` для Docker
В современных контейнерах логи не пишут в файлы внутри контейнера — их выводят в `stdout` в формате **однострочного JSON (Structured Logging)**, чтобы агент сбора логов (Promtail / FluentBit / Vector) автоматически индексировал поля `level`, `user_id`, `request_id` и `latency_ms`.

| Почему `print()` — это боль на проде | Что даёт `logging.getLogger(__name__)` |
| :--- | :--- |
| Неизвестно, в каком файле, строке и во сколько произошёл вывод | Автоматически подставляет `%(asctime)s`, `%(name)s`, `%(lineno)d` |
| Нельзя одной переменной `LOG_LEVEL=WARNING` заглушить отладочный шум | Мгновенно переключает детальность логов без изменения кода |
| Теряет стектрейс ошибки (`except Exception as e: print(e)`) | Метод **`logger.exception("...")`** (или `exc_info=True`) сохраняет полный Traceback! |
| Текст с переносами строк рвёт парсинг в Kibana / Grafana Loki | **JSON-форматтер** упаковывает всё событие и стектрейс в одну валидную JSON-строку |

---
### 3. Три золотых правила Python-логирования
> **Junior vs Senior**:
> - **Junior**: Вызывает `logging.basicConfig()` внутри каждого импортируемого файла, пишет `logger.error(f"User {user} failed: {e}")` (теряя Traceback и тратя CPU на форматирование строки даже когда уровень лога отключён) или случайно логирует пароли и номера банковских карт (`PAN` / `CVV`).
> - **Senior**: Во всех модулях создаёт логгер строго через **`logger = logging.getLogger(__name__)`** (тогда имя логгера совпадает с путём пакета `src.billing.services`), `dictConfig` вызывает ровно 1 раз в точке старта `main.py`, а в блоке `except` использует **`logger.exception("Payment failed")`** и передаёт бизнес-поля через словарь **`extra={"order_id": 42, "request_id": req_id}`**.

---
### 4. Живая проверка: промышленный JSON-форматтер для `logging` в 15 строк
Соберём на стандартном модуле `logging` настоящий `JsonFormatter`, превращающий лог и поля `extra` в структурированный JSON для Kibana / Loki:

```python
import json
import logging
import io

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for key in ("request_id", "order_id", "latency_ms"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["traceback"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)

stream = io.StringIO()
handler = logging.StreamHandler(stream)
handler.setFormatter(JsonFormatter())

logger = logging.getLogger("billing.service")
logger.setLevel(logging.INFO)
logger.handlers = [handler]
logger.propagate = False

logger.info("Оплата проведена успешно", extra={"request_id": "req-77", "order_id": 42, "latency_ms": 18})
print("Структурированный JSON-лог:", stream.getvalue().strip())
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-211. Уровни логирования в Python.md"] = r"""📖 Перечитать конспект: Уровни логирования в Python: от DEBUG (10) до CRITICAL (50) >>
### 1. Ментальная модель: Порог чувствительности сигнализации
Если на продакшене каждую секунду проходят 1000 запросов и каждый запрос пишет по 20 отладочных строк, диск сервера забьётся за час, а дежурный инженер утонет в информационном шуме.
Поэтому в Python у каждого лог-сообщения есть числовой **Уровень важности (`Level`)** от `10` до `50`. Логгер и хендлер работают как плотина с заданной высотой: если на продакшене выставлен уровень **`INFO (20)`**, то все сообщения с уровнем $\ge 20$ проходят в лог, а все сообщения `DEBUG (10)` отбрасываются!

```text
Шкала уровней logging (при пороге на проде LEVEL = INFO [20]):
  10 · DEBUG    ──► 🛑 Отброшено плотиной (10 < 20)
═══════════════════ [ Порог фильтрации: INFO (20) ] ═══════════════════
  20 · INFO     ──► ✅ Проходит (штатные бизнес-события: заказ создан)
  30 · WARNING  ──► ✅ Проходит (аномалия, но сервис справился: Retry #1, устаревший API)
  40 · ERROR    ──► ✅ Проходит (конкретный запрос/задача упали с ошибкой!)
  50 · CRITICAL ──► ✅ Проходит (фатальная авария всего сервиса: БД недоступна, диск полон!)
```

---
### 2. Таблица 5 стандартных уровней: когда какой вызывать в бэкенде?
Путаница между `WARNING`, `ERROR` и `CRITICAL` приводит к тому, что дежурные инженеры либо получают ложные ночные звонки, либо пропускают реальную аварию:

| Уровень | Числовой код | Метод вызова | Чёткий инженерный критерий выбора | Реальный пример в коде |
| :--- | :--- | :--- | :--- | :--- |
| **`DEBUG`** | `10` | `logger.debug()` | Технические детали для локальной отладки разработчиком | SQL-запросы, сырые тела ответов, шаги алгоритма |
| **`INFO`** | `20` | `logger.info()` | **Штатная работа**: ключевые вехи жизненного цикла и бизнеса | `Старт сервера на :8000`, `Заказ #42 оплачен` |
| **`WARNING`** | `30` | `logger.warning()` | **Нештатная ситуация**, но запрос выполнен (или сработает `retry`) | `Запрос к банку занял 2.8с (медленно)`, `429 Rate Limit от клиента` |
| **`ERROR`** | `40` | `logger.error()` / `.exception()` | **Операция не удалась**: клиент получил `500` или упала задача Celery | `Не удалось списать оплату: таймаут шлюза после 3 попыток` |
| **`CRITICAL`** | `50` | `logger.critical()` | **Весь инстанс приложения не может работать дальше** | `Пул соединений к БД полностью мёртв`, `Не удалось загрузить ключи шифрования` |

---
### 3. Почему клиентская ошибка `400`/`404` — это НЕ `logger.error()`?
> **Junior vs Senior**:
> - **Junior**: Логирует неверный пароль пользователя (`401 Unauthorized`) или ненайденный товар (`404 Not Found`) через `logger.error()`. Когда на сайт заходит бот и перебирает 1000 несуществующих URL `/admin.php`, система мониторинга взрывается сотнями ложных алертов `ERROR`, хотя бэкенд работает идеально!
> - **Senior**: Строго разделяет **ошибки клиента (`4xx` — это `INFO` или `WARNING`)** и **ошибки сервера (`5xx` — это `ERROR`)**. Уровень `ERROR` в логах означает одно: *«Сломалась наша система или интеграция — требуется внимание инженера!»*.

---
### 4. Живая проверка: маршрутизация HTTP-статусов и событий по уровням `logging`
Проверим на Python классификатор событий и убедимся, какие сообщения проходят через порог `INFO (20)` на продакшене:

```python
import logging

def classify_http_event(status_code: int, latency_ms: int, db_down: bool = False) -> int:
    if db_down:
        return logging.CRITICAL  # 50
    if status_code >= 500:
        return logging.ERROR     # 40
    if status_code == 429 or latency_ms > 1000:
        return logging.WARNING   # 30
    if status_code >= 200:
        return logging.INFO      # 20
    return logging.DEBUG         # 10

events = [
    ("GET /items -> 200 (12ms)", 200, 12, False),
    ("GET /items/999 -> 404 (5ms)", 404, 5, False),
    ("POST /search -> 200 SLOW (1450ms)", 200, 1450, False),
    ("POST /pay -> 502 Gateway Error", 502, 300, False),
    ("DB Pool Exhausted!", 503, 5000, True),
]

prod_threshold = logging.INFO
for desc, code, ms, down in events:
    lvl = classify_http_event(code, ms, down)
    lvl_name = logging.getLevelName(lvl)
    passed = lvl >= prod_threshold
    print(f"{desc:<34} -> {lvl_name:<8} ({lvl}) | В прод-логе: {passed}")
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-212. Отладка в Python_ traceback, pdb и.md"] = r"""📖 Перечитать конспект: Отладка в Python: анатомия Traceback, breakpoint() и pdb >>
### 1. Ментальная модель: Запись чёрного ящика (`Traceback`) и Стоп-кран времени (`breakpoint()`)
Когда в Python происходит необработанное исключение, интерпретатор печатает **Traceback (Трассировку стека вызовов)**.
Новички пугаются длинного текста ошибки и читают его сверху вниз, теряясь в чужих библиотеках.
Запомните главное правило чтения Traceback: **читайте его СНИЗУ ВВЕРХ!**
1. **Самая последняя строчка** — это **ЧТО случилось** (тип исключения и сообщение, например `ZeroDivisionError: division by zero`).
2. **Строчка прямо над ней** — это **ГДЕ именно случился взрыв** (файл, номер строки и функция).
3. **Строчки выше** — это цепочка звонков: кто кого вызвал на пути к этой точке (от `main()` до места аварии).

А если нужно остановить время прямо за секунду до аварии и заглянуть внутрь всех переменных — вставьте в код встроенную функцию **`breakpoint()`** (добавлена в Python 3.7+, вызывает интерактивный отладчик **`pdb`**)!

```text
Как читать Traceback (СНИЗУ ВВЕРХ ▲):
  File "app/api.py", line 10, in create_order       (3. Кто вызвал сервис?)
    total = calc_item_price(item)
  File "app/services.py", line 25, in calc_item_price (2. ГДЕ В ВАШЕМ КОДЕ упало?) ▲
    return item["price"] / item["qty"]
ZeroDivisionError: division by zero                 (1. ЧТО СЛУЧИЛОСЬ? Деление на 0!) ▲
```

---
### 2. Горячие клавиши интерактивного отладчика `pdb` и `Post-mortem` отладка
Когда выполнение кода доходит до `breakpoint()`, программа встаёт на паузу, и в терминале открывается приглашение `(Pdb)`, где вы можете выполнять любой Python-код и двигаться по шагам:

| Команда `pdb` / `pytest` | Полное имя | Что делает? |
| :--- | :--- | :--- |
| **`n`** | `next` | Выполнить текущую строку и перейти к **следующей строке в текущей функции** (не ныряя внутрь вызовов) |
| **`s`** | `step` | **Шагнуть внутрь** вызываемой на этой строке функции (`Step Into`) |
| **`c`** | `continue` | Снять паузу и продолжить обычное выполнение до следующего `breakpoint()` |
| **`l` / `ll`** | `list` / `longlist` | Показать исходный код вокруг текущей строки со стрелочкой `->` |
| **`p expr` / `pp expr`** | `print` / `pprint` | Красиво распечатать значение любой переменной или выражения |
| **`w` (`bt`)** | `where` | Показать текущий стек вызовов (где мы находимся) |
| **`pytest --pdb`** | *Post-mortem* | Автоматически открывает отладчик `pdb` **в момент падения любого теста** с живыми переменными! |

---
### 3. Защита от забытого `breakpoint()` на продакшене (`PYTHONBREAKPOINT=0`)
> **Junior vs Senior**:
> - **Junior**: Отлаживает код десятками `print("ТУТ 1", x)`, `print("ТУТ 2")`, а если ставит `breakpoint()` — случайно коммитит его в продакшен. Когда на боевом сервере код доходит до `breakpoint()`, воркер Uvicorn навечно зависает в ожидании ввода с клавиатуры!
> - **Senior**: Использует **`pytest --pdb`** (отладчик открывается сам при падении теста без изменения файлов кода!), в CI ставит правило линтера `ruff` (**`T100`** — запрет на `breakpoint()` и `pdb.set_trace()` в коммитах), а в продакшен-контейнере задаёт переменную окружения **`PYTHONBREAKPOINT=0`**, которая мгновенно отключает любые случайно забытые `breakpoint()`.

---
### 4. Живая проверка: программный разбор стека исключения через модуль `traceback`
Используем стандартный модуль `traceback` в Python 3.13, чтобы автоматически извлечь из исключения точный файл, строку, имя функции и значения локальных переменных кадра аварии:

```python
import sys
import traceback

def apply_discount(price: int, discount_pct: int) -> float:
    factor = 100 - discount_pct
    return price / factor  # Упадёт при discount_pct == 100!

def checkout_cart() -> float:
    return apply_discount(price=2500, discount_pct=100)

try:
    checkout_cart()
except ZeroDivisionError:
    exc_type, exc_val, exc_tb = sys.exc_info()
    frames = traceback.extract_tb(exc_tb)
    last_frame = frames[-1]  # Самый нижний кадр стека — точка взрыва!
    tb_locals = exc_tb.tb_next.tb_frame.f_locals if exc_tb and exc_tb.tb_next else {}
    print(f"1. ЧТО случилось : {exc_type.__name__}: {exc_val}")
    print(f"2. ГДЕ случилось : функция '{last_frame.name}' (строка {last_frame.lineno}): {last_frame.line}")
    print(f"3. Локальные переменные в момент взрыва: {tb_locals}")
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-213. Мониторинг и метрики.md"] = r"""📖 Перечитать конспект: Мониторинг и метрики: Prometheus, Grafana, RED и перцентили p95/p99 >>
### 1. Ментальная модель: Приборная панель самолёта (`Metrics`) против Бортового журнала (`Logs`)
В чём разница между **Логами** и **Метриками**?
- **Логи** — это подробные текстовые рассказы о каждом отдельном событии (дорого хранить, медленно считать по миллионам записей).
- **Метрики** — это лёгкие числовые датчики во времени (**Time Series**), которые занимают копейки памяти и позволяют за 0.01 секунды построить графики в **Grafana** и разбудить дежурного алертом, если процент ошибок `5xx` превысил 1%!

Стандарт индустрии — связка **Prometheus + Grafana**: ваш Python-сервис выставляет эндпоинт `/metrics`, а сервер **Prometheus** сам каждые 15 секунд заходит на него (**Pull-модель**) и забирает текущие показания счётчиков.

```text
[FastAPI Сервис (/metrics)] ◄── Pull каждые 15 сек ── [Prometheus (TSDB)]
                                                             │
                                          ┌──────────────────┴──────────────────┐
                                          ▼                                     ▼
                               [Grafana (Дашборды RED)]              [Alertmanager (Telegram/PagerDuty)]
```

---
### 2. Четыре типа метрик Prometheus и метод `RED` для микросервисов
В Prometheus все показатели делятся на 4 математических типа, а для мониторинга любого HTTP-сервиса используют метод **RED** (**R**ate — число запросов в секунду `RPS`, **E**rrors — число ошибок в секунду, **D**uration — время ответа):

| Тип метрики Prometheus | Как изменяется? | Пример в Python-бэкенде |
| :--- | :--- | :--- |
| **`Counter` (Счётчик)** | **Только растёт вверх** (сбрасывается в 0 только при рестарте) | `http_requests_total`, `orders_created_total`, `errors_5xx_total` |
| **`Gauge` (Датчик / Спидометр)** | Может расти **и вверх, и вниз** | `active_db_connections`, `memory_usage_bytes`, `celery_queue_length` |
| **`Histogram` (Гистограмма)** | Раскладывает замеры по корзинам (`buckets`: `<=0.05s`, `<=0.1s`, `<=0.5s`) | `http_request_duration_seconds` — позволяет считать **перцентили `p95` и `p99`**! |
| **`Summary` (Сводка)** | Считает квантили прямо на стороне клиента Python | Редко используется в кластерах (нельзя агрегировать между репликами) |

---
### 3. Почему «Среднее время ответа (Average Latency)» нагло врёт?
Это любимый вопрос архитекторов на собеседованиях!
Представьте, что к вашему API пришло 100 запросов: **99 запросов** отработали мгновенно за **10 мс**, а **1 запрос** (оформление крупного VIP-заказа) завис на **10 000 мс (10 секунд!)**.
Чему равно **среднее арифметическое**? $\approx 110\text{ мс}$ — на графике средней скорости всё выглядит прекрасно!
А чему равен **99-й перцентиль (`p99`)**? **`10 000 мс`**! Перцентиль **`p95` / `p99`** показывает время, за которое укладываются 95% или 99% самых медленных запросов реальных пользователей.

> **Junior vs Senior**:
> - **Junior**: Смотрит только на график `Average Latency`, а в метрики Prometheus добавляет метку (label) `user_id` или `email`: `http_requests_total{user_id="..."}`. В итоге для 1 миллиона пользователей создаётся 1 миллион отдельных временных рядов (**High Cardinality Explosion**), и сервер Prometheus падает от нехватки оперативной памяти (`OOM`)!
> - **Senior**: Строит дашборды и алерты строго по перцентилям **`p95` и `p99`** из `Histogram`, а в метки (`labels`) метрик кладёт только ограниченный набор значений: `method`, `route_template` (`/users/{id}`, а не `/users/42`!) и `status_code`.

---
### 4. Живая проверка: почему `p99` разоблачает латентные тормоза, которые прячет `Average`
Сравним на Python среднее арифметическое (`mean`) и перцентили `p50` (медиану), `p95`, `p99` на реальном распределении задержек API:

```python
def percentile(sorted_data: list[float], pct: int) -> float:
    idx = max(0, int(len(sorted_data) * pct / 100) - 1)
    return sorted_data[idx]

# 95 быстрых запросов по 15 мс, 4 запроса по 450 мс и 1 тяжёлый запрос на 4800 мс:
latencies_ms = sorted([15.0] * 95 + [450.0] * 4 + [4800.0])
avg_ms = sum(latencies_ms) / len(latencies_ms)

print(f"Обманчивое Среднее (Average) : {avg_ms:.1f} мс (кажется, что всё летает!)")
print(f"Медиана (p50)                : {percentile(latencies_ms, 50):.1f} мс")
print(f"95-й перцентиль (p95)        : {percentile(latencies_ms, 95):.1f} мс")
print(f"99-й перцентиль (p99, ХВОСТ!): {percentile(latencies_ms, 99):.1f} мс (видна реальная боль VIP-клиентов!)")
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-214. Sentry_ мониторинг ошибок в продакшене.md"] = r"""📖 Перечитать конспект: Sentry: перехват, группировка и диагностика ошибок в продакшене >>
### 1. Ментальная модель: Автоматический криминалист на месте происшествия
Когда на продакшене у пользователя случается `500 Internal Server Error`, искать причину вручную по миллионам строк текстовых логов — долго и мучительно. Более того: если одна ошибка случилась 10 000 раз за минуту, в логах будет 10 000 одинаковых простыней текста.
**Sentry** — это система отслеживания ошибок (Error Tracking), которая подключается к вашему FastAPI / Django / Celery всего **тремя строчками кода** через `DSN`-ключ и при любом необработанном исключении автоматически делает полный криминалистический снимок:
1. **Fingerprint & Grouping**: схлопывает 10 000 одинаковых падений в **одну карточку Issue** со счётчиком `Events: 10k` и числом пострадавших пользователей (`Users affected: 85`).
2. **Stack Trace + Local Variables**: показывает точный код вокруг строки взрыва и значения всех переменных в момент падения.
3. **Breadcrumbs («Хлебные крошки»)**: хронология действий за секунды до аварии (какой SQL-запрос выполнялся в SQLAlchemy, какой HTTP-вызов ушёл в банк, какой лог записался).

```text
Исключение в FastAPI / Celery
             │
             ▼ (перехватывается Sentry SDK автоматически!)
┌──────────────────────────────────────────────────────────────────────┐
│ Снимок события (Sentry Event):                                       │
│  • Stacktrace + значения локальных переменных в каждом кадре         │
│  • Breadcrumbs: [SQL SELECT user] ──► [HTTP POST bank] ──► [CRASH!] │
│  • Контекст   : user_id=42, release="billing@1.4.2", env="prod"      │
│  • Фильтр PII : пароли, токены и cookies вырезаны (send_default_pii) │
└──────────────────────────────────────────────────────────────────────┘
```

---
### 2. Интеграция `sentry-sdk` в Python и обогащение контекста
Чтобы Sentry автоматически связал ошибки FastAPI, SQLAlchemy и воркеров Celery в единую картину, достаточно инициализировать SDK при старте приложения:

```python
# Инициализация на старте приложения (конфигурация из окружения):
# sentry_sdk.init(
#     dsn=os.environ["SENTRY_DSN"],
#     environment="production",
#     release="billing-api@1.4.2",
#     send_default_pii=False,        # Безопасность: не слать пароли и cookies!
#     traces_sample_rate=0.1,        # Профилирование 10% транзакций (Performance)
# )
```

| Механизм Sentry | Что он даёт разработчику? | Как управляется в коде? |
| :--- | :--- | :--- |
| **Breadcrumbs (Хлебные крошки)** | Показывает цепочку SQL-запросов, HTTP-вызовов и логов перед падением | Собирается автоматически + `sentry_sdk.add_breadcrumb(...)` |
| **User & Tags Context** | Позволяет фильтровать ошибки по `user_id`, тарифу или региону | `sentry_sdk.set_user({"id": 42})`, `set_tag("plan", "pro")` |
| **Release Tracking** | Показывает, **какой именно релиз/коммит** породил новую ошибку | Параметр `release="1.4.2-f89a12b"` в `init()` |
| **Scrubbing (`before_send`)** | Вырезает секреты и персональные данные перед отправкой по сети | Хук `before_send(event, hint)` + `send_default_pii=False` |

---
### 3. Безопасность данных (PII) и защита от «Голого `except Exception: pass`»
> **Junior vs Senior**:
> - **Junior**: Оборачивает код в `try: ... except Exception: logger.info("ошибка")`, проглатывая исключение (из-за чего Sentry вообще не узнаёт о падении!), или отправляет в Sentry сырые тела запросов с паролями и данными банковских карт.
> - **Senior**: Если исключение перехвачено в `try/except`, но о нём нужно сообщить в мониторинг, явно вызывает **`sentry_sdk.capture_exception(exc)`** (или `logger.exception()`), привязывает тег релиза `release` и настраивает хук **`before_send`** для очистки чувствительных полей (`password`, `token`, `authorization`).

---
### 4. Живая проверка: симулятор группировки Sentry (`Fingerprint`), `Breadcrumbs` и очистки `before_send`
Реализуем на Python конвейер обработки исключений в стиле `sentry-sdk`: запись хлебных крошек, очистку секретов в `before_send` и дедупликацию ошибок по `fingerprint`:

```python
class MiniSentryClient:
    def __init__(self) -> None:
        self.breadcrumbs: list[str] = []
        self.issues: dict[str, dict] = {}

    def add_breadcrumb(self, category: str, message: str) -> None:
        self.breadcrumbs.append(f"[{category}] {message}")

    def before_send_scrub(self, payload: dict) -> dict:
        clean = payload.copy()
        for sensitive in ("password", "card_cvv", "secret_token"):
            if sensitive in clean:
                clean[sensitive] = "[Filtered]"
        return clean

    def capture_exception(self, exc: Exception, func_name: str, request_data: dict) -> str:
        fingerprint = f"{type(exc).__name__}@{func_name}"
        scrubbed_data = self.before_send_scrub(request_data)
        if fingerprint not in self.issues:
            self.issues[fingerprint] = {
                "count": 0,
                "breadcrumbs": list(self.breadcrumbs),
                "sample_request": scrubbed_data,
            }
        self.issues[fingerprint]["count"] += 1
        return fingerprint

sentry = MiniSentryClient()
sentry.add_breadcrumb("sql", "SELECT * FROM users WHERE id = 42")
sentry.add_breadcrumb("http", "POST https://bank.example/charge -> 503")

for _ in range(3):  # Ошибка произошла 3 раза подряд
    fp = sentry.capture_exception(TimeoutError("Bank timeout"), "charge_card", {"user_id": 42, "card_cvv": "999"})

issue = sentry.issues[fp]
print(f"Issue '{fp}' сгруппирован (count={issue['count']})")
print(f"Хлебные крошки до падения : {issue['breadcrumbs']}")
print(f"Очищенные данные (PII)    : {issue['sample_request']}")
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-215. Celery, Redis и Django_ асинхронные задачи.md"] = r"""📖 Перечитать конспект: Celery, Redis и Django/FastAPI: боевая архитектура фоновых задач >>
### 1. Ментальная модель: Фабрика фоновых воркеров (`Worker`) и Будильник по расписанию (`Celery Beat`)
В реальном бэкенде фоновые задачи бывают двух видов:
1. **Реактивные (по событию от пользователя)**: пользователь нажал «Оформить заказ» ➔ API вызвал `generate_invoice.delay(order_id)` ➔ **Celery Worker** тут же подхватил задачу из **Redis**.
2. **Периодические (по расписанию, как `cron`)**: каждую ночь в 03:00 нужно списывать абонентскую плату или чистить просроченные токены. За это отвечает отдельный процесс-планировщик **`Celery Beat`** — он работает как будильник: сам тяжёлую работу не делает, а просто по расписанию закидывает билетики задач в Redis для воркеров!

```text
[Django / FastAPI] ──task.delay(42)──┐
                                     ▼
[Celery Beat (Расписание)] ──► [ Брокер Redis ] ──► [ Пул Celery Workers ]
                                                           │
                                                           ▼
                                                    [ База данных PostgreSQL ]
```

---
### 2. Самая коварная ловушка Django + Celery: гонка транзакции БД и `transaction.on_commit`!
Представьте классический код в сервисе оплаты:
```python
# ❌ ОПАСНЫЙ КОД (Race Condition между Postgres и Redis!):
def create_order_bad(data):
    with transaction.atomic():
        order = Order.objects.create(status="PAID")   # 1. Запись ещё в незакоммиченной транзакции!
        send_receipt_task.delay(order.id)             # 2. Задача мгновенно (за 0.5 мс) улетела в Redis!
        # ... тут ещё 50 мс выполняется код до COMMIT в Postgres ...
```
Что произойдёт на быстром сервере? Воркер Celery схватит задачу из Redis за **1 миллисекунду** и сделает `Order.objects.get(id=order.id)`, пока транзакция в веб-сервере **ещё НЕ закоммитилась**! Воркер получит ошибку **`Order.DoesNotExist`** и упадёт!
**Решение сеньора**: всегда отправлять задачу в очередь только **после успешного `COMMIT`** транзакции БД через хук **`transaction.on_commit(lambda: send_receipt_task.delay(order.id))`**!

```python
# ✅ ЭТАЛОННЫЙ НАДЁЖНЫЙ ТАСК CELERY:
# @shared_task(
#     bind=True,
#     autoretry_for=(TimeoutError, ConnectionError),
#     retry_backoff=True,           # Экспоненциальная пауза: 1с, 2с, 4с, 8с...
#     retry_jitter=True,            # Случайный разброс, чтобы не положить внешний сервис
#     max_retries=5,
#     acks_late=True,               # Подтверждать задачу в брокере ТОЛЬКО после выполнения!
# )
# def send_receipt_task(self, order_id: int) -> None: ...
```

| Настройка Celery | Зачем она жизненно необходима на продакшене? |
| :--- | :--- |
| **`transaction.on_commit(...)`** | Гарантирует, что задача улетит в Redis **только после** того, как запись реально сохранена (`COMMIT`) в PostgreSQL |
| **`acks_late=True`** | По умолчанию Celery удаляет задачу из брокера *до* начала выполнения. С `acks_late=True` задача подтверждается **после завершения** (не потеряется при рестарте контейнера!) |
| **`retry_backoff=True`** | При падении внешнего API делает паузы $1\text{с} \to 2\text{с} \to 4\text{с} \to 8\text{с}$, давая внешнему сервису восстановиться |
| **`soft_time_limit` / `time_limit`** | Защищает воркер от вечного зависания на одном запросе без таймаута |
| **Строго 1 экземпляр `Celery Beat`** | Если запустить 2 контейнера `celery beat`, каждая периодическая задача будет запускаться **дважды**! |

---
### 3. Архитектура надёжных фоновых пайплайнов
> **Junior vs Senior**:
> - **Junior**: Вызывает `.delay(order.id)` прямо посередине открытой транзакции БД, ловя плавающий `DoesNotExist`, не ставит `time_limit` и масштабирует контейнер `celery beat` до 3 реплик вместе с воркерами, списывая подписку с клиентов по 3 раза.
> - **Senior**: Оборачивает вызов `.delay()` в `transaction.on_commit`, включает `acks_late=True` + `retry_backoff=True`, делает задачи идемпотентными и разделяет очереди по приоритетам (`-Q high_priority,default`), чтобы генерация тяжёлого месячного отчёта не задержала отправку SMS-кода входа.

---
### 4. Живая проверка: как `transaction.on_commit` спасает от гонки `DoesNotExist`
Наглядно воспроизведём на Python гонку между открытой транзакцией БД и быстрым воркером Celery, и убедимся, как хук `on_commit` на 100% устраняет проблему:

```python
class DatabaseWithTransactions:
    def __init__(self) -> None:
        self.committed_rows: dict[int, str] = {}
        self._staged_rows: dict[int, str] = {}
        self._on_commit_hooks: list = []

    def insert_in_tx(self, row_id: int, val: str) -> None:
        self._staged_rows[row_id] = val  # Ещё НЕ видно другим процессам (READ COMMITTED)!

    def on_commit(self, callback) -> None:
        self._on_commit_hooks.append(callback)

    def commit(self) -> None:
        self.committed_rows.update(self._staged_rows)
        self._staged_rows.clear()
        while self._on_commit_hooks:
            hook = self._on_commit_hooks.pop(0)
            hook()

db = DatabaseWithTransactions()
worker_log: list[str] = []

def celery_worker_read(order_id: int) -> None:
    if order_id in db.committed_rows:
        worker_log.append(f"SUCCESS ✅: воркер увидел заказ #{order_id} ({db.committed_rows[order_id]})")
    else:
        worker_log.append(f"RACE ERROR ❌: DoesNotExist! Заказ #{order_id} ещё не закоммичен в БД!")

# 1. Ошибка новичка: вызов воркера ДО commit()
db.insert_in_tx(101, "Order #101")
celery_worker_read(101)  # Воркер сработал мгновенно до commit!
db.commit()

# 2. Решение сеньора: вызов через db.on_commit()
db.insert_in_tx(102, "Order #102")
db.on_commit(lambda: celery_worker_read(102))
db.commit()

for entry in worker_log:
    print(entry)
```
"""

NOTES[r"Юнит 7.6 · Очереди и мониторинг\📚 Конспекты\К-216. Health checks_ readiness и liveness.md"] = r"""📖 Перечитать конспект: Health Checks: Liveness, Readiness и Startup пробы для Zero-Downtime >>
### 1. Ментальная модель: «Пульс бьётся» (`Liveness`) vs «Готов принимать клиентов» (`Readiness`)
Как Kubernetes, Docker или балансировщик нагрузки понимают, что ваш контейнер с Python-бэкендом жив и способен обрабатывать трафик? Через специальные проверочные HTTP-эндпоинты — **Health Checks (Пробы здоровья)**!
Но почему нельзя сделать всего один эндпоинт `/health` на все случаи жизни? Потому что у оркестратора есть **два совершенно разных действия**:
1. **`Liveness Probe` (`/health/live` — Проверка живучести)**: отвечает на вопрос *«Не завис ли сам процесс Python в вечном дедлоке?»*. Если эта проба падает — оркестратор **УБИВАЕТ и перезапускает контейнер (`Restart`)**.
2. **`Readiness Probe` (`/health/ready` — Проверка готовности)**: отвечает на вопрос *«Может ли этот контейнер прямо сейчас обслуживать запросы клиентов (доступны ли БД и Redis)?»*. Если эта проба падает — оркестратор **НЕ убивает контейнер**, а просто **временно убирает его из балансировщика трафика**, пока база данных не ответит снова!

```text
Оркестратор (Kubernetes / Балансировщик)
  │
  ├──► GET /health/live  (проверяет только цикл событий Python)
  │      └── Если 500/Timeout ──► 🔨 ПЕРЕЗАПУСТИТЬ КОНТЕЙНЕР (Restart Pod)
  │
  └──► GET /health/ready (делает SELECT 1 в Postgres и PING в Redis)
         └── Если 503         ──► 🚧 УБРАТЬ ИЗ ТРАФИКА (Контейнер жив, ждёт БД!)
```

---
### 2. Три типа проб и смертельная опасность проверки БД в `Liveness Probe`
Подумайте, что случится, если вы по ошибке вставите проверку `SELECT 1` к базе данных внутрь **`Liveness Probe`**!
Допустим, база данных PostgreSQL моргнула на 5 секунд из-за переключения реплики. Все 20 ваших контейнеров API одновременно возвращают `500` на `Liveness Probe` ➔ Kubernetes думает, что все 20 контейнеров зависли, и **одновременно убивает и перезапускает все 20 серверов приложения (`Cascading Restart Storm`)**, устраивая полный даунтайм сайта на ровном месте!

| Тип пробы | Эндпоинт | Что проверяется внутри? | Действие оркестратора при отказе |
| :--- | :--- | :--- | :--- |
| **`Startup Probe`** | `/health/startup` | Завершилась ли тяжёлая инициализация при холодном старте (прогрев кэша, ML-модели) | Ждёт окончания старта, блокируя `Liveness`, чтобы не убить медленно стартующий сервис |
| **`Liveness Probe`** | `/health/live` | **Только сам процесс** (мгновенный `return {"status": "alive"}` без походов в БД и внешние API!) | **Убивает и пересоздаёт контейнер** (`docker restart` / `Restart Pod`) |
| **`Readiness Probe`** | `/health/ready` | Короткий `SELECT 1` в БД + `PING` в Redis с жёстким таймаутом 1–2 сек | **Отключает подачу пользовательского трафика** на этот инстанс (возвращает `503 Service Unavailable`) |

---
### 3. Как `Readiness Probe` обеспечивает деплой без единой ошибки (`Zero-Downtime Rolling Update`)
> **Junior vs Senior**:
> - **Junior**: Делает один эндпоинт `/health`, который ходит во все внешние микросервисы и базу данных, и вешает его и на `liveness`, и на `readiness`. При малейшем лаге соседнего сервиса весь кластер уходит в бесконечный цикл перезагрузок (`CrashLoopBackOff`).
> - **Senior**: Держит `/health/live` абсолютно легковесным и автономным, а в `/health/ready` проверяет критические хранилища (`Postgres`, `Redis`) и выключает `Readiness` сразу при получении сигнала `SIGTERM`, чтобы балансировщик перестал слать новые запросы на останавливающийся контейнер ещё до того, как закроется соединение!

---
### 4. Живая проверка: маршрутизация трафика и оркестрация по `Liveness` vs `Readiness`
Смоделируем на Python поведение Kubernetes при кратковременном сбое БД и убедимся, почему разделение проб спасает кластер от каскадного рестарта:

```python
def liveness_endpoint(event_loop_responsive: bool) -> int:
    # Никаких обращений к БД! Только проверка, что сам процесс Python не завис:
    return 200 if event_loop_responsive else 500

def readiness_endpoint(event_loop_responsive: bool, db_ok: bool, redis_ok: bool, shutting_down: bool) -> int:
    if not event_loop_responsive or shutting_down or not db_ok or not redis_ok:
        return 503  # 503 Service Unavailable -> временно убрать из балансировщика
    return 200

def k8s_probe_decision(loop_ok: bool, db_ok: bool, redis_ok: bool, sigterm: bool = False) -> dict:
    live_code = liveness_endpoint(loop_ok)
    ready_code = readiness_endpoint(loop_ok, db_ok, redis_ok, sigterm)
    action = "KILL_AND_RESTART_POD 🔨" if live_code != 200 else (
        "SEND_TRAFFIC 🟢" if ready_code == 200 else "REMOVE_FROM_LOAD_BALANCER 🚧 (Keep Pod Alive!)"
    )
    return {"live": live_code, "ready": ready_code, "k8s_action": action}

print("1. Штатная работа (всё живо)      :", k8s_probe_decision(loop_ok=True, db_ok=True, redis_ok=True))
print("2. Кратковременный рестарт БД     :", k8s_probe_decision(loop_ok=True, db_ok=False, redis_ok=True))
print("3. Получен SIGTERM при деплое     :", k8s_probe_decision(loop_ok=True, db_ok=True, redis_ok=True, sigterm=True))
print("4. Процесс Python завис в дедлоке :", k8s_probe_decision(loop_ok=False, db_ok=True, redis_ok=True))
```
"""


def main() -> None:
    # 1. Перемещаем Ф-204 из Юнит 7.2 в Юнит 7.3 (где он используется по Карте Мастерства в навыке 7.3.1)
    src_f204 = os.path.join(MOD7_DIR, r"Юнит 7.2 · Docker основы\📇 Карточки\Ф-204. Docker Hub и теги образов.md")
    dst_f204 = os.path.join(MOD7_DIR, r"Юнит 7.3 · Docker продвинутый\📇 Карточки\Ф-204. Docker Hub и теги образов.md")
    if os.path.exists(src_f204):
        os.makedirs(os.path.dirname(dst_f204), exist_ok=True)
        shutil.move(src_f204, dst_f204)
        print("Moved Ф-204 to Юнит 7.3 · Docker продвинутый\\📇 Карточки\\")

    # 2. Обновляем ссылку на Ф-204 в 00 · 🗺️ Карта Мастерства.md
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE, "r", encoding="utf-8") as f:
            map_text = f.read()
        old_link = "[[07 · 🚀 Инфраструктура/Юнит 7.2 · Docker основы/📇 Карточки/Ф-204. Docker Hub и теги образов]]"
        new_link = "[[07 · 🚀 Инфраструктура/Юнит 7.3 · Docker продвинутый/📇 Карточки/Ф-204. Docker Hub и теги образов]]"
        if old_link in map_text:
            map_text = map_text.replace(old_link, new_link)
            with open(MAP_FILE, "w", encoding="utf-8") as f:
                f.write(map_text)
            print("Updated Ф-204 link in 00 · 🗺️ Карта Мастерства.md")

    # 3. Записываем все 47 обогащённых конспектов К-170..К-216
    assert len(NOTES) == 47, f"Expected 47 notes, got {len(NOTES)}"
    for rel_path, content in NOTES.items():
        full_path = os.path.join(MOD7_DIR, rel_path)
        assert os.path.exists(full_path), f"Missing target file: {full_path}"
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

    print(f"Successfully enriched all {len(NOTES)} K-notes of Module 07 (К-170..К-216)!")


if __name__ == "__main__":
    main()
