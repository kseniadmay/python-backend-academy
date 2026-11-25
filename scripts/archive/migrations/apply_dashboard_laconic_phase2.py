import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
academy_path = os.path.join(root, 'academy.html')

with open(academy_path, 'r', encoding='utf-8') as f:
    content = f.read()

print('Initial academy.html length:', len(content))

# 1. Streamline Echelon Topbar: remove redundant subrow (0 XP badge) and foot-desc, keep briefing button and tier title
old_topbar = """      <!-- Зона 1: Шапка Эшелона (.echelon-topbar-clean) -->
      <div class="echelon-topbar-clean" style="padding:16px 20px;border-radius:20px;margin-bottom:18px;display:flex;flex-direction:column;gap:12px;background:rgba(18, 22, 31, 0.65);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);border:1px solid rgba(255, 255, 255, 0.08);box-shadow:var(--shadow-1);">
        <!-- Ряд 1: Звание слева, аудио-компаньон и кнопка «Справка» справа -->
        <div class="echelon-topbar-row-top" style="display: flex; justify-content: space-between; align-items: center; width: 100%; gap: 10px;">
          <h1 class="rank-title-glow echelon-bordeaux-title" style="margin:0;font-size:1.32rem;">${readinessRank}</h1>
          <div class="echelon-topbar-actions" style="display:inline-flex;align-items:center;gap:8px;flex-shrink:0;">
            <button class="topbar-audio-btn btn btn-ghost-quiet" id="dashAudioCompanionBtn" title="Голосовой брифинг Сократа" aria-label="Голосовой наставник Сократ" style="padding:6px 10px;border-radius:10px;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;justify-content:center;gap:5px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.12);backdrop-filter:blur(12px);color:var(--ink-muted);cursor:pointer;transition:all .2s ease;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:block;flex-shrink:0;">
                <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
                <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
              </svg>
              <span class="topbar-audio-text">Брифинг</span>
            </button>
            <a href="#/docs" class="topbar-help-btn btn btn-ghost-quiet" style="padding:6px 10px;border-radius:10px;text-decoration:none;font-size:.82rem;font-weight:600;display:inline-flex;align-items:center;justify-content:center;gap:5px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.12);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);color:var(--ink-muted);flex-shrink:0;" title="Информация и критерии грейда" aria-label="Информация и критерии грейда">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:block;flex-shrink:0;"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
              <span class="topbar-help-text">О модуле</span>
            </a>
          </div>
        </div>

        <!-- Ряд 2: Чистая строка суточного прогресс-бейджа XP и эшелона -->
        <div class="echelon-topbar-subrow" style="display:flex;align-items:center;justify-content:space-between;width:100%;">
          <div class="echelon-subrow-xp" style="display:flex;align-items:center;min-width:0;">
            ${todayXp() === 0
              ? `<span class="day-xp-badge empty-day-badge" style="background:rgba(245, 158, 11, 0.10);border:1px solid rgba(245, 158, 11, 0.28);color:#fbbf24;white-space:nowrap;display:inline-flex;align-items:center;" title="Сделайте первый шаг дня: +15 XP">⚡ 0&nbsp;XP за сутки</span>`
              : `<span class="day-xp-badge" style="white-space:nowrap;" title="Заработано за сутки: ${tXp} XP">⚡ +${todayXp()}&nbsp;XP за сутки</span>`
            }
          </div>
          <span class="meta" style="font-size:.74rem;color:var(--ink-muted);white-space:nowrap;margin-left:auto;">Эшелон 1 · Фундамент</span>
        </div>

        <!-- Прогресс эшелона -->
        <div class="echelon-clean-wrap" style="width:100%;" title="Готовность к 1-му тех-скринингу">
          <div class="echelon-clean-meta" style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:nowrap;margin-bottom:6px;">
            ${e1CurMp === 0
              ? `<span class="echelon-readiness-emerald" style="font-weight:700;font-size:.84rem;flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                  <span class="echelon-label-full">Готовность к тех-скринингу</span>
                  <span class="echelon-label-mobile">Готовность к тех-скринингу</span>
                </span>
                <span class="meta echelon-mp-counter" style="font-size:.74rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 7px;border-radius:6px;white-space:nowrap;flex-shrink:0;">Тема 1 из ${curUnitTotal} · Старт</span>`
              : `<span class="echelon-readiness-emerald" style="font-weight:700;font-size:.84rem;flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                  <span class="echelon-label-full">Готовность к тех-скринингу: ${e1Pct}%</span>
                  <span class="echelon-label-mobile">Готовность к тех-скринингу: ${e1Pct}%</span>
                </span>
                <span class="meta echelon-mp-counter" style="font-size:.74rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:2px 7px;border-radius:6px;white-space:nowrap;flex-shrink:0;">${curUnitDone === 0 ? `Тема 1 из ${curUnitTotal} · Старт` : `${curUnitDone} из ${curUnitTotal} тем`}</span>`
            }
          </div>
          <div class="echelon-clean-track ${e1CurMp === 0 ? 'is-zero' : ''}" style="height:8px;border-radius:999px;position:relative;box-shadow:inset 0 1px 2px rgba(0,0,0,0.4);${e1CurMp === 0 ? 'background:rgba(255, 255, 255, 0.06);' : 'background:rgba(255,255,255,0.08);'}">
            ${e1CurMp === 0
              ? `<div class="echelon-clean-fill" style="width:0%;"></div>`
              : `<div class="echelon-clean-fill" style="width:${e1Pct}%;height:100%;border-radius:999px;background:linear-gradient(90deg, #059669 0%, #10b981 50%, #34d399 100%);box-shadow:0 0 12px rgba(16,185,129,0.5);transition:width .35s ease;"></div>`
            }
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:.76rem;color:#94a3b8;margin-top:6px;">
            <span style="color:#94a3b8;min-width:0;">
              <span class="echelon-foot-desc-desk">Допуск к первому скринингу</span>
              <span class="echelon-foot-desc-mob">Допуск к первому скринингу</span>
            </span>
            <span style="font-weight:700;font-size:.74rem;color:${e1CurMp === 0 ? '#34d399' : '#34d399'};white-space:nowrap;flex-shrink:0;">${e1CurMp === 0 ? 'Старт 🚀' : 'Цель: 100% 🎯'}</span>
          </div>
        </div>
      </div>"""

