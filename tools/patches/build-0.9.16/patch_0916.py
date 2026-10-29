import os
import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


assert s.count('0.9.15') == 4, s.count('0.9.15')
rep('<title>Stargate Command 0.9.15</title>', '<title>Stargate Command 0.9.16</title>')
rep('BUILD 0.9.15', 'BUILD 0.9.16', 2)
rep("const BUILD_VER = '0.9.15';", "const BUILD_VER = '0.9.16';")

rep("function regenPerMin() { return REGEN_BASE * (1 + [4, 6, 7].filter(n => state.gt.tier >= n && n <= rxRouted()).length) + glRegen(); }",
    "function relayRegen() {\n  if (!state.fobs) return 0;\n  const n = Object.values(state.fobs).filter(f => f.role === 'pw' && !f.dry).length;\n  return Math.min(FOB_RELAY_CAP, n * FOB_RELAY);\n}\nfunction regenPerMin() { return REGEN_BASE * (1 + [4, 6, 7].filter(n => state.gt.tier >= n && n <= rxRouted()).length) + glRegen() + relayRegen(); }")

rep("const FOB_UPKEEP = 15;\n", """const FOB_UPKEEP = 15;
const FOB_UPKEEP_STEP = 5;
const FOB_ROLE_COST = 100;
const FOB_RELAY = 2;
const FOB_RELAY_CAP = 8;
const FOB_ROLE_DEF = {
  sup: { name: 'Supply depot', short: 'SUPPLY', sup: 150, rp: 30 },
  rp: { name: 'Research outpost', short: 'RESEARCH', sup: 60, rp: 100 },
  pw: { name: 'Power relay', short: 'POWER', sup: 70, rp: 40 }
};
const FOB_ROLE_KEYS = ['sup', 'rp', 'pw'];
function fobUpkeepOf(id) { return FOB_UPKEEP + FOB_UPKEEP_STEP * Math.max(0, Object.keys(state.fobs || {}).indexOf(id)); }
function fobUpkeepTotal() { return Object.keys(state.fobs || {}).reduce((a, id) => a + fobUpkeepOf(id), 0); }
function fobSetRole(id, role) {
  const f = state.fobs && state.fobs[id];
  if (!f || !FOB_ROLE_DEF[role] || f.role === role || state.res.supplies < FOB_ROLE_COST) return;
  state.res.supplies -= FOB_ROLE_COST;
  const lost = f.stock.sup;
  const lostr = f.stock.rp;
  f.role = role;
  f.stock = { sup: 0, rp: 0 };
  log(`The base on ${wname(world(id))} was converted to a ${FOB_ROLE_DEF[role].name}. Cost ${FOB_ROLE_COST} supplies; the stockpile of ${lost} supplies and ${lostr} research points was cleared.`, 'warn');
  renderAll();
}
""")

rep("function fobEstablish(wid) {", "function fobEstablish(wid, role) {")
rep("state.fobs[wid] = { staff: fobStaffNew(), guard: FOB_GUARD,", "state.fobs[wid] = { role: FOB_ROLE_DEF[role] ? role : 'sup', staff: fobStaffNew(), guard: FOB_GUARD,")
rep("Cost ${FOB_COST} supplies. It produces ${FOB_SUP + FOB_PERK_SUP} supplies and ${FOB_RP + FOB_PERK_RP} research points every ${fmt(FOB_MS)}; a Tel'tak collects the stockpile.`, 'ok');",
    "Cost ${FOB_COST} supplies. Role: ${FOB_ROLE_DEF[f.role].name}, ${FOB_ROLE_DEF[f.role].sup} supplies and ${FOB_ROLE_DEF[f.role].rp} research points every ${fmt(FOB_MS)}${f.role === 'pw' ? ', and +' + FOB_RELAY + ' gate power per minute' : ''}; a Tel'tak collects the stockpile.`, 'ok');")

rep("""      if (state.res.supplies < FOB_UPKEEP) {
        if (!f.dry) log(`The base on ${wname(w)} could not be supplied (${FOB_UPKEEP} supplies upkeep) and produced nothing.`, 'warn');""",
"""      if (!f.role) f.role = 'sup';
      const upk = fobUpkeepOf(id);
      if (state.res.supplies < upk) {
        if (!f.dry) log(`The base on ${wname(w)} could not be supplied (${upk} supplies upkeep) and produced nothing.`, 'warn');""")
