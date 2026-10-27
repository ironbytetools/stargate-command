import re, sys

M = sys.argv[1]
OUT = sys.argv[2]
html = open(M, encoding='utf-8').read()
js = html[html.index('<script>') + 8:html.rindex('</script>')]
css = html[html.index('<style>') + 7:html.index('</style>')]
start = html.index('<div class="cols">')
end = html.index('</div>\n<script>')
markup = html[start:end]


def skip_str(s, i):
    q = s[i]
    i += 1
    while i < len(s):
        if s[i] == '\\':
            i += 2
            continue
        if s[i] == q:
            return i + 1
        i += 1
    return i


def remove_fn(src, name):
    m = re.search(r'^function ' + name + r'\(', src, re.M)
    if not m:
        print('MISSING fn', name)
        sys.exit(1)
    i = src.index('{', m.end())
    depth = 0
    while i < len(src):
        ch = src[i]
        if ch in '\'"`':
            i = skip_str(src, i)
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                i += 1
                break
        i += 1
    while i < len(src) and src[i] == '\n':
        i += 1
    return src[:m.start()] + src[i:]


def rep(old, new, count=1):
    global js
    n = js.count(old)
    if n != count:
        print('MISMATCH', n, 'expected', count, 'for', old[:100])
        sys.exit(1)
    js = js.replace(old, new)


tail = js.index("const feed = document.getElementById('feed');")
js = js[:tail]

for fn in ['setTier', 'drawTiers', 'cycleWorld', 'cycleNight', 'toggleFx', 'demoClock', 'cycleMode', 'ensureAudio', 'toggleSound', 'medicIdx']:
    js = remove_fn(js, fn)

rep("let worldPick = -1;\nlet nightPick = 0;\n", "")
rep("let haz = 'med';\nlet tier = 2;", "let haz = 'med';\nlet tier = 0;\nlet cfg = null;\nlet active = false;\nlet feed = null;")
rep("const th = worldPick >= 0 ? THEMES[worldPick] : THEMES[Math.floor(Math.random() * THEMES.length)];", "const th = THEMES[cfg.theme];")
rep("const night = nightPick === 0 ? Math.random() < 0.25 : nightPick === 2;", "const night = cfg.night;")
rep("const tm = TEAMS[Math.floor(Math.random() * TEAMS.length)];", "const tm = cfg.team;")
rep("const hurt = Math.random() < 0.5 ? Math.floor(Math.random() * tm.roles.length) : -1;", "const hurt = cfg.hurt;")
rep("tm, hurt, seed:", "tm, hurtSet: new Set(hurt), seed:")
rep("clockEnd: performance.now() + 270000", "clockEnd: performance.now() + cfg.remain")
rep("G.guess = G.found ? { x: G.tx, y: G.ty } : (G.mark || null);", "G.guess = G.found ? { x: G.px, y: G.py } : (G.mark || null);")

rep("const hurt = it.i === G.hurt;", "const hurt = G.hurtSet.has(it.i);")
rep("const med = G.hurt >= 0 && it.i === medicIdx();", "const med = G.hurtSet.size > 0 && it.i === medicIdx();")
rep("i === G.hurt ? 1.4 : 1", "G.hurtSet.has(i) ? 1.4 : 1")
rep("const med = G.hurt >= 0 ? medicIdx() : -1;", "const med = G.hurtSet.size > 0 ? medicIdx() : -1;")
rep("const hurt = i === G.hurt;", "const hurt = G.hurtSet.has(i);")
rep("(G.hurt >= 0 ? ', 1 INJURED' : ', NONE INJURED')", "(G.hurtSet.size > 0 ? ', ' + G.hurtSet.size + ' INJURED' : ', NONE INJURED')")

