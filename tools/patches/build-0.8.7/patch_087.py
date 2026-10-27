import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
assert s.count('0.8.6') == 3, s.count('0.8.6')
s = s.replace('0.8.6', '0.8.7')
def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:70])
    s = s.replace(a, b)

rep("const KLABEL = { def: 'Defense', dip: 'Diplomacy', exp: 'Exploration', rec: 'Recon', assist: 'Assist', assault: 'Assault', malp: 'MALP' };",
    "const KLABEL = { def: 'Defense', dip: 'Diplomacy', exp: 'Exploration', rec: 'Recon', assist: 'Assist', assault: 'Assault', malp: 'MALP', tk: \"Tel'tak\" };")

rep("""  x.rolled = false;
  later(() => teltakDue(sid), ms);
  sfx.chime();
  log(`${tkName(x)} departed on a supply run to ${wname(w)}. Cost ${TK_FEE} supplies. Round trip ${fmt(ms)}.`, '');""",
"""  x.rolled = false;
  x.lid = openMission('tk', w, [], { ship: tkName(x) + ' (' + (x.id === 'tk2' ? 'Level 3' : 'Level 2') + ' wreck)' });
  mev(x.lid, `${tkName(x)} departed for ${wname(w)}. Cost ${TK_FEE} supplies. Round trip ${fmt(ms)}.`);
  later(() => tkArrive(sid), Math.round(ms / 2));
  later(() => teltakDue(sid), ms);
  sfx.chime();
  log(`${tkName(x)} departed on a supply run to ${wname(w)}. Cost ${TK_FEE} supplies. Round trip ${fmt(ms)}.`, '');""")

rep("""function teltakDue(sid) {
  const x = state.arm.ships.find(s => s.id === sid);
  if (!x || x.status !== 'away') return;
  const w = world(x.world);
  if (!x.rolled) {""",
"""function tkArrive(sid) {
  const x = state.arm.ships.find(s => s.id === sid);
  if (!x || x.status !== 'away' || x.arrived) return;
  x.arrived = true;
  const w = world(x.world);
  mev(x.lid, `Arrived at ${w ? wname(w) : 'the world'}. Cargo loading.`);
}

function teltakDue(sid) {
  const x = state.arm.ships.find(s => s.id === sid);
  if (!x || x.status !== 'away') return;
  const w = world(x.world);
  if (!x.arrived) tkArrive(sid);
  if (!x.rolled) {""")

rep("""      later(() => teltakDue(sid), extra);
      log(`${tkName(x)} was delayed on the return from ${w ? wname(w) : 'its run'}. Arriving ${fmt(extra)} late.`, 'warn');""",
"""      later(() => teltakDue(sid), extra);
      mflag(x.lid, 'delayed');
      mev(x.lid, `Delayed on the return leg. Arriving ${fmt(extra)} late.`);
      log(`${tkName(x)} was delayed on the return from ${w ? wname(w) : 'its run'}. Arriving ${fmt(extra)} late.`, 'warn');""")

rep("""  x.rolled = false;
  sfx.chime();
  log(`${tkName(x)} returned from ${w ? wname(w) : 'its run'} with ${y} supplies.`, 'ok');""",
"""  x.rolled = false;
  x.arrived = false;
  mresult(x.lid, null, { supplies: y });
  mclose(x.lid, `Returned from ${w ? wname(w) : 'its run'} with ${y} supplies.`);
  x.lid = null;
  sfx.chime();
  log(`${tkName(x)} returned from ${w ? wname(w) : 'its run'} with ${y} supplies.`, 'ok');""")

