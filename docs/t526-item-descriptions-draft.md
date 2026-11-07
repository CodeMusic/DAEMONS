# T-526 — item descriptions that still read as FireRed's (DRAFT)

*Drafted 2026-11-07 while the user was away. **Every line below is DRAFT, and none of it is in the engine.** The
words are the user's to approve, change or refuse. Approve rows by name:
`python3 tools/port_item_text.py --write --approved ITEM ...`, which writes only those rows' descriptions and
nothing else; then list them in `T526_APPROVED` in the same tool, so its whole-table `--write` keeps them.*

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
| RED SCARF | An item to be held by a DAEMON. / It boosts the holding DAEMON's / COOL condition in CONTESTS. | A red scarf, handed out on a / holiday. It changes nothing in / battle. It is worn for the day. | CONTESTS are Hoenn's and do not exist here. PARADE DAYS gives this scarf, and it has `HOLD_EFFECT_NONE`. |
| BLUE SCARF | … STYLIST condition in CONTESTS. | A blue scarf, handed out on a / holiday. It changes nothing in / battle. It is worn for the day. | The same as the RED SCARF. |
| PINK SCARF | … CUTE condition in CONTESTS. | A pink scarf, handed out on a / holiday. It changes nothing in / battle. It is worn for the day. | The same, except nothing gives this one out. It is drafted to match its set. |
| GREEN SCARF | … SMART condition in CONTESTS. | A green scarf, handed out on a / holiday. It changes nothing in / battle. It is worn for the day. | The same. CLOVER DAY and PARADE DAYS both give it. |
| YELLOW SCARF | … TOUGH condition in CONTESTS. | A yellow scarf, handed out on a / holiday. It changes nothing in / battle. It is worn for the day. | The same as the RED SCARF. |
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

## Questions for the user

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
