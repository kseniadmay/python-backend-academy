#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_didactic_code_upgrade.py

Модернизация блоков кода в конспектах и карточках:
1. Замена интерактивных кнопок «▶ Запустить код» на дидактическую шапку:
   бейдж языка Python + кнопка «Копировать» (data-copy-code="1").
2. Удаление пустых рудиментов <div class="snippet-out hidden"></div>.
3. Добавление стилей .code-lang-tag и .btn-copy-code (для темной и светлой тем).
4. Добавление функции copySnippetCode и обработчика клика data-copy-code.
5. Обновление функции decorateCodeBlocksWithRunBtn.
"""

import re
from pathlib import Path

def upgrade_html_text(text: str) -> str:
    # 1. Замена экранированных кнопок запуска в JSON-структурах
    def repl_esc(m):
        lang = m.group(1) or 'python'
        has_slash = '\\/' in m.group(0)
        slash = '\\/' if has_slash else '/'
        return f'<div class=\\"code-run-bar\\"><span class=\\"code-lang-tag\\">{lang}<{slash}span><button type=\\"button\\" class=\\"btn-copy-code\\" data-copy-code=\\"1\\" title=\\"Скопировать код\\">Копировать<{slash}button><{slash}div>'

    pat_esc = re.compile(
        r'<div class=\\"code-run-bar\\">(?:<span class=\\"(?:mono meta|code-lang-tag)\\">([a-zA-Z0-9_+-]*)<\\?\/span>)?<button type=\\"button\\" class=\\"btn-inline-run\\"[^>]*>▶ Запустить код<\\?\/button><\\?\/div>'
    )
    text, n_esc = pat_esc.subn(repl_esc, text)
    print(f"  Replaced {n_esc} escaped run-bars.")

    # 2. Замена неэкранированных кнопок запуска
    def repl_unesc(m):
        lang = m.group(1) or 'python'
        return f'<div class="code-run-bar"><span class="code-lang-tag">{lang}</span><button type="button" class="btn-copy-code" data-copy-code="1" title="Скопировать код">Копировать</button></div>'

    pat_unesc = re.compile(
        r'<div class="code-run-bar">(?:<span class="(?:mono meta|code-lang-tag)">([a-zA-Z0-9_+-]*)<\/span>)?<button type="button" class="btn-inline-run"[^>]*>▶ Запустить код<\/button><\/div>'
    )
    text, n_unesc = pat_unesc.subn(repl_unesc, text)
    print(f"  Replaced {n_unesc} unescaped run-bars.")

    # 3. Удаление snippet-out hidden элементов
    pat_out_esc = re.compile(r'<div class=\\"snippet-out hidden\\"><\\?\/div>')
    text, n_out_esc = pat_out_esc.subn('', text)
    print(f"  Removed {n_out_esc} escaped snippet-out elements.")

    pat_out_unesc = re.compile(r'<div class="snippet-out hidden"><\/div>')
    text, n_out_unesc = pat_out_unesc.subn('', text)
    print(f"  Removed {n_out_unesc} unescaped snippet-out elements.")

    # 4. Обновление функции decorateCodeBlocksWithRunBtn
    new_decorate = """function decorateCodeBlocksWithRunBtn(htmlStr){
  let s = String(htmlStr || '');

  // 1. Нормализация кода во всех сниппетах (перенос хвостовых комментариев НАД строкой)
  s = s.replace(/<pre\\b[^>]*><code\\b[^>]*>([\\s\\S]*?)<\\/code><\\/pre>/gi, function(full, codeInner){
    const normalized = normalizeCodeSnippets(codeInner);
    const looksLikePython = !(/^(SELECT|INSERT|UPDATE|DELETE|CREATE|FROM|docker|git|GET|POST|PATCH|PUT|paths:)/i.test(normalized.trim()));
    const highlighted = (looksLikePython && typeof highlightPythonTokens === 'function') ? highlightPythonTokens(normalized) : normalized;
    return `<pre><code>${highlighted}</code></pre>`;
  });

  // 2. Если перед <pre> есть code-run-bar — приводим к чистой дидактической плашке с кнопкой копирования
  s = s.replace(/<div\\s+class=["']code-run-bar["']>([\\s\\S]*?)<\\/div>(\\s*<pre\\b[^>]*><code\\b[^>]*>[\\s\\S]*?<\\/code><\\/pre>)/gi, function(full, barInner, prePart){
    return `<div class="code-run-bar"><span class="code-lang-tag">python</span><button type="button" class="btn-copy-code" data-copy-code="1" title="Скопировать код">Копировать</button></div>${prePart}`;
  });

  // Если snippet-wrap не имел code-run-bar вовсе — добавляем дидактическую плашку перед <pre>
  s = s.replace(/(<div\\s+class=["']snippet-wrap["'][^>]*>)(\\s*<pre\\b[^>]*><code\\b[^>]*>)/gi, '$1<div class="code-run-bar"><span class="code-lang-tag">python</span><button type="button" class="btn-copy-code" data-copy-code="1" title="Скопировать код">Копировать</button></div>$2');

  // Убираем старые рудименты snippet-out
  s = s.replace(/<div\\s+class=["']snippet-out\\s*hidden["']>\\s*<\\/div>/gi, '');

  if(s.indexOf('snippet-wrap') !== -1 || s.indexOf('code-snippet-wrap') !== -1) return s;

  // 3. Для сырых блоков <pre><code> оборачиваем в snippet-wrap с кнопкой копирования
  return s.replace(/<pre><code>([\\s\\S]*?)<\\/code><\\/pre>/g, function(full, codeInner){
    const looksLikePython = !(/^(SELECT|INSERT|UPDATE|DELETE|CREATE|FROM|docker|git|GET|POST|PATCH|PUT|paths:)/i.test(codeInner.trim()));
    const subParts = splitLongCodeSnippets(codeInner);
    return subParts.map(sp => {
      const highlighted = looksLikePython ? highlightPythonTokens(sp) : sp;
      const langLabel = looksLikePython ? 'python' : 'code';
      return `<div class="snippet-wrap"><div class="code-run-bar"><span class="code-lang-tag">${langLabel}</span><button type="button" class="btn-copy-code" data-copy-code="1" title="Скопировать код">Копировать</button></div><pre><code>${highlighted}</code></pre></div>`;
    }).join('\\n');
  });
}"""

    pat_func = re.compile(r'function decorateCodeBlocksWithRunBtn\(htmlStr\)\{[\s\S]*?\n\}', re.MULTILINE)
    if pat_func.search(text):
        text = pat_func.sub(lambda _: new_decorate, text, count=1)
        print("  Updated decorateCodeBlocksWithRunBtn successfully.")

    # 5. Добавление стилей для .code-lang-tag и .btn-copy-code
    css_to_add = """
/* Дидактические плашки сниппетов кода без запуска с кнопкой быстрого копирования */
.code-run-bar{display:flex !important;align-items:center !important;justify-content:space-between !important;background:rgba(15,23,42,0.75) !important;border:1px solid rgba(255,255,255,0.10) !important;border-bottom:1px solid rgba(255,255,255,0.06) !important;border-radius:12px 12px 0 0 !important;padding:6px 12px !important;user-select:none;}
.code-lang-tag{display:inline-flex !important;align-items:center !important;gap:6px !important;font-family:var(--font-m, 'JetBrains Mono', monospace) !important;font-size:0.72rem !important;font-weight:700 !important;color:#94a3b8 !important;text-transform:uppercase !important;letter-spacing:0.06em !important;}
.code-lang-tag::before{content:'' !important;display:inline-block !important;width:6px !important;height:6px !important;border-radius:50% !important;background:#10b981 !important;box-shadow:0 0 6px rgba(16,185,129,0.6) !important;}
.btn-copy-code{display:inline-flex !important;align-items:center !important;gap:5px !important;background:rgba(255,255,255,0.05) !important;color:#94a3b8 !important;border:1px solid rgba(255,255,255,0.12) !important;border-radius:8px !important;padding:3px 10px !important;font-family:var(--font-s, 'Onest', sans-serif) !important;font-size:0.72rem !important;font-weight:600 !important;cursor:pointer !important;transition:all 0.2s cubic-bezier(0.16,1,0.3,1) !important;line-height:1.3 !important;}
.btn-copy-code:hover{background:rgba(16,185,129,0.15) !important;color:#10b981 !important;border-color:rgba(16,185,129,0.40) !important;}
.btn-copy-code.is-copied{background:rgba(16,185,129,0.25) !important;color:#a7f3d0 !important;border-color:#10b981 !important;}
[data-theme="light"] .code-run-bar{background:rgba(241,245,249,0.90) !important;border-color:rgba(0,0,0,0.08) !important;}
[data-theme="light"] .code-lang-tag{color:#64748b !important;}
[data-theme="light"] .btn-copy-code{background:rgba(0,0,0,0.04) !important;color:#64748b !important;border-color:rgba(0,0,0,0.12) !important;}
[data-theme="light"] .btn-copy-code:hover{background:rgba(5,150,105,0.12) !important;color:#059669 !important;border-color:rgba(5,150,105,0.35) !important;}
[data-theme="light"] .btn-copy-code.is-copied{background:rgba(5,150,105,0.18) !important;color:#065f46 !important;border-color:#059669 !important;}
"""
    if '.btn-copy-code{' not in text:
        text = text.replace('</style>', css_to_add + '\n</style>', 1)
        print("  Appended didactic code CSS styles.")

    # 6. Добавление функции copySnippetCode и обработчика клика
    copy_js = """
// Инвариант: быстрое копирование сниппета кода в буфер обмена
function copySnippetCode(btnEl){
  if(!btnEl) return;
  const wrap = btnEl.closest('.snippet-wrap, .code-snippet-wrap') || btnEl.parentElement.parentElement;
  const codeEl = wrap ? wrap.querySelector('pre code, code') : null;
  const rawText = codeEl ? (codeEl.innerText || codeEl.textContent || '') : '';
  if(!rawText) return;

  function markCopied(){
    const origText = btnEl.textContent;
    btnEl.classList.add('is-copied');
    btnEl.textContent = '✓ Скопировано';
    setTimeout(function(){
      btnEl.classList.remove('is-copied');
      btnEl.textContent = origText;
    }, 1600);
  }

  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(rawText).then(markCopied).catch(function(){
      fallbackCopyText(rawText);
      markCopied();
    });
  } else {
    fallbackCopyText(rawText);
    markCopied();
  }
}

function fallbackCopyText(text){
  try {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    ta.style.top = '0';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
  } catch(e){}
}
"""
    if 'function copySnippetCode(' not in text:
        text = text.replace('async function runInlineSnippet(btnEl){', copy_js + '\nasync function runInlineSnippet(btnEl){', 1)
        print("  Injected copySnippetCode function.")

    old_click = "const runInl = e.target.closest('[data-run-inline], [data-run-snippet]');"
    new_click = """const copyBtn = e.target.closest('[data-copy-code]');
  if(copyBtn){
    e.preventDefault();
    e.stopPropagation();
    copySnippetCode(copyBtn);
    return;
  }

  const runInl = e.target.closest('[data-run-inline], [data-run-snippet]');"""
    if old_click in text and 'const copyBtn = e.target.closest' not in text:
        text = text.replace(old_click, new_click, 1)
        print("  Injected copyBtn click handler in document listener.")

    return text

def main():
    st_path = Path("standards/standards.html")
    print(f"Upgrading {st_path}...")
    orig = st_path.read_text(encoding="utf-8")
    upgraded = upgrade_html_text(orig)
    st_path.write_text(upgraded, encoding="utf-8")
    print(f"Saved {st_path} ({len(orig)} -> {len(upgraded)} bytes).")

    # Синхронизация с academy.html
    ac_path = Path("academy.html")
    print(f"Syncing to {ac_path}...")
    ac_path.write_text(upgraded, encoding="utf-8")
    print(f"Saved {ac_path} (100% match).")

    # Обновление data/content/notes.json
    notes_path = Path("data/content/notes.json")
    if notes_path.exists():
        print(f"Upgrading {notes_path}...")
        notes_txt = notes_path.read_text(encoding="utf-8")
        pat_notes_esc = re.compile(
            r'<div class=\\"code-run-bar\\">(?:<span class=\\"(?:mono meta|code-lang-tag)\\">([a-zA-Z0-9_+-]*)<\\?\/span>)?<button type=\\"button\\" class=\\"btn-inline-run\\"[^>]*>▶ Запустить код<\\?\/button><\\?\/div>'
        )
        def repl_notes(m):
            lang = m.group(1) or 'python'
            return f'<div class=\\"code-run-bar\\"><span class=\\"code-lang-tag\\">{lang}<\\/span><button type=\\"button\\" class=\\"btn-copy-code\\" data-copy-code=\\"1\\" title=\\"Скопировать код\\">Копировать<\\/button><\\/div>'
        
        notes_txt, n1 = pat_notes_esc.subn(repl_notes, notes_txt)
        pat_notes_out = re.compile(r'<div class=\\"snippet-out hidden\\"><\\?\/div>')
        notes_txt, n2 = pat_notes_out.subn('', notes_txt)
        notes_path.write_text(notes_txt, encoding="utf-8")
        print(f"  notes.json: replaced {n1} buttons, removed {n2} snippet-outs.")

if __name__ == '__main__':
    main()
