import re
import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.6') == 4, s.count('0.9.6')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.6</title>', '<title>Stargate Command 0.9.7</title>')
rep('BUILD 0.9.6', 'BUILD 0.9.7', 2)
rep("const BUILD_VER = '0.9.6';", "const BUILD_VER = '0.9.7';")

COM_JS = r'''function comFreqText(f) { return (30 + f * 482).toFixed(3); }

function comRadioHtml(g, w) {
  const K = (k, x, y, a, b, c) => `<button class="ak${c || ''}" data-ck="${k}" style="left:${x}px;top:${y}px">${a}${b ? '<small>' + b + '</small>' : ''}</button>`;
  let h = '<div class="asti"><div class="ahd l"></div><div class="ahd r"></div><div class="aface">';
  h += '<span class="alb" style="left:12px;top:6px">GPS</span><span class="alb" style="left:70px;top:6px">USB/KDU</span>';
  h += '<i class="apl" style="left:14px;top:20px;width:36px;height:36px"></i><i class="apl" style="left:72px;top:20px;width:48px;height:48px"></i>';
  h += '<span class="alb" style="left:24px;top:60px">J2</span><span class="alb" style="left:88px;top:72px">J4</span>';
  h += '<span class="alb" style="left:6px;top:94px;font-size:9px">225-2000 MHz</span><i class="apl big" style="left:18px;top:108px;width:72px;height:72px"></i><span class="alb" style="left:6px;top:184px">J8</span>';
  h += '<span class="alb" style="left:10px;top:206px;font-size:9px">30-512 MHz</span><i class="apl big" style="left:18px;top:220px;width:72px;height:72px"></i><span class="alb" style="left:6px;top:296px">J5</span>';
  h += '<div class="abz"><div class="alog">ASTI</div><div class="alcd">';
  h += '<div class="al1"><span>BAT <i class="bat"><b></b><b></b><b></b><b></b></i></span><span>SIG <i class="sig"><u id="combar"></u></i></span><span>' + (g.kind === 1 ? 'EMG' : 'CHK') + '</span></div>';
  h += '<div class="al2"><span class="alc">0' + g.kind + '-CUE</span><span id="comfq" class="alf"></span><span class="alu">MHZ</span></div>';
  h += '<canvas id="comscope" width="296" height="38"></canvas>';
  h += '<div class="al4"><span id="comstatus">STATIC</span><span id="comtimer"></span></div>';
  h += '<div class="al5"><span>' + wname(w).toUpperCase() + '</span><span>HAZ ' + (HAZ_LABEL[w.hazard] || '').toUpperCase() + '</span></div>';
  h += '</div></div>';
  h += K('vp', 120, 184, '+', 'VOL', ' sq') + K('vm', 120, 226, '&minus;', '', ' sq');
  h += K('d1', 172, 184, '1', 'ABC CALL') + K('d2', 254, 184, '2', 'DEF LT') + K('d3', 336, 184, '3', 'GHI MODE');
  h += K('d4', 172, 226, '4', 'JKL BDL') + K('d5', 254, 226, '5', 'MNO ZERO') + K('d6', 336, 226, '6', 'PQR PGM');
  h += K('d7', 172, 268, '7', 'STU OPT') + K('d8', 254, 268, '8', 'VWX PGM') + K('d9', 336, 268, '9', 'YZ PRT');
  h += K('pp', 418, 184, '+', 'PRE', ' sq') + K('pm', 418, 226, '&minus;', '', ' sq');
  h += K('clr', 120, 268, 'CLR', '', ' sq') + K('ent', 418, 268, 'ENT', '', ' sq');
  h += K('d0', 172, 310, '0', '') + K('fl', 254, 310, '&#9664;', 'FINE') + K('fr', 336, 310, '&#9654;', 'FINE');
  h += '<div id="comknob" class="akn" style="left:508px;top:34px"><div class="kd"><i></i></div></div>';
  ['OFF', 'CT', 'PT', 'LD', 'Z'].forEach((t, i) => { h += '<span class="alb" style="left:588px;top:' + (22 + i * 24) + 'px;font-size:11px">' + t + '</span>'; });
  h += '<span class="alb" style="left:520px;top:158px">J1</span><span class="alb" style="left:520px;top:172px;font-size:9px">AUDIO</span><i class="apl big" style="left:508px;top:192px;width:96px;height:96px"></i><i class="apl cab" style="left:526px;top:210px;width:60px;height:60px"></i>';
  h += '<i class="apl" style="left:524px;top:304px;width:44px;height:44px"></i><span class="alb" style="left:578px;top:318px">J7</span>';
  h += '</div></div>';
  return h;
}

function comSync() {
  const g = COMG;
  if (!g) return;
  const q = $('comfq');
  if (q) q.textContent = comFreqText(g.f);
  const k = $('comknob');
  if (k) k.firstChild.style.transform = 'rotate(' + (g.f * 270 - 135).toFixed(1) + 'deg)';
}

function comKeyAct(k) {
  if (!COMG || COMG.phase !== 'tune' || COMG.ended) return;
  const d = { fl: -0.01, fr: 0.01, vp: 0.002, vm: -0.002, pp: 0.05, pm: -0.05 }[k];
  noise(0.04, 0.04, 2600, 1800, 0, 1);
  if (d !== undefined) comNudge(d);
  else if (k === 'clr') comClose();
}

function comBindRadio() {
  document.querySelectorAll('#combody [data-ck]').forEach(b => {
    let t1 = 0;
    let t2 = 0;
    const stop = () => { clearTimeout(t1); clearInterval(t2); b.classList.remove('dn'); };
    b.addEventListener('pointerdown', e => {
      e.preventDefault();
      b.classList.add('dn');
      comKeyAct(b.dataset.ck);
      if (['fl', 'fr', 'vp', 'vm', 'pp', 'pm'].includes(b.dataset.ck)) t1 = setTimeout(() => { t2 = setInterval(() => comKeyAct(b.dataset.ck), 90); }, 350);
    });
    ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev => b.addEventListener(ev, stop));
  });
  const kn = $('comknob');
  if (kn) {
    let last = null;
    const ang = e => { const r = kn.getBoundingClientRect(); return Math.atan2(e.clientY - (r.top + r.height / 2), e.clientX - (r.left + r.width / 2)); };
    kn.addEventListener('pointerdown', e => { e.preventDefault(); last = ang(e); kn.setPointerCapture(e.pointerId); });
    kn.addEventListener('pointermove', e => {
      if (last === null) return;
      const a = ang(e);
      let d = a - last;
      if (d > Math.PI) d -= 2 * Math.PI;
      if (d < -Math.PI) d += 2 * Math.PI;
      last = a;
      comNudge(d / (1.5 * Math.PI) * 0.6);
    });
    ['pointerup', 'pointercancel'].forEach(ev => kn.addEventListener(ev, () => { last = null; }));
    kn.addEventListener('wheel', e => { e.preventDefault(); comNudge((e.deltaY < 0 ? 1 : -1) * 0.004); }, { passive: false });
  }
}

let comBr = 1;

function comUnit(html) {
  const old = $('comlcd');
  const top = old ? old.scrollTop : 0;
  const U = (k, x, y, w, h, a, c) => `<button class="uk${c || ''}" data-uk="${k}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px">${a}</button>`;
  let h = '<div class="cu"><div class="cunub"></div><i class="cuic pw"></i><i class="cuic al"></i>';
  h += '<div class="cuscr"><div id="comlcd"><div class="lh"><i></i><div><b>' + $('comtitle').textContent + '</b><span>' + $('comsub').textContent + '</span></div></div>' + html + '</div></div>';
  h += U('sp', 18, 58, 52, 44, 'VOL+', ' sm') + U('sm', 18, 112, 52, 44, 'VOL&minus;', ' sm') + U('grp', 18, 176, 52, 36, '1', ' sm');
  h += U('bp', 478, 58, 52, 44, 'BRT+', ' sm') + U('bm', 478, 112, 52, 44, 'BRT&minus;', ' sm') + U('grp2', 478, 176, 52, 36, '2', ' sm');
  h += U('grp', 24, 304, 52, 42, 'GRP', ' sm') + U('home', 86, 304, 56, 42, '&#8962;', '') + U('alt', 24, 358, 62, 42, 'ALT', ' sm') + U('x', 96, 358, 52, 42, '&#10005;', '');
  h += U('up', 236, 292, 52, 38, '&#9650;', '') + U('lf', 180, 332, 52, 38, '&#9664;', '') + '<i class="ukc" style="left:236px;top:332px"></i>' + U('rt', 292, 332, 52, 38, '&#9654;', '') + U('dn', 236, 372, 52, 38, '&#9660;', '');
  h += U('ok', 432, 304, 78, 42, '&#10003;', '') + U('bk', 432, 358, 78, 42, '&#8617;', '');
  h += U('a', 22, 424, 92, 54, 'A', ' big') + U('b', 124, 424, 92, 54, 'B', ' big') + U('c', 226, 424, 92, 54, 'C', ' big') + U('ic', 328, 424, 92, 54, 'IC', ' big') + U('or', 430, 424, 92, 54, 'O/R', ' big');
  h += '</div>';
  $('combody').innerHTML = h;
  const l = $('comlcd');
  l.scrollTop = top;
  l.style.filter = 'brightness(' + comBr + ')';
  document.querySelectorAll('#combody [data-uk]').forEach(b => {
    let t1 = 0;
    let t2 = 0;
    const stop = () => { clearTimeout(t1); clearInterval(t2); b.classList.remove('dn'); };
    b.addEventListener('pointerdown', e => {
      e.preventDefault();
      b.classList.add('dn');
      comUKey(b.dataset.uk);
      if (b.dataset.uk === 'up' || b.dataset.uk === 'dn') t1 = setTimeout(() => { t2 = setInterval(() => comUKey(b.dataset.uk), 80); }, 350);
    });
    ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev => b.addEventListener(ev, stop));
  });
  comTagKeys();
}

function comActBtns() {
  const l = $('comlcd');
  if (!l) return [];
  return [...l.querySelectorAll('button')].filter(b => !/^\s*CLOSE\s*$/i.test(b.textContent));
}

function comTagKeys() {
  comActBtns().forEach((b, i) => { if (i < 3) b.dataset.ak = 'ABC'[i]; else delete b.dataset.ak; });
}

function comUKey(k) {
  const l = $('comlcd');
  if (!l) return;
  noise(0.04, 0.04, 2400, 1700, 0, 1);
  if (k === 'up') l.scrollTop -= 46;
  else if (k === 'dn') l.scrollTop += 46;
  else if (k === 'ok') l.scrollTop += l.clientHeight - 30;
  else if (k === 'bk') l.scrollTop -= l.clientHeight - 30;
  else if (k === 'home') l.scrollTop = 0;
  else if (k === 'x' || k === 'or') comClose();
  else if (k === 'bp' || k === 'bm') { comBr = Math.max(0.6, Math.min(1.5, comBr + (k === 'bp' ? 0.15 : -0.15))); l.style.filter = 'brightness(' + comBr + ')'; }
  else if (k === 'a' || k === 'b' || k === 'c') { const bs = comActBtns(); const b = bs['abc'.indexOf(k)]; if (b) b.click(); }
}

new MutationObserver(comTagKeys).observe($('combody'), { childList: true, subtree: true });

function comRender() {
  const g = COMG;
  const w = world(g.wid);
  $('comtitle').textContent = g.kind === 1 ? 'COMM 1 // EMERGENCY CONTACT' : 'COMM 2 // CHECK-IN';
  $('comsub').textContent = wname(w).toUpperCase() + ' // HAZARD ' + (HAZ_LABEL[w.hazard] || '').toUpperCase();
  if (g.phase !== 'tune') { comUnit('<p class="dim">RECONNAISSANCE DRONE LAUNCHING</p>'); return; }
  $('combody').innerHTML = comRadioHtml(g, w);
  comBindRadio();
  comSync();
}

function comNudge(d) { if (COMG && COMG.phase === 'tune' && !COMG.ended) { COMG.f = Math.max(0, Math.min(1, COMG.f + d)); comSync(); } }
function comFreq(v) { if (COMG && COMG.phase === 'tune' && !COMG.ended) { COMG.f = +v / 1000; comSync(); } }

'''
i = s.index('function comRender() {')
j = s.index('function comFrame(now) {')
s = s[:i] + COM_JS + s[j:]

