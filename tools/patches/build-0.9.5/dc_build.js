function buildDC() {
  let s = '<svg id="dcSvg" viewBox="0 0 1000 560" preserveAspectRatio="xMidYMid meet">';
  s += '<defs>';
  s += '<radialGradient id="dcBg" cx="50%" cy="48%" r="70%"><stop offset="0" stop-color="#06181f"/><stop offset="0.6" stop-color="#020b0f"/><stop offset="1" stop-color="#010405"/></radialGradient>';
  s += '<linearGradient id="dcRim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6fd3ea"/><stop offset="0.5" stop-color="#1c5a74"/><stop offset="1" stop-color="#0b2a3a"/></linearGradient>';
  s += '<radialGradient id="dcHzG"><stop offset="0" stop-color="#f2ffff"/><stop offset="0.45" stop-color="#4cc3ff"/><stop offset="0.85" stop-color="#1257c8"/><stop offset="1" stop-color="#0a3a96"/></radialGradient>';
  s += '</defs>';
  s += '<rect x="4" y="4" width="992" height="552" rx="18" fill="url(#dcBg)" stroke="#2fd0e8" stroke-width="3"/>';
  s += '<rect x="10" y="10" width="980" height="540" rx="14" fill="none" stroke="#0f4258" stroke-width="1"/>';
  s += '<g id="dcEmblem" transform="translate(48 38)"><g id="dcEmblemG" class="dcemb"></g></g>';
  s += '<text x="82" y="30" class="dct">STARGATE COMMAND</text><text x="82" y="46" class="dct dim2">DIALING COMPUTER</text>';
  s += '<g id="dcDots"></g>';
  s += '<text x="986" y="26" class="dct dim2" text-anchor="end">DESTINATION</text>';
  s += '<text id="dcDest" x="986" y="46" class="dcbig" text-anchor="end">------</text>';
  s += '<text id="dcDestSub" x="986" y="58" class="dct dim2" text-anchor="end"></text>';
  for (let k = 0; k < 7; k++) s += `<path id="dct${k}" class="dctrace" d="${dcTrace(k)}"/>`;
  s += `<g transform="translate(${DC_CX} ${DC_CY})">`;
  s += '<circle r="186" fill="#05121c" stroke="#0e3d56" stroke-width="2"/>';
  s += '<circle r="170" fill="none" stroke="url(#dcRim)" stroke-width="14"/>';
  s += '<g id="dcRing"><circle r="146" fill="none" stroke="#0a2433" stroke-width="40"/>';
  for (let i = 0; i < N; i++) {
    s += `<line x1="0" y1="-124" x2="0" y2="-129" stroke="#0f4258" stroke-width="1" transform="rotate(${((i + 0.5) * STEP).toFixed(2)})"/>`;
    s += `<g class="dcgl" id="dcgl${i}" transform="rotate(${(i * STEP).toFixed(3)}) translate(0 -148) scale(0.85)">${GLYPHS[i]}</g>`;
  }
  s += '</g>';
  for (let j = 0; j < 9; j++) s += `<g transform="rotate(${j * 40})"><path id="dcch${j}" class="dcchev" d="M-15 -192 L15 -192 L9 -164 L0 -153 L-9 -164 Z"/></g>`;
  s += '<circle r="126" fill="none" stroke="#0e4a66" stroke-width="3"/>';
  s += '<circle r="120" fill="#020a12"/>';
  s += '<circle id="dcHz" r="0" fill="url(#dcHzG)"/>';
  s += '<circle id="dcRip1" r="0" fill="none" stroke="#e9ffff" stroke-width="1.5"/><circle id="dcRip2" r="0" fill="none" stroke="#b6f0ff" stroke-width="1"/><circle id="dcRip3" r="0" fill="none" stroke="#8ad8ff" stroke-width="1"/>';
  s += '<circle id="dcIris" r="0" fill="#3a4d63" stroke="#0a111b" stroke-width="2"/>';
  s += '<circle r="121" fill="none" stroke="#4ab6d8" stroke-opacity="0.5" stroke-width="1.5"/>';
  s += '</g>';
  s += '<g id="dcHeroes">';
  for (let k = 0; k < 7; k++) s += `<g id="dchero${k}" class="dchero" style="display:none"></g>`;
  s += '</g>';
  for (let k = 0; k < 7; k++) {
    const top = dcBoxTop(k);
    s += `<g id="dcbox${k}"><rect id="dcbr${k}" class="dcbox" x="690" y="${top}" width="80" height="46" rx="3"/><text x="698" y="${top + 30}" class="dcnum">${k + 1}</text><text id="dcbs${k}" x="698" y="${top + 40}" class="dct tiny dim2">--</text><g id="dcbg${k}" class="dcbgl" transform="translate(744 ${top + 23}) scale(1.5)"></g></g>`;
  }
  s += '<text x="782" y="82" class="dct dim2 tiny">SEQUENCE COMPILER</text>';
  for (let i = 0; i < N; i++) {
    const cx = 782 + (i % 4) * 51;
    const cy = 90 + Math.floor(i / 4) * 38;
    s += `<g id="dccg${i}" class="dccg"><rect x="${cx}" y="${cy}" width="47" height="34" rx="3"/><g class="dcsg" transform="translate(${cx + 23.5} ${cy + 17}) scale(1.15)">${GLYPHS[i]}</g></g>`;
  }
  s += '<rect x="20" y="62" width="250" height="130" rx="3" class="dccell"/><text x="28" y="80" class="dct dim2 tiny">ACTIVE MISSIONS</text><text id="dcMsCount" x="262" y="80" class="dct tiny" text-anchor="end">0</text><line x1="24" y1="86" x2="266" y2="86" stroke="#1d4a5e" stroke-width="1"/>';
  s += '<text id="dcMsNone" x="145" y="136" class="dct tiny dim2" text-anchor="middle">NO ACTIVE MISSIONS</text>';
  for (let r = 0; r < 5; r++) {
    const y = 106 + r * 18;
    s += `<text id="dcmn${r}" x="28" y="${y}" class="dct tiny dcmsn"></text><text id="dcmt${r}" x="92" y="${y}" class="dct tiny dim2"></text><text id="dcme${r}" x="262" y="${y}" class="dct tiny dcmse" text-anchor="end"></text>`;
  }
  s += '<text id="dcClock" x="20" y="222" class="dcmid">00:00:00</text>';
  s += '<text id="dcDate" x="20" y="242" class="dct dim2"></text>';
  const cells = [['pwr', 'POWER'], ['sup', 'SUPPLIES'], ['naq', 'NAQUADAH'], ['rp', 'RESEARCH'], ['away', 'TEAMS AWAY'], ['lvl', 'LEVEL']];
  cells.forEach((c, i) => {
    const x = 20 + (i % 2) * 129;
    const y = 252 + Math.floor(i / 2) * 50;
    s += `<rect x="${x}" y="${y}" width="121" height="46" rx="3" class="dccell"/><text x="${x + 6}" y="${y + 16}" class="dct dim2 tiny">${c[1]}</text><text id="dcv_${c[0]}" x="${x + 6}" y="${y + 38}" class="dcval">0</text><polyline id="dcs_${c[0]}" class="dcspark" points=""/>`;
  });
  const bits = ['10110010 0110', '01001101 1010', '11010011 0101', '00101110 1001', '10011010 0110'];
  bits.forEach((b, i) => { s += `<text x="20" y="${414 + i * 15}" class="dct tiny dim2">${b}</text>`; });
  s += '<g style="display:none">';
  for (let k = 0; k < 7; k++) {
    s += `<rect id="dcrw${k}" class="dcrow" x="0" y="0" width="1" height="1"/><text id="dcrt${k}">--</text>`;
  }
  s += '</g>';
  s += '<rect x="20" y="480" width="960" height="64" rx="6" class="dcfoot"/>';
  s += '<text x="34" y="498" class="dct dim2 tiny">WORMHOLE TIME</text><text id="dcCount" x="34" y="530" class="dcmono">--:--.---</text>';
  s += '<rect x="226" y="488" width="350" height="48" rx="3" class="dcstbox"/><text id="dcStatus" x="401" y="521" class="dcstat2" text-anchor="middle">STANDBY</text>';
  s += '<text x="596" y="498" class="dct dim2 tiny">IDC TRANSPONDER:</text><text id="dcAuth" x="596" y="516" class="dcmid2">----</text><text id="dcLst" x="596" y="534" class="dct tiny dim2"></text>';
  s += '<text id="dcUser" x="970" y="508" class="dct" text-anchor="end">USER: GATE TECH</text><text id="dcSys" x="970" y="526" class="dct" text-anchor="end">SYS: NOMINAL</text>';
  s += '</svg>';
