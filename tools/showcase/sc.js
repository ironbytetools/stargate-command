(function () {
  const g = id => document.getElementById(id);
  let active = '';
  let hazard = 'low';
  let hints = 0;

  function closeAll() {
    try { if (typeof RXG !== 'undefined' && RXG) { RXG = null; g('rxgame').hidden = true; } } catch (e) { /* none */ }
    try { if (typeof GLG !== 'undefined' && GLG) { GLG = null; g('glgame').hidden = true; } } catch (e) { /* none */ }
    try { if (typeof HPG !== 'undefined' && HPG) { clearInterval(HPG.iv); HPG = null; g('hpgame').hidden = true; } } catch (e) { /* none */ }
    try { if (typeof CTG !== 'undefined' && CTG) { CTG = null; g('ctgame').hidden = true; } } catch (e) { /* none */ }
    try { if (typeof COMG !== 'undefined' && COMG) comClose(); } catch (e) { /* none */ }
    try { if (window.DRONE && DRONE.isActive()) DRONE.abort(); } catch (e) { /* none */ }
    try { if (typeof AARG !== 'undefined' && AARG) aarReset(); } catch (e) { /* none */ }
  }
  function fresh() {
    closeAll();
    resetGame();
    state.started = true;
    state.tourDone = true;
    g('titlescreen').hidden = true;
    g('menu').hidden = true;
    state.res.supplies = 500;
    state.res.power = 120;
    document.body.classList.remove('gv');
    showView('base');
    renderAll();
  }
  function gate(w) {
    state.dest = w.id;
    state.target = w.addr.slice();
    state.planet = wname(w);
    state.gate = 'open';
    state.openT = performance.now() - 5000;
    state.irisClosed = false;
    state.incoming = null;
    state.chevrons = 7;
    showView('gate');
    renderAll();
  }
  function away(w, overdue) {
    const t = state.teams[0];
    t.status = 'away';
    t.depart = Date.now() - 600000;
    t.eta = Date.now() + 1e10;
    const lid = openMission('exp', w, [t], {});
    t.mission = { mid: missionToken(), worldId: w.id, kind: 'exp', mt: 'exp', gtags: [], ids: [t.id], lid, overdue: !!overdue };
    return t;
  }
  function normalWorld() {
    const w = state.worlds.find(x => x.kind === 'normal') || state.worlds[0];
    w.hazard = hazard;
    return w;
  }

  const rxJob = key => () => {
    fresh();
    selectRoom('quarter');
    state.rx = rxLoad(null);
    RXPARK = null;
    if (key === 'evt') state.rx.evt = true;
    else if (key === 'off') state.rx.off = 'lab';
    else state.rx.node = key === 'zpm' ? { zpm: true } : { tier: +key.slice(1) };
    rxOpen();
  };
  const rxSolo = k => () => {
    fresh();
    selectRoom('quarter');
    state.rx = rxLoad(null);
    RXPARK = null;
    state.rx.off = 'lab';
    rxOpen();
    RXG.stages = [k];
    RXG.si = 0;
    RXG.key = 'sc';
    rxStageStart();
    rxDraw();
  };
  const glRun = (n) => () => {
    fresh();
    selectRoom('arch');
    state.glyph.a[n - 1].f = true;
    state.glyph.a[n - 1].fails = hints;
    GLG = { n, type: GL_ARTS[n - 1].type, vis: false, res: null };
    glNew();
    g('glgame').hidden = false;
    glRender();
  };
  const hammond = () => {
    fresh();
    selectRoom('brief');
    state.mini.hpCd = 0;
    hpOpen();
  };
  const carter = cat => () => {
    fresh();
    selectRoom('lab');
    state.perm.carter = true;
    state.mini.ctCd = 0;
    const p = { id: 'sc-demo', kind: 'gate', tier: 1, total: 600000, left: 600000, asked: false };
    state.lab.projs.push(p);
    const pool = CT_Q.map((q, i) => i).filter(i => CT_Q[i].cat === cat);
    const q = CT_Q[hpPick(pool)];
    const opts = glShuffle([{ t: q.real, ok: true }].concat(q.fake.map(t => ({ t, ok: false }))));
    CTG = { pid: p.id, q, opts, res: null };
    g('ctgame').hidden = false;
    ctRender();
  };
  const aar = () => {
    fresh();
    const w = normalWorld();
    const t = state.teams[0];
    const id = openMission('exp', w, [t], {});
    const r = mfind(id);
    r.state = 'closed';
    r.ended = clock();
    r.yield = { supplies: 34, naquadah: 6, research: 12 };
    r.intelEnd = Math.min(5, w.intel + 1);
    r.ret = [crewSnap(t)];
    selectRoom('brief');
    aarOpen(id);
  };
  const comm = kind => () => {
    fresh();
    const w = normalWorld();
    away(w, kind === 1);
    gate(w);
    if (kind === 1) com1();
    else com2();
  };
  const recon = () => {
    fresh();
    const w = state.worlds.find(x => x.stronghold) || state.worlds[0];
    w.intel = Math.max(w.intel, 2);
    w.hazard = hazard;
    state.droneCd = 0;
    gate(w);
    droneKeyUpdate();
    droneRecon();
  };

  const SECS = [
    { t: 'REACTOR CONTROL TABLET', d: 'Quartermaster. Six puzzles, played as the five jobs the game gives you.', items: [
      ['rx-evt', 'Power fluctuation', 'Conduit + Breaker', rxJob('evt')],
      ['rx-t4', 'Reactor tier I', 'Balance + Load shedding', rxJob('t4')],
      ['rx-t6', 'Reactor tier II', 'Pipes + Breaker', rxJob('t6')],
      ['rx-t7', 'Reactor tier III', 'Balance + Phase', rxJob('t7')],
      ['rx-zpm', 'ZPM install', 'Pipes + Phase', rxJob('zpm')],
      ['rx-off', 'Restore output', 'Conduit only', rxJob('off')]
    ] },
    { t: 'REACTOR PUZZLES, ONE AT A TIME', d: 'Any single puzzle on its own.', items: [
      ['rs-grid', 'Conduit puzzle', '', rxSolo('grid')],
      ['rs-knobs', 'Power balance', 'three knobs', rxSolo('knobs')],
      ['rs-pipe', 'Pipe routing', '', rxSolo('pipe')],
      ['rs-breaker', 'Breaker sequence', '', rxSolo('breaker')],
      ['rs-phase', 'Phase match', 'three knobs', rxSolo('phase')],
      ['rs-shed', 'Load shedding', '', rxSolo('shed')]
    ] },
    { t: 'GLYPH DECODE CONSOLE', d: 'Archeology Office. The hint level is how many tablets you have already failed. After a decode, the System Lord seal step appears.', hints: true, items: [
      ['gl-1', 'Fragment matching', '', glRun(1)],
      ['gl-2', 'Tablet reassembly', '', glRun(2)],
      ['gl-3', 'Cipher deduction', '', glRun(3)]
    ] },
    { t: 'HAMMOND\'S PAPERWORK', d: 'Briefing Room. 90 seconds, 12 forms, keys 1 to 4 and D.', items: [['hp', 'Binder desk', '', hammond]] },
    { t: 'CARTER\'S QUESTIONS', d: 'Science Lab. One question per topic; five topics.', items: [
      ['ct-reactor', 'Reactors and power', '', carter('reactor')],
      ['ct-dial', 'Dialing and the gate', '', carter('dial')],
      ['ct-sec', 'Security and iris', '', carter('sec')],
      ['ct-malp', 'MALPs', '', carter('malp')],
      ['ct-arm', 'Armory and tech', '', carter('arm')]
    ] },
    { t: 'AFTER-ACTION REPORT', d: 'Briefing Room. Type the report from the mission log.', items: [['aar', 'File a report', '', aar]] },
    { t: 'RADIO AND DRONE', d: 'Gate Room. Hazard sets the search area and difficulty.', hazard: true, items: [
      ['rd-1', 'COMM 1: overdue team', 'tune, then fly the drone', comm(1)],
      ['rd-2', 'COMM 2: recall a team', 'tune, then recall', comm(2)],
      ['rd-recon', 'Assault recon drone', 'stronghold survey', recon]
    ] }
  ];
  const ACTIONS = {};

  function build() {
    let h = '<div class="sct">SGC COMMAND</div><div class="scs">MINIGAME SHOWCASE // BUILD ' + BUILD_VER + '</div><div class="scn">A sandbox. Every button starts a fresh game state and nothing is saved.</div>';
    SECS.forEach(s => {
      h += '<div class="scsec"><div class="scst">' + s.t + '</div><div class="scsd">' + s.d + '</div>';
      if (s.hints) h += '<div class="scseg" data-seg="hints">' + [0, 1, 2, 3].map(n => '<button data-v="' + n + '" class="' + (n === hints ? 'on' : '') + '">HINTS ' + n + '</button>').join('') + '</div>';
      if (s.hazard) h += '<div class="scseg" data-seg="hazard">' + ['low', 'med', 'high'].map(n => '<button data-v="' + n + '" class="' + (n === hazard ? 'on' : '') + '">' + n.toUpperCase() + '</button>').join('') + '</div>';
      s.items.forEach(it => {
        ACTIONS[it[0]] = it[3];
        h += '<button class="scb" data-id="' + it[0] + '"' + (it[3] ? '' : ' disabled') + '><b>' + it[1] + '</b>' + (it[2] ? '<small>' + it[2] + '</small>' : '') + '</button>';
      });
      h += '</div>';
    });
    g('scbar').innerHTML = h;
  }
  function launch(id) {
    const f = ACTIONS[id];
    if (!f) return;
    active = id;
    try { history.replaceState(null, '', '#' + id); } catch (e) { /* none */ }
    f();
    document.querySelectorAll('#scbar .scb').forEach(b => b.classList.toggle('on', b.dataset.id === id));
  }
  function init() {
    const bar = document.createElement('aside');
    bar.id = 'scbar';
    document.body.appendChild(bar);
    document.body.classList.add('sc');
    build();
    fresh();
    bar.addEventListener('click', e => {
      const sg = e.target.closest('[data-seg]');
      if (sg && e.target.dataset.v !== undefined) {
        if (sg.dataset.seg === 'hints') hints = +e.target.dataset.v;
        else hazard = e.target.dataset.v;
        sg.querySelectorAll('button').forEach(b => b.classList.toggle('on', b === e.target));
        if (active) launch(active);
        return;
      }
      const b = e.target.closest('.scb');
      if (b && !b.disabled) launch(b.dataset.id);
    });
    const h = (location.hash || '').slice(1);
    if (h && ACTIONS[h]) launch(h);
  }
  window.addEventListener('load', () => setTimeout(init, 200));
})();
