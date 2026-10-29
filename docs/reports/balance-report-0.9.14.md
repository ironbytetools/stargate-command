# Balance Playtest - Build 0.9.14, Levels 1 to 5

Date: 2026-10-27. Scope: resource collection and spending across the whole game. This pass covers the economy pieces added since the 0.6.12 report that were never playtested: FOB output, Tel'tak collection, boss assaults, Armory and vehicle costs, Gate Room ladder, Lab tiers, rescue teams.

## Method

The unmodified 0.9.14 game code was loaded in headless Chromium on a virtual clock (rendering and audio stubbed, no game rules touched). A scripted player plays Level 1 to the end of Level 5 using the game's own functions. 20 sessions on the main policy, plus what-if batches of 5 to 10. Level 5 is cleared when its fourth stronghold falls.

Player policy in the main runs: two Exploration teams to start and a third when affordable; explore the cheapest unexplored world (faction and lab worlds included, because they count toward the final-stronghold lock); raise Recon, Security and Assault teams to the level's team limit; assault non-lord strongholds first and the lord last, with all ready Assault, Security and Recon teams up to the size the odds formula wants (2 team-equivalents per level), two ATVs on assaults, and a 15-minute wait for 55% odds before going anyway; request a Special Operations rescue whenever a member is captured; request Air Force Logistics whenever allowed; establish a FOB on every captured stronghold; buy Tel'tak ships when restored; collect from FOBs with a Truck when no Tel'tak is available. Research queue: Gate tiers 1 to 3, armor, Truck, packs, weapons, optics, then Reactor I to III and the rest of the Armory. Gear is bought per team and issued as soon as researched. Supplies are held back for the next assault fee and sends before gear, team raising and Lab upgrades, but not before FOBs, Tel'tak ships or Gate tiers.

Not modeled: every minigame (Hammond paperwork, After-Action Report, glyph decode, Carter, COMM radio, drone flight), diplomacy and faction standing perks, Defend missions against raids, MALP use and MALP tier upgrades, vehicle parts, drone and Truck upgrades beyond tier 3, hidden worlds. The drone recon before a lord assault is replaced by the GOOD result (+10 points, no alert). Reactor routing and power events are assumed solved the moment they appear. Treat every supply and research surplus below as an upper bound for what a human accumulates, and treat the clear times as a floor for a player who never loses time to minigames or hesitation.

## Results (main policy, 20 sessions)

| | Median | Fastest / slowest |
|---|---|---|
| Time to Level 2 | 44 min | 35 / 69 |
| Time to Level 3 | 114 min | 82 / 202 |
| Time to Level 4 | 230 min | 155 / 280 |
| Time to Level 5 | 258 min | 203 / 302 |
| Level 5 cleared | 353 min | 292 / 398 |
| Minutes spent per level, L1 / L2 / L3 / L4 / L5 | 44 / 63 / 115 / 23 / 91 | |
| Assaults per session / failed per session | 14.6 / 3.6 | |
| Assault win rate versus the game's own estimate | 75.6% vs 77.8% (291 assaults) | |

Win rate by level, the odds the game showed, and assaults in the sample:

| Level | Win | Estimate | Assaults |
|---|---|---|---|
| 1 | 83% | 73% | 24 |
| 2 | 66% | 68% | 61 |
| 3 | 65% | 71% | 93 |
| 4 | 80% | 83% | 25 |
| 5 | 91% | 91% | 88 |

Where supplies came from and went, per session average (Level 1 to clear):

| Supplies in | Amount | Share |
|---|---|---|
| Exploration returns | 3,213 | 13% |
| Air Force Logistics | 2,466 | 10% |
| FOB Truck pickups | 7,020 | 29% |
| Tel'tak runs | 9,824 | 41% |
| Boss spoils (100 x level) | 1,500 | 6% |
| Total | 24,023 | |

