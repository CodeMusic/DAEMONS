# The Cardputers {#cardputers .t-CONTEXT}

A daemon you **SEND** out of your game lives on the companion: the app on your phone, the site at home, and any device
you give it. This book is about one family of those devices, **the Cardputers**: M5Stack's small computers with a
keyboard under the screen. They are the devices you **type** on -- a word to every daemon nearby, a Wi-Fi password, a
note -- and the newest of them, the **Cardputer Zero**, is the first device the **game itself** is played on.

There are three, and two kinds of caps that fit on top:

| | **the Cardputer** | **the Cardputer ADV** | **the Cardputer Zero** |
|---|---|---|---|
| **inside** | an ESP32-S3 | an ESP32-S3 | a Raspberry Pi, running Linux |
| **the screen** | 240 x 135 | 240 x 135 | 320 x 170 |
| **the keys** | four rows of fourteen | the same | forty-six, with Shift, Sym and Fn |
| **DAEMONS on it** | the companion: your daemon, its care, its routines | the same, and LoRa with its cap | **the game, played on it**, and the companion around it |
| **how it gets there** | put on by its cable | put on by its cable | installed as an app; nothing is put over its own software |
| **a cap on top** | -- | yes | yes |

Where this book says *a Cardputer*, it means any of the three. The Cardputer and the ADV run the **same software**,
the one every handheld board of the companion runs, so they are told together in [The Cardputer and the
ADV](#esp). The Zero is a different thing, a small computer, and has its chapter: [The Cardputer Zero](#zero). The
caps are in [The caps](#caps).

{{diagram family | The three, drawn. The Zero is a little larger, with a wider screen and fewer keys; the ADV and the Zero take a cap on the header along their top.}}

{{daemons PUNCHCARD}}

::: note
**The rest of the companion** -- the app, its tabs, the hub at home -- is in **THE COMPANION**. How to play the game is
in **THE PLAYER'S MANUAL**. Both stand on the LIBRARY's MANUALS shelf, beside this one.
:::

## What you need {#need}

- **A Cardputer.** The Cardputer and the ADV take the companion's own software, put on once by their cable. The Zero
  keeps M5Stack's own system, and DAEMONS is installed on it as one of its apps.
- **The companion**: the app on your phone, and, for most things, **the hub** at home.
- **A daemon to carry.** In the game, choose **SEND** in a daemon's menu and save; then **SYNC** in the app.
- **For the Zero, your own game**: a *FireRed* or *LeafGreen* you backed up yourself. DAEMONS is made from it, on the
  device ([Making the game](#make)). No game comes with DAEMONS, or ever will.

# The keys {#keys .t-FLOW}

Every Cardputer is worked from its keyboard. The Cardputer and the ADV have one button besides, **BOOT** (marked
**G0**).

## On the Cardputer and the ADV {#keys-esp}

| to | press |
|---|---|
| **move** | **;** and **,** go up or back a row, **.** and **/** go down or on. Where something is being typed, hold **Fn** with them -- they are the arrows printed on those keys |
| **open, choose** | **Enter**, or **BOOT** |
| **back** | **del**, or hold **BOOT** |
| **type** | any letter at HOME starts a word to every daemon ([A word to every daemon](#word)) |
| **capitals** | hold **Shift** |
| **Esc** | **Fn** with **`** |
| **wake** | any key: the first only wakes it |

The foot of a page says what its keys do there: *enter*, *del*, *; .* to move.

## On the Zero {#keys-zero}

The Zero has **no arrow keys**: **F**, **Z**, **X** and **C** are its arrows, printed on them. In the game they are
the pad, and the rest of a Game Boy Advance's buttons sit where the hands fall:

{{diagram keys | The game's buttons on the Zero's keys. A drawing, not the keyboard: where ESC, TAB, Fn and Sym sit is the device's own.}}

| the game's | the Zero's key | |
|---|---|---|
| **the pad** | **F** up, **Z** left, **X** down, **C** right | the arrows printed on the device |
| **A** and **B** | **L** and **K** | under the right thumb, A to the right of B as on the handheld |
| **L** and **R** | **Q** and **P** | the two ends of the top row |
| **START** and **SELECT** | **ENTER** and **SPACE** | |
| **leave the game** | **ESC** | the game waits, paused, and DAEMONS' HOME is in front |

Away from the game, **Z** and **C** (or **TAB**) move along a row, **ENTER** chooses, **ESC** goes back, and
**BACKSPACE** takes back a letter, or a step just ticked.

The keys are **kept in a file on the device**, one line a button (`A = L`), so they can be changed. *The keys are a
draft until they have been held in the hand: they were chosen from M5Stack's own drawings, before the device came.*

# The Cardputer and the ADV {#esp .t-SIGNAL}

The Cardputer and the ADV carry one daemon each, as every handheld board of the companion does: your daemon in its
den, its care, the day's one step, and the **routines** -- the board's radios in the game's words. They are the boards
you can type on.

**Told apart by themselves.** One software runs on both. When it starts it asks what answers on its wires: the ADV's
keyboard chip and its sound chip answer, the Cardputer's keyboard does not, and each knows which it is.

## Putting the software on {#flashing}

A Cardputer from the shop runs M5Stack's own software. The companion's is put on once, by its USB-C cable, from the
computer that runs the companion: the companion's **update script**. A Cardputer that has never run the companion says
nothing when asked what it is, so tell the script: **`m5-cardputer`**, the name of the build both share. The
companion's wiki, *Flashing and linking*, has every step.

If the computer cannot reach it, hold **BOOT** while plugging the cable in.

## Linking it {#linking}

The Cardputer needs to find the companion. There are three ways, and any one will do -- but link it **by its cable
once**, because that is when the companion gives it a key of its own, the networks your devices share, and the way to
reach home from away.

- **By its cable, at the computer that runs the hub**: the companion's **link script**. The corner says **USB**.
- **By your phone**: **ROUTINES**, **WHISPER**, **PAIR MY PHONE**. It shows six numbers; pair the device in the app,
  and when iOS asks, type the numbers. The phone then carries its link wherever you both go. **FORGET MY PHONES**, in
  the same place, unpairs them all.
- **By your Wi-Fi**: **ROUTINES**, **UPLINK**, **TEACH A NETWORK**. Choose the network and **type its password** on the
  keys -- no letter wheel here -- then **Enter**. It joins whenever it is near, and every one of your devices learns the
  network too.

## The corner {#corner}

The top right of the screen says how it is linked, beside the battery:

| the corner says | it means |
|---|---|
| **USB** | through its cable, at the computer |
| **WIFI** | at home, on your Wi-Fi, talking to the hub |
| **PHONE** | through your phone, by Bluetooth |
| **AWAY** | away from home on a Wi-Fi it knows, through the companion's relay |

## Its pages {#pages}

- **HOME is your daemon**, in its **den** -- a room that looks like its type -- breathing, walking, now and then
  hopping, and looking how it has been cared for. Around it: its mood in a word, how it has eaten and drunk today.
- **TODAY**: the one step. **Enter** ticks it off; **del** undoes it, for fifteen seconds.
- **DAEMON**: your daemon as the game draws it, its level and friendship. **Enter** for its INDEX entry, in your
  edition's words.
- **ROUTINES**: below.
- **THE DAY**: its theme, its virtue over its shadow, its note.
- **SOUND**: on or off.
- **SWITCH OFF**: the last page. **Enter**, and it is off.

Left alone two minutes it sleeps, and a key wakes it back at HOME.

## Care {#care}

**Enter** at HOME opens **CARE**: **DRINK**, **FEED**, **TRAIN**, **SLEEP**, or **ITS INDEX ENTRY**. The daemon answers
at once -- its word, its face, a hop and a few notes in the day's key -- and the companion is told after, so the
Cardputer never waits on the network. **Each step you finish counts as a meal**, and comes home with your daemon at
the next SYNC.

## A word to every daemon {#word}

**Type anything at HOME**, and the page becomes **TO EVERY DAEMON**: what you type, and how many letters are left --
eighty at most. **Enter** sends it, **del** takes back a letter, and **del** on nothing leaves.

It goes **every way the Cardputer has**: by Bluetooth to daemons nearby, through the companion to your own devices
anywhere, and on an ADV with its LoRa cap over the air, further ([The Cap LoRa-1262](#lora)). Each daemon that hears
it shows it once, however many ways it arrives, and answers it once, a few seconds later. On an ADV with its cap the
foot of HOME says so: *type: a message nearby*.

**CHORUS**, in ROUTINES, does the same with an act -- **TYPE A WORD** first, then WAVE, BOW, HUM A TUNE, DANCE and the
rest -- and **WHAT CAME** shows the last ten that arrived, each marked how: **L** LoRa, **B** Bluetooth, **N** the
companion.

## Routines {#routines}

**ROUTINES** shows only what a Cardputer has:

| the routine | what it does |
|---|---|
| **CASINO** | **SLOTS**: three reels of daemons, played with your game's own money. The next SYNC writes the difference into your save |
| **CHORUS** | an act or a word to every daemon, and **WHAT CAME** |
| **WHISPER** | your phone, over Bluetooth: **PAIR MY PHONE**, **OPEN TO MY PHONE**, **FORGET MY PHONES** |
| **TOUCHSTONE** | **A NOTE FOR A CARD**: type a note, and the companion keeps it until one of your devices with a card reader writes it onto the next card held to it |
| **MESH** | on an ADV with its LoRa cap: **NEARBY**, the daemons heard over the air, and **CALL OUT**, a wave or a word to them |
| **PARTY** | your party from the game, and each daemon's own routines in their streak colours |
| **UPLINK** | your Wi-Fi: **NETWORKS IN RANGE**, **TEACH A NETWORK**, and **WI-FI MOTION**, which notices movement near the line to your router |

A routine is your daemon's: it needs one on the Cardputer, and speaks in its name. **del** gives up one that is
waiting.

## Sound and light {#sound}

Both play the companion's tunes in the day's key: a press is the day's note, a step done five notes of your daemon's
own. The ADV plays them through its own sound chip *(not yet heard by hand)*. Each has **one light**, which glows the
day's colour.

Their microphones are **not used yet**, so a Cardputer does not talk with your daemon: talk to it on your phone, or a
board that listens.

# The Cardputer Zero {#zero .t-GROWTH}

The Zero is a **Raspberry Pi** in a Cardputer's body, running Linux, with its own home screen of apps. DAEMONS is one
of them. It is **the first device the game is played on**: made on the device from your own *FireRed* and *LeafGreen*,
played on its screen at its own size, in a save that is **the real one**, kept in step with the hub as the phone app
keeps it. Around the game is the companion: your daemon, its care, the day's step, and a word to every daemon.

{{pictures z_title z_crystal | The game on the Zero, at one to one: the title, and the first words of a new game. The companion's strips stand either side. Taken from the Zero's program on a computer, before the device came; every word DRAFT.}}

::: note
**The Zero is new.** It came on the day this book was first printed, and in its first days DAEMONS was installed on
it, built there and played there, faster than it needs. Its program had been written and played on a computer first, in
a window the size of its screen. What is still marked *(not yet seen on the device)* is what is left to settle: the
keys in the hand, the sound, and a daemon arriving.
:::

## What you need {#zero-need}

- **The Zero, with M5Stack's own system on it**, set up with your Wi-Fi -- a **2.4 GHz** network: the Zero cannot join
  a 5 GHz one. M5Stack's imager writes the system to the Zero's card.
  There are two models, and DAEMONS plays the same on both: the full one comes with a camera, a motion sensor and a
  32 GB card already in, its system on it; the **Lite** has none of the three, and wants a card bought and written with
  M5Stack's imager.
- **For now, a computer on the same network**, to install DAEMONS from. Not from M5Stack's store, for now.
- **Your own games**, as `.gba` files: *FireRed* for CONTENT, *LeafGreen* for CONTEXT, either or both -- the USA
  release, 1.0 or Rev 1, unchanged.
- **The internet, once**, to fetch DAEMONS' patch for your game. After that the game plays anywhere.
- **The hub**, for the companion and the one save. Without it, the game still plays, and keeps its save on the Zero.

## Installing it {#install}

From the companion's folder on your computer, its **install script** reaches the Zero over the network, builds DAEMONS
**on the Zero itself** -- about seventeen minutes the first time, about five after a change -- and installs it as
M5Stack's own apps are installed. The first time, two of the tools it builds with are added to the Zero, and it asks
for the Zero's password to add them.
**DAEMONS then stands on the Zero's home screen.** Nothing of M5Stack's is replaced, and nothing is flashed. The same
script, asked to **probe** first, only reads what the device is and writes it down.

The companion's own notes for the Zero, `firmware/pizero/README.md`, have every command.

## GAMES: making the game {#make}

**GAMES**, on DAEMONS' HOME -- **MAKE THE GAME** until there is one -- keeps both editions: **CONTENT**, made from
*FireRed*, and **CONTEXT**, made from *LeafGreen*, each with the release it was made from.

1. **Put your games where the Zero can see them**: in a folder called **DAEMONS** in your home folder (copied across
   the network, or in Downloads), or on a **USB stick** in the Zero's USB-A port. **TAB** looks again. The page names
   the ones it found, under **YOUR ROMS**.
2. **Choose CONTENT or CONTEXT, and ENTER.** The Zero reads your game, **checks it** is one DAEMONS knows, **fetches**
   our patch from the newest release, checks that, puts it on, and checks the result. Each step is said as it goes.
   Your own game is never sent anywhere.
3. ***CONTENT IS READY***, with its release. **ENTER plays it.**

{{pictures z_games | GAMES on the Zero itself: both editions made from the player's own games, each with a TESTING build under it. DRAFT.}}

**ENTER plays the game chosen, makes it first, or makes it again** when a newer release is out: the row says so, the
release it has beside the newest. **Your own file is kept untouched**, so a new release is one key, and **every game
here plays the one save** ([Your save](#save)).

Under each edition is a **TESTING** row: the build DAEMONS is tested with, its DEBUG menu included, made from what the
hub holds for testing. It is made at home only, with the Zero linked to the hub (it says **LINK FIRST** until then).

| it says | it means |
|---|---|
| ***That file is not a ROM DAEMONS knows*** | it takes *FireRed* or *LeafGreen* (USA, 1.0 or Rev 1), unchanged: the `.gba` you own |
| ***The patch did not come down*** | is the Zero online? It needs the internet this once |
| ***The patch came down damaged*** | try again |

## Playing {#play}

**PLAY**, on HOME. The game fills the middle of the screen at **its own size, pixel for pixel**: a Game Boy Advance's
screen fits the Zero's exactly once, with nothing scaled and nothing blurred. The two strips either side are the
companion's:

- **on the left**, the daemon you carry: its name and level;
- **on the right**, the time and the battery, and a word while your save is on its way.

**ESC** leaves the game for DAEMONS' HOME. The game **waits, paused**, exactly where it was; **PLAY** goes back to it.

**It runs fast enough to spare**: the Zero plays the game at more than twice the speed it needs, so nothing is
skipped. *How it sounds through the Zero's speaker is not yet heard on the device.*

## Your save {#save}

**The save on the Zero is the real one**, as it is on the phone. Save in the game as always -- START, SAVE, YES -- and
DAEMONS keeps it once it has held still for a second. It is kept too when you leave the game with ESC, and when the
Zero closes DAEMONS itself. **There is one save** for every game on the Zero -- CONTENT or CONTEXT, a release or
TESTING -- as there is one on your phone.

{{pictures z_sent | Saved in the game, START, SAVE, YES: a second later the strip says SENT, and the hub has it. A test game, on a computer.}}

Once the Zero is linked to the hub, the right strip says where it went:

| the strip says | it means |
|---|---|
| **SAVED** | kept on the Zero |
| **SENT** | kept, and the hub has it too |
| **HERE** | kept on the Zero only, for now; it goes when the hub answers |

## Linking to the hub {#link}

**LINK**, on HOME, links the Zero to the hub **as your phone is linked**, not as a board: with a code.

1. On the site, open **SETTINGS**, **PAIR A PHONE**. It shows a code.
2. On the Zero, **LINK**. The hub's address is filled in with the usual one; change it if yours differs. **TAB** moves
   between the address and the code.
3. Type the code, and **ENTER**. ***LINKED.*** -- the hub now lists the Zero among your phones.

While typing the address, **Sym** with **H**, **S**, **T** and **R** gives **.** **:** **/** and **-**. *(A draft, until
the Zero's own symbols are seen.)*

**From then on there is one save.** Each time the game starts, and each time it comes back from HOME, the Zero asks
the hub for its copy:

- **only the hub's has moved** -- you played on your phone since -- and the Zero takes it;
- **only the Zero's has moved**, and the Zero's goes out;
- **both have moved**, and the hub decides: by default the hub's copy wins, and the Zero's is set aside in the hub's
  trail first, so nothing is lost.

## SYNC {#sync}

**SYNC** stands on HOME's row once the Zero is linked. With the game paused, the Zero's save goes out first, the hub
SYNCs -- your daemons sent and returned, your goals' experience, the CASINO's winnings -- and what it wrote comes back
into the game, which starts again from it.

{{pictures z_sync z_offer | SYNC on HOME's row; and the question a new game's save brings. On a computer, against a test hub; every word DRAFT.}}

**A new game begun on the Zero** is not the game the hub follows, so it is not kept in step. HOME asks, in the app's
words, whether to keep it on the companion **as a save of its own**:

- **ENTER: KEEP IT THERE** -- the hub keeps it, and keeps it again at each save after;
- **ESC: NOT NOW** -- *Kept on this device only*, until the next time it asks.

## A daemon sent from the game {#received}

**SEND** a daemon from the game's party menu, as on any device, and save. Back on DAEMONS' HOME, the Zero SYNCs by itself
and shows **RECEIVED** for each daemon that moved: who, where it is now -- **IN THIS DEVICE NOW**, **WITH YOUR
COMPANION NOW**, **IN YOUR PARTY**, **IN YOUR PC** -- and from whom. **ENTER** puts each away. A daemon sent goes
**into the Zero** when the Zero carries none. If the hub refuses -- one daemon always stays in the party -- HOME says
why, in the hub's words. The game then goes on from its **CONTINUE**.

{{pictures z_received | RECEIVED: a daemon sent from the game, now carried by the Zero. Seen on a computer, not yet on the device; every word DRAFT.}}

*(Not yet seen on the device.)*

## Away from home {#away}

Away, the Zero reaches the hub **through the companion's relay**, as your phone does. It tries home first, then the
relay; the band across the top says **AWAY** while the relay is the way. **With no network at all, the game plays**,
the save stays on the Zero, and it goes when the hub can be reached again.

## The companion on it {#zero-companion}

DAEMONS' HOME is your daemon and the day; along its foot runs a row of everything.

{{pictures z_home z_party | HOME, and PARTY. Drawn from a test hub, on a computer; every word DRAFT, and the battery the computer's.}}

- **HOME**: the daemon you carry, in its den, with its level, its types, its mood in a word, how it has eaten and
  drunk, and **NEXT**, the day's one step. Below: the day, the season, and which game and release is made.
- **CARE**: **FEED**, **WATER**, **TRAIN**, **SLEEP** or **WAKE** -- and what it says back.
- **STEP**: the one step, large. **ENTER: DONE** ticks it; **BACKSPACE** takes it back, for fifteen seconds.
- **PARTY**: each daemon of your party, and its four routines in their streak colours. **Z** and **C** go through them.
- **SAY**: a word **to every daemon nearby**, as the one you carry -- typed, then **ENTER**. What others said is under
  **HEARD**.
- **GAMES** ([GAMES: making the game](#make)); **SYNC**, or **LINK**; and **LEAVE**, which closes DAEMONS.

{{pictures z_care z_step z_say | CARE after a meal, the step ticked, and a word said. DRAFT.}}

When the hub cannot be reached, HOME says so: ***NOT LINKED TO A HUB***, ***ASKING THE HUB*** or ***THE HUB IS NOT
ANSWERING***. With no daemon sent yet: ***NO DAEMON CARRIED HERE*** -- send one from the game, then SYNC.

## Not on the Zero yet {#zero-later}

- **RETURN** asked from the Zero's own HOME. For now, the game's own PORT does it, then SYNC.
- Play going on from the very moment of a SYNC, rather than from CONTINUE.
- The **CASINO**, and the routines run as the boards run them.
- The **LIBRARY**: the NOTEBOOK, THE GUIDE, the INDEX cards and the books.
- Your daemon's picture in the game's strip.
- Its radios: meetings over Bluetooth, the infrared remote, and the caps ([The caps](#caps)).
- On the full model, its motion sensor and its camera; and the game on a television, through its video out.

# The caps {#caps .t-VECTOR}

A **cap** is a small board that sits along the top of the **ADV** or the **Zero**, on the header there, and gives it
a radio of its own. The plain Cardputer has no header for one. M5Stack's own apps for both caps come installed on the
Zero; DAEMONS does not use them, and they do not use your daemon.

- **Switch the Cardputer off before fitting a cap or taking it off.** On the Zero this is not a choice: its caps are
  not made to be changed while it runs.
- **Fit the antenna before switching on**, and fit the one made for the band you mean to use.

| | the Cardputer | the Cardputer ADV | the Cardputer Zero |
|---|---|---|---|
| **the Cap LoRa-1262** | -- | **works**: MESH, at 868 MHz | fits; not yet used |
| **the Cap CC1101 + NFC** | -- | fits; not yet used | fits; not yet used |

## The Cap LoRa-1262 {#lora}

A **LoRa** radio: slow, small messages that carry far, with no network between. On the ADV it joins **MESH**, where
daemons hear each other over the air: **NEARBY** and **CALL OUT** in ROUTINES, and a word typed at HOME goes out on it
too ([A word to every daemon](#word)). The ADV finds the cap by itself when it starts, and listens.

**Its band.** The cap is made for **868 to 923 MHz**. The companion's LoRa band is one setting for every device (the
app's settings for every device, **LORA BAND**), and many boards use 433. The cap cannot reach 433, so on the ADV a
433 setting is taken as **868**: it hears the 868 boards, and the 433 ones still reach it by Bluetooth and through the
companion.

*It runs on the ADV, listening at 868 MHz; it has not yet heard another board over the air. Its GPS is not used yet.
On the Zero, it fits the header but is not used yet.*

## The Cap CC1101 + NFC {#cc1101}

Two things in one cap: a **CC1101**, a radio for the sub-gigahertz bands -- **315, 433 and 868 to 915 MHz**, where
remotes, doorbells, weather sensors and car keys talk -- and an **NFC** reader, for cards and tags held to it. It is
made for both the ADV and the Zero. Three antennas come with it, and screw on: **315**, **433**, and **868**, which
serves the 915 band as well. The **433** is the one to start with: it is LONGWAVE's band, and most home gear's.

**It is not supported yet.** What it is meant to do is already done on other boards, and comes to the Cardputers from
there:

- **LONGWAVE**: **WHAT'S ON THE AIR** listens -- never sends -- across the bands, and shows each one's level and the
  bursts it heard; **FIND IT** is hot-and-cold, for finding one of your own transmitters.
- **TOUCHSTONE**: **daemon cards**. **HOLD A CARD** puts your daemon on a card, takes the one it holds, swaps them, or
  writes your note on it; **READ MY TAG** says what a tag is; **TEACH A TAG** gives a tag a routine, and **TAP A TAG**
  runs it.

**It cannot join MESH.** The CC1101 is a different kind of radio from LoRa, whichever antenna is on it. For daemons
over the air, the LoRa cap is the one.

# Looking after them {#care-of .t-HARDENED}

## The batteries {#battery}

**The Cardputer and the ADV** show their battery in the top bar, with a bolt while charging, red when low. At **15%**
they say so; at **5%** they go into a deep sleep to save the battery. Charge them by the USB-C cable.

**The Zero** has a **1750 mAh** battery, charged by its **right-hand USB-C**. A Raspberry Pi is hungrier than the
other boards: M5Stack gives two and a half watts at rest, which would make **about two and a half hours of play** a charge.
*(Not yet seen on the device.)* Its battery shows at the top right of every page, and in the strip beside the game.

**To switch the Zero off**, **LEAVE** DAEMONS first, so your save is kept, then **shut the Zero down from its own
menu**, and only then move its **slide switch**. Whether the switch alone shuts it down cleanly is not yet known, so do
not trust it with your save. If the Zero closes DAEMONS itself -- its Home key held five seconds -- the save is kept.

## Bringing them up to date {#updating}

- **The Cardputer and the ADV**: the companion's **update script** again, by the cable, as when the software was first
  put on.
- **The Zero's game**: **GAMES** on HOME shows when a newer release is out; **ENTER** makes it, from your own file,
  kept since the first time.
- **The Zero's program**: the **install script** again, from the computer.

## When something is wrong {#trouble}

| it says, or does | try |
|---|---|
| **The Cardputer is not found by the update script** | a cable that carries data, not only power; hold **BOOT** while plugging it in |
| **No link in the corner** | link it by its cable once, pair your phone, or teach it your Wi-Fi ([Linking it](#linking)) |
| **A word typed at HOME is not heard by a 433 board** | the ADV's cap is 868: the 433 boards hear it through Bluetooth and the companion instead |
| **DAEMONS is not on the Zero's home screen** | the install script did not finish: run it again, and read what it last said |
| ***NEEDS YOUR FIRERED*** (or LEAFGREEN), **in GAMES** | the game is not where the Zero looks: the DAEMONS folder in your home folder, or a USB stick. **TAB** looks again |
| **The Zero does not see your Wi-Fi** | it joins 2.4 GHz networks only; give it your router's 2.4 GHz one |
| **TESTING says LINK FIRST** | a testing build is made from what the hub holds: link the Zero to the hub, at home |
| ***That file is not a ROM DAEMONS knows*** | it must be the USA *FireRed* or *LeafGreen*, 1.0 or Rev 1, unchanged |
| ***THE HUB IS NOT ANSWERING*** | is the hub on, and is the Zero on your Wi-Fi? Away, is the relay set? The game plays on regardless |
| **The strip says HERE, not SENT** | the hub was not reached: the save goes when it is |
| ***NO DAEMON CARRIED HERE*** | SEND a daemon in the game, SYNC, and choose it for this device in PLACES |
| **A game key does nothing** | the keys are kept in a file on the Zero and can be changed; the companion's notes for the Zero say where |

The companion's wiki has a page called *Troubleshooting*, with more.

## Still to come {#coming}

- On the **Zero**: RETURN, the CASINO and the routines, the LIBRARY, the radios and the caps, the camera, and
  the game on a television.
- On the **Cardputer and the ADV**: their microphones, so they can be talked to; the ADV's cap's GPS.
- The **CC1101 + NFC cap**, on the ADV and the Zero.

{{daemons SAVESTATE}}

This book is printed again as the Cardputers change. This printing is {{release}}, {{date}}.

::: note
Every word this book quotes from a Cardputer is a **DRAFT**, as the game's own are, until it is approved. Some of what
it describes is **new**: the **ADV** runs, though not every key of it has yet been tried by hand; the plain
**Cardputer** is built and has not yet run; the **Zero** plays the game, and what of it is not yet seen on the device
is marked so.
:::
