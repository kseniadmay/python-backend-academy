const fs = require('fs');

let xml = fs.readFileSync('C:/Users/fury6/.gemini/antigravity/scratch/docx_unpacked/word/document.xml', 'utf8');

// 1. Header: remove Junior, update location
xml = xml.replace(/Junior Python Backend Developer\s+\|\s+Москва/g, 'Python Backend Developer  |  Нижний Новгород / Удалённо');

// 2. About section
const oldAboutRegex = /Python Backend Developer с опытом RESTful API development.*?Ищу команду для роста как backend-инженер\./s;
const newAbout = 'Python Backend Developer с фокусом на проектирование REST API на Django REST Framework и FastAPI. Уделяю внимание производительности: оптимизирую запросы к PostgreSQL (устранение N+1), внедряю Redis-кэширование и асинхронную обработку задач на Celery. Проекты разворачиваю в Docker, настраиваю CI/CD, покрываю код автотестами на pytest (coverage 88%). Английский B2.';
xml = xml.replace(oldAboutRegex, newAbout);

// 3. DevOps: Railway -> Render
xml = xml.replace(/Gunicorn, Railway, GitHub Actions/g, 'Gunicorn, Render, GitHub Actions');

// 4. Projects: update Recipe API link & add RecipeBot
const oldProjectTarget = '<w:t>GitHub: github.com/kseniadmay/recipeapi</w:t></w:r></w:p>';
const newProjectReplacement = `<w:t>Live Demo: recipeapi-service.onrender.com/docs/  |  GitHub: github.com/kseniadmay/recipeapi</w:t></w:r></w:p>` +
`<w:p w14:paraId="7BCA6D31" w14:textId="71647B21" w:rsidR="000E01B3" w:rsidRPr="004E6CB8" w:rsidRDefault="00EC2FC3"><w:pPr><w:spacing w:before="60" w:after="20"/><w:rPr><w:lang w:val="en-US"/></w:rPr></w:pPr><w:r w:rsidRPr="00D239D2"><w:rPr><w:rFonts w:ascii="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:b/><w:bCs/><w:color w:val="374151"/><w:sz w:val="19"/><w:szCs w:val="19"/><w:lang w:val="en-US"/></w:rPr><w:t>Recipe Telegram Bot</w:t></w:r><w:r w:rsidR="004E6CB8" w:rsidRPr="004E6CB8"><w:rPr><w:rFonts w:ascii="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:color w:val="6B7280"/><w:sz w:val="18"/><w:szCs w:val="18"/><w:lang w:val="en-US"/></w:rPr><w:t xml:space="preserve">  |  Python, python-telegram-bot, REST API client  |  2026</w:t></w:r></w:p>` +
`<w:p w14:paraId="1FCBD5BC" w14:textId="05894FD9" w:rsidR="000E01B3" w:rsidRPr="00F17953" w:rsidRDefault="00EC2FC3"><w:pPr><w:spacing w:after="50"/><w:rPr><w:rFonts w:ascii="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:color w:val="374151"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr></w:pPr><w:r w:rsidRPr="004E6CB8"><w:rPr><w:rFonts w:ascii="Calibri" w:eastAsia="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:color w:val="374151"/><w:sz w:val="19"/><w:szCs w:val="19"/><w:lang w:val="en-US"/></w:rPr><w:t>Telegram: @recipeapibot  |  GitHub: github.com/kseniadmay/RecipeBot</w:t></w:r></w:p>`;

if (xml.includes(oldProjectTarget)) {
    xml = xml.replace(oldProjectTarget, newProjectReplacement);
    console.log('Projects successfully updated!');
} else {
    console.warn('Warning: oldProjectTarget not matched directly, checking fuzzy match');
}

// 5. Replace any remaining em-dashes
xml = xml.replace(/—/g, '–');

fs.writeFileSync('C:/Users/fury6/.gemini/antigravity/scratch/docx_unpacked/word/document.xml', xml, 'utf8');
console.log('Finished patching document.xml');
