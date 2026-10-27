# Factions and diplomacy (0.6.0)

All numbers below were chosen by Brad unless marked ASSUMPTION.

## Standing and tiers
- Each faction has a standing score. Diplomatic missions raise it. Tiers: Contact (1 point), Partner (5), Ally (12), Sworn (25). Standing never drops and tiers never fall.
- A Diplomat Team earns 3 standing per completed mission. Only Diplomat Teams can run diplomatic missions (ASSUMPTION: the 1-point baseline in the question only meant "slower than a Diplomat").
- Standing stops at Sworn. A Sworn faction cannot be sent more diplomatic missions.

## Diplomat Team
- New team type. Raise 50 supplies, send 10 supplies. Limited to one per level like the other types. Same 50% price increase per extra team.
- Roster: Team Lead, Diplomat, Linguist, Aide. First team is Amb. Hartwell, Dr. Lindqvist, Dr. Osei, Lt. Navarro.
- No camaraderie and no gear (ASSUMPTION, like Exploration).
- Must be accompanied by at least one Security team. Group returns together, same rules as other group missions.

## Diplomatic mission
- Mission type DIPLOMACY in the mission picker. Exactly one Diplomat team plus one or more Security teams. No other team types, no vehicles.
- Target must be a known faction world (intel 2 or more) whose faction is below Sworn.
- Takes 5:00 (Asgard speeds it up). No ambush roll. Cost is the team send costs (10 plus 5 per Security team).
- On return, the faction gains 3 standing. Security teams earn camaraderie like on an Exploration mission (10, no hurt case possible).

## Peaceful link
- A faction world is Peaceful from Partner tier on. Cannot be lost.

## Benefits (active from Partner, growing at Ally and Sworn)
- Langaran: exploration supply yield +10% / +20% / +30% (ASSUMPTION: Brad's percentage question named only Tollan, Asgard and Nox; I applied the same 10/20/30 to Langaran. Flagged for review.)
- Tollan: research projects finish 10% / 20% / 30% faster. Stacks multiplicatively with the staffed Lab bonus.
- Tok'ra: Partner shows stronghold difficulty band and defenses on any stronghold already found. Ally shows ambush odds on every world. Sworn lowers stronghold defense by 10% in assault odds.
- Free Jaffa: assault odds +5 / +10 / +15 points. At Sworn, one free casualty replacement per level.
- Asgard: missions, recalls and assist rescues 10% / 20% / 30% faster (assaults not affected, ASSUMPTION).
- Nox: infirmary healing 10% / 20% / 30% faster. (My earlier "calm their sector" idea was dropped.)

## Income at Sworn
- Every 10 minutes while Sworn: Langaran 250 supplies, Tollan 250 research points, Tok'ra, Free Jaffa, Asgard and Nox 50 supplies each. The first payment arrives 10 minutes after reaching Sworn.

## Where it shows
- Briefing Room: Faction relations panel (tier, standing, active benefit, next benefit, next payment timer).
- Starmap world panel: faction row with tier and standing; the map badge shows the tier.
- Mission log: Diplomacy missions with a Standing gained line.
