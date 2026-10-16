const fs = require('fs');

const ast = JSON.parse(fs.readFileSync('local_file_ast.json', 'utf8'));
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));
const exactMap = JSON.parse(fs.readFileSync('exact_42_days_map.json', 'utf8'));

const remById = new Map();
allRems.forEach(r => remById.set(r._id, r));

function resolveFullText(key, depth = 0) {
  if (!key || depth > 3) return '';
  if (typeof key === 'string') return key;
  if (Array.isArray(key)) {
    return key.map(part => {
      if (typeof part === 'string') return part;
      if (part && typeof part === 'object') {
        if (part.text) return part.text;
        if (part.textOfDeletedRem) return part.textOfDeletedRem.join(' ');
        if (part.i === 'q' && part._id) {
          const target = remById.get(part._id);
          if (target) return resolveFullText(target.key, depth + 1);
        }
      }
      return '';
    }).join('');
  }
  return '';
}

function norm(s) {
  return (s || '').toLowerCase().replace(/[^a-zа-яё0-9]/gi, ' ').replace(/\s+/g, ' ').trim();
}

// Map day IDs
const dayMap = {};
exactMap.forEach(m => {
  dayMap[m.dayNum] = m.dayId;
});

// Topic map
const topicMap = {
  1: '31DthKFeDUSFy8kIf',
  2: '9KxSKro6nlcoZCCBl',
  3: '0IpA4W3iyh9beq2Lh',
  4: 'K7J5Um8xr3O9heMxv',
  8: 'AF7cK0oKUkcbdDR5Z',
  9: '1N3Socza2f94IRoE7',
  10: 'WTbFgiLCgSV8e2dnM',
  11: 'JDHEgCaLJVcaFr6is',
  12: 'phwIImGVeXttAUYbA',
  13: 'bKQUp0bNb8cGiR7dr',
  15: '0jnGYoC4LMlS3P7ON',
  16: '5rkqcmMAyUbN0Vke8',
  17: 'eTrJWkIVfPITVMoj3',
  18: 't1o58b5THG5vNSk9e',
  19: '5sEstc4mdKN7snoYP',
  20: 'VQXkbYN5T2BxFrduz',
  22: 'UXutSmCbGvgUzVro7',
  23: 'SxOTF6YHeTDvMCPs7',
  24: 'ItFWzl1GPSQTj5ZRj',
  25: 'pFqVPTMSofWEKJ2Oh',
  26: 'CeEHOA7zOu4eXEqj5',
  27: 'GbaXHnwGsSSc2ZNhQ',
  29: 'q7aXpevG2kiUKso1V',
  30: '1ROIV9i19u72vTJ53',
  31: 'Hw3wSc2uAA72QttKW',
  32: '22z7fvTiWF6fncggu',
  33: 'PpGxSbpK9Sx1hsGTU',
  34: 'IqO2rjYVySNwkPM59',
  36: 'cdDFn7vCzjjSdTUn7',
  37: '1JcnnCZd8qEAC0raX',
  38: 'An5a4v3ArfqIdEobr',
  39: '61qPBRQJFa1jZUl86',
  40: 'wfiThaYeDbVnPErjI',
  41: 'E8NC56N8tFfJL4FeN'
};

// Build complete plan of updates
const updates = [];

// 1. Rules under "Как читать это расписание" (3wGp1954eti6HY9Ej)
const ruleIds = ['sg4EKHSyf5ljrsA1A', '6VkE0AEt18JPo4scJ', 'KZyRktW0PRU4efS4k', '3AluFrydbWIHwuzDg'];
ruleIds.forEach((rId, idx) => {
  updates.push({
    id: rId,
    update: { $set: { parent: '3wGp1954eti6HY9Ej', f: 'a' + (idx + 1) } },
    desc: `Rule ${idx + 1}`
  });
});

// 2. TOC under "🗂️ Оглавление" (sKMQGofj7WYX3gsrt)
const tocIds = [
  'Tjh5dy8ht48Box2te', // Week 1
  'EwBSIwFkVhKgGf0ia', // Week 2
  'PbOCjt2aRSZt6ZvwU', // Week 3
  'agUOhBd0lYhBQWDFp', // Week 4
  'NIgtLiD1MkLn2rMM5', // Week 5
  '1nEwuP2BzBvf6d4y0', // Week 6
  'jRuK0K3l0m2WSaDEr'  // Day 42
];
tocIds.forEach((tId, idx) => {
  updates.push({
    id: tId,
    update: { $set: { parent: 'sKMQGofj7WYX3gsrt', f: 'a' + (idx + 1) } },
    desc: `TOC item ${idx + 1}`
  });
});

// 3. For each of 42 days:
ast.weeks.forEach(w => {
  w.days.forEach(d => {
    const dayId = dayMap[d.num];
    const m = exactMap.find(x => x.dayNum === d.num);
    if (!dayId || !m) return;

    // Update day title cleanly
    updates.push({
      id: dayId,
      update: { $set: { key: [d.title] } },
      desc: `Day ${d.num} title: "${d.title}"`
    });

    // Topic (if day has topic)
    if (topicMap[d.num]) {
      updates.push({
        id: topicMap[d.num],
        update: { $set: { parent: dayId, f: 'a0' } },
        desc: `Day ${d.num} topic`
      });
    }

    // Theory
    if (m.theoryId) {
      updates.push({
        id: m.theoryId,
        update: { $set: { parent: dayId, f: 'a1' } },
        desc: `Day ${d.num} Theory`
      });
    }

    // Coding
    if (m.codingId) {
      updates.push({
        id: m.codingId,
        update: { $set: { parent: dayId, f: 'a2' } },
        desc: `Day ${d.num} Coding`
      });
    }

    // Review days: Standout & Checklist
    if (m.standoutId) {
      updates.push({
        id: m.standoutId,
        update: { $set: { parent: dayId, f: 'a3' } },
        desc: `Day ${d.num} Standout`
      });
    }
    if (m.checklistId) {
      const fVal = m.standoutId ? 'a4' : 'a3';
      updates.push({
        id: m.checklistId,
        update: { $set: { parent: dayId, f: fVal } },
        desc: `Day ${d.num} Checklist`
      });
    }
  });
});

console.log(`Total structural updates prepared: ${updates.length}`);
fs.writeFileSync('all_structural_updates.json', JSON.stringify(updates, null, 2), 'utf8');
