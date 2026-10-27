const fs=require('fs');
const avg=a=>a.length? a.reduce((x,y)=>x+y,0)/a.length : NaN;
const pct=(a,p)=>{const s=[...a].sort((x,y)=>x-y);return s[Math.min(s.length-1,Math.floor(p*s.length))]};
const rows=[['Today (0.6.12)','log.json'],['Two Exploration teams at start','v_twoExp.json'],['Lock needs 3 of 4','v_lock3.json'],['Lock needs 2 of 4','v_lock2.json'],['Injury on ambush 50%','v_inj50.json'],['Injury on ambush 25%','v_inj25.json'],['Two teams + lock 3 + injury 50%','v_combo.json'],['Build 0.6.13 as shipped','v13.json']];
console.log('variant | n | reached L2 | L2 median | mean | p10 | p90 | first assault sent (median) | supplies at assault dial (median) | exploration income/min | RP at L2 (mean) | first-assault win%');
for(const [n,f] of rows){
  if(!fs.existsSync(f)){ console.log(n,'(missing)'); continue; }
  const R=JSON.parse(fs.readFileSync(f)); const d=R.filter(r=>r.done); const T=d.map(r=>r.done.t);
  const send=d.map(r=>{const e=r.ev.find(e=>e.k==='send'&&e.kind==='assault');return e&&e.t}).filter(x=>x!=null);
  const sup=d.map(r=>{const e=r.ev.find(e=>e.k==='dial'&&e.kind==='assault');return e&&e.supplies}).filter(x=>x!=null);
  const ei=avg(d.map(r=>r.inc.explore/r.done.t));
  const fw=R.map(r=>{const g=r.glog.find(g=>/^Assault on .* (succeeded|failed)/.test(g[1]));return g?(/succeeded/.test(g[1])?1:0):null}).filter(x=>x!=null);
  console.log([n,R.length,d.length,pct(T,.5).toFixed(1),avg(T).toFixed(1),pct(T,.1).toFixed(1),pct(T,.9).toFixed(1),pct(send,.5).toFixed(1),pct(sup,.5),ei.toFixed(1),avg(d.map(r=>r.research)).toFixed(0),(avg(fw)*100).toFixed(0)].join(' | '));
}
