import sys

src = open('base086.html', encoding='utf-8').read()


def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        print('MISMATCH', n, 'expected', count, 'for', old[:100])
        sys.exit(1)
    src = src.replace(old, new)


rep('<title>Stargate Command 0.8.5</title>', '<title>Stargate Command 0.8.6</title>')
rep('BUILD 0.8.5</div>', 'BUILD 0.8.6</div>', 2)

PAUSE_JS = r'''<script>
const PAUSE = (() => {
  const rn = Date.now.bind(Date);
  const rp = performance.now.bind(performance);
  const rsi = window.setInterval.bind(window);
  const keep = new Set();
  const reg = new Set();
  let n = 0;
  let at = 0;
  let atp = 0;
  let off = 0;
  let offp = 0;
  Date.now = () => (n ? at : rn()) - off;
  performance.now = () => (n ? atp : rp()) - offp;
  window.setInterval = (f, ms) => rsi(function () { if (n && !keep.has(f)) return; return f.apply(this, arguments); }, ms);
  const arm = o => {
    o.s = rp();
    o.id = setTimeout(() => { reg.delete(o); o.f(); }, o.ms);
  };
  return {
    keep: f => keep.add(f),
    later: (f, ms) => { const o = { f, ms }; reg.add(o); if (!n) arm(o); return o.id; },
    on: () => n > 0,
    pause: () => {
      if (n++) return;
      at = rn();
      atp = rp();
      reg.forEach(o => { if (o.s === undefined) return; clearTimeout(o.id); o.ms = Math.max(0, o.ms - (atp - o.s)); o.s = undefined; });
    },
    resume: () => {
      if (!n) return;
      if (--n) return;
      off += rn() - at;
      offp += rp() - atp;
      reg.forEach(arm);
    }
  };
})();
</script>
'''
rep('<script>const AUDIO_DATA=', PAUSE_JS + '<script>const AUDIO_DATA=')

rep('''function later(fn, ms) {
  const g = GEN;
  return setTimeout(() => { if (g === GEN) fn(); }, ms);
}''', '''function later(fn, ms) {
  const g = GEN;
  return PAUSE.later(() => { if (g === GEN) fn(); }, ms);
}''')

rep('''  <div class="panel wide">
    <h2>Operations log</h2>
    <div id="log" class="log"></div>
  </div>''', '''  <div class="panel wide">
    <h2 class="ltabs"><button id="lt-log" class="lt on" onclick="logTab('log')">OPERATIONS LOG</button><button id="lt-brief" class="lt" onclick="logTab('brief')">MISSION BRIEFING<span id="lt-n"></span></button></h2>
    <div id="log" class="log"></div>
    <div id="briefs" class="log" hidden></div>
  </div>''')

rep('id="fsbtn" onclick="toggleFullscreen()">FULL SCREEN</button>', 'id="fsbtn" onclick="toggleFullscreen()">FULL SCREEN</button><button onclick="tourReplay()">TOUR</button>')

CSS = r'''
.ltabs { display: flex; gap: 6px; flex-wrap: wrap; }
.lt { border: 1px solid var(--steel-dim); color: var(--dim); padding: 4px 10px; font-size: var(--fs-sm); letter-spacing: 0.18em; }
.lt.on { border-color: var(--accent); color: var(--accent); background: rgba(var(--accent-rgb), 0.10); }
.lt .nb { margin-left: 8px; color: var(--warn); }
#briefs[hidden], #log[hidden] { display: none; }
#briefs .bf { margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px solid var(--steel-dim); }
#briefs .bh { color: var(--accent); letter-spacing: 0.1em; font-size: var(--fs-sm); }
#briefs .bf.note .bh { color: var(--warn); }
#briefs .bf .controls { margin: 6px 0 0; justify-content: flex-start; }
#tour { position: fixed; inset: 0; z-index: 110; background: rgba(2, 6, 12, 0.78); }
#tour[hidden] { display: none; }
#tour.hi { background: transparent; }
#tourhi { position: fixed; border: 2px solid var(--accent); box-shadow: 0 0 0 9999px rgba(2, 6, 12, 0.78), 0 0 18px rgba(var(--accent-rgb), 0.7); border-radius: 3px; pointer-events: none; }
#tourhi[hidden] { display: none; }
#tourcard { position: fixed; left: 50%; transform: translateX(-50%); width: min(560px, 92vw); background: var(--panel); border: 1px solid var(--accent); box-shadow: 0 0 28px rgba(var(--accent-rgb), 0.25); padding: 16px 18px; }
#tourcard .tspk { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
#tourcard .tbadge { width: 40px; height: 40px; border: 1px solid var(--accent); display: flex; align-items: center; justify-content: center; color: var(--accent); letter-spacing: 0.06em; font-size: var(--fs-md); clip-path: polygon(25% 0, 75% 0, 100% 50%, 75% 100%, 25% 100%, 0 50%); background: rgba(var(--accent-rgb), 0.08); }
#tourcard .tname { color: var(--accent); letter-spacing: 0.2em; font-size: var(--fs-sm); }
#tourcard .tcnt { margin-left: auto; color: var(--dim); font-size: var(--fs-xs); letter-spacing: 0.16em; }
#tourcard .ttl { color: var(--dim); letter-spacing: 0.18em; font-size: var(--fs-xs); margin-bottom: 6px; }
#tourcard p { font-size: var(--fs-md); line-height: 1.55; margin: 0 0 14px; }
#tourcard .tbtn { display: flex; justify-content: space-between; gap: 10px; }
'''
i = src.index('</style>')
src = src[:i] + CSS + src[i:]

