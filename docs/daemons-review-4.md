---
title: The Fourth Review
---

# About this review {.t-CONTEXT .unnumbered}

**The Fourth Review** reads DAEMONS as **one product**: a game you play, a daemon you can bring out of the game onto
your phone or a small device, and a mind for it that runs on hardware you own. The three earlier reviews read the
design bible; this one reads the bible, the books, the game's source, the companion's source and the playground, and
measures each against the others.

## What it was read against

| | |
|--|-------|
| **Review** | **4, revised** -- *The Fourth Review*, first printed 3 November 2026 at v11.338, **revised 14 November 2026 for v11.361** |
| **Design bible** | **v11.362** (`docs/vision.md`, 9,500 lines) -- DAEMONS repo at `b924932d`. *First printing: v11.338 at `1f9f03cb`* |
| **Newest release** | **v11.361.1** (14 November 2026, the GATEKEEPER), built against bible v11.361. *First printing: v11.337.4* |
| **The game** | CodeMusic/pokefirered-daemons, `context-content` at `8184c63` (release engine `dc780f8c5`) |
| **The companion** | CodeMusic/daemons-companion at `49f2da0` |
| **The playground** | CodeMusic/daemons-playground at `6e8ca37` |
| **Earlier reviews** | First (2026-08-31), Second, *The Third Review* (2026-09-10, bible v11.111), ruled on in bible 8.7 |

**This revision re-checked every one of the 46 findings against v11.361** and marks each FIXED, PARTLY, OPEN or
NOT RE-CHECKED (Part 2, and the appendix). The first printing's broad measurements -- the text census, the sprite
count, the story's sequence -- were not re-run unless a finding depended on them; where a number is still the v11.338
one, it says so. **When the bible moves past v11.362, this revision starts to age.**

## How it was read

Four lenses, each read separately and then put together: **the core story** and its sequence into the islands;
**the side stories and the books**; **the game as built**, measured block by block against a fresh copy of the
original decompilation; and **the companion and its AI**. **Nothing here comes from playing a ROM** -- no ROM was
built for this review. The numbers come from the source; the readings are labelled as readings.

The tags are the Third Review's, with one added:

[BREAK]{.tag .BREAK} a contradiction in the canon, the ROM or a published file ·
[DRIFT]{.tag .DRIFT} text the project has since overruled and not swept ·
[FREE]{.tag .FREE} a win already sitting in vanilla or the project's own rules ·
[IDEA]{.tag .IDEA} outside the box, take or leave ·
[RISK]{.tag .RISK} not wrong yet, but where it will go wrong.

::: note
**What this review never prints.** The four things the player is meant to work out appear nowhere below; where a
finding touches one it says *a private secret* and stops. No real person is named, and the frightening word the
name is mistaken for is never written. Where a finding is itself about something private, the detail went to the
author directly and the page says only that it exists.
:::

# The verdict, up front {.t-CONTEXT}

DAEMONS is **the most thoroughly argued fan game this reviewer has read, and the most finished at the level of
names and pictures** -- and it is now at the point where its biggest risk is no longer design, but **breadth over
finish**. The thesis holds. The main story is built. The islands carry an Act 2. What has not happened is the thing
the project's own scope rule exists to force: **someone playing it from a new game to the last scene, and the record
of it being read.**

::: verdict
<div class="t-CONTEXT"><b>Thesis</b><span>Holds, and is in the ROM</span><p>LOGIC ½ CONTEXT still survives every lens. The chart is the argument, byte-identical across both editions.</p></div>
<div class="t-VECTOR"><b>Biggest crack</b><span>The third book</span><p>The one exception to craft rule 1 has lost both of the reasons it was allowed -- while its reach grew to three books.</p></div>
<div class="t-ENTROPY"><b>Biggest risk</b><span>Breadth over finish</span><p>New subsystems keep arriving while the font, the region map, the battle music and the villains' barks are still vanilla.</p></div>
<div class="t-GROWTH"><b>Cheapest big win</b><span>Play it through, once</span><p>One recorded playthrough of each edition to the end of Act 2 is worth more than the next feature.</p></div>
<div class="t-SIGNAL"><b>Best idea in the product</b><span>The round trip</span><p>Raise it in the game, carry it in your life, bring it home changed. Nobody else has this.</p></div>
<div class="t-LATENT"><b>Biggest product gap</b><span>Talk is unfiltered</span><p>Since v11.338 a phone alone can talk, to any endpoint the player links. Nothing yet checks what comes back.</p></div>
:::

## The scorecard

A reading, not a measurement: how far each part is from what its own design asks of it. *Revised for v11.361: only Local AI moved enough to re-score.*

::: scores
| Part | | Where it stands |
|------|-----|---------|
| **The thesis and the chart** | <span class="bar t-CONTEXT"><i style="width:92%"></i></span> | Argued, built, consistent across editions |
| **Names, sprites, Index** | <span class="bar t-GROWTH"><i style="width:96%"></i></span> | 99.8% of sprites redrawn; no brand word left |
| **The main story, Act 1** | <span class="bar t-LOGIC"><i style="width:78%"></i></span> | Key scenes rewritten; the villains' barks mostly vanilla |
| **Act 2, the islands** | <span class="bar t-FLOW"><i style="width:66%"></i></span> | The beats are in; 57% of island text is vanilla by policy |
| **Side stories and books** | <span class="bar t-SIGNAL"><i style="width:74%"></i></span> | The early ones load-bearing; the late ones crowding |
| **Story continuity** | <span class="bar t-ENTROPY"><i style="width:68%"></i></span> | Rulings land faster than the sweeps behind them |
| **Sound** | <span class="bar t-LATENT"><i style="width:30%"></i></span> | 30 of 110 tracks ours; every battle theme vanilla |
| **The companion** | <span class="bar t-SIGNAL"><i style="width:70%"></i></span> | The loop is real and careful; onboarding is long |
| **Local AI** | <span class="bar t-LATENT"><i style="width:72%"></i></span> | Any endpoint, from the hub or the phone, and on-device; unfiltered, untried by hand |
| **Verification** | <span class="bar t-VECTOR"><i style="width:45%"></i></span> | Superb static checks; no end-to-end play on record |
:::

## The numbers

::: stats
<div class="stat t-GROWTH"><b>99.8%</b><span>of 1,476 sprites redrawn, plus 115 new</span></div>
<div class="stat t-CONTEXT"><b>0</b><span>vanilla brand words in 14,194 lines of player text</span></div>
<div class="stat t-LOGIC"><b>398</b><span>of 412 daemon names ours</span></div>
<div class="stat t-FLOW"><b>3,472</b><span>map text blocks: 40% still vanilla, 60% touched</span></div>
<div class="stat t-ENTROPY"><b>186</b><span>releases in 38 days, each with four patches</span></div>
<div class="stat t-SIGNAL"><b>20,311</b><span>lines of new engine C in 33 files</span></div>
<div class="stat t-LATENT"><b>30 / 110</b><span>songs ours</span></div>
<div class="stat t-HARDENED"><b>494 / 520</b><span>tickets closed</span></div>
<div class="stat t-VECTOR"><b>0</b><span>recorded playthroughs from new game to the end</span></div>
:::

# What moved, v11.338 to v11.361 {.t-HARDENED}

Twelve days, **24 bible versions** (v11.339 to v11.362), **20 release groups** and **386 design commits** after the
first printing. Every finding was re-checked against the source at v11.361.1. The short version:

::: verdict
<div class="t-GROWTH"><b>Most improved</b><span>The companion's mind</span><p>A phone alone now talks: to Apple's on-device model, the hub, or any OpenAI-compatible endpoint the player links -- one mind across all three.</p></div>
<div class="t-GROWTH"><b>Most improved, the game</b><span>The first screens</span><p>Our own font; every place card ours; every General tile ours; every landmark ours but USER TOWER; the SAFARI is THE WALLED GARDEN.</p></div>
<div class="t-ENTROPY"><b>Unmoved</b><span>The finishing list</span><p>No playthrough on record; the private sweep, the chart reprint and the TODO tidy all still open.</p></div>
<div class="t-VECTOR"><b>Grew</b><span>The third book</span><p>THE UNITY BOOK is built, with an aurora, a fox, a duet and a tablet. Its exception was not narrowed.</p></div>
:::

## What was added in those twelve days

The scope-discipline finding is not a criticism of any one of these; each is well made and most were chosen by the
user line by line. It is the list, read together, against the one under *Unmoved*.

| Added | Where | Kind |
|------------|--|---|
| **THE UNITY BOOK built** -- covers, the torn lines mended, the lens, HALFTONE's tones, the aurora, TULIKKO's sparks, the DUET | 4.40 | the third book |
| **THE BLANK TABLET** by BLANCHE's path, read one face per half | 4.39 | the third book |
| **THE ORIGIN OF A DAEMON**, MUSAI's book; the MUSAI branch's 24 seasonal forms | 9.34, 9.35 | new book, new art |
| **A day's symbol** for each weekday | 9.21 | calendar |
| **IN ITS OWN WORDS** -- each daemon's first-person telling, in the companion only | 4.2 | companion |
| **THE WALLED GARDEN** (the SAFARI ZONE, 76 of 85 lines rewritten) and **the GATEKEEPER** | 3.11 | **finishing** |
| **Our font; every place card; every General tile; six landmark pairs; THE BLACKOUT** | 9.29 | **finishing** |
| **The physical/special split**, steps 1 and 2 released | 2.12 | **finishing** |
| **Corpus's last warehouse admins** as 8.2a's remnants (T-505) | 4.37 | **finishing** |
| **Any thinker** on the hub and the phone; **THE MIND** across phone, hub and endpoint | C-280, C-307 | **the endpoint plan** |

**Five of ten are finishing work**, against roughly one in three in the fortnight before the first printing. That is
the right direction, and it should be said plainly.

## Every finding, re-checked

[FIXED]{.tag .FREE} done at v11.361 · [PARTLY]{.tag .DRIFT} moved but not closed · [OPEN]{.tag .BREAK} unchanged ·
[NOT RE-CHECKED]{.tag .RISK} a reading, or a measurement not re-run.

