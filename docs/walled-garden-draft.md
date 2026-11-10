# THE WALLED GARDEN -- the SAFARI ZONE redrafted (T-540, DRAFT)

**Every in-game line in this file is DRAFT.** Nothing here is in the engine, the companion or `vision.md`; it is for
the user to pick from. Written 2026-11-10 from the user's multiple-choice decision of the same day.

## The decision

The SAFARI ZONE stops being a pay-to-hunt animal park and becomes **THE WALLED GARDEN**: a curated, walled platform
run as a sandbox. The user wanted something like a quarantine zone that is not about illness; a sandbox is exactly
that, the isolation of untrusted code. The agreed shape:

- daemons that are not signed run only inside the wall, and the wall exists so that nothing leaves unvetted;
- the GUESTBOX is an expiring guest session (the tip *"The clock only runs while you walk"* is a metered session);
- the four zones become four **RINGS** of permission;
- the WARDEN, nicknamed LATENCY, keeps the platform and holds his TOKEN;
- the SECRET HOUSE's prize, DRIVER03 TRAVERSE (a ferry across water), is the way out.

The name is THE WALLED GARDEN wherever a player reads it. Dialogue shortens it to *the GARDEN* where a person
would. **SAFARI ZONE survives only as an old name someone remembers**: A puts it on a shelf in the WARDEN's house;
B gives it to HOLT's grandfather and to a father on the boat.

**Craft rules held.** Nobody says what a walled garden is for or what it costs (rule 1): the visitors love it, the
staff are cheerful, and the jokes carry it (rule 6). No illness word appears anywhere, and the vanilla office line
*"I think he's got a speech problem!"* -- a pathology -- is replaced in both directions by what actually happened:
his words are unsigned (rule 3). People are animals; no line names a species.

## Two choices that run through every line

1. **A or B, line by line.** A is the light touch: the name, the session, the RINGS, a joke or two. B leans on the
   wall: messages held as PENDING, a notice nobody can sign, a WARDEN who hid the door himself.
