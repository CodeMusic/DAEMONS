# Welcome to DAEMONS {#welcome .t-CONTEXT}

DAEMONS is a total conversion of *Pokémon FireRed* and *LeafGreen* for the Game Boy Advance. Machines evolved into
creatures, and this is a game about what happened next. You keep an INDEX, you bind DAEMONS, you run them against
other USERS, and you work your way through eight BENCHMARKS -- and almost everything is written down somewhere.

{{screens hello crystal | The opening, as a new game begins. CRYSTAL CLEAR keeps the lab in your home town.}}

## Two editions, one game {#editions}

The slash in the title is literal. **CONTEXT** and **CONTENT** are two editions built from one source, the way Red
and Blue, and FireRed and LeafGreen, always were.

| | **CONTENT** | **CONTEXT** |
|---|---|---|
| made from | *FireRed* | *LeafGreen* |
| leans toward, early | CONTENT, LOGIC, STRATUM, LEGACY | CONTEXT, LATENT, VECTOR, ENTROPY |
| its year | the **northern** hemisphere's | the **southern** hemisphere's, two seasons on |
| its instrument | the HARP | the FLUTE |
| its INDEX | every entry, in its own words | every entry, in other words |

Both tell the same story in the same towns, and every daemon exists in both. They differ in which daemons you meet,
in what the INDEX says about them, in the year they keep and in what you play. **The type chart is the same,
byte for byte, in both** -- that never changes. And because each edition cannot bind some daemons, finishing the
INDEX takes someone else's game: another player's context, over a link cable.

## A few words you will meet {#words}

DAEMONS renames almost everything. The game never stops to explain its words; this table does, once.

::: two
| you knew | here it is |
|---|---|
| Pokémon | **DAEMON** |
| Pokédex | **THE INDEX** |
| Trainer | **USER** |
| wild | **UNBOUND** |
| catching | **BINDING** |
| Poké Ball | **USERBOX** |
| moves | **ROUTINES** |
| fainted | **HALTED** |
| evolution | **RECOMPILE** |
| run away | **DETACH** |

| you knew | here it is |
|---|---|
| Gym | **BENCHMARK** |
| Badge | **MARK** |
| Elite Four | **THE REVIEW BOARD** |
| Pokémon Center | **CHECKPOINT** |
| Poké Mart | **THE REPO** |
| PC storage | **COLD STORAGE**, the **PORT** |
| Bag | **POOL** |
| TM, HM | **PLUGIN**, **DRIVER** |
| Town Map | **SITEMAP** |
| Prof. Oak | **CRYSTAL CLEAR** |
:::

