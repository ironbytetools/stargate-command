const { chromium } = require('playwright');
const fs = require('fs');
const [,, outFile, nRuns, maxMin, cfgJson, gamePath, seed0] = process.argv;
(async () => {
  const browser = await chromium.launch({ args:['--no-sandbox','--autoplay-policy=no-user-gesture-required'] });
  const results = [];
  for (let i=0;i<+nRuns;i++){
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    const errs=[]; page.on('pageerror', e=>errs.push(String(e)));
    await page.addInitScript({path:'vt.js'});
    await page.goto('file://' + require('path').resolve(gamePath || 'game.html'));
    await page.evaluate(()=>{ try{localStorage.clear();}catch(e){} });
    await page.evaluate(()=>{ startNew(); try{ if(typeof tourEnd==='function') tourEnd(); }catch(e){} while(PAUSE.on()) PAUSE.resume(); });
    await page.evaluate((c)=>{ window.__CFG=c; }, Object.assign({maxMin:+maxMin}, JSON.parse(cfgJson||'{}')));
    await page.addScriptTag({ path: 'bot2.js' });
    const t0=Date.now();
    for (let m=0;m<+maxMin;m++){
      await page.evaluate(()=>__vt.advance(60000));
      if(await page.evaluate(()=>!!BOT.done)) break;
    }
    const r = await page.evaluate(()=>({cfg:BOT.cfg, done:BOT.done, ev:BOT.ev, series:BOT.series, wait:BOT.wait, inc:BOT.inc, spent:BOT.spent, spentRP:BOT.spentRP, stats:BOT.stats, naq:state.res.naquadah, fobRoles:Object.values(state.fobs||{}).map(f=>f.role), lvT:BOT.lvT, tierT:BOT.tierT, lvAvg:BOT.lvAvg, level:state.level, sup:state.res.supplies, power:state.res.power, research:state.research, glog:BOT.glog.slice(-400), fobs:Object.keys(state.fobs||{}).length, gt:state.gt.tier, labTier:state.lab.tier||0, ships:state.arm.ships.length, teams:state.teams.map(t=>t.type), diag:{teams:state.teams.map(t=>[t.type,t.status,t.members.map(m=>m.status).join('/')]), holds:state.worlds.filter(w=>w.level===state.level&&w.stronghold).map(w=>[w.name,w.status,w.intel,!!w.lord,!!w.recon,!!w.treaty,typeof finalLocked==='function'&&finalLocked(w), cooldownLeft()]), assaultCd:cooldownLeft(), blockedUntil:BOT.blockedUntil, now:Date.now()}}));
    r.errs = errs.concat(await page.evaluate(()=>window.__errs||[])).slice(0,10);
    results.push(r); fs.writeFileSync(outFile, JSON.stringify(results));
    await ctx.close();
    console.error('run', i, r.done ? (r.done.t.toFixed(1)+' lvl '+r.done.lvl+(r.done.cleared?' CLEARED':'')) : 'NOT DONE', 'errs', r.errs.length, 'wall', ((Date.now()-t0)/1000).toFixed(0)+'s', JSON.stringify(r.lvT));
    if(r.errs.length) console.error(r.errs.slice(0,3).join('\n'));
  }
  await browser.close();
})();