new_topbar = """      <!-- Зона 1: Шапка Эшелона (.echelon-topbar-clean) -->
      <div class="echelon-topbar-clean" style="padding:14px 18px;border-radius:18px;margin-bottom:14px;display:flex;flex-direction:column;gap:10px;background:rgba(18, 22, 31, 0.65);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);border:1px solid rgba(255, 255, 255, 0.08);box-shadow:var(--shadow-1);">
        <!-- Ряд 1: Звание и эшелон слева, аудио-компаньон справа -->
        <div class="echelon-topbar-row-top" style="display:flex;justify-content:space-between;align-items:center;width:100%;gap:10px;">
          <div style="display:flex;align-items:baseline;gap:10px;min-width:0;flex-wrap:wrap;">
            <h1 class="rank-title-glow echelon-bordeaux-title" style="margin:0;font-size:1.24rem;">${readinessRank}</h1>
            <span class="meta echelon-tier-tag" style="font-size:.74rem;color:var(--ink-muted);white-space:nowrap;">Эшелон 1 · Фундамент</span>
          </div>
          <div class="echelon-topbar-actions" style="display:inline-flex;align-items:center;gap:8px;flex-shrink:0;">
            <button class="topbar-audio-btn btn btn-ghost-quiet" id="dashAudioCompanionBtn" title="Голосовой брифинг Сократа" aria-label="Голосовой наставник Сократ" style="padding:5px 10px;border-radius:10px;font-size:.80rem;font-weight:600;display:inline-flex;align-items:center;justify-content:center;gap:5px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.12);backdrop-filter:blur(12px);color:var(--ink-muted);cursor:pointer;transition:all .2s ease;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:block;flex-shrink:0;">
                <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
                <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
              </svg>
              <span class="topbar-audio-text">Брифинг</span>
            </button>
          </div>
        </div>

        <!-- Прогресс эшелона: лаконичный трек с чистым заголовком -->
        <div class="echelon-clean-wrap" style="width:100%;" title="Готовность к 1-му тех-скринингу">
          <div class="echelon-clean-meta" style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:nowrap;margin-bottom:6px;">
            ${e1CurMp === 0
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
            }
          </div>
          <div class="echelon-clean-track ${e1CurMp === 0 ? 'is-zero' : ''}" style="height:6px;border-radius:999px;position:relative;box-shadow:inset 0 1px 2px rgba(0,0,0,0.4);${e1CurMp === 0 ? 'background:rgba(255, 255, 255, 0.06);' : 'background:rgba(255,255,255,0.08);'}">
            ${e1CurMp === 0
              ? `<div class="echelon-clean-fill" style="width:0%;"></div>`
              : `<div class="echelon-clean-fill" style="width:${e1Pct}%;height:100%;border-radius:999px;background:linear-gradient(90deg, #059669 0%, #10b981 50%, #34d399 100%);box-shadow:0 0 12px rgba(16,185,129,0.5);transition:width .35s ease;"></div>`
            }
          </div>
        </div>
      </div>"""

