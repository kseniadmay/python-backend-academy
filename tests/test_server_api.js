const assert = require('assert');
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const net = require('net');

const ROOT = path.resolve(__dirname, '..');
const SERVER = path.join(ROOT, 'scripts', 'server.js');

async function getFreePort() {
  const socket = net.createServer();
  await new Promise((resolve, reject) => socket.listen(0, '127.0.0.1', resolve).once('error', reject));
  const { port } = socket.address();
  await new Promise(resolve => socket.close(resolve));
  return port;
}

async function waitForServer(baseUrl, child) {
  for (let attempt = 0; attempt < 20; attempt++) {
    if (child.exitCode !== null) throw new Error(`Server exited early with code ${child.exitCode}: ${child.__output || ''}`);
    try {
      const response = await fetch(`${baseUrl}/healthz`, { signal: AbortSignal.timeout(300) });
      if (response.ok) return;
    } catch (_) {}
    await new Promise(resolve => setTimeout(resolve, 150));
  }
  throw new Error('Server did not become healthy within 9 seconds');
}

function request(url, options = {}) {
  return fetch(url, { signal: AbortSignal.timeout(5000), ...options });
}

async function stopChild(child) {
  if (child.exitCode !== null || child.signalCode !== null) return;
  await new Promise(resolve => {
    const timer = setTimeout(resolve, 2000);
    child.once('exit', () => { clearTimeout(timer); resolve(); });
    child.kill();
  });
}

async function main() {
  const port = await getFreePort();
  const testDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'academy-api-test-'));
  const child = spawn(process.execPath, [SERVER], {
    cwd: ROOT,
    env: { ...process.env, PORT: String(port), PBA_DATA_DIR: testDataDir, NODE_ENV: 'test', DATABASE_URL: '', SYNC_TOKEN: '' },
    stdio: ['ignore', 'pipe', 'pipe']
  });
  child.__output = '';
  child.stdout.on('data', chunk => { child.__output += chunk.toString(); });
  child.stderr.on('data', chunk => { child.__output += chunk.toString(); });
  const baseUrl = `http://127.0.0.1:${port}`;
  console.log(`Starting isolated test server on ${port}`);

  try {
    await waitForServer(baseUrl, child);
    console.log('✓ server health');

    const summaryResponse = await request(`${baseUrl}/api/v1/content/summary`);
    assert.match(summaryResponse.headers.get('content-type') || '', /application\/json/);
    const summary = await summaryResponse.json();
    assert.strictEqual(summary.ok, true);
    assert.strictEqual(summary.tasksCount, 401);
    console.log('✓ content summary');

    const modules = await (await request(`${baseUrl}/api/v1/content/modules`)).json();
    assert.strictEqual(modules.length, 7);

    const note = await (await request(`${baseUrl}/api/v1/content/notes/${encodeURIComponent('К-001')}`)).json();
    assert.strictEqual(note.ok, true);
    assert.ok(note.note);
    console.log('✓ notes endpoint');

    const deck = await (await request(`${baseUrl}/api/v1/content/cards/${encodeURIComponent('Ф-001')}`)).json();
    assert.strictEqual(deck.ok, true);
    assert.ok(deck.deck);
    console.log('✓ cards endpoint');

    const taskList = await (await request(`${baseUrl}/api/v1/content/tasks?level=1&topic=Python`)).json();
    assert.ok(taskList.count > 0);
    const task = await (await request(`${baseUrl}/api/v1/content/tasks/401`)).json();
    assert.strictEqual(task.task.id, 401);
    console.log('✓ task endpoints');

    const search = await (await request(`${baseUrl}/api/v1/content/search?q=FastAPI`)).json();
    assert.strictEqual(search.ok, true);
    assert.ok(Array.isArray(search.results));

    const initialSync = await (await request(`${baseUrl}/api/v1/sync`)).json();
    assert.strictEqual(initialSync.updatedAt, 0);
    const bundle = { academyState: { xp: 12, completedTasks: [1] }, ideStatus: {}, ideDrafts: {} };
    const push = await request(`${baseUrl}/api/v1/sync`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bundle, baseUpdatedAt: 0, device: 'api-test', clientId: 'api-test-client' })
    });
    assert.strictEqual(push.status, 200);
    const pushed = await push.json();
    assert.strictEqual(pushed.bundle.academyState.xp, 12);
    const pulled = await (await request(`${baseUrl}/api/v1/sync`)).json();
    assert.strictEqual(pulled.bundle.academyState.completedTasks[0], 1);
    console.log('✓ sync endpoints');

    const feedback = await request(`${baseUrl}/api/v1/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ context: 'api-test', message: 'isolated integration test' })
    });
    assert.strictEqual(feedback.status, 200);
    assert.strictEqual((await feedback.json()).ok, true);

    const redirect = await request(`${baseUrl}/practice_ide.html`, { redirect: 'manual' });
    assert.strictEqual(redirect.status, 302);
    assert.strictEqual(redirect.headers.get('location'), '/academy.html#/practice');

    const missingApi = await request(`${baseUrl}/api/v1/missing`);
    assert.strictEqual(missingApi.status, 404);
    assert.match(missingApi.headers.get('content-type') || '', /application\/json/);
    console.log('✓ Node production server API v1, sync, feedback, and trainer route passed');
  } finally {
    await stopChild(child);
    fs.rmSync(testDataDir, { recursive: true, force: true });
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
