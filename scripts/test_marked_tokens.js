const marked = require('marked');

const tests = [
    "Test 1: Normal List\n- Skill 1\n  - Criteria 1\n- Skill 2",
    "Test 2: Empty bullet\n- Skill 1\n  - Criteria 1\n-\n- Skill 2",
    "Test 3: Empty bullet with space\n- Skill 1\n  - Criteria 1\n- \n- Skill 2",
    "Test 4: Non-breaking space bullet\n- Skill 1\n  - Criteria 1\n- &nbsp;\n- Skill 2",
    "Test 5: Header H3\n### Skill 1\n- Criteria 1\n\n### Skill 2",
    "Test 6: Header H4\n#### Skill 1\n- Criteria 1\n\n#### Skill 2",
    "Test 7: Box drawing divider\n- Skill 1\n  - Criteria 1\n- ──────────────────────────\n- Skill 2"
];

for (const t of tests) {
    console.log("==========================================");
    console.log(t.split('\n')[0]);
    const tokens = marked.lexer(t.slice(t.indexOf('\n') + 1));
    console.log("Tokens summary:");
    for (const tok of tokens) {
        if (tok.type === 'list') {
            console.log("  LIST (items: " + tok.items.length + ")");
            for (const it of tok.items) {
                console.log("    ITEM text:", JSON.stringify(it.text.slice(0, 40)));
            }
        } else if (tok.type === 'heading') {
            console.log("  HEADING depth:", tok.depth, "text:", tok.text);
        } else {
            console.log("  " + tok.type + ":", JSON.stringify(tok.text || ""));
        }
    }
}
