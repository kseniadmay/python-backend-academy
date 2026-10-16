const fs = require('fs');
const allRems = JSON.parse(fs.readFileSync('all_rems_dump.json', 'utf8'));

// Find a rem that has a todo checkbox
const todoRem = allRems.find(r => r.apu === true);
console.log('Sample rem with apu:', todoRem);
