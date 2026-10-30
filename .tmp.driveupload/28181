const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const { spawn } = require('child_process');

const ROOT_DIR = path.resolve(__dirname, '..');
const DATA_DIR = path.resolve(process.env.PBA_DATA_DIR || path.join(ROOT_DIR, 'data'));
const CONTENT_DIR = path.join(ROOT_DIR, 'data', 'content');
const PORT = Number(process.env.PORT || process.env.PBA_PORT) || 8080;
const CLOUDFLARED = path.join(__dirname, 'cloudflared.exe');
const SYNC_DEVICE_TTL_MS = 60 * 1000;
const SYNC_TOKEN = process.env.SYNC_TOKEN || '';
const DATABASE_URL = process.env.DATABASE_URL || '';
const CONTENT_CACHE = new Map();

if (process.env.NODE_ENV === 'production' && (!DATABASE_URL || !SYNC_TOKEN)) {
    throw new Error('Production requires DATABASE_URL and SYNC_TOKEN');
}

let syncPool = null;
let syncSchemaReady = null;

async function getSyncPool() {
    if (!DATABASE_URL) return null;
    if (!syncPool) {
        const { Pool } = require('pg');
        syncPool = new Pool({
            connectionString: DATABASE_URL,
            ssl: process.env.PGSSLMODE === 'disable' ? false : { rejectUnauthorized: false }
        });
    }
    if (!syncSchemaReady) {
        syncSchemaReady = syncPool.query(`CREATE TABLE IF NOT EXISTS academy_progress_sync (
            id smallint PRIMARY KEY DEFAULT 1 CHECK (id = 1),
            updated_at bigint NOT NULL,
            device text,
            client_id text,
            bundle jsonb NOT NULL
        )`);
    }
    await syncSchemaReady;
    return syncPool;
}

async function readSyncRecord(syncFile) {
    const pool = await getSyncPool();
    if (pool) {
        const result = await pool.query('SELECT updated_at, device, client_id, bundle FROM academy_progress_sync WHERE id = 1');
        const row = result.rows[0];
        return row ? { updatedAt: Number(row.updated_at), device: row.device, clientId: row.client_id, bundle: row.bundle } : null;
    }
    try {
        const parsed = JSON.parse(fs.readFileSync(syncFile, 'utf8'));
        return parsed && typeof parsed === 'object' && parsed.bundle ? parsed : null;
    } catch (e) {
        return null;
    }
}

async function writeSyncRecord(syncFile, record) {
    const pool = await getSyncPool();
    if (pool) {
        await pool.query(
            `INSERT INTO academy_progress_sync (id, updated_at, device, client_id, bundle)
             VALUES (1, $1, $2, $3, $4::jsonb)
             ON CONFLICT (id) DO UPDATE SET updated_at = EXCLUDED.updated_at, device = EXCLUDED.device, client_id = EXCLUDED.client_id, bundle = EXCLUDED.bundle`,
            [String(record.updatedAt), record.device, record.clientId, JSON.stringify(record.bundle)]
        );
        return;
    }
    const dataDir = path.dirname(syncFile);
    if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
    const tempFile = `${syncFile}.${process.pid}.${Math.random().toString(36).slice(2)}.tmp`;
    fs.writeFileSync(tempFile, JSON.stringify(record), 'utf8');
    fs.renameSync(tempFile, syncFile);
}

function readFeedbackQueue(queueFile) {
    if (!fs.existsSync(queueFile)) return [];
    try {
        const parsed = JSON.parse(fs.readFileSync(queueFile, 'utf8'));
        return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
        return [];
    }
}

function readRequestBody(req, maxBytes = 5 * 1024 * 1024) {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', chunk => {
            body += chunk;
            if (body.length > maxBytes) {
                req.destroy();
                reject(new Error('Payload too large'));
            }
        });
        req.on('end', () => resolve(body));
        req.on('error', reject);
    });
}

function syncAuthorized(req) {
    if (!SYNC_TOKEN) return true;
    const supplied = String(req.headers.authorization || '').replace(/^Bearer\s+/i, '');
    const expected = Buffer.from(SYNC_TOKEN);
    const actual = Buffer.from(supplied);
    return expected.length === actual.length && crypto.timingSafeEqual(expected, actual);
}

// Detect real LAN IP (filter out Hyper-V, vEthernet, WSL, VPN, Loopback)
function getLocalIp() {
    const interfaces = os.networkInterfaces();
    let fallback = '127.0.0.1';
    for (const name of Object.keys(interfaces)) {
        const lowerName = name.toLowerCase();
        if (lowerName.includes('vethernet') || lowerName.includes('hyper-v') ||
            lowerName.includes('wsl') || lowerName.includes('virtual') ||
            lowerName.includes('vpn') || lowerName.includes('loopback') ||
            lowerName.includes('bluetooth')) {
            continue;
        }
        for (const net of interfaces[name]) {
            if (net.family === 'IPv4' && !net.internal) {
                if (net.address.startsWith('192.168.')) {
                    return net.address;
                }
                if (fallback === '127.0.0.1') {
                    fallback = net.address;
                }
            }
        }
    }
    return fallback;
}

