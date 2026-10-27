# Drone Scanning and Storyline - Design (DRAFT)

Status: draft for Brad to react to. Nothing here is built. Decisions marked (Brad) were chosen by him; everything else is a proposal.

## Scanning (decided direction)
- (Brad) Landmarks seen by the Reconnaissance Drone can be scanned to reveal finds.
- (Brad) Find types: alien tech and artifacts, story clues, mission intel, and resource caches (supplies and/or research points, recovered by a follow-up mission).
- (Brad) Scanning is available in both drone scenarios: rescue flights (COMM 1) and assault recon.
- Proposal: scanning is optional and costs wormhole time (the clock is the only time factor). One or two scannable landmarks per flight, so rescue stays the priority.
- Proposal: scan by holding the reticle on a landmark, the same dwell as tagging a contact.
- Proposal: the telemetry strip carries hints. Radiation rises near an energy source or artifact; pressure and O2 shift near a sealed structure.
- Proposal: finds are fixed per world and saved, so a find stays found. Discovered sites show on the starmap and become follow-up missions (Exploration to recover a cache, Assault or Recon where a stronghold holds it).
- Proposal: higher drone tiers and the planned Sensors part widen scan range and detail.

## Delivery of story finds (Brad: both)
- A short result appears at scan time ("Ancient marker, partial chart").
- The full decoded entry arrives later from the Archeology Office. Dr. Daniel Jackson decodes (she counts as a linguist). Dr. Jay Felger was removed from the game, so he is not used.
- Tech finds go to the Lab for Col. Carter and Dr. Lee (existing reverse-engineering model).

## Storyline spine (Brad: C, both threads braided)
Draft outline, for Brad to edit.

Thread 1, the Ancient trail (quiet mystery):
- One Ancient clue site per level, each decoded into a fragment: Level 1 Alpha Centauri, Level 2 Barnard's Star, Level 3 Sirius, Level 4 Epsilon Eridani.
- Fragments point toward Level 5 Tau Ceti, where the existing Ancient Lab holds the gate coordinate to Atlantis (Pegasus galaxy). The existing reveal on mission completion stays the payoff.

Thread 2, the warning (Goa'uld threat):
- Early scans and stronghold intel pick up stray Goa'uld transmissions (Levels 1 and 2).
- Level 3 stronghold intel reveals the plan to attack Earth and raises DEFCON; the final Level 3 stronghold gives the fleet-tracking intel (existing Sol Defense arc in armory-design.md).
- The arc closes when the last Level 4 stronghold is captured.

The braid (proposal):
- The Goa'uld are following the same Ancient trail and want the Atlantis address. Stronghold intel and scanned sites show they have already searched some clue sites.
- The Level 4 victory ends the attack on Earth and reveals what they were after, which sends the player to the Level 5 Ancient Lab.
- Ancient fragments also carry defense hints that feed Sol Defense research (Tollan and Ancient defense tech, deferred build).

## Answers (Brad)
1. Clue sites: several per level, with some optional.
2. Goa'uld pressure on the Ancient trail: flavor only (no race, no lost sites).
3. Story beats are delivered by SGC briefings.
Still open: fixed or random worlds for clue sites, cache reward sizes (keep small early), whether missing a clue ever blocks the ending (recommendation: never).

## System Lords (Brad)
- Every level has a major System Lord from the show. Decided: Level 1 is Apophis, Level 5 is Anubis.
- Decided (Brad): Level 2 Cronus, Level 3 Yu (the Earth attack plan behind the Level 3 DEFCON raise), Level 4 Ba'al (his last stronghold ends the Sol Defense arc).
- Final order: Apophis, Cronus, Yu, Ba'al, Anubis.
- Each lord appears on one level only. The lord sits in the level's last stronghold; capturing it is the boss assault and ends his effects on the level.
- Level 4's last stronghold still ends the Sol Defense arc (armory-design.md).

## Resource worlds and Forward Operations Bases (Brad's decisions plus draft)
Decided (Brad):
- Conquered strongholds turn into resource worlds.
- A resource world produces on a timer while garrisoned, and the output builds up at the world to a cap. A Tel'tak run collects it. Past the cap, production pauses.
- A living lord can retake a resource world only until he falls (his last stronghold captured). After that every world in the level is permanent.
- New team type: Forward Operations Base (FOB) Team. Roster: Garrison Commander, 10 security personnel, 1 scientist, 1 archeologist.
- The limit on teams changes to fit: one FOB Team per conquered stronghold (Barracks capacity to be checked when built).

Proposals, still to confirm:
- Decided (Brad): the 10 security personnel are a pooled counter (10 of 10), not named people. Raids reduce the counter.
- Decided (Brad): the FOB Team includes a small medical group for injuries. Decided (Brad): 1 doctor and 2 medics, named like the other specialists. Raid losses split into wounded and killed; wounded return to the counter over time at a rate set by the medical group, killed need replacements sent through the gate. Without medical staff, wounded recover slowly or not at all.
- Named characters: Garrison Commander, scientist, archeologist, and the medical group.
- While stationed, the FOB Team is unavailable for missions. Recalling it stops production and leaves the world open to retaking while the lord lives.
- Scientist: raises output or speeds reverse-engineering of local finds. Archeologist: ties to scanning, for example revealing nearby clue sites and speeding decoding.
- Resource type varies by world: supplies, research points, power, naquadah. Output and cap scale with level.
- Cost scales with the large roster. Numbers to set once the roster and cost model are settled.

## FOB numbers (Brad)
- FOB Team cost: 100 supplies.
- FOB output: 50 supplies and 25 research points every 6.5 minutes while garrisoned (roughly 461 supplies and 231 research points an hour per base). The 100-supply cost pays back in about 13 minutes of output.
- Stockpile cap: still to set. Proposal: 6 payouts (39 minutes, 300 supplies and 150 research points). The two Tel'taks and their 2-minutes-per-light-year runs are the throttle on how much can be collected.
- Raid casualty split (Brad): leans FOB-strong, because a base is a defensive position.
  Proposal: a raid is repelled when the garrison counter holds roughly 6 or more; typical losses are 0 to 2 of the 10, split about 70% wounded and 30% killed; wounded recover through the medical group; the world is only lost if the counter is overrun to 0 while the lord is alive. Raid strength scales by level. Numbers to confirm when this is built.

## Game tour and how-to popups (new request, Brad)
- Features have grown, so the game needs a basic tour at the start and a how-to popup whenever a feature unlocks. Both should be easy to understand and keep the player immersed in the game.
- Decided (Brad): spotlight tour plus a guided first mission (raise a team, plan a mission, send it).
- Decided (Brad): unlock popups are briefing cards, queued and shown at base. They never interrupt a live wormhole or minigame.
- Decided (Brad): an end-of-mission brief popup appears after every mission. The player can turn these off in game settings, except for Assault missions, which always show it.
- Decided (Brad): build order is 0.8.4 drone stage only, then the tour and popups as 0.8.5.
- Narration (voice) not yet chosen: Brad asked for examples of two options, Hammond + Carter and a neutral SGC computer voice.
- Proposal: a Field Manual index lists every popup so any of them can be replayed, with a Replay Orientation button in Settings.

## Depends on
- 0.8.4 drone stage (COMM 1 rescue flight) and the assault recon scenario.
- Archeology Office (0.7.0), Lab reverse-engineering (armory-design.md), Sol Defense build (deferred).