assert old_topbar in content, 'Target old_topbar not found'
content = content.replace(old_topbar, new_topbar, 1)
print('1. [PASS] Streamlined Echelon Topbar applied')

# 2. Streamlined SRS zero state: compact preview with clean single padlock and counter
old_srs_zero = """                : (!hasReviewedAnyCard
                    ? `<div style="display:flex;flex-direction:column;gap:8px;width:100%;">
                          <div class="srs-clean-preview" style="display:flex;align-items:center;justify-content:space-between;gap:8px;padding:8px 12px;border-radius:10px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);cursor:pointer;transition:transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease;" title="Нажмите, чтобы узнать условие открытия колоды" onclick="showToast('Пройдите первые 3 шага теории, чтобы открыть флеш-колоду темы (+10 XP)', 'info');">
                            <div style="display:flex;align-items:center;gap:7px;min-width:0;flex:1 1 auto;">
                              <span style="display:inline-flex;align-items:center;gap:4px;color:var(--ink-muted);opacity:0.85;">
                                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;flex-shrink:0;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;flex-shrink:0;"><rect x="3" y="6" width="14" height="15" rx="2"></rect><path d="M7 2h12a2 2 0 0 1 2 2v13"></path></svg>
                              </span>
                              <span style="font-weight:600;color:var(--ink);font-size:0.78rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                                ${escapeHtmlStr(cleanTitle)}
                              </span>
                            </div>
                          </div>
                          <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;padding:4px 4px 0;font-size:.74rem;">
                            <span style="color:var(--ink-muted);font-size:.74rem;display:inline-flex;align-items:center;gap:5px;" title="🌱 Откроется после 3 шагов теории · +10 XP">
                              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--emerald)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;flex-shrink:0;filter:drop-shadow(0 0 4px rgba(16,185,129,0.5));"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path></svg>
                              <span class="srs-act-text-desk">Откроется после 3 шагов теории (+10&nbsp;XP)</span>
                              <span class="srs-act-text-mob">Откроется после 3 шагов (+10&nbsp;XP)</span>
                            </span>
                            <div style="display:flex;align-items:center;gap:6px;background:rgba(255,255,255,0.03);padding:2px 8px;border-radius:6px;border:1px solid rgba(255,255,255,0.06);">
                              <span style="font-size:0.70rem;color:var(--ink-muted);">${theoryDoneCount}/3</span>
                              <span style="display:inline-flex;gap:4px;align-items:center;">
                                <span style="width:6px;height:6px;border-radius:50%;background:${theoryDoneCount >= 1 ? '#10b981' : 'rgba(255,255,255,0.18)'};${theoryDoneCount >= 1 ? 'box-shadow:0 0 6px rgba(16,185,129,0.7);' : ''}"></span>
                                <span style="width:6px;height:6px;border-radius:50%;background:${theoryDoneCount >= 2 ? '#10b981' : 'rgba(255,255,255,0.18)'};${theoryDoneCount >= 2 ? 'box-shadow:0 0 6px rgba(16,185,129,0.7);' : ''}"></span>
                                <span style="width:6px;height:6px;border-radius:50%;background:${theoryDoneCount >= 3 ? '#10b981' : 'rgba(255,255,255,0.18)'};${theoryDoneCount >= 3 ? 'box-shadow:0 0 6px rgba(16,185,129,0.7);' : ''}"></span>
                              </span>
                            </div>
                          </div>
                        </div>`"""

