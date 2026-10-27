# Balance Playtest - Build 0.6.12, Level 1 to Level 2

Date: 2026-10-21. Scope: the four economy changes that landed without a playtest (logistics supply income, Tel'tak base 100, power by light years, 120 cap) plus the 60-supply opening against the 150-supply first assault.

## Method

The unmodified 0.6.12 game code was loaded in headless Chromium on a virtual clock (rendering, audio and autosave stubbed; no game rules touched). A scripted player played Level 1 to Level 2 using the game's own functions: auto-dial, send, return through the iris, raise teams, replace casualties, request logistics, convert naquadah. 40 sessions with logistics on (the real game) and 40 with logistics off (a what-if showing the pre-0.6.9 economy). Cap 150 minutes per session.

Player behaviour: explore the cheapest-gate unexplored world with the Exploration team, raise Recon after the first clean return and survey the stronghold, raise the Assault team when cash allows, assault with Assault + Recon, replace the dead, raise a Security team if a captured member blocks the Assault team. Logistics: Hill and Peterson requested whenever allowed.

Not modeled: MALP use, vehicles, Lab, Gate Room tiers, Armory, research spending of any kind, Tel'tak (not reachable before Level 2). The bot knows which world is the stronghold, so it never eats a forced ambush. Treat supply surplus as an upper bound; the in-game sinks are real (assault team 40, Recon 20, Security 25, Lab 100/250/500, Gate Room security 150 and Harriman 200, gear 40 to 160 each, MALP tiers 50+).

## Results

| | Logistics on (current) | Logistics off (what-if) |
|---|---|---|
| Sessions reaching Level 2 inside 150 min | 38 of 40 | 35 of 40 |
| Time to Level 2, median / mean | 35.4 / 37.9 min | 57.2 / 62.6 min |
| Time to Level 2, fastest 10% / slowest 10% | 14.0 / 64.7 min | 31.0 / 100.3 min |
| Median minute supplies first reach 161 (fee + sends) | 12 | 31 |
| Median minute all 4 regular worlds explored | 30.9 | 25.5 |
| Median minute first assault sent | 31.4 | 35.3 |
| Supplies on hand when the first assault is dialed, median | 335 | 172 |
| Income per minute, exploration / logistics | 5.95 / 7.10 | 5.77 / 0 |
| Share of supplies earned that came from logistics | 57% | 0% |
| Minutes spent waiting on power | 0.0 | 0.0 |
| Minutes with power pinned at the 120 cap | 42% | 51% |
| Extra time a failed assault adds | +24 min | +42 min |
| First-assault win rate (both configs pooled, 80 sessions) | 60% | game estimate 62% |

## Findings

1. Logistics moved cash forward by about 19 minutes and left exploration as the only gate. Cash for the assault is there at about minute 12; the assault goes at about minute 31 because the final stronghold is locked until all four regular worlds have a clean exploration. Without logistics, cash (minute 31) and exploration (minute 25 to 31) finished together, which is the balanced case. With it, the player spends roughly 19 minutes repeating exploration trips with a fat wallet.
2. Logistics out-earns the exploration loop. 7.1 supplies per minute for free, no power, no risk, against 5.95 for the whole Exploration team loop. Peterson (12) and Hill (25) together give about 37 per 7-minute cycle.
3. The opening is no longer a problem. 60 starting supplies against the 150 fee resolves itself by minute 12 with logistics on. Without logistics it is the pace-setter and a failed first assault can strand a player below the 5-supply Exploration send cost (5 of 40 what-if sessions never recovered inside 150 minutes).
4. Exploration trips are the drag. About 4 in 10 Exploration trips come back ambushed or hurt: no research, world not marked explored, 70% yield, and a 2.5 to 5 minute stand-down. Four clean worlds take a median of 8 to 9 trips. At Level 1 only one Exploration team is allowed, so the loop is strictly serial.
5. Power is not a constraint at Level 1. Zero minutes waiting on power in 80 sessions, pinned at the cap about half the time. Naquadah (+15 each) adds about 30 power per two trips. The 120 cap and the regeneration rate do nothing yet at Level 1 and Level 2.
6. A failed assault is expensive in time, not supplies: 150 lost, casualties, 20-minute program-wide cooldown, then a 2.5 to 5 minute heal. +24 minutes with logistics on.
7. Captured-member bind at Level 1. A captured member in the only Assault team cannot return until that stronghold falls, and team limit at Level 1 is one per type, so the player must raise a Security team (25) to assault again. It happened in 2 of 38 sessions with logistics and 7 of 35 without.

## Arithmetic only, not played

- Gate power at base regeneration 12 per minute, cost plus 5 auto-dial: Level 1 about 3.1 to 3.6 min per dial, Level 2 4.2 to 4.7, Level 3 5.9 to 6.4, Level 4 7.2 to 7.7, Level 5 8.1 to 8.6. With a 120 cap, Level 5 banks one dial plus 22 to 28 spare. Power starts to bite at Level 3.
- Tel'tak: yield 100 x hazard (100 / 125 / 150), round trip 2 minutes per light year, 2 supplies per run, 20% chance of 1 to 3 minutes delay, never ambushed. A Level 1 world at about 4 ly: about 12.5 per minute at low hazard, about 19 at high. Level 2 world at about 6 ly: about 8 to 12.5. One Tel'tak roughly doubles the Level 1 income total of about 13 per minute; two roughly triple it.

## Re-running

Tools in tools/balance-sim. Copy the game file there as game.html (or pass a path as the 7th argument). `node run.js out.json 40 1 150 0` runs 40 sessions with logistics on, cap 150 min, no reserve; swap the 1 for 0 for logistics off. `node an.js`, `an2.js` and `an3.js` read nolog.json and log.json. Needs the playwright package and Chromium.

## Open for decision

Nothing in the game or in the numbers was changed in this pass.
