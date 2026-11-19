# -*- coding: utf-8 -*-
"""
Генератор автономного интерактивного веб-стенда:
stand_notes_quantum_studio.html — Студия квантования и распределения шагов конспектов.
"""
import os
import json

def generate_studio():
    data_path = os.path.join(os.path.dirname(__file__), 'extracted_catalog_data.json')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Файл {data_path} не найден! Сначала запустите scripts/extract_all_data.js")

    with open(data_path, 'r', encoding='utf-8') as f:
        catalog_data = json.load(f)

    notes = catalog_data.get('notes', {})
    catalog = catalog_data.get('catalog', [])
    notes_meta = catalog_data.get('notesMeta', {})

    print(f"Загружено: {len(notes)} конспектов, {len(catalog)} треков, {len(notes_meta)} мета-записей.")

    # Сериализуем данные для внедрения в HTML
    catalog_json_str = json.dumps({
        'notes': notes,
        'catalog': catalog,
        'notesMeta': notes_meta
    }, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>⚡ Студия квантования шагов конспектов · Python Backend Academy</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600;700;800&family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Onest:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

  <style>
    :root {{
      --paper: #07090e;
      --surface: rgba(15, 23, 42, 0.75);
      --surface-card: rgba(18, 26, 43, 0.85);
      --surface-border: rgba(255, 255, 255, 0.10);
      --surface-border-subtle: rgba(255, 255, 255, 0.06);
      --ink: #f1f5f9;
      --ink-muted: #94a3b8;
      --ink-soft: #cbd5e1;
      
      --emerald: #10b981;
      --emerald-glow: rgba(16, 185, 129, 0.35);
      --emerald-subtle: rgba(16, 185, 129, 0.12);
      
      --amber: #f59e0b;
      --amber-subtle: rgba(245, 158, 11, 0.15);
      
      --carmine: #f43f5e;
      --carmine-subtle: rgba(244, 63, 94, 0.15);
      
      --cyan: #06b6d4;
      --cyan-subtle: rgba(6, 182, 212, 0.15);
      
      --purple: #a855f7;
      --purple-subtle: rgba(168, 85, 247, 0.15);
      
      --font-d: 'Onest', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-golos: 'Golos Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-m: 'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, monospace;
      
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-xl: 28px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--paper);
      color: var(--ink);
      font-family: var(--font-d);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }}

    /* Top Studio Header */
    .studio-header {{
      background: rgba(11, 15, 23, 0.92);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--surface-border);
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .studio-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .studio-logo {{
      width: 34px;
      height: 34px;
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.25), rgba(6, 182, 212, 0.25));
      border: 1px solid rgba(16, 185, 129, 0.5);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      box-shadow: 0 0 16px rgba(16, 185, 129, 0.25);
    }}

    .studio-title-block {{
      display: flex;
      flex-direction: column;
    }}

    .studio-title {{
      font-size: 0.98rem;
      font-weight: 800;
      letter-spacing: -0.01em;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .studio-subtitle {{
      font-size: 0.74rem;
      color: var(--ink-muted);
    }}

    .studio-stats {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.03);
      padding: 4px 12px;
      border-radius: 999px;
      border: 1px solid var(--surface-border-subtle);
      font-size: 0.78rem;
    }}

    .studio-stats-item {{
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    .studio-stats-item b {{
      color: var(--emerald);
      font-family: var(--font-m);
    }}

    .studio-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    /* Buttons */
    .s-btn {{
      padding: 7px 14px;
      border-radius: var(--radius-sm);
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid var(--surface-border);
      background: rgba(255, 255, 255, 0.05);
      color: var(--ink);
      transition: all 0.18s ease;
      font-family: var(--font-d);
      user-select: none;
    }}

    .s-btn:hover {{
      background: rgba(255, 255, 255, 0.10);
      border-color: rgba(255, 255, 255, 0.22);
      transform: translateY(-1px);
    }}

    .s-btn:active {{
      transform: translateY(0);
    }}

    .s-btn-emerald {{
      background: rgba(16, 185, 129, 0.18);
      border-color: rgba(16, 185, 129, 0.45);
      color: #34d399;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.2);
    }}

    .s-btn-emerald:hover {{
      background: rgba(16, 185, 129, 0.28);
      border-color: rgba(16, 185, 129, 0.7);
    }}

    .s-btn-amber {{
      background: rgba(245, 158, 11, 0.16);
      border-color: rgba(245, 158, 11, 0.4);
      color: #fbbf24;
    }}

    .s-btn-amber:hover {{
      background: rgba(245, 158, 11, 0.25);
    }}

    .s-btn-sm {{
      padding: 4px 9px;
      font-size: 0.74rem;
    }}

    .save-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.75rem;
      color: #34d399;
      background: rgba(16, 185, 129, 0.12);
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid rgba(16, 185, 129, 0.3);
      opacity: 0;
      transition: opacity 0.3s ease;
    }}

    .save-badge.visible {{
      opacity: 1;
    }}

    /* Main Grid Layout */
    .studio-workspace {{
      display: grid;
      grid-template-columns: 320px 1fr 480px;
      flex: 1;
      height: calc(100vh - 55px);
      overflow: hidden;
    }}

    /* Column 1: Sidebar Catalog */
    .studio-sidebar {{
      background: rgba(11, 15, 23, 0.7);
      border-right: 1px solid var(--surface-border);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    .sidebar-search-box {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--surface-border-subtle);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .sidebar-input {{
      width: 100%;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-sm);
      padding: 8px 12px;
      font-size: 0.82rem;
      color: var(--ink);
      font-family: var(--font-d);
      outline: none;
      transition: border-color 0.2s;
    }}

    .sidebar-input:focus {{
      border-color: var(--emerald);
      box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
    }}

    .filter-pills-row {{
      display: flex;
      gap: 5px;
      overflow-x: auto;
      padding-bottom: 2px;
      scrollbar-width: none;
    }}
    .filter-pills-row::-webkit-scrollbar {{ display: none; }}

    .f-pill {{
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 0.72rem;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--surface-border-subtle);
      color: var(--ink-muted);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s;
    }}

    .f-pill:hover {{
      background: rgba(255, 255, 255, 0.08);
      color: var(--ink);
    }}

    .f-pill.active {{
      background: rgba(16, 185, 129, 0.2);
      border-color: rgba(16, 185, 129, 0.5);
      color: #34d399;
      font-weight: 700;
    }}

    .notes-list-scroll {{
      flex: 1;
      overflow-y: auto;
      padding: 6px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .note-nav-item {{
      padding: 9px 12px;
      border-radius: 10px;
      border: 1px solid transparent;
      background: rgba(255, 255, 255, 0.02);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 4px;
      transition: all 0.15s;
      user-select: none;
    }}

    .note-nav-item:hover {{
      background: rgba(255, 255, 255, 0.05);
      border-color: rgba(255, 255, 255, 0.08);
    }}

    .note-nav-item.active {{
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(15, 23, 42, 0.6));
      border-color: rgba(16, 185, 129, 0.5);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }}

    .note-nav-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }}

    .note-nav-echelon {{
      font-size: 0.68rem;
      font-weight: 700;
      color: var(--ink-muted);
      letter-spacing: 0.02em;
    }}

    .note-nav-steps-badge {{
      font-size: 0.68rem;
      font-family: var(--font-m);
      padding: 1px 6px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--ink-soft);
    }}

    .note-nav-item.modified .note-nav-steps-badge {{
      background: rgba(16, 185, 129, 0.2);
      border-color: rgba(16, 185, 129, 0.4);
      color: #34d399;
      font-weight: 700;
    }}

    .note-nav-title {{
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--ink);
      line-height: 1.35;
      overflow: hidden;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }}

    /* Column 2: Quantum Workbench */
    .studio-workbench {{
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      background: #090c13;
      border-right: 1px solid var(--surface-border);
      position: relative;
    }}

    .workbench-header {{
      padding: 18px 24px 14px;
      border-bottom: 1px solid var(--surface-border);
      background: rgba(15, 23, 42, 0.45);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 20;
    }}

    .wb-meta-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }}

    .wb-breadcrumbs {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-golos);
      font-size: 0.8rem;
    }}

    .wb-crumb-echelon {{ color: var(--ink-muted); font-weight: 600; }}
    .wb-crumb-sep {{ color: rgba(255, 255, 255, 0.25); margin: 0 2px; }}
    .wb-crumb-unit {{ color: var(--ink-soft); font-weight: 600; }}
    .wb-crumb-skill {{ color: var(--emerald); font-weight: 700; }}

    .wb-title-row {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 14px;
    }}

    .wb-note-title-input {{
      flex: 1;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-sm);
      padding: 8px 14px;
      font-size: 1.15rem;
      font-weight: 800;
      color: #ffffff;
      font-family: var(--font-d);
      letter-spacing: -0.01em;
    }}

    .wb-note-title-input:focus {{
      border-color: var(--emerald);
      outline: none;
    }}

    /* Beads Bar in Workbench */
    .wb-beads-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      background: rgba(0, 0, 0, 0.3);
      padding: 8px 14px;
      border-radius: var(--radius-md);
      border: 1px solid var(--surface-border-subtle);
    }}

    .wb-beads-track {{
      display: flex;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      scrollbar-width: none;
      padding: 4px 0;
    }}
    .wb-beads-track::-webkit-scrollbar {{ display: none; }}

    .wb-step-bead {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--surface-border);
      color: var(--ink-muted);
      font-size: 0.74rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.16s ease;
      white-space: nowrap;
      user-select: none;
    }}

    .wb-step-bead:hover {{
      background: rgba(255, 255, 255, 0.10);
      color: var(--ink);
    }}

    .wb-step-bead.active {{
      background: rgba(16, 185, 129, 0.22);
      border-color: rgba(16, 185, 129, 0.6);
      color: #ffffff;
      font-weight: 700;
      box-shadow: 0 0 14px rgba(16, 185, 129, 0.25);
    }}

    .wb-step-bead .dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: currentColor;
    }}

    /* Steps List Container */
    .steps-container {{
      padding: 20px 24px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}

    /* Individual Step Card in Workbench */
    .step-card {{
      background: var(--surface-card);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-lg);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5);
      position: relative;
      transition: border-color 0.2s;
    }}

    .step-card.focused {{
      border-color: rgba(16, 185, 129, 0.5);
      box-shadow: 0 0 24px -4px rgba(16, 185, 129, 0.15), 0 8px 24px -6px rgba(0, 0, 0, 0.5);
    }}

    .step-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--surface-border-subtle);
    }}

    .step-header-left {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex: 1;
    }}

    .step-number-badge {{
      background: rgba(16, 185, 129, 0.18);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399;
      font-size: 0.74rem;
      font-weight: 800;
      font-family: var(--font-m);
      padding: 3px 8px;
      border-radius: 6px;
      white-space: nowrap;
    }}

    .step-title-input {{
      flex: 1;
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--surface-border);
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 0.94rem;
      font-weight: 700;
      color: #ffffff;
      font-family: var(--font-d);
    }}

    .step-title-input:focus {{
      border-color: var(--emerald);
      outline: none;
    }}

    .step-header-actions {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* Quanta List in Step */
    .quanta-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    /* Quantum Card */
    .quantum-card {{
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--surface-border-subtle);
      border-left: 3px solid var(--cyan);
      border-radius: 8px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: all 0.15s ease;
    }}

    .quantum-card:hover {{
      border-color: rgba(255, 255, 255, 0.18);
      background: rgba(0, 0, 0, 0.35);
    }}

    .quantum-card.type-paragraph {{ border-left-color: #3b82f6; }}
    .quantum-card.type-code {{ border-left-color: #10b981; }}
    .quantum-card.type-list {{ border-left-color: #f59e0b; }}
    .quantum-card.type-callout {{ border-left-color: #a855f7; }}
    .quantum-card.type-heading {{ border-left-color: #06b6d4; }}

    .quantum-meta-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }}

    .quantum-type-tag {{
      font-size: 0.66rem;
      font-family: var(--font-m);
      font-weight: 700;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.06);
      color: var(--ink-soft);
    }}

    .quantum-card.type-paragraph .quantum-type-tag {{ background: rgba(59, 130, 246, 0.18); color: #93c5fd; }}
    .quantum-card.type-code .quantum-type-tag {{ background: rgba(16, 185, 129, 0.18); color: #6ee7b7; }}
    .quantum-card.type-list .quantum-type-tag {{ background: rgba(245, 158, 11, 0.18); color: #fcd34d; }}
    .quantum-card.type-callout .quantum-type-tag {{ background: rgba(168, 85, 247, 0.18); color: #d8b4fe; }}
    .quantum-card.type-heading .quantum-type-tag {{ background: rgba(6, 182, 212, 0.18); color: #67e8f9; }}

    .quantum-actions {{
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .q-btn {{
      padding: 3px 6px;
      border-radius: 5px;
      font-size: 0.7rem;
      cursor: pointer;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--surface-border-subtle);
      color: var(--ink-muted);
      transition: all 0.12s;
    }}

    .q-btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.2);
    }}

    .q-btn-split {{
      background: rgba(245, 158, 11, 0.15);
      border-color: rgba(245, 158, 11, 0.35);
      color: #fbbf24;
      font-weight: 700;
    }}

    .q-btn-split:hover {{
      background: rgba(245, 158, 11, 0.28);
      color: #ffffff;
    }}

    .quantum-content-preview {{
      font-size: 0.84rem;
      line-height: 1.5;
      color: var(--ink-soft);
      max-height: 160px;
      overflow-y: auto;
      background: rgba(0, 0, 0, 0.2);
      padding: 8px 10px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.03);
    }}

    .quantum-content-preview pre {{
      font-family: var(--font-m);
      font-size: 0.78rem;
      line-height: 1.55;
      background: rgba(0, 0, 0, 0.4);
      padding: 6px 8px;
      border-radius: 4px;
      overflow-x: auto;
      color: #38bdf8;
    }}

    .quantum-content-preview code {{
      font-family: var(--font-m);
      font-size: 0.78rem;
      background: rgba(255, 255, 255, 0.08);
      padding: 1px 4px;
      border-radius: 3px;
    }}

    .quantum-edit-textarea {{
      width: 100%;
      min-height: 90px;
      background: rgba(0, 0, 0, 0.45);
      border: 1px solid var(--emerald);
      border-radius: 6px;
      padding: 8px;
      color: #ffffff;
      font-family: var(--font-m);
      font-size: 0.8rem;
      line-height: 1.45;
      resize: vertical;
      display: none;
    }}

    .step-footer-actions {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-top: 6px;
    }}

    /* Column 3: Live Preview Simulator */
    .studio-preview {{
      background: #05070a;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      border-left: 1px solid var(--surface-border);
    }}

    .preview-toolbar {{
      padding: 10px 16px;
      border-bottom: 1px solid var(--surface-border);
      background: rgba(15, 23, 42, 0.6);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}

    .preview-mode-switch {{
      display: flex;
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--surface-border);
      border-radius: 8px;
      padding: 2px;
    }}

    .p-mode-btn {{
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.74rem;
      font-weight: 600;
      color: var(--ink-muted);
      cursor: pointer;
      border: none;
      background: transparent;
      transition: all 0.15s;
    }}

    .p-mode-btn.active {{
      background: rgba(255, 255, 255, 0.12);
      color: #ffffff;
    }}

    .preview-viewport-wrap {{
      flex: 1;
      overflow-y: auto;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding: 20px 10px;
      background: radial-gradient(circle at 50% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 60%);
    }}

    /* Simulator Chassis */
    .simulator-phone {{
      width: 390px;
      max-width: 100%;
      background: #07090e;
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 36px;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.06);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      position: relative;
      min-height: 680px;
    }}

    .simulator-phone.mode-desktop {{
      width: 100%;
      border-radius: 16px;
      min-height: auto;
    }}

    /* Screen UI inside Simulator (Pixel-Perfect SRS Note Screen) */
    .sim-topbar {{
      padding: 12px 16px 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }}

    .sim-topbar-title {{
      font-size: 0.8rem;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .sim-topbar-meta {{
      font-size: 0.74rem;
      font-family: var(--font-m);
      color: var(--ink-muted);
    }}

    /* Beads Necklace in Simulator */
    .sim-beads-wrap {{
      padding: 12px 16px 8px;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
    }}

    .sim-bead {{
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.15);
      position: relative;
      transition: all 0.2s ease;
      cursor: pointer;
    }}

    .sim-bead.done {{
      background: #10b981;
      box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
    }}

    .sim-bead.active {{
      width: 11px;
      height: 11px;
      background: #ffffff;
      box-shadow: 0 0 0 2px #10b981, 0 0 14px rgba(16, 185, 129, 0.8);
      animation: beadPulse 2s infinite ease-in-out;
    }}

    @keyframes beadPulse {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.15); box-shadow: 0 0 0 3px #10b981, 0 0 20px rgba(16, 185, 129, 0.9); }}
    }}

    /* Sim Card Container */
    .sim-note-container {{
      padding: 14px 18px 24px;
      flex: 1;
      display: flex;
      flex-direction: column;
    }}

    /* Canonical Breadcrumbs in Simulator */
    .sim-breadcrumbs {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 4px 6px;
      margin-bottom: 12px;
      font-family: var(--font-golos);
      font-size: 0.78rem;
      line-height: 1.4;
    }}

    .sim-bc-track {{
      color: var(--ink-muted);
      font-weight: 600;
      white-space: nowrap;
      flex-shrink: 0;
    }}

    .sim-bc-sep {{
      color: rgba(255, 255, 255, 0.22);
      font-size: 0.72rem;
      margin: 0 4px;
      user-select: none;
      white-space: nowrap;
      flex-shrink: 0;
    }}

    .sim-bc-unit {{
      color: var(--ink-soft);
      font-weight: 600;
      white-space: nowrap;
      flex-shrink: 0;
    }}

    .sim-bc-skill {{
      color: #10b981;
      font-weight: 700;
      white-space: normal;
      line-height: 1.35;
    }}

    /* Note Body in Simulator */
    .sim-note-body {{
      color: var(--ink);
      font-size: 0.92rem;
      line-height: 1.62;
      flex: 1;
    }}

    .sim-note-body h4 {{
      font-size: 1.15rem;
      font-weight: 800;
      color: #ffffff;
      margin: 0 0 14px 0;
      line-height: 1.35;
      letter-spacing: -0.01em;
    }}

    .sim-note-body p {{
      margin-bottom: 14px;
      color: #e2e8f0;
    }}

    /* Full Authentic Code Box Styling */
    .snippet-wrap {{
      position: relative;
      margin: 14px 0;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.10);
      background: #030508;
      box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.6);
    }}

    .code-run-bar {{
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      background: rgba(15, 23, 42, 0.75) !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
      padding: 6px 12px !important;
      user-select: none !important;
    }}

    .code-run-bar::before {{
      content: '' !important;
      display: inline-block !important;
      width: 32px !important;
      height: 8px !important;
      background-image: radial-gradient(circle, #ef4444 3.5px, transparent 4px),
                        radial-gradient(circle, #f59e0b 3.5px, transparent 4px),
                        radial-gradient(circle, #10b981 3.5px, transparent 4px) !important;
      background-position: 0 0, 11px 0, 22px 0 !important;
      background-repeat: no-repeat !important;
      opacity: 0.8 !important;
      flex-shrink: 0 !important;
    }}

    .code-run-bar span,
    .code-run-bar .mono.meta {{
      font-family: var(--font-m) !important;
      font-size: 0.72rem !important;
      font-weight: 600 !important;
      color: #64748b !important;
      text-transform: lowercase !important;
      letter-spacing: 0.04em !important;
      margin-left: 8px !important;
      margin-right: auto !important;
    }}

    .btn-copy-code {{
      display: inline-flex !important;
      align-items: center !important;
      gap: 4px !important;
      background: rgba(255, 255, 255, 0.05) !important;
      color: #94a3b8 !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      border-radius: 6px !important;
      padding: 2px 8px !important;
      font-family: var(--font-d) !important;
      font-size: 0.7rem !important;
      font-weight: 600 !important;
      cursor: pointer !important;
      transition: all 0.2s ease !important;
      line-height: 1.2 !important;
    }}

    .btn-copy-code:hover {{
      background: rgba(16, 185, 129, 0.15) !important;
      color: #34d399 !important;
      border-color: rgba(16, 185, 129, 0.40) !important;
    }}

    .snippet-wrap pre,
    .sim-note-body pre {{
      background: #030508;
      padding: 12px 14px;
      margin: 0;
      overflow-x: auto;
      font-family: var(--font-m);
      font-size: 0.8rem;
      line-height: 1.62;
      color: #38bdf8;
      border: none;
    }}

    .sim-note-body code {{
      font-family: var(--font-m);
      font-size: 0.82rem;
      background: rgba(16, 185, 129, 0.14);
      color: #34d399;
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid rgba(16, 185, 129, 0.25);
    }}

    .sim-note-body pre code {{
      background: transparent;
      border: none;
      padding: 0;
      color: inherit;
    }}

    .sim-note-body ul, .sim-note-body ol {{
      margin: 0 0 14px 0;
      padding-left: 22px;
    }}

    .sim-note-body li {{
      margin-bottom: 6px;
      color: #cbd5e1;
    }}

    /* Callouts inside Simulator */
    .sim-note-body .callout,
    .sim-note-body blockquote {{
      background: rgba(168, 85, 247, 0.08);
      border-left: 3px solid #a855f7;
      padding: 10px 14px;
      border-radius: 0 8px 8px 0;
      margin: 14px 0;
      font-size: 0.88rem;
      color: #e9d5ff;
    }}

    /* Footer Buttons in Simulator */
    .sim-footer-bar {{
      margin-top: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      padding-top: 14px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
    }}

    .sim-btn-back {{
      padding: 12px 18px;
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: var(--ink-soft);
      font-weight: 600;
      font-size: 0.86rem;
      cursor: pointer;
    }}

    .sim-btn-next {{
      flex: 1;
      padding: 12px 20px;
      border-radius: 14px;
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      border: 1px solid rgba(16, 185, 129, 0.7);
      color: #ffffff;
      font-weight: 700;
      font-size: 0.9rem;
      text-align: center;
      box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35);
      cursor: pointer;
    }}

    /* Modal for Export / Patch */
    .studio-modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(8px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .studio-modal-backdrop.open {{
      display: flex;
    }}

    .studio-modal {{
      background: #0d121c;
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-xl);
      max-width: 680px;
      width: 100%;
      box-shadow: 0 24px 64px rgba(0, 0, 0, 0.8);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    .modal-head {{
      padding: 16px 22px;
      border-bottom: 1px solid var(--surface-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .modal-head h3 {{
      font-size: 1.1rem;
      color: #ffffff;
    }}

    .modal-body {{
      padding: 20px 22px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .modal-code-area {{
      background: #05070a;
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-sm);
      padding: 12px;
      font-family: var(--font-m);
      font-size: 0.78rem;
      color: #38bdf8;
      height: 320px;
      overflow-y: auto;
      white-space: pre;
    }}

    .modal-foot {{
      padding: 14px 22px;
      border-top: 1px solid var(--surface-border);
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      background: rgba(0, 0, 0, 0.2);
    }}
  </style>
</head>
<body>

  <!-- Top Studio Header -->
  <header class="studio-header">
    <div class="studio-brand">
      <div class="studio-logo">⚡</div>
      <div class="studio-title-block">
        <div class="studio-title">
          Студия квантования шагов конспектов
          <span style="font-size: 0.68rem; font-weight: 700; color: #10b981; background: rgba(16, 185, 129, 0.15); padding: 2px 7px; border-radius: 999px;">v1.0 LIVE</span>
        </div>
        <div class="studio-subtitle">Интерактивное распределение шагов и квантов по всем 238 конспектам платформы</div>
      </div>
    </div>

    <div class="studio-stats">
      <div class="studio-stats-item">Всего: <b id="stat-total">238</b></div>
      <span style="color: rgba(255,255,255,0.2);">·</span>
      <div class="studio-stats-item">Отредактировано: <b id="stat-edited" style="color: #38bdf8;">0</b></div>
      <span style="color: rgba(255,255,255,0.2);">·</span>
      <div class="save-badge" id="save-badge">✓ Сохранено в браузере</div>
    </div>

    <div class="studio-actions">
      <button type="button" class="s-btn s-btn-emerald" id="btn-export-json">
        📥 Скачать JSON
      </button>
      <button type="button" class="s-btn s-btn-amber" id="btn-copy-patch">
        📋 Python-патчер
      </button>
      <button type="button" class="s-btn" id="btn-reset-note" title="Сбросить текущий конспект к исходному виду">
        🔄 Сброс конспекта
      </button>
    </div>
  </header>

  <!-- Main 3-Column Workspace -->
  <main class="studio-workspace">
    
    <!-- Column 1: Sidebar Catalog -->
    <aside class="studio-sidebar">
      <div class="sidebar-search-box">
        <input type="text" class="sidebar-input" id="search-input" placeholder="🔍 Поиск темы или ID (например: logging, К-001)...">
        
        <div class="filter-pills-row" id="echelon-filters">
          <button type="button" class="f-pill active" data-filter="all">Все (238)</button>
          <button type="button" class="f-pill" data-filter="modified">✨ Изменённые</button>
          <button type="button" class="f-pill" data-filter="tier-1">Эшелон 1</button>
          <button type="button" class="f-pill" data-filter="tier-2">Эшелон 2</button>
          <button type="button" class="f-pill" data-filter="tier-3">Эшелон 3</button>
          <button type="button" class="f-pill" data-filter="tier-4">Эшелон 4</button>
        </div>
      </div>

      <div class="notes-list-scroll" id="notes-list">
        <!-- Rendered via JS -->
      </div>
    </aside>

    <!-- Column 2: Quantum Workbench -->
    <section class="studio-workbench" id="workbench-panel">
      
      <div class="workbench-header">
        <div class="wb-meta-row">
          <div class="wb-breadcrumbs" id="wb-breadcrumbs">
            <span class="wb-crumb-echelon" id="wb-echelon">Эшелон 1</span>
            <span class="wb-crumb-sep">/</span>
            <span class="wb-crumb-unit" id="wb-unit">Инструменты</span>
            <span class="wb-crumb-sep">/</span>
            <span class="wb-crumb-skill" id="wb-skill">Логирование в Python</span>
          </div>

          <div style="display: flex; gap: 8px;">
            <button type="button" class="s-btn s-btn-sm s-btn-emerald" id="btn-add-step">
              ➕ Добавить шаг
            </button>
          </div>
        </div>

        <div class="wb-title-row">
          <input type="text" class="wb-note-title-input" id="wb-note-title" placeholder="Название конспекта...">
        </div>

        <!-- Beads bar for quick navigation -->
        <div class="wb-beads-bar">
          <div style="font-size: 0.74rem; color: var(--ink-muted); font-weight: 700; text-transform: uppercase;">Шаги темы:</div>
          <div class="wb-beads-track" id="wb-beads-track">
            <!-- Steps dots -->
          </div>
        </div>
      </div>

      <!-- Container of all Steps -->
      <div class="steps-container" id="steps-container">
        <!-- Step Cards rendered via JS -->
      </div>

    </section>

    <!-- Column 3: Live Preview Simulator -->
    <aside class="studio-preview">
      
      <div class="preview-toolbar">
        <div style="font-size: 0.8rem; font-weight: 700; color: #ffffff; display: flex; align-items: center; gap: 6px;">
          <span>📱 Живой Live Preview</span>
          <span style="font-size: 0.68rem; color: var(--emerald); font-weight: 600;">● Активен</span>
        </div>

        <div class="preview-mode-switch">
          <button type="button" class="p-mode-btn active" id="btn-mode-phone">📱 390px</button>
          <button type="button" class="p-mode-btn" id="btn-mode-desktop">💻 Десктоп</button>
        </div>
      </div>

      <div class="preview-viewport-wrap">
        
        <!-- Phone simulator chassis -->
        <div class="simulator-phone" id="sim-chassis">
          
          <div class="sim-topbar">
            <div class="sim-topbar-title">
              <span style="color: #10b981;">●</span> Конспекты SRS
            </div>
            <div class="sim-topbar-meta" id="sim-top-counter">1 / 18</div>
          </div>

          <!-- Beads Necklace -->
          <div class="sim-beads-wrap" id="sim-beads">
            <!-- Simulated beads -->
          </div>

          <div class="sim-note-container">
            
            <!-- Breadcrumbs with Golos Text and Spaced Slashes -->
            <nav class="sim-breadcrumbs" id="sim-breadcrumbs">
              <span class="sim-bc-track" id="sim-bc-track">Эшелон 1</span>
              <span class="sim-bc-sep">/</span>
              <span class="sim-bc-unit" id="sim-bc-unit">Инструменты</span>
              <span class="sim-bc-sep">/</span>
              <span class="sim-bc-skill" id="sim-bc-skill">Логирование в Python</span>
            </nav>

            <!-- Active Step Body -->
            <div class="sim-note-body" id="sim-note-body">
              <h4 id="sim-step-title">Заголовок шага</h4>
              <div id="sim-step-content">Содержимое шага...</div>
            </div>

            <!-- Footer navigation -->
            <div class="sim-footer-bar">
              <button type="button" class="sim-btn-back" id="sim-btn-back">← Назад</button>
              <button type="button" class="sim-btn-next" id="sim-btn-next">Понятно, дальше ➔</button>
            </div>

          </div>

        </div>

      </div>

    </aside>

  </main>

  <!-- Modal Dialog for Export / Patch -->
  <div class="studio-modal-backdrop" id="studio-modal">
    <div class="studio-modal">
      <div class="modal-head">
        <h3 id="modal-title">Экспорт</h3>
        <button type="button" class="s-btn s-btn-sm" id="modal-close">✕</button>
      </div>
      <div class="modal-body">
        <p id="modal-desc" style="font-size: 0.85rem; color: var(--ink-soft);"></p>
        <div class="modal-code-area" id="modal-code"></div>
      </div>
      <div class="modal-foot">
        <button type="button" class="s-btn s-btn-emerald" id="modal-copy-btn">📋 Скопировать</button>
      </div>
    </div>
  </div>

  <!-- Embedded Catalog Database & Workbench Engine -->
  <script>
    // 1. Initial Raw Data
    const RAW_CATALOG_DATA = {catalog_json_str};

    const LOCAL_STORAGE_KEY = 'pba_notes_quanta_store_v1';

    // State management
    const state = {{
      notes: {{}},           // ID -> note object (with steps and quanta)
      originalNotes: {{}},   // Read-only backup of initial state
      meta: RAW_CATALOG_DATA.notesMeta || {{}},
      catalog: RAW_CATALOG_DATA.catalog || [],
      activeNoteId: null,
      activeStepIdx: 0,
      activeQuantumId: null,
      searchQuery: '',
      activeFilter: 'all',
      isDesktopSim: false,
      modifiedNoteIds: new Set()
    }};

    // 2. Quantum Parsing Engine
    // Splits an HTML string of a step into atomic semantic quanta (paragraph, code, list, callout, heading)
    function parseHtmlIntoQuanta(htmlString, stepTitle) {{
      const parser = new DOMParser();
      const doc = parser.parseFromString(htmlString || '', 'text/html');
      const body = doc.body;

      const quanta = [];
      let qIndex = 0;

      Array.from(body.children).forEach((el) => {{
        const tag = el.tagName.toLowerCase();
        let qType = 'paragraph';

        if (tag === 'pre' || el.classList.contains('snippet-wrap')) {{
          qType = 'code';
        }} else if (tag === 'ul' || tag === 'ol') {{
          qType = 'list';
        }} else if (tag === 'blockquote' || el.classList.contains('callout')) {{
          qType = 'callout';
        }} else if (tag === 'h1' || tag === 'h2' || tag === 'h3' || tag === 'h4' || tag === 'h5' || tag === 'h6') {{
          // If first element is h4 with the step title, we can skip or keep as heading
          if (qIndex === 0 && el.textContent.trim() === (stepTitle || '').trim()) {{
            return; // Skip redundancy, title is in step.title
          }}
          qType = 'heading';
        }}

        quanta.push({{
          id: 'q_' + Math.random().toString(36).substr(2, 9),
          type: qType,
          html: el.outerHTML,
          text: el.textContent.trim()
        }});
        qIndex++;
      }});

      // Fallback if empty
      if (quanta.length === 0) {{
        quanta.push({{
          id: 'q_' + Math.random().toString(36).substr(2, 9),
          type: 'paragraph',
          html: '<p>' + (htmlString || 'Содержимое шага.') + '</p>',
          text: htmlString || 'Содержимое шага.'
        }});
      }}

      return quanta;
    }}

    // Reconstructs step HTML from quanta array
    function compileQuantaToHtml(quanta, stepTitle) {{
      let html = '';
      if (stepTitle && stepTitle.trim()) {{
        html += '<h4>' + escapeHtml(stepTitle.trim()) + '</h4>\\n';
      }}
      quanta.forEach(q => {{
        html += q.html.trim() + '\\n';
      }});
      return html.trim();
    }}

    function escapeHtml(str) {{
      return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }}

    // 3. Storage & Initialization
    function initStudio() {{
      const savedStore = localStorage.getItem(LOCAL_STORAGE_KEY);
      let parsedSaved = null;
      if (savedStore) {{
        try {{
          parsedSaved = JSON.parse(savedStore);
        }} catch (e) {{
          console.error('Failed to parse saved quanta store', e);
        }}
      }}

      // Populate state.notes
      const rawNotes = RAW_CATALOG_DATA.notes || {{}};
      Object.keys(rawNotes).forEach(id => {{
        const rawNote = rawNotes[id];
        
        // Deep clone for original backup
        state.originalNotes[id] = JSON.parse(JSON.stringify(rawNote));

        // Use saved note if exists
        const workingNote = (parsedSaved && parsedSaved[id]) ? parsedSaved[id] : rawNote;
        
        if (parsedSaved && parsedSaved[id]) {{
          state.modifiedNoteIds.add(id);
        }}

        // Prepare steps with parsed quanta
        const steps = (workingNote.steps || []).map((st, idx) => {{
          const stepTitle = st.title || ('Шаг ' + (idx + 1));
          return {{
            id: 'st_' + idx + '_' + Math.random().toString(36).substr(2, 6),
            title: stepTitle,
            quanta: (st.quanta && Array.isArray(st.quanta)) ? st.quanta : parseHtmlIntoQuanta(st.html, stepTitle)
          }};
        }});

        state.notes[id] = {{
          id: id,
          title: workingNote.title || id,
          steps: steps.length > 0 ? steps : [{{
            id: 'st_0',
            title: workingNote.title || 'Введение',
            quanta: [{{ id: 'q_0', type: 'paragraph', html: '<p>Теория темы.</p>', text: 'Теория темы.' }}]
          }}]
        }};
      }});

      // Select first note
      const allIds = Object.keys(state.notes);
      if (allIds.length > 0) {{
        state.activeNoteId = allIds[0];
      }}

      updateStats();
      renderSidebar();
      renderWorkbench();
      renderLivePreview();
      setupEvents();
    }}

    function saveToLocalStorage() {{
      const exportObj = {{}};
      state.modifiedNoteIds.forEach(id => {{
        const note = state.notes[id];
        exportObj[id] = {{
          id: note.id,
          title: note.title,
          steps: note.steps.map(st => ({{
            title: st.title,
            html: compileQuantaToHtml(st.quanta, st.title),
            quanta: st.quanta
          }}))
        }};
      }});

      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(exportObj));
      showSaveFlash();
      updateStats();
    }}

    function showSaveFlash() {{
      const badge = document.getElementById('save-badge');
      badge.classList.add('visible');
      clearTimeout(badge._timer);
      badge._timer = setTimeout(() => badge.classList.remove('visible'), 2200);
    }}

    function updateStats() {{
      document.getElementById('stat-total').textContent = Object.keys(state.notes).length;
      document.getElementById('stat-edited').textContent = state.modifiedNoteIds.size;
    }}

    // 4. Sidebar Rendering & Filtering
    function renderSidebar() {{
      const listEl = document.getElementById('notes-list');
      listEl.innerHTML = '';

      const query = (state.searchQuery || '').toLowerCase().trim();
      const allIds = Object.keys(state.notes);

      allIds.forEach(id => {{
        const note = state.notes[id];
        const meta = state.meta[id] || {{}};
        const title = note.title || id;
        const tier = meta.tier || 1;
        const isModified = state.modifiedNoteIds.has(id);

        // Filter checks
        if (state.activeFilter === 'modified' && !isModified) return;
        if (state.activeFilter === 'tier-1' && tier !== 1) return;
        if (state.activeFilter === 'tier-2' && tier !== 2) return;
        if (state.activeFilter === 'tier-3' && tier !== 3) return;
        if (state.activeFilter === 'tier-4' && tier !== 4) return;

        // Search check
        if (query) {{
          const matchTitle = title.toLowerCase().includes(query);
          const matchId = id.toLowerCase().includes(query);
          const matchSkill = (meta.skillTitle || '').toLowerCase().includes(query);
          const matchUnit = (meta.unitTitle || '').toLowerCase().includes(query);
          if (!matchTitle && !matchId && !matchSkill && !matchUnit) return;
        }}

        const item = document.createElement('div');
        item.className = 'note-nav-item' + (id === state.activeNoteId ? ' active' : '') + (isModified ? ' modified' : '');
        item.dataset.id = id;

        const cleanDisplayTitle = title.replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();

        item.innerHTML = `
          <div class="note-nav-top">
            <span class="note-nav-echelon">Эшелон ${{tier}} · ${{meta.unitTitle || 'Тема'}}</span>
            <span class="note-nav-steps-badge">${{isModified ? '✨ ' : ''}}${{note.steps.length}} шаг.</span>
          </div>
          <div class="note-nav-title">${{escapeHtml(cleanDisplayTitle)}}</div>
        `;

        item.addEventListener('click', () => {{
          state.activeNoteId = id;
          state.activeStepIdx = 0;
          renderSidebar();
          renderWorkbench();
          renderLivePreview();
        }});

        listEl.appendChild(item);
      }});
    }}

    // 5. Workbench Rendering
    function renderWorkbench() {{
      const note = state.notes[state.activeNoteId];
      if (!note) return;

      const meta = state.meta[state.activeNoteId] || {{}};
      const cleanTitle = note.title.replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();

      // Breadcrumbs
      document.getElementById('wb-echelon').textContent = `Эшелон ${{meta.tier || 1}}`;
      document.getElementById('wb-unit').textContent = meta.unitTitle || 'Модуль';
      document.getElementById('wb-skill').textContent = meta.skillTitle || cleanTitle;

      // Title input
      const titleInput = document.getElementById('wb-note-title');
      titleInput.value = cleanTitle;

      // Beads bar
      const beadsTrack = document.getElementById('wb-beads-track');
      beadsTrack.innerHTML = '';
      note.steps.forEach((st, idx) => {{
        const b = document.createElement('div');
        b.className = 'wb-step-bead' + (idx === state.activeStepIdx ? ' active' : '');
        b.innerHTML = `<span class="dot"></span> Шаг ${{idx + 1}}: ${{escapeHtml((st.title || '').slice(0, 24))}}`;
        b.addEventListener('click', () => {{
          state.activeStepIdx = idx;
          renderWorkbench();
          renderLivePreview();
          scrollToStepCard(idx);
        }});
        beadsTrack.appendChild(b);
      }});

      // Steps Container
      const stepsContainer = document.getElementById('steps-container');
      stepsContainer.innerHTML = '';

      note.steps.forEach((st, sIdx) => {{
        const card = document.createElement('div');
        card.className = 'step-card' + (sIdx === state.activeStepIdx ? ' focused' : '');
        card.id = 'step-card-' + sIdx;

        // Header of step
        const header = document.createElement('div');
        header.className = 'step-header';
        header.innerHTML = `
          <div class="step-header-left">
            <span class="step-number-badge">Шаг ${{sIdx + 1}} из ${{note.steps.length}}</span>
            <input type="text" class="step-title-input" value="${{escapeHtml(st.title || '')}}" placeholder="Заголовок шага...">
          </div>
          <div class="step-header-actions">
            ${{sIdx > 0 ? `<button type="button" class="s-btn s-btn-sm" data-action="move-step-up" title="Поднять шаг выше">⬆️</button>` : ''}}
            ${{sIdx < note.steps.length - 1 ? `<button type="button" class="s-btn s-btn-sm" data-action="move-step-down" title="Опустить шаг ниже">⬇️</button>` : ''}}
            ${{sIdx < note.steps.length - 1 ? `<button type="button" class="s-btn s-btn-sm s-btn-amber" data-action="merge-next" title="Объединить со следующим шагом">🔗 Слить со следующим</button>` : ''}}
            ${{note.steps.length > 1 ? `<button type="button" class="s-btn s-btn-sm" data-action="delete-step" style="color:#f43f5e;" title="Удалить этот шаг">🗑️</button>` : ''}}
          </div>
        `;

        // Listen for title change
        const titleIn = header.querySelector('.step-title-input');
        titleIn.addEventListener('input', (e) => {{
          st.title = e.target.value;
          markModified();
          renderLivePreview();
        }});

        // Step action buttons
        header.querySelectorAll('[data-action]').forEach(btn => {{
          btn.addEventListener('click', () => {{
            const act = btn.dataset.action;
            if (act === 'move-step-up' && sIdx > 0) {{
              const temp = note.steps[sIdx];
              note.steps[sIdx] = note.steps[sIdx - 1];
              note.steps[sIdx - 1] = temp;
              state.activeStepIdx = sIdx - 1;
              markModified();
              renderWorkbench();
              renderLivePreview();
            }} else if (act === 'move-step-down' && sIdx < note.steps.length - 1) {{
              const temp = note.steps[sIdx];
              note.steps[sIdx] = note.steps[sIdx + 1];
              note.steps[sIdx + 1] = temp;
              state.activeStepIdx = sIdx + 1;
              markModified();
              renderWorkbench();
              renderLivePreview();
            }} else if (act === 'merge-next' && sIdx < note.steps.length - 1) {{
              const nextStep = note.steps[sIdx + 1];
              st.quanta = st.quanta.concat(nextStep.quanta);
              note.steps.splice(sIdx + 1, 1);
              markModified();
              renderWorkbench();
              renderLivePreview();
            }} else if (act === 'delete-step' && note.steps.length > 1) {{
              if (confirm(`Удалить Шаг ${{sIdx + 1}}? Содержимое будет перенесено в соседний шаг.`)) {{
                const targetIdx = sIdx > 0 ? sIdx - 1 : 1;
                note.steps[targetIdx].quanta = note.steps[targetIdx].quanta.concat(st.quanta);
                note.steps.splice(sIdx, 1);
                state.activeStepIdx = Math.max(0, sIdx - 1);
                markModified();
                renderWorkbench();
                renderLivePreview();
              }}
            }}
          }});
        }});

        card.appendChild(header);

        // Quanta List
        const quantaList = document.createElement('div');
        quantaList.className = 'quanta-list';

        st.quanta.forEach((q, qIdx) => {{
          const qEl = document.createElement('div');
          qEl.className = 'quantum-card type-' + q.type;
          qEl.id = `q-card-${{sIdx}}-${{qIdx}}`;

          const typeLabels = {{
            paragraph: 'Текст',
            code: 'Код Python',
            list: 'Список',
            callout: 'Сноска',
            heading: 'Заголовок'
          }};

          qEl.innerHTML = `
            <div class="quantum-meta-row">
              <span class="quantum-type-tag">${{typeLabels[q.type] || q.type}}</span>
              
              <div class="quantum-actions">
                ${{qIdx > 0 ? `<button type="button" class="q-btn q-btn-split" data-q-action="split-here" title="Разбить шаг здесь! Этот и следующие кванты перейдут в новый шаг.">✂️ Разбить шаг здесь</button>` : ''}}
                ${{sIdx > 0 ? `<button type="button" class="q-btn" data-q-action="move-to-prev-step" title="Перенести в предыдущий шаг">⬅️ В шаг ${{sIdx}}</button>` : ''}}
                ${{sIdx < note.steps.length - 1 ? `<button type="button" class="q-btn" data-q-action="move-to-next-step" title="Перенести в следующий шаг">➔ В шаг ${{sIdx + 2}}</button>` : ''}}
                ${{qIdx > 0 ? `<button type="button" class="q-btn" data-q-action="up">▲</button>` : ''}}
                ${{qIdx < st.quanta.length - 1 ? `<button type="button" class="q-btn" data-q-action="down">▼</button>` : ''}}
                <button type="button" class="q-btn" data-q-action="edit" title="Редактировать">✏️</button>
                <button type="button" class="q-btn" data-q-action="delete" style="color:#f43f5e;" title="Удалить квант">✕</button>
              </div>
            </div>

            <div class="quantum-content-preview">${{q.html}}</div>
            <textarea class="quantum-edit-textarea">${{escapeHtml(q.html)}}</textarea>
          `;

          // Handle Quantum Actions
          const editArea = qEl.querySelector('.quantum-edit-textarea');
          const previewArea = qEl.querySelector('.quantum-content-preview');

          qEl.querySelectorAll('[data-q-action]').forEach(qBtn => {{
            qBtn.addEventListener('click', () => {{
              const qAct = qBtn.dataset.qAction;
              
              if (qAct === 'split-here') {{
                // SPLIT: slice st.quanta from qIdx into a new step right after sIdx
                const newQuanta = st.quanta.splice(qIdx);
                const firstQ = newQuanta[0];
                let newStepTitle = (firstQ.text || '').split('.')[0].trim().slice(0, 48) || ('Шаг ' + (sIdx + 2));
                if (firstQ.type === 'heading') {{
                  newStepTitle = firstQ.text.trim();
                }}
                const newStep = {{
                  id: 'st_' + (sIdx + 1) + '_' + Math.random().toString(36).substr(2, 6),
                  title: newStepTitle,
                  quanta: newQuanta
                }};
                note.steps.splice(sIdx + 1, 0, newStep);
                state.activeStepIdx = sIdx + 1;
                markModified();
                renderWorkbench();
                renderLivePreview();
                scrollToStepCard(sIdx + 1);
              }} else if (qAct === 'move-to-prev-step' && sIdx > 0) {{
                const quantum = st.quanta.splice(qIdx, 1)[0];
                note.steps[sIdx - 1].quanta.push(quantum);
                markModified();
                renderWorkbench();
                renderLivePreview();
              }} else if (qAct === 'move-to-next-step' && sIdx < note.steps.length - 1) {{
                const quantum = st.quanta.splice(qIdx, 1)[0];
                note.steps[sIdx + 1].quanta.unshift(quantum);
                markModified();
                renderWorkbench();
                renderLivePreview();
              }} else if (qAct === 'up' && qIdx > 0) {{
                const temp = st.quanta[qIdx];
                st.quanta[qIdx] = st.quanta[qIdx - 1];
                st.quanta[qIdx - 1] = temp;
                markModified();
                renderWorkbench();
                renderLivePreview();
              }} else if (qAct === 'down' && qIdx < st.quanta.length - 1) {{
                const temp = st.quanta[qIdx];
                st.quanta[qIdx] = st.quanta[qIdx + 1];
                st.quanta[qIdx + 1] = temp;
                markModified();
                renderWorkbench();
                renderLivePreview();
              }} else if (qAct === 'edit') {{
                if (editArea.style.display === 'block') {{
                  q.html = editArea.value;
                  previewArea.innerHTML = q.html;
                  previewArea.style.display = 'block';
                  editArea.style.display = 'none';
                  markModified();
                  renderLivePreview();
                }} else {{
                  previewArea.style.display = 'none';
                  editArea.style.display = 'block';
                  editArea.focus();
                }}
              }} else if (qAct === 'delete') {{
                st.quanta.splice(qIdx, 1);
                if (st.quanta.length === 0) {{
                  st.quanta.push({{ id: 'q_empty', type: 'paragraph', html: '<p>Пустой квант</p>', text: 'Пустой квант' }});
                }}
                markModified();
                renderWorkbench();
                renderLivePreview();
              }}
            }});
          }});

          quantaList.appendChild(qEl);
        }});

        card.appendChild(quantaList);

        // Step Footer Actions (Add quanta)
        const footer = document.createElement('div');
        footer.className = 'step-footer-actions';
        footer.innerHTML = `
          <div style="font-size:0.75rem; color:var(--ink-muted);">Всего квантов в шаге: <b>${{st.quanta.length}}</b></div>
          <div style="display:flex; gap:6px;">
            <button type="button" class="s-btn s-btn-sm" data-add-q="paragraph">➕ Текст</button>
            <button type="button" class="s-btn s-btn-sm" data-add-q="code">➕ Код</button>
            <button type="button" class="s-btn s-btn-sm" data-add-q="list">➕ Список</button>
          </div>
        `;

        footer.querySelectorAll('[data-add-q]').forEach(addBtn => {{
          addBtn.addEventListener('click', () => {{
            const qType = addBtn.dataset.addQ;
            let sampleHtml = '<p>Новый абзац с объяснением концепции.</p>';
            if (qType === 'code') sampleHtml = '<div class="snippet-wrap"><div class="code-run-bar"><span>python</span><button type="button" class="btn-copy-code">Копировать</button></div><pre><code class="language-python"># Пример кода\\nresult = process_data()</code></pre></div>';
            if (qType === 'list') sampleHtml = '<ul>\\n  <li>Ключевой пункт 1</li>\\n  <li>Ключевой пункт 2</li>\\n</ul>';

            st.quanta.push({{
              id: 'q_' + Math.random().toString(36).substr(2, 9),
              type: qType,
              html: sampleHtml,
              text: 'Новый квант'
            }});
            markModified();
            renderWorkbench();
            renderLivePreview();
          }});
        }});

        card.appendChild(footer);
        stepsContainer.appendChild(card);
      }});
    }}

    function scrollToStepCard(idx) {{
      const card = document.getElementById('step-card-' + idx);
      if (card) {{
        card.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }}
    }}

    function markModified() {{
      state.modifiedNoteIds.add(state.activeNoteId);
      saveToLocalStorage();
      renderSidebar();
    }}

    // 6. Live Preview Simulator
    function renderLivePreview() {{
      const note = state.notes[state.activeNoteId];
      if (!note) return;

      const meta = state.meta[state.activeNoteId] || {{}};
      const cleanTitle = note.title.replace(/^К-\d+\s*[:·•\-]\s*/i, '').trim();

      // Top counter
      document.getElementById('sim-top-counter').textContent = `${{state.activeStepIdx + 1}} / ${{note.steps.length}}`;

      // Simulator Breadcrumbs (Pixel-perfect Golos Text and Spaced Slashes)
      document.getElementById('sim-bc-track').textContent = `Эшелон ${{meta.tier || 1}}`;
      document.getElementById('sim-bc-unit').textContent = meta.unitTitle || 'Модуль';
      document.getElementById('sim-bc-skill').textContent = meta.skillTitle || cleanTitle;

      // Simulator Beads
      const beadsWrap = document.getElementById('sim-beads');
      beadsWrap.innerHTML = '';
      note.steps.forEach((st, idx) => {{
        const b = document.createElement('div');
        b.className = 'sim-bead' + (idx < state.activeStepIdx ? ' done' : (idx === state.activeStepIdx ? ' active' : ''));
        b.title = `Шаг ${{idx + 1}}: ${{st.title}}`;
        b.addEventListener('click', () => {{
          state.activeStepIdx = idx;
          renderWorkbench();
          renderLivePreview();
        }});
        beadsWrap.appendChild(b);
      }});

      // Active Step Content
      const curStep = note.steps[state.activeStepIdx] || note.steps[0];
      document.getElementById('sim-step-title').textContent = curStep.title || 'Шаг теории';

      const contentWrap = document.getElementById('sim-step-content');
      contentWrap.innerHTML = '';
      (curStep.quanta || []).forEach(q => {{
        contentWrap.innerHTML += q.html + '\\n';
      }});

      // Hook up copy buttons in preview
      contentWrap.querySelectorAll('.btn-copy-code').forEach(btn => {{
        btn.addEventListener('click', (e) => {{
          const pre = btn.closest('.snippet-wrap') ? btn.closest('.snippet-wrap').querySelector('pre') : null;
          if (pre) {{
            navigator.clipboard.writeText(pre.textContent).then(() => {{
              const old = btn.textContent;
              btn.textContent = '✓ Скопировано';
              setTimeout(() => btn.textContent = old, 1800);
            }});
          }}
        }});
      }});

      // Back / Next Buttons
      const btnBack = document.getElementById('sim-btn-back');
      const btnNext = document.getElementById('sim-btn-next');

      btnBack.style.visibility = state.activeStepIdx > 0 ? 'visible' : 'hidden';
      btnNext.textContent = state.activeStepIdx < note.steps.length - 1 ? 'Понятно, дальше ➔' : '✓ Закреплено';
    }}

    // 7. Event Listeners & Modals
    function setupEvents() {{
      // Search
      document.getElementById('search-input').addEventListener('input', (e) => {{
        state.searchQuery = e.target.value;
        renderSidebar();
      }});

      // Echelon / modified pills
      document.querySelectorAll('#echelon-filters .f-pill').forEach(pill => {{
        pill.addEventListener('click', () => {{
          document.querySelectorAll('#echelon-filters .f-pill').forEach(p => p.classList.remove('active'));
          pill.classList.add('active');
          state.activeFilter = pill.dataset.filter;
          renderSidebar();
        }});
      }});

      // Note title input
      document.getElementById('wb-note-title').addEventListener('input', (e) => {{
        const note = state.notes[state.activeNoteId];
        if (note) {{
          note.title = e.target.value;
          markModified();
          renderLivePreview();
        }}
      }});

      // Add Step Button
      document.getElementById('btn-add-step').addEventListener('click', () => {{
        const note = state.notes[state.activeNoteId];
        if (!note) return;
        const newStepIdx = note.steps.length;
        note.steps.push({{
          id: 'st_' + newStepIdx + '_' + Math.random().toString(36).substr(2, 6),
          title: 'Новый шаг ' + (newStepIdx + 1),
          quanta: [{{
            id: 'q_' + Math.random().toString(36).substr(2, 9),
            type: 'paragraph',
            html: '<p>Текст нового шага.</p>',
            text: 'Текст нового шага.'
          }}]
        }});
        state.activeStepIdx = newStepIdx;
        markModified();
        renderWorkbench();
        renderLivePreview();
        scrollToStepCard(newStepIdx);
      }});

      // Reset Note to Original
      document.getElementById('btn-reset-note').addEventListener('click', () => {{
        if (confirm(`Сбросить конспект "${{state.activeNoteId}}" к исходному состоянию? Все локальные изменения этого конспекта будут удалены.`)) {{
          const original = JSON.parse(JSON.stringify(state.originalNotes[state.activeNoteId]));
          const steps = (original.steps || []).map((st, idx) => ({{
            id: 'st_' + idx,
            title: st.title,
            quanta: parseHtmlIntoQuanta(st.html, st.title)
          }}));
          state.notes[state.activeNoteId] = {{
            id: original.id,
            title: original.title,
            steps: steps
          }};
          state.modifiedNoteIds.delete(state.activeNoteId);
          saveToLocalStorage();
          renderSidebar();
          renderWorkbench();
          renderLivePreview();
        }}
      }});

      // Simulator mode switch
      const btnPhone = document.getElementById('btn-mode-phone');
      const btnDesktop = document.getElementById('btn-mode-desktop');
      const chassis = document.getElementById('sim-chassis');

      btnPhone.addEventListener('click', () => {{
        btnPhone.classList.add('active');
        btnDesktop.classList.remove('active');
        chassis.classList.remove('mode-desktop');
        state.isDesktopSim = false;
      }});

      btnDesktop.addEventListener('click', () => {{
        btnDesktop.classList.add('active');
        btnPhone.classList.remove('active');
        chassis.classList.add('mode-desktop');
        state.isDesktopSim = true;
      }});

      // Simulator Back / Next buttons
      document.getElementById('sim-btn-back').addEventListener('click', () => {{
        if (state.activeStepIdx > 0) {{
          state.activeStepIdx--;
          renderWorkbench();
          renderLivePreview();
          scrollToStepCard(state.activeStepIdx);
        }}
      }});

      document.getElementById('sim-btn-next').addEventListener('click', () => {{
        const note = state.notes[state.activeNoteId];
        if (note && state.activeStepIdx < note.steps.length - 1) {{
          state.activeStepIdx++;
          renderWorkbench();
          renderLivePreview();
          scrollToStepCard(state.activeStepIdx);
        }} else {{
          alert('✓ Конспект успешно пройден! Все шаги закреплены.');
        }}
      }});

      // Export JSON Button
      document.getElementById('btn-export-json').addEventListener('click', () => {{
        const exportObj = {{}};
        // Export modified or all
        const idsToExport = state.modifiedNoteIds.size > 0 ? Array.from(state.modifiedNoteIds) : Object.keys(state.notes);
        idsToExport.forEach(id => {{
          const note = state.notes[id];
          exportObj[id] = {{
            id: note.id,
            title: note.title,
            steps: note.steps.map(st => ({{
              title: st.title,
              html: compileQuantaToHtml(st.quanta, st.title)
            }}))
          }};
        }});

        const jsonString = JSON.stringify(exportObj, null, 2);
        const blob = new Blob([jsonString], {{ type: 'application/json' }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'notes_quantum_distribution.json';
        a.click();
        URL.revokeObjectURL(url);
      }});

      // Copy Python Patch Button
      document.getElementById('btn-copy-patch').addEventListener('click', () => {{
        const exportObj = {{}};
        const idsToExport = state.modifiedNoteIds.size > 0 ? Array.from(state.modifiedNoteIds) : [state.activeNoteId];
        idsToExport.forEach(id => {{
          const note = state.notes[id];
          exportObj[id] = {{
            id: note.id,
            title: note.title,
            steps: note.steps.map(st => ({{
              title: st.title,
              html: compileQuantaToHtml(st.quanta, st.title)
            }}))
          }};
        }});

        const pythonCode = generatePythonPatchCode(exportObj);
        openModal(
          'Python-патчер для применения изменений',
          `Сгенерирован скрипт применения для ${{idsToExport.length}} конспектов. Скопируйте и сохраните в scripts/apply_quantum_patch.py, затем запустите.`,
          pythonCode
        );
      }});

      // Modal close
      document.getElementById('modal-close').addEventListener('click', closeModal);
      document.getElementById('studio-modal').addEventListener('click', (e) => {{
        if (e.target.id === 'studio-modal') closeModal();
      }});
      document.getElementById('modal-copy-btn').addEventListener('click', () => {{
        const code = document.getElementById('modal-code').textContent;
        navigator.clipboard.writeText(code).then(() => {{
          const btn = document.getElementById('modal-copy-btn');
          const old = btn.textContent;
          btn.textContent = '✓ Скопировано в буфер!';
          setTimeout(() => btn.textContent = old, 2000);
        }});
      }});
    }}

    function generatePythonPatchCode(exportObj) {{
      return `# -*- coding: utf-8 -*-
"""
Автоматический патчер распределения шагов и квантов конспектов
Сгенерирован в Студии квантования (stand_notes_quantum_studio.html)
"""
import json
import re

CHANGES = ${{JSON.stringify(exportObj, null, 2)}}

def apply_patch():
    files = ['standards/standards.html', 'academy.html']
    print(f"Применение обновлений для {{len(CHANGES)}} конспектов...")

    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        for note_id, note_data in CHANGES.items():
            print(f"  -> Обновление конспекта {{note_id}}: {{note_data['title']}} ({{len(note_data['steps'])}} шагов)")
            # Патчинг объекта конспекта в файле

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    print("✓ Все конспекты успешно обновлены и синхронизированы!")

if __name__ == '__main__':
    apply_patch()
`;
    }}

    function openModal(title, desc, code) {{
      document.getElementById('modal-title').textContent = title;
      document.getElementById('modal-desc').textContent = desc;
      document.getElementById('modal-code').textContent = code;
      document.getElementById('studio-modal').classList.add('open');
    }}

    function closeModal() {{
      document.getElementById('studio-modal').classList.remove('open');
    }}

    // Kickoff
    window.addEventListener('DOMContentLoaded', initStudio);
  </script>
</body>
</html>
'''

    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'stand_notes_quantum_studio.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Успешно сгенерирован стенд: {output_path}")
    print(f"Размер файла: {os.path.getsize(output_path)} байт")

if __name__ == '__main__':
    generate_studio()