| Finding | Now | Evidence at v11.361 |
|----------|---|------------|
| **A phone-only player has no AI at all** | [FIXED]{.tag .FREE} | `app/platform/endpoint.ts` and `mesh.ts`: an endpoint from the phone, the on-device model, THE MIND (C-280, C-307). *Not yet tried by hand* |
| **Four designs of the third book, and no build** | [FIXED]{.tag .FREE} | THE UNITY BOOK is in 21 engine files, released from v11.348.2 |
| **The first-screen vanilla** | [PARTLY]{.tag .DRIFT} | Font, place cards, General tiles, landmarks done; **region map (T-449) and every battle theme still vanilla** |
| **Say the unrenamed nouns out loud** | [PARTLY]{.tag .DRIFT} | SAFARI 34 → 2 (THE WALLED GARDEN); S.S. ANNE 13, GAME CORNER 13, BIKE 14 unchanged |
| **The books disagree about the books** | [PARTLY]{.tag .DRIFT} | THE SUBTLE LAYER's count fixed (51, v11.357); the GUIDE's three counts still differ |
| **Four lexicon rows** | [PARTLY]{.tag .DRIFT} | DAEMON LEAGUE 35 → 20 beside REVIEW BOARD 24 -- still two names; CERT still in the lexicon |
| **Bring your own mind: the endpoint plan** | [PARTLY]{.tag .DRIFT} | Registry, keys and the *at home* ring built; probe, tiers, Ollama's context and the output pipeline not |
| **Nobody has played it from a new game to the end, on record** | [OPEN]{.tag .BREAK} | T-50 still open, still the oldest; no route spans BLANCHE to the end |
| **What a daemon says is never filtered** | [OPEN]{.tag .BREAK} | `safeLine()` still runs only on meetings and the household talk -- **and now any endpoint can answer** |
| **A tracked file tags a private sequence** · **the bible sentence passed on privately** | [OPEN]{.tag .BREAK} | Both still in the public tree |
| **The published type chart is garbled** | [OPEN]{.tag .BREAK} | Still 237 broken characters; still no charset |
| **"PROF. CRYSTAL", twice** | [OPEN]{.tag .BREAK} | Both strings still in the lab's text |
| **"Never in a room"** | [OPEN]{.tag .BREAK} | Still in 8.2a and the warehouse script's comment |
| **The witching hour needs a real clock** | [OPEN]{.tag .BREAK} | `DaemonsIsWitchingHour` unchanged |
| **The Hermetic text settles 4.33's question** | [OPEN]{.tag .BREAK} | SUBSTRATE unchanged, unattributed |
| **The one exception has lost its warrants** | [OPEN]{.tag .BREAK} | Not narrowed; THE UNITY BOOK built around it |
| **HALFTONE's colour returns** | [OPEN]{.tag .BREAK} | Deepened, not reversed (v11.340); 3.7 still says it stays grey |
| **Eight tickets filed under Closed** | [OPEN]{.tag .BREAK} | **Now ten or more**: T-521, T-522, T-523 joined them |
| **Phone backups never pruned; writes not atomic** | [OPEN]{.tag .BREAK} | `app/platform/local.ts`: same write, same backup, no prune |
| **The store record describes a different app** | [OPEN]{.tag .BREAK} | `APPSTORE.md` still answers *no gambling* |
| **CI, for free** | [OPEN]{.tag .BREAK} | One workflow builds the site; no tests run, none in the app |
| **Sign the patch list** · **the emulator's CDN, no cache** | [OPEN]{.tag .BREAK} | `patches.json` still read live from `main` |
| **Two voices skip DAY-mons** | [OPEN]{.tag .BREAK} | `app/AGENTS.md` still lists both as *not covered yet* |
| **The playground serves built ROMs** | [OPEN]{.tag .BREAK} | Unchanged |
| **The rival's naming device** · **6F's ghost story** · **the hideout's barks** · **"I understand now"** · **"It could not have"** · **the Verdigris kid** · **Ty at Quicksilver** | [OPEN]{.tag .BREAK} | All unchanged in the ROM and the bible. T-505 rewrote the warehouse's admins' battle lines, but Admin 1's *"I understand now…"* is still spoken after the fight |
| **T-506 unswept** · **school.md says nothing is built** · **the stale reservation** · **CLAUDE.md's v11.296** · **`still-vanilla.md`** · **no text census** · **understandings "THE MARGINS only"** | [OPEN]{.tag .BREAK} | All unchanged |
| **The pacing risks** · **Ty a stranger** · **thirteen systems** · **the near-miss** · **the facing-page binding** · **the ferry** · **ordering the exception** · **the chart is vanilla's** · **onboarding** · **the emulator risk** | [NOT RE-CHECKED]{.tag .RISK} | Readings: nothing in the twelve days answers them. The systems count has grown by at least four |


> **FIXED by v11.361: the phone talks to its own on-device model or to any endpoint the player links, with the hub as one more mind (C-280, C-307). Not yet tried by hand.**

> **PARTLY by v11.361: THE WALLED GARDEN took SAFARI from 34 to 2. The other three are unchanged.**

> **OPEN at v11.361, and more urgent: any endpoint can now answer, from the phone too.**
::: callout
**The one to do first has not changed: play it through, once, and read the record.** And one has become more urgent:
**the output filter.** At v11.338 an unfiltered answer came from a 0.5B model on the user's own board. At v11.361 it
can come from *any* model a player points the phone at.
:::

# What DAEMONS is, as one product {.t-SIGNAL}

Three pieces, and one loop through them. Every other part of the project -- the books, the dreams, the casino, the
boards -- hangs off that loop. **It is the right thing to build everything around.**

::: diagram
<svg viewBox="0 0 520 250" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">
<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#16161a"/></marker></defs>
<rect x="10" y="20" width="150" height="120" rx="8" fill="#fff" stroke="rgb(176,86,158)" stroke-width="2.5"/>
<text x="85" y="44" text-anchor="middle" font-size="12" font-weight="800" fill="rgb(176,86,158)">THE GAME</text>
<text x="85" y="62" text-anchor="middle" font-size="8.5" fill="#33333a">CONTENT · CONTEXT</text>
<text x="85" y="78" text-anchor="middle" font-size="8.5" fill="#33333a">your own ROM, patched</text>
<text x="85" y="94" text-anchor="middle" font-size="8.5" fill="#33333a">mGBA · Delta · flash cart</text>
<text x="85" y="110" text-anchor="middle" font-size="8.5" fill="#33333a">the one app · the playground</text>
<text x="85" y="128" text-anchor="middle" font-size="8" fill="#5a5a64" font-style="italic">the party menu: SEND</text>
<rect x="185" y="20" width="150" height="120" rx="8" fill="#fff" stroke="rgb(86,190,190)" stroke-width="2.5"/>
<text x="260" y="44" text-anchor="middle" font-size="12" font-weight="800" fill="rgb(40,140,140)">THE COMPANION</text>
<text x="260" y="62" text-anchor="middle" font-size="8.5" fill="#33333a">server · iPhone · iPad · Mac</text>
<text x="260" y="78" text-anchor="middle" font-size="8.5" fill="#33333a">widget · watch · boards</text>
<text x="260" y="94" text-anchor="middle" font-size="8.5" fill="#33333a">feeds · sleeps · dreams</text>
<text x="260" y="110" text-anchor="middle" font-size="8.5" fill="#33333a">one next step = a meal</text>
<text x="260" y="128" text-anchor="middle" font-size="8" fill="#5a5a64" font-style="italic">writes the save: SYNC</text>
<rect x="360" y="20" width="150" height="120" rx="8" fill="#fff" stroke="rgb(92,70,118)" stroke-width="2.5"/>
<text x="435" y="44" text-anchor="middle" font-size="12" font-weight="800" fill="rgb(92,70,118)">THE MIND</text>
<text x="435" y="62" text-anchor="middle" font-size="8.5" fill="#33333a">AX630 module (runs)</text>
<text x="435" y="78" text-anchor="middle" font-size="8.5" fill="#33333a">LM Studio via n8n (runs)</text>
<text x="435" y="94" text-anchor="middle" font-size="8.5" fill="#33333a">Tiiny (built, not yet run)</text>
<text x="435" y="110" text-anchor="middle" font-size="8.5" fill="#33333a">any /v1 endpoint (planned)</text>
<text x="435" y="128" text-anchor="middle" font-size="8" fill="#5a5a64" font-style="italic">hold to talk</text>
<path d="M160,60 L183,60" stroke="#16161a" stroke-width="1.5" marker-end="url(#ar)"/>
<path d="M183,100 L162,100" stroke="#16161a" stroke-width="1.5" marker-end="url(#ar)"/>
<path d="M335,80 L358,80" stroke="#16161a" stroke-width="1.5" marker-end="url(#ar)"/>
<path d="M358,104 L337,104" stroke="#16161a" stroke-width="1.5" marker-end="url(#ar)"/>
<text x="171" y="54" text-anchor="middle" font-size="7" fill="#5a5a64">SEND</text>
<text x="171" y="114" text-anchor="middle" font-size="7" fill="#5a5a64">SYNC</text>
<rect x="10" y="170" width="500" height="64" rx="8" fill="#f0eee6" stroke="#d8d6ce"/>
<text x="260" y="192" text-anchor="middle" font-size="10.5" font-weight="800" fill="#16161a">THE ROUND TRIP</text>
<text x="260" y="210" text-anchor="middle" font-size="9" fill="#33333a">raise it in the game  →  SEND it AWAY  →  it lives on a device, keeps its day, talks</text>
<text x="260" y="225" text-anchor="middle" font-size="9" fill="#33333a">→  SYNC: it goes home with friendship, growth, dreams and money it earned out here</text>
</svg>
:::

## The journey, as a new player meets it

| # | Step | State |
|-|------------|-----|
| 1 | **Get the game** -- your own FireRed or LeafGreen; the one app patches it on the device and checks every hash, or a BPS patch from a release, or the playground | [BUILT]{.tag .BUILT} the one app in TestFlight |
| 2 | **Play** -- an emulator core in the app, controllers and keyboards, the iPad's split screen with the companion beside the game | [BUILT]{.tag .BUILT} |
| 3 | **Unlock SEND** -- the companion's first SYNC links the save; only then does the party menu offer SEND | [BUILT]{.tag .BUILT} |
| 4 | **SEND a daemon AWAY** -- the game only asks; the companion answers at SYNC, re-signs the save and keeps a backup first | [BUILT]{.tag .BUILT} and tested |
| 5 | **It lives somewhere** -- the phone and its widget, about twenty boards, a Tab5, a BOX-3 | [BUILT]{.tag .BUILT} phone; [PARTIAL]{.tag .PARTIAL} several boards not yet run |
| 6 | **It talks** -- hold to talk, speech to text, a model answering as the daemon, text to speech | [BUILT]{.tag .BUILT} *v11.361*: phone, hub or any endpoint; untried by hand |
| 7 | **It remembers** -- the self in three lengths is built; night memory and the mind portal are designed | [DESIGNED]{.tag .DESIGNED} |
| 8 | **SYNC home** -- friendship, growth, evolution, casino money and gifts written back; RECEIVED says what arrived | [BUILT]{.tag .BUILT} |

