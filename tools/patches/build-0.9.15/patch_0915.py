import os
import sys
src, dst = sys.argv[1:3]
D4 = os.environ.get('DIFF4', '65')
D5 = os.environ.get('DIFF5', '80')
ATV = os.environ.get('ATV_ASSAULT', '0.02')
s = open(src, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)


assert s.count('0.9.14') == 4, s.count('0.9.14')
rep('<title>Stargate Command 0.9.14</title>', '<title>Stargate Command 0.9.15</title>')
rep('BUILD 0.9.14', 'BUILD 0.9.15', 2)
rep("const BUILD_VER = '0.9.14';", "const BUILD_VER = '0.9.15';")

rep("{ n: 4, name: 'Reactor I', rp: 1000,", "{ n: 4, name: 'Reactor I', rp: 600,")

rep("planets: 6, holds: 1, factions: [\"Tok'ra\", 'Free Jaffa']", "planets: 6, holds: 2, factions: [\"Tok'ra\", 'Free Jaffa']")

rep("function levelTarget(lv) { return Math.min(100, BASE_DIFF * Math.pow(DIFF_STEP, lv - 1)); }",
    "const DIFF_LATE = { 4: " + D4 + ", 5: " + D5 + " };\nfunction levelTarget(lv) { return Math.min(100, DIFF_LATE[lv] || BASE_DIFF * Math.pow(DIFF_STEP, lv - 1)); }")

if ATV != '0.03':
    rep("perTier: { time: 0.10, assault: 0.03 }", "perTier: { time: 0.10, assault: " + ATV + " }")

rep("const FOB_PERK_RP = 10;\n", "const FOB_PERK_RP = 10;\nconst FOB_UPKEEP = 15;\nconst FOB_TRUCK_SUP = 250;\nconst FOB_TRUCK_RP = 125;\nconst TK_CAP_SUP = 400;\nconst TK_CAP_RP = 200;\n")

rep("""  const cost = f.dead * REPLACE_COST;
  if (state.res.supplies < cost) return;
  state.res.supplies -= cost;
  f.guard += f.dead;
  log(`${f.dead} security personnel were posted to ${wname(world(wid))} as replacements. Cost ${cost} supplies.`, '');
  f.dead = 0;
  renderAll();""", """  const rc = replaceCost();
  if (state.res.supplies < rc) return;
  if (rc === 0) state.fac.freeRepl[state.level] = true;
  state.res.supplies -= rc;
  f.dead--;
  f.guard++;
  sfx.chime();
  log(`A replacement security officer was posted to ${wname(world(wid))}. Cost ${rc} supplies.${rc === 0 ? ' Free Jaffa courtesy.' : ''}`, 'ok');
  renderAll();""")

rep("""  f.rt = Date.now() + RAID_CHECK_MS;
  if (f.guard <= 0) { fobOverrun(w); return; }
  const loss = n ? ` ${wd} wounded and ${kl} killed.` : ' No casualties.';
  log(`No team answered the raid on ${wname(w)}. The garrison ${strong ? 'drove the attackers off' : 'barely held'} with ${f.guard} fit defenders left.${loss}`, strong ? 'warn' : 'alert');""",
"""  f.rt = Date.now() + RAID_CHECK_MS;
  const ls = Math.floor(f.stock.sup / 2);
  const lr = Math.floor(f.stock.rp / 2);
  f.stock.sup -= ls;
  f.stock.rp -= lr;
  if (f.guard <= 0) { fobOverrun(w); return; }
  const loss = n ? ` ${wd} wounded and ${kl} killed.` : ' No casualties.';
  const loot = ls || lr ? ` The raiders carried off ${ls} supplies and ${lr} research points from the stockpile.` : '';
  log(`No team answered the raid on ${wname(w)}. The garrison ${strong ? 'drove the attackers off' : 'barely held'} with ${f.guard} fit defenders left.${loss}${loot}`, strong ? 'warn' : 'alert');""")

rep("const a = Math.min(f.stock.sup, FOB_SUP + FOB_PERK_SUP);\n  const r = Math.min(f.stock.rp, FOB_RP + FOB_PERK_RP);",
    "const a = Math.min(f.stock.sup, FOB_TRUCK_SUP);\n  const r = Math.min(f.stock.rp, FOB_TRUCK_RP);")

