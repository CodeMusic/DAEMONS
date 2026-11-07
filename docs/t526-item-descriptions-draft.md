# T-526 — item descriptions that still read as FireRed's (DRAFT)

*Drafted 2026-11-07 while the user was away. **Every line below is DRAFT.** **Built the same day:** the user,
2026-11-07, "Build all 16". All 16 are in `T526_APPROVED` in `tools/port_item_text.py` and in the engine. The user's
answers changed four things:

- **SUBTLE LAYER:** the item says USER, and so does the book's cover: "a USER's handbook" (`tools/gensubtle.py`,
  `tools/bookpdf.py`, and the companion's book page through `companion_export.py`).
- **The scarves name the day.** RED, BLUE and YELLOW say PARADE DAYS. GREEN says CLOVER DAY and PARADE DAYS. PINK
  says "like the ones handed out on PARADE DAYS", because nothing gives it out.
- **S.S. TICKET** keeps HOLT, and **LAVA COOKIE** keeps "baked on hot stone".
- **TOKEN CASE** keeps its name for now.*

**The picture:** `qa/screenshots/` (T-526), drawn by `python3 tools/port_item_text.py --sheet OUT.png`. It shows
each description as it is now beside its draft, in the BAG's own font and 200x48 window, with the 198px budget
dotted.

## How the sweep was done

All 376 rows of `engineGba/src/data/items.json` were read, then checked for:

- vanilla and Hoenn place names;
- POKéMON words the vocabulary pass missed;
- type names and state names DAEMONS renamed;
- vanilla verbs the vocabulary pass never had;
- vanilla's object where the item is ours.

Each finding was then checked for **reachability** (2.10's rule, as `port_item_text.py` already applies it to the
berries). A row is drafted when the player can hold the item, from any of these sources:

- a map item or a hidden item;
- a mart;
- a gift script;
- a holiday in `src/data/daemons_holidays.h`;
- a wild daemon's held item.

Every line was measured with the engine's own width table (`tools/fontwidth.py`) against the 198px item-description
budget in `docs/engine.md`. None is over it, and none is longer than three lines.

## The drafts (16)

