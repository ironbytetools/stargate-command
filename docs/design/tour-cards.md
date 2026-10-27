# Stargate Command: tour and briefing cards (built in 0.8.6)

Voices:
- **Opening tour (section A):** General Hammond and Colonel Carter, alternating. Hammond speaks plainly as the base commander. Carter handles the technical parts. Original wording, no quoted lines.
- **Everything after the tour (sections B to E):** the base computer. Terse, factual, present tense, labelled BASE COMPUTER.

Each card has a speaker line, a title, 1 to 3 sentences and a button (NEXT, GOT IT or DONE). Tour cards have SKIP TOUR. Event cards have CLOSE and show once per game (saved). A TOUR entry in the Menu replays the tour only.

Anything in [brackets] is a trigger note for me, not card text.

## A. Opening tour (auto on a new game, 8 cards, skippable)

**A1. GEN. HAMMOND**
Welcome to Stargate Command. This installation sits under Cheyenne Mountain, and everything we do goes through that gate. You will send teams out, bring back what they find, and decide what the base does next. Colonel Carter will walk you through the facility.
[NEXT]

**A2. COL. CARTER // THE FACILITY**
This is the Facility. Every room is on the map, and selecting one shows its staff, equipment and options. The Operations log along the bottom records everything that happens on base.
[NEXT] [points at the room map]

**A3. COL. CARTER // RESOURCES**
Supplies pay for missions and replacements. Power opens the gate, and naquadah can be converted into power. Research unlocks upgrades. All four totals are in the header.
[NEXT] [points at the header resources]

**A4. GEN. HAMMOND // TEAMS**
The Barracks is where your teams live. You start with two Exploration teams. Look after them. Camaraderie grows with every successful mission, and it improves their odds when things go wrong.
[NEXT] [highlights Barracks]

**A5. COL. CARTER // THE GATE ROOM**
Open the GATE ROOM tab. The starmap lists the worlds we know about. The dialing computer dials the selected world, and the Mission panel sends teams once the wormhole is open. A wormhole stays open for five minutes.
[NEXT] [points at the GATE ROOM tab]

**A6. GEN. HAMMOND // THE MENU**
MENU holds your saves, Settings, Help, Sound and Full Screen. The game saves on its own, and you can keep three save slots as well.
[NEXT] [points at MENU]

**A7. COL. CARTER // WHAT TO EXPECT**
From here on the base computer files a briefing when a mission ends, and a note the first time something new happens. Open the MISSION BRIEFING tab on the Operations log to read them.
[NEXT] [points at the MISSION BRIEFING tab]

**A8. GEN. HAMMOND // YOUR FIRST ORDERS**
Pick a world on the starmap, dial it, and send an Exploration team through. Good luck. You can replay this tour from MENU.
[DONE]

## B. First-time event cards (base computer, once each)

**B1. BASE COMPUTER // FIRST WORLD SELECTED** [first time a world is selected on the starmap]
SELECTING A DESTINATION: The selected world is shown on the dialing computer. Dialing costs power by distance. Use AUTO-DIAL, or rotate the ring and press LOCK on each symbol.
[GOT IT]

**B2. BASE COMPUTER // WORMHOLE OPEN** [first time a wormhole opens]
WORMHOLE ESTABLISHED: The wormhole stays open for 5 minutes. Choose teams in the Mission panel and press SEND. You can send several missions through one open wormhole.
[GOT IT]

**B3. BASE COMPUTER // TEAM RETURNING** [first time a team is marked RETURNING and an incoming activation starts]
INBOUND ACTIVATION: Returning teams come through the gate. Wait for the IDC, then open the iris. A closed iris turns the team away.
[GOT IT]

**B4. BASE COMPUTER // FIRST AMBUSH OR INJURY** [first injury]
CASUALTIES: Injured personnel recover in the Infirmary. Killed personnel are replaced from supplies in the Barracks.
[GOT IT]

**B5. BASE COMPUTER // FIRST INCOMING WORMHOLE** [first unscheduled incoming]
UNSCHEDULED ACTIVATION: The alert bar shows the IDC transponder. A friendly code comes with a team or allied name. An unrecognized signature is hostile, so close the iris.
[GOT IT]

## C. Systems as they unlock (base computer, once each)

**C1. BASE COMPUTER // SURVEY COMPLETE: STRONGHOLD IDENTIFIED** [first stronghold at intel 2 or higher]
STRONGHOLDS: A Goa'uld stronghold can be assaulted by Assault teams once surveyed. The estimate before sending combines camaraderie, team size and the stronghold's defenses. Capture them all to clear the level.
[GOT IT]

