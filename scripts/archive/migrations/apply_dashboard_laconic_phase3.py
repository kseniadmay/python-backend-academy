import os
import sys

ACADEMY_PATH = '/Users/fury/OneDrive/Python_Backend_Academy/academy.html'
ETALON_PATH = '/Users/fury/OneDrive/Python_Backend_Academy/Эталоны.html'
ETALONS_FOLDER_PATH = '/Users/fury/OneDrive/Python_Backend_Academy/Эталоны/Эталоны.html'
SW_PATH = '/Users/fury/OneDrive/Python_Backend_Academy/sw.js'
TEST_PATH = '/Users/fury/OneDrive/Python_Backend_Academy/tests/test_dashboard_regression.js'

with open(ACADEMY_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update mobile CSS for echelon clean meta
old_css = '''    .dashboard-container .echelon-clean-meta {
      display: flex !important;
      flex-direction: column !important;
      align-items: flex-start !important;
      gap: 6px !important;
      width: 100% !important;
      margin-bottom: 6px !important;
    }
    .dashboard-container .echelon-readiness-emerald {
      white-space: normal !important;
      overflow: visible !important;
      text-overflow: clip !important;
      width: 100% !important;
      font-size: 0.88rem !important;
      line-height: 1.35 !important;
    }
    .dashboard-container .echelon-clean-meta .echelon-mp-counter {
      align-self: flex-start !important;
      margin-left: 0 !important;
    }'''

new_css = '''    .dashboard-container .echelon-clean-meta {
      display: flex !important;
      flex-direction: row !important;
      justify-content: space-between !important;
      align-items: center !important;
      gap: 8px !important;
      width: 100% !important;
      margin-bottom: 4px !important;
    }
    .dashboard-container .echelon-readiness-emerald {
      white-space: nowrap !important;
      overflow: hidden !important;
      text-overflow: ellipsis !important;
      font-size: 0.82rem !important;
      line-height: 1.2 !important;
      flex: 1 1 auto !important;
      min-width: 0 !important;
    }
    .dashboard-container .echelon-clean-meta .echelon-mp-counter {
      align-self: center !important;
      margin-left: auto !important;
      flex-shrink: 0 !important;
    }'''

if old_css not in content:
    print('ERROR: old_css not found in academy.html')
    sys.exit(1)

content = content.replace(old_css, new_css, 1)

# 2. Update echelon topic counter and mobile readiness label in viewDashboard
old_echelon = '''            ${e1CurMp === 0
              ? `<span class="echelon-readiness-emerald" style="font-weight:700;font-size:.82rem;flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                  <span class="echelon-label-full">Готовность к тех-скринингу</span>
                  <span class="echelon-label-mobile">Готовность к тех-скринингу</span>
                </span>
                <span class="meta echelon-mp-counter" style="font-size:.74rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 7px;border-radius:6px;white-space:nowrap;flex-shrink:0;">Тема 1 из ${curUnitTotal} · Старт</span>`
              : `<span class="echelon-readiness-emerald" style="font-weight:700;font-size:.82rem;flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                  <span class="echelon-label-full">Готовность к тех-скринингу: ${e1Pct}%</span>
                  <span class="echelon-label-mobile">Готовность к тех-скринингу: ${e1Pct}%</span>
                </span>
                <span class="meta echelon-mp-counter" style="font-size:.74rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 7px;border-radius:6px;white-space:nowrap;flex-shrink:0;">${curUnitDone === 0 ? `Тема 1 из ${curUnitTotal} · Старт` : `${curUnitDone} из ${curUnitTotal} тем`}</span>`
            }'''

new_echelon = '''            ${e1CurMp === 0
              ? `<span class="echelon-readiness-emerald" style="font-weight:700;font-size:.82rem;flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                  <span class="echelon-label-full">Готовность к тех-скринингу</span>
                  <span class="echelon-label-mobile">Тех-скрининг</span>
                </span>
                <span class="meta echelon-mp-counter" style="font-size:.74rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 7px;border-radius:6px;white-space:nowrap;flex-shrink:0;">Тема 1 из ${curUnitTotal}</span>`
              : `<span class="echelon-readiness-emerald" style="font-weight:700;font-size:.82rem;flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                  <span class="echelon-label-full">Готовность к тех-скринингу: ${e1Pct}%</span>
                  <span class="echelon-label-mobile">Тех-скрининг: ${e1Pct}%</span>
                </span>
                <span class="meta echelon-mp-counter" style="font-size:.74rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 7px;border-radius:6px;white-space:nowrap;flex-shrink:0;">${curUnitDone === 0 ? `Тема 1 из ${curUnitTotal}` : `${curUnitDone} из ${curUnitTotal} тем`}</span>`
            }'''

if old_echelon not in content:
    print('ERROR: old_echelon not found in academy.html')
    sys.exit(1)

content = content.replace(old_echelon, new_echelon, 1)

# 3. Update streak grammar in goalMicroHintText
old_streak = '''  const goalMicroHintText = remainingGoalSteps > 0
    ? (tXp === 0
        ? (currentStreakVal > 0 ? `Первый шаг дня продлит серию 🔥 <b>${currentStreakVal + 1} дн.</b>` : `Сделайте первый шаг дня ⚡`)
        : `⚡ 1 шаг = +15 XP · До цели: <b>${remainingGoalSteps}&nbsp;${stepsWord}</b>`)
    : `⚡ Дневная цель выполнена! Отличный темп`;'''

new_streak = '''  const goalMicroHintText = remainingGoalSteps > 0
    ? (tXp === 0
        ? (currentStreakVal > 0 ? `Первый шаг продлит серию до 🔥 <b>${currentStreakVal + 1} дн.</b>` : `Сделайте первый шаг дня ⚡`)
        : `⚡ 1 шаг = +15 XP · До цели: <b>${remainingGoalSteps}&nbsp;${stepsWord}</b>`)
    : `⚡ Дневная цель выполнена! Отличный темп`;'''

if old_streak not in content:
    print('ERROR: old_streak not found in academy.html')
    sys.exit(1)

content = content.replace(old_streak, new_streak, 1)

# 4. Update SRS closed deck text to dynamically reflect remaining steps
old_srs = '''                      <div style="display:flex;align-items:center;gap:6px;padding:6px 2px 0;font-size:.74rem;">
                        <span style="color:var(--ink-muted);font-size:.74rem;display:inline-flex;align-items:center;gap:5px;" title="🌱 Откроется после 3 шагов теории · +10 XP">
                          <span class="srs-act-text-desk">🌱 Откроется после 3 шагов теории (+10&nbsp;XP)</span>
                          <span class="srs-act-text-mob">🌱 Откроется после 3 шагов (+10&nbsp;XP)</span>
                        </span>
                      </div>`'''

new_srs = '''                      <div style="display:flex;align-items:center;gap:6px;padding:6px 2px 0;font-size:.74rem;">
                        <span style="color:var(--ink-muted);font-size:.74rem;display:inline-flex;align-items:center;gap:5px;" title="🌱 ${theoryDoneCount === 0 ? 'Откроется после 3 шагов теории · +10 XP' : `До открытия: ${remainingSteps} ${stepsText} · +10 XP`}">
                          <span class="srs-act-text-desk">${theoryDoneCount === 0 ? '🌱 Откроется после 3 шагов теории (+10&nbsp;XP)' : `🌱 До открытия: ${remainingSteps}&nbsp;${stepsText} (+10&nbsp;XP)`}</span>
                          <span class="srs-act-text-mob">${theoryDoneCount === 0 ? '🌱 Откроется после 3 шагов (+10&nbsp;XP)' : `🌱 До открытия: ${remainingSteps}&nbsp;${stepsText} (+10&nbsp;XP)`}</span>
                        </span>
                      </div>`'''

if old_srs not in content:
    print('ERROR: old_srs not found in academy.html')
    sys.exit(1)

content = content.replace(old_srs, new_srs, 1)

# Write updated academy.html and synchronize etalons
with open(ACADEMY_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

with open(ETALON_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

with open(ETALONS_FOLDER_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('SUCCESS: academy.html and both etalons updated and synchronized!')

# 5. Bump Service Worker cache in sw.js
with open(SW_PATH, 'r', encoding='utf-8') as f:
    sw_code = f.read()

sw_code = sw_code.replace("const CACHE_NAME = 'academy-pwa-v51';", "const CACHE_NAME = 'academy-pwa-v52';")
sw_code = sw_code.replace("const CACHE_NAME = 'academy-pwa-v50';", "const CACHE_NAME = 'academy-pwa-v52';")

with open(SW_PATH, 'w', encoding='utf-8') as f:
    f.write(sw_code)

print('SUCCESS: sw.js cache bumped to v52!')

# 6. Update tests in test_dashboard_regression.js
with open(TEST_PATH, 'r', encoding='utf-8') as f:
    test_code = f.read()

# Update Bug 138 assertion
test_code = test_code.replace(
    "academyHtml.includes('Тема 1 из ${curUnitTotal} · Старт') &&\n    academyHtml.includes('${curUnitDone === 0 ? `Тема 1 из ${curUnitTotal} · Старт` : `${curUnitDone} из ${curUnitTotal} тем`}')",
    "academyHtml.includes('Тема 1 из ${curUnitTotal}') &&\n    academyHtml.includes('${curUnitDone === 0 ? `Тема 1 из ${curUnitTotal}` : `${curUnitDone} из ${curUnitTotal} тем`}') &&\n    !academyHtml.includes('Тема 1 из ${curUnitTotal} · Старт')"
)

# Add Bug 140
bug140_fn = '''
// 7. Bug 140 (Defect 7): Третья фаза лаконичности дашборда по канону Жадного Дескриптора (Decision 47)
function testBug140_GreedyDescriptorPhaseThreeDashboardPerfection(){
  assert(
    !academyHtml.includes('· Старт`'),
    'Bug 140: redundant "· Старт" pleonasm must be eliminated from echelon topic counter'
  );
  assert(
    academyHtml.includes('Первый шаг продлит серию до 🔥 <b>${currentStreakVal + 1} дн.</b>'),
    'Bug 140: streak hint must follow proper Russian grammar with "до"'
  );
  assert(
    academyHtml.includes('Тех-скрининг'),
    'Bug 140: mobile echelon label must use compact "Тех-скрининг"'
  );
  assert(
    academyHtml.includes('До открытия: ${remainingSteps}&nbsp;${stepsText} (+10&nbsp;XP)'),
    'Bug 140: closed SRS preview must dynamically reflect remaining steps'
  );
  console.log('✓ Bug 140: Greedy Descriptor Phase Three dashboard perfection verified');
}
'''

if 'testBug140_GreedyDescriptorPhaseThreeDashboardPerfection' not in test_code:
    test_code = test_code.replace(
        'testBug139_GreedyDescriptorPhaseTwoDashboardConciseness();',
        'testBug139_GreedyDescriptorPhaseTwoDashboardConciseness();\ntestBug140_GreedyDescriptorPhaseThreeDashboardPerfection();'
    )
    test_code = test_code.replace(
        'console.log(\'  ALL DASHBOARD REGRESSION TESTS (BUGS 134..139) PASSED (100%)  \');',
        'console.log(\'  ALL DASHBOARD REGRESSION TESTS (BUGS 134..140) PASSED (100%)  \');'
    )
    test_code = test_code.replace('testBug134_SingleDominantCtaLabelNo2MinAndContinueFurther();', bug140_fn + '\ntestBug134_SingleDominantCtaLabelNo2MinAndContinueFurther();')

with open(TEST_PATH, 'w', encoding='utf-8') as f:
    f.write(test_code)

print('SUCCESS: test_dashboard_regression.js updated with Bug 140!')
