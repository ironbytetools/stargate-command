const fs=require('fs');
const q=(a,p)=>{ if(!a.length) return NaN; const s=[...a].sort((x,y)=>x-y); return s[Math.min(s.length-1,Math.floor(p*(s.length)))]; };
const avg=a=>a.length? a.reduce((x,y)=>x+y,0)/a.length : NaN;
function rep(name,f){
  const R=JSON.parse(fs.readFileSync(f));
  const done=R.filter(r=>r.done);
  const T=done.map(r=>r.done.t);
  console.log('\n=== '+name+' n='+R.length+' reached L2: '+done.length);
  console.log('time to L2 min  mean',avg(T).toFixed(1),'p10',q(T,.1).toFixed(1),'median',q(T,.5).toFixed(1),'p90',q(T,.9).toFixed(1),'max',Math.max(...T).toFixed(1));
  const att=r=>r.ev.filter(e=>e.k==='send'&&e.kind==='assault');
  console.log('assault attempts mean',avg(done.map(r=>att(r).length)).toFixed(2),' first-win rate',(done.filter(r=>att(r).length===1).length/done.length).toFixed(2));
  const firstAtt=done.map(r=>att(r)[0]&&att(r)[0].t).filter(x=>x!=null);
  console.log('first assault sent at min: mean',avg(firstAtt).toFixed(1),'median',q(firstAtt,.5).toFixed(1));
  // supplies at first assault dial
  const sa=done.map(r=>{const d=r.ev.find(e=>e.k==='dial'&&e.kind==='assault');return d&&d.supplies}).filter(x=>x!=null);
  console.log('supplies on hand at first assault dial: mean',avg(sa).toFixed(0),'median',q(sa,.5),'  (need ~',150+8+3,')');
  const ex=done.map(r=>r.inc.explore), lg=done.map(r=>r.inc.logistics), wh=done.map(r=>r.inc.wormhole);
  console.log('income by L2 (mean): explore',avg(ex).toFixed(0),' logistics',avg(lg).toFixed(0),' friendly wormhole',avg(wh).toFixed(0));
  const rate=(a)=>avg(done.map((r,i)=>a[i]/r.done.t));
  console.log('income per min: explore',rate(ex).toFixed(2),' logistics',rate(lg).toFixed(2),' wormhole',rate(wh).toFixed(2));
  console.log('spent (mean): explore sends',avg(done.map(r=>r.spent.explore)).toFixed(0),' recon',avg(done.map(r=>r.spent.recon)).toFixed(0),' raise',avg(done.map(r=>r.spent.raise)).toFixed(0),' assault(fee+sends)',avg(done.map(r=>r.spent.assault)).toFixed(0),' replace',avg(done.map(r=>r.spent.replace||0)).toFixed(0));
  console.log('dials mean',avg(done.map(r=>r.dials)).toFixed(1));
  const w=k=>avg(done.map(r=>(r.wait[k]||0)/60));
  console.log('idle-decision minutes (gate free, nothing sent): waiting on power',w('power').toFixed(1),' supplies',w('supplies').toFixed(1),' assault cooldown',w('cooldown').toFixed(1),' no ready team',w('team').toFixed(1),' fighters injured/captured',w('fighters').toFixed(1));
  // power at cap fraction and supply surplus
  let capMin=0,totMin=0,surplus=[];
  done.forEach(r=>r.series.forEach(s=>{ totMin++; if(s[2]>=120) capMin++; }));
  console.log('minutes with power pinned at 120 cap:',(100*capMin/totMin).toFixed(0)+'%');
  console.log('research points at L2 mean',avg(done.map(r=>r.research)).toFixed(0));
  // supplies curve: mean at minute 5,10,15,20,30
  const at=m=>avg(done.filter(r=>r.series[m]).map(r=>r.series[m][1]));
  console.log('mean supplies @5/10/15/20/30/40 min:',[5,10,15,20,30,40].map(m=>at(m).toFixed(0)).join(' / '));
  // time of first moment supplies >= 161 (assault ready cash) 
  const cashT=done.map(r=>{const s=r.series.find(s=>s[1]>=161);return s?s[0]:null}).filter(x=>x!=null);
  console.log('first minute with >=161 supplies: median',q(cashT,.5),' mean',avg(cashT).toFixed(1));
  // when all 4 regular worlds explored?  use glog count of +100/+150 research returns
  const expl=done.map(r=>{ // time of last first-time explore: approximate using research: count 'returned from' w/ research
    const x=r.glog.filter(g=>/returned from .* with .*supplies/.test(g[1])&&/\+\d+ research/.test(g[1])); return x.length; });
  console.log('successful exploration returns by L2 (mean)',avg(expl).toFixed(1));
  const dead=done.map(r=>r.glog.filter(g=>/killed|captured/.test(g[1])&&/Assault on/.test(g[1])).length);
  console.log('runs with assault deaths/captures:',dead.filter(x=>x>0).length+'/'+done.length);
  return R;
}
rep('NO logistics','nolog.json'); rep('WITH logistics','log.json');
