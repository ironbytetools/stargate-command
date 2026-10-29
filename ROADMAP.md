# Stargate Command - Roadmap

Built:
- 0.8.5: drone spotting made forgiving (slower exposure, faster recovery, smaller defender cones, amber proximity warning), header reduced to MENU with Settings, Help, Sound and Full Screen inside the Menu, Gate Room and Facility scaled to fit the display
- 0.8.6: opening tour (Hammond and Carter) with pause, Mission Briefing tab, recon odds bonus; root is 0.8.6, older builds in versions/archive/
- 0.8.4: COMM 1 Reconnaissance Drone (free-flight signal chase scored by distance) replaces the triangulation; assault recon flight with a DRONE key, strength reduction, alert penalty and 5-minute cooldown (see docs/design/minigames-design.md)
- 0.7.1: radio contact - COMM 1 and COMM 2 keys, tune-and-triangulate minigame, 3:30 overdue rule, hidden ambush events, fix band effects on assists (see docs/design/minigames-design.md)
- 0.7.0: Archeology Office room, permanent staff (Lee, Felger, Langford), Facility layout with a narrow room column (see docs/design/minigames-design.md)
- 0.6.14: Special Operations rescue teams in the Quartermaster (five real units, rescue overdue teams and captured members; see docs/design/rescue-design.md)
- 0.6.13: two starting Exploration teams, final-stronghold lock at 75% of regular worlds rounded down, ambush injury chance halved (from the 0.6.12 balance pass)
- 0.6.12: power capped at 120 (regeneration tiers kept)
- 0.6.11: gate power by light years (8 per ly, orbit-order offset), power cap removed with Reactor tiers as regeneration, Abandoned Ancient Research Ship and ZPM (see gate-power-design.md)
- 0.6.10: logistics limited to two shipments in transit at once
- 0.6.9: Air Force Logistics supply requests in the Quartermaster (six real bases, four transport tiers, shared cooldown, level unlocks; see docs/design/logistics-design.md); Tel'tak base return raised to 100
- 0.6.8: Gate Room - dead space removed (starmap held to the dialing computer height), map controls moved onto the map
- 0.6.7: Gate Room - dialing controls moved into the dialing computer as keyboard keys; active mission table replaces the wormhole ring (teams on one mission show as one row)
- 0.6.6: Gate Room - starmap panel ends level with the dialing computer panel
- 0.6.5: Gate Room layout restored to the 0.6.2 arrangement; kept the new dialing controls and IDC transponder text (0.6.3 and 0.6.4 superseded)
- 0.6.3: Gate Room screen rework - fits the window, log at the bottom, Mission under the controls, drag-swap and resizable panels saved in Settings, console-style dialing controls, IDC transponder text on the dialing computer
- 0.6.2: room card cleanup - staff strip, selectable cards in the Lab, Gate Room, Barracks, Motor Pool and Armory, help-toggled descriptions, Armory staff moved to the Barracks
- 0.6.1: Science Lab upgrades - three tiers, parallel project slots, pace, project and rush discounts, Lab offline during construction (see docs/design/lab-design.md)
- 0.5.8: galaxy and starmap overhaul - five real star systems (one per level, Level 5 final), galaxy view and orbital system view with moons and stations, live path tracking in both layers, per-system gate power cost (see docs/design/galaxy-design.md)

Planned:
- 0.7.1 to 0.7.4 (built) minigames, in testing (all designed in docs/design/minigames-design.md). Released to root Oct 25 2026 with 0.8.0 to 0.8.5; Game Guide refreshed
- 0.7.5 (RELEASED): rescue request on the COMM 1 result screen only (was planned as 0.6.16).
- 0.5.9 (complete): research phase two. Gate Room ladder (gate-upgrades-design.md), Armory gear, alien tech and Tel'tak (docs/design/armory-design.md)
- 0.6.0 (built, in testing): factions and diplomacy (docs/design/faction-design.md). Logistics from the Campaign Logic doc is now covered by 0.6.9
- Diplomatic Peaceful worlds for non-faction worlds (proposed): the Diplomat Team and DIPLOMACY mission exist for faction worlds. Still to design: whether ordinary worlds can be made Peaceful, odds, cost, eligibility and whether peace can be lost

Ideas not yet built:
- ZPM effects, Pegasus dial cost and Atlantis travel (ZPM is installed on the reactor; details to hash out)
- Mission log entries for Tel'tak runs
- Later alien tech from levels 3 to 5 fixed-world finds (levels 3 to 5 artifacts are reserved)
- Sol Defense build: DEFCON system, Goa'uld fleet tracker, Sol Defense Status screen (galactic fleet map, time to attack, X-302 and Ion Cannon research states), Tollan and Ancient defense tech; story runs from Level 3 intel to the last Level 4 stronghold (see docs/design/armory-design.md)
- Base upgrades: power reactor, extra rooms, shielding
- Characters and portraits (dropped Oct 22: role icons only, already in game)
- Fuller sound design and music
- Mobile touch layout pass
- Team morale or experience, and linguist-specific contact missions
- Level 5 ending and what the Atlantis address unlocks (second game hook)
- Starmap polish: level-cleared banner
- Opening balance: starting supplies versus the 150-supply first assault (left as is for now)
- Barracks roster swaps and loadouts
- Balance pass on 0.6.12 (Level 1 to 2) done: findings in docs/reports/balance-report-0.6.12.md, tuning decisions pending
- Built 0.6.15: diplomacy for ordinary worlds with raid alerts (see docs/design/diplomacy-design.md). Needs playtest.

