# What this is {#what .t-GROWTH}

A daemon you carry on a phone or a watch is a picture and a voice. **This is the design for giving it a body**: a robot
it can move, hear through and speak from. You talk to it. It answers as itself, and while it answers it wags, sits,
tilts its head or walks to you, because those movements are part of what it said.

It is one system for many bodies. Some bodies arrive knowing how to move. Some have to find out. A new one is added by
writing one small folder, and nothing else changes.

::: note
**This is a design, reviewed and not yet built.** You answered its twelve questions on 2026-11-24, and Part 15
records each answer and what is still open. Every name in capitals is still DRAFT and yours to change. Next come its
tickets, B-1 onward, and the first wrapper: the PiDog, the body RoverByte was made from.
:::

{{diagram whole | The whole of it. The phone finds the body and puts a daemon in it. The house tells the body who the daemon is and helps it hear, think and speak. The body program is the same on every body; only the wrapper under it differs.}}

## What you asked for {#asked}

Your request, 2026-11-24, as ten requirements. The rest of the book refers to them by number.

| | The requirement |
|------|------------------------------------------------------------------------|
| **R1** | **General.** Any body, by adding a wrapper. The first is the PiDog. A second, a finished robot driven by its own API, follows. More will be built. |
| **R2** | **Two kinds of body.** Some come with predefined actions. Others learn to use their body by trial and error. |
| **R3** | **You talk to it.** Speech is heard, a language model answers, and the answer is spoken. |
| **R4** | **Actions are the model's tools**: the ones the body was given and the ones it has learned. |
| **R5** | **The answer carries its actions inline, in braces**, like `{BARK}`. It is split into an ordered list (words to speak, an action, more words) and performed: speech by a voice, actions by servo routines. |
| **R6** | **The daemon's persona** is the model's system message and context. |
| **R7** | **Wi-Fi alone is enough.** Tailscale may be installed for development and is never needed. |
| **R8** | **Bluetooth to the phone.** The app shows the robot you have, and you embody it with a daemon. |
| **R9** | **Raspberry Pi first**: a Zero 2 W, a 4B, perhaps a 5. |
| **R10** | **In this order**: research, the bible's entries, this book, your review, tickets, the build. |

## What it is not {#not}

- **Not a robotics framework.** There is no ROS here, no path planning and no map of the room. A body does named
  things in the place where it stands, and may walk a little when it has room.
- **Not a new mind.** The daemon's self, feelings, memory, dreams and voice already live in the companion. This design
  gives that mind a body and adds nothing to who the daemon is.
- **Not in the game.** The cartridge has no radio. An embodied daemon is AWAY, as a daemon on a watch is (bible 9.25).
- **Not a safety-rated machine.** It is a hobby robot under a person's eye. Part 11 says what the design does about
  that, and what it cannot.

## The design, on one page {#decisions}

| | The proposal | Why | Part |
|---------|---------------------------------------|---------------------------------------|---------|
| **D1** | **One body program, and one wrapper for each kind of body.** A wrapper is a sheet that describes the body and a driver that moves it. | Everything hard is written once. A new body is a day's work, and the dog's code never leaks into the rest. | 4 |
| **D2** | **Actions are the only way a daemon moves.** Every action passes one gate. STOP is a reflex outside any model. | A language model must never reach a servo. It names an action, and the body decides. | 5 |
| **D3** | **The answer is words with `{ACTIONS}` in braces**, performed as beats in the order written. A model's tool calls are read into the same beats. | It is what RoverByteOS already did, it streams, and small models write it more reliably than JSON. | 6 |
| **D4** | **Actions belong to the body. The self belongs to the daemon.** | A body's movements are learned on its own servos and would be wrong on any other. | 7 |
| **D5** | **A body is a device that carries a daemon**, by the companion's existing device list, key, carry and SELF. | Nothing parallel is invented: the app already shows devices and already puts a daemon in one. | 7 |
| **D6** | **A body learns in three ways: SHOWN, TRIED and FOUND.** A new action is untrusted until it has proved itself. | They are the three learning paradigms the game's starters already stand for, and research says which of each works on cheap servos. | 10 |
| **D7** | **Bluetooth for what is near and small, Wi-Fi for the rest, and the body always dials out.** Tailscale is off unless you turn it on. | Any network works when nothing has to reach in. | 8 |
| **D8** | **The machinery takes THE BRAIN's regions.** A body is one more host. | THE BRAIN was decided on 2026-11-24 for every AI harness. A body is where its motor half becomes real. | 3 |
| **D9** | **Its own repository, `daemons-embodied`, in Python on the body.** | Every robot's own library is Python. It holds nothing personal and nothing of the game's. | 14 |
| **D10** | **Where a body thinks is a setting: ON BOARD, MESH or HYBRID.** A frontier model only when you ask for it and approve it. | Yours, in review. One body should work alone, use the fastest mind in the house, or share the work between them. | 9 |
| **D11** | **A body learns to speak as it learns to move.** Its words start few and grow from talking with you, and each is kept in its daemon's own voice. | Yours, in review. It is meant to learn from you, and a small vocabulary can be made ready in its own voice ahead of time. | 10 |

# Where it comes from {#lineage .t-LEGACY}

Three things were read before any of this was drawn: your own earlier robots, the companion as it stands today, and
what others have published. This part is what each one settles.

## The Rover line {#rover}

The game's reinforcement line already tells this story. **ROVERCUB** is the portable build, **ROVERSEER** the server,
**ROVERBYTE** the dog: software, then infrastructure, then a body. Their INDEX categories are PORTABLE, PREDICTIVE and
**EMBODIED**.

{{sprites ROVERCUB ROVERSEER ROVERBYTE}}

{{daemons ROVERBYTE}}

The bible notes that the line gains its second type, SIGNAL (perception), at the moment it gains a body. This design
is those two entries built: a daemon that can at last check what it predicted, and that keeps what it got wrong
(Part 10).

## What RoverByteOS already proved {#proved}

RoverByteOS is the robot dog's software in your `RoverByte` repository: Python on a Raspberry Pi, driving a SunFounder
PiDog. It was read file by file. Most of this design is in it already, in a first form.

| RoverByteOS did this | This design |
|------|------|
| **The answer carried its actions inline, in order.** The form was a quoted name in square brackets, `["sit"]`, with a mood in angle brackets, `<"curious">`. A small parser returned an ordered list of `content` and `action` items. | **Kept, as the centre of the design** (D3). The brackets become braces, `{SIT}`, as you described it. Square brackets are now what speech engines use for their own sound tags, and a brace never occurs in speech. The old forms are still read. |
| **On the dog, the list ran strictly in order**: speak, then act, then speak. The body never moved while it spoke. Through its web API the order was lost, because speech and actions ran on separate threads. | **Order is kept everywhere, and movement may overlap speech** when an action says it may, on a different channel (Part 5). |
| **32 named actions**, 23 of SunFounder's and nine of your own: wag tail, pray, butt up, twerk, dab, floss, woah, gangnam style, bottle flip. | **All carried into the PiDog's wrapper** as its given actions (Part 12). |
| **A posture state**: stand, sit or lie, with the right transition run first, and the head's pitch corrected for each. | **Kept, as a graph of postures** every body's sheet may declare. |
| **Reflexes were written and never switched on**: a touch brought a nod and a wag; being lifted brought a splayed "flying" pose and a whoop; being set down, a stand. | **They are the first reflexes of the new body program**, and they run with no model at all. |
| **Names drifted between files.** Three actions failed on every call because the table and the functions disagreed, and the direct voice commands named actions that did not exist. The errors were swallowed. | **One repertoire, checked when the body starts.** A name that does not resolve stops the start. |
| **Everything thought in the cloud** (speech to text, the model, the voice), with no wake word and no way to interrupt. | **The body and the house first** (Part 8). A wake word, a stop word, and speaking over it are designed in. |
| **A small web API**: `/rover/action`, `/rover/speak`, and a page and a handheld remote that called them. | **The body keeps a door of that shape** (Part 8), so a page or a remote can still command it. |
| **Learning was wanted and never begun**: "Nightly Training: the AI dreams by updating itself", "movement pattern learning", a shared store of tricks. | **PRACTICE, and the night that follows it** (Part 10). |

RoverSeer and RoverSeerApi (the Pi 5 that heard with a local Whisper, thought with a local model and spoke with Piper)
proved the local voice loop and named its states. PenphinMind and the RoverRadio firmware gave THE BRAIN its words.
Their motor regions were named and left empty: `MotorCortex` held a pin map, `Cerebellum` a note that said it would be
written when needed. **It is needed now.**

## What the companion already has {#has}

The companion was surveyed for every seam a body should plug into. Nothing below is new work.

| What a body needs | What exists | Where |
|------------------------------|------------------------------------------|------------------------------------|
| **An identity** | a device id made of its kind and the end of its address, such as `pidog-a1b2c3` | `server/src/deviceid.ts` |
| **To be listed** | the device registry, and YOUR DEVICES in the app | `server/src/devices.ts`, `app/screens/places/Places.tsx` |
| **A daemon put in it** | carry: one daemon to a device, a device to a daemon | `server/src/carry.ts`, `POST /api/devices/carry` |
| **Who the daemon is** | the SELF, in three lengths (about 80, 300 and 1,500 words) | `server/src/self.ts`, `GET /api/self` |
| **A turn of talk** | hear, think and speak, on the house's own models | `POST /api/ai/talk` |
| **Its own voice** | a voice recipe for each daemon | `server/src/ai/voiceof.ts` |
| **A Bluetooth link** | one service and a line protocol, bonded by a passkey | `firmware/esp32/src/link.cpp`, `app/platform/handheld.ts` |
| **A shared list of Wi-Fi networks** | handed to a board over its link | C-93 |
| **A way home from anywhere** | the relay, with a key for each device | C-82 |
| **A shape for its machinery** | THE BRAIN's regions, signal and rings | `docs/BRAIN.md`, `server/src/brain/signal.ts` |
| **A rule for what it may do** | HANDS: named actions, the risky ones ask | `docs/ZEROKIT.md` 5, C-462 |

