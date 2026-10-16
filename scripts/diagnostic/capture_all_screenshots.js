async function run() {
  // Screenshot 1: Top
  await fetch('http://127.0.0.1:9999/eval', {
    method: 'POST',
    body: 'window.scrollTo(0, 0); true;'
  });
  await new Promise(r => setTimeout(r, 1200));
  await fetch('http://127.0.0.1:9999/screenshot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: 'C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\screenshot_1_top.png' })
  });

  // Screenshot 2: Day 03, 04, 05
  await fetch('http://127.0.0.1:9999/eval', {
    method: 'POST',
    body: 'const d = Array.from(document.querySelectorAll("[data-rem-id]")).find(el => el.textContent.includes("День 03")); if (d) d.scrollIntoView(); true;'
  });
  await new Promise(r => setTimeout(r, 1200));
  await fetch('http://127.0.0.1:9999/screenshot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: 'C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\screenshot_2_day3.png' })
  });

  // Screenshot 3: Day 22
  await fetch('http://127.0.0.1:9999/eval', {
    method: 'POST',
    body: 'const d = Array.from(document.querySelectorAll("[data-rem-id]")).find(el => el.textContent.includes("День 22")); if (d) d.scrollIntoView(); true;'
  });
  await new Promise(r => setTimeout(r, 1200));
  await fetch('http://127.0.0.1:9999/screenshot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: 'C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\screenshot_3_day22.png' })
  });

  console.log('Screenshots captured successfully!');
}

run();
