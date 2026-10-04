const fs = require('fs');

const localFile = fs.readFileSync('C:\\Users\\fury6\\Downloads\\Расписание подготовки Junior+ Python Backend Developer.md', 'utf8');
const lines = localFile.split(/\r?\n/);

const localDays = [];
let curDay = null;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  const m = line.match(/^###\s*(.*День\s*0?(\d+).*)$/);
  if (m) {
    if (curDay) localDays.push(curDay);
    const dNum = parseInt(m[2]);
    curDay = {
      num: dNum,
      rawTitle: m[1].replace(/^\*\*/, '').replace(/\*\*$/, '').trim(),
      lineIdx: i,
      topic: '',
      lines: []
    };
  } else if (curDay) {
    curDay.lines.push(line);
  }
}
if (curDay) localDays.push(curDay);

console.log(`Local file has ${localDays.length} days:`);
localDays.forEach(d => {
  console.log(`Day ${d.num < 10 ? '0' + d.num : d.num}: "${d.rawTitle}"`);
});
