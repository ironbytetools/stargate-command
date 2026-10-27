const fs=require('fs');
const avg=a=>a.length? a.reduce((x,y)=>x+y,0)/a.length : NaN;
const med=a=>{const s=[...a].sort((x,y)=>x-y);return s[Math.floor(s.length/2)]};
function tl(name,f){
  const R=JSON.parse(fs.readFileSync(f));
  const rows=[];
  R.forEach((r,i)=>{
    if(!r.done) return;
    const worlds=new Set(); let t4=null, survey=null, aslRaised=null, cash=null;
    r.glog.forEach(g=>{
      const m=/returned from (\S+) with .*\+\d+ research/.exec(g[1]);
      if(m && !worlds.has(m[1])){ worlds.add(m[1]); if(worlds.size===4 && t4==null) t4=g[0]; }
      if(/Stronghold confirmed|stronghold/i.test(g[1]) && /Recon Team 1 returned/.test(g[1]) && survey==null) survey=g[0];
      if(/Assault Team 1 raised/.test(g[1]) && aslRaised==null) aslRaised=g[0];
    });
    const s=r.series.find(s=>s[1]>=161); cash=s?s[0]:null;
    const send=r.ev.find(e=>e.k==='send'&&e.kind==='assault');
    rows.push({i, t4, survey, aslRaised, cash, send: send&&send.t, l2:r.done.t});
  });
  const c=k=>rows.map(x=>x[k]).filter(v=>v!=null);
  console.log('\n'+name+' (medians, min): all 4 worlds explored',med(c('t4')),' recon found stronghold',med(c('survey')),' cash>=161',med(c('cash')),' assault team raised',med(c('aslRaised')),' first assault sent',med(c('send')),' L2',med(c('l2')));
  const gap=rows.filter(x=>x.cash!=null&&x.send!=null).map(x=>x.send-x.cash);
  console.log('minutes between cash-ready and first assault sent: median',med(gap).toFixed(1),' mean',avg(gap).toFixed(1));
  const gap2=rows.filter(x=>x.t4!=null&&x.send!=null).map(x=>x.send-x.t4);
  console.log('minutes between 4th world explored and assault sent: median',med(gap2).toFixed(1),' mean',avg(gap2).toFixed(1));
  // number of exploration trips per distinct world needed, failed trips
  const trips=R.filter(r=>r.done).map(r=>r.ev.filter(e=>e.k==='send'&&e.kind==='explore').length);
  const succ=R.filter(r=>r.done).map(r=>r.glog.filter(g=>/returned from .* with .*supplies/.test(g[1])&&/\+\d+ research/.test(g[1])).length);
  const amb=R.filter(r=>r.done).map(r=>r.glog.filter(g=>/ambushed/.test(g[1])).length);
  console.log('exploration trips sent mean',avg(trips).toFixed(1),' of which clean/RP',avg(succ).toFixed(1),' ambush events',avg(amb).toFixed(1));
  const stuck=R.filter(r=>!r.done);
  console.log('not finished in 150 min:',stuck.length);
  stuck.slice(0,3).forEach(r=>{ console.log('  stuck sample: sup',r.sup,'last:',r.glog.filter(g=>/Assault|captured|killed|raised|replacement/.test(g[1])).slice(-3).map(g=>g[0]+' '+g[1].slice(0,130)).join(' || ')); });
}
tl('NO logistics','nolog.json'); tl('WITH logistics','log.json');
