const fs = require('fs');
const tree = JSON.parse(fs.readFileSync('current_tree.json', 'utf8'));
console.log('Root elements count:', tree.length);
tree.forEach((node, i) => {
  console.log(`[${i}] id=${node.id} f=${node.f} text="${node.text}" (subKids: ${node.subKidsCount})`);
  if (node.subKids && node.subKids.length > 0) {
    node.subKids.forEach((sk, j) => {
      console.log(`   [${j}] id=${sk.id} f=${sk.f} text="${sk.text}" (subSub: ${sk.subSubCount})`);
      if (sk.subSub && sk.subSub.length > 0) {
        sk.subSub.forEach((ssk, k) => {
          console.log(`      [${k}] id=${ssk.id} f=${ssk.f} text="${ssk.text}" (children: ${ssk.childrenCount})`);
        });
      }
    });
  }
});
