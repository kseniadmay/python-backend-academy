async function run() {
  await fetch('http://127.0.0.1:9999/eval', {
    method: 'POST',
    body: 'window.scrollTo(0, 0); const doc = document.querySelector(".document-title") || document.querySelector(".rem-container"); if (doc) doc.scrollIntoView(); true;'
  });
  await new Promise(r => setTimeout(r, 1000));
  const res = await fetch('http://127.0.0.1:9999/screenshot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: 'C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\top_web_view.png' })
  });
  console.log(await res.json());
}
run();