rep("""    c.fillStyle = '#050c14';
    c.fillRect(0, 0, W, H);
    c.strokeStyle = '#143247';""", """    c.clearRect(0, 0, W, H);
    c.strokeStyle = 'rgba(31,42,8,0.35)';""")
rep("    c.strokeStyle = inw ? '#6dffb0' : '#7ffbff';", "    c.strokeStyle = '#1d2608';")
rep("""    $('combody').innerHTML = '<p class="danger">SIGNAL LOST // THE WORMHOLE CLOSED BEFORE CONTACT WAS ESTABLISHED.</p><p class="dim">Dial the planet again and press the COM key.</p><div class="controls"><button onclick="comClose()">CLOSE</button></div>';
    $('comtitle').textContent = 'RADIO CONTACT FAILED';""", """    $('comtitle').textContent = 'RADIO CONTACT FAILED';
    comUnit('<p class="danger">SIGNAL LOST // THE WORMHOLE CLOSED BEFORE CONTACT WAS ESTABLISHED.</p><p class="dim">Dial the planet again and press the COM key.</p><div class="controls"><button onclick="comClose()">CLOSE</button></div>');""")
rep("""  $('combody').innerHTML = `<div class="res-row"><span>Position fix</span>""", """  comUnit(`<div class="res-row"><span>Position fix</span>""")
rep("""    <div id="comrescue">${comRescueHtml()}</div>
    <div class="controls"><button onclick="comClose()">CLOSE</button></div>`;""", """    <div id="comrescue">${comRescueHtml()}</div>
    <div class="controls"><button onclick="comClose()">CLOSE</button></div>`);""")
