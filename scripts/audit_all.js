const http = require('http');

function evalCDP(jsCode) {
  return new Promise((resolve, reject) => {
    const req = http.request('http://127.0.0.1:9999/eval', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain; charset=utf-8' }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    });
    req.on('error', reject);
    req.write(jsCode);
    req.end();
  });
}

async function auditAll() {
  const code = `(async () => {
    try {
      const el = document.querySelector('[data-rem-id]');
      const fiberKey = Object.keys(el || {}).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
      let curr = el ? el[fiberKey] : null;
      let rem = null;
      while (curr) {
        if (curr.memoizedProps && curr.memoizedProps.rem && curr.memoizedProps.rem.getTinyGraph) {
          rem = curr.memoizedProps.rem;
          break;
        }
        curr = curr.return;
      }
      const tg = rem.getTinyGraph();
      const rc = tg.getRemCollection();
      const all = await rc.DatabaseStore.fetchAllImpl();
      const doc = all.find(r => r._id === 'GwREY4bq5eQvPyeAB');
      
      const weeks = all.filter(r => r.parent === doc._id)
        .filter(w => {
          const t = (w.key || []).map(k => typeof k === 'string' ? k : (k.text || '')).join('');
          return t.includes('Неделя');
        })
        .sort((a, b) => (a.f || '').localeCompare(b.f || ''));

      const issues = [];
      for (const w of weeks) {
        const wTitle = (w.key || []).map(k => typeof k === 'string' ? k : (k.text || '')).join('');
        const days = all.filter(r => r.parent === w._id).sort((a, b) => (a.f || '').localeCompare(b.f || ''));
        for (const d of days) {
          const dTitle = (d.key || []).map(k => typeof k === 'string' ? k : (k.text || '')).join('');
          if (dTitle.includes('**')) issues.push({ type: 'day_title_bold', id: d._id, text: dTitle });
          
          const dKids = all.filter(r => r.parent === d._id).sort((a, b) => (a.f || '').localeCompare(b.f || ''));
          for (const k of dKids) {
            const kTitle = (k.key || []).map(x => typeof x === 'string' ? x : (x.text || '')).join('');
            if (kTitle.includes('**')) issues.push({ type: 'kid_bold', id: k._id, day: dTitle, text: kTitle });
            if (kTitle.includes('_' + String.fromCharCode(96) + '_' + String.fromCharCode(96) + '_')) issues.push({ type: 'kid_glitch', id: k._id, day: dTitle, text: kTitle });
          }
        }
      }

      // Check TOC
      const toc = all.find(r => r.parent === doc._id && (r.key || []).some(k => typeof k === 'string' && k.includes('Оглавление')));
      let tocIssues = [];
      if (toc) {
        const tocKids = all.filter(r => r.parent === toc._id);
        tocIssues = tocKids.map(tk => ({
          id: tk._id,
          text: (tk.key || []).map(x => typeof x === 'string' ? x : (x.text || '')).join(''),
          ps: tk.ps
        }));
      }

      return JSON.stringify({ issues, tocCount: tocIssues.length, tocKids: tocIssues });
    } catch (e) {
      return JSON.stringify({ error: e.message });
    }
  })()`;

  const res = await evalCDP(code);
  console.log(res.value);
}

auditAll();