rep("""  const flags = [r.ambushed && (r.state !== 'active' || r.known) ? 'ambushed' : '', r.overdue ? 'overdue' : '', r.rescued ? 'rescued' : ''].filter(Boolean).join(', ') || 'None';""",
"""  const flags = [r.ambushed && (r.state !== 'active' || r.known) ? 'ambushed' : '', r.delayed ? 'delayed' : '', r.overdue ? 'overdue' : '', r.rescued ? 'rescued' : ''].filter(Boolean).join(', ') || 'None';
  if (r.kind === 'tk') {
    let t = `<div class="dispatch-row"><div><h2>${r.id} // ${KLABEL[r.kind]}</h2></div><button onclick="closeMissionLog()">BACK</button></div>`;
    t += '<h2>Summary</h2>' + row('Ship', r.ship || "Tel'tak") + row('Destination', `${r.world} // hazard ${hzLabel(r)}`) + row('Launched', r.started) + row('Ended', r.ended || 'In progress') + row('Status', r.state === 'active' ? 'ACTIVE' : 'CLOSED') + row('Flags', flags) + `<div class="mrow">${r.result || 'Supply run in progress.'}</div>`;
    t += '<h2 style="margin-top:10px">Cargo</h2>' + row('Supplies returned', y.supplies || 0);
    t += '<h2 style="margin-top:10px">Events</h2>' + (r.events.length ? r.events.map(e => `<div class="mrow"><span class="dim">[${e.t}]</span> ${e.msg}</div>`).join('') : '<p class="dim">No events.</p>');
    return t;
  }""")

rep("""  if (!state.briefs || r.briefed) return;
  r.briefed = true;""",
"""  if (!state.briefs || r.briefed || r.kind === 'tk') return;
  r.briefed = true;""")

rep("""  state.arm.ships.forEach(x => { if (x.status === 'away') { const id = x.id; later(() => teltakDue(id), Math.max(0, x.eta - Date.now())); } });""",
"""  state.arm.ships.forEach(x => { if (x.status === 'away') { const id = x.id; if (!x.arrived && x.lid) { const mr = mfind(x.lid); const w = world(x.world); const half = w ? tkRoundMs(w) / 2 : 0; if (mr && w) later(() => tkArrive(id), Math.max(0, x.eta - half - Date.now())); } later(() => teltakDue(id), Math.max(0, x.eta - Date.now())); } });""")

rep(""".mc.layer button { font-size: 11px; letter-spacing: 0.1em; padding: 0 12px; }""",
""".mc.layer button { font-size: 11px; letter-spacing: 0.1em; padding: 0 12px; }
.mc.smban { left: 50%; top: 52px; transform: translateX(-50%); flex-direction: column; align-items: center; gap: 4px; padding: 10px 18px; background: rgba(4, 14, 24, 0.94); border: 1px solid var(--accent); box-shadow: 0 0 16px rgba(var(--accent-rgb), 0.35); text-align: center; max-width: 82%; }
.mc.smban b { color: var(--accent); letter-spacing: 0.18em; font-size: 15px; }
.mc.smban span { font-size: 12px; color: #bfe9f2; }
.mc.smban button { height: 28px; font-size: 11px; letter-spacing: 0.1em; margin-top: 4px; }""")

rep("""          <div class="mc layer"><button id="sm-toggle" onclick="toggleLayer()">GALAXY CHART</button></div>""",
"""          <div class="mc layer"><button id="sm-toggle" onclick="toggleLayer()">GALAXY CHART</button></div>
          <div class="mc smban" id="smban" hidden></div>""")

rep("""function checkLevel() {
  const L = state.level;
  const holds = state.worlds.filter(x => x.level === L && x.stronghold);
  if (!holds.length || !holds.every(x => x.status === 'captured')) return;""",
"""function checkLevel() {
  const L = state.level;
  const holds = state.worlds.filter(x => x.level === L && x.stronghold);
  if (!holds.length || !holds.every(x => x.status === 'captured')) return;
  state.banners = state.banners || {};
  if (!state.banners[L]) { state.banners[L] = 1; state.smBanner = L; }""")

