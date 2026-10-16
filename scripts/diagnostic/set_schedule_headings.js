/**
 * Скрипт для RemNote: расстановка заголовков H1 (недели), H2 (дни), H3 (тема/секции дня).
 * 
 * Правила и структура:
 * - Недели: Заголовок 1 уровня (H1)
 * - Дни: Заголовок 2 уровня (H2)
 * - Тема дня (секции "Теория дня", "Вечерний кодинг", "Чек-лист"): Заголовок 3 уровня (H3)
 *
 * Среда: Node.js (встроенный модуль node:sqlite)
 * Соответствует регламенту remnote-sync:
 * - Прямая работа с SQLite базой remnote.db в транзакции
 * - Корректные поля u, p, tp, apu, ps, bpc
 * - Откат lastSync в таблице sync2.quanta для чистой синхронизации с RemNote Cloud
 * - PRAGMA wal_checkpoint(FULL)
 * - Десктопный клиент RemNote.exe НЕ запускается
 */

const { DatabaseSync } = require('node:sqlite');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 1. Поиск базы данных
const DEFAULT_DB_PATH = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const dbPath = process.argv[2] || DEFAULT_DB_PATH;

if (!fs.existsSync(dbPath)) {
  console.error(`❌ База данных RemNote не найдена по пути: ${dbPath}`);
  process.exit(1);
}

// 2. Проверка запущенных процессов RemNote.exe (по регламенту десктоп запрещен)
try {
  const tasklist = execSync('tasklist', { encoding: 'utf8' });
  if (tasklist.toLowerCase().includes('remnote.exe')) {
    console.log('⚠️ Обнаружен запущенный процесс RemNote.exe. Завершаем перед записью в SQLite...');
    execSync('taskkill /F /IM RemNote.exe', { stdio: 'ignore' });
  }
} catch (e) {
  // Игнорируем ошибки проверки процессов
}

const db = new DatabaseSync(dbPath, { open: true });

// Идентификаторы структуры расписания
const ROOT_DOC_ID = 'HKILo3FLoxkwXggHD';
const HEADER_POWERUP_ID = 'NJMkj3YuMydmWUx02'; // Системный Powerup "Заголовок" (rcrt: r)

const WEEKS = [
  { id: 'woi7lmQesvLXOwKfk', num: 1 },
  { id: 'wXwSfI7PMK0xZ6WKv', num: 2 },
  { id: 'wRKo2afWo8mhdqhf6', num: 3 },
  { id: 'w0irf7AlORpYbDsKP', num: 4 },
  { id: 'wmOOjohySF0mb8DYU', num: 5 },
  { id: 'wscAWAuAmrmNYAtLx', num: 6 }
];

/**
 * Установка уровня заголовка для объекта Rem в формате RemNote
 * @param {object} doc - JSON-объект документа
 * @param {'H1'|'H2'|'H3'|null} level - уровень заголовка
 * @param {number} nowTs - текущий таймстемп
 */
function setHeading(doc, level, nowTs) {
  if (!level) {
    if (doc.tp && doc.tp[HEADER_POWERUP_ID]) {
      delete doc.tp[HEADER_POWERUP_ID];
      doc['tp,u'] = nowTs;
    }
    if (doc.apu && doc.apu.r) {
      delete doc.apu.r;
      doc['apu,u'] = nowTs;
    }
    if (doc.ps && doc.ps.r_s) {
      delete doc.ps.r_s;
      doc['ps,u'] = nowTs;
    }
    if (doc.bpc && doc.bpc.r) {
      delete doc.bpc.r;
      doc['bpc,u'] = nowTs;
    }
  } else {
    // Включаем powerup заголовка
    doc.tp = doc.tp || {};
    doc.tp[HEADER_POWERUP_ID] = { t: false, ",u": nowTs };
    doc['tp,u'] = nowTs;

    // Включаем активный powerup в apu
    doc.apu = doc.apu || {};
    doc.apu.r = { v: true, ",u": nowTs };
    doc['apu,u'] = nowTs;

    // Задаем размер заголовка в ps.r_s
    doc.ps = doc.ps || {};
    doc.ps.r_s = {
      v: {
        v: [level],
        s: level
      },
      ",u": nowTs
    };
    doc['ps,u'] = nowTs;

    // Задаем bpc для полной обратной совместимости
    doc.bpc = doc.bpc || {};
    doc.bpc.r = {
      s: {
        v: [{ i: "q" }],
        s: level
      }
    };
    doc['bpc,u'] = nowTs;
  }

  // Метки изменения документа для облачной синхронизации
  doc.u = nowTs;
  doc.p = nowTs;
}

