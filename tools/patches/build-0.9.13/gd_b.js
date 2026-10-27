const GDC = { t: '#3fe0d0', y: '#f3e9a8', a: '#ffb84a', ok: '#5dffa0', bad: '#ff6a5a', dim: '#3d8a84', bg: '#010a0b' };
function gdT(x, y, txt, col, size, anchor) { return rxT(x, y, txt, col, size, anchor); }
function gdWrap(t, n) {
  const out = [];
  let cur = '';
  t.split(' ').forEach(w => {
    if ((cur + ' ' + w).trim().length > n) { out.push(cur); cur = w; } else cur = (cur + ' ' + w).trim();
  });
  if (cur) out.push(cur);
  return out;
}
function gdHintLines() {
  const f = Math.min(3, glArt(GLG.n).fails);
  const hs = GL_HINTS[GLG.type].slice(Math.max(0, f - 2), f);
  let lines = [];
  hs.forEach(h => { lines = lines.concat(gdWrap(h.toUpperCase(), 66)); });
  return lines.slice(0, 5);
}
function gdG(edges, x, y, size, col) { return glInscLines(edges, x, y, size / 60, col, 3.6); }

function gdMon() {
  const i = GLG.i;
  const ar = GL_ARTS[GLG.n - 1];
  const fr = GLG.frame || 0;
  let h = `<rect width="450" height="300" style="fill:${GDC.bg}"/>`;
  h += gdT(14, 22, 'TRANSLATION MODE' + (fr % 10 < 5 ? '_' : ''), GDC.t, 15);
  h += gdT(436, 22, ar.name.toUpperCase(), GDC.dim, 10, 'end');
  h += `<line x1="10" y1="31" x2="440" y2="31" style="stroke:${GDC.dim}"/>`;
  let status = 'UNIDENTIFIED SOURCE! ' + (fr % 10 < 6 ? '_TRACE' : '');
  let scol = GDC.a;
  const mk = GLG.mark;
  if (GLG.res === 'fail') {
    h += gdT(225, 100, 'TRACE FAILED', GDC.bad, 26, 'middle');
    h += gdT(225, 134, 'THIS TABLET DEFEATED YOU. THERE IS NO PENALTY.', GDC.t, 12, 'middle');
    h += gdT(225, 154, 'PRESS ENTER FOR A FRESH TABLET.', GDC.y, 12, 'middle');
    status = 'TRACE FAILED';
    scol = GDC.bad;
  } else if (GLG.res === 'win') {
    status = 'CODE ACCEPTED';
    scol = GDC.ok;
    if (mk && !mk.done) {
      h += gdT(225, 62, 'SEAL DETECTED', GDC.y, 20, 'middle');
      h += gdT(225, 78, 'COMPARE THE SEAL ON THE TRAY.', GDC.t, 10, 'middle');
      h += gdT(225, 91, 'PRESS THE KEY OF THE LORD WHO CARVED IT.', GDC.t, 10, 'middle');
      LORDS.forEach((l, k) => {
        const x = 12 + k * 86;
        h += rxR(x, 102, 80, 108, 'rgba(63,224,208,.06)', GDC.dim);
        h += gdMarkSvg(k, x + 20, 108, 40, GDC.y, 3.4);
        h += gdT(x + 40, 168, l.n.toUpperCase(), GDC.t, 11, 'middle');
        h += gdT(x + 40, 200, 'KEY ' + (k + 1), GDC.dim, 10, 'middle');
      });
      h += gdT(225, 228, 'CLEAR = SKIP // NO PENALTY EITHER WAY', GDC.dim, 10, 'middle');
    } else {
      h += gdT(225, 62, 'INSCRIPTION DECODED', GDC.ok, 20, 'middle');
      let y = 88;
      gdWrap(ar.lore, 62).concat([''], gdWrap(GLG.out || '', 62)).forEach(l => { h += gdT(14, y, l, GDC.y, 11); y += 15; });
      if (mk && mk.ok === true) h += gdT(14, y + 6, 'SEAL IDENTIFIED: ' + LORDS[mk.lv - 1].n.toUpperCase() + '. STRONGHOLD LOCATED.', GDC.ok, 11);
      else if (mk && mk.ok === false) h += gdT(14, y + 6, 'THE SEAL COULD NOT BE IDENTIFIED.', GDC.a, 11);
      h += gdT(225, 262, 'PRESS ENTER OR CLOSE', GDC.dim, 11, 'middle');
    }
  } else if (GLG.type === 1) {
    const cur = gd1Cur();
    for (let k = 0; k < 6; k++) {
      const x = 9 + k * 72;
      const pd = i.paired[k];
      h += rxR(x, 48, 64, 64, pd ? 'rgba(93,255,160,.1)' : 'rgba(63,224,208,.05)', pd ? GDC.ok : (k === cur ? GDC.y : GDC.dim));
      h += gdG(glKey(i.gs[k]) && i.gs[k], x + 6, 54, 52, pd ? GDC.ok : GDC.y);
      if (k === cur) h += `<path d="M${x + 32} 122 l-7 8 h14 z" style="fill:${GDC.y}"/>`;
    }
    h += gdT(14, 160, 'FIND THE FRAGMENT CUT FROM THE MARKED GLYPH.', GDC.t, 11);
    h += gdT(14, 178, 'PRESS ITS KEY. D-PAD CHANGES THE MARKED GLYPH.', GDC.dim, 10);
    h += gdT(14, 200, 'MISTAKES LEFT: ' + (i.max - i.miss), (i.max - i.miss) <= 1 ? GDC.bad : GDC.a, 12);
    if (GLG.vis) h += gdT(436, 200, 'LIBRARY BOOK: KEY ' + (i.order.findIndex(k => k === cur) + 1), GDC.ok, 12, 'end');
  } else if (GLG.type === 2) {
    gdWrap('MOVE THE CURSOR OVER THE TRAY TABLET WITH THE D-PAD. ENTER PICKS A TILE, THEN ENTER ON ANOTHER TILE SWAPS THEM. LOCKED TILES ARE ALREADY SET.', 34).forEach((l, k) => { h += gdT(14, 54 + k * 16, l, GDC.t, 11); });
    h += gdT(14, 160, 'MOVES LEFT: ' + (i.max - i.moves), (i.max - i.moves) <= 3 ? GDC.bad : GDC.a, 14);
    if (GLG.vis) {
      h += `<svg x="320" y="46" width="110" height="110" viewBox="0 0 150 150">${i.content}</svg>`;
      h += gdT(375, 172, 'LIBRARY BOOK', GDC.ok, 10, 'middle');
    }
  } else {
    h += gdT(14, 50, 'FIND THE 4-GLYPH CODE. NO GLYPH REPEATS.', GDC.t, 11);
    h += gdT(14, 64, 'GREEN: RIGHT PLACE // AMBER: WRONG PLACE', GDC.dim, 10);
    for (let s = 0; s < 4; s++) {
      const x = 14 + s * 52;
      const v = i.cur[s];
      h += rxR(x, 74, 46, 46, 'rgba(63,224,208,.05)', i.known.includes(s) ? GDC.ok : GDC.dim);
      if (v >= 0) h += gdG(i.gl[v], x + 4, 78, 38, i.known.includes(s) ? GDC.ok : GDC.y);
      else h += gdT(x + 23, 104, '?', GDC.dim, 18, 'middle');
    }
    h += gdT(436, 98, 'GUESSES LEFT: ' + (i.max - i.hist.length), GDC.a, 12, 'end');
    h += gdT(436, 114, 'ENTER SUBMITS // CLEAR BACKSPACES', GDC.dim, 9, 'end');
    const rows = i.hist.slice(-5);
    rows.forEach((r, n) => {
      const y = 130 + n * 20;
      r.g.forEach((v, s) => { h += gdG(i.gl[v], 14 + s * 22, y - 2, 18, r.g[s] === i.code[s] ? GDC.ok : (i.code.includes(v) ? GDC.a : GDC.y)); });
      h += gdT(112, y + 13, r.e + ' EXACT // ' + r.p + ' MISPLACED', GDC.dim, 10);
    });
  }
  if (!GLG.res) {
    let y = 232;
    gdHintLines().forEach(l => { h += gdT(14, y, l, GDC.a, 9.5); y += 11; });
  }
  h += `<rect x="0" y="280" width="450" height="20" style="fill:rgba(63,224,208,.18)"/>`;
  h += gdT(10, 294, status, scol, 11);
  h += gdT(440, 294, 'ATTEMPT ' + (glArt(GLG.n).fails + 1), GDC.dim, 10, 'end');
  return h;
}

