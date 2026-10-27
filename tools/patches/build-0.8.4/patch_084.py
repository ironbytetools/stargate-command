import re, sys

src = open('base.html', encoding='utf-8').read()
engine = open('drone-engine.js', encoding='utf-8').read()
dcss = open('drone-engine.js.css', encoding='utf-8').read()
dhtml = open('drone-engine.js.html', encoding='utf-8').read()


def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        print('MISMATCH', n, 'expected', count, 'for', old[:100])
        sys.exit(1)
    src = src.replace(old, new)


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


def remove_fn(name):
    global src
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
        if ch == '/' and src[i + 1] == '/':
            i = src.index('\n', i)
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
    src = src[:m.start()] + src[i:]


rep('<title>Stargate Command 0.8.3</title>', '<title>Stargate Command 0.8.4</title>')
rep('BUILD 0.8.3</div>', 'BUILD 0.8.4</div>', 2)

rep("{ id: 'pin', name: 'PINPOINT', max: 10,", "{ id: 'pin', name: 'PINPOINT', max: 30,")
rep("{ id: 'good', name: 'GOOD', max: 30,", "{ id: 'good', name: 'GOOD', max: 80,")
rep("{ id: 'rough', name: 'ROUGH', max: 60,", "{ id: 'rough', name: 'ROUGH', max: 160,")

rep("const COM_MAP = 420;\nconst COM_ST = [{ n: 'A', x: 36, y: 384 }, { n: 'B', x: 384, y: 384 }, { n: 'C', x: 210, y: 36 }];\n", "")

for fn in ['comTrueAng', 'comTri', 'comLocked', 'comTriUi', 'comPick', 'comLockBearing', 'comMapClick', 'comFix']:
    remove_fn(fn)

i0 = src.index("  } else {\n    h += `<p class=\"dim small\">Take a bearing from each relay station")
i1 = src.index("    comTriUi();\n  }\n", i0) + len("    comTriUi();\n  }\n")
src = src[:i0] + "  } else {\n    h += '<p class=\"dim small\">Reconnaissance drone launching.</p>';\n  }\n" + src[i1:]
rep("  if (g.phase === 'tri') comTriUi();\n", "")

rep("    else { g.phase = 'tri'; comRender(); }\n", "    else comDroneLaunch();\n")
rep("function comWatch() {\n  if (!COMG || COMG.ended) return;\n", "function comWatch() {\n  if (!COMG || COMG.ended || COMG.phase === 'drone') return;\n")

