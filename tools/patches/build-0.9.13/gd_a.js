const GD_MARKS = [
  'M14 46 C12 30 28 28 30 38 C32 50 46 48 46 34 C46 24 38 16 28 18 M28 18 L19 12 L21 24 Z',
  'M8 48 L8 24 L20 34 L30 10 L40 34 L52 24 L52 48 Z M8 54 H52',
  'M30 18 m-14 0 a14 14 0 1 0 28 0 a14 14 0 1 0 -28 0 M22 6 Q30 -2 38 6 M30 4 V46 M14 50 Q22 58 30 50 Q38 58 46 50',
  'M30 24 m-8 0 a8 8 0 1 0 16 0 a8 8 0 1 0 -16 0 M22 30 L3 22 L8 36 L21 38 M38 30 L57 22 L52 36 L39 38 M30 34 V54 M23 54 H37',
  'M17 6 L24 26 L10 44 L30 56 L50 44 L36 26 L43 6 L30 20 Z'
];
function gdMarkSvg(i, x, y, size, col, sw) {
  return `<g transform="translate(${x} ${y}) scale(${size / 60})" style="fill:none;stroke:${col};stroke-width:${sw || 3.2};stroke-linecap:round;stroke-linejoin:round"><path d="${GD_MARKS[i]}"/></g>`;
}
function gdMarkHtml(i, size) {
  return `<svg viewBox="0 0 60 60" width="${size}" height="${size}" class="glsvg"><path d="${GD_MARKS[i]}" style="fill:none;stroke:currentColor;stroke-width:3.4;stroke-linecap:round;stroke-linejoin:round"/></svg>`;
}
function gdLordWorld(n) {
  const ar = GL_ARTS[n - 1];
  const name = LORDS[ar.lv - 1].n;
  return state.worlds.find(w => w.lord === name && w.stronghold && w.status !== 'captured' && w.intel < 2) || null;
}
function gdMarkInit() {
  const lw = gdLordWorld(GLG.n);
  GLG.mark = lw ? { lv: GL_ARTS[GLG.n - 1].lv, wid: lw.id, done: false } : null;
}
function gdMarkPick(j) {
  const m = GLG.mark;
  if (!m || m.done || j > 4) return;
  m.done = true;
  const lord = LORDS[m.lv - 1].n;
  if (j === m.lv - 1) {
    const w = state.worlds.find(x => x.id === m.wid);
    if (w && w.intel < 2) w.intel = 2;
    m.ok = true;
    log('The seal on the inscription is the mark of ' + lord + '. His stronghold at ' + (w ? wname(w) : 'the system') + ' is now known.', 'ok');
    sfx.chime();
  } else {
    m.ok = false;
    log('The seal on the inscription could not be identified.', '');
    sfx.fail();
  }
  glRender();
  renderAll();
}

function gdBuild() {
  const keys = [0, 1, 2, 3, 4, 5].map(j => `<button class="gdk" id="gdk${j}" onclick="gdKey(${j})"></button>`).join('');
  const pad = [['up', '▲', 2], ['left', '◀', 4], ['enter', 'ENTER', 5], ['right', '▶', 6], ['down', '▼', 8]].map(p => `<button class="gdp gdp-${p[0]}" onclick="gdPad('${p[0]}')">${p[1]}</button>`).join('');
  const side = [['book', 'BOOK'], ['clear', 'CLEAR'], ['giveup', 'GIVE UP'], ['close', 'CLOSE']].map(s => `<button class="gds ${s[0]}" onclick="gdSide('${s[0]}')">${s[1]}</button>`).join('');
  $('glbody').innerHTML = `<div id="gdfit"><div id="gddev">
    <div id="gdmon"><svg id="gdsvg" viewBox="0 0 450 300" width="450" height="300"></svg></div>
    <div id="gdtray"><svg id="gdtsvg" viewBox="0 0 224 300" width="224" height="300"></svg></div>
    <div id="gdkeys">${keys}</div><div id="gdpad">${pad}</div><div id="gdside">${side}</div>
  </div></div>`;
}

function gdFit() {
  const f = $('gdfit');
  const host = $('glbody');
  if (!f || !host || !GLG) return;
  const w = host.clientWidth;
  const h = host.clientHeight;
  if (!w || !h) return;
  GLG.fw = w;
  GLG.fh = h;
  const s = Math.min(1.25, w / 760, h / 540);
  GLG.scale = s;
  f.style.width = Math.floor(760 * s) + 'px';
  f.style.height = Math.floor(540 * s) + 'px';
  $('gddev').style.transform = 'scale(' + s + ')';
}
setInterval(() => {
  if (!GLG || $('glgame').offsetParent === null) return;
  const host = $('glbody');
  if (host && (host.clientWidth !== GLG.fw || host.clientHeight !== GLG.fh)) gdFit();
  GLG.frame = (GLG.frame || 0) + 1;
  if (GLG.frame % 5 === 0 && !GLG.res) gdDraw();
}, 100);
window.addEventListener('resize', () => { if (GLG) gdFit(); });

function glLibrary() {
  if (!GLG || GLG.vis || GLG.res) return;
  GLG.vis = true;
  glRender();
}

function glRender() {
  if (!GLG) return;
  const ar = GL_ARTS[GLG.n - 1];
  $('gltitle').textContent = GLG.res === 'win' ? 'INSCRIPTION DECODED' : 'DECODE // ' + ar.name.toUpperCase();
  $('glsub').textContent = GL_TYPES[GLG.type] + ' // ATTEMPT ' + (glArt(GLG.n).fails + 1) + ' // LEVEL ' + ar.lv;
  if (!$('gddev')) gdBuild();
  if (!GLG.scale) gdFit();
  gdDraw();
}

