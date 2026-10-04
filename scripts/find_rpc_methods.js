const fs = require('fs');

const content = fs.readFileSync('C:\\Projects\\remnote-plugin-template-react\\node_modules\\@remnote\\plugin-sdk\\dist\\lib.js', 'utf8');

// Find occurrences of card methods
const re = /call\("card\.([^"]+)"/g;
let m;
const methods = new Set();
while ((m = re.exec(content)) !== null) {
  methods.add(m[1]);
}
console.log('Methods on card namespace:', Array.from(methods));

// Find occurrences of rem methods
const reRem = /call\("rem\.([^"]+)"/g;
const remMethods = new Set();
while ((m = reRem.exec(content)) !== null) {
  remMethods.add(m[1]);
}
console.log('Methods on rem namespace count:', remMethods.size);
console.log('Card related rem methods:', Array.from(remMethods).filter(x => x.toLowerCase().includes('card')));
