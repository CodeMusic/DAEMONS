# T-535 — the second item-description sweep (DRAFT)

*Drafted 2026-11-09 (the user picked "Item description sweep"). **Every line below is DRAFT, and nothing is in the
engine.** The drafts are `T535` in `tools/port_item_text.py`. `T535_APPROVED` is empty, so a plain `--write` still
changes nothing. To approve rows: `python3 tools/port_item_text.py --write --approved ITEM ...`, then add the same
rows to `T535_APPROVED`.*

**The pictures** are in `qa/screenshots/2026-11-09/`:

- **9Nov2026 T535 13** shows the 18 BAG rows in the BAG's own font and 200x48 window, at 1x and 2x
  (`--t535-sheet OUT.png`).
- **9Nov2026 T535 14** shows the 20 berries in the TRAP TABLE's 200x32 window. That window shows two lines. The
  sheet is at 1x and 3x (`--t535-trap-sheet OUT.png`).

The dotted line on each sheet marks the 198px budget.

## Why a second sweep

T-526 kept these rows "on purpose", under the rule that an object stays an object. Then T-525 batch 4 drew an icon
for each one, showing what the item is. The batch-4 film shows they still read as FireRed:

- the valuables say "sold at a high price";
- the mushrooms say "popular among certain people";
- the shards say "from some sort of a tool";
- POWDER JAR names a BERRY CRUSHER;
- all twenty berries share vanilla's one line.

To find every row like these, each engine description was compared with pret's `upstream/master` `items.json`.
Rows at a 0.75 match or higher were then checked for reachability by T-526's rule (2.10). A row is drafted only if
a map, a mart, a script, a holiday, a trade or a wild daemon's held item gives the item out.

Every line was measured with the engine's own width table, and none is over 198px. Every BAG row is three lines or
fewer, and every berry is exactly two. Each draft is about as long as the line it replaces.

## The drafts (38)

### The BAG (18)