function glWin() {
  if (!GLG) return;
  GLG.res = 'win';
  glDecoded(GLG.n);
  gdMarkInit();
  glRender();
  renderAll();
}

function gdKey(j) {
  if (!GLG) return;
  if (GLG.res === 'win') { if (GLG.mark && !GLG.mark.done) gdMarkPick(j); return; }
  if (GLG.res) return;
  if (GLG.type === 1) gd1Key(j);
  else if (GLG.type === 3) gd3Key(j);
  gdDraw();
}
function gdPad(b) {
  if (!GLG) return;
  if (GLG.res === 'fail') { if (b === 'enter') glRetry(); return; }
  if (GLG.res === 'win') { if (b === 'enter' && (!GLG.mark || GLG.mark.done)) glClose(); return; }
  if (GLG.type === 1) gd1Pad(b);
  else if (GLG.type === 2) gd2Pad(b);
  else if (b === 'enter') glGuess3();
  if (GLG && !GLG.res) gdDraw();
}
function gdSide(b) {
  if (!GLG) return;
  if (b === 'close') { glClose(); return; }
  if (GLG.res === 'win') { if (b === 'clear' && GLG.mark && !GLG.mark.done) { GLG.mark.done = true; GLG.mark.ok = null; glRender(); } return; }
  if (GLG.res) return;
  if (b === 'book') glLibrary();
  else if (b === 'giveup') glFail();
  else if (b === 'clear' && GLG.type === 3) gd3Clear();
  if (GLG && !GLG.res) gdDraw();
}

document.addEventListener('keydown', e => {
  if (!GLG || $('glgame').offsetParent === null || e.key === 'Escape') return;
  const eat = () => { e.preventDefault(); e.stopImmediatePropagation(); };
  const k = e.key;
  const map = { ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right', Enter: 'enter', ' ': 'enter' };
  if (map[k]) { eat(); gdPad(map[k]); return; }
  if (k === 'Backspace' || k === 'Delete') { eat(); gdSide('clear'); return; }
  if (k === 'b' || k === 'B') { eat(); gdSide('book'); return; }
  if (/^[1-6]$/.test(k)) { eat(); gdKey(+k - 1); }
}, true);

// ----- fragment matching -----
function gd1Next(from) {
  const i = GLG.i;
  for (let s = 0; s < 6; s++) {
    const k = (from + s) % 6;
    if (!i.paired[k]) return k;
  }
  return -1;
}
function gd1Cur() {
  const i = GLG.i;
  if (i.cur === undefined || i.cur < 0 || i.paired[i.cur]) i.cur = gd1Next(0);
  return i.cur;
}
function gd1Key(j) {
  const i = GLG.i;
  const cur = gd1Cur();
  const k = i.order[j];
  if (cur < 0 || i.paired[k]) return;
  if (k === cur) {
    i.paired[k] = true;
    i.flash = -1;
    sfx.tick();
    if (i.paired.every(Boolean)) { glWin(); return; }
    i.cur = gd1Next(cur + 1);
  } else {
    i.miss++;
    i.flash = j;
    sfx.fail();
    later(() => { if (GLG && GLG.i === i) { i.flash = -1; gdDraw(); } }, 600);
    if (i.miss >= i.max) glFail();
  }
}
function gd1Pad(b) {
  const i = GLG.i;
  const cur = gd1Cur();
  if (cur < 0) return;
  if (b === 'right' || b === 'down') i.cur = gd1Next(cur + 1);
  else if (b === 'left' || b === 'up') {
    for (let s = 1; s <= 6; s++) { const k = (cur + 6 - s) % 6; if (!i.paired[k]) { i.cur = k; break; } }
  }
}

// ----- tablet reassembly -----
function gd2Cur() {
  const i = GLG.i;
  if (i.cur === undefined) i.cur = [0, 1, 2, 3, 4, 5, 6, 7, 8].find(s => !i.lock.includes(s));
  return i.cur;
}
function gd2Pad(b) {
  const i = GLG.i;
  let c = gd2Cur();
  const x = c % 3;
  const y = Math.floor(c / 3);
  if (b === 'left') c = y * 3 + Math.max(0, x - 1);
  else if (b === 'right') c = y * 3 + Math.min(2, x + 1);
  else if (b === 'up') c = Math.max(0, y - 1) * 3 + x;
  else if (b === 'down') c = Math.min(2, y + 1) * 3 + x;
  else if (b === 'enter') { gd2Enter(c); return; }
  i.cur = c;
}
function gd2Enter(s) {
  const i = GLG.i;
  i.cur = s;
  if (i.lock.includes(s)) { sfx.fail(); return; }
  if (i.sel < 0) { i.sel = s; sfx.tick(); return; }
  if (i.sel === s) { i.sel = -1; return; }
  [i.pos[i.sel], i.pos[s]] = [i.pos[s], i.pos[i.sel]];
  i.sel = -1;
  i.moves++;
  sfx.tick();
  if (i.pos.every((v, k) => v === k)) { glWin(); return; }
  if (i.moves >= i.max) glFail();
}
function gdTile(s) {
  if (!GLG || GLG.type !== 2 || GLG.res) return;
  gd2Enter(s);
  if (GLG && !GLG.res) gdDraw();
}

// ----- cipher -----
function gd3Key(j) {
  const i = GLG.i;
  if (i.cur.includes(j)) return;
  const s = i.cur.findIndex(v => v === -1);
  if (s < 0) return;
  i.cur[s] = j;
  sfx.tick();
}
function gd3Clear() {
  const i = GLG.i;
  for (let s = 3; s >= 0; s--) {
    if (i.cur[s] !== -1 && !i.known.includes(s)) { i.cur[s] = -1; return; }
  }
}
