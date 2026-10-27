const { chromium } = require('playwright');
const fs = require('fs');
const [,, outFile, nRuns, logi, maxMin, reserve] = process.argv;
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox','--autoplay-policy=no-user-gesture-required'] });
  const results = [];
  for (let i=0;i<+nRuns;i++){
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    const errs=[]; page.on('pageerror', e=>errs.push(String(e)));
    await page.addInitScript({path:'vt.js'});
    await page.goto('file://' + require('path').resolve(process.argv[7] || 'game.html') + '');
    await page.evaluate(()=>{ try{localStorage.clear();}catch(e){} });
    await page.evaluate(()=>{ startNew(); });
    await page.evaluate((c)=>{ window.__CFG=c; }, Object.assign({logistics: logi==='1', reserve: +reserve||0}, JSON.parse(process.argv[8]||'{}')));
    await page.addScriptTag({ path: 'bot.js' });
    const total = +maxMin;
    for (let m=0;m<total;m++){
      await page.evaluate(()=>__vt.advance(60000));
      const done = await page.evaluate(()=>!!BOT.done);
      if(done) break;
    }
    const r = await page.evaluate(()=>({done:BOT.done, ev:BOT.ev, series:BOT.series, wait:BOT.wait, inc:BOT.inc, spent:BOT.spent, dials:BOT.dials, level:state.level, sup:state.res.supplies, power:state.res.power, research:state.research, glog:BOT.glog}));
    r.errs = errs.concat(await page.evaluate(()=>window.__errs||[]));
    results.push(r);
    await ctx.close();
    console.error('run', i, r.done ? r.done.t.toFixed(1) : 'NOT DONE', 'errs', errs.length);
  }
  fs.writeFileSync(outFile, JSON.stringify(results));
  await browser.close();
})();
