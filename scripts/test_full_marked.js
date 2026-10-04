const marked = require('marked');

const md = [
    "- [ ] ⚡ **Skill 1.1.1**",
    "  - 🎯 **Критерий мастерства**: тест",
    "",
    "- ────────────────────────────────────────",
    "",
    "- [ ] ⚡ **Skill 1.1.2**"
].join('\n');

const tokens = marked.lexer(md);
console.log("Tokens count:", tokens.length);
for (const tok of tokens) {
    console.log("Token type:", tok.type);
    if (tok.type === 'list') {
        console.log("  Items count:", tok.items.length);
        for (const item of tok.items) {
            console.log("    Item text:", JSON.stringify(item.text.slice(0, 50)));
        }
    }
}