- Mobile touch layout (parked): no phone version; a tablet would be an exclusive tablet version, tested on a real device later. See docs/design/backlog-design.md
- Smaller backlog design decisions recorded in docs/design/backlog-design.md (Tel'tak log, level-cleared banner, rescue milestones, linked team groups, vehicle parts, save export/import, portraits, sound, base upgrades with Electrical Station)
- Drone scanning, System Lords per level and FOB resource worlds (designed, not built): see docs/design/drone-scanning-story-design.md. Lords: Apophis, Cronus, Yu, Ba'al, Anubis. FOB Team: Garrison Commander, pooled 10-person security counter, scientist, archeologist, doctor and 2 medics. Number tuning still open.
- 0.8.6 (released Oct 25 2026): opening tour by Hammond and Carter with game pause, Mission Briefing tab on the Operations log (base computer end-of-mission briefs and first-time notes), recon adds +15/+10/+5 points to assault odds. 
- 0.8.7 (built): Tel'tak mission log entries, level-secured starmap banner, CLEARED system marker. 
- 0.8.8 (built): full-width screen fit, Briefing Steps mission panel with tabs, hidden ineligible assets and REPEAT LAST, linked team groups.
- 0.9.0 (built Oct 26 2026, not released): System Lords per level (Apophis, Cronus, Yu, Ba'al, Anubis) as story-only bosses in each system's top stronghold; boss assault x1.1 defenses, x1.5 fee, other strongholds first, drone recon required, spoils on win. Rebuild with tools/build-0.9.0/patch_090.py.
- 0.9.1 (built Oct 26 2026, not released): Forward Operating Bases on captured strongholds (100 supplies; garrison of 10, 100 supplies + 50 RP per 6:30, stockpile cap 1000/500, Tel'tak collection, raids while the lord lives with Defend missions) and uniform buttons across all rooms.
- 0.9.2 (built Oct 26 2026, not released): Serpent's Grasp as battle music (raid alerts, lord assaults) and Evolution in the calm rotation; FOB scientist and archeologist perks (+10 RP, +20 supplies per output); Truck plus Exploration team collects a FOB payout.
- 0.8.10 (built Oct 26 2026, not released): faction lead on every successful Exploration return from a regular world (reveals one unmet faction world, filed as first contact), and a structured Mission Briefing card with outcome badge and labelled fields. Rebuild with tools/build-0.8.10/patch_0810.py.
- 0.8.9 (built Oct 26 2026): rescue record milestones, vehicle parts (Lab research then Motor Pool fitting; Armor, Engine, Cargo, Sensors, 3 levels each) and save export/import (Save Files screen on the title and in Settings). Rebuild with tools/build-0.8.9/patch_089.py. Released to root Oct 26 2026 together with 0.8.7 and 0.8.8; Game Guide refreshed.
- 0.9.4 (built Oct 26 2026, not released): Off-World Operations room for FOBs, Tel'tak supply runs moved to the Quartermaster with an in-game destination list, paged Mission Briefing viewer. Rebuild with tools/build-0.9.4/patch_094.py.
- Proposed: replace the four remaining native drop-downs (mission asset adders, Barracks Loadout, save import) with the in-game list style; Easter eggs tied to the TV series (list sent Oct 26, awaiting picks).
- Hidden worlds (BUILT in 0.9.17 Oct 27 2026, not released; see CHANGELOG; remaining open: reward and odds balance) (decided Oct 26 2026): at least one hidden world in every system. One artifact per hidden world, found by an Exploration team. A Linguist decodes it in the Archeology Office with the existing glyph minigames; the decode reveals the world and its address on the starmap (no partial clues). First decode shows a popup mini-story summary tied to the TV series lore. The cartouche that points to Abydos is a candidate first find. Factions move onto the hidden worlds: faction first contact comes from decoding instead of Exploration faction leads, and diplomacy there makes the worlds Peaceful. Open: reward per world, how existing faction leads (0.8.10) and diplomacy are reworked, which worlds go in which system. See docs/design/hidden-worlds-design.md.


- Minigames in panels (0.9.6): done. Remaining native drop-downs still to replace with in-game lists.

- 0.9.9 (built Oct 26 2026, not released): group editor with pick-from-list membership, teams in several groups, required 5-character tags on teams and groups, tag / mission abbreviation / countdown rows on the dialing computer. Rebuild with tools/build-0.9.9/patch_099.py.

- Released to root Oct 26 2026: 0.9.9 (rolls up 0.9.4 to 0.9.9). Game Guide rebuild pending.
- Picks Oct 26 2026: Easter eggs = Gate address nods and Staff chatter (SG-1 team tag and series-date events not picked). Device-style treatment for Reactor re-route, Glyph decode, Hammond paperwork and Carter explanation (all four picked). New minigames: Brad wants more ideas, mostly for the player to have fun; MALP drive, Infirmary triage, Motor Pool diagnostics and IDC verification not picked yet, ideas list sent.
- 0.9.10 (built Oct 26 2026, not released): Dr. Daniel Jackson replaces Dr. Langford; 25 new Carter questions (40 total). Rebuild with tools/build-0.9.10/patch_0910.py.
- Oct 26 2026: Hide the SGC minigame parked after Brad shelved it (decisions kept in docs/design/easter-eggs-design.md). Staff chatter and gate address nods drafted for approval in the same file.
- Released to root Oct 26 2026: 0.9.11 (rolls up 0.9.4 to 0.9.11), Game Guide rebuilt for 0.9.11. Brad's verdict on the 0.9.5 OS test: good; scope still open.
- Oct 26 2026: Base Computer OS decided: leave versions/sgc-command-0.9.5-os-test.html as a separate test file, not merged. Note: it was built on 0.9.4, so any future merge means rebuilding on the current build.
- Oct 26 2026: Device-style treatment order decided: Reactor re-route first (then glyph, Hammond, Carter). Brad supplies reference photos (main panel, input controls, display, gauges and lamps); waiting on photos for the reactor.
- Oct 26 2026: reactor device puzzles picked (conduit Sudoku, three-knob balance, pipe routing, breaker sequence, phase match, load shedding); Brad wants mixed multi-stage puzzles. Notes in docs/design/reactor-device-design.md.
- Oct 26 2026: reactor device fixed pairs approved (see docs/design/reactor-device-design.md). Next: layout pass, then build as 0.9.12.
- Oct 26 2026: reactor tablet built as 0.9.12 (not released). Next: glyph decode console, then Hammond binder desk.
- Oct 26 2026: glyph decode console built as 0.9.13 (not released). Next: Hammond binder desk. Brad wants a minigame showcase HTML file once all minigames are finalized (one page with every minigame playable standalone).
- Oct 26 2026: Hammond binder desk built as 0.9.14 (not released). Device minigames done. Open: new-minigame picks, then the minigame showcase HTML.
- Oct 26 2026: Brad supplied reference pictures for glyph decode and Hammond paperwork; Carter stays simple. Designs in docs/design/device-minigames-design.md.
- Oct 26 2026: device build order reactor (0.9.12), glyph, Hammond; Hammond uses binder tabs; lord symbols as decode bonus.

## Minigame update (cancelled Oct 28 2026)
- Tel'tak asteroid run (0.9.20) and Raid defense (0.9.21) were built, then removed by Brad in 0.9.22. Dig site brushwork and Mess hall card night are dropped. The earlier minigames (reactor, glyph, Hammond, COMM, drone) stay. Design notes remain in docs/design/minigames-design.md.
- Minigame showcase built (sgc-minigame-showcase.html); add each new minigame to tools/showcase/sc.js when it ships.
- Balance pass on 0.9.14 (Levels 1 to 5) done Oct 27 2026: findings in docs/reports/balance-report-0.9.14.md, tools in tools/balance-sim (bot2.js, run2.js, an5.py). Nothing in the game changed; tuning picks A to G pending.
- 0.9.15 (built Oct 27 2026, not released): balance pass tuning E, C, B, D from docs/reports/balance-report-0.9.14.md (Reactor I 600 RP, Level 4 second stronghold, Level 4/5 defense 65/80 with ATV bonus 0.02 per tier, raid stockpile loss, Truck 250/125, Tel'tak cap 400/200, FOB upkeep 15, FOB replacement at SGC cost). Picks A, F, G still open. Guide not rebuilt.
- 0.9.16 (built Oct 27 2026, not released): FOB roles (Supply depot, Research outpost, Power relay), escalating upkeep 15 + 5 per base, Tel'tak fuel ceil(ly/4) naquadah, FOB role save fix. Open: Level 5 odds slightly under 65% target (retune?), release 0.9.15/0.9.16 to dist, rebuild Game Guide, balance picks A, F, G.
- 0.9.22 (built Oct 28 2026, RELEASED Oct 28 2026): asteroid run and Raid defense removed; build is 0.9.19 content. Raid alerts back to Defend mission or garrison alone.
- Released to root Oct 28 2026: 0.9.22 (rolls up 0.9.15 to 0.9.22), Game Guide rebuilt for 0.9.22 (38 pages), showcase rebuilt, tagged v0.9.22. Open: balance picks A (assault cooldown), F (gear costs), G (extend bot to MALP tiers, vehicle parts, minigame income); Level 5 retune; hidden-world reward values and find odds; outpost numbers; Off-World Operations unlock timing.
- 0.9.23 (built and RELEASED Oct 28 2026): assault cooldown 15 minutes on every level (pick A). Pick F left as is, pick G skipped. Level 5 retune checked and not needed (30 sessions: 66% win against the 65% target). Hidden-world and outpost numbers confirmed. To release: copy to dist, archive 0.9.22, rebuild showcase, update the Game Guide quick reference (20 to 15 minutes), commit and tag v0.9.23.
