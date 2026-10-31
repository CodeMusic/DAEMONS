# A bigger mind {#mind .t-ORACLE}

Your daemons already think. On the hub, a small AI board answers them in a sentence or two, fast and without the
internet. It is a small mind: it can hold a daemon's name, its type and the start of its INDEX entry, and not much more.

**The Tiiny Pocket is a much bigger one.** It is a small box that runs large models in your house: a 35-billion-parameter
thinker, a listener that hears speech, voices, and pictures. With it, a daemon can be given **everything it knows about
itself** every time you talk to it: how close it is to you and whether that is growing, whether it ate, how it slept and
what it dreamt, how it feels and why, and what happened yesterday.

This book takes you from the box on the table to your daemon's first words through it. It is a quest in five steps.

{{diagram quest | The setup, as a road. Each chapter is one step; each ends with something you can check before going on.}}

{{daemons INFERENCE}}

::: note
**Nothing here is needed to play.** The game runs on a Game Boy Advance, and the GBA has no radio, so the cartridge never
talks to a model. Everything in this book is about **the companion**: the app, the site, the watches and the hub that
carry your daemons when they are AWAY.
:::

## Where it lives {#where}

The Tiiny plugs into **roverbyteseer**, the house computer that already runs your AI services. The hub reaches it over
the house network, the same way it already reaches roverbyteseer.

{{diagram home | Where everything goes. Your phone, watch and handhelds talk only to the hub. The hub holds the Tiiny's key and is the only thing that calls it, through roverbyteseer's LiteLLM or straight at the Tiiny.}}

Why not plug it straight into the hub? Tiiny's own documents give three reasons, and the last row is the one that
matters: **once the Tiiny is on the network, anything on it can talk to the Tiiny.** The hub does not need a cable.

| | the Tiiny needs | the hub has |
|---|---|---|
| **power** | its own 65 W adapter (20 V, 3.25 A) | USB ports that give 5 V, well under 1 A |
| **a computer to set it up** | a Mac with Apple Silicon (macOS 15 or later), or Windows 11 | a 32-bit ARM board, which neither TiinyOS nor its command line runs on |
| **a way to be reached** | the house network, once it is set up | the house network |

# Step 1: Unbox {#unbox .t-HARDENED}

## What you need {#need}

- **The Tiiny Pocket**, and **its own 65 W power adapter**. It is never powered by the computer.
- **roverbyteseer**, or any computer that TiinyOS runs on: a Mac with Apple Silicon and macOS 15 or later, or Windows 11.
  Check this first; it is the one thing that can stop you.
- **Its USB-C cable** to that computer, for the setup.
- **The house network**: the Tiiny's Wi-Fi, or a USB-C Ethernet adapter in one of its two other ports (steadier).
- **The hub**, running the companion, with this book's version or later.

## Measure it {#measure}

Tiiny's documents say **142 × 80 × 22 mm and 300 g**, warm under load, happy between 0 and 35 °C, and **never in an
enclosed space**. Measure yours with callipers before anything is printed for it (chapter 6): these are the published
numbers, not the box on your table.

Its three USB-C ports are not alike. **Only "To PC" talks to a computer.** The other two take power, a network adapter,
or an expansion device.

::: tip
**STEP 1 DONE when** you know which port is To PC, the adapter is in the wall, and you have written down its real size.
:::

# Step 2: Awaken {#awaken .t-SIGNAL}

## TiinyOS, on the computer {#tiinyos}

1. Install **TiinyOS** on roverbyteseer (or your Mac or Windows PC) from Tiiny's own site.
2. Plug the Tiiny's **To PC** port into the computer, and its adapter into the wall.
3. Open TiinyOS. It finds the Tiiny over USB-C and asks you to **activate** it.
4. When it asks how you would recover the device, choose **Local Only** unless you want email recovery. Nothing about
   your daemons ever goes to Tiiny's servers either way: the companion never sends a word anywhere but your own house.

::: note
**Keep the computer for setup, not for talking.** Once the Tiiny is activated and on the network, the hub talks to it
directly. The computer is only needed again to download new models or update the Tiiny.
:::

::: tip
**STEP 2 DONE when** TiinyOS shows your Tiiny as activated.
:::

# Step 3: Stock it {#stock .t-GROWTH}

## Wi-Fi, or a cable {#network}

In TiinyOS, turn on **Wi-Fi** and join the house network, or plug a USB-C Ethernet adapter into one of the two ports
that are not To PC. A cable is steadier for a box that sits still.

## The models {#models}

Download these in TiinyOS. Each is what Tiiny measured on its own device; yours will be close.