rep("""      f.next = now + FOB_MS;
      if (f.stock.sup < FOB_CAP_SUP || f.stock.rp < FOB_CAP_RP) {
        f.stock.sup = Math.min(FOB_CAP_SUP, f.stock.sup + FOB_SUP + FOB_PERK_SUP);
        f.stock.rp = Math.min(FOB_CAP_RP, f.stock.rp + FOB_RP + FOB_PERK_RP);
        ch = true;
        if (f.stock.sup >= FOB_CAP_SUP && f.stock.rp >= FOB_CAP_RP) log(`The stockpile on ${wname(w)} is full. Production is paused until a Tel'tak collects it.`, 'warn');
      }""", """      f.next = now + FOB_MS;
      if (state.res.supplies < FOB_UPKEEP) {
        if (!f.dry) log(`The base on ${wname(w)} could not be supplied (${FOB_UPKEEP} supplies upkeep) and produced nothing.`, 'warn');
        f.dry = true;
        ch = true;
      } else {
        state.res.supplies -= FOB_UPKEEP;
        f.dry = false;
        ch = true;
        if (f.stock.sup < FOB_CAP_SUP || f.stock.rp < FOB_CAP_RP) {
          f.stock.sup = Math.min(FOB_CAP_SUP, f.stock.sup + FOB_SUP + FOB_PERK_SUP);
          f.stock.rp = Math.min(FOB_CAP_RP, f.stock.rp + FOB_RP + FOB_PERK_RP);
          if (f.stock.sup >= FOB_CAP_SUP && f.stock.rp >= FOB_CAP_RP) log(`The stockpile on ${wname(w)} is full. Production is paused until a Tel'tak collects it.`, 'warn');
        }
      }""")

rep("""    hb += `<div class="res-row"><span>Raid check</span>""", """    hb += `<div class="res-row"><span>Upkeep</span><span>${FOB_UPKEEP} SUP / ${fmt(FOB_MS)}${b.dry ? ' // <span class="warn">UNSUPPLIED</span>' : ''}</span></div>`;
    hb += `<div class="res-row"><span>Raid check</span>""")

rep("""<button onclick="fobReplace('${id}')" ${b.dead && state.res.supplies >= b.dead * REPLACE_COST ? '' : 'disabled'}>REPLACE ${b.dead} // ${b.dead * REPLACE_COST} SUP</button>""",
    """<button onclick="fobReplace('${id}')" ${b.dead && state.res.supplies >= replaceCost() ? '' : 'disabled'}>REPLACE 1 // ${replaceCost()} SUP${b.dead ? ' (' + b.dead + ' LOST)' : ''}</button>""")

rep("""A Tel'tak sent to the world collects everything; a Logistic Truck sent with an Exploration team collects one payout. The scientist and archeologist add ${FOB_PERK_RP} RP and ${FOB_PERK_SUP} supplies to each output. While the System Lord of that level lives, the base is raided: answer with a Defend mission, or the garrison fights alone. Wounded recover slowly; killed are replaced for ${REPLACE_COST} supplies each. If every defender falls the stronghold is lost.""",
    """A Tel'tak sent to the world loads up to ${TK_CAP_SUP} supplies and ${TK_CAP_RP} research points; a Logistic Truck sent with an Exploration team collects up to ${FOB_TRUCK_SUP} and ${FOB_TRUCK_RP}. Whatever is not loaded stays in the stockpile. The scientist and archeologist add ${FOB_PERK_RP} RP and ${FOB_PERK_SUP} supplies to each output. Each base costs ${FOB_UPKEEP} supplies every ${fmt(FOB_MS)} in upkeep, paid from SGC supplies; if you cannot pay, it produces nothing that interval. While the System Lord of that level lives, the base is raided: answer with a Defend mission, or the garrison fights alone and the raiders carry off half the stockpile. Wounded recover slowly; killed are replaced one at a time for ${REPLACE_COST} supplies each, as with SGC teams. If every defender falls the stronghold is lost.""")

rep("""    x.load = { sup: f.stock.sup, rp: f.stock.rp };
    f.stock.sup = 0;
    f.stock.rp = 0;
    mev(x.lid, `Arrived at ${wname(w)}. Loaded ${x.load.sup} supplies and ${x.load.rp} research points from the base.`);""",
"""    x.load = { sup: Math.min(f.stock.sup, TK_CAP_SUP), rp: Math.min(f.stock.rp, TK_CAP_RP) };
    f.stock.sup -= x.load.sup;
    f.stock.rp -= x.load.rp;
    mev(x.lid, `Arrived at ${wname(w)}. Loaded ${x.load.sup} supplies and ${x.load.rp} research points from the base.${f.stock.sup || f.stock.rp ? ' ' + f.stock.sup + ' supplies and ' + f.stock.rp + ' research points remain in the stockpile.' : ''}`);""")

rep("""A run brings back the world's maximum supply roll (${TK_BASE} times the world's hazard multiplier), with no carry cap.""",
    """A run to an explored world brings back its maximum supply roll (${TK_BASE} times the world's hazard multiplier). A run to a base loads up to ${TK_CAP_SUP} supplies and ${TK_CAP_RP} research points; the rest stays in the stockpile.""")

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