rep('''<div id="menu" hidden>''', '''<div id="tour" hidden>
  <div id="tourhi" hidden></div>
  <div id="tourcard">
    <div class="tspk"><div class="tbadge" id="tbadge"></div><div class="tname" id="tname"></div><div class="tcnt" id="tcnt"></div></div>
    <div class="ttl" id="tttl"></div>
    <p id="ttxt"></p>
    <div class="tbtn"><button id="tskip" onclick="tourSkip()">SKIP TOUR</button><button id="tnext" onclick="tourNext()">NEXT</button></div>
  </div>
</div>
<div id="menu" hidden>''')

rep('    droneCd: 0,\n    sops:', '    droneCd: 0,\n    tourDone: false,\n    briefs: [],\n    seen: {},\n    briefRead: 0,\n    logTab: \'log\',\n    sops:')

rep('    dcdLeft: Math.max(0, state.droneCd - now),\n', '    dcdLeft: Math.max(0, state.droneCd - now),\n    tourDone: state.tourDone,\n    briefs: state.briefs,\n    seen: state.seen,\n    briefRead: state.briefRead,\n')
rep('  state.droneCd = now + (d.dcdLeft || 0);\n', '''  state.droneCd = now + (d.dcdLeft || 0);
  state.tourDone = d.tourDone !== undefined ? d.tourDone : true;
  state.briefs = d.briefs || [];
  state.seen = d.seen || briefSeenAll();
  state.briefRead = d.briefRead || 0;
  state.logTab = 'log';
''')

rep('''function renderLog() {
  $('log').innerHTML = state.logs.map(l => `<div class="${l.cls}">[${l.t}] ${l.msg}</div>`).join('');
}''', '''function renderLog() {
  $('log').innerHTML = state.logs.map(l => `<div class="${l.cls}">[${l.t}] ${l.msg}</div>`).join('');
  renderBriefs();
}''')

rep('''function mend(r) {
  r.state = 'closed';
  r.ended = clock();
  const w = world(r.worldId);
  r.intelEnd = w ? w.intel : r.intelStart;
}''', '''function mend(r) {
  r.state = 'closed';
  r.ended = clock();
  const w = world(r.worldId);
  r.intelEnd = w ? w.intel : r.intelStart;
  briefMission(r);
}''')

rep("  log('Stargate Command online. Select a room, or enter the gate room and pick a destination on the starmap.');\n  beginGame();\n}",
    "  log('Stargate Command online. Select a room, or enter the gate room and pick a destination on the starmap.');\n  beginGame();\n  tourStart(false);\n}")

