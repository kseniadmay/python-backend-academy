const fs = require('fs');

const content = fs.readFileSync('C:\\Projects\\remnote-plugin-template-react\\node_modules\\@remnote\\plugin-sdk\\dist\\lib.js', 'utf8');

const idx = content.indexOf('CardNamespace');
if (idx !== -1) {
  console.log('CardNamespace snippet:');
  console.log(content.slice(idx - 100, idx + 400));
}

const idxCard = content.indexOf('class Card ');
if (idxCard !== -1) {
  console.log('class Card snippet:');
  console.log(content.slice(idxCard, idxCard + 500));
}