rep("        state.res.supplies -= FOB_UPKEEP;\n        f.dry = false;", "        state.res.supplies -= upk;\n        f.dry = false;")
rep("f.stock.sup = Math.min(FOB_CAP_SUP, f.stock.sup + FOB_SUP + FOB_PERK_SUP);\n          f.stock.rp = Math.min(FOB_CAP_RP, f.stock.rp + FOB_RP + FOB_PERK_RP);",
    "f.stock.sup = Math.min(FOB_CAP_SUP, f.stock.sup + FOB_ROLE_DEF[f.role].sup);\n          f.stock.rp = Math.min(FOB_CAP_RP, f.stock.rp + FOB_ROLE_DEF[f.role].rp);")

a = s.index("  const help = `<p class=\"dim small help\">A base makes ${FOB_SUP")
b = s.index("\n", a)
s = s[:a] + """  const help = `<p class="dim small help">Each base is built as a Supply depot (${FOB_ROLE_DEF.sup.sup} supplies and ${FOB_ROLE_DEF.sup.rp} research points per ${fmt(FOB_MS)}), a Research outpost (${FOB_ROLE_DEF.rp.sup} and ${FOB_ROLE_DEF.rp.rp}) or a Power relay (${FOB_ROLE_DEF.pw.sup} and ${FOB_ROLE_DEF.pw.rp}, and +${FOB_RELAY} gate power per minute, up to +${FOB_RELAY_CAP} in total). Changing a base's role costs ${FOB_ROLE_COST} supplies and clears its stockpile. Output stops when the stockpile holds ${FOB_CAP_SUP} supplies and ${FOB_CAP_RP} research points. Upkeep is ${FOB_UPKEEP} supplies per ${fmt(FOB_MS)} for the first base and ${FOB_UPKEEP_STEP} more for each base built before it; if the SGC cannot pay, that base produces nothing for the interval. A Tel'tak sent to the world loads up to ${TK_CAP_SUP} supplies and ${TK_CAP_RP} research points; a Logistic Truck sent with an Exploration team collects up to ${FOB_TRUCK_SUP} and ${FOB_TRUCK_RP}. Whatever is not loaded stays in the stockpile. While the System Lord of that level lives, the base is raided: answer with a Defend mission, or the garrison fights alone and the raiders carry off half the stockpile. Wounded recover slowly; killed are replaced one at a time for ${REPLACE_COST} supplies each, as with SGC teams. If every defender falls the stronghold is lost.</p>`;""" + s[b:]

rep("""    hb += `<div class="res-row"><span>Upkeep</span><span>${FOB_UPKEEP} SUP / ${fmt(FOB_MS)}${b.dry ? ' // <span class="warn">UNSUPPLIED</span>' : ''}</span></div>`;""",
    """    hb += `<div class="res-row"><span>Role</span><span>${FOB_ROLE_DEF[b.role || 'sup'].name.toUpperCase()} // ${FOB_ROLE_DEF[b.role || 'sup'].sup} SUP ${FOB_ROLE_DEF[b.role || 'sup'].rp} RP${(b.role || 'sup') === 'pw' ? ' // +' + FOB_RELAY + ' POWER/MIN' : ''}</span></div>`;
    hb += `<div class="res-row"><span>Upkeep</span><span>${fobUpkeepOf(id)} SUP / ${fmt(FOB_MS)}${b.dry ? ' // <span class="warn">UNSUPPLIED</span>' : ''}</span></div>`;""")

rep("""<button onclick="fobRecall('${id}')">${state.fobConfirm === id ? 'CONFIRM RECALL' : 'RECALL BASE'}</button></div>`;""",
    """<button onclick="fobRecall('${id}')">${state.fobConfirm === id ? 'CONFIRM RECALL' : 'RECALL BASE'}</button></div>`;
    hb += `<div class="controls" style="margin:0 0 12px;justify-content:flex-start">${FOB_ROLE_KEYS.filter(k => k !== (b.role || 'sup')).map(k => `<button onclick="fobSetRole('${id}','${k}')" ${state.res.supplies >= FOB_ROLE_COST ? '' : 'disabled'}>TO ${FOB_ROLE_DEF[k].short} // ${FOB_ROLE_COST} SUP</button>`).join('')}</div>`;""")

