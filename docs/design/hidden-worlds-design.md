# Hidden worlds and decoded faction contact (built in 0.9.17, not released)

Decided with Brad, Oct 26 2026.

Concept: the Archeology Office glyph decode (Linguist on station) reveals hidden worlds, as the cartouche does in the TV series.

Decisions:
- Reveal method: decode to reveal. The artifact is decoded and the world and its address appear on the starmap. No partial address, no survey step.
- One artifact per hidden world.
- Every system has at least one hidden world.
- First decode shows a popup with a short mini-story summary tied to TV series lore.
- Candidate first find: the cartouche that leads to Abydos.
- Factions: the factions now found by Exploration faction leads (0.8.10) shift onto the hidden worlds. Contact comes from decoding instead of exploration. Diplomacy there makes the worlds Peaceful.

Open questions (Brad to decide before building):
- What each hidden world gives (unique find, one-time reward, other).
- How the 0.8.10 faction-lead rule and the current diplomacy rules are reworked.
- Which worlds and stories go in which system, and the artifact each uses (the ten existing glyph artifacts or new ones).
- Hidden world count per system beyond the minimum of one.

Related: docs/design/faction-design.md, docs/design/minigames-design.md (glyph decoding), docs/design/galaxy-design.md.

## Decisions, Oct 27 2026 (Brad)
- Build slot: 0.9.17 (hidden worlds and decoded faction contact).
- 0.8.10 faction leads on Exploration returns are removed. Faction contact comes only from decoding. Factions already met in older saves stay met.
- Each hidden world: first-decode popup with a mini-story, a brief history of the faction, and the rewards and bonuses the faction offers; plus a one-time reward of supplies or research.
- New artifacts are authored for the hidden worlds (separate from the existing ten bonus glyph artifacts).
- Placement stays as the current assignment: L1 Langaran, L2 Tollan, L4 Tok'ra and Free Jaffa, L5 Asgard and Nox. Level 3 gets a story-only hidden world with no faction.