new_srs_zero = """                : (!hasReviewedAnyCard
                    ? `<div class="srs-clean-preview" style="display:flex;align-items:center;justify-content:space-between;gap:8px;padding:8px 12px;border-radius:10px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);cursor:pointer;transition:transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease;" title="Нажмите, чтобы узнать условие открытия колоды" onclick="showToast('Пройдите первые 3 шага теории, чтобы открыть флеш-колоду темы (+10 XP)', 'info');">
                        <div style="display:flex;align-items:center;gap:7px;min-width:0;flex:1 1 auto;">
                          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;flex-shrink:0;color:var(--ink-muted);"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                          <span style="font-weight:600;color:var(--ink);font-size:0.78rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                            ${escapeHtmlStr(cleanTitle)}
                          </span>
                        </div>
                        <div style="display:flex;align-items:center;gap:6px;background:rgba(255,255,255,0.03);padding:2px 8px;border-radius:6px;border:1px solid rgba(255,255,255,0.06);flex-shrink:0;">
                          <span style="font-size:0.70rem;color:var(--ink-muted);">${theoryDoneCount}/3</span>
                          <span style="display:inline-flex;gap:4px;align-items:center;">
                            <span style="width:6px;height:6px;border-radius:50%;background:${theoryDoneCount >= 1 ? '#10b981' : 'rgba(255,255,255,0.18)'};${theoryDoneCount >= 1 ? 'box-shadow:0 0 6px rgba(16,185,129,0.7);' : ''}"></span>
                            <span style="width:6px;height:6px;border-radius:50%;background:${theoryDoneCount >= 2 ? '#10b981' : 'rgba(255,255,255,0.18)'};${theoryDoneCount >= 2 ? 'box-shadow:0 0 6px rgba(16,185,129,0.7);' : ''}"></span>
                            <span style="width:6px;height:6px;border-radius:50%;background:${theoryDoneCount >= 3 ? '#10b981' : 'rgba(255,255,255,0.18)'};${theoryDoneCount >= 3 ? 'box-shadow:0 0 6px rgba(16,185,129,0.7);' : ''}"></span>
                          </span>
                        </div>
                      </div>
                      <div style="display:flex;align-items:center;gap:6px;padding:6px 2px 0;font-size:.74rem;">
                        <span style="color:var(--ink-muted);font-size:.74rem;display:inline-flex;align-items:center;gap:5px;" title="🌱 Откроется после 3 шагов теории · +10 XP">
                          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--emerald)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:-1px;flex-shrink:0;filter:drop-shadow(0 0 4px rgba(16,185,129,0.5));"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path></svg>
                          <span class="srs-act-text-desk">🌱 Откроется после 3 шагов теории (+10&nbsp;XP)</span>
                          <span class="srs-act-text-mob">🌱 Откроется после 3 шагов (+10&nbsp;XP)</span>
                        </span>
                      </div>`"""

assert old_srs_zero in content, 'Target old_srs_zero not found'
content = content.replace(old_srs_zero, new_srs_zero, 1)
print('2. [PASS] Streamlined SRS zero state applied')

with open(academy_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated academy.html successfully. New length:', len(content))

# Byte-for-byte sync to etalons
etalon_path = os.path.join(root, 'Эталоны', 'Эталоны.html')
root_etalon = os.path.join(root, 'Эталоны.html')
shutil.copy2(academy_path, etalon_path)
shutil.copy2(academy_path, root_etalon)
print('Synchronized Эталоны/Эталоны.html and Эталоны.html')