| Item | Now | DRAFT | Why |
|---|---|---|---|
| NUGGET | A nugget of pure gold that gives / off a lustrous gleam. / It can be sold at a high price. | A lump of pure gold. It does / nothing at all, and every shop / will pay a great deal for it. | "Sold at a high price" is vanilla's line. The joke stays under the line and is never said (craft rule 6). |
| PEARL | A relatively small pearl that / sparkles in a pretty silver color. / It can be sold cheaply. | A small pearl that sparkles a / pretty silver. A shop will give / a little for it. | These are vanilla's words. The price is kept, as something a shop does. |
| BIG PEARL | A quite-large pearl that sparkles / in a pretty silver color. / It can be sold at a high price. | The same silver pearl, left to / grow for longer. A shop will / give a great deal for it. | A pearl's size comes from time. |
| STARDUST | A pretty red sand with a loose, / silky feel. / It can be sold at a high price. | A pretty red sand with a loose, / silky feel. It sells for far / more than sand should. | The first line is kept. Only the price line was vanilla's. |
| STAR PIECE | A shard of a pretty gem that / sparkles in a red color. / It can be sold at a high price. | A red gem cut as a star, one / arm broken off. It sells for a / great deal even so. | The icon shows a star with one arm broken off. |
| TINYMUSHROOM | A small and rare mushroom. / It is quite popular among certain / people. | A small, rare mushroom. The / ROUTINE ARCHIVIST on TWO ISLAND / takes two for one lesson. | The "certain people" is one person: the ROUTINE ARCHIVIST in `TwoIsland_House`, who teaches a ROUTINE for two TINYMUSHROOMS. |
| BIG MUSHROOM | A large and rare mushroom. / It is very popular among certain / people. | A large, rare mushroom. The / ROUTINE ARCHIVIST on TWO ISLAND / takes it for one lesson. | The ARCHIVIST takes one BIG MUSHROOM for a lesson. |
| HEART SCALE | A pretty, heart-shaped scale that / is extremely rare. It glows faintly / in the colors of a rainbow. | A pale, heart-shaped scale with / growth lines. It glows faintly in / every color. PAIRING DAY gives it. | PAIRING DAY hands it out (`daemons_holidays.h`), and it is also hidden at TANOBY RUINS. Nothing in the game uses it. |
| RED SHARD | A small red shard. / It appears to be from some sort of / a tool made long ago. | A small red piece with a groove / cut to fit something. Whatever / it fit was made long ago. | The icon is a worked piece with a cut groove. Wild daemons hold these. |
| BLUE SHARD | (the same, blue) | A small blue piece with a groove / cut to fit something. Whatever / it fit was made long ago. | The same as the RED SHARD. |
| YELLOW SHARD | (the same, yellow) | A small yellow piece with a / groove cut to fit something. / Whatever it fit was made long ago. | The same as the RED SHARD. The word "yellow" moves the line break. |
| GREEN SHARD | (the same, green) | A small green piece with a / groove cut to fit something. / Whatever it fit was made long ago. | The same as the RED SHARD. |
| MOOMOO MILK | Highly nutritious milk. It restores / the HP of one DAEMON by 100 / points. | Milk from TWO ISLAND, sold there / by the bottle. It restores the HP / of one DAEMON by 100 points. | "Highly nutritious" is vanilla's. TWO ISLAND's shop sells the milk, and NEST DAY gives it. |
| GLITTER MAIL | A piece of MAIL featuring a cute / SPIKE print. It is to be held by / a DAEMON. | MAIL printed with a SPIKE in / glitter. Write on it, and a / DAEMON will hold it. | "A cute ... print" and "It is to be held" are vanilla's. FIR LIGHTS and the holiday presents give it. |
| SHADOW MAIL | A piece of MAIL featuring / a cute FADING print. It is / to be held by a DAEMON. | MAIL printed with a FADING, half / gone into the paper. Write on it, / and a DAEMON will hold it. | The icon shows the print fading out. MASK NIGHT gives it. |
| DREAM MAIL | A piece of MAIL to be held by a / DAEMON. It will bear the print of / the DAEMON holding it. | MAIL with an outline left blank. / It takes the print of the DAEMON / that holds it. | The meaning is vanilla's and the words are ours. The icon is a dashed outline, waiting. SIX ISLAND's mart sells it. |
| FAB MAIL | A piece of MAIL featuring a / gorgeous, extravagant print. It / is to be held by a DAEMON. | MAIL in a gold lattice print, far / too fine for what it will say. / A DAEMON will hold it. | "Gorgeous, extravagant" is vanilla's. PAIRING DAY and a trade give it. |
| POWDER JAR | A jar for storing BERRY POWDER / made using a BERRY CRUSHER. | A jar for the BERRY POWDER made / by crushing BERRIES. DOLDRUM / CITY's medicine-maker wants it. | Nothing in the game is called a BERRY CRUSHER. The game has "a Wireless Adapter machine for crushing BERRIES" at the CHECKPOINTS' DIRECT CORNER, and the BERRY CRUSH minigame. BERRY POWDER keeps its name. The man who gives the jar and trades for the powder is in DOLDRUM CITY (`CeruleanCity_House5`). |

### The TRAP TABLE: the twenty berries (two lines each)

These berries kept their vanilla names, and they are literal fruit, not TRAPs. Each line describes the fruit its
icon shows (T-525 batch 4) and the taste and firmness that `src/berry.c` gives it. Flavours are written in lower
case, so no berry reads like one of the five flavour TRAPs. Every berry's line replaces the one they all shared:
"Can be ground up into a powder as / an ingredient for medicine."

