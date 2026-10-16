const fs = require('fs');
const path = require('path');

function replaceQuotesInCodeLine(line) {
  // If line has triple quotes, handle carefully or skip
  if (line.includes('"""') || line.includes("'''")) {
    return line;
  }
  
  // Skip Dockerfile exec format: CMD ["...", "..."] or ENTRYPOINT ["...", "..."]
  if (/^\s*(CMD|ENTRYPOINT|VOLUME)\s*\[/.test(line)) {
    return line;
  }

  // Regex to match string literals with double quotes:
  // prefix can be r, u, f, b, rf, fr, rb, br (case-insensitive) or empty
  // group 1: prefix
  // group 2: content inside quotes
  const regex = /([rubfRUBF]{0,2})"((?:[^"\\]|\\.)*)"/g;

  return line.replace(regex, (match, prefix, content, offset, fullStr) => {
    // If inside content there is an unescaped single quote, keep double quotes
    if (/(?:[^\\]|^)'/.test(content)) {
      return match;
    }
    
    // If content has \", convert to " since inside single quotes it doesn't need escaping
    const newContent = content.replace(/\\"/g, '"');
    
    return `${prefix}'${newContent}'`;
  });
}

// Test cases
const tests = [
  'describe(name="Alex", age=30)',
  'print(f"Вызов {func.__name__} с args={args}, kwargs={kwargs}")',
  'user = {"name": "Alex", "age": 30}',
  'f = open("data.txt", "r")',
  'names = ["Alice", "Bob", "Charlie"]',
  '"""Greets the user"""',
  `return f"Money({self.amount}, '{self.currency}')"`,
  `query = f"SELECT * FROM users WHERE username = '{username}'"`,
  'CMD ["uvicorn", "main:app"]',
  'msg = "He said \\"Hello\\""'
];

tests.forEach(t => {
  console.log('BEFORE:', t);
  console.log('AFTER: ', replaceQuotesInCodeLine(t));
  console.log();
});
