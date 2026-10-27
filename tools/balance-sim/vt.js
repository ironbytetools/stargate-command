(function(){
  let now = 1760000000000, seq = 1; const q = new Map();
  const T0 = now;
  Date.now = () => now;
  performance.now = () => now - T0 + 1000;
  window.setTimeout = (fn, ms, ...a) => { const id = seq++; q.set(id, {t: now + Math.max(0, +ms||0), fn: () => fn(...a), iv: 0, id}); return id; };
  window.setInterval = (fn, ms, ...a) => { const id = seq++; const iv = Math.max(1, +ms||1); q.set(id, {t: now + iv, fn: () => fn(...a), iv, id}); return id; };
  window.clearTimeout = window.clearInterval = id => { q.delete(id); };
  window.requestAnimationFrame = () => 0;
  window.__vt = { async advance(ms){
    const end = now + ms;
    for(;;){
      let best = null;
      for (const e of q.values()) if (e.t <= end && (!best || e.t < best.t || (e.t === best.t && e.id < best.id))) best = e;
      if (!best) break;
      now = best.t;
      if (best.iv) best.t = now + best.iv; else q.delete(best.id);
      try { best.fn(); } catch(e) { (window.__errs = window.__errs || []).push(String(e)); }
      for (let k=0;k<4;k++) await null;
    }
    now = end;
  }, n(){ return q.size; } };
})();