new_fns = r'''const DRONE_CD_MS = 300000;
const DRONE_COL = { exp: '#7ffbff', rec: '#6dffb0', asl: '#ff9a7a', sec: '#ff9a7a', dip: '#7ffbff' };
const DRONE_ROLE = { 'Team Lead': 'L', 'Team Leader': 'L', Soldier: 'S', Scientist: 'Sc', Linguist: 'Li', Sniper: 'Sn', 'Recon Specialist': 'R', Rifleman: 'Rf', 'Machine Gunner': 'G', Grenadier: 'Gr', Diplomat: 'Li', Aide: 'S' };
const DRONE_THEME = [[/tundra|plateau/i, 0], [/desert/i, 1], [/forest|jungle|ocean|archipelago/i, 2], [/ruin/i, 3], [/volcan/i, 4]];
let droneWid = null;

function droneTier() {
  let t = 0;
  state.vehicles.forEach(v => { if (v.type === 'drone' && v.status === 'home') t = Math.max(t, v.tier || 0); });
  return Math.max(0, Math.min(5, t));
}

function droneTheme(w) {
  const hit = DRONE_THEME.find(x => x[0].test(w.type));
  if (hit) return hit[1];
  let h = 0;
  for (const ch of String(w.id)) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return h % DRONE.themes;
}

function droneRole(r) { return DRONE_ROLE[r] || 'S'; }

function droneRemain() { return Math.max(5000, WORMHOLE_MS - (performance.now() - state.openT)); }

function comDroneLaunch() {
  const g = COMG;
  g.phase = 'drone';
  $('comgame').hidden = true;
  const w = world(g.wid);
  const roles = [];
  const hurt = [];
  let col = '#ffd36b';
  let label;
  if (g.lead) {
    const mates = groupMates(g.lead);
    mates.forEach(t => {
      const hm = hitMember(t);
      t.members.forEach(x => {
        if (x.status === 'killed' || x.status === 'captured') return;
        if (hm && x === hm) hurt.push(roles.length);
        roles.push(droneRole(x.role));
      });
    });
    col = DRONE_COL[g.lead.type] || '#7ffbff';
    label = mates.map(t => t.name).join(', ').toUpperCase();
  } else {
    state.teams.forEach(t => t.members.forEach(x => { if (x.status === 'captured' && x.at === g.wid) roles.push(droneRole(x.role)); }));
    label = 'CAPTIVE PERSONNEL';
  }
  if (!roles.length) roles.push('S');
  droneWid = g.wid;
  DRONE.start({
    mode: 'rescue', hazard: w.hazard, tier: droneTier(), theme: droneTheme(w), night: Math.random() < 0.25,
    team: { n: label, col, roles }, hurt, remain: droneRemain(),
    title: 'COMM 1 // RECONNAISSANCE DRONE', sub: wname(w).toUpperCase() + ' // HAZARD ' + (HAZ_LABEL[w.hazard] || '').toUpperCase(),
    onDone: s => comDroneDone(s), onAbort: () => comClose()
  });
}

function comDroneDone(s) {
  const g = COMG;
  if (!g) return;
  g.ended = true;
  g.phase = 'done';
  $('comgame').hidden = false;
  const dist = s.dist;
  const band = bandForErr(dist);
  const lines = g.lead ? establishFix(g.lead, band, dist) : [];
  const cn = comCapNames(g.wid);
  if (cn.length) lines.push(`Radio contact: ${cn.join(', ')} ${cn.length === 1 ? 'is' : 'are'} being held captive on this world. Position fix ${band.name}.`);
  sfx.chime();
  $('comtitle').textContent = s.linkLost ? 'CONTACT LOST // FIX AS MARKED' : 'CONTACT ESTABLISHED';
  const fix = dist >= 99999 ? 'NO FIX' : Math.round(dist) + ' M FROM TEAM';
  const iv = band.intel >= 1 ? 'one extra intel tier' : (band.intel === 0 ? 'full intel' : (band.intel === -1 ? 'one intel tier fewer' : 'no intel'));
  const asst = g.lead ? `<div class="res-row"><span>Assist travel time</span><span>${fmt(Math.round(band.assistMs * fastMul()))}</span></div>
    <div class="res-row"><span>Rescued team yield</span><span>${Math.round(band.yield * 100)}%</span></div>
    <div class="res-row"><span>Assist intel</span><span>${iv}</span></div>` : '';
  $('combody').innerHTML = `<div class="res-row"><span>Position fix</span><span class="${band.id === 'pin' || band.id === 'good' ? 'ok' : 'warn'}">${band.name} // ${fix}</span></div>
    ${asst}
    <h2 style="margin-top:10px">Sitrep</h2>${lines.map(l => `<div class="mrow">${l}</div>`).join('')}
    <div id="comrescue">${comRescueHtml()}</div>
    <div class="controls"><button onclick="comClose()">CLOSE</button></div>`;
}

function droneReconAvail() {
  const w = state.dest ? world(state.dest) : null;
  if (!w || !comLink() || !w.stronghold || w.intel < 2 || w.status === 'captured') return { ok: false, label: 'RECON' };
  if (COMG || DRONE.isActive()) return { ok: false, label: 'RECON' };
  const cd = state.droneCd - Date.now();
  if (cd > 0) return { ok: false, label: 'READY ' + fmt(cd) };
  return { ok: true, label: 'RECON' };
}

function droneKeyUpdate() {
  const b = $('b-drone');
  if (!b) return;
  const a = droneReconAvail();
  b.disabled = !a.ok;
  b.classList.toggle('lit', a.ok);
  b.querySelector('small').textContent = a.label;
}

function droneRecon() {
  if (!droneReconAvail().ok) return;
  const w = world(state.dest);
  droneWid = w.id;
  DRONE.start({
    mode: 'recon', hazard: w.hazard, tier: droneTier(), theme: droneTheme(w), night: Math.random() < 0.25,
    team: { n: 'DRONE', col: '#ff9a7a', roles: ['S'] }, hurt: [], remain: droneRemain(),
    title: 'RECONNAISSANCE DRONE // ASSAULT SURVEY', sub: wname(w).toUpperCase() + ' // HAZARD ' + (HAZ_LABEL[w.hazard] || '').toUpperCase(),
    onDone: s => reconDone(w.id, s), onAbort: () => {}
  });
  droneKeyUpdate();
}

function reconDone(wid, s) {
  const w = world(wid);
  state.droneCd = Date.now() + DRONE_CD_MS;
  if (!w) { renderAll(); return; }
  const pct = s.total ? s.tagged / s.total : 0;
  const b = pct >= 1 ? { id: 'FULL PICTURE', red: 15, intel: 5 } : (pct >= 0.7 ? { id: 'GOOD', red: 10, intel: 4 } : (pct >= 0.4 ? { id: 'PARTIAL', red: 5, intel: 0 } : { id: 'POOR', red: 0, intel: 0 }));
  const red = s.spotted ? Math.floor(b.red / 2) : b.red;
  const intel = s.spotted ? 0 : b.intel;
  w.recon = { red, alert: !!s.spotted, id: b.id, tagged: s.tagged, total: s.total };
  if (intel > w.intel) w.intel = intel;
  log(`Drone survey of ${wname(w)}: ${s.tagged} of ${s.total} contacts tagged (${b.id}). Enemy strength estimate -${red}%.${s.spotted ? ' The drone was spotted and lost; the defenders are alerted (-10 points on assault odds).' : ''}${intel ? ' Intel raised to tier ' + intel + '.' : ''}`, s.spotted ? 'warn' : 'ok');
  renderAll();
}

function reconRed(w) { return w && w.recon ? w.recon.red : 0; }
function reconAlert(w) { return w && w.recon && w.recon.alert ? 0.1 : 0; }
function reconNote(w) {
  if (!w || !w.recon) return '';
  return ` Drone recon: enemy strength -${w.recon.red}%${w.recon.alert ? ', defenders alerted (-10 points)' : ''}.`;
}

setInterval(() => {
  if (DRONE.isActive() && (!comLink() || state.dest !== droneWid)) DRONE.linkLost();
  droneKeyUpdate();
}, 500);

function establishFix('''
rep("function establishFix(", new_fns)