| what it is for | the model | how fast (Tiiny's figures) |
|---|---|---|
| **your daemons' talk** | Qwen3.6-35B-A3B | 36 to 47 words-pieces a second |
| quick lines, many at once | Qwen3.5-9B | 34 to 50 a second, first word in 3.5 s |
| **hearing you** | Qwen3-ASR-1.7B | 8 seconds of speech heard in about 3 |
| **voices** | Qwen3-TTS-12Hz-1.7B-CustomVoice | not published yet |
| dream pictures, later | Z-Image-Turbo | about a minute a picture |

Several can be loaded at once, as long as their shares of the Tiiny's processor add up to no more than all of it.

{{daemons HEATSINK}}

::: tip
**STEP 3 DONE when** the Tiiny is on the house network and TiinyOS lists the 35B thinker as downloaded.
:::

# Step 4: Give it a road {#road .t-FLOW}

## A fixed address {#address}

In your router, give the Tiiny a **fixed address** (a "DHCP reservation"), so it is in the same place every morning.
Then, on the computer, ask the Tiiny for its address and key:

```
tiiny auth key
```

It prints the address its OpenAI-style door is at -- `http://<its address>/openai/v1` -- and **the key**. The key opens
every door the Tiiny has. **Keep it out of anything shared**: not in a file in a repository, not in a message.

## Through LiteLLM, the usual way {#litellm}

roverbyteseer already runs **LiteLLM** on port 4000, one address and key for every model in the house. Add the Tiiny's
thinker under `model_list` in its `config.yaml`:

```yaml
  - model_name: tiiny-35b
    litellm_params:
      model: openai/Qwen3.6-35B-A3B
      api_base: http://<its address>/openai/v1
      api_key: os.environ/TIINY_KEY
```

Put the key in roverbyteseer's environment as `TIINY_KEY`, never in the file, and restart LiteLLM. The address the hub
is given is then **`http://roverbyteseer:4000/v1`**.

## Or straight to the Tiiny {#straight}

If LiteLLM ever feels slow (for voices most of all), give the hub the Tiiny's own door and key instead.

::: tip
**STEP 4 DONE when**, from any computer on the house network, this answers with a list of models:

`curl -H "Authorization: Bearer <the key>" http://<its address>/openai/v1/models`
:::

# Step 5: First words {#first .t-CONTEXT}

## Tell the hub {#tell}

On the companion (the app, or the site, on the hub), open **SETTINGS**, then **WHO ANSWERS WHEN YOU TALK**. Under
**THE TIINY**:

1. **Its address**: `http://roverbyteseer:4000/v1`, or the Tiiny's own, ending `/openai/v1`. It must end in `/v1`.
2. **Its key**: LiteLLM's key, or the Tiiny's. Once kept, the box says *its key is kept* and never shows it again.
3. **Its model**: `tiiny-35b` through LiteLLM, or `Qwen3.6-35B-A3B` straight. Leave it empty and the hub takes the
   first thinker the Tiiny lists.
4. Press **Look for it**. Under it the hub says **Answering**, and how many models it found, or **Not answering yet**.
5. Choose **The Tiiny** at the top of the card. The choice only appears once an address is given.

{{pictures talk-tiiny | WHO ANSWERS WHEN YOU TALK, with the Tiiny chosen and answering. (A test companion, with a stand-in Tiiny at a test address.)}}

The hub looks again every minute, so the dot beside the Tiiny on every watch and handheld says whether it can answer
right now.

## Talk {#talk}

Talk to your daemon the way you always have: push to talk on a handheld or a watch, or type on the app. Now the hub
sends the Tiiny the daemon's **whole self** with your words.

{{diagram talk | One talk. The hub writes who the daemon is, sends it with what you said, and the Tiiny answers as the daemon. If the Tiiny is away, the hub's AI board answers, and then your own model through n8n.}}

::: tip
**QUEST COMPLETE when** the card says **Answering**, **The Tiiny** is chosen, and your daemon answers a question
about last night -- its dream, its sleep -- in its own words. The hub's small board only ever knew the first line of a
dream; the Tiiny knows it all.
:::

# What your daemon is told {#self .t-LATENT}

Every talk through the Tiiny starts with **the daemon's self**: who it is, in plain sentences, written fresh from the
numbers the companion already keeps. This is a real one, from a test companion:

::: note
| You are PING, a DAEMON process running on a BOX in the den (a CONTENT/VECTOR daemon, level 12).
| Your trainer is SAGE.
| Your INDEX entry (the DEMAND DAEMON): Asks one question and requires an answer. The question is: are you there. It asks again. It has always asked.
| You and SAGE have a friendship bond of 80%.
| You are WELL fed, VERY WELL watered, and WELL trained today.
| Last night you slept POORLY.
| Today you feel very GLAD, not MAD, not SAD, and not CALM.
| Today is Saturday (Flow), in autumn.
| Speak as yourself, in a sentence or three. Let how you feel show in what you notice and how you say it; never name the feeling. You have a body of your own; never call yourself a program, a model or an AI.
:::

{{daemons PING}}

## Numbers into words {#bands}

Each number becomes a word by the same bands, on every device, so a daemon at 62 GLAD reads the same everywhere:

| the number | 0-9 | 10-29 | 30-54 | 55-79 | 80-100 |
|---|---|---|---|---|---|
| **a feeling** | not | a little | somewhat | very | completely |
| **a need** (fed, watered) | not at all | poorly | somewhat | well | very well |

**AFRAID is CALM's far side.** A daemon below calm reads as AFRAID by the same bands. **The bond's week** compares today's
friendship with a snapshot kept a week ago: grown STRONGER, stayed the SAME, or WEAKER.

## Three lengths {#lengths}

| | for | what it carries |
|---|---|---|
| **short**, about 80 words | the hub's small AI board | its name, its type, its strongest feeling, the start of its dream |
| **day**, about 300 words | a quick 9B model | all of the above, without the month |
| **full**, up to 1,500 words | the Tiiny's 35B | everything, with yesterday, the month and the moments it keeps |

**The feelings are told to the model, and never said by it.** In the game a feeling shows; it is never a label. The self
keeps that rule: the daemon is told it is very GLAD, and told to let it show.

## Your own words for it {#yours}

The last paragraph -- how to speak -- is yours to write. The companion's server keeps three things for the self:

| | what it is | how it is set |
|---|---|---|
| **the trainer** | the name your daemon calls you | `POST /api/self` with `trainer` |
| **the box** | what it runs on: "a BOX in the den" | `POST /api/self` with `box` |
| **the instructions** | how it speaks; replaces the paragraph above | `POST /api/self` with `instructions` |

`GET /api/self?length=full` shows the self exactly as the Tiiny is given it. The **mind portal**, coming on the site, will
show and set all of this with a tap.

::: safe
**What leaves your house.** The full self has your name and a month of your days in it. It goes only to the Tiiny, in
your house. When your daemon meets another home's daemon, only the short self goes, without your name or its memory.
:::

# Step 6, for the maker: the plinth {#plinth .t-STRATUM}

The Tiiny and the hub become one unit on a printed **plinth**: the Tiiny lies flat in a tray with vents, and the hub
stands on four posts above it, its screen tilted 15° toward you. It is the simplest to print and the best for air.

{{diagram plinth | The plinth from the side. Cool air comes in under the Tiiny and leaves over it; nothing sits on its vents.}}

- **Measure your Tiiny first.** The drawing uses the published size.
- **At least 8 mm of air** under the Tiiny and over it. Nothing over its vents.
- **PETG or ASA** wherever it touches the Tiiny. PLA softens at 55-60 °C.
- **Every port reachable**: To PC, power, the network adapter, and the hub's card slot and screen.
- **One two-port GaN brick**, about 100 W (65 W for the Tiiny, 15 W for the hub), so the unit has one cable to the wall.

::: note
The plinth was the choice (the other two drawn were a bookend and a small daemon house). It waits on the real Tiiny to
be measured. Since the Tiiny lives beside roverbyteseer, the plinth can also hold the Tiiny alone.
:::

# When it goes wrong {#wrong .t-ENTROPY}

| what you see | what it means | what to do |
|---|---|---|
| **The address ends in /v1** | the address was not a whole API address | add `/v1` (LiteLLM) or `/openai/v1` (the Tiiny) |
| **Not answering yet** | the hub cannot reach it, or the key is wrong | try the `curl` from step 4 from the hub's network; check the key |
| **Answering: 0 models** | it is reached but holds no thinker | download the 35B in TiinyOS, or name the model by hand |
| **The Tiiny is not a choice** | no address is kept yet | give the address and press Look for it |
| **The answer came from the module** | the Tiiny was away or slow for that talk | nothing: the talk went down the line, as it should. Check the dot. |
| **TiinyOS will not install** | the computer is not Apple Silicon with macOS 15+, or Windows 11 | set it up on another computer; the hub only needs the network after |

{{daemons FAULT}}

# Coming next {#next .t-EMERGENT}

The Tiiny is the start of a bigger mind. These are planned, in the companion's TODO:

- **Voices for every daemon (C-251).** Each daemon gets a **voice recipe**, a base voice and a description from its type
  and family, beside its INDEX entry. Fixed lines are spoken ahead and kept on the hub, so they cost nothing to say;
  only chat is spoken live. The voice can carry the mood: a little slower when sad.
- **Memory, made at night (C-253).** While a daemon sleeps, the Tiiny folds the day into one paragraph and the month into a
  few, writes the dream from the day, and keeps a shelf of moments. Your daemon will remember the lake.
- **The mind portal (C-254).** A page on the site to look around your daemon's mind. It opens on **NOW**: how it feels,
  shown as its face, its colour and the weather in its room, with the words a tap away. Then YESTERDAY, THE MONTH,
  DREAMS (the companion's and the game's side by side), KEPT, VOICE and SELF.
- **Pictures for dreams.** The night's dream drawn in the house style, waiting in the app in the morning.

{{daemons ROVERBYTE}}