rep("""  $('combody').innerHTML = h;
}

function comRecall""", """  comUnit(h);
}

function comRecall""")

a = s.index('<div id="drone" hidden>')
b = s.index('<div id="titlescreen">')
old = s[a:b]
hint = re.search(r'<div class="hint" id="dr_hint">.*\n', old).group(0).rstrip('\n')
NEW_DRONE = '''<div id="drone" hidden>
  <div class="dch">
    <i class="scr a"></i><i class="scr b"></i><i class="scr c"></i><i class="scr d"></i>
    <div class="dhd l"></div><div class="dhd r"></div>
    <div class="dscr">
      <div class="dtop">
        <div class="dtl"><span id="dr_title"></span><span id="dr_sub"></span></div>
        <div class="dbox"><span>HDG</span><b id="dr_hdg"></b></div>
        <div class="dbox"><span>ALT</span><b id="dr_alt"></b></div>
        <div class="dbox"><span>SPD</span><b id="dr_spd"></b></div>
        <div class="dbox"><span>ZOOM</span><b id="dr_zm"></b></div>
      </div>
      <div class="dmain">
        <div class="dleft">
          <div class="feed" id="dr_feed">
            <canvas id="dr_cv" width="800" height="600"></canvas>
            <div class="scan"></div>
            <div class="zv" id="dr_zv"><div class="zt" id="dr_zvt">ZOOM VIEW</div><canvas id="dr_tv" width="300" height="152"></canvas></div>
            ''' + hint + '''
          </div>
          <div class="dtele" id="dr_tele"></div>
        </div>
        <div class="dright" id="dr_side">
          <div class="dbt" id="dr_sh"></div>
          <div id="dr_stier"></div>
          <div id="dr_srx"></div>
          <canvas id="dr_radar" width="260" height="260"></canvas>
          <div id="dr_sbody"></div>
        </div>
      </div>
      <div class="dinfo" id="dr_info" hidden></div>
    </div>
    <div class="dkeys">
      <i class="rb pw"></i><i class="rb"></i><i class="rb"></i>
      <button class="mkey" id="dr_bmode" onclick="DRONE.toggleMode()">OPTICAL</button>
      <button class="mkey" id="dr_bml" onclick="DRONE.mouseLook()">MOUSE LOOK</button>
      <button class="mkey" id="dr_bact"></button>
      <button class="mkey" id="dr_bact2"></button>
      <button class="mkey" id="dr_binfo" onclick="DRONE.info()">INFO</button>
      <button class="mkey red" id="dr_abort" onclick="DRONE.abort()">ABORT</button>
    </div>
  </div>
</div>
'''
s = s[:a] + NEW_DRONE + s[b:]

d0 = s.index("const $d = id => document.getElementById('dr_' + id);")
d1 = s.index('window.DRONE = {')
seg = s[d0:d1]
seg = seg.replace("'#7ffbff'", "'#6fe87c'").replace('rgba(127,251,255', 'rgba(111,232,124').replace("'#6dffb0'", "'#b4ff5a'")
s = s[:d0] + seg + s[d1:]

