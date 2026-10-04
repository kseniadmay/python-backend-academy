const fs = require('fs');
const raw = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\sections_raw.json', 'utf8'));
const daysMap = raw.dayMap;

// Find sections whose day was null
const mapping = JSON.parse(fs.readFileSync('C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\section_to_day_mapping.json', 'utf8'));
for (const [id, m] of Object.entries(mapping.taskSectionMapping)) {
  if (m.day === null) {
    console.log(`Unmapped task sec [${id}] (${m.kidsCount} kids): "${m.text}"`);
    const sec = raw.taskSections.find(x => x.id === id);
    if (sec) {
      console.log('  sample kids:', sec.kidsText.slice(0, 3));
    }
  }
}