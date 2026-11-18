# Sound census, 2026-11-16: what the GBA build still plays as pret made it

*T-565, the census first (the user, 2026-11-16). Nothing in the engine or its audio was changed to make this. It is a
snapshot of `engineGba/` (pokefirered-daemons at `637f5751f`) compared with `upstream/master` (pret/pokefirered).
It is meant to agree the split with the Musical Instruments lane, which owns `src/play.c` and the songs (T-417, T-521).*

**How it was counted.** Every `MUS_` and `SE_` constant in `include/constants/songs.h` was looked up in `src/`,
`data/` (scripts, map scripts, battle scripts, battle animation scripts) and every `data/maps/*/map.json` music field.
**Ours** means its `.mid` in `sound/songs/midi/` differs from upstream's or is new. **Pret's** means the file is
byte-identical to upstream. **Unused** means nothing reachable plays it: no reference at all, a reference only in code
the game never reaches, or a reference only in the wireless, link, Mystery Gift or e-Reader features.
"How often a player hears it" is estimated from the structure of the game (how many maps, how many trainers, which
events). No play-time data was recorded.

## Where it stands, 2026-11-18: the twelve batches done

*Updated by the Musical Instruments lane after T-565's last batch. The rest of this file is the census as taken on
2026-11-16, kept as the record of where the work began.*

| # | Batch | Lane | Released | Tool |
|---|---|---|---|---|
| 1 | menu and UI sounds | game | v11.385.1 | `genuisounds.py` |
| 2 | battle music, nine slots | instruments | v11.386.1 | `genbattlemusic.py` |
| 3, 7 | fanfares and jingles; the toy piano; the pitched sounds | instruments | v11.384.1 | `genfanfares.py` |
| 4 | battle sounds apart from moves | game | v11.386.1 | `genuisounds.py --batch 4` |
| 5 | everyday overworld music, with LURID's and DOLDRUM's own | instruments | v11.387.1 | `genoverworldmusic.py` |
| 6 | field sounds | game | v11.388.1 | `genuisounds.py --batch 6` |
| 8 | story set-pieces, the credits, THE WALLED GARDEN's own | instruments | v11.388.1 | `genstorymusic.py` |
| 9 | the islands | instruments | v11.390.1 | `genislandmusic.py` |
| 10 | move sounds | game | v11.389.1 | `genuisounds.py` |
| 11 | cries, all 388 | game | v11.391.1 | (the game lane's) |
| 12 | our own instruments under voicegroup191 and the dawn chorus | instruments | v11.392.1 | `genbank.py` |

**Every song and sound effect in the game is ours now, except these.** *Music, 22 slots still pret's* (`MUS_FUCHSIA` plays nowhere since T-592, 2026-11-18: its last six
maps -- the Ember Spa, the Sea Cottage, a house each in HALFTONE and ARDOR, two on SIX ISLAND's water path -- play the
music of the map their door opens onto; the rest are T-593, batch 13, to be drafted): the two game corners' `MUS_GAME_CORNER` with its jingles (`MUS_SLOTS_WIN`, `MUS_SLOTS_JACKPOT`, `MUS_TOO_BAD`); the
union room; scripted scenes (`MUS_FOLLOW_ME` at QUICKSILVER, `MUS_JIGGLYPUFF` in SLATE's CHECKPOINT, `MUS_SCHOOL`,
`MUS_PHOTO`, `MUS_TEACHY_TV_MENU`/`_SHOW`, `MUS_OBTAIN_ITEM`); the legendary and link battle `MUS_RS_VS_TRAINER` and
`MUS_RS_VS_GYM_LEADER`; and what an event ticket or nothing reaches (`MUS_ENCOUNTER_DEOXYS`, `MUS_VS_DEOXYS`,
`MUS_MYSTERY_GIFT`, `MUS_BERRY_PICK`, `MUS_POKE_JUMP`, `MUS_OBTAIN_BERRY`, `MUS_INTRO_FIGHT`, `MUS_HEAL_UNUSED`).
*Sound effects, 43 still pret's:* mostly the wireless games, contests and berries the build never reaches
(`SE_BALLOON_*`, `SE_CONTEST_*`, `SE_POKE_JUMP_*`, `SE_BERRY_BLENDER`, `SE_POKENAV_*`, the truck), the game corner's
roulette, and fourteen move sounds batch 10 left as they were (`SE_M_HEAL_BELL` and `SE_M_MORNING_SUN` among them, which
battle keeps; the field has had its own since batch 3). **Whether any of these is drafted is the user's call.**

