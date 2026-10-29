s = open('build_guide.py', encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


rep('BUILD = "0.9.14"', 'BUILD = "0.9.22"')
rep('content: "BUILD 0.9.14  //  TRAINING COPY"', 'content: "BUILD 0.9.22  //  TRAINING COPY"')

rep('3 of 5 at Level 4 and 4 of 6 at Level 5.', '3 of 4 at Level 4 and 4 of 6 at Level 5.')

rep('["Naquadah","Converted to power in the Quartermaster","Some exploration returns"]',
    '["Naquadah","Converted to power in the Quartermaster, and burned as fuel by Tel\'tak supply runs","Some exploration returns, some outposts"]')
rep('"Exploration returns, Tel\'tak runs, logistics shipments, factions at Sworn"]',
    '"Exploration returns, Tel\'tak runs, logistics shipments, base and outpost output, factions at Sworn"]')

rep('["Archeology Office","Permanent staff, inscriptions found on Exploration missions, glyph decoding and the artifact collection.',
    '["Archeology Office","Permanent staff, inscriptions found on Exploration missions, glyph decoding, the artifact collection and the list of hidden worlds.')
rep('["Off-World Operations","Forward Operating Base manager: active bases and their stockpiles, raid status and available sites. The room appears once a stronghold has been captured or a base exists."]',
    '["Off-World Operations","Forward Operating Base and outpost manager: active bases with their roles, stockpiles and upkeep, outposts and their events, raid status and available sites. The room appears once a stronghold has been captured, or a base or outpost exists."]')

rep('["4","Epsilon Eridani","6","1","2 (Tok\'ra, Free Jaffa)",""]',
    '["4","Epsilon Eridani","6","2","2 (Tok\'ra, Free Jaffa)","Second stronghold added in 0.9.15"]')
rep('small("Counts include strongholds and faction worlds.")',
    'small("Counts include strongholds and faction worlds. Faction worlds stay off the starmap until their hidden-world artifact is decoded, and Level 3 has an extra story-only hidden world (Abydos).")')
rep('"**Faction worlds** belong to a friendly faction and are reached by diplomacy (Section 10).",',
    '"**Faction worlds** belong to a friendly faction. They are hidden worlds: decode the faction\'s artifact in the Archeology Office to reveal them, then reach them by diplomacy (Section 10).","**Hidden worlds** are seven special worlds, one or two per level from Level 1 to Level 5, each behind its own artifact (Section 16). Decoding reveals the world on the starmap and in dialing.","**Outposts** can be built on explored regular worlds (Section 9).",')

rep('h2("Faction leads")\np("Every successful Exploration return from a regular world gives one lead: traders on the world name the home world of a faction you have not yet met, which is added to the starmap at intel tier 2 and to Faction Relations. This repeats until every faction on your levels is known.")',
    'h2("Hidden worlds and faction contact")\np("Exploration returns no longer name faction home worlds. Instead, every successful Exploration return from a regular world rolls for the next undiscovered hidden-world inscription at or below your level: 40% on the first return, plus 30 points for each miss, so one is found by the third return at the latest. Decode it in the Archeology Office (Section 16). Decoding reveals the world and its address, files first contact with its faction and pays a one-time reward.")\nh2("Revisit events")\np("An Exploration team returning from an already explored regular world has a 50% chance of an event on top of its normal yield: a supply cache (+35 supplies), data (+45 research points, more likely on ruins and mountains), local traders (+1 naquadah) or a Goa\'uld patrol (lose 20 supplies, more likely on high-hazard worlds). The event is shown in the return text and the yield.")')

rep('Build one in the Off-World Operations room for 100 supplies; that room also lists active bases, their stockpiles, raid status and available sites.',
    'Build one in the Off-World Operations room for 100 supplies and choose its role; that room also lists active bases, their roles and stockpiles, the total upkeep, raid status and available sites.')
rep('"**Output:** 100 supplies and 50 research points every 6:30, plus 20 supplies from the archeologist and 10 research points from the scientist, into a stockpile capped at 1000 supplies and 500 research points. Production pauses when the stockpile is full.",',
    '"**Roles:** a base is given a role when it is established. A Supply depot makes 150 supplies and 30 research points every 6:30, a Research outpost 60 supplies and 100 research points, and a Power relay 70 supplies and 40 research points plus 2 gate power per minute, up to +8 in total across all relays. The archeologist adds 20 supplies and the scientist 10 research points to each output. Output goes into a stockpile capped at 1000 supplies and 500 research points, and production pauses when it is full. Changing a role costs 100 supplies and empties the stockpile.","**Upkeep:** every 6:30 each base costs the SGC 15 supplies plus 5 for each base built before it, so the second costs 20, the third 25 and so on; the Off-World Operations header shows the total. If the SGC cannot pay, that base produces nothing for the interval and shows UNSUPPLIED (an unsupplied Power relay gives no power).",')
rep('"**Collecting:** a Tel\'tak sent to the world loads the whole stockpile and pays it on return. An Exploration team with a Logistic Truck sent to the world collects one payout (120 supplies and 60 research points) instead; that trip brings back only the haul. Without a truck the send is blocked.",',
    '"**Collecting:** a Tel\'tak sent to the world loads up to 400 supplies and 200 research points from the stockpile and pays them on return; the rest stays in the stockpile. An Exploration team with a Logistic Truck sent to the world collects up to 250 supplies and 125 research points instead; that trip brings back only the haul. Without a truck the send is blocked.",')
rep('If nobody answers, the garrison fights alone.', 'If nobody answers, the garrison fights alone and the raiders carry off half the stockpile, supplies and research points alike.')
rep('killed are replaced for 15 supplies each with REPLACE.', 'killed are replaced one at a time with REPLACE for 15 supplies each, and the Free Jaffa free replacement applies.')

rep('RECALL BASE (two clicks) abandons a base and its stockpile."])',
    '''RECALL BASE (two clicks) abandons a base and its stockpile."])
h2("Outposts")
p("Any explored regular world (not a stronghold, faction world, the lab or the ship) can host an outpost, built and managed in the Off-World Operations room beside the bases and marked with an OUTPOST badge on the starmap. An outpost has no stockpile and needs no Truck or Tel'tak: it delivers straight to the SGC every 6:30.")
ul(["**Cost:** 60 supplies for the first outpost, plus 20 for each outpost already built. The garrison is 4. POST 1 replaces a lost guard for 20 supplies. ABANDON asks for confirmation.","**Upkeep:** 10 supplies per interval, plus 3 for each level above 1.","**Output:** set by the world type and raised 25% for each level above 1."])
table(["WORLD TYPE","OUTPOST OUTPUT PER 6:30 (LEVEL 1)"],[["Temperate forest","45 supplies"],["Arid desert","15 supplies and 1 naquadah"],["Frozen tundra","15 supplies and 30 research points"],["Ocean archipelago","30 supplies and 15 research points"],["Volcanic highlands","10 supplies and 2 naquadah"],["Jungle lowlands","30 supplies and 10 research points"],["Mountain plateau","15 supplies, 10 research points and 1 naquadah"],["Ancient ruins field","45 research points"]])
h2("Outpost events")
p("After each delivery an outpost rolls for an event: 15%, 25% or 35% on a low, medium or high hazard world. Each event has a 2:00 decision window and a default that applies if you do not answer. Costs and rewards scale like output.")
ul(["**Raid:** REINFORCE for 40 supplies, or HOLD and lose 0 to 2 guards. An outpost with no guards left is overrun.","**Trader:** pay 50 supplies for 80 research points, or decline. More common on settled worlds.","**Site found** (ruins, mountains and deserts): pay 20 supplies to survey it for 100 research points, 80 supplies or naquadah, or ignore it.","**Tremors** (seismic worlds): pay 50 supplies, or skip one delivery."])''')

rep('Faction worlds are only identified at intel tier 2, so a survey or MALP must find them before a diplomatic mission can be sent.',
    'Faction worlds are hidden worlds: decode the faction\'s artifact in the Archeology Office (Section 16) to reveal the world and file first contact, and only then can a diplomatic mission be sent.')

rep('"Each run costs 2 supplies and takes 2 minutes per light year of round trip."',
    '"Each run costs 2 supplies and naquadah for fuel: the light years to the system divided by 4, rounded up, which is 2 on Levels 1 and 2 and 3 on Levels 3 to 5. The ship will not launch without it, and the SEND button shows the cost. A run takes 2 minutes per light year of round trip."')
rep("It loads the base's whole stockpile on arrival and pays the supplies and research points on return; the run costs the usual 2 supplies and shows the haul in the mission log.",
    "It loads up to 400 supplies and 200 research points of the base's stockpile on arrival (the rest stays in the stockpile) and pays them on return; the run costs the usual 2 supplies and naquadah fuel and shows the haul in the mission log. Tel'tak runs are sent with SEND only.")

rep('"-10% mission time (capped at 50%) and +3 points assault odds"', '"-10% mission time (capped at 50%) and +2 points assault odds"')
rep('["4","Reactor I","1,000","6:00","none"', '["4","Reactor I","600","6:00","none"')

rep('p("Ten collectable artifacts, two per star system, are hidden behind inscriptions. They are separate from the alien technology in the Armory.',
    'p("Ten collectable artifacts, two per star system, are hidden behind inscriptions. Seven further hidden-world artifacts are described at the end of this section. They are separate from the alien technology in the Armory.')

anchor = 'p("Collecting all ten puts the Ancient Repository Stone on display in the Archeology Office.'
i = s.index(anchor)
j = s.index('\n', i)
hid = '''
h2("Hidden worlds")
p("Seven further artifacts, separate from the ten above, each reveal a hidden world. They are found as inscriptions on Exploration returns (Section 8) and decoded in the Archeology Office with the same three glyph puzzles, from the Hidden worlds list under the level tabs.")
table(["LEVEL","HIDDEN WORLD","FACTION","ONE-TIME REWARD"],[["1","Langara","Langaran","100 supplies"],["2","Tollana","Tollan","120 research points"],["3","Abydos","None (story only; becomes an explorable regular world)","200 supplies"],["4","Vorash","Tok'ra","150 research points"],["4","Chulak","Free Jaffa","250 supplies"],["5","Orilla","Asgard","250 research points"],["5","Nox Haven","Nox","300 supplies"]])
p("A successful decode reveals the world and its address on the starmap and for dialing, files first contact with its faction, pays the reward and opens a popup with a short story about the world, the faction's history, the benefits of each tier and its Sworn income. READ in the list reopens the popup.")'''
s = s[:j] + hid + s[j:]

rep('["Artifacts","10 total, 2 per level"]', '["Artifacts","10 total, 2 per level, plus 7 hidden-world artifacts"]')
rep('["Logistics requests in transit","2"],', '["Logistics requests in transit","2"],["Base and outpost output interval","6:30"],["Base stockpile cap","1000 supplies and 500 research points"],["Tel\'tak load from a base","400 supplies and 200 research points"],["Tel\'tak fuel","Light years divided by 4, rounded up, in naquadah"],["Outpost cost","60 supplies, plus 20 for each outpost already built"],')

open('build_guide.py', 'w', encoding='utf-8').write(s)
print('ok')