rep("document.getElementById('hint').style.display = 'none'", "$d('hint').style.display = 'none'")
rep("<button onclick=\"newGame()\">NEW MISSION</button>", "")
rep("<button onclick=\"newGame()\">NEW TEAM POSITION</button>", "")
rep("<div class=\"note\">Proposed numbers, still to confirm.</div>", "")
rep("onclick=\"confirmRecon()\"", "onclick=\"DRONE.confirmRecon()\"")
rep("onclick=\"toggleMark()\"", "onclick=\"DRONE.toggleMark()\"")
rep("onclick=\"confirmFix()\"", "onclick=\"DRONE.confirmFix()\"")
rep('id="sigbar"', 'id="dr_sigbar"')
rep('id="rxs"', 'id="dr_rxs"')
rep('id="rcon"', 'id="dr_rcon"')
rep("  if (G.done) s += resultHtml();\n", "  if (G.done) s += resultHtml() + '<div class=\"ctl\"><button onclick=\"DRONE.finish()\">' + (rc ? 'FILE SURVEY' : 'CONTINUE') + '</button></div>';\n")
rep("function loop(now) {\n  requestAnimationFrame(loop);", "function loop(now) {\n  if (!active) return;\n  requestAnimationFrame(loop);")


rep("G.expo += dt * (0.10 + 0.20 * spd01 + 0.12 * altN) * inC;", "G.expo += dt * (0.05 + 0.10 * spd01 + 0.06 * altN) * inC;")
rep("G.expo = Math.max(0, G.expo - dt * 0.15);", "G.expo = Math.max(0, G.expo - dt * 0.30);")
rep("r: 100, half: 0.75", "r: 75, half: 0.75")
rep("r: 70, half: 0.62", "r: 52, half: 0.62")
rep("r: 75, half: 0.55", "r: 56, half: 0.55")
rep("    let inC = 0;\n    G.obs.forEach(o => {", "    let inC = 0;\n    let warn = false;\n    G.obs.forEach(o => {")
rep("      if (d < r && Math.abs(wrapA(Math.atan2(ddx, -ddy) - o.head)) < o.half) inC = Math.max(inC, 1.4 - d / r);\n", "      const aoff = Math.abs(wrapA(Math.atan2(ddx, -ddy) - o.head));\n      if (d < r && aoff < o.half) inC = Math.max(inC, 1.4 - d / r);\n      else if (d < r * 1.35 && aoff < o.half + 0.3) { warn = true; o.known = true; }\n")
rep("    G.inCone = inC > 0;\n", "    G.inCone = inC > 0;\n    G.warn = warn && inC === 0;\n")
rep("c.fillText('IN DEFENDER VIEW', W / 2, 62); c.textAlign = 'left'; }", "c.fillText('IN DEFENDER VIEW', W / 2, 62); c.textAlign = 'left'; }\n    else if (G.warn) { c.fillStyle = '#ffd36b'; c.textAlign = 'center'; c.font = '13px monospace'; c.fillText('DEFENDER NEARBY', W / 2, 62); c.textAlign = 'left'; }")
rep("  if (Math.abs(zoom - lastZoom) > 0.01) {", "  if (G.mode === 'recon' && G.warn && !G.done && !G.linkLost) {\n    const nw = performance.now();\n    if (!snd.wt || nw - snd.wt > 800) { snd.wt = nw; beep(330, 0.07, 0.05, 'triangle'); }\n  }\n  if (Math.abs(zoom - lastZoom) > 0.01) {")
rep("Staying inside a wedge builds exposure.", "An amber DEFENDER NEARBY warning and a slow tick sound when you close on a defender view. Staying inside a wedge builds exposure.")

js = js.replace("document.getElementById(", "$d(")
js = js.replace("document.getElementById", "$d")

head = "(function () {\nconst $d = id => document.getElementById('dr_' + id);\n"

