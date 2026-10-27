const fs=require('fs');
const avg=a=>a.length? a.reduce((x,y)=>x+y,0)/a.length : NaN;
const med=a=>{const s=[...a].sort((x,y)=>x-y);return s[Math.floor(s.length/2)]};
for(const [n,f] of [['NO logistics','nolog.json'],['WITH logistics','log.json']]){
  const R=JSON.parse(fs.readFileSync(f));
  const first=R.map(r=>{const g=r.glog.find(g=>/^Assault on .* (succeeded|failed)/.test(g[1])); return g? (/succeeded/.test(g[1])?1:0):null; }).filter(x=>x!=null);
  const estim=R.flatMap(r=>r.glog.filter(g=>/^Assault on/.test(g[1])).slice(0,1).map(g=>+/\((\d+)% estimate/.exec(g[1])[1]));
  console.log(n,'first-assault win rate',(avg(first)*100).toFixed(0)+'% of',first.length,' (game estimate mean',avg(estim).toFixed(0)+'%)');
  const done=R.filter(r=>r.done);
  const att=r=>r.ev.filter(e=>e.k==='send'&&e.kind==='assault').length;
  const one=done.filter(r=>att(r)===1).map(r=>r.done.t), more=done.filter(r=>att(r)>=2).map(r=>r.done.t);
  console.log('  L2 time: one assault mean',avg(one).toFixed(1),'(n='+one.length+')  two+ assaults mean',avg(more).toFixed(1),'(n='+more.length+')  penalty',(avg(more)-avg(one)).toFixed(1),'min');
  const t4=done.map(r=>{const w=new Set();let t=null;r.glog.forEach(g=>{const m=/returned from (\S+) with .*\+\d+ research/.exec(g[1]);if(m&&!w.has(m[1])){w.add(m[1]);if(w.size===4&&t==null)t=g[0];}});return t}).filter(x=>x!=null).sort((a,b)=>a-b);
  console.log('  4th distinct world explored: mean',avg(t4).toFixed(1),'p10',t4[Math.floor(t4.length*.1)].toFixed(1),'median',med(t4).toFixed(1),'p90',t4[Math.floor(t4.length*.9)].toFixed(1));
  const sec=done.filter(r=>r.glog.some(g=>/Security Team 1 raised/.test(g[1]))).length;
  console.log('  runs that had to raise a Security team after a failed assault:',sec+'/'+done.length);
  const lostMin=done.map(r=>{const w=r.glog.filter(g=>/Exploration Team 1 were ambushed|returned from .* Exploration failed|injured\. Team stands down/.test(g[1])).length;return w});
  const inj=R.map(r=>r.glog.filter(g=>/Exploration failed: no research earned/.test(g[1])).length);
  console.log('  exploration trips that failed (injury, no RP) per run mean',avg(inj).toFixed(1));
}
