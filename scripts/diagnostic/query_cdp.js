const http = require('http');

const req = http.request({
  hostname: 'localhost',
  port: 9222,
  path: '/json',
  method: 'GET',
  headers: {
    'Host': 'localhost:9222'
  }
}, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      const list = JSON.parse(data);
      console.log('Open targets count:', list.length);
      for (const t of list) {
        console.log(`[${t.type}] title="${t.title}" url="${t.url}"`);
      }
    } catch (e) {
      console.error('Error parsing JSON:', e.message, 'Raw:', data);
    }
  });
});

req.on('error', err => console.error('Request error:', err));
req.end();