function getText(key) {
  if (!key) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) {
    return key.map(p => (typeof p === 'string' ? p : (p.text || ''))).join('');
  }
  return '';
}

const nowTs = Date.now();
console.log(`\n🚀 Запуск расстановки заголовков в RemNote (ts=${nowTs})...`);

db.exec('BEGIN TRANSACTION;');

try {
  let weeksCount = 0;
  let daysCount = 0;
  let topicsCount = 0;

  // 1. Проверяем корень расписания
  const rootRow = db.prepare("SELECT doc FROM quanta WHERE _id = ?").get(ROOT_DOC_ID);
  if (!rootRow) {
    throw new Error(`Корневой документ расписания не найден: ${ROOT_DOC_ID}`);
  }

  for (const weekInfo of WEEKS) {
    const weekRow = db.prepare("SELECT doc FROM quanta WHERE _id = ?").get(weekInfo.id);
    if (!weekRow) {
      console.warn(`⚠️ Неделя ${weekInfo.num} (${weekInfo.id}) не найдена в базе`);
      continue;
    }

    // Присваиваем Неделе заголовок 1 уровня (H1)
    const weekDoc = JSON.parse(weekRow.doc);
    setHeading(weekDoc, 'H1', nowTs);
    db.prepare("UPDATE quanta SET doc = ? WHERE _id = ?").run(JSON.stringify(weekDoc), weekInfo.id);
    weeksCount++;
    console.log(`📌 [H1] Неделя ${weekInfo.num}: "${getText(weekDoc.key).slice(0, 50)}..."`);

    // Получаем дни недели (из поля children или по parent)
    let dayIds = weekDoc.children || [];
    if (dayIds.length === 0) {
      const dayRows = db.prepare("SELECT _id FROM quanta WHERE doc LIKE ?").all(`%"parent":"${weekInfo.id}"%`);
      dayIds = dayRows.map(r => r._id);
    }

    for (const dayId of dayIds) {
      const dayRow = db.prepare("SELECT doc FROM quanta WHERE _id = ?").get(dayId);
      if (!dayRow) continue;

      // Присваиваем Дню заголовок 2 уровня (H2)
      const dayDoc = JSON.parse(dayRow.doc);
      setHeading(dayDoc, 'H2', nowTs);
      db.prepare("UPDATE quanta SET doc = ? WHERE _id = ?").run(JSON.stringify(dayDoc), dayId);
      daysCount++;

      // Получаем подсекции дня (Теория дня, Вечерний кодинг, Чек-лист)
      const subSections = db.prepare("SELECT _id, doc FROM quanta WHERE doc LIKE ?").all(`%"parent":"${dayId}"%`);
      for (const sub of subSections) {
        const subDoc = JSON.parse(sub.doc);
        const title = getText(subDoc.key);

        // Присваиваем теме/секциям дня заголовок 3 уровня (H3)
        setHeading(subDoc, 'H3', nowTs);
        db.prepare("UPDATE quanta SET doc = ? WHERE _id = ?").run(JSON.stringify(subDoc), sub._id);
        topicsCount++;
      }
    }
  }

  // 2. Откатываем lastSync в sync2.quanta для принудительной синхронизации правок в RemNote Cloud
  const syncRow = db.prepare("SELECT doc FROM sync2 WHERE _id = 'quanta'").get();
  if (syncRow) {
    const syncDoc = JSON.parse(syncRow.doc);
    syncDoc.lastSync = nowTs - 2000;
    syncDoc.lastSyncFullBatchDoneTime = nowTs - 2000;
    db.prepare("UPDATE sync2 SET doc = ? WHERE _id = 'quanta'").run(JSON.stringify(syncDoc));
    console.log(`🔄 Откачен sync2.quanta lastSync на ${nowTs - 2000} (для синхронизации с облаком).`);
  }

  db.exec('COMMIT;');
  console.log(`\n✅ Транзакция успешно зафиксирована (COMMIT).`);
  console.log(`📊 Итоги расстановки:`);
  console.log(`   - Недели (H1): ${weeksCount}`);
  console.log(`   - Дни (H2):    ${daysCount}`);
  console.log(`   - Секции/Темы дня (H3): ${topicsCount}`);

  // 3. Выполняем PRAGMA wal_checkpoint(FULL)
  const walRes = db.prepare('PRAGMA wal_checkpoint(FULL);').get();
  console.log(`💾 Чекпоинт WAL:`, walRes);

} catch (err) {
  db.exec('ROLLBACK;');
  console.error('❌ Ошибка при обновлении RemNote, выполнен откат транзакции (ROLLBACK):', err);
  process.exit(1);
}
