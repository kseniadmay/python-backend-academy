#!/usr/bin/env node
/**
 * make_baseline_review.js — генерирует scripts/visual_report/baseline_review.html:
 * одна страница со всеми эталонами scripts/visual_baselines/ для визуального
 * утверждения человеком. Запуск: node scripts/make_baseline_review.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

const BASELINE_DIR = path.join(__dirname, 'visual_baselines');
const OUT = path.join(__dirname, 'visual_report', 'baseline_review.html');

const files = fs.readdirSync(BASELINE_DIR).filter(f => f.endsWith('.png')).sort();
const groups = {};
for (const f of files) {
  const base = f.replace(/_(desktop|mobile)\.png$/, '');
  (groups[base] = groups[base] || []).push(f);
}

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
const img = (f, cls) => f
  ? `      <figure class="${cls}"><figcaption>${esc(f)}</figcaption><img src="../visual_baselines/${esc(f)}" loading="lazy"></figure>\n`
  : '';

let html = `<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Утверждение визуальных эталонов — ${files.length} кадров</title>
<style>
body{background:#0d1016;color:#e7e9ee;font-family:Onest,'Segoe UI',sans-serif;margin:0;padding:24px}
h1{font-size:22px}h2{font-size:16px;color:#f59e0b;margin:32px 0 12px;border-bottom:1px solid #262b36;padding-bottom:6px}
.grid{display:flex;flex-wrap:wrap;gap:20px}
figure{margin:0;background:#141821;border:1px solid #262b36;border-radius:10px;padding:10px}
figcaption{font-size:12px;color:#9aa3b2;margin-bottom:8px;font-family:Consolas,monospace}
img{display:block;border-radius:6px;max-width:100%;height:auto}
.desk img{width:720px}.mob img{width:390px}
.hint{color:#9aa3b2;font-size:13px;max-width:900px;line-height:1.5}
</style>
</head>
<body>
<h1>Утверждение визуальных эталонов (${files.length} кадров)</h1>
<p class="hint">Это «нулевая точка»: с этими снимками сравниваются все будущие прогоны visual_test.js (допуск 0.1%).
Если кадр выглядит неправильно — назовите имя файла, эталоны переснимут и закоммитят заново.
Мобильные кадры — 390×844 @2x, десктопные — 1440×900.</p>
`;

for (const [base, fs_] of Object.entries(groups)) {
  const desk = fs_.find(f => f.endsWith('desktop.png'));
  const mob = fs_.find(f => f.endsWith('mobile.png'));
  html += `<h2>${esc(base)}</h2>\n<div class="grid">\n${img(desk, 'desk')}${img(mob, 'mob')}</div>\n`;
}
html += '</body></html>\n';

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, html, 'utf8');
console.log(`OK: ${OUT} — групп ${Object.keys(groups).length}, кадров ${files.length}`);