RADAR = r'''const dotMask = (() => {
  const m = document.createElement('canvas');
  m.width = 260;
  m.height = 260;
  const x = m.getContext('2d');
  for (let i = 0; i < 11000; i++) {
    x.fillStyle = 'rgba(0,0,0,' + (0.45 + Math.random() * 0.55).toFixed(2) + ')';
    x.fillRect(Math.floor(Math.random() * 260), Math.floor(Math.random() * 260), 2, 2);
  }
  return m;
})();
const echoCv = document.createElement('canvas');
echoCv.width = 260;
echoCv.height = 260;

function drawRadar(now) {
  const cv = $d('radar');
  const c = cv.getContext('2d');
  const S = 260;
  const sc = S / G.WS;
  c.fillStyle = '#010402';
  c.fillRect(0, 0, S, S);
  const ec = echoCv.getContext('2d');
  ec.globalCompositeOperation = 'source-over';
  ec.clearRect(0, 0, S, S);
  ec.drawImage(G.exp, 0, 0);
  ec.globalCompositeOperation = 'source-in';
  ec.fillStyle = 'rgba(240,230,60,1)';
  ec.fillRect(0, 0, S, S);
  ec.globalCompositeOperation = 'destination-in';
  ec.drawImage(dotMask, 0, 0);
  c.drawImage(echoCv, 0, 0);
  c.drawImage(echoCv, 0, 0);
  const dx = G.cam.x * sc;
  const dy = G.cam.y * sc;
  c.strokeStyle = 'rgba(111,232,124,0.32)';
  c.lineWidth = 1;
  c.fillStyle = 'rgba(111,232,124,0.75)';
  c.font = '8px monospace';
  c.textAlign = 'left';
  const rstep = G.WS / 6;
  for (let k = 1; k <= 8; k++) {
    const rr = k * rstep * sc;
    if (rr > S * 1.2) break;
    c.beginPath(); c.arc(dx, dy, rr, 0, 7); c.stroke();
    c.fillText(Math.round(k * rstep), dx + 2, dy - rr + 9);
  }
  c.strokeStyle = 'rgba(111,232,124,0.2)';
  c.beginPath(); c.moveTo(dx, 0); c.lineTo(dx, S); c.moveTo(0, dy); c.lineTo(S, dy); c.stroke();
  const sa = (now * 0.0022) % (Math.PI * 2);
  for (let i = 0; i < 26; i++) {
    c.fillStyle = 'rgba(111,232,124,' + (0.2 * (1 - i / 26)).toFixed(3) + ')';
    c.beginPath();
    c.moveTo(dx, dy);
    c.arc(dx, dy, S * 1.5, sa - (i + 1) * 0.035, sa - i * 0.035);
    c.closePath();
    c.fill();
  }
  c.strokeStyle = 'rgba(160,255,170,0.9)';
  c.beginPath(); c.moveTo(dx, dy); c.lineTo(dx + Math.cos(sa) * S * 1.5, dy + Math.sin(sa) * S * 1.5); c.stroke();
  c.strokeStyle = 'rgba(111,232,124,0.7)';
  c.strokeRect(0.5, 0.5, S - 1, S - 1);
  c.fillStyle = '#6fe87c';
  c.font = '10px monospace';
  c.textAlign = 'center';
  c.fillText('N', S / 2, 11);
  const gx = G.gate.x * sc;
  const gy = G.gate.y * sc;
  c.strokeStyle = '#6fe87c';
  c.beginPath(); c.moveTo(gx, gy - 5); c.lineTo(gx + 5, gy); c.lineTo(gx, gy + 5); c.lineTo(gx - 5, gy); c.closePath(); c.stroke();
  c.fillText('GATE', gx, gy + 16);
  if (G.mode === 'recon') {
    c.strokeStyle = 'rgba(255,107,107,0.7)';
    c.setLineDash([4, 4]);
    c.beginPath(); c.arc(G.site.x * sc, G.site.y * sc, 70 * sc, 0, 7); c.stroke();
    c.setLineDash([]);
    c.fillStyle = '#ff8a7a';
    c.fillText('TARGET SITE', G.site.x * sc, G.site.y * sc - 76 * sc);
    G.obs.forEach(o => {
      if (!o.known && !G.done) return;
      const r = o.r * (G.night ? 0.75 : 1) * sc;
      c.fillStyle = 'rgba(255,90,70,0.24)';
      c.beginPath();
      c.moveTo(o.x * sc, o.y * sc);
      c.arc(o.x * sc, o.y * sc, r, o.head - o.half - Math.PI / 2, o.head + o.half - Math.PI / 2);
      c.closePath();
      c.fill();
    });
    G.contacts.forEach(ct => {
      if (!ct.tagged && !G.done) return;
      c.fillStyle = ct.kind === 'def' ? '#ff6b6b' : '#ffe14a';
      if (ct.kind === 'def') { c.beginPath(); c.arc(ct.x * sc, ct.y * sc, 3, 0, 7); c.fill(); } else c.fillRect(ct.x * sc - 3, ct.y * sc - 3, 6, 6);
    });
  }
  if (G.trail.length > 1) {
    c.strokeStyle = 'rgba(111,232,124,0.45)';
    c.setLineDash([2, 3]);
    c.beginPath();
    G.trail.forEach((p, i) => { if (i) c.lineTo(p.x * sc, p.y * sc); else c.moveTo(p.x * sc, p.y * sc); });
    c.stroke();
    c.setLineDash([]);
  }
  c.strokeStyle = 'rgba(111,232,124,0.55)';
  c.setLineDash([3, 4]);
  c.beginPath(); c.arc(dx, dy, sweepR() * sc, 0, 7); c.stroke();
  c.setLineDash([]);
  const half = (70 * Math.PI / 180) / 2 / zoom;
  c.fillStyle = 'rgba(111,232,124,0.2)';
  c.beginPath();
  c.moveTo(dx, dy);
  c.arc(dx, dy, sweepR() * sc, yaw - half - Math.PI / 2, yaw + half - Math.PI / 2);
  c.closePath();
  c.fill();
  c.save();
  c.translate(dx, dy);
  c.rotate(yaw);
  c.fillStyle = '#ffe14a';
  c.beginPath(); c.moveTo(0, -7); c.lineTo(5, 6); c.lineTo(0, 3); c.lineTo(-5, 6); c.closePath(); c.fill();
  c.restore();
  if (G.mark) {
    const mx = G.mark.x * sc;
    const my = G.mark.y * sc;
    c.strokeStyle = '#b4ff5a';
    c.lineWidth = 2;
    c.beginPath(); c.moveTo(mx - 7, my); c.lineTo(mx + 7, my); c.moveTo(mx, my - 7); c.lineTo(mx, my + 7); c.stroke();
    c.lineWidth = 1;
  }
  if (G.mode === 'rescue' && (G.found || G.done)) {
    const tx = G.px * sc;
    const ty = G.py * sc;
    c.strokeStyle = '#b4ff5a';
    c.lineWidth = 2;
    c.beginPath(); c.arc(tx, ty, 8, 0, 7); c.stroke();
    c.lineWidth = 1;
    c.fillStyle = '#b4ff5a';
    c.fillText('TEAM', tx, ty - 12);
  }
  c.textAlign = 'left';
}

function actKeys(rc) {
  const a = $d('bact');
  const b = $d('bact2');
  if (G.done) { a.textContent = rc ? 'FILE SURVEY' : 'CONTINUE'; a.disabled = false; a.classList.remove('on'); a.onclick = finish; b.style.display = 'none'; return; }
  if (rc) { a.textContent = 'END SURVEY'; a.disabled = false; a.classList.remove('on'); a.onclick = confirmRecon; b.style.display = 'none'; return; }
  a.textContent = G.markMode ? 'MARKING...' : 'PLACE FIX';
  a.classList.toggle('on', G.markMode);
  a.disabled = !!(G.found || G.linkLost);
  a.onclick = toggleMark;
  b.style.display = '';
  b.textContent = 'CONFIRM FIX';
  b.disabled = !((G.found || G.mark) && !G.done);
  b.onclick = confirmFix;
}

'''
i = s.index('function drawRadar(now) {')
j = s.index('function maxVis()')
s = s[:i] + RADAR + s[j:]

