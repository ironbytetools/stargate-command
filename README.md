# Stargate Command

A Stargate SG-1 base-management game in a single HTML file. Current build: 0.9.14.

## Play and read
- dist/sgc-command.html: the playable game (current release, open in a browser); dist/sgc-command.html.zip is the same file zipped
- dist/sgc-minigame-showcase.html: every minigame playable on its own (sandbox, nothing is saved, no music)
- dist/SGC-Command-Game-Guide.pdf: the player guide for the current release

## Project records
- CHANGELOG.md: what each build changed, how it was verified, open assumptions (newest at the bottom)
- ROADMAP.md: ideas, decisions and what is next
- docs/design/: one design note per system (armory, backlog, diplomacy, device minigames, drone scanning, factions, galaxy, gate power, gate upgrades, lab, logistics, minigames, missions, reactor, rescue, research, and more)
- docs/reports/: balance reports and what-if analysis

## Layout
- dist/: release files only (what gets played, shared or printed)
- builds/: working builds, one HTML file per version; builds/archive/ holds every older build
- tools/patches/build-X.Y.Z/: the patch script and parts that turn the previous build into that version
- tools/guide/: source of the Game Guide PDF (render.sh)
- tools/showcase/: source of the minigame showcase
- tools/audio/: sound effect and music build scripts
- tools/balance-sim/: headless playtest bot and analysis scripts
- assets/soundtrack/: source music; assets/mockups/: design mockups; assets/reference/: reference screenshots and sound reels

## Release steps
1. Build the new version: python3 tools/patches/build-X.Y.Z/patch_XYZ.py builds/<previous>.html builds/sgc-command-X.Y.Z.html
2. Copy it to dist/sgc-command.html and rewrite dist/sgc-command.html.zip
3. Move the previous builds to builds/archive/
4. Rebuild the showcase: python3 tools/showcase/patch_showcase.py dist/sgc-command.html dist/sgc-minigame-showcase.html
5. Rebuild the Game Guide in tools/guide/ and copy the PDF to dist/
6. Update CHANGELOG.md, ROADMAP.md and the build number above
