# -*- coding: utf-8 -*-
import subprocess
import shutil
import re

with open('mockup_skill_1_1_1.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add CSS for new concepts
extra_css = """
  /* --- НОВЫЕ КОНЦЕПЦИИ НАВИГАЦИИ (БЕЗ ГОРИЗОНТАЛЬНЫХ ТАБОВ) --- */

  /* Концепция 1: Stories Bar в шапке (Zero-Tabs) */
  .sprint-stories-track {
    display: flex;
    gap: 10px;
    align-items: center;
    width: 100%;
    margin-top: 4px;
  }
  .stories-seg {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 3px 0;
    text-align: left;
    transition: transform 0.15s ease;
  }
  .stories-seg:hover {
    transform: translateY(-1px);
  }
  .stories-seg-bar {
    height: 5px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.10);
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }
  .stories-seg-fill {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #10b981, #34d399);
    transition: width 0.3s ease;
  }
  .stories-seg.active .stories-seg-fill {
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
  }
  .stories-seg-txt {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--ink-soft);
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .stories-seg.active .stories-seg-txt {
    color: #fff;
    font-weight: 800;
  }
  .stories-seg.done .stories-seg-txt {
    color: var(--moss);
  }

  /* Концепция 2: Bottom Control Dock */
  .bottom-control-dock {
    position: sticky;
    bottom: 20px;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 10px 16px;
    margin-top: 24px;
    border-radius: 18px;
    background: rgba(13, 16, 22, 0.90);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.5);
  }
  .dock-pill {
    display: flex;
    gap: 4px;
    padding: 3px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.06);
  }
  .dock-btn {
    background: transparent;
    border: none;
    color: var(--ink-soft);
    font-size: 0.78rem;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 9px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .dock-btn:hover {
    color: var(--ink);
  }
  .dock-btn.active {
    background: rgba(16, 185, 129, 0.20);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
  }
  .dock-btn.done {
    color: var(--moss);
  }

  /* Концепция 3: Continuous Flow Header */
  .continuous-step-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 32px 0 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
  .continuous-step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(16, 185, 129, 0.15);
    color: var(--moss);
    border: 1px solid rgba(16, 185, 129, 0.3);
    font-weight: 800;
    font-size: 0.82rem;
  }
  .continuous-step-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: var(--ink);
  }
"""

if '</style>' in html and 'sprint-stories-track' not in html:
    html = html.replace('</style>', extra_css + '\n</style>', 1)

# Add HTML for stories track inside topbar
stories_track_html = """
            <div class="sprint-stories-track" id="stories-track">
              <button class="stories-seg done" id="st-seg-theory" onclick="switchStage('theory')">
                <span class="stories-seg-bar"><span class="stories-seg-fill" id="st-fill-theory" style="width:100%;"></span></span>
                <span class="stories-seg-txt" id="st-txt-theory">1 · Конспект ✓</span>
              </button>
              <button class="stories-seg" id="st-seg-cards" onclick="switchStage('cards')">
                <span class="stories-seg-bar"><span class="stories-seg-fill" id="st-fill-cards" style="width:15%;"></span></span>
                <span class="stories-seg-txt" id="st-txt-cards">2 · Карточки (1/9)</span>
              </button>
              <button class="stories-seg" id="st-seg-code" onclick="switchStage('code')">
                <span class="stories-seg-bar"><span class="stories-seg-fill" id="st-fill-code" style="width:0%;"></span></span>
                <span class="stories-seg-txt" id="st-txt-code">3 · Практика (0/5)</span>
              </button>
            </div>
"""

# Replace the old topbar progress track with stories-track by default
old_track = '<div class="sprint-progress-track">'
if old_track in html and 'id="stories-track"' not in html:
    html = html.replace(old_track, stories_track_html + '\n            <div class="sprint-progress-track" id="default-progress-track" style="display:none;">', 1)

# Add options to the style selector
old_select = '<select id="tab-style-select" onchange="changeTabStyle(this.value)">'
new_select = '''<select id="tab-style-select" onchange="changeTabStyle(this.value)">
                <option value="stories" selected>★ Stories-Header (0 табов)</option>
                <option value="bottomdock">★ Нижний док (Bottom Dock)</option>
                <option value="continuous">★ Сквозной урок (Continuous)</option>
                <option value="underline">Линейный (Underline)</option>
                <option value="stepper">Пошаговый трек (Stepper)</option>
                <option value="milestones">Микро-карточки</option>
                <option value="capsule">Капсула (прежняя)</option>'''

if old_select in html:
    # replace options
    html = re.sub(r'<select id="tab-style-select"[^>]*>.*?</select>', new_select + '\n              </select>', html, flags=re.DOTALL)

# Add Bottom Control Dock right after stages
bottom_dock_html = """
        <!-- НИЖНИЙ ПЛАВАЮЩИЙ ДОК ДЛЯ КОНЦЕПЦИИ 2 -->
        <div id="bottom-control-dock" class="bottom-control-dock" style="display:none;">
          <button class="btn btn-ghost" onclick="prevStageAction()" style="padding:7px 14px;border-radius:12px;">← Назад</button>
          <div class="dock-pill">
            <button class="dock-btn active" id="dock-btn-theory" onclick="switchStage('theory')">📖 Конспект ✓</button>
            <button class="dock-btn" id="dock-btn-cards" onclick="switchStage('cards')">🎴 Карточки (1/9)</button>
            <button class="dock-btn" id="dock-btn-code" onclick="switchStage('code')">💻 Практика (0/5)</button>
          </div>
          <button class="btn btn-primary" onclick="nextStageAction()" id="dock-cta-btn" style="padding:7px 18px;border-radius:12px;background:var(--moss-gradient);box-shadow:var(--shadow-moss);">Понятно, дальше ➔</button>
        </div>
"""

if 'id="bottom-control-dock"' not in html and '<!-- КОНЕЦ СТАДИЙ -->' in html:
    html = html.replace('<!-- КОНЕЦ СТАДИЙ -->', bottom_dock_html + '\n        <!-- КОНЕЦ СТАДИЙ -->')
elif 'id="bottom-control-dock"' not in html:
    html = html.replace('</div>\n    </main>', bottom_dock_html + '\n        </div>\n    </main>')

# Update JavaScript logic in changeTabStyle and switchStage
old_change_func = 'function changeTabStyle(styleName) {'
new_js_logic = """
  let currentNavStyle = 'stories';

  function changeTabStyle(styleName) {
    currentNavStyle = styleName;
    document.querySelectorAll('.tabs-variant-block').forEach(el => el.style.display = 'none');
    const bottomDock = document.getElementById('bottom-control-dock');
    const storiesTrack = document.getElementById('stories-track');
    const defaultTrack = document.getElementById('default-progress-track');

    if(bottomDock) bottomDock.style.display = (styleName === 'bottomdock') ? 'flex' : 'none';

    if(styleName === 'stories') {
      if(storiesTrack) storiesTrack.style.display = 'flex';
      if(defaultTrack) defaultTrack.style.display = 'none';
      // Скрываем все горизонтальные табы напрочь!
    } else if(styleName === 'bottomdock') {
      if(storiesTrack) storiesTrack.style.display = 'none';
      if(defaultTrack) defaultTrack.style.display = 'block';
    } else if(styleName === 'continuous') {
      if(storiesTrack) storiesTrack.style.display = 'flex';
      if(defaultTrack) defaultTrack.style.display = 'none';
      // Показываем все этапы одновременно
      document.querySelectorAll('.stage-view').forEach(el => el.style.display = 'block');
      return;
    } else {
      if(storiesTrack) storiesTrack.style.display = 'none';
      if(defaultTrack) defaultTrack.style.display = 'block';
      const targetBlock = document.getElementById('tabs-variant-' + styleName);
      if(targetBlock) targetBlock.style.display = 'block';
    }

    // Возвращаем изолированный показ текущей стадии
    document.querySelectorAll('.stage-view').forEach(el => el.style.display = 'none');
    const activeStage = document.getElementById('stage-' + curStage);
    if(activeStage) activeStage.style.display = 'block';

    updateAllTabStates(curStage);
  }

  function prevStageAction() {
    if(curStage === 'code') switchStage('cards');
    else if(curStage === 'cards') switchStage('theory');
  }

  function nextStageAction() {
    if(curStage === 'theory') switchStage('cards');
    else if(curStage === 'cards') switchStage('code');
    else alert('Спринт успешно завершен! +30 XP');
  }
"""

if old_change_func in html:
    html = html.replace('function changeTabStyle(styleName) {', new_js_logic + '\n  function oldChangeTabStyle(styleName) {')

with open('mockup_skill_1_1_1.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('design_mockups/mockup_skill_1_1_1.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Mockup HTML updated successfully with new concepts!")