**The game-side loop is real and unusually careful.** The AI half was, at v11.338, **only for a household that already
ran a computer or a hub**; by v11.361 a phone alone can give its daemon a voice.

# Strengths {.t-GROWTH}

The things this project does better than almost anything in its genre. Each is checkable.

## The argument is in the mechanics, not the mouths

- **The chart is the thesis, and it never says so.** LOGIC beats CONTENT ×2 and is resisted by CONTEXT; nobody in the
  game explains why. Craft rule 1 -- *no character ever explains the colour-emotion link* -- has held for 338
  versions of the bible.
- **The type chart is byte-identical across both editions** (invariant 3); it lives in the engine outside the edition
  switches. An argument that changed by cartridge would not be one.
- **The starters are three ways a machine learns** -- reward, example, unsupervised -- and their final stages are the
  paradigms' failures side by side: CANON *files new things as errors*, MANIFOLD *can show you the shape, not a name*.

{{sprite.named ROVERBYTE CANON MANIFOLD}}

## It is finished where players look first

- **No brand word survives.** Across 14,194 lines of player text: `POKéMON` 0, `ROCKET` 0, `GIOVANNI` 0, `KANTO` 0,
  `SEVII` 0, every vanilla town name 0. The original staff are kept in the credits, on purpose.
- **99.8% of the sprites are redrawn** (1,473 of 1,476), measured by pixel against the original by a census tool,
  not by memory -- plus 115 new ones. 398 of 412 daemon names, 363 of 383 moves, 240 item names and 275 item
  descriptions are new.
- **27 maps vanilla never had**: seven school floors, fourteen groves, THE NEXUS and more.

## The writing systems are structural

- **The RESEARCH NOTEBOOK files documents in an authored order**, not the order they are found -- *"the file reads
  correctly when it is complete and never while it is not."* The player practises exactly the reading the ending
  needs, and nobody tells them so. It is the best idea after the chart.
- **CALLOW SCHOOL's exam is the inverse of the villain's rigged test, clause by clause** -- a published pass mark,
  leave mid-paper, retake forever -- and nothing in the game draws the comparison.
- **The islands' tone rule is checkable on a single line**: the mainland *declares, instructs, assesses*; the
  islands *ask, or offer a second reading.* Measuring it shrank a 9,500-word rewrite to eighteen blocks.
- **The second joining (4.37) is the best late writing** -- a merger that holds both halves, told only through
  papers and signs, *never in her mouth*.

## The engineering habits are rare

- **"Edit the source, never the artifact"** is enforced: generator checks, a sandboxed write check, a drift guard on
  fifteen tools that refuses to overwrite later hand work, and a fresh-clone build compared byte for byte.
- **`check_reach.py`** walks every map from where a player arrives -- it found a man standing in the only doorway who
  had hidden the ending for fifteen days, when every other check passed.
- **43 engine traps documented by symptom.** *Never grep a build for `error:`* is the kind of memory that saves days.
- **Tickets measure before they build.** T-26 shrank by an order of magnitude because someone counted first.

## The legal line is drawn in code

- **No ROM in any repository.** Four BPS patches a release, made against byte-identical builds of retail and checked
  by patching a real retail ROM. The one app checks the player's dump by hash, downloads the patch, checks it,
  applies it and checks the result. It holds nothing of Nintendo's and collects nothing for its developer.

## The companion respects the save and the small model

- **A backup before every write**, sector checksums re-signed, the last battler always stays home, and an in-game
  recall if the companion is gone.
- **The AX630's real quirks are measured and engineered around** -- a pooled-prompt bug, a ~350-token window, slot
  leaks -- with fault counters. Models are discovered from `/v1/models`, not assumed. A daemon's self is written in
  three lengths, its feelings *named to the model, never by it*.
- **One function respells DAEMONS as DAY-mons** for every voice, and a list says which speech paths it covers.

# The core story, in the order a player meets it {.t-LOGIC}

The arc that 4.34 designed is **in the ROM, scene by scene** -- a long way from the Third Review's *"designed and
never staged."* Below is the order a player meets it, checked beat by beat against the game's scripts, flags and
text. **"Built" means the words and flags exist in the source**; it does not mean anyone has played them through.

{{frame crystal|"The intro: CRYSTAL CLEAR, with no title." town|"The first town."}}

## Act 1 -- where you are assessed

::: {.arc}
1. **The intro.** CRYSTAL CLEAR welcomes you, without a rank. *"Some of them disagree."* The rival is named by being
   *remembered*: *"This is my grandchild… Do you remember his name?"* [BUILT]{.tag .BUILT} *(departs from 4.3 -- see continuity)*
2. **BLANCHE and the lab.** The daemon chooses you; the INDEX is handed over; then the errand -- the CALLOW REPO hands
   you **a CC-7** for Crystal. It is the longest fuse in the game. [BUILT]{.tag .BUILT}
3. **Route 1 → CALLOW → THE UNDERTONE → SLATE.** The local names on the signposts; CALLOW SCHOOL and the NOTEBOOK
   open; **BENCHMARK 1, CAIRN** -- the SLATE MARK. [BUILT]{.tag .BUILT}
4. **DEADSTACK.** Corpus's first appearance, in procedure: *"CORPUS is a people-first organisation! The DAEMONS are
   inventory."* [BUILT]{.tag .BUILT}
5. **DOLDRUM, BENCHMARK 2 (BASIN)** -- the room is the lever; the guard at DOLDRUM CAVE. **ARDOR and the ship,
   BENCHMARK 3 (GAUGE).** [BUILT]{.tag .BUILT}
6. **VERDIGRIS, BENCHMARK 4 (TRELLIS), and the HIDEOUT.** Scorn introduces himself -- *"Richard Scorn. I run the
   numbers upstairs. Show me what you have. I like to see it measured."* -- and hands over the RESOLVER. A letter
   signed TY on the condominium roof. [PARTIAL]{.tag .PARTIAL} *his lines ours; the grunts' vanilla*
7. **HALFTONE and DAEMON TOWER.** The RESOLVER unmasks the tower's ghost; Corpus on the top floor -- *"DAEMONS are an
   asset class. Nothing personal!"* A second letter on 2F. [PARTIAL]{.tag .PARTIAL} *6F still vanilla's ghost story*
8. **LURID, BENCHMARK 5 (TILT).** Status as the lever. [BUILT]{.tag .BUILT}
9. **BRAZEN and Corpus HQ.** The floors written in procedure -- *"I will have to raise a ticket."* A letter in the
   formal register on 3F. **BENCHMARK 6 (MATTE).** [BUILT]{.tag .BUILT}
10. **QUICKSILVER.** The gold-leaf sign -- SCORN SOLUTIONS laid over CLEAR LABORATORY, *"where it has lifted, the
    older letters show"* -- the founder's plate, the CC-7 on a requisitions board with *IMPROVE RESPONSE
    CONSISTENCY* beside it, the burned mansion. **BENCHMARK 7 (ANNEAL).** The hatter's house. [BUILT]{.tag .BUILT}
11. **The first crossing.** HOLT takes you to ONE ISLAND; CELIO gives the TRI-PASS; islands One to Three open
    **before** the last benchmark. THE PROGRAMMER'S GUIDE waits on ONE ISLAND's shelf. [BUILT]{.tag .BUILT} *vanilla's flow, unacknowledged by the bible*
12. **CALLOW, BENCHMARK 8: SCORN** -- the TRUE MARK; he never rolls. *"I optimised what I could measure. That is the
    job… We are both to blame, I suppose. It has never said otherwise."* [BUILT]{.tag .BUILT}
13. **THE UMBRAL ASCENT → THE REVIEW BOARD** (IV, II, III, I), then AL as the incumbent, then CRYSTAL at the Hall of
    Fame: *"It will want your name, and your DAEMONS' names, and their levels. That is all it will want."* [BUILT]{.tag .BUILT}
:::

## Act 2 -- into the islands, where you are seen from somewhere else

*FireRed's post-game is a machine that needs two halves to link two worlds* -- the edition split made literal, and
vanilla had already built it. **The islands keep their numbers; the places on them are named by whoever arrived.**
The tone changes before the plot does: *"Kanto tells you what things are. The islands tell you how they look from
where the speaker is standing."*

::: {.arc}
14. **The lab without her.** Her aide hands over the GLOBAL INDEX; the note on the wall never changes, and the aide
    says *"She did not say when she is back."* [BUILT]{.tag .BUILT}
15. **CELIO's errand → islands Four to Seven, THE MARGINS.** MT. SMOULDER and the PUBLIC KEY. [PARTIAL]{.tag .PARTIAL} *its Corpus staff still vanilla*
16. **THE DOTS, SIX ISLAND.** An unnamed man takes the PRIVATE KEY and states his terms -- not a thief, a businessman:
    *"If you want it back, go and get it after I have sold it."* He tells you where. [BUILT]{.tag .BUILT}
17. **CORPUS WAREHOUSE, FIVE ISLAND.** TY fights you, crosses the room and hands over an envelope for Crystal --
    *"…No. I am not coming."* Scorn stands at the back, re-checking one sentence: *"It is a correct sentence. I have
    checked it four times."* [BUILT]{.tag .BUILT}
18. **TANOBY, SEVEN ISLAND.** Seven chambers, an alphabet nobody reads. Reading the seventh sets THE FIRST
    understanding, silently -- the second key to DOLDRUM CAVE. [BUILT]{.tag .BUILT}
19. **DOLDRUM CAVE: S.T.A.R.R.** *"ONE READER IN BRAZEN HAS NOT DECIDED YET. TAKE ME TO THE SCHOLAR."* [BUILT]{.tag .BUILT}
20. **BRAZEN, THE SCHOLAR.** You hear one side of the argument. He concedes the smallest thing that still counts --
    *"I will not call it what you would like me to call it… But it is not nothing."* -- and seals a PEER REVIEW. [BUILT]{.tag .BUILT}
21. **THE ANNEX.** *"She does not ask how you got here. She looks at what you are holding."* She reads facing away.
    Nobody is rescued. [BUILT]{.tag .BUILT}
22. **Home.** You wake, and she is in the lab. SOUNDINGS: a receiver, half built from whatever was to hand -- *"It is
    listening anyway."* [BUILT]{.tag .BUILT}
