# DAEMONS v11.307.3 — release notes

*Released 2026-10-20 21:29 · built against the design bible v11.307*

- **Engine**: CodeMusic/pokefirered-daemons `b85aa8e46` (context-content)
- **Design**: CodeMusic/DAEMONS `44563659`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `d5ad72517d9aad8281700749a7aab07c31bf38b5` |
| `daemonsContext.gba` | CONTEXT | `0e44254fe4fb8bf71eb43ea2f002fb1ed628ea16` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `5cfeb692b83537700ec268738da9ea4dd5393285` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `db2509f2cf3d3599efb69c9e65d9eb0bea87d018` |

## The engine since v11.307.2

- `b85aa8e46` T-18 P2: A on THE FOLLOWER -- facing the tile it stands on and pressing A (field_control_avatar.c asks Follower_GetInteractionScript after the people, before the signs: it is a sprite, so a person on its tile answers first) runs EventScript_Follower (data/scripts/follower.inc). Follower_Talk turns it to face the player, lifts the trainers' own bubble over it (trainer_see.c's CreateEmoticonSprite: ? at friendship 0-99, ! at 100-219, the smile at 220-255, !! when it notices something) and leaves its words in gStringVar4, in the daemon's text colour: the line for its friendship (the plan's five readings, 0-49/50-99/100-149/150-219/220-255), then one mood when one holds -- an unfound hidden item within two tiles (not underfoot ones), the place (THE NEXUS; HALFTONE, DOLDRUM CAVE unread with it), and outdoors outside BREATHVERSE the sky (rain, thunderstorm, snow, fog, wind), the watch (night, dusk, dawn; the day has none), else the season. A mood's two lines take turns. 34 lines, every one DRAFT, each at most 208px with a 10-letter name. Costs: IWRAM 0 (the turn counter fits sFollower's padding, still 72 B), EWRAM 0, save 0, ROM ~3 KB (code ~1.3 KB, lines ~1.6 KB).

## The design and tools since v11.307.2

- `44563659` T-18 P2 built (engine b85aa8e46): A on the follower -- tools/routes/follower-talk.json (12 stops: friendship 0/70/120/150/255, night/dusk/dawn, rain/thunderstorm/snow/fog/wind, the four seasons, HALFTONE, THE NEXUS, a hidden item noticed, indoors the friendship line alone; all pass in CONTENT and CONTEXT); theatre_route.py learns `follower talk` (face it without stepping into it, film the bubble, capture the boxes); TODO notes P2 on T-18's row
- `9b093ea1` TODO: T-18 P1 released v11.307.2; the user keeps the sprite and the 8 OPTIONS rows, wants shiny palettes (P3)
- `3b65a12f` qa: T-18 P1 the follower walks and hides
- `04a087da` ROM release v11.307.2: a follower daemon walks behind you and hides -- T-18 P1 (OPTIONS row FOLLOWER, DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