| Berry | DRAFT | berry.c |
|---|---|---|
| RAZZ | A red berry, hard as a pebble. / It tastes spicy, then dry. | very hard; spicy, dry |
| BLUK | A soft blueberry under a little / crown. Dry first, then sweet. | soft; dry, sweet |
| NANAB | A banana, very hard. Sweet, with / something bitter under it. | very hard; sweet, bitter |
| WEPEAR | A pear harder than it looks. / Bitter and sour all the way down. | super hard; bitter, sour |
| PINAP | A small pineapple. Spicy and sour, / and the leaves are not for eating. | hard; spicy, sour |
| POMEG | A pomegranate, very hard. Spicy, / sweet and bitter, all in one. | very hard; spicy, sweet, bitter |
| KELPSY | A blue root that grows like kelp. / Dry, bitter and a little sour. | hard; dry, bitter, sour |
| QUALOT | A dimpled yellow round. Spicy, / sweet and sour, by turns. | hard; spicy, sweet, sour |
| HONDEW | A netted honeydew. Spicy, dry and / bitter, which melons rarely are. | hard; spicy, dry, bitter |
| GREPA | A soft bunch of pale gold grapes. / Dry, sweet and sour together. | soft; dry, sweet, sour |
| TAMATO | A soft, very red tomato. Spicier / than a tomato has any right to be. | soft; spicy 20 |
| CORNN | A purple cob in its husk. Mostly / dry, with a little sweetness. | hard; dry 20, sweet 10 |
| MAGOST | A mangosteen, hard-shelled. Sweet / inside, and bitter at the rind. | hard; sweet 20, bitter 10 |
| RABUTA | A hairy rambutan, soft to hold. / Bitter, with a sour finish. | soft; bitter 20, sour 10 |
| NOMEL | A lemon, very large and very hard. / Sour, as lemons are. A bit spicy. | super hard, 285mm; sour 20, spicy 10 |
| SPELON | A long red fruit covered in spines. / Fiercely spicy. Hold it carefully. | soft; spicy 40 |
| PAMTRE | A long pink fruit in bands, so soft / it bruises. Very dry. | very soft; dry 40 |
| WATMEL | A big striped melon, soft and / heavy. Very sweet. | soft, 250mm; sweet 40 |
| DURIN | A durian, thorned and hard. Very / bitter, and it smells. | hard; bitter 40 |
| BELUE | A glossy plum-black berry, so soft / it barely holds. Very sour. | very soft; sour 40 |

Where the berries come from:

- RAZZ to PINAP are found on the map (hidden on routes and on THREE, FIVE, SIX and SEVEN ISLAND).
- POMEG to NOMEL come only from DODRIO BERRY PICKING over wireless.
- SPELON to BELUE come from PICKUP.

## Checked, and kept as they stand

- **METEORITE, PEER REVIEW and ENVELOPE** are already ours.
- **T-526's 16 rows** (TOKEN CASE, the scarves, RETRO MAIL, LAVA COOKIE and the rest) are not redone.
- **FRESH WATER, SODA POP and LEMONADE** are worded as in vanilla, but they say truly what the drinks are. T-526
  kept them on purpose, and the user approved that. They are a question below.
- **TEA** is a key item in the story: the lady in VERDIGRIS makes it. It is left alone.
- **TIMER BOX and PREMIER BOX** are worded as in vanilla, but T-526 kept the "somewhat different BOX" set, and the
  user approved it.
- **MP UP, MP MAX, BICYCLE and TRI-PASS** are true as written.
- These rows still read as vanilla, but nothing hands the items out, so they are left alone:
  - SHOAL SALT, SHOAL SHELL and FLUFFY TAIL;
  - ORANGE, HARBOR, MECH, WOOD, WAVE, BEAD and TROPIC MAIL;
  - ENIGMA BERRY;
  - the Hoenn key items (as in T-526);
  - MYSTICTICKET (Mystery Gift only).

## Questions for the user

1. **The berries no longer mention BERRY POWDER.** The only use these 20 have here is the BERRY CRUSH, which needs
   the wireless machine. Only POWDER JAR's line now says so. Should some berries say "crushes to BERRY POWDER"
   instead of their taste?
2. **The valuables' joke.** NUGGET's "It does nothing at all" and STARDUST's "more than sand should" sit under
   craft rule 6. Is that the right amount of joke, or should they be plainer?
3. **The mushrooms name the ROUTINE ARCHIVIST.** That tells the player where the mushrooms go. Vanilla left it
   vague.
4. **MOOMOO MILK**, "sold there by the bottle", adds a little detail to the world. Should the drinks get the same
   treatment, or stay as T-526 left them?
5. **RETRO MAIL** still ends "It is to be held by a DAEMON." (T-526). If the new MAIL lines are approved, it no longer
   matches its set.
