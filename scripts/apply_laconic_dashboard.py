import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_path = os.path.join(root, 'academy.html')

with open(academy_path, 'r', encoding='utf-8') as f:
    content = f.read()

print('Initial academy.html length:', len(content))

# 1. Eyebrow in Hero Card: remove redundant 'ФОКУС ·'
t1 = '  const focusEyebrowText = `● ФОКУС · ${cleanUnitTitle.toUpperCase()}`;'
r1 = '  const focusEyebrowText = `● ${cleanUnitTitle.toUpperCase()}`;'
assert t1 in content, 'Target 1 not found'
content = content.replace(t1, r1, 1)
print('1. [PASS] Removed redundant "ФОКУС ·" from eyebrow')

# 2. Balanced second row in echelon topbar (XP badge + Echelon subtitle)
t2 = """        <!-- Ряд 2: Чистая строка суточного прогресс-бейджа XP -->
        <div class="echelon-topbar-subrow" style="display:flex;align-items:center;width:100%;">
          <div class="echelon-subrow-xp" style="display:flex;align-items:center;min-width:0;">
            ${todayXp() === 0
              ? `<span class="day-xp-badge empty-day-badge" style="background:rgba(245, 158, 11, 0.10);border:1px solid rgba(245, 158, 11, 0.28);color:#fbbf24;white-space:nowrap;display:inline-flex;align-items:center;" title="Сделайте первый шаг дня: +15 XP">⚡ 0&nbsp;XP за сутки</span>`
              : `<span class="day-xp-badge" style="white-space:nowrap;" title="Заработано за сутки: ${tXp} XP">⚡ +${todayXp()}&nbsp;XP за сутки</span>`
            }
          </div>
        </div>"""

r2 = """        <!-- Ряд 2: Чистая строка суточного прогресс-бейджа XP и эшелона -->
        <div class="echelon-topbar-subrow" style="display:flex;align-items:center;justify-content:space-between;width:100%;">
          <div class="echelon-subrow-xp" style="display:flex;align-items:center;min-width:0;">
            ${todayXp() === 0
              ? `<span class="day-xp-badge empty-day-badge" style="background:rgba(245, 158, 11, 0.10);border:1px solid rgba(245, 158, 11, 0.28);color:#fbbf24;white-space:nowrap;display:inline-flex;align-items:center;" title="Сделайте первый шаг дня: +15 XP">⚡ 0&nbsp;XP за сутки</span>`
              : `<span class="day-xp-badge" style="white-space:nowrap;" title="Заработано за сутки: ${tXp} XP">⚡ +${todayXp()}&nbsp;XP за сутки</span>`
            }
          </div>
          <span class="meta" style="font-size:.74rem;color:var(--ink-muted);white-space:nowrap;margin-left:auto;">Эшелон 1 · Фундамент</span>
        </div>"""
assert t2 in content, 'Target 2 not found'
content = content.replace(t2, r2, 1)
print('2. [PASS] Balanced echelon subrow with Echelon 1 title')

# 3. Punchy and laconic micro-hint in daily goal card
t3 = """  const goalMicroHintText = remainingGoalSteps > 0
    ? (tXp === 0
        ? (currentStreakVal > 0 ? `Сделайте первый шаг дня ⚡ · Продлите серию до <b>${currentStreakVal + 1} дней</b>` : `Сделайте первый шаг дня ⚡`)
        : `⚡ 1 микро-шаг = +15 XP · До цели: <b>${remainingGoalSteps}&nbsp;${stepsWord}</b>`)
    : `⚡ Дневная цель выполнена! Отличный темп`;"""

r3 = """  const goalMicroHintText = remainingGoalSteps > 0
    ? (tXp === 0
        ? (currentStreakVal > 0 ? `Первый шаг дня продлит серию 🔥 <b>${currentStreakVal + 1} дн.</b>` : `Сделайте первый шаг дня ⚡`)
        : `⚡ 1 шаг = +15 XP · До цели: <b>${remainingGoalSteps}&nbsp;${stepsWord}</b>`)
    : `⚡ Дневная цель выполнена! Отличный темп`;"""
assert t3 in content, 'Target 3 not found'
content = content.replace(t3, r3, 1)
print('3. [PASS] Laconic goal micro-hint applied')

# 4. Zero-state SRS: remove distracting link to all decks on day 1
t4 = """              : (!hasReviewedAnyCard
                  ? `<div style="margin-top:auto;padding-top:8px;border-top:1px solid rgba(255,255,255,0.04);display:flex;align-items:center;justify-content:flex-start;min-height:24px;font-size:0.74rem;color:var(--ink-muted);"><a href="#/cards" class="link-quiet text-muted" style="text-decoration:none;display:inline-flex;align-items:center;gap:4px;font-size:0.74rem;transition:color .2s ease;">Все колоды ➔</a></div>`
                  : `<div style="display:flex;justify-content:flex-end;"><a href="#/cards" class="btn-srs-pill link-quiet text-muted">Обзор колод ➔</a></div>`
                )"""

r4 = """              : (!hasReviewedAnyCard
                  ? ''
                  : `<div style="display:flex;justify-content:flex-end;"><a href="#/cards" class="btn-srs-pill link-quiet text-muted">Обзор колод ➔</a></div>`
                )"""
assert t4 in content, 'Target 4 not found'
content = content.replace(t4, r4, 1)
print('4. [PASS] Omitted distracting "Все колоды ➔" link during zero-state SRS')

# 5. Accordion: minimal lock icon on mobile instead of repetitive text badge
t5 = '<span class="dash-step-locked-badge-desk">🔒 Закрыто</span><span class="dash-step-locked-badge-mob">🔒 Закрыто</span>'
r5 = '<span class="dash-step-locked-badge-desk">🔒 Закрыто</span><span class="dash-step-locked-badge-mob">🔒</span>'
assert t5 in content, 'Target 5 not found'
content = content.replace(t5, r5, 1)
print('5. [PASS] Compact mobile lock icon applied to accordion')

# 6. Remove redundant micro-footer in dashboard
t6 = """      <div class="dash-micro-footer" style="text-align:center;padding:12px 0;font-size:0.72rem;color:var(--ink-muted);opacity:0.6;">
        Python Backend Academy
      </div>"""
r6 = ''
assert t6 in content, 'Target 6 not found'
content = content.replace(t6, r6, 1)
print('6. [PASS] Redundant dashboard micro-footer removed')

# 7. Max tokens in skill title format
t7 = 'const formatSkillTitleWithChips = (title, maxTokens = 4) => {'
r7 = 'const formatSkillTitleWithChips = (title, maxTokens = 3) => {'
assert t7 in content, 'Target 7 not found'
content = content.replace(t7, r7, 1)
print('7. [PASS] Format skill title maxTokens reduced to 3')

# Write updated academy.html
with open(academy_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated academy.html successfully. New length:', len(content))

# Byte-for-byte sync to etalons
etalon_path = os.path.join(root, 'Эталоны', 'Эталоны.html')
root_etalon = os.path.join(root, 'Эталоны.html')
shutil.copy2(academy_path, etalon_path)
shutil.copy2(academy_path, root_etalon)
print('Synchronized Эталоны/Эталоны.html and Эталоны.html')
