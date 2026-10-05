let marked;
try {
  marked = require('marked');
} catch (e) {
  console.log('[SKIP] Optional module "marked" not installed. Scratch test skipped.');
  process.exit(0);
}


console.log("Tokens for '- ---':");
console.log(marked.lexer('- ---'));

console.log("\nTokens for '- ───':");
console.log(marked.lexer('- ───'));

console.log("\nTokens for '- &nbsp;':");
console.log(marked.lexer('- &nbsp;'));
