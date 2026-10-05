# -*- coding: utf-8 -*-
"""
sync_feedback_backlog.py
Синхронизирует очередь фидбека (data/user_feedback_queue.json) и GitHub Gist
с единым журналом замечаний FEEDBACK_BACKLOG.md.
"""
import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
QUEUE_FILE = os.path.join(DATA_DIR, 'user_feedback_queue.json')
BACKLOG_FILE = os.path.join(ROOT_DIR, 'FEEDBACK_BACKLOG.md')

def load_local_queue():
    if not os.path.isfile(QUEUE_FILE):
        return []
    try:
        with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[!] Ошибка чтения {QUEUE_FILE}: {e}")
        return []

def load_gist_queue():
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_GIST_TOKEN')
    gist_id = os.environ.get('GIST_ID') or os.environ.get('ACADEMY_GIST_ID')
    if not token or not gist_id:
        return []
    try:
        url = f"https://api.github.com/gists/{gist_id}"
        req = urllib.request.Request(url, headers={
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Python-Backend-Academy-Sync',
            'Accept': 'application/vnd.github+json'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            files = data.get('files', {})
            feedback_file = files.get('academy_feedback.json') or files.get('user_feedback_queue.json')
            if feedback_file and 'content' in feedback_file:
                items = json.loads(feedback_file['content'])
                return items if isinstance(items, list) else []
    except Exception as e:
        print(f"[!] Пропуск Gist синхронизации (нет доступа или ошибка сети): {e}")
    return []

def get_existing_rev_ids(backlog_text):
    return set(re.findall(r'REV-\d+', backlog_text))

def sync():
    if not os.path.isfile(BACKLOG_FILE):
        print(f"[!] Файл бэклога {BACKLOG_FILE} не найден.")
        return False

    with open(BACKLOG_FILE, 'r', encoding='utf-8') as f:
        backlog_text = f.read()

    existing_ids = get_existing_rev_ids(backlog_text)
    local_items = load_local_queue()
    gist_items = load_gist_queue()

    combined_items = local_items + [g for g in gist_items if g not in local_items]
    added_count = 0

    # Determine next REV ID number
    max_num = 5
    for rid in existing_ids:
        m = re.match(r'REV-(\d+)', rid)
        if m:
            max_num = max(max_num, int(m.group(1)))

    new_entries = []
    for item in combined_items:
        text = (item.get('text') or '').strip()
        ctx = (item.get('context') or '').strip()
        ts = item.get('createdAt') or item.get('timestamp') or datetime.now().isoformat()
        
        # Check if already in backlog
        if text and text in backlog_text:
            continue

        max_num += 1
        new_id = f"REV-{max_num:03d}"
        entry = (
            f"\n### [{new_id}] {text.splitlines()[0][:80]}\n"
            f"- **Статус**: [ ] Запланировано\n"
            f"- **Контекст**: `{ctx}`\n"
            f"- **Дата**: {ts}\n"
            f"- **Описание**: {text}\n"
        )
        new_entries.append(entry)
        added_count += 1

    if new_entries:
        updated_text = backlog_text + "\n" + "\n".join(new_entries)
        with open(BACKLOG_FILE, 'w', encoding='utf-8', newline='\n') as f:
            f.write(updated_text)
        print(f"[+] Добавлено {added_count} новых замечаний в {BACKLOG_FILE}")
    else:
        print(f"[✓] Бэклог {BACKLOG_FILE} синхронизирован, новых замечаний нет.")

    return True

if __name__ == '__main__':
    sync()
