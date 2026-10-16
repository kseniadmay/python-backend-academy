const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const doc1 = db.prepare("SELECT doc FROM quanta WHERE _id = '0BsCGn84rl1w7yvwX'").get();
console.log('Sample rem with powerup W8rTD8BBpLU5OJ98H (List Item):');
console.log(JSON.stringify(JSON.parse(doc1.doc), null, 2));