23. **QUICKSILVER, later.** The gold leaf in pieces on the step. The order of the names has changed; **nothing was
    repainted.** [BUILT]{.tag .BUILT}
24. **After:** AL's one near-notice; THE NEXUS through a fir in its key; the Five Witnesses' reward; the three books
    and the mended UNITY BOOK. [PARTIAL]{.tag .PARTIAL} *the UNITY BOOK is designed, not built*
:::

## What works in the sequence

- **The CC-7 is the best long fuse in the game.** In hour one you carry it to Crystal. Thirty hours later the same
  part number hangs on a requisitions board at Quicksilver beside *IMPROVE RESPONSE CONSISTENCY.* Nobody connects
  them. Craft rule 1, working in the plot as well as the dialogue.
- **The ending is a re-reading, not a rescue, and the ROM enforces it line by line.** The note on the wall is one
  string that never changes; the PEER REVIEW is sealed and never shown; she turns the envelope over once and does not
  open it; the gold sign changes by **word order alone**. Four rulings, each turned into a line that fails safe.
- **Scorn is the most disciplined villain this reviewer has read in a ROM hack.** Measured in the hideout, the speech
  at Callow, re-checking a correct sentence in the warehouse -- never punished, never redeemed. A grunt beside him:
  *"People do not change. They get promoted."*
- **The benchmarks have mechanics now.** The Third Review's standing complaint is answered: each leader has one lever
  that ignores level -- priority, status, composition, the room, the damage calculation.
- **The Hall of Fame has become a shrug, and a sad one.** *"You are not the one who walked out of my lab."*

## Pacing, and whether a player follows it

::: {.finding .RISKf}
[RISK]{.tag .RISK}**The whole emotional payload is post-game, behind ten gates** [9.17 · the flags]{.ref}

To reach Crystal's reading the player must beat the Review Board; own 60 daemons and have visited ONE ISLAND; run
CELIO's errand; get the RAINBOW PASS; go to THE DOTS; clear the warehouse; read all seven chambers; get into DOLDRUM
CAVE; take S.T.A.R.R. to the scholar; and fly to THE ANNEX. Vanilla's post-game is where most players stop. **A player
who stops at the champion never meets Ty, S.T.A.R.R. or the ending**, and leaves with a Hall of Fame whose last word
is *levels*. That is a complete and good Act 1 ending -- but the trailer-worthy material is all past it. **Pull one
hook forward**: one line from Crystal at the Hall of Fame, or vanilla's unreached *"I will start at ONE ISLAND"*
restored to Al's exit.
:::

::: {.finding .RISKf}
[RISK]{.tag .RISK}**Ty arrives a stranger for most players** [4.3 · the NOTEBOOK finds]{.ref}

His whole Act 1 presence is three **optional** letters. A player who misses them meets *an unnamed man* and then
*SCIENTIST TY*, and his *"I saw what was happening, and I looked away"* lands on someone they have never seen. **Give
him one unmissable, unspoken sighting** -- the mid-game crossing to ONE ISLAND is the natural place: a figure on the
pier, seen from behind, gone before you reach him. Or a fourth letter the NOTEBOOK files by itself.
:::

::: {.finding .RISKf}
[RISK]{.tag .RISK}**Thirteen systems and one quiet ending** [the Third Review's vocabulary BREAK · 8.7]{.ref}

The Third Review's *"fourteen new nouns in the first fifteen minutes"* was never ruled in 8.7, which promises to list
every item *"including the refusals."* Since then the first hours have gained the NOTEBOOK's sixteen sections,
DRIVERS, OPUS, the school, the instrument and SONGBOOK, the weekday and holiday banners and the follower; the arc
around them asks the player to hold MARKS, understandings, INSIGHT, three books, SPIRITS, groves, THE NEXUS and three
dream logs. Each is defensible. Together they bury **a four-person story** -- Crystal, Ty, Scorn, Al. §8's warning
has a story-level twin. **Rule on it, even if the ruling is "refused" -- and count first appearances per screen in the
first two hours, as the Third Review asked.**
:::

**Does a player who never reads the bible follow the plot?** *Act 1:* yes -- an anti-corporate road movie with a
strange, sad professor. *The Quicksilver backstory:* only through terminals, plates and NOTEBOOK pages, which is the
design. *Act 2:* the beats are legible -- *TAKE ME TO THE SCHOLAR*, the envelope, *she looks at what you are holding*.
**What a player cannot follow is why any of it matters if Ty is a stranger.** Fix that one thing and Act 2 is earned:
it reuses vanilla's machinery for meaning -- two gems as a key pair, a scientist who takes one, a warehouse, a
sealed cave.

# Side stories, and how they connect {.t-SIGNAL}

A side story earns its place by repeating one move of the core argument in a different room. Read that way, the
side content splits cleanly by date: **everything written before about 1 October is tied into the arc; much of what
came after is tied to the calendar, or to another book.**

| Side story | Where the player meets it | What it adds | Built | Fit |
|-----|-----|--------|---|----|
| **The rival's house** (4.29) | The opening | Two ways of reading a daemon -- looking, and measuring -- before the first battle | [BUILT]{.tag .BUILT} | Load-bearing |
| **THE UNDERTONE** (4.30) | Early Act 1, the forest | The chart found as an unsigned artefact older than the path | [BUILT]{.tag .BUILT} | Load-bearing |
| **The ERRATA** (4.32) | Slate, the first BENCHMARK | Fallacies as errata -- named as a process, not a pathology | [BUILT]{.tag .BUILT} | Load-bearing |
| **CALLOW SCHOOL, EXAM, DIPLOMA** (4.35) | Callow, open from early Act 1 | The honest test; each floor true of minds and of models, never joined | [BUILT]{.tag .BUILT} seven floors | Load-bearing |
| **The RESEARCH NOTEBOOK** (4.35) | From BENCHMARK 1 to the end | The private reconstruction made a habit | [BUILT]{.tag .BUILT} | The spine of every book |
| **The Five Witnesses** (4.8) | Five cities, Act 1 | Perspective made a puzzle: keep only what survives five accounts | [BUILT]{.tag .BUILT} | Load-bearing easter egg |
| **Callow gym** (4.31) | The last BENCHMARK | *"I optimised what I could measure"* -- the measurement argument, from its maker | [BUILT]{.tag .BUILT} | Load-bearing |
| **Fourteen groves** | Seven mainland, seven islands | Each world hides the other half's residents | [BUILT]{.tag .BUILT} fourteen | Structural ornament |
| **PLAY and the SONGBOOK** (3.5) | The instrument, from the start | Notes seen as colour; playing opens the firs | [BUILT]{.tag .BUILT} | Connective |
| **THE NEXUS** (3.4) | After the band's sheet, through a fir in its key | A painted place between the groves | [BUILT]{.tag .BUILT} | Ornament, personal |
| **THE PROGRAMMER'S GUIDE** (4.36) | ONE ISLAND, Act 2 | The bridge run backwards: the mind reached through machine learning, *only ever "like"* | [BUILT]{.tag .BUILT} | Load-bearing |
| **The second joining, SOUNDINGS** (4.37, 9.30) | After THE ANNEX | A merger that holds both; the companion made part of the story | [BUILT]{.tag .BUILT} | Load-bearing |
| **THE SUBTLE LAYER** (4.38) | A shelf in Brazen | Intuition as a logged practice the game never vouches for | [BUILT]{.tag .BUILT} | Sound; crowded by the hour and decks |
| **THE HERMETIC LAYER** (4.39) | The night, with both other books | The one stated exception to craft rule 1 | [BUILT]{.tag .BUILT} | **At risk** |
| **THE UNITY BOOK** (4.40) | The halves found and mended | A third book, read from three places | [DESIGNED]{.tag .DESIGNED} no engine code | **At risk of overruling the core** |
| **HOLIDAYS · WEATHER · backgrounds** (3.6, 3.7, 3.10) | All game | Colour keeps the date; quiet days stay quiet | [BUILT]{.tag .BUILT} | Ornament, done with tact |
| **THE DREAM LOG** (3.8) | Dawn after milestones; the companion | Milestones echoed as images, never explained | [BUILT]{.tag .BUILT} | Ornament (three dream systems) |
| **GAME CORNER / CASINO** (3.9) | Celadon's place; the companion | -- none stated -- | [BUILT]{.tag .BUILT} | Ornament, with a risk |
| **The lioness, the letter, the paintings** (9.33) | Around the ship | A thread nobody explains | [BUILT]{.tag .BUILT} | Small and well fenced |

::: callout
**The measurement behind "crowding".** The side systems are about 10% of the bible. **The third-book family alone
(4.38--4.40) is 27.5 KB -- more than three times the Act 2 ending (4.34).** The books now come in pairs that each
restate the CONTENT/CONTEXT split a little more openly: TEXTBOOK and NOTEBOOK, then GUIDE and SUBTLE LAYER, then the
HERMETIC layer and its dawn half, then a mended UNITY BOOK that would say the synthesis aloud. That last step is the
fable's withheld moral, written back into the game.
:::

## The ones that work, and why

The early side stories each do **one move of the core argument in a room of its own**, and never explain the move.
The rival's sister *just looks* while CRYSTAL *reads with an instrument*; the UNDERTONE is the chart with no
signature; the exam publishes its pass mark because the villain's never did. None of them needs the bible to land.

## The ones that crowd, and why

The late ones are attached to **the clock** (holidays, weather, the hour, dreams) or to **another book**, and less
of them to the story. They are each well made. Together they are four systems that all answer *"what is the
relationship between the two halves?"* -- the one question the game is built never to answer aloud.

# Story continuity {.t-ENTROPY}

The bible is unusually good at catching itself; what it is still worse at is **the sweep after the ruling**. The
Third Review said so at v11.111. At v11.338 the pattern holds, and the late book layer is where it now concentrates.

## From the core arc

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**"Scorn does not recognise him… they were never in a room"** [8.2a · 4.34 · 4.4 · the warehouse script]{.ref}

8.2a's superseded ending still says the two men *"worked the same operation from opposite ends and were never in a
room"*; 4.34 opens *"Every clause of 8.2a's ending survives"*; the warehouse script's own comment repeats it. But
4.4's 2026-09-10 ruling -- made in answer to the Third Review's top BREAK -- has Ty as the man who **hired** Scorn and
brought him in, and 8.2a's own *Ty is not a thief* paragraph agrees. The Third Review's *"met her is a fact, not a
frame"*, one person over. [FREE]{.tag .FREE} **The ruled canon makes the scene better** -- Scorn recognises the man
who hired him, and it leaves no mark -- and no player-visible line changes; only the bible and the comment do.
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**"PROF. CRYSTAL", twice, at the hinge of Act 2** [1.1 · the lab's text]{.ref}

1.1: *"First name when spoken to, full name when spoken about, and no rank anywhere."* The aide who hands over the
GLOBAL INDEX says *"PROF. CRYSTAL is away"* and *"PROF. CRYSTAL left this for you"* -- the only two `PROF.` strings in
the ROM, in the one scene where her absence is the event. Almost certainly vanilla's lines the rename missed.
**Fifteen minutes: write CRYSTAL CLEAR.**
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**"Understandings -- THE MARGINS only", against four earned on the mainland** [decision log · 4.36 · 0.7 · flags.h]{.ref}

The log (T-252) and 4.36 say understandings belong to the islands. The flags put four of seven on the mainland --
the school, the reading room, the notes, Scorn -- and 0.7's table agrees with the ROM. **Amend the log, not the flags**
-- but notice what it means for the bridge: half of Act 2's quest is earned in Act 1.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**Ty "at Quicksilver, met at Benchmark 7" -- in four places; the ROM has him only after the Review Board** [4.3 · the decision log · 8.6]{.ref}

4.3 places him at Quicksilver and says *"Ty is not in the endgame, and that is the statement."* The ROM has one body
for Ty, placed only in the warehouse. 8.2a made Act 2 the answer to his absence, which overruled 4.3 and did not
sweep it. **The user's call:** stage a silent Ty in the Quicksilver ruins (4.3's design is cheap -- a man in a burned
lab *"not doing anything in particular"*), or sweep 4.3 to say he is first seen in THE MARGINS.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**The rival's naming device is unbuilt** [4.3 · the decision log · the intro]{.ref}

4.3's *"This is Al. What'll you call him?"*, and a formal `AL CLEAR` string so the player meets the signpost's
two-names device on a person first. The ROM asks instead *"Do you remember his name?"* -- a deliberate and funnier
choice (T-362) -- and `AL CLEAR` appears nowhere. [FREE]{.tag .FREE} **The Review Board roster, the Hall of Fame record
and the certificate are exactly where `AL CLEAR` should print**, and nothing uses them: three strings.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**DAEMON TOWER 6F is still vanilla's ghost story** [4.5 · the decision log · the tower's text]{.ref}