| Item (shown as) | Now | DRAFT | Why |
|---|---|---|---|
| TOKEN CASE (`COIN_CASE`) | Holds the tokens the GAME CORNER / deals in. It holds up to 9,999. | A token spends only where it was / issued. Holds the GAME CORNER's / COINS, up to 9,999. | It said "tokens", but the GAME CORNER deals in COINS everywhere else. The place keeps its name (CORPUS GAME CORNER, vision 3.9). |
| S.S. TICKET | The ticket required for sailing on / the ferry S.S. ANNE. / It has a drawing of a ship on it. | Passage on the S.S. ANNE, at / ARDOR CITY. Made out to HOLT, / who gave it to you instead. | This is vanilla's ferry ticket. HOLT hands it over because he was invited and will not go ("You go."). The ship keeps its name. |
| BIKE VOUCHER | Take this voucher to the BIKE SHOP / in DOLDRUM CITY and exchange it / for a bicycle. | One BICYCLE, owed to whoever / holds this. The BIKE SHOP in / DOLDRUM CITY pays it out. | This is vanilla's instruction with only the town renamed. |
| LAVA COOKIE | LAVARIDGE TOWN's local specialty. / It heals all the status problems of / one DAEMON. | A cookie baked on hot stone, sold / on TWO ISLAND. Ends every state / of one DAEMON. | LAVARIDGE is in Hoenn. TWO ISLAND's shop sells the cookie, and it is also hidden on the S.S. ANNE and given on holidays. Its effect is `ITEM3_STATUS_ALL`, the same as ROLLBACK, so it ends every state. |
| RED SCARF | An item to be held by a DAEMON. / It boosts the holding DAEMON's / COOL condition in CONTESTS. | A red scarf, handed out on / PARADE DAYS. It changes nothing / in battle. It is worn for the day. | CONTESTS are Hoenn's and do not exist here. PARADE DAYS gives this scarf, and it has `HOLD_EFFECT_NONE`. |
| BLUE SCARF | … STYLIST condition in CONTESTS. | A blue scarf, handed out on / PARADE DAYS. It changes nothing / in battle. It is worn for the day. | The same as the RED SCARF. |
| PINK SCARF | … CUTE condition in CONTESTS. | A pink scarf, like the ones handed / out on PARADE DAYS. It changes / nothing in battle. | The same, except nothing gives this one out. It is drafted to match its set. |
| GREEN SCARF | … SMART condition in CONTESTS. | A green scarf, handed out on / CLOVER DAY and PARADE DAYS. It / changes nothing in battle. | The same. CLOVER DAY and PARADE DAYS both give it. |
| YELLOW SCARF | … TOUGH condition in CONTESTS. | A yellow scarf, handed out on / PARADE DAYS. It changes nothing / in battle. It is worn for the day. | The same as the RED SCARF. |
| NET BOX | A somewhat different BOX that / works especially well on / WATER- and SWARM-type DAEMON. | … / FLOW- and SWARM-type DAEMONS. | WATER is FLOW here. The vocabulary pass also took the plural for a singular. |
| NEST BOX | … works especially well on weaker / DAEMON. | … / DAEMONS. | Plural taken for singular. |
| REPEAT BOX | … works especially well on DAEMON / bound before. | … DAEMONS / bound before. | Plural taken for singular. |
| DESCEND BOX (`DIVE_BALL`) | … works especially well on DAEMON / deep in the sea. | … DAEMONS / deep in the sea. | Plural taken for singular. Nothing gives this one out; it is drafted with its set. |
| LUXURY BOX | A comfortable BOX that makes a / captured wild DAEMON quickly grow / friendly. | … / bound wild DAEMON quickly grow / friendly. | "captured" is the one capture verb the vocabulary pass never had. Everywhere else, catch has become bind. |
| RETRO MAIL | A piece of MAIL featuring a print / of three cute DAEMON. It is to / be held by a DAEMON. | … / of three cute DAEMONS. … | Plural taken for singular. |
| SUBTLE LAYER | THE SUBTLE LAYER. A trainer's / handbook of the craft: read, / write and link. | THE SUBTLE LAYER. A USER's / handbook of the craft: read, / write and link. | TRAINER is USER everywhere else. **This one is a question, not a fix** (see below). |

## Checked and right as it stands

**CALM TONE** (`YELLOW_FLUTE`), "… Ends THRASHING.", is correct:

- Its effect is `sItemEffect_YellowFlute = ITEM3_CONFUSION`.
- CONFUSION is THRASHING in vision 1.6.
- It can be used only in battle (`FieldUseFunc_OakStopsYou`, `BattleUseFunc_Medicine`), and THRASHING is the state
  that ends with the fight.

No draft is needed.

## Kept on purpose

These stay as they are under 2.8 and T-14's rule: an object stays an object. Their wording is FireRed's, but it
describes the thing truly in this world.

- **The drinks:** FRESH WATER, SODA POP, LEMONADE and MOOMOO MILK.
- **Things you sell:** NUGGET, PEARL, BIG PEARL, STARDUST, STAR PIECE, HEART SCALE and the mushrooms.
- **The coloured shards.**
- **TEA:** the lady in VERDIGRIS still makes it.
- **SECRET KEY, METEORITE, POWDER JAR, PREMIER BOX and TIMER BOX.**
- **The other mail.**
- **The berries that only "can be ground up into a powder":** BERRY POWDER and its maker are both in DOLDRUM.

## Left alone: Hoenn items nothing in the game hands out

None of these is held by any map, mart, script, holiday or wild daemon. They are listed so the sweep is complete.

- **Items:** SHOAL SALT, SHOAL SHELL, FLUFFY TAIL, ENIGMA BERRY.
- **Key items:** CONTEST PASS, WAILMER PAIL, SOOT SACK, BASEMENT KEY, {POKEBLOCK} CASE, EON TICKET, RED ORB, BLUE ORB,
  SCANNER, GO-GOGGLES, MACH BIKE, ACRO BIKE, ROOT FOSSIL, CLAW FOSSIL, DEVON SCOPE.
