import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.16') == 4, s.count('0.9.16')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.16</title>', '<title>Stargate Command 0.9.17</title>')
rep('BUILD 0.9.16', 'BUILD 0.9.17', 2)
rep("const BUILD_VER = '0.9.16';", "const BUILD_VER = '0.9.17';")

HW = r'''
  { n: 11, lv: 1, type: 1, hid: true, fac: 'Langaran', wname: 'Langara', name: 'Kelownan Survey Plate', lore: 'A survey plate from a Kelownan archive, stamped with a gate address that was never logged.',
    story: 'Cross-referencing the plate against the Stargate database, the Archeology Office found an address no team has dialed: Langara, a world that grew up cut off from the Goa\'uld and stayed hidden because its gate sat buried for generations.',
    hist: 'Langara is home to three nations, Kelowna, Terrania and the Andari Federation, held in an uneasy alliance by a Joint Ruling Council after long wars. It is the only known source of naquadria, a volatile derivative of naquadah, and its people have a mid-twentieth-century culture that the Goa\'uld never shaped.',
    rew: ['supplies', 100] },
  { n: 12, lv: 2, type: 2, hid: true, fac: 'Tollan', wname: 'Tollana', name: 'Tollana Registry Tablet', lore: 'A registry tablet of fine alloy, broken into tiles.',
    story: 'The reassembled tablet lists a world whose gate was removed from public records. The Tollan kept their home quiet to protect technology they considered too dangerous for younger worlds.',
    hist: 'The Tollan are an advanced human people known for phase-shift technology and the Ion Cannon defense that kept the Goa\'uld at bay. They are cautious about sharing it, judging other worlds not yet ready for it.',
    rew: ['research', 120] },
  { n: 13, lv: 3, type: 3, hid: true, fac: null, wname: 'Abydos', name: 'Abydonian Cartouche', lore: 'A royal cartouche carved with a sealed code of symbols.',
    story: 'The cartouche carries the seven symbols of the first world ever reached through the Stargate. Abydos was once a mining colony of Ra, and a team stepped through the gate there that began everything.',
    hist: '', rew: ['supplies', 200] },
  { n: 14, lv: 4, type: 3, hid: true, fac: "Tok'ra", wname: 'Vorash', name: "Tok'ra Memory Crystal", lore: 'A crystal case sealed with a lock of symbols.',
    story: 'The crystal holds a cipher-locked record of a refuge reached by a tunnel network. Its deduction code opens an address the Tok\'ra protect with great care.',
    hist: 'The Tok\'ra are symbiotes who broke from the Goa\'uld in the days of the queen Egeria. They work as infiltrators against the System Lords and are slow to trust, but Earth earned their alliance through shared enemies.',
    rew: ['research', 150] },
  { n: 15, lv: 4, type: 1, hid: true, fac: 'Free Jaffa', wname: 'Chulak', name: 'Jaffa Rebellion Tablet', lore: 'An oath tablet cracked in transit, with the mark of a free Jaffa cell.',
    story: 'The tablet names a rally point for Jaffa who turned against their false gods. Its fragments match a gate address held back from Goa\'uld spies.',
    hist: 'The Free Jaffa are warriors who rejected the gods they once served. Led by veterans such as Bra\'tac and Teal\'c, they fight to break the symbiote hold on their people and to win freedom for the Jaffa nation.',
    rew: ['supplies', 250] },
  { n: 16, lv: 5, type: 2, hid: true, fac: 'Asgard', wname: 'Orilla', name: 'Asgard Beam Chart', lore: 'A plate of beaming coordinates and engineering notes.',
    story: 'The reassembled chart shows beam coordinates and a gate address inside protected space. The Asgard have kept their last homeworld off every public map.',
    hist: 'The Asgard are a technologically advanced race who shielded young worlds, Earth among them, under a protection treaty. Their cloned bodies are failing, and they have long sought help against the genetic decay that threatens them.',
    rew: ['research', 250] },
  { n: 17, lv: 5, type: 3, hid: true, fac: 'Nox', wname: 'Nox Haven', name: 'Nox Forest Tablet', lore: 'A tablet in a gentle script, locked by a cipher of leaves.',
    story: 'The cipher opens a record of a forest world that no scanner can see. The Nox hide in plain sight and rarely leave a trace behind them.',
    hist: 'The Nox are a peaceful people who refuse to fight and cloak themselves from outsiders. Their healing is far beyond Earth medicine, and they once restored a fallen member of SG-1 to life.',
    rew: ['supplies', 300] }'''
