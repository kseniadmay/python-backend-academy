# 🚀 Развёртывание и сервисное окружение (`deploy/`)

В этой директории находятся конфигурации демонов systemd и инструкции для развёртывания платформы **Python Backend Academy** на выделенных серверах (Linux VPS) и в облачных сервисах.

---

## 📁 Содержимое

| Файл | Описание |
|---|---|
| [`systemd/academy_fastapi.service`](systemd/academy_fastapi.service) | Юнит systemd для запуска модульного бэкенда на **FastAPI** (`python3 -m backend.run`) |
| [`systemd/academy_node.service`](systemd/academy_node.service) | Юнит systemd для легковесного Node.js сервера синхронизации (`node scripts/server.js`) |

---

## 🛠️ Установка и управление службой на Linux

### 1. Выбор и копирование юнита

Для основного бэкенда на FastAPI:
```bash
# Копирование в пользовательский каталог systemd:
mkdir -p ~/.config/systemd/user
cp deploy/systemd/academy_fastapi.service ~/.config/systemd/user/academy.service

# Либо общесистемная установка (требует sudo):
sudo cp deploy/systemd/academy_fastapi.service /etc/systemd/system/academy.service
```

### 2. Запуск и автозагрузка

```bash
# Пользовательский режим:
systemctl --user daemon-reload
systemctl --user enable --now academy.service
systemctl --user status academy.service

# Системный режим:
sudo systemctl daemon-reload
sudo systemctl enable --now academy.service
sudo systemctl status academy.service
```

### 3. Просмотр логов

```bash
# Для пользовательского юнита:
journalctl --user -u academy.service -f

# Для системного юнита:
sudo journalctl -u academy.service -f
```

---

## ☁️ Подключение базы данных (PostgreSQL / Neon)

1. Подключение к СУБД PostgreSQL настраивается через переменную окружения `DATABASE_URL` (например, Neon Database или локальный инстанс).
2. Секретный токен синхронизации задаётся переменной `SYNC_TOKEN`.
