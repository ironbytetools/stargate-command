# Stargate Command - Changelog (was build-status.md)

Folder layout changed Oct 27 2026: versions/ is now builds/, releases moved from the root to dist/, tools/build-X became tools/patches/build-X, tools/guide-build became tools/guide, tools/audio-build became tools/audio, mockups/ and Game Soundtrack/ moved under assets/, roadmap.md became ROADMAP.md and build-status.md became CHANGELOG.md. Entries below keep the paths as they were when written.

## 0.9.4 (BUILT Oct 26 2026, not yet released): Off-World Operations room, Tel'tak in the Quartermaster, paged mission briefs

File: versions/sgc-command-0.9.4.html (built from 0.9.3, 21.7 MB, md5 40fa885d...). Rebuild: python3 tools/build-0.9.4/patch_094.py versions/sgc-command-0.9.3.html versions/sgc-command-0.9.4.html

Brad's requests and decisions: end-of-mission brief uses the whole panel with back/forward paging; Tel'tak interface moves to the Quartermaster with a more direct supply-run flow; FOB manager moves out of the Quartermaster (he chose a new room); no OS drop-downs, everything styled in-game.

Changed:
- New room "Off-World Operations" (card label LEVEL 22, my number) holds the Forward Operating Base manager: active bases on the left, available sites and help on the right. The card appears once any stronghold is captured or a base exists (my reading of the recommended option). Card shows bases active or RAIDS INBOUND. Raid alert chips still point to the Briefing Room (Defend missions are planned there).
- Tel'tak ships leave the Armory (its Tel'tak tab is gone; Armory shows equipment only) and live in the Quartermaster under Air Force Logistics. Each ship row: status and SEND button, then a Destination button that opens an in-game list of explored worlds and FOBs (distance, round trip, hazard and supply yield, or FOB stockpile) with SELECT buttons. No native drop-down. A ship remembers its last destination. Restored wrecks are put in service from the same panel. The Quartermaster card shows Tel'tak ready / total; the active-run chip now opens the Quartermaster.
- Quartermaster layout: Stores, Air Force Logistics and Tel'tak Supply Runs stack in the left column; Reactor on the right.
- Mission Briefing tab: shows one brief at a time with BACK (older) and NEXT (newer) buttons and a BRIEF n / total counter. Opens on the newest; a new brief arriving while you read an older one keeps your place. Panel is taller (290 px in the Facility view; fills the row in the Gate Room view).
- Tutorial note FB1 now says Off-World Operations.

Verified (headless Chromium on the build with audio stripped, same code as the shipped file: stripped md5 matches): zero script errors; every room and tab, plus Quartermaster list open, Briefing tab in both views, at 1440x900, 1024x700 and 1920x1080: 0 covered, clipped or overflowing controls (audit confirmed to flag deliberately broken CSS); real-mouse flow in the Quartermaster (put in service, choose destination, select, send); fee paid, return yield matches the world's roll, destination remembered; FOB pickup returns the full stockpile; ops card hidden before first capture and shown after; brief paging, place kept on new brief, 60-brief cap.

Not verified: Brad's screenshot did not arrive, so the brief panel size is my reading; real playback and Safari; old save loaded from a 0.9.3 file (no schema change, new ship field falls back when missing); Game Guide not rebuilt (still 0.9.3 text: Tel'tak and FOB locations are out of date there).

Open: four native drop-downs remain (mission panel ADD TEAM / VEHICLE / MALP, Barracks Loadout, save import slot); Easter egg list sent to Brad for picks.

## RELEASE Oct 26 2026: root is now 0.9.3

sgc-command.html (+ .zip) is 0.9.3. versions/ holds sgc-command-0.9.3.html; 0.9.2 moved to versions/archive/. Game Guide rebuilt for build 0.9.3 (33 pages). Rebuild: python3 tools/build-0.9.3/patch_093.py <0.9.2 file> <out>.

