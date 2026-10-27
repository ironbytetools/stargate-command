function rxFeed() {
  const r = state.rx;
  const f = RXG.frame;
  let core = RXC.ok;
  let gate = RXC.ok;
  if (!RXG.done) {
    if (RXG.reason === 'evt') {
      core = (f % 4 < 2 || f % 7 === 0) ? RXC.bad : 'rgba(255,90,90,.25)';
      gate = (f % 5 < 3) ? RXC.warn : 'rgba(255,184,74,.25)';
    } else if (RXG.reason === 'node') {
      core = RXC.warn;
    } else if (r.off === 'gate') {
      gate = RXC.bad;
    }
  }
  return `<circle cx="428" cy="17" r="6" style="fill:${core}"/>` + rxT(438, 21, 'CORE', RXC.dim, 10) + `<circle cx="490" cy="17" r="6" style="fill:${gate}"/>` + rxT(500, 21, 'GATE', RXC.dim, 10);
}

function rxDoneDraw() {
  const keys = Object.keys(RX_PRESETS);
  let h = rxT(280, 78, 'THE REACTOR IS STABLE', RXC.ok, 20, 'middle');
  h += rxT(280, 104, 'CHOOSE HOW POWER IS SPLIT. CHANGE IT ANY TIME AT THE QUARTERMASTER.', RXC.dim, 11, 'middle');
  keys.forEach((k, i) => {
    const x = 60 + (i % 2) * 230;
    const y = 130 + Math.floor(i / 2) * 62;
    const on = state.rx.preset === k;
    h += rxR(x, y, 210, 50, on ? 'rgba(127,251,255,.2)' : 'rgba(0,0,0,.4)', on ? RXC.g : RXC.st, `onpointerdown="rxPreset('${k}')"`);
    h += rxT(x + 105, y + 31, (i + 1) + '  ' + RX_PRESETS[k].name.toUpperCase(), on ? RXC.g : RXC.a, 14, 'middle', 'pointer-events="none"');
  });
  h += rxT(280, 280, RX_PRESETS[state.rx.preset].desc, RXC.a, 12, 'middle');
  h += rxR(190, 304, 180, 40, 'rgba(93,255,160,.18)', RXC.ok, 'onpointerdown="rxAbandon()"');
  h += rxT(280, 330, 'CONTINUE', RXC.ok, 16, 'middle', 'pointer-events="none"');
  return h;
}

function rxHelpDraw() {
  const lines = RX_HELP[RXG.k] || [];
  let h = rxR(20, 44, 520, 316, 'rgba(2,10,16,.96)', RXC.a);
  h += rxT(40, 74, 'HELP // ' + RX_NAMES[RXG.k], RXC.g, 15);
  lines.forEach((l, i) => { h += rxT(40, 108 + i * 24, l, RXC.a, 13); });
  h += rxT(280, 346, 'PRESS INFO TO RETURN', RXC.dim, 12, 'middle');
  return h;
}

function rxDraw() {
  if (!RXG) return;
  const svg = $('rxsvg');
  if (!svg) return;
  const n = RXG.stages.length;
  const sNo = Math.min(RXG.si + 1, n);
  let h = `<rect x="0" y="0" width="560" height="380" style="fill:${RXC.bg}"/>`;
  h += `<rect x="0" y="0" width="560" height="34" style="fill:rgba(127,251,255,.1)"/><line x1="0" y1="34" x2="560" y2="34" style="stroke:${RXC.st}"/>`;
  h += rxT(12, 22, RXG.done ? 'ROUTING COMPLETE' : RX_NAMES[RXG.k], RXG.done ? RXC.ok : RXC.g, 14);
  if (!RXG.done) {
    h += rxT(280, 22, 'STAGE ' + sNo + ' / ' + n, RXC.dim, 12, 'middle');
    for (let i = 0; i < n; i++) h += `<circle cx="${350 + i * 16}" cy="17" r="4.5" style="fill:${i < RXG.si ? RXC.ok : (i === RXG.si ? RXC.a : 'none')};stroke:${RXC.dim}"/>`;
  }
  h += rxFeed();
  if (RXG.done) h += rxDoneDraw();
  else if (RXG.trans > 0) {
    h += rxT(280, 170, 'STAGE ' + RXG.si + ' COMPLETE', RXC.ok, 26, 'middle');
    h += rxT(280, 204, 'NEXT: ' + RX_NAMES[RXG.stages[RXG.si]], RXC.a, 15, 'middle');
  } else {
    h += RX_DRAW[RXG.k]();
    if (RXG.info) h += rxHelpDraw();
  }
  if (!RXG.done) {
    if (RXG.abort > 0) h += rxT(280, 372, 'PRESS ABORT AGAIN // AN OUTPUT WILL GO OFFLINE', RXC.bad, 12, 'middle');
    else h += rxT(10, 372, 'INFO = HELP', RXC.dim, 10) + rxT(550, 372, RXG.reason === 'evt' ? 'ABORT x2 = GIVE UP' : 'ABORT = LEAVE (KEEPS PROGRESS)', RXC.dim, 10, 'end');
  }
  svg.innerHTML = h;
  const kn = RX_USEKN[RXG.k];
  for (let i = 0; i < 3; i++) {
    const el = $('rxkn' + i);
    if (!el) continue;
    const use = !!kn && !RXG.done && !RXG.trans;
    el.className = 'rxknob' + (use ? '' : ' off') + (use && RXG.sel === i ? ' sel' : '');
    $('rxdial' + i).style.transform = 'rotate(' + (-135 + RXG.kn[i] * 2.7) + 'deg)';
    $('rxknl' + i).textContent = kn ? kn[i] : '--';
  }
}