| Supplies out | Amount |
|---|---|
| Gear (bought per team) | 8,750 |
| Assault fees | 5,177 |
| Exploration and recon sends | 1,240 |
| Team raising and replacements | 1,153 |
| FOBs, Tel'tak ships and fees | 1,368 |
| Lab tiers and Gate tiers | 1,462 |
| Total | 19,152 |

Research points: income 22,781 (exploration 50%, FOBs 15%, Tel'tak 22%, boss spoils 13%), spent 15,264 (Gate ladder 3,941, Armory 5,215, vehicles 6,108). Left at clear: 4,903 supplies and 7,517 research points.

Average stockpile while on each level, supplies / research points: L1 117 / 295, L2 216 / 480, L3 301 / 606, L4 576 / 1,414, L5 1,530 / 3,585.

Share of minutes with gate power under 40: L1 45%, L2 63%, L3 46%, L4 38%, L5 31%.

What-if batches:

| Variant | Sessions | Median clear | Range | Note |
|---|---|---|---|---|
| Main policy | 20 | 353 | 292 to 398 | |
| No FOBs, no Tel'tak | 5 | 368 | 308 to 452 | supplies at clear 560 |
| No Air Force Logistics | 5 | 350 | 281 to 473 | Level 1 takes 70 min instead of 44 |
| Reactor tiers researched first | 10 | 333 | 268 to 400 | Reactor I at minute 36 instead of 101 |

## Findings

1. The game is paced by the assault cooldown, not by the economy. 14.6 assaults at about 24 minutes each (20-minute cooldown plus the mission) is 350 minutes, which is the clear time. The floor with no failures is 11 strongholds at about 22 minutes, around 240 minutes; failures add about 85 on average. Removing FOBs and Tel'tak, removing logistics, or fixing power early moved the median clear time by 20 minutes or less in either direction, inside the session-to-session spread.
2. Passive income is 70% of all supplies. FOB pickups and Tel'tak runs together bring 16,844 of 24,023 supplies; the exploration loop that the first levels are built around brings 13%. A FOB makes 120 supplies and 60 RP per 6:30, about 18.5 supplies per minute each. By Level 5 the player holds about 10 FOBs with a nominal 180 supplies per minute, but average uncollected stock sits at 4,000 to 6,000 against a 1,000 cap per FOB, so most production is thrown away: a Truck run lifts at most 120 supplies and 60 RP, and only two Tel'taks exist. Collection capacity, not FOB output, sets the real income.
3. The economy is tight early and slack late, but never broken. Levels 1 to 3 run on a stockpile of 117 to 301 supplies. At clear the player holds 4,900 supplies and 7,500 RP, with optional sinks the bot did not touch (vehicle parts, MALP tiers, Truck and drone tiers, more vehicles) worth well over 20,000 RP. So there is no wasted-wealth problem on the research side. Gear is the biggest supply sink (8,750), larger than assault fees (5,177), because it is bought per team and team limits grow with level.
4. Assault difficulty is not monotonic for a player who scales their groups. Win rate runs 83%, 66%, 65%, 80%, 91% across Levels 1 to 5, with the game's estimate tracking reality to within a few points. Levels 2 and 3 are the hardest and the final level is the easiest. The odds formula divides group size by 2 x level; a single Assault, Security and Recon group scores 30% on size at Level 5 and the first bot, which sent exactly that group, won only about 57% of its assaults, so the scaling requirement is a hidden rule players have to discover.
5. Level lengths are uneven: median 44, 63, 115, 23 and 91 minutes. They follow the stronghold count (1, 2, 3, 1, 4) times the cooldown. Level 4 has one stronghold and takes 23 minutes, a speed bump between Level 3 and Level 5.
6. Gate power is the early bottleneck. Power sits under 40 in 45% to 63% of minutes on Levels 1 and 2, and only a Reactor tier fixes it. Reactor I costs 1,000 RP after Gate tiers 1 to 3 at 100, 200 and 300; with the default queue it landed at minute 101, with Reactor first at minute 36. Faster power barely changed the clear time (333 versus 353 minutes) because the cooldown binds, but it removes the power-starved stretch from Levels 1 to 3.
7. FOB raids have no consequence for a player who ignores them. Across 20 sessions about 3.5 raid checks per session went unanswered and no base was overrun; the 10-person garrison absorbs the raid and heals itself. Defend missions are optional in practice.
8. Estimate and outcome agree, so the odds display can be trusted: 77.8% estimated against 75.6% won over 291 assaults.
9. Without Air Force Logistics the Level 1 opening takes about 70 minutes instead of 44, consistent with the 0.6.12 report (logistics moved cash forward by about 19 minutes at Level 1).

## Arithmetic cross-checks

The clear time of 353 minutes matches 14.6 assaults x about 24 minutes. Boss spoils match the code: 100 x level supplies, 200 x level RP, 1,500 and 3,000 in total across the five lords. FOB rate: 120 / 6.5 min = 18.5 supplies per minute. A Tel'tak round trip is 2 minutes per light year, so about 9 minutes at Level 1 and 24 minutes at Level 5, taking whatever the FOB has banked up to 1,000. Gate ladder cost in the code: 4,100 RP and 650 supplies. Armory research: 3,800 RP for the six standard lines plus 1,700 for the alien items.

## Decisions for Brad (nothing in the game was changed in this pass)

Open for picks:

A. Pacing target. Leave the 20-minute assault cooldown, or shorten it (for example to 15 minutes, which takes roughly 70 minutes off a clear), or scale it by level.
B. Level 4 speed bump. Leave it, add a second stronghold to Level 4, or raise its difficulty.
C. Difficulty curve. Raise Levels 4 and 5 (final level wins 91%) or soften Levels 2 and 3 (about 65%), or leave it.
D. FOB and Tel'tak. Leave as is (uncollected stock acts as a free reserve), lower FOB output, raise the collection cap per Truck run, or add more collection cost; and decide whether raids should threaten an unattended base.
E. Early power. Smooth the Reactor I research cost (1,000 RP after a 300 RP step), move Reactor I earlier in the ladder, or leave it.
F. Gear economics. Gear is bought per team; leave, or add a cost ceiling per tier.
G. Whether to extend the bot to MALP tiers, vehicle parts and the minigame income so the late-game RP picture is complete before tuning.

## Re-running

Tools in tools/balance-sim: bot2.js (the player), run2.js (the harness), an5.py (the analysis). Copy the game file there as game.html. `node run2.js out.json 10 800 '{"scaleTeams":true,"atv":true}' game.html` runs 10 sessions capped at 800 game minutes. Config keys: logistics, fob, tk, reactorFirst, scaleTeams, atv, secExp, maxExp, reserve, minOdds, oddsWaitMin. `python3 an5.py out.json` prints the summary. Needs the playwright package and Chromium. The harness ends the opening tour and any held pause before the bot starts; without that the game clock stays frozen.

## Follow-up: 0.9.15 tuning (picks E, C, B, D)

Brad picked E (Reactor I cost cut to 600 RP), C (rising difficulty: about 70% on Level 4 and 65% on Level 5), B (second Level 4 stronghold) and D (raid teeth, bigger Truck pickups, a Tel'tak load cap, FOB upkeep, FOB replacement at the SGC rate). Built as 0.9.15 (builds/sgc-command-0.9.15.html); numbers I chose are listed in CHANGELOG.md.

Result of 10 full-game sessions on 0.9.15 (same bot and policy as the main runs):

| | 0.9.14 | 0.9.15 |
|---|---|---|
| Level 5 cleared, median (range) | 353 (292 to 398) | 405 (308 to 493) |
| Minutes per level, L1 / L2 / L3 / L4 / L5 | 44 / 63 / 115 / 23 / 91 | 45 / 47 / 92 / 58 / 106 |
| Assault odds shown, Level 4 / Level 5 | 83% / 91% | 69% / 66% |
| Assault win rate, Level 4 / Level 5 | 80% / 91% | 77% / 71% (26 and 56 assaults) |
| Reactor I researched, median minute | 101 | 65 |
| Gate power under 40, Level 1 / Level 2 | 45% / 63% | 27% / 35% |
| Supplies and RP left at clear | 4,900 / 7,500 | 8,000 / 17,400 |

Findings:

1. Defense could not reach the odds targets alone. Defense carries one third of the odds formula and caps at 100, and the bot's two ATVs added up to +19 points on Levels 4 and 5, so the late game was easy because spare research turns into ATV tiers. Level 4 defense 65, Level 5 defense 80 and an ATV bonus of 2 points per tier (was 3) land the odds on target. Players who skip ATVs see 62% on Level 4 and 58% on Level 5.
2. Clear time rose by about 50 minutes: the second Level 4 stronghold (about 35 minutes) plus more failed assaults late.
3. D did not shrink the late-game surplus. Truck pickups at 250 / 125 raised FOB income (12,900 supplies against 7,000), and the Tel'tak cap and 15-supply upkeep do not offset it. Average unspent stock on Level 5 is 3,400 supplies and 11,800 RP against 1,500 and 3,600 before. If the aim is a tighter late game, the knobs are the Truck pickup, the upkeep (15 per base per 6:30), or the cap on FOB stockpile.
4. About 5 raid checks per session went unanswered in the bot runs; each costs half the stockpile at that base.

## 0.9.16 follow-up (Oct 27 2026): roles, escalating upkeep, Tel'tak fuel

Brad chose FOB specialization with scaling upkeep and naquadah as Tel'tak run fuel so resources force choices. Built as 0.9.16 (roles 150/30, 60/100, 70/40; relay +2 power per minute capped +8; role change 100 supplies; upkeep 15 + 5 per earlier base; fuel ceil(ly/4) naquadah).

Bot sessions (policy as before, plus a role cycle and a 3-naquadah reserve per Tel'tak):

| Role plan | Median clear (min) |
|---|---|
| Mix (supply, research, power cycle) | 435 |
| All Supply depot | 463 |
| Power-heavy | 409 |

Findings: the role plans give different Level 5 stockpiles, so the choice matters rather than one plan dominating by a wide margin; power-heavy is fastest because power starvation was the early bottleneck. Naquadah converted to power was about 190 per session against about 70 spent on fuel, so fuel competes with conversion but does not starve it. Level 5 win rate pooled about 58% (156 assaults, noisy) against the 65% target.

Delivered tools: tools/balance-sim/bot2.js and run2.js are updated for roles and fuel (config key roles, for example roles:["pw","rp","sup"]).

## 0.9.23 follow-up (Oct 28 2026): 15 minute cooldown, Level 5 check

Brad picked A as a flat 15 minute assault cooldown, left F as is, skipped G, and asked for a Level 5 retune. 30 full-game sessions on the 0.9.22 rules with the 15 minute cooldown (difficulty 80 on Level 5 unchanged), bot as before with scaleTeams and atv on:

| | 0.9.15 (20 min, 10 sessions) | 0.9.23 (15 min, 30 sessions) |
|---|---|---|
| Level 5 cleared, median (range) | 405 (308 to 493) | 392 (259 to 546) |
| Minutes per level, L1 to L5 | 45 / 47 / 92 / 58 / 106 | 45 / 54 / 86 / 60 / 130 |
| Win rate, L4 / L5 | 77% / 71% | 64% / 66% |
| Shown estimate, L4 / L5 | 69% / 66% | 64% / 63% |
| Level 5 assaults in sample | 56 | 182 |

Finding: Level 5 is on the 65% target with the larger sample, so no retune was applied. The 58% from the 0.9.16 runs came from 156 assaults pooled across different FOB role plans, which change how much research goes into ATV tiers. Clear time barely moved (13 minutes) because the bot already waits for 55% odds and the pace is also set by raising teams, gate power and research. Late stock is still large: 2,029 supplies and 11,509 RP unspent at clear.

Runs: node run2.js out.json 15 800 '{"scaleTeams":true,"atv":true}' game.html, two processes in parallel.