function gdShard(j, cx, cy, edges, on, pd, cur) {
  const r = 34;
  const pts = [];
  for (let a = 0; a < 7; a++) {
    const ang = a / 7 * Math.PI * 2 + j;
    const rr = r * (0.75 + 0.25 * Math.sin(a * 2.3 + j * 1.7));
    pts.push((cx + Math.cos(ang) * rr).toFixed(1) + ',' + (cy + Math.sin(ang) * rr).toFixed(1));
  }
  let s = `<polygon points="${pts.join(' ')}" style="fill:${pd ? '#26231a' : '#5b5240'};stroke:${pd ? '#3a3527' : '#2a2518'};stroke-width:2;opacity:${pd ? .45 : 1}"/>`;
  if (!pd) s += glInscLines(edges, cx - 20, cy - 22, 40 / 60, '#e8d79a', 3.8);
  s += gdT(cx - 28, cy - 22, j + 1, '#ffcf6a', 12);
  if (cur) s += `<polygon points="${pts.join(' ')}" style="fill:none;stroke:#ffcf6a;stroke-width:2;stroke-dasharray:4 3"/>`;
  return s;
}

function gdTray() {
  const i = GLG.i;
  let h = `<defs><radialGradient id="gdglow" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="#ffcf6a" stop-opacity=".55"/><stop offset="1" stop-color="#2a1a06" stop-opacity=".9"/></radialGradient></defs>`;
  h += `<rect width="224" height="300" style="fill:url(#gdglow)"/>`;
  h += gdT(112, 20, 'ARTIFACT TRAY', '#ffe7a8', 11, 'middle');
  const mk = GLG.mark;
  if (GLG.res === 'win' && mk && !mk.done) {
    h += `<rect x="30" y="50" width="164" height="190" rx="8" style="fill:#5b5240;stroke:#2a2518;stroke-width:3"/>`;
    h += gdMarkSvg(mk.lv - 1, 52, 80, 120, '#e8d79a', 3.8);
    h += gdT(112, 262, 'SEAL', '#ffe7a8', 11, 'middle');
    return h;
  }
  if (GLG.type === 1) {
    const cur = gd1Cur();
    i.order.forEach((k, j) => {
      const cx = 60 + (j % 2) * 104;
      const cy = 76 + Math.floor(j / 2) * 78;
      h += gdShard(j, cx, cy, i.fr[k], true, i.paired[k], k === cur && GLG.vis);
    });
  } else if (GLG.type === 2) {
    const c = gd2Cur();
    for (let s = 0; s < 9; s++) {
      const t = i.pos[s];
      const x = 10 + (s % 3) * 70;
      const y = 44 + Math.floor(s / 3) * 70;
      h += `<svg x="${x}" y="${y}" width="68" height="68" viewBox="${(t % 3) * 50} ${Math.floor(t / 3) * 50} 50 50" onpointerdown="gdTile(${s})" style="cursor:pointer">${i.content}</svg>`;
      if (i.lock.includes(s)) h += `<rect x="${x}" y="${y}" width="68" height="68" style="fill:rgba(93,255,160,.12);stroke:#5dffa0;stroke-width:2;pointer-events:none"/>`;
      if (i.sel === s) h += `<rect x="${x + 2}" y="${y + 2}" width="64" height="64" style="fill:rgba(255,207,106,.25);stroke:#ffcf6a;stroke-width:3;pointer-events:none"/>`;
      if (c === s) h += `<rect x="${x - 1}" y="${y - 1}" width="70" height="70" style="fill:none;stroke:#3fe0d0;stroke-width:2.5;pointer-events:none"/>`;
    }
  } else {
    h += `<rect x="14" y="50" width="196" height="190" rx="8" style="fill:#5b5240;stroke:#2a2518;stroke-width:3"/>`;
    i.gl.forEach((g, j) => {
      const x = 24 + (j % 2) * 94;
      const y = 62 + Math.floor(j / 3 * 1) * 0;
      const yy = 62 + Math.floor(j / 2) * 58;
      const used = i.cur.includes(j);
      h += glInscLines(g, x + 8, yy, 44 / 60, used ? '#7d7152' : '#e8d79a', 3.8);
      h += gdT(x, yy + 14, j + 1, '#ffcf6a', 11);
    });
  }
  return h;
}

