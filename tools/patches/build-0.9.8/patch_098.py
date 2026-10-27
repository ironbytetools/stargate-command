import re
import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.7') == 4, s.count('0.9.7')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.7</title>', '<title>Stargate Command 0.9.8</title>')
rep('BUILD 0.9.7', 'BUILD 0.9.8', 2)
rep("const BUILD_VER = '0.9.7';", "const BUILD_VER = '0.9.8';")

a = s.index('<div id="drone" hidden>')
b = s.index('<div id="titlescreen">')
old = s[a:b]
hint = re.search(r'<div class="hint" id="dr_hint">.*\n', old).group(0).rstrip('\n')


def fk(f, label, extra='', cls=''):
    return '<button class="fk' + cls + '" data-f="' + f + '" ' + extra + '>' + label + '</button>'


top = ''.join(fk('F' + str(n), 'HELP' if n == 13 else '', 'data-fk="help"' if n == 13 else '', ' top') for n in range(13, 21))
left = '\n      '.join([
    fk('F1', 'OPTICAL', 'id="dr_bmode" onclick="DRONE.toggleMode()"'),
    fk('F2', 'MOUSE LOOK', 'id="dr_bml" onclick="DRONE.mouseLook()"'),
    fk('F3', '', 'id="dr_bact"'),
    fk('F4', '', 'id="dr_bact2"'),
    fk('F5', 'INFO', 'id="dr_binfo" onclick="DRONE.info()"'),
    fk('F6', 'ABORT', 'id="dr_abort" onclick="DRONE.abort()"', ' red'),
])
right = '\n      '.join([
    fk('F7', 'ZOOM IN', 'data-fk="zi"'),
    fk('F8', 'ZOOM OUT', 'data-fk="zo"'),
    fk('F9', 'CLIMB', 'data-fk="cl"'),
    fk('F10', 'DESCEND', 'data-fk="ds"'),
    fk('F11', 'LEVEL', 'data-fk="lv"'),
    fk('F12', 'BOOST', 'data-fk="bo"'),
])
NEW_DRONE = '''<div id="drone" hidden>
  <div class="dch">
    <div class="ftop">''' + top + '''</div>
    <div class="fl">
      ''' + left + '''
    </div>
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
    <div class="fr">
      ''' + right + '''
    </div>
    <div class="fbot"><button class="fb" data-fk="bd">BRT-</button><button class="fb" data-fk="bu">BRT+</button><button class="fb">CAM</button><button class="fb">REC</button><i class="pwr"></i></div>
  </div>
</div>
'''
s = s[:a] + NEW_DRONE + s[b:]

i = s.index('const dotMask = (() => {')
j = s.index("const echoCv = document.createElement('canvas');")
s = s[:i] + s[j:]
rep("""  ec.globalCompositeOperation = 'source-in';
  ec.fillStyle = 'rgba(240,230,60,1)';
  ec.fillRect(0, 0, S, S);
  ec.globalCompositeOperation = 'destination-in';
  ec.drawImage(dotMask, 0, 0);
  c.drawImage(echoCv, 0, 0);
  c.drawImage(echoCv, 0, 0);""", """  ec.globalCompositeOperation = 'source-in';
  ec.fillStyle = 'rgba(60,190,90,0.15)';
  ec.fillRect(0, 0, S, S);
  c.drawImage(echoCv, 0, 0);""")

rep("b.style.display = 'none'", "b.style.visibility = 'hidden'", 2)
rep("b.style.display = '';", "b.style.visibility = '';")

rep("""init();

window.DRONE = {""", """let drBr = 1;

function fkAct(n) {
  if (!active) return;
  if (n === 'zi') zoom = Math.min(TIERS[tier].zoom, zoom * 1.1);
  else if (n === 'zo') zoom = Math.max(1, zoom / 1.1);
  else if (n === 'lv') pitch = 0.04;
  else if (n === 'help') $d('hint').style.display = '';
  else if (n === 'bd' || n === 'bu') {
    drBr = Math.max(0.6, Math.min(1.5, drBr + (n === 'bu' ? 0.15 : -0.15)));
    document.querySelector('#drone .dscr').style.filter = 'brightness(' + drBr + ')';
  }
  sfxClick();
}

document.querySelectorAll('#drone [data-fk]').forEach(b => {
  const n = b.dataset.fk;
  const hold = { cl: 'e', ds: 'q', bo: 'Shift' }[n];
  let t1 = 0;
  let t2 = 0;
  const stop = () => { clearTimeout(t1); clearInterval(t2); b.classList.remove('dn'); if (hold) keys[hold] = false; };
  b.addEventListener('pointerdown', e => {
    e.preventDefault();
    b.classList.add('dn');
    if (hold) { keys[hold] = true; hideHint(); return; }
    fkAct(n);
    if (n === 'zi' || n === 'zo') t1 = setTimeout(() => { t2 = setInterval(() => fkAct(n), 80); }, 300);
  });
  ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev => b.addEventListener(ev, stop));
});

init();

window.DRONE = {""")