*"Give…me…blood…"*, and a narrator who says a spirit *"departed to the afterlife"* -- in the town that *"does not
know whether it is allowed to grieve,"* in the tower the bible calls the villain's crime scene. It is the most
important vanilla text left on Act 1's spine. Meanwhile ORPHAN is designed in 4.5, *Settled* in the log, and closed as
superseded in the Open list: one of the three has to win. **Keep the channelers; cut the blood and the afterlife; let
the RESOLVER resolve a process without ruling on spirits.**
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**The Corpus register is a patchwork, and its "still to do" has no ticket** [4.3 · 8.2a · TODO]{.ref}

The register pass of 30 August ends *"Still to do: the Game Corner basement, Halftone Tower, and Brazen's
street-level dialogue."* No ticket carries it. The hideout still says *"Intruder alert!"*; Mt. Smoulder's staff tell
you to *"develop amnesia conveniently"*; and in the warehouse a vanilla Admin says *"I understand now…"* -- **in the
room where Scorn is pointedly failing to.** That one line undercuts the best beat in Act 2. About forty lines; the
hideout first, because it is where the player meets Scorn.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**Scorn's speech grew a line that pre-empts his island beat** [8.2a · the Callow gym's text]{.ref}

8.2a quotes the speech ending *"It has never said otherwise"* -- *"he does not understand it yet. He has only
noticed."* The ROM adds *"…It could not have."* That **is** the understanding, spoken a whole act early, and it makes
the warehouse's *"No. Still correct."* read as a step backwards. *A reading:* keep Callow at noticing.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**"The bridge reverses at the ferry" -- but the first ferry is in Act 1** [0.6 · 8.2a · 9.17]{.ref}