**And five gaps**, each small, each a ticket after review:

1. **No Raspberry Pi of ours speaks Bluetooth yet.** The link exists for the ESP32 boards only.
2. **The phone holds one linked device at a time.** A body is a second.
3. **The device pictures have no body in them.** A kind the app does not know is drawn as a grey board.
4. **The SELF cannot be fetched with a board's own key.** A Pi pairs as a phone today, which opens more than a body needs.
5. **HANDS is designed and not built.** This design builds it, as the gate (Part 5).

## What others have found {#field}

| Who | What they do | What this design takes |
|------------------------|------------------------------------------|------------------------------------|
| **SunFounder**, the PiDog's maker | Their current example asks the model for its words and then a last line, `ACTIONS: wag tail, sit`. It speaks, and the actions run beside the speech in no order. Sensor events reach the model as text. | The action names. Not the format: a trailer cannot say *when*. |
| **Reachy Mini** (Pollen Robotics, Hugging Face) | A daemon owns the motors and their safety; apps are its clients. Movements are tools. A small idle motion is blended under every move, and frozen while it listens. | The split into a body program and its clients; the idle layer; freezing it to listen. |
| **GhostShell** (2025) | Reads action tokens out of the model's stream and runs them as they arrive: in order on one channel, at once across channels. It finished 15 of 15 tasks against 6 of 15 for ordinary function calling. | The strongest evidence for D3, and the channel rule. |
| **A study of models under 2 billion parameters** (2026) | Only 5 of 1,000 raw answers were valid JSON. With a forgiving parser the best reached 75 to 79 percent. | Small models are never asked for JSON. They write a closed list of names, under a grammar. |
| **LeRobot, Viam, ros2_control** | Each describes a robot before connecting to it: its joints, what it senses, what it can be told. Viam adds one "do anything" call beside the typed ones. | The sheet, and the driver's short list of calls. |
| **Learning on real legged robots, 2004 to 2026** | Tuning a gait's dozen numbers on the robot itself works in 100 to 300 trials. Learning from nothing works only on robots that can feel their own joints. | Part 10 is built on this. |

The sources are listed in Part 15.

# The shape {#shape .t-STRATUM}

## Three layers {#layers}

**The wrapper** is the only part that knows what kind of body this is. It has two files: a sheet that describes the
body, and a driver with a short list of calls that reach its servos, sensors, speaker and lights.

**The body program** is the same on every body. It reads the sheet and builds from it the repertoire (every action
the body has), the gate every action passes, the motion engine that turns an action into timed, limited movement, the
senses, and the reflexes. It runs with no model and no network, and it never stops running.

**The daemon's turn** is the conversation: wake, hear, think as the daemon, and perform the answer. It is a client of
the body program. It may crash, wait on a slow model or lose the network, and the body under it stays safe.

::: tip
**Why two programs and not one.** A servo left mid-move by a crashed voice loop is how robots break. The part that
holds the motors is kept small, has nothing to do with audio or models, and is restarted by the system if it ever
stops. Everything else asks it politely. Reachy Mini is built the same way, and RoverByteOS's hardest bugs were the
places where it was not.
:::

## The words {#words}

Every one is DRAFT.

| Word | What it means here |
|------------------|------------------------------------------------------------|
| **BODY** | Any robot a daemon can be in. |
| **WRAPPER** | The folder that makes one kind of body usable: its sheet and its driver. |
| **SHEET** | The wrapper's description of the body: joints, senses, voice, actions, limits. |
| **ACTION** | One named thing the body can do: `WAG`, `SIT`, `WALK`. The only unit a daemon can ask for. |
| **REPERTOIRE** | Every action this body has, given or learned. THE BRAIN's word. |
| **POSTURE** | A stable way of resting: lying, sitting, standing. Actions start from one and end in one. |
| **CHANNEL** | A part of the body that does one thing at a time: legs, head, tail, voice, lights. |
| **BEAT** | One item of an answer: something to SAY or something to DO. |
| **PERFORMANCE** | An answer as an ordered list of beats, carried out. |
| **GATE** | The four questions every DO beat is asked before the body moves. |
| **REFLEX** | What the body does with no model: STOP, catching a fall, lying down on a low cell. |
| **MANNER** | How it moves and sounds just now: quick or slow, large or small, the colour of its lights. |
| **PRACTICE** | The time a body spends learning new actions, with a person present. |
| **EMBODY** | To put a daemon into a body. Its reverse is COME OUT. |

## One body program, in THE BRAIN's regions {#brain}

