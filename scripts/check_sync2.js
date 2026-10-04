const { DatabaseSync } = require('node:sqlite');
const dbPath = 'C:/Users/fury6/remnote/remnote-6a7345f0a3f205110d2692d2/remnote.db';
const db = new DatabaseSync(dbPath, { open: true });

const syncRow = db.prepare("SELECT doc FROM quanta WHERE _id = 'sync2'").get();
console.log('sync2 doc:', syncRow ? syncRow.doc : 'null');
