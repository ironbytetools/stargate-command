import sys, base64
src, dst, serp, evo = sys.argv[1:5]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.1') == 4, s.count('0.9.1')
s = s.replace('0.9.1', '0.9.2')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
rep('const AUDIO_DATA={', 'const AUDIO_DATA={"serpent": "' + b64(serp) + '", "evo": "' + b64(evo) + '", ')

rep("const MUSIC = { title: ['title'], calm: ['emanc', 'hathor'], tense: ['enemy'], win: ['credits'] };",
    "const MUSIC = { title: ['title'], calm: ['emanc', 'hathor', 'evo'], tense: ['enemy'], battle: ['serpent'], win: ['credits'] };")
rep("""  if (state.incoming || overdueTeams().length) return 'tense';""",
"""  if (Object.keys(state.dipl.alerts).length || state.teams.some(t => t.status === 'away' && t.mission && t.mission.kind === 'assault' && world(t.mission.worldId) && world(t.mission.worldId).lord)) return 'battle';
  if (state.incoming || overdueTeams().length) return 'tense';""")
rep("if (mus.mode !== 'tense' || want === 'win' || now - mus.since > 20000) {",
    "if ((mus.mode !== 'tense' && mus.mode !== 'battle') || want === 'win' || now - mus.since > 20000) {")

rep("const FOB_HEAL_MS = 120000;", "const FOB_HEAL_MS = 120000;\nconst FOB_PERK_SUP = 20;\nconst FOB_PERK_RP = 10;")
rep("""        f.stock.sup = Math.min(FOB_CAP_SUP, f.stock.sup + FOB_SUP);
        f.stock.rp = Math.min(FOB_CAP_RP, f.stock.rp + FOB_RP);""",
"""        f.stock.sup = Math.min(FOB_CAP_SUP, f.stock.sup + FOB_SUP + FOB_PERK_SUP);
        f.stock.rp = Math.min(FOB_CAP_RP, f.stock.rp + FOB_RP + FOB_PERK_RP);""")
s = s.replace('${FOB_SUP} supplies and ${FOB_RP} research', '${FOB_SUP + FOB_PERK_SUP} supplies and ${FOB_RP + FOB_PERK_RP} research')
assert s.count('FOB_SUP + FOB_PERK_SUP} supplies') >= 3
rep("The base makes 100 supplies and 50 research points every 6:30 until its stockpile is full, and a Tel\\'tak sent to that world collects it.",
    "The base makes 100 supplies and 50 research points every 6:30, plus 20 supplies from the archeologist and 10 research points from the scientist, until its stockpile is full. A Tel\\'tak sent to that world collects it all; a Logistic Truck sent with an Exploration team collects one payout (120 supplies and 60 research points).")
rep("""A Tel'tak sent to the world collects everything. While""", """A Tel'tak sent to the world collects everything; a Logistic Truck sent with an Exploration team collects one payout. The scientist and archeologist add ${FOB_PERK_RP} RP and ${FOB_PERK_SUP} supplies to each output. While""")

rep("vg, vfx, lid, due0: t.eta };", "vg, vfx, lid, due0: t.eta, truck: vsel.some(id => { const v = vehOf(id); return !!v && v.type === 'truck'; }) };")
rep("""        msg += ' Exploration failed: no research earned.';
      }
""", """        msg += ' Exploration failed: no research earned.';
      }
      if (m.truck && fobOn(w)) msg += fobTruck(w, yl);
""")
rep("function fobTick() {", """function fobTruck(w, yl) {
  const f = state.fobs[w.id];
  const a = Math.min(f.stock.sup, FOB_SUP + FOB_PERK_SUP);
  const r = Math.min(f.stock.rp, FOB_RP + FOB_PERK_RP);
  if (!a && !r) return ' The truck found the base stockpile empty.';
  f.stock.sup -= a;
  f.stock.rp -= r;
  state.res.supplies += a;
  state.research += r;
  yl.supplies = (yl.supplies || 0) + a;
  yl.research = (yl.research || 0) + r;
  return ` The truck hauled ${a} supplies and ${r} research points from the base stockpile.`;
}

function fobTick() {""")
rep("""    h += `<div class="dim small" style="margin:4px 0">${b.staff.map(m => m.role + ' ' + m.name).join(' // ')}</div>`;""",
    """    h += `<div class="dim small" style="margin:4px 0">${b.staff.map(m => m.role + ' ' + m.name).join(' // ')}</div>`;""")

