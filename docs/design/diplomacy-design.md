# Diplomacy for ordinary worlds: design (built as 0.6.15)

Approved by Brad. Numbers are his; assumptions are marked.

## Rules

- Eligible: regular worlds and strongholds on the current level that have been surveyed (intel 2 or higher; assumption, same bar as faction worlds). Not captured, not already under treaty. Ancient ship and Lab are excluded.
- Mission: the existing Diplomacy mission type (one Diplomat team plus a Security escort, 5:00, no ambush, no vehicles). Cost is the team costs; strongholds add 10 supplies.
- Each completed mission gives +1 standing with that world.
- Treaty chance on a mission is rolled with the standing held before the mission. A treaty is guaranteed when standing reaches the threshold.

| | Regular world | Stronghold |
|---|---|---|
| Treaty chance | 10% + 15% per standing | 5% + 10% per standing |
| Guaranteed at standing | 4 | 6 |
| Expected missions to treaty | about 3 | about 4 |
| Raid check on a treaty world | every 15:00 | every 15:00 |
| Raid chance per check | 15% | 30% |

## Treaty effects

- Regular world: peaceful, so ambushes stop there. It still has to be explored to count as explored.
- Stronghold: stays hostile for assault purposes and must still be assaulted to clear the level. A treaty stronghold counts as one resolved world toward the final-stronghold lock (the 75% rule), and it does not count as "the final stronghold" while under treaty. Rule used: lockLeft adds one per other uncaptured treaty stronghold; the final stronghold is the last uncaptured stronghold without a treaty.
- Sending an assault against a treaty stronghold voids the treaty (assumption).

## Raid alert

- When a raid hits, an alert runs for 2:00 (badge on the world, chip in the active strip, log line).
- Response: a DEFEND mission (new mission type) with a Security or Assault team to that world. The raid is repelled the moment the team goes through the gate. The team returns after 2:00 like any mission and earns +10 camaraderie. No ambush on a defense.
- No response in time: the treaty is void and standing is halved (rounded down). A stronghold also stops counting toward the lock.
- After a repelled raid the raid timer restarts at 15:00.
- Consequence to watch: the gate must be free and powered to dial in 2:00. A busy gate can cost you the treaty (intended).

## Not changed

- Faction worlds work as before (+3 standing, tier ladder, perks).
- Peaceful by capture is unchanged.

## Open items for playtest

- Whether 2:00 is enough in practice to dial and send.
- Whether raids on strongholds at 30% feel fair, since a stronghold treaty only helps the lock.
- Whether a treaty regular world should count as explored for the lock (currently it does not).