const localIp = getLocalIp();

const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.mjs': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.woff2': 'font/woff2',
    '.woff': 'font/woff',
    '.ttf': 'font/ttf',
    '.zip': 'application/zip',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.txt': 'text/plain; charset=utf-8',
    '.md': 'text/markdown; charset=utf-8'
};

function sendJson(res, statusCode, payload, extraHeaders = {}) {
    const body = JSON.stringify(payload);
    res.writeHead(statusCode, {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-cache, must-revalidate',
        ...extraHeaders
    });
    res.end(body);
}

function readContentJson(fileName, fallback) {
    try {
        const filePath = path.join(CONTENT_DIR, fileName);
        const modifiedAt = fs.statSync(filePath).mtimeMs;
        const cached = CONTENT_CACHE.get(fileName);
        if (cached && cached.modifiedAt === modifiedAt) return cached.value;
        const value = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        CONTENT_CACHE.set(fileName, { modifiedAt, value });
        return value;
    } catch (err) {
        return fallback;
    }
}

const server = http.createServer((req, res) => {
    // CORS headers for local LAN & mobile access
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    res.setHeader('Surrogate-Control', 'no-store');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    const parsedUrl = new URL(req.url, 'http://localhost');
    let reqUrl;
    try {
        reqUrl = decodeURI(parsedUrl.pathname);
    } catch (err) {
        sendJson(res, 400, { ok: false, error: 'Invalid URL encoding' });
        return;
    }

    if (reqUrl === '/healthz' || reqUrl === '/api/v1/health' || reqUrl === '/api/v1/health/') {
        sendJson(res, 200, { ok: true }, { 'Cache-Control': 'no-store' });
        return;
    }

    // REST API v1 for the decomposed frontend
    if (reqUrl === '/api/v1/content/summary') {
        const manifest = readContentJson('manifest.json', {});
        sendJson(res, 200, {
            ok: true,
            modulesCount: (manifest.modules || []).length,
            notesCount: manifest.totalNotes || 0,
            cardsCount: manifest.totalDecks || 0,
            flashcardsCount: manifest.totalFlashcards || 0,
            tasksCount: manifest.totalTasks || 0,
            version: manifest.version || '1.0.0'
        });
        return;
    }

    if (reqUrl === '/api/v1/content/modules') {
        const manifest = readContentJson('manifest.json', {});
        sendJson(res, 200, manifest.modules || []);
        return;
    }

    const noteMatch = reqUrl.match(/^\/api\/v1\/content\/notes\/([^/]+)$/);
    if (noteMatch && req.method === 'GET') {
        const noteId = decodeURIComponent(noteMatch[1]);
        const note = readContentJson('notes.json', {})[noteId];
        if (!note) {
            sendJson(res, 404, { detail: `Конспект с ID ${noteId} не найден` });
            return;
        }
        sendJson(res, 200, { ok: true, note });
        return;
    }

    const deckMatch = reqUrl.match(/^\/api\/v1\/content\/cards\/([^/]+)$/);
    if (deckMatch && req.method === 'GET') {
        const deckId = decodeURIComponent(deckMatch[1]);
        const deck = readContentJson('cards.json', {})[deckId];
        if (!deck) {
            sendJson(res, 404, { detail: `Колода с ID ${deckId} не найдена` });
            return;
        }
        sendJson(res, 200, { ok: true, deck });
        return;
    }

    if ((reqUrl === '/api/v1/content/tasks' || reqUrl === '/api/v1/content/tasks/') && req.method === 'GET') {
        const allTasks = readContentJson('tasks.json', []);
        const rawLevel = parsedUrl.searchParams.get('level');
        const level = rawLevel ? Number.parseInt(rawLevel, 10) : null;
        const topic = (parsedUrl.searchParams.get('topic') || '').toLocaleLowerCase();
        if (rawLevel && (!Number.isInteger(level) || level < 1 || level > 7)) {
            sendJson(res, 422, { detail: 'level must be between 1 and 7' });
            return;
        }
        const tasks = allTasks.filter(task => (level === null || task.level === level) &&
            (!topic || String(task.topic || '').toLocaleLowerCase().includes(topic)));
        sendJson(res, 200, { ok: true, count: tasks.length, tasks });
        return;
    }

    const taskMatch = reqUrl.match(/^\/api\/v1\/content\/tasks\/(\d+)$/);
    if (taskMatch && req.method === 'GET') {
        const taskId = Number.parseInt(taskMatch[1], 10);
        const task = readContentJson('tasks.json', []).find(item => item.id === taskId);
        if (!task) {
            sendJson(res, 404, { detail: `Задача с ID ${taskId} не найдена` });
            return;
        }
        sendJson(res, 200, { ok: true, task });
        return;
    }

    if (reqUrl === '/api/v1/content/search' && req.method === 'GET') {
        const query = (parsedUrl.searchParams.get('q') || '').trim();
        if (query.length < 2) {
            sendJson(res, 422, { detail: 'q must contain at least 2 characters' });
            return;
        }
        const needle = query.toLocaleLowerCase();
        const notes = readContentJson('notes.json', {});
        const tasks = readContentJson('tasks.json', []);
        const results = [];
        for (const [id, note] of Object.entries(notes)) {
            if (String(note.title || '').toLocaleLowerCase().includes(needle)) {
                results.push({ type: 'note', id, title: note.title, snippet: `Конспект ${id}` });
                if (results.length >= 20) break;
            }
        }
        if (results.length < 20) {
            for (const task of tasks) {
                if (`${task.title || ''} ${task.desc || ''}`.toLocaleLowerCase().includes(needle)) {
                    results.push({ type: 'task', id: task.id, title: task.title, snippet: `Задача #${task.id} (${task.tier || ''})` });
                    if (results.length >= 20) break;
                }
            }
        }
        sendJson(res, 200, { ok: true, query, count: results.length, results });
        return;
    }

    // REST API: Bug Reports / Mobile Feedback Queue (supports both /api/v1/feedback and legacy /api/bug-report)
    if (reqUrl === '/api/v1/feedback' || reqUrl === '/api/v1/feedback/' || reqUrl === '/api/bug-report' || reqUrl === '/api/bug-report/') {
        const queueFile = path.join(DATA_DIR, 'user_feedback_queue.json');

        if (req.method === 'POST') {
            readRequestBody(req, 5 * 1024 * 1024).then(body => {
                const report = JSON.parse(body || '{}');
                if (!fs.existsSync(DATA_DIR)) {
                    fs.mkdirSync(DATA_DIR, { recursive: true });
                }
                const queue = readFeedbackQueue(queueFile);
                if (!report.timestamp) report.timestamp = new Date().toISOString();
                if (!report.createdAt) report.createdAt = new Date().toLocaleString('ru-RU');
                queue.push(report);
                fs.writeFileSync(queueFile, JSON.stringify(queue, null, 2), 'utf8');
                console.log(`[+] [Feedback Queue] Получено новое замечание: [${report.context || 'unknown'}] (${queue.length} в очереди)`);
                sendJson(res, 200, { ok: true, count: queue.length, id: queue.length });
            }).catch(err => {
                sendJson(res, 400, { ok: false, error: err.message });
            });
            return;
        }

        if (req.method === 'GET') {
            const queue = readFeedbackQueue(queueFile);
            sendJson(res, 200, { ok: true, count: queue.length, reports: queue });
            return;
        }
    }

    // REST API: Cross-device progress sync (supports both /api/v1/sync and legacy /api/sync)
    if (reqUrl === '/api/sync' || reqUrl === '/api/sync/' || reqUrl === '/api/v1/sync' || reqUrl === '/api/v1/sync/') {
        const syncFile = path.join(DATA_DIR, 'progress_sync.json');

        if (!syncAuthorized(req)) {
            sendJson(res, 401, { ok: false, error: 'Unauthorized' });
            return;
        }

        if (req.method === 'GET') {
            readSyncRecord(syncFile).then(stored => {
                sendJson(res, 200, {
                    ok: true,
                    updatedAt: stored ? stored.updatedAt : 0,
                    device: stored ? stored.device : null,
                    bundle: stored ? stored.bundle : null
                });
            }).catch(err => {
                console.error('[Sync] GET failed:', err.message);
                sendJson(res, 503, { ok: false, error: 'Sync storage unavailable' });
            });
            return;
        }

        if (req.method === 'POST') {
            readRequestBody(req, 8 * 1024 * 1024).then(async body => {
                const payload = JSON.parse(body || '{}');
                const bundle = payload.bundle;
                if (!bundle || typeof bundle !== 'object' || !bundle.academyState || typeof bundle.academyState !== 'object') {
                    sendJson(res, 400, { ok: false, error: 'bundle.academyState is required' });
                    return;
                }
                const stored = await readSyncRecord(syncFile);
                const baseUpdatedAt = Number(payload.baseUpdatedAt) || 0;
                const clientId = String(payload.clientId || payload.device || 'unknown');
                const storedClientId = stored && String(stored.clientId || stored.device || '');
                const staleLocalWrite = stored && storedClientId && storedClientId !== clientId && stored.updatedAt > baseUpdatedAt + SYNC_DEVICE_TTL_MS;
                if (staleLocalWrite) {
                    sendJson(res, 409, { ok: false, conflict: true, updatedAt: stored.updatedAt, device: stored.device, bundle: stored.bundle });
                    console.log(`[!] [Sync] Конфликт устройств (${payload.device} vs ${stored.device}) — отправлен запрос на повторное слияние`);
                    return;
                }
                let nextBundle = bundle;
                if (stored && storedClientId !== clientId) {
                    nextBundle = {
                        academyState: Object.assign({}, stored.bundle.academyState || {}, bundle.academyState),
                        ideStatus: Object.assign({}, stored.bundle.ideStatus || {}, bundle.ideStatus || {}),
                        ideDrafts: Object.assign({}, stored.bundle.ideDrafts || {}, bundle.ideDrafts || {})
                    };
                }
                const record = { updatedAt: Date.now(), device: String(payload.device || 'unknown'), clientId, bundle: nextBundle };
                await writeSyncRecord(syncFile, record);
                console.log(`[+] [Sync] Прогресс сохранён (${(body.length / 1024).toFixed(1)} KB, устройство: ${record.device})`);
                sendJson(res, 200, { ok: true, updatedAt: record.updatedAt, bundle: record.bundle });
            }).catch(err => {
                console.error('[Sync] POST failed:', err.message);
                sendJson(res, 400, { ok: false, error: err.message });
            });
            return;
        }
    }

    if (reqUrl === '/' || reqUrl === '' || reqUrl === '/index.html') {
        reqUrl = '/academy.html';
    }

    if (reqUrl === '/practice_ide.html') {
        res.writeHead(302, { Location: '/academy.html#/practice', 'Cache-Control': 'no-cache, must-revalidate' });
        res.end();
        return;
    }

    if (reqUrl.startsWith('/api/')) {
        sendJson(res, 404, { ok: false, error: 'API endpoint not found' });
        return;
    }

    const safePath = path.normalize(reqUrl).replace(/^(\.\.[\/\\])+/, '');
    let filePath = path.join(ROOT_DIR, safePath);

    if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
        filePath = path.join(filePath, 'academy.html');
    }

    if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
        filePath = path.join(ROOT_DIR, 'academy.html');
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    try {
        const stat = fs.statSync(filePath);
        res.writeHead(200, {
            'Content-Type': contentType,
            'Content-Length': stat.size,
            'Cache-Control': 'no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0',
            'Access-Control-Allow-Origin': '*'
        });

        const stream = fs.createReadStream(filePath);
        stream.pipe(res);
    } catch (e) {
        res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('Server Error: ' + e.message);
    }
});

