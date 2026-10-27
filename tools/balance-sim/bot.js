(function(){
const cfg = window.__CFG;
const B = window.BOT = { cfg, t0: Date.now(), job: null, ev: [], series: [], wait: {power:0,supplies:0,cooldown:0,team:0,other:0,busy:0}, inc: {explore:0,logistics:0,wormhole:0,wormholeHostile:0}, spent: {explore:0,recon:0,raise:0,assault:0,other:0}, dials:0, assaults: [], done:null, lastMin:-1 };
window.autosaveNow=function(){}; window.scheduleAutosave=function(){};
const tm = () => (Date.now()-B.t0)/60000;
const ev = (k, d) => B.ev.push(Object.assign({t:+tm().toFixed(2), k}, d||{}));
['renderHud','renderMap','updateMarkers','renderAlert','renderLog','renderMissions','renderStrip','renderAll','renderGate','renderHeader','renderStores','renderRoom','renderDC','renderChevrons','renderStarmapMap','renderStarmap','renderFacility'].forEach(n=>{ if (typeof window[n]==='function') window[n]=function(){}; });
const _fm = window.finishMission; window.finishMission = function(t){ const b=state.res.supplies; _fm.apply(this, arguments); B.inc.explore += state.res.supplies-b; };
const _lg = window.lgDue; window.lgDue = function(id){ const b=state.res.supplies; _lg.apply(this, arguments); const d=state.res.supplies-b; if(d>0){B.inc.logistics+=d; ev('logistics',{id,d});} };
const _ri = window.resolveIncoming; window.resolveIncoming = function(){ const inc=state.incoming; const b=state.res.supplies; _ri.apply(this, arguments); const d=state.res.supplies-b; if(inc && !inc.ret){ if(d>0){B.inc.wormhole+=d; ev('wormhole',{d});} else if(d<0){B.inc.wormholeHostile+=d; ev('hostile',{d});} } };
const _rs = window.resolveAssault; window.resolveAssault = function(){ const b=state.level; _rs.apply(this, arguments); ev('assaultResolved',{lvl:state.level}); };
B.glog=[]; const _log=window.log; window.log=function(msg,cls){ B.glog.push([+tm().toFixed(2), msg]); return _log.apply(this, arguments); };
if(cfg.lockNeed!=null){ window.finalLocked=function(w){ if(!w.stronghold||w.status==='captured') return false; const left=holdsLeft(); if(left.length!==1||left[0].id!==w.id) return false; const reg=state.worlds.filter(x=>x.level===state.level&&!x.stronghold); const d=reg.filter(x=>x.status==='explored'||x.status==='captured').length; return d<Math.min(cfg.lockNeed,reg.length); }; }
if(cfg.injP!=null){ window.rollHit=function(t){ const m=t.mission; if(Math.random()<cfg.injP && Math.random()>=injMod(t)){ const pool=t.members.filter(x=>x.status==='ready'); if(pool.length) m.hitId=pool[Math.floor(Math.random()*pool.length)].id; } }; }
if(cfg.twoExp){ state.teams.push(makeTeam('exp',1)); }
const idleGate = () => state.gate==='closed' && !state.incoming && !state.busy && state.chevrons===0;
const L = () => state.worlds.filter(w=>w.level===state.level);
const teamOf = type => state.teams.find(t=>t.type===type);
const readyTeam = type => state.teams.find(t=>t.type===type && teamReady(t));
function startJob(kind, w, types, mtype, malp){
  B.job = {kind, wid:w.id, types, mtype, malp:!!malp, t:Date.now(), stage:'dial'};
  setDest(w.id);
  if(state.dest!==w.id){ B.job=null; return false; }
  autoDial();
  B.dials++;
  ev('dial',{kind, world:w.name, cost:gateCostFor(w), supplies:state.res.supplies, power:state.res.power});
  return true;
}
function stepJob(){
  const j = B.job; if(!j) return;
  if(Date.now()-j.t > 180000 && j.stage==='dial'){ ev('dialTimeout'); B.job=null; try{ state.abortDial=true; }catch(e){} return; }
  if(j.stage==='dial'){
    if(state.gate==='open' && !state.incoming && state.dest===j.wid && gateReady()){
      state.sel = []; state.selVeh=[]; state.withMalp=false;
      j.types.forEach(tp=>{ const t=readyTeam(tp); if(t) state.sel.push(t.id); });
      setMType(j.mtype);
      if(j.malp){ const m=homeMalp(); if(m){ state.withMalp=true; state.malpPick=m.id; } }
      const g = checkGroup();
      if(!g.ok){ ev('sendBlocked',{why:g.reasons.join('|')}); disengage(); B.job=null; return; }
      const sup0=state.res.supplies;
      dispatch();
      const spent = sup0-state.res.supplies;
      if(j.kind==='explore') B.spent.explore+=spent; else if(j.kind==='assault') B.spent.assault+=spent; else B.spent.recon+=spent;
      ev('send',{kind:j.kind, cost:spent, est: g.est});
      if(state.gate==='open' && !state.incoming) disengage();
      B.job=null;
    } else if(state.gate==='closed' && !state.busy && !state.incoming && state.chevrons===0 && Date.now()-j.t>5000){
      ev('dialFailed'); B.job=null;
    }
  }
}
function pickExploreWorld(){
  const away = new Set(state.teams.filter(t=>t.status==='away'&&t.mission&&t.mission.worldId).map(t=>t.mission.worldId));
  const reg0 = L().filter(w=>!w.stronghold && w.kind!=='ship');
  const reg = reg0.filter(w=>!away.has(w.id)).length ? reg0.filter(w=>!away.has(w.id)) : reg0;
  const un = reg.filter(w=>w.status!=='explored' && w.status!=='captured');
  if(un.length) return un.sort((a,b)=>gateCostFor(a)-gateCostFor(b))[0];
  return reg.sort((a,b)=>gateCostFor(a)-gateCostFor(b))[0];
}
function decide(){
  const held = L().filter(w=>w.stronghold && w.status!=='captured')[0];
  const reg = L().filter(w=>!w.stronghold);
  const allExplored = held ? !finalLocked(held) : false;
  const sup = state.res.supplies, pw = state.res.power;
  const cd = cooldownLeft()>0;
  const exp = readyTeam('exp'), rec = readyTeam('rec');
  const pc = w => gateCostFor(w)+AUTO_COST;
  for(const t of state.teams){ for(const m of t.members){ if(m.status==='killed' && state.res.supplies>=replaceCost()){ replaceMember(t.id,m.id); B.spent.replace=(B.spent.replace||0)+REPLACE_COST; ev('replace',{t:t.type}); return; } } }
  if(!teamOf('rec') && reg.some(w=>w.status==='explored') && sup>=20+cfg.reserve){ raiseTeam('rec'); B.spent.raise+=20; ev('raise',{t:'rec'}); return; }
  if(held && held.intel<2 && rec){
    if(pw>=pc(held) && sup>=3){ startJob('recon', held, ['rec'], 'rec', false); return; }
    B.wait.power++; return;
  }
  if(held && allExplored && held.intel>=2){
    const aslT = teamOf('asl');
    const blocked = aslT && aslT.members.some(m=>m.status==='captured');
    if(!aslT && sup>=40+ASSAULT_BASE+11){ raiseTeam('asl'); B.spent.raise+=40; ev('raise',{t:'asl'}); return; }
    if(blocked && !teamOf('sec') && sup>=25+ASSAULT_BASE+11){ raiseTeam('sec'); B.spent.raise+=25; ev('raise',{t:'sec'}); return; }
    const fighters = ['asl','sec'].map(readyTeam).filter(Boolean);
    if(fighters.length){
      const grp = fighters.map(t=>t.type).concat(rec?['rec']:[]);
      const need = assaultCost(held)+grp.reduce((a,tp)=>a+TYPES[tp].cost,0);
      if(cd){ B.wait.cooldown++; }
      else if(sup<need){ B.wait.supplies++; }
      else if(pw<pc(held)){ B.wait.power++; return; }
      else { if(startJob('assault', held, grp, 'asl', false)) return; }
    } else if(aslT) { B.wait.fighters=(B.wait.fighters||0)+1; }
  }
  if(!exp){ B.wait.team++; return; }
  const w = pickExploreWorld();
  if(!w) return;
  if(sup < TYPES.exp.cost){ B.wait.supplies++; return; }
  if(pw < pc(w)){ B.wait.power++; return; }
  startJob('explore', w, ['exp'], 'exp', false);
}
setInterval(function(){
  if(B.done) return;
  const m = Math.floor(tm());
  if(m!==B.lastMin){ B.lastMin=m; B.series.push([m, state.res.supplies, Math.round(state.res.power), state.res.naquadah, state.research]); }
  if(state.level>=2){ B.done = {t:tm(), lvl:state.level}; ev('level2'); return; }
  if(state.res.naquadah>=1 && state.res.power<=POWER_CAP-15){ convertNaq(); B.inc.naqConv=(B.inc.naqConv||0)+1; }
  if(cfg.logistics){ ['hill','peterson'].forEach(id=>{ const u=lgUnit(id); if(u.lv<=state.level && !state.lg.units[id] && lgCdLeft()<=0 && Object.keys(state.lg.units).length<LG_MAX){ lgRequest(id); } }); }
  const inc = state.incoming;
  if(inc){
    if(!inc.ret && !inc.friendly && !state.irisClosed){ toggleIris(); }
    else if(!inc.ret && !state.irisClosed && !inc.idc){ toggleIris(); }
    if(inc.idc && inc.friendly && state.irisClosed){ toggleIris(); }
    return;
  }
  if(B.job){ stepJob(); return; }
  if(!idleGate()){ B.wait.busy++; return; }
  if(dueTeams().length) { return; }
  decide();
}, 1000);
})();
