# Minigames - Design (draft, decisions from Brad)

Status: design complete (numbers approved by Brad). Build in progress; see build-status.md.

## Chosen minigames
1. Glyph decoding (Linguist) - mandatory
2. Reactor power routing - mandatory
3. Radio contact for overdue teams - mandatory
4. Hammond's paperwork - optional
5. Carter's techno-babble - optional (chosen from the second idea list)

Not yet picked from the second list: assault breach planning, intercepted Goa'uld transmissions, defend mission, archaeological dig, pack loading, sector sweep, naquadah refining, logistics dispatch, training room, poker night, Teal'c sparring, Walter's iris check.

## 1. Glyph decoding
- Collection of 10 artifacts, 2 per level, separate from the existing alien tech artifacts (healing device, Jaffa staff, reserved later ones).
- Mandatory: an artifact can only be collected by decoding its inscription.
- Not used for the Ancient Facility (Level 5). The facility may have hints about it, but decoding must not affect it.
- Inscriptions: per level, one comes from a fixed world and one from a chance find on an Exploration mission elsewhere in the level. Chance find: base 5%, rising 15% per Exploration mission in the level that does not find it.
- Decoding happens in a new room card, the Archeology Office. A Linguist must be on station to decode.
- Puzzle types: 1 fragment matching, 2 tablet reassembly, 3 cipher deduction. Rotation across artifacts 1 to 10: 1, 2, 3, 2, 3, 1, 1, 2, 3, 2 (two artifacts on a level always use different types).
- Attempts: unlimited, no penalty.
- Hints: three text hints per inscription, unlocked by failed attempts. A Linguist on station can also consult a book in the library that shows a visual hint.
- Result of a successful decode: the artifact's world is revealed. A second Exploration mission recovers it. Some artifacts lead to worlds with discoverable alien technology (example: a crashed Goa'uld glider used to reverse engineer the X-302).
- Level rewards (table approved by Brad):
  - Level 1: +15% supply yield for Exploration teams. Artifact leads to no alien tech world.
  - Level 2: +10% research point yield. An artifact leads to a crashed Death Glider (X-302 reverse engineering).
  - Level 3: lower ambush chance for all teams. An artifact leads to a Goa'uld fleet beacon (feeds the Sol Defense intel).
  - Level 4: faster Infirmary healing or lower assault injury odds. An artifact leads to Tollan or Ancient defense tech (Ion Cannon path).
  - Level 5: gate power regeneration boost. Hints only toward the Ancient Facility, which decoding must not affect.
  - Final bonus for all 10: permanent +10% camaraderie gain for all teams, plus a named relic that sits in the Archeology Office as a trophy with a small bonus attached. Relic (approved): Ancient Repository Stone, +5% research yield.
  - Approved values: Level 3 ambush chance -5 points for all teams; Level 4 assault injury and casualty odds -10% (stacks with armor); Level 5 gate power regeneration +6 per minute.
- Library books: already in the Archeology Office and free to use. The only requirement is a Linguist on station (visual hint is available on top of the three text hints).

## Permanent personnel (new)
- Named staff from the show, separate from team members.
- Lab (changed by Brad): two permanent slots. Col. Samantha Carter is on station from the start at no cost (and is the ASK CARTER source). Dr. Bill Lee takes the Level 4 slot (400 supplies). Dr. Jay Felger is removed.
- Archeology Office: one permanent slot, unlocking at Level 2: Dr. Daniel Jackson.
- A permanent Lab specialist always counts as a scientist on station; the Archeology Office specialist always counts as a Linguist on station.
- Filling a slot costs supplies: Archeology Office Level 2 150, Lab Level 2 200, Lab Level 4 400.

## Room card cleanup (new)
- Remove the personnel and team member lists from the room cards entirely. Cards get narrower, giving more of the screen to the selected room's info card.
- On-station staff show on the selected room's panel only. OPEN: narrower card layout.

