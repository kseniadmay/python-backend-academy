const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawn, execSync } = require('child_process');

const ROOT_DIR = path.resolve(__dirname, '..');
const PORT = 8080;
const CLOUDFLARED = path.join(__dirname, 'cloudflared.exe');

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
    let reqUrl = decodeURI(req.url.split('?')[0].split('#')[0]);

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
    if (fs.existsSync(CLOUDFLARED)) {
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
    } else {
        console.log('[!] cloudflared.exe не найден, туннель не запущен.');
    }
});
