const fs = require('fs');

const content = fs.readFileSync('C:\\Projects\\remnote-plugin-template-react\\node_modules\\@remnote\\plugin-sdk\\dist\\lib.js', 'utf8');

const idx = content.indexOf('class rs extends');
if (idx !== -1) {
  console.log('class rs:');
  console.log(content.slice(idx, idx + 600));
}

const idxZt = content.indexOf('class zt extends');
if (idxZt !== -1) {
  console.log('class zt:');
  console.log(content.slice(idxZt, idxZt + 800));
}
