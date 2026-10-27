import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.4') == 4, s.count('0.9.4')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('<title>Stargate Command 0.9.4</title>', '<title>Stargate Command 0.9.5</title>')
rep('BUILD 0.9.4', 'BUILD 0.9.5', 2)
rep("const BUILD_VER = '0.9.4';", "const BUILD_VER = '0.9.5';")
rep("""  const h = gate ? st.offsetHeight : FIT.H.base;
  const s = Math.max(FIT.min, Math.min(FIT.max, window.innerWidth / FIT.W, window.innerHeight / h));
  const wc = window.innerWidth / s;
  if (gate && m) FIT.lock = m.offsetWidth;
  if (gate && dw) dw.style.maxWidth = dw.offsetWidth + 'px';
  st.style.width = wc + 'px';
  FIT.s = s;
  if (gate) fitStarmap();
  st.style.transform = 'scale(' + s + ')';
""", """  const h = gate ? st.offsetHeight : FIT.H.base;
  const clampS = hh => Math.max(FIT.min, Math.min(FIT.max, window.innerWidth / FIT.W, window.innerHeight / hh));
  let s = clampS(h);
  let wc = window.innerWidth / s;
  st.style.width = wc + 'px';
  FIT.s = s;
  if (gate) {
    for (let i = 0; i < 40; i++) {
      st.style.transform = 'scale(' + s + ')';
      fitStarmap();
      const s2 = clampS(st.offsetHeight);
      if (s2 >= s - 0.0008) break;
      s = s2;
      wc = window.innerWidth / s;
      st.style.width = wc + 'px';
      FIT.s = s;
    }
  }
  st.style.transform = 'scale(' + s + ')';
""")
rep("#dcwrap { max-width: calc((var(--vh, 100vh) - 250px) * 800 / 560); margin: 0 auto; }", "#dcwrap { margin: 0 auto; }\n#ctrlpanel.kb { max-width: none; }")

BDC = open(__file__.replace('patch_095h.py','dc_build.js'), encoding='utf-8').read()
a = s.index("function buildDC() {")
b = s.index("  $('dcwrap').innerHTML = s;", a)
s = s[:a] + BDC + s[b:]
rep("const DC_CX = 400;", "const DC_CX = 455;")
rep("      x = DC_CX + (752 - DC_CX) * e;", "      x = DC_CX + (744 - DC_CX) * e;")
rep("  const bx = 644;\n  const lanes = [598, 606, 614, 622, 628, 634, 640];", "  const bx = 690;\n  const lanes = [652, 658, 664, 670, 674, 678, 682];")
rep("const sx = k === 4 ? 213 :", "const sx = k === 4 ? 268 :")
rep("cx=\"${292 + c * 8}\"", "cx=\"${330 + c * 8}\"")
rep("    const x = 20 + (i % 2) * 92;\n    const y = 214 + Math.floor(i / 2) * 38;\n    $('dcs_' + c).setAttribute('points', sparkPoints(h, x + 44, y + 4, 38, 10));", "    const x = 20 + (i % 2) * 129;\n    const y = 252 + Math.floor(i / 2) * 50;\n    $('dcs_' + c).setAttribute('points', sparkPoints(h, x + 66, y + 24, 48, 14));")
rep("min: 0.6, max: 1.6", "min: 0.5, max: 1.6")
EXTRA = "\n.dct { font-size: 14px; }\n.dct.tiny, .tiny { font-size: 12.5px; }\n.dct.stat { font-size: 15px; }\n.dcval { font-size: 18px; }\n.dcmid { font-size: 23px; }\n#ctrlpanel .krow > button.k, #ctrlpanel .krow > #irispanel { flex: 1 1 0; min-width: 0; }\n#ctrlpanel .krow > #irispanel button.k { width: 100%; }\n#ctrlpanel .kb button.k.lock, .kb button.k.lock { max-width: none; }\nbody.gv #smpanel { position: absolute; left: 8px; right: 8px; bottom: 8px; flex: none; height: auto; max-height: 48%; margin: 0; z-index: 4; box-sizing: border-box; background: rgba(3, 10, 18, 0.94); }\nbody.gv #smpanel:empty { display: none; }"
i = s.rindex("</style>")
s = s[:i] + EXTRA.replace("\\n", "\n") + "\n" + s[i:]
rep("</div><div id=\"smpanel\"></div></div>", "<div id=\"smpanel\"></div></div></div>")
rep("  const h = (sm.getBoundingClientRect().bottom - m.getBoundingClientRect().top) / FIT.s - pad - $('smpanel').offsetHeight - 8;", "  const h = (sm.getBoundingClientRect().bottom - m.getBoundingClientRect().top) / FIT.s - pad;")
rep("    $('dcrt' + k).textContent = eng ? 'OK' : '--';\n  }\n", "    $('dcrt' + k).textContent = eng ? 'OK' : '--';\n  }\n  const litG = new Set();\n  for (let k = 0; k < ADDR_LEN; k++) if (DC.filled[k] && src && src[k] !== undefined) litG.add(src[k]);\n  for (let i = 0; i < N; i++) $('dccg' + i).classList.toggle('on', litG.has(i));\n")
rep("Math.max(9, Math.min(15, 15 * 30 / Math.max(1, code.text.length)))", "Math.max(8, Math.min(15, 15 * 20 / Math.max(1, code.text.length)))")
rep("    $('dcbs' + k).textContent = eng ? 'ENCODED' : '--';", "    $('dcbs' + k).textContent = '';")
rep("if (st !== DC.statusCache) { $('dcStatus').textContent = st; DC.statusCache = st; }", "if (st !== DC.statusCache) { $('dcStatus').textContent = st; $('dcStatus').style.fontSize = Math.min(22, 330 / (st.length * 0.72)).toFixed(1) + 'px'; DC.statusCache = st; }")
EXTRA2 = ".dcnum { fill: #ffd23a; font-size: 20px; font-family: inherit; font-weight: bold; }\n.dcstat2 { fill: #ffd23a; font-size: 22px; letter-spacing: 0.1em; font-family: inherit; }\n.dcstbox { fill: #020a0d; stroke: #1a6a88; stroke-width: 1.2; }\n.dcbox { fill: #0a0405; stroke: #7a1818; }\n.dcbox.on { fill: #6b0f0f; stroke: #ff5a3a; }\n.dcgl { color: #b8912a; }\n.dcgl.top { color: #ffe27a; filter: drop-shadow(0 0 4px #ffd23a); }\n.dchero { color: #ffd23a; filter: drop-shadow(0 0 6px #ffb800); }\n.dcbgl { color: #ffd23a; }\n.dccg rect { fill: #03090c; stroke: #5a4a14; }\n.dcsg { color: #b8912a; fill: currentColor; stroke: currentColor; stroke-width: 1.2; stroke-linecap: round; stroke-linejoin: round; }\n.dccg.on rect { fill: #6b0f0f; stroke: #ff5a3a; }\n.dccg.on .dcsg { color: #ffe27a; }\n.dccell { fill: #03090c; }\n.dcmono, .dcmid2 { fill: #ffd23a; }\n.dcmid { fill: #ffd23a; }\n.dcmid2.red, .dcmono.red { fill: #ff4a3a; }\n"
i = s.rindex("</style>")
s = s[:i] + EXTRA2 + s[i:]