rep("""      else if (known && !w.salvage) g.reasons.push('Nothing is left to recover on this captured stronghold.');""",
"""      else if (known && !w.salvage && !(fobOn(w) && state.selVeh.some(id => { const v = vehOf(id); return !!v && v.type === 'truck'; }))) g.reasons.push(fobOn(w) ? 'Send a Logistic Truck with the team to collect from the base.' : 'Nothing is left to recover on this captured stronghold.');""")
rep("""    if (m.forced) {
      if (w.intel < 2) w.intel = 2;""", """    if (w.stronghold && w.status === 'captured' && !w.salvage && fobOn(w)) {
      msg += '.' + fobTruck(w, yl);
    } else if (m.forced) {
      if (w.intel < 2) w.intel = 2;""")

rep(".dispatch-row button.mid, .staff-row button.mid, .res-row button.mid { width: auto; }", ".dispatch-row button.mid, .staff-row button.mid, .res-row button.mid { width: auto; }\n.staff-row > span:last-child:has(> button), .res-row > span:last-child:has(> button), .staff-row > span:last-child:has(> select), .res-row > span:last-child:has(> select) { flex: none; overflow: visible; }\n.dispatch-row > div:last-child:has(> button) { flex: none; }\n.staff-row > span:first-child, .res-row > span:first-child { min-width: 0; }")

rep("let h = '<h2>Forward Operating Bases</h2>';", "let h = '<h2 style=\"margin-top:20px\">Forward Operating Bases</h2>';")
rep('<div class="dim small" style="margin:4px 0">${b.staff', '<div class="dim small" style="margin:4px 0;text-align:left">${b.staff')

rep("function renderGate() {", """let PD = false;
let PDT = 0;
const HELD = new Map();
function pdRelease() {
  PD = false;
  clearTimeout(PDT);
  setTimeout(() => { const f = [...HELD.values()]; HELD.clear(); f.forEach(fn => fn()); }, 0);
}
document.addEventListener('pointerdown', () => { PD = true; clearTimeout(PDT); PDT = setTimeout(pdRelease, 1500); }, true);
['pointerup', 'pointercancel'].forEach(ev => document.addEventListener(ev, pdRelease, true));
window.addEventListener('blur', pdRelease);
(function () {
  const d = Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML');
  ['map', 'strip', 'dispatch', 'smmap', 'smpanel'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    Object.defineProperty(el, 'innerHTML', { configurable: true, get() { return d.get.call(this); }, set(h) {
      if (this.__h === h) { HELD.delete(this); return; }
      if (PD) { HELD.set(this, () => { this.innerHTML = h; }); return; }
      HELD.delete(this);
      this.__h = h;
      d.set.call(this, h);
    } });
  });
})();

function renderGate() {""")
rep("""  $('room').innerHTML = `<h2>${r.name} // ${r.lvl}</h2><p class="dim help">${r.desc}</p>` + strip + '<div class="rbody">' + body + '</div>';
  sectionize($('room').querySelector('.rbody'));""", """  const rh = `<h2>${r.name} // ${r.lvl}</h2><p class="dim help">${r.desc}</p>` + strip + '<div class="rbody">' + body + '</div>';
  if ($('room').__h === rh) { HELD.delete('room'); return; }
  if (PD) { HELD.set('room', renderRoom); return; }
  HELD.delete('room');
  $('room').__h = rh;
  $('room').innerHTML = rh;
  sectionize($('room').querySelector('.rbody'));""")


rep("\n.controls { justify-content: flex-start; }\n", "\n.controls { justify-content: flex-start; }\n#comgame .controls, #hpgame .controls, #ctgame .controls, #rxgame .controls, #glgame .controls, #xfer .controls, #menu .controls { justify-content: center; }\n#rxgame .controls button { min-width: 84px; }\n#titlescreen, #menu, #settings, #xfer, #comgame, #rxgame, #glgame, #hpgame, #ctgame { align-items: flex-start; }\n#titlescreen > *, #menu > *, #settings > *, #xfer > *, #comgame > *, #rxgame > *, #glgame > *, #hpgame > *, #ctgame > * { margin-block: auto; }\n#settings .controls button:not(.swatch), #xfer .controls button { min-width: 170px; }\n")
rep("EXPORT / IMPORT SAVES", "SAVE FILES")
rep("RESET TO DEFAULTS", "RESET DEFAULTS")
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
