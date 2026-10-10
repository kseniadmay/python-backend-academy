# -*- coding: utf-8 -*-
import shutil
import re
import os
import subprocess

ACADEMY_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html"
BACKUP_PATH = r"C:\Users\fury6\OneDrive\Python_Backend_Academy\academy.html.bak"

shutil.copyfile(ACADEMY_PATH, BACKUP_PATH)
print("Backup created at academy.html.bak")

with open(ACADEMY_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Стили CSS для echelon-topbar-clean и dots-necklace
css_to_add = """
  /* ================= CLEAN ECHELON TOPBAR & JEWEL DOTS NECKLACE ================= */
  .echelon-topbar-clean {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 18px;
    margin-bottom: 20px;
    border-radius: 18px;
    background: var(--surface);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow: var(--shadow-1);
  }
  .echelon-clean-wrap {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .echelon-clean-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.78rem;
    font-weight: 700;
  }
  .echelon-clean-track {
    height: 6px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.04);
  }
  .echelon-clean-fill {
    height: 100%;
    border-radius: 999px;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.45);
    transition: width .35s ease;
  }
  .topic-eyebrow-track {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 12px;
    padding: 0 2px;
  }
  .topic-eyebrow-tags {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.76rem;
    font-weight: 700;
    color: var(--ink-muted);
  }
  .topic-eyebrow-unit {
    color: var(--ink);
    font-weight: 800;
  }
  .topic-eyebrow-num {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.25);
    color: var(--moss);
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.70rem;
    font-weight: 700;
  }
  .dots-necklace {
    display: flex;
    align-items: center;
    gap: 9px;
    position: relative;
    padding: 4px 6px;
  }
  .dots-necklace-wire {
    position: absolute;
    left: 8px;
    right: 28px;
    height: 1.5px;
    background: rgba(255, 255, 255, 0.10);
    z-index: 1;
  }
  .dots-necklace-wire-active {
    position: absolute;
    left: 8px;
    height: 1.5px;
    background: #10b981;
    box-shadow: 0 0 6px #10b981;
    z-index: 2;
    transition: width .3s ease;
  }
  .dot-jewel {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #0d1016;
    border: 1.5px solid rgba(255, 255, 255, 0.18);
    position: relative;
    z-index: 3;
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
  }
  .dot-jewel:hover {
    transform: scale(1.4);
  }
  .dot-jewel.done {
    background: #10b981;
    border-color: #34d399;
    box-shadow: 0 0 7px rgba(16, 185, 129, 0.75);
  }
  .dot-jewel.active {
    width: 14px;
    height: 14px;
    background: #34d399;
    border: 2px solid #ffffff;
    box-shadow: 0 0 12px #10b981, 0 0 24px rgba(52, 211, 153, 0.9);
    animation: jewel-pulse 2s infinite ease-in-out;
  }
  .dot-jewel.milestone {
    border-color: rgba(245, 158, 11, 0.6);
    background: rgba(245, 158, 11, 0.15);
  }
  .dots-necklace-label {
    font-size: 0.72rem;
    font-family: var(--font-m);
    font-weight: 800;
    color: var(--moss);
    margin-left: 2px;
    position: relative;
    z-index: 3;
  }
"""

if ".echelon-topbar-clean" not in content:
    target_css_insert = "  /* ---------- Section 7: Interview Priority Echelons, Header Overlap Fix & Skill Tree Polish ---------- */"
    content = content.replace(target_css_insert, target_css_insert + "\n" + css_to_add, 1)
    print("Added CSS styles")

# 2. Обновление INTERVIEW_ECHELONS
old_ech = """const INTERVIEW_ECHELONS = {
  1: { tier: 1, icon: '🚨', badgeClass: 'echelon-badge--t1', label: '🚨 Эшелон 1 · Скрининг и база', shortLabel: '🚨 Эшелон 1', desc: 'Отсев на HR/тех-скрининге и первых 15 минутах собеседования (Python Core, Сложность и Два указателя, HTTP/REST, SQL JOIN, Git и pytest)' },
  2: { tier: 2, icon: '🔥', badgeClass: 'echelon-badge--t2', label: '🔥 Эшелон 2 · Тех-ядро и стек', shortLabel: '🔥 Эшелон 2', desc: 'Основное техническое собеседование по выбранному стеку (ООП, Итераторы, GIL/Asyncio, FastAPI + SQLAlchemy или Django + DRF, ACID/Индексы, Docker, Веб-безопасность)' },
  3: { tier: 3, icon: '⚡', badgeClass: 'echelon-badge--t3', label: '⚡ Эшелон 3 · Продакшен-инженерия', shortLabel: '⚡ Эшелон 3', desc: 'Вопросы уровня Strong Junior / Middle (Redis, Celery/Kafka, SOLID и Чистая архитектура, Сложные графы и DP, CI/CD, Linux/Nginx, Observability)' },
  4: { tier: 4, icon: '👑', badgeClass: 'echelon-badge--t4', label: '👑 Эшелон 4 · Архитектурный резерв', shortLabel: '👑 Эшелон 4', desc: 'Второй стек в резерве (невыбранная ветка стека + Flask, DDD, Highload System Design)' }
};"""

new_ech = """const INTERVIEW_ECHELONS = {
  1: { tier: 1, icon: '🚨', badgeClass: 'echelon-badge--t1', label: '🚨 Эшелон 1: Скрининг · Базовый Python', shortLabel: '🚨 Эшелон 1: Скрининг', focus: 'Базовый Python', targetLabel: 'к скринингу', desc: 'Первичный отсев на HR и тех-скрининге (Python Core, сложность O(n), два указателя, SQL JOIN, HTTP/REST, Git и pytest)', color: '#34d399', gradient: 'linear-gradient(90deg, #f43f5e, #34d399)' },
  2: { tier: 2, icon: '🎯', badgeClass: 'echelon-badge--t2', label: '🎯 Эшелон 2: Тех-интервью · Стек и базы данных', shortLabel: '🎯 Эшелон 2: Тех-интервью', focus: 'Стек и базы данных', targetLabel: 'к тех-интервью', desc: 'Основное техническое собеседование по выбранному стеку (ООП, Итераторы, Asyncio/GIL, FastAPI + SQLAlchemy или Django + DRF, ACID/Индексы, Docker)', color: '#fbbf24', gradient: 'linear-gradient(90deg, #f59e0b, #10b981)' },
  3: { tier: 3, icon: '⚡', badgeClass: 'echelon-badge--t3', label: '⚡ Эшелон 3: Лайвкодинг · Сервисы и продакшен', shortLabel: '⚡ Эшелон 3: Лайвкодинг', focus: 'Сервисы и продакшен', targetLabel: 'к лайвкодингу', desc: 'Инженерия уровня Strong Junior / Middle (Redis, Celery/Kafka, SOLID и Чистая архитектура, CI/CD, Linux/Nginx, Observability)', color: '#34d399', gradient: 'linear-gradient(90deg, #10b981, #06b6d4)' },
  4: { tier: 4, icon: '👑', badgeClass: 'echelon-badge--t4', label: '👑 Эшелон 4: Финал · Системный дизайн и оффер', shortLabel: '👑 Эшелон 4: Финал', focus: 'Системный дизайн и оффер', targetLabel: 'к офферу', desc: 'Конкурентное преимущество на оффер (Highload, System Design, паттерны проектирования, альтернативный фреймворк в резерве)', color: '#c084fc', gradient: 'linear-gradient(90deg, #a855f7, #ec4899)' }
};"""

if old_ech in content:
    content = content.replace(old_ech, new_ech, 1)
    print("Updated INTERVIEW_ECHELONS")

with open(ACADEMY_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved academy.html intermediate")
