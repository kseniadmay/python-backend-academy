async function capture() {
  const shots = [
    { name: 'top', eval: 'window.scrollTo(0, 0);' },
    { name: 'day2', eval: 'const el = Array.from(document.querySelectorAll("[data-rem-id]")).find(e => e.textContent.includes("День 02")); if (el) el.scrollIntoView();' },
    { name: 'day7', eval: 'const el = Array.from(document.querySelectorAll("[data-rem-id]")).find(e => e.textContent.includes("День 07")); if (el) el.scrollIntoView();' },
    { name: 'day22', eval: 'const el = Array.from(document.querySelectorAll("[data-rem-id]")).find(e => e.textContent.includes("День 22")); if (el) el.scrollIntoView();' },
    { name: 'day42', eval: 'const el = Array.from(document.querySelectorAll("[data-rem-id]")).find(e => e.textContent.includes("День 42")); if (el) el.scrollIntoView();' }
  ];

  for (const shot of shots) {
    await fetch('http://127.0.0.1:9999/eval', {
      method: 'POST',
      body: shot.eval + ' true;'
    });
    await new Promise(r => setTimeout(r, 1000));
    await fetch('http://127.0.0.1:9999/screenshot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: `C:\\Users\\fury6\\.gemini\\antigravity\\scratch\\final_${shot.name}.png` })
    });
  }
  console.log('All final screenshots taken!');
}

capture();