rep("""    hc += `<div class="staff-row"><span><b>${wname(w)}</b> <span class="dim">${sysOf(w.level).star} // captured</span></span><button onclick="fobEstablish('${w.id}')" ${state.res.supplies >= FOB_COST ? '' : 'disabled'}>ESTABLISH // ${FOB_COST} SUP</button></div>`;""",
    """    hc += `<div class="staff-row nob"><span><b>${wname(w)}</b> <span class="dim">${sysOf(w.level).star} // captured</span></span></div>`;
    hc += `<div class="controls" style="margin:0 0 12px;justify-content:flex-start">${FOB_ROLE_KEYS.map(k => `<button onclick="fobEstablish('${w.id}','${k}')" ${state.res.supplies >= FOB_COST ? '' : 'disabled'}>${FOB_ROLE_DEF[k].short} // ${FOB_COST} SUP</button>`).join('')}</div>`;""")

rep("const left = `<h2>Active bases <span class=\"dim\">${ids.length}</span></h2>${hb ||",
    "const left = `<h2>Active bases <span class=\"dim\">${ids.length}${ids.length ? ' // UPKEEP ' + fobUpkeepTotal() + ' SUP PER ' + fmt(FOB_MS) + (relayRegen() ? ' // RELAYS +' + relayRegen() + ' POWER/MIN' : '') : ''}</span></h2>${hb ||")

rep("const TK_FEE = 2;\n", "const TK_FEE = 2;\nconst TK_FUEL_LY = 4;\n")
rep("function tkWorldInfo(w) {", "function tkFuel(w) { return Math.max(1, Math.ceil(tkLy(w) / TK_FUEL_LY)); }\nfunction tkWorldInfo(w) {")
rep("return tkLy(w) + ' LY // ' + fmt(tkRoundMs(w)) + ' ROUND TRIP // ' + tail;", "return tkLy(w) + ' LY // ' + fmt(tkRoundMs(w)) + ' ROUND TRIP // ' + tkFuel(w) + ' NAQ // ' + tail;")
rep("!tkWorlds().includes(w) || state.res.supplies < TK_FEE) return;\n  state.res.supplies -= TK_FEE;",
    "!tkWorlds().includes(w) || state.res.supplies < TK_FEE || state.res.naquadah < tkFuel(w)) return;\n  const fuel = tkFuel(w);\n  state.res.supplies -= TK_FEE;\n  state.res.naquadah -= fuel;")
rep("Cost ${TK_FEE} supplies. Round trip", "Cost ${TK_FEE} supplies and ${fuel} naquadah. Round trip", 2)
rep("""<button ${w && state.res.supplies >= TK_FEE ? '' : 'disabled'} onclick="sendTeltak('${x.id}')">SEND // ${TK_FEE} SUP</button>""",
    """<button ${w && state.res.supplies >= TK_FEE && state.res.naquadah >= tkFuel(w) ? '' : 'disabled'} onclick="sendTeltak('${x.id}')">SEND // ${TK_FEE} SUP + ${w ? tkFuel(w) : '?'} NAQ</button>""")
rep("Tel'tak ships are never ambushed.", "Each run burns 1 naquadah per ${TK_FUEL_LY} light years of the system, rounded up, so the same naquadah cannot also be converted to power. Tel'tak ships are never ambushed.")

rep("o[k] = { staff: f.staff.map(m => Object.assign({}, m)), guard: f.guard,", "o[k] = { role: f.role || 'sup', dry: !!f.dry, staff: f.staff.map(m => Object.assign({}, m)), guard: f.guard,")
rep("state.fobs[k] = { staff: f.staff, guard: f.guard | 0,", "state.fobs[k] = { role: FOB_ROLE_DEF[f.role] ? f.role : 'sup', dry: !!f.dry, staff: f.staff, guard: f.guard | 0,")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