rep("  const diffS = 100 - effDiff(w);\n", "  const diffS = 100 - effDiff(w) * (1 - reconRed(w) / 100);\n")
rep("+ gearAssault(teams) + jaffaBonus());", "+ gearAssault(teams) + jaffaBonus() - reconAlert(w));")
rep("including the ${assaultCost(w)} assault fee.`;", "including the ${assaultCost(w)} assault fee.${reconNote(w)}`;")
rep("    const p = Math.min(1, assaultChance(g.teams.filter(t => t.type === 'asl' || t.type === 'rec' || t.type === 'sec'), w) + vfx.assault);\n",
    "    const p = Math.min(1, assaultChance(g.teams.filter(t => t.type === 'asl' || t.type === 'rec' || t.type === 'sec'), w) + vfx.assault);\n    delete w.recon;\n")

rep('''            <button class="k com2" id="b-com2" onclick="com2()">COMM 2<small>CHECK-IN</small></button>
''', '''            <button class="k com2" id="b-com2" onclick="com2()">COMM 2<small>CHECK-IN</small></button>
            <button class="k com2" id="b-drone" onclick="droneRecon()">DRONE<small>RECON</small></button>
''')
rep("  $('b-com2').classList.toggle('lit', c2);\n", "  $('b-com2').classList.toggle('lit', c2);\n  droneKeyUpdate();\n")

rep("    lg: { units: {}, cdUntil: 0, open: false },\n", "    lg: { units: {}, cdUntil: 0, open: false },\n    droneCd: 0,\n")
rep("    sops: { reqs: Object.keys(state.sops.reqs)", "    dcdLeft: Math.max(0, state.droneCd - now),\n    sops: { reqs: Object.keys(state.sops.reqs)")
rep("  state.sops = { reqs: {}, pick: null };\n", "  state.droneCd = now + (d.dcdLeft || 0);\n  state.sops = { reqs: {}, pick: null };\n")

ov_css = '''
#drone { position: fixed; inset: 0; z-index: 95; overflow-y: auto; }
#drone[hidden] { display: none; }
#drone .dhead { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 8px; }
#drone .dhead .sub { margin-bottom: 0; text-align: left; }
#drone .dhead h1 { text-align: left; }
.kcom { gap: 4px; }
.kb .kcom button.k { height: 31px; min-height: 31px; padding: 0 8px; line-height: 1.1; }
.kb .kcom button.k small { font-size: 8px; }
'''
rep("</style>", dcss + ov_css + "</style>", 1) if src.count("</style>") == 1 else None
if src.count("</style>") != 1:
    i = src.index("</style>")
    src = src[:i] + dcss + ov_css + src[i:]

overlay = '''<div id="drone" hidden>
  <div class="wrap">
    <div class="dhead"><div><h1 id="dr_title"></h1><div class="sub" id="dr_sub"></div></div><button id="dr_abort" onclick="DRONE.abort()">ABORT</button></div>
    ''' + dhtml.strip() + '''
  </div>
</div>
'''
rep('<div id="rxgame" hidden>', overlay + '<div id="rxgame" hidden>')

rep("  if (COMG.phase === 'tune') comTune(dt, now);\n  else comTri(now);\n", "  if (COMG.phase === 'tune') comTune(dt, now);\n")
rep("""  } else if (COMG.phase === 'tri' && e.key === ' ') {
    e.preventDefault();
    e.stopImmediatePropagation();
    comLockBearing();
  }
""", "  }\n")

i = src.rindex('</body>')
src = src[:i] + '<script>\n' + engine + '</script>\n' + src[i:]

open('out.html', 'w', encoding='utf-8').write(src)
print('ok', len(src))
