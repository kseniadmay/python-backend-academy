const http = require('http');

http.get('http://127.0.0.1:9222/json/list', (res) => {
  let data = '';
  console.log('Status code:', res.statusCode);
  console.log('Headers:', res.headers);
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('Raw data length:', data.length);
    console.log('Raw data:', data);
  });
}).on('error', err => console.error('Connection error:', err));