rep("""  $d('tele').innerHTML = cells.map(x => '<div class="t"><div class="k">' + x[0] + '</div><div class="v ' + x[2] + '">' + x[1] + '</div></div>').join('');""",
    """  cells.push(['POS X/Y', Math.round(G.cam.x) + ' / ' + Math.round(G.cam.y) + ' M', '']);
  const box = (t, names) => '<div class="tb"><div class="tt">' + t + '</div>' + names.map(n => cells.find(x => x[0] === n)).map(x => '<div class="tr"><span>' + x[0] + '</span><b class="' + x[2] + '">' + x[1] + '</b></div>').join('') + '</div>';
  $d('tele').innerHTML = box('ENVIRONMENT', ['TEMP', 'ATMOS O2', 'PRESSURE', 'RADIATION', 'GRAVITY', 'WIND', 'TERRAIN']) + box('OWN POSITION (NAV)', ['POS X/Y', 'FROM GATE', 'LINK', 'WORMHOLE']);
  $d('hdg').textContent = String(Math.round(((yaw * 180 / Math.PI) % 360 + 360) % 360)).padStart(3, '0') + ' DEG';
  $d('alt').textContent = G.alt.toFixed(0) + ' M';
  $d('spd').textContent = G.speed.toFixed(0) + ' M/S';
  $d('zm').textContent = zoom.toFixed(1) + 'X';""")

rep("""    s = '<div class="ctl"><button onclick="DRONE.confirmRecon()" ' + (G.done ? 'disabled' : '') + '>END SURVEY</button></div>';""", """    s = '';
    actKeys(true);""")
rep("""    s = '<div class="ctl"><button class="' + (G.markMode ? 'on' : '') + '" onclick="DRONE.toggleMark()" ' + (G.done || G.found || G.linkLost ? 'disabled' : '') + '>' + (G.markMode ? 'MARKING: CLICK THE RADAR' : 'PLACE FIX MARKER') + '</button><button onclick="DRONE.confirmFix()" ' + ((G.found || G.mark) && !G.done ? '' : 'disabled') + '>CONFIRM FIX</button></div>';""", """    s = '';
    actKeys(false);""")
rep("""  if (G.done) s += resultHtml() + '<div class="ctl"><button onclick="DRONE.finish()">' + (rc ? 'FILE SURVEY' : 'CONTINUE') + '</button></div>';
  $d('sbody').innerHTML = s;""", """  $d('info').innerHTML = '<div class="dbt">OPERATING NOTES</div>' + s;
  $d('sbody').innerHTML = G.done ? resultHtml() : '<div class="dim">ALL STATIONS NOMINAL. PRESS INFO FOR OPERATING NOTES.</div>';""")
rep("""  $d('hint').style.display = '';""", """  $d('hint').style.display = '';
  $d('info').hidden = true;
  $d('binfo').classList.remove('on');""")
rep("""  isActive: () => active,""", """  info: () => { const e = $d('info'); e.hidden = !e.hidden; $d('binfo').classList.toggle('on', !e.hidden); },
  isActive: () => active,""")