## 2. Reactor power routing
- Mandatory. Split reactor output between gate, lab and shields with a Sudoku-style constraint.
- Pairs with the regeneration tiers (12/24/36/48 per minute) and the ZPM install.
- Trigger: rare power events, plus installing a Reactor tier or the ZPM opens the routing screen.
- Outputs: more power to the gate gives faster power regeneration, to the Lab a faster research pace, to the shields reduced losses from Goa'uld raids and ambushes.
- Puzzle: conduit grid (rows and columns carry set totals) for power events; node routing (relay nodes with capacity limits) for Reactor tier and ZPM installs.
- Events are tied to gate use: a power event can occur after 10 plus a random 1 to 5 gate activations (11 to 15, confirmed by Brad). The count to the next event starts when the minigame is completed.
- Consequence: an unanswered event knocks one output offline, chosen at random among the three but never the one boosted by the current preset, until the player re-routes.
  - Gate offline: power regeneration stops; the gate stays dialable.
  - Lab offline: running research pauses.
  - Shields offline: no reduction until fixed.
- Result: solving unlocks preset splits for the player to choose from. Balanced: all three at base. Gate-heavy, Lab-heavy, Shield-heavy: +50% on the chosen output, -25% on the other two. The player can change preset at any time at no cost.
- Shields (minimal version): a single reduction on ambush injury odds and Goa'uld raid losses (the 0.6.15 raid events). A fuller shield system waits for the Sol Defense build.
- Shield reduction: -10% at Balanced, -15% at Shield-heavy, -7.5% at the other two heavy presets (approved).

