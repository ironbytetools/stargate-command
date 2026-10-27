const ROLE_COL = { exp: '#7ffbff', rec: '#5be8c4', asl: '#ff9a5c', dip: '#b79cff', sec: '#ffd36a', '': '#8fb4ff' };

function roleKey(role, type) {
  const r = String(role || '').replace(' (permanent)', '');
  if (type === 'sec') return 'sec';
  if (r === 'Team Lead' || r === 'Team Leader') return 'cmd';
  const m = { Soldier: 'inf', Rifleman: 'inf', Scientist: 'sci', Linguist: 'globe', Sniper: 'scope', 'Recon Specialist': 'recon', 'Machine Gunner': 'mg', Grenadier: 'gren', Diplomat: 'olive', Aide: 'scroll', Medical: 'med' };
  return m[r] || 'inf';
}

function roleIcon(role, type, status) {
  const k = roleKey(role, type);
  let col = ROLE_COL[type || ''] || ROLE_COL[''];
  let extra = '';
  let dash = '';
  if (status === 'injured') {
    col = '#ff4d4d';
    extra = '<path d="M37 5V13M33 9H41" stroke="#ff4d4d" stroke-width="2.4"/>';
  } else if (status === 'captured') {
    col = '#ffb347';
    dash = ' stroke-dasharray="4 2.5"';
  } else if (status === 'killed') {
    col = '#6b7785';
    extra = '<path d="M5 28L41 5" stroke="#6b7785" stroke-width="2.2"/>';
  }
  return `<svg class="rico" viewBox="0 0 46 33" aria-hidden="true"><rect x="1.5" y="1.5" width="43" height="30" rx="2" fill="#07101c" stroke="${col}" stroke-width="2"${dash}/><rect x="5" y="5" width="36" height="23" fill="none" stroke="${col}" stroke-opacity=".35"/>${roleIco(k, 23, 16.5, 11, col)}${extra}</svg>`;
}

function secGroup(el) {
  let cur = null;
  Array.from(el.children).forEach(k => {
    if (!cur || k.tagName === 'H2') {
      cur = document.createElement('div');
      cur.className = 'rsec';
      el.insertBefore(cur, k);
    }
    cur.appendChild(k);
  });
}

function sectionize(root) {
  if (!root) return;
  let cur = null;
  Array.from(root.children).forEach(k => {
    if (k.classList.contains('rgrid')) {
      cur = null;
      Array.from(k.children).forEach(c => { c.classList.add('rcol'); secGroup(c); });
      return;
    }
    if (!cur || k.tagName === 'H2') {
      cur = document.createElement('div');
      cur.className = 'rsec';
      root.insertBefore(cur, k);
    }
    cur.appendChild(k);
  });
}

function fitMain() {
  const m = document.querySelector('main');
  if (!m) return;
  if (document.body.classList.contains('gv') || window.innerWidth <= 900) { if (m.style.minHeight) m.style.minHeight = ''; return; }
  const top = m.getBoundingClientRect().top + window.scrollY;
  const v = Math.max(480, window.innerHeight - top) + 'px';
  if (m.style.minHeight !== v) m.style.minHeight = v;
}

window.addEventListener('resize', fitMain);
setInterval(fitMain, 400);

