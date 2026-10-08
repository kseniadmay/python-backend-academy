const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const { spawn, execSync } = require('child_process');

const ROOT_DIR = path.resolve(__dirname, '..');
const PORT = Number(process.env.PORT || process.env.PBA_PORT) || 8080;
const CLOUDFLARED = path.join(__dirname, 'cloudflared.exe');
const SYNC_DEVICE_TTL_MS = 60 * 1000;
const SYNC_TOKEN = process.env.SYNC_TOKEN || '';
const DATABASE_URL = process.env.DATABASE_URL || '';
if (process.env.NODE_ENV === 'production' && (!DATABASE_URL || !SYNC_TOKEN)) {
    throw new Error('Production requires DATABASE_URL and SYNC_TOKEN');
}
let syncPool = null;
let syncSchemaReady = null;

async function getSyncPool() {
    if (!DATABASE_URL) return null;
    if (!syncPool) {
        const { Pool } = require('pg');
        syncPool = new Pool({ connectionString: DATABASE_URL, ssl: process.env.PGSSLMODE === 'disable' ? false : { rejectUnauthorized: false } });
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
    } catch (e) { return null; }
}

async function writeSyncRecord(syncFile, record) {
    const pool = await getSyncPool();
    if (pool) {
        await pool.query(`INSERT INTO academy_progress_sync (id, updated_at, device, client_id, bundle)
            VALUES (1, $1, $2, $3, $4::jsonb)
            ON CONFLICT (id) DO UPDATE SET updated_at = EXCLUDED.updated_at, device = EXCLUDED.device, client_id = EXCLUDED.client_id, bundle = EXCLUDED.bundle`,
        [String(record.updatedAt), record.device, record.clientId, JSON.stringify(record.bundle)]);
        return;
    }
    const dataDir = path.dirname(syncFile);
    if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
    const tempFile = `${syncFile}.${process.pid}.${Math.random().toString(36).slice(2)}.tmp`;
    fs.writeFileSync(tempFile, JSON.stringify(record), 'utf8');
    fs.renameSync(tempFile, syncFile);
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

const server = http.createServer((req, res) => {
    // CORS headers for local LAN & mobile access
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
        res.writeHead(204);
        res.end();
        return;
    }

    let reqUrl = decodeURI(req.url.split('?')[0].split('#')[0]);

    if (reqUrl === '/healthz') {
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
        res.end(JSON.stringify({ ok: true }));
        return;
    }

    // REST API: Bug Reports / Mobile Feedback Queue
    if (reqUrl === '/api/bug-report' || reqUrl === '/api/bug-report/') {
        const dataDir = path.join(ROOT_DIR, 'data');
        const queueFile = path.join(dataDir, 'user_feedback_queue.json');

        if (req.method === 'POST') {
            let body = '';
            req.on('data', chunk => {
                body += chunk;
                if (body.length > 5 * 1024 * 1024) req.destroy();
            });
            req.on('end', () => {
                try {
                    const report = JSON.parse(body || '{}');
                    if (!fs.existsSync(dataDir)) {
                        fs.mkdirSync(dataDir, { recursive: true });
                    }
                    let queue = [];
                    if (fs.existsSync(queueFile)) {
                        try {
                            const parsed = JSON.parse(fs.readFileSync(queueFile, 'utf8'));
                            if (Array.isArray(parsed)) queue = parsed;
                        } catch(e) {
                            queue = [];
                        }
                    }
                    if (!report.timestamp) report.timestamp = new Date().toISOString();
                    if (!report.createdAt) report.createdAt = new Date().toLocaleString('ru-RU');
                    queue.push(report);
                    fs.writeFileSync(queueFile, JSON.stringify(queue, null, 2), 'utf8');
                    console.log(`[+] [Feedback Queue] Получено новое замечание: [${report.context || 'unknown'}] (${queue.length} в очереди)`);
                    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
                    res.end(JSON.stringify({ ok: true, count: queue.length, id: queue.length }));
                } catch(err) {
                    res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
                    res.end(JSON.stringify({ ok: false, error: err.message }));
                }
            });
            return;
        }

        if (req.method === 'GET') {
            let queue = [];
            if (fs.existsSync(queueFile)) {
                try {
                    const parsed = JSON.parse(fs.readFileSync(queueFile, 'utf8'));
                    if (Array.isArray(parsed)) queue = parsed;
                } catch(e) {
                    queue = [];
                }
            }
            res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
            res.end(JSON.stringify({ ok: true, count: queue.length, reports: queue }));
            return;
        }
    }

    // REST API: Cross-device progress sync (PostgreSQL in cloud, local JSON in development)
    // GET  /api/sync -> { ok, updatedAt, device, bundle }
    // POST /api/sync -> { bundle:{academyState,ideStatus,ideDrafts}, baseUpdatedAt, device }
    //   409 { ok:false, conflict:true, ...current } when another device pushed a newer bundle (client re-merges and retries)
    if (reqUrl === '/api/sync' || reqUrl === '/api/sync/') {
        const dataDir = path.join(ROOT_DIR, 'data');
        const syncFile = path.join(dataDir, 'progress_sync.json');

        if (!syncAuthorized(req)) {
            res.writeHead(401, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
            res.end(JSON.stringify({ ok: false, error: 'Unauthorized' }));
            return;
        }

        if (req.method === 'GET') {
            readSyncRecord(syncFile).then(stored => {
                res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
                res.end(JSON.stringify({ ok: true, updatedAt: stored ? stored.updatedAt : 0, device: stored ? stored.device : null, bundle: stored ? stored.bundle : null }));
            }).catch(err => {
                console.error('[Sync] GET failed:', err.message);
                res.writeHead(503, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
                res.end(JSON.stringify({ ok: false, error: 'Sync storage unavailable' }));
            });
            return;
        }

        if (req.method === 'POST') {
            let body = '';
            req.on('data', chunk => {
                body += chunk;
                if (body.length > 8 * 1024 * 1024) req.destroy();
            });
            req.on('end', async () => {
                try {
                    const payload = JSON.parse(body || '{}');
                    const bundle = payload.bundle;
                    if (!bundle || typeof bundle !== 'object' || !bundle.academyState || typeof bundle.academyState !== 'object') {
                        res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
                        res.end(JSON.stringify({ ok: false, error: 'bundle.academyState is required' }));
                        return;
                    }
                    const stored = await readSyncRecord(syncFile);
                    const baseUpdatedAt = Number(payload.baseUpdatedAt) || 0;
                    // Lost-update guard: another device pushed a bundle this sender has never seen -> ask it to re-merge
                    const clientId = String(payload.clientId || payload.device || 'unknown');
                    const storedClientId = stored && String(stored.clientId || stored.device || '');
                    const staleLocalWrite = stored && storedClientId && storedClientId !== clientId && stored.updatedAt > baseUpdatedAt + SYNC_DEVICE_TTL_MS;
                    if (staleLocalWrite) {
                        res.writeHead(409, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
                        res.end(JSON.stringify({ ok: false, conflict: true, updatedAt: stored.updatedAt, device: stored.device, bundle: stored.bundle }));
                        console.log(`[!] [Sync] Конфликт устройств (${payload.device} vs ${stored.device}) — отправлен запрос на повторное слияние`);
                        return;
                    }
                    let nextBundle = bundle;
                    if (stored && storedClientId !== clientId) {
                        // Merge monotonic progress server-side as well, so simultaneous pushes cannot erase completions.
                        nextBundle = {
                            academyState: Object.assign({}, stored.bundle.academyState || {}, bundle.academyState),
                            ideStatus: Object.assign({}, stored.bundle.ideStatus || {}, bundle.ideStatus || {}),
                            ideDrafts: Object.assign({}, stored.bundle.ideDrafts || {}, bundle.ideDrafts || {})
                        };
                    }
                    const record = { updatedAt: Date.now(), device: String(payload.device || 'unknown'), clientId, bundle: nextBundle };
                    await writeSyncRecord(syncFile, record);
                    console.log(`[+] [Sync] Прогресс сохранён (${(body.length / 1024).toFixed(1)} KB, устройство: ${record.device})`);
                    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
                    res.end(JSON.stringify({ ok: true, updatedAt: record.updatedAt, bundle: record.bundle }));
                } catch (err) {
                    console.error('[Sync] POST failed:', err.message);
                    res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
                    res.end(JSON.stringify({ ok: false, error: err.message }));
                }
            });
            return;
        }
    }

    if (reqUrl === '/' || reqUrl === '' || reqUrl === '/index.html') {
        reqUrl = '/academy.html';
    }

    const safePath = path.normalize(reqUrl).replace(/^(\.\.[\/\\])+/, '');
    let filePath = path.join(ROOT_DIR, safePath);

    // If directory, look for academy.html
    if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
        filePath = path.join(filePath, 'academy.html');
    }

    if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
        // Fallback to academy.html for SPA hash routes
        filePath = path.join(ROOT_DIR, 'academy.html');
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    try {
        const stat = fs.statSync(filePath);
        res.writeHead(200, {
            'Content-Type': contentType,
            'Content-Length': stat.size,
            'Cache-Control': 'no-cache',
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

    // Запуск Cloudflare Tunnel
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
                console.log(`📱 Прямая ссылка для смартфона (HTTPS):`);
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