rep("  { n: 10, lv: 5, type: 2, name: 'Repository Key Tablet', lore: 'A key tablet in the Ancients\\' own script.', facility: true }\n];",
    "  { n: 10, lv: 5, type: 2, name: 'Repository Key Tablet', lore: 'A key tablet in the Ancients\\' own script.', facility: true }," + HW + "\n];")

rep("miss: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 } };\n}", "miss: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }, hm: 0 };\n}")
rep("  Object.assign(b.miss, d.miss || {});\n", "  Object.assign(b.miss, d.miss || {});\n  b.hm = d.hm | 0;\n")
rep("function glAll() { return !!state.glyph && state.glyph.a.every(x => x.c); }", "function glAll() { return !!state.glyph && state.glyph.a.slice(0, 10).every(x => x.c); }")
rep("function glCount() { return state.glyph ? state.glyph.a.filter(x => x.c).length : 0; }", "function glCount() { return state.glyph ? state.glyph.a.slice(0, 10).filter(x => x.c).length : 0; }")

rep("  return msg;\n}\n\nfunction glSite(n) {", """  msg += hwFind(w);
  return msg;
}

function hwFind(w) {
  if (!w || w.kind !== 'normal' || !state.glyph) return '';
  const p = GL_ARTS.filter(a => a.hid && a.lv <= state.level && !glArt(a.n).f).sort((a, b) => a.n - b.n)[0];
  if (!p) return '';
  const chance = HW_CHANCE_BASE + HW_CHANCE_STEP * (state.glyph.hm | 0);
  if (Math.random() >= chance) { state.glyph.hm = (state.glyph.hm | 0) + 1; return ''; }
  state.glyph.hm = 0;
  glArt(p.n).f = true;
  sfx.chime();
  const t = ' An inscription was found: ' + p.name + '. It speaks of a hidden world. Decode it in the Archeology Office.';
  log('Inscription found on ' + wname(w) + ': ' + p.name + '. It speaks of a hidden world. Decode it in the Archeology Office.', 'ok');
  return t;
}

const HW_CHANCE_BASE = 0.4;
const HW_CHANCE_STEP = 0.3;

function hwOf(n) { return state.worlds.find(w => w.hart === n) || (state.hidden || []).find(w => w.hart === n) || null; }

function hwBuild(ar, extra) {
  const s = sysOf(ar.lv);
  const used = new Set(state.worlds.concat(state.hidden || [], extra || []).map(w => addrKey(w.addr)));
  let addr;
  do { addr = newTarget(); } while (used.has(addrKey(addr)));
  const idx = GL_ARTS.filter(a => a.hid && a.lv === ar.lv && a.n < ar.n).length;
  return {
    id: 'w' + (++worldSeq),
    code: 'A' + String(worldSeq).padStart(2, '0'),
    name: ar.wname,
    sector: s.star,
    addr,
    level: ar.lv,
    kind: ar.fac ? 'faction' : 'normal',
    faction: ar.fac || null,
    stronghold: false,
    diff: 0,
    type: WTYPES[Math.floor(Math.random() * WTYPES.length)],
    env: WENVS[Math.floor(Math.random() * WENVS.length)],
    hazard: ['low', 'med', 'high'][Math.floor(Math.random() * 3)],
    intel: 0,
    status: 'unexplored',
    orb: { r: 236 + idx * 14, a: 0.6 + ar.lv * 1.3 + idx * 2.4 },
    moons: [],
    stn: [],
    fresh: false,
    hart: ar.n
  };
}

function hwEnsure(lv, extra) {
  if (!state.hidden) state.hidden = [];
  GL_ARTS.filter(a => a.hid && a.lv === lv).forEach(ar => {
    if (hwOf(ar.n)) return;
    const w = hwBuild(ar, extra);
    if (glArt(ar.n).d) { w.intel = ar.fac ? 2 : 1; state.worlds.push(w); } else state.hidden.push(w);
  });
}

function hwMigrate() {
  if (!state.hidden) state.hidden = [];
  const busy = id => state.dest === id || state.teams.some(t => t.mission && t.mission.worldId === id);
  state.worlds.slice().forEach(w => {
    if (w.kind !== 'faction' || w.hart) return;
    const ar = GL_ARTS.find(a => a.hid && a.fac === w.faction);
    if (!ar) return;
    w.hart = ar.n;
    if (w.intel >= 2 || (state.fac.met && state.fac.met[w.faction]) || busy(w.id)) {
      const a = glArt(ar.n);
      a.f = true; a.d = true; a.c = true;
      if (w.intel < 2) w.intel = 2;
    } else {
      state.worlds.splice(state.worlds.indexOf(w), 1);
      state.hidden.push(w);
    }
  });
  for (let lv = 1; lv <= state.level; lv++) hwEnsure(lv);
}

function hwReveal(n) {
  const ar = GL_ARTS[n - 1];
  let w = (state.hidden || []).find(x => x.hart === n);
  if (w) {
    state.hidden.splice(state.hidden.indexOf(w), 1);
    w.fresh = true;
    w.intel = Math.max(w.intel, ar.fac ? 2 : 1);
    state.worlds.push(w);
  } else w = hwOf(n);
  if (w && ar.fac) factionContact(w, 'The Archeology Office', null);
  return w;
}

function hwPopHtml(ar, w) {
  let h = '<p>' + ar.story + '</p>';
  if (ar.fac) {
    const F = FACTIONS[ar.fac];
    h += '<h2>The ' + ar.fac + '</h2><p>' + ar.hist + '</p>';
    h += '<h2>What they offer</h2>';
    ['Partner', 'Ally', 'Sworn'].forEach((t, i) => { h += '<div class="res-row"><span>' + t + '</span><span>' + F.perk[i] + '</span></div>'; });
    h += '<div class="res-row"><span>Sworn income</span><span>' + F.pay[1] + ' ' + (F.pay[0] === 'research' ? 'research points' : 'supplies') + ' every 10 minutes</span></div>';
    h += '<p class="dim small">Send a Diplomat team with a Security team to raise standing. A Partner world cannot be lost.</p>';
  } else {
    h += '<p class="dim small">This world is open to Exploration missions like any other gate address.</p>';
  }
  h += '<div class="res-row"><span>Discovery reward</span><span class="ok">+' + ar.rew[1] + ' ' + (ar.rew[0] === 'research' ? 'research points' : 'supplies') + '</span></div>';
  return h;
}

function hwPop(n, first) {
  const ar = GL_ARTS[n - 1];
  const w = hwOf(n);
  let el = document.getElementById('hwpop');
  if (!el) {
    el = document.createElement('div');
    el.id = 'hwpop';
    el.innerHTML = '<div class="titlebox"><div class="title" id="hwtitle"></div><div class="sub" id="hwsub"></div><div class="panel" id="hwbody"></div><div class="controls" style="margin-top:10px"><button onclick="hwClose()">CLOSE</button></div></div>';
    document.body.appendChild(el);
  }
  document.getElementById('hwtitle').textContent = (first ? 'HIDDEN WORLD LOCATED // ' : 'HIDDEN WORLD // ') + (w ? w.name : ar.wname).toUpperCase();
  document.getElementById('hwsub').textContent = (w ? w.sector : sysOf(ar.lv).star).toUpperCase() + ' // LEVEL ' + ar.lv;
  document.getElementById('hwbody').innerHTML = hwPopHtml(ar, w);
  el.hidden = false;
}
function hwClose() {
  const el = document.getElementById('hwpop');
  if (el) el.hidden = true;
}

function hwRowHtml(n) {
  const a = glArt(n);
  const ar = GL_ARTS[n - 1];
  const here = glLinguists() > 0;
  let st;
  let btn = '';
  if (a.d) {
    const w = hwOf(n);
    st = '<span class="ok">WORLD REVEALED // ' + (w ? wname(w) : ar.wname) + '</span>';
    btn = '<button onclick="hwPop(' + n + ', false)">READ</button>';
  } else if (a.f) {
    st = '<span class="warn">INSCRIPTION FOUND' + (a.fails ? ' // ' + a.fails + ' failed' : '') + '</span>';
    btn = '<button onclick="glOpen(' + n + ')" ' + (here ? '' : 'disabled title="A Linguist must be on station"') + '>DECODE</button>';
  } else st = '<span class="dim">○ NO INSCRIPTION YET</span>';
  return '<div class="dispatch-row"><div><b>' + (a.f ? ar.name : 'Hidden world artifact') + '</b> <span class="dim">Level ' + ar.lv + ' // ' + GL_TYPES[ar.type] + '</span><div class="mrow">' + st + '</div></div><div>' + btn + '</div></div>';
}

function glSite(n) {""")

