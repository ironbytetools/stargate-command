# Smaller backlog: design decisions (Oct 21 2026)

Status: design only, nothing built. Numbers below are Brad's choices.

## Tel'tak runs in the mission log
- Each run gets its own mission ID, clickable from the log.
- Entry records: destination world, supplies returned (after hazard multiplier), ship used (Level 2 wreck or Level 3 wreck), timestamped events (launch, delay, arrival, return).

## Starmap level-cleared banner
- One-time announcement when the level's final stronghold is captured.
- Persistent CLEARED marker on that system's map once every planet in it is Peaceful.

## Rescue record milestones
- Per team. Two counters: assists performed and times rescued.
- Only assists performed is a reward track; times rescued is display only and earns no badge.
- Five tiers at 1 / 3 / 6 / 10 / 15 assists.
- Every tier gives: a title, a one-time payout, a permanent assist travel bonus.
- Titles: Rescuer, Lifeline, Guardian, Sentinel, Angel of the Gate.
- Payout per tier: 25 / 50 / 75 / 100 / 150 supplies plus equal research points.
- Assist travel time -5% per tier (-25% at tier 5), applied on top of the COMM 1 accuracy band.

## Linked teams (groups) - replaces Barracks roster swaps
- Link and unlink on the Barracks team edit screen. Teams must be on station to link or unlink.
- A team belongs to one group; no cap on teams per group.
- Adding a linked team to a mission builder adds the whole group at once.
- A group has a player-editable name; default is "<lead team's type> Team N" (lead = first team linked).
- A group is broken while any member is stood down or away; the group is unavailable as a group during that time, and the remaining teams can be sent unlinked. It relinks when the sent team returns and the stood-down team is ready.

## Vehicle parts
- Four parts: Armor, Engine, Cargo, Sensors. Truck: Armor, Engine, Cargo. Drone: Armor, Engine, Sensors. ATV: Armor, Engine, Cargo.
- Extras on top of the 5 vehicle tiers. Shared stock that applies to the vehicle type (not per vehicle).
- 3 levels per part. Each level researched in the Lab, then bought with supplies.
- Research per level: 75 / 150 / 225 RP + 25 / 50 / 75 supplies. Purchase: 25 / 50 / 75 supplies.
- Effects, one tier's worth per level: Cargo +5% yield (Truck, ATV); Engine ATV -10% mission time, Truck and Drone -5%; Sensors Drone -3 ambush points; Armor all vehicles -33% repair time (free at III) and the 25% failed-assault vehicle loss drops 8 points per level.

## Save export and import
- Export a single slot or all four slots (autosave and three manual) in a bundle. Import single or bundle.
- Buttons on the title screen and in Settings.
- Imports from newer builds are blocked; older builds are accepted and upgraded.
- Import only into empty slots.

## Characters and portraits
- Stylized silhouettes with role badges. Subjects: generated team members, permanent staff, faction contacts, Special Ops units and logistics bases.
- Shown in the Barracks team edit screen and member rows, and in room staff strips.
- Reflect injured, killed and captured states.
- Mockups first; nothing is added until Brad has seen them.
- No likenesses of the show's characters or actors; staff get original silhouettes with rank and role badges.

## Sound and music
- Adds: expanded gate sounds, per-room ambience, UI and alert sounds, music.
- Settings: Master, Music and Effects sliders.
- Production method open: Brad leans to embedded audio files; size estimate 5-9 MB total versus about 50 KB if synthesized in code. Demos of both music styles (dark ambient, orchestral-style) to be rendered for him to hear before deciding.

## Mobile touch layout (parked, future task)
- No phone version. A tablet would be a separate exclusive version.
- Touch items already listed: dialing computer keys and rotate cluster, starmap pan and zoom, minigames, mission builder dropdowns.
- Gate Room on small screens: scrollable stack. Tested on a real device by Brad, not soon.

## Base upgrades
- Electrical Station room card: where researched reactor upgrades are installed and where the ZPM is installed.
- New rooms wanted: Intelligence / Communications, Training, Engineering / Workshop.
- Paid in supplies and build time like Lab upgrades.
- Build split decided after design is finished.
- Open: what each new room does, Electrical Station tiers and ZPM effect, unlock levels, costs, whether Engineering hosts the vehicle parts.