0.9.3 changes (Brad's requests):
- Briefing Room and Barracks no longer show the on-station staff strip (names and role icons) above the room panel. The Lab, Infirmary and Archeology Office keep theirs.
- A Tel'tak on a supply run now appears on the starmap as a small gold arrow, in both the galaxy chart and the system view, with a faint dashed route. It points outbound, turns around at halfway for the return leg, and is gone on return. A delayed ship waits at the Sol end. Hover shows the ship name and destination. Works with FOB pickup runs too.
- Tests: new check script (strip removed in Briefing and Barracks, kept in Lab/Infirmary/Archeology; icon present in both views, moves, flips, disappears on return), plus FOB 34/34, music/perks/truck 10/10, text-fit 0 issues at 1440/1024/1920, whole-game clip/cover audit 0 issues, real-mouse clicks 40/40.

## RELEASE Oct 26 2026: root is now 0.9.2

sgc-command.html (+ .zip) is 0.9.2 and rolls up 0.8.10, 0.9.0, 0.9.1 and 0.9.2. versions/ holds only sgc-command-0.9.2.html; 0.8.9 to 0.9.1 are in versions/archive/. Game Guide rebuilt for build 0.9.2 (33 pages): faction leads, end-of-mission briefing, System Lords, Forward Operating Bases, Tel'tak and Truck collection, new music. README current build line updated.

Correction to 0.9.1/0.9.2 button pass: the first uniform-button change clipped the left side of buttons in Lab rows (Armory, Alien Tech, Vehicle Parts and others), because the button's wrapper span has overflow hidden and shrank. Fixed in 0.9.2 (wrapper no longer shrinks or clips; the CSS rule had lost on specificity). My earlier audit measured positions only and missed it. The audit now checks that every button is reachable at its left, centre and right points (nothing covering or clipping it) across every room and every tab at 1440x900 and 1024x700, plus the title, Gate Room, mission steps and menu; the new check flags the old file and passes the new one. FOB panel spacing and staff line alignment also tidied.

Housekeeping: tools/guide-build/build_guide_089.py.bak is a leftover backup that could not be deleted (delete is off); safe to remove by hand.

Addendum (final 0.9.2, md5 ca3021d0...): mission panel on the Gate Room no longer loses clicks (panel was rebuilding every tick and while the mouse was pressed; rebuilds are now skipped when nothing changed and deferred during a press; real-mouse test 40/40 vs 20/40 before). Minigame and overlay buttons centred and uniform, Settings/overlay top no longer cut off on short screens, labels SAVE FILES / RESET DEFAULTS. Root release refreshed with this build.

## 0.9.2 (BUILT Oct 26 2026, not yet released): new soundtrack, FOB staff perks, Truck collection

File: versions/sgc-command-0.9.2.html (built from 0.9.1, 21.7 MB). Rebuild: python3 tools/build-0.9.2/patch_092.py versions/sgc-command-0.9.1.html versions/sgc-command-0.9.2.html tools/build-0.9.2/serpent.mp3 tools/build-0.9.2/evo.mp3

Brad's decisions: music plus FOB staff perks; a Truck sent with an Exploration team to a FOB collects like a Tel'tak.

Changed:
- Music: "Within The Serpent's Grasp (Suite)" plays as a new battle mode during any raid alert and while a team is out on an assault on a System Lord stronghold (held at least 20 s, like the tense mode). "Evolution (Unreleased)" joins the calm rotation (Emancipation, Hathor, Evolution). Both re-encoded to 80 kbps and embedded; file grows 12.8 MB to 21.7 MB.
- FOB staff perks: scientist adds 10 RP and archeologist adds 20 supplies to each output (so 120 supplies and 60 RP per 6:30; base 100/50 unchanged).
- Truck collection: an Exploration team with a Logistic Truck sent to a FOB world is now allowed (the Exploration block on captured strongholds lifts for that case) and collects one payout (120 supplies, 60 RP) from the stockpile; without a truck the send is blocked with a message naming the truck. That trip gives only the haul, no normal exploration loot, so it cannot be farmed.

Verified (headless Chromium, zero script errors): both tracks embedded and decode; mode logic (calm / battle on raid alert / calm after); calm rotation order; perk output 120/60; truck haul and mission yield; no truck blocked with stock untouched; all 34 FOB checks and the every-room text-fit audit at three sizes rerun on this file.

Assumptions (mine):
- Perk sizes (+20 supplies, +10 RP) and one-payout truck haul are my numbers; doctor and medics keep the existing healing role.
- Not auditioned: I did not hear the tracks, so mapping them to battle and calm is by title and length (8:45 and 2:23).

Not verified: actual playback and fades in a browser with sound, Safari, load time with the larger file.

Open action items:
- Listen to the new tracks in play and say if either belongs elsewhere.
- Play 0.8.10 to 0.9.2; then release to root with the Game Guide refreshed.

## 0.9.1 (BUILT Oct 26 2026, not yet released): Forward Operating Bases and uniform buttons

File: versions/sgc-command-0.9.1.html (built from 0.9.0). Rebuild: python3 tools/build-0.9.1/patch_091.py versions/sgc-command-0.9.0.html versions/sgc-command-0.9.1.html

Brad's decisions: stockpile cap 1000 supplies and 500 RP; timed raid checks with the garrison fighting back; output 100 supplies and 50 RP per interval. Mid-build request: interactive buttons must be uniform and aligned throughout the game.

Changed:
- FOB: any captured stronghold can host one from the Quartermaster room (new "Forward Operating Bases" panel under Air Force Logistics) for 100 supplies. Staff: Garrison Commander, scientist, archeologist, doctor, two medics (named; scientist/archeologist have no perks yet) plus a pooled counter of 10 security personnel.
- Output 100 supplies + 50 RP every 6:30 into a stockpile capped at 1000 / 500 (production pauses when both are full, with a log line).
- Collection: Tel'taks can be sent to a FOB world (picker shows the stockpile); on arrival the whole stockpile is loaded, on return supplies and research are paid and shown in the mission log.
- Raids: while the level's System Lord lives, a check every 15:00 with 30% chance raises a RAID alert (2:00); a Defend mission answers it as before. Unanswered: garrison fights alone. Garrison of 6+ fit loses 0 to (2 + floor((level-1)/2)); below 6 loses 2 to 5. Losses 70% wounded, 30% killed. Wounded heal 1 per 2:00; killed replaced for 15 supplies each (REPLACE button). If no fit defender remains, the base is overrun, the stockpile is lost and the stronghold reverts to hostile (must be assaulted again). Shields can absorb a raid as for treaties.
- When the lord falls, raids on that system's FOBs end for good (message in the spoils line). RECALL BASE (two-click confirm) abandons a base and its stockpile.
- FOB badge on the world, one new SGC briefing (FB1) on the first captured stronghold, saves carry FOBs (old saves load with none).
- Buttons: every action button inside a row (staff, resource, dispatch) is now one size (230 wide, same height and font), right aligned; gear selects match; standalone control buttons use the same size and align left; mission panel BACK/NEXT/REPEAT/SEND share one size. Lab labels shortened to "RP // SUP // time" (the row already names the tier) and CONVERT NAQUADAH is now "NAQUADAH +15 POWER" so nothing shrinks its text.

Verified (headless Chromium, zero script errors): 34 FOB checks (establish, cap, Tel'tak load and pay, alert, Defend answered, unanswered losses, healing, replace, overrun, lord fall stops raids, save round trip, old save); button size census (one size per row type) and the text-fit audit on every room and tab at 1440x900, 1024x700, 1920x1080; earlier suites rerun on this file (only version-string and known test-bug failures).

Assumptions (mine):
- Raids hit only the security counter; the named staff are never lost.
- Defend mission against a FOB uses the existing mission (no extra cost or risk) and resets the raid timer.
- A recalled or lost FOB loses its stockpile.
- At 920 supplies/hour per FOB the economy shifts a lot; the Tel'tak trip count is the throttle. Watch balance in play.

Not verified: real playthrough balance, FOBs on Levels 4 and 5, Safari, the Gate Room dial pad buttons were left as a deliberate console (not changed).

Open action items:
- Brad plays 0.8.10, 0.9.0 and 0.9.1; release to root with the Game Guide refreshed (faction lead, briefing card, System Lords, FOBs).
- Confirm earlier assumptions: Armor III free repair, part research times, guaranteed faction lead, boss spoils scale.

## 0.9.0 (BUILT Oct 26 2026, not yet released): System Lords and boss assaults

File: versions/sgc-command-0.9.0.html (built from 0.8.10). Rebuild: python3 tools/build-0.9.0/patch_090.py versions/sgc-command-0.8.10.html versions/sgc-command-0.9.0.html

Brad's decisions: lords are story-only while alive (no level-wide effect); boss assault is harder, pricier and recon-gated; SGC briefing names the lord on arrival and the stronghold shows his name at intel tier 2.

Changed:
- One lord per system: Apophis (Level 1), Cronus (2), Yu (3), Ba'al (4), Anubis (5). He holds the system's highest-difficulty stronghold (ties go to the last), tagged at world creation and added to existing saves on load.
- Boss assault rules: defenses x1.1 (capped at 100), assault fee x1.5 (225 at Level 1), cannot be sent until every other stronghold in the system is captured or under treaty, and needs a drone recon flown on that stronghold first (the existing DRONE key; spent when the assault is sent, as before). The send panel states which condition is missing.
- Win: +100 supplies and +200 research points per level number (L1 100/200 up to L5 500/1000), "<Lord> has fallen. Spoils: ..." in the Operations log, mission log and mission result; the LEVEL SECURED banner reads "<Lord> has fallen."
- Starmap and world panel: SYSTEM LORD: <NAME> badge on the stronghold from intel tier 2, changing to <NAME> DEFEATED once captured.
- Five SGC briefings (one per lord, filed when the system unlocks; existing games get the ones for levels already reached) naming him, a line of character and the boss conditions.

Verified (headless Chromium, full file, zero script errors): one lord per level with the right name on the highest-difficulty stronghold across all five systems; fee 150 -> 225 and difficulty 15 -> 16.5; recon requirement blocks and releases; a two-stronghold system blocks the lord until the other falls; boss win pays 100/200, logs the fall, badge flips to DEFEATED, banner names him; briefings filed for levels 1 and 2; an older save without lords gets them on load; 0.8.9/0.8.10 regression suites (vehicle parts, save files, faction lead, briefing card) pass.

Assumptions (mine):
- Spoils scale 100 supplies and 200 research points times the level number; the fee, difficulty and recon numbers are the ones Brad picked.
- Lord character lines are short originals and not tied to the show's scripts.
- The treaty exception that lets the last stronghold be reached applies to the lord too: a stronghold under treaty does not block him.
- Existing saves: the lord is the highest-difficulty stronghold even if it was already captured, in which case the lord counts as fallen.

Not verified: Levels 3 to 5 in a real playthrough (spawned in a test, not played), balance of the boss odds against real teams, Safari.

Open action items:
- Brad plays 0.8.10 and 0.9.0; release to root with the Game Guide refreshed (return-log faction lead, briefing card, System Lords).
- Next candidate: FOB resource worlds (needs lords in place, now done).

## 0.8.10 (BUILT Oct 26 2026, not yet released): faction leads on Exploration returns, structured end-of-mission briefing

File: versions/sgc-command-0.8.10.html (built from 0.8.9). Rebuild: python3 tools/build-0.8.10/patch_0810.py versions/sgc-command-0.8.9.html versions/sgc-command-0.8.10.html

Why: Brad was on Level 2 and had not met a faction world, and the end-of-mission briefing read as one paragraph. Cause of the first: world kinds stay hidden until visited, and the final-stronghold unlock only asks for 75% of the non-stronghold worlds, so the faction world is easy to skip entirely (Level 1's Langaran included).

Changed:
- Faction lead: every successful Exploration return from a regular world reveals one unmet faction world (lowest level first, levels up to the current one) and says so in the return text, Operations log, mission log and briefing: "On <world> the team met <Faction> traders, who gave the address of their home world, <world>. The <Faction> are now on the Faction Relations list." The faction world becomes intel 2 (faction badge on the starmap, Diplomat mission unlocked) and first contact is filed as before. Failed or injured explorations give no lead. Systems with two faction worlds reveal them on successive returns. A direct visit to a faction world still works as before.
- Mission Briefing card: header with an outcome badge (CLEAN, AMBUSHED, INJURIES, OVERDUE, CASUALTIES), then labelled fields: TEAM and WORLD, RESULT (the summary sentence only), YIELD and INTEL, INJURED and LOST (or one PERSONNEL line when none), FINDS (artifacts, inscriptions, faction contact, recovered items, thermal mapping), AAR hint. Old briefings in existing saves keep their old text.

Verified (headless Chromium, full file, zero script errors): first regular-world Exploration return reveals the faction world, files first contact, lists it in Faction Relations; second return gives no repeat; briefing card for a clean mission and a mission with injury, loss, artifact and faction contact (fields land in the right rows); 0.8.9 regression suites (vehicle parts, save export/import, text-fit audit) rerun on this build with zero failures.

Assumptions (mine):
- The lead is guaranteed on the first successful return, not a chance. Easy to change to a probability if you want it less certain.
- Existing games benefit immediately: a Level 2 game with the Level 1 faction still unmet gets that world first.
- Result sentences are sorted into RESULT or FINDS by keyword; an unusual sentence could land in RESULT.

Not verified: a long real playthrough, the briefing on assault, recon and assist missions beyond the shared card code, Safari.

Open action items:
- Brad plays 0.8.10 (not yet in root; Game Guide and root release come with the next release).
- Pick the content of 0.9.0.

## 0.8.9 (RELEASED Oct 26 2026, current release): rescue record milestones, vehicle parts, save export/import

File: versions/sgc-command-0.8.9.html (built from 0.8.8). Rebuild: python3 tools/build-0.8.9/patch_089.py versions/sgc-command-0.8.8.html versions/sgc-command-0.8.9.html

Changed:
- Rescue record milestones per team (docs/design/backlog-design.md): tiers at 1 / 3 / 6 / 10 / 15 assists performed, titles Rescuer, Lifeline, Guardian, Sentinel, Angel of the Gate. Crossing a tier pays 25 / 50 / 75 / 100 / 150 supplies plus equal research points at once, logged and written to the assist mission's log entry. Assist travel -5% per tier, applied after the COMM 1 accuracy band; a mixed assist group uses its highest-tier team. Barracks Team details shows count, title, travel bonus and next tier.
- Vehicle parts: Armor, Engine, Cargo (Truck, ATV) and Sensors (Drone). Shared per vehicle type, 3 levels each. Each level is researched in the Lab (new VEHICLE PARTS tab: 75 / 150 / 225 RP + 25 / 50 / 75 supplies, 3 / 6 / 9 minutes, Lab tier discounts and Carter apply) and then fitted in the Motor Pool (25 / 50 / 75 supplies, new Vehicle parts section on each vehicle tab). Next level can be researched only after the previous one is fitted.
- Part effects per level: Cargo +5% yield; Engine mission time -10% ATV, -5% Truck and Drone; Sensors -3 ambush points; Armor repair time -33% and failed-assault vehicle loss -8 points (25% -> 17 / 9 / 1%). Armor III makes repairs free and instant, and ambush damage is repaired on return at no cost. Parts show in the vehicle bonus lines, mission builder and mission log through the existing vehicle effect totals.
- Save export/import: new SAVE FILES screen on the title screen and in Settings. Export any one slot or all four (autosave plus three manual) to a .json bundle; the in-progress game is autosaved first so the autosave export is current. Import a bundle or a single save: each save gets a destination dropdown limited to empty slots (same-name slot proposed first), saves from a newer build are blocked with the reason shown, earlier builds and pre-0.8.9 saves are accepted and flagged UPGRADED ON LOAD, incomplete or non-save files are rejected, two saves aimed at one slot import nothing, and an occupied slot is never overwritten. Saves now carry the build number.
- Saves: vehicle parts and in-flight parts research save and load. Older saves load with all parts at 0.

Verified (headless Chromium, full file, zero script errors): rescue tiers and payouts and travel time; every part effect on the vehicle totals; research/buy cost and duration per level, sequencing, no fourth level, duplicate research blocked; armor repair time, cost and loss odds at 0 / I / II / III; free repair path and auto-repair on ambush return; save/load round trip of parts and an in-flight parts project; an old save with no parts or build number loads; export of one slot and all four (file name, bundle shape, autosave current); import into full slots proposes nothing, into freed slots lands same-name, label rewritten, imported save resumes; newer build blocked, older and pre-0.8.9 accepted, incomplete, junk and non-JSON files rejected; duplicate and occupied targets protected; Esc closes the screen. Text-fit audit (clipped, off-screen and out-of-panel elements) on the title screen, Save Files screen (empty, in game, with import list), Settings, Lab VEHICLE PARTS tab and all three Motor Pool tabs at 1440x900, 1024x700 and 1920x1080: zero findings after the Lab rows were restructured (effect text on its own line). Screenshots reviewed.

Assumptions (mine):
- A mixed assist group travels at the best rescuer's bonus; Special Ops rescue units do not earn titles.
- "Free at III" for Armor read as no supplies and no time; ambush damage on a vehicle with Armor III is repaired on return rather than left damaged.
- Lab research times for parts (3 / 6 / 9 minutes) were not in the design; chosen to sit between MALP tier 1 and 2.
- A part must be fitted before the next level can be researched.
- Import of a save into the autosave slot is allowed only while that slot is empty (a running game refills it every 10 seconds).

Not verified: the browser download prompt on Safari and Firefox (tested in Chromium only), a real 12 MB file picked through the OS file dialog, real-time lab timers end to end (completion triggered directly), sound.

Release (Oct 26 2026): Brad played 0.8.7 to 0.8.9 and cleared them. Root sgc-command.html and sgc-command.html.zip are now 0.8.9; 0.8.6, 0.8.7 and 0.8.8 moved to versions/archive/. Game Guide rebuilt for build 0.8.9 (31 pages): save files, linked groups, three-step mission builder, rescue record, Tel'tak log tab, LEVEL SECURED and CLEARED, vehicle parts. Source: tools/guide-build/build_guide.py.

Open action items:
- Confirm or correct the assumptions above, mainly Armor III and the lab times.
- Pick the next build from the roadmap.

## 0.8.8 (RELEASED Oct 26 2026 with 0.8.9): full-width screen fit, Briefing Steps mission panel, linked team groups

File: versions/sgc-command-0.8.8.html (built from 0.8.7). Rebuild: python3 tools/build-0.8.8/patch_088.py versions/sgc-command-0.8.7.html versions/sgc-command-0.8.8.html

Changed:
- Screen fit fills the window width: scale worked out at the 1500 px design width exactly as in 0.8.5 (same text size), then the stage widens to the full window. Dialing computer and starmap held at design size, centered in their panels; logs, mission panel and Facility panels stretch.
- Mission panel is now three steps (option C): 1 TYPE (six type cards with a one-line rule), 2 ASSETS (TEAMS / VEHICLES / MALPS tabs, only assets that can go on the chosen type and are on station are listed), 3 REVIEW (type, destination, teams, vehicles, MALP, odds and cost note, SEND). BACK / NEXT in the footer with a running count. Gate status and the overdue section stay above the steps. Dropdowns removed.
- REPEAT LAST on step 1: reloads the last send (type, teams, vehicles, MALP), drops anything not available and lists it, and jumps to REVIEW.
- Linked team groups (Barracks, under the Teams list): NEW GROUP, JOIN <group>, UNLINK, rename; on station only; one group per team; no cap. Default name "<lead type> Team N". In step 2 a ready group shows as one GROUP row that adds all its teams; other teams, vehicles and a MALP can be added alongside. A group is listed only when every member is ready and eligible for the type; when broken, its ready members show as individual teams.
- Saves: groups, last mission. Older saves load with no groups.

Verified (headless Chromium, full file, zero script errors): group create and join; step 2 shows the group plus an unlinked team; group + team + MALP sent as one mission; last mission saved and REPEAT LAST reloads 3 teams + MALP into REVIEW; with a member away the group splits into individual teams; Gate Room stage height unchanged (1119); no scroll at 1600x950, 1366x768, 2560x1080, 1280x1024.

- Default group name is now "<lead type> Group N" (e.g. Exploration Group 1).
- Text fit pass across the game: titles, card labels, room-card headers and status lines, staff and stat rows, badges, buttons and panel headings are single line. Anything that does not fit is shrunk (75% floor) instead of wrapping or running out of its box, and labels of one kind in one set (room titles, a row of tab cards, mission type cards) shrink together so they stay the same size. Tab card rows need 118 px per card before flowing to a second row (Gate Room tiers now 5 + 2). Facility room column 214 -> 240 px. Room titles letter-spacing 0.13em. Top nav no longer wraps; the active-missions strip scrolls sideways. Quartermaster card shows SUPPLIES only (power is in the header).
- Text fit verified by an automated audit (tools/build-0.8.8 is the patch; the audit runs every room, every tab card and every mission panel step with research, upgrades, vehicles, groups and an away team active) at 1366x768, 1600x950, 1920x1080, 2560x1080: zero overflow, wrapped titles, clipped labels or uneven card sets; one panel heading style game-wide.

Not covered by the audit: minigame screens, drone flight, title screen, tour card. They get the same global rules (buttons, headings, badges) but were not walked.

Assumptions (mine):
- Groups appear only in step 2's TEAMS tab; the assist SEND ASSIST button in the overdue section still uses the teams added in step 2.

## 0.8.7 (RELEASED Oct 26 2026 with 0.8.9): backlog bundle - Tel'tak log, level-secured banner, CLEARED marker

File: versions/sgc-command-0.8.7.html (built from 0.8.6). Rebuild: python3 tools/build-0.8.7/patch_087.py versions/sgc-command-0.8.6.html versions/sgc-command-0.8.7.html

Changed:
- Tel'tak supply runs get mission IDs and a new TEL'TAK tab in the mission log. Detail shows ship (with which wreck it came from), destination, launch and end times, flags (delayed), supplies returned, and timestamped events: departure, arrival at the world (halfway through the round trip), delay, return.
- Starmap banner when a level's final stronghold falls: "<STAR> // LEVEL N SECURED" with the next system named, shown over the map until ACKNOWLEDGE. Once per level per game, saved.
- CLEARED marker: green ring and check on the galaxy chart, and "// CLEARED" in the system header, while every world in the system is Peaceful. A one-time log line when a system first clears.
- Saves: banners, pending banner and cleared systems saved; older saves load with already-cleared systems recorded silently.

Verified (headless Chromium, full file, zero script errors): Tel'tak run creates M-0001 with all events and 100 supplies; capturing all Level 1 strongholds with treaties on the rest shows the banner, unlocks Level 2, logs CLEARED and draws the marker.

Assumptions (mine):
- CLEARED is live: if a Goa'uld raid breaks a treaty, the marker drops until peace returns (the log line fires only once).
- The Ancient Lab and Ancient research ship count toward CLEARED once explored, since they can never become Peaceful otherwise.
- Tel'tak runs get no base computer briefing or AAR.

## 0.8.6 (RELEASED Oct 25 2026, superseded by 0.8.9): opening tour, Mission Briefing tab, recon odds bonus

File: versions/sgc-command-0.8.6.html (built from 0.8.5); root sgc-command.html is 0.8.6. All older builds moved to versions/archive/. Rebuild: copy versions/archive/sgc-command-0.8.5.html to tools/build-0.8.6/base086.html, run patch_086.py (writes out086.html). Design text: docs/design/tour-cards.md. Intermediate copies are in _to_delete/build-0.8.6-temp.

Changed:
- Opening tour on every new game (not on resume or load): 8 cards, General Hammond and Colonel Carter alternating, with a highlight on the screen element each card is about. NEXT, SKIP TOUR, Enter or Space for next, Escape to skip. MENU has a TOUR button that replays it.
- Game time pauses while the tour is open: the clock, mission and healing timers, power regeneration, the wormhole and all scheduled events freeze and resume where they left off. The soundtrack keeps playing. Done with a paused game clock (Date.now and performance.now), a pause-aware timer list behind later(), and a guard on interval callbacks; PAUSE.pause and PAUSE.resume are available for any later takeover screen.
- Operations log panel now has two tabs, OPERATIONS LOG and MISSION BRIEFING, on both the Facility and Gate Room screens. A NEW count shows unread briefings.
- Mission briefing from the base computer whenever a mission closes: team names, world, result, yield, intel change, injured, killed or captured, and an OPEN MISSION LOG button (plus a note when an After-Action Report is available).
- Base computer notes filed once per game on the same tab, as drafted in tour-cards.md sections B to D (first destination, wormhole, return, injury, incoming wormhole, stronghold, research, Armory, Motor Pool, faction, logistics, level cleared, COMM 1, drone, power event, inscription, Briefing Room, Science Lab, After-Action Report).
- Recon now adds points to final assault odds: all contacts tagged +15, 70% or more +10, 40% or more +5, under 40% none. Spotted halves the bonus (rounded down: 7, 5, 2) and keeps the -10 alert penalty. This replaces the old difficulty reduction, which was tiny at low levels. Drone result screen, log line and the assault note show points.
- Saves: tourDone, briefs, seen notes and the unread count are saved. Older saves load with the tour marked done and every note marked seen, so they do not replay or flood the tab.

Verified (headless Chromium on a slim copy with the music data blanked, zero script errors): tour shows on a new game and pauses the game (clock delta 0 over 1.5 s, a timer set during the tour fires only after it ends); all 8 cards step through with the right titles and the last card shows DONE; Menu TOUR replays and Escape skips; first-destination note and a mission briefing post, the tab shows 3 NEW, switching tabs clears it, OPEN MISSION LOG opens the Briefing Room log; odds 45.33% with no recon, 60.33% at +15, 42.33% with a spotted drone (+7 and -10); save and load round trip.
Not verified: the full 12.7 MB file in a browser, Safari and Firefox, touch, a full real playthrough triggering every note, pausing under a long tour with a wormhole open, sound by ear.

Assumptions (mine):
- Event notes go to the Mission Briefing tab instead of popups, because you said the only popup would be the tour. D1 and D2 are filed when COMM 1 or the DRONE key is pressed (not before the flight starts). D5 and D6 are filed the first time the Briefing Room or Science Lab is opened.
- Minigames and the drone keep their existing rule that the wormhole timer keeps running; only the tour pauses the game.
- The tab sits on the one shared Operations log panel, so it also appears on the Facility screen.
- Tour card text is the version you approved, with card 7 reworded to point at the MISSION BRIEFING tab instead of a Settings toggle.

Open action items:
- Play 0.8.6: check the tour reads well and the briefing tab is where you want it.
- Next: undecided.

## 0.8.5 (RELEASED Oct 25 2026, superseded by 0.8.6): drone spotting tuning, Menu consolidation, fit-to-display scaling

File: versions/sgc-command-0.8.5.html (built from 0.8.4). Released to root Oct 25 2026. Rebuild: in tools/build-0.8.4, run make_engine.py on mockups/ui/comm1-mockups.html, copy versions/sgc-command-0.8.3.html to base.html, run patch_084.py (out.html), copy out.html to base085.html, run patch_085.py (out085.html).

Changed:
- Drone spotting made achievable (Brad picked all four options): exposure builds about half as fast (0.05 + 0.10 x speed + 0.06 x altitude per second, was 0.10 + 0.20 + 0.12), so about 20 to 25 seconds hovering low inside a cone (was about 10); recovery outside the cones doubled (0.30 per second, was 0.15); every defender view range cut 25% (towers 100 to 75 m, guards 70 to 52 m, patrols 75 to 56 m); a tier 0 drone now sees defenders (105 to 150 m thermal) well before it enters their cones.
- New warning before you are seen: approaching within 1.35 times a defender's range of its view cone (and near its facing) shows an amber DEFENDER NEARBY on the feed, reveals that defender's wedge on the radar, and ticks every 0.8 seconds. The existing red IN DEFENDER VIEW and exposure bar are unchanged.
- Header now carries only MENU. SETTINGS, HELP, SOUND and FULL SCREEN moved into an Options block at the top of the Game Menu (same buttons, same behavior and keyboard shortcuts f and s). The Menu's own SETTINGS button was removed to avoid a duplicate. Title-screen Settings is unchanged.
- Fit-to-display scaling on the Gate Room and the Facility: the whole screen (header, tabs, panels, log) is laid out at a fixed 1500 px design width and scaled uniformly to fit the window (minimum 0.6, maximum 1.6), centered with side margins on wide windows. Gate Room fills the window height with no scrolling at 1500x950, 1920x1080, 1366x768, 1440x900 and 2560x1440 (scale 0.85, 0.97, 0.69, 0.80, 1.29). Facility scales by the same rule from a 1000 px reference height and scrolls if a room panel is taller. Overlays (title, menu, settings, radio and drone screens) are not scaled.

Assumptions I made that were not explicitly decided (flag any that are wrong):
- Scaling rule: uniform scale from a fixed design size with a 0.6 floor, rather than reflowing to the window width. The gate computer keeps its proportions and wide windows get side margins (reflowing wider made the dialing computer taller and shrank everything).
- Facility reference height is 1000 px; taller room panels scroll instead of shrinking the whole screen again.
- The warning radius (1.35 times range, 0.3 rad past the cone edge) and tick rate are mine.
- This is 0.8.5, so the tour and briefing-card popups move to 0.8.6.

Verified (headless Chromium, zero console errors, on a copy with the music data blanked out; gameplay code identical): header shows only MENU; Menu lists Settings, Help, Sound, Full Screen plus saves; Sound toggles the mute state, Help toggles the help class, Settings opens from the Menu; Gate Room and Facility fit with no scroll at five window sizes; a starmap world click selects the world under the scaling; exposure after 3 s at rest low inside a guard cone is 0.124 (about 24 s to spotted); exposure drains to 0 in 1.5 s behind the guard; warning flag set 1.15 times range ahead of a cone with no exposure; screenshots reviewed at 1920x1080, 1440x900 and the Menu.
Not verified: the full 12.7 MB file in a browser (test copy only differs in the embedded music), Safari and Firefox scaling, touch layouts, the music and sound by ear, drone feel at the new spotting numbers (your call), fullscreen mode with the scaling, window resize while a minigame overlay is open.

Open action items:
- Play 0.8.5 and say whether the spotting numbers feel right.
- Check the Gate Room and Facility scaling on your own display, especially text size on a smaller window.
- The recon strength effect at low levels (0.8.4 finding) is still open.
- 0.7.5 and 0.8.0 to 0.8.5 are not yet released to root.
- Next planned: 0.8.6 tour and briefing-card popups.

## 0.8.4 (BUILT, awaiting Brad's review): Reconnaissance Drone replaces the COMM 1 triangulation

File: versions/sgc-command-0.8.4.html (built from 0.8.3). Not yet released to root. Rebuild: in tools/build-0.8.4, run make_engine.py on mockups/ui/comm1-mockups.html (writes drone-engine.js plus its .css and .html), copy versions/sgc-command-0.8.3.html to base.html, then run patch_084.py (writes out.html).

Changed:
- COMM 1: tuning is unchanged. After the signal locks, the player flies a Reconnaissance Drone through the wormhole from a mission control console (live feed, MALP-style telemetry strip, radar) instead of the old three-station bearing puzzle. Free flight: WASD to move, Q and E for altitude, Shift to boost, mouse drag or arrow keys to look, wheel to zoom, T for optical and thermal. No move budget; the flight runs until the wormhole closes.
- Signal strength rises with proximity to the team. Hazard sets the help: low gives a SIG marker pointing at the team; medium gives a marker off by up to about 25 degrees that drifts, plus haze; high gives no marker and a noisy strength reading with heavy haze.
- Holding the reticle on the heat signature locks the team and always scores Pinpoint. Without a lock the player places a marker on the radar. Fix bands by distance: Pinpoint within 30 m, Good 80 m, Rough 160 m, Poor beyond (or no marker). The band effects are the approved ones (assist travel 1:00 / 1:30 / 2:00 / 3:00, yield 100 / 90 / 80 / 70%, intel +1 / full / -1 / none). If the wormhole closes first the link drops and the marker placed so far is scored, otherwise Poor.
- The zoom view shows every member of the overdue group (all teams in the group), with the injured member lying down and a medic kneeling. The result screen shows distance in metres.
- Drone tier = the best Unmanned Drone at home in the Motor Pool (tier 0 basic drone when none is owned). Tiers 0 to 5: sight 1/1/1/2/2/3 cells, zoom 2.0 to 5.0x, speed 14/18/22/28/34/42 m/s (mockup table, approved).
- Assault recon: new DRONE key on the dialing computer keypad under COMM 2, available with the gate open to a known (intel 2) stronghold that has not been captured. Free to launch, runs on the wormhole clock. Tag every contact (defenders show on thermal, structures only in optical) by holding the reticle; staying in a defender's red cone builds exposure (faster when flying fast or high); at 100% the drone is shot down.
- Recon results: all tagged = Full picture (enemy strength -15%, intel raised to tier 5), 70% or more = Good (-10%, intel tier 4), 40% or more = Partial (-5%), under 40% = Poor (0%). A spotted drone halves the reduction, gives no intel and alerts the defenders. Results last until the next assault is sent on that stronghold, then clear. The drone is never permanently lost.
- Assault odds: the strength reduction scales the stronghold difficulty term inside the success average; an alert subtracts 10 points from the final success. The send panel's estimate line shows the recon status.
- Drone cooldown 5:00 after a filed recon survey (the key shows READY m:ss). Saved with the game (older saves load with no cooldown).
- Removed the triangulation map, stations and bearing sweep code. The Radio Contact result, sitrep and Request Rescue block are unchanged.
- Drone audio runs on the game's Effects bus, so the Master and Effects sliders and the sound toggle apply.
- Keypad: the three left keys (COMM 1, COMM 2, DRONE) are 31 px high to fit the extra key; the Gate Room is 7 px taller than 0.8.3 (it already scrolled to the log at 950 px high).

Finding for review: the recon strength reduction is small at low levels. Level 1 stronghold difficulty is about 15, so -15% moves the difficulty term from 85 to 87.25, which is +0.75 points on the final odds (measured 45.0% to 45.75%). The alert penalty (-10 points) is far larger than the best recon reward. If recon should matter more, the options are applying the reduction to the final success percentage, or to the whole difficulty-to-success mapping; your call.

Assumptions I made that were not explicitly decided (flag any that are wrong):
- The 5-minute cooldown applies to assault recon only; rescue flights are never blocked. Aborting a recon flight does not start it.
- Intel mapping for recon: Full picture raises intel to tier 5 (stronghold defenses), Good to tier 4 (difficulty band); Partial and Poor give none.
- Planet scenery follows the world type (tundra, plateau, desert, forest, jungle, ocean, ruins, volcanic); night is a 25% chance.
- A captive-only radio contact (no overdue team) flies to the captives, shown as a captive group, with the same fix bands.
- The flight starts with the wormhole time left; the drone and COMM screens ignore the Escape key during a flight (ABORT button instead).
- Hint panel shows at the start of every flight and closes on the first movement key.

Verified (headless Chromium, zero console errors): load and new game; DRONE key states (unavailable, ready, cooling down); recon flight start, flight with keys, thermal toggle, END SURVEY, filing the survey, cooldown, recon fields on the world; recon odds (45.0% base, 45.75% at -15%, 35.0% alerted); rescue flow from COMM 1 tuning into the drone, marker placement, confirm fix, result screen, Request Rescue block, contact flag and fix band on the team; reticle lock on a real 4-member group (Pinpoint, zoom view with injured and medic, 0 m); link loss mid-flight scored as the marker or Poor; defender tagging; shot-down drone path (alert recorded); drone tiers 0, 1, 3, 5 read from the Motor Pool; abort without cooldown; save and resume with cooldown and recon intact; screenshots reviewed (keypad, recon feed, rescue feed, lock, spotted, results).
Not verified: Safari and touch layouts, real tier 2 and 4 flights (table checked at 0, 1, 3 and 5), group flights with more than one team, a full real-time five-minute wormhole run, sound by ear, pointer-lock mouse look.

Open action items:
- Review 0.8.4, especially the recon strength finding and the assumptions above.
- Released Oct 25 2026: 0.7.5 and 0.8.0 to 0.8.5 went to root together (sgc-command.html is 0.8.5, about 12.7 MB with the soundtrack); README and Game Guide (30 pages) refreshed for 0.8.5.
- Next planned: 0.8.5 tour and briefing-card popups (narration voice still unchosen); scanning, System Lords and FOB teams stay parked.

## 0.8.3 (BUILT, awaiting Brad's review): After-Action Report changes from 0.8.2 play

File: versions/sgc-command-0.8.3.html (built from 0.8.1 with tools/build-0.8.2/patch_083.py, which includes everything in 0.8.2). Not yet released to root. 0.8.2 below stays as history.

Changed:
- AAR has no time limit and no par; the clock and par are gone. Reward tier is set by accuracy only: 95%+ Excellent, 85%+ Standard, 70%+ Rough, below 70% rejected with a free retry. Rewards unchanged (supplies 5/10/15, research points 5/10/15, camaraderie +2/+4/+6 for eligible teams).
- AAR line titles are left-aligned above their input boxes.
- Mission log summary has a Teams row naming every team on the mission; the Flags line reads "None" when empty.
- Reports filed in 0.8.2 keep working (the saved time is ignored).

Assumption awaiting Brad: with no speed factor I kept the same three accuracy bands for the tiers; say if accurate completion should pay one flat reward instead.

Verified (headless browser): tier thresholds by accuracy, blank report rejected and retry, rewards, report saved and reloaded, 0.8.1 save resume, faction first contact on MALP tier 1 and 2, Teams row, "None" flag, left-aligned titles in a screenshot.
Not verified: Safari, touch layouts, real timers.

Open action items:
- Review 0.8.3 and confirm the tier assumption.
- 0.8.0 to 0.8.3 not yet released to root.

## 0.8.2 (BUILT, awaiting Brad's review): faction first contact and After-Action Report

File: versions/sgc-command-0.8.2.html (built from 0.8.1). Not yet released to root. Rebuild: tools/build-0.8.2/patch_082.py on the 0.8.1 file.

Faction first contact:
- The first time a faction becomes known, by any route (Exploration visit, Recon survey, assist survey, MALP at tier 2 or higher), the Operations log and the mission log events get "<Team> discovered the <Faction>. The <Faction> seemed open to diplomacy." (the MALP reads "The MALP discovered ..."). Logged once per faction.
- An Exploration visit to a faction world now identifies it (intel 2): it shows in Faction Relations and unlocks a Diplomat mission. Supplies and research still pay out.
- Faction Relations card shows "First contact [time] // by".
- Found while testing: before this build an Exploration visit to a faction world gave no discovery at all, and only MALP tier 2+ or Recon survey revealed factions.
- Saves from 0.8.1 load: factions already known are marked silently so no message repeats.

After-Action Report (typing minigame, optional):
- Briefing Room mission log: open a closed Exploration, Recon, Assist or Assault mission, press COMPLETE AAR. Entry box on the left of the room card, mission details stay on the right. One report per mission; the mission shows its result afterwards.
- Fields typed from the log: mission type, launch time, return time, team names, world, injuries, casualties (killed or captured), yield (Supplies, Naquadah, Research) and intel tier. Case does not matter.
- Scoring: character accuracy over all fields, time from the first keystroke against a par (field length at 35 words per minute, minimum 15 s). Excellent 95%+ at or under par, Standard 85%+ within 2x par, Rough 70%+, below 70% rejected with free retry.
- Rewards Rough/Standard/Excellent: supplies 5/10/15, research points 5/10/15, camaraderie +2/+4/+6 for each Recon, Assault and Security team on the mission. Exploration teams earn no camaraderie.
- Mission log detail: team stats at launch and at return removed; added Injured and Killed or captured rows to the summary so the report can be written from the log.

Assumptions awaiting Brad:
- Typing pace for par is 35 words per minute (my pick; he approved par time, not the pace).
- The log records times only, no date, so the report asks for launch time and return time.
- Supplies and research points pay for every eligible mission, including ones with no Exploration team.
- Camaraderie follows the existing rounding and the +10% glyph bonus.

Verified (headless browser): faction contact on Exploration, Recon, MALP tier 1 (silent) and tier 2; once-only message; Faction Relations note; AAR flow end to end including blank rejection and retry, tier thresholds, rewards to supplies, research and Recon camaraderie, focus kept while typing, save and reload of the report, 0.8.1 save resume. Screenshots reviewed: mission detail, empty and filled form, accepted result.
Not verified: real timers end to end, Safari, touch layouts, a faction visit in a long real playthrough, assist-route first contact.

Open action items:
- Review 0.8.2 and confirm the pace and time-only assumptions.
- 0.8.0 to 0.8.2 not yet released to root.

## 0.8.1 (BUILT, awaiting Brad's review): room panel layout and role icons

File: versions/sgc-command-0.8.1.html (built from 0.8.0, which holds the music). Not yet released to root. Rebuild: tools/build-0.8.1/patch_ui.py on the 0.8.0 file.

Changed:
- Room info panels now stretch down to the Operations Log (the log sits at the bottom of the screen); on screens narrower than 901 px the old stacked layout is kept. A room taller than the screen still scrolls the page, not the panel.
- Each section of a room panel (Teams, Raise a team, Team details, Loadout, Members, Stores, Reactor, Healing, Patients, and so on) is now its own inner panel. Sections split at each heading; the last panel in each column grows to fill the height.
- Role icons (framed unit-symbol style from the portrait mockup) now appear on team members instead of portraits: room staff strips, the Infirmary patient list, Lab and Archeology permanent staff, and Barracks team details. Frame color follows team type; injured members show a red frame with a cross, captured members an amber dashed frame, killed members a grey frame with a strike line.
- Icon mapping: Team Lead/Leader pennant, Soldier/Rifleman crossed lines, Scientist crossed retorts, Linguist globe, Sniper crosshair, Recon Specialist slash, Machine Gunner rounds, Grenadier grenade, Diplomat olive branch, Aide scroll, Medical cross, every Security Forces member the shield.

- Long lists now use card buttons along the top of the panel (Brad's call), with only the selected group shown below: Barracks teams by team type, Briefing Room mission log by Active or mission type, faction relations one faction at a time, Armory equipment by Weapons, Armor, Packs, Optics and Devices, Archeology glyph artifacts by level (with that level's bonus). The Lab's research list already used card buttons.
- Alignment: rows now center their labels, name boxes, status text and buttons on each other; Ask Carter matches other buttons; Members name boxes line up; Loadout dropdowns share one width.

Verified (headless Chromium, 1600x900 and 1280x720): all nine rooms render with no console errors, injured, captured and killed states show in Barracks and Infirmary.
Not done: icons on mission and rescue screens (Brad chose room strips, Barracks and states first). Portraits dropped; role icons only.

## 0.8.0 (BUILT, awaiting Brad's listen-through): music and sound effects

File: versions/sgc-command-0.8.0.html (built from 0.7.5, about 13 MB because the audio is embedded). Not yet released to root.

Changed:
- Music: five tracks from the Game Soundtrack folder, encoded to 64 kbps stereo and embedded. Title screen plays the Main Title. In game, calm plays Emancipation then Hathor in turn; tense (incoming wormhole or an overdue team) plays The Enemy Within; level cleared plays the End Credits. Tracks crossfade over 2.5 seconds, returning from tense to calm waits at least 20 seconds, music pauses when the tab is hidden and starts on the first click or key press.
- Effects: unchanged from 0.7.5 (the original generated sounds), now routed through the Effects slider. A polished effects set was tried (layered synthesis, then recorded-style samples) and Brad rejected it as sounding like a comedy reel; tools/audio-build keeps sfx.js and make_sfx.py for a later attempt but they are not in the build.
- Settings: Master, Music and Effects sliders, saved with the other settings. The SOUND button still mutes everything.
- Build: tools/audio-build (patch_sound.py and build_audio.py). Run patch_sound.py on 0.7.5 then build_audio.py to rebuild.

Verified (headless Chromium): title music plays, switches to calm on New Game and tense on an incoming wormhole, sliders change bus gain, no console errors. Not verified: how it sounds on real speakers.

Open: the soundtrack is copyrighted show music, so keep this build out of any public repository.

## 0.7.5 (RELEASED Oct 21 2026, current release): rescue request on the COMM 1 result screen (the planned 0.6.16)

File: versions/sgc-command-0.7.5.html (built from 0.7.4). Numbered 0.7.5 because 0.6.16 would now be out of order.

Changed:
- The Special Operations rescue request now lives only on the COMM 1 result screen (CONTACT ESTABLISHED). Under the Sitrep a Request Rescue list shows the five units (locked ones show their level) with REQUEST buttons that target the team just contacted (or the captured members). After a request the list is replaced by that unit's status (TO SGC, then RESCUE).
- The Quartermaster no longer has a rescue button, panel or active-request row; it is back to REQUEST SUPPLIES only. The header strip still shows each request's travel time.
- Rescue behavior and numbers are unchanged.
- COMM 1 now also works on a dialed world that holds captured members (Brad's call). The COMM 1 key lights and the same tune and triangulate minigame runs; the result screen says who is held captive and lists the rescue units for them. With no overdue team the assist rows (travel time, yield, intel) are hidden, since the fix quality does not change a captured-member rescue. If an overdue team is also on that world, both targets show on the one result screen.

Verified (headless Chromium): COMM 1 fix then the result screen shows the rescue list (overdue team and captured-member cases), request works and shows status, Quartermaster has no rescue text, save and load keeps the request, no console errors.
Released: sgc-command.html is build 0.7.5, README says 0.7.5, and SGC-Command-Game-Guide.pdf was rebuilt for 0.7.5 (28 pages; Sections 3, 8, 11 and 16 updated for the COMM 1 rescue request).

Release (Oct 21 2026): sgc-command.html is now build 0.7.4 and includes the whole 0.7 line (0.7.0 to 0.7.4). README says build 0.7.4. SGC-Command-Game-Guide.pdf was rebuilt for 0.7.4 (new Section 16 Minigames, updated Facility, dialing, overdue, Lab and quick reference; source in tools/guide-build/build_guide.py). Brad approved: "Everything looks good."

## 0.7.4 (RELEASED to sgc-command.html): Hammond's paperwork and Carter's techno-babble

File: versions/sgc-command-0.7.4.html (built from 0.7.3). See docs/design/minigames-design.md, sections 4 and 5.

Changed:
- Permanent Lab staff changed (Brad): Col. Samantha Carter is permanent Lab staff from the start (free, pre-assigned, counts as the on-station scientist for the 15% pace bonus). Dr. Bill Lee takes the Level 4 slot (400 supplies). Dr. Jay Felger is removed. Old saves get Carter, and a save that had Lee or Felger gets Lee.
- Hammond's paperwork (Briefing Room): 12 forms, 90 seconds, 10 correct to pass, 3 mistakes fails (2 allowed). 4 stamps by form type (keys 1 to 4) or DENY (D). 4 of 12 forms are flawed: wrong amount, missing signature, wrong department, expired date. Win: +50 supplies, and the next 2 missions that include a Logistic Truck launched within 15 minutes carry +75% supplies (added to the truck tier bonus, and the carry cap rises 75%; counted per mission). Cooldown 10 missions (any mission launch or assist counts); failure or walking away has no cooldown.
- Carter's techno-babble: an ASK CARTER button sits on each Lab research project's title line, only while Carter is on station. One question per project, four explanations, one real. Right: research bonus paid when the project completes, 25/50/75/100/125 by tier 1 to 5 (one-off projects count as tier 3, tiers above 5 count as 5). Wrong: project delayed by 10% of its total time rounded up to 30 seconds. Cooldown 20 missions, separate from Hammond's. 15 questions in 5 groups (reactor, dialing, security, MALP, Armory).

Assumptions for Brad to review (mine, not settled):
- Carter pre-assigned for free "from the beginning" changes the Lab economy: the 15% faster pace now applies to slot 1 from the start. Say if she should cost supplies or unlock at a level.
- Each project can be asked about once (so a cooldown-free project cannot be farmed).
- The Carter wrong-answer delay can exceed the original project time (it is added, not capped).
- Boosted truck missions also raise naquadah yield, as the truck tier bonus already does.
- Question wording and form wording are mine.

Verified (headless Chromium): Carter on station and button present or absent, setback of 30 s on a 2:00 project, cooldown 20 counting down per mission, bonus 75 paid on a tier 3 project, 15 questions with answer lengths balanced, paperwork win/lose/timeout, reward and cooldown, truck boost charges and window expiry, save and load, no console errors.
- Next: playtest 0.7.4. The 0.7 line is then complete; release to root and refresh the Game Guide PDF after Brad approves.

## 0.7.3 (built, released as part of 0.7.4): Glyph decoding and artifacts

File: versions/sgc-command-0.7.3.html (built from 0.7.2). See docs/design/minigames-design.md, section 1.

Changed:
- 10 collectable artifacts, 2 per level, separate from the alien-tech artifacts. The Archeology Office panel lists them, the five level bonuses, the relic and how many are collected.
- Inscriptions: each level has one fixed normal world (set when the level is generated; old saves get one on load) that always yields the odd artifact's inscription on a successful Exploration mission. The even artifact is a chance find on any other normal world of that level: 5%, then +15% for each Exploration mission that misses, reset on a find.
- Decoding needs a Linguist on station (the permanent Dr. Langford counts). Unlimited attempts, no penalty. Puzzle by artifact: 1,2,3,2,3,1,1,2,3,2.
- Puzzles (mine, flag for review): Fragment matching (match 6 broken fragments to whole glyphs, 4 mistakes allowed); Tablet reassembly (3x3 swap puzzle of a carved stone slab with rows of glyphs, 14 moves, scrambled with 6 swaps); Cipher deduction (4-glyph code from 6, 8 guesses, green/amber feedback).
- Hints: each failed or abandoned tablet unlocks one of 3 text hints for that artifact, and each one also pre-solves one piece (a pair, a tile or a code position) in later attempts. CONSULT LIBRARY BOOK gives a visual hint once per attempt.
- A successful decode reveals an existing normal world of that level as the artifact site (ARTIFACT SITE badge, intel set to at least 1). A successful Exploration mission there recovers the artifact. Both artifacts of a level collected unlocks that level's bonus: L1 +15% supply yield, L2 +10% research, L3 ambush chance -5 points, L4 assault injury and casualty odds -10%, L5 gate regeneration +6 per minute.
- All 10: relic "Ancient Repository Stone" (approved) on display: +10% camaraderie gain for all teams and +5% research yield.
- Artifacts 3, 6 and 8 name a Death Glider, a fleet beacon and defense technology in the decode text. These are lore only until the X-302, Sol Defense and Ion Cannon builds; Level 5 decode text mentions the Ancient facility and has no effect on it.

Assumptions for Brad to review (mine, not settled):
- Puzzle designs, move limits and mistake limits above.
- Level 4 odds cut applies to assault injury and casualties only.
- Camaraderie gain +10% is applied as an average (a fractional gain rolls up by chance).
- Artifact names are my own picks.
- Placement note: the artifact site can be any normal world of that level, including one you already explored.

Verified (headless Chromium): fixed-world inscription through a real returning mission, chance find rising by steps, all three puzzles solved and failed, hint unlocks, site assignment, badge, artifact recovery, all level bonuses and the final relic values, regen 18 with level 5 bonus, camaraderie gain average, save and load of the glyph state, no console errors.
- Next: playtest 0.7.3, then 0.7.4 Hammond's paperwork and Carter's techno-babble.

## 0.7.2 (built, released as part of 0.7.4): Reactor power routing and shields

File: versions/sgc-command-0.7.2.html (built from 0.7.1). See docs/design/minigames-design.md, section 2.

Changed:
- Power events: after 11 to 15 wormhole activations (outbound and incoming both count), a POWER FLUCTUATION opens the conduit puzzle once the gate is closed and idle. Counting starts at game start, then restarts when a routing puzzle is solved.
- Conduit puzzle (events and re-routing): 4x4 grid, values 1 to 5, no repeats in a row or column, every row and column matches its target total. 7 locked conduits; every generated grid has exactly one solution (30 sampled).
- Abandoning an event puzzle knocks one output offline, random among Gate, Lab and Shields but never the one the current preset boosts. No timer: the event is answered now or abandoned (Escape does not abandon an event). The Quartermaster shows RE-ROUTE POWER until it is solved; no new event fires while an output is offline.
- Offline effects: Gate stops regeneration (still dialable); Lab research pauses; Shields give no reduction.
- Node routing puzzle (Reactor tier install and ZPM install): 5 relays for a tier, 7 for the ZPM; each relay sends its whole capacity to one output and every output must hit its exact load. A newly installed Reactor tier does not add its regeneration until its connection is routed (old saves count as routed).
- Presets (unlocked by the first solved puzzle, changeable any time free): Balanced, Gate-heavy, Lab-heavy, Shield-heavy at +50% on the boosted output and -25% on the others. Shield reduction 10% Balanced, 15% Shield-heavy, 7.5% the other two.
- Shields apply to ambush injury odds (AMBUSH_INJ_P times one minus the reduction) and to unanswered Goa'uld raids: that percentage is the chance the shields absorb the raid and the treaty holds.
- Quartermaster Reactor panel: routing preset, output status, shield reduction, preset buttons, and the route or re-route button.
- State: state.rx in the save (old saves load with defaults).

Assumptions for Brad to review (mine, not settled):
- Event timing: opens when the gate is closed and idle, never mid-wormhole or over a COMM screen.
- Raid shield rule: the reduction percentage is a chance to absorb an unanswered raid.
- Shields reduce ambush injury odds only; assault injuries are untouched.
- The ZPM has no gameplay effect yet, so its routing is ceremony until Pegasus content.
- Lab offline shows only on the Quartermaster panel and in the log, not on the Lab panel.

Verified (headless Chromium): grid solution counts, event trigger and deferral while the gate is open, abandon and offline pick excluding the boosted output, offline gate regen, grid solve, preset effects (gate 18 per minute, lab pace 1.5x), node puzzle for a Reactor tier and the ZPM, routed tier regen 12 to 24, Lab pause and resume, save state, no console errors.
- Next: playtest 0.7.2, then 0.7.3 glyph decoding.

## 0.7.1 (built, released as part of 0.7.4): Radio contact

- COMM 2 radio voice: after tuning, a voice says "Team all clear." while no ambush has happened. Once an ambush has happened (fought clear, team returning late) the report says so; a stuck team gives no answer. An ambush still to come is never revealed.
File: versions/sgc-command-0.7.1.html (built from 0.7.0). See docs/design/minigames-design.md, section 3.

Changed:
- COMM 1 and COMM 2 keys on the left of the dialing keyboard, stacked (COMM 1 over COMM 2), styled like the other keys. COMM 1 flashes red when the wormhole is stable to a planet with an overdue team that has not been contacted; COMM 2 lights blue when the wormhole is stable to a planet with a team that can be recalled. Greyed out otherwise, and while the iris is closed.
- COMM 1 minigame (overdue teams only): tune the frequency out of the static (hold it steady), then take bearings from three relay stations by locking each sweeping line when centered, click where the lines meet and confirm the fix. Accuracy gives a band: Pinpoint (within 10%), Good (10 to 30%), Rough (30 to 60%), Poor (over 60%). The 5-minute wormhole keeps running; if it closes the minigame ends with no contact.
- Contact gives the sitrep. A fix band sets the assist: travel time 1:00 / 1:30 / 2:00 / 3:00, rescued team yield 100 / 90 / 80 / 70% (supplies and research), assist intel +1 tier / full / -1 tier / none.
- COMM 2 (teams that are not overdue): simple tune-to-frequency task, then a recall prompt per team group. A recalled team is home in 1:00 with 80% of the yield (supplies and research).
- Overdue rule: a stuck team (the existing 1-in-25 ambush outcome, Level 2 and up) is flagged overdue 3:30 after its scheduled return, and the 15-minute self-return timer starts at that flag. A late team shows PAST DUE instead of a changing countdown; the dialing computer table shows LATE.
- Ambushes are hidden: no OPS log line and no mission log event or ambushed flag until contact (sitrep) or the team's return.
- The Gate Room mission panel now says PRESS COMM 1 instead of the ESTABLISH CONTACT button. Overdue recall and SEND ASSIST work as before after contact.
- Saves: late-return times carry over; older saves load unchanged.

Assumptions to review:
- Minigame difficulty numbers (mine): tuning window 12% / 9% / 6% of the dial for Low / Medium / High hazard, signal jitter 2 / 5 / 10%, bearing sweep +-6.6 / 13.2 / 22 degrees with periods 1.8 / 1.4 / 1.0 seconds, static dots 40 / 140 / 300; hold time 1.2 s (COMM 1) and 0.7 s (COMM 2). Search area is x1 / x2 / x3 and fix error is measured in percent of the low-hazard map width.
- COMM 2 can recall exploration, recon and security missions. It cannot recall assault, assist, diplomacy or defend missions.
- Before an ambushed team's due time COMM 2 reports "all quiet" and a recall then still rolls the ambush when the team comes home. A team that is stuck but not yet flagged overdue answers "no answer" and cannot be recalled.
- When two overdue groups share a planet, COMM 1 works on one at a time.
- A failed assist team still goes overdue at once on arrival (not after 3:30) and its ambush line shows in the log.
- Rescue teams (Special Operations) still need no radio contact.

Verified (headless Chromium, virtual clock): stuck team shows PAST DUE with no ambush text in the log or mission log, then flagged overdue 3:30 later with the visible overdue event; COMM 1 flashes and COMM 2 lights; full COMM 1 run (tune, three bearings, fix, Pinpoint, assist time 1:00); COMM 2 run and recall (80% yield, 1:00 return); save and load of a stuck team; no console errors. Screenshots of the keyboard and the minigame.

Not verified: playing the minigame by hand (timing of the sweeping line, how hard Medium and High feel), COMM 2 on a team with a pending ambush, simultaneous groups on one planet, Safari and touch.

Open action items:
- Play the minigame and tell me if the difficulty numbers feel right.
- Next: 0.7.2 reactor power routing and shields (built).

## 0.7.0 (built, released as part of 0.7.4): Archeology Office, permanent staff, Facility layout
File: versions/sgc-command-0.7.0.html (built from 0.6.15). First of five minigame builds; see docs/design/minigames-design.md.

Changed:
- Facility screen: the room cards no longer show people. They are now a narrow column on the left, and the selected room's panel fills the rest of the width. Staff and teams show on the room's own panel (the staff strip). Below 900 px wide the cards go back to a two-column grid above the panel. The Gate Room screen is unchanged.
- New room: Archeology Office (card label LEVEL 20), key 9. Shows Linguists on station and the permanent staff section; glyph decoding is a COMING LATER placeholder until 0.7.3.
- Linguists now sit in the Archeology Office instead of the Science Lab. Only Scientists add the Lab research pace bonus, as the design says.
- Permanent staff (separate from teams, always on station): Dr. Bill Lee (Lab, unlocks Level 2, 200 supplies), Dr. Jay Felger (Lab, Level 4, 400), Dr. Catherine Langford (Archeology Office, Level 2, 150). Lab staff count as a scientist on station; Langford counts as a Linguist. New PERMANENT STAFF card in the Lab, and a section in the Archeology Office. Saved with the game; older saves load with none assigned.

Assumptions to review:
- Archeology Office card label is LEVEL 20 (my pick; it sits between the Infirmary and the Lab in the real complex numbering).
- It is last in the room order so keys 1 to 8 keep their rooms.
- Linguists moving out of the Lab reduces Lab pace if a team's Linguist was the only staff on station.
- The two Lab permanent staff are both scientists and each can take one slot's 15% bonus, so with the Lab's 1 slot only the first matters until Lab upgrades add slots.
- The room art on the Gate Room and Motor Pool cards is hidden in the narrow layout.

Verified (headless Chromium, 1440 and 800 px): no console errors; new layout screenshots for Archeology Office and Lab; assigning permanent staff (level gate, cost, always on station); Lab and Archeology occupants; save, reload and an older save without the new field; key 9 selects the Archeology Office, key 6 still the Lab; Gate Room screen unchanged.

Not verified: the 800 px layout beyond a screenshot, long sessions, Safari and touch.

Open action items:
- Review the layout and the assumptions above.
- Next: 0.7.1 radio contact (COMM 1 and COMM 2, overdue at 3:30), then 0.7.2 reactor routing, 0.7.3 glyph decoding, 0.7.4 Hammond's paperwork and Carter's techno-babble.

## 0.6.15 (RELEASED Oct 21 2026): Diplomacy for ordinary worlds
File: versions/sgc-command-0.6.15.html (built from 0.6.14). Released: root sgc-command.html is 0.6.15; Game Guide PDF rebuilt for 0.6.15 (15 pages). See docs/design/diplomacy-design.md.
- Diplomacy missions can target surveyed regular worlds and strongholds. +1 standing per mission; treaty chance 10% + 15% per standing (regular, guaranteed at 4) or 5% + 10% per standing (stronghold, guaranteed at 6). Stronghold talks cost 10 extra supplies.
- Treaty makes a regular world peaceful. A treaty stronghold stays hostile for assault but counts toward the final-stronghold lock.
- Raids: every 15:00 a treaty world is checked (15% regular, 30% stronghold). A 2:00 alert starts; a DEFEND mission (Security or Assault team) through the gate repels it. Unanswered: treaty void, standing halved.
- Assault on a treaty stronghold voids the treaty.
- Verified headless: treaty guaranteed on mission 4 (regular), alert, defend, lost-treaty, no-alert rejection, save/load of alert and raid timers, lock rule with a second stronghold. Not verified: visuals of the new chips and badges, long-run balance.
- Assumptions to confirm: intel 2 needed to target; a treaty regular world does not count as explored for the lock; assault voids the treaty; stronghold expected missions is about 4 (the table I gave said 5).

## 0.6.14 (released Oct 21 2026, superseded by 0.6.15): Special Operations rescue teams
File: versions/sgc-command-0.6.14.html (built from 0.6.13). See docs/design/rescue-design.md. Released: root sgc-command.html is 0.6.14; Game Guide PDF rebuilt for 0.6.14 (14 pages, rebuilt from extracted text because the original source was not saved).

Changed:
- New Special Operations Rescue section on the Quartermaster card, under Air Force Logistics. Five real US units, one per level: Army Rangers (Level 1, 5:00 to the SGC, fee 10, 40% delay), Air Force Pararescue (Level 2, 4:00, 15, 30%), Marine Raiders (Level 3, 3:00, 20, 20%), Navy SEALs (Level 4, 2:00, 25, 10%), Delta Force (Level 5, 1:00, 30, never delayed).
- Pick a target from the dropdown (an overdue team, or the captured members on a stronghold), then request a unit. Requests are free. The team travels to the SGC; on arrival the gate dials out on its own (normal gate power plus the 5 auto-dial) and sends the team, paying the fee at that moment. The gate closes behind it.
- A rescue always succeeds after a 2-minute mission. An overdue team is rescued as with an assist (ambush cleared, self-return timer paused while the rescue runs, then it returns through the gate as usual). Captured members are freed on the spot and are ready for duty. The Level 1 Assault/Security dead end is closed.
- A delayed team arrives 1 to 3 minutes late (rolled on arrival, like the Tel'tak). A unit can be requested again as soon as its rescue is done. Rescue limits are separate from logistics. Requests appear in the active missions strip and the mission log (kind: rescue). Requests are saved and restored.

Assumptions to review:
- Delay applies to the trip to the SGC, not to the mission through the gate.
- No radio contact is needed to request a rescue of an overdue team.
- If the target is gone before the team reaches the gate (an overdue team returned on its own, or the stronghold fell), the team stands down with no fee.
- While waiting at the SGC the card shows what holds it (gate busy, power short, fee short) and it dials as soon as it can.
- The returning rescued team is not escorted by the special ops team in the mission list; the team is simply ready to be requested again.

Verified (headless Chromium, virtual clock): captured-member rescue end to end (travel 5:00, standby, dial-out, fee 10 paid at dispatch, gate closes, member freed, mission logged), overdue-team rescue end to end (waits for power, dials, timer paused, rescued flag, team comes home ready), Level 1 request for Level 2+ units locked, save and resume mid-travel (time left preserved, request completes after resume), Quartermaster and Briefing screens render with a rescue in the log, zero console errors, 8 full economy sessions with zero errors.

Not verified: delay roll visually (the 40% path was not forced), several simultaneous requests competing for the gate, a manual dial interrupted by a rescue, the look of the new Quartermaster section.

Open action items:
- Review the assumptions above.
- Next playtest: Level 1 with research spending.

## 0.6.13: exploration pacing from the balance pass
File: versions/sgc-command-0.6.13.html (built from 0.6.12). See docs/reports/balance-report-0.6.12.md and docs/reports/balance-whatifs-0.6.12.md.

Changed:
- New games start with two Exploration teams (Team 2: Capt. Mercer, Sgt. Alvarez, Dr. Novak, Dr. Haddad). The Exploration limit is the higher of 2 and the current level; other types still equal the level.
- The final stronghold of a level unlocks once 75% of that level's regular (non-stronghold) worlds, rounded down, have been explored or captured: 3 of 4 at Level 1, 3 of 5 at Level 2, 1 of 2 at Level 3, 3 of 5 at Level 4, 4 of 6 at Level 5. The blocked message states how many more are needed.
- An ambush injures a team member with half the old chance (the camaraderie and armor reduction still applies on top).

Assumptions to review:
- Raising an Exploration team beyond the two starting teams costs base price for the first extra team and +50% for each after, as the second team did before.
- Saves started before 0.6.13 keep one Exploration team.
- Regular worlds include faction and Ancient Lab worlds.

Verified (headless Chromium, virtual clock): new game has two Exploration teams with unique crews, Exploration limit 2 at Level 1 and a third raise is blocked, lock counts 3 / 2 / 1 / 0 more worlds as worlds are explored, ambush injury rate 50.1% over 20000 rolls, per-level lock needs 3 / 1 / 3 / 4 for Levels 2 to 5, zero console errors. 40 simulated sessions: Level 2 median 15.1 minutes (was 35.4 in 0.6.12), 38 of 40 reached Level 2 inside 150 minutes, supplies at the first assault dial 192 median.

Not verified: loading an older save, sound, the Barracks card at Level 1 by eye.

Open action items:
- Special Operations rescue teams (design in progress).
- Assault and Security captured-member dead end at Level 1 (rescue teams are meant to free captured members).
- Next playtest: Level 1 with research spending.

## 0.6.12: power capped at 120
File: versions/sgc-command-0.6.12.html (built from 0.6.11).

Changed:
- Power is capped at 120. Regeneration (12 per minute, 24 / 36 / 48 with Reactor I to III) stops at the cap. Naquadah conversion (+15) is disabled at the cap and cannot overfill it. The Quartermaster and the facility card show power as n / 120 with the bar back.
- Saves with more than 120 power are clamped to 120 on load.

Verified (headless Chromium): regeneration stops at 120 from 118, conversion is blocked at the cap and the button disables, header and Quartermaster text show / 120, zero console errors.

Not verified: load from a real older save over 120.

Open action items:
- Playtest: at a 120 cap a Level 5 dial (92 to 98) leaves 22 to 28, so a second dial waits for regeneration; Level 1 dials (32 to 38) allow three from a full pool.

## 0.6.11: gate power by light years, power regeneration, Ancient research ship and ZPM
File: versions/sgc-command-0.6.11.html (built from 0.6.10). See gate-power-design.md.

Changed:
- Gate power cost is 8 per light year of the world's distance, rounded. Orbit order shifts each world's distance by a fixed offset from -0.4 ly (innermost) to +0.4 ly (outermost), spread evenly. Costs by level: L1 32 to 38, L2 45 to 51, L3 66 to 72, L4 81 to 87, L5 92 to 98. Starmap shows a Distance row and per-system cost ranges.
- Reactor capacity removed. Power has no cap and regenerates 12 per minute at base. Reactor I, II and III now set regeneration to 24, 36 and 48 per minute. Naquadah conversion (+15) works at any power level. Failed lock (2 power) and auto-dial (+5) unchanged. Starting power stays 80.
- Exploring the Level 5 Ancient Lab now also reveals a second gate address: the Ancient Research Ship, a special one-off peaceful world (no ambush, gate cost 98 from a fixed +0.4 ly offset). Exploring it with an Exploration team recovers the ZPM, once.
- The Quartermaster Reactor section shows ZPM status and an INSTALL ZPM button. Installed onto the reactor, it has no other effect yet.
- The Atlantis panel says dialing needs a ZPM installed; Atlantis is still not dialable.

Assumptions I made (flag any that are wrong):
- Offsets use the world's orbit order within its system (inner to outer), excluding the research ship, so costs do not shift when the ship appears.
- The research ship's yield is a normal exploration yield plus the ZPM, and it can be re-explored for supplies; the ZPM is granted only once. It cannot be a Tel'tak run target.
- Saves made on 0.6.10 or earlier whose Ancient Lab is already explored get the research ship added on load.
- Old saves with power above the former cap keep their power.

Verified (headless Chromium): per-world costs match the table at all five levels; regeneration at all four tiers; real regeneration over 6 seconds; naquadah conversion at high power; Ancient Lab exploration reveals the ship once; ship exploration sets the ZPM; the install button appears only after recovery; save data holds the ZPM; screenshot of the Level 5 system view with the ship reviewed; zero console errors.

Not verified: a full-length real mission to the ship through the gate; load from a real older save; balance of 8 power per ly against real pacing.

Open action items:
- Decide what the installed ZPM does, what a Pegasus dial costs and how Atlantis travel works.
- Playtest the power economy (no cap, with regeneration tiers).

## 0.6.10: logistics capped at two shipments in transit
File: versions/sgc-command-0.6.10.html (built from 0.6.9).

Changed:
- No more than two logistics shipments can be in transit at once. Further REQUEST buttons are disabled until one arrives, and the status line shows "n / 2 SHIPMENTS IN TRANSIT". The shared post-arrival cooldown still applies.

Assumption: the cap counts shipments in transit only; it does not limit how many requests can be made over time.

Verified (headless Chromium): two requests accepted, a third is ignored and every other REQUEST button is disabled, status reads 2 / 2, an arrival frees a slot and a new request is accepted, zero console errors.

Not verified: full-length real timers; load from an older save in a real browser.

## 0.6.9: Air Force Logistics supply requests, Tel'tak return raised
File: versions/sgc-command-0.6.9.html (built from 0.6.8). See docs/design/logistics-design.md.

Changed:
- Quartermaster card has a new Air Force Logistics section with a REQUEST SUPPLIES button that opens the unit list. Six real bases: Peterson SFB (10 km, Truck, 1:00, 12 supplies, Level 1), Hill AFB (800 km, Helicopter, 4:00, 25, Level 1), Travis AFB (1,600 km, C-130, 7:00, 55, Level 2), Wright-Patterson AFB (1,900 km, C-130, 8:00, 70, Level 3), Ramstein AB (8,000 km, C-17, 14:00, 125, Level 4), Kadena AB (9,500 km, C-17, 16:00, 150, Level 5).
- Requests are free. Each unit sends one shipment at a time. When any shipment arrives, all logistics requests are blocked until that tier's cooldown ends (Truck 2:00, Helicopter 3:00, C-130 5:00, C-17 8:00). Supplies credit on arrival with an Operations log entry.
- Shipments show in the Active Missions table, the strip on every screen and the Quartermaster card status. Shipments and the cooldown are saved and resume after loading.
- Tel'tak base supply return raised from 40 to 100 (times the world hazard multiplier, so 100 to 150 per run).

Assumptions I made (flag any that are wrong):
- A shipment in transit from one unit does not block requests to other units; only a unit's own transit and the post-arrival cooldown block. A second arrival during a cooldown extends it to the longer remaining time.
- Cooldown timers pause while the game is closed, like the other timers.
- Delivery times are fixed per unit (scaled by distance across the table), not computed from a formula.
- Loads are the proposed table scaled up 25% as chosen.

Verified (headless Chromium): button and all six units render; Level 1 shows four units locked; locked units cannot be requested; request sets transit; a second request to the same unit is ignored; other units can be requested while one is in transit; arrival credits supplies and starts the cooldown; the cooldown blocks requests; save data holds transit and cooldown; strip shows the shipment; zero console errors; screenshot reviewed at 1440x900.

Not verified: real-time arrival over full timers; load from a save made on 0.6.8 in a real browser; Active Missions table row with a logistics shipment on screen; balance against real pacing (Tel'tak at 100 and logistics together may make supplies plentiful).

Open action items:
- Confirm or correct the assumptions above and playtest the supply balance.

## 0.6.8 : Gate Room dead space removed, map controls moved onto the map
File: versions/sgc-command-0.6.8.html (built from 0.6.7). Layout only, no game rules changed.

Changed:
- The Dialing computer panel height now sets the row height. Selecting a world on the starmap no longer stretches the panel, so the blank band above the keyboard is gone. The dialing computer display is the same size as before. The Starmap panel stays level with it.
- Map controls moved inside the map like a standard map app: + and - stacked top-right, a recenter icon under them, and the GALAXY CHART / ENTER SYSTEM toggle top-left. The old button row above the map is gone.
- The map keeps its aspect ratio, sized to the space above a fixed-height info box (it scrolls if a world has more detail than fits; address glyphs sit on the header row). At 1440x900 the map is about 645 px wide.
- Dialing status strip fits on one line with shorter text (SELECT A DESTINATION, ALIGN n STEPS // CLOCKWISE, ALIGNED // PRESS LOCK, WORMHOLE STABLE, NEED n POWER, INBOUND // DIAL LOCKED OUT). Slightly tighter gaps around the display and keyboard.

Verified (headless Chromium at 1280x720, 1440x900, 1920x1080): panel bottoms identical with nothing selected, a world selected and the galaxy chart showing; zoom, recenter, layer toggle and drag-pan work; clicking a planet selects it; zero console errors; screenshot reviewed at 1440x900.

Not verified: the Lab and room-card regression suites on this build; the Atlantis and system-list info boxes (they scroll if they exceed the box).

## 0.6.7: Keyboard controls and active mission table
File: versions/sgc-command-0.6.7.html (built from 0.6.6). Interface only, no game rules changed.

Changed:
- Dialing controls moved into the Dialing computer panel and restyled as keyboard keys: status strip (chevrons locked, power, next action), rotate keys -5 / -1 / +1 / +5 around a wide LOCK key, then AUTO-DIAL, CANCEL DIALING, DISENGAGE WORMHOLE and an IRIS key showing its state. Unavailable keys are dimmed. The separate controls panel is gone.
- The wormhole ring in the dialing computer is replaced by an ACTIVE MISSIONS table (unit, task and world, time left). Teams sent together on one mission show as one row ("EXP +1"). Also listed: MALPs away or held, vehicles repairing, Tel'tak supply runs and Lab projects and upgrades. Five rows; extra missions show as "+N MORE". The header shows the total. Wormhole time stays in the footer bar.
- Layout: Starmap ends level with the Dialing computer; Operations log and Mission sit side by side below.

Verified (headless Chromium): zero console errors; grouped teams collapse to one row; keys, AUTO-DIAL start and iris toggle work; screenshot reviewed at 1440x900.

Not verified: other window sizes; full Lab and room-card regression suites on this build; assault and assist groups with real missions (grouping keyed by the shared mission ids).

## 0.6.6: Starmap aligned with dialing computer
File: versions/sgc-command-0.6.6.html (built from 0.6.5). Layout only.

Changed:
- Gate Room: the Starmap panel now ends level with the Dialing computer panel (checked at 1440x900: both span the same rows). The dialing controls and Mission panels start on the same line beneath them. The dialing computer is centered in its panel.
- Operations log stays under the dialing controls on the left; Mission runs down the right side beneath the starmap.

Verified (headless Chromium): zero console errors; panel tops and bottoms measured and screenshot reviewed at 1440x900.

Not verified: other window sizes.

## 0.6.5: Gate Room layout restored
File: versions/sgc-command-0.6.5.html (built from 0.6.2).

Changed:
- Gate Room screen layout is back to the 0.6.2 arrangement: Dialing computer and controls on the left with the Operations log under them, Starmap and Mission on the right. No dragging, resizing or layout settings. The 0.6.3 no-scroll fit is also gone, so the screen scrolls about 150 px at 1440x900 as in 0.6.2.
- Kept from 0.6.3: the redesigned dialing controls (readout with chevrons locked, gate power and next-action prompt; rotate clusters around a large LOCK; AUTO-DIAL; CANCEL DIALING, DISENGAGE WORMHOLE and the iris box with lamp) and the IDC TRANSPONDER text on the dialing computer (IDC CONFIRMED - team name).
- 0.6.3 and 0.6.4 are superseded by this build.

Verified (headless Chromium): zero console errors; Gate Room screenshot reviewed; IDC text for a returning team; the 33 Lab checks and room-card clicks re-run and pass.

Not verified: the controls redesign at narrow window widths.


## 0.6.3 (superseded): Gate Room screen rework
File: versions/sgc-command-0.6.3.html (0.6.2 kept untouched beside it). Layout and interface only, no game rules changed.

New:
- Gate Room fits the window with no page scrolling (checked at 1280x720, 1440x900 and 1920x1080, and with the incoming-wormhole bar showing). The dialing computer and starmap scale to whatever space their panel has; Mission and Operations log scroll inside their panels.
- Default layout: Dialing computer, Dialing controls and Mission stacked on the left, Starmap on the right, Operations log across the bottom like the Facility screen.
- Rearrange: drag a panel by its title (the three-bar icon) onto another panel to swap places. Resize: drag the dividers (left/right, between the three left panels, and above the log). All five panels can move, including the log.
- The layout is saved with Settings (this browser, not inside game saves). RESET LAYOUT in Settings restores the default. Settings RESET TO DEFAULTS also resets it.
- Dialing controls redesigned: readout line (chevrons locked, gate power cost and available, next-action prompt), then rotate cluster, a large LOCK, the other rotate cluster and AUTO-DIAL, then CANCEL DIALING, DISENGAGE WORMHOLE and an iris box with an indicator lamp. The duplicate destination readout is gone (the dialing computer already shows it).
- Dialing computer: the Authorization code area is now IDC TRANSPONDER. It reads AWAITING IDC while waiting, IDC CONFIRMED - team name(s) for a returning team, IDC CONFIRMED - ALLIED SIGNATURE for an allied incoming gate, NO IDC - UNRECOGNIZED SIGNATURE for a hostile one, NO SIGNAL when idle. The line under it shows the iris state.

Assumptions I made (flag any that are wrong):
- Default proportions chosen to fit 1440x900: dialing computer about 48% of the left stack, controls 28%, mission 24%, log about 12% of the height.
- The incoming signal status moved into the readout prompt (INBOUND WORMHOLE // DIALING LOCKED OUT); the red alert bar is unchanged.
- Allied non-returning signals say ALLIED SIGNATURE since no team name exists for them.
- Swapping a panel into a very small slot can shrink it a lot (a starmap in a small slot shrinks to a few pixels); drag a divider to give it room.

Verified (headless Chromium): zero console errors; no page scroll at three window sizes and with the alert bar; drag-swap between slots; all four dividers; layout saved to settings and restored after reload; reset layout; log moves back to the Facility screen and returns; IDC text for awaiting, returning team, hostile; the 33 Lab checks and all room-card clicks re-run and pass; screenshots reviewed.

Not verified: touch dragging on a tablet, narrow windows below 1280 wide, a long Mission panel in a small slot.

Open action items:
- Play the Gate Room in your browser: adjust the layout and tell me what default feels right.
- Still open: Langaran perk assumption, Peaceful worlds for non-faction worlds, logistics.

## 0.6.2: room card cleanup
File: versions/sgc-command-0.6.2.html (0.6.1 kept untouched beside it). Layout pass only, no game rules changed.

New:
- Every room card follows one pattern: title, a compact STAFF strip under it (name chips with a status dot, red when injured), then the contents. The room description line now sits behind the HELP toggle. The Personnel Present lists are gone.
- Selectable cards: Science Lab (MALP, Gate Room, Armory, Alien Tech, Lab Upgrades), Gate Room (seven tier chips with a detail panel), Barracks (the five team types replace the long Raise a Team list), Motor Pool (MALPs, Truck, Drone, ATV), Armory (Equipment, Tel'tak). Each card shows a one-line status; the chosen card is remembered while the game runs.
- Science Lab left column: research slots with the auto-assigned scientist named on each slot (first slot gets the first scientist on station), time, bar and rush; offline banner with construction timer.
- Quartermaster split into Stores and Reactor (power bar, recovery, gate cost). Infirmary shows the healing math (base time, medical officer, healing device, Nox, current time) and a Patients list. Briefing Room faction rows shortened to benefit and next benefit.
- Team members who were listed under the Armory (Soldier and other non-Lab, non-lead roles) now show in the Barracks, including on the Barracks room card dots.

Assumptions I made (flag any that are wrong):
- You left the Lab card list open, so I made Lab Upgrades a fifth card (Armory opens its six lines, Alien Tech holds the four artifact and wreck items).
- Linguists count as Lab staff and are assigned to slots like Scientists, as in 0.6.1.
- Selected cards reset when you reload; they are not saved.

Verified (headless Chromium): zero console errors; the 33 Lab checks from 0.6.1 re-run and pass; clicking every card opens the right content; the selected card persists when you change rooms and come back; screenshots of all eight rooms reviewed. Fixed during testing: doubled status icons and a Gate chip label overflow.

Not verified: narrow screens, a large roster (the staff strip with many chips), Briefing Room with several factions and missions.

Open action items:
- Play the rooms in your browser and tell me what still feels cluttered.
- Still open: Langaran perk assumption, Peaceful worlds for non-faction worlds, logistics.

## 0.6.1: Science Lab upgrades
File: versions/sgc-command-0.6.1.html (0.6.0 kept untouched beside it). Design in docs/design/lab-design.md.

New:
- Lab upgrade ladder, three tiers: 100 / 250 / 500 supplies, built over 2:00 / 5:00 / 10:00. Each tier adds +5% research pace, -5% project cost, -5% rush cost. Slots: 1, 1, 2, 3 at tiers 0 to 3.
- The Lab is offline while an upgrade is built: running projects pause, no new projects, rush disabled. The strip, Lab card and Lab room show a construction timer.
- Parallel research: the Lab room lists every slot (project, time left, progress bar, own RUSH button, or EMPTY). Gate Room, MALP and Armory research all share the slots.
- A scientist on station speeds one slot each (the first N projects get the 15% cut).
- Project cost discount applies to research points and supplies on every research project; the Lab and Gate Room cards show the discounted costs.
- Active missions strip has one chip per running project plus the upgrade chip. Saves keep tier, projects and construction; old saves with one project load as tier 0 with that project in slot 1.

Assumptions I made (flag any that are wrong):
- Cost reduction applies to both research points and supplies of research projects, and not to purchases after research.
- Pace is read as speed: tier 3 is 1.15x speed.
- A Linguist on station counts toward the per-slot staff bonus, as it did before (Scientist or Linguist are both Lab staff).
- A Lab upgrade can be started while projects are running; they pause and resume.
- Only one Gate Room project at a time, and no duplicate Armory items in parallel.

Verified (headless Chromium, 33 checks): zero console errors. Costs 100 / 95 research points at tier 0 / 1; slot counts 1, 1, 2, 3; third project blocked at two slots; second project blocked at tier 0; upgrade costs deducted and double-build blocked; Lab offline blocks starts; projects frozen during construction and resuming after; pace factors 0.85, 0.8095 and 0.7727 with two scientists; rush cost -5%; strip chips; screenshots of the Lab at tier 0 building, tier 2 with two projects and tier 3 reviewed. Save and load round trip with tier 2, two projects and a build in progress; old-format save migration.

Not verified: a real-time play through all three construction timers, narrow screens, Tollan stacking with Lab tiers in the live UI.

Open action items:
- Review the assumptions above, then play the Lab in your browser.
- Still open from 0.6.0: Langaran perk assumption, whether non-faction worlds can be made Peaceful, logistics.

## 0.6.0: factions and diplomacy
File: versions/sgc-command-0.6.0.html (0.5.9 kept untouched beside it). Design in docs/design/faction-design.md.

New:
- Diplomat Team: new team type (raise 50, send 10, Team Lead, Diplomat, Linguist, Aide). No camaraderie or gear.
- DIPLOMACY mission type: one Diplomat team plus at least one Security team to a known faction world. 5:00, no ambush, group returns together. +3 standing per mission for the faction.
- Standing tiers: Contact 1, Partner 5, Ally 12, Sworn 25 points. A faction world is Peaceful from Partner. Standing never falls.
- Perks from Partner on, growing at Ally and Sworn: Langaran supply yield, Tollan research speed, Tok'ra intel then 10% weaker defenses, Free Jaffa assault odds and a free replacement per level at Sworn, Asgard faster missions, recalls and rescues, Nox faster healing (10, 20, 30%).
- Sworn income every 10 minutes: Langaran 250 supplies, Tollan 250 research, the rest 50 supplies.
- Briefing Room Faction relations panel, starmap faction row and badge with tier, mission log Standing gained line. Saves keep standing and payment timers; old saves load with no standing.

Assumptions I made (flag any that are wrong):
- Only Diplomat Teams can run diplomatic missions (Exploration teams cannot).
- Langaran perk is +10, 20, 30% exploration supply yield (you gave percentages only for Tollan, Asgard, Nox).
- Asgard speed applies to exploration, recon and diplomatic missions, recalls and assist rescues, not assaults or MALPs.
- Tok'ra Partner reveals difficulty band and defenses on strongholds already found; Ally reveals ambush odds on every world.
- Free Jaffa and Tok'ra bonuses add to assault odds before vehicle bonuses; the Sworn Tok'ra defense cut is small at low levels (about 0.5 points at Level 1).
- First Sworn payment arrives 10 minutes after reaching Sworn. Limit one Diplomat team per level like other types. No vehicles on diplomatic missions. Nox "calm their sector" dropped.
- Faction worlds are only identified at intel 2, so a Recon survey or MALP must find them before a diplomatic mission.

Verified (headless Chromium): zero console errors. Diplomat raise and roster; picker filtering; Security required; cost 15; no ambush; 5:00 duration; standing 3, 6, 9, 12 with tier and peaceful flip at Partner; Security camaraderie 10 per mission; all six perk scalings; Tok'ra reveal rules and Sworn defense cut; Free Jaffa +5/10/15 and free replacement once per level; Asgard 0.7x at Sworn; payments (225 supplies, 200 research, once per cooldown); save and load of standing, timers and free replacement; Briefing Room screenshot. Earlier armory and group-mission checks re-run on 0.6.0; one old check (Security 95% score) fails identically on 0.5.9, caused by team camaraderie differences in the test, not game logic.

Not verified: real-time 5-minute mission through the live UI, a full play to Sworn, narrow screens.

Open action items:
- Review the assumptions above, especially the Langaran perk.
- Tell me whether non-faction worlds should get diplomatic Peaceful missions next, or logistics.
- Base upgrades (Lab upgrades, extra project slots) from 0.5.9 are still unscheduled.

## 0.5.9 (complete)
File: versions/sgc-command-0.5.9.html

Research phase two. Part one is the Gate Room upgrade path (gate-upgrades-design.md). Part two, below, is the Armory and alien technology (docs/design/armory-design.md). Both decided by Brad. Base upgrades (Lab upgrades, extra project slots) are still to come.
- Seven-tier shared ladder. Each tier needs its Lab research finished before you can advance. Supply tiers: research unlocks it, then a one-click instant purchase in the Gate Room. Reactor tiers: the research itself installs them.
- T1 Gate security detail (100 RP, 2:00, 150 supplies): hostile incursions no longer steal supplies (the 10 power loss still happens).
- T2 Chief Master Sergeant Walter Harriman (200 RP, 4:00, 200 supplies): opens the iris on a valid IDC (allied or returning teams) and closes it when no IDC arrives; if he closed it, he reopens it when the wormhole ends.
- T3 Dialing speed I (300 RP, 5:00, 100 supplies): auto-dial step 90 to 60 ms, lock pause 550 to 400 ms. T5 Dialing speed II (500 RP, 8:00, 200 supplies): 45 ms and 250 ms.
- T4, T6, T7 Reactor I to III (1000 RP each, 6:00, 10:00, 14:00): max power 200, 300, 400.
- Gate Room card in the Facility shows the ladder with INSTALLED, BUY, RESEARCHING, RESEARCH IN THE LAB and LOCKED states. Lab shows the next tier under Gate Room research. The one-project queue, scientist bonus, rush and the active missions strip all handle gate projects.
- Saves include the ladder; older saves start at tier 0.

Assumptions I made (flag any that are wrong):
- Unlock research costs only research points; the supplies are paid at purchase.
- Security stops the supply theft only, not the power drain.
- The Harriman auto-iris applies to hostile and allied incoming wormholes at the moment the IDC result arrives.
- Reactor tiers cost no supplies (you gave only research points).

Verified (headless Chromium): all seven tiers researched, rushed and bought in order; max power 400, dial timings 45 and 250 ms; costs deducted correctly; Harriman closed the iris on a hostile signal; zero console errors; Gate Room screenshot reviewed.

Not verified: security detail during a real hostile incursion resolving to the end, Harriman opening for an allied or returning team, save and load of a mid-ladder state.

### Part two: Armory and alien technology
File: versions/sgc-command-0.5.9.html (same file)

New:
- Armory gear, 22 items. Packs (Rucksack 45, Tactical Ruck 60, Expedition Pack 75, Heavy Haul Pack 95 supplies cap), body armor (5, 10, 15, 20% fewer injuries and casualties), optics (Tactical Optics -2, Night Vision -4, Thermal Imager -6 points ambush chance, and Thermal Imager lets a Recon survey reveal intel tier 5), weapons per team type (Exploration MP5 and P90; Recon MP5SD and M110; Assault M4A1, M249 and M203), each with assault points and an injury cut as in docs/design/armory-design.md.
- Flow: research in the Lab (research points up front, timed, one project at a time, in order within each line), then buy one unit per purchase in the Armory (100/200/300/400 RP, 2/4/6/8 minutes, 40/80/120/160 supplies by position in the line), then issue it to a team in the Barracks. Each team has weapon, armor, pack (Exploration only) and optics slots; gear can be changed while the team is on station and returns to stock when removed.
- Effects: pack cap clips the Exploration supply roll (default Field Pack 30; naquadah is outside the cap) and the log says how much was left behind. Armor and weapon injury cuts combine, then stack with camaraderie as a relative cut on ambush injury and assault casualties. Weapon assault points are the average across the Recon and Assault teams in the group, added to the assault success score. Optics cut each team's own ambush chance.
- Alien tech: the Goa'uld healing device artifact is recovered on a successful exploration of one fixed Level 1 world, and the Jaffa staff weapon on a fixed Level 2 world. Each is researched in the Lab (healing device 200 RP 4:00, staff weapon 300 RP 6:00), then bought (150 supplies each). The healing device is installed once and halves Infirmary healing. The staff weapon is a Recon or Assault weapon worth +15 assault points and a 10% injury cut.
- Healing: base Infirmary healing is now 5:00. Maj. Hale halves it (2:30) and the healing device halves it again (1:15 with both, 2:30 device alone).
- Tel'tak: a wreck is recovered when a fixed stronghold is captured (first stronghold in the Level 2 list and in the Level 3 list). Each is restored in the Lab (600 RP, 12:00) and put into service in the Armory for 200 supplies. Up to two ships. A run to an explored regular world costs 2 supplies, takes 2 minutes per light year round trip, and returns that world's maximum supply roll (40 x hazard multiplier, no carry cap, no truck bonus). One run in five is delayed 1 to 3 minutes. Never ambushed or damaged.
- Armory room shows stock, purchases, healing device install and the Tel'tak controls. Lab shows Armory research and alien technology. Barracks team details show the loadout with a summary of its effects. Active missions strip shows Tel'tak runs. Saves include everything; older saves load with empty Armory state, and tagged worlds already explored or captured grant their artifacts.

Assumptions I made (flag any that are wrong):
- The fixed artifact worlds are the first regular world generated in Level 1 and Level 2; the Tel'tak wrecks come from the first stronghold in the Level 2 and Level 3 lists. An exploration that comes back injured does not earn the artifact; explore the world again.
- Weapon injury cuts for non-alien weapons (3, 6 and 8%) came from the draft you approved; they add to the armor cut before camaraderie stacks.
- Weapon assault points average across the Recon and Assault teams in a group rather than adding up.
- Optics apply to the team carrying them only; a MALP launched alongside is unaffected.
- Gear stays with a team if a member is killed and is not lost in a failed assault.
- Tel'tak runs can go to any explored regular world in any level. The hazard and expected yield show only once the world has intel tier 3, but the run always pays the real maximum.
- The Tel'tak delay is decided when the ship reaches its return time, not at launch.
- Tel'tak runs do not get a mission log entry yet; they appear in the operations log and the active missions strip.
- A Recon survey no longer lowers an existing intel tier 5 to 4 (it used to set 4 outright).

Verified (headless Chromium, 36 checks plus a statistical run): zero console errors; research order and one-project rule; purchase, equip, unequip and stock counts; wrong-slot rejection; pack cap clipping 60 to 45 and 30 with the log note; armor 20% and camaraderie tier 5 stacking to 60%; staff +15 and M203 +11 points in the assault chance; artifact recovery on a successful exploration; healing device install, rates 4 and 2 with and without Hale; Tel'tak research, service, fee, 528 second round trip for 4.4 ly, delay path and arrival yield of 50 on a medium world; wreck recovery flag; save and load round trip; an older save without Armory data; Armory, Lab and Barracks screens reviewed. Assault casualties over 3000 trials per case: 10.2% killed with no gear, 7.6% with armor 20% (expected 8%), 6.8% with armor and staff (expected 7.2%).

Not verified: real-time Tel'tak runs and 12 minute research end to end, a full gate dispatch and return that earns an artifact through the live UI, a real stronghold assault that drops a wreck (flag checked directly), Safari and touch layouts, narrow screens, sound, long-session balance.

Open action items:
- Review the assumptions above, especially the fixed artifact worlds and weapon assault points averaging.
- Next for 0.5.9: base upgrades (Lab upgrades, extra project slots). Then factions as 0.6.0, and the Sol Defense build (see docs/design/armory-design.md).

### Part three: group missions, Security teams and Peaceful worlds
File: versions/sgc-command-0.5.9.html (same file; design in docs/design/mission-design.md)

New:
- Mission type picker in the gate room (Exploration, Recon Survey, Assault, Assist). The team dropdown only shows teams the type accepts, and the send button checks the composition and target.
- Group missions: all teams sent together are one mission with one mission log entry, one ambush roll (the lowest chance among the teams), one shared delay, and one return. Injuries are still rolled per team. A group goes overdue as one, and contact, recall and assist act on the whole group.
- Overdue only on worlds at Level 2 and above.
- Security team (Air Force Security Forces, raise 25, send 5). On Exploration missions any Security team neutralizes 80% of ambushes. Counts as 95% of a team in assault team size and 95% of weapon points. Uses the Assault weapon line, armor, optics and the staff weapon. Can assist overdue teams.
- Assaults can include an optional Exploration team. Without one, the stronghold's wreck is not recovered at capture and the stronghold is flagged for salvage; an Exploration mission to that captured stronghold recovers it.
- Peaceful worlds: a captured stronghold is Peaceful and has no ambushes (also for MALPs). Badge and intel row show it. Diplomatic missions that make other worlds Peaceful are on the roadmap.

Assumptions I made (flag any that are wrong):
- Security earns camaraderie on an Exploration mission, 10 clean or 5 if injured (same as Recon), and no yield. It also earns camaraderie from assaults like Assault.
- Recon teams in an Exploration mission still survey the world as before; the mission type only limits who can be sent.
- Exploration teams in an assault take casualty rolls like everyone else but earn no camaraderie.
- The Assist type is reserved for rescues: the normal send is blocked while it is selected.
- Salvage of a missed wreck needs a normal Exploration mission to the captured stronghold; the ambush rules there are the peaceful ones (none).
- The group's ambush chance preview in the gate room shows the Recon-adjusted world chance before camaraderie, gear and vehicles, as before.

Verified (headless Chromium, 37 checks plus the earlier 41 re-run): zero console errors. Security raise and roster; picker filtering for each type; group of three teams in one mission record with equal return times; shared ambush; Security neutralization with no injuries; escort log; Level 1 group delayed, not overdue, shared delay 1 to 3 minutes, stale timers ignored; Level 2 group overdue as one with contact and recall acting on both teams; peaceful world with ambush roll forced to zero; assault validity with Security and Exploration; Security at 95% in the team-size score; wreck recovered with an Exploration team, missed and flagged without one, then salvaged; nothing-left block; save and load of a group mission; gate room and Barracks screens reviewed. Assault casualties over 3000 trials per case still match.

Not verified: real-time group timers end to end, an overdue group rescued by an assist team through the live UI, Security neutralizing at the real 80% rate over many trials, Safari and narrow screens.

Open action items:
- Review the assumptions above.
- Roadmap: diplomatic missions that make worlds Peaceful need design questions (who goes, cost, time, odds, faction link) before building.

## 0.5.8
File: versions/sgc-command-0.5.8.html

Galaxy and starmap overhaul (all counts, costs and names decided by Brad).
- Five real star systems, one per level: Alpha Centauri (L1, 4.4 ly), Barnard's Star (L2, 6.0), Sirius (L3, 8.6), Epsilon Eridani (L4, 10.5), Tau Ceti (L5, 11.9). Level 5 is the final level; clearing its strongholds logs a placeholder message because the ending is decided later.
- World counts: L1 5 (1 stronghold, 1 faction), L2 7 (2, 1), L3 5 (3, 0), L4 6 (1, 2), L5 10 (4 strongholds, 2 faction, 1 Ancient Lab). Counts include strongholds and factions.
- Two map layers: galaxy chart (flat star chart with Sol, range rings in light years, hour ticks, Orion Spur band, schematic scale) and orbital system view (star, orbits, planets, moons, stations). Click a star to enter its system; GALAXY CHART button returns. Locked systems show as UNCHARTED dots. Level-up opens the galaxy chart on the new star.
- Worlds have invented names under the real star as sector, with moons and stations named off the parent world (moons and stations appear once the world has intel tier 1).
- Gate power cost is fixed per system: 10, 20, 30, 40, 50 for levels 1 to 5; auto-dial extra cost is a flat 5. Cost follows the destination world, so old systems keep their own cost.
- Live travel paths: each away team shows a route line and marker on both layers. Outbound uses the first quarter of the mission time (first half on the galaxy leg, second half on the system leg); the team then sits at the planet; when the return wormhole is incoming the marker travels back. Overdue teams show a red line.
- Faction planets are dialable placeholders marked FACTION with the faction name (modeled on friendly SG-1 factions: Langaran, Tollan, Tok'ra, Free Jaffa, Asgard, Nox; editable). Diplomacy arrives in 0.6.0.
- Ancient Lab world on Tau Ceti: exploring it records a Pegasus Galaxy gate address (City of Atlantis), shown on the galaxy chart and selectable. The address cannot be dialed; it leaves the story open for a second game.
- Starmap detail panel now sits below the map instead of covering it. Old saves load: worlds are given orbits and kinds automatically.

Assumptions I made (flag any that are wrong):
- Mission timeline is not changed; the path markers are a display of the existing timers.
- Faction and lab worlds count as worlds that must be explored before the final stronghold of a level unlocks.
- The first quarter of mission time for the outbound leg and a return trip lasting the incoming-wormhole time.
- Faction names per level are my placeholders.

Verified (headless Chromium 1440 x 900 to 1000): zero console errors. Counts per level match the table; gate cost 10, 30, 50 at levels 1, 3, 5; auto-dial plus gate spent the right power; team launched through an open gate shows a marker that moves; Atlantis reveal; save and load round trip; old-format world migration. Screenshots reviewed: system view, galaxy chart, Level 5 system with lab.

Not verified: natural-time full mission cycle with return marker, old 0.5.7 save files loaded from real browser storage, touch panning, and Safari.

## 0.5.7
File: versions/sgc-command-0.5.7.html

Interface pass: design, branding, uniformity, readability (all decided by Brad). No game rules changed.
- Settings panel (SETTINGS button in the header, on the title screen and in the game menu, or press S). Accent color: six tested presets (Cyan default, Azure, Violet, Rose, Gold, Silver), each at least 7.9:1 contrast on the panels. Accent reaches the interface only: buttons, borders, headings, room cards, glows and the emblem. The dialing computer and starmap keep their show-style colors. Text size: Small, Normal, Large. Reset to defaults. Settings are saved in the browser separately from game saves and apply on the title screen.
- Full screen: FULL SCREEN button in the header and in Settings, F key. Hidden where the browser does not support it.
- Uniform controls: two control heights only (34 px standard, 28 px compact for toolbars and list rows) for buttons, dropdowns and text fields. Row buttons share a minimum width so they align in a column. Rows share one height and padding. Panels share one padding and gap. Duplicate and dead style rules removed.
- Readability: secondary text raised from 2.7:1 to 5.9:1 contrast. Font sizes now come from four size steps that scale with the text size setting; minimum text size raised from 8 to 9 px to 11 px outside the SVG art. Visible keyboard focus outline.
- Status icons alongside color: good states show a circle, warnings a triangle, danger a square (and the header status badge a matching symbol). The operations log is unchanged.
- HELP and SOUND now show their state with an on/off marker instead of spelled-out text, so the header fits on one row at 1440 wide.
- Active missions strip beside the room tabs on every screen: off-world teams, MALPs away or held, vehicles under repair and the Lab project, each with a live timer. Click a chip to jump to that room. Shows NO ACTIVE MISSIONS when idle.
- Keyboard shortcuts: 1 to 8 jump to a room, B facility, G gate room, F full screen, S settings, Esc opens the menu or closes a panel. Shortcuts are ignored while typing in a field and when Ctrl, Cmd or Alt is held.
- Branding: original hexagon emblem (seven dial nodes over a chevron) in the accent color on the header and title screen, with a wordmark lockup and a divider rule under the title. It is an invented mark and does not copy any show insignia.

Assumptions I made (flag any that are wrong):
- Accent presets avoid green, amber and red so they never read as status colors.
- Header buttons are the compact size; the Facility and Gate Room tabs, send, dial and rush buttons are the standard size.
- The header wraps to two rows at widths under about 1400 px or at Large text.
- Fullscreen is not remembered between sessions; browsers only allow it from a click or key press.

Verified (headless Chromium at 1440 x 900, plus 1280 x 800 and Large text): zero console errors. Control heights measured at 28 and 34 px only on both screens. Settings open from the title screen, accent and text size apply and persist, Escape closes settings then opens the menu then closes it, number keys, B and G switch screens, the strip shows the right chips, mission builder and research tests from 0.5.5 and 0.5.6 still pass. Screenshots reviewed: facility, gate room, settings, title.

Not verified: real fullscreen entry (headless browsers refuse it), Safari, touch devices, and long sessions with a non-default accent.

Moved to 0.5.8: research phase two (Armory equipment, base upgrades, alien technology projects). Factions stay planned as 0.6.0.

## 0.5.6
File: versions/sgc-command-0.5.6.html

Mission builder in the gate room (all decided by Brad):
- The Off-World Teams panel is now the Mission panel. Overdue teams and the send controls stay as they were.
- Three dropdowns replace the JOIN, INCLUDE and MALP buttons: ADD TEAM, ADD VEHICLE, ADD MALP. Each lists only what is not already on the mission. Teams or vehicles that are off-world, standing down or damaged still appear in the list but greyed out with their status.
- Everything added shows in a mission list with a REMOVE button on each row. Team rows show type, send cost, camaraderie, member count and rescue record. Vehicle rows show tier and bonus. The MALP row shows tier, survey tier received and return odds if ambushed. The vehicle bonus summary and assault estimate lines are unchanged.
- Limits unchanged: two vehicles per send (the vehicle dropdown shows VEHICLE LIMIT when full) and one MALP per send.
- An open dropdown is not refreshed away by the panel's automatic updates.

Assumptions I made (flag any that are wrong):
- The panel title changed from Off-World Teams to Mission. The Briefing Room list keeps the Off-World Teams name.
- Unavailable teams and vehicles stay in the dropdowns, greyed out, so their status is still visible. Live return timers are no longer shown in this panel (they remain in the Briefing Room and Barracks).

Verified (headless Chromium at 1440 x 900): zero console errors. Dropdowns list the right items, selecting adds to the list, REMOVE returns items to the dropdown, the third vehicle is blocked at the limit, the MALP dropdown locks once one is added, the focus guard keeps an open dropdown intact, and a mission built from the dropdowns sends and sets the team and MALP away. Screenshot reviewed.

Not verified: native dropdown behavior in Safari and on touch devices, and a team returning through the gate after a dropdown send.

## 0.5.5
File: versions/sgc-command-0.5.5.html
Design record: docs/design/research-design.md

Research mechanic, phase one (all decided by Brad):
- Science Lab runs one timed research project at a time. The Lab panel shows research points, research pace, the current project with a live timer and progress bar, a RUSH button, personnel present, and a MALP upgrades list.
- MALP upgrades only in this phase. Each MALP has its own tier 0 to 5. A project costs research points and supplies up front. Tier 1 to 5: 100 / 200 / 300 / 400 / 500 points, 50 / 100 / 150 / 200 / 250 supplies, 2:00 / 6:30 / 11:00 / 15:30 / 20:00.
- Return odds when ambushed: base 30%, tier 1 to 5 are 20 / 40 / 60 / 80 / 100%. Intel revealed: tier 0 and 1 reveal 1, tiers 2 to 5 reveal 2 to 5. Mission speed unchanged.
- Flat 15% less project time while a scientist or linguist is on station; otherwise base pace. Research never pauses.
- Rush: 20 research points per minute of remaining time, rounded up, finishes immediately.
- A MALP in the Lab is out of service until the project ends (shown as UPGRADING IN LAB in the Motor Pool). A rebuilt MALP starts at tier 0.
- Fifth intel tier added (stronghold defenses). It shows on stronghold worlds only, as exact difficulty and team limit. The starmap intel row now reads x / 5. Recon surveys still reveal 1 to 4.
- Gate room send panel: one button per MALP at home showing its number and tier. The selected button is the unit that launches.
- Mission log and operations log record the MALP number, tier and the survey tier received.
- Lab card status reads RESEARCHING // MALP T# while a project runs. The Lab project and MALP tiers are saved and restored.

Assumptions I made (flag any that are wrong):
- The tier 5 defenses row shows exact difficulty and the assault team limit (twice the level). The assault odds preview already appears in the send panel once teams are selected.
- Rush cost uses the actual remaining time, so the 15% reduction lowers it too.
- Research progress counts only while the game is running, like healing; it does not advance while the game is closed.
- Only one project can run, and a second MALP upgrade cannot be queued behind it.

Verified (headless Chromium at 1440 x 900): zero console errors. Upgrade start deducts 100 points and 50 supplies, scientist pace gives 1:41 of a 2:00 project, base pace applies when the team is away, rush cost 34 points matches the formula, rush completes the upgrade and returns the MALP home, ambushed return odds at tiers 0, 1, 3, 5 follow the table with forced random values, intel 1, 1, 3, 5 revealed, MAX TIER row shows at tier 5, save and load restore the project, the UPGRADING IN LAB status shows in the Motor Pool. Screenshot of the Lab reviewed.

Not verified: a project running to natural completion in real time, the gate room MALP buttons in a real send, narrower windows and touch layouts.

Next: base upgrades (Lab upgrades and extra project slots), Armory equipment, alien technology projects; factions remain planned as 0.6.0.

## 0.5.4
File: versions/sgc-command-0.5.4.html

Facility screen reorganized (layout only, no game rules changed). All decided by Brad:
- Room strip across the top: eight room cards in two rows of four. Top row: Gate Room 28, Briefing Room 27, Barracks 25, Quartermaster 23. Bottom row: Infirmary 21, Science Lab 19, Armory 18, Motor Pool 17. Each card shows name, level, one live status line and staff dots (injured in red). The Gate Room card has a mini gate with live chevrons and wormhole color, the Motor Pool card shows MALP bays. The elevator shaft is gone.
- Full-width room panel below the strip, filled by the selected room. The TEAMS / BARRACKS / STORES side tabs are removed. Operations log stays full-width at the bottom.
- Gate Room panel: gate status, iris toggle, wormhole time left, ENTER GATE ROOM.
- Briefing Room panel: off-world teams with live timers, a DIAL shortcut on overdue teams (sets the destination and opens the gate room), personnel present, and the Mission log with the ID detail view.
- Barracks (new room): team roster, raise-a-team cards, and a team details pane with stats, member statuses, injury timers and REPLACE for killed members. Team names are editable at any time. A member name is editable only while that member is on station (team not away, member not killed or captured).
- Quartermaster (new room): supplies, power, naquadah, research, MALP and vehicle summary, naquadah converter.
- Infirmary: injured members with heal timers, and Maj. Hale.
- Science Lab and Armory: description, personnel, and a COMING LATER placeholder row (research queue, equipment).
- Motor Pool: unchanged content.
- Old saves load fine; an unknown saved room falls back to the Gate Room.
- Fixed: the Infirmary list showed NaN heal time for a frame before the ticker corrected it.

Assumptions I made (flag any that are wrong):
- Barracks and Quartermaster show no staff dots because staff are placed by role and neither room has a role mapped to it.
- Card status lines wording (for example "ALL TEAMS HOME", "NO PATIENTS") is mine.
- The DIAL shortcut in the Briefing Room is disabled while the gate is busy; if the gate is already set to that world it shows GATE ROOM instead.

Verified (headless Chromium at 1440 x 900): zero console errors; all eight room panels render; screenshots reviewed for Barracks and Briefing Room; member name inputs lock when the team is away and when a member is killed, and stay editable for injured members on station.

Not verified: narrower windows and touch layouts, Safari, a full mission cycle through the new panels.

Next: research mechanic design (timed research, queue, what it unlocks) before the 0.6.0 factions work.

## 0.5.3
File: versions/sgc-command-0.5.3.html

Changes from 0.5.2 (all decided by Brad):
- Vehicle upgrade mechanic in the Motor Pool. Three vehicle types, up to 3 of each: Logistic Truck, Unmanned Drone, ATV / Side-by-side. Each unit has its own tier.
- Cost, paid in research points only: BUY 200 (starts at tier 1), upgrades to tier 2, 3, 4, 5 cost 300, 450, 600, 750.
- Per tier effects: Truck +5% yield, Drone -3 points of ambush chance, ATV -10% mission time (capped at 50%) and +3 points on the assault success estimate. A unit's bonuses scale with its tier.
- Gate room send panel lists each vehicle with INCLUDE; up to 2 vehicles per send and the whole group benefits. The panel shows the combined bonus.
- Damage and loss: a vehicle whose send was ambushed returns damaged (repair 10 supplies, 3 minutes). A failed assault loses each vehicle with 25% chance, the rest return damaged. A vehicle returns when the last team of its send is home.
- The mission log records vehicles, damage and losses.
- Data is built so individual parts can be added later: each vehicle holds a parts list whose effects add to the tier bonuses.

Assumptions I made (flag any that are wrong):
- Truck yield raises supplies and the naquadah amount; research and the naquadah find chance are unaffected.
- Bonuses from two vehicles of the same type add together.
- Vehicles do not go on assist missions or MALP-only sends.
- A vehicle is damaged by any ambush on the send, including an ambush the team fights clear.
- Drone ambush cut is subtracted from the chance before camaraderie applies, minimum 0.
- Upgrading needs the vehicle at home; a damaged vehicle must be repaired first.

Verified (headless Chromium): zero errors. Buying and upgrading with research, send with two vehicles (eta cut 20%, yield +15%, assault +6 points), vehicles away then home, ambush damage, repair for 10 supplies, save and reload mid-repair, loss and damage after a failed assault (direct test), screenshots of the Motor Pool and send panel reviewed.

Not verified: a failed assault end to end through the gate, sound, narrow layouts.

## 0.5.2
File: versions/sgc-command-0.5.2.html

Changes from 0.5.1 (all decided by Brad):
- Mission log in the Briefing Room: every Exploration, Recon, Assist, Assault and MALP mission gets an ID (M-0001 and up). Click an ID to open the full record, BACK returns to the list.
- Each record shows: summary (world, hazard, launch and end times, status, flags, result), yield and intel (supplies, naquadah, research, camaraderie gained, intel tier before and after), a timestamped event list (launch, ambush, overdue, radio contact, recall, assist sent, rescue, injuries, returns), and team stats at launch and at return (camaraderie and each member's status).
- Exploration yield now scales with the world's hazard: Low 1.0x, Medium 1.25x, High 1.5x on supplies. The naquadah find chance (60% base) and research (100 base) use the same multiplier.

Assumptions I made (flag any that are wrong):
- Hazard shows in the log as UNKNOWN until the world has intel tier 3 or higher, so the log does not reveal hidden hazard early.
- The naquadah amount (1 to 3) is unchanged; only the chance scales. High hazard gives 90%, medium 75%, low 60%.
- The log keeps the latest 150 missions. A record closes when all of its teams are back home.
- Old saves load with an empty log; missions already under way when upgrading have no record.
- Assault records hold the whole group in one record.

Verified (headless Chromium): zero errors. Exploration on a high-hazard world (research 150, yields recorded), Recon plus MALP launch, overdue, assist with rescue, all four records closed with launch and return stats, log list and detail screens, screenshots reviewed.

Not verified: an assault record end to end, sound, narrow layouts.

## 0.5.1
File: versions/sgc-command-0.5.1.html

Changes from 0.5.0 (all decided by Brad):
- Ambush chances are unchanged (30/40/50% by hazard). An ambushed mission now goes overdue only 1 time in 25.
- The other ambushes: the team fights clear, returns 1 to 3 minutes late, and still rolls for an injured member (same camaraderie-based roll as before).
- Assist teams: the 0.5.0 fix stands (2 supplies each, no assault fee, no stronghold rule). The assist button did nothing in 0.4.6 when supplies were under the team's send cost (8 for Assault); that was silent. 0.5.0 logs a message instead.

Assumptions I made:
- Ambushes that do not go overdue still roll for an injury, as an ambush did before overdue existed.
- The 1 in 25 applies to ambushed regular missions only; an ambushed assist team still goes overdue.

Verified (headless Chromium): 3000 simulated ambushes gave 114 overdue (3.8%); a non-overdue ambush returned 2:00 late and then came due; zero errors.

## 0.5.0
File: versions/sgc-command-0.5.0.html

Changes from 0.4.6 (all decided by Brad):
- Assist missions: after radio contact with an overdue team, Recon and Assault teams (not Exploration) can be sent to assist. Flat 2 supplies per assisting team, no assault fee and no stronghold rule, so it works on stronghold worlds. A rescue only: the stronghold is untouched.
- The assist clears the ambush for certain and rescues the team. The assist teams bring back no yield. The rescued team and the assist teams come home together through the gate (0.4.5 IDC and iris rules).
- A rescued team takes no yield penalty from injuries (no yield cut unless a member is killed). Injured members start healing on arrival.
- Timer pause: the overdue team's 15-minute self-return pauses while an assist is on its way and resumes with the time it had left if the assist fails.
- Assist camaraderie: 1.5x the normal gain (10 base, so +15). A Recon + Assault assist earns 2x instead (+20). The rescued team earns its regular amount. A failed assist earns nothing.
- Assist-only intel on the world by makeup: Recon-only tier 3, Assault-only tier 1, mixed all 4 tiers.
- Assist ambush: 10% for a Recon-only assist (normal Recon reduction and camaraderie apply), 0% when an Assault team is in the group, and 0.5% double ambush.
- Rescue record: each team tracks rescues performed and times rescued, shown in the Off-World Teams panel, the barracks and the hover tip. Milestone rewards come in a later version.
- Barracks: select a team to open its screen with stats, rename the team and each member (press Enter). Roster swaps and loadouts come later.
- Hover over a team in the Off-World Teams panel (including overdue rows) for its stats.
- The send panel shows an assist summary (cost, ambush risk, camaraderie multiplier, intel tier) while assist teams are joined, and the normal SEND is disabled in that case. SEND ASSIST gives a log message instead of failing silently.

Assumptions I made (flag any that are wrong):
- Assist missions take 2 minutes, the standard mission time.
- A failed (ambushed) assist team becomes overdue itself, can be rescued like any team, and does not complete the rescue. The original team keeps waiting and its timer resumes.
- Double ambush means all assist teams in the group are ambushed, even with an Assault team in it.
- Rescued teams get full yield, research and camaraderie as if uninjured.
- Only one assist group at a time per overdue team; recall is blocked while an assist is en route.
- Hover stats use the browser's native tooltip (a short delay before it appears).

Verified (headless Chromium): zero errors. Assault-only assist on a stronghold world (2 supplies, timer paused, rescue, joint return, +15 CAM, tier 1), Recon-only ambushed assist (assist team goes overdue, target timer resumes), mixed assist (tier 4, 2x, +20), save and reload mid-assist, rename of team and member, barracks open and back, hover text on rows. Screenshot of the barracks screen reviewed.

Not verified: real-time waits beyond fast-forwarded clock, sound, narrow layouts.

## 0.4.6
File: versions/sgc-command-0.4.6.html

Changes from 0.4.5 (all decided by Brad):
- New Motor Pool room (Level 17) at the bottom of the facility cutaway. It stores mobile equipment: three MALP bays that show stock and status, and a room panel with each MALP's status, a BUY MALP 25 button, and locked rows for Logistic Truck, Unmanned Drone and ATV / Side-by-side marked COMING LATER.
- MALPs are now a stock: start with 1, hold up to 3, buy more for 25 supplies each. Only one MALP goes through per activation; extras are spares. A lost MALP is removed from stock (buy a replacement). A held MALP is recovered when its stronghold is captured.
- Gate room: the MALP row shows how many are on station and INCLUDE sends one. The starmap and Stores tab show MALPs on station out of stock.
- Old saves load: the single MALP becomes stock of one (a lost one becomes zero).

Assumptions I made:
- The Motor Pool is Level 17 and sits below the Armory.
- Buying is done in the Motor Pool only; the Stores tab just reports stock.
- Vehicle rows are display only, no costs or stats yet.

Verified (headless Chromium): zero errors. Buy to the cap of 3, cap blocks a fourth, one MALP per send, second send uses another, loss removes from stock, return, snapshot of stock. Screenshot of the Motor Pool reviewed.

Not verified: loading an old 0.4.x save, sound.

## 0.4.5
File: versions/sgc-command-0.4.5.html

Changes from 0.4.4 (all decided by Brad):
- Teams now come home through the gate. When a mission ends (normal return, the 15-minute overdue return, a recalled team after its 1:00, or an assault) the team is marked RETURNING // AWAITING GATE and the gate calls in like an unscheduled off-world activation: alert, klaxon, inbound dialing sequence, wormhole.
- The team's IDC transponder arrives partway through. After the IDC shows, opening the iris brings the team through immediately (the wormhole shuts a moment later). Rewards, research and injuries are applied on arrival, not before.
- Teams on the same world that are due together come back in one activation. Assist teams come home with the team they assisted.
- Gate busy: a due return waits for the gate to be idle, same as random activations. The exception: if the open outbound wormhole is to that team's planet, the team returns through it (IDC after about 2 seconds, 14-second window).
- Iris kept closed: the team is turned away, Recon and Assault teams lose 5 camaraderie (Exploration teams have none), and the gate calls again 1 minute later.
- Rewards and the iris: the iris closes automatically when a return activation starts, so the player opens it after the IDC.

Assumptions I made (flag any that are wrong):
- Camaraderie loss for a turned-away return is 5 per Recon or Assault team.
- The iris closes by itself at the start of a return activation. Random unscheduled activations are unchanged.
- Assault teams also come home through the gate after the assault resolves (results apply at once, the team returns later).
- The MALP still returns instantly.

Verified (headless Chromium): zero errors. Return on an open wormhole, return from a dialed incoming, IDC and iris open, arrival applying rewards, turned away with the 1-minute retry, grouped return of three teams, assault return queued. Screenshot reviewed.

Not verified: real-time waits, saving while a return is pending end to end, sound.

## 0.4.4
File: versions/sgc-command-0.4.4.html

Changes from 0.4.3 (all decided by Brad):
- Space reduction: the operations log moved into the left column under the dialing controls in the gate room, and into the right column under the teams panel in the facility view, so neither screen has dead space or a full-width log below. Panel padding and gaps tightened. The dialing computer is capped so it fits the window height.
- Dialing controls: readout on one line, ring buttons and AUTO-DIAL on one centered row, CANCEL DIALING, DISENGAGE WORMHOLE and the iris on a second centered row.
- World intel is now a compact overlay at the bottom of the starmap (name, badges, glyphs, two-column intel, SET DESTINATION), so the starmap panel stays the same size as the dialing computer. The default map view sits the worlds higher so the overlay does not cover them.
- Screens reviewed at 1440 x 900: title, facility (teams, barracks, stores), gate room, menu, incoming alert.

Assumptions I made:
- Level 2 and later maps and the all-levels view can have worlds under the overlay; zoom and pan still work.

Verified (headless Chromium): zero errors; dialing, cancel, MALP send with gate open, 5-minute close and incoming flows unchanged.

Not verified: widths below about 1100 px, mobile, sound.

## 0.4.3
File: versions/sgc-command-0.4.3.html

Changes from 0.4.2 (all decided by Brad):
- Gate room window removed. The dialing computer screen is now the main panel, with the ring, chevrons, wormhole and iris (a grey disc when closed) drawn on it.
- Dialing controls condensed into one panel directly under the dialing computer: destination and alignment readout, ring buttons, LOCK, AUTO-DIAL, CANCEL DIALING, DISENGAGE WORMHOLE, iris.
- Starmap is now a permanent panel on the right, the same width and map height as the dialing computer (both 800 x 560 proportions). Zoom, pan, view toggle and world intel work as before; the world intel sits under the map inside the starmap panel. SET DESTINATION no longer closes anything.
- Off-world teams panel sits directly under the starmap.
- Gate room view uses two equal columns.

Assumptions I made:
- World intel lives inside the starmap panel under the map, which makes that panel taller than the dialing computer. Say if you want the intel moved.
- Escape and the OPEN STARMAP button are gone since the map is always visible.
- The "new worlds" pulse on the map clears once the gate room is opened.

Verified (headless Chromium): zero errors; dial, cancel, open, MALP send with gate staying open, 5-minute close and incoming flows unchanged; starmap select and SET DESTINATION; panel widths 699 px each and map and computer heights match to a pixel. Screenshot reviewed.

Not verified: narrow and mobile layouts, sound.

## 0.4.2
File: versions/sgc-command-0.4.2.html

Changes from 0.4.1 (all decided by Brad):
- Gate room window: lit chevrons glow orange with gradients, light shafts, floor shadow and glow under the gate, rim highlights and bevel, a layered event horizon with brighter rim and bloom.
- Dialing computer is now a show-style screen under the window: DESTINATION header, status text (STANDBY, OUTGOING/INCOMING DIALING SEQUENCE, CHEVRONS ENCODED, WORMHOLE ESTABLISHED, OUTGOING/INCOMING WORMHOLE ACTIVE, DIALING ABORTED), seven result boxes joined by circuit traces to the chevrons (blue idle, red when encoded), a large glyph that flares in the gate center on each lock and flies into its box, left column (clock and date, timer arc, 2x3 stat grid with sparklines, status, 7-row checklist), footer (wormhole countdown, authorization and LST codes, USER and SYS). Incoming wormholes show the inbound glyphs the same way.
- Right column is now Dialing controls (destination, starmap, ring, lock, auto-dial, iris) with separate CANCEL DIALING and DISENGAGE WORMHOLE buttons. Cancel works on manual or auto dials and stops auto-dial.
- The gate no longer closes after sending a team or MALP. Teams can be sent after the MALP through the same wormhole. Recalling an overdue team no longer closes it either.
- Wormhole time limit is 5 minutes (the show's 38, shortened). The footer and arc count down, turning red in the last minute, then the gate shuts down. Elapsed wormhole time is saved with the game.

Assumptions I made (flag any that are wrong):
- Incoming wormholes count down their own short activation timer in the footer, not the 5 minutes.
- Authorization and LST codes are decorative, derived from the dialed address.
- The old glyph strip in the controls panel is hidden, since the new screen replaces it.
- Earlier 0.4.1 assumptions still stand (assist teams only give camaraderie, etc.).

Verified (headless Chromium): zero console errors. Status text across idle, dialing, cancelled, active and incoming. Cancel stops auto-dial and resets chevrons. Gate stays open after a MALP send with the team still sendable. 5-minute close with log message. Elapsed time in the save snapshot. Incoming sequence reaches WORMHOLE ESTABLISHED. Screenshots reviewed: gate room, dialing screen mid-lock and wormhole active.

Not verified: sound, a full 5 minutes in real time, sending a team after a MALP end to end (checked that it is allowed), mobile layout, performance on slow machines.

Open action items:
- Confirm the assumptions above and the open 0.4.1 ones; 0.5.0 questions still stand (tier thresholds, logistics and diplomat costs, faction names, ally bonuses, assist team benefit).

## 0.4.1
File: versions/sgc-command-0.4.1.html

Changes from 0.4.0 (all decided by Brad):
- Title screen: NEW GAME or RESUME. Autosave plus three manual slots (MENU > SAVE, with an overwrite confirm). Autosave runs on changes, every 10 seconds, and when the page is hidden or closed. Timers pause while the game is closed: mission, heal and cooldown time left is saved and restored. Saves live in the browser's local storage. NEW GAME asks to confirm when an autosave exists. MENU also has EXIT TO TITLE SCREEN.
- Assault cost: per-team send costs plus the 150 fee (x1.25 per level above 1). Level 1 with one Assault and one Recon team is 161.
- Recon ambush cut: the first Recon team multiplies the world's ambush chance by 0.9 (low 27%, medium 36%, high 45%), each extra Recon team takes 5 more points off, floor 5%.
- Unsurveyed stronghold, Exploration team: normal ambush roll with Recon and camaraderie applied, no yield or research, stronghold revealed on return.
- Planet names (for example P3X-3456) show under every world on the starmap and everywhere else. Names no longer wait for a MALP survey; type and environment still do.
- Starmap zoom and pan: mouse wheel zooms at the cursor, drag pans, + / - / RECENTER buttons.
- Unscheduled gate activations are rare: one every 20 to 30 minutes, the first no sooner than 20 minutes in. An activation that comes due while the gate is dialing or open is postponed a full interval instead of firing when the gate closes.
- Overdue teams: an ambush that reaches its return time makes the team OVERDUE instead of delaying it. It returns on its own after 15 minutes. The ambush casualty is rolled when the team goes overdue (camaraderie reduces the chance) and is revealed by radio contact.
- Radio contact: an OVERDUE panel in the gate room has a DIAL button that sets the destination to the team's planet. Dial as usual (10 power, auto-dial +6). With the wormhole open, ESTABLISH CONTACT gives a status report, then RECALL (team home in 1:00) or SEND ASSIST (Recon or Assault teams only, normal send cost, they return with the overdue team and each earn 10 camaraderie). The gate closes after the last overdue team on that planet is recalled.
- Casualty rule: an ambushed team with no injury returns with full yield and research. An injured member cuts yield by 30%, earns no research, and stands the team down.
- Declutter: HELP toggle hides explanatory text, header trimmed to two lines, iris control moved into the dialing panel, facility side panels are tabs (TEAMS, BARRACKS, STORES), operations log shortened.

Assumptions I made (flag any that are wrong):
- Assist teams have no ambush and no benefit beyond camaraderie. The "send a message" part of contact is not built.
- Teams on assist or overdue duty are away and cannot take other missions.
- Overdue and assist state survive save and resume; an incoming wormhole in progress and a half-dialed gate do not (the gate resumes closed, open wormholes resume open).
- Saving needs local storage. If a browser blocks it for local files the title screen says saving is unavailable.

Verified (headless Chromium): zero console errors. Title screen, new game, autosave, slot save with overwrite confirm, reload and resume restoring supplies, teams, away timers, cooldown, camaraderie, healing and destination. A mission with 1 second left finished after resume. New game confirm replaces the autosave. Recon risk values for low, medium and high at 0 to 3 Recon teams. Assault total cost 161. Hidden stronghold exploration reveals the stronghold and earns no research. Overdue path: becomes overdue with a 15 minute timer, DIAL shortcut sets destination, contact report, assist dispatch, recall in 1:00, team and assist team return, injury applied, yield cut. Incoming activation postponed with gate open and fires when idle, first activation scheduled 27 minutes out. Screenshots reviewed: title, gate room, facility tabs.

Not verified: real 15-minute overdue timeout and 20-30 minute incoming timing end to end, sound, Safari local-storage saving, touch pinch zoom (buttons work), long-session balance.

Open action items:
- Confirm the assumptions above, and tell me what assist should actually do for the overdue team.
- 0.5.0 rules already settled: four alliance tiers (Contact, Partner, Ally, Sworn; thresholds still to set), faction returns are automatic income at the top tier on a 10-minute cooldown, diplomatic missions run 5 minutes with no ambush (raise and send costs still to set). Open: logistics costs, faction names, ally bonus amounts.

## 0.4.0
File: versions/sgc-command-0.4.0.html
Source of rules: Campaign Logic doc (rev 72) plus the rulings below.

New:
- Levels and gate addresses: Level 1 is 4 addresses with 1 stronghold at difficulty 15. Each later level is 10 addresses with 3 strongholds. Level difficulty is 10% above the previous level, and each stronghold rolls within plus or minus 5% of its level target. Winning every stronghold of a level unlocks the next.
- Final stronghold of a level is locked until every non-stronghold world in that level has had a successful exploration.
- Starmap overlay, opened from the gate room (OPEN STARMAP in the dialing computer panel). Galaxy chart of star dots with a current-level / all-levels view. Select a world for intel, status badges and assault cooldown, then SET DESTINATION to load its address into the dialing computer. Escape closes it. New worlds pulse until the map is opened.
- Intel tiers: 1 name/type/environment, 2 stronghold flag, 3 ambush risk hint, 4 difficulty band. Base MALP reveals tier 1. A Recon survey reveals all four on return.
- Missions follow team type: Exploration (regular worlds only), Recon (any world, surveys), Assault (known strongholds only). Teams can still share one gate activation.
- Assault flow: success % shown before sending (average of camaraderie scaled to 0-100 against the 500 cap, team size scaled against twice the current level, and 100 minus difficulty). Cost is 150 supplies at Level 1, x1.25 per level above 1 (150, 188, 234, 293). 20-minute program-wide cooldown after any assault, win or lose. Assaults take 2 minutes.
- Casualties: a failed assault rolls each member at 10% killed, 10% captured, 25% injured. A win rolls one quarter of those odds. Camaraderie tier modifier reduces all of these relatively. Killed members are replaced for 15 supplies, instantly. Captured members come back after a successful assault on that stronghold. Each killed or captured member costs the team 25 camaraderie. Teams with a killed or captured member cannot be sent.
- Camaraderie: Recon and Assault teams earn 10 per success and 5 per failure, capped at 500, no floor. Tiers at 50, 163, 275, 388, 500 for 5%, 16.25%, 27.5%, 38.75%, 50%. The modifier cuts ambush chance and injury/casualty chance relatively.
- MALP: one unit, free to launch, rides with any group or alone. Return odds 100% unambushed, 30% ambushed. A lost MALP is rebuilt for 25 supplies. On a stronghold it is held until that stronghold is captured. Survey intel arrives at launch.
- World hazard: each world has a hidden low / medium / high rating setting its base ambush chance at 30% / 40% / 50%. Revealed at intel tier 3.
- Research points: 100 per successful exploration return, tracked in the header. Nothing spends them yet.
- Team economics: raise costs are Recon 20, Assault 40, Exploration 80, each extra team of a type 50% of base more. Send costs stay 3 / 5 / 8. Each team type is limited to the current level.

Assumptions I made that were not explicitly decided (flag any that are wrong):
- A stronghold assault costs 150 x 1.25^(level-1) for the whole group, instead of the per-team send costs.
- Recon cuts the ambush chance by 20 points for the first Recon team and 5 for each extra (floor 5%), applied to the world's base chance, instead of setting it to 20%.
- Recon mission counts as a success when it is not hit by a damaging ambush.
- An Exploration team sent to a stronghold that has not been surveyed is treated as a forced ambush: no yield, no research, injury rules apply, and the stronghold is revealed on return.
- A failed or ambushed exploration still pays supplies minus 30% but no research and does not mark the world explored.
- Ambush injury now has a chance of no injury equal to the camaraderie modifier.
- The 0.3.0 rule that Assault teams make ambushes harmless is now inert, since Assault teams only go to strongholds.
- Old levels' non-stronghold worlds remain dialable for repeat exploration. Old strongholds are captured and not dialable for assault.
- Assault camaraderie and team size use the Recon and Assault teams on the mission.
- A MALP launched with Recon teams uses their ambush reduction, no camaraderie reduction, no delay.
- Starting resources unchanged: 60 supplies, 80 power, one Exploration team, one MALP.

Verified (headless Chromium): zero console errors across load, starmap, dial and send flows. Costs 150 / 188 / 234 / 293. Level 1 is 4 worlds with 1 stronghold at difficulty 14 to 16; Level 2 is 10 worlds with 3 strongholds at 16 to 17. Unique addresses. Exploration dispatch, supply cost, research award, explored status. Forced ambush on a hidden stronghold and intel reveal. Exploration blocked on known strongholds. Final stronghold lock and release. Assault estimate (45% single Assault team, 62% with Recon at Level 1). Assault win captures the world, unlocks Level 2, starts the 20:00 cooldown, and the cooldown blocks the next assault. Casualty rates over 3000 trials per case: failed 10.1% killed, 9.8% captured, 25.2% injured; win 2.4% killed, 6.1% injured; camaraderie tier 5 cut killed to 4.8%. Camaraderie tier boundaries. Team limit by level and raise limit block. MALP launch, intel tier 1, loss, rebuild, hold on stronghold, release on capture. Killed-member replacement for 15 supplies keeping camaraderie. Full UI path: starmap select, set destination, auto-dial, join, send. Screenshots reviewed: starmap Level 1 and Level 2, gate room dispatch panel.

Not verified: real 2-minute and 20-minute timers end to end (completion was triggered directly in tests), sound, Safari and touch layouts, long-session balance (starting 60 supplies against a 150-supply first assault is a slow opening).

Open action items:
- Confirm or correct the assumptions above.
- Faction, logistics and diplomacy are the 0.5.0 scope. Equipment list is still open.

## 0.3.0
Teams, costs, ambush and healing rules, first-person gate room. Superseded.

## 0.2.0
Real gate, authentic 7-chevron dialing, iris, incoming wormholes, facility map, audio. Superseded.

## 0.1.0
Text-panel prototype. Superseded.

## 0.9.5 OS TEST (experimental, not a release)
- File: versions/sgc-command-0.9.5-os-test.html (built from 0.9.4 by tools/build-0.9.5-os/patch_095os.py). Not copied to the root.
- Gate Room only: Base Computer workspace with taskbar, windows (Dialer with keys attached, Starmap, World Intel, Mission Planner, Base Log), minimize/maximize, tray, boot screen (click to skip).
- Separate save and settings keys (sgc-os-test-save-, sgc-os-test-settings), so real saves are untouched.
- Open: free drag/resize, tour cards in gate view untested, maximized-map overflow ~11 px, real audio/Safari not tested.
- Awaiting Brad's verdict.

## 0.9.5 (built, NOT released)
- File: versions/sgc-command-0.9.5.html (from 0.9.4 via tools/build-0.9.5/patch_095d.py + dc_build.js). Root game still 0.9.3.
- Gate Room dialing computer redrawn wide (1000x560) in the show's style: black screen, teal frame, red numbered chevron slots with the glyph shown inside, yellow glyphs, Sequence Compiler grid (39 glyphs, lit as encoded), big status readout in the footer. COMM/DRONE stay in the keyboard. Dial screen and keyboard fill the panel width; larger text.
- Starmap fills its panel; world readout is now an overlay on the map.
- Layout fit: stage scale solved iteratively; FIT.min lowered 0.6 to 0.5 so smaller windows still fit without scrolling.
- Active Missions table on the dial screen now lists only off-world teams and groups; the header chip strip shows everything else (MALPs, vehicle repairs, Tel'tak, special ops, logistics, lab) and reads NO OTHER ACTIVITY when idle.
- Mission planner: clicking a mission type advances to Assets.
- Keyboard: COMM 1/COMM 2/DRONE are full key height and row-aligned with the keys beside them. Right side has SEND MALP (MALP alone) and a tall EMBARK key (teams only). The MALP no longer travels with a team send; a MALP sent alone gets no Recon-team ambush reduction.
- Starmap map now fills its whole panel (map aspect follows the panel size). The map rescales to the space above the readout, so a selected planet's details never cover the system. The drone view opens inside the starmap panel instead of full screen; switching to the base view is blocked while a drone is flying.
- Built by tools/build-0.9.5/patch_095h.py + dc_build.js.
- Open: Game Guide screenshots/text still 0.9.3; dropped COMM side-column experiment lives in _to_delete/.

## 0.9.6 (built, NOT released)
- File: versions/sgc-command-0.9.6.html (from 0.9.5 via tools/build-0.9.6/patch_096.py). Root game still 0.9.3.
- Fixed-size panels: Facility room panel, room list and Gate Room Mission panel no longer grow with content. Lists scroll inside the panel; the Ops log is always on screen (Facility log row 250 px, Gate Room log row 275 px, both at stage scale).
- Ops log and Mission Briefing fill their whole panel and scroll inside it.
- Minigames are no longer popups. Reactor re-route runs in the Quartermaster panel, glyph decode in the Archeology Office, Hammond paperwork in the Briefing Room, Carter explanation in the Science Lab, COMM 1 / COMM 2 in the Gate Room dialing computer panel. Drone stays in the starmap panel.
- Navigation: untimed games (reactor, glyph, Carter) park when you pick another room and return when you come back. Timed games lock navigation (Hammond paperwork locks the Briefing Room, COMM locks the Gate Room) until finished or closed, with a warning in the Ops log.
- Behavior change: a reactor power fluctuation or new reactor tier no longer pops a game over everything. The reactor game opens when the player is in the Quartermaster; the existing alert log line says to go there.
- Verified (headless Chromium, build with audio removed; full file confirmed identical apart from audio by hash): zero page errors; room panel constant at 545 px across all nine rooms (Barracks was 717); with 5 FOBs the old build grew the room panel to 1,340 px and pushed the log to y=1508 on a 900 px window, 0.9.6 holds the log at y=716 to 878; checked at 1440x900, 1920x1080 and 1280x720. Reactor, Hammond and glyph games open inside the correct panel, park and return, and are hidden in other rooms. Hammond blocks room and view changes; COMM blocks leaving the Gate Room. COMM and Carter screens reviewed.
- Not verified: Safari and touch layouts; ≤900 px mobile layout; real-time Hammond and COMM play-through; reactor node (tier / ZPM) mode; glyph types 2 and 3; sound.
- Open: Game Guide still 0.9.3 text and screenshots. Not yet confirmed whether the 250 px Facility log row feels right against the Mission Briefing text.

## 0.9.7 (built, NOT released)
- File: versions/sgc-command-0.9.7.html (from 0.9.6 via tools/build-0.9.7/patch_097.py). Root game still 0.9.3.
- COMM contact redesigned as the real hardware, filling the dialing computer panel with no game chrome. Stage 1, tuning: ASTI-style field radio (olive chassis, handles, GPS/USB/J-connectors, yellow-green LCD with scope, signal and battery bars, MHz readout, backlit keypad, rotary knob). Knob (drag or wheel) tunes; arrow keys fine-tune; VOL +/- micro-trim; PRE +/- coarse; CLR aborts. Stage 2, results: compact control unit (color LCD, D-pad, A/B/C/IC/O-R keys). Position fix, sitrep and rescue/recall options show on its LCD; up/down scroll, A/B/C press the first three action buttons, O/R or X closes, BRT keys change LCD brightness.
- Drone interface redesigned after the rugged marine radar display: chassis with handles and screws, scanlined black screen, green phosphor readout boxes (HDG / ALT / SPD / ZOOM), ENVIRONMENT and OWN POSITION (NAV) tables, radar PPI with range rings centered on the drone, rotating sweep with trail, yellow speckled echoes for covered ground, bottom key row (OPTICAL/THERMAL, MOUSE LOOK, PLACE FIX / CONFIRM FIX or END SURVEY / FILE SURVEY / CONTINUE, INFO, ABORT). Operating notes moved behind the INFO key. Camera feed keeps natural optical and thermal colors; its HUD overlay is now green. Feed canvas is 4:3 (was 16:10).
- Verified (headless Chromium, audio-free build, full file confirmed identical apart from audio by hash): zero page errors; COMM 1 tune with keys, knob drag and wheel; lock hands over to the drone; drone rescue and recon modes, optical and thermal, INFO overlay, marker placement, confirm, continue; results appear on the control unit with A/B tags and working scroll; O/R closes; COMM 2 result and signal-lost paths. Screenshots reviewed.
- Not verified: real audio and key clicks, touch input on the knob, Safari, rescue and recall buttons with a live team, tier 0-5 drone range visuals at night.
- Open: Game Guide screenshots of the COMM and drone screens are out of date.

## 0.9.8 (built, NOT released)
- File: versions/sgc-command-0.9.8.html (from 0.9.7 via tools/build-0.9.8/patch_098.py). Root game still 0.9.3.
- Drone interface now sits in an olive rugged display frame with chamfered corners and F-keys, taken from the new reference picture. Left F1-F6: OPTICAL/THERMAL, MOUSE LOOK, PLACE FIX (END SURVEY / FILE SURVEY / CONTINUE by state), CONFIRM FIX, INFO, ABORT. Right F7-F12: ZOOM IN, ZOOM OUT, CLIMB (hold), DESCEND (hold), LEVEL (pitch reset), BOOST (hold). Top F13 HELP (re-shows the controls card); F14-F20 are cosmetic. Bottom row: BRT-/BRT+ change screen brightness, CAM and REC cosmetic, power lamp. The old bottom button row is gone.
- Radar: yellow echo dots removed. Covered ground is now a faint green tint so defender view cones read clearly.
- Verified (headless Chromium, audio-free build, full file confirmed identical apart from audio by hash): zero page errors; F13 help, F7 zoom, held F9 climb, BRT keys; rescue and recon layouts; defender cones visible on the radar in recon.
- Not verified: touch and Safari, key legends at small window sizes, live play with sound.

## 0.9.9 (built, NOT released)
- File: versions/sgc-command-0.9.9.html (from 0.9.8 via tools/build-0.9.9/patch_099.py). Root game still 0.9.3.
- Group rework: Barracks has a Linked groups panel (replaces the per-team link box). Create a group with a name and a 5-character tag, then EDIT it and pick its teams from a list of every team (ADD / IN GROUP). DELETE GROUP removes it. A team can belong to any number of groups. Membership can be edited at any time (a group is only a selection shortcut; it is unavailable while any member is away).
- Tags: every team and group has a required 5-character tag (A-Z, 0-9, uppercase, unique across teams and groups). New teams get EXP01 / REC01 / ASL01 / DIP01 / SEC01 style defaults; new groups default to GRP01 style; both are editable (team: Barracks team details; group: group editor). Bad length or a duplicate is rejected with an Ops log warning. Old saves are backfilled on load (team tag from type and team number, groups GRP01...).
- Mission builder step 2: groups and teams show their tag first. A group is listed for a mission type when every member is eligible. A group with a member away shows greyed with the unavailable tags named; its ready members appear as individual teams. A team in two or more groups also stays listed on its own.
- Dialing computer Active Missions: each row is tag, mission-type abbreviation (EXP, REC, ASL, DEF, AST, DIP) and countdown; the world name was dropped. A mission with groups shows the group tags only (Brad's call; extra single teams are hidden), two groups as AAAAA/BBBBB, more as +N. Ungrouped multi-team missions show the first team's tag +N. Missions store mt and the group tags at dispatch (gtags).
- Verified (headless Chromium, zero page errors): default tags; bad-length and duplicate tag rejected, punctuation stripped; group create with duplicate-tag rejection; add and remove members; Security team in two groups; groups listed per mission type; away member greys the group with the member named; exploration mission with a group sends and shows ALPHA / EXP / 1:58; single Recon team shows REC01 / REC / 1:58; Barracks and dialing computer screenshots reviewed.
- Not verified: two groups in one mission row, assault and assist rows with real missions, save and reload with tags and groups (backfill path with an old 0.9.8 save), narrow window sizes, tag display on other screens (header chips, Briefing Room, mission log still use names).
- Open: tags not yet shown outside the Barracks, mission builder and dialing computer. Game Guide not updated.

## Release (Oct 26 2026): 0.9.9 to root
- Root sgc-command.html and sgc-command.html.zip are now 0.9.9, rolling up 0.9.4 to 0.9.9 (Off-World Operations, wide dialing computer and starmap, fixed-size panels with minigames in their rooms, hardware-style COMM and drone, multi-group teams with 5-character tags and dialing computer rows). 0.9.3 to 0.9.8 moved to versions/archive/. versions/ holds 0.9.9 and the 0.9.5 OS test build.
- Pre-release check: an old-format save (no team or group tags) loads in 0.9.9 and gets tags backfilled, zero errors.
- Game Guide (SGC-Command-Game-Guide.pdf) still describes 0.9.3. Rebuild pending: tools/guide-build/build_guide.py, render.sh run twice.
- Open: verdict on the 0.9.5 OS test build; Easter egg picks; native drop-down replacement picks; minigame hardware treatment for reactor, glyph, Hammond and Carter.

## 0.9.10 (built, NOT released)
- File: versions/sgc-command-0.9.10.html (from 0.9.9 via tools/build-0.9.10/patch_0910.py; question text in tools/build-0.9.10/questions.py). Root game is 0.9.9.
- Archeology Office permanent linguist is now Dr. Daniel Jackson (was Dr. Catherine Langford). Same slot, Level 2 unlock, 150 supplies; glyph hints now carry his name. Saves with Langford hired load as Jackson hired.
- Carter's lab questions: 25 new, 40 total (reactor 8, dialing 8, security 8, MALP 7, armory 9). Researched against series reference pages (gateworld.net wiki, rdanderson.com lexicon, stargate.fandom.com) on naquadah generators and overloads, gate energy and the 38-minute limit, address drift, 39 symbols, matter-to-energy transit, DHD versus dialing computer, iris material and Tollan phasing, radio through the iris, MALP sensors and false relay images, the gate room ramp, zat shots, sarcophagus side effects, transport rings and their range, hyperspace windows. Each has one real answer and three plausible wrong ones. Answer lengths balanced so the real answer is the longest in 10 of 25 (the original 15 were 5 of 15).
- Verified (headless Chromium, zero page errors): 40 questions load, all five categories have 7 or more, every question has 3 wrong answers; Jackson shows in the Archeology Office; hint text; an old save with Langford hired migrates to Jackson.
- Not verified: playing the new questions by hand in the Lab panel; question quality is Brad's read.
- Open: the Game Guide still mentions Langford and has not been rebuilt past 0.9.3.

## 0.9.11 (built and RELEASED Oct 26 2026): Easter eggs
- File: versions/sgc-command-0.9.11.html (from 0.9.10 via tools/build-0.9.11/patch_0911.py). Always on, no setting (Brad's call).
- Staff chatter: a rare idle line in the Operations log, one every 8 to 15 minutes, from Gen. Hammond, Col. Carter, Dr. Lee (only once hired) and Dr. Jackson (only once hired). 4, 4, 3 and 3 lines in original wording. Never during a timed minigame, the opening tour, the title screen or an incoming wormhole; the paused game does not tick. A line is not repeated within the last six.
- Gate address nods: the dialing computer's sequence compiler cells carry hover titles naming the constellation each glyph stands for (39 names, glyph 0 is Earth). The first dial to each world prints an address readout of its six constellations plus the point of origin. Dialing the same world five times in a row gets a Carter remark. The first dial to a system after it is secured notes the addresses are in the permanent record. Seen-flags are saved (eg in the save file; older saves start fresh).
- Verified (headless Chromium, zero page errors): readout, streak and secured lines fire once; chatter only names hired staff; hover titles on all 39 compiler cells and a real hit test on a cell; save round trip and a save without the new field.
- Not verified: how the native hover tooltip looks and how long it takes to appear; chatter pacing over a real session.

## RELEASE Oct 26 2026: root is now 0.9.11
- Root sgc-command.html and sgc-command.html.zip are 0.9.11, rolling up 0.9.4 to 0.9.11: Off-World Operations room, wide dialing computer, fixed-size panels with minigames in their rooms, hardware-style COMM and drone, multi-group teams with 5-character tags, Dr. Jackson, 40 Carter questions, staff chatter and address nods. 0.9.9 and 0.9.10 moved to versions/archive/ with 0.9.3 to 0.9.8 before them. versions/ holds 0.9.11 and the 0.9.5 OS test build.
- Game Guide rebuilt for 0.9.11 (35 pages): Off-World Operations room, fixed panels, tags and linked groups, the dialing computer display and Active Missions rows, SEND MALP and EMBARK, paged Mission Briefing, Tel'tak runs in the Quartermaster, minigames in panels, the radio and the drone console, 40 Carter questions, Jackson, staff chatter and readouts. Source: tools/guide-build/build_guide.py (edit applied by patch_guide_0911.py; the 0.9.3 source is build_guide_093.py.bak). Rendered with render.sh run twice.
- Brad's verdict on the 0.9.5 OS test build: good. Scope for any Base Computer OS (Gate Room only or whole Facility) is still open; the test file stays in versions/.
- Open: Base Computer OS scope; device-style treatment for reactor, glyph, Hammond and Carter; which new minigames to design; Hide the SGC shelved (see docs/design/easter-eggs-design.md).
- Base Computer OS (Oct 26 2026): Brad chose to leave the 0.9.5 OS test as a separate test file. Open item closed.

## 0.9.12 (BUILT Oct 26 2026, not released): Reactor control tablet
- File: versions/sgc-command-0.9.12.html (from 0.9.11 via tools/build-0.9.12/patch_0912.py plus rx_a.js, rx_b.js, rx_c.js, rx_device.css). Rebuild: python3 tools/build-0.9.12/patch_0912.py versions/sgc-command-0.9.11.html versions/sgc-command-0.9.12.html
- The Quartermaster reactor puzzles now run on a rugged tablet (720x540, scaled to fit the panel): screen with header (title, STAGE n / N dots, CORE and GATE feed lamps that flicker red during a power fluctuation), 8 side buttons (up, down, left, right, SEL, ALT, INFO, ABORT), 5 number keys and 3 rotary knobs. Keyboard: arrows, Enter/Space = SEL, Backspace/Delete/X/0 = ALT, I = INFO, 1-5, Esc.
- Six puzzles: conduit Sudoku (old grid, now with cursor and keys), power balance (3 knobs, each output nudged by the previous knob, hold in band), pipe routing (5x4 rotate tiles, SEL clockwise, ALT counter-clockwise, three outputs), breaker sequence (length 4 for events, 5 otherwise, mistake replays), phase match (AMP, FRQ, PHS knobs with a scope), load shedding (7 systems, 2 locked, land in the green band under the cap).
- Fixed pairs as approved: power fluctuation = Sudoku then Breaker; tier I (4) = Knobs then Load shedding; tier II (6) = Pipe then Breaker; tier III (7) = Knobs then Phase; ZPM = Pipe then Phase; restore offline output = Sudoku only.
- ABORT: on a power fluctuation press twice (an output goes offline, same as before); otherwise one press leaves the tablet and keeps finished stages (parked, no penalty). Done screen: preset buttons (keys 1-4, arrows) and CONTINUE.
- The old relay puzzle (rxGenNode, rxNodeLoads, rxPick, rxAssign) is removed.
- Verified headless: all six pairings solved end to end (solver per puzzle), breaker mistake replays, zero script errors, screenshots of every puzzle, help overlay, done screen, small window scaling. Not verified: real touch dragging on the knobs, Safari, Brad's eyes on the feel and difficulty.

## 0.9.13 (BUILT Oct 26 2026, not released): Glyph decode console
- File: versions/sgc-command-0.9.13.html (from 0.9.12 via tools/build-0.9.13/patch_0913.py plus gd_a.js, gd_b.js, gd.css). Rebuild: python3 tools/build-0.9.13/patch_0913.py versions/sgc-command-0.9.12.html versions/sgc-command-0.9.13.html
- Archeology Office decoding now runs on a console (760x540, scaled to fit): teal Message Relay monitor (TRANSLATION MODE_ prompt, status bar UNIDENTIFIED SOURCE! _TRACE, ends on CODE ACCEPTED or TRACE FAILED), a lit artifact tray, six glyph keys, D-pad with ENTER, and BOOK, CLEAR, GIVE UP, CLOSE. Keyboard: arrows, Enter/Space, Backspace/Delete = CLEAR, B = BOOK, 1-6, Esc = close.
- Fragment matching: monitor shows the whole glyphs with a marker; the keypad faces show the six fragments (shards on the tray carry the same numbers); press the key of the matching fragment; D-pad moves the marker. Tablet reassembly: the slab is on the tray as 3x3 tiles, D-pad cursor, ENTER picks then swaps (tiles are also tappable). Cipher: keys put glyphs in the code slots, CLEAR backspaces, ENTER submits.
- Rules, hints, rewards and attempts unchanged. Library book highlights the answer key (or shows the whole tablet).
- System Lord decode bonus (my design, Brad can change): after a decode, if that level's lord stronghold is still unknown, the tray shows the carved seal and the five lord marks (original drawings, not show art) appear on keys 1-5; the right key reveals the stronghold (intel 2), a wrong key or CLEAR gives nothing and costs nothing. Lord of level N = LORDS[N-1].
- Verified headless: all three types won and failed, retry, library, clear, seal pick (stronghold intel 0 to 2), zero script errors, screenshots of every screen. Not verified: Brad's eyes on layout, touch.

## 0.9.14 (BUILT Oct 26 2026, not released): Hammond binder desk
- File: versions/sgc-command-0.9.14.html (from 0.9.13 via tools/build-0.9.14/patch_0914.py plus hp_desk.js). Rebuild: python3 tools/build-0.9.14/patch_0914.py versions/sgc-command-0.9.13.html versions/sgc-command-0.9.14.html
- Briefing Room paperwork is now a desk scene (760x540, scaled to fit): open ring binder with the form on the left page, a checklist on the right page whose boxes tick or cross as you file, four colored tabs (1 Supply, 2 Personnel, 3 Medical, 4 Operations), a red D DENY stamp, a flatbed-style timer, counters, a sticky note carrying the last result in Hammond's name, a pen and WALK AWAY. Keys 1-4 file the form into the tab, D denies, Enter on the result card closes or retries, Esc leaves. Tabs and deny are also clickable.
- Rules, reward (+50 supplies, 2 truck boosts), 90 s timer, 12 forms, 10 correct, fail at the third mistake, cooldown unchanged.
- Verified headless: filing, wrong filing, deny, win (+50 supplies, 2 charges), fail, retry via Enter, number keys and D, zero script errors, screenshots. Not verified: Brad's eyes, touch.
- All four device-style minigames are now built (reactor 0.9.12, glyph 0.9.13, Hammond 0.9.14); Carter stays simple by decision.

## RELEASE Oct 26 2026: root is now 0.9.14
- Root sgc-command.html and sgc-command.html.zip are 0.9.14, rolling up 0.9.12 (reactor tablet), 0.9.13 (glyph decode console with System Lord seal bonus) and 0.9.14 (Hammond binder desk). 0.9.11, 0.9.12 and 0.9.13 moved to versions/archive/; versions/ holds 0.9.14 and the 0.9.5 OS test build.
- Game Guide rebuilt for 0.9.14 (36 pages): tablet puzzles and pairings table, glyph console and seal bonus, binder desk. Source: tools/guide-build/build_guide.py (edit applied by patch_guide_0914.py; the 0.9.11 source is build_guide_0911.py.bak).

## Minigame showcase (BUILT Oct 26 2026, built from 0.9.14)
- File: sgc-minigame-showcase.html in the project root (0.6 MB; the game with music stripped plus a launcher). Rebuild: python3 tools/showcase/patch_showcase.py sgc-command.html sgc-minigame-showcase.html (parts: sc.js, sc.css). Deep links by hash, for example #rx-evt or #gl-3.
- Left menu: reactor jobs (5) and each reactor puzzle alone (6), glyph console (3 types, hint level 0 to 3, System Lord seal step always offered), Hammond binder desk, Carter questions (5 topics), After-Action Report, radio COMM 1, COMM 2, assault recon drone (hazard low, med, high), and a greyed PLANNED list (asteroid run, dig site, card night, raid defense).
- Every button resets to a fresh game state and seeds the scenario (overdue team, open gate, mission to report, and so on). Saves use a separate key, autosave off, incoming wormholes, Easter eggs and music off, so it cannot touch real saves.
- Verified headless: all 24 launchers open the right minigame with zero errors; screenshots of the reactor, glyph, Hammond, Carter, AAR, radio and drone. Not verified: playing each through by hand, Safari, narrow windows (needs about 1200 px width).
- Add each new minigame to SECS in sc.js when it ships.

## 0.9.15 (BUILT Oct 27 2026, not released): balance pass tuning (E, C, B, D)
- File: builds/sgc-command-0.9.15.html (from 0.9.14 via tools/patches/build-0.9.15/patch_0915.py). Rebuild: python3 tools/patches/build-0.9.15/patch_0915.py builds/sgc-command-0.9.14.html builds/sgc-command-0.9.15.html. Source: docs/reports/balance-report-0.9.14.md, picks E, C, B, D.
- E: Reactor I costs 600 RP instead of 1,000 (Reactor II and III unchanged). Median Reactor I lands at minute 65 instead of 101 with the same research order.
- B: Level 4 (Epsilon Eridani) has 2 strongholds instead of 1 (6 planets: 2 strongholds, 2 faction worlds, 2 normal; the lock needs 3 of the 4 non-stronghold worlds explored). Level 4 takes about 58 minutes instead of 23. Saves already past the Level 4 unlock keep their one-stronghold Level 4.
- C: stronghold defense target is 65 on Level 4 and 80 on Level 5 (was 20 and 22 from the 15 x 1.1 per level curve; Levels 1 to 3 unchanged). ATV assault bonus is 2 points per tier instead of 3. Bot odds: Level 4 69%, Level 5 66% for a player who scales groups and uses ATVs; 62% and 58% with no ATVs. Defense alone could not reach the targets: defense carries one third of the odds formula and caps at 100, and two tier-5 ATVs were worth up to +19 points late.
- D: raids: an unanswered raid on a FOB takes half the stockpile (supplies and RP) on top of the garrison losses. Logistic Truck pickup is up to 250 supplies and 125 RP (was one output, 120 and 60). Tel'tak loads at most 400 supplies and 200 RP from a FOB; the rest stays in the stockpile (runs to ordinary explored worlds are unchanged). FOB upkeep is 15 supplies per base every 6:30 from SGC supplies; if the SGC cannot pay, the base produces nothing that interval (UNSUPPLIED shows in Off-World Operations). FOB replacements are one at a time at the SGC replacement cost (15 supplies, with the Free Jaffa free replacement applied); the old bulk button ignored the Free Jaffa perk.
- Numbers I chose and Brad can change: upkeep 15, Tel'tak cap 400 / 200, raid loss one half, Truck 250 / 125, defense 65 / 80, ATV 0.02. Constants: FOB_UPKEEP, FOB_TRUCK_SUP, FOB_TRUCK_RP, TK_CAP_SUP, TK_CAP_RP, DIFF_LATE, VEH.atv.perTier.
- Verified headless: 10 full-game bot sessions all clear with zero script errors; median clear 405 minutes (308 to 493) against 353 for 0.9.14 (extra Level 4 stronghold plus more Level 4 and 5 failures); win and estimate by level in the 0.9.15 section of the balance report. Unit test (tools/patches/build-0.9.15/verify_0915.js): upkeep deducted per interval, unpaid interval produces nothing, raid halves the stockpile, Truck takes 250 / 125, Tel'tak loads 400 / 200, replacement costs 15 each, free replacement sets the per-level flag, Off-World Operations panel shows upkeep, replace button and help text. A 0.9.14 save with 2, 5 and 7 FOBs loads in 0.9.15 with no script errors (CORRECTION Oct 27: the FOB-timers-running part of that check was not valid, the test game was not ticking after load; timers after load were re-checked properly on 0.9.16 with a 0.9.15 save and tick correctly). Not verified: Brad's eyes on the panel text, real raid events with the Defend mission, saves loaded from before Level 4 reaching Level 4, Safari.
- Not changed: dist/sgc-command.html is still 0.9.14; the Game Guide is not rebuilt for 0.9.15 (FOB pickup, Tel'tak cap, upkeep, raids, Reactor I cost, Level 4 strongholds, ATV bonus).

## 0.9.16 (BUILT Oct 27 2026, not released): FOB roles, escalating upkeep, Tel'tak fuel

- File: builds/sgc-command-0.9.16.html (from 0.9.15 via tools/patches/build-0.9.16/patch_0916.py, SHA-256 d9ce6a83...). Rebuild and compare: node tools/patches/build-0.9.16/verify_0916.js builds/sgc-command-0.9.15.html builds/sgc-command-0.9.16.html (prints IDENTICAL). Brad's picks: ideas 2 and 4 from the resource-decisions list, with the recommended options.
- FOB roles, chosen when the base is established: Supply depot 150 supplies / 30 RP per 6:30; Research outpost 60 / 100; Power relay 70 / 40 plus +2 gate power per minute per relay, capped at +8 total (an unsupplied relay gives nothing). Changing a role costs 100 supplies and empties the stockpile. Old bases load as Supply depots. These numbers are mine; Brad picked the structure, not the figures.
- Escalating upkeep: 15 supplies per 6:30 for the first base plus 5 for each base built before it (10 bases = 375 per interval). Total shown in the Off-World Operations header.
- Tel'tak fuel: each run burns ceil(light years / 4) naquadah (2, 2, 3, 3, 3 on Levels 1 to 5) plus the 2 supply fee; the ship will not launch without it, and the button shows the cost. Competes with converting naquadah to gate power.
- Save fix: FOB role and unsupplied flag are now saved and restored (0.9.15 dropped the unsupplied flag on load).
- Verified headless: unit checks (role output, role change cost and stockpile clear, relay cap, escalating upkeep, fuel deducted and launch blocked without it, panel text and buttons); a 0.9.15 save loads with bases as Supply depots, upkeep escalating, FOB timers ticking and the bot finishing Level 5; a 0.9.16 save with mixed roles and one unsupplied base keeps both after load; zero script errors. Full-game bot sessions: median clear 435 min on a role mix, 463 all-supply, 409 power-heavy; naquadah converted about 190 per session against about 70 spent on fuel.
- Not verified: Brad's eyes on the new panel layout, real Defend missions, Safari, long human-speed play. Level 5 assault win rate in these runs was about 58% pooled (156 assaults, noisy) against the 65% target and 71% in the 0.9.15 runs; a Level 5 retune may be wanted.
- Not changed: dist is still 0.9.14; Game Guide not rebuilt (0.9.15 and 0.9.16 changes are not in it).


## 0.9.17 (BUILT Oct 27 2026, not released): hidden worlds and decoded faction contact
Source: builds/sgc-command-0.9.16.html patched by tools/patches/build-0.9.17/patch_0917.py to builds/sgc-command-0.9.17.html. Design: docs/design/hidden-worlds-design.md.

- Seven hidden worlds, each behind its own new artifact (separate from the ten bonus artifacts): L1 Langara (Langaran), L2 Tollana (Tollan), L3 Abydos (story only, no faction), L4 Vorash (Tok'ra) and Chulak (Free Jaffa), L5 Orilla (Asgard) and Nox Haven (Nox). They are extra to each system's planet count and stay off the starmap, dialing and the 75% lock until decoded.
- Finding: each successful Exploration return from a regular world rolls for the next undiscovered hidden artifact at or below the current level (40% first, +30% per miss, so at most the third return). Decode in the Archeology Office with the existing three glyph minigames, under the level tabs in a Hidden worlds list.
- Decode: reveals the world and its address, files faction first contact (shown as "The Archeology Office discovered the ..."), pays a one-time reward (assumed values: Langara 100 supplies, Tollana 120 RP, Abydos 200 supplies, Vorash 150 RP, Chulak 250 supplies, Orilla 250 RP, Nox Haven 300 supplies), and opens a popup with the mini-story, the faction history, tier benefits and Sworn income. READ in the list reopens it.
- Faction leads from Exploration returns (0.8.10) are removed. Faction Relations says to decode inscriptions.
- Older saves: faction worlds already met stay on the map with their artifact marked decoded; unmet faction worlds move to the hidden list (kept visible if a team is bound for them or they are the selected destination); missing hidden worlds for levels already reached (such as Abydos) are added. Saves carry a hidden list; saves from before this build load.

Verified (headless Chromium, full file, zero script errors): new game places Langara in the hidden list and not on the map; the artifact find escalates and is guaranteed by the third return; decode moves the world onto the starmap at intel 2, files first contact, pays the reward and opens the popup; levels 2 to 5 generate six more hidden worlds with visible planet counts unchanged; Abydos reveals as an explorable regular world; save and reload keep the hidden list; an old-format save (faction worlds inline, no hidden list, ten artifact entries) migrates correctly; screenshots of the popup and Archeology Office reviewed.
Not verified: real decode minigame play-through by hand, Faction Relations and starmap look with all seven revealed, a long playthrough, Safari, touch layouts, reward balance.
Open: reward values, find odds, whether the Archeology panel intro text should mention hidden worlds, Game Guide not rebuilt.


## 0.9.18 (BUILT Oct 27 2026, not released): outposts on regular worlds and world events
Source: builds/sgc-command-0.9.17.html patched by tools/patches/build-0.9.18/patch_0918.py to builds/sgc-command-0.9.18.html.

- Outposts, managed in Off-World Operations beside the FOBs. Built on any explored regular world (not strongholds, factions, the lab or the ship). Cost 60 supplies, +20 for each outpost already built. Garrison 4. Upkeep 10 supplies per interval, +3 per level above 1. Delivers straight to base every 6:30 (no stockpile, no Truck), with output set by world type and scaled +25% per level above 1: Temperate forest 45 sup; Arid desert 15 sup + 1 naquadah; Frozen tundra 15 sup + 30 RP; Ocean archipelago 30 sup + 15 RP; Volcanic highlands 10 sup + 2 naquadah; Jungle lowlands 30 sup + 10 RP; Mountain plateau 15 sup + 10 RP + 1 naquadah; Ancient ruins field 45 RP. POST 1 replaces a guard for 20 supplies; ABANDON asks for confirmation. A starmap OUTPOST badge and an Off-World Operations room card (outposts and events) show status.
- Outpost events (random, timed): after each delivery an outpost rolls 15% / 25% / 35% by world hazard for an event with a 2:00 decision window and a default if unanswered. RAID (weighted by hazard): REINFORCE for 40 supplies, or HOLD and lose 0 to 2 guards; at 0 guards the outpost is overrun. TRADER (more on settled worlds): pay 50 supplies for 80 RP, or decline. SITE FOUND (ruins, mountains, deserts): pay 20 supplies to survey for 100 RP, 80 supplies or naquadah, or ignore. TREMORS (seismic worlds): pay 50 supplies or skip one delivery. Costs and rewards scale like output.
- Revisit events: an Exploration team returning from an already explored regular world has a 50% chance of an event on top of the normal yield: supply cache (+35 sup), data (+45 RP, more likely on ruins and mountains), local traders (+1 naquadah), or a Goa'uld patrol (lose 20 supplies, more likely on high hazard). Shown in the return text and yield.
- Off-World Operations now also opens when an outpost exists. Saves carry outposts; older saves load with none.

Verified (headless Chromium, full file, zero script errors): candidate list, build costs 60 then 80, deliveries and upkeep, event creation, REINFORCE cost, timeout default, revisit outcomes and the no-event case for first visits, save and reload keeping outposts, screenshots of the room with outposts and with a pending event.
Not verified: balance (no sim run; numbers are my assumptions, naquadah in particular), real timers over several intervals, a long playthrough, Safari, touch layouts.
Open: output and event numbers, whether outposts should need a Truck or Tel'tak pickup like FOBs, whether raid losses should also cost supplies, Game Guide not rebuilt.

## 0.9.19 (BUILT Oct 27 2026, not released): starmap banner box and dialing computer overlap
Source: builds/sgc-command-0.9.18.html patched by tools/patches/build-0.9.19/patch_0919.py to builds/sgc-command-0.9.19.html.

- Starmap: the empty rectangle near the top of the map was the Level Secured banner element. Its own display rule overrode the hidden attribute, so the empty box (border and padding) showed whenever no banner was pending. Added a hidden rule for map overlays; the box now disappears when there is no banner. The banner content itself already rendered correctly when a level was secured.
- Dialing computer: the left column (Active Missions and the six stat cells) was 250 wide and touched the gate ring and chevrons. It is now 230 wide, with the stat cells 111 wide, the mission text columns and sparklines moved to match, giving a clear gap to the ring. The gate, trace lines and chevron boxes did not move.

Verified (headless Chromium at 1280x700, 2x scale): banner element is display none with no pending banner; screenshot of the dialing computer reviewed, left column clear of the ring. Not verified: a populated mission list at the narrower width (text columns estimated), other window sizes by eye, Safari.

## 0.9.20 (BUILT Oct 27 2026, REMOVED in 0.9.22): Tel'tak asteroid run
Source: builds/sgc-command-0.9.19.html patched by tools/patches/build-0.9.20/patch_0920.py (flight code in tkrun.js beside it) to builds/sgc-command-0.9.20.html. Showcase rebuilt as builds/sgc-minigame-showcase-0.9.20.html (tools/showcase/sc.js has the new TEL'TAK ASTEROID RUN section; patch_showcase.py now matches any build number in the title).

- Quartermaster, Tel'tak Supply Runs: a FLY IT button beside SEND, same availability rules (destination chosen, 2 supplies and the naquadah fuel in stock). It takes over the whole Quartermaster panel (no popup, no title bar; the playfield fills the panel at any size, message and buttons overlay it). SEND still launches at the normal trip length.
- Flight: overhead 2D view (first built as a first-person cockpit, changed at Brad's request: graphics limits). The ship is drawn as the Tel'tak wedge from Brad's reference pictures (bowed delta hull, curved seam bands, engraved gold plating, fanned engine block, glass canopy at the tip); asteroids scroll right to left. The hull has four segments (bridge, fore, cargo, engine); each hit lands on the segment struck and tints it amber, then red. Arrow keys or WASD, or drag in the window; Enter or Space starts and launches, Escape cancels. Cancel costs nothing.
- Result: a clean flight cuts 30% off the round trip; each hit costs 6 points of that (5 hits or more: no cut). Hits never cost supplies. LAUNCH deducts the normal 2 supplies and the fuel and sends the ship with the shortened trip; the log and mission record say the trip was shortened. One flight per launch, no retry.
- Hazard sets difficulty from the destination world: asteroid spawn gap 1150 / 850 / 720 ms and speed 150 / 180 / 200 for Low / Medium / High; 30 seconds; rocks 11 to 25 in radius.
- Ships carry the actual trip length (x.ms) so a reload mid-trip keeps the half-way arrival right for shortened trips.

Verified (headless Chromium, full file, zero script errors): button states, intro, flight, hit counting and per-section damage, result, LAUNCH leaving a ship away with a trip at exactly 70% of base after a clean flight and the cost deducted, no cut after a hit-heavy flight, cancel path, showcase section; screenshots of intro, flight and result reviewed. Dodging bot (keyboard speed, 30 Hz, 15 runs per level) cleared with zero hits 73% / 53% / 27% on Low / Medium / High with the wedge hull.
Not verified: hand play, touch drag, Safari, a reload mid-trip with a shortened run, the showcase at narrow widths (its right edge clips at 1280 wide, as the existing sections do).
Open (my numbers, change freely): 30% cut, 6 points per hit, 30 seconds, hazard densities and speeds. Game Guide not rebuilt.

## 0.9.21 (BUILT Oct 27 2026, REMOVED in 0.9.22): Raid defense
Source: builds/sgc-command-0.9.20.html patched by tools/patches/build-0.9.21/patch_0921.py (game code in rdrun.js beside it) to builds/sgc-command-0.9.21.html. Showcase rebuilt as builds/sgc-minigame-showcase-0.9.21.html (new RAID DEFENSE section in tools/showcase/sc.js; the 0.9.20 showcase moved to builds/archive/).

- Off-World Operations: a base under a raid alert shows a RAID DEFENSE button in its card. The game takes over the whole panel as a rugged tablet (bezel, corner guards, carry strap and side button column modeled on Brad's photo); the keys along the bottom are the controls.
- Play (modeled on Canyon Defense, Brad's reference): overhead view of a winding canyon road leading to the base. Four waves of Jaffa infantry, heavy Jaffa and Death Gliders (gliders fly straight to the base, ignoring the road). Build on the rock beside the road: GUN NEST 40 coins (ground and air, short range), MORTAR 75 (ground only, splash, long range), AA BATTERY 60 (air only). Up to three upgrade levels per defense (70% of cost each: +50% damage, +10% range, faster fire); sell returns 60% of what was paid. Kills earn coins (6 / 14 / 9), +20 coins between waves. Keys: 1 to 3 pick a defense, click rock to build, click a defense to select it, U upgrade, S sell, SPACE start or skip to the next wave, P pause, F fast, Esc deselect or quit. Side buttons: WAVE, PAUSE, FAST, QUIT.
- Starting coins follow the garrison: 80 + 12 per fit defender (200 at 10, 128 at 4). The world's level scales the waves (raider counts and +18% health per level above 1).
- Outcome (my recommendation, applied as the default): the base has 10 breach points; each raider that reaches it costs its leak value (1, or 2 for heavies). Zero breaches: raid repelled, no losses, the raid timer restarts. Otherwise the standard raid (garrison casualties and half the stockpile) is applied scaled by breaches / 10; 10 breaches is the full standard raid. Ops log records the result.
- Quit rule: the alert timer is frozen while you play. Quitting returns to the alert with its remaining time; you can retry, send a DEFEND team, or let it expire into the standard raid. A finished game ends the alert.
- Save compatibility: nothing new is saved. fobRaid(w, fr, pre) gained two optional arguments; the old call is unchanged.

Verified (headless Chromium, full file, zero script errors): button appears only under an alert with the lord alive; open, mouse and key placement, upgrade, selection, wave flow, kills and leaks, finish with zero breaches (repelled) and with ten (full standard raid: 2 wounded 1 killed, half stockpile lost at full strength), alert frozen while playing and kept on quit, Enter and Esc handling, showcase section, switching minigames closes it; screenshots of the open tablet and live play reviewed. Greedy bot (places by path coverage, 6 runs per cell) leaks 0 / 0 / 0 / 0 / about 3 at full garrison on Levels 1 to 5, and about 0 / 0 / 1 / 3 / 10 with a garrison of 6.
Not verified: hand play, touch, Safari, balance by people, a reload during a game (a game is not saved), the showcase layout (its right edge clips at common window sizes, as the older sections do).
Open (my numbers, change freely): coin costs and starting coins, wave sizes and health scaling, 10 breach points, 60% sell value, +20 wave bonus.


## 0.9.22 (BUILT Oct 28 2026, not released): Tel'tak asteroid run and Raid defense removed

File: builds/sgc-command-0.9.22.html (21.8 MB). Rebuild: python3 tools/patches/build-0.9.22/patch_0922.py builds/sgc-command-0.9.19.html builds/sgc-command-0.9.22.html

Brad's request and decisions: take the asteroid run and Raid defense minigames out of the game. Build from 0.9.19 under a new number (0.9.20 and 0.9.21 held only those two games, so nothing else is lost). Raid alerts go back to the 0.9.19 rules. Dig site brushwork and Mess hall card night are dropped from the plans as well.

Changed:
- 0.9.22 is 0.9.19 with the build number changed (title, banner, BUILD_VER). Checked: with the version string normalised it is byte for byte the same file as 0.9.19.
- Tel'tak supply runs: SEND only, no FLY IT button, no 30% flight cut.
- FOB raid alerts: no RAID DEFENSE button. Answer with a Defend mission, or the garrison fights alone and the raiders carry off half the stockpile. The scaled-by-breaches loss rule from 0.9.21 is gone.
- Showcase (builds/sgc-minigame-showcase-0.9.22.html): the two sections and the PLANNED list are removed from tools/showcase/sc.js. patch_showcase.py now matches any build number in the title.
- 0.9.20 and 0.9.21 files, their patch folders and the 0.9.21 showcase moved to builds/archive/removed-minigames/ (local only, not in git) in case they are wanted again.

Verified (headless Chromium, audio stripped): game and showcase both load with zero script errors and report 0.9.22; no tkgame, rdgame, tkFly, rdOpen, tkClose or rdClose anywhere in either file; Quartermaster shows SEND and no FLY IT, and SEND puts the ship away; a FOB under a raid alert shows RAID in Off-World Operations and no RAID DEFENSE button; an unanswered raid removes half the stockpile (400 to 200 supplies, 100 to 50 RP). Showcase sidebar lists the existing sections only.
Not verified: loading a save made in 0.9.20 or 0.9.21 (they added no saved fields; a Tel'tak ship may carry a spare ms value that 0.9.22 ignores), Safari, hand play.
Game Guide: not rebuilt, and it never mentioned either game.


## 0.9.22 RELEASED to root (Oct 28 2026): batch 0.9.15 to 0.9.22

- dist/sgc-command.html is build 0.9.22 (copied from builds/sgc-command-0.9.22.html), dist/sgc-command.html.zip rewritten (zip contents compared byte for byte with the html). Builds 0.9.14 to 0.9.19 and the interim showcase moved to builds/archive/; leftover test files from builds/_to_delete/ moved to builds/archive/removed-minigames/_to_delete/ (local only).
- dist/sgc-minigame-showcase.html rebuilt with tools/showcase/patch_showcase.py from dist/sgc-command.html; byte for byte the same as the 0.9.22 showcase verified earlier. No trace of the removed minigames in either file.
- Game Guide rebuilt: tools/guide/patch_guide_0922.py applied to build_guide.py (build 0.9.22, 38 pages, was 35). Updated: Reactor I 600 RP, Level 4 second stronghold and lock count (3 of 4), hidden worlds and decoded faction contact (faction leads removed), revisit events, FOB roles, upkeep, Truck and Tel'tak caps, raid stockpile loss, replacement, Tel'tak naquadah fuel and SEND only, outposts with output table and events, ATV bonus +2, hidden-world table in the Archeology section, quick-reference rows. Contents page numbers settled over two renders and checked. Pages 19 to 21 and 35 reviewed as images.
- Guide values mirror the shipped numbers. The open items (hidden-world rewards and odds, outpost numbers) are in it as they are today; a change to any of them needs a Guide refresh.
- Not verified: the Guide text against hand play of every new screen, Safari, saves from 0.9.20 and 0.9.21 in 0.9.22.


## 0.9.23 (BUILT Oct 28 2026, not released): assault cooldown 15 minutes

File: builds/sgc-command-0.9.23.html (SHA-256 426274cf...). Source: builds/sgc-command-0.9.22.html patched by tools/patches/build-0.9.23/patch_0923.py. Rebuild: python3 tools/patches/build-0.9.23/patch_0923.py builds/sgc-command-0.9.22.html builds/sgc-command-0.9.23.html

- Balance pick A, Brad's call: the assault cooldown is 15 minutes on every level (was 20). ASSAULT_CD_MS and the assault result text ("Assault cooldown started: 15:00.") changed; the build number is the only other difference (line diff against 0.9.22 shows six changed lines).
- Level 5 retune: Brad asked for it, targeting about 65%. Not applied: 30 bot sessions on this build's rules (0.9.22 with the 15 minute cooldown, Level 5 difficulty still 80) won 66% of Level 5 assaults (182 assaults) against a shown estimate of 63%, so Level 5 is on target. The 58% in the 0.9.16 runs was sampling noise plus role-plan differences.
- Bot results, 30 full-game sessions (scaleTeams and atv on, roles default), zero script errors, all 30 cleared: median clear 392 minutes (259 to 546) against 405 on 0.9.15 and 435 on 0.9.16 with the 20 minute cooldown; level minutes median 45 / 54 / 86 / 60 / 130. Win rate and shown estimate by level: L1 68% / 73% (44 assaults), L2 67% / 66% (89), L3 64% / 69% (140), L4 64% / 64% (94), L5 66% / 63% (182). Reactor I at minute 69. Unspent at clear: 2,029 supplies, 11,509 RP. Unanswered raid checks 4.3 per session, no overruns.
- Picks F (gear costs) and G (extend bot) were declined by Brad. Hidden-world and outpost numbers confirmed as shipped.
- Not done: Game Guide (still 0.9.22: its quick reference says 20 minutes), dist, commit.
- Not verified: hand play, Safari.

## 0.9.23 RELEASED to root (Oct 28 2026)

- dist/sgc-command.html is build 0.9.23 (zip rewritten and compared byte for byte), 0.9.22 moved to builds/archive/, showcase rebuilt from the new dist file, Game Guide rebuilt with tools/guide/patch_guide_0923.py (build number and the quick-reference assault cooldown, 20 to 15 minutes; 38 pages, contents unchanged). Committed and tagged v0.9.23.
