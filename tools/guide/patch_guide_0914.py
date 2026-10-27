s = open('build_guide.py', encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


rep('BUILD = "0.9.11"', 'BUILD = "0.9.14"')
rep('content: "BUILD 0.9.11  //  TRAINING COPY"', 'content: "BUILD 0.9.14  //  TRAINING COPY"')

rep('p("No minigame opens as a popup. Each runs inside the panel',
    'p("Reactor routing, glyph decoding and Hammond\'s paperwork are styled as devices: a rugged control tablet, a translation console and a desk with a binder. Each scales to fit its panel.")\np("No minigame opens as a popup. Each runs inside the panel')

rep('"**Conduit puzzle.** A 4 by 4 grid of conduits. Fill each with a value from 1 to 5. No value may repeat in a row or column, and every row and column must add up to its target. Some conduits are locked. Click a conduit, then pick a value or press 1 to 5.",',
    '"**The tablet.** Reactor routing runs on a rugged control tablet in the Quartermaster panel: a screen with a stage counter, eight side buttons (up, down, left, right, SEL, ALT, INFO, ABORT), five number keys and three knobs. Keyboard: arrows, Enter or Space for SEL, Backspace, Delete, X or 0 for ALT, I for INFO, 1 to 5, Esc to leave. INFO shows help for the current puzzle. Large jobs run as two stages, shown by the dots in the header.","**Conduit puzzle.** A 4 by 4 grid of conduits. Fill each with a value from 1 to 5. No value may repeat in a row or column, and every row and column must add up to its target. Some conduits are locked. Move the cursor with the arrows and press 1 to 5, or press SEL to cycle the value.",')
rep('Choosing ABANDON, instead of solving the puzzle, knocks', 'Pressing ABORT twice during a power event, instead of solving it, knocks')
a = s.index('"**Relay puzzle.**')
b = s.index('"**Presets.**')
s = s[:a] + '"**New connections.** Installing a Reactor tier or the ZPM opens a two-stage routing job (see the table below). A new Reactor tier adds its power only after both stages are solved. Leaving with ABORT keeps finished stages and returns you to the same stage later, with no penalty. The ZPM has no gameplay effect yet; routing it is only a record of the install.",' + s[b:]
rep('table(["PRESET","GATE REGENERATION"',
    'table(["JOB","STAGE 1","STAGE 2"],[["Power fluctuation","Conduit puzzle","Breaker sequence"],["Reactor I","Power balance","Load shedding"],["Reactor II","Pipe routing","Breaker sequence"],["Reactor III","Power balance","Phase match"],["ZPM","Pipe routing","Phase match"],["Restore an offline output","Conduit puzzle","none"]])\nul(["**Power balance.** Turn the three knobs (gate, lab, shields) until each output sits in its green band and hold it there. Each output is also nudged by the knob before it. Drag or scroll a knob, or pick one with left and right and turn it with up and down.","**Pipe routing.** Rotate the tiles of a 5 by 4 grid so power flows from the PWR block to all three outputs. SEL rotates clockwise, ALT counter-clockwise, or tap a tile.","**Breaker sequence.** Watch five breakers light up, then flip them in the same order with keys 1 to 5. The sequence is four long during a power event and five otherwise. A mistake replays the same sequence.","**Phase match.** Match a dashed signal with the AMP, FRQ and PHS knobs until all three lamps are green, then hold steady.","**Load shedding.** Switch systems off until the total load sits in the green band just under the reactor cap. Life support and the gate core are locked on."])\ntable(["PRESET","GATE REGENERATION"')

rep('"**Decoding.** Open the Archeology Office',
    '"**The console.** Decoding runs on a console: a teal Message Relay monitor, a lit artifact tray, six glyph keys, a D-pad with ENTER, and BOOK, CLEAR, GIVE UP and CLOSE keys. Keyboard: arrows, Enter, Backspace for CLEAR, B for the book, 1 to 6, Esc to close.","**Decoding.** Open the Archeology Office')
rep('Match six broken fragments to the whole glyphs they were cut from. Four mistakes are allowed.',
    'The monitor marks one whole glyph and the six keypad keys show the broken fragments. Press the key of the fragment cut from the marked glyph; the D-pad changes the marked glyph. Four mistakes are allowed.')
rep('Click two tiles to swap them until the inscription is whole, within 14 moves.',
    'The slab sits on the lit tray. Move the cursor with the D-pad, press ENTER on a tile to pick it and ENTER on another to swap them (or tap tiles), until the inscription is whole, within 14 moves.')
rep('Green marks the right glyph in the right place and amber the right glyph in the wrong place.',
    'Keys 1 to 6 enter glyphs, CLEAR backspaces and ENTER submits. Green marks the right glyph in the right place and amber the right glyph in the wrong place.')
rep('CONSULT LIBRARY BOOK gives a visual hint once per attempt.', 'The BOOK key gives a visual hint once per attempt.')
rep('A second successful Exploration mission there recovers the artifact."])',
    'A second successful Exploration mission there recovers the artifact.","**System Lord seal.** After a decode, if the System Lord of that level has a stronghold you have not located, the tray shows the seal carved on the artifact and keys 1 to 5 show the five lords\' marks. Press the key of the lord who carved it to reveal his stronghold. A wrong key, or CLEAR, gives nothing and costs nothing."])')

rep("Stamp each form with the stamp matching its type (1 Supply, 2 Personnel, 3 Medical, 4 Operations), or press D to deny it.",
    "The forms sit on an open binder with four coloured tabs. File each form in the tab matching its type (keys 1 Supply, 2 Personnel, 3 Medical, 4 Operations, or click the tab), or press D to deny it. A checklist on the facing page ticks as you go, a flatbed-style timer counts down, and a sticky note carries Hammond's comment on the last form.")
open('build_guide.py', 'w', encoding='utf-8').write(s)
print('guide patched')