## 3. Radio contact for overdue teams
- Mandatory. Tune through static and triangulate the team's position.
- COMM 1 (new key on the dialing computer keyboard): emergency frequency used only for overdue teams. Opens the full minigame.
- COMM 2: for any team that is not overdue; used to recall the team early. It replaces the separate Recall key: a simple tune-to-frequency task, then a recall prompt. Recall needs contact first, returns the team home in 1 minute, and the team brings back 80% of the full yield for the planet.
- Flow: a team goes overdue; the player dials the planet; wormhole established; the player presses COMM 1; plays the minigame; once radio contact is established the team gives a sitrep explaining why they are overdue.
- Ambushes and similar events must not appear in the OPS log before contact is established. The only way to check a team's status is to establish radio contact after dialing the planet. On contact, the log records the sitrep only; full details appear in the mission log when the team returns.
- The 5-minute wormhole timer keeps running during the minigame; running out closes the gate and the player must redial.
- COMM 1 puzzle: tune the dial to lock the signal out of static, then take bearings from stations to pin the position (Brad asked which is more fun; this is Claude's pick).
- Result: scored accuracy of the triangulation affects the assist mission: assist travel time, rescue result, and intel gained.
- Rescue teams (Special Operations) still need no radio contact.
- Overdue definition (Brad): a team is flagged overdue 3:30 past its scheduled return time. The 1 to 3 minute ambush delay clears before that, so only stuck teams (the existing 1-in-25 ambush outcome) cross the line. A team ambushed and stuck on the planet needs the full minigame to triangulate its position(s) so the rescue or assist team can find it quickly. Teams in one group share one fix.
- The existing 15-minute self-return timer starts when the team is flagged overdue (confirmed by Brad).
- Accuracy bands (approved by Brad), fix error measured against the search area:
  - Pinpoint (within 10%): assist travel 1:00, rescued team full yield, assist full intel tier set plus one extra tier (max 5).
  - Good (10 to 30%): assist travel 1:30, rescued team 90% yield, full intel tier set.
  - Rough (30 to 60%): assist travel 2:00 (base), rescued team 80% yield, intel tiers reduced by one.
  - Poor (over 60%, or no fix): assist travel 3:00, rescued team 70% yield, no intel from the assist.
- Difficulty scales by world hazard rating (approved, steep): low gets a small search area and light static, medium about 2x the area, high about 3x the area with heavy static.

## 4. Hammond's paperwork
- Optional. Stamp the right forms against the clock while requisitions pile up.
- Launched from the Briefing Room.
- Rules: each form has a type (supply, personnel, medical, ops) and the player picks the matching stamp; some forms have a flaw (wrong amount, missing signature) and must be denied instead.
- Success is a threshold: stamp enough forms correctly before the clock runs out for the full reward. On failure the player can retry with no cooldown.
- Reward (revised by Brad): 50 supplies, and the next 2 missions that include a Logistic Truck carry 75% more supplies, provided they are launched within 15 minutes of finishing the minigame; unused charges are lost when the window ends. This replaces the earlier +90% team yield boost; there is no team selection.
- The 75% adds to the truck tier bonus (+5% per tier, so a tier 3 truck gives +90%) and raises the carry cap by the same amount.
- Cooldown: 10 missions, counted from missions launched after the minigame finishes.
- Numbers (approved): 12 forms, 90 seconds, 10 correct to pass with 2 mistakes allowed; flaw types wrong amount, missing signature, wrong department, expired date; any mission launched counts toward the cooldown.

## 5. Carter's techno-babble
- Optional.
- Trigger: each active Lab project has an optional ASK CARTER button, available on any project.
- Format: one question per play. Carter gives four explanations of the project; one is real science from the show's world and three are plausible nonsense. Pick the real one.
- Reward: a correct answer gives a bonus on completion, a flat payout that scales with the project's tier; the project finishes normally and pays the bonus when done.
- Wrong answer: a small setback; the nonsense answer sets the project back slightly (a short delay), so guessing has a cost.
- Cooldown: 20 missions.
- Payout (approved): research points only, 25/50/75/100/125 by tier 1 to 5; one-off projects count as tier 3.
- Setback (approved): 10% of the project's total time, rounded up to 30 seconds.
- Cooldown counter is separate from Hammond's paperwork.

## After-Action Report (typing minigame) - decided 2026-10-24/25, not built
Decided:
- Optional. Briefing Room mission log: select a finished mission, press COMPLETE AAR.
- Layout: AAR entry box on the left side of the room info card; mission details stay visible on the right while typing (transcription task).
- Team before/after status removed from the mission log detail view.
- Eligible: base mission types only (Exploration, Recon Survey, Assault, Assist). Not MALP, Tel'tak runs, diplomacy or defend.
- Real English, typed from the visible log: mission type, date and time, team name, world, outcome (injuries, casualties), yield and intel gained.
- One report per mission, no overall cooldown.
- Reward: camaraderie (teams that earn it), research points, supplies, scaled by accuracy and speed against a par time.

Finding: camaraderie is capped at 500 (tiers at 50/163/275/388/500); Exploration and Diplomatic teams do not earn camaraderie in the game; assault win +10, loss +5, assist 15 or 20.

Approved 2026-10-25 (tiers and numbers):
- Par time = report length at a fixed typing pace; no hard time limit.
- Excellent: 95%+ accuracy and at or under par. Standard: 85%+ accuracy within 2x par. Rough: 70%+ accuracy, any time. Below 70%: no reward, free retry on the same mission.
- Rewards Rough/Standard/Excellent: supplies 5/10/15, research points 5/10/15, camaraderie +2/+4/+6.
- Who gets what: research points go to the Exploration team on the mission; camaraderie goes to the other teams attached to that mission (Recon, Assault, Security). Exploration teams earn no camaraderie.
- Assumption (to confirm): supplies stay a flat payout for the mission regardless of team makeup.

Built in 0.8.2. Fields as built: mission type, launch time, return time, team names, world, injuries, casualties, yield, intel tier. Pace for par is 35 words per minute (assumption). The log shows times only, so there is no date field.

Changed in 0.8.3: no time limit and no par pace. Reward tier is by accuracy only (95/85/70 percent bands), below 70 percent is a free retry.

## COMM 1 Reconnaissance Drone (built 0.8.4; supersedes the triangulation in section 3)
- COMM 1 tuning stays. After the lock the player flies the drone: free flight, no sectors and no move budget, running on the wormhole clock. Signal strength rises with proximity to the team; hazard sets the help (low marker, medium drifting marker and haze, high strength only).
- Lock the heat signature with the reticle for a guaranteed Pinpoint, or place a marker on the radar. Bands by distance: 30 m, 80 m, 160 m, beyond. Band effects as in section 3 (assist travel 1:00 / 1:30 / 2:00 / 3:00, yield 100 / 90 / 80 / 70%, intel +1 / full / -1 / none).
- Drone tier is the best Unmanned Drone at home (tier 0 basic when none): sight 1/1/1/2/2/3, zoom 2.0 to 5.0x, speed 14 to 42 m/s.
- Assault recon (DRONE key): tag all contacts in a stronghold (5/7/9 defenders and 1/2/3 patrols by hazard, plus 3 structures); exposure in patrol cones ends the flight. Full picture -15% strength and intel 5; 70% or more -10% and intel 4; 40% or more -5%; below 40% none. Spotted: reduction halved, no intel, alerted (-10 points on assault success). Strength reduction scales the difficulty term of the assault odds. Results clear when the next assault is sent. Cooldown 5:00 after a filed survey; no permanent drone loss.
- Later (not built): overwatch tagging during an assault, landmark scanning (see drone-scanning-story-design.md).
- Spotting (0.8.5): exposure build 0.05 + 0.10 x speed + 0.06 x altitude per second inside a cone, recovery 0.30 per second, defender view ranges tower 75 m, guard 52 m, patrol 56 m; amber DEFENDER NEARBY warning with a slow tick when nearing a cone.


## 0.8.6 recon odds (replaces the difficulty reduction)

Assault recon adds points to the final assault success: all contacts tagged +15, 70% or more +10, 40% or more +5, under 40% none. A spotted drone halves the bonus (rounded down) and the defenders-alerted penalty of -10 points still applies. Intel rules and the 5-minute cooldown are unchanged. Tour, briefing tab and base computer notes: docs/design/tour-cards.md.

## New minigame ideas, round 2 (Oct 26 2026, awaiting Brad's picks)
Still open from round 1: MALP drive, Infirmary triage, Motor Pool diagnostics, IDC verification.
- Tel'tak asteroid run (Brad's idea): optional on a supply run, fly the ship through an asteroid field and dodge; score shortens the run. Proposal: arrow keys or touch drag, 30 s field, density scales with destination hazard, finish clean for the biggest cut (about 30% off the trip), hits cost time bonus only, never supplies; cockpit styled like the other devices.
- Cargo hold packing (Quartermaster): fit crates into the Tel'tak hold, tight pack raises the run's supply carry.
- Chevron rhythm (Gate Room): lock chevrons on the beat to shave dial time.
- Beacon sweep (Operations): tune a radio sweep to find a lost team's beacon, improves rescue odds.
- Dig site brushwork (Archeology): brush dirt off an artifact, relaxing, small research reward.
- Envoy dinner (Briefing Room): pick answers that fit a faction's character for reputation.
- Mess hall card night (Barracks): low-stakes cards for a camaraderie bump.
- Raid defense (Operations): place turrets on a Forward Operating Base during a raid alert.
- Target range (Armory): zat and staff shooting range for a small morale or training reward.

## Planned future minigame update (Brad's picks, Oct 26 2026)
Update Oct 28 2026: the asteroid run and Raid defense were built (0.9.20, 0.9.21) and then removed in 0.9.22; Dig site brushwork and Mess hall card night are dropped. This section and the Raid defense notes below are history only.
- Tel'tak asteroid run (Brad's idea): optional on a supply run, fly through an asteroid field and dodge; proposal above (about 30% off the trip, hits cost time only).
- Dig site brushwork (Archeology Office)
- Mess hall card night (Barracks)
- Raid defense (Operations, Forward Operating Base raids)
Not picked, kept on the list: cargo hold packing, chevron rhythm, beacon sweep, envoy dinner, target range, MALP drive, Infirmary triage, Motor Pool diagnostics, IDC verification.

## Raid defense (built 0.9.21, Oct 27 2026)
Brad's reference: Canyon Defense (overhead tower defense, enemies on a canyon road, turrets on the rock beside it, coins from kills). Display: rugged tablet from Brad's photo. Triggered from a FOB raid alert in Off-World Operations. Waves, defenses, outcome mapping and quit rule are in CHANGELOG.md under 0.9.21. Open numbers are listed there.

