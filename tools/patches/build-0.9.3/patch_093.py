import sys
src, dst = sys.argv[1:3]
s = open(src, encoding='utf-8').read()
assert s.count('0.9.2') == 4, s.count('0.9.2')
s = s.replace('0.9.2', '0.9.3')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

rep("  const strip = staffStripHtml(k === 'med' ? here.filter(m => m.id === 'medic') : here, ['brief', 'barracks', 'lab', 'med', 'arch'].includes(k) ? 'NO STAFF ON STATION' : '');",
    "  const strip = (k === 'brief' || k === 'barracks') ? '' : staffStripHtml(k === 'med' ? here.filter(m => m.id === 'medic') : here, ['lab', 'med', 'arch'].includes(k) ? 'NO STAFF ON STATION' : '');")

rep("""function markerXY(t, layer, sysLv) {
  const w = world(t.mission.worldId);
  if (!w) return null;
  const s = sysOf(w.level);
  const tp = teamP(t);
""", """function tkP(x) {
  const w = world(x.world);
  if (!w || x.status !== 'away') return null;
  if (x.rolled) return { w, p: 0, st: 'back' };
  const ms = tkRoundMs(w);
  const f = Math.max(0, Math.min(1, (Date.now() - (x.eta - ms)) / ms));
  return f < 0.5 ? { w, p: f * 2, st: 'out' } : { w, p: (1 - f) * 2, st: 'back' };
}

function markerXY(t, layer, sysLv) {
  return markerGen(world(t.mission.worldId), teamP(t), layer, sysLv);
}

function markerGen(w, tp, layer, sysLv) {
  if (!w) return null;
  const s = sysOf(w.level);
""")

rep("""function markersSvg(layer, sysLv, sc) {
  let h = '';
""", """function tkShapeAttr(m, sc) {
  const ang = Math.atan2(m.ey - m.oy, m.ex - m.ox) * 180 / Math.PI + (m.st === 'back' ? 180 : 0);
  return `translate(${m.x.toFixed(1)} ${m.y.toFixed(1)}) rotate(${ang.toFixed(0)}) scale(${(sc * 1.6).toFixed(3)})`;
}

function tkMarkersSvg(layer, sysLv, sc) {
  let h = '';
  state.arm.ships.forEach(x => {
    const tp = tkP(x);
    if (!tp) return;
    const m = markerGen(tp.w, tp, layer, sysLv);
    if (!m) return;
    h += `<line x1="${m.ox.toFixed(1)}" y1="${m.oy.toFixed(1)}" x2="${m.ex.toFixed(1)}" y2="${m.ey.toFixed(1)}" stroke="#ffd36a" stroke-opacity="0.3" stroke-width="${(1.1 * sc).toFixed(2)}" stroke-dasharray="${(2 * sc).toFixed(1)} ${(4 * sc).toFixed(1)}"/>`;
    h += `<path data-tkm="${x.id}" transform="${tkShapeAttr(m, sc)}" d="M7 0 L-5 -4.5 L-2.5 0 L-5 4.5 Z" fill="#ffd36a" stroke="#02060c" stroke-width="1.2"><title>${tkName(x)} // supply run to ${wname(tp.w)}</title></path>`;
  });
  return h;
}

function markersSvg(layer, sysLv, sc) {
  let h = tkMarkersSvg(layer, sysLv, sc);
""")

rep("""function updateMarkers() {
  if ($('view-gate').hidden) return;
  const layer = state.mapLayer;
  const sysLv = Math.min(state.mapSys || 1, state.level);
""", """function updateMarkers() {
  if ($('view-gate').hidden) return;
  const layer = state.mapLayer;
  const sysLv = Math.min(state.mapSys || 1, state.level);
  document.querySelectorAll('[data-tkm]').forEach(el => {
    const x = state.arm.ships.find(v => v.id === el.dataset.tkm);
    const tp = x ? tkP(x) : null;
    const m = tp ? markerGen(tp.w, tp, layer, sysLv) : null;
    if (!m) { el.setAttribute('visibility', 'hidden'); return; }
    el.setAttribute('visibility', 'visible');
    el.setAttribute('transform', tkShapeAttr(m, mapView.w / 800));
  });
""")
open(dst, 'w', encoding='utf-8').write(s)