server.listen(PORT, '0.0.0.0', () => {
    console.log('========================================================');
    console.log('       🐍 Python Backend Academy — Web Server');
    console.log('========================================================');
    console.log(`📁 Папка проекта: ${ROOT_DIR}`);
    console.log(`💻 Локальный адрес на ПК: http://127.0.0.1:${PORT}/academy.html#/`);
    console.log(`📱 Локальный адрес (Wi-Fi): http://${localIp}:${PORT}/academy.html#/`);
    console.log('========================================================');

    if (process.platform === 'win32' && fs.existsSync(CLOUDFLARED)) {
        console.log('[+] Подключение защищенного туннеля Cloudflare (HTTPS)...');
        const tunnel = spawn(CLOUDFLARED, ['tunnel', '--protocol', 'http2', '--url', `http://127.0.0.1:${PORT}`], {
            cwd: path.dirname(CLOUDFLARED)
        });

        let tunnelFound = false;
        const handleLog = (chunk) => {
            const str = chunk.toString();
            const m = str.match(/https:\/\/[a-z0-9-]+\.trycloudflare\.com/i);
            if (m && !tunnelFound) {
                tunnelFound = true;
                const publicUrl = m[0];
                const phoneUrl = `${publicUrl}/academy.html#/`;
                fs.writeFileSync(path.join(ROOT_DIR, 'tunnel_url.txt'), phoneUrl, 'utf8');

                console.log('\n========================================================');
                console.log('🎉 САЙТ АКАДЕМИИ ДОСТУПЕН С ТЕЛЕФОНА!');
                console.log('========================================================');
                console.log('📱 Прямая ссылка для смартфона (HTTPS):');
                console.log(`   ${phoneUrl}`);
                console.log('========================================================\n');
            }
        };

        tunnel.stdout.on('data', handleLog);
        tunnel.stderr.on('data', handleLog);
    } else if (process.platform === 'win32') {
        console.log('[!] cloudflared.exe не найден, туннель не запущен.');
    }
});