rep("function glDecoded(n) {\n  const a = glArt(n);\n  const ar = GL_ARTS[n - 1];\n  a.d = true;\n",
    """function glDecoded(n) {
  const a = glArt(n);
  const ar = GL_ARTS[n - 1];
  a.d = true;
  if (ar.hid) {
    a.c = true;
    const hw = hwReveal(n);
    if (ar.rew[0] === 'research') state.research += ar.rew[1];
    else state.res.supplies += ar.rew[1];
    const nm = hw ? wname(hw) : ar.wname;
    const t = 'Decoded: ' + ar.name + '. The address of ' + nm + (ar.fac ? ', home of the ' + ar.fac + ',' : '') + ' is now on the starmap. +' + ar.rew[1] + ' ' + (ar.rew[0] === 'research' ? 'research points' : 'supplies') + '.';
    log(t, 'ok');
    if (GLG) GLG.out = t;
    sfx.chime();
    hwPop(n, true);
    return;
  }
""")

rep("function gdMarkInit() {\n", "function gdMarkInit() {\n  if (GL_ARTS[GLG.n - 1].hid) { GLG.mark = null; return; }\n")

rep("h += glRowHtml(lv * 2 - 1) + glRowHtml(lv * 2);\n  return h;",
    """h += glRowHtml(lv * 2 - 1) + glRowHtml(lv * 2);
  const hws = GL_ARTS.filter(a => a.hid && a.lv === lv);
  if (hws.length) {
    h += '<h2>Hidden worlds</h2><p class="dim small">A decoded inscription of this kind reveals a hidden world and its address. Inscriptions turn up on Exploration missions.</p>';
    hws.forEach(a => { h += hwRowHtml(a.n); });
  }
  return h;""")

