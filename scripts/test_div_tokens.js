const marked = require('marked');

console.log("Tokens for '- ---':");
console.log(marked.lexer('- ---'));

console.log("\nTokens for '- ───':");
console.log(marked.lexer('- ───'));

console.log("\nTokens for '- &nbsp;':");
console.log(marked.lexer('- &nbsp;'));