## Headline

| | Constants | Ours | Pret's, still played | Pret's, not played |
|---|---|---|---|---|
| **Music** (`MUS_`, 256 and up) | 110 | **30** | **66** (2 only via an event ticket) | 14 |
| **Sound effects** (`SE_`, 1–255 and ours after 350) | 273 | **18** | **221** | 34 |
| of which move animations (`SE_M_`) | 130 | 0 | 122 | 8 |
| **Cries** (not `SE_` constants) | 388 | 0 | **388**, all of them | 0 |

- **Every sound effect the player hears is pret's**, except PLAY's sixteen notes (the HARP and the FLUTE), THE
  CREATOR'S HOUR's tone and THE DAWN CHORUS. That includes every menu click, every battle sound and every cry.
- **Most music by map count is ours.** That covers BLANCHE, CALLOW, SLATE, BRAZEN, VERDIGRIS, ARDOR, HALFTONE,
  QUICKSILVER, the routes out of BLANCHE, the dark places, the Corpus building, the ruined lab, the fourteen groves and
  THE NEXUS. **But battle music is entirely pret's**, and battle is where a player spends the most listening time.
- **A second layer, for later.** Our songs on `voicegroup191` (the title, CALLOW, the groves, THE NEXUS) have our notes
  but use the retail instrument samples (`sc88pro_*`, `steinway_b_piano`, `classical_choir_voice_ahhs`). Our songs on
  `voicegroup192` (the Game Boy bank: the eleven tracks carried from the classic build) use only the GBA's PSG
  channels, with no samples. Only `voicegroup193` (HARP, FLUTE) and the chorus chirp in `voicegroup194` are samples
  we made ourselves. Getting rid of the retail samples is a separate job from getting rid of pret's notes.

## Music

### Ours (30)

