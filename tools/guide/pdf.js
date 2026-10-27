const { chromium } = require('playwright');
(async()=>{
const b = await chromium.launch({});
const p = await b.newPage();
await p.goto('file:///tmp/guide/guide.html');
await p.pdf({path:'/tmp/guide/guide.pdf',format:'Letter',printBackground:true,preferCSSPageSize:true});
await b.close();
})();