glue = r'''
function medicIdx() {
  const h = [...G.hurtSet][0];
  const n = G.tm.roles.length;
  if (h === undefined) return -1;
  for (let k = h + 1; k < n; k++) if (!G.hurtSet.has(k)) return k;
  for (let k = h - 1; k >= 0; k--) if (!G.hurtSet.has(k)) return k;
  return -1;
}

function ensureAudio() {
  if (snd) return snd;
  try {
    if (typeof ac !== 'function' || !ac() || !BUS) return null;
    const ctx = AC;
    const out = BUS.fx;
    const len = ctx.sampleRate * 2;
    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    const ns = ctx.createBufferSource();
    ns.buffer = buf;
    ns.loop = true;
    const bp = ctx.createBiquadFilter();
    bp.type = 'bandpass';
    bp.frequency.value = 2400;
    bp.Q.value = 0.6;
    const ng = ctx.createGain();
    ng.gain.value = 0;
    ns.connect(bp);
    bp.connect(ng);
    ng.connect(out);
    ns.start();
    const rot = ctx.createOscillator();
    rot.type = 'sawtooth';
    rot.frequency.value = 62;
    const lfo = ctx.createOscillator();
    lfo.frequency.value = 14;
    const lg = ctx.createGain();
    lg.gain.value = 0.5;
    const rg = ctx.createGain();
    rg.gain.value = 0;
    const lp = ctx.createBiquadFilter();
    lp.type = 'lowpass';
    lp.frequency.value = 420;
    lfo.connect(lg);
    lg.connect(rg.gain);
    rot.connect(lp);
    lp.connect(rg);
    rg.connect(out);
    rot.start();
    lfo.start();
    snd = { ctx, out, ng, bp, rg, rot, lfo, ns, on: true };
    return snd;
  } catch (e) { return null; }
}

function stopAudio() {
  if (!snd) return;
  try {
    snd.ng.gain.value = 0;
    snd.rg.gain.value = 0;
    snd.ns.stop();
    snd.rot.stop();
    snd.lfo.stop();
    snd.ng.disconnect();
    snd.rg.disconnect();
  } catch (e) {}
  snd = null;
}

function beep(freq, dur, vol, type) {
  if (!snd || !snd.on) return;
  const o = snd.ctx.createOscillator();
  const g = snd.ctx.createGain();
  o.type = type || 'sine';
  o.frequency.value = freq;
  g.gain.setValueAtTime(vol, snd.ctx.currentTime);
  g.gain.exponentialRampToValueAtTime(0.0001, snd.ctx.currentTime + dur);
  o.connect(g);
  g.connect(snd.out);
  o.start();
  o.stop(snd.ctx.currentTime + dur);
}

function summary() {
  if (G.mode === 'recon') return { mode: 'recon', tagged: G.tagged, total: G.contacts.length, spotted: G.spotted, linkLost: G.linkLost };
  const g = G.guess;
  const dist = G.found ? 0 : (g ? Math.hypot(g.x - G.px, g.y - G.py) : 99999);
  return { mode: 'rescue', dist, found: G.found, linkLost: G.linkLost, marked: !!g };
}

function stop() {
  active = false;
  for (const k in keys) keys[k] = false;
  drag = null;
  try { if (document.pointerLockElement === feed) document.exitPointerLock(); } catch (e) {}
  stopAudio();
  document.getElementById('drone').hidden = true;
}

function start(c) {
  cfg = c;
  haz = c.hazard;
  tier = c.tier;
  modeSel = c.mode;
  thermal = false;
  $d('bmode').textContent = 'OPTICAL';
  $d('bmode').classList.remove('on');
  $d('hint').style.display = '';
  $d('title').textContent = c.title;
  $d('sub').textContent = c.sub;
  document.getElementById('drone').hidden = false;
  active = true;
  newGame();
  ensureAudio();
  requestAnimationFrame(loop);
}

function finish() {
  if (!active || !G || !G.done) return;
  const s = summary();
  const f = cfg.onDone;
  stop();
  if (f) f(s);
}

function abort() {
  if (!active) return;
  const f = cfg.onAbort;
  stop();
  if (f) f();
}

function linkLost() {
  if (!active || !G || G.done) return;
  G.linkLost = true;
  G.guess = G.found ? { x: G.px, y: G.py } : (G.mark || null);
  G.done = true;
  render();
}

function init() {
  feed = $d('feed');
  feed.addEventListener('pointerdown', e => { if (e.target.closest('.hint') || e.target.closest('.zv')) return; drag = { x: e.clientX, y: e.clientY }; feed.classList.add('drag'); feed.setPointerCapture(e.pointerId); });
  feed.addEventListener('pointermove', e => {
    if (!drag) return;
    const dx = e.clientX - drag.x;
    const dy = e.clientY - drag.y;
    drag = { x: e.clientX, y: e.clientY };
    yaw = wrapA(yaw + dx * 0.0042 / zoom);
    pitch = Math.max(-0.45, Math.min(0.55, pitch + dy * 0.0035 / zoom));
  });
  feed.addEventListener('pointerup', () => { drag = null; feed.classList.remove('drag'); });
  feed.addEventListener('pointercancel', () => { drag = null; feed.classList.remove('drag'); });
  feed.addEventListener('wheel', e => { e.preventDefault(); zoom = Math.max(1, Math.min(TIERS[tier].zoom, zoom * (e.deltaY < 0 ? 1.12 : 1 / 1.12))); }, { passive: false });
  window.addEventListener('keydown', e => {
    if (!active) return;
    e.stopImmediatePropagation();
    const k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    if (k.startsWith('Arrow') || k === ' ' || k === 'Tab') e.preventDefault();
    keys[k] = true;
    if ('wasdqe'.indexOf(k) >= 0 || k.startsWith('Arrow')) hideHint();
    if (k === 't' && !e.repeat) toggleMode();
  }, true);
  window.addEventListener('keyup', e => {
    if (!active) return;
    e.stopImmediatePropagation();
    keys[e.key.length === 1 ? e.key.toLowerCase() : e.key] = false;
  }, true);
  window.addEventListener('blur', () => { for (const k in keys) keys[k] = false; });
  document.addEventListener('pointerlockchange', () => { $d('bml').classList.toggle('on', document.pointerLockElement === feed); });
  document.addEventListener('mousemove', e => {
    if (!active || document.pointerLockElement !== feed) return;
    yaw = wrapA(yaw + e.movementX * 0.0028 / zoom);
    pitch = Math.max(-0.45, Math.min(0.55, pitch - e.movementY * 0.0025 / zoom));
  });
  $d('radar').addEventListener('pointerdown', e => {
    if (!active || !G || !G.markMode || G.done || G.found || G.linkLost) return;
    const r = e.currentTarget.getBoundingClientRect();
    G.mark = { x: (e.clientX - r.left) / r.width * G.WS, y: (e.clientY - r.top) / r.height * G.WS };
    G.markMode = false;
    render();
  });
}

init();

window.DRONE = {
  start, stop, finish, abort, linkLost, hideHint, toggleMode, mouseLook, toggleMark, confirmFix, confirmRecon,
  isActive: () => active,
  themes: THEMES.length
};
})();
'''

