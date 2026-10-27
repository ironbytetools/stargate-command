import re
s = open('build_guide.py', encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


rep('BUILD = "0.9.3"', 'BUILD = "0.9.11"')
rep('content: "BUILD 0.9.3  //  TRAINING COPY"', 'content: "BUILD 0.9.11  //  TRAINING COPY"')

rep("shows nine rooms as a narrow column of cards", "shows up to ten rooms as a narrow column of cards")
rep("Clicking an entry in the strip jumps to the relevant room.\")", "Clicking an entry in the strip jumps to the relevant room. Every panel keeps a fixed size: a list that grows scrolls inside its own panel, so the Operations log and Mission Briefing are always on screen.\")")
rep("Air Force Logistics requests and the Gate Room upgrade ladder.", "Air Force Logistics requests, Tel'tak supply runs, the reactor and the Gate Room upgrade ladder.")
rep("A Linguist must be on station to decode.\"]])", "A Linguist must be on station to decode.\"],[\"Off-World Operations\",\"Forward Operating Base manager: active bases and their stockpiles, raid status and available sites. The room appears once a stronghold has been captured or a base exists.\"]])")
rep('["Dr. Catherine Langford","Archeology Office","Level 2","150 supplies"]', '["Dr. Daniel Jackson","Archeology Office","Level 2","150 supplies"]')
rep("and Dr. Langford counts", "and Dr. Jackson counts")
rep("9 Archeology Office\"]", "9 Archeology Office. Off-World Operations has no number key; click its card\"]")

rep('h2("Linked team groups")', 'h2("Tags and linked groups")')
a = s.index('p("In the Barracks, under the Teams list')
b = s.index('\n', a)
s = s[:a] + '''p("Every team and every group has a required **5-character tag** of letters and digits, such as EXP01 or ALPHA. Tags are unique across teams and groups and are shown wherever space is short: the mission builder, the Barracks lists and the Active Missions list on the dialing computer. New teams get a default tag from their type and number (EXP01, REC01, ASL01, DIP01, SEC01) that you can change in the team details. A tag of the wrong length, or one already in use, is refused with a warning in the Operations log.")
p("The Barracks **Linked groups** panel creates groups. Type a name and a tag, press **CREATE GROUP**, then press **EDIT** on the group and pick its teams from the list with ADD. A team can belong to any number of groups, so a Security team can sit in both an exploration group and an assault group. Membership can be changed at any time, and groups can be deleted. In the mission builder a ready group appears as one GROUP row that adds every team in it at once. A group is offered only when every member is eligible for the chosen mission type. While any member is away or stood down, the group row is greyed out and names the teams that are not ready, and the others can still be sent as individual teams. A team that belongs to two or more groups also stays listed on its own.")''' + s[b:]

rep('h2("Power cost")', 'h2("The dialing computer display")\np("The dialing computer is drawn wide, in the style of the show\'s SGC console: seven red numbered chevron slots with the locked glyph shown inside, a Sequence Compiler grid of all 39 glyphs that lights as each one is encoded, a large status readout in the footer and an IDC transponder box. Point at any glyph in the compiler to see the constellation it stands for. The **Active Missions** list shows only teams and groups that are off-world, one row per mission: the tag (the group tag when the mission includes a group), a three-letter mission code (EXP, REC, ASL, DEF, AST or DIP) and the time left. Everything else that is busy, such as a MALP, a vehicle repair, a Tel\'tak run, a rescue request, a logistics shipment or a Lab project, shows in the strip along the top of the screen, which reads NO OTHER ACTIVITY when idle. The starmap fills its own panel beside the dialing computer, with the selected world\'s details drawn on the map and the drone view opening inside it.")\np("The first time you dial a world, the Operations log prints an address readout that names its six constellations and the point of origin.")\nh2("Power cost")')
rep('Both are greyed out otherwise (Section 16)."])', 'Both are greyed out otherwise (Section 16).","**DRONE** sits below them and launches a reconnaissance drone flight at a surveyed assault target (Sections 9 and 16).","**SEND MALP** sends the MALP alone through an open wormhole. **EMBARK** sends the selected teams. A MALP no longer rides with a team send."])')

rep('["MALP","The MALP alone or riding with any team"', '["MALP","The MALP, sent alone with SEND MALP"')
rep("A MALP can go alone or ride with any team.", "A MALP goes alone: send it with SEND MALP on the dialing computer. It no longer rides with a team send, and a MALP sent alone gets no Recon-team ambush reduction.")
rep("and the after-action report.\")", "and the after-action report. Briefs are shown one at a time: **BACK** moves to an older brief and **NEXT** to a newer one, with a BRIEF n / total counter. A new brief arriving while you read an older one does not move you.\")")

rep("Build one from the Forward Operating Bases panel in the Quartermaster room for 100 supplies.", "Build one in the Off-World Operations room for 100 supplies; that room also lists active bases, their stockpiles, raid status and available sites.")
rep("Once restored, a Tel'tak runs independent supply missions to an explored world you choose.", "Once restored, a Tel'tak is put in service from the Quartermaster, under Air Force Logistics, and runs independent supply missions to an explored world you choose. Each ship has its own row with a SEND button and a Destination button that opens an in-game list of explored worlds and Forward Operating Bases showing distance, round trip, hazard and yield or stockpile, and the ship remembers its last destination.")

rep("Hammond's paperwork, Carter's techno-babble and the After-Action Report are optional.\")", "Hammond's paperwork, Carter's techno-babble and the After-Action Report are optional.\")\np(\"No minigame opens as a popup. Each runs inside the panel of the room it belongs to: reactor routing in the Quartermaster, glyph decoding in the Archeology Office, Hammond's paperwork in the Briefing Room, Carter's questions in the Science Lab and radio contact in the dialing computer panel. Untimed games (reactor, glyph, Carter) are parked when you choose another room and return when you come back. Timed games (Hammond's paperwork and radio contact) lock navigation until they are finished or closed, with a warning in the Operations log.\")")
rep("with heavier static and a faster sweep.\"])", "with heavier static and a faster sweep.\",\"**The radio.** Tuning uses a field radio with a rotary knob (drag it or use the wheel), arrow keys for fine tuning, VOL + and - for micro trim, PRE + and - for coarse steps and CLR to abort. The result appears on a compact control unit with a colour LCD, a D-pad and A, B and C keys that press the first three options on screen; O/R or X closes it and the BRT keys change the brightness.\"])")
rep("and T switches between optical and thermal.\",", "and T switches between optical and thermal.\",\"**Display.** The drone console is an olive rugged display in the style of a marine radar unit, with green readouts for heading, altitude, speed and zoom and a radar with range rings and a sweep. Covered ground shows as a faint green tint so defender view cones read clearly. Left keys: F1 optical or thermal, F2 mouse look, F3 place fix, end survey or continue, F4 confirm fix, F5 info, F6 abort. Right keys: F7 and F8 zoom, F9 climb, F10 descend, F11 level, F12 boost. F13 shows the controls card and the BRT keys change brightness.\",")
rep("When the gate next sits closed and idle, the conduit puzzle opens.", "Go to the Quartermaster: when the gate is closed and idle, the conduit puzzle opens in its panel.")
rep("Each project can be asked about once.", "Each project can be asked about once. There are 40 questions in five groups (reactor, dialing, security, MALP and armory), and the group follows the project.")

rep("The log keeps the latest 150 missions.\"])", "The log keeps the latest 150 missions.\",\"**Staff chatter.** Now and then the Operations log carries a short remark from General Hammond, Colonel Carter, Dr. Lee (once hired) or Dr. Jackson (once hired). They are flavor only and never appear during a timed minigame.\",\"**Address readouts.** The first dial to each world prints an address readout. Dialing the same world five times in a row draws a remark from Colonel Carter, and the first dial to a system after it is secured notes that its addresses are now in the permanent record.\"])")
rep('["Team limit per type"', '["Tag","5 letters or digits, unique across teams and groups"],["Team limit per type"')

open('build_guide.py', 'w', encoding='utf-8').write(s)
print('guide patched', len(s))