THE BRAIN (the companion's `docs/BRAIN.md`, decided 2026-11-24) gives every AI harness one shape: named regions, each
reached by the same small signal on every host, and a table of which hosts run which region. **A body is one more
host, and it is the one where the motor regions stop being names.**

| Region | On a body | Where it runs |
|------------------------|------------------------------------------------|------------------------|
| **BRAINSTEM** | Its cell, its heat, whether it has fallen. The reflexes. STOP. Sleeping and waking. | the body, always |
| **CEREBELLUM** | The motion engine: timing, the limits of every joint, the tempo of a manner. What it has learned about its own body. | the body |
| **BASAL GANGLIA** | The repertoire and the gate: go, ask first, or no-go. This is HANDS. | the body |
| **SOMATOSENSORY, VESTIBULAR** | Touch, balance, distance, where a sound came from. THE BRAIN named these as later regions. A body makes them first. | the body |
| **PSYCHIC CORTEX** | The radios: Bluetooth and Wi-Fi. RoverByte's own name for them. | the body |
| **THALAMUS** | Who answers each need: the body itself, the house, the relay, a model you named. | the body, for itself |
| **SALIENCE, AMYGDALA** | The low road: a few words that act at once. The daemon's feeling, as two numbers that set its manner. | the body (words); the house (feeling) |
| **CORTEX: auditory, language, motor speech, visual** | Hearing, thinking, the voice, sight. | the body where it can; else the house |
| **HIPPOCAMPUS** | What happened: each turn, each touch, each trial of PRACTICE, kept as events. The night's consolidation. | the body records; the hub keeps |
| **HYPOTHALAMUS** | The clock and the drives: quiet hours, a low cell as hunger, rest after effort. | the hub's, with a copy on the body |

**Three of THE BRAIN's rules carry straight over.**

- **The ring.** A signal marked `body` never leaves the device: every reflex, and STOP. Anything a person said, and
  anything the camera saw, is `home` at most. Only what you allow is `world`.
- **A host says what it runs.** A body answers with its connectome entry, and the hub's thalamus adds it to the
  house:

```json
{ "name": "pidog-a1b2c3", "at": "body",
  "regions": { "brainstem": {"power": 1}, "cerebellum": {"power": 1},
               "basal_ganglia": {"power": 1}, "thalamus": {"power": 1},
               "cortex.auditory": {"power": 0.3} } }
```

- **Mind and machine stay apart** (the companion's C-387). Who the daemon is stays psychology, in the companion:
  `self.ts`, `feelings.ts`, `memory.ts`, `dreams.ts`. Everything in `daemons-embodied` is machinery and takes
  anatomy's names. The body program is *handed* a self as text. It never builds one.

::: note
**This makes the body the second user of THE BRAIN's interface**, which is the moment `docs/BRAIN.md` 9 says the
interface moves out of the companion into a repository of its own, pinned by tag. Whether that move happens before the
body program is written was question 9, and you decided it: **it moves now**, and the body pins it by tag as the
companion pins PRAXIS.
:::

# The wrapper {#wrapper .t-HARDENED}

**Adding a body means writing one folder.** That is requirement R1, and it is the test every other choice in this
book is held to.

{{diagram wrapper | A wrapper, and three bodies that fill their sheets differently. The same body program runs all three.}}

## The sheet {#sheet}

The sheet is a file the body program can read before it touches the hardware. This is the PiDog's, shortened.

```yaml
body: pidog
name: PiDog                  # what the app calls this kind of body
shape: quadruped
maker: SunFounder
joints:                      # leave out for a body you can only command
  - {id: lf_upper, channel: legs, min: -90, max: 90, rest: 45,
     top_speed: 428, feels: none}
  - {id: head_yaw, channel: head, min: -90, max: 90, rest: 0,
     top_speed: 300, feels: none}
  - {id: tail,     channel: tail, min: -90, max: 90, rest: 0,
     top_speed: 500, feels: none}
  # ... twelve in all
senses:
  balance: {kind: balance, rate_hz: 20}      # roll and pitch
  range:   {kind: range, min_m: 0.02, max_m: 4.0}
  touch:   {kind: touch, pads: [front, rear], strokes: true}
  ears:    {kind: sound_bearing, step_deg: 20}
  eye:     {kind: sight}
  cell:    {kind: cell, full_v: 8.4, low_v: 6.8, empty_v: 6.4}
voice:  {speaker: true, microphone: true}
lights: {kind: strip, count: 11}
postures: [lie, sit, stand]
settle: lie                  # where STOP leaves it
limits: {tilt_deg: 40, hold_s: 5, rest_ratio: 2.0}
actions: actions/            # the ones it comes with (Part 5)
```

**Angles are degrees, lengths are metres, speeds are degrees a second**, on every body. `feels` says whether a joint
can report where it is: `none`, `position` or `current`. It decides which kinds of learning the body can do (Part 10).

## The driver {#driver}

The driver is a Python class with ten calls. A body implements the ones it has.

| Call | What it does | Needed |
|------------------------|------------------------------------------------|------------------------|
| `connect()` / `close()` | Open the hardware; leave it settled. | always |
| `status()` | Cell, heat, whether it is upright, whether each part answers. | always |
| `stop()` | **Halt every channel now.** Safe from any thread at any moment. Returns within 150 ms. | always |
| `settle()` | Go to the posture the sheet names, and rest there. | always |
| `move(targets, ms)` | Send joints toward angles, to arrive in `ms`. Returns at once. | a body with joints |
| `run(native, args)` | Run one of the maker's own routines by its key. | a body with native actions |
| `sense(name)` | Read one sense, in the sheet's units. | each sense it has |
| `play(sound)` / `hear()` | Audio out, audio in. | a body with a voice |
| `light(manner)` | Show a manner on its lights or its face. | a body with lights |

**Three rules bind every driver.**

1. **Nothing a model wrote ever reaches a driver.** The body program passes only names and numbers it has checked
   against the sheet. *The reason is concrete:* the PiDog's own library looks an action up by running `eval` on its
   name, so a careless wrapper would execute whatever a model typed.
2. **The driver refuses a target outside the sheet's range**, even though the body program has already checked it.
   The two checks are kept in two places on purpose.
3. **`stop()` is proved before anything else is written.** The body check (below) calls it in the middle of every
   action the body has.

There is one more call, `command(raw)`, for whatever a body has that the sheet cannot say. It is reachable from a
developer's own code and from nowhere else: no action may use it until that use has been given a name in the sheet.

## Two levels of access {#levels}

A wrapper may offer either level or both, and this is what R2 turns into.

::: keep
| | **Action level** | **Joint level** |
|------------------|------------------------------|------------------------------|
| The body offers | named routines: its maker's, or its API's | each joint, with its range |
| On the first day | it can already act | it can only rest |
| It can learn | new actions made by joining the ones it has | new movements of its own |
| Examples | a finished robot with an API | something you built yourself |
:::

**The PiDog offers both**, which is why it is the right first body: it acts on day one from its given actions, and
its open joints let PRACTICE be built and tested on it.

## Senses, by kind {#senses}

A sense is declared by its kind, and each kind has fixed units. The body program turns raw readings into a short list
of **events**, and those are what the rest of the system hears about.

| Kind | Reads | Events the body program makes of it |
|------------------|------------------------------|------------------------------------------|
| `balance` | roll and pitch in degrees; turn rate | TILTED, FELL, PICKED UP, PUT DOWN, STILL |
| `range` | metres to the nearest thing ahead | SOMETHING NEAR, ROOM AHEAD |
| `touch` | which pad, and a stroke's direction | PATTED, STROKED, HELD |
| `sound_bearing` | degrees round from its nose | A SOUND FROM THE LEFT (and so on) |
| `sight` | a frame, on request | none: it is asked for, never streamed |
| `cell` | volts and percent | CELL LOW, CELL EMPTY, CHARGING |
| `heat` | degrees Celsius | TOO WARM |
| `joint_feel` | each joint's position or current | STALLED, PUSHED |

An event can do three things. It can **fire a reflex** (FELL). It can **become a line of the daemon's context**
(*"someone is stroking your head"*). And some events may **start a turn of their own**, so the daemon reacts without
being spoken to: at most one in a while, and never while it is listening.

## The body check {#check}

`bodycheck` is the one test a wrapper must pass. It runs twice: **dry**, with the servos' power off, and **live**.

- The sheet is complete and its units make sense.
- Every action in the wrapper resolves to something the driver can run, and none is missing its one line of
  description.
- Every action ends in the posture it says it ends in.
- `stop()` halts the body within its time from the middle of every action.
- A target one degree outside a joint's range is refused by the body program, and again by the driver.
- A fall, simulated, brings the reflex and nothing else.
- The body still passes with no network.

**A simulated body passes the same check.** `wrappers/sim` is a body with no hardware: the body program runs against
it on any computer, which is how most of this system can be built and tested without the robot on the desk.

## Adding a body {#adding}

1. Copy `wrappers/_template` to `wrappers/<your-body>`.
2. Fill in the sheet from what the body has.
3. Write the driver's calls for those parts.
4. Run the body check dry, then live.
5. Draw its 32 by 32 picture for the app, and name its kind.

That is the whole of it. The repertoire, the gate, the performance, the links, the app's pages and PRACTICE all come
from the sheet.

# The repertoire {#repertoire .t-GROWTH}

**The repertoire is the list of everything this body can do.** It is what the daemon is shown as its tools (R4), and
it is the only vocabulary the body accepts.

## An action {#action}

Every action, whoever made it, is one record.

```yaml
name: SHAKE_PAW
says: offer a front paw to be shaken      # the one line the model reads
origin: given                # given, shown, tried, found or joined
uses: [legs]                 # the channels it needs
from: sit                    # the posture it starts in
to: sit                      # the posture it ends in
flows: false                 # may speech go on over it?
class: gesture               # how the gate treats it
finish: true                 # must it finish once begun?
takes: []                    # its arguments, each with a range
does: {native: hand_shake}   # or keyframes, or a generator (below)
knows: {ms: 2400, runs: 0, clean: 0}
```

`does` takes one of three forms:

- **`native`**: one of the maker's own routines, by its key. The driver runs it.
- **`keyframes`**: a list of poses, each a set of joint angles and a time to reach it. The motion engine runs it.
- **`generator`**: a named pattern with numbers, such as a walking gait with its stride, lift and timing. PRACTICE
  tunes those numbers (Part 10).

`knows` is what the body has measured about the action: how long it takes, how often it has run, how often it ran
cleanly. It is the cerebellum's part of the record, and the gate reads it.

## Where an action comes from {#origin}

::: keep
| Origin | Who made it | Trust at first |
|------------|------------------------------------------|------------------------------|
| **given** | the wrapper: the maker's routines, and yours | trusted |
| **shown** | a person, in the app (Part 10) | trusted once they have watched it run |
| **tried** | the body, by scored trials toward a goal | untrusted |
| **found** | the body, noticing something it could do while looking for something else | untrusted |
| **joined** | existing actions run in a row, under a new name | as its least trusted part |
:::

**An untrusted action asks before it runs** (the gate, below). After ten clean runs with a person watching it becomes
trusted. A person can trust one sooner, pin one so it is always offered, or have the body forget one. Each change is
written down with its date.

## Postures {#postures}

The sheet names the body's postures, and every action says which it starts from and which it leaves the body in. The
body program keeps them as a graph and **finds the way there itself**: asked for `SHAKE_PAW` while standing, it sits
first. The daemon never has to think about it, and the model's list of actions stays short.

On the PiDog the graph is three postures in a row, *lie, sit, stand*, and the step from sitting to standing is the
maker's own routine for it.

## Channels {#channels}

A channel is a part of the body that can do one thing at a time. An action says which channels it uses. Two actions
on different channels can run together; two on the same channel run one after the other.

**An action either FLOWS or HOLDS.** A wag flows: the daemon keeps talking over it. A sit holds: the next words wait
until the body is down. The record says which, and Part 6 shows what that does to a performance.

**Under every action is an idle layer**: breathing, a glance toward a sound, a small sway as it speaks. It is quiet
movement the body makes by itself so that it never looks switched off. It yields to any action that needs the
channel, and **it is frozen while the body listens**, because servos are loud and the microphone is inches away.

## The gate {#gate}

{{diagram gate | The gate, and the reflex that goes round it. A beat that fails question 1 or 3 is dropped or asked about; the words around it are still spoken.}}

Question 3 turns on the action's **class**:

| Class | What it is | Outcome |
|------------------|------------------------------|------------------------------------------------|
| `gesture` | a movement in place | **go** |
| `sound` | a bark, a howl, a tune | **go** by day; **no-go** in quiet hours, when a soft version is used if the body has one |
| `travel` | anything that moves the body from its spot | **go** if ROAM is on and its range sense shows room; **ask first** if ROAM is on and there is no room to see; **no-go** if ROAM is off |
| `asks` | reads a sense and returns it (Part 6) | **go**; a look through the camera says so with its lights |
| `untrusted` | any action not yet trusted | **ask first** |
| `sends`, `spends`, `deletes`, `moves` | an action that reaches outside the body: it sends a message, spends, or deletes or moves something that is not its own | **ask first**, always. These are HANDS' four (C-462), unchanged. |

**ROAM** is a switch a person sets, in the app or by voice: *this body is on the floor and may walk.* It is off when a
body starts, and it turns itself off when the body is picked up. A PiDog has no sense for the edge of a table, so
nothing else can stand in for it.

**ASK FIRST** is said aloud (*"May I try something new?"*) and shown on the phone. A yes by voice, by a tap on the
phone, or by a pat on the head lets it run. Silence for ten seconds is a no.

Every beat that reaches the gate is logged with its outcome: gone, asked and allowed, asked and refused, or dropped.

## STOP {#stop}

**STOP does not pass through the gate, the daemon or any model.** It is the brainstem's, and it has five sources:

- **A word.** "Stop" is heard on the body by a small model of its own that listens for nothing else.
- **A touch.** A hand held on it.
- **The phone.** A red button on the body's page, sent over Bluetooth.
- **A fall.** Tilt past the sheet's limit.
- **Its cell or its heat.** Too low, or too warm.

On any of them, every channel halts, whatever was queued is dropped, speech is cut, and the body goes to its `settle`
posture. Then it says what happened, once, if it can.

::: safe
**What "settle" can and cannot mean.** The PiDog's servos stay powered and holding after any command, and SunFounder's
staff say the newer ones cannot be released from software. So this body cannot go limp. Its settle is to lie down,
which is the posture that loads its servos least. A body that can cut its servos' power may do that instead; the
sheet says which.
:::

## Manner {#manner}

A daemon's feeling reaches its body as a **manner**: a tempo, a size of movement, a colour and rhythm for the lights,
and a tone for the voice. The companion already computes how a daemon feels (`feelings.ts`), and RoverSeerApi named
the two numbers that carry it, valence and arousal. A calm, glad daemon wags slowly and wide. An excited one is quick
and small.

The same action is therefore never quite the same twice, and nothing has to be learned for that: the motion engine
scales the action's times and angles, inside its limits.

RoverByteOS let the model set the mood with a tag of its own, `<"curious">`. That is kept: a manner can be written as
a beat, `{CURIOUS}`, and it lasts until the next one.

# The performance {#performance .t-SIGNAL}

**An answer is performed, not just spoken.** This part is requirement R5 in full: the format the model writes, how
it is taught, how the answer becomes beats, and how the beats become sound and movement.

{{diagram performance | One answer, three ways of looking at it. The model wrote four actions; one is not in this body's repertoire and is dropped without a word.}}

## The format {#format}

```
answer  =  ( words | "{" NAME args "}" )*
NAME    =  a name from the repertoire, such as WAG or SHAKE_PAW
args    =  zero or more values, separated by spaces
```

- **A name in braces is an action. Everything else is spoken.**
- **An action happens at the place it is written.**
- **Names are matched without regard to case**, and a space or a hyphen is read as an underscore, so `{shake paw}` is
  `SHAKE_PAW`. Where the first words of a tag are a known name, the rest are its arguments: `{WALK forward 3}`.
- **Arguments are checked against the action's record.** A value out of range is brought to the nearest allowed one.
  A missing one takes its default.
- **An unknown name is dropped**, logged and counted, and the words on either side close up. It is never spoken.
- **A brace that never closes** is treated as words, with the brace taken out.
- **Nothing in braces ever reaches the voice.** The speech text is cleaned twice: of the tags, and then by the
  companion's `sayable()`, which also sees that the word *daemon* is said DAY-mon.

::: tip
**Why braces, and why inline.** Inline is what RoverByteOS did, and it is the only form that says *when*. A list at
the end of the answer cannot put the wag before the question. JSON holds everything back until its last bracket, and
models under two billion parameters almost never write it correctly. A tag in the stream can be acted on the moment
it closes, while the model is still writing. Braces, because ElevenLabs and others now use square brackets for sounds
the voice should make, and a brace never occurs in ordinary speech.
:::

## Teaching the model {#teaching}

The daemon's system message is built from four blocks, in this order. Only the first comes from the companion.

```
1  WHO YOU ARE          the daemon's SELF, from the hub (Part 7)

2  YOUR BODY, NOW       You are in a body: a PiDog, a small four-legged
                        robot with a head, a tail, a voice and lights.
                        You are sitting. Someone is stroking your head.
                        Your cell is at 71 percent. You have been in this
                        body for twelve days.

3  WHAT YOU CAN DO      {WAG} wag your tail
                        {SIT} sit down
                        {TILT_HEAD} tilt your head to one side
                        {SHAKE_PAW} offer a front paw to be shaken
                        {LOOK} look, and be told what you see
                        ...

4  HOW TO DO IT         To move, write an action in braces at the place
                        in your answer where you would do it. Use only
                        the actions above, spelled as they are. Never
                        speak of the braces. One or two an answer is
                        plenty; none is fine.
```

Every word of blocks 2 and 4 is DRAFT.

**The list in block 3 is chosen, not dumped.** A large model is given the whole repertoire. A small one is given
about fifteen: the pinned ones, the ones that fit the body's posture, and the ones most used. Published tests agree
that a small model's accuracy falls as its list of tools grows. The AX630 kit's prompt is shorter than any of these
and holds fewer still (Part 9).

## Three dialects, one performance {#dialects}

Models differ, so the body reads three forms and turns them all into the same beats.

::: keep
| Dialect | Who writes it | How it is read |
|------------------------|------------------------------|------------------------------------------------|
| **Braces in the text** | any model; the form taught above | as it streams |
| **Tool calls** | a large model in the house or the cloud that prefers them | each call becomes a DO beat at the point in the answer where it was made |
| **Braces under a grammar** | a small model on the body itself | the model is *unable* to write a name that is not in the list: llama.cpp holds its output to a grammar made from the repertoire |
:::

A fourth is read for old times' sake: RoverByteOS's `["sit"]` and `<"curious">`.

## Actions that ask {#asks}

Most actions express something, and the daemon needs nothing back. A few **ask**: `{LOOK}` returns what the camera
sees, `{MEASURE}` how far the nearest thing is, `{CELL}` how much charge is left.

When an asking action is reached, the beats before it are performed, the body answers it, and the result goes back to
the model as a tool's result. The model then writes the rest. To the person it is one answer with a natural pause in
it: *"Let me see..."*, a look, *"that is a very red ball."*

HANDS' actions are asking actions too. *Reading out the day's tickets* is one: it is `{TICKETS}`, its class is plain
reading, and its result comes back as words for the daemon to say in its own way.

## Performing {#performing}

1. **Cut as it arrives.** A SAY beat closes at the end of a sentence; a DO beat closes with its brace. Each is sent
   on at once, so the body is moving and speaking before the model has finished.
2. **Each DO goes through the gate** (Part 5). What passes is handed to the motion engine.
3. **Each SAY goes to the voice**, a sentence at a time, and the sound is queued on the voice channel.
4. **Order is kept.** A beat starts when the beat before it allows:
   - after a **SAY**, when its sound has finished;
   - after a **DO that holds**, when the movement has finished;
   - after a **DO that flows**, at once.
5. **Only what was actually said is remembered.** If the performance is cut short, the daemon's memory of the turn
   holds the words that reached the speaker and the actions that ran, not the ones that were planned.

## Spoken over {#over}

People interrupt. The body handles it in two stages, as the better voice agents do.

- **A sound that might be speech** lowers its voice to a quarter and pauses the idle layer.
- **Confirmed speech** stops its voice, lets an action marked `finish` complete and settles any other, drops the
  beats still waiting, and listens.

A short "mm" or "yes" while it talks is not an interruption, and the body does not treat it as one.

**"Stop" is not an interruption.** It is the reflex (Part 5), heard by its own small model, and it halts everything
whether or not anything else is working.

## The turn {#turn}

{{diagram turn | One turn. The dashed box is the round trip an asking action makes; the amber road is the handful of words that never need a model.}}

**The low road** (step 3) is THE BRAIN's name for answers that need no deliberation. Here it is a short table of
words that act directly: *stop, sit, down, stand, quiet, come out.* RoverByteOS had the same idea in its "hey rover"
commands. They work with no network and no model, on every tier of hardware, and they are the body's floor: whatever
else is missing, it still does these.

**What starts a turn** is its name being said, a touch, the phone, or an event the body program lets through (being
picked up, something coming near, a long quiet). While a turn is under way it shows that it is listening or thinking,
with its lights and a small movement of its own.

# The daemon and the body {#daemon .t-CONTEXT}

## A body is a device that carries {#carry}

The companion already has the idea this design needs. **A device carries a daemon** (C-80): one daemon to a device,
and a daemon in one device at a time, so that choosing another device for it moves it there. A carried daemon is
**AWAY** from the game (bible 9.25), washed out in the party, safe, and able to come home changed (9.26).

**To embody a daemon is to have a body carry it.** Nothing about that is new: the same list, the same route
(`POST /api/devices/carry`), the same rule. A daemon in the PiDog is not on the watch. The watch shows where it went.

Any daemon can be embodied in any body. A ROVERBYTE in a dog's body is only the one that has come the whole way.

## What belongs to whom {#whose}

| The daemon brings | The body keeps |
|------|------|
| its SELF: who it is, how it feels, its day | its sheet |
| its own voice | its repertoire, learned actions included |
| its memories, and its bond with you | its calibration: where each joint's true middle is |
| its manner | what it has measured about each action |
| the words it has learned, and its lines kept in its own voice (Part 10) | its settings: where it thinks, whether it may ROAM |
| what it remembers of being in this body | its trials, and what it has learned about itself |

**A different daemon in the same body can do everything the last one could**, and does it in its own manner. **The
same daemon in a different body** remembers the old one and has to find out what this one can do.

::: tip
**Why the body keeps its actions (D4).** An action is a set of angles and timings found on these particular servos,
with this weight and this fur. Carried to another body it would be wrong, and on a body with different joints it
would be meaningless. What a daemon can carry between bodies is what it *remembers*: that it once learned to offer a
paw, and what that was like.
:::

## Arriving and leaving {#arriving}

{{diagram embody | Pairing happens once for a body. After that, putting a daemon in or taking it out is one tap, and the body never needs the phone to keep going.}}

**The SELF is fetched, kept, and refreshed.** The body asks the hub for the daemon's SELF in the length its thinker
can hold (short for a small model on the body, full for the house's). It keeps the last one it was given, in a file
only it can read, so the daemon is still itself when the house cannot be reached. It asks again when it wakes and
when the hub says the daemon's day has changed.

**Arriving is performed.** When a daemon is put in, the body does not simply change its name. It stirs, stretches,
looks about and speaks: the first performance in that body, made from the body's own given actions. Leaving is the
reverse: a few words, the settle posture, lights down.

## What the body gives back {#back}

Everything that happens in a body is recorded as events, in the form PRAXIS already uses, and sent to the hub when it
can be reached.

- **A pat is a care.** The companion already counts cares given, and they already build the bond (9.27).
- **A turn is a conversation**, and joins the talks the daemon remembers.
- **A day in a body is part of the daemon's day**, so the night's memory and the morning's dream have a body in them.
- **A daemon can grow up while embodied**, by the rules that already travel (9.26).

Nothing in the game changes. The cartridge sees an AWAY daemon come home with more friendship than it left with.

# Links {#links .t-FLOW}

{{diagram links | Requirement R7 is the third panel: no phone, no tailnet, any Wi-Fi.}}

## Bluetooth {#bluetooth}

**The body speaks the companion's own link.** The ESP32 boards already offer one Bluetooth service with a line
protocol, and the app already speaks it (`app/platform/handheld.ts`). The body program offers the same service from
a Raspberry Pi, through BlueZ and the `bluez-peripheral` library. The app needs no second protocol.

**What travels over it** is small and local:

| Line | Direction | What it carries |
|------------------|------------------|------------------------------------------------------|
| `HELLO` | body to phone | its kind, its id, the protocol's number: as the boards send today |
| `SHEET` | body to phone | the sheet in short: what it is, what it has, how many actions |
| `NETWORKS` | phone to body | the shared list of Wi-Fi networks (C-93) |
| `HUB` | phone to body | the hub's address and a one-time pairing code |
| `STATE` | both | cell, posture, who is in it, whether ROAM is on, where it thinks |
| `STOP` | phone to body | the reflex |
| `DO`, `SAY` | phone to body | one action, or a line to speak: for the body's page in the app |
| `PRACTICE` | both | a pose to hold, a trial's result, a yes or a no (Part 10) |

**Pairing is by a spoken code.** The boards pair by showing six numbers on their screen. A body has no screen, so it
**says** them, and you type them into the phone. The link is then bonded and encrypted, and a stranger's phone is
dropped. A body with no speaker blinks the code on its lights instead.

**Sound does not travel over Bluetooth** in the ordinary way. The handhelds can already send a short recording up the
link in pieces, and a body with no Wi-Fi may fall back to that, slowly. A phone's hotspot is the better answer.

**Two things the app needs** (gaps 2 and 1 of Part 2): to hold more than one linked device, and for iOS to keep the
link while the app is in the background. Both are known work with the library the app already uses.

::: note
**Improv was considered and set aside.** Improv is an open standard for giving a device its Wi-Fi over Bluetooth, and
it would be the least custom choice for a new product. Here it would be a second protocol beside one that already
exists, already bonds, and already carries the list of networks. It also sends the password in the clear unless
bonding is added to it.
:::

## Wi-Fi {#wifi}

**The body dials out and nothing dials in.** That one rule is what makes R7 true: it works on a home network, a
phone's hotspot or a café's Wi-Fi, with no port opened and no address to know.

It tries, in order:

1. **The hub at home**, at the address the phone gave it.
2. **The relay**, when home does not answer: the same hub, reached from outside (C-82).
3. **A model you named**: any service that speaks the OpenAI shape, for hearing, thinking or speaking. This is how a
   body works for someone with no hub at all.
4. **Itself.**

This order is the body's thalamus. Each need (hear, think, speak) is routed separately, so a Pi 5 away from home may
hear and speak by itself and send only the thinking out.

**What the body asks the hub for** exists today: to pair, to say hello, the daemon's SELF, a turn of talk, a line in
the daemon's voice, and the device's state. **One thing is new**: a turn that streams, so that the first sentence is
spoken while the rest is still being thought. Until it is built, the body takes the whole answer and cuts it into
beats itself, which costs a second or two and changes nothing else.

## Tailscale {#tailscale}

Tailscale is a convenience for whoever is building the body: a stable name to reach it by from another room. It is
installed by the developer's setup script as a service that is **off**, turned on and off by one command, capped in
the memory it may use, and **nothing in the body program ever names a tailnet address.** On a Zero 2 W, with 300 to
400 MB free, that cap matters.

## The body's own door {#door}

The body program answers on a small local door, for the turn, for a page in a browser, and for any remote you care
to build:

| Route | What it does |
|------------------------|------------------------------------------------|
| `GET /body/sheet` | the sheet |
| `GET /body/status` | cell, posture, who is in it, what it is doing |
| `GET /body/repertoire` | every action, with its record |
| `POST /body/do` | one action, through the gate |
| `POST /body/say` | a line with actions in braces, performed |
| `POST /body/stop` | the reflex |

It is RoverByteOS's `/rover/action` and `/rover/speak` under plainer names. It answers the body itself always, and
the house's network only to a caller holding the body's key. `stop` alone needs no key: anyone in the room may stop
it.

## Keys {#keys}

No key, password or network name is ever in the repository. A body keeps what it is given in its own configuration
folder, readable by it alone, and the repository's tests fail on anything that looks like a secret.

# Which computer {#tiers .t-VECTOR}

**The body's computer decides how much of a turn it can do alone.** Everything else in this book is the same on all
of them.

::: tip
**Decided, 2026-11-24: the first build keeps the Pi Zero 2 W that is in the dog now and adds an AX630 board, the
LLM630 Compute Kit, as its brain.** It is supported on your kit as it stands, it draws the least power of the choices
that have a mind of their own, and the pair is the one the companion already designed for the Cardputer Zero. *If it
works, the same two boards go into every creature you build.*
:::

| | **Zero 2 W alone** | **Zero 2 W + AX630 kit** | **Pi 4** | **Pi 5** |
|------------------------|------------------|------------------|------------------|------------------|
| Reflexes, STOP, the gate, movement | on the body | on the body | on the body | on the body |
| Its name, and the stop word | on the body | on the body | on the body | on the body |
| **Hearing** | elsewhere | on the kit | on the body | on the body |
| **Seeing** what is around it | elsewhere | on the kit | elsewhere | on the body, slowly |
| **Thinking** | elsewhere | small, on the kit | elsewhere | small, on the body |
| **The voice** | lines it has kept | kept lines; the kit's plain voice | kept lines; a plain voice | kept lines; a plain voice |
| Alone, with no network | reflexes, direct words, kept lines | a whole small turn | hears and speaks; cannot think | a whole small turn |
| Power | least | a little more | more | most |
| On your kit (Robot HAT V4) | yes | yes | yes | no: it needs the newer HAT |

**What stands behind each cell** (every number is published, and none was measured here):

- **Its name and the stop word.** Small always-on models of the kind Home Assistant's voice project runs; one
  measured about 5 percent of a single Zero 2 W core. The ready-made ones answer to fixed words, and a word of our
  own has to be trained, a few hours on the house's GPU. You chose one word of our own for every body, and a touch.
- **The end of speech.** Silero's detector (MIT licence, about 2 MB).
- **The AX630 kit.** M5Stack publishes 10.3 tokens a second on this chip for a model of half a billion parameters,
  with its first word after about a third of a second, and 3.6 tokens a second at one and a half billion. **Its
  prompt is short: 128 to 256 tokens.** So ON BOARD the daemon's SELF is two lines and its list of actions is brief.
  It hears with Whisper and speaks in one stock voice; neither has a published speed, and timing them is the first
  bench job. It draws about one and a half watts while it works.
- **Hearing on a Pi.** Moonshine's streaming models (MIT). Its maker reports 237 ms on a Pi 5 for the smallest,
  against nearly six seconds for Whisper's smallest.
- **Thinking on a Pi 5.** A model of half a billion to one and a half billion parameters runs at 10 to 25 tokens a
  second under llama.cpp: about twice the kit's speed, with room for a long prompt, at several times the power.
  Models of three billion and more are too slow to talk with.
- **A plain voice on a Pi.** Piper, at about a fifth of real time on a Pi 5 and a third on a Pi 4. Its maintained
  version is under the GPL, so a body runs it as a separate program and does not link it.
- **The Raspberry Pi AI HAT+ 2** was measured by two reviewers as slower than the Pi 5's own processor for language
  models. It is not part of this design.

::: note
**The daemon's own voice is made in the house**, by a large model, from its recipe. No board on a body can make it.
What a body can do is *keep* it: every line the daemon speaks at home is kept on the body as sound, and each night
the house prepares the words it is learning (Part 10). So alone it says what it has learned in its own voice, and
anything new in the kit's plain one.
:::

## Where it thinks {#mind}

**Where a body thinks is a setting**, on the body's page in the app, beside which daemon it hosts and whether it may
ROAM. You asked for three. Each is a different way of setting the body's thalamus (Part 3).

| | **ON BOARD** | **MESH** | **HYBRID** |
|------------------------|------------------|------------------|------------------------|
| In a line | everything on the body | the fastest mind in the house | each thing where it is done best |
| Reflexes, STOP, direct words | the body | the body | the body |
| Hearing | the kit | the house; the kit if none answers | the kit |
| Seeing what is around it | the kit | the house | the kit |
| A short, simple turn | the kit | the house | the kit |
| A turn that needs depth | the kit, as best it can | the house | the house |
| The voice | kept lines; the kit's for the rest | its own, from the house | kept lines at once; its own from the house for new ones |
| What leaves the body | nothing | what was said | only what is sent on |

- **ON BOARD** is private and whole, and it works anywhere. Its limits are the kit's small model and short prompt.
- **MESH** is what your other devices do today: THE MESH picks the fastest mind that answers, the Tiiny when it is
  awake. It gives the best answers and the daemon's own voice, and it needs the house or the relay.
- **HYBRID** is THE BRAIN's two roads on one body. The kit is the low road. It hears and sees, and before anything
  else it answers a few typed questions about what was said: *is this a direct word? a care? small talk? does it
  need the house?* What it can answer, it answers at once. What needs depth goes to the house, with the kit having
  already said how much of the SELF to send. If the house does not answer in time, the kit's own answer is used.

**HYBRID is the setting a body starts with** (decided). It is also the last of the three to be built, so until it
exists a new body starts on MESH. A body that loses its network behaves as ON BOARD whatever its setting, and goes
back when the network does.

**A frontier model, only when you ask and approve.** A hard task can go to a large model outside the house, each
time on your request and with your yes. It is the gate's ASK FIRST (Part 5) applied to thinking, and THE BRAIN's
`world` ring. A setting on the daemon can switch even the asking off. Nothing a person said goes with the task
unless you say so.

**A body lends its mind.** Resting on its charger, the kit joins THE MESH as a small node and takes hearing,
speaking and seeing jobs from the rest of the house (the companion's C-466). It stops the moment its own daemon is
spoken to.

# Learning the body {#practice .t-EMERGENT}

**PRACTICE is the time a body spends learning what it can do.** It is requirement R2, and it is the part of this
design with the most research behind it and the most left to prove.

{{diagram practice | PRACTICE. Three ways in, one trial harness, one way out: an action in the repertoire, untrusted until it has proved itself.}}

## Three ways, and they are the starters' three {#three}

The game's three first daemons stand for the three ways a machine learns (bible 8.2). A body learns in the same
three.

::: keep
| | The way | In machine learning | The starter | What it needs |
|------------|------------------------------|------------------|------------------|------------------------|
| **SHOWN** | A person gives the right answer. | supervised | LABEL | a person, and the app |
| **TRIED** | It tries, is scored, and tries again. | reinforcement | ROVERCUB | a goal it can measure |
| **FOUND** | It notices what it can do, with no goal at all. | unsupervised | CLUSTER | nothing but time |
:::

{{sprites LABEL ROVERCUB CLUSTER}}

## What the research rules out {#ruled}

A PiDog has twelve hobby servos that **cannot report where they are**, a balance sense, a distance sense, and no
simulator its maker stands behind. That closes more doors than it opens, and it is better to say so before designing.

| Method | Why not, on this body |
|------------------------|------------------------------------------------|
| **Learning to walk from nothing by deep reinforcement learning** | Every published success on a real legged robot had joints that report their position and speed. None was done on hobby servos. |
| **A self-model built by babbling** (Bongard, Lipson) | It needs joint-angle sensors, or a ring of cameras and a GPU. The camera methods' own authors say they may fail for legs, because the ground's push is not visible. |
| **Thousands of trials** (MAP-Elites, curiosity-driven exploration) | The famous results ran millions of trials in simulation. On hardware alone, expect tens of results, and a hobby servo will not live through twenty thousand. |
| **Distance from the balance sense** | Adding up a cheap accelerometer's readings drifts by more than 150 metres in a minute. It cannot say how far the body walked. |
| **A vision model as the only judge** | The 2026 work on this found that no general model is reliable at saying whether a robot succeeded. |
| **A robot foundation model** (the VLAs) | None runs on a Pi, and none was trained on anything like a toy quadruped. |

## What it can measure {#measure}

Learning needs a score, and a score needs a measurement the body can trust.

| Measure | Trust | Use |
|------------------------------------|------------------|------------------------------|
| **Tilt, and whether it fell** | high | the abort signal, and a score for steadiness |
| **How far the wall is, before and after**, standing still | good | how far it moved toward a wall |
| **How much it turned**, over a few seconds | fair; it drifts | turns, short ones |
| **A marker on its back, seen by a camera above** | good | how far and which way it moved, anywhere |
| **A person's yes or no; a pat** | high, and slow | the last word on any action |
| **Whether a servo stalled** | not available without added hardware | none yet |

**The camera above can be the phone.** Propped on a shelf looking down, it watches a printed marker on the body's
back and reports where it went. That is the cheap, proven signal in the published work, and it uses hardware you are
already holding. It is the later of the two: the wall and the balance sense come first.

## The trial harness {#harness}

**Whatever proposes a movement, every trial runs the same way.** This is built first, before any learning, and it is
where the safety lives.

1. **Check the proposal** against every joint's range and speed, and against the poses already known to be unsteady.
   A proposal is only ever a small step from something that has already run safely.
2. **Start from rest**, easing in over two seconds.
3. **Run it**, for fourteen seconds at most, recording the balance sense throughout.
4. **Abort at once** on tilt past the limit, a touch, a word, or the phone's link dropping.
5. **Return to rest**, easing out, and read the after-measures standing still.
6. **Rest** for at least twice as long as it moved.
7. **Write the trial down**: what was sent, what was measured, how it ended.

A candidate is run two or three times before its score is believed. Published gait tuning found single runs too
noisy to learn from.

**A failed trial is kept.** It is what makes the next proposal better, and ROVERBYTE's entry in CONTEXT said so
before any of this was designed: *"It kept them anyway, marked, so it could tell next time."*

## SHOWN {#shown}

**A person makes the movement and the body keeps it.** On a body whose joints can feel, that means moving its limbs
by hand while it records. A PiDog's cannot, so on it SHOWN is the app's **pose page**: a slider for each joint, a
row of poses, and a play button. You set a pose, add it, set the next, and play them through. It is what Petoi's
Skill Composer does for their dog, and it is how your own nine actions were written, with numbers typed into Python.

The daemon can help in two ways. It can **propose**: asked for "a play bow", the model writes a few candidate rows of
poses inside the limits, and you pick the one that looks right. One 2025 study found a person's choice among a
model's candidates settled in about four rounds. And it can **name**: it watches what you made and offers a name and
the one line that will describe it to itself later.

## TRIED {#tried}

**A goal, a movement with numbers in it, and a search.** The PiDog's library already has two gait generators, a walk
and a trot, each with a stride, a lift and a timing. They were tuned for a bare kit on a hard floor. **Yours has fur
and its own floor.** Tuning those numbers for your dog is the natural first goal: *walk further in ten seconds, and
stay level.*

The search is **Bayesian optimisation**: after each trial it updates its picture of which numbers work and picks the
next ones to try where it expects to learn most. It is the method with the best record on real robots with no joint
sensing: about 120 trials for a Sony Aibo's walk in 2007, about 80 for a small biped. With each candidate run twice
or three times, that is **two or three hours of the robot's time**, spread over several charges and several days.

A person can be the score. Say *"good"*, or pat it, in the moment after a trial, and that trial counts for more.
That is clicker training, and it is why the reinforcement line is a dog.

## FOUND {#found}

**Every trial is kept for what it did, whatever it was for.** A trial that was meant to walk forward and instead
turned the body a quarter of the way round is a bad walk and a good turn. So each one is filed by its *outcome*: how
far, which way, how steady. The best one in each cell of a coarse grid is kept.

After a few hundred trials that grid is a small map from *what I want to happen* to *what to send*, and the body can
offer an action it was never taught: `{WALK forward 0.3}` or `{TURN left 45}`, answered by the nearest thing it has
actually done. This is the idea behind the best-known result in the field, cut down to what hardware alone can
afford: tens of cells, not thousands.

**Babbling has a small part.** With a person present and the body lying or sitting, it makes small random movements
inside its limits and records how its balance answers. From that it learns which poses are steady and which are
not, and that makes every later proposal safer. It is not how it learns to walk.

## Learning to speak {#speak}

**You added this in review: a body learns to speak as it learns to move.** In your words: *"its vocabulary can start
simple, but it is meant to learn from you, so as you talk to it, what it says grows."*

- **Its words start few.** In a body, a daemon begins with a small set: its name and yours, yes and no, the names of
  its actions, a few feelings, and its sounds. It speaks in short sentences made mostly of words it has.
- **It learns them from you, in the same three ways.** SHOWN: you teach it a word (*"say ball"*). FOUND: a word you
  use with it on several days becomes one of its own. TRIED: it tries a word it has just heard, and your answer (a
  yes, a pat, a correction) keeps it or drops it.
- **Its sentences grow with its words.** First words and sounds, then short phrases, then talk. Where those lines
  fall is DRAFT. They are counted in words learned, not in days.
- **Every word is kept in its own voice.** Each line it speaks at home is kept on the body as sound. And each night
  the house says the words and short phrases it is learning, in its voice, and sends them over. A small vocabulary
  can be made ready ahead of time, and that is what lets a body speak as itself with no network: **alone, what it can
  say in its own voice is exactly what it has learned so far.**
- **Its words are the daemon's, not the body's.** Actions stay with the body (Part 7). Words go with the daemon to
  its next body, and home to the companion, which keeps the list as part of who the daemon is.

**How the model is held to it.** A large model is steered by a line in its SELF: *you are still learning to speak;
use short sentences, mostly from the words you know; you may try one word you have just heard* (DRAFT). The words
follow it. The small model on the kit is given the same list and little else, which suits its short prompt.

**Two things this leaves open**: whether a daemon's speech also starts small on the phone and the watch, where
today it speaks freely; and how fast it should grow.

## The night {#night}

No servo moves at night. **The day's trials are read again**: the search's picture is redrawn from all of them, the
grid is rebuilt, actions that have started to fail are marked untrusted, and the model reads the numbers and writes
a short list of what to try tomorrow, which a person may accept or ignore.

It is the same night THE BRAIN gives the hippocampus, and the one RoverByte's notes asked for in 2025: *the AI dreams
by updating itself based on past experiences.* The daemon's own dream that night is made by the companion, as ever,
and it may now have the day's practice in it. And the house says the words the daemon is learning, in its own voice,
and sends them to the body for the morning.

## Rules of practice {#rules}

::: safe
1. **A person starts it and stays.** PRACTICE begins from the phone and ends when the phone's link drops.
2. **On the floor, on something soft, with nothing to fall from.**
3. **A budget.** Forty trials or fifteen minutes of movement a session, whichever is first. Then it rests.
4. **The cell.** Not below its low mark. The pack's own cut-off is a hard power cut that corrupts the Pi's card, so
   the body lies down and shuts itself down properly well before it.
5. **Heat.** No pose is held against load for more than five seconds, and it rests twice as long as it moves. A body
   in fur sheds heat more slowly, and that ratio can be raised in its sheet.
6. **Small steps.** No trial is far from one that has already run safely.
7. **Nothing learned is trusted at once.** A new action asks before it runs until it has run cleanly ten times.
:::

# Keeping it safe {#safety .t-ENTROPY}

Safety is in every part of this book. This part gathers it, so that it can be reviewed in one place.

## What a model can never do {#never}

- **Reach a servo.** It writes names. The body decides.
- **Use a name that is not in the repertoire.** It is dropped.
- **Run code.** There is no shell and no `eval` anywhere a model's words travel.
- **Override STOP,** or the gate's ask.
- **Send what was said or seen out of the house,** unless you have allowed that road.

## What the body does without being asked {#does}

| When | It |
|------------------------|------------------------------------|
| it tilts past its limit | stops, and settles when it is upright again |
| it is picked up | stops walking, turns ROAM off, and may enjoy it |
| its cell is low | says so, lies down, and refuses to travel |
| its cell is nearly empty | settles, and shuts itself down cleanly |
| it is too warm | rests until it is not |
| the body program stops answering | the system restarts it, and it starts settled |
| the voice loop stops answering | nothing: the body program carries on |
| its network is gone | carries on with what it has (Part 9) |

## What it cannot promise {#cannot}

- **It cannot see an edge.** A PiDog has no sense for the end of a table. ROAM is the only guard, and a person
  sets it.
- **It cannot go limp.** Its servos hold. A hand caught in a joint is held until the joint moves.
- **It cannot feel a stalled servo.** Time limits stand in for the sense it lacks.
- **Its microphone is always open** for its name and the stop word. Those two are heard on the body and nothing
  else is kept or sent until one of them is heard. A light shows when it is listening, and a line in the app shows
  everything it sent out and where.
- **It is not a toy for a child left alone with it,** nor safe around a pet that might bite it or be pinched by it.

# The first body: the PiDog {#pidog .t-GROWTH}

{{diagram pidog | The PiDog as its sheet sees it: twelve joints on three of its five channels, and six senses.}}

## What it has {#pihas}

| Part | What it is | What the wrapper makes of it |
|------------------|------------------------------------------|------------------------------------|
| **12 servos** | two to a leg (no sideways hip), three in the neck (yaw, roll, pitch), one in the tail. None reports its position. | twelve joints on three channels: legs, head, tail |
| **Balance** | an SH3001, read 20 times a second | tilt, falls, being picked up and put down |
| **Distance** | an ultrasonic sensor in the head | something near, room ahead, the wall measure for PRACTICE |
| **Touch** | two pads on the head, which also tell a stroke forward from a stroke back | patted, stroked, held; a yes; a STOP |
| **Sound direction** | three microphones, a bearing in steps of 20 degrees | a sound from one side; turning to face a voice |
| **Camera** | 5 megapixels, in the nose | `{LOOK}` |
| **Lights** | a strip of 11 on the chest | its manner; listening, thinking |
| **Speaker and microphone** | on the newer HAT; the first kit has a USB microphone | the voice channel |
| **Cell** | two 18650s, 8.4 V full, cut off hard at 6.0 V | the cell sense, and an early, clean shutdown |

## Its brain: a Zero and a kit {#pibrain}

**Decided: the Pi Zero 2 W that is in it now, with an LLM630 Compute Kit on its back.** The Zero runs the body
program: servos, senses, reflexes, the gate, Bluetooth. The kit hears, sees, thinks in a small way and speaks
(Part 9).

**Your kit is the first PiDog kit.** Your code for it dates from October 2024, and the second kit went on sale in
July 2025. Its Robot HAT gives 5 volts at 3 amps, and SunFounder does not support a Pi 5 on it. To be sure, look at
the HAT: its version is printed on it, and only the newer one has a ZERO button and a microphone on the board. A
Pi 5 with the newer HAT stays possible later, and nothing in the design changes if it comes.

**Five things to settle on the bench before the pair is trusted:**

1. **The Zero has one USB port for data.** The kit's link and the first kit's USB microphone both want it. A small
   hub, or the kit reached over Wi-Fi or the serial pins instead.
2. **Power for the kit**: from the HAT's 5 volt rail, beside twelve servos, or a cell of its own. The companion's
   bench list for the Cardputer Zero and its kit asks the same (C-458, C-459).
3. **How fast it hears and speaks.** Whisper and the kit's voice have no published speed on this chip.
4. **How much of a daemon fits in 128 to 256 tokens**, with a list of actions beside it.
5. **Where it sits**, under the fur, without overheating. The kit is about 90 by 32 by 12 mm, and it warms as it
   works.

## Its given actions {#given}

The wrapper begins with 48 actions: SunFounder's, yours, and three that ask, under one set of names.

| Channel | Actions | Class |
|------------------|------------------------------------------------------|------------------|
| **legs: postures** | `LIE`, `SIT`, `STAND`, `HALF_SIT`, `LIE_PAWS_OUT` | gesture, holds |
| **legs: travel** | `FORWARD`, `BACKWARD`, `TURN_LEFT`, `TURN_RIGHT`, `TROT` | travel, holds |
| **legs: tricks** | `STRETCH`, `PUSH_UP`, `SCRATCH`, `SHAKE_PAW`, `HIGH_FIVE`, `TWIST`, `FEET_SHAKE`, `DOZE_OFF` | gesture, holds |
| **legs: yours** | `PRAY`, `BUTT_UP`, `TWERK`, `DAB`, `FLOSS`, `WOAH`, `GANGNAM`, `BOTTLE_FLIP` | gesture, holds |
| **head** | `NOD`, `SHAKE_HEAD`, `TILT_HEAD`, `THINK`, `RECALL`, `RELAX_NECK`, `LOOK_DOWN`, `FLUSTER`, `SURPRISE`, `ALERT`, `LICK` | gesture, flows |
| **tail** | `WAG` | gesture, flows |
| **voice** | `BARK`, `BARK_HARDER`, `PANT`, `HOWL`, `GROWL`, `SNORE`, `WHOOP` | sound, flows |
| **asks** | `LOOK`, `MEASURE`, `CELL` | asks |

The old names are kept as other spellings of the new ones, so `{wag tail}`, `{handshake}` and `{bark harder}` still
mean what they meant.

## Its reflexes {#reflexes}

::: keep
| Event | Reflex | From |
|------------------|------------------------------------|------------------------------|
| **PICKED UP** | legs stop; the splayed "flying" pose; a whoop | RoverByteOS, written and never switched on |
| **PUT DOWN** | stands | the same |
| **PATTED** | a nod and a wag, lights warm | the same |
| **FELL** | stops; when level again, lies and then rises | new |
| **CELL LOW**, **TOO WARM** | says so, lies down | new |
:::

## Traps this wrapper has to cover {#traps}

Reading the PiDog's library and its forum turned up a list of things that would each have cost a day.

- **The action table runs `eval` on a name.** The wrapper calls it only with keys from its own closed list.
- **`stop_and_lie(speed)` passes its speed into the wrong argument**, so it always runs at 50. The wrapper calls the
  parts itself.
- **"Wait until done" returns one pose early** for the head and tail. The wrapper waits on its own timing.
- **`speak()` kills the sound server on every call.** The wrapper plays sound itself.
- **Touch and the sound bearing are polled, not pushed.** The wrapper polls them on its own thread.
- **The library never checks the cell.** The pack's own cut-off at 6.0 V is a hard power cut, and users report
  corrupted cards. The wrapper watches the voltage.
- **Many servos moving at once can reset the Pi.** The library staggers them at start-up only. The motion engine
  keeps to a limit on how many joints accelerate together.
- **A process that dies keeps the pins claimed**, and the next start fails. The body program is a service that
  cleans up after itself.
- **The legs have no published limits** beyond the servos' own half-turn. Measuring a safe range for each is the
  wrapper's first bench job, and those numbers are the sheet.
- **Calibration is a per-dog file** of offsets, up to 20 degrees a joint. The wrapper reads it and never writes it.
- **It needs a 64-bit system**, and SunFounder's staff recommend the current Raspberry Pi OS.

## Without the robot: the simulated body {#sim}

`wrappers/sim` is a body made only of its sheet. It draws itself as a stick figure in a browser page from the
PiDog's own published leg lengths (42 mm upper, 76 mm lower, on a body 117 by 98 mm), answers every driver call, and
makes up a believable balance reading. It cannot say whether a gait walks. It can say whether the system works, and
that is most of what there is to build.

SunFounder publishes no model of the PiDog for a physics simulator. Three exist from its community, of unchecked
accuracy and mostly with no licence, so none is taken into the repository. They are noted in Part 15 for the day
PRACTICE wants one.

# A body you command {#commanded .t-ORACLE}

Your second robot is a finished machine driven through its maker's API. It needs a different kind of wrapper, and
the design was shaped so that it is the *same* system with fewer parts filled in.

| | A body with open joints | A body you command |
|------------------|------------------------------------|------------------------------------|
| **The sheet** | joints, senses, actions | actions, and whatever senses its API reports |
| **The driver** | owns the servos, their timing and their limits | owns the session: its address, its login, its connection |
| **An action** | keyframes the motion engine plays | one of the maker's commands, sent by name |
| **How it knows an action is done** | it timed it | the robot says so, or it asks until it does |
| **STOP** | every channel halts within 150 ms | the maker's own stop, sent at once; how fast is theirs |
| **Stopping mid-action** | always | only if the maker allows |
| **Learning** | SHOWN, TRIED and FOUND | joining its commands into new named actions; SHOWN, if its API has a pose mode |
| **Safety** | this design's limits | the maker's own, with this design's gate in front |

Three published robots show the range such a wrapper has to cover: a Unitree Go2 takes numbered sport commands over
a network; a Petoi Bittle takes short text tokens over a serial line; a Misty takes web requests. Each would be a
sheet of twenty lines and a driver of about a hundred.

**What is needed from you** is its name and its API. Its wrapper is a phase of its own (Part 14), after the PiDog
has proved the body program.

# Building it {#building .t-LATENT}

## The repository {#repo}

```
daemons-embodied/
  README.md   CLAUDE.md   LAYOUT.md   TODO.md
  docs/                  this design; a page for each wrapper
  embodied/              the body program
    brainstem/           status, reflexes, STOP, the watchdog
    cerebellum/          the motion engine; what the body knows of itself
    basal_ganglia/       the repertoire and the gate
    senses/              readings into events
    psychic/             Bluetooth, Wi-Fi, the body's door
    hippocampus/         events, kept and sent
    sheet.py             the sheet, read and checked
  turn/                  the daemon's turn: a client of the body program
    ears/  thinker/  voice/  words/  performance/
  practice/              the harness; shown, tried, found; the night
  wrappers/
    _template/           copy this to add a body
    sim/                 a body with no hardware
    pidog/               the first
  tools/                 bodycheck, install, the service files
  tests/
```

**Python, on the body.** The companion's Pi devices are C++, and that was right for a screen and a game. A body's own
library is Python on every robot looked at for this book, and so are the speech and model tools. The body program
talks to the hub over the hub's existing routes, so the two languages never meet in one process.

**Installed as two services**, `daemons-body` (the body program) and `daemons-turn`, by a script run from a computer
over SSH, as the companion's Pi devices are. A third, the developer's Tailscale, is off.

**Public, at CodeMusic/daemons-embodied, with nothing personal in it**: no key, no network name, no daemon's SELF, no
recording.

**Its tickets are B-1 onward**, in a Redmine project and a lane of their own, BODIES (decided). **THE BRAIN's
interface is not kept here**: it is pinned by tag from a repository of its own (decided), as PRAXIS is.

## Phases {#phases}

Each phase ends in something that can be seen working. They are the outline of its tickets, B-1 onward.

| | Phase | Done when |
|------|------------------------------------------------------|------------------------------------------|
| **A** | **Foundations.** The repository, the sheet, the driver's calls, the simulated body, the body check. | the simulated body passes the check on any computer |
| **B** | **The performance.** The format's reader, the beats, the gate, the motion engine, channels. | a typed line with braces is performed by the simulated body, in order, with STOP working |
| **C** | **The PiDog's wrapper**, on its Zero 2 W. Its sheet, its 48 actions, its senses and reflexes, its traps. | the real dog passes the check, live, and performs a typed line |
| **D** | **The daemon's turn, on the MESH.** Its name, the stop word, hearing and thinking and the voice through the house, the SELF, speaking over it. | you talk to a daemon in the dog, at home |
| **E** | **Bluetooth and the app.** The link on a Pi, the spoken code, Wi-Fi handed over, the body in YOUR DEVICES with its page and its settings, EMBODY, STOP. | a new body is paired and a daemon put in it from the phone alone |
| **F** | **ON BOARD.** The kit on the bench (Part 12), its link to the Zero, hearing, a small turn and a plain voice on it, kept lines. | it holds a small turn with the house switched off |
| **G** | **HYBRID.** The low road on the kit, depth from the house, sight on the kit. A frontier model on request. | one conversation uses both, and you cannot hear the join |
| **H** | **Learning to speak.** Its words, its lines kept in its own voice, the night's phrases. | alone, it says a word you taught it, as itself |
| **I** | **PRACTICE, shown.** The trial harness, the pose page, naming, trust. | you teach it an action from the phone and the daemon uses it |
| **J** | **PRACTICE, tried and found.** The search, the measures, the grid, the night. | its walk is measurably better than the kit's, on your floor |
| **K** | **A body you command.** Your second robot's wrapper. | the same daemon moves from the dog to it |
| **L** | **Later.** A Pi 5 and the newer HAT; THE BRAIN's signals end to end; sharing actions between bodies of one kind. | |

**A, B and most of D need no robot.** C needs the dog on the bench, E the phone, F the kit. That lets several move
at once.

## What changes elsewhere {#elsewhere}

| Where | What |
|------------------|------------------------------------------------------|
| **The companion's hub** | The SELF and a turn of talk reachable with a body's own key. A body's picture and name. The words a daemon has learned, kept with its SELF, and its lines made ready at night. Later, a turn that streams. |
| **The companion's app** | More than one linked device. A body's page: which daemon, status, STOP, ROAM, where it thinks, its repertoire, its words, the pose page, PRACTICE. |
| **THE BRAIN** | Its interface moves to a repository of its own, now, with a Python file beside the TypeScript. The body fills in the motor regions. |
| **The Zero and its kit** (C-453 to C-466) | Reused: the kit's software, its link and its place in THE MESH were written for the Cardputer Zero. |
| **HANDS (C-462)** | Built, as the gate. Its classes for actions that reach outside are the gate's last row. |
| **The game** | Nothing. |

## Risks {#risks}

| Risk | How likely | What the design does |
|------------------------------|------------------|------------------------------------------------|
| **A servo overheats or strips**, under fur, during PRACTICE | likely, sooner or later | time limits, rest ratios, small steps, a budget; spare servos are cheap and the calibration file survives a swap |
| **The cell is too short-lived** for a session of trials | likely | sessions are short by rule; it can run while charging |
| **A small model writes actions badly** | certain, without help | a grammar it cannot leave; a short list; unknown names dropped silently |
| **Motor noise spoils hearing** | likely | the idle layer freezes while it listens; it does not listen while it walks |
| **The Pi resets when many servos move** | known on the first kit | the motion engine limits how many accelerate together; the kit's version decides the Pi |
| **Bluetooth on a Pi is fiddly** | fair | it carries only small things; everything else has a second road |
| **Learning to walk better takes too long to be fun** | fair | SHOWN gives a new action in minutes; TRIED is the long game and is not on the first path |
| **The kit's prompt is too short for a daemon** | likely | ON BOARD carries a two-line self and a short list; HYBRID sends depth to the house |
| **The Zero has one USB port** | certain | settled on the bench before anything is mounted (Part 12) |
| **The design is larger than the first build** | certain | phases A to D are a daemon in a dog, and they need nothing from Part 10 |

# What you decided {#review .t-CONTEXT}

You read the design on 2026-11-24 and answered its twelve questions by choice. Two of your answers added to the
design, and five things are still open.

## The twelve answers {#questions}

| | The question | Decided |
|------|---------------------|---------------------------------------------|
| **1** | Braces, or the old brackets | **Braces**, `{SIT}`. The old `["sit"]` and `<"mood">` are still read. |
| **2** | Which kit, and which computer | Yours is the first kit (Robot HAT V4). **The Zero 2 W stays in it, with an LLM630 Compute Kit as its brain.** A Pi 5 with the newer HAT may follow. |
| **3** | Who keeps a learned action | **The body.** |
| **4** | May it walk | **Only with ROAM on.** |
| **5** | May it practise alone | **No.** A person is present. |
| **6** | What wakes it | **One word of our own, and a touch.** The word itself is still to be chosen. |
| **7** | Its voice alone | **Its own voice, kept, and words that grow** (Part 10). |
| **8** | Where its tickets live | **A Redmine project and a lane of its own, BODIES.** Its tickets are B-1 onward. |
| **9** | THE BRAIN's interface | **A repository of its own, now.** |
| **10** | The words | **All kept**, DRAFT as ever. |
| **11** | Where this book stands | **On the DESIGNS shelf, and read aloud**, in a voice you pick from three samples. |
| **12** | The second robot | Its name and its API, when you have them. |

## Two things you added {#added}

- **Where it thinks** (Part 9). A setting on every body: ON BOARD, MESH or HYBRID, with HYBRID the one a body
  starts on. A frontier model only when you ask for it and approve it.
- **Learning to speak** (Part 10). Its words start few and grow from talking with you, and each is kept in its
  daemon's own voice.

## Still open {#open}

1. **The wake word itself.** RoverByteOS used "hey rover".
2. **The kit on the bench**: five questions (Part 12).
3. **This book's voice**: three samples for you to choose from.
4. **Whether a daemon's speech also starts small on the phone and the watch.**
5. **The second robot's name and API.**

## Sources {#sources}

::: small
**Your own repositories**, read 2026-11-24: `RoverByte` (RoverByteOS: `ai_interaction.py`, `action_flow.py`,
`preset_actions.py`, `rover_control.py`, `runRoverOS.py`, `api_server.py`; RoverCodeBase; The RoverVerse), `RoverCub`,
`RoverSeer`, `RoverSeerApi`, `PenphinMind`, `CodeMusai`. The companion: `docs/BRAIN.md`, `docs/ZEROKIT.md`,
`docs/MIND.md`, `docs/DEVICES.md`, `docs/INHERITANCE.md`, and the files named in Part 2.

**The PiDog**: SunFounder's `pidog` 1.4.0, `robot-hat` 2.5.8 and `sunfounder-voice-assistant` 1.1.9, read from
source at github.com/sunfounder; docs.sunfounder.com/projects/pidog; the Robot HAT V4 and V5 pages; SunFounder's
forum, for power, heat, the cell and the missing simulator model. Community models: Joel-Baptista/pidog_ros2 and
pidog_rl, EvanJayChou/pidog_rl_policy.

**Speech and small models**: Moonshine (github.com/moonshine-ai/moonshine; arXiv 2602.12241); Silero VAD; Smart
Turn v3 (github.com/pipecat-ai/smart-turn); OHF-Voice/linux-voice-assistant; Piper (OHF-Voice/piper1-gpl) and the
sherpa-onnx speed tables; Arm's and the Stratosphere Laboratory's Raspberry Pi 5 model measurements; llama.cpp's
function-calling and grammar documents; arXiv 2609.07370 on small models and JSON; CNX Software and Jeff Geerling on
the AI HAT+ 2.

**Speech and action together**: GhostShell (arXiv 2508.05298); Pollen Robotics' reachy_mini_conversation_app;
SunFounder's local chatbot example; Pipecat and LiveKit on interruption; ElevenLabs on audio tags.

**Describing a body**: LeRobot's hardware integration guide; Viam's component APIs; ros2_control's hardware
interface; the Reachy Mini SDK; Unitree's, Petoi's and Misty's command APIs.

**Bluetooth**: bluez-peripheral; Improv Wi-Fi (improv-wi-fi.com/ble); Apple's Core Bluetooth background guide;
dotintent/react-native-ble-plx.

**Learning a body**: Bongard, Zykov and Lipson, *Science* 2006; Kohl and Stone, ICRA 2004; Lizotte and others, IJCAI
2007; Calandra and others, 2016; Cully and others, *Nature* 2015 (arXiv 1407.3501); Smith and others on
quality-diversity without a simulator (arXiv 2304.12080); Lee and others on QuadraTot, 2013; Smith, Kostrikov and
Levine, *A Walk in the Park* (arXiv 2208.07860); Wu and others, *DayDreamer* (arXiv 2206.14176); RealAnt (arXiv
2011.03085); Forestier, Mollard and Oudeyer on intrinsically motivated goal exploration (arXiv 1708.02190); Woodman
on inertial drift, 2007; SafeOpt (arXiv 1602.04450); Petoi's Skill Composer; on models proposing and judging
movement: arXiv 2504.20459, 2502.03717, 2306.15724 and 2601.00675.

Numbers quoted from these are their authors'. Nothing in this book has yet been measured on your robot.
:::
