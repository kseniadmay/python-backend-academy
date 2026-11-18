# -*- coding: utf-8 -*-
"""
scripts/apply_russian_card_answers.py

Комплексное переписывание ответов флеш-карточек согласно правилам русского языка:
1. Заглавная буква в начале ответа и в начале каждого предложения.
2. Типографическое длинное тире « — » вместо дефиса и короткого тире между словами.
3. Литературные грамматические нормы (например, «байтов» в родительном падеже).
4. Устранение пробелов перед знаками препинания и двойных пробелов.
5. Обязательная точка в конце каждого ответа карточки (включая окончания на </code>, </span>, ), », code, ссылки).
6. Синхронизация всех 4 канонических слоёв платформы:
   - data/content/cards.json (все 287 колод, 6101 карточка)
   - knowledge_base/**/📇 Карточки/*.md (все 287 markdown-файлов)
   - standards/standards.html (все 7 треков Mastery + runtime-функция formatCardAnswerHTML)
   - academy.html (100% побайтовая идентичность стандарта)
"""

import json
import os
import re
import sys
import shutil

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, '..'))


def mask_html_and_code(text):
    tokens = {}
    counter = [0]

    def repl(m):
        key = f"___TK_{counter[0]}___"
        counter[0] += 1
        tokens[key] = m.group(0)
        return key

    # 1. HTML-комментарии
    masked = re.sub(r'<!--[\s\S]*?-->', repl, text)
    # 2. Блоки кода <div class="fc-code-box">...</div>
    masked = re.sub(r'<div\b[^>]*>[\s\S]*?</div>', repl, masked)
    # 3. <pre>...</pre>
    masked = re.sub(r'<pre\b[^>]*>[\s\S]*?</pre>', repl, masked)
    # 4. <code>...</code>
    masked = re.sub(r'<code\b[^>]*>[\s\S]*?</code>', repl, masked)
    # 5. Markdown backticks `...`
    masked = re.sub(r'`[^`\n]+`', repl, masked)
    # 6. Математические формулы
    masked = re.sub(r'<span class="math-formula">[\s\S]*?</span>', repl, masked)
    masked = re.sub(r'\$[^\$\n]+\$', repl, masked)
    # 7. Оставшиеся HTML-теги
    masked = re.sub(r'</?[a-zA-Z0-9]+[^>]*>', repl, masked)

    return masked, tokens


def unmask_html_and_code(text, tokens):
    res = text
    for k in reversed(list(tokens.keys())):
        res = res.replace(k, tokens[k])
    return res


