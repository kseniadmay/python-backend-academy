const net = require('net');

const server = net.createServer((clientSocket) => {
  const targetSocket = net.connect({ host: '127.0.0.1', port: 8080 }, () => {
    clientSocket.pipe(targetSocket);
    targetSocket.pipe(clientSocket);
  });

  clientSocket.on('error', () => targetSocket.destroy());
  targetSocket.on('error', () => clientSocket.destroy());
});

server.listen(8080, '::1', () => {
  console.log('IPv6 [::1]:8080 bridge to IPv4 127.0.0.1:8080 active!');
});