BRIEF_JS = r'''
const BRIEF_NOTES = {
  B1: ['SELECTING A DESTINATION', 'The selected world is shown on the dialing computer. Dialing costs power by distance. Use AUTO-DIAL, or rotate the ring and press LOCK on each symbol.'],
  B2: ['WORMHOLE ESTABLISHED', 'The wormhole stays open for 5 minutes. Choose teams in the Mission panel and press SEND. You can send several missions through one open wormhole.'],
  B3: ['INBOUND ACTIVATION', 'Returning teams come through the gate. Wait for the IDC, then open the iris. A closed iris turns the team away.'],
  B4: ['CASUALTIES', 'Injured personnel recover in the Infirmary. Killed personnel are replaced from supplies in the Barracks.'],
  B5: ['UNSCHEDULED ACTIVATION', 'The alert bar shows the IDC transponder. A friendly code comes with a team or allied name. An unrecognized signature is hostile, so close the iris.'],
  C1: ['STRONGHOLD IDENTIFIED', 'A Goa\'uld stronghold can be assaulted by Assault teams once surveyed. The estimate before sending combines camaraderie, team size and the stronghold\'s defenses. Capture them all to clear the level.'],
  C2: ['RESEARCH', 'Research points fund projects in the Science Lab: facility and gate upgrades, equipment and the Armory\'s alien technology.'],
  C3: ['ARMORY', 'Researched gear is bought here and issued to teams in the Barracks. Tel\'tak cargo ships are kept here for supply runs.'],
  C4: ['MOTOR POOL', 'MALPs survey worlds ahead of your teams. Trucks, drones and ATVs are built and upgraded with research, and they join missions to improve results.'],
  C5: ['DIPLOMACY', 'A friendly faction has been identified. Diplomat teams travel with a Security team to raise standing, which unlocks perks and, at Sworn, regular income.'],
  C6: ['LOGISTICS', 'Tel\'tak runs bring back a world\'s maximum supply roll. Up to two shipments can be in transit. Air Force Logistics can also send supply requests.'],
  C7: ['LEVEL CLEARED', 'The next system is unlocked, with new worlds on the starmap. The team limit rises by one per type.'],
  D1: ['RADIO CONTACT', 'An overdue team needs a radio fix. Tune the frequency out of the static, then fly the reconnaissance drone to the team. A better fix means a faster assist and a better yield. The wormhole timer keeps running.'],
  D2: ['RECONNAISSANCE DRONE', 'Tag every contact at the stronghold and stay out of the red view cones. An amber warning shows before a defender sees you. A full survey improves the assault odds and reveals intel. If the drone is spotted, the benefit is halved and the assault is harder. The drone then needs a 5 minute cooldown.'],
  D3: ['POWER EVENT', 'The reactor is unstable. Solve the conduit puzzle to restore balance, or abandon it and lose one output until you re-route power at the Quartermaster.'],
  D4: ['ANCIENT INSCRIPTION', 'A Linguist in the Archeology Office can decode it. Decoding reveals an artifact site, and a second Exploration mission there recovers the artifact.'],
  D5: ['PAPERWORK', 'General Hammond has forms to stamp. Stamp each by type, deny the flawed ones, and finish in 90 seconds. It pays supplies and a supply bonus on the next missions with a Logistic Truck.'],
  D6: ['ASK CARTER', 'Press ASK CARTER on a research project. Pick the one real explanation of four. A right answer adds research points. A wrong answer delays the project.'],
  D7: ['AFTER-ACTION REPORT', 'Open a closed mission in the Briefing Room mission log and press COMPLETE AAR. Type the report from the log. Accuracy decides the reward.']
};

function briefSeenAll() {
  const o = {};
  Object.keys(BRIEF_NOTES).forEach(k => { o[k] = true; });
  return o;
}

function logTab(k) {
  state.logTab = k;
  if (k === 'brief') state.briefRead = state.briefs.length;
  renderBriefs();
}

function renderBriefs() {
  const el = $('briefs');
  if (!el || !state.briefs) return;
  const on = state.logTab === 'brief';
  $('log').hidden = on;
  el.hidden = !on;
  $('lt-log').classList.toggle('on', !on);
  $('lt-brief').classList.toggle('on', on);
  const unread = on ? 0 : Math.max(0, state.briefs.length - state.briefRead);
  $('lt-n').innerHTML = unread ? `<span class="nb">${unread} NEW</span>` : '';
  if (on) state.briefRead = state.briefs.length;
  el.innerHTML = state.briefs.length ? state.briefs.map(b => `<div class="bf ${b.cls || ''}"><div class="bh">[${b.t}] BASE COMPUTER // ${b.title}</div><div>${b.body}</div>${b.mid ? `<div class="controls"><button onclick="briefOpen('${b.mid}')">OPEN MISSION LOG</button></div>` : ''}</div>`).join('') : '<div class="dim">No briefings yet. The base computer files one when a mission ends.</div>';
}

function briefOpen(mid) {
  showView('base');
  selectRoom('brief');
  openMissionLog(mid);
}

function postBrief(title, body, cls, mid) {
  if (!state.briefs) return;
  state.briefs.unshift({ t: clock(), title, body, cls: cls || '', mid: mid || '' });
  if (state.briefs.length > 60) state.briefs.pop();
  if (state.logTab === 'brief') state.briefRead = state.briefs.length;
  renderBriefs();
}

function briefNote(k) {
  if (!state.started || !state.seen || state.seen[k]) return;
  state.seen[k] = true;
  const n = BRIEF_NOTES[k];
  if (n) postBrief(n[0], n[1], 'note');
}

function briefMission(r) {
  if (!state.briefs || r.briefed) return;
  r.briefed = true;
  const y = r.yield || {};
  const w = world(r.worldId);
  const iEnd = r.intelEnd === null ? (w ? w.intel : r.intelStart) : r.intelEnd;
  const inj = aarNames(aarWho(r, ['injured']));
  const cas = aarNames(aarWho(r, ['killed', 'captured']));
  const out = r.result ? `${r.result}` : 'Mission closed.';
  const body = `${r.launch.map(c => c.name).join(', ')} // ${r.world}. ${out}<br>Yield: supplies ${y.supplies || 0}, naquadah ${y.naquadah || 0}, research ${y.research || 0}. Intel: tier ${r.intelStart} to ${iEnd}.<br>Injured: ${inj}. Killed or captured: ${cas}.${aarEligible(r) ? '<br>An After-Action Report can be filed for this mission.' : ''}`;
  postBrief(`MISSION COMPLETE // ${r.id} // ${KLABEL[r.kind]}`, body, '', r.id);
  briefNote('D7');
}

function briefWatch() {
  if (!state.started || !state.seen) return;
  const c = {
    B1: () => !!state.dest,
    B2: () => state.gate === 'open',
    B3: () => !!(state.incoming && state.incoming.ret),
    B4: () => allMembers().some(m => m.status === 'injured'),
    B5: () => !!(state.incoming && !state.incoming.ret),
    C1: () => state.worlds.some(w => w.stronghold && w.intel >= 2),
    C2: () => state.research > 0,
    C3: () => Object.keys(state.arm.done || {}).length > 0,
    C4: () => state.vehicles && state.vehicles.length > 0,
    C5: () => Object.keys((state.fac && state.fac.met) || {}).length > 0,
    C6: () => (state.arm.ships || []).length > 0 || Object.keys(state.lg.units || {}).length > 0,
    C7: () => state.level > 1,
    D3: () => !!(state.rx && state.rx.evt),
    D4: () => typeof GL_ARTS !== 'undefined' && state.glyph && GL_ARTS.some(a => glArt(a.n).f),
    D5: () => state.room === 'brief',
    D6: () => state.room === 'lab'
  };
  Object.keys(c).forEach(k => { if (!state.seen[k]) { let ok = false; try { ok = c[k](); } catch (e) { ok = false; } if (ok) briefNote(k); } });
}

setInterval(briefWatch, 1000);

const _com1 = com1;
com1 = function () { briefNote('D1'); return _com1.apply(this, arguments); };
const _droneRecon = droneRecon;
droneRecon = function () { if (droneReconAvail().ok) briefNote('D2'); return _droneRecon.apply(this, arguments); };

const TOUR_CARDS = [
  { who: 'GEN. HAMMOND', b: 'GH', ttl: 'WELCOME', txt: 'Welcome to Stargate Command. This installation sits under Cheyenne Mountain, and everything we do goes through that gate. You will send teams out, bring back what they find, and decide what the base does next. Colonel Carter will walk you through the facility.' },
  { who: 'COL. CARTER', b: 'SC', ttl: 'THE FACILITY', sel: '#map', txt: 'This is the Facility. Every room is on the map, and selecting one shows its staff, equipment and options. The Operations log along the bottom records everything that happens on base.' },
  { who: 'COL. CARTER', b: 'SC', ttl: 'RESOURCES', sel: '#res', txt: 'Supplies pay for missions and replacements. Power opens the gate, and naquadah can be converted into power. Research unlocks upgrades. All four totals are in the header.' },
  { who: 'GEN. HAMMOND', b: 'GH', ttl: 'TEAMS', sel: ".rcard[onclick=\"selectRoom('barracks')\"]", txt: 'The Barracks is where your teams live. You start with two Exploration teams. Look after them. Camaraderie grows with every successful mission, and it improves their odds when things go wrong.' },
  { who: 'COL. CARTER', b: 'SC', ttl: 'THE GATE ROOM', sel: '#tab-gate', txt: 'Open the GATE ROOM tab. The starmap lists the worlds we know about. The dialing computer dials the selected world, and the Mission panel sends teams once the wormhole is open. A wormhole stays open for five minutes.' },
  { who: 'GEN. HAMMOND', b: 'GH', ttl: 'THE MENU', sel: 'header .controls button', txt: 'MENU holds your saves, Settings, Help, Sound and Full Screen. The game saves on its own, and you can keep three save slots as well.' },
  { who: 'COL. CARTER', b: 'SC', ttl: 'WHAT TO EXPECT', sel: '#lt-brief', txt: 'From here on the base computer files a briefing when a mission ends, and a note the first time something new happens. Open the MISSION BRIEFING tab on the Operations log to read them.' },
  { who: 'GEN. HAMMOND', b: 'GH', ttl: 'YOUR FIRST ORDERS', txt: 'Pick a world on the starmap, dial it, and send an Exploration team through. Good luck. You can replay this tour from MENU.' }
];

const TOUR = { i: 0, on: false };

function tourStart(force) {
  if (TOUR.on || (!force && state.tourDone)) return;
  state.tourDone = true;
  TOUR.on = true;
  TOUR.i = 0;
  PAUSE.pause();
  showView('base');
  $('tour').hidden = false;
  document.addEventListener('keydown', tourKey, true);
  tourShow();
}

function tourReplay() {
  closeMenu();
  tourStart(true);
}

function tourShow() {
  const c = TOUR_CARDS[TOUR.i];
  if (c.sel && c.sel.indexOf('#lt-brief') === 0) logTab('log');
  $('tbadge').textContent = c.b;
  $('tname').textContent = c.who;
  $('tcnt').textContent = (TOUR.i + 1) + ' / ' + TOUR_CARDS.length;
  $('tttl').textContent = c.ttl;
  $('ttxt').textContent = c.txt;
  $('tnext').textContent = TOUR.i === TOUR_CARDS.length - 1 ? 'DONE' : 'NEXT';
  $('tskip').hidden = TOUR.i === TOUR_CARDS.length - 1;
  const hi = $('tourhi');
  const el = c.sel ? document.querySelector(c.sel) : null;
  const card = $('tourcard');
  card.style.top = '';
  card.style.bottom = '';
  if (el) {
    const r = el.getBoundingClientRect();
    hi.hidden = false;
    hi.style.left = (r.left - 4) + 'px';
    hi.style.top = (r.top - 4) + 'px';
    hi.style.width = (r.width + 8) + 'px';
    hi.style.height = (r.height + 8) + 'px';
    $('tour').classList.add('hi');
    if (r.top + r.height / 2 > window.innerHeight / 2) card.style.top = '70px';
    else card.style.bottom = '70px';
  } else {
    hi.hidden = true;
    $('tour').classList.remove('hi');
    card.style.top = Math.max(60, window.innerHeight / 2 - 120) + 'px';
  }
}

function tourNext() {
  if (!TOUR.on) return;
  if (TOUR.i >= TOUR_CARDS.length - 1) { tourEnd(); return; }
  TOUR.i++;
  tourShow();
}

function tourSkip() { tourEnd(); }

function tourEnd() {
  if (!TOUR.on) return;
  TOUR.on = false;
  $('tour').hidden = true;
  document.removeEventListener('keydown', tourKey, true);
  PAUSE.resume();
  renderAll();
}

function tourKey(e) {
  if (!TOUR.on) return;
  e.stopPropagation();
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tourNext(); }
  else if (e.key === 'Escape') { e.preventDefault(); tourSkip(); }
}

window.addEventListener('resize', () => { if (TOUR.on) tourShow(); });

PAUSE.keep(musTick);
PAUSE.keep(fitMain);
PAUSE.keep(briefWatch);
'''
rep('\nloadSettings();\n', BRIEF_JS + '\nloadSettings();\n')