**C2. BASE COMPUTER // RESEARCH AVAILABLE** [first time research points are earned]
RESEARCH: Research points fund projects in the Science Lab: facility and gate upgrades, equipment and the Armory's alien technology.
[GOT IT]

**C3. BASE COMPUTER // ARMORY** [first time an Armory item is researched]
ARMORY: Researched gear is bought here and issued to teams in the Barracks. Tel'tak cargo ships are kept here for supply runs.
[GOT IT]

**C4. BASE COMPUTER // MOTOR POOL** [first MALP or vehicle upgrade available]
MOTOR POOL: MALPs survey worlds ahead of your teams. Trucks, drones and ATVs are built and upgraded with research, and they join missions to improve results.
[GOT IT]

**C5. BASE COMPUTER // FACTION CONTACT** [first faction discovered]
DIPLOMACY: A friendly faction has been identified. Diplomat teams travel with a Security team to raise standing, which unlocks perks and, at Sworn, regular income.
[GOT IT]

**C6. BASE COMPUTER // LOGISTICS** [first time logistics or Tel'tak run becomes available]
LOGISTICS: Tel'tak runs bring back a world's maximum supply roll. Up to two shipments can be in transit. Air Force Logistics can also send supply requests.
[GOT IT]

**C7. BASE COMPUTER // LEVEL CLEARED** [first level cleared]
LEVEL CLEARED: The next system is unlocked, with new worlds on the starmap. The team limit rises by one per type.
[GOT IT]

## D. Minigame briefings (base computer, once each)

**D1. BASE COMPUTER // COMM 1: EMERGENCY** [first time COMM 1 is pressed]
RADIO CONTACT: An overdue team needs a radio fix. Tune the frequency out of the static, then fly the reconnaissance drone to the team. A better fix means a faster assist and a better yield. The wormhole timer keeps running.
[LAUNCH]

**D2. BASE COMPUTER // DRONE: ASSAULT RECON** [first time the DRONE key is pressed]
RECONNAISSANCE DRONE: Tag every contact at the stronghold and stay out of the red view cones. An amber warning shows before a defender sees you. A full survey improves the assault odds and reveals intel. If the drone is spotted, the benefit is halved and the assault is harder. The drone then needs a 5 minute cooldown.
[LAUNCH]

**D3. BASE COMPUTER // REACTOR UNSTABLE** [first power event]
POWER EVENT: The reactor is unstable. Solve the conduit puzzle to restore balance, or abandon it and lose one output until you re-route power at the Quartermaster.
[GOT IT]

**D4. BASE COMPUTER // INSCRIPTION FOUND** [first inscription found]
ANCIENT INSCRIPTION: A Linguist in the Archeology Office can decode it. Decoding reveals an artifact site, and a second Exploration mission there recovers the artifact.
[GOT IT]

**D5. BASE COMPUTER // HAMMOND'S PAPERWORK** [first time the Briefing Room paperwork is available]
PAPERWORK: General Hammond has forms to stamp. Stamp each by type, deny the flawed ones, and finish in 90 seconds. It pays supplies and a supply bonus on the next missions with a Logistic Truck.
[GOT IT]

**D6. BASE COMPUTER // ASK CARTER** [first time Col. Carter is on station and a project is available]
ASK CARTER: Press ASK CARTER on a research project. Pick the one real explanation of four. A right answer adds research points. A wrong answer delays the project.
[GOT IT]

**D7. BASE COMPUTER // AFTER-ACTION REPORT** [first time a mission closes in the log]
AFTER-ACTION REPORT: Open a closed mission in the Briefing Room mission log and press COMPLETE AAR. Type the report from the log. Accuracy decides the reward.
[GOT IT]

## E. End-of-mission briefings (base computer, every mission)

When a mission ends, the base computer files a briefing on the MISSION BRIEFING tab of the Operations log: team names, world, result, yield, intel change, injured, killed or captured, and an OPEN MISSION LOG button. Event notes (sections B to D) are filed on the same tab instead of popping up. Only the tour takes over the screen, and it pauses game time while the soundtrack keeps playing.

Not built as written: D1 and D2 are filed when COMM 1 or the DRONE key is pressed, not before the flight. D5 and D6 are filed the first time the Briefing Room or Science Lab is opened.
