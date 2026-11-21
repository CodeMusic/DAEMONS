# The Kode Dot {#kodedot .t-CONTEXT}

A daemon you **SEND** out of your game lives on the companion: the app on your phone, the site at home, and any device
you give it. This book is about one of those devices, **the Kode Dot**: Kode's pocket maker device, a small device with
a bright screen, and more radios and senses in it than any other device the companion knows.

It is the device that holds **every routine in one pocket**. The routines are a device's radios in the game's words,
each with a colour of its own, and the Dot has all five:

| the routine | the radio | on the Dot |
|---|---|---|
| **FLARE** | infrared, as a TV remote speaks | two emitters and a receiver |
| **WHISPER** | Bluetooth | Bluetooth LE |
| **TOUCHSTONE** | NFC: cards, stickers and phones held close | an NFC reader |
| **LODESTONE** | **125 kHz**: the older tags of key fobs and door cards | a 125 kHz reader, which no other device of the companion has |
| **UPLINK** | Wi-Fi | Wi-Fi on 2.4 and 5 GHz |

And around them: a screen that answers to touch, a pad and two buttons, a light that glows a routine's colour, a
motor that **taps** your hand, a speaker and a microphone, a compass, a motion sensor, and a battery.

{{daemons ANODE}}

::: note
**The Dot is not here yet.** Kode ships it in December 2026, and this book was first printed before it came. Everything
in it was seen in **Kode's own simulator**, which runs the real DAEMONS program on a model of the Dot's chips -- its
screen, its buttons, its light, its Wi-Fi -- but has **no NFC, no 125 kHz and no infrared**. What is not yet seen on
the device is marked *(not yet seen on the device)*.
:::

::: note
**The rest of the companion** -- the app, its tabs, the hub at home -- is in **THE COMPANION**. How to play the game is
in **THE PLAYER'S MANUAL**. Both stand on the LIBRARY's MANUALS shelf, beside this one.
:::

## What you need {#need}

- **A Kode Dot.** It comes with Kode's own launcher, **kodeOS**, and keeps it: DAEMONS is installed as **one of its
  apps**, beside Kode's own. Nothing of Kode's is replaced.
- **The companion**, with **the hub** at home: the Dot talks to it over your Wi-Fi.
- **A daemon to carry.** In the game, choose **SEND** in a daemon's menu and save; then **SYNC** in the app.
- **For now, a computer** with the Dot's USB cable, to install DAEMONS and tell it where the companion is. Not from
  Kode's store, for now.

## How it runs {#how}

