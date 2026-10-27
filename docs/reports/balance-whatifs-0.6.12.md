# Balance What-Ifs - Build 0.6.12, Level 1 to Level 2

Follow-up to balance-report-0.6.12.md. Brad picked three levers to speed up exploration: a second Exploration team at Level 1, an easier final-stronghold lock, and fewer ambush injuries. Each was run as a what-if on a scratch copy of 0.6.12 (logistics on, as in the real game). Nothing in the game or its docs was changed. Exact values for any lever are Brad's to set; the rows below are test points, not proposals.

## Test points

| Variant | Sessions | Reached Level 2 | Level 2 median | p10 / p90 | First assault sent (median) | Supplies at assault dial (median) | Exploration income per min | Research points at Level 2 |
|---|---|---|---|---|---|---|---|---|
| Today (0.6.12) | 40 | 38 | 35.4 | 14.0 / 64.7 | 31.4 | 335 | 5.9 | 581 |
| Two Exploration teams at start | 30 | 28 | 29.7 | 13.3 / 55.8 | 21.0 | 296 | 9.9 | 838 |
| Lock needs 3 of 4 worlds | 30 | 29 | 32.4 | 13.8 / 81.9 | 16.3 | 197 | 5.9 | 643 |
| Lock needs 2 of 4 worlds | 30 | 29 | 19.4 | 14.4 / 42.9 | 15.5 | 182 | 5.5 | 442 |
| Ambush injures 50% of the time (today about 100%) | 30 | 30 | 28.4 | 15.8 / 46.5 | 19.0 | 251 | 6.6 | 738 |
| Ambush injures 25% of the time | 30 | 29 | 23.8 | 15.8 / 61.8 | 18.1 | 214 | 6.7 | 809 |
| Two teams + lock 3 of 4 + injury 50% | 30 | 29 | 15.5 | 12.8 / 61.2 | 11.8 | 183 | 11.2 | 1159 |

Times are minutes. Assault needs about 161 supplies at the dial (150 fee + sends). With 30 to 40 sessions per row, differences under about 5 minutes are noise.

## Reading the table

- The lock is the strongest single lever on the median, because it is the wall the bot hits at about minute 31 today. Easing it also pulls supplies on hand at the assault down toward the 161 needed.
- Injury chance helps the typical run but not the tail: failed assaults still push the slow 10% out.
- A second Exploration team raises exploration income by about two thirds (5.9 to 9.9 per minute) and research points by about 45%, so it deepens the supply surplus even as it speeds the lock. Modeled as the two teams sent to different worlds, two dials per cycle. Sending both to one world would roughly double supplies and research per dial and was not modeled.
- The combined row lands supplies at the assault (183) close to the cost (161), which is the balance seen before logistics.

## Dead end found while testing

Assault-capable teams are Assault and Security. A captured member stays captured until that stronghold falls, and Level 1 allows one team per type. If both the Assault team and the fallback Security team each have a captured member, no team can assault and nothing else frees them. This stranded 9 of the 270 sessions across these runs (1 of 40 with logistics on today). It may be a true soft-lock; it was inferred from code and sessions, not confirmed by hand.

## Not modeled

MALP, vehicles, Lab, Gate Room tiers, Armory, research spending, Tel'tak. The player knows which world is the stronghold. Two-team behavior assumed one team per world.

## Open for decision

- Exact values: ambush injury chance, how many worlds the lock needs, whether the second Exploration team is free and whether the Level 1 Exploration cap becomes 2.
- Whether the second Assault team at Level 1 still wanted, or the two starting Exploration teams replace that idea.
- The captured-member dead end.
- Next playtest: Level 1 with research spending.
