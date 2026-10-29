(function(){
const cfg = Object.assign({logistics:true, reserve:30, maxExp:3, minOdds:0.55, oddsWaitMin:15, fob:true, tk:true, secExp:true, spend:true, truckBuy:true}, window.__CFG||{});
const B = window.BOT = { cfg, t0: Date.now(), job: null, ev: [], series: [], lvT: {}, done: null, lastMin: -1,
  inc: {explore:0, logistics:0, wormhole:0, wormholeHostile:0, fob:0, fobRP:0, tk:0, tkRP:0, spoils:0, spoilsRP:0, expRP:0},
  spent: {explore:0, recon:0, assault:0, raise:0, replace:0, lab:0, gateSup:0, gear:0, fob:0, tkBuy:0, tkFee:0, malp:0, veh:0, other:0},
  spentRP: {gate:0, arm:0, veh:0},
  wait: {power:0, supplies:0, cooldown:0, team:0, busy:0, odds:0},
  stats: {assaults:0, wins:0, fobOverrun:0, fobStockMax:0, raidsUnanswered:0}, glog: [], tsupSum:0, trpSum:0, tn:0, lvAvg:{} };
window.autosaveNow=function(){}; window.scheduleAutosave=function(){};
const tm = () => (Date.now()-B.t0)/60000;
const ev = (k, d) => B.ev.push(Object.assign({t:+tm().toFixed(2), k}, d||{}));
['renderHud','renderMap','updateMarkers','renderAlert','renderLog','renderMissions','renderStrip','renderAll','renderGate','renderHeader','renderStores','renderRoom','renderDC','renderChevrons','renderStarmapMap','renderStarmap','renderFacility'].forEach(n=>{ if (typeof window[n]==='function') window[n]=function(){}; });
const hookDelta = (name, key, rpKey) => { const f = window[name]; window[name] = function(){ const s=state.res.supplies, r=state.research; const o=f.apply(this, arguments); B.inc[key]+=state.res.supplies-s; if(rpKey) B.inc[rpKey]+=state.research-r; return o; }; };
const _fm = window.finishMission; window.finishMission = function(t){ const s=state.res.supplies, r=state.research; const fs=B.inc.fob, fr=B.inc.fobRP; _fm.apply(this, arguments); B.inc.explore += (state.res.supplies-s) - (B.inc.fob-fs); B.inc.expRP += (state.research-r) - (B.inc.fobRP-fr); };
const _ft = window.fobTruck; window.fobTruck = function(w, yl){ const s=state.res.supplies, r=state.research; const o=_ft.apply(this, arguments); B.inc.fob += state.res.supplies-s; B.inc.fobRP += state.research-r; return o; };
const _td = window.teltakDue; window.teltakDue = function(sid){ const s=state.res.supplies, r=state.research; const o=_td.apply(this, arguments); B.inc.tk += state.res.supplies-s; B.inc.tkRP += state.research-r; return o; };
const _lg = window.lgDue; window.lgDue = function(id){ const b=state.res.supplies; _lg.apply(this, arguments); const d=state.res.supplies-b; if(d>0){B.inc.logistics+=d;} };
const _ri = window.resolveIncoming; window.resolveIncoming = function(){ const inc=state.incoming; const b=state.res.supplies; _ri.apply(this, arguments); const d=state.res.supplies-b; if(inc && !inc.ret){ if(d>0) B.inc.wormhole+=d; else if(d<0) B.inc.wormholeHostile+=d; } };
const _rs = window.resolveAssault; window.resolveAssault = function(ids, wid, p){ const s=state.res.supplies, r=state.research; const lv0=state.level; const w=world(wid); const cs=w&&w.status; _rs.apply(this, arguments); B.stats.assaults++; const won = w && w.status==='captured' && cs!=='captured'; if(won){ B.stats.wins++; if(w.lord){ B.inc.spoils += state.res.supplies-s; B.inc.spoilsRP += state.research-r; } } ev('assault',{lvl:lv0, won:!!won, lord:!!(w&&w.lord), p:+p.toFixed(2)}); };
const _fo = window.fobOverrun; if(_fo) window.fobOverrun = function(w){ B.stats.fobOverrun++; ev('fobOverrun',{lvl:w.level}); return _fo.apply(this, arguments); };
const _fr = window.fobRaid; if(_fr) window.fobRaid = function(w){ B.stats.raidsUnanswered++; return _fr.apply(this, arguments); };
const _fp = window.finishProject; window.finishProject = function(p, note){ const ok=state.lab.projs.includes(p); const o=_fp.apply(this, arguments); if(ok && p.kind==='gate'){ (B.tierT=B.tierT||{})['g'+p.tier]=+tm().toFixed(1); } return o; };
const _bgt = window.buyGateTier; window.buyGateTier = function(){ const n=state.gt.ready; const o=_bgt.apply(this, arguments); if(n && state.gt.tier===n){ (B.tierT=B.tierT||{})['g'+n]=+tm().toFixed(1); } return o; };
const _lv = window.checkLevel; window.checkLevel = function(){ const l=state.level; _lv.apply(this, arguments); if(state.level!==l){ B.lvT[state.level]=+tm().toFixed(1); ev('level',{lvl:state.level}); } if(state.cleared && !B.lvT.cleared){ B.lvT.cleared=+tm().toFixed(1); } };
const _log=window.log; window.log=function(msg,cls){ B.glog.push([+tm().toFixed(2), msg]); return _log.apply(this, arguments); };

const FOBR = (cfg.roles && cfg.roles.length) ? cfg.roles : ['sup','rp','pw','sup','sup','rp','pw','sup','rp','sup'];
const naqRes = () => (typeof tkFuel==='function' && state.arm.ships.length) ? 3*state.arm.ships.length : 0;
const idleGate = () => state.gate==='closed' && !state.incoming && !state.busy && state.chevrons===0;
const L = () => state.worlds.filter(w=>w.level===state.level);
const teamsOf = type => state.teams.filter(t=>t.type===type);
const readyTeam = type => state.teams.find(t=>t.type===type && teamReady(t));
const reserve = () => cfg.reserve;
function goalRes(){ const h=L().filter(w=>w.stronghold && w.status!=='captured' && !w.treaty).sort((a,b)=>(!!a.lord-!!b.lord)); return h.length ? assaultCost(h[0])+45 : 0; }
function sp(cat, fn){ const s=state.res.supplies; fn(); const d=s-state.res.supplies; if(d>0) B.spent[cat]=(B.spent[cat]||0)+d; return d>0; }
function spRP(cat, fn){ const r=state.research; fn(); const d=r-state.research; if(d>0) B.spentRP[cat]=(B.spentRP[cat]||0)+d; return d>0; }

const RQ = ['gate1','gate2','ar1','truck','ar2','pk1','wx1','wa1','op1','gate3','pk2','ar3','wa2','op2','wx2','wr1','gate4','pk3','ar4','wa3','op3','gate5','gate6','gate7','pk4','wr2','staff','heal','tk1','tk2'];
const RQ2 = ['gate1','gate2','gate3','gate4','ar1','truck','ar2','pk1','wx1','wa1','op1','gate5','pk2','ar3','wa2','op2','wx2','wr1','gate6','gate7','pk3','ar4','wa3','op3','pk4','wr2','staff','heal','tk1','tk2'];
function nextResearch(){
  for(const k of (cfg.reactorFirst?RQ2:RQ)){
    if(k.startsWith('gate')){ const n=+k.slice(4); if(state.gt.tier>=n || state.gt.ready===n) continue; if(state.gt.tier+1!==n) return null; return k; }
    if(k==='truck'){ if(state.vehicles.some(v=>v.type==='truck')) continue; return k; }
    const it=armItem(k); if(!it||state.arm.done[k]) continue;
    if(it.alien && !state.arm.art[k]) continue;
    if(!it.alien && armNext(it.line)!==it) continue;
    return k;
  }
  return null;
}
function doSpend(){
  if(state.rx){ if(state.rx.node){ state.rx.routed=Math.max(state.rx.routed||0, state.rx.node.tier||0); state.rx.node=null; } if(state.rx.evt){ state.rx.evt=false; } state.rx.off=null; for(const n of RX_REACTOR_TIERS){ if(state.gt.tier>=n && state.rx.routed<n) state.rx.routed=n; } }
  const sup=()=>state.res.supplies;
  for(const t of state.teams){ for(const m of t.members){ if(m.status==='killed' && sup()>=replaceCost()+reserve()){ sp('replace',()=>replaceMember(t.id,m.id)); return true; } } }
  if(state.gt.ready && sup()>=GATE_TIERS[state.gt.ready-1].sup+reserve()){ return sp('gateSup', buyGateTier); }
  if(!state.lab.build && !state.lab.projs.length && labTier()<3 && sup()>=LAB_TIERS[labTier()].sup+reserve()+goalRes()){ return sp('lab', startLabUpgrade); }
  if(labOnline()){
    for(let g=0; g<3; g++){
      const nx=nextResearch(); if(!nx) break;
      if(!labCanStart()) break;
      const before=state.lab.projs.length, rp0=state.research;
      if(nx.startsWith('gate')) startGateResearch();
      else if(nx==='truck'){ if(state.research>=VEH_BUY){ spRP('veh',()=>buyVehicle('truck')); } break; }
      else startArmResearch(nx);
      if(state.lab.projs.length>before){ const d=rp0-state.research; if(nx.startsWith('gate')) B.spentRP.gate+=d; else B.spentRP.arm+=d; } else break;
    }
  }
  const tr=state.vehicles.find(v=>v.type==='truck');
  if(tr && tr.tier<3 && state.research>=VEH_UP[tr.tier+1]+400 && tr.status==='home'){ spRP('veh',()=>upgradeVehicle(tr.id)); }
  if(cfg.tk) for(const k of ['tk1','tk2']){ if(state.arm.done[k] && !state.arm.ships.some(x=>x.id===k) && sup()>=200+reserve()){ return sp('tkBuy',()=>buyArm(k)); } }
  if(state.arm.done.heal && !state.arm.dev && sup()>=150+reserve()+goalRes()){ return sp('gear',()=>buyArm('heal')); }
  for(const t of state.teams){
    if(t.status==='away') continue;
    for(const slot of ['p','a','o','w']){
      const cands=ARM_ITEMS.filter(i=>!i.alien||i.id==='staff').filter(i=>i.slot===slot && i.types.includes(t.type) && state.arm.done[i.id]).sort((a,b)=>b.rp-a.rp);
      if(!cands.length) continue;
      const best=cands[0];
      if(t.gear && t.gear[slot]===best.id) continue;
      if(armStock(best.id)>=1){ equipGear(t.id,slot,best.id); continue; }
      if(sup()>=best.sup+reserve()+goalRes()){ return sp('gear',()=>buyArm(best.id)); }
    }
  }
  const held=L().filter(w=>w.stronghold && w.status!=='captured');
  const imminent = held.length && L().filter(w=>!w.stronghold&&w.kind!=='ship').every(w=>w.status==='explored'||w.status==='captured');
  const hold = imminent ? assaultCost(held[0])+60 : 0;
  const lim=teamLimit('exp');
  if(teamsOf('exp').length<Math.min(lim,cfg.maxExp) && sup()>=raiseCost('exp')+reserve()+goalRes()){ return sp('raise',()=>raiseTeam('exp')); }
  if(cfg.fob){ for(const w of state.worlds){ if(w.stronghold && w.status==='captured' && !w.salvage && !fobOn(w) && sup()>=FOB_COST+reserve()){ return sp('fob',()=>fobEstablish(w.id, FOBR[Object.keys(state.fobs||{}).length % FOBR.length])); } } }
  if(!teamsOf('rec').length && L().some(w=>!w.stronghold && w.status==='explored') && sup()>=raiseCost('rec')+reserve()){ return sp('raise',()=>raiseTeam('rec')); }
  if(cfg.secExp && !teamsOf('sec').length && teamsOf('rec').length && sup()>=raiseCost('sec')+reserve()){ return sp('raise',()=>raiseTeam('sec')); }
  if(!teamsOf('asl').length && teamsOf('rec').length && L().some(w=>w.stronghold&&w.status!=='captured') && sup()>=raiseCost('asl')+reserve()){ return sp('raise',()=>raiseTeam('asl')); }
  if(cfg.scaleTeams){
    for(const tp of ['asl','sec','rec']){
      if(teamsOf(tp).length && teamsOf(tp).length<teamLimit(tp) && sup()>=raiseCost(tp)+reserve()+goalRes()){ return sp('raise',()=>raiseTeam(tp)); }
    }
  }
  if(cfg.atv){
    const atvs=state.vehicles.filter(v=>v.type==='atv');
    if(atvs.length<2 && state.research>=VEH_BUY+800 && state.vehicles.some(v=>v.type==='truck')){ return spRP('veh',()=>buyVehicle('atv')); }
    const lo=atvs.filter(v=>v.status==='home' && v.tier<VEH_MAX).sort((a,b)=>a.tier-b.tier)[0];
    if(lo && state.research>=VEH_UP[lo.tier+1]+800){ return spRP('veh',()=>upgradeVehicle(lo.id)); }
  }
  return false;
}
function doRescue(){
  const tg=sopTargets().find(x=>x.tkind==='cap');
  if(!tg) return false;
  const u=SOPS.filter(x=>x.lv<=state.level && !state.sops.reqs[x.id]).sort((a,b)=>a.fee-b.fee)[0];
  if(!u) return false;
  state.sops.pick=tg.key; sopRequest(u.id); B.stats.rescueReq=(B.stats.rescueReq||0)+1; ev('rescueReq'); return true;
}
function doTeltak(){
  for(const x of state.arm.ships){
    if(x.status!=='home' || state.res.supplies<TK_FEE) continue;
    if(typeof tkFuel==='function' && state.res.naquadah<3) { B.stats.tkNoFuel=(B.stats.tkNoFuel||0)+1; continue; }
    const ws=tkWorlds();
    if(!ws.length) continue;
    const away=new Set(state.arm.ships.filter(s=>s.status==='away').map(s=>s.world));
    const score=w=>{ if(fobOn(w)){ const f=state.fobs[w.id]; return (f.stock.sup+f.stock.rp)/tkRoundMs(w)*1000; } return tkYield(w)/tkRoundMs(w)*1000*0.5; };
    const cand=ws.filter(w=>!away.has(w.id)).sort((a,b)=>score(b)-score(a));
    if(!cand.length) continue;
    x.dest=cand[0].id; const n0=state.res.naquadah; sp('tkFee',()=>sendTeltak(x.id)); if(state.res.naquadah<n0){ B.stats.tkRuns=(B.stats.tkRuns||0)+1; B.stats.tkFuel=(B.stats.tkFuel||0)+(n0-state.res.naquadah); } return true;
  }
  return false;
}
function startJob(kind, w, types, mtype, veh, ids){
  B.job = {kind, wid:w.id, types, mtype, veh:veh||[], ids:ids||null, t:Date.now(), stage:'dial'};
  setDest(w.id);
  if(state.dest!==w.id){ B.job=null; return false; }
  autoDial();
  return true;
}
function stepJob(){
  const j=B.job; if(!j) return;
  if(Date.now()-j.t>180000 && j.stage==='dial'){ ev('dialTimeout'); B.job=null; try{ state.abortDial=true; }catch(e){} return; }
  if(state.gate==='open' && !state.incoming && state.dest===j.wid && gateReady()){
    state.sel=[]; state.selVeh=[]; state.withMalp=false;
    if(j.ids){ j.ids.forEach(id=>{ const t=state.teams.find(x=>x.id===id); if(t&&teamReady(t)) state.sel.push(id); }); j.types.filter(tp=>tp==='exp').forEach(tp=>{ const t=readyTeam(tp); if(t) state.sel.push(t.id); }); } else j.types.forEach(tp=>{ const t=readyTeam(tp); if(t) state.sel.push(t.id); });
    state.selVeh=j.veh.slice();
    setMType(j.mtype);
    const w=world(j.wid);
    if(j.kind==='assault' && w.lord && !w.recon){ w.recon={red:10,alert:false,id:'GOOD',tagged:1,total:1}; if(w.intel<4) w.intel=4; }
    const g=checkGroup();
    if(!g.ok){ ev('sendBlocked',{why:g.reasons.join('|'), kind:j.kind}); disengage(); B.job=null; B.blockedUntil=Date.now()+60000; return; }
    const s0=state.res.supplies;
    dispatch();
    const spent=s0-state.res.supplies;
    B.spent[j.kind==='explore'||j.kind==='truck'?'explore':(j.kind==='assault'?'assault':'recon')]+=spent;
    if(j.kind==='assault') ev('assaultSent',Object.assign({lvl:state.level, est:+(g.est||0).toFixed(2), cost:spent, world:w.name, lord:!!w.lord}, B.meta||{}));
    if(state.gate==='open' && !state.incoming) disengage();
    B.job=null;
  } else if(state.gate==='closed' && !state.busy && !state.incoming && state.chevrons===0 && Date.now()-j.t>5000){
    ev('dialFailed'); B.job=null;
  }
}
function pickExploreWorld(){
  const away=new Set(state.teams.filter(t=>t.status==='away'&&t.mission&&t.mission.worldId).map(t=>t.mission.worldId));
  const regAll=L().filter(w=>!w.stronghold);
  const normals=regAll.filter(w=>w.kind!=='ship' && w.kind!=='faction' && w.kind!=='lab');
  const un=regAll.filter(w=>w.status!=='explored' && w.status!=='captured' && !away.has(w.id));
  const pool=un.length?un:(normals.length?normals:regAll).filter(w=>!away.has(w.id));
  const use=pool.length?pool:regAll;
  const pw=state.res.power;
  const afford=use.filter(w=>gateCostFor(w)+AUTO_COST<=pw);
  return (afford.length?afford:use).slice().sort((a,b)=>gateCostFor(a)-gateCostFor(b))[0];
}
let oddsSince=null;
function decide(){
  const pc=w=>gateCostFor(w)+AUTO_COST;
  const sup=state.res.supplies, pw=state.res.power;
  const exp=readyTeam('exp'), rec=readyTeam('rec');
  const held=L().filter(w=>w.stronghold && w.status!=='captured' && !w.treaty);
  const nonLord=held.filter(w=>!w.lord);
  const order=nonLord.concat(held.filter(w=>w.lord));
  const target=order[0];
  if(target && !finalLocked(target) && target.intel<2 && rec){
    if(pw>=pc(target) && sup>=3){ startJob('recon', target, ['rec'], 'rec'); return; }
    B.wait.power++; return;
  }
  if(Date.now()<(B.blockedUntil||0)) return;
  const aslT=teamsOf('asl')[0];
  if(target && target.intel>=2 && !finalLocked(target) && cooldownLeft()===0){
    const fighters=['asl','sec'].map(readyTeam).filter(Boolean);
    const blocked=teamsOf('asl').some(t=>t.members.some(m=>m.status==='captured'));
    const ready=(tp)=>state.teams.filter(t=>t.type===tp && teamReady(t));
    if((ready('asl').length||ready('sec').length) && aslT){
      const want=2*state.level; let ne=0; const grpT=[];
      for(const tp of ['asl','sec','rec']){ for(const t of ready(tp)){ if(cfg.scaleTeams || !grpT.some(x=>x.type===tp)){ grpT.push(t); ne+=(tp==='sec'?SEC_WEIGHT:1); } if(ne>=want+0.5) break; } if(ne>=want+0.5) break; }
      const grp=grpT.map(t=>t.type);
      const ids=grpT.map(t=>t.id);
      if(!grpT.some(t=>t.type==='asl'||t.type==='sec')) { B.wait.team++; }
      else {
      const extraExp=((target.level===2||target.level===3) && exp && !(state.arm.art['tk'+(target.level-1)]));
      const atvs=state.vehicles.filter(v=>v.type==='atv' && v.status==='home').slice(0,VEH_PER_SEND);
      const need=assaultCost(target)+grpT.reduce((a,t)=>a+TYPES[t.type].cost,0)+(extraExp?TYPES.exp.cost:0);
      const fx=vehFx(atvs.map(v=>v.id));
      const est=Math.min(1,assaultChance(grpT, target)+(target.lord?0.10:0)+fx.assault);
      const camS=grpT.reduce((a,t)=>a+Math.max(0,Math.min(CAM_CAP,t.cam)),0)/grpT.length/CAM_CAP*100; const neq=grpT.reduce((a,t)=>a+(t.type==='sec'?SEC_WEIGHT:1),0);
      B.meta={diff:+effDiff(target).toFixed(1), atv:+fx.assault.toFixed(2), gear:+gearAssault(grpT).toFixed(2), cam:+camS.toFixed(0), size:+Math.min(100,neq/(2*state.level)*100).toFixed(0), n:grpT.length};
      if(sup<need){ B.wait.supplies++; }
      else if(pw<pc(target)){ B.wait.power++; return; }
      else if(est<cfg.minOdds){ if(oddsSince==null) oddsSince=tm(); if(tm()-oddsSince<cfg.oddsWaitMin){ B.wait.odds++; } else { oddsSince=null; startJob('assault', target, grp.concat(extraExp?['exp']:[]), 'asl', atvs.map(v=>v.id), ids); return; } }
      else { oddsSince=null; startJob('assault', target, grp.concat(extraExp?['exp']:[]), 'asl', atvs.map(v=>v.id), ids); return; }
      }
    }
  }
  const tr=state.vehicles.find(v=>v.type==='truck' && v.status==='home');
  if(tr && exp){
    const fw=state.worlds.filter(w=>fobOn(w)).sort((a,b)=>state.fobs[b.id].stock.sup-state.fobs[a.id].stock.sup)[0];
    if(fw){
      const f=state.fobs[fw.id];
      const tkOwn=state.arm.ships.length;
      if((f.stock.sup>=300 || f.stock.rp>=150 || f.stock.sup>=FOB_CAP_SUP) && !(tkOwn && f.stock.sup<900) && pw>=pc(fw) && sup>=TYPES.exp.cost){ startJob('truck', fw, ['exp'], 'exp', [tr.id]); return; }
    }
  }
  if(!exp){ B.wait.team++; return; }
  const w=pickExploreWorld(); if(!w) return;
  if(sup<TYPES.exp.cost){ B.wait.supplies++; return; }
  if(pw<pc(w)){ B.wait.power++; return; }
  const types=['exp']; if(cfg.secExp && readyTeam('sec') && sup>=TYPES.exp.cost+TYPES.sec.cost+reserve()) types.push('sec');
  startJob('explore', w, types, 'exp');
}
setInterval(function(){
  if(B.done) return;
  const m=Math.floor(tm());
  if(m!==B.lastMin){ B.lastMin=m;
    const stk=Object.values(state.fobs||{}).reduce((a,f)=>a+f.stock.sup,0); if(stk>B.stats.fobStockMax) B.stats.fobStockMax=stk;
    B.series.push([m, state.res.supplies, Math.round(state.res.power), state.res.naquadah, state.research, state.level, Object.keys(state.fobs||{}).length, stk]);
    B.tsupSum+=state.res.supplies; B.trpSum+=state.research; B.tn++;
    const lv=state.level; const a=B.lvAvg[lv]||(B.lvAvg[lv]={n:0,sup:0,rp:0,pw:0}); a.n++; a.sup+=state.res.supplies; a.rp+=state.research; a.pw+=state.res.power;
  }
  if(state.cleared || tm()>(cfg.maxMin||600)){ B.done={t:tm(), lvl:state.level, cleared:!!state.cleared}; return; }
  if(state.res.naquadah>naqRes() && state.res.power<=POWER_CAP-15){ convertNaq(); B.stats.naqConv=(B.stats.naqConv||0)+1; }
  if(cfg.logistics){ LG_UNITS.forEach(u=>{ if(u.lv<=state.level && !state.lg.units[u.id] && lgCdLeft()<=0 && Object.keys(state.lg.units).length<LG_MAX){ lgRequest(u.id); } }); }
  const inc=state.incoming;
  if(inc){
    if(!inc.ret && !inc.friendly && !state.irisClosed){ toggleIris(); }
    else if(!inc.ret && !state.irisClosed && !inc.idc){ toggleIris(); }
    if(inc.idc && inc.friendly && state.irisClosed){ toggleIris(); }
    return;
  }
  if(cfg.spend){ let n=0; while(n++<6 && doSpend()){} }
  if(cfg.tk) doTeltak();
  doRescue();
  if(B.job){ stepJob(); return; }
  if(!idleGate()){ B.wait.busy++; return; }
  if(dueTeams().length) return;
  decide();
}, 1000);
})();