rep("function facLead(w, t, mid) {\n  if (!w || w.kind !== 'normal' || !state.fac) return '';",
    "function facLead(w, t, mid) {\n  return '';\n}\nfunction facLeadOld(w, t, mid) {\n  if (!w || w.kind !== 'normal' || !state.fac) return '';")
rep("No factions contacted yet. Survey worlds to find them.", "No factions contacted yet. Decode inscriptions in the Archeology Office to find their hidden worlds.")

rep("  s.factions.forEach(() => kinds.push('faction'));\n", "")
rep("  tagArmory(out);\n  return out;\n}", "  hwEnsure(lv, out);\n  tagArmory(out);\n  return out;\n}")

rep("    worlds: state.worlds,\n    research: state.research,", "    worlds: state.worlds,\n    hidden: state.hidden || [],\n    research: state.research,")
rep("  state.worlds = d.worlds;\n  upgradeWorlds(state.worlds);", "  state.worlds = d.worlds;\n  state.hidden = Array.isArray(d.hidden) ? d.hidden : [];\n  upgradeWorlds(state.worlds);")
rep("  Object.keys(FACTIONS).forEach(n => { if (!state.fac.met[n] && facKnown(n)) state.fac.met[n] = { t: '', by: '' }; });\n",
    "  Object.keys(FACTIONS).forEach(n => { if (!state.fac.met[n] && facKnown(n)) state.fac.met[n] = { t: '', by: '' }; });\n  hwMigrate();\n")

rep("#glgame[hidden] { display: none; }\n", """#glgame[hidden] { display: none; }
#hwpop { position: fixed; inset: 0; z-index: 95; display: flex; align-items: center; justify-content: center; overflow-y: auto; padding: 18px; background: rgba(2, 6, 12, 0.94); }
#hwpop[hidden] { display: none; }
#hwpop .titlebox { width: min(600px, 100%); margin-block: auto; }
#hwpop .panel p { margin: 8px 0; }
""")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