engine = head + js.rstrip() + '\n' + glue

# the audio replacement happens before updateAudio is used; ensure no leftover references to removed names
for bad in ['setTier', 'drawTiers', 'cycleWorld', 'cycleNight', 'toggleFx', 'cycleMode', 'demoClock', 'toggleSound', 'worldPick', 'nightPick', 'TEAMS[']:
    for m in re.finditer(re.escape(bad), engine):
        line = engine[:m.start()].count('\n') + 1
        print('LEFTOVER', bad, 'line', line)

open(OUT, 'w', encoding='utf-8').write(engine)

# CSS
def scope(sel):
    out = []
    for s in sel.split(','):
        s = s.strip()
        if s == ':root' or s == 'body':
            out.append('#drone')
        elif s == '*':
            out.append('#drone, #drone *')
        else:
            out.append('#drone ' + s)
    return ', '.join(out)

def scope_rules(text):
    res = []
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', text):
        res.append(scope(m.group(1)) + ' {' + m.group(2) + '}')
    return '\n'.join(res)

parts = []
pos = 0
for m in re.finditer(r'@media[^{]*\{((?:[^{}]*\{[^{}]*\})*)\s*\}', css):
    parts.append(scope_rules(css[pos:m.start()]))
    head_m = css[m.start():css.index('{', m.start())]
    parts.append(head_m + '{\n' + scope_rules(m.group(1)) + '\n}')
    pos = m.end()
parts.append(scope_rules(css[pos:]))
cssout = '\n'.join(parts)
cssout = cssout.replace('#drone  {', '#drone {').replace('canvas#cv', 'canvas#dr_cv').replace('#drone #radar', '#drone #dr_radar')

markup = markup.replace('onclick="hideHint()"', 'onclick="DRONE.hideHint()"')
markup = markup.replace('onclick="toggleMode()"', 'onclick="DRONE.toggleMode()"')
markup = markup.replace('onclick="mouseLook()"', 'onclick="DRONE.mouseLook()"')
markup = re.sub(r'\bid="([a-z]+)"', lambda m: 'id="dr_' + m.group(1) + '"', markup)
open(OUT + '.css', 'w', encoding='utf-8').write(cssout)
open(OUT + '.html', 'w', encoding='utf-8').write(markup)
print('ok', len(engine), len(cssout), len(markup))
