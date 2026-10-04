const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const doc = db.prepare("SELECT doc FROM quanta WHERE _id = 'W8rTD8BBpLU5OJ98H'").get();
console.log(doc ? doc.doc : 'null');
