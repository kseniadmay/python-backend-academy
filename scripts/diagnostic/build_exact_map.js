const fs = require('fs');
const assign = JSON.parse(fs.readFileSync('clean_assignment.json', 'utf8'));

const dayIds = [
  'zpZwfS8TMSFhDlY1V', 'Tlykz8LNU7L8MFEI7', 'j3gd3N4j8MjMlrBTY', 'yNs77PwLpXvimCex0', 'lWJugKYIPB9JtgZxO', 'SZAGTXB0Rxs2nCtD3', 'Zr08REWGATxtsCUoY',
  'fbL4LiZvo1PDwiBEj', 'ppd8NHQHoTgTE552K', 'oyFb7yfEOKkWBIlm5', 'gfnEh1wcSzO1ZU8NP', 'WljuLIF8qPcA9IXbg', 'EM4s6fVZGPjYRS8pb', 't4tkDifkEZGZhSV7X',
  'oH5QTJDcYyjDQfPvo', 'fpAHeY4xRuviHrsEE', 'kZ3hlbdT1QwNrz0xv', 'x611HlnEPTB0QGabA', 'uMIjvWelpMjEohZpH', 't5mpC1g0mPOVo9kzp', 'c2mpprEZRTzKRJwWn',
  'sc8pMIDZUZ3JoNsYR', 'zRrjnju5ZmhH6HogD', 'lkjmeKwTMawPo2Vo7', 'kL3n0A1Ww7xlxbP6Y', 'qQDlTL8Ra5t2Hhjvd', 'UpV34wp6QwELIPdco', '9CSqUag62ySNRpVbK',
  'YuolGnT0UPnRxXAM2', 'oPp4cGj5MNG8I8EMN', 'q9MKCl1DQo6SqIgwG', 'onYLmCchqenutnGVo', 'SnkUjtJDZ1mGZ0n3Q', 'mwL47zmz9JetWGNNI', 'Sa2NV96RJQCer4jVy',
  'mBvNesvAnxFsgX82o', 'bseL7eBWfNy0psKfO', 'mAgZP2MeGn5mTgMJx', 'uG3ClSF3mxA14cpo7', 'mfRO92pr9UFPWIWe7', 'XgtGkGyoesdbADs0P', 'sp4zr5SUUNylcnzZC'
];

const exactMap = assign.map((a, idx) => ({
  dayNum: a.dayNum,
  weekNum: a.weekNum,
  dayId: dayIds[idx],
  theoryId: a.theory ? a.theory.id : null,
  codingId: a.coding ? a.coding.id : null,
  checklistId: a.checklist ? a.checklist.id : null,
  standoutId: a.standout ? a.standout.id : null
}));

fs.writeFileSync('exact_42_days_map.json', JSON.stringify(exactMap, null, 2), 'utf8');

console.log('Verified exact 42 days mapping:');
exactMap.forEach(m => {
  const d = m.dayNum < 10 ? '0' + m.dayNum : m.dayNum;
  console.log(`Day ${d} [${m.dayId}]: T=${m.theoryId} | C=${m.codingId} | Ch=${m.checklistId || '-'} | St=${m.standoutId || '-'}`);
});