a = s.index("  state.malps.forEach(m => {\n    if (m.status === 'away') out.push(['MALP '")
b = s.index("  return out;\n}\n\nfunction dcMissions")
s = s[:a] + s[b:]
rep("  state.teams.filter(t => t.status === 'away').forEach(t => chips.push(['brief', `<b>${t.name}</b> ${teamStatus(t)}`]));\n", "")
rep("<span class=\"chip idle dim\">NO ACTIVE MISSIONS</span>", "<span class=\"chip idle dim\">NO OTHER ACTIVITY</span>")
rep("onclick=\"setMType('${k}')\"><b>${MTYPES[k][0]}</b><span>${MT_SHORT[k]}</span></div>`).join('')}</div>`;", "onclick=\"setMType('${k}',1)\"><b>${MTYPES[k][0]}</b><span>${MT_SHORT[k]}</span></div>`).join('')}</div><p class=\"dim small\">Click a mission type to continue.</p>`;")
rep("function setMType(k) {\n  if (!MTYPES[k]) return;\n  state.mType = k;", "function setMType(k, adv) {\n  if (!MTYPES[k]) return;\n  state.mType = k;\n  if (adv) state.mStep = 1;")
rep("""          </div>
          </div>
          <p class="small dim help">Hold arrows""", """          </div>
          <div class="kcom ksend">
            <button class="k go" id="b-malp" onclick="sendMalp()" disabled>SEND MALP</button>
            <button class="k go embark" id="b-send" onclick="embark()" disabled>EMBARK</button>
          </div>
          </div>
          <p class="small dim help">Hold arrows""")
rep("  const canSend = gateReady() && !state.irisClosed && g.ok && (sel.length > 0 || g.malp) && !assistMode;\n", "  const canSend = gateReady() && !state.irisClosed && g.ok && (sel.length > 0 || g.malp) && !assistMode;\n  const gT = (() => { const sw = state.withMalp; state.withMalp = false; const x = checkGroup(); state.withMalp = sw; return x; })();\n  $('b-send').disabled = !(gateReady() && !state.irisClosed && gT.ok && sel.length > 0 && !assistMode);\n  $('b-malp').disabled = !(gateReady() && !state.irisClosed && state.withMalp && !!homeMalp() && !!state.dest);\n")
i = s.rindex("</style>")
s = s[:i] + ".kcom { justify-content: flex-start; gap: 5px; margin-bottom: 0; }\n.kb .kcom button.k { height: 44px; min-height: 44px; }\n.kb .ksend button.k { min-width: 96px; font-size: 13px; }\n.kb .ksend button.k.embark { height: 93px; min-height: 93px; font-size: 15px; letter-spacing: 0.18em; }\n.kb .ksend button.k.go:not(:disabled) { border-color: #3fd07a; box-shadow: 0 4px 0 #050d16, 0 0 12px rgba(63, 208, 122, 0.45); }\n" + s[i:]