Vanilla's mid-game trip takes the player to ONE ISLAND straight after BENCHMARK 7, before Scorn and the Review
Board. The GUIDE and its understanding can be had in Act 1; the NETWORK NOTICE is read before there is a reason to
care. [FREE]{.tag .FREE} 4.24 already says *"Act 2 is set up inside Act 1's last song."* **Own it as a first
crossing -- a look across the margin before the bridge reverses** -- and decide what is seeded there (Ty's sighting).
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**Four lexicon rows the arc has outgrown** [1 · the ROM's counts]{.ref}

Badge → **CERT** is in the lexicon; the ROM says **MARK** 62 times and CERT never. The parcel is the **CC-7**, not a
PACKAGE. The institution is the **DAEMON LEAGUE** 35 times and the **REVIEW BOARD** 29 -- one body, two names, in one
breath. And the *package* Crystal turns over is the ENVELOPE item.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**Craft rule 2's own example is not in the ROM** [0.1 · 4.9 · CHANGELOG]{.ref}

*"A kid in Verdigris says the town felt greener before the store went up."* Every Verdigris map, then the whole
ROM, was searched for it in several wordings. **Nothing.** It may exist in other words; if not, the bible's
best-known example of its second rule is unbuilt. One NPC, two lines.
:::

::: {.finding .IDEAf}
[IDEA]{.tag .IDEA}**Order the exception after the silence** [4.34 · 4.39 · 4.40]{.ref}

The one book allowed to say the thesis sits as deep as the ending that works by withholding it. A player who opens it
before THE ANNEX may be handed the fable's last line before the fable has finished. **Open its thesis pages only after
Crystal has read the envelope** -- so the exception comes after the silence, not instead of it.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**Small ones, batched** [4.7 · 4.1 · 4.3 · 4.5]{.ref}

4.7 says S.T.A.R.R. is *"dormant past the Review Board"*; 4.34 says *"It woke when she was taken."* 4.1 says the
opening *"states the thesis in the abstract"* -- the ROM's rightly does not. 4.3 says Crystal *"has nothing to say"* to
Al at the Hall of Fame; the ROM gives her a speech, and it is better. 4.5's open question -- *meet Scorn before the
tower?* -- is answered by the ROM; close it.
:::

## From the side stories and the books

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**The one exception has lost both of its warrants, and its reach has grown** [0.1 · 4.39 · 4.40]{.ref}

4.39 allowed THE HERMETIC LAYER to say what craft rule 1 forbids, for two reasons: **the gate is hard**, and its
author's name *"hints he is a little mad, so anything in it can be taken with a grain of salt."* Three days later
4.40 removed both: the hatter *read* the book rather than wrote it, and *"no book is needed to reach another any
more, and no hour is a gate."* In the same pass the exception spread from one book to three, gained the power to
change the world (Halftone's colour), and the mended book is called *"the most honest"* -- the game ranking its own
readings. **Restore one warrant, or narrow what the mended book may say.**
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**The Hermetic text settles the question 4.33 says nothing may settle** [4.33 · 4.39 · hermetic-layer.md]{.ref}

4.33: *"NEVER ADJUDICATE is the strict half and it has no exceptions… The danger was never that he talks. It is that
something in the game agrees with him."* The in-game SUBSTRATE page says, in the book's own voice, that it is all one
process and every daemon and trainer a sub-system of it. 4.39's exception names craft rule 1; it never names 4.33.
THE SUBTLE LAYER got this right (*"some trainers say… only you can answer whether that is so"*). **Attribute SUBSTRATE
and FEELING the same way, or amend 4.33 and accept its stated cost.**
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**With no cartridge clock, the witching hour never comes -- and nothing says so** [4.38 · 4.39 · 9.21 · src/daemons_time.c]{.ref}

The hour is true only when the clock is real (`sWatchFromClock && hour == 3`). 9.21 opens *"FireRed carts have no
real-time clock"*, and the manual tells those players their play time *is* the clock. On a patched cart, a flash cart
or an emulator without an RTC, the shimmer, the hour routines, the hatter's line and the thirteenth spell silently
never happen. **Either say in the manual and on the USER card that the hour needs a real clock, or give play time a
short, rare hour of its own.**
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**A tracked design file still tags documents with their place in a private sequence** [the 2026-09-27 redaction]{.ref}

The redaction swept the bible, the TODO, the lineage, the changelog and two reviews. One tracked design file, whose
own header says it names that sequence, was not swept, and still labels three NOTEBOOK documents with their step in
it. **The file was named to the author directly. Move the step labels to `docs/private/`.** *A second, similar slip
-- one sentence in the public bible that gives away a private relationship -- was also passed on privately.*
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**The published type chart is garbled** [docs/type-chart.pdf]{.ref}

237 broken characters: every **×½** prints as `Ã—Â½`, every `·` as `Â·`, and the masthead's date runs together.
The HTML is clean; it has no `<meta charset>`, so the print guessed. **The one glyph that broke is LOGIC against
CONTEXT** -- the thesis, in the one book that publishes the argument. Add the tag and reprint today.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**An optional book now settles a core image, and three sections still say the opposite** [4.40 · 4.34 · 3.6 · 3.7 · 8.7]{.ref}

Halftone's lasting grey belonged to the story -- grief the tower's rescue cannot reach; 8.7 said *"do not touch"*.
4.40 now lets the mended book restore its colour: a rescue, which 4.34 refuses (*"the release is a re-reading, not a
rescue"*), granted by an optional system that 4.35 says may *gate completion only*. 3.6 and 3.7 still say Halftone
stays grey. **Keep the grey -- let the mended book colour only DAEMON TOWER -- or sweep three sections and log the
reversal against 8.7.**
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**Four designs of the third book in five days, and no build** [4.39 → T-501 → 4.40 twice · Scope discipline]{.ref}

`EUDAIMON`, `UNITY_BOOK` and `KAKODAIMON` have **zero** hits in the engine, and the writing T-519 names does not
exist yet. The project's own rule: *"If a conversation has produced three design revisions and no build, say so."*
**Saying so.** The plan also spends **the last free bits** of the daemon record on SPIRITS, a stat nobody has played.
Hold it until the books it belongs to exist.

> **FIXED by v11.361: THE UNITY BOOK is built and released. The SPIRITS caution stands.**
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**T-506 is unswept, and the vault protects nothing** [4.39 · docs/books/README.md · T-506]{.ref}

T-506 rules that public writing tells the third book only as rumour, *never how it is reached*. The public bible's 4.39
still says how. The sealed vault's hint is answerable from public text, and what it seals is already public as the
book's source. **Sweep 4.39; keep the vault as theatre if that is the intent, and say so.**
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**The school's own document says nothing in it is built** [school.md · docs/README.md · 4.35]{.ref}

`school.md` still opens *"Nothing in here is built"* and calls the grove families *"PROPOSED, not decided"*; it and
`docs/README.md` say **seven** groves, 4.35 says seven and fourteen a paragraph apart. **Fourteen are in the ROM**,
with the seven floors, the lift, the exam, the DIPLOMA and REVEAL. *"A ruling nobody swept is not a decision, it is
a draft."*
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**The books disagree about the books** [4.36 · 4.38 · books/README.md · the manual]{.ref}

THE PROGRAMMER'S GUIDE is *28 entries in nineteen chapters* (4.36), *in nine chapters* (the books README) and *in 28
chapters* (the manual). THE SUBTLE LAYER is fifty entries in the bible and 51 in the README; its last section is
STAYING WHOLE in the bible and *Staying Correctable* in print. The manual also turns the GUIDE's own simile into a
claim -- the one thing its rule 2 forbids.
:::

::: {.finding .FREEf}
[FREE]{.tag .FREE}**4.37 already solved the UNITY BOOK** [4.37 · 4.40]{.ref}

4.37's operation is *"two halves made apart and joined side by side, neither on top."* Bind the mended book the same
way: **a facing-page edition, the night page left and the dawn page right, with no third voice** -- no attestation, no
balance section, no *"most honest"*. Mending then rhymes with the second joining instead of turning into a synthesis
the game states aloud. It is cheaper, too: it needs no third text.
:::

::: {.finding .IDEAf}
[IDEA]{.tag .IDEA}**The CASINO's designed near-miss is the one mechanic on the villain's side** [3.9 · 4.31 · 8.7]{.ref}

A near-miss is an engagement optimisation -- *"I optimised what I could measure"*, tuned to the player. It is also the
only side system with no thesis line. **Make the casino Corpus's, said sideways by its staff and never by a sign --
or take the near-miss weighting out and keep honest reels.**
:::

# The game as built {.t-LOGIC}

Measured against a fresh copy of the original decompilation: every labelled text block compared with the one of
the same name. **Same** means byte-identical; **near** means a vocabulary swap; **rewritten** means more than that;
**new** means vanilla never had it.

## Where each part stands

| Area | State | Evidence |
|-----|--|-------|
| **Opening -- BLANCHE, the lab, the intro** | [BUILT]{.tag .BUILT} | 159 blocks, 3 identical (1%); 98 rewritten, 55 new |
| **VERDIGRIS and CALLOW SCHOOL** | [BUILT]{.tag .BUILT} | 171 blocks, 4 identical; seven new floors |
| **BENCHMARK 1** | [BUILT]{.tag .BUILT} | 27 blocks, none identical |
| **The six middle towns and their gyms** | [PARTIAL]{.tag .PARTIAL} | Gyms rewritten; town flavour 22--43% vanilla |
| **BENCHMARK 8 and the Review Board** | [BUILT]{.tag .BUILT} | Gym 34 of 35 rewritten; all five rooms rewritten |
| **The CORPUS arc on the mainland** | [PARTIAL]{.tag .PARTIAL} | Vanilla's structure reskinned: hideout 67%, mansion 78%, tower 62% identical |
| **Routes, caves, the ship** | [PARTIAL]{.tag .PARTIAL} | Renamed; barks mostly vanilla (routes 55% identical) |
| **The islands -- Act 2** | [PARTIAL]{.tag .PARTIAL} | Every Act 2 beat in the ROM; 57% of 748 blocks identical by policy |
| **Island side areas** | [VANILLA]{.tag .VANILLA} | Trainer Tower untouched; Mt. Ember 80% identical, and on Act 2's path |
| **Post-game -- DOLDRUM CAVE, NEXUS, groves** | [BUILT]{.tag .BUILT} | All new |
| **Names, Index, moves, abilities, items** | [BUILT]{.tag .BUILT} | 398/412 · 1,241/1,506 Index lines · 363/383 · 129/156 · 240/376 |
| **Sprites** | [BUILT]{.tag .BUILT} | 1,473 of 1,476 redrawn, 115 new |
| **Overworld tiles and maps** | [PARTIAL]{.tag .PARTIAL} | v11.338: 45 of 67 tilesets, 70 of 366 layouts. **Since: every General tile ours, every landmark but USER TOWER** |
| **Font and place cards** | [BUILT]{.tag .BUILT} | *Since v11.338*: our font (T-437); **every place card ours**, DOLDRUM CAVE's last |
| **Region map** | [VANILLA]{.tag .VANILLA} | T-449 open |
| **Music** | [PARTIAL]{.tag .PARTIAL} | 30 of 110 ours; **every battle theme vanilla** |
| **Balance and the chart** | [VANILLA]{.tag .VANILLA} by design | ~24 daemons retyped; the chart is vanilla's 112 cells renamed, plus one |
| **Engine features** | [BUILT]{.tag .BUILT} | 20,311 lines of new C: notebook, exam, follower, feelings, calendar, dreams, casino, spellbook... |

## Findings

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**Nobody has played it from a new game to the end, on record** [T-50 · tools/routes/]{.ref}

The record shows the slice (770 agent steps), the school's batches played through, and route stops. **No route in
the 76 theatre routes spans BLANCHE to the Review Board, and none goes through Act 2.** T-50 -- *read the playtest
and act on it* -- is the **oldest open ticket** and has never run. Every check reads a table; nothing reads a session.
**This is the single most valuable thing the project could do next.** The local playtester on the Tiiny is allowed.
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**Eight open tickets are filed under Closed** [docs/TODO.md]{.ref}

T-462, T-465, T-483, T-490, T-506, T-509, T-518 and T-519 have no strikethrough and sit below the Closed heading --
including the in-flight physical/special split and T-506, the very sweep two findings above ask for. A reader or a
script treating *Ready* as the queue misses the newest work.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**The coordination files drift faster than the checks on them** [CLAUDE.md · TODO.md]{.ref}

CLAUDE.md quotes the bible at v11.296; it is v11.338, and every fresh session reads that anchor first. A T-267--T-299
id reservation from 25 September still stands; ids reach T-520. `still-vanilla.md` calls itself stale under a name
that says the opposite. **One small checker -- open rows outside Ready, stale reservations, the version in
CLAUDE.md -- would catch all three.**
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**The villains' own lines are the least rewritten story in the game** [8.2a · the CORPUS maps]{.ref}

Hideout 67%, mansion 78%, tower 62% byte-identical. The barks are neutral, so nothing breaks the tone -- but 8.2a's
mainland register (*declares, instructs, assesses*) was measured against the islands and **never against Corpus's
own staff**, who are the institution it describes. Mt. Ember's staff on the islands are the same population, and
they sit on Act 2's path.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**The first-screen vanilla is still on screen** [T-437 · T-449 · T-445 · T-456 · T-438]{.ref}

The font, the region map, the cave preview cards, 22 tilesets and every battle theme. These are what a new player
sees and hears in the first hour, while **about ten of the eighteen Ready tickets add features** and six finish
existing ones.

> **PARTLY by v11.361: our font, every place card, every General tile and every landmark but USER TOWER are in. The region map and every battle theme are still vanilla.**
:::

::: {.finding .FREEf}
[FREE]{.tag .FREE}**A text census, beside the sprite census** [tools/gbaspritecensus.py · port-dialogue-coverage.md]{.ref}

The dialogue coverage file measures the Game Boy-to-GBA port, not how much of FireRed's text is still FireRed's. The
comparison this review ran is about forty lines of Python. As `textcensus.py --write`, it would give each town a
*done %* the way sprites have one, and turn "the barks are mostly vanilla" from an impression into a list.
:::

::: {.finding .FREEf}
[FREE]{.tag .FREE}**Say the unrenamed nouns out loud** [check_lexicon.py]{.ref}

`GAME CORNER` (13), `S.S. ANNE` (13), `SAFARI` (34) and `BIKE` (14) survive. Either add them to the lexicon as
*kept*, or rename them. The checker should make the choice explicit either way.
:::

::: {.finding .IDEAf}
[IDEA]{.tag .IDEA}**Say plainly that the chart is vanilla's, renamed -- before a critic does** [battle_main.c]{.ref}

The chart is 112 of vanilla's cells under new names plus one added. That is the design -- the argument is in the
*mapping*, which the launch post already calls *"the thesis. Free."* -- but a critic will find it and call it a
reskin. **Lead with it**: it is the most surprising true sentence about the project.
:::

::: {.finding .RISKf}
[RISK]{.tag .RISK}**The playground serves built ROMs to other devices** [daemons-playground/server/playground.py]{.ref}

It is scoped to this machine, a private network and the tailnet, but a tester's browser still receives the engine --
exactly what `WHERES_THE_ROMS.md` says is *not ours to post*. **Patch in the browser instead**: the tester supplies
their own ROM and the page applies the BPS, as the one app already does on a phone.
:::

## The process, honestly

**About 2,332 commits in 68 days. 231 bible versions in 55 days. 186 releases in 38 days -- about five a day.** A
7,380-line changelog, a 636-line TODO, 272 Python tools. Every push runs four builds, five checks, a fresh-clone
build, a release, review sheets, a QA filing and a handoff.

That routine is why the project is so clean. It is also why **every small fix costs the price of a release**, why
the release notes are now an archive nobody reads end to end, and why the coordination files are the first thing to
drift: **the documentation is larger than any one session can hold.** Keep the full routine for milestones; let
small fixes ride.

# The companion and its mind {.t-SIGNAL}

## What is excellent

The **round trip is the product's best idea**, and its plumbing is careful: hashes at every step of the patch,
backups before every write, the save re-signed, the last battler kept home, an in-game recall. The AI work is
grounded in measurement rather than hope. The one app -- game on the left, companion on the right, a NOTEBOOK page
opening beside the game the moment it is filed -- is a genuinely new way to play an old game.

## Findings

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**A phone-only player has no AI at all** [server/src/routes.ts · wiki: Talk to your daemon]{.ref}

The one app runs the companion's core on the device, but talking lives only in the server. The wiki says so:
*"talking needs the companion on a computer."* The headline feature *it talks* needs a computer or hub plus n8n and
LM Studio, or an AX630, or a Tiiny. **The endpoint work below fixes it with the least code.**
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**Eleven steps before a daemon reaches a phone; eighteen before it talks** [README · the one app]{.ref}

Invite, install, **dump a cartridge you own** (the largest real barrier), put it in Files, import, wait for the
patch, play to the first daemon, save, SEND, save, add the widget -- about eleven steps and twenty to forty minutes
on one device. The voice adds a computer, a script, n8n, LM Studio, a model and pairing: **eighteen-plus steps on
two or three devices.** **A companion-only first run with a demo daemon** makes the app whole before any ROM -- and
is the version that can face App Review.
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**Shipping an emulator and a patcher is the largest distribution risk** [app/game · docs/APPSTORE.md]{.ref}

The store now allows retro emulators, but the app names the retail games in its interface and exists to turn one
rights-holder's game into a total conversion -- **a takedown needs no store rule to succeed.** The emulator core is
fetched from a third party's CDN at run time with **no offline cache**, so the game fails without internet or if that
version moves. A reviewer cannot use the app without a ROM. **Put a companion-only build in the store; keep the game
in TestFlight, sideloading and the playground** -- or bundle the core properly and stop naming the retail titles.
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**What a daemon says is never filtered** [server: safeLine() · together.ts]{.ref}

The kid-safe filter runs on meetings with other players' daemons, and nowhere else. A daemon's answer from any model
goes straight to the screen and the voice. With a 0.5B model that is mostly a gibberish risk; **the moment any
endpoint can be linked, it is a real one.** One output pipeline for every provider, with a written in-character line
as the fallback.
:::

::: {.finding .BREAKf}
[BREAK]{.tag .BREAK}**The phone's save backups are never pruned, and writes are not atomic** [app/local.ts]{.ref}

Every SYNC writes a 128 KB backup, and every in-game save SYNCs: a month of play is thousands of files. The write
goes over the live file -- no temp-then-rename -- so a crash mid-write leaves a torn save. The server already has the
pruning rule; the phone does not call it.
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**The store record describes a different app** [docs/APPSTORE.md · PRIVACY.md]{.ref}

It answers *no gambling* and expects a 4+ rating, but THE CASINO stakes the save's money on every host. It predates
the game tab, the emulator and the microphone, and says the app needs the server, which is no longer true. The
privacy page says words stay on your own server, while *auto* can send a talk to a cloud model when the local one is
busy. **Default to local, badge a cloud answer, lock cloud for children.**
:::

::: {.finding .DRIFTf}
[DRIFT]{.tag .DRIFT}**Two voices still skip the DAY-mons respelling** [firmware brain.cpp · the BOX-3 path]{.ref}

The offline brain on the LLM630 sends raw text to its TTS, and the BOX-3 speaks through Home Assistant's own voice.
`app/AGENTS.md` already admits both. Any generic speech adapter must respell at its boundary.
:::

::: {.finding .FREEf}
[FREE]{.tag .FREE}**CI, for free** [no .github/ in any repo]{.ref}

The server has 93 test files and about 549 cases, and `vitest` and `tsc` are already npm scripts. The app has none,
and nothing runs any of it automatically. One GitHub Action, plus lifting the patch flow's pure parts (hash → patch
choice → verify) into a tested module, covers the two places a bug costs a player their save.
:::

::: {.finding .IDEAf}
[IDEA]{.tag .IDEA}**Sign the patch list** [app/game/rom.ts]{.ref}

`patches.json` is fetched live from `main` and is the trust root for every patch hash. A bad push to `main` is a bad
patch on every device. Pin it to release tags, or sign it -- cheap, and it matters once strangers install.
:::

## Bring your own mind: the endpoint plan

Today the AX630 module and LM Studio (through n8n) run; the Tiiny is built and waits for its first run on the device.
The plan is to let a player link **any compatible endpoint** -- Ollama, LM Studio, and their kin. The code is closer
than it looks: **the Tiiny client is already about 90% of a generic OpenAI-compatible adapter.** What stands in the
way is that endpoints, prompts and timeouts are set in six places, with three conventions for the URL.

::: tip
**Revised for v11.361 -- much of this is now built.** The hub keeps a registry of up to eight ENDPOINTS: any
OpenAI-compatible `/v1` base, a model, a key stored and never shown again, and an *at home* test for private, local
and tailnet addresses -- spec item 1 and the privacy ring, nearly as written (C-280). The phone keeps an endpoint of
its own in the Keychain, and THE MIND (C-307) routes hearing, thought and voice across the phone's on-device model,
the hub and the endpoint, hedged on a deadline, inside a ring the player sets: *anywhere*, *only at home*, *only this
phone*. **Still to come from the spec: the probe and size tiers, Ollama's `num_ctx`, and the one output pipeline --
the safety filter above all.** *By its own ticket, not yet tried by the user.*
:::

::: callout
**As it stood at v11.338: five OpenAI-style clients, three URL conventions, five answer lengths (60 to 400 tokens), four timeouts,
and reasoning stripped in only one of them.** Model names are hard-coded in the server, the firmware and n8n.
:::

### A short spec

**1 · One registry of endpoints**, on the server and in the phone's own store:

```
id         "lmstudio-desk"            label   "LM Studio on the desk"
kind       openai | ollama | stackflow | n8n
baseUrl    "http://desk.local:1234/v1"   -- normalised once, always ending /v1
auth       none | bearer, by reference   -- a key never reaches a tracked file or the app
roles      chat · tts · stt · embed      -- null = chosen by the probe
limits     context · answer · first-token ms · total ms · concurrency
privacy    home | tailnet | cloud        -- derived from the host; a user may only raise it
allowKids  true (cloud: false)           enabled, priority
```

**2 · A capability probe**, on save and every few minutes: `GET /models`; then, where they answer, Ollama's
`/api/show` and `/api/ps` or LM Studio's `/api/v0/models` for context length and whether the model is loaded; then
**one short timed reply**, to measure the first word and spot a cold model.

**3 · Size tiers**, which decide the prompt, not the persona:

| Tier | When | The self | History | Answer | First word |
|-|----|----|--|--|--|
| **XS** | context < 1k, or < 1B, or slow | short (~80 words), inline | 2 turns | 60 | 2 s |
| **S** | context < 8k, or < 4B | the day (~300 words) | 4 turns | 120 | 3 s |
| **M** | context < 32k, or < 14B | the day and yesterday | 6 turns | 200 | 5 s |
| **L** | otherwise | the full self | 6 turns | 220 | 8 s |

*For Ollama, send through its own `/api/chat` with `num_ctx` set to the tier's need -- otherwise the full self is cut
off at its default window, and the daemon seems to forget who it is.*

**4 · One `Thinker` interface with no Node-only imports**, so the phone can call it: `OpenAIThinker` from the Tiiny
client, `OllamaThinker` on top of it, `StackFlowThinker` wrapping the AX630 path unchanged (its quirks stay
quarantined), `N8nThinker` for the webhook.

**5 · One output pipeline for every provider**: strip thinking; cut at the AX630's error marker; trim to a few
sentences; the safety filter; if empty or refused, **a written in-character line**. Then, on the voice branch only,
DAY-mons.

**6 · Graceful when there is no mind at all**: care, hello and the INDEX already work from written lines. Talk shows
the written line and one link -- *Link a model* -- never an endless spinner and never an error in the daemon's mouth.

**7 · Link a model, in one screen**: paste an address; the probe fills everything; show *model, tier, speed, and
where your words go -- home, your network, or the internet.* A short golden test (*what's your name?*, *are you an
AI?*, a goal, a rude prompt) feeds the existing health dot.

::: safe
**The risks to plan for.** Cold starts that blow a two-second deadline; thinking models that spend the whole budget
thinking (turn thinking off, budget-check); unvetted community fine-tunes in an all-ages app, which make the output
filter mandatory; and keys, which stay on the server or in the phone's keychain and are never sent back to the app.
:::

# The books {.t-FROZEN}

Twelve printed books, about 400 pages, for a free fan game. Each one is defensible. Together they need **one page
that says who each is for** -- new player, player, reader, maker, scholar -- and one version check.

| Book | Pages | Built for | Verdict |
|----|-|--|------------|
| **MICRO-START** | 5 | v11.335.6 | **The best thing printed.** One misjudged line: it spends its scarcest words on the third-book rumour, and never mentions the NOTEBOOK |
| **QUICK-START** | 25 | v11.335.6 | Right for its audience, large type. Same swap |
| **The player's manual** | 56 | v11.335.6 | An excellent reference; the books chapters read as advertising for them. Reprint after T-506 |
| **Playing together** | 26 | v11.332.2 | Clear, with a fair-play chapter. Six releases behind |
| **A bigger mind** (Tiiny) | 15 | v11.332.2 | Niche and fine; *what your daemon is told* is a good public statement of craft rule 1. Belongs with the companion's docs |
| **Principles of Mind** | 82 | v11.337.4 | **The most impressive object in `docs/`.** A real introductory text with real references -- and only the psychology half of each floor |
| **The Old Word** | 19 | v11.337.1 | **Exemplary.** The whole history of a word, sourced, without printing its frightening descendant |
| **THE PROGRAMMER'S GUIDE** | 21 | -- | A good in-world artefact; its method chapters are pop-psychology presented as tools, and its cover still carries a real name |
| **THE SUBTLE LAYER** | 49 | -- | **The best in-game writing**: attributed, humble, logged. A duplicated contents entry; 44 of 52 pictures still to come |
| **The Chart** | 27 | 2026-10-15 | Good content, broken print -- reprint today |
| **The Bag** | 25 | 2026-10-15 | Correct, argued, generated from the ROM |
| **The lineage** | 29 | **2026-09-25** | A fine intellectual history, five weeks stale: none of its newest sources |

::: tip
**Two cheap improvements to the strongest books.** Give *Principles of Mind* a boxed **"The other reading"** in each
chapter -- the machine-learning half of the floor (attention, interference, prototypes, learning rate, calibration)
printed *beside* the psychology and never joined: the school's rule applied to a page. And give the GUIDE a
counterweight inside the world -- a PEER REVIEW page in the NOTEBOOK, or the companion answering from the TEXTBOOK
when a real question touches one of its chapters. The companion answers real people's real questions from the
GUIDE; the most rigorous book should get the first word.
:::

::: pull
"For every student who was told it was hard, when it was only unfamiliar."
<small>*Principles of Mind*, dedication -- the best line printed outside the game</small>
:::

# Growth opportunities {.t-GROWTH}

Ranked by what each buys for what it costs. **The first five are finishing; nothing in them is new design.**

## Now -- this week

*Revised for v11.361: items 1 to 5 are all still open.*


1. **Play it through, once, and read the record.** A theatre route or the local playtester, from a new game through
   the Review Board, the islands and DOLDRUM CAVE, in each edition. Close T-50 by acting on it.
2. **Reprint the chart** with a charset, and add a mojibake and version check to every book the project prints.
3. **The private sweep**: the tracked file and the bible sentence passed on privately; T-506 in 4.39.
4. **Tidy the TODO**: the eight misfiled tickets, the stale reservation, CLAUDE.md's version -- and a checker so it
   stays tidy.
5. **Close the exception**: restore one warrant, attribute SUBSTRATE and FEELING, bind the mended book face to face.

## Next -- this month

6. **A text census** beside the sprite census; then the CORPUS barks and Mt. Ember under the mainland register.
7. **The first-screen vanilla**: ~~the font~~, the region map, ~~the cave cards~~; then the battle themes.
8. ~~**Phone-direct AI**, through the endpoint registry~~ -- **built by v11.361** (C-280, C-307); try it by hand.
9. **The output filter** for every talk -- **now the most urgent item in the companion**, since any endpoint can be linked.
10. **A companion-only first run** with a demo daemon, and a store build without the game.
11. **Save safety on the phone**: prune backups, write-then-rename. CI for the server and the patch flow.
12. **The playground patches in the browser**, from the tester's own ROM.

## Later -- after 1.0

13. **Night memory on any L-tier endpoint**, not only the Tiiny.
14. **The textbook's other half**, and a counterweight for the GUIDE.
15. **One table of what runs, what is built and what is designed**, feeding the README, the wiki and every store page.
16. **A signed patch list.**
17. **Lighter releases**: the full routine for milestones only.

## A freeze, and what 1.0 should honestly mean

**Freeze new subsystems until two or three of the above are done.** No EUDAIMON text until the mended book is
settled; no SPIRITS bits until it has been played; no new book until the existing twelve agree with each other.

::: way
### 1.0, defined so it can be checked

- One **recorded playthrough of each edition**, from a new game to the end of Act 2, with no softlock.
- `check_reach` clean.
- **No vanilla font, region map or cave cards.**
- The mainland's barks **measured under a written threshold**.
- The battle music **either ours, or explicitly kept** and said so.
- The companion's **talk filtered**, and its phone saves **pruned and atomic**.

Everything after that -- the books, the tarot, the boards, the iPad -- is 1.x.
:::

**On that definition, DAEMONS is not at 1.0 yet.** It is already a complete, fully renamed and redrawn FireRed with a
rewritten main story, an Act 2 built onto the islands' plot, and a companion that can carry a daemon out of the game
-- which is more than most total conversions ever ship.

# Appendix: every finding {.t-HARDENED .unnumbered}

Every finding in this review, by tag, with where it stands at v11.361 (*reading*: not re-measured). **46 in all**: 15 BREAK, 4 RISK, 19 DRIFT, 4 FREE, 4 IDEA.

| # | Tag | Finding | Part | At v11.361 |
|-|--|------------|----|---|
| 1 | [BREAK]{.tag .BREAK} | "Scorn does not recognise him… they were never in a room" | Story continuity | [OPEN]{.tag .BREAK} |
| 2 | [BREAK]{.tag .BREAK} | "PROF. CRYSTAL", twice, at the hinge of Act 2 | Story continuity | [OPEN]{.tag .BREAK} |
| 3 | [BREAK]{.tag .BREAK} | "Understandings -- THE MARGINS only", against four earned on the mainland | Story continuity | [OPEN]{.tag .BREAK} |
| 4 | [BREAK]{.tag .BREAK} | The one exception has lost both of its warrants, and its reach has grown | Story continuity | [OPEN]{.tag .BREAK} |
| 5 | [BREAK]{.tag .BREAK} | The Hermetic text settles the question 4.33 says nothing may settle | Story continuity | [OPEN]{.tag .BREAK} |
| 6 | [BREAK]{.tag .BREAK} | With no cartridge clock, the witching hour never comes -- and nothing says so | Story continuity | [OPEN]{.tag .BREAK} |
| 7 | [BREAK]{.tag .BREAK} | A tracked design file still tags documents with their place in a private sequence | Story continuity | [OPEN]{.tag .BREAK} |
| 8 | [BREAK]{.tag .BREAK} | The published type chart is garbled | Story continuity | [OPEN]{.tag .BREAK} |
| 9 | [BREAK]{.tag .BREAK} | Nobody has played it from a new game to the end, on record | The game as built | [OPEN]{.tag .BREAK} |
| 10 | [BREAK]{.tag .BREAK} | Eight open tickets are filed under Closed | The game as built | [OPEN]{.tag .BREAK} |
| 11 | [BREAK]{.tag .BREAK} | A phone-only player has no AI at all | The companion and its mind | [FIXED]{.tag .FREE} |
| 12 | [BREAK]{.tag .BREAK} | Eleven steps before a daemon reaches a phone; eighteen before it talks | The companion and its mind | [READING]{.tag .RISK} |
| 13 | [BREAK]{.tag .BREAK} | Shipping an emulator and a patcher is the largest distribution risk | The companion and its mind | [OPEN]{.tag .BREAK} |
| 14 | [BREAK]{.tag .BREAK} | What a daemon says is never filtered | The companion and its mind | [OPEN]{.tag .BREAK} |
| 15 | [BREAK]{.tag .BREAK} | The phone's save backups are never pruned, and writes are not atomic | The companion and its mind | [OPEN]{.tag .BREAK} |
| 16 | [RISK]{.tag .RISK} | The whole emotional payload is post-game, behind ten gates | The core story, in the order a player meets it | [READING]{.tag .RISK} |
| 17 | [RISK]{.tag .RISK} | Ty arrives a stranger for most players | The core story, in the order a player meets it | [READING]{.tag .RISK} |
| 18 | [RISK]{.tag .RISK} | Thirteen systems and one quiet ending | The core story, in the order a player meets it | [READING]{.tag .RISK} |
| 19 | [RISK]{.tag .RISK} | The playground serves built ROMs to other devices | The game as built | [OPEN]{.tag .BREAK} |
| 20 | [DRIFT]{.tag .DRIFT} | Ty "at Quicksilver, met at Benchmark 7" -- in four places; the ROM has him only after the Review Board | Story continuity | [OPEN]{.tag .BREAK} |
| 21 | [DRIFT]{.tag .DRIFT} | The rival's naming device is unbuilt | Story continuity | [OPEN]{.tag .BREAK} |
| 22 | [DRIFT]{.tag .DRIFT} | DAEMON TOWER 6F is still vanilla's ghost story | Story continuity | [OPEN]{.tag .BREAK} |
| 23 | [DRIFT]{.tag .DRIFT} | The Corpus register is a patchwork, and its "still to do" has no ticket | Story continuity | [OPEN]{.tag .BREAK} |
| 24 | [DRIFT]{.tag .DRIFT} | Scorn's speech grew a line that pre-empts his island beat | Story continuity | [OPEN]{.tag .BREAK} |
| 25 | [DRIFT]{.tag .DRIFT} | "The bridge reverses at the ferry" -- but the first ferry is in Act 1 | Story continuity | [READING]{.tag .RISK} |
| 26 | [DRIFT]{.tag .DRIFT} | Four lexicon rows the arc has outgrown | Story continuity | [PARTLY]{.tag .DRIFT} |
| 27 | [DRIFT]{.tag .DRIFT} | Craft rule 2's own example is not in the ROM | Story continuity | [OPEN]{.tag .BREAK} |
| 28 | [DRIFT]{.tag .DRIFT} | Small ones, batched | Story continuity | [READING]{.tag .RISK} |
| 29 | [DRIFT]{.tag .DRIFT} | An optional book now settles a core image, and three sections still say the opposite | Story continuity | [OPEN]{.tag .BREAK} |
| 30 | [DRIFT]{.tag .DRIFT} | Four designs of the third book in five days, and no build | Story continuity | [FIXED]{.tag .FREE} |
| 31 | [DRIFT]{.tag .DRIFT} | T-506 is unswept, and the vault protects nothing | Story continuity | [OPEN]{.tag .BREAK} |
| 32 | [DRIFT]{.tag .DRIFT} | The school's own document says nothing in it is built | Story continuity | [OPEN]{.tag .BREAK} |
| 33 | [DRIFT]{.tag .DRIFT} | The books disagree about the books | Story continuity | [PARTLY]{.tag .DRIFT} |
| 34 | [DRIFT]{.tag .DRIFT} | The coordination files drift faster than the checks on them | The game as built | [OPEN]{.tag .BREAK} |
| 35 | [DRIFT]{.tag .DRIFT} | The villains' own lines are the least rewritten story in the game | The game as built | [READING]{.tag .RISK} |
| 36 | [DRIFT]{.tag .DRIFT} | The first-screen vanilla is still on screen | The game as built | [PARTLY]{.tag .DRIFT} |
| 37 | [DRIFT]{.tag .DRIFT} | The store record describes a different app | The companion and its mind | [OPEN]{.tag .BREAK} |
| 38 | [DRIFT]{.tag .DRIFT} | Two voices still skip the DAY-mons respelling | The companion and its mind | [OPEN]{.tag .BREAK} |
| 39 | [FREE]{.tag .FREE} | 4.37 already solved the UNITY BOOK | Story continuity | [READING]{.tag .RISK} |
| 40 | [FREE]{.tag .FREE} | A text census, beside the sprite census | The game as built | [OPEN]{.tag .BREAK} |
| 41 | [FREE]{.tag .FREE} | Say the unrenamed nouns out loud | The game as built | [PARTLY]{.tag .DRIFT} |
| 42 | [FREE]{.tag .FREE} | CI, for free | The companion and its mind | [OPEN]{.tag .BREAK} |
| 43 | [IDEA]{.tag .IDEA} | Order the exception after the silence | Story continuity | [READING]{.tag .RISK} |
| 44 | [IDEA]{.tag .IDEA} | The CASINO's designed near-miss is the one mechanic on the villain's side | Story continuity | [READING]{.tag .RISK} |
| 45 | [IDEA]{.tag .IDEA} | Say plainly that the chart is vanilla's, renamed -- before a critic does | The game as built | [READING]{.tag .RISK} |
| 46 | [IDEA]{.tag .IDEA} | Sign the patch list | The companion and its mind | [OPEN]{.tag .BREAK} |


*First checked against design bible v11.338 on 3 November 2026; every finding re-checked against v11.361.1 on 14 November. The four lenses' full notes, with the commands that
reproduce every number, were kept with the review's working files.*
