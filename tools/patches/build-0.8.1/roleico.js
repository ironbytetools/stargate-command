function roleIco(k,cx,cy,sc,col){
const st=`stroke="${col}" stroke-width=".16" fill="none" stroke-linecap="round" stroke-linejoin="round"`;
const fl=(r)=>`<g transform="rotate(${r})"><path d="M-.16-.85H.16V-.3L.5.55Q.62.85.38.85H-.38Q-.62.85-.5.55L-.16-.3Z" ${st}/><path d="M-.34.38H.34" ${st}/></g>`;
const blade=(r)=>`<g transform="rotate(${r})"><path d="M0-.95L.09-.6V.45H-.09V-.6Z" fill="${col}"/><path d="M-.3.45H.3" ${st} stroke-width=".18"/><path d="M0 .45V.85" ${st} stroke-width=".18"/></g>`;
const I={
cmd:`<path d="M-.5-.95V.95" ${st} stroke-width=".18"/><path d="M-.5-.85L.8-.45L-.5-.05Z" fill="${col}"/>`,
inf:`<path d="M-.85-.6L.85.6M-.85.6L.85-.6" ${st} stroke-width=".2"/>`,
sci:fl(-38)+fl(38),
globe:`<circle r=".8" ${st}/><ellipse rx=".36" ry=".8" ${st}/><path d="M-.8 0H.8M-.66-.42H.66M-.66.42H.66" ${st} stroke-width=".1"/>`,
recon:`<path d="M-.85.6L.85-.6" ${st} stroke-width=".26"/>`,
scope:`<circle r=".7" ${st}/><path d="M0-1V-.3M0 .3V1M-1 0H-.3M.3 0H1" ${st}/><circle r=".08" fill="${col}"/>`,
mg:[-.5,0,.5].map(x=>`<path d="M${x-.17} .6V-.3Q${x-.17}-.8 ${x}-.9Q${x+.17}-.8 ${x+.17}-.3V.6Z" fill="${col}"/>`).join("")+`<path d="M-.8.78H.8" ${st} stroke-width=".14"/>`,
gren:`<ellipse cy=".25" rx=".5" ry=".6" fill="${col}"/><rect x="-.2" y="-.5" width=".4" height=".24" fill="${col}"/><path d="M.12-.46L.62-.7L.72-.5" ${st}/><path d="M-.4.05H.4M-.45.35H.45" stroke="#07101c" stroke-width=".1"/>`,
sec:`<path d="M0-.95L.78-.62V.12C.78.6.36.85 0 .98C-.36.85-.78.6-.78.12V-.62Z" ${st}/><path d="M-.34-.1L0-.45L.34-.1M-.34.25L0-.1L.34.25" ${st} stroke-width=".13"/>`,
sig:`<path d="M.28-.95L-.58.1H-.06L-.28.95L.62-.2H.1Z" fill="${col}"/>`,
med:`<path d="M-.28-.85H.28V-.28H.85V.28H.28V.85H-.28V.28H-.85V-.28H-.28Z" fill="${col}"/>`,
compass:`<circle r=".82" ${st} stroke-width=".12"/><path d="M0-.95L.18-.18L.95 0L.18.18L0 .95L-.18.18L-.95 0L-.18-.18Z" fill="${col}"/>`,
olive:`<path d="M-.8.75Q-.1-.1.8-.75" ${st} stroke-width=".14"/>`+[[-.5,.4,-50],[-.25,.14,-55],[0,-.1,-50],[.28,-.34,-55],[.52,-.52,-50]].map(([x,y,r])=>`<path d="M0 0C.14-.16.34-.16.46 0C.34.16.14.16 0 0Z" fill="${col}" transform="translate(${x} ${y}) rotate(${r})"/><path d="M0 0C.14-.16.34-.16.46 0C.34.16.14.16 0 0Z" fill="${col}" transform="translate(${x} ${y}) rotate(${r+100})"/>`).join(""),
sun:`<circle r=".36" fill="${col}"/>`+[0,45,90,135,180,225,270,315].map(a=>`<path d="M0-.55V-.9" ${st} stroke-width=".14" transform="rotate(${a})"/>`).join(""),
swords:blade(-40)+blade(40),
scroll:`<rect x="-.55" y="-.62" width="1.1" height="1.24" rx=".08" ${st}/><path d="M-.3-.3H.3M-.3 0H.3M-.3.3H.1" ${st} stroke-width=".1"/><circle cx="-.55" cy="-.62" r=".16" fill="${col}"/><circle cx="-.55" cy=".62" r=".16" fill="${col}"/>`
};
return `<g transform="translate(${cx} ${cy}) scale(${sc})">${I[k]||""}</g>`}