- **The ABANDONED SHIP keys:** RM. 1 KEY, RM. 2 KEY, RM. 4 KEY, RM. 6 KEY, STORAGE KEY.

The DEBUG kit can still show them.

## Questions for the user (answered 2026-11-07, above)

1. **SUBTLE LAYER.** The book's cover subtitle is "a trainer's handbook" (`tools/gensubtle.py`, `tools/bookpdf.py`).
   Should the item say USER while the cover keeps "trainer"? Should both say USER? Or should both keep "trainer",
   because it is the book's own phrase?
2. **TOKEN CASE.** The draft keeps the GAME CORNER's name, because the game calls it that. A separate question is
   that the case is named TOKEN while the WARDEN's key (`GOLD_TEETH`) is also called TOKEN, so two different items
   share the word.
3. **The scarves.** Should they say "a holiday", or name the day? PARADE DAYS gives four of them and CLOVER DAY one,
   but the holiday table may still change.
4. **LAVA COOKIE.** "Baked on hot stone" is new detail about the world. It nods to the heat of MT. SMOULDER nearby
   without naming it.

## The TRAP TABLE (added 2026-11-07, the user's two decisions)

The T-525 batch-3 agent filmed the TRAP TABLE (qa 7Nov2026 T525 22), and the user decided two fixes.

**THROTTLE TRAP's row ran over.** The user chose to widen the row and keep the name.

- Each row of the TRAP TABLE's list is built into a fixed slot in `src/berry_pouch.c`. A row holds FONT_SMALL (3
  bytes), {NO}{CLEAR 0x01} (5), two digits, a space, FONT_NORMAL (3), the name and its EOS.
- A 13-letter name makes that 28 bytes, and vanilla's slot was 27. The EOS spilled into the next row, so the screen
  read "THROTTLE TRAP№02 SU" and lost the x2.
- The slot is now 32 bytes (`BERRY_ROW_LEN`), in the allocation and every index.
- The BAG's list (`item_menu.c`, 19-byte rows: a 4-byte colour code, 13 letters and the EOS) and the TM CASE
  (`tm_case.c`, 29-byte rows, which an HM with a 12-letter routine fills exactly) both fit. The item PC points at the
  name itself.

**Ten TRAP descriptions were three lines in a two-line window.** The user chose "Rewrite to 2 lines". The window is
200x32, FONT_NORMAL at y=2, and every line is within the 198px budget. All ten are DRAFT.

| TRAP | Was (the third line never showed) | DRAFT |
|---|---|---|
| THROTTLE TRAP | Armed against one condition and / spent on it. Ends THROTTLED, / once. | Armed against one condition, spent / on it. Ends THROTTLED, once. |
| SUSPEND TRAP | Fires the moment the daemon stops / being scheduled. Ends SUSPENDED, / once. | Fires when the daemon stops being / scheduled. Ends SUSPENDED, once. |
| THRASH TRAP | Catches a daemon making no / progress against itself. Ends / THRASHING, once. | Catches a daemon working against / itself. Ends THRASHING, once. |
| LOW MARK | The level at which something is / done about it. Restores 10 HP / when health falls, once. | A mark set low. When health falls, / it restores 10 HP, once. |
| HIGH MARK | The same idea, set higher and / worth more. Restores 30 HP when / health falls, once. | The same, set higher. When health / falls, it restores 30 HP, once. |
| SPICY, DRY, SWEET, BITTER and SOUR TRAP | Restores health, and may leave a / daemon THRASHING. Which is which / depends on the daemon. | Restores health. Whether it causes / THRASHING depends on the daemon. |

The picture is `python3 tools/port_item_text.py --trap-sheet OUT.png`: each row before and after, in the TRAP
TABLE's own window, at real size and at 3x.