The [glossary](#glossary) at the back has the rest.

## Before you start {#before}

::: safe
**DAEMONS is a fan project, and no ROM is ever shared.** It is published as small **patches** that you apply to a
*FireRed* or *LeafGreen* ROM you made from **your own cartridge**. Nobody in the project can give you a ROM; please
don't ask anyone else for one.
:::

::: note
**Every word quoted from the game in this manual is a DRAFT**, as the game's own words are until each is approved.
The pictures are real: each game screen was captured from a built ROM, and each daemon is drawn from the build this
manual was made with ({{release}}, against the design bible {{bible}}). The game changes often, so a screen here may be
a release or two behind the one you play.
:::

This manual tells you **how** things work. It never tells you **where** anything is: finding things is the game, and
some places in it are mentioned by nothing at all.


# Ways to play {#ways .t-SIGNAL}

DAEMONS runs anywhere a *FireRed* does, and a few places besides. Pick the way that suits you; the game is the same in
every one, and a save can move between most of them.

| you have | the way to play |
|---|---|
| your own *FireRed* or *LeafGreen* cartridge | [patch your own ROM](#patch), then any of the ways below |
| a computer | [mGBA](#mgba) |
| an iPhone or iPad | [Delta](#delta), or [the one app](#oneapp) (in testing) |
| a GameSir Pocket Taco on an iPhone | [the one app](#controls), with real buttons (in testing) |
| a Game Boy Advance | [a flash cartridge](#gba) |
| a browser, on a network someone runs it on | [the playground](#playground) |
| the source, and a Mac or Linux machine | [build it yourself](#build), the [DEBUG builds](#debug) and the [classic Game Boy build](#classic) |
| a phone, a watch or a board, alongside any of these | [the companion](#companion) |

## Patch your own cartridge {#patch}

A patch is a short list of differences. Applied to the ROM it was made for, it turns that ROM into DAEMONS: *FireRed*
becomes **CONTENT**, *LeafGreen* becomes **CONTEXT**. A patch checks the ROM before it changes anything, so the wrong
one simply refuses -- it cannot harm your file.

::: way
### 1. Back up your cartridge

Any GBA cartridge reader makes a copy of it, a *dump* (a GB Operator, a GBxCart RW, or a Nintendo DS Lite with a
homebrew dumping tool). Save it as a `.gba` file.

### 2. Find the patch that fits it

Each game was printed twice, as **1.0** and **Rev 1**, and a patch fits only the exact ROM it was made from. A patcher
shows your ROM's CRC32 and SHA-1 the moment you open it; they must match one row.

{{patches}}

Other regions, ROMs that are already patched and bad dumps will not match. The full table, with every checksum and the
MD5s too, is `ROM RELEASE/HOW_TO_PATCH.md` in the repository.

### 3. Download it and apply it

Take the newest release from **github.com/CodeMusic/DAEMONS/releases** and download the one `.bps` under **Assets**
that matches your row. Then, in a browser on any computer or phone, open **Rom Patcher JS**
(marcrobledo.com/RomPatcher.js): choose your ROM, then the patch, then **Apply patch**. It runs on your own device and
uploads nothing. Floating IPS, MultiPatch and RetroArch's own patching all work as well.
:::

::: tip
**Keep your clean original.** Every new release is applied to the original, never to a ROM you already patched. Give
the new DAEMONS ROM the same file name as the old one, and your emulator or cartridge finds the same save. Copy your
`.sav` somewhere safe first: releases are built to keep saves working, and a backup costs nothing.
:::

## mGBA, on a computer {#mgba}

::: way
### The emulator DAEMONS is built and tested in

**mGBA** (mgba.io) runs on Windows, macOS and Linux. Open your patched ROM and play. It can also **soft-patch**: put the
`.bps` beside your clean ROM under the same name (`FireRed.gba` and `FireRed.bps`) and mGBA applies it every time it
loads, leaving the ROM untouched.

Its keys, until you change them (Settings, Keyboard): **X** is A, **Z** is B, **Enter** is START, **Backspace** is
SELECT, **A** and **S** are L and R, and the arrows move.
:::

**The clock.** DAEMONS reads a cartridge clock, and mGBA gives it one from your computer's. mGBA keeps that clock in
16 bytes at the end of the save, so its saves are 131,088 bytes rather than 131,072. If the game's date ever looks
wrong, see [Help](#help).

## Delta, on an iPhone or iPad {#delta}

::: way
### Patch in Safari, play in Delta

Delta can't patch by itself. Patch in Safari with Rom Patcher JS, which saves the result to **Files**; then in Delta,
press **+** and import the patched file. Delta keeps its own save for it.
:::

A new game, or a busy moment, can hold a black screen for a few seconds on a phone. Give it time before deciding it has
stopped.

## A real Game Boy Advance {#gba}

::: way
### With a flash cartridge

A flash cartridge -- an EZ-Flash, an EverDrive and the like -- plays the patched ROM on the hardware itself. Copy the
patched `.gba` to its SD card.

- **Save type:** leave it on automatic. DAEMONS saves exactly as *FireRed* does, 128 KB of flash.
- **The clock:** if the cartridge has a clock battery, switch its clock (RTC) **on** for this game in the cartridge's
  own menu, and set the time there. Then, at the terminal in your bedroom, type **TIME**: a **CLOCK** line with today's
  date means the game is reading it. Without a clock the game still plays, and its days follow your play time.
- **Updating:** the save sits beside the ROM on the SD card as its own `.sav` (an EZ-Flash Omega keeps it in `SAVER`),
  matched by **file name**. Copy it off first, then replace the `.gba` with the new one under the same name. The cart
  writes the save to the card when you next boot or reset into its menu, so do that before taking the card out.
:::

## The one app, on an iPhone or iPad {#oneapp}

::: way
### The game and the companion together (in testing)

The companion's own app can hold the game. Give it your own *FireRed* or *LeafGreen* once, from Files: it recognises the
ROM, fetches the matching patch from the newest release, applies it **on the device**, checks the result, and plays it
in a **GAME** tab, with your original kept untouched beside it. A newer release is offered with one tap.

**The game's save is the companion's.** Showing the companion pauses the game; SEND and SYNC write the save, and the game
carries on from it. On an iPad on its side, the game sits on the left and the companion beside it, and a NOTEBOOK page
just filed or the INDEX card of a daemon just met opens next to the game.
:::

{{pictures app-game ipad | The GAME tab before a game is given, on an iPhone; and an iPad on its side, the game beside the companion (the iPad simulator, a made-up save).}}

*Internal and in testing for now: it is built and run on the project's own iPhone and iPads, and is not on the App
Store or TestFlight. A Mac version is planned.* More in [the companion](#companion).

### Buttons on the screen, or in your hands {#controls}

On an iPhone or an iPad the game draws a Game Boy Advance's buttons on the screen: the cross, A and B, L and R, START
and SELECT.

Or clip on a **GameSir Pocket Taco** -- a controller shaped like the lower half of a Game Boy Advance, which plugs into
the iPhone's USB-C. While it is on, the game moves up into the top half of the screen, the half the Taco leaves in view,
and the buttons on the screen hide; take it off and they come back. *In testing: this is built and has not yet been
tried with a Taco in hand, so which of its buttons does what may still change.*

## The playground, in a browser {#playground}

::: way
### The game in a browser, for demos and beta tests

**daemons-playground** plays DAEMONS in a browser from one address: choose an edition (or its DEBUG build), start a new
game or continue from a `.sav`, and play -- with the keyboard on a computer, or buttons on the screen on a phone. Beside
the game, in tabs: a companion of its own for the daemons you SEND, each release's notes, and help.

It is never a public site. Whoever runs it serves the ROMs they built themselves, and it answers only their own
machine, their private network and their tailnet. If someone runs one for you, open the address they give you.
:::

| on a computer | |
|---|---|
| arrows | move |
| **X** / **Z** | A / B |
| **Enter** / **V** | START / SELECT |
| **Q** / **E** | L / R |

On an iPhone, sound may only start inside a tap, so the page puts **TAP TO PLAY** over the game; that tap starts it.
The game keeps its save in the browser, and **a `.sav` can be downloaded** at any time.

**To run one**, with DAEMONS and its releases built on the machine, from the DAEMONS folder:

```
playground/bindPlayground.sh          # the newest release, on port 4740
playground/bindPlayground.sh --build  # this machine's own build instead
```

## The DEBUG builds {#debug}

::: way
### For testing, not for a first play

Each edition has a **testing build**, `daemonsContent_debug.gba` and `daemonsContext_debug.gba`, with a save of its own
so testing never touches a playthrough. A new game starts as a normal one does; its START menu has one more row,
**DEBUG**: *"Testing tools. Not part of the game."*
:::

{{screens debug-page debug-events | DEBUG's first page, and GAME EVENTS: the story's pieces, each given or taken in story order.}}

- **GAME EVENTS** hands the game out a piece at a time, in story order, each row marked **+** when held and **·** when
  not: everything at once, the roster, every daemon, the MARKS, the NOTEBOOK, the books and more.
- **JUMP** reaches a place without playing to it. **ENCOUNTER** sets the season and the weather. **TIME** (the
  watch) forces dawn, day, dusk or night. **SOUND** plays any song or sound. **HEAL** and **MART** do what they say.
- Hold **B** to walk through tall grass without meeting anything.

The testing builds are not published with the releases. Build one yourself (below), or play it in the playground.

## Build it yourself {#build}

From the source, on a Mac or Linux machine. DAEMONS is three repositories joined by links: the design and its tools,
and the two engines, which are kept beside it and never merged in.

```
git clone https://github.com/CodeMusic/DAEMONS.git
cd DAEMONS
./setup.sh                 # the engines beside it, the links, and the agbcc compiler
./bindDaemons.sh           # build CONTENT and open it in mGBA
./bindDaemons.sh context   # CONTEXT
./bindDaemons.sh --debug   # the testing build
```

You need `arm-none-eabi-gcc` (Homebrew's works) and **agbcc**, which `setup.sh` builds. The ROMs come out as
`engineGba/daemonsContent.gba` and `engineGba/daemonsContext.gba`. **A build you make is for you alone** -- it carries
Nintendo's engine, so it is never shared; what the project publishes is patches.

## The classic Game Boy build {#classic}

::: way
### Where DAEMONS began

DAEMONS was first built on the original Game Boy, on *Red* and *Blue*, and moved to the GBA in September 2026. The Game
Boy build still compiles and still plays its opening stretch, the *vertical slice*, in both editions. It is kept as a
reference and **is not updated any more**; the GBA game is the real one.
:::

```
./bindDaemons.sh --classic           # CONTENT on the Game Boy, opened in SameBoy
./bindDaemons.sh context --classic   # CONTEXT
```

It needs [RGBDS](https://rgbds.gbdev.io). Expect fewer daemons, the old greyscale-and-colour look, and none of what the
GBA game has grown since.

## The companion {#companion-way}

Not a way to play the game itself, but a way to take a daemon out of it: your phone, a watch or a small board can
**host** a daemon you SEND from your party, and bring it home again. It works beside every way above that keeps a save
you can reach. It has [a chapter of its own](#companion).


# Getting started {#start .t-GROWTH}

## The buttons {#buttons}

The game opens on its own page about them: *"The buttons, in the order they matter. Names, not places. Check your
bindings."*

{{screen controls | The first page of a new game.}}

| button | what it does |
|---|---|
| **+ Control Pad** | moves you; chooses in menus |
| **A** | confirms, checks things, talks, turns the page of a message |
| **B** | goes back, cancels; in the DEBUG build, held, walks through tall grass |
| **START** | opens the menu |
| **SELECT** | moves things in a list; uses the item you registered |
| **L**, **R** | help, outside battle; **in battle**, L opens the INDEX and R shows PERSPECTIVE |

## A new game {#newgame}

CRYSTAL CLEAR introduces herself and the world. Then she asks a question: *"When these disagree, which of them do you
follow?"* -- **REASON** or **INSTINCT**. Your answer is who you play. Then you choose your name, and your rival's.

{{screens crystal reason bedroom=Your_room | CRYSTAL CLEAR, the question answered, and your room as the game begins.}}

**Your room has a terminal.** Type **TIME** at it and it tells you what clock the game is reading: a **CLOCK** line
with the date when there is a real clock (a cartridge's or an emulator's), and play time when there is not.

**Your first daemon** comes from CRYSTAL CLEAR's lab, one of three, each a different way of learning:

{{daemons LABEL CLUSTER ROVERCUB}}

## The menu {#menu}

**START** opens it, in two columns.

{{screens start-menu usercard | The START menu (this is the testing build, so DEBUG is in it; the game you play has no DEBUG row), and your USER card. Each row of the menu explains itself in the line along the bottom.}}

| | |
|---|---|
| **INDEX** | every daemon you have seen and bound -- [its chapter](#index) |
| **DAEMONS** | your party of up to six, and what each can do outside battle |
| **POOL** | your bag: items, key items, PLUGINS and more, in pockets |
| *your name* | your USER card: your MARKS, the day and the clock |
| **SAVE** | a complete record of your progress |
| **OPTION** | text speed, sound, the battle style, and **FOLLOWER** on or off |
| **HELP** | how to play, and how to do things (L and R open it too) |

## Saving {#saving}

**SAVE** from the START menu writes one complete record. There is one save for each ROM, kept by your emulator or
cartridge beside the ROM. Save often, and back the `.sav` file up before you update to a new release.

## CHECKPOINTS and THE REPO {#checkpoints}

A **CHECKPOINT** restores your daemons, health and state together, free; it is where you return when every daemon you
carry has HALTED. Upstairs in each, someone will tell you about the companion. **THE REPO** sells what you need: items
to repair a daemon, USERBOXES to bind one, and more as you go.

{{screens checkpoint port | A CHECKPOINT, and the PORT, where daemons you are not carrying wait in COLD STORAGE.}}

Your PC is a **PORT**. Booted at a CHECKPOINT or at home, it opens **COLD STORAGE**, where every daemon you bind past
your six goes, in boxes, and your own items' store.

## Getting about {#about-routines}

Some routines work outside battle as well as in it. Taught by a **DRIVER**, they open the way:

| routine | outside battle |
|---|---|
| **PRUNE** | cuts a thin tree back |
| **CRACK** | breaks a cracked rock |
| **DISPLACE** | moves a boulder |
| **TRAVERSE** | crosses water, riding out on a manta |
| **ASCEND** | climbs a waterfall |
| **VERBOSE** | lights a dark cave |
| **GOTO** | takes you to a CHECKPOINT you have already reached -- you come apart into bits and notes and arrive |

And a few items: the **BICYCLE**; the **SITEMAP**, the map of everywhere; **EJECT**, out of a cave; **SUPPRESS**, to
keep unbound daemons away for a while; **GREP**, which finds hidden items nearby.


# The world {#world .t-FLOW}

The world keeps time, gives every day of the week its own note and colour, turns through the seasons of its own
hemisphere, has weather and keeps the real calendar's holidays. Nothing in the game explains any of it -- you notice.

{{screen town | A town by day.}}

## The clock {#clock}

With a clock (an emulator's, or a cartridge's switched on) the game follows the real hour. Without one, play time is
the clock: each part of the day lasts fifteen minutes of play, so an hour of play is a day. Your USER card says which
clock you are on.

| | hours |
|---|---|
| **dawn** | 5 to 7 |
| **day** | 7 to 18 |
| **dusk** | 18 to 20 |
| **night** | 20 to 5 |

The light tints the outdoor maps as the day goes.

{{screens sky-clear=Day sky-dusk=Dusk sky-night=Night | The same road by day, at dusk and at night.}}

## The week {#week}

Every day of the week is its own, Sunday first, and the game carries each one in three places without ever saying
what it means:

- **its name**, when you step outside -- the sign that names the town slides in again: *F · WEDNESDAY · NIGHT*;
- **its note**, C on Sunday up the scale to B on Saturday, which TUNE at your bedroom terminal sounds before its song;
- **its colour**, the rainbow in order from Sunday's red to Saturday's violet, on the trim round every CHECKPOINT's dome.

**What a day means is for the books to suggest, and for you to notice.** The companion's TODAY says it outright, and
each of the two books keeps its part of it -- THE GUIDE the day's virtue over its shadow, THE SUBTLE LAYER its centre,
its word and its note:

{{week}}

A virtue is always said **over** its shadow, never as its cure: a shadow is something to light and balance, not
something to cut out. Your [MARKS](#marks-each) print the same pairs, and on your USER card each of the seven
bands waits in shadow until its virtue lights it. The centres are the body's seven, as THE SUBTLE LAYER sets them out
(the chakras), from the Root up to the Crown.

## The seasons {#seasons}

The seasons repaint the world, and **the two editions keep the two hemispheres' years**: CONTENT the northern and
CONTEXT the southern, two seasons on. So in the same week one player's world is in spring and the other's in autumn,
and while it snows in one, the other is in high summer.

| from | CONTENT, the north | CONTEXT, the south |
|---|---|---|
| 21 March | spring | autumn |
| 21 June | summer | winter |
| 22 September | autumn | spring |
| 21 December | winter | summer |

Without a clock, a season lasts seven hours of play, and a new game begins in CONTENT's summer -- which is CONTEXT's
winter. On many early roads the tall grass changes with the seasons -- one of its daemons belongs to the season and
one to the hour -- so some are met only at a time of year, or a time of day. The INDEX's NATIVE line says when. The
companion keeps your edition's year too, by the real date -- so when your game has a clock, the season on your watch is
the one in your game.

{{screens sky-winter=Winter sky-spring=Spring}}

{{screens sky-clear=Summer sky-autumn=Autumn | One road through CONTENT's year.}}

## The weather {#weather}

The weather follows the season, over the ordinary outdoor maps -- so it follows your edition's hemisphere too. It is
drawn from the date, so two players in the same edition on the same day see the same sky. A spell can begin at any
minute, last from ten minutes to a whole day, and cover one town or the whole region. Most of the time the sky is clear.

{{screens sky-rain=Rain sky-storm=Storm sky-snow=Snow | Spring brings rain and storms; winter, snow.}}

{{screens sky-fog=Fog sky-wind=Wind | Autumn brings fog, and WIND.}}

| season | its weather |
|---|---|
| spring | rain, and storms |
| summer | storms; most days clear |
| autumn | fog, and WIND |
| winter | snow |

The weather reaches into battle too -- see [battles](#weather-battle) -- and some daemons come out only in one. The
INDEX says so.

**Out here, the companion follows the real sky.** Set your city on the companion's site and its watches and boards
wear the weather where you are -- clear, cloudy, fog, rain, snow or a storm -- along with the hour, your edition's
season and the day's holiday. At the [CASINO](#companion-casino) each of them leans the day's luck a little, one way or
the other, and **Why** opens each reason.

## Holidays {#holidays}

The game keeps the real calendar's holidays, under the world's own names: **three a month**, one shared by both
editions, one for CONTENT's northern year and one for CONTEXT's southern -- so midsummer's LONGEST DAY comes in June
in one and in December in the other. Playing on one changes the game a little and never gates it: its own light and
sky, some daemons turning up more on their day, fireworks, and a gift once a year. On two days a year each edition lets
in the other's daemons. A *quiet* day is named and left as it is: no colour, and no fireworks.

**Every month has a colour and a note.** The months run up the scale from January's C, red, to December's B, purple.
The day's banner and your USER card show them, and on the 1st the banner plays the month's note. What you are told on
a holiday is kept in **THE YEAR**, in your NOTEBOOK.

{{holidays}}

Without a clock the year is twenty-eight hours of play, beginning at the north's midsummer, and each holiday lasts one
part of a day -- fifteen minutes. The companion keeps the same days, under their everyday names, and its watches,
boards and CASINO dress for them.

## The SITEMAP {#map}

The **SITEMAP**, in your POOL's key items, is the map of everywhere. Register it to SELECT and it opens with one
press. It keeps the region's shape, so finding your way is unchanged, but it is drawn in the game's own look: paper
and ink, routes like a score, and the sea a shuffle of bits and notes.

{{screen sitemap | The SITEMAP, open on your home town.}}

## Colour is friendship {#colour}

A daemon's colours fill as it comes to trust you: nearly grey, with a hint of its type, at first; half its colour once
it is friendly; the whole of it at the most. People keep their colour. Some trainers' daemons never warm to anyone.

## Places the game never points to {#hidden}

Some places in DAEMONS are mentioned by no sign and no one. Finding them is the game. If you find one, please keep it
out of bug reports, so the next player can find it too.

## Music {#music}

Each town has its key. Four have themes of their own, and each hidden place has a loop of its own.


# Daemons {#daemons .t-CONTENT}

## Binding {#binding}

Walk in tall grass, in caves or on the water and an **UNBOUND** daemon may announce itself. Weaken it, then offer it a
box and see whether it will run there. The boxes climb a ladder of privilege, each binding more surely than the last:

| | |
|---|---|
| **USERBOX** | where everyone starts |
| **ADMINBOX** | better |
| **SUPERBOX** | better again |
| **ROOTBOX** | never fails |

A daemon you bind joins your party of six, or goes to COLD STORAGE when the party is full. Binding a daemon writes it
into the INDEX as **owned**; meeting one writes it as **seen**.

## Your party {#party}

{{screens party sum-info | Your party, and a daemon's first page: its number, name and type, its USER and where you met it.}}

Each daemon has four pages. **L** and **R**, or left and right, turn them:

- **DAEMON INFO** -- its number, name and type, its USER and ID No., its nature, and where you met it.
- **DAEMON SKILLS** -- health, its five statistics, experience, and its ability and what it does.
- **KNOWN ROUTINES** -- its four routines, each with its type and how many times it can run.
- **A fourth page for how it is.** A daemon feels things -- glad, cross, low, calm, afraid -- from what happens to it in
  play. The page shows it as a place on a grid and a line, never as a word: the game never names a feeling, and a
  feeling is never a status.

{{screens sum-skills sum-routines sum-feelings | Its skills, its routines, and how it is: "It goes where you go, as ever."}}

## Routines {#routines}

A daemon knows up to four **ROUTINES**, learned as it grows or taught by a **PLUGIN** (kept in the **TOOLKIT**) or a
**DRIVER**. Each routine has a type, and a small mark beside its name for what it does: strike, raise, lower,
afflict, mend or guard. Every routine also carries a signature of its own in battle -- a few glyphs of bits, and a
three-note figure in its type's key.

## States {#states}

A daemon can be left in one of six states, and items undo them:

| state | what it does | undone by |
|---|---|---|
| **LEAKING** | loses a little health every turn | **PATCH** |
| **CASCADING** | loses more every turn | **PATCH** |
| **SUSPENDED** | does nothing until it resumes | **RESUME** |
| **THROTTLED** | slowed, and sometimes stalls | **PRIORITY** |
| **OVERHEATED** | takes damage, and hits softer | **COOLANT** |
| **HUNG** | does nothing until something intervenes | **PREEMPT** |

**THRASHING** passes when the battle ends. **ROLLBACK** clears every state; **RECOVER** restores health;
**SNAPSHOT** restores both. A daemon whose health runs out has **HALTED**: **RESTART** starts it again with half its
health, **REBOOT** with all of it.

## Growing {#growing}

Battles give a daemon experience; levels make it stronger and teach it routines. At the right moment a daemon
**RECOMPILES** -- it becomes the next thing in its line. Most do it by level; some need an item, some a trade, some
trust, and some an hour of the day.

## The daemon behind you {#follower}

**The daemon at the head of your party walks behind you**, drawn at your own size. Press **A** on it and it tells you
how it is -- how much it trusts you, and how it feels, in a line of its own; it notices the weather, the hour and the
season. It hides on the water and goes into a CHECKPOINT's machine while it is healed. **OPTION** turns it off.

{{screen follower-talk | Talking to the daemon behind you.}}


# Battles and the type chart {#battles .t-LOGIC}

## The battle screen {#battle-screen}

{{screens battle battle-routines | A wild PREEMPT. For the first two seconds of every battle the question gives way to a reminder of L and R; then the routines.}}

| | |
|---|---|
| **ROUTINES** | choose one of your daemon's four |
| **POOL** | use an item |
| **DAEMON** | send out another |
| **DETACH** | get away, from an unbound daemon |
| **L**, in battle | the INDEX entry of the daemon you are facing |
| **R**, held | **PERSPECTIVE**: the same fight, drawn from the other side, for as long as you hold it |

## The seventeen types {#types}

Every daemon has a type, or two, and so does every routine. The types are the vocabulary of thinking machines; each
has a one-line idea that tells you how it behaves.

{{typelist}}

## The chart {#chart}

Read across from the attacking routine's type to the defending daemon's. **2** hits twice as hard, **½** half as hard,
and **0** not at all. A blank is an ordinary hit.

{{typechart | All 111 relations, read from the game's own table. It is the same in both editions.}}

**A daemon of two types** takes both readings, multiplied: twice and twice is four times, twice and half is ordinary,
and a 0 in either is 0. A routine of the daemon's own type hits half as hard again.

## Weather in battle {#weather-battle}

Weather never touches the chart, but each kind lifts its own routines a quarter stronger, and the battle takes its
tint:

| weather | lifts |
|---|---|
| storm | **SIGNAL** |
| fog | **LATENT** |
| WIND | **VECTOR** |

Snow falls as hail.


# BENCHMARKS, MARKS and ROOTS {#marks .t-LEGACY}

## The eight BENCHMARKS {#benchmarks}

Eight towns have a **BENCHMARK**, and a leader who runs it. Each tests one thing, mechanically: its lesson is in how
the fight works, so it cannot simply be out-levelled. Pass it and you earn its **MARK**.

## The MARKS {#marks-each}

There are **eight MARKS**, and each prints a **virtue over its shadow** -- a MARK is a lesson as much as a badge. They
show on your USER card. Each MARK also lets your daemons do more outside battle, and lets daemons you were given obey
you to a higher level.

## ROOTS: what you come to understand {#roots}

The quest has two halves. The MARKS are one. The other is the **understandings**, seven of them, arrived at rather than
won: some of what the game teaches comes quietly and is never announced. Each understanding held shows as a **ROOT**
on your USER card, in its own colour.

**A MARK and its ROOT pair.** Once you hold both, its leader has more to say, and a **union PLUGIN** comes with it --
a routine no one teaches otherwise. When a pair is held, an **insight** may arrive on a later step; and when every pair
is held, a last note.

::: tip
The **STREAM** in your POOL replays every lesson a MARK or a ROOT has opened, as many times as you like.
:::

## THE REVIEW BOARD {#reviewboard}

With eight MARKS the road leads to **THE REVIEW BOARD**, four reviewers in a row, and then the one who holds the
place they guard.


# The INDEX {#index .t-STRATUM}

**THE INDEX** records every daemon you meet. CRYSTAL CLEAR gives it to you early; it starts empty.

{{screen index-toc | The INDEX's contents: seen and owned, by number, by kind, and by where they run.}}

## Every entry, twice {#twice}

Each of the INDEX's entries is written **twice**, once for each edition, and the two disagree: different flat
sentences about the same creature, and for some, different heights and weights, each stated as fact. Nobody in the game
explains it.

{{daemons PING NIBBLE}}

## What an entry holds {#entry}

- its **number**, **name**, **category** and **types**; its height and weight;
- its entry, in your edition's words;
- **NATIVE**: where it lives -- a region, and when it keeps to them, its edition (CONTENT ONLY, CONTEXT ONLY), its
  hours, its seasons and its weather (IN RAIN). NOT IN THE WILD means you will not meet it unbound;
- **FIRST MET** and **BOUND**: where you first saw it, and how it joined you.

In battle, **L** opens the entry of the daemon you are facing.

## OPUS, and the GLOBAL INDEX {#opus}

The INDEX can be opened further. **OPUS**, once you have it, adds a margin to each entry (press SELECT on an entry).
At first the INDEX holds only the region's first 151; later in the story, the **GLOBAL INDEX** takes it past them.


# The NOTEBOOK and CALLOW SCHOOL {#notebook .t-SWARM}

## The NOTEBOOK {#notebook-pages}

The **NOTEBOOK** keeps the pages you find and the pages you write, in sections: school notes, loose pages, lab notes,
letters, the **SONGBOOK**, **THE YEAR** and more. Each page says where it was found, and a page you have not read yet
carries a dot. A few end on a **QR code**: scan it with a phone, and it opens a song.

::: note
This manual shows no NOTEBOOK page: what they say is for you to read in the game.
:::

## The DREAM LOG {#dreams}

After certain moments, at the next dawn, you say *"I had a dream."* -- and the dream is filed in the NOTEBOOK as a
picture with a title, never with an interpretation. Some dreams kept there are other people's.

**ITS DREAMS.** A daemon carried on a watch dreams while it sleeps there. At the next SYNC its dream comes home into
your save, and at the next dawn it is filed under **ITS DREAMS** -- titled, never explained.

## THE LOG {#thelog}

Once you carry THE SUBTLE LAYER, **THE LOG** counts the reads and leans you were given, and which of them came true.
Only the log decides. See [the subtle layer](#subtle).

## CALLOW SCHOOL {#school}

**CALLOW SCHOOL** has seven floors, a **TEXTBOOK**, and an **EXAM** you can leave halfway and come back to. Pass it
and you earn a **DIPLOMA**, which opens doors elsewhere. Your NOTEBOOK keeps your school notes.


# The books {#books .t-LATENT}

DAEMONS has two books to find and read: **THE PROGRAMMER'S GUIDE TO THE HUMAN MIND** and **THE SUBTLE LAYER**. Both
are adapted from the author's own books and rewritten for the game's world, and every word of both is still a draft.
Each stays hidden until you find it. The game never says where, and neither does this manual.

Once your save holds a book, you read it from your POOL's key items, a page at a time -- and the companion's LIBRARY
opens it too, as a book: its cover, its contents, then each page in turn, with READ ALOUD.

**The two books are your two ways from the opening.** At the start CRYSTAL asked which you follow when the two
disagree, [REASON or INSTINCT](#newgame). On the companion either book, once held, can be asked anything -- and **THE
GUIDE answers as REASON would, THE SUBTLE LAYER as INSTINCT would.** Neither is the careful one; they answer
differently, and both are yours.

| | THE GUIDE | THE SUBTLE LAYER |
|----|----------|----------|
| **what it is** | the mind as software, an engineer's manual | a trainer's handbook of the layer under the solid world |
| **in the game** | POOL → key items, a page at a time | the same, with a picture on every page |
| **in the LIBRARY** | its cover, its contents, each page, READ ALOUD | the same, and TWO VOICES |
| **asked** | it answers as REASON would | it answers as INSTINCT would, and asks back |
| **carried** | its margins fill as you come to understand things | you start to notice things, and it gives you its cards |

## THE PROGRAMMER'S GUIDE TO THE HUMAN MIND {#guide}

{{cover guide}}

The mind treated as software, written as an engineer's manual: the brain is the hardware, and thoughts, feelings and
habits are code that can be read, debugged and rewritten. Its tools come from NLP, CBT, mindfulness, hypnotherapy and
journaling, each set out as a way of working on the system, in 28 chapters from *Understanding the Mind as Software*
to *The Path Forward*. Its page on security sets out each day's **virtue over its shadow** -- the same pairs your
MARKS print, and the ones in [the week](#week).

[]{.clear}

### Carrying it: the margins

Reading the GUIDE grants nothing, and it asks nothing of you. But it is not finished. When you come to understand
something out in the world -- one of the seven [ROOTS](#roots) -- a note appears under the chapter it concerns,
indented and in the GUIDE's cyan, as if someone had written it in the margin. Go back to a chapter you have read, and
see what has been added.

### ASK THE GUIDE: REASON

In the companion's LIBRARY, open THE GUIDE and type a question -- or, on a phone, **HOLD TO ASK ALOUD** and say it. On
a T-Watch Ultra, ask it by voice from BOOKS. **It answers as REASON would**: from the page nearest your question, in
its own voice, read aloud if you like. About one answer in three it ends on **the day's virtue over its shadow**.

## THE SUBTLE LAYER {#subtlebook}

{{cover subtle}}

A trainer's handbook: what trainers do with the layer under the solid world, and what they notice when they do it.
It holds the craft and the physics side by side and chooses neither -- reading (the clairs), steering (the psi) and
bonding, what the physics allows, belief and the words that shape it, balancing mind and body, a routine for the week,
and how to stay correctable. Every page has a picture, and in **TWO VOICES** a second, asking voice is printed faint.

**Once you carry it, you start to notice things**, each marked in the book's purple. [The next chapter](#subtle) is
about them. And on the companion it gives you [its cards](#cards).

[]{.clear}

### ASK THE SUBTLE LAYER: INSTINCT

Open it in the LIBRARY and **ASK** -- typed, or held and said aloud on a phone, or by voice from a T-Watch Ultra's
BOOKS. **It answers as INSTINCT would**: one line from the page nearest your question, and then **a question back**,
printed faint, that turns you to what you notice. Now and then the question is set in the day's **centre, word or
note** ([the week](#week)).

**TWO VOICES** is the book's own entry made a way to ask it: *one says a thing, the other asks what it means.* Asked in
TWO VOICES, it answers only in that asking voice, a clarifying question each turn.

### TODAY'S QUESTION, and THE JOURNAL

Once a day the book asks you something of its own, from its routine -- at waking, at rest, before steering -- set in
the day's centre, word and note. What you answer is kept in **THE JOURNAL**, with the day and the centre, as the book
tells a trainer to keep a log. On a T-Watch Ultra you can answer it aloud.

## THE SUBTLE LAYER's cards {#cards}

Carry THE SUBTLE LAYER and the companion gives you its cards: **twenty-two**, numbered 0 to XXI, each on the book's
purple and each with **two faces** -- one for each of your two ways.

| | |
|----|-----------|
| **REASON** | a circuit board under green, and a daemon of machines and learning; a keyword at the top and, under the daemon, a phrase for reason |
| **INSTINCT** | a living net of nodes under gold, and a daemon of the mind; a keyword and a phrase for instinct |

{{pictures cards-reason | The REASON faces of cards 0 to III: BOOTSTRAP, COMPILE, LATENT and GROWTH.}}

{{pictures cards-instinct | The same four cards' INSTINCT faces: FIRST STEP, FOCUS, SUBTEXT and NURTURE. Drawn from the companion's own files; every word DRAFT.}}

A card comes up on either face, and always upright. Now and then one is **SHINY**: its colours turned over, a gold foil
edge, and a glint. There are three ways to draw, and no more:

| | |
|----|-----------|
| **THE DAY'S CARD** | the same all day, and yours alone -- another trainer has their own; it is kept in THE JOURNAL beside the day's answer |
| **DRAW A CARD** | whenever you want one: out and about, or one each with a friend |
| **PAST · PRESENT · FUTURE** | a spread of three, never the same card twice |

**A card is a prompt for noticing, never a prediction.** As with every read, THE LOG decides. In the app the cards are
in THE SUBTLE LAYER's book, above TODAY'S QUESTION; on the watches, in BOOKS.

::: note
**Where the answers come from.** Every answer is drawn from the book's own pages. A phone on its own answers with the
page's own sentence; with the companion's hub and its AI board, the hub can put it in the book's voice. The books are
asked on the companion only -- the game's copies are for reading. *All of this is new: built, and still being tried on
the watches.*
:::

## THE HERMETIC LAYER, a rumour {#rumour}

::: rumour
Trainers tell of a third book. Nobody who wrote this manual has held it, and the game will not say whether it is real.

They call it **THE HERMETIC LAYER**, and they say it is a grimoire: not a guide and not a handbook but a book of
workings, which does what the other two only describe and bends rules the rest of the game keeps. Some say the GUIDE's
reason and THE SUBTLE LAYER's noticing were only ever its two halves. **Some say it finds only those who have read the
other two. It is said to keep an hour of its own.** It is said to open with a warning, and that some who read it to
the end went a little mad. Its author is said to have made hats. Some say he went mad; he says he went through.
:::

### Where the story comes from

The rumour borrows from things that are true.

- **The Hermetica.** Greek writings from Roman Egypt, of the first centuries AD, set down under the name of **Hermes
  Trismegistus**, "thrice-great Hermes": the Greek messenger god joined to Thoth, Egypt's god of writing and wisdom.
  Renaissance Florence took them for older than Moses -- Marsilio Ficino translated them for Cosimo de' Medici in
  1463 -- until Isaac Casaubon dated them in 1614. Their name is still on the alchemists' airtight seal: *hermetic*.
- **The Emerald Tablet.** A few lines of alchemy, said to have been carved by Hermes himself on a slab of emerald,
  first known in Arabic and later in Latin. Isaac Newton translated it. Its best-known line comes down to four words:
  **as above, so below** -- what runs in the small runs like what runs in the great.
- **Grimoires.** The word is the old French for *grammar*: a book of spells was a book of how words go together.
  *Glamour* comes from *grammar* too, by way of the Scots *gramarye*, magic learned from books.
- **Mercury, and the hatters.** For the alchemists, mercury -- the metal that runs like water, named for Hermes' Roman
  self -- was the go-between, the spirit of change in every working. Felt hatters of the 1700s and 1800s set their fur
  with a mercury compound and breathed its vapour for years; it shook their hands and their nerves, and "mad as a
  hatter" was said of them before Lewis Carroll ever wrote his Hatter.
- **The witching hour.** Folk belief kept one hour of the night as the one when the boundary is thinnest and witches
  and spirits are most abroad -- Hamlet's "very witching time of night". The tellers never agreed which hour.

If the book is real, the game will not say so, and neither will this manual.

# The subtle layer, in play {#subtle .t-CONTEXT}

Carry THE SUBTLE LAYER and the game shows you small things it never showed before, each marked in the book's
**purple**. Not every one lands. The NOTEBOOK's **THE LOG** keeps the count of what you were told and what came true,
and only the log decides.

## The daemon notices first {#notice}

Now and then the daemon behind you stops, turns, and a **purple ripple** rises from it, with a glint where it looks:
something is there that you have not found yet. Press A on it, and what it says comes in purple.

{{screens notice notice-line | The ripple, and the line that follows it.}}

## Reads {#reads}

As you arrive somewhere, a read may come to you: **"A read:"** and a line -- someone close by, rain before long. Some
reads are about nothing, worded the same. When the thing it named happens, THE LOG marks the read as landed.

## Leans {#leans}

In battle, a lean may stand where *"What will ... do?"* stood: what the other side is about to do. A lean is right
more often as your reading grows, and never always.

{{screens read lean | A read on arrival, and a lean in battle.}}

## Words under words {#under}

And now and then there is a faint purple line beneath what someone says: a few words they did not say aloud.

{{screen under | Words under words.}}

## Out here too {#out-here}

Once your save holds the book, the companion's watches notice too: the daemon on the face stops and turns, a purple
**"A read:"** comes with a soft tap, and at the CASINO's reels, sometimes, **"A lean:"** while they turn. The companion
judges each by what happens after and keeps the count; it never says a read was right before it lands. There too the
book can be asked, asks its question of the day, and draws [its cards](#cards).

{{pictures watch | On a watch: the daemon notices first, two reads, and a lean at the reels. A mock-up drawn from the watch's own firmware, not a photograph; every word DRAFT.}}


# PLAY: the HARP and the FLUTE {#play .t-ENTROPY}

Each edition has an instrument: **the HARP in CONTENT, the FLUTE in CONTEXT.** You are given it in the course of the
story. Take it out and a **KEY WHEEL** of twelve keys opens; choose one, and it folds into a **STAFF**.

{{screens keywheel songbook-write | The KEY WHEEL, and a song written into the SONGBOOK as it is learned (CONTEXT's FLUTE).}}

| | |
|---|---|
| the notes of the scale, one to seven | **DOWN, LEFT, UP, RIGHT, B, A, SELECT** |
| an octave up, or down | hold **R**, or **L** |
| put it away | **START** |

Every note has its own colour -- C red, D orange, E yellow, F green, G blue, A indigo, B violet -- and stays bright in
any light.

## Seven songs {#songs}

**Seven songs** are heard somewhere in the world. Play one back, in its key, and it is learned, and each does
something of its own. **Some things in the world listen** -- and to them the right notes in the wrong key are not
quite the same tune. What you learn is written in the **SONGBOOK**, in the notes' colours.

The companion has your instrument too: once the game has given it to you, its SONGBOOK lets you play it by touch, and
it listens for your songs as the game does.


# The GAME CORNER and the CASINO {#casino .t-EMERGENT}

## The GAME CORNER {#gamecorner}

The GAME CORNER's slot machines play with the daemons you have **seen**: as your INDEX fills, new ones come to the
reels. A coin and the season's piece turn with them, and on a holiday the reels wear its hats. Luck comes from the
game's own day -- the holiday, the sky, the hour and the season. Coins are kept in your **TOKEN CASE**.

{{screens slot-ask slots | A slot machine, and its reels.}}

## The CASINO {#companion-casino}

The companion has a CASINO of its own, on the phone, the site, the Tab5 and every board: three reels of your own party.
**Its coins are your game's money**: it starts from what your save holds, and the next SYNC writes what was won or
lost into the save -- never below nothing and never past 999999. Its odds move with the day, between 90 and 100 back
for every 100 bet, and **THE HOUSE** tells you today's odds and why.


# The companion {#companion .t-VECTOR}

**Your daemons can leave the game.** **daemons-companion** lets your phone, a watch or a small board **host** a daemon
from your party. You feed it, give it a drink, train it and put it to bed; you can talk with it; tell it what you want
to get done and it turns that into **one next step**. As you get things done it thrives -- and it comes home to your
save with what it learned.

Everything runs **on your own machines**: a local server, no accounts, no hosting. It reads a DAEMONS save -- a
**copy** of yours -- and never needs a ROM.

## SEND, AWAY and home {#send}

1. **Point the companion at a copy of your save** and SYNC once. From then on, a party daemon's menu in the game offers
   **SEND**.
2. **SEND** a daemon: the game saves, the companion reads the save and marks it **AWAY**, and a device of yours hosts it.
   With more than one device, each can host a different daemon.
3. **Bring it home** the same way, reversed. It comes back with the friendship it built -- and, if it crossed the line
   while it was out there, recompiled: the companion applies the game's own rules, and the game finishes the change.

{{screens party-send send-ask | SEND, from a daemon's menu in the party.}}

An AWAY daemon is drawn washed out in your party, the PORT and its summary, so it is never lost. It can't battle, be
traded or be released while it is away, and if the companion can ever not be reached, the game can call it home on its
own. While it is away, the people who tend daemons between battles sometimes hear how it is doing -- well, fine or
quiet, never worse. The companion calls these **SOUNDINGS**.

::: safe
**Never point the companion at the save you play from while the game is running.** SYNC writes the save, so it must
never write one the game is about to write over. Every SYNC makes a backup first.
:::

## Where a daemon can live {#hosts}

| | |
|----|-----------|
| **your phone** | the companion's app, on an iPhone or iPad, with a **home-screen widget** of its own: DRINK, FEED, TRAIN and, at bedtime, SLEEP |
| **a browser** | the companion's site, on the computer that runs it -- the same screens as the app |
| **the one app** | the game and the companion together on an iPhone or iPad ([above](#oneapp)) |
| **a watch** | the LilyGO **T-Watch S3**, and the bigger **T-Watch Ultra**, which knows when you sleep and walk, wakes you gently, reads you the books and answers when you ask them, draws THE SUBTLE LAYER's cards, and takes a card to its NFC |
| **a board** | most LilyGO and M5Stack boards: the T-Embed family, the T-Deck, the T-Display-S3 Pro and AMOLED, the M5StickS3 and StickC-Plus, the CoreS3, M5GO, Fire, Dial and Cardputer -- the daemon drawn as the game draws it, its routines with it |
| **a control center** | the M5Stack **Tab5** |
| **your home** | an ESP32-S3-BOX-3 running Home Assistant's voice assistant can wear the daemon as its face |
| **a hub that never sleeps** | a small Linux board (an M5Stack CoreMP135) can be the companion's server; with an AI board stacked on it, it talks as your daemon, tells its dreams, and answers as THE GUIDE and THE SUBTLE LAYER once you have found them |

{{pictures widget | The daemon on an iPhone's home screen: the widget, drawn from its real views, before and after FEED, small, and with no daemon chosen.}}

## What it shows of your game {#tabs}

The app, the site and the Tab5 share six tabs, and **show only what your save has already reached** -- a MARK not yet
earned, a place not yet found or a book not yet in your hands shows as *not yet*, and nothing more.

| | |
|----|-----------|
| **TODAY** | the day -- its note, its word, its virtue over its shadow, its centre and your edition's season ([the week](#week)) -- **THE ONE THING**, the next step, your daemon's care, and your game: where you saved, your MARKS, your money |
| **DAEMON** | yours and its care, your party as the game draws it, the **INDEX** with each daemon's NATIVE line, **SOUNDINGS**, **DREAMS** and, once the book is held, **READS** |
| **GOALS** | one goal, its steps and milestones, and walking |
| **LIBRARY** | **THE PLAYER'S MANUAL** -- this book, kept on your phone -- CALLOW SCHOOL and your DIPLOMA, THE GUIDE and THE SUBTLE LAYER once found (each to read and to [ask](#books), and THE SUBTLE LAYER's [cards](#cards)), the NOTEBOOK, the SONGBOOK with your instrument, and STREAM's lessons |
| **YOU** | you as the game draws you, your MARKS and ROOTS, the region maps, the story so far, and **THE ROAD AHEAD** -- the next step, and never anything past it |
| **PLACES** | your devices, which daemon each hosts, and your home |

## Nights and dreams {#nights}

A watch keeps the night: tuck the daemon in (CARE, SLEEP), or on the T-Watch Ultra just sleep, and it feels the
stillness. In the morning your daemon has had a dream -- deep, quiet or restless -- read aloud if you like and kept in
a journal. At the next SYNC the last dream goes home into your save, for the game's **ITS DREAMS**. A good week shows on
the daemon, subtly.

## Running it {#running}

On the computer that keeps your save copy, with Node 24, from the companion's folder:

```
./bindCompanion.sh          # the server, then the site in your browser
./bindCompanion.sh phone    # build the app onto a plugged-in iPhone
./bindCompanion.sh always   # keep the server running, and the Mac awake on power
```

Then pair your phone from the site, add the widget, and SEND. The boards are flashed with `updateCompanion.sh` and
linked over their USB cable with `linkCompanion.sh`. The companion's own wiki has every step, every board and every
setting: **github.com/CodeMusic/daemons-companion/wiki**.


# Help {#help .t-FROZEN}

## Something went wrong {#trouble}

| what you see | what to do |
|---|---|
| *Source checksum mismatch*, or *wrong input file* | your ROM is not the version that patch was made for: try the other patch for your game (1.0 or Rev 1) |
| the title says FIRERED or LEAFGREEN | the patch was not applied: open the **patched** file, or check that a soft-patch's two names match |
| a white screen, or it will not start | usually a bad dump: dump the cartridge again |
| a long black screen at the start of a new game | wait a few seconds; a phone is slower than a computer |
| the date in the game is decades out (mGBA) | mGBA's clock in the save was never set. Back up the `.sav`, cut it to its first 131,072 bytes, and mGBA starts the clock again from your computer's |
| the flash cart does not read an mGBA save | cut it to exactly 131,072 bytes (`head -c 131072 in.sav > out.sav`); back up both copies first |
| the days do not follow the real date | no clock is being read: switch the cartridge's RTC on, and check with **TIME** at your bedroom's terminal |
| my old *FireRed* save does not work | it is not meant to: start a new game, under the DAEMONS ROM's own name |

## Updating to a new release {#updating}

1. Copy your `.sav` somewhere safe.
2. Download the new patch for your ROM, and apply it to your **clean original** -- never to a ROM you already patched.
3. Give the result the **same file name** as before, so your emulator or cartridge finds the same save.

## Reporting a bug {#bugs}

Open an issue at **github.com/CodeMusic/DAEMONS/issues** and say which release you are playing (it is in the release's
name, like `{{release}}`), which edition, and how you play it. Please leave out where hidden things are.


# Glossary {#glossary .t-OPAQUE}

::: {.two .gloss}
**ADMINBOX, SUPERBOX, ROOTBOX** -- better boxes for binding; a ROOTBOX never fails.

**AWAY** -- a daemon you SENT to the companion.

**BENCHMARK** -- a town's test, and its leader. Pass it for a MARK.

**BINDING** -- catching an UNBOUND daemon in a box.

**CENTRE** -- the day's place in the body, in THE SUBTLE LAYER: the Root up to the Crown.

**CHECKPOINT** -- where your daemons are restored, free.

**COLD STORAGE** -- where daemons wait past your six, through a PORT.

**CRYSTAL CLEAR** -- who keeps the lab in your home town.

**DETACH** -- to get away from a battle with an unbound daemon.

**DRIVER** -- teaches a routine that works outside battle too.

**GOTO** -- to a CHECKPOINT you have reached, in a flash of bits.

**HALTED** -- out of health. RESTART or REBOOT it, or visit a CHECKPOINT.

**HEARSAY** -- what people say about the people you meet.

**INDEX** -- the record of every daemon you meet.

**INSTINCT** -- one of your two ways; THE SUBTLE LAYER answers as it would.

**KEY WHEEL** -- where your instrument's key is chosen.

**MARK** -- a BENCHMARK's prize: a virtue over its shadow.

**NATIVE** -- where and when a daemon lives, in its INDEX entry.

**NOTEBOOK** -- the pages you find and write.

**OPUS** -- margins for the INDEX.

**PERSPECTIVE** -- R, held, in battle.

**PLUGIN** -- teaches a routine; kept in the TOOLKIT.

**POOL** -- your bag.

**PORT** -- a PC.

**REASON** -- the other of your two ways; THE GUIDE answers as it would.

**RECOMPILE** -- what a daemon does when it becomes the next in its line.

**ROLL CALL** -- finds trainers who want a rematch.

**ROOT** -- an understanding you hold.

**ROUTINE** -- a move.

**SEND** -- out of the party, to the companion.

**SHADOW** -- what a virtue is said over: something to light and balance, never to cure.

**SITEMAP** -- the map of everywhere.

**SONGBOOK** -- the songs you have learned.

**STREAM** -- lessons, replayed.

**SUPPRESS** -- keeps unbound daemons away for a while.

**THE DAY'S CARD** -- THE SUBTLE LAYER's card for today, on the companion.

**THE REPO** -- the shop.

**THE REVIEW BOARD** -- the last four, and the one after them.

**TOKEN CASE** -- holds the GAME CORNER's coins.

**TRAP TABLE** -- holds what you grow and pick.

**TWO VOICES** -- THE SUBTLE LAYER asked in its asking voice.

**UNBOUND** -- wild.

**USER** -- a trainer: you, and everyone you fight.

**USERBOX** -- the first box for binding.
:::


# About this manual {#colophon .t-HARDENED}

This manual describes **{{release}}**, built against the design bible **{{bible}}** ({{date}}). It is made by
`tools/manual.py` from `docs/manual/` in the DAEMONS repository, and printed again with each release: the daemons,
their INDEX entries, the types, the chart, the week, the holidays and the patches are read from the build itself, and
the game screens are
frames captured from built ROMs in the project's test emulator. Every word quoted from the game is a draft.

**DAEMONS is a fan project**, unaffiliated with and unendorsed by Nintendo, Creatures Inc. or GAME FREAK Inc. Pokémon
is their trademark. It is built on **pret**'s decompilations of *FireRed* (pokefirered) and *Red* (pokered), and would
not exist without them. No ROM, and nothing of Nintendo's, is distributed: the project publishes patches for your own
cartridge's game.

| | |
|---|---|
| the game | github.com/CodeMusic/DAEMONS |
| its engine | github.com/CodeMusic/pokefirered-daemons |
| the companion | github.com/CodeMusic/daemons-companion |
| the playground | github.com/CodeMusic/daemons-playground |