def clean_and_punctuate_answer(text: str) -> str:
    if not text:
        return ''
    s = text.strip()
    if not s:
        return ''

    masked, tokens = mask_html_and_code(s)

    # 1. Нормализация пробелов вокруг знаков препинания
    masked = re.sub(r'\s+([,:;])', r'\1', masked)
    masked = re.sub(r'\s+([!?])', r'\1', masked)
    masked = re.sub(r'(?<!\.)\s+\.(?!\.)', '.', masked)
    masked = re.sub(r'\s+\)', ')', masked)
    masked = re.sub(r'\(\s+', '(', masked)
    masked = re.sub(r'[ \t]{2,}', ' ', masked)

    # 2. Нормализация тире между словами (длинное тире с отбивкой пробелами)
    masked = re.sub(r' (?:\u2013|\u2014|-|–) ', ' — ', masked)

    # 3. Нормы русского языка
    # Форма родительного падежа: байтов
    masked = re.sub(r'(\b\d+\s+)байт\b', r'\1байтов', masked)
    masked = re.sub(r'(\bпоследовательност\w*\s+)байт\b', r'\1байтов', masked)
    masked = re.sub(r'(\bмассив\w*\s+)байт\b', r'\1байтов', masked)
    # Пунктуация в оборотах и сложноподчинённых предложениях
    # Сопоставительный союз «чем ..., тем ...» — строго запятая, а не тире
    masked = re.sub(r'\b(чем\b[^.!?;—\n]+?)\s+(?:—|–|-)\s+(тем\b)', r'\1, \2', masked, flags=re.IGNORECASE)
    masked = re.sub(r'\b(в том же процессе)\s+(что и)\b', r'\1, \2', masked)
    masked = re.sub(r'\b(задачи)\s+(ограниченные скоростью)\b', r'\1, \2', masked)
    verbs = r'(?:указывает|гарантирует|означает|показывает|проверяет|подтверждает|требует|сообщает|говорит|следит|утверждает|считает|значит|убеждается)'
    masked = re.sub(rf'(\b{verbs}(?:\s+___TK_\d+___|\s+[A-Za-z0-9_]+)?)\s+(что|чтобы)\b', r'\1, \2', masked, flags=re.IGNORECASE)
    masked = re.sub(r'(?<![,:;—\-\(\[\{])\s+\b(при котором|в котором|из которого|для которого|с помощью которого|на котором|по которому)\b', r', \1', masked)
    masked = re.sub(r'(\b[а-яА-Яa-zA-Z0-9_>]+)\s+(так как)\b', r'\1, \2', masked)

    # 4. Заглавная буква в начале русского текста
    if masked and 'а' <= masked[0] <= 'я':
        masked = masked[0].upper() + masked[1:]

    # Заглавная буква после точки с пробелом
    def cap_after_period(m):
        return m.group(1) + m.group(2).upper()
    masked = re.sub(r'(\.\s+)([а-я])', cap_after_period, masked)

    # Восстановление маскированного кода и тегов
    res = unmask_html_and_code(masked, tokens).strip()

    # 5. Обязательная точка в конце (терминальная пунктуация)
    # Если заканчивается на </div> (контейнер сниппета, где пояснение внутри уже с точкой)
    if res.endswith('</div>'):
        return res

    # Если уже есть терминальный знак (. ! ? …)
    if re.search(r'[.!?…]\s*$', res):
        return res

    # Окончания на закрывающие теги и разметку
    if res.endswith('</code>') or res.endswith('</span>') or res.endswith('`') or res.endswith('$') or res.endswith(')'):
        return res + '.'

    # Окончание на закрывающую кавычку
    if res.endswith('»'):
        # Если внутри кавычек вопрос или восклицание («Кто ты?»), точка по правилам не ставится
        if re.search(r'[!?]»$', res):
            return res
        return res + '.'

    if res.endswith('"') or res.endswith("'"):
        return res + '.'

    # Обычный текст / символ в конце
    return res + '.'