function gdDraw() {
  if (!GLG || !$('gdsvg')) return;
  $('gdsvg').innerHTML = gdMon();
  $('gdtsvg').innerHTML = gdTray();
  const i = GLG.i;
  const mk = GLG.mark;
  for (let j = 0; j < 6; j++) {
    const el = $('gdk' + j);
    if (!el) continue;
    let face = '';
    let cls = 'gdk';
    if (GLG.res === 'win') {
      if (mk && !mk.done && j < 5) face = gdMarkHtml(j, 42);
      else cls += ' off';
    } else if (GLG.res) cls += ' off';
    else if (GLG.type === 1) {
      const k = i.order[j];
      face = glSvg(i.fr[k], 42);
      if (i.paired[k]) cls += ' off';
      if (i.flash === j) cls += ' bad';
      if (GLG.vis && k === gd1Cur()) cls += ' hint';
    } else if (GLG.type === 3) {
      face = glSvg(i.gl[j], 42);
      if (i.cur.includes(j)) cls += ' off';
      if (GLG.vis && i.code.includes(j)) cls += ' hint';
    } else cls += ' off';
    el.className = cls;
    el.innerHTML = face + '<i>' + (j + 1) + '</i>';
  }
  const bk = document.querySelector('#gdside .book');
  if (bk) bk.className = 'gds book' + (GLG.vis || GLG.res ? ' off' : '');
}