CSS = r'''
#comgame { padding: 0; background: radial-gradient(ellipse at 50% 30%, #11160f, #050705 75%); }
#comgame .titlebox .title, #comgame .titlebox .sub { display: none; }
#comgame .titlebox { height: 100%; }
#combody { display: flex; align-items: center; justify-content: center; overflow: auto; }
.asti { position: relative; width: 660px; height: 372px; flex: none; font-family: Arial, Helvetica, sans-serif; }
.ahd { position: absolute; top: 70px; width: 34px; height: 232px; border: 10px solid #0a0b0a; border-radius: 18px; box-shadow: inset 0 0 0 1px #2b2f2a, 0 2px 5px #000; }
.ahd.l { left: 0; border-right-width: 0; }
.ahd.r { right: 0; border-left-width: 0; }
.aface { position: absolute; left: 18px; right: 18px; top: 0; bottom: 0; background: radial-gradient(ellipse at 30% 10%, rgba(255,255,255,0.07), transparent 60%), linear-gradient(160deg, #4f5e3e 0%, #404d34 55%, #36422c 100%); border-radius: 10px; box-shadow: inset 0 0 0 2px #2a3322, inset 0 2px 0 rgba(255,255,255,0.12), 0 6px 18px rgba(0,0,0,0.65); }
.alb { position: absolute; font: 700 10px Arial, sans-serif; color: #e3e8d0; letter-spacing: 0.05em; white-space: nowrap; }
.apl { position: absolute; border-radius: 50%; background: radial-gradient(circle, #050505 0 26%, #1b1d1b 28% 50%, #7a8078 52% 57%, #242724 59% 100%); box-shadow: 0 2px 4px #000, inset 0 0 0 2px #0b0c0b; }
.apl.big { background: radial-gradient(circle, #040404 0 22%, #3a3d39 24% 34%, #0c0d0c 36% 50%, #8a9088 52% 58%, #262926 60% 100%); }
.apl.cab { background: radial-gradient(circle, #0a0a0a 0 55%, #1d1f1d 58% 100%); box-shadow: 0 0 0 3px #060606; }
.abz { position: absolute; left: 120px; top: 12px; width: 344px; height: 160px; background: linear-gradient(#2d3724, #1e2618); border-radius: 12px; box-shadow: inset 0 0 0 2px #10150c, inset 0 2px 0 rgba(255,255,255,0.1), 0 3px 6px rgba(0,0,0,0.5); }
.alog { position: absolute; left: 0; right: 0; top: 4px; text-align: center; font: 900 17px Arial Black, Arial, sans-serif; letter-spacing: 0.12em; color: #e9ecd8; }
.alcd { position: absolute; left: 10px; right: 10px; top: 28px; bottom: 10px; border-radius: 6px; background: linear-gradient(#cfe054, #aebf36); box-shadow: inset 0 0 16px rgba(40,60,0,0.6), inset 0 0 0 2px #0f1408; color: #1d2608; font: 700 10.5px "Courier New", monospace; padding: 3px 8px; display: flex; flex-direction: column; justify-content: space-between; text-shadow: 0 0 1px rgba(29,38,8,0.4); }
.alcd .al1, .alcd .al4, .alcd .al5 { display: flex; justify-content: space-between; gap: 8px; letter-spacing: 0.08em; }
.alcd .al5 { font-size: 9px; opacity: 0.8; }
.alcd .al2 { display: flex; align-items: baseline; gap: 8px; }
.alcd .alc { font-size: 13px; }
.alcd .alf { font: 900 25px "Courier New", monospace; letter-spacing: 0.04em; flex: 1; text-align: right; }
.alcd .alu { font-size: 10px; }
.alcd #comscope { width: 296px; height: 38px; display: block; background: none; border: 0; margin: 0 auto; }
.bat, .sig { display: inline-flex; gap: 1px; border: 1px solid #1d2608; padding: 1px 2px; height: 9px; width: 42px; vertical-align: -1px; }
.bat b { flex: 1; background: #1d2608; }
.sig { padding: 1px; }
.sig u { display: block; height: 100%; width: 0%; background: #1d2608; text-decoration: none; }
.ak { position: absolute; width: 76px; height: 36px; padding: 0; min-height: 0; min-width: 0; background: linear-gradient(#272c23, #121510); border: 1px solid #0a0c08; border-radius: 5px; box-shadow: 0 3px 0 #090b07, inset 0 1px 0 rgba(255,255,255,0.08); color: #dcee4a; font: 700 14px Arial, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; text-shadow: 0 0 6px rgba(220,238,74,0.75); line-height: 1; gap: 1px; }
.ak small { font-size: 7.5px; color: #b9c93a; letter-spacing: 0.05em; font-weight: 400; text-shadow: none; }
.ak.sq { width: 46px; }
.ak.dn { transform: translateY(2px); box-shadow: 0 1px 0 #090b07; background: linear-gradient(#1c2018, #0e110c); }
.akn { position: absolute; width: 74px; height: 74px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #3b3e3a, #0c0d0c 70%); box-shadow: 0 3px 8px #000, inset 0 0 0 3px #060706, 0 0 0 4px #1b1f19; cursor: grab; touch-action: none; }
.akn .kd { position: absolute; inset: 6px; border-radius: 50%; background: repeating-conic-gradient(#222522 0 8deg, #0e100e 8deg 16deg); box-shadow: inset 0 0 0 2px #060706; }
.akn .kd i { position: absolute; left: 50%; top: 2px; width: 4px; height: 24px; margin-left: -2px; background: #f1f4e6; border-radius: 2px; }
.cu { position: relative; width: 548px; height: 500px; flex: none; background: radial-gradient(ellipse at 30% 5%, rgba(255,255,255,0.08), transparent 55%), linear-gradient(160deg, #50603f, #3b482f); border-radius: 16px; box-shadow: inset 0 0 0 2px #232b1c, inset 0 2px 0 rgba(255,255,255,0.12), 0 8px 22px rgba(0,0,0,0.7); font-family: Arial, Helvetica, sans-serif; }
.cunub { position: absolute; left: 12px; top: -12px; width: 26px; height: 30px; background: linear-gradient(90deg, #0b0c0a, #2c302a, #0b0c0a); border-radius: 6px 6px 3px 3px; }
.cuic { position: absolute; top: 14px; width: 14px; height: 14px; border: 2px solid #e3e8d0; border-radius: 50%; }
.cuic.pw { left: 60px; border-top-color: transparent; }
.cuic.al { right: 60px; border-radius: 3px 3px 7px 7px; }
.cuscr { position: absolute; left: 78px; top: 34px; width: 392px; height: 250px; background: #000; border-radius: 8px; box-shadow: inset 0 0 0 3px #101310, 0 0 0 4px #1a2015; overflow: hidden; }
#comlcd { position: absolute; inset: 6px; border-radius: 4px; background: radial-gradient(ellipse at 70% 0%, #1d2d86 0%, #0a0f3a 45%, #02030f 100%); color: #fff; font: 12px Arial, sans-serif; overflow-y: auto; padding: 8px 10px; scrollbar-width: none; }
#comlcd::-webkit-scrollbar { display: none; }
#comlcd .lh { display: flex; gap: 10px; align-items: center; padding-bottom: 8px; border-bottom: 1px solid rgba(190,205,255,0.55); margin-bottom: 4px; }
#comlcd .lh i { width: 14px; height: 14px; border-radius: 50%; border: 2px solid #fff; flex: none; box-shadow: inset 0 0 0 3px #0a0f3a, inset 0 0 0 9px #fff; }
#comlcd .lh b { display: block; font-size: 13px; letter-spacing: 0.04em; }
#comlcd .lh span { display: block; font-size: 10px; color: #a9b6e8; }
#comlcd h2 { color: #8fb2ff; font: 700 11px Arial, sans-serif; letter-spacing: 0.1em; margin: 10px 0 4px; text-transform: uppercase; }
#comlcd .res-row, #comlcd .dispatch-row, #comlcd .staff-row { display: flex; justify-content: space-between; gap: 8px; padding: 6px 0; min-height: 0; flex-wrap: wrap; border-bottom: 1px solid rgba(190,205,255,0.4); }
#comlcd .dim, #comlcd .small { color: #a9b6e8; }
#comlcd .ok { color: #8dffb0; }
#comlcd .warn { color: #ffe27a; }
#comlcd .danger { color: #ff8a8a; }
#comlcd .mrow { font-size: 11.5px; padding: 3px 0; }
#comlcd p { margin: 6px 0; }
#comlcd .controls { justify-content: flex-start; margin: 8px 0 0; }
#comlcd button { width: auto; min-width: 0; min-height: 22px; padding: 0 10px; background: #1a2a8c; color: #fff; border: 1px solid #7f98ff; border-radius: 11px; font: 700 11px Arial, sans-serif; letter-spacing: 0.04em; white-space: normal; text-align: left; }
#comlcd button[data-ak]::before { content: attr(data-ak); display: inline-block; margin-right: 6px; width: 14px; height: 14px; line-height: 14px; text-align: center; border-radius: 50%; background: #fff; color: #1a2a8c; font-size: 10px; flex: none; }
.uk { position: absolute; padding: 0; min-height: 0; min-width: 0; background: linear-gradient(#2d302b, #171916); border: 1px solid #0b0c0a; border-radius: 7px; color: #e7eadb; font: 700 17px Arial, sans-serif; display: flex; align-items: center; justify-content: center; box-shadow: 0 3px 0 #0a0b09, inset 0 1px 0 rgba(255,255,255,0.1); cursor: pointer; }
.uk.sm { font-size: 11px; letter-spacing: 0.04em; }
.uk.big { font-size: 22px; border-radius: 9px; }
.uk.dn { transform: translateY(2px); box-shadow: 0 1px 0 #0a0b09; }
.ukc { position: absolute; width: 52px; height: 38px; background: #151714; border-radius: 4px; box-shadow: inset 0 0 0 1px #0b0c0a; }
#starmap #drone { --pg: #6fe87c; --cy: #6fe87c; --line: #1f5c2a; --dim: #4fa35c; --ok: #b4ff5a; --warn: #ffe14a; --bad: #ff5a4a; --txt: #aef5b4; --panel: #020503; background: #070908; color: var(--pg); font: 11px/1.35 "Courier New", monospace; overflow: hidden; padding: 0; }
#starmap #drone .dch { position: absolute; inset: 0; background: linear-gradient(145deg, #1d211e, #0b0d0c 60%, #161917); padding: 9px 16px 8px; display: flex; flex-direction: column; gap: 6px; box-shadow: inset 0 0 0 2px #050606, inset 0 0 0 3px #2a302b; }
#starmap #drone .dhd { position: absolute; top: 20%; bottom: 20%; width: 9px; background: linear-gradient(90deg, #050606, #2c322d, #050606); border-radius: 5px; }
#starmap #drone .dhd.l { left: 3px; }
#starmap #drone .dhd.r { right: 3px; }
#starmap #drone .scr { position: absolute; width: 6px; height: 6px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #5a605b, #1b1e1c); }
#starmap #drone .scr.a { left: 5px; top: 5px; }
#starmap #drone .scr.b { right: 5px; top: 5px; }
#starmap #drone .scr.c { left: 5px; bottom: 5px; }
#starmap #drone .scr.d { right: 5px; bottom: 5px; }
#starmap #drone .dscr { flex: 1 1 0; min-height: 0; position: relative; display: flex; flex-direction: column; gap: 5px; background: #020503; border: 1px solid #0f3016; box-shadow: inset 0 0 26px rgba(60,200,80,0.12), 0 0 0 3px #0a0c0b; padding: 6px 8px; overflow: hidden; }
#starmap #drone .dscr::after { content: ""; position: absolute; inset: 0; pointer-events: none; background: repeating-linear-gradient(to bottom, rgba(0,0,0,0) 0, rgba(0,0,0,0) 2px, rgba(0,0,0,0.13) 3px); z-index: 20; }
#starmap #drone .dtop { display: flex; gap: 5px; align-items: stretch; flex: none; }
#starmap #drone .dtl { flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; justify-content: center; }
#starmap #drone .dtl span:first-child { color: var(--pg); font-size: 11.5px; letter-spacing: 0.14em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
#starmap #drone .dtl span:last-child { color: var(--dim); font-size: 9px; letter-spacing: 0.14em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
#starmap #drone .dbox { border: 1px solid var(--line); padding: 1px 6px; min-width: 62px; text-align: center; background: rgba(40,160,60,0.06); }
#starmap #drone .dbox span { display: block; font-size: 8px; color: var(--dim); letter-spacing: 0.14em; }
#starmap #drone .dbox b { font: 13px "Courier New", monospace; color: var(--pg); font-weight: normal; }
#starmap #drone .dmain { flex: 1 1 0; min-height: 0; display: grid; grid-template-columns: minmax(0, 1.9fr) minmax(0, 1fr); gap: 6px; }
#starmap #drone .dleft { display: flex; flex-direction: column; gap: 5px; min-height: 0; min-width: 0; }
#starmap #drone .dleft .feed { flex: 0 0 auto; width: 100%; aspect-ratio: 4 / 3; border: 1px solid #1f5c2a; }
#starmap #drone .dtele { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; min-height: 0; overflow: hidden; }
#starmap #drone .tb { border: 1px solid var(--line); padding: 2px 6px 3px; background: rgba(40,160,60,0.05); }
#starmap #drone .tt { color: var(--dim); font-size: 8.5px; letter-spacing: 0.14em; border-bottom: 1px solid var(--line); margin-bottom: 2px; padding-bottom: 1px; }
#starmap #drone .tr { display: flex; justify-content: space-between; gap: 6px; font-size: 10px; line-height: 1.5; color: var(--dim); }
#starmap #drone .tr b { font-weight: normal; color: var(--pg); }
#starmap #drone .tr b.warn { color: var(--warn); }
#starmap #drone .tr b.bad { color: var(--bad); }
#starmap #drone .dright { display: flex; flex-direction: column; gap: 5px; min-height: 0; min-width: 0; overflow: hidden; }
#starmap #drone .dbt { border: 1px solid var(--line); padding: 2px 6px; color: var(--pg); font-size: 9px; letter-spacing: 0.1em; background: rgba(40,160,60,0.08); flex: none; }
#starmap #drone #dr_stier, #starmap #drone #dr_srx { flex: none; border: 1px solid var(--line); padding: 2px 6px; background: rgba(40,160,60,0.05); font-size: 9.5px; }
#starmap #drone #dr_stier:empty, #starmap #drone #dr_srx:empty { display: none; }
#starmap #drone .row { display: flex; gap: 8px; justify-content: space-between; border: 0; padding: 0; color: var(--dim); }
#starmap #drone .row b { color: var(--pg); font-weight: normal; }
#starmap #drone .meter { height: 6px; background: #031006; border: 1px solid var(--line); margin: 2px 0; }
#starmap #drone .meter i { background: var(--pg); }
#starmap #drone canvas#dr_radar { flex: none; display: block; width: 100%; max-width: 100%; height: auto; aspect-ratio: 1; align-self: center; margin: 0; border: 1px solid #2f7d3b; box-shadow: 0 0 10px rgba(80,220,100,0.18); background: #010402; }
#starmap #drone #dr_sbody { flex: 1 1 0; min-height: 0; overflow-y: auto; border: 1px solid var(--line); padding: 3px 6px; font-size: 10px; background: rgba(40,160,60,0.04); scrollbar-width: thin; }
#starmap #drone .result { border-top: 0; margin: 0; padding: 0; }
#starmap #drone .result h2 { margin: 0 0 3px; color: var(--pg); font-size: 10px; letter-spacing: 0.12em; }
#starmap #drone .dinfo { position: absolute; inset: 6px; z-index: 12; background: rgba(2,6,3,0.97); border: 1px solid var(--line); padding: 8px; overflow: auto; font-size: 10.5px; }
#starmap #drone .dinfo[hidden] { display: none; }
#starmap #drone .note { color: var(--txt); margin: 6px 0; }
#starmap #drone .dkeys { display: flex; align-items: center; gap: 6px; flex: none; }
#starmap #drone .rb { flex: none; width: 15px; height: 15px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #4d544e, #151816); border: 1px solid #000; box-shadow: 0 1px 0 #3a403b; }
#starmap #drone .rb.pw { box-shadow: 0 1px 0 #3a403b, 0 0 6px #6fe87c; border-color: #2f7d3b; background: radial-gradient(circle at 35% 30%, #8dff9a, #1f6a2a); }
#starmap #drone .mkey { flex: 1 1 0; min-width: 0; height: 28px; min-height: 0; padding: 0 4px; background: linear-gradient(#1a2c1e, #0a130c); color: var(--pg); border: 1px solid #2f7d3b; border-radius: 3px; font: 11px "Courier New", monospace; letter-spacing: 0.12em; text-transform: uppercase; white-space: nowrap; overflow: hidden; box-shadow: 0 2px 0 #040604; cursor: pointer; }
#starmap #drone .mkey:hover:not(:disabled) { background: #14321b; }
#starmap #drone .mkey.on { background: #1f4d29; color: #d8ffde; box-shadow: 0 0 9px rgba(111,232,124,0.55); }
#starmap #drone .mkey:disabled { opacity: 0.35; cursor: not-allowed; }
#starmap #drone .mkey.red { color: #ff8a7a; border-color: #8a2f25; }
#starmap #drone .hint button { background: linear-gradient(#1a2c1e, #0a130c); color: var(--pg); border: 1px solid #2f7d3b; border-radius: 3px; min-height: 0; height: 24px; padding: 0 12px; font: 11px "Courier New", monospace; letter-spacing: 0.12em; }
#starmap #drone .hint { background: rgba(2,8,3,0.95); border-color: var(--line); color: var(--txt); }
#starmap #drone .hint h2 { color: var(--pg); }
'''
rep('</style>\n</head>', CSS + '</style>\n</head>')

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