def apply_updates():
    print("====================================================================")
    print("  🚀 Тотальная русификация и расстановка точек в ответах карточек  ")
    print("====================================================================")

    # 1. data/content/cards.json
    cards_json_path = os.path.join(_ROOT, 'data', 'content', 'cards.json')
    with open(cards_json_path, 'r', encoding='utf-8') as f:
        cards_data = json.load(f)

    cards_json_updated = 0
    total_json_cards = 0
    for did, deck in cards_data.items():
        for card in deck.get('cards', []):
            total_json_cards += 1
            old_a = card.get('a', '')
            new_a = clean_and_punctuate_answer(old_a)
            if old_a != new_a:
                card['a'] = new_a
                cards_json_updated += 1

    with open(cards_json_path, 'w', encoding='utf-8') as f:
        json.dump(cards_data, f, ensure_ascii=False, indent=2)
    print(f"[1/4] data/content/cards.json: обновлено {cards_json_updated} из {total_json_cards} карточек")

    # 2. knowledge_base/**/*.md
    kb_dir = os.path.join(_ROOT, 'knowledge_base')
    kb_files_updated = 0
    kb_lines_updated = 0
    kb_total_lines = 0

    for root, dirs, files in os.walk(kb_dir):
        for fname in files:
            if fname.endswith('.md') and 'Карточки' in root:
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()

                lines = content.splitlines()
                new_lines = []
                file_changed = False

                for line in lines:
                    m = re.match(r'^(\d+\.\s+.*?\s*>>\s*)(.*)$', line)
                    if m:
                        kb_total_lines += 1
                        prefix = m.group(1)
                        ans = m.group(2).strip()
                        new_ans = clean_and_punctuate_answer(ans)
                        if ans != new_ans:
                            file_changed = True
                            kb_lines_updated += 1
                            new_lines.append(f"{prefix}{new_ans}")
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)

                if file_changed:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines) + '\n')
                    kb_files_updated += 1

    print(f"[2/4] knowledge_base: обновлено {kb_lines_updated} карточек в {kb_files_updated} файлах")

    # 3. standards/standards.html
    standards_path = os.path.join(_ROOT, 'standards', 'standards.html')
    academy_path = os.path.join(_ROOT, 'academy.html')

    with open(standards_path, 'r', encoding='utf-8') as f:
        html = f.read()

    tracks = ['PY_MASTERY', 'WEB_MASTERY', 'BACKEND_MASTERY', 'ALGO_MASTERY', 'DB_MASTERY', 'ARCH_MASTERY', 'INFRA_MASTERY']
    tracks_updated_count = 0
    total_track_cards = 0

    for tr in tracks:
        m = re.search(rf'(const\s+{tr}\s*=\s*)(\{{.*?\}})(;\s*(?:const|window))', html, re.DOTALL)
        if not m:
            print(f"  ВНИМАНИЕ: Трек {tr} не найден в standards.html!")
            continue

        prefix = m.group(1)
        raw_json = m.group(2)
        suffix = m.group(3)
        track_data = json.loads(raw_json)

        track_changed = False
        decks = track_data.get('decks', {})
        for did, d in decks.items():
            for card in d.get('cards', []):
                total_track_cards += 1
                old_a = card.get('a', '')
                new_a = clean_and_punctuate_answer(old_a)
                if old_a != new_a:
                    card['a'] = new_a
                    tracks_updated_count += 1
                    track_changed = True

        if track_changed:
            new_raw_json = json.dumps(track_data, ensure_ascii=False)
            old_block = m.group(0)
            new_block = prefix + new_raw_json + suffix
            html = html.replace(old_block, new_block, 1)

    # Также совершенствуем formatCardAnswerHTML для гарантии точек в UI
    old_is_two_simple = """        if(isTwoSimpleParts){
          const cleanP1 = capitalizeSentenceStart(p1.replace(/\\s+(?:—|–|-)\\s*$/g, '').trim());
          const cleanP2 = p2.replace(/^\\s*(?:—|–|-)\\s*/g, '').trim();
          const combined = cleanP1 + ' — ' + cleanP2;
          const formatted = (typeof formatRichInlineText === 'function') ? formatRichInlineText(combined) : combined;
          return `<div class=\"fc-answer-multiline\"><div class=\"fc-answer-item\"><span class=\"fc-answer-text\">${formatted}</span></div></div>`;
        }"""

    new_is_two_simple = """        if(isTwoSimpleParts){
          const cleanP1 = capitalizeSentenceStart(p1.replace(/\\s+(?:—|–|-)\\s*$/g, '').trim());
          let cleanP2 = p2.replace(/^\\s*(?:—|–|-)\\s*/g, '').trim();
          if(!cleanP2.endsWith('.') && !cleanP2.endsWith('!') && !cleanP2.endsWith('?') && !cleanP2.endsWith('…')){
            cleanP2 += '.';
          }
          const combined = cleanP1 + ' — ' + cleanP2;
          const formatted = (typeof formatRichInlineText === 'function') ? formatRichInlineText(combined) : combined;
          return `<div class=\"fc-answer-multiline\"><div class=\"fc-answer-item\"><span class=\"fc-answer-text\">${formatted}</span></div></div>`;
        }"""

    if old_is_two_simple in html:
        html = html.replace(old_is_two_simple, new_is_two_simple, 1)
        print("  ✓ formatCardAnswerHTML (isTwoSimpleParts) дополнен гарантией точки")

    old_items_map = """        const itemsHtml = parts.map(part => {
          const capitalized = capitalizeSentenceStart(part.replace(/^\\s*(?:—|–|-|•|\\*)\\s*/, '').trim());
          const normalized = capitalized.replace(/\\s+(?:—|–|-)\\s+/g, ' — ');
          const formatted = (typeof formatRichInlineText === 'function') ? formatRichInlineText(normalized) : normalized;
          return `<div class=\"fc-answer-item\"><span class=\"fc-answer-bullet\" style=\"display:none !important;\"></span><span class=\"fc-answer-text\">${formatted}</span></div>`;
        }).join('');"""

    new_items_map = """        const itemsHtml = parts.map(part => {
          let capitalized = capitalizeSentenceStart(part.replace(/^\\s*(?:—|–|-|•|\\*)\\s*/, '').trim());
          let normalized = capitalized.replace(/\\s+(?:—|–|-)\\s+/g, ' — ');
          if(!normalized.endsWith('.') && !normalized.endsWith('!') && !normalized.endsWith('?') && !normalized.endsWith('…') && !normalized.endsWith(';')){
            normalized += '.';
          }
          const formatted = (typeof formatRichInlineText === 'function') ? formatRichInlineText(normalized) : normalized;
          return `<div class=\"fc-answer-item\"><span class=\"fc-answer-bullet\" style=\"display:none !important;\"></span><span class=\"fc-answer-text\">${formatted}</span></div>`;
        }).join('');"""

    if old_items_map in html:
        html = html.replace(old_items_map, new_items_map, 1)
        print("  ✓ formatCardAnswerHTML (itemsHtml) дополнен гарантией точки для списков")

    old_capsule = """      if(isCapsuleCode){
        const reescaped = escapeHtmlStr(cleanCode);
        const codeHtml = (typeof highlightPythonTokens === 'function') ? highlightPythonTokens(reescaped) : reescaped;
        const expFormatted = (typeof formatRichInlineText === 'function') ? formatRichInlineText(explanation) : explanation;
        return `
          <div class=\"fc-code-capsule\">
            <code class=\"fc-code-primary\">${codeHtml}</code>
          </div>
          <div class=\"fc-answer-explanation\">
            <span class=\"fc-explanation-dash\">—</span> ${expFormatted}
          </div>
        `;
      }"""

    new_capsule = """      if(isCapsuleCode){
        const reescaped = escapeHtmlStr(cleanCode);
        const codeHtml = (typeof highlightPythonTokens === 'function') ? highlightPythonTokens(reescaped) : reescaped;
        let expClean = explanation.trim();
        if(!expClean.endsWith('.') && !expClean.endsWith('!') && !expClean.endsWith('?') && !expClean.endsWith('…')){
          expClean += '.';
        }
        const expFormatted = (typeof formatRichInlineText === 'function') ? formatRichInlineText(expClean) : expClean;
        return `
          <div class=\"fc-code-capsule\">
            <code class=\"fc-code-primary\">${codeHtml}</code>
          </div>
          <div class=\"fc-answer-explanation\">
            <span class=\"fc-explanation-dash\">—</span> ${expFormatted}
          </div>
        `;
      }"""

    if old_capsule in html:
        html = html.replace(old_capsule, new_capsule, 1)
        print("  ✓ formatCardAnswerHTML (codeCapsule) дополнен гарантией точки")

    old_default_ret = "  return (typeof formatRichInlineText === 'function') ? formatRichInlineText(s) : s;"
    new_default_ret = """  let finalAns = s;
  if(!finalAns.endsWith('</div>') && !finalAns.endsWith('.') && !finalAns.endsWith('!') && !finalAns.endsWith('?') && !finalAns.endsWith('…') && !(finalAns.endsWith('»') && (finalAns.includes('?') || finalAns.includes('!')))){
    finalAns += '.';
  }
  return (typeof formatRichInlineText === 'function') ? formatRichInlineText(finalAns) : finalAns;"""

    if old_default_ret in html:
        html = html.replace(old_default_ret, new_default_ret, 1)
        print("  ✓ formatCardAnswerHTML (default return) дополнен гарантией точки")

    with open(standards_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[3/4] standards/standards.html: обновлено {tracks_updated_count} карточек в 7 треках Mastery")

    # 4. academy.html (100% побайтовая идентичность)
    shutil.copyfile(standards_path, academy_path)
    print(f"[4/4] academy.html: синхронизирован со standards.html (100% побайтовая идентичность)")

    print("====================================================================")
    print("  ✓ Успешно завершено! Все ответы соответствуют нормам и имеют точки ")
    print("====================================================================")


if __name__ == '__main__':
    apply_updates()