rep('  return Math.min(1, Math.max(0, Math.min(100, (camS + sizeS + diffS) / 3)) / 100 + gearAssault(teams) + jaffaBonus() - reconAlert(w));',
    '  return Math.min(1, Math.max(0, Math.min(100, (camS + sizeS + diffS) / 3)) / 100 + gearAssault(teams) + jaffaBonus() + reconBonus(w) - reconAlert(w));')
rep('  const diffS = 100 - effDiff(w) * (1 - reconRed(w) / 100);', '  const diffS = 100 - effDiff(w);')
rep('function reconRed(w) { return w && w.recon ? w.recon.red : 0; }', 'function reconRed(w) { return w && w.recon ? w.recon.red : 0; }\nfunction reconBonus(w) { return reconRed(w) / 100; }')

rep("<span>Enemy strength estimate</span><span>-' + red + '%'", "<span>Assault odds</span><span>+' + red + ' points'")
rep("Enemy strength estimate -${red}%.${s.spotted", "Assault odds +${red} points.${s.spotted")
rep("Drone recon: enemy strength -${w.recon.red}%${w.recon.alert ? ', defenders alerted (-10 points)' : ''}.", "Drone recon: +${w.recon.red} points${w.recon.alert ? ', defenders alerted (-10 points)' : ''}.")

open('out086.html', 'w', encoding='utf-8').write(src)
print('ok', len(src))