rep("function dispatch() {\n", "function embark() {\n  const sw = state.withMalp;\n  state.withMalp = false;\n  dispatch();\n  state.withMalp = sw && !!homeMalp();\n  renderAll();\n}\n\nfunction sendMalp() {\n  const ss = state.sel.slice();\n  const sv = state.selVeh.slice();\n  state.sel = [];\n  state.selVeh = [];\n  dispatch();\n  state.sel = ss;\n  state.selVeh = sv;\n  renderAll();\n}\n\nfunction dispatch() {\n")
rep("${g.malp ? ' + MALP' : ''}`", "`")
rep("onclick=\"dispatch()\">${label}</button>", "onclick=\"${sel.length ? 'embark()' : 'sendMalp()'}\">${label}</button>")
rep("    h += nt;\n", "    if (malpIn) h += '<p class=\"small dim\">The MALP is sent on its own with SEND MALP. EMBARK sends the teams only.</p>';\n    h += nt;\n")

rep("let mapCam = null;", "let mapCam = null;\nlet MAP_A = 800 / 560;\nfunction mapBase() { const w = Math.max(800, 560 * MAP_A); return { x: 400 - w / 2, y: 280 - w / MAP_A / 2, w }; }")
rep("  let vx = 0;\n  let vy = 0;\n  let vw = 800;\n  if (mapCam) { vx = mapCam.x; vy = mapCam.y; vw = mapCam.w; }\n  mapView = { x: vx, y: vy, w: vw };\n  const vh = vw * 560 / 800;", "  const mb = mapBase();\n  let vx = mb.x;\n  let vy = mb.y;\n  let vw = mb.w;\n  if (mapCam) { vx = mapCam.x; vy = mapCam.y; vw = mapCam.w; }\n  mapView = { x: vx, y: vy, w: vw };\n  const vh = vw / MAP_A;")
rep("mapView.w * 560 / 800", "mapView.w / MAP_A", 2)
a = s.index("  m.style.maxWidth = '';\n  const pad = parseFloat(getComputedStyle(sm).paddingBottom) || 0;")
b = s.index("if (window.ResizeObserver) new ResizeObserver(fitStarmap)")
s = s[:a] + """  const pad = parseFloat(getComputedStyle(sm).paddingBottom) || 0;
  const hh = Math.floor((sm.getBoundingClientRect().bottom - m.getBoundingClientRect().top) / FIT.s - pad);
  if (hh > 120) {
    const sp = $('smpanel');
    const ph = sp && sp.firstChild ? sp.offsetHeight + 12 : 0;
    const ah = Math.max(120, hh - ph);
    m.style.height = hh + 'px';
    $('smmap').style.height = ah + 'px';
    const wv = m.clientWidth;
    const na = Math.max(1, Math.min(3, wv / ah));
    if (wv > 0 && Math.abs(na - MAP_A) > 0.004) { MAP_A = na; renderStarmapMap(); }
  }
}
""" + s[b:]
rep("function showView(name) {\n", "function showView(name) {\n  if (name !== 'gate' && window.DRONE && DRONE.isActive()) return;\n")
rep("</script>\n</body>", "</script>\n<script>\n$('starmap').appendChild($('drone'));\nif (window.ResizeObserver) new ResizeObserver(fitStarmap).observe($('smpanel'));\n</script>\n</body>")
i = s.rindex("</style>")
s = s[:i] + """body.gv .smmap { height: 100%; }\nbody.gv #smbox { background: #02060c; }
body.gv #smbox { height: auto; }
#starmap { position: relative; }
#starmap #drone { position: absolute; inset: 0; z-index: 40; min-height: 0; overflow: hidden auto; font-size: 11px; line-height: 1.35; }
#starmap #drone[hidden] { display: none; }
#starmap #drone .wrap { max-width: none; padding: 8px 10px 10px; }
#starmap #drone h1 { font-size: 14px; letter-spacing: 2px; }
#starmap #drone .sub { font-size: 10px; margin-bottom: 6px; }
#starmap #drone .dhead { margin-bottom: 4px; }
#starmap #drone .cols { grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr); gap: 8px; }
#starmap #drone .panel { padding: 6px; }
#starmap #drone .tele { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 4px; margin-top: 6px; }
#starmap #drone .zv { width: 170px; top: 8px; right: 8px; }
#starmap #drone canvas#dr_radar { width: 100%; height: auto; max-width: 220px; display: block; margin: 0 auto; }
#starmap #drone .hint { padding: 8px 10px; font-size: 10px; width: 86%; }
""" + s[i:]

open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(s))
