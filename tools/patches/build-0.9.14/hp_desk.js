const HPC = { paper: '#ece5cc', ink: '#241d10', dim: '#7a6f4f', wood1: '#4a3522', wood2: '#2c1f13', cover: '#2d3a46', ok: '#2f8f4a', bad: '#c0392b' };
const HP_TAB = { sup: '#e0b13a', per: '#5aa0e0', med: '#e06a6a', ops: '#6ac27a' };
function hpT(x, y, txt, col, size, anchor, extra) {
  return `<text x="${x}" y="${y}" style="fill:${col};font-size:${size}px;text-anchor:${anchor || 'start'};font-family:'Courier New',monospace" ${extra || ''}>${txt}</text>`;
}
function hpRc(x, y, w, h, fill, stroke, rx, extra) {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx || 0}" style="fill:${fill};stroke:${stroke || 'none'};stroke-width:2${(extra || '').includes('onpointerdown') ? ';cursor:pointer' : ''}" ${extra || ''}/>`;
}
function hpFit() {
  const f = $('hpfit');
  const host = $('hpbody');
  if (!f || !host || !HPG) return;
  const w = host.clientWidth;
  const h = host.clientHeight;
  if (!w || !h) return;
  HPG.fw = w;
  HPG.fh = h;
  const s = Math.min(1.25, w / 760, h / 540);
  HPG.scale = s;
  f.style.width = Math.floor(760 * s) + 'px';
  f.style.height = Math.floor(540 * s) + 'px';
  $('hpdev').style.transform = 'scale(' + s + ')';
}
window.addEventListener('resize', () => { if (HPG) hpFit(); });

function hpTick() {
  if (!HPG || HPG.res) return;
  const left = HPG.endAt - performance.now();
  if (left <= 0) { hpEnd(false); return; }
  const host = $('hpbody');
  if (host && (host.clientWidth !== HPG.fw || host.clientHeight !== HPG.fh)) hpFit();
  hpDraw();
}

function hpRender() {
  if (!HPG) return;
  $('hptitle').textContent = HPG.res === 'win' ? 'PAPERWORK SIGNED' : (HPG.res === 'fail' ? 'PAPERWORK REJECTED' : 'HAMMOND\'S PAPERWORK');
  $('hpsub').textContent = 'BRIEFING ROOM // FILE EACH FORM IN ITS TAB, OR DENY THE FLAWED ONES';
  if (!$('hpdev')) $('hpbody').innerHTML = '<div id="hpfit"><div id="hpdev"><svg id="hpsvg" viewBox="0 0 760 540" width="760" height="540"></svg></div></div>';
  if (!HPG.scale) hpFit();
  hpDraw();
}

function hpTabClick(k) { if (HPG && !HPG.res) hpAct(k); }