CSS = r'''
#starmap #drone { background: #050605; }
#starmap #drone .dch { position: absolute; inset: 0; display: grid; grid-template-columns: 66px minmax(0, 1fr) 66px; grid-template-rows: 44px minmax(0, 1fr) 40px; gap: 0; padding: 0; background: radial-gradient(ellipse at 30% 8%, rgba(255,255,255,0.09), transparent 55%), linear-gradient(145deg, #4e5e3d, #394729 55%, #2d3923); clip-path: polygon(18px 0, calc(100% - 18px) 0, 100% 18px, 100% calc(100% - 18px), calc(100% - 18px) 100%, 18px 100%, 0 calc(100% - 18px), 0 18px); box-shadow: none; }
#starmap #drone .dch::before { content: ""; position: absolute; inset: 0; pointer-events: none; box-shadow: inset 0 0 0 2px #1d2616, inset 0 3px 0 rgba(255,255,255,0.15), inset 0 -3px 0 rgba(0,0,0,0.35); z-index: 3; }
#starmap #drone .dscr { grid-column: 2; grid-row: 2; margin: 0; border-radius: 10px; border: 3px solid #0a0d08; box-shadow: inset 0 0 26px rgba(60,200,80,0.12), 0 0 0 2px #222c1a, 0 0 0 3px #0d110a; }
#starmap #drone .ftop { grid-column: 2; grid-row: 1; display: flex; justify-content: space-between; align-items: center; padding: 0 2px; }
#starmap #drone .fbot { grid-column: 2; grid-row: 3; display: flex; justify-content: center; align-items: center; gap: 12px; }
#starmap #drone .fl { grid-column: 1; grid-row: 2; display: flex; flex-direction: column; justify-content: space-around; align-items: center; padding: 4px 0; }
#starmap #drone .fr { grid-column: 3; grid-row: 2; display: flex; flex-direction: column; justify-content: space-around; align-items: center; padding: 4px 0; }
#starmap #drone .fk { width: 58px; height: 46px; min-height: 0; min-width: 0; padding: 0 2px; background: linear-gradient(#272b25, #0f120e); border: 1px solid #050604; border-radius: 6px; box-shadow: 0 3px 0 #070806, inset 0 1px 0 rgba(255,255,255,0.1); color: #cfe3b5; font: 700 9.5px Arial, sans-serif; letter-spacing: 0.02em; text-transform: uppercase; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px; line-height: 1.05; text-align: center; white-space: normal; overflow: hidden; cursor: pointer; }
#starmap #drone .fk::before { content: attr(data-f); font: 700 11px Arial, sans-serif; color: #fff; letter-spacing: 0.02em; }
#starmap #drone .fk.top { height: 32px; width: 56px; gap: 1px; }
#starmap #drone .fk:hover:not(:disabled) { background: linear-gradient(#333a2f, #151912); }
#starmap #drone .fk.on { color: #b4ff5a; box-shadow: 0 3px 0 #070806, 0 0 10px rgba(111,232,124,0.7); }
#starmap #drone .fk.red { color: #ff9a8a; }
#starmap #drone .fk.dn { transform: translateY(2px); box-shadow: 0 1px 0 #070806; }
#starmap #drone .fk:disabled { opacity: 0.4; cursor: not-allowed; }
#starmap #drone .fb { width: 50px; height: 22px; min-height: 0; min-width: 0; padding: 0; background: linear-gradient(#272b25, #0f120e); border: 1px solid #050604; border-radius: 5px; box-shadow: 0 2px 0 #070806, inset 0 1px 0 rgba(255,255,255,0.1); color: #cfe3b5; font: 700 8px Arial, sans-serif; letter-spacing: 0.04em; cursor: pointer; }
#starmap #drone .fb.dn { transform: translateY(1px); }
#starmap #drone .pwr { display: block; width: 22px; height: 22px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #4a504a, #121512); border: 1px solid #050604; box-shadow: 0 2px 0 #070806; position: relative; }
#starmap #drone .pwr::after { content: ""; position: absolute; left: 6px; top: 6px; width: 8px; height: 8px; border-radius: 50%; background: #7dff8a; box-shadow: 0 0 6px #7dff8a; }
'''
rep('</style>\n</head>', CSS + '</style>\n</head>')

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
