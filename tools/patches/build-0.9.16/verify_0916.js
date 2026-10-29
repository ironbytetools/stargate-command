const fs=require('fs'),crypto=require('crypto'),cp=require('child_process');
const [,, src, built] = process.argv;
cp.execSync(`python3 ${__dirname}/patch_0916.py ${src} /tmp/_r16.html`);
const h=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
console.log(h('/tmp/_r16.html')===h(built)?'IDENTICAL':'DIFFERENT', h(built));