| Slot | What it is | Plays in | Made by |
|---|---|---|---|
| `mus_title` | the title theme, transcribed from the rendered recording | title screen | `tools/stems2midi.py` (2026-09-04) |
| `mus_new_game_intro` | the intro theme behind CRYSTAL CLEAR's speech | new game | stems, re-cut 2026-09-06/07 |
| `mus_caught_intro` | the binding sound (the classic build's capture jingle) | every capture, before pret's `MUS_CAUGHT` | `tools/port_music.py` |
| `mus_pallet` | Blanche, with CRYSTAL's motif | BLANCHE and its houses | `port_music.py` |
| `mus_route1` | The Bleed (C to F) | Routes 1 and 2, both underground tunnels | `port_music.py` |
| `mus_mt_moon` | the dark places (05) | Mt. Moon, Rock Tunnel, Victory Road (8 maps) | `port_music.py` |
| `mus_celadon` | Awakening S.T.A.R.R. | VERDIGRIS and 11 interiors | `port_music.py` |
| `mus_cinnabar` | QUICKSILVER: S.T.A.R.R. and Ty | QUICKSILVER, its lab and houses (6) | `port_music.py` |
| `mus_lavender` | Love Persists | HALFTONE and 2 houses | `port_music.py` |
| `mus_vermillion` | Scorn's Solution | ARDOR, 3 houses, the Route 11 gate (6) | `port_music.py` |
| `mus_silph` | Nine Scars, Nine Breaches | the Corpus building (12 floors) | `port_music.py` |
| `mus_poke_mansion` | 1001 Fatal Error | the ruined lab, the Route 21 station (5) | `port_music.py` |
| `mus_brazen` *(appended)* | Fit for Work | BRAZEN and 6 interiors | `port_music.py` |
| `mus_slate` *(appended)* | Slate City | SLATE, its houses and museum (5) | `port_music.py` |
| `mus_callow` *(appended)* | The Christmas Cloak of Self | CALLOW, its house, all seven school floors (9) | `tools/gengrovemusic.py` (T-05) |
| `mus_nexus` *(appended)* | built on the singing fir's notes | THE NEXUS | `tools/gennexustheme.py` (T-409) |
| `mus_grove_*` ×14 *(appended)* | one loop per universe, from the user's recordings | the fourteen groves and the Breathverse | `gengrovemusic.py` (T-408) |

### Pret's, ranked by how often a player hears it

*Tier 1: heard many times an hour, throughout the game.*

| # | Constant | Where it plays | Why it ranks here |
|---|---|---|---|
| 1 | `MUS_VS_WILD` | every wild battle (`GetBattleBGM`, `src/pokemon.c`) | the single most-heard piece in the game |
| 2 | `MUS_VS_TRAINER` | every trainer battle except leaders, Elite Four and the champion | about 700 trainer entries |
| 3 | `MUS_POKE_CENTER` | 58 maps: every centre (both floors), every mart, all of VERDIGRIS's store, the colosseums | visited in every town, over and over |
| 4 | `MUS_VICTORY_WILD` | after every wild win | follows #1 |
| 5 | `MUS_ROUTE3` | 23 maps: Routes 3–10, 16–22, Kindle Road, Treasure Beach, Bond Bridge, Three Island Port, Cape Brink | the game's main route theme |
| 6 | `MUS_LEVEL_UP` | every level-up, **every item found** (`EventScript_PlayFanfareObtainedItem`), TMs, 46 call sites | a fanfare you hear dozens of times an hour |
| 7 | `MUS_VICTORY_TRAINER` | after every trainer win | follows #2 |
| 8 | `MUS_CYCLING` | whenever the player rides the bike, in place of the map's own music | covers our town and route themes too, from mid-game on |
| 9 | `MUS_HEAL` | every centre heal, the rival's house, the S.S. ANNE captain | each centre visit |
| 10 | `MUS_ENCOUNTER_BOY` | the trainer "eyes meet" jingle for 440 trainer entries (male, intense, cool, swimmer, hiker, rich, Elite Four) | before most trainer battles |

*Tier 2: heard every session, or for long stretches of one part of the game.*

| Constant | Where it plays |
|---|---|
| `MUS_ENCOUNTER_GIRL` | the eyes-meet jingle for 157 entries (female, girl, twins) |
| `MUS_ENCOUNTER_ROCKET` | the eyes-meet jingle for 145 entries (suspicious, and every class without its own) |
| `MUS_FUCHSIA` | 20 maps: DOLDRUM and LURID with their houses, the bike shop, the Safari office, the Sea Cottage, the Ember Spa |
| `MUS_PEWTER` | 22 maps: every gatehouse, Route 2's buildings, the Day Care, the underground entrances |
| `MUS_GYM` | all ten gyms, and the UMBRA PLATEAU centre and Lorelei's room |
| `MUS_VS_GYM_LEADER` / `MUS_VICTORY_GYM_LEADER` | every leader and the Elite Four |
| `MUS_SURF` | whenever the player is on the water |
| `MUS_VIRIDIAN_FOREST` | 13 maps: the forest, Diglett's Cave, Seafoam Islands, Berry Forest, Dunsparce Tunnel, Pattern Bush |
| `MUS_ROUTE11` | Routes 11–15 |
| `MUS_ROUTE24` | Routes 24 and 25, and the start of the new-game speech |
| `MUS_CAUGHT` | every capture, after our `mus_caught_intro` |
| `MUS_OBTAIN_KEY_ITEM` | 35 call sites: every key item, including our own story items |
| `MUS_OBTAIN_TMHM`, `MUS_OBTAIN_BADGE` | each TM given by a person, each MARK |
| `MUS_EVOLUTION_INTRO`, `MUS_EVOLUTION`, `MUS_EVOLVED` | every evolution; **`MUS_EVOLUTION` is also the Safari Zone's map music (9 maps)**, and `MUS_EVOLVED` plays in `daemons_spirits.c` |
| `MUS_GAME_FREAK` | **every boot**, as the logo's star (played as a sound effect in `intro.c`, before our thank-you card) |
| `MUS_SEVII_123`, `_45`, `_67`, `_ROUTE`, `_CAVE`, `_DUNGEON` | the islands: 15, 11, 9, 18, **53** and 14 maps. Five groves and FINDERS BEACH are out there |
| `MUS_NET_CENTER` | One Island's centre (both floors) |
| `MUS_SS_ANNE` | 26 maps, one visit |
| `MUS_ROCKET_HIDEOUT` | 11 maps: the hideout, the Power Plant (moved here on purpose), Cerulean Cave, the warehouse, Bruno's room |
| `MUS_POKE_TOWER` | the tower in HALFTONE (7 floors) and Agatha's room |
| `MUS_VICTORY_ROAD` | UMBRA PLATEAU's exterior, Route 23, Lance's room, the champion's room |
| `MUS_TRAINER_TOWER` | Trainer Tower (11 maps) |

*Tier 3: heard once, or a handful of times, at story moments.*

`MUS_ENCOUNTER_RIVAL` and `MUS_RIVAL_EXIT` (the rival's eight scenes); `MUS_OAK` and `MUS_OAK_LAB` (BLANCHE's opening);
`MUS_NEW_GAME_INSTRUCT` and `MUS_NEW_GAME_EXIT` (around our intro theme); `MUS_ENCOUNTER_GYM_LEADER` (16 set pieces,
**including THE NEXUS**); `MUS_VS_CHAMPION`; `MUS_VS_LEGEND` and `MUS_VS_MEWTWO`; `MUS_HALL_OF_FAME`, `MUS_SLOW_PALLET`
(the Hall of Fame room) and `MUS_CREDITS`; `MUS_MOVE_DELETED`; `MUS_DEX_RATING`; `MUS_POKE_FLUTE`; `MUS_PHOTO`;
`MUS_JIGGLYPUFF` (SLATE's centre); `MUS_SCHOOL` (a house in Sevault Canyon); `MUS_FOLLOW_ME` (QUICKSILVER);
`MUS_GAME_CORNER` (two game corners); `MUS_TEACHY_TV_MENU` (the Teachy TV item).
**Only through an event ticket:** `MUS_ENCOUNTER_DEOXYS`, `MUS_VS_DEOXYS` (Birth Island).

### Pret's, not played (14)

- **Never reached:** `MUS_INTRO_FIGHT` (T-320's thank-you card goes straight to the title, so intro scene 1 never
  runs); `MUS_OBTAIN_ITEM` (decorations, Mystery Gift and the e-Reader only, plus a DEBUG hotkey); `MUS_OBTAIN_BERRY`,
  `MUS_SLOTS_JACKPOT` and `MUS_SLOTS_WIN` (only in the fanfare table); `MUS_HEAL_UNUSED` and `MUS_TEACHY_TV_SHOW` (no
  references); `MUS_DUMMY` (silence).
- **Wireless, link or Mystery Gift only:** `MUS_RS_VS_TRAINER`, `MUS_RS_VS_GYM_LEADER`, `MUS_UNION_ROOM`,
  `MUS_MYSTERY_GIFT`, `MUS_BERRY_PICK`, `MUS_POKE_JUMP`, `MUS_TOO_BAD`.

None of these needs a replacement. A future cleanup could point them at silence, which would also shrink the ROM.

## Sound effects

### Ours (18)

`SE_HARP_C` to `SE_HARP_C_HIGH` and `SE_FLUTE_C` to `SE_FLUTE_C_HIGH` (16): PLAY's notes, reached as
`SE_HARP_C + n` from `src/play.c` and `src/daemons_signature.c`. `SE_AAH_PAD`: THE CREATOR'S HOUR (`daemons_hours.c`).
`SE_DAWN_CHORUS`: the dawn chorus (`daemons_hours.c`, `daemons_aurora.c`).

### Pret's, still played (221), grouped by context

*The count is call sites in C and scripts, a rough guide to how much each is used. It is not a measure of how often it
is heard: one call site for `SE_DOOR` fires at every door in the game.*

**Menus and UI (25), the most-heard sounds in the game.**
`SE_SELECT` **477 call sites**, by far the most-heard sound in the build: every confirmation in every menu, our own
NOTEBOOK, school, NEXUS and book reader included. Then `SE_FAILURE` 32, `SE_PC_LOGIN` 14, `SE_BOO` 14, `SE_CLICK` 14,
`SE_USE_ITEM` 13, `SE_SHOP` 12, `SE_WIN_OPEN` 9 (the start menu opening), `SE_DING_DONG` 7, `SE_PC_OFF` 6,
`SE_CARD_OPEN` 6, `SE_BAG_POCKET` 6, `SE_SUCCESS` 5, `SE_RS_SHOP` 5, `SE_SAVE` 4, `SE_BAG_CURSOR` 4, `SE_PC_ON` 3,
`SE_CARD_FLIP` 2, `SE_CARD_FLIPPING` 2, `SE_ROTATING_GATE` 1, `SE_DEX_SCROLL` 1, `SE_DEX_PAGE` 1, `SE_HELP_OPEN`,
`SE_HELP_CLOSE` and `SE_HELP_ERROR` 1 each. *(The region map and Fame Checker also borrow four move sounds:
`SE_M_SWIFT`, `SE_M_SPIT_UP`, `SE_M_LOCK_ON`, `SE_M_HYPER_BEAM2`.)*

**Battle, apart from moves (24).**
Every battle: `SE_MUGSHOT` and the transition, `SE_BALL_OPEN`, `SE_BALL_TRAY_ENTER`, `SE_BALL_TRAY_BALL` and
`SE_BALL_TRAY_EXIT` (the party balls), `SE_EFFECTIVE`, `SE_NOT_EFFECTIVE`, `SE_SUPER_EFFECTIVE` (every hit),
`SE_FAINT`, `SE_EXP` and `SE_EXP_MAX`, `SE_LOW_HEALTH` (the low-HP alarm, which loops), `SE_FLEE`.
Every capture: `SE_BALL_THROW`, `SE_BALL`, `SE_BALL_BOUNCE_1` to `_4`, `SE_BALL_CLICK`, `SE_BALL_TRADE`.
Rare: `SE_SHINY`, `SE_SWITCH`, `SE_DEOXYS_MOVE`. *The effectiveness three are worth calling out: the type chart is
the argument (CLAUDE.md invariant 3), and the sound of a hit landing is the chart speaking.*

**Move animations (119 `SE_M_` in battle, and 3 used only outside battle).**
Every move plays one or more. The battle animation scripts were rewritten heavily for DAEMONS (about 14,000 changed
lines, T-392, T-480, T-489), but still draw on 123 of pret's sounds. `genanims.py` chooses which vanilla sound each routine borrows. The most-used are `SE_M_MINIMIZE` (**220
uses**: the default cue in `tools/genanims.py`, which writes the generated routines, T-134), `SE_M_ICY_WIND` 25, `SE_M_COMET_PUNCH` 22, `SE_M_BUBBLE3` 19,
`SE_M_TELEPORT` 15, `SE_M_TAKE_DOWN`, `SE_M_DRAGON_RAGE` and `SE_M_PSYBEAM2` 18 each, and `SE_M_PSYBEAM` 16.
Twenty-eight of them are also used in the field or in menus: `CUT` (36 sites, every grove's bush), `STRENGTH`,
`ROCK_THROW` (Rock Smash), `FLY`, `DIG`, `TELEPORT`, `HEAL_BELL` (GOTO's ribbon, our unity and spirits scenes), `MORNING_SUN` (the NOTEBOOK), `MOONLIGHT`, `HAZE`, `CONFUSE_RAY`, `REFLECT` (Flash), `SWEET_SCENT`, `RAZOR_WIND2`, `EXPLOSION`,
`WING_ATTACK`, `HARDEN`, `MINIMIZE` (our spellbook), and evolution and trade sparkles. `SE_M_DIVE` is used only in
the field.

**Field (50).**
Moving around: `SE_DOOR` and `SE_SLIDING_DOOR` (every door), `SE_EXIT` 14, `SE_WARP_IN` 27 and `SE_WARP_OUT` 4 (every
warp, PLAY's door, THE NEXUS), `SE_LEDGE`, `SE_WALL_HIT` (walking into a wall), `SE_BIKE_HOP`, `SE_BIKE_BELL`,
`SE_PUDDLE`, `SE_FALL` 7, `SE_ICE_BREAK`, `SE_ICE_CRACK`, `SE_ESCALATOR`, `SE_ELEVATOR` (the school's lift).
Events: `SE_PIN` 31 (the "!" over a head), `SE_UNLOCK` 18, `SE_REPEL`, `SE_ITEMFINDER`, `SE_FIELD_POISON`,
`SE_GLASS_FLUTE`, `SE_EGG_HATCH`, `SE_APPLAUSE` (Hall of Fame), `SE_VEND`, `SE_BANG`, `SE_SHIP`, `SE_SS_ANNE_HORN`,
`SE_RS_DOOR`, `SE_TRUCK_MOVE`, `SE_LAVARIDGE_FALL_WARP`, `SE_CONTEST_CURTAIN_FALL`, `SE_CONTEST_MONS_TURN` (the VS
Seeker), `SE_CONTEST_PLACE` (the slot machine), `SE_POKE_JUMP_FAILURE` (the start menu).
Weather: `SE_RAIN`, `SE_RAIN_STOP`, `SE_DOWNPOUR`, `SE_DOWNPOUR_STOP`, `SE_THUNDERSTORM`, `SE_THUNDERSTORM_STOP`,
`SE_THUNDER`, `SE_THUNDER2`. These are heard more often than in vanilla because of the weather and hours work.
**The toy piano, `SE_NOTE_C` to `SE_NOTE_C_HIGH` (8):** pret's Glass Flute and berry-picking notes, which DAEMONS
uses for **the day's note** (`SE_NOTE_C + weekday`, in `field_control_avatar.c` and `field_specials.c`) and for **the
singing fir's tune and the holiday songs** (`field_specials.c`, `src/data/daemons_holidays.h`).

**Cries (388): every one is pret's.** `sound/cry_tables.inc` and `sound/direct_sound_samples/cries/` are untouched.
Every battle plays at least two, and so do every switch-in, the INDEX and every party screen. A cry is a recorded
sample (DirectSound), not a MIDI. It is the largest single body of Nintendo audio left in the build, and the hardest
to replace.

### Pret's, not played (34)

- **No reference (29):** `SE_FU_ZAKU`, `SE_CONTEST_CONDITION_LOSE`, `SE_CONTEST_HEART`, `SE_CONTEST_CURTAIN_RISE`,
  `SE_CONTEST_ICON_CHANGE`, `SE_CONTEST_ICON_CLEAR`, `SE_ICE_STAIRS`, `SE_TRUCK_STOP`, `SE_TRUCK_UNLOAD`,
  `SE_TRUCK_DOOR`, `SE_BERRY_BLENDER`, `SE_BRIDGE_WALK`, `SE_BALLOON_BLUE`, `SE_BALLOON_YELLOW`, `SE_ROULETTE_BALL`,
  `SE_ROULETTE_BALL2`, `SE_TAILLOW_WING_FLAP`, `SE_INTRO_BLAST`, `SE_ORB`, `SE_POKENAV_OFF`, `SE_DEX_SEARCH`, and eight
  move sounds: `SE_M_GUST2`, `SE_M_FLAME_WHEEL2`, `SE_M_FIRE_PUNCH`, `SE_M_PAY_DAY`, `SE_M_BRICK_BREAK`,
  `SE_M_GIGA_DRAIN`, `SE_M_TRI_ATTACK2`, `SE_M_ATTRACT2`.
- **Wireless minigames only (5):** `SE_POKENAV_ON`, `SE_BALLOON_RED`, `SE_BREAKABLE_DOOR`, `SE_MUD_BALL`,
  `SE_POKE_JUMP_SUCCESS`.

## Proposed batches, most-heard first

*A proposal for agreeing the split, not a decision. The line drawn here: **songs, fanfares and anything pitched or
played as an instrument go to the Musical Instruments lane** (it owns `play.c` and the songs). **Short non-musical
sound effects and the wiring (which map or event plays what) go to the game lane.** Where a batch is both, the lane
that writes the notes leads and the other lane wires them.*

| # | Batch | What is in it | Lane |
|---|---|---|---|
| 1 | **Menu and UI sounds** | `SE_SELECT` and the 24 others above. One small family of sounds in one timbre, made once and used everywhere | **game** |
| 2 | **Battle music** | `MUS_VS_WILD`, `MUS_VS_TRAINER`, `MUS_VICTORY_WILD`, `MUS_VICTORY_TRAINER`, then `MUS_VS_GYM_LEADER`, `MUS_VICTORY_GYM_LEADER`, `MUS_VS_CHAMPION`, `MUS_VS_LEGEND`, `MUS_VS_MEWTWO`. Four slots cover most of a player's battle time | **instruments** (game wires any change to `GetBattleBGM`) |
| 3 | **Fanfares and jingles** | `MUS_LEVEL_UP`, `MUS_HEAL`, `MUS_CAUGHT`, `MUS_OBTAIN_KEY_ITEM`, `MUS_OBTAIN_TMHM`, `MUS_OBTAIN_BADGE`, the three eyes-meet jingles (`MUS_ENCOUNTER_BOY`, `_GIRL`, `_ROCKET`), `MUS_EVOLUTION_INTRO`, `MUS_EVOLUTION`, `MUS_EVOLVED`, `MUS_MOVE_DELETED`, `MUS_DEX_RATING`, `MUS_POKE_FLUTE`, `MUS_GAME_FREAK`. Each is a few seconds long and heard constantly: the cheapest big win | **instruments** |
| 4 | **Battle sounds, apart from moves** | the effectiveness three, `SE_FAINT`, `SE_EXP`, `SE_LOW_HEALTH`, `SE_FLEE`, `SE_MUGSHOT`, the ball and tray family | **game** |
| 5 | **Everyday overworld music** | `MUS_POKE_CENTER`, `MUS_ROUTE3`, `MUS_CYCLING`, `MUS_SURF`, `MUS_FUCHSIA` (DOLDRUM, LURID), `MUS_PEWTER` (gatehouses), `MUS_GYM`, `MUS_ROUTE11`, `MUS_ROUTE24`, `MUS_VIRIDIAN_FOREST`. Several have candidates already: song-status.md lists 14 reviewed opera tracks with no home | **instruments** for the notes; **game** for re-pointing maps (`port_music.py`'s `MAP_MUSIC`, map.json) |
| 6 | **Field sounds** | doors, warps, ledge, wall, bike, puddle, fall, ice, `SE_PIN`, `SE_UNLOCK`, the item and repel sounds, weather, and the field uses of `SE_M_CUT`, `STRENGTH`, `ROCK_THROW`, `FLY`, `DIG`, `TELEPORT` | **game** |
| 7 | **The toy piano** | `SE_NOTE_C` to `SE_NOTE_C_HIGH`: the day's note, the singing fir, the holiday songs. Probably moved onto the HARP and FLUTE voices so there is one instrument voice in the game | **instruments** |
| 8 | **Story set-piece music** | the rival's two, `MUS_OAK`, `MUS_OAK_LAB`, `MUS_NEW_GAME_INSTRUCT`, `MUS_NEW_GAME_EXIT`, `MUS_ENCOUNTER_GYM_LEADER` (THE NEXUS uses it), `MUS_SS_ANNE`, `MUS_ROCKET_HIDEOUT`, `MUS_POKE_TOWER`, `MUS_VICTORY_ROAD`, `MUS_TRAINER_TOWER`, `MUS_HALL_OF_FAME`, `MUS_SLOW_PALLET`, `MUS_CREDITS`, the Safari Zone (`MUS_EVOLUTION`'s map use: give it its own slot) | **instruments** (several are natural homes for the unplaced opera tracks) |
| 9 | **The islands** | the six `MUS_SEVII_*` and `MUS_NET_CENTER` | **instruments** |
| 10 | **Move animation sounds** | the 119 `SE_M_` sounds in battle. Too many to replace one by one; better done as a small palette per DAEMONS type, chosen in `tools/genanims.py` (which already picks each routine's sound) | **game** |
| 11 | **Cries** | all 388. A separate ticket: a daemon's voice is a design question before it is an audio one | **game**, design first |
| 12 | **Retail samples under our own songs** | `voicegroup191`'s and `194`'s `sc88pro_*`, `steinway_b_piano` and choir, swapped for samples we make, as `geninstruments.py` did for PLAY | **instruments** |
| — | not played | the 14 songs and 34 sound effects listed as not played. No replacement needed | — |

## Pipeline: what exists for making our own

**Music** has five ways in, and every one writes a MIDI into `sound/songs/midi/` plus a line in `midi.cfg` that
names its voicegroup:

- `tools/port_music.py`: the classic build's RGBDS tracks re-emitted as MIDI on `voicegroup192` (PSG, the Game Boy
  bank). It also owns which maps play each town's theme (`MAP_MUSIC`). It **replaces a slot's MIDI** rather than
  adding a row, so no constant moves. This is the cheapest way to swap a pret track out.
- `tools/mp3midi.py`: transcribes a recording with librosa (signal processing, not a model).
- `tools/stems2midi.py` (with `tools/bpextract.py`): builds a track from separated stems. Used for the title.
- `tools/gengrovemusic.py`: loops cut from the user's recordings onto a universe's "band" voicegroup. Used for
  the groves and CALLOW.
- `tools/gennexustheme.py`: a theme composed in code on known notes. Used for THE NEXUS.

**Sound effects.** Our 18 were made by `tools/genplaysounds.py` (16 one-note MIDIs on `voicegroup193`),
`tools/geninstruments.py` (HARP and FLUTE *synthesized*, Karplus-Strong and a breathy sine, written as
`daemons_harp.wav` and `daemons_flute.wav` into `direct_sound_samples/`) and `tools/genchorus.py` (a synthesized
rising chirp plus a choir pad, on `voicegroup194`). Every one of them was **appended**: a new constant after 350 in
`songs.h`, a new row in `song_table.inc` (player 2 or 3) and a new `midi.cfg` line. **Replacing a pret SE in place is
simpler:** since pret converted every sound effect to MIDI (upstream, March 2026), `se_select.mid` and the rest can be
overwritten with no constant or table change. Most of pret's SEs use the PSG square and noise voices, so a
synthesized replacement needs no sample at all. **There is no general SE generator yet.** Batch 1 would want one, along
the lines of `genplaysounds.py`: a few lines per effect, a `--preview` WAV, and the `--write` and report habit every
`tools/` script follows.

**The history, from `git log` in the engine:** 2026-09-02/03, the eleven classic tracks were carried
(`port_music.py`); 09-04, the capture sound and `voicegroup192`; 09-04, the title from stems on `voicegroup191`;
09-06/07, the intro theme; 09-23, SLATE given its own slot and `mus_pewter` put back to pret's (T-226); 10-16, THE
NEXUS (T-409); 10-17, the fourteen groves (T-408) and PLAY's notes (T-417); 10-18, our own HARP and FLUTE (T-425);
10-19, CALLOW (T-05); 11-04, THE CREATOR'S HOUR's pad (T-519); 11-07, the dawn chorus (T-528). **No pret sound effect
has been replaced. All 18 of ours are new sounds.**