2. **How the RINGS count** (the four area signs). **A counts down, as a processor does**: RING 3 at the gate
   (CENTER), RING 2 (EAST, vanilla's AREA 1), RING 1 (NORTH, AREA 2), **RING 0** (WEST, AREA 3) where the SECRET
   HOUSE and the way out are: the deeper, the more privileged. **B counts up by depth**: RING 1 to RING 4. Dialogue
   says *the innermost RING* or *the deepest RING*, so it reads right either way.

## Widths -- THE WALLED GARDEN fits everywhere but one box

THE WALLED GARDEN is 17 characters, **102px** in the normal font and **84px** in the small one (measured with
`tools/fontwidth.py`, the engine's own tables). Today's widest place name is CORPUS WAREHOUSE (96px, 80px small).

| surface | where | room | THE WALLED GARDEN | |
|---|---|---|---|---|
| map-name popup | `map_name_popup.c` | 112px | 102px | fits, 10 to spare |
| name card (T-445) | `map_preview_screen.c` `sMapNameWindow` | 104px | 102px | **fits, 1px each side** |
| region map name | `region_map.c` WIN_MAP_NAME | 118px | 102px | fits |
| SAVE window | `start_menu.c` PrintSaveStats | 112px | 102px | fits |
| every name buffer | `mapName[19]`, `dungeonName[19]`, `mapName[25]`, `place[32]` | 18 characters | 17 | fits |
| FAME CHECKER place | `fame_checker.c`, small font | 84px | 84px | **fits, 0 to spare** |
| **INDEX FIRST MET** | `pokedex_screen.c` DexScreen_PrintFirstMet, small font | **80px** | **84px** | **4px OVER** |

**The one problem is the INDEX's FIRST MET box.** It prints `MET <place>` in an 80px window, or the place alone when
that is wider -- and the place alone is 84px, so a daemon first met in the GARDEN would draw 4px past its window.
CORPUS WAREHOUSE is exactly 80 today, so nothing has needed a fallback before. Three ways, for the user:

- **(recommended)** keep THE WALLED GARDEN everywhere and teach that one box to drop a leading `THE ` when the place
  is still too wide: it prints **WALLED GARDEN** (65px small). One `if` in `DexScreen_PrintFirstMet`; no name
  changes, and any later `THE ...` place gets the same fallback.
- name the mapsec **WALLED GARDEN** (78px, 65px small) and keep THE WALLED GARDEN in dialogue and signs only. Fits
  every surface with room, but the popup and the map would not say the name the user chose.
- name it **THE GARDEN** (60px). Rejected here: it loses the wall, which is the whole idea.

The START menu's RETIRE row is the other tight one: a column holds 48px after its cursor (T-483). **LOG OUT** is
42px; **SIGN OUT** is exactly 48, 0 to spare. A takes LOG OUT.

Every DRAFT line below was measured the way `check_lexicon.py` measures (`{PLAYER}` as seven W's, codes as
nothing) against its own pane: message boxes and signs 208px; the START description, region-map description,
quest log and help panes against the widest line the engine already ships in them (233, 196, 216 and 248px; help
topics 208). **None is over.**

## The census -- every player-visible SAFARI, and what else the change touches

Read from engineGba at `b1280ca99` (read only). *Vanilla* is pret's `upstream/master`.

**Dialogue and signs (data/maps, 12 maps, about 60 labels).** The gate's attendant (13 labels, 6 naming the
place); the OFFICE (4, all about the WARDEN); the four rest houses (SARA and the gift-binder; the tired three; the
items, the prize and T-534's MUSAI line; TILT's line, ROCK, BAIT and the hiker); the SECRET HOUSE attendant (4); the
WARDEN's house (11, the garbled three and the DRIVER04 speech, which names the place); HOLT's grandfather in
FuchsiaCity_House1; LURID CITY's street (two people on the SAFARI GAME, ERIK, and four signs: the zone, the game,
the WARDEN's home, the office); the CHECKPOINT nurse and the MART in LURID; the two passengers in SSAnne_2F_Room5;
and inside, four REST HOUSE signs, four area signs and seven USER TIPS / REQUEST NOTICE signs (T-324).

**Engine strings.** `data/text/safari_zone.inc`: the exit question and the two PA calls (*"Your SAFARI GAME is
over!"*); the rest of that file is unused Hoenn text in Japanese. `src/battle_message.c`: the out-of-GUESTBOXES
ANNOUNCER line (the BOX/BAIT/ROCK/DETACH menu, the GUESTBOXES label and the watching/angry/eating reactions name no
place and stay). `src/strings.c`: the START menu's RETIRE and its description (*"Retire from the SAFARI GAME and
return to the registration counter."*), the step and BOX counter (*"{STR_VAR_1}/{STR_VAR_2} BOXES"*, unchanged),
and the region map's area description (*"An amusement park outside LURID CITY..."*). `src/data/text/quest_log.h`:
two (*"had a great time with DAEMON in the SAFARI ZONE"*, and the bare name). `data/text/help_system.inc`: three
topics (*"What do I do in a SAFARI GAME?"*), two answers and the BOX, BAIT and ROCK help. `data/text/fame_checker.inc`:
TILT's line and its origin place.

**Names, from their sources (never the generated headers, engine.md trap 11).**

- **The mapsec**: `src/data/region_map/region_map_sections.json` `"name": "SAFARI ZONE"` becomes THE WALLED
  GARDEN. It feeds the popup, the region map, the SAVE window, the INDEX's FIRST MET, the quest log's place, the
  attendant's dreams and the companion export. *The C symbol `sMapsecName_SAFARI_ZONE` is generated from the
  name, so it becomes `sMapsecName_THE_WALLED_GARDEN`, and **`src/region_map.c` line 667 names
  `sMapsecName_SAFARI_ZONE` by hand** (the dungeon table's SAFARI row): rename it in the same commit, or the build
  fails on an undeclared symbol (engine.md trap 11).*
- **The name card (T-445)**: the window prints the mapsec name over the picture, so the words follow the mapsec.
  **The picture is a park**, drawn 2026-11-05; redrawing it with a wall belongs with the SAFARI buildings, which
  `tools/gbahomes.py` already holds "for the SAFARI redesign (the user, 2026-11-10)".
- **The GUESTBOX** (`src/data/items.json`, source `tools/port_item_text.py`): *"A temporary host, issued at the gate
  and expiring at the gate. Its rights are minimal."* already says the session. **Unchanged.**
- **The TOKEN** (items.json): *"The WARDEN's key. Without it, nothing he says can be read."* **Unchanged.**
- **The attendant's dreams** (`docs/attendant_dreams.json`, built by `tools/gbadreams.py`), DRAFT A / B:
  - title `BEHIND THE GATE` -> A `BEHIND THE WALL` (90px, same as today) / B unchanged;
  - first: *"I dreamt of a wild park behind a / gate, and a little house deep in it."* -> A *"I dreamt of a garden
    behind a / wall, and a little house deep in it."* / B *"I dreamt of a garden where nothing / was allowed out,
    and a little house."*;
  - second: *"I dreamt of the SAFARI ZONE in / LURID CITY."* -> both *"I dreamt of THE WALLED GARDEN / in LURID
    CITY."* (the rest unchanged).
- **TILT's line** has three homes: the rest house's `text.inc`, `data/text/fame_checker.inc` (with its origin place
  `SAFARI ZONE` -> THE WALLED GARDEN, 84px small, 0 to spare) and its source in `tools/port_hearsay.py`. Change all
  three together, or the tool will put it back.
- **T-534's MUSAI line** (the north rest house, the user's pick A) never names the place: **it stays word for word**.
- **The INDEX's area names**: the area page draws markers, not names; the only name is FIRST MET (above).
- **`tools/generator_drift.json`** lists six of these `text.inc` files as carrying hand work after their tool last
  ran; the build should edit by hand and keep the drift note true.

**The companion (read only here; another session owns it).** Nothing in `companion/app` names the place by hand
(the one hit is a browser user-agent). Every SAFARI ZONE it shows comes from `tools/companion_export.py` reading
the mapsec name, so after the engine change a re-export carries it: `server/data/maps.json` (9 maps' `place`),
`planner_story.json` (the `safari_zone` step's label and place), `planner_wild.json` (four areas' `place`),
`planner_curve.json` (`"next": "SAFARI ZONE"`), `profile_layout.json` (mapsec 136), and the dream log's HER DREAMS
from `attendant_dreams.json`. **What the companion session needs to do**: re-run the export, check
`companion_export.py --check` is clean, and look at any place where a name of 17 characters meets a fixed width in the
app. `items.json`'s GUESTBOX and TOKEN are unchanged.

**Outside the game.** `engineAi/server/progress_steps.json` labels the step `"Safari Zone"` (the AI playtester's
list, which the attendant's dreams key on by id): rename the label, never the id. `docs/holidays.json` names the
maps by their `MAP_SAFARI_ZONE_*` constants, which do not change. The map folders, labels and constants
(`SafariZone_*`, `FLAG_*SAFARI*`, `BATTLE_TYPE_SAFARI`) are code, not words, and stay.

## The bible paragraph (a proposal for vision.md, not written there)

> ### THE WALLED GARDEN (T-540, the user, 2026-11-10)
>
> **The SAFARI ZONE is a platform.** Behind LURID's gate is a curated, walled sandbox where daemons that carry no
> signature are allowed to run, and the wall is there so that nothing leaves it unvetted: a daemon goes out only on
> a GUESTBOX, the platform's own host, issued at the gate and expiring there (1.3's one dim pip). **The player is a
> guest**, on a session metered by the step, and leaves their own daemons at the gate, because what comes in from
> outside is unvetted too. Its four zones are four **RINGS** of permission, the deeper the more privileged. **The
> WARDEN keeps it**; his staff call him LATENCY because every review waits on him, and while his TOKEN is lost
> nothing he says verifies -- though the office goes on obeying it. **At the deepest ring the SECRET HOUSE gives
> away the one thing in the garden that works outside it**: DRIVER03, TRAVERSE, which crosses the water the wall
> never reached.
>
> *What the user asked for was a quarantine that is not about illness, and a sandbox is exactly that: the isolation
> of untrusted code.* **Craft rule 3 binds it**: no line names an illness, and vanilla's *"speech problem"* became
> words that do not verify. **Craft rule 1 binds it harder**: nobody says what a walled garden is for or what it
> costs. The visitors love it. It is safe. Nothing in it surprises anybody. **SAFARI ZONE survives only as an old
> name, remembered.**

## The lines

Each entry gives vanilla (pret), today (engineGba `b1280ca99`), DRAFT A and DRAFT B, the widest line of each, and a
one-line story note. *(unchanged)* means the draft keeps today's words.

### THE GATE -- the attendant (FuchsiaCity_SafariZone_Entrance)

**`FuchsiaCity_SafariZone_Entrance_Text_WelcomeToSafariZone`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  
*She is cheerful and certain; the wall is the best thing about the place. Comedy carries it (craft rule 6).*

| | text | widest |
|---|---|---|
| vanilla | `Welcome to the SAFARI ZONE!` | 159px |
| today | `Welcome to the SAFARI ZONE!` | 159px |
| DRAFT A | `Welcome to THE WALLED GARDEN!` | 172px |
| DRAFT B | `Welcome to THE WALLED GARDEN!\nPlease sign in as a guest.` | 172px |

**`FuchsiaCity_SafariZone_Entrance_Text_PlaySafariGameFor500`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  
*B says the rule of the wall in her own words: a daemon leaves only on a host the platform issued.*

| | text | widest |
|---|---|---|
| vanilla | `For just ¥500, you can play the\nSAFARI GAME.\pYou can roam the wide-open safari\nand catch what you like.\pWould you like to play?` | 187px |
| today | `For just ¥500, you can bind all\nthe DAEMON you want in the park!\pWould you like to join the hunt?` | 183px |
| DRAFT A | `For just ¥500, you get a guest\nsession in the GARDEN.\pBind whatever runs in there!\nWould you like to sign in?` | 175px |
| DRAFT B | `Nothing in the GARDEN may leave\nunless it leaves on one of ours.\p¥500 for a guest session.\nWould you like to sign in?` | 177px |

**`FuchsiaCity_SafariZone_Entrance_Text_ThatllBe500WeOnlyUseSpecialBalls`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  
*The GUESTBOX is the platform's own host: one dim pip (1.3), restricted and expiring.*

| | text | widest |
|---|---|---|
| vanilla | `That'll be ¥500, please!\pWe only use a special kind of \nPOKé BALLS here.` | 168px |
| today | `That'll be ¥500 please!\pWe only use a special GUESTBOX\nhere.` | 173px |
| DRAFT A | `That'll be ¥500, please!\pOnly our own GUESTBOXES run\npast the wall.` | 156px |
| DRAFT B | `That'll be ¥500, please!\pIn here, only a GUESTBOX is\ntrusted. We issue those.` | 154px |

**`FuchsiaCity_SafariZone_Entrance_Text_CallYouOnPAWhenYouRunOut`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  
*The metered session, said once at the gate.*

| | text | widest |
|---|---|---|
| vanilla | `We'll call you on the PA when you\nrun out of time or SAFARI BALLS.\pWell, I'll wish you the best of\nluck!` | 188px |
| today | `We'll call you on the PA when you\nrun out of time or GUESTBOXes!` | 188px |
| DRAFT A | `Your session ends when your steps\nor your GUESTBOXES run out.\pWe'll tell you on the PA!` | 184px |
| DRAFT B | `We'll call you on the PA when\nyour session expires!` | 164px |

**`FuchsiaCity_SafariZone_Entrance_Text_GoingToLeaveSafariZoneEarly`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Are you going to leave the\nSAFARI ZONE early?` | 149px |
| today | `Are you going to leave the\nSAFARI ZONE early?` | 149px |
| DRAFT A | `Are you signing out of\nTHE WALLED GARDEN early?` | 142px |
| DRAFT B | `Leaving before your session\nexpires?` | 150px |

**`FuchsiaCity_SafariZone_Entrance_Text_PleaseReturnSafariBalls`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Please return any SAFARI BALLS\nyou may have left.` | 173px |
| today | `Please return any GUESTBOXes you\nhave left.` | 184px |
| DRAFT A | `Please return any GUESTBOXES you\nhave left. They expire here.` | 185px |
| DRAFT B | `Any GUESTBOXES you have left\nexpire at the gate. Hand them in!` | 186px |

**`FuchsiaCity_SafariZone_Entrance_Text_GoodLuck`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Good luck!` | 58px |
| today | `Good luck!` | 58px |
| DRAFT A | `Enjoy your session!` | 106px |
| DRAFT B | `Enjoy your session!` | 106px |

**`FuchsiaCity_SafariZone_Entrance_Text_CatchFairShareComeAgain`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Did you catch your fair share?\nCome again!` | 170px |
| today | `Did you bind your fair share? Come\nagain!` | 192px |
| DRAFT A | `Signed out. Did you bind your\nfair share? Come again!` | 163px |
| DRAFT B | `Your session is closed.\nCome again!` | 125px |

**`FuchsiaCity_SafariZone_Entrance_Text_FirstTimeAtSafariZone`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Hi! Is it your first time here at\nthe SAFARI ZONE?` | 180px |
| today | `Hi! Is it your first time here at\nthe SAFARI ZONE?` | 180px |
| DRAFT A | `Hi! Is it your first time in\nTHE WALLED GARDEN?` | 149px |
| DRAFT B | `Hi! Is this your first session\nin THE WALLED GARDEN?` | 160px |

**`FuchsiaCity_SafariZone_Entrance_Text_ExplainSafariZone`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  
*Four zones become four RINGS of permission. B gives the whole rule of the place in her voice and never says why it should worry anyone.*

| | text | widest |
|---|---|---|
| vanilla | `The SAFARI ZONE actually has\nfour zones in it.\pEach zone has different kinds of\nPOKéMON, even some rare ones.\pUse the supplied SAFARI BALLS to\ncatch them.\pYou can also throw BAIT or ROCKS\nbesides the SAFARI BALLS.\pIf you throw BAIT, the POKéMON\nbecomes less likely to flee, but\lharder to catch.\pIf you throw ROCKS, the POKéMON\nbecomes more likely to flee, but\leasier to catch.\pWhen you run out of time or SAFARI\nBALLS, it's game over for you!` | 195px |
| today | `SAFARI ZONE has 4 zones in it.\pEach zone has different kinds of\nDAEMONS. Use GUESTBOXes to bind\lthem!\pWhen you run out of time or\nGUESTBOXes, it's game over for you!\pBefore you go, open an unused\nDAEMON BOX so there's room for new\lDAEMON!` | 198px |
| DRAFT A | `The GARDEN has four RINGS.\pEach RING runs different kinds of\nDAEMONS. Use GUESTBOXES to bind\lthem!\pWhen your steps or GUESTBOXES\nrun out, your session expires!\pBefore you go, open an unused\nDAEMON BOX so there's room for new\lDAEMON!` | 193px |
| DRAFT B | `Nothing in here has been signed,\nso nothing in here gets out.\pUnless it runs on a GUESTBOX.\nThose are ours, and they're vetted.\pFour RINGS. The deeper you go,\nthe more you're allowed.\pBefore you go, open an unused\nDAEMON BOX so there's room for new\lDAEMON!` | 196px |

**`FuchsiaCity_SafariZone_Entrance_Text_PlayerReceived30SafariBalls`** (`data/maps/FuchsiaCity_SafariZone_Entrance/text.inc`)  
*Unchanged: it already says GUESTBOXES.*

| | text | widest |
|---|---|---|
| vanilla | `{PLAYER} received 30 SAFARI BALLS\nfrom the attendant.` | 189px |
| today | `{PLAYER} received 30 GUESTBOXES\nfrom the attendant.` | 177px |
| DRAFT A | `{PLAYER} received 30 GUESTBOXES\nfrom the attendant.` *(unchanged)* | 177px |
| DRAFT B | `{PLAYER} received 30 GUESTBOXES\nfrom the attendant.` *(unchanged)* | 177px |


### THE OFFICE -- the staff (FuchsiaCity_SafariZone_Office)

**`FuchsiaCity_SafariZone_Office_Text_NicknamedWardenSlowpoke`** (`data/maps/FuchsiaCity_SafariZone_Office/text.inc`)  
*The nickname stops being about a vacant look and becomes about his job: every review waits on him.*

| | text | widest |
|---|---|---|
| vanilla | `We nicknamed the WARDEN\n“SLOWPOKE.”\pYou know, he has that vacant look\nlike a SLOWPOKE.` | 188px |
| today | `We nicknamed the WARDEN\n“LATENCY.”\pYou know, he has that vacant look\nlike a LATENCY.` | 188px |
| DRAFT A | `We nicknamed the WARDEN\n“LATENCY.”\pAsk him anything. The answer\ncomes back. Eventually.` | 155px |
| DRAFT B | `We nicknamed the WARDEN\n“LATENCY.”\pEvery request goes through him.\nHe gets to all of them. Slowly.` | 176px |

**`FuchsiaCity_SafariZone_Office_Text_WardenIsVeryKnowledgeable`** (`data/maps/FuchsiaCity_SafariZone_Office/text.inc`)  
*A: the joke is the whole critique, and nobody makes it. B keeps vanilla's fossils as retired daemons.*

| | text | widest |
|---|---|---|
| vanilla | `WARDEN SLOWPOKE is very\nknowledgeable about POKéMON.\pHe even has some fossils of rare,\nextinct POKéMON.` | 184px |
| today | `WARDEN LATENCY is very\nknowledgeable about DAEMON.\pHe even has some fossils of rare,\nextinct DAEMON.` | 184px |
| DRAFT A | `WARDEN LATENCY reviews every\nDAEMON that runs in the GARDEN.\pHe's never let a bad one out.\nHe's never let many out at all.` | 176px |
| DRAFT B | `WARDEN LATENCY knows every\nDAEMON that runs in here.\pHe keeps the ones nothing runs\nanymore, too. At his house.` | 167px |

**`FuchsiaCity_SafariZone_Office_Text_CouldntUnderstandWarden`** (`data/maps/FuchsiaCity_SafariZone_Office/text.inc`)  
*Replaces 'a speech problem' (a pathology, craft rule 3): his words are unsigned, not broken. B: the staff obey orders nobody can verify.*

| | text | widest |
|---|---|---|
| vanilla | `WARDEN SLOWPOKE came in, but\nI couldn't understand him.\pI think he's got a speech problem!` | 191px |
| today | `WARDEN LATENCY came in, but I\ncouldn't understand him.\pI think he's got a speech problem!` | 191px |
| DRAFT A | `WARDEN LATENCY came in, but\nnothing he said would verify.\pWithout his TOKEN, it all\narrives as noise.` | 160px |
| DRAFT B | `WARDEN LATENCY came in, but I\ncouldn't read a word of it.\pHe hasn't signed in for days.\nWe still do what he says, though.` | 186px |

**`FuchsiaCity_SafariZone_Office_Text_PrizeInSafariZone`** (`data/maps/FuchsiaCity_SafariZone_Office/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `WARDEN SLOWPOKE is running a\npromotion campaign right now.\pTry to get to the farthest corner\nof the SAFARI ZONE.\pIf you can make it, you'll win a\nvery convenient prize.` | 185px |
| today | `WARDEN LATENCY is running a\npromotion campaign right now.\pTry to get to the farthest corner\nof the SAFARI ZONE.\pIf you can make it, you'll win a\nvery convenient prize.` | 185px |
| DRAFT A | `WARDEN LATENCY is running a\npromotion campaign right now.\pTry to get to the farthest corner\nof the GARDEN.\pIf you can make it, you'll win a\nvery convenient prize.` | 185px |
| DRAFT B | `WARDEN LATENCY is running a\npromotion campaign right now.\pTry to reach the innermost RING.\pNo guest has, yet. The prize is\nvery convenient.` | 180px |


### THE REST HOUSES

**`SafariZone_Center_Text_WhereDidErikGo`** (`data/maps/SafariZone_Center_RestHouse/text.inc`)  
*SARA is inside the wall and ERIK is outside it, in LURID CITY, each waiting on the other. Nothing between them is delivered until it is reviewed.*

| | text | widest |
|---|---|---|
| vanilla | `SARA: Where did my boyfriend,\nERIK, go?` | 164px |
| today | `SARA: Where did my boyfriend,\nERIK, go?` | 164px |
| DRAFT A | `SARA: ERIK said he'd meet me\nhere. Did he sign in?` | 160px |
| DRAFT B | `SARA: My messages to ERIK\nall say PENDING.` | 145px |

**`SafariZone_Center_Text_CatchingMonsAsGifts`** (`data/maps/SafariZone_Center_RestHouse/text.inc`)  
*A visitor who loves the place, for exactly the reason the player may come to doubt.*

| | text | widest |
|---|---|---|
| vanilla | `I'm catching POKéMON to take home\nas gifts.` | 188px |
| today | `I'm binding DAEMON to take home as\ngifts!` | 191px |
| DRAFT A | `I'm binding DAEMONS to take home\nas gifts. They're all vetted!` | 180px |
| DRAFT B | `Gifts from the GARDEN are the\nsafest kind. Nothing in them\lsurprises anybody.` | 164px |

**`SafariZone_East_Text_HowManyDidYouCatch`** (`data/maps/SafariZone_East_RestHouse/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `How many did you catch?\nI'm bushed from the effort!` | 151px |
| today | `How many did you bind? I'm bushed\nfrom the work!` | 188px |
| DRAFT A | `How many did you bind? I'm bushed\nfrom the work!` *(unchanged)* | 188px |
| DRAFT B | `How many did you bind? I've\nwalked my whole session!` | 153px |

**`SafariZone_East_Text_CaughtChanseyAllWorthwhile`** (`data/maps/SafariZone_East_RestHouse/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `I caught a CHANSEY!\pThat makes this all worthwhile.` | 171px |
| today | `I bound an UPTIME!\pThat makes this all worthwhile!` | 172px |
| DRAFT A | `I bound an UPTIME!\pThat makes this all worthwhile!` *(unchanged)* | 172px |
| DRAFT B | `I bound an UPTIME!\pIt's been approved and everything!` | 191px |

**`SafariZone_East_Text_TiredFromAllTheFun`** (`data/maps/SafariZone_East_RestHouse/text.inc`)  
*Unchanged.*

| | text | widest |
|---|---|---|
| vanilla | `Whew!\nI'm tired from all the fun!` | 148px |
| today | `Whew!\nI'm tired from all the fun!` | 148px |
| DRAFT A | `Whew!\nI'm tired from all the fun!` *(unchanged)* | 148px |
| DRAFT B | `Whew!\nI'm tired from all the fun!` *(unchanged)* | 148px |

**`SafariZone_East_Text_KeepAnyItemFoundOnSafari`** (`data/maps/SafariZone_North_RestHouse/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `You can keep any item you find in\nthe SAFARI ZONE.\pBut, you'll run out of time if you\ntry for all of them at once.` | 187px |
| today | `You can keep any item you find in\nthe SAFARI ZONE.\pBut, you'll run out of time if you\ntry for all of them at once.` | 187px |
| DRAFT A | `You can keep any item you find in\nthe GARDEN. It's all been checked.\pBut your session will expire if\nyou try for all of them at once.` | 192px |
| DRAFT B | `Items found in here are vetted\nalready. Keep them!\pBut your session will expire if\nyou try for all of them at once.` | 181px |

**`SafariZone_East_Text_PrizeInDeepestPartOfSafariZone`** (`data/maps/SafariZone_North_RestHouse/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Go to the deepest part of the\nSAFARI ZONE. You will win a prize!` | 193px |
| today | `Go to the deepest part of the\nSAFARI ZONE. You will win a prize!` | 193px |
| DRAFT A | `Go to the deepest RING of the\nGARDEN. You will win a prize!` | 168px |
| DRAFT B | `The deepest RING has a house in\nit. Nobody I know has been in.` | 179px |

**`SafariZone_East_Text_MyEeveeEvolvedIntoFlareon`** (`data/maps/SafariZone_North_RestHouse/text.inc`)  
*T-534's MUSAI line, the user's pick (A). It never names the place, so it stays word for word in both.*

| | text | widest |
|---|---|---|
| vanilla | `My EEVEE evolved into FLAREON.\pBut, a friend's EEVEE turned into a\nVAPOREON. I wonder why?` | 192px |
| today | `My MUSAI became a CODEMUSAI.\pMy friend's became a CAREMUSAI.\nMine reasons. Theirs just knows.\pSide by side, they argue,\nand then they agree.` | 176px |
| DRAFT A | `My MUSAI became a CODEMUSAI.\pMy friend's became a CAREMUSAI.\nMine reasons. Theirs just knows.\pSide by side, they argue,\nand then they agree.` *(unchanged)* | 176px |
| DRAFT B | `My MUSAI became a CODEMUSAI.\pMy friend's became a CAREMUSAI.\nMine reasons. Theirs just knows.\pSide by side, they argue,\nand then they agree.` *(unchanged)* | 176px |

**`SafariZone_West_Text_KogaPatrolsSafariEverySoOften`** (`data/maps/SafariZone_West_RestHouse/text.inc`)  
*Its source is tools/port_hearsay.py, and the FAME CHECKER carries the same words (data/text/fame_checker.inc): change all three together.*

| | text | widest |
|---|---|---|
| vanilla | `The SAFARI ZONE's huge, wouldn't\nyou say?\pFUCHSIA's GYM LEADER, KOGA, \npatrols the grounds every so often.\pThanks to him, we can play here\nknowing that we're safe.` | 196px |
| today | `TILT walks the SAFARI ZONE every\nso often.\pThings go wrong less after he has\nbeen. Nobody's seen him fix a\lthing.` | 187px |
| DRAFT A | `TILT walks THE WALLED GARDEN\nevery so often.\pThings go wrong less after he has\nbeen. Nobody's seen him fix a\lthing.` | 185px |
| DRAFT B | `TILT walks the GARDEN every so\noften.\pThings go wrong less after he has\nbeen. Nobody's seen him fix a\lthing.` | 185px |

**`SafariZone_West_Text_RocksMakeMonRunButEasierCatch`** (`data/maps/SafariZone_West_RestHouse/text.inc`)  
*Unchanged.*

| | text | widest |
|---|---|---|
| vanilla | `Tossing ROCKS at POKéMON might\nmake them run, but they'll be\leasier to catch.` | 171px |
| today | `Tossing ROCKs at DAEMON might make\nthem run, but they'll be easier to\lbind.` | 193px |
| DRAFT A | `Tossing ROCKs at DAEMON might make\nthem run, but they'll be easier to\lbind.` *(unchanged)* | 193px |
| DRAFT B | `Tossing ROCKs at DAEMON might make\nthem run, but they'll be easier to\lbind.` *(unchanged)* | 193px |

**`SafariZone_West_Text_BaitMakesMonStickAround`** (`data/maps/SafariZone_West_RestHouse/text.inc`)  
*Unchanged.*

| | text | widest |
|---|---|---|
| vanilla | `Using BAIT will make POKéMON more\nlikely to stick around if they get\lbusy eating.` | 188px |
| today | `Using BAIT will make DAEMON more\nlikely to stick around if they get\lbusy eating.` | 186px |
| DRAFT A | `Using BAIT will make DAEMON more\nlikely to stick around if they get\lbusy eating.` *(unchanged)* | 186px |
| DRAFT B | `Using BAIT will make DAEMON more\nlikely to stick around if they get\lbusy eating.` *(unchanged)* | 186px |

**`SafariZone_West_Text_HikedLotsDidntSeeMonIWanted`** (`data/maps/SafariZone_West_RestHouse/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `I hiked a lot, but I didn't see any\nPOKéMON I wanted.` | 194px |
| today | `I hiked a lot, but I didn't see any\nDAEMON I wanted.` | 194px |
| DRAFT A | `I hiked a lot, but I didn't see any\nDAEMON I wanted.` *(unchanged)* | 194px |
| DRAFT B | `I hiked a lot, but the DAEMON I\nwanted doesn't run in here.` | 178px |


### THE SECRET HOUSE -- its attendant (SafariZone_SecretHouse)

**`SafariZone_SecretHouse_Text_CongratsYouveWon`** (`data/maps/SafariZone_SecretHouse/text.inc`)  
*She has waited at the deepest ring for anyone to arrive. She is not unhappy; she is relieved.*

| | text | widest |
|---|---|---|
| vanilla | `Ah! Finally!\pYou're the first person to reach\nthe SECRET HOUSE!\pAlthough I made a campaign\nfor our grand opening,\pI was getting worried that no one\nwould win our campaign prize.\pCongratulations!\nYou have won!` | 184px |
| today | `Ah! Finally!\pYou're the first person to reach\nthe SECRET HOUSE!\pAlthough I made a campaign\nfor our grand opening,\pI was getting worried that no one\nwould win our campaign prize.\pCongratulations!\nYou have won!` | 184px |
| DRAFT A | `Ah! Finally!\pYou're the first guest to reach\nthe SECRET HOUSE!\pAlthough I made a campaign\nfor our grand opening,\pI was getting worried that no one\nwould win our campaign prize.\pCongratulations!\nYou have won!` | 184px |
| DRAFT B | `Ah! Finally!\pYou're the first guest to get\nthis far in.\pThe prize is the one thing in\nthe GARDEN nobody reviews.\pCongratulations!\nYou have won!` | 159px |

**`SafariZone_SecretHouse_Text_ExplainSurf`** (`data/maps/SafariZone_SecretHouse/text.inc`)  
*The prize at the bottom of the wall is the way over it. Neither line says so.*

| | text | widest |
|---|---|---|
| vanilla | `HM03 is SURF.\pPOKéMON will be able to ferry you\nacross water using it.\pAnd, this HM isn't disposable, so\nyou can use it over and over.\pYou're super lucky for winning this\nfabulous prize!` | 189px |
| today | `DRIVER03 is TRAVERSE.\pDAEMON will be able to ferry you\nacross water using it.\pAnd, this DRIVER isn't disposable,\nso you can use it over and over.\pYou're super lucky for winning this\nfabulous prize!` | 189px |
| DRAFT A | `DRIVER03 is TRAVERSE.\pDAEMON will be able to ferry you\nacross water using it.\pAnd, this DRIVER isn't disposable,\nso you can use it over and over.\pThe wall doesn't reach the water.\nNobody ever thought it had to.` | 185px |
| DRAFT B | `DRIVER03 is TRAVERSE.\pDAEMON will be able to ferry you\nacross water using it.\pAnd, this DRIVER isn't disposable,\nso you can use it over and over.\pIt works outside the GARDEN, too.\nMost things in here don't.` | 186px |

**`SafariZone_SecretHouse_Text_ReceivedHM03FromAttendant`** (`data/maps/SafariZone_SecretHouse/text.inc`)  
*Unchanged.*

| | text | widest |
|---|---|---|
| vanilla | `{PLAYER} received HM03\nfrom the attendant!` | 123px |
| today | `{PLAYER} received DRIVER03 from\nthe attendant!` | 175px |
| DRAFT A | `{PLAYER} received DRIVER03 from\nthe attendant!` *(unchanged)* | 175px |
| DRAFT B | `{PLAYER} received DRIVER03 from\nthe attendant!` *(unchanged)* | 175px |

**`SafariZone_SecretHouse_Text_DontHaveRoomForPrize`** (`data/maps/SafariZone_SecretHouse/text.inc`)  
*Unchanged.*

| | text | widest |
|---|---|---|
| vanilla | `You don't have room for this\nfabulous prize!` | 156px |
| today | `You don't have room for this\nfabulous prize!` | 156px |
| DRAFT A | `You don't have room for this\nfabulous prize!` *(unchanged)* | 156px |
| DRAFT B | `You don't have room for this\nfabulous prize!` *(unchanged)* | 156px |


### THE WARDEN, nicknamed LATENCY, and his house (FuchsiaCity_WardensHouse)

**`FuchsiaCity_WardensHouse_Text_HifFuffHefifoo`** (`data/maps/FuchsiaCity_WardensHouse/text.inc`)  
*Without his TOKEN nothing he says verifies. A keeps vanilla's garble as the comedy; B stamps it, so the player reads why.*

| | text | widest |
|---|---|---|
| vanilla | `WARDEN: Hif fuff hefifoo!\pHa lof ha feef ee hafahi ho.\nHeff hee fwee!` | 160px |
| today | `WARDEN: Hif fuff hefifoo!\pHa lof ha feef ee hafahi ho.\nHeff hee fwee!` | 160px |
| DRAFT A | `WARDEN: Hif fuff hefifoo!\pHa lof ha feef ee hafahi ho.\nHeff hee fwee!` *(unchanged)* | 160px |
| DRAFT B | `UNSIGNED: Hif fuff hefifoo!\pHa lof ha feef ee hafahi ho.\nHeff hee fwee!` | 160px |

**`FuchsiaCity_WardensHouse_Text_AhHowheeHoHoo`** (`data/maps/FuchsiaCity_WardensHouse/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Ah howhee ho hoo!\nEef ee hafahi ho!` | 102px |
| today | `Ah howhee ho hoo!\nEef ee hafahi ho!` | 102px |
| DRAFT A | `Ah howhee ho hoo!\nEef ee hafahi ho!` *(unchanged)* | 102px |
| DRAFT B | `UNSIGNED: Ah howhee ho hoo!\nEef ee hafahi ho!` | 161px |

**`FuchsiaCity_WardensHouse_Text_HeOhayHeHaHoo`** (`data/maps/FuchsiaCity_WardensHouse/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Ha?\nHe ohay heh ha hoo ee haheh!` | 168px |
| today | `Ha?\nHe ohay heh ha hoo ee haheh!` | 168px |
| DRAFT A | `Ha?\nHe ohay heh ha hoo ee haheh!` *(unchanged)* | 168px |
| DRAFT B | `UNSIGNED: Ha?\nHe ohay heh ha hoo ee haheh!` | 168px |

**`FuchsiaCity_WardensHouse_Text_WardenPoppedInHisTeeth`** (`data/maps/FuchsiaCity_WardensHouse/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `The WARDEN popped in his teeth!` | 178px |
| today | `The WARDEN signed in with it!` | 161px |
| DRAFT A | `The WARDEN signed in with it!` *(unchanged)* | 161px |
| DRAFT B | `The WARDEN signed in.\nHis words verify again!` | 126px |

**`FuchsiaCity_WardensHouse_Text_ThanksSonGiveYouSomething`** (`data/maps/FuchsiaCity_WardensHouse/text.inc`)  
*The son and lassie labels already carry one text (T-260); the same change goes into both.*

| | text | widest |
|---|---|---|
| vanilla | `WARDEN: Thanks, son!\nYou're a real lifesaver!\pNo one could understand a word\nthat I said, not a one!\pI was too ashamed to show my face\naround the OFFICE, even.\pLet me give you something for your\ntrouble.` | 193px |
| today | `WARDEN: Thanks, friend!\nYou're a real lifesaver!\pNo one could understand a word\nthat I said, not a one!\pI was too ashamed to show my face\naround the OFFICE, even.\pLet me give you something for your\ntrouble.` | 193px |
| DRAFT A | `WARDEN: Thanks, friend!\nYou're a real lifesaver!\pNothing I sent would verify.\nNot a word, not a one!\pI was too ashamed to show my face\naround the OFFICE, even.\pLet me give you something for your\ntrouble.` | 193px |
| DRAFT B | `WARDEN: Thanks, friend!\nYou're a real lifesaver!\pNothing I sent would verify.\nThe OFFICE obeyed it anyway.\pThat's worse, if you think\nabout it. Nobody does.\pLet me give you something for your\ntrouble.` | 193px |

**`FuchsiaCity_WardensHouse_Text_ThanksLassieGiveYouSomething`** (`data/maps/FuchsiaCity_WardensHouse/text.inc`)  
*Same words as the line above.*

| | text | widest |
|---|---|---|
| vanilla | `WARDEN: Thank you, lassie!\nYou're a real lifesaver!\pNo one could understand a word\nthat I said, not a one!\pI was too ashamed to show my face\naround the OFFICE, even.\pLet me give you something for your\ntrouble.` | 193px |
| today | `WARDEN: Thanks, friend!\nYou're a real lifesaver!\pNo one could understand a word\nthat I said, not a one!\pI was too ashamed to show my face\naround the OFFICE, even.\pLet me give you something for your\ntrouble.` | 193px |
| DRAFT A | `WARDEN: Thanks, friend!\nYou're a real lifesaver!\pNothing I sent would verify.\nNot a word, not a one!\pI was too ashamed to show my face\naround the OFFICE, even.\pLet me give you something for your\ntrouble.` | 193px |
| DRAFT B | `WARDEN: Thanks, friend!\nYou're a real lifesaver!\pNothing I sent would verify.\nThe OFFICE obeyed it anyway.\pThat's worse, if you think\nabout it. Nobody does.\pLet me give you something for your\ntrouble.` | 193px |

**`FuchsiaCity_WardensHouse_Text_ExplainStrength`** (`data/maps/FuchsiaCity_WardensHouse/text.inc`)  
*B: the keeper of the wall hid its door at the far end on purpose. The one line where he lets it slip.*

| | text | widest |
|---|---|---|
| vanilla | `WARDEN: Inside HM04 you'll find\nSTRENGTH.\pIt lets POKéMON move boulders when\nyou're outside of battle.\pOh yes, did you find the SECRET\nHOUSE in the SAFARI ZONE?` | 196px |
| today | `WARDEN: Inside DRIVER04 you'll find\nDISPLACE.\pIt lets DAEMON move boulders when\nyou're outside of battle.\pOh yes, did you find the SECRET\nHOUSE in the SAFARI ZONE?` | 196px |
| DRAFT A | `WARDEN: Inside DRIVER04 you'll find\nDISPLACE.\pIt lets DAEMON move boulders when\nyou're outside of battle.\pOh yes, did you find the SECRET\nHOUSE in the GARDEN?` | 196px |
| DRAFT B | `WARDEN: Inside DRIVER04 you'll find\nDISPLACE.\pIt lets DAEMON move boulders when\nyou're outside of battle.\pOh yes, the SECRET HOUSE. I put\nthe way across in there myself.\pA wall wants a door somewhere.` | 196px |

**`FuchsiaCity_WardensHouse_Text_MonPhotosFossilsOnDisplay`** (`data/maps/FuchsiaCity_WardensHouse/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `POKéMON photos and fossils are on\ndisplay.` | 186px |
| today | `DAEMON photos and fossils are on\ndisplay.` | 180px |
| DRAFT A | `DAEMON photos and fossils are on\ndisplay.` *(unchanged)* | 180px |
| DRAFT B | `Photos of DAEMONS the GARDEN\nretired are on display.` | 164px |

**`FuchsiaCity_WardensHouse_Text_OldMonMerchandiseOnDisplay`** (`data/maps/FuchsiaCity_WardensHouse/text.inc`)  
*A: THE OLD NAME, remembered by the shelf. B keeps it for the neighbour (below).*

| | text | widest |
|---|---|---|
| vanilla | `Old POKéMON merchandise is on\ndisplay.` | 164px |
| today | `Old DAEMON merchandise is on\ndisplay.` | 158px |
| DRAFT A | `Old merchandise is on display.\nMost of it still says SAFARI ZONE.` | 189px |
| DRAFT B | `Old merchandise is on display.\nMost of it still says SAFARI ZONE.` | 189px |

**`FuchsiaCity_House1_Text_WardenIsOldHasFalseTeeth`** (`data/maps/FuchsiaCity_House1/text.inc`)  
*HOLT's grandfather. B: THE OLD NAME, remembered by the one man old enough to.*

| | text | widest |
|---|---|---|
| vanilla | `The SAFARI ZONE's WARDEN is old, \nbut he's still very much active.\pAll his teeth are false, though.` | 189px |
| today | `The SAFARI ZONE's WARDEN is old, \nbut he's still very much active.\pHe keeps losing his TOKEN, though.` | 191px |
| DRAFT A | `The GARDEN's WARDEN is old,\nbut he's still very much active.\pHe keeps losing his TOKEN, though.` | 191px |
| DRAFT B | `The WARDEN has kept that place\nsince it was the SAFARI ZONE.\pHe keeps losing his TOKEN, though.` | 191px |


### LURID CITY -- the street, the signs, and the people who talk about it

**`FuchsiaCity_Text_DidYouTrySafariGame`** (`data/maps/FuchsiaCity/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Did you try the SAFARI GAME?\pThere are some rare POKéMON that\ncan only be caught there.` | 185px |
| today | `Did you try the SAFARI GAME? Some\nDAEMONS can only be bound there.` | 193px |
| DRAFT A | `Did you sign in to the GARDEN?\nSome DAEMONS only run in there.` | 176px |
| DRAFT B | `Some DAEMONS run inside the wall\nand nowhere else. Did you go in?` | 181px |

**`FuchsiaCity_Text_SafariZoneZooInFront`** (`data/maps/FuchsiaCity/text.inc`)  
*Vanilla's zoo is the platform's shop window.*

| | text | widest |
|---|---|---|
| vanilla | `The SAFARI ZONE has a zoo in front\nof the entrance.\pOut back is the SAFARI GAME for\ncatching POKéMON.` | 196px |
| today | `SAFARI ZONE has a zoo in front of\nthe entrance.\pOut back is the SAFARI GAME for\nbinding DAEMON.` | 189px |
| DRAFT A | `The pens out front are the\nGARDEN's showcase.\pThe GARDEN itself is behind the\nwall. Guests only.` | 173px |
| DRAFT B | `The pens out front are what\nthe GARDEN shows you.\pWhat it keeps is behind the\nwall.` | 153px |

**`FuchsiaCity_Text_WheresSara`** (`data/maps/FuchsiaCity/text.inc`)  
*The other half of SARA's line: outside the wall.*

| | text | widest |
|---|---|---|
| vanilla | `ERIK: Where's SARA?\nI said I'd meet her here.` | 140px |
| today | `ERIK: Where's SARA?\nI said I'd meet her here.` | 140px |
| DRAFT A | `ERIK: SARA's in there. I sent\nher a message an hour ago.` | 160px |
| DRAFT B | `ERIK: SARA said to meet her\nhere. She's not answering.` | 155px |

**`FuchsiaCity_Text_SafariZoneSign`** (`data/maps/FuchsiaCity/text.inc`)  
*T-324's sign, its name changed (A) or its promise (B).*

| | text | widest |
|---|---|---|
| vanilla | `POKéMON PARADISE\nSAFARI ZONE` | 96px |
| today | `SAFARI ZONE\nEverything In Here\lIs UNBOUND` | 101px |
| DRAFT A | `THE WALLED GARDEN\nEverything In Here\lIs UNBOUND` | 102px |
| DRAFT B | `THE WALLED GARDEN\nNothing Leaves\lUnchecked` | 102px |

**`FuchsiaCity_Text_SafariGameSign`** (`data/maps/FuchsiaCity/text.inc`)  
*Your own daemons are outside code too: they wait at the gate.*

| | text | widest |
|---|---|---|
| vanilla | `SAFARI GAME\nPOKéMON-U-CATCH!` | 96px |
| today | `SAFARI GAME\nGUESTBOXES only. Leave\lyour own daemons at the gate.` | 166px |
| DRAFT A | `GUEST ENTRY\nGUESTBOXES only. Leave\lyour own daemons at the gate.` | 166px |
| DRAFT B | `GUEST SESSIONS\nGUESTBOXES only. Leave\lyour own daemons at the gate.` | 166px |

**`FuchsiaCity_Text_WardensHomeSign`** (`data/maps/FuchsiaCity/text.inc`)  
*B is LATENCY's joke on his own door.*

| | text | widest |
|---|---|---|
| vanilla | `SAFARI ZONE\nWARDEN'S HOME` | 75px |
| today | `SAFARI ZONE\nWARDEN'S HOME` | 75px |
| DRAFT A | `THE WALLED GARDEN\nWARDEN'S HOME` | 102px |
| DRAFT B | `WARDEN'S HOME\nReplies May Take A While` | 136px |

**`FuchsiaCity_Text_SafariZoneOfficeSign`** (`data/maps/FuchsiaCity/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `POKéMON PARADISE!\nWelcome to the SAFARI ZONE!\lSAFARI ZONE OFFICE` | 159px |
| today | `DAEMON PARADISE! Welcome to the\nSAFARI ZONE! SAFARI ZONE OFFICE` | 186px |
| DRAFT A | `A SAFE PLACE TO RUN! Welcome to\nTHE WALLED GARDEN! GARDEN OFFICE` | 192px |
| DRAFT B | `EVERYTHING HERE IS REVIEWED!\nTHE WALLED GARDEN OFFICE` | 168px |

**`FuchsiaCity_PokemonCenter_1F_Text_VisitSafariZoneForPokedex`** (`data/maps/FuchsiaCity_PokemonCenter_1F/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `If you're working on a POKéDEX,\nvisit the SAFARI ZONE.\pAll sorts of rare POKéMON breed\nthere.` | 176px |
| today | `If you're working on an INDEX, visit\nthe SAFARI ZONE.\pAll sorts of rare DAEMONS breed\nthere.` | 197px |
| DRAFT A | `If you're working on an INDEX, visit\nTHE WALLED GARDEN.\pAll sorts of rare DAEMONS run\nthere, and only there.` | 197px |
| DRAFT B | `If you're working on an INDEX, visit\nthe GARDEN.\pIts DAEMONS are signed to run\nnowhere else.` | 197px |

**`FuchsiaCity_Mart_Text_DontTheyHaveSafariZonePennants`** (`data/maps/FuchsiaCity_Mart/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Don't they have any pennants\npromoting the SAFARI ZONE?\pHow about some paper lanterns?\nAren't there even any calendars?` | 178px |
| today | `Don't they have any pennants\npromoting the SAFARI ZONE?\pHow about some paper lanterns?\nAren't there even any calendars?` | 178px |
| DRAFT A | `Don't they have any pennants\npromoting THE WALLED GARDEN?\pHow about some paper lanterns?\nAren't there even any calendars?` | 178px |
| DRAFT B | `Don't they have any pennants\nfrom the GARDEN?\pThey don't let anything out of\nthere. Not even a calendar.` | 166px |

**`SSAnne_2F_Room5_Text_HaveYouGoneToSafariZone`** (`data/maps/SSAnne_2F_Room5/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Have you gone to the SAFARI ZONE\nin FUCHSIA CITY?\pThere are many kinds of rare\nPOKéMON.` | 189px |
| today | `Have you gone to the SAFARI ZONE\nin LURID CITY?\pIt had many rare kinds of\nDAEMONS!!` | 189px |
| DRAFT A | `Have you been to THE WALLED\nGARDEN in LURID CITY?\pIt had many rare kinds of\nDAEMONS!!` | 160px |
| DRAFT B | `Have you been to the GARDEN\nin LURID CITY?\pNothing in there can hurt you.\nIt's wonderful!!` | 167px |

**`SSAnne_2F_Room5_Text_WeThinkSafariZoneIsAwesome`** (`data/maps/SSAnne_2F_Room5/text.inc`)  
*B: THE OLD NAME again, from a father, corrected by his child.*

| | text | widest |
|---|---|---|
| vanilla | `Me and my daddy think the SAFARI\nZONE is awesome!\lI wish we could go there again.` | 185px |
| today | `Me and my daddy think the SAFARI\nZONE is awesome!\lI wish we could go there again.` | 185px |
| DRAFT A | `Me and my daddy think the GARDEN\nis awesome! Nothing bad gets in!\lI wish we could go there again.` | 185px |
| DRAFT B | `My daddy still calls it the SAFARI\nZONE. It's a GARDEN now.\lIt has a wall!` | 191px |


### THE SIGNS AND TIPS INSIDE -- four zones become four RINGS

**`SafariZone_Center_Text_RestHouse`** (`data/maps/SafariZone_Center/text.inc`)  
*B: the rest houses are the review queue. A keeps T-401's REST HOUSE.*

| | text | widest |
|---|---|---|
| vanilla | `REST HOUSE` | 60px |
| today | `REST HOUSE` | 60px |
| DRAFT A | `REST HOUSE` *(unchanged)* | 60px |
| DRAFT B | `WAITING ROOM` | 72px |

**`SafariZone_East_Text_RestHouse`** (`data/maps/SafariZone_East/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `REST HOUSE` | 60px |
| today | `REST HOUSE` | 60px |
| DRAFT A | `REST HOUSE` *(unchanged)* | 60px |
| DRAFT B | `WAITING ROOM` | 72px |

**`SafariZone_North_Text_RestHouse`** (`data/maps/SafariZone_North/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `REST HOUSE` | 60px |
| today | `REST HOUSE` | 60px |
| DRAFT A | `REST HOUSE` *(unchanged)* | 60px |
| DRAFT B | `WAITING ROOM` | 72px |

**`SafariZone_West_Text_RestHouse`** (`data/maps/SafariZone_West/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `REST HOUSE` | 60px |
| today | `REST HOUSE` | 60px |
| DRAFT A | `REST HOUSE` *(unchanged)* | 60px |
| DRAFT B | `WAITING ROOM` | 72px |

**`SafariZone_Center_Text_CenterArea`** (`data/maps/SafariZone_Center/text.inc`)  
*A counts down as a machine does (RING 3 at the gate, RING 0 where the way out is: the deeper, the more privileged). B counts up by depth (RING 1 to RING 4).*

| | text | widest |
|---|---|---|
| vanilla | `CENTER AREA` | 66px |
| today | `CENTER AREA` | 66px |
| DRAFT A | `RING 3` | 36px |
| DRAFT B | `RING 1` | 36px |

**`SafariZone_East_Text_AreaSign`** (`data/maps/SafariZone_East/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `AREA 1\nWEST: CENTER AREA` | 101px |
| today | `AREA 1\nWEST: CENTER AREA` | 101px |
| DRAFT A | `RING 2\nWEST: RING 3` | 71px |
| DRAFT B | `RING 2\nWEST: RING 1` | 71px |

**`SafariZone_North_Text_Area2`** (`data/maps/SafariZone_North/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `AREA 2` | 36px |
| today | `AREA 2` | 36px |
| DRAFT A | `RING 1` | 36px |
| DRAFT B | `RING 3` | 36px |

**`SafariZone_West_Text_AreaSign`** (`data/maps/SafariZone_West/text.inc`)  
*The SECRET HOUSE is here: RING 0 in A.*

| | text | widest |
|---|---|---|
| vanilla | `AREA 3\nEAST: CENTER AREA` | 101px |
| today | `AREA 3\nEAST: CENTER AREA` | 101px |
| DRAFT A | `RING 0\nEAST: RING 3` | 71px |
| DRAFT B | `RING 4\nEAST: RING 1` | 71px |

**`SafariZone_Center_Text_PressStartToCheckTime`** (`data/maps/SafariZone_Center/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `TRAINER TIPS\pPress START to check\nremaining time.` | 115px |
| today | `USER TIPS\pPress START to see how\nmuch time is left.` | 127px |
| DRAFT A | `USER TIPS\pPress START to see how\nmuch of your session is left.` | 159px |
| DRAFT B | `USER TIPS\pPress START to see how\nmuch of your session is left.` | 159px |

**`SafariZone_East_Text_TimeDeclinesOnlyWhileYouWalk`** (`data/maps/SafariZone_East/text.inc`)  
*A keeps it: the user named this line as the metered session already.*

| | text | widest |
|---|---|---|
| vanilla | `TRAINER TIPS\pThe remaining time declines only\nwhile you walk.` | 175px |
| today | `USER TIPS\pThe clock only runs while you\nwalk. Standing still is free.` | 164px |
| DRAFT A | `USER TIPS\pThe clock only runs while you\nwalk. Standing still is free.` *(unchanged)* | 164px |
| DRAFT B | `USER TIPS\pYour session is metered by the\nstep. Standing still is free.` | 167px |

**`SafariZone_North_Text_SecretHouseStillAhead`** (`data/maps/SafariZone_North/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `TRAINER TIPS\pThe SECRET HOUSE is still ahead.` | 182px |
| today | `USER TIPS\pThe SECRET HOUSE is further\nin. Keep going.` | 155px |
| DRAFT A | `USER TIPS\pThe SECRET HOUSE is further\nin. Keep going.` *(unchanged)* | 155px |
| DRAFT B | `USER TIPS\pThe SECRET HOUSE is one RING\nfurther in. Keep going.` | 164px |

**`SafariZone_North_Text_ZigzagThroughTallGrass`** (`data/maps/SafariZone_North/text.inc`)  
*Unchanged.*

| | text | widest |
|---|---|---|
| vanilla | `TRAINER TIPS\pPOKéMON hide in tall grass.\pZigzag through grassy areas to\nflush them out.` | 170px |
| today | `USER TIPS\pDaemons hide in tall grass.\pWalk it back and forth to\nflush them out.` | 148px |
| DRAFT A | `USER TIPS\pDaemons hide in tall grass.\pWalk it back and forth to\nflush them out.` *(unchanged)* | 148px |
| DRAFT B | `USER TIPS\pDaemons hide in tall grass.\pWalk it back and forth to\nflush them out.` *(unchanged)* | 148px |

**`SafariZone_North_Text_WinFreeHMFindSecretHouse`** (`data/maps/SafariZone_North/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `TRAINER TIPS\pWin a free HM for finding the\nSECRET HOUSE.` | 159px |
| today | `USER TIPS\pFind the SECRET HOUSE and a\nDRIVER is yours to keep.` | 157px |
| DRAFT A | `USER TIPS\pFind the SECRET HOUSE and a\nDRIVER is yours to keep.` *(unchanged)* | 157px |
| DRAFT B | `USER TIPS\pFind the SECRET HOUSE. Its\nDRIVER is the one thing in here\lyou don't have to give back.` | 173px |

**`SafariZone_West_Text_PleaseFindWardensLostTeeth`** (`data/maps/SafariZone_West/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `REQUEST NOTICE\pPlease find the SAFARI WARDEN's\nlost GOLD TEETH.\lThey're around here somewhere.\pReward offered!\nContact: WARDEN` | 175px |
| today | `REQUEST NOTICE\pThe WARDEN has lost his TOKEN\nsomewhere out here.\pReward offered!\nContact: WARDEN` | 167px |
| DRAFT A | `REQUEST NOTICE\pThe WARDEN has lost his TOKEN\nsomewhere in the GARDEN.\pReward offered!\nContact: WARDEN` | 167px |
| DRAFT B | `REQUEST NOTICE\pThe WARDEN has lost his TOKEN.\nHe cannot sign this notice.\pReward offered (unsigned).\nContact: WARDEN` | 172px |

**`SafariZone_West_Text_SearchForSecretHouse`** (`data/maps/SafariZone_West/text.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `TRAINER TIPS\pZone Exploration Campaign!\nThe Search for the SECRET HOUSE!` | 188px |
| today | `USER TIPS\pZONE EXPLORATION CAMPAIGN!\pThe SECRET HOUSE is out here.\nNobody will say where.` | 168px |
| DRAFT A | `USER TIPS\pGARDEN EXPLORATION CAMPAIGN!\pThe SECRET HOUSE is out here.\nNobody will say where.` | 168px |
| DRAFT B | `USER TIPS\pRING EXPLORATION CAMPAIGN!\pThe SECRET HOUSE is in here.\nNobody will say where.` | 160px |


### THE SESSION ITSELF -- the PA, the menu, the battle, the help

**`SafariZone_Text_WouldYouLikeToExit`** (`data/text/safari_zone.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Would you like to exit the SAFARI\nZONE right now?` | 188px |
| today | `Would you like to exit the SAFARI\nZONE right now?` | 188px |
| DRAFT A | `Would you like to sign out of\nTHE WALLED GARDEN right now?` | 163px |
| DRAFT B | `End your guest session now?` | 151px |

**`SafariZone_Text_TimesUp`** (`data/text/safari_zone.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `PA: Ding-dong!\pTime's up!\pPA: Your SAFARI GAME is over!` | 168px |
| today | `PA: Ding-dong!\pTime's up!\pPA: Your SAFARI GAME is over!` | 168px |
| DRAFT A | `PA: Ding-dong!\pYour steps are used up!\pPA: Your guest session has\nexpired!` | 145px |
| DRAFT B | `PA: Ding-dong!\pSESSION EXPIRED.\pPA: Please return to the gate!` | 170px |

**`SafariZone_Text_OutOfBalls`** (`data/text/safari_zone.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `PA: Ding-dong!\pYou are out of SAFARI BALLS!\pPA: Your SAFARI GAME is over!` | 168px |
| today | `PA: Ding-dong!\pYou are out of GUESTBOXES!\pPA: Your SAFARI GAME is over!` | 168px |
| DRAFT A | `PA: Ding-dong!\pYou are out of GUESTBOXES!\pPA: Your guest session has\nexpired!` | 153px |
| DRAFT B | `PA: Ding-dong!\pYou are out of GUESTBOXES!\pPA: Please return to the gate!` | 170px |

**`sText_OutOfSafariBalls`** (`src/battle_message.c`)  

| | text | widest |
|---|---|---|
| vanilla | `{PLAY_SE SE_DING_DONG}ANNOUNCER: You're out of\nSAFARI BALLS! Game over!\p` | 143px |
| today | `{PLAY_SE SE_DING_DONG}ANNOUNCER: You're out of\nGUESTBOXES! Game over!\p` | 137px |
| DRAFT A | `{PLAY_SE SE_DING_DONG}ANNOUNCER: You're out of\nGUESTBOXES! Session expired!\p` | 160px |
| DRAFT B | `{PLAY_SE SE_DING_DONG}PA: You're out of GUESTBOXES!\nPlease return to the gate.\p` | 167px |

**`gText_MenuRetire`** (`src/strings.c`)  
*The START menu's first row while a session runs. A column holds 48px after its cursor (T-483): LOG OUT is 42, SIGN OUT exactly 48 with 0 to spare.*

| | text | widest |
|---|---|---|
| vanilla | `RETIRE` | 36px |
| today | `RETIRE` | 36px |
| DRAFT A | `LOG OUT` | 42px |
| DRAFT B | `SIGN OUT` | 48px |

**`gStartMenuDesc_Retire`** (`src/strings.c`)  

| | text | widest |
|---|---|---|
| vanilla | `Retire from the SAFARI GAME and return to\nthe registration counter.` | 233px |
| today | `Retire from the SAFARI GAME and return to\nthe registration counter.` | 233px |
| DRAFT A | `Sign out of your guest session and\nreturn to the gate.` | 189px |
| DRAFT B | `End your session in THE WALLED\nGARDEN and return to the gate.` | 171px |

**`gText_MenuSafariStats`** (`src/strings.c`)  
*Unchanged: steps and BOXES.*

| | text | widest |
|---|---|---|
| vanilla | `{STR_VAR_1}/{STR_VAR_2}\nBALLS  {STR_VAR_3}` | 42px |
| today | `{STR_VAR_1}/{STR_VAR_2}\nBOXES {STR_VAR_3}` | 36px |
| DRAFT A | `{STR_VAR_1}/{STR_VAR_2}\nBOXES {STR_VAR_3}` *(unchanged)* | 36px |
| DRAFT B | `{STR_VAR_1}/{STR_VAR_2}\nBOXES {STR_VAR_3}` *(unchanged)* | 36px |

**`Help_Text_WhatDoIDoInSafari`** (`data/text/help_system.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `What do I do in a SAFARI GAME?` | 176px |
| today | `What do I do in a SAFARI GAME?` | 176px |
| DRAFT A | `What do I do in THE WALLED GARDEN?` | 200px |
| DRAFT B | `What do I do as a guest?` | 140px |

**`Help_Text_WhatAreSafariRules`** (`data/text/help_system.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `What are the SAFARI GAME rules?` | 180px |
| today | `What are the SAFARI GAME rules?` | 180px |
| DRAFT A | `What are the GARDEN's rules?` | 158px |
| DRAFT B | `What are the guest session rules?` | 184px |

**`Help_Text_WantToEndSafari`** (`data/text/help_system.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `I want to end this SAFARI GAME!` | 178px |
| today | `I want to end this SAFARI GAME!` | 178px |
| DRAFT A | `I want to end my guest session!` | 174px |
| DRAFT B | `I want to sign out!` | 106px |

**`Help_Text_AnswerWhatAreSafariRules`** (`data/text/help_system.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `Your SAFARI GAME ends once you have\ntraveled a certain distance or thrown\lall your SAFARI BALLS.\lOpen the MENU to check the remaining\lnumber of steps and SAFARI BALLS.` | 206px |
| today | `Your SAFARI GAME ends once you have\ntraveled a certain distance or thrown\lall your GUESTBOXES. Open the MENU to\lcheck the remaining number of steps and\lGUESTBOXES.` | 218px |
| DRAFT A | `Your guest session ends once you have\ntraveled a certain distance or thrown\lall your GUESTBOXES. Open the MENU to\lcheck the remaining number of steps and\lGUESTBOXES.` | 218px |
| DRAFT B | `Your guest session ends once you have\ntraveled a certain distance or thrown\lall your GUESTBOXES. Open the MENU to\lcheck the remaining number of steps and\lGUESTBOXES.` | 218px |

**`Help_Text_AnswerWantToEndSafari`** (`data/text/help_system.inc`)  
*Follows the START label's pick.*

| | text | widest |
|---|---|---|
| vanilla | `If you would like to cut your SAFARI\nGAME short, open the MENU and select\l“RETIRE” at the top of the list.` | 207px |
| today | `If you would like to cut your SAFARI\nGAME short, open the MENU and select\l“RETIRE” at the top of the list.` | 207px |
| DRAFT A | `If you would like to end your guest\nsession early, open the MENU and select\l“LOG OUT” at the top of the list.` | 219px |
| DRAFT B | `If you would like to end your guest\nsession early, open the MENU and select\l“SIGN OUT” at the top of the list.` | 219px |

**`Help_Text_HowToUseBall`** (`data/text/help_system.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `{CIRCLE_1} Select to throw the special POKé\n   BALL used only in the SAFARI ZONE.\nWhen wild POKéMON appear, throw lots\nof SAFARI BALLS to catch them!` | 214px |
| today | `{CIRCLE_1} Select to throw the special BOX\n   used only in the SAFARI ZONE.\nWhen wild DAEMONS appear, throw lots\nof GUESTBOXES to bind them!` | 205px |
| DRAFT A | `{CIRCLE_1} Select to throw the special BOX\n   used only in THE WALLED GARDEN.\nWhen wild DAEMONS appear, throw lots\nof GUESTBOXES to bind them!` | 205px |
| DRAFT B | `{CIRCLE_1} Select to throw the special BOX\n   issued at the GARDEN's gate.\nWhen wild DAEMONS appear, throw lots\nof GUESTBOXES to bind them!` | 205px |

**`Help_Text_HowToUseBait`** (`data/text/help_system.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `{CIRCLE_1} Select to throw the special food\n   used only in the SAFARI ZONE.\nIt is POKéMON food rolled up into\na ball for easy eating. When BAIT is\nthrown, the wild POKéMON may get\nattracted by it, and may not flee!` | 202px |
| today | `{CIRCLE_1} Select to throw the special food\n   used only in the SAFARI ZONE.\nIt is DAEMON food rolled up into\na box for easy eating. When BAIT is\nthrown, the wild DAEMON may get\nattracted by it, and may not DETACH!` | 205px |
| DRAFT A | `{CIRCLE_1} Select to throw the special food\n   used only in THE WALLED GARDEN.\nIt is DAEMON food rolled up into\na box for easy eating. When BAIT is\nthrown, the wild DAEMON may get\nattracted by it, and may not DETACH!` | 205px |
| DRAFT B | `{CIRCLE_1} Select to throw the special food\n   used only in THE WALLED GARDEN.\nIt is DAEMON food rolled up into\na box for easy eating. When BAIT is\nthrown, the wild DAEMON may get\nattracted by it, and may not DETACH!` | 205px |

**`Help_Text_HowToUseRock`** (`data/text/help_system.inc`)  

| | text | widest |
|---|---|---|
| vanilla | `{CIRCLE_1} Select to throw a rock lying on\n   the ground in the SAFARI ZONE.\nThrowing a rock at a POKéMON may \nmake it run away, but it becomes easier\nto catch!` | 218px |
| today | `{CIRCLE_1} Select to throw a rock lying on\n   the ground in the SAFARI ZONE.\nThrowing a rock at a DAEMON may \nmake it run away, but it becomes easier\nto bind!` | 218px |
| DRAFT A | `{CIRCLE_1} Select to throw a rock lying on\n   the ground in THE WALLED GARDEN.\nThrowing a rock at a DAEMON may \nmake it run away, but it becomes easier\nto bind!` | 218px |
| DRAFT B | `{CIRCLE_1} Select to throw a rock lying on\n   the ground in THE WALLED GARDEN.\nThrowing a rock at a DAEMON may \nmake it run away, but it becomes easier\nto bind!` | 218px |


### THE MAP, THE LOG AND THE FAME CHECKER

**`gText_RegionMap_AreaDesc_SafariZone`** (`src/strings.c`)  
*Four lines, each ending \n (TODO 557).*

| | text | widest |
|---|---|---|
| vanilla | `An amusement park outside FUCHSIA\nCITY where many rare POKéMON can\nbe observed in the wild.\nCatch them in a popular game!` | 188px |
| today | `An amusement park outside LURID\nCITY where many rare DAEMON can\nbe observed in the wild. Bind them\nin a popular game!` | 190px |
| DRAFT A | `A platform behind a wall outside\nLURID CITY. DAEMONS that are not\nsigned run here, and only here.\nGuests may bind them.` | 186px |
| DRAFT B | `LURID CITY's curated park. Its\nDAEMONS run inside the wall and\nnowhere else. Guests welcome,\nmetered by the step.` | 174px |

**`gText_QuestLog_HadGreatTimeInSafariZone`** (`src/data/text/quest_log.h`)  

| | text | widest |
|---|---|---|
| vanilla | `{PLAYER} had a great time with POKéMON\nin the SAFARI ZONE.` | 214px |
| today | `{PLAYER} had a great time with\nDAEMON in the SAFARI ZONE.` | 166px |
| DRAFT A | `{PLAYER} had a great time with\nDAEMON in THE WALLED GARDEN.` | 166px |
| DRAFT B | `{PLAYER} spent a guest session in\nTHE WALLED GARDEN.` | 178px |

**`gText_QuestLog_SafariZone`** (`src/data/text/quest_log.h`)  

| | text | widest |
|---|---|---|
| vanilla | `SAFARI ZONE` | 66px |
| today | `SAFARI ZONE` | 66px |
| DRAFT A | `THE WALLED GARDEN` | 102px |
| DRAFT B | `THE WALLED GARDEN` | 102px |