rep("""function closeStarmap() {""",
"""function sysCleared(lv) {
  const ws = state.worlds.filter(w => w.level === lv);
  return ws.length > 0 && ws.every(w => peaceful(w) || ((w.kind === 'lab' || w.kind === 'ship') && (w.status === 'explored' || w.status === 'captured')));
}

function checkCleared() {
  const seed = !state.clearedSys;
  state.clearedSys = state.clearedSys || {};
  SYSTEMS.forEach(s => {
    if (s.lv > state.level || state.clearedSys[s.lv] || !sysCleared(s.lv)) return;
    state.clearedSys[s.lv] = 1;
    if (!seed) log(`${s.star} system CLEARED. Every world at Level ${s.lv} is now peaceful.`, 'ok');
  });
}

function dismissSmBanner() { state.smBanner = null; renderStarmapMap(); }

function smBannerHtml() {
  const lv = state.smBanner;
  if (!lv) return '';
  const s = sysOf(lv);
  const last = lv >= MAX_LEVEL;
  return `<b>${s.star.toUpperCase()} // LEVEL ${lv} SECURED</b><span>The final stronghold has fallen.${last ? ' Every charted system is secured.' : ` Level ${lv + 1} is unlocked: ${sysOf(lv + 1).star} is now on the chart.`}</span><button onclick="dismissSmBanner()">ACKNOWLEDGE</button>`;
}

function closeStarmap() {""")

rep("""    const fresh = state.worlds.some(w => w.level === s.lv && w.fresh);
    const sel = state.mapSys === s.lv;""",
"""    const fresh = state.worlds.some(w => w.level === s.lv && w.fresh);
    const sel = state.mapSys === s.lv;
    const clr = sysCleared(s.lv);""")

rep("""    h += `<text class="sub" style="font-size:${(9 * sc).toFixed(1)}px" x="${g.x.toFixed(1)}" y="${(g.y + 39 * sc).toFixed(1)}">LEVEL ${s.lv} // ${s.ly} LY</text>`;
    h += '</g>';""",
"""    h += `<text class="sub" style="font-size:${(9 * sc).toFixed(1)}px" x="${g.x.toFixed(1)}" y="${(g.y + 39 * sc).toFixed(1)}">LEVEL ${s.lv} // ${s.ly} LY</text>`;
    if (clr) h += `<circle cx="${g.x.toFixed(1)}" cy="${g.y.toFixed(1)}" r="${(11 * sc).toFixed(1)}" fill="none" stroke="#6dff9e" stroke-width="${(1.6 * sc).toFixed(2)}"/><text x="${g.x.toFixed(1)}" y="${(g.y - 16 * sc).toFixed(1)}" text-anchor="middle" fill="#6dff9e" style="font-size:${(9.5 * sc).toFixed(1)}px;letter-spacing:.16em">&#10003; CLEARED</text>`;
    h += '</g>';""")

rep("""    $('smlevel').textContent = `${s.star.toUpperCase()} // LEVEL ${sysLv} // STRONGHOLDS ${done} / ${holds.length} // UNEXPLORED ${unexp}`;
  }""",
"""    $('smlevel').textContent = `${s.star.toUpperCase()} // LEVEL ${sysLv} // STRONGHOLDS ${done} / ${holds.length} // UNEXPLORED ${unexp}${sysCleared(sysLv) ? ' // CLEARED' : ''}`;
  }
  checkCleared();
  const bn = $('smban');
  if (bn) { const bh = smBannerHtml(); bn.hidden = !bh; if (bn.innerHTML !== bh) bn.innerHTML = bh; }""")

rep("""    mapSys: 1,
    cleared: false,""", """    mapSys: 1,
    cleared: false,
    banners: {},
    smBanner: null,
    clearedSys: {},""")
rep("""    cleared: state.cleared,
    atlantis""", """    cleared: state.cleared,
    banners: state.banners,
    smBanner: state.smBanner,
    clearedSys: state.clearedSys,
    atlantis""")
rep("""  state.cleared = !!d.cleared;""", """  state.cleared = !!d.cleared;
  state.banners = d.banners || {};
  state.smBanner = d.smBanner || null;
  state.clearedSys = d.clearedSys || null;""")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