Kode's launcher, **kodeOS**, is what the Dot starts in. An app on the Dot is a **whole program of its own**: open
DAEMONS, and while it runs, kodeOS does not. Leave it, and the Dot starts again into kodeOS. So the Dot opens on Kode's
launcher, with DAEMONS one tap away, and **any restart goes back to the launcher** -- which is why DAEMONS keeps
everything that matters as it goes ([The den](#den)).

**Wi-Fi comes with it.** The network kodeOS has joined is the one DAEMONS uses, so join your Wi-Fi in kodeOS's own
settings first.

# Setting it up {#setup .t-GROWTH}

## Installing it {#install}

From a clone of Kode's **KodeOS** on your computer, its **kcli** tool installs an app over the cable:

```
python KodeOS/tools/kcli.py -p PORT install daemons.bin
```

**PORT** is the Dot's cable on your computer. **daemons.bin** is DAEMONS for the Dot, made from the companion's own
folder for it, `firmware/kodedot/`; its notes, `firmware/kodedot/README.md`, have every command. When the install is
done, **DAEMONS stands in kodeOS's Apps**.

*(Not yet seen on the device: in the simulator it installs the same way.)*

## Telling it where the companion is {#address}

The first time it opens, DAEMONS does not know where your companion is, and says so:

{{pictures den_none | No companion yet: the den waits, and says how to give it one. In the simulator; every word DRAFT.}}

Tell it **once, over its cable**, with DAEMONS open: the companion's address is the computer that runs the hub, on
port **4730**.

```
python KodeOS/tools/kcli.py -p PORT cmd 'function name="server" arg="http://HOST:4730"'
```

**HOST** is that computer's name or address on your network. The Dot keeps it in kodeOS's settings, so it is asked for
once, and goes looking at once.

**At home, the Dot needs no key.** It is a board on the companion's door for devices, known by its own name --
**kode-dot-** and the last six characters of its chip's address -- and the companion finds it a daemon to carry: one you
have sent that no other device is carrying. **PLACES**, in the app, chooses another; the Dot is listed there as a
**Kode Dot**.

*(Not yet seen on the device: in the simulator the address is typed at its console, which is the same line.)*

# The buttons {#buttons .t-FLOW}

The Dot has a **pad** of four directions, and two buttons, **TOP** and **BOTTOM**. Its screen answers to a **tap** too.

| to | press |
|---|---|
| **move** | the pad: **up** and **down**. In the den, **left** and **right** move along the cares as well |
| **choose, open, run** | **TOP**, or tap the row |
| **back** | **BOTTOM** |
| **home to kodeOS** | **BOTTOM** in the den; or **BOTTOM held three seconds**, from anywhere |

**Every move taps your hand**, a small tick from the Dot's motor, and **the light glows** in the colour of the routine
you are on.

The foot of each page says what TOP and BOTTOM do there: *TOP: open*, *BOTTOM: back*.

**If DAEMONS ever does not start**, hold **BOTTOM** and **left** together for about a second: the Dot starts again into
kodeOS.

# The den {#den .t-LEGACY}

**DAEMONS opens on your daemon, in its den.**

{{pictures den den_fed | The den: the day and its virtue over its shadow, the daemon as the companion draws it, its name and level, its mood and how it has eaten and drunk today. Then FEED, and its word back. A synthetic save, in the simulator; every word DRAFT.}}

- **At the top, the day**: its name, and its **virtue over its shadow**, in the day's colour -- the same day as on your
  phone.
- **Your daemon**, drawn by the companion, **three times its size**, pixel for pixel. When it changes -- it grows, or
  the companion draws it anew -- the Dot fetches the new picture.
- **Its name and level**, and under them **its mood in a word**, then **fed** and **drank**: how many of the day's
  meals and drinks it has had.
- **NEXT**: the day's one step, when there is one.
- **Its word back**, after a care.
- **The cares**: **DRINK**, **FEED**, **TRAIN** and **SLEEP**. While it sleeps, **WAKE** stands in SLEEP's place.
- **ROUTINES**, under them ([Routines](#routines)).
- **The foot** says how it stands with the companion ([What the foot says](#foot)).

## Care {#care}

**Move to a care and press TOP**, or tap it. The den **answers at once** -- the count goes up, its word comes back --
and the companion is told after, so **the Dot never waits on the network**.

{{pictures den_asleep | SLEEP: "Goodnight.", its mood asleep, and WAKE where SLEEP was. DRAFT.}}

**A care is never lost.** Each is **kept on the Dot, in order**, until the companion takes it. Go home to kodeOS, let the
battery run down, walk out of your Wi-Fi: the cares wait, and go when the companion can be reached, oldest first. The
Dot keeps **sixteen**; past that, the oldest gives way.

{{diagram care | A care's way home. Drawn at once on the Dot, kept there in order, sent when the companion answers; the companion's word and the den come back.}}

**The Dot asks the companion again every thirty seconds**, and whenever a care has gone, so the den stays as the
companion has it: a meal given on your phone shows on the Dot too.

## What the foot says {#foot}

| the foot says | it means |
|---|---|
| **HOME** | the companion answered: what you see is what it has |
| **LOOKING FOR THE COMPANION** | asking, just now -- when DAEMONS opens, or when it is told a new address |
| **NO COMPANION SET** | it has not been told where the companion is ([Telling it where the companion is](#address)) |
| **NO NETWORK** | the Dot is not on a Wi-Fi: join one in kodeOS's settings |
| **THE COMPANION IS NOT ANSWERING** | on a Wi-Fi, but the companion did not answer: is the hub on, and is the address right? |
| **THE COMPANION SAID NO** | the companion answered, and refused |
| **THE COMPANION CANNOT READ THIS DOT** | it answered with something the Dot could not read: perhaps a companion of another version |

Whatever it says, **the den still works**: cares are drawn and kept, and go when the companion answers.

When the companion has no daemon for the Dot, the den says ***No daemon here*** -- choose one for the Dot in the app's
**PLACES**. The cares are hidden until it has one; **ROUTINES** stays.

# Routines {#routines .t-SIGNAL}

**ROUTINES**, under the cares, lists the five, each in its colour, with its radio beside its name. **TOP** opens one;
inside, its routines are listed, and **TOP** runs one.

{{pictures routines routines_lode lodestone | ROUTINES; LODESTONE chosen, the light amber; and LODESTONE's own list. In the simulator; every word DRAFT.}}

A routine is **your daemon's**: it runs in its name. **BOTTOM** goes back a page, and from ROUTINES back to the den.

## LODESTONE: 125 kHz {#lodestone}

A **lodestone** is a stone that is a magnet of itself. **125 kHz tags** are the older kind: the fob on a key ring that
opens a door, the card for a building or a gym. They speak by **magnetic pull** rather than radio -- the reader's
field wakes the tag, and the tag answers by tugging at it -- so the routine that reads them is named for the stone.
No other device of the companion has one.

### READ MY TAG {#read}

**Hold your tag to the Dot, and press TOP.** The Dot listens for **five seconds**, and shows what it
heard:

{{pictures read_listen read_none | Listening; and nothing heard -- the simulator has no reader, so it hears nothing, as it should. DRAFT.}}

- **A tag heard**: its kind, and **its number**, large, on the screen. ***Shown here only, never kept.***
- ***No tag heard.*** -- move the tag about, or closer, and press **TOP** again.
- ***The reader is busy*** or ***would not start*** -- wait a moment, and **TOP** again.

**The number is shown on the screen and nowhere else.** It is never written to the Dot's log, never kept, and never
sent to the companion, the phone or the hub.

**What it reads, for now: EM4100 tags**, the commonest kind -- a plain number and nothing else. Other kinds of 125 kHz
tag come later, once the Dot has heard the ones you carry.

*(Not yet seen on the device: the simulator has no reader.)*

### Only your own tags {#own}

**LODESTONE is for your own tags**: the fob you were given for your own door, the card that is yours. It reads them so
that one Dot can stand for all of them, as each fob does for itself. It does **not** read tags that are not yours, it
never guesses or steps through numbers at a reader, and it never touches the secure kind -- bank cards, passports,
anything that keeps a secret -- which a 125 kHz reader cannot reach in any case.

## The other four {#others}

**FLARE**, **WHISPER**, **TOUCHSTONE** and **UPLINK** stand in ROUTINES, each in its colour, and say ***Nothing here
yet.*** Their routines come from the companion's other devices, where they already run, once the Dot has come and its
radios can be tried by hand:

| the routine | what it will do on the Dot |
|---|---|
| **FLARE** | your **remotes**: teach the Dot a button of a remote you own, and press it from the Dot -- power, volume, the rest |
| **WHISPER** | your **phone**, over Bluetooth. Pair it in **kodeOS's own settings** first: an app on the Dot cannot make a new pairing, but uses the ones kodeOS has made |
| **TOUCHSTONE** | **daemon cards**: put your daemon on a card or a sticker, take one from it, read what a tag is, and give a tag a routine to run when it is tapped |
| **UPLINK** | your **Wi-Fi**: the networks in range, and the one list of networks every device of yours shares |

# Looking after it {#care-of .t-HARDENED}

## The battery {#battery}

The Dot has a **1000 mAh** battery, charged by its cable. How long DAEMONS runs on a charge is *(not yet
seen on the device)*.

## Bringing it up to date {#updating}

**Install it again**, the same way, with the newer **daemons.bin** ([Installing it](#install)). The companion's address
and the cares waiting are kept in kodeOS's settings, and should stay *(not yet seen on the device)*.

## When something is wrong {#trouble}

| it says, or does | try |
|---|---|
| **DAEMONS is not in kodeOS's Apps** | the install did not finish: run it again, and read what **kcli** last said |
| **DAEMONS does not start** | hold **BOTTOM** and **left** together about a second: the Dot starts again into kodeOS. Then install it again |
| **NO COMPANION SET** | give it the companion's address, over its cable ([Telling it where the companion is](#address)) |
| **NO NETWORK** | join your Wi-Fi in kodeOS's own settings, then open DAEMONS again |
| **THE COMPANION IS NOT ANSWERING** | is the hub on, and on the same network? Is the address the right computer, on port 4730? Cares wait meanwhile |
| ***No daemon here*** | SEND a daemon in the game, SYNC, and choose it for the Dot in **PLACES** |
| ***No tag heard.*** | hold the tag close, and move it slowly over the Dot; a tag that is not EM4100 is not read yet |
| **The den shows an old picture** | it is fetched again when the daemon changes; open DAEMONS again to ask at once |

The companion's wiki has a page called *Troubleshooting*, with more.

## Still to come {#coming}

- **LODESTONE**: **KEEP A TAG** -- read one of your tags and keep it on the Dot, under a name; **MY TAGS** -- the kept
  tags, and the Dot standing in for one, held to your own reader; **COPY TO A BLANK** -- write a kept tag to a blank
  card you own. **A kept tag never leaves the Dot**: not to the companion, the phone, the hub or your save. Forgetting
  it on the Dot is the end of it.
- **FLARE**, **WHISPER**, **TOUCHSTONE** and **UPLINK**, as above.
- **The den kept on the Dot**, so it opens on your daemon at once, before the companion answers; its face as it feels,
  and its den drawn in its type.
- **Away from home**, through the companion's relay, as the phone reaches it.
- **The companion's address chosen on the Dot**, rather than over the cable.
- And what only the Dot has together, for you to choose: **a compass**, so your daemon can point the way home; **steps**,
  its walk with you; **its heartbeat in your hand**, quicker when it is hungry; and **push to talk**.

{{daemons CATHODE}}

This book is printed again as the Dot changes. This printing is {{release}}, {{date}}.

::: note
Every word this book quotes from the Dot is a **DRAFT**, as the game's own are, until it is approved. The Dot is
**new**: DAEMONS for it is built and runs in Kode's simulator, the den against a test companion; the device itself has
not yet come. What is not yet seen on the device is marked so.
:::