function hpDraw() {
  if (!HPG || !$('hpsvg')) return;
  const now = performance.now();
  let h = `<defs><linearGradient id="hpwood" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${HPC.wood1}"/><stop offset="1" stop-color="${HPC.wood2}"/></linearGradient></defs>`;
  h += `<rect width="760" height="540" style="fill:url(#hpwood)"/>`;
  for (let i = 0; i < 14; i++) h += `<line x1="0" y1="${20 + i * 40}" x2="760" y2="${24 + i * 40 + (i % 3)}" style="stroke:rgba(0,0,0,.18);stroke-width:1"/>`;
  // binder
  h += hpRc(20, 56, 546, 458, HPC.cover, '#101820', 10);
  h += hpRc(32, 70, 244, 430, HPC.paper, '#b5ab88', 3);
  h += hpRc(288, 70, 232, 430, HPC.paper, '#b5ab88', 3);
  [110, 250, 390].forEach(y => { h += `<circle cx="282" cy="${y}" r="9" style="fill:#9aa4ab;stroke:#4a5359;stroke-width:3"/>`; });
  // tabs
  HP_KEYS.forEach((k, i) => {
    const y = 80 + i * 102;
    const fl = HPG.fl && now < HPG.fl.t && HPG.fl.k === k;
    h += hpRc(522, y, 52, 98, HP_TAB[k], fl ? (HPG.fl.ok ? HPC.ok : HPC.bad) : '#00000055', 6, `onpointerdown="hpTabClick('${k}')"`);
    h += hpT(548, y + 18, i + 1, HPC.ink, 14, 'middle', 'pointer-events="none"');
    h += `<text transform="translate(552 ${y + 92}) rotate(-90)" style="fill:${HPC.ink};font-size:10.5px;font-family:'Courier New',monospace;pointer-events:none">${HP_TYPES[k].stamp}</text>`;
  });
  // form
  if (!HPG.res) {
    const f = HPG.forms[HPG.idx];
    const T = HP_TYPES[f.k];
    h += hpT(44, 96, 'SGC // CHEYENNE MOUNTAIN', HPC.dim, 10);
    h += hpT(44, 122, T.title, HPC.ink, 17, 'start', 'style="font-weight:bold"');
    h += hpT(264, 96, 'REF ' + f.ref, HPC.dim, 11, 'end');
    h += `<line x1="44" y1="132" x2="264" y2="132" style="stroke:#8a7f5f"/>`;
    const rows = [['ROUTE TO', f.dept], ['ITEM', f.item], ['QTY x UNIT', f.qty + ' x ' + f.unit], ['TOTAL STATED', String(f.total)], ['SIGNED', f.signer || ''], ['VALID UNTIL', 'DAY ' + f.until]];
    rows.forEach((r, n) => {
      const y = 168 + n * 48;
      h += hpT(44, y - 14, r[0], HPC.dim, 10);
      if (r[1]) h += hpT(44, y + 6, r[1], HPC.ink, 16, 'start', 'style="font-weight:bold"');
      else h += hpT(44, y + 6, '', HPC.ink, 16) + `<line x1="44" y1="${y + 6}" x2="200" y2="${y + 6}" style="stroke:${HPC.ink};stroke-dasharray:3 3"/>` + hpT(210, y + 4, '(blank)', HPC.dim, 10);
    });
    h += hpT(44, 470, 'TODAY IS DAY ' + f.day, HPC.dim, 12);
    h += hpT(44, 490, 'FILE IN THE MATCHING TAB.', HPC.dim, 10);
  } else {
    h += hpT(154, 280, HPG.res === 'win' ? 'SIGNED OFF' : 'SENT BACK', HPG.res === 'win' ? HPC.ok : HPC.bad, 20, 'middle', 'style="font-weight:bold"');
  }
  // checklist
  h += hpT(304, 96, 'CHECKLIST', HPC.ink, 16, 'start', 'style="font-weight:bold"');
  h += hpT(504, 96, 'NEED ' + MINI_HP_PASS, HPC.dim, 10, 'end');
  for (let i = 0; i < MINI_HP_FORMS; i++) {
    const y = 120 + i * 31;
    const done = HPG.marks && HPG.marks[i] !== undefined;
    h += hpRc(306, y - 15, 20, 20, 'none', HPC.ink, 2);
    if (done) {
      const ok = HPG.marks[i];
      h += `<path d="${ok ? 'M309 ' + (y - 5) + ' l6 7 l11 -16' : 'M310 ' + (y - 12) + ' l10 14 M320 ' + (y - 12) + ' l-10 14'}" style="fill:none;stroke:${ok ? HPC.ok : HPC.bad};stroke-width:3;stroke-linecap:round"/>`;
    }
    h += hpT(338, y, 'FORM ' + (i + 1), !HPG.res && i === HPG.idx ? HPC.ink : HPC.dim, 13, 'start', !HPG.res && i === HPG.idx ? 'style="font-weight:bold"' : '');
    if (!HPG.res && i === HPG.idx) h += `<line x1="338" y1="${y + 3}" x2="410" y2="${y + 3}" style="stroke:${HPC.ink};stroke-width:2"/>`;
  }
  // scanner timer
  const left = Math.max(0, HPG.endAt - performance.now());
  h += hpRc(592, 28, 148, 70, '#1b2229', '#566673', 6);
  h += hpRc(600, 36, 132, 36, '#0a1a10', '#2b4d38', 3);
  h += hpT(666, 63, HPG.res ? '--:--' : fmt(left), left < 15000 && !HPG.res ? '#ff6a5a' : '#5dffa0', 24, 'middle');
  h += hpT(666, 90, 'FLATBED TIMER', '#8fa6bb', 9, 'middle');
  // counters
  h += hpT(592, 130, 'CORRECT', '#e6dfc8', 11);
  h += hpT(740, 130, HPG.ok + ' / ' + MINI_HP_PASS, '#8cf0a8', 14, 'end');
  h += hpT(592, 152, 'MISTAKES (FAIL AT ' + (MINI_HP_MISS + 1) + ')', '#e6dfc8', 11);
  h += hpT(740, 152, String(HPG.bad), HPG.bad >= MINI_HP_MISS ? '#ff8f8f' : '#ffd36a', 14, 'end');
  // deny stamp
  const fd = HPG.fl && now < HPG.fl.t && HPG.fl.k === 'deny';
  h += hpRc(592, 176, 148, 66, '#8a2a22', fd ? (HPG.fl.ok ? '#5dffa0' : '#ffffff') : '#4a120e', 8, `onpointerdown="hpTabClick('deny')"`);
  h += hpT(666, 216, 'D  DENY', '#ffe3df', 20, 'middle', 'pointer-events="none" style="font-weight:bold;fill:#ffe3df;font-family:\'Courier New\',monospace;font-size:20px;text-anchor:middle"');
  // sticky note
  const note = HPG.last ? HPG.last : 'File what is right. Deny what is not.';
  h += `<polygon points="592,262 740,258 744,390 596,394" style="fill:${HPG.last && !HPG.lastOk ? '#ffb9a8' : '#ffe27a'};stroke:#00000033"/>`;
  hpWrap(note, 17).slice(0, 7).forEach((l, i) => { h += hpT(602, 284 + i * 16, l, '#3a3210', 12); });
  h += hpT(736, 384, '- G. HAMMOND', '#5a4f1a', 10, 'end');
  // pen
  h += `<g transform="translate(600 440) rotate(-8)"><rect width="130" height="9" rx="4" style="fill:#1c2a3a;stroke:#0a111a"/><rect x="100" width="22" height="9" style="fill:#c9ced3"/><polygon points="130,0 144,4.5 130,9" style="fill:#d6c7a0"/></g>`;
  // walk away
  h += hpRc(592, 478, 148, 36, 'rgba(0,0,0,.35)', '#8fa6bb', 6, 'onpointerdown="hpClose()"');
  h += hpT(666, 501, 'WALK AWAY', '#d8e6f0', 13, 'middle', 'pointer-events="none" style="fill:#d8e6f0;font-size:13px;text-anchor:middle;font-family:\'Courier New\',monospace"');
  // result overlay
  if (HPG.res) {
    h += `<rect width="760" height="540" style="fill:rgba(0,0,0,.55)"/>`;
    h += hpRc(130, 130, 500, 250, '#ece5cc', '#241d10', 8);
    const win = HPG.res === 'win';
    h += hpT(380, 176, win ? 'PAPERWORK SIGNED' : 'PAPERWORK REJECTED', win ? HPC.ok : HPC.bad, 24, 'middle', 'style="font-weight:bold;fill:' + (win ? HPC.ok : HPC.bad) + ';font-size:24px;text-anchor:middle;font-family:\'Courier New\',monospace"');
    const msg = win ? 'Hammond signs off. +' + MINI_HP_SUP + ' supplies. The next ' + MINI_HP_CHARGES + ' missions that include a Logistic Truck, launched within ' + fmt(MINI_HP_WINDOW) + ', carry ' + Math.round(MINI_HP_BOOST * 100) + '% more supplies.' : 'Hammond sends it back: ' + HPG.ok + ' correct, ' + HPG.bad + ' wrong. You need ' + MINI_HP_PASS + ' correct with no more than ' + MINI_HP_MISS + ' mistakes. There is no cooldown on a retry.';
    hpWrap(msg, 50).forEach((l, i) => { h += hpT(160, 214 + i * 20, l, HPC.ink, 14); });
    if (win) {
      h += hpRc(300, 320, 160, 40, '#2f8f4a', '#154a26', 6, 'onpointerdown="hpClose()"') + hpT(380, 346, 'CLOSE', '#fff', 16, 'middle', 'pointer-events="none" style="fill:#fff;font-size:16px;text-anchor:middle;font-family:\'Courier New\',monospace"');
    } else {
      h += hpRc(220, 320, 160, 40, '#2f8f4a', '#154a26', 6, 'onpointerdown="hpClose();hpOpen()"') + hpT(300, 346, 'TRY AGAIN', '#fff', 16, 'middle', 'pointer-events="none" style="fill:#fff;font-size:16px;text-anchor:middle;font-family:\'Courier New\',monospace"');
      h += hpRc(400, 320, 160, 40, '#555', '#222', 6, 'onpointerdown="hpClose()"') + hpT(480, 346, 'CLOSE', '#fff', 16, 'middle', 'pointer-events="none" style="fill:#fff;font-size:16px;text-anchor:middle;font-family:\'Courier New\',monospace"');
    }
  }
  $('hpsvg').innerHTML = h;
}
function hpWrap(t, n) {
  const out = [];
  let cur = '';
  t.split(' ').forEach(w => {
    if ((cur + ' ' + w).trim().length > n) { out.push(cur); cur = w; } else cur = (cur + ' ' + w).trim();
  });
  if (cur) out.push(cur);
  return out;
}

document.addEventListener('keydown', e => {
  if (!HPG || !HPG.res || e.key !== 'Enter') return;
  e.preventDefault();
  e.stopImmediatePropagation();
  if (HPG.res === 'win') hpClose();
  else { hpClose(); hpOpen(); }
}, true);
