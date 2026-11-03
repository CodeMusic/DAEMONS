---
title: DAEMONS press kit
---

# How to use this kit {.t-CONTEXT .unnumbered}

This is the promotional companion to *The Fourth Review* (design bible **v11.338**, release **v11.337.4**, 3 November
2026). The review says what is true and what is not yet; this kit says it out loud, and it **only says things the
review found to be true**. Where a feature is in testing, the copy says so.

Three kinds of page are in here:

- **The words** -- the pitch at three lengths, the three pillars, a fact sheet, who it is for and how to talk about it.
- **The rules** -- what never goes in a post (some of them legal, some of them the game's own).
- **The cards** -- square pages at the back, one idea each, **made to be posted on their own**. Each is also saved as a
  1080 x 1080 PNG in `docs/marketing/cards/`, with a caption for it on the page *Captions for the cards*.

::: note
**Every word quoted from the game is a DRAFT**, as everywhere in DAEMONS. If a line is rewritten in the game, rewrite
it in the post before reusing it.
:::

# The pitch {.t-CONTEXT}

## In eight words

**Machines evolved into creatures. Now they need friends.**

## In twenty-five

**DAEMONS** is a fan-made Game Boy Advance adventure where the machines came alive as creatures -- and a companion app
lets yours step out of the game and live on your phone.

## In a hundred

*Say it DAY-mons.* In DAEMONS, the machines grew up into creatures, and everyone you meet is an animal. You set out
from CRYSTAL CLEAR's lab with your first DAEMON, earn eight MARKS from eight town leaders, fill an INDEX of every one
you meet, and slowly piece together a story the game never stops to explain. Underneath, the seventeen types are an
argument about how minds work: LOGIC is resisted by CONTEXT, and nobody ever says why. When you are ready, **SEND** a
daemon **AWAY** -- and it keeps its life on your phone, a watch or a little board on your desk, with a mind you can
run on your own hardware at home.

{{sprite.named ROVERCUB LABEL CLUSTER}}

<p class="small" style="text-align:center">The three first daemons -- one for each way a machine can learn: by reward, by example, and by finding the shape on its own.</p>

# Three pillars {.t-SIGNAL}

Everything DAEMONS says about itself fits under one of three. Lead with the first; let the other two be the surprise.

::: way
### 1 · A game you play

A full adventure on the Game Boy Advance -- towns, routes, eight leaders, a rival, a mystery -- in **two editions,
CONTENT and CONTEXT**: one story, told two ways, with the same type chart in both. Seventeen types named for how
minds work (LOGIC, CONTEXT, LATENT, SIGNAL, ENTROPY...), every one of Kanto's 151 creatures reborn as a DAEMON, and
books hidden in the world to find and read. It never explains itself. You work it out.
:::

{{frame battle|"A battle: the routine menu, with the INDEX and PERSPECTIVE on the shoulder buttons." crystal|"CRYSTAL CLEAR, who studies DAEMONS as a profession."}}

::: way
### 2 · A daemon that comes out of the game

In your party, choose **SEND**, and the daemon steps out. On your phone's home screen it gets thirsty, hungry,
sleepy; it is glad after a meal and dozes at night. **Tell it what you want to get done, and it finds one next
step** -- each step you finish feeds it, and the experience goes home with it at the next **SYNC**. Watches, pocket
boards, a radio with a dial: any of them can host one, one daemon to each.
:::

::: way
### 3 · A mind that lives in your house

A daemon out here can **talk** -- hold to talk, and it answers in the voice of its INDEX entry. That mind runs on
hardware *you* own: today the AX630 module on the companion's hub, or LM Studio on your own computer through the
companion server; the Tiiny is wired and waiting for its first run. **Next, any OpenAI-compatible endpoint** --
Ollama, LM Studio and their kin, linked straight from the phone -- so the computer you already have can be its mind. No account, no
cloud required, and the app collects nothing for its developer.
:::

::: callout
**Honest footing for the third pillar.** Talking needs the companion running on a computer or the hub today -- a
phone on its own does not talk yet. The AX630 and LM Studio paths run; the Tiiny is built and not yet run on the
device; the general "link any endpoint" setting is *planned* (see the review, Part 5). Say **"coming"** for Ollama
and for phone-only talk until they ship.
:::

# The fact sheet {.t-LOGIC}

| | |
|---|--------|
| **Name** | DAEMONS (say *DAY-mons*). The project's working title is CONTEXT / CONTENT -- the names of the two editions. |
| **What** | A total conversion of a Game Boy Advance classic, built from the community's open decompilation, plus a companion app and devices |
| **Editions** | **CONTENT** (made from FireRed) and **CONTEXT** (made from LeafGreen) |
| **Platforms** | Your own cartridge's ROM, patched (mGBA, Delta, a flash cart); in a browser on your own network (the *playground*); **one app for iPhone, iPad and Apple Silicon Mac** -- game and companion together (in TestFlight testing) |
| **Companion hosts** | Phone and home-screen widget; LilyGO T-Embed, T-Deck, T-Watch S3 and Ultra, T-Display; M5Stack Stick, Core, Dial, Cardputer, Tab5; ESP32-S3-BOX-3 as a Home Assistant voice |
| **Local AI** | AX630 module on the hub; LM Studio via the companion server; Tiiny (built, first run pending); any OpenAI-compatible endpoint, from the phone too, *coming* (Ollama, LM Studio) |
| **Price** | Free. A fan project, never sold |
| **What you need** | A FireRed or LeafGreen you own. **No ROM is distributed** -- a patch is applied to yours |
| **Current release** | v11.337.4 (2 November 2026), built against design bible v11.337 |
| **Manuals** | MICRO-START (5 pp) · QUICK-START (25 pp, large type) · the player's manual · *Playing together* · *A bigger mind* (Tiiny) · *The Old Word* (why DAY-mons) · *Principles of Mind* (the in-game school's textbook) |
| **Source** | github.com/CodeMusic -- DAEMONS (design), pokefirered-daemons (the game), daemons-companion (app, server, firmware), daemons-playground (browser) |

# Who it is for {.t-GROWTH}

Write to one of these at a time. A post that tries to reach all four reaches none.

| Who | What they care about | Lead with | Card |
|-------|-------|-------|--|
| **Fans of the classic creature games and ROM hacks** | A *real* total conversion: new names, new chart, new story, the old feel | "Every one of the 151, reborn" · the two editions · the type chart | 2, 4, 6 |
| **People who think about minds** -- psychology, ML, philosophy | An argument you can *play*, never preached | "LOGIC is resisted by CONTEXT. Nobody says why." · *Principles of Mind* | 3, 5 |
| **Makers and tinkerers** -- ESP32, M5Stack, LilyGO, Home Assistant | A creature that lives on the board on their desk | SEND / SYNC · the boards · LoRa | 7, 8 |
| **Local-AI people** -- Ollama, LM Studio, home-lab | A character for their model to be, offline and private | "Your daemon's mind runs in your house" | 9 |

::: tip
**The thing nobody else has** is the round trip: *raise it in the game, carry it in your life, bring it home
changed.* When in doubt, lead with that.
:::

# How to talk about it {.t-FROZEN}

## Always

- **Say it DAY-mons**, and spell it DAEMONS. Every voice the project uses respells it before it is spoken.
- **Say what is in testing.** The one app is in TestFlight; some boards are built and not yet run on the real thing.
  Promising less and delivering more is this project's whole register.
- **Bring your own game.** Every post that says how to play says *a patch for the FireRed or LeafGreen you own*.
- **Credit the community**: built on the open pokefirered decompilation by pret.

## Never

- **Never use Nintendo's or The Pokémon Company's names, logos or characters in a headline, a thumbnail or a
  hashtag.** Describe it as *"a fan total conversion of a Game Boy Advance classic"*. Never post a ROM or a link to
  one, and never post vanilla screens.
- **Never sell anything** connected to the game, and never ask for money for it.
- **Never write the frightening word** that DAEMONS is mistaken for. The game says the old Greek one, *daimon*: a
  guiding spirit.
- **Never say the thesis.** The game never explains why LOGIC fails against CONTEXT, and neither should a post. Show
  the chart; let people argue in the replies.
- **Never spoil what the player is meant to work out** -- who is related to whom, what is written where, the order things happened. *"Its stories are there to
  piece together"* is as far as a post goes.
- **Never call them AI** in the game's voice. Nobody in the world does. (In a post *about* the local mind, "local AI"
  is fine -- it is the hardware, not the daemon.)

## Tone

Warm, plain and a little dry -- CRYSTAL CLEAR's register. Short sentences. Capitals for the game's own nouns (INDEX,
MARKS, SEND, SYNC), because the game uses them. No exclamation marks in the game's voice.

# Captions for the cards {.t-SIGNAL}

One caption per card, ready to paste. Hashtags last, five at most; leave them off on platforms that do not use them.

| # | Card | Caption |
|-|------|-------------------|
| 1 | **Machines that evolved into creatures** | The machines came alive, and grew up into creatures. You go out to meet them. DAEMONS is a free fan-made adventure for the Game Boy Advance -- say it DAY-mons. #DAEMONS #GBA #FanGame #ROMhack |
| 2 | **Say it DAY-mons** | An old Greek word for a guiding spirit -- the voice that speaks to you from somewhere you don't control. That's who you travel with. #DAEMONS #etymology |
| 3 | **LOGIC is resisted by CONTEXT** | Seventeen types, and every one is a way of thinking. LOGIC hits CONTENT hard and barely scratches CONTEXT. The game never says why. What do you think? #DAEMONS #typechart |
| 4 | **Choose how it learns** | Three first daemons, three ways a machine learns. ROVERCUB learns by reward. LABEL learns by example. CLUSTER finds the shape on its own. Which one is yours? #DAEMONS #starters |
| 5 | **Crystal Clear studies DAEMONS** | "I study DAEMONS as a profession." Meet CRYSTAL CLEAR -- she'll hand you your first one, and never once tell you what to think. #DAEMONS |
| 6 | **Two editions, one argument** | CONTENT and CONTEXT: one story, told two ways. The same type chart in both, because an argument that changes by cartridge isn't one. #DAEMONS #GBA |
| 7 | **It doesn't have to stay in the cartridge** | In your party, choose SEND. Your daemon steps out of the game and onto your phone -- hungry, sleepy, glad to see you. SYNC, and it goes home with everything that happened. #DAEMONS #companion |
| 8 | **One next step** | Tell your daemon what you want to get done. It finds one next step. Finish it, and that's a meal. #DAEMONS #productivity |
| 9 | **A mind in your house** | Your daemon can talk -- and its mind runs on hardware you own, on your own network: an AX630 module or LM Studio today, Ollama and any OpenAI-compatible endpoint on the way. #DAEMONS #LocalAI #Ollama #LMStudio |
| 10 | **Any board can host one** | A watch, a pocket keyboard, a radio with a dial. Most LilyGO and M5Stack boards can host a daemon -- one daemon to each. #DAEMONS #ESP32 #M5Stack #LilyGO |
| 11 | **Bring your own game** | DAEMONS is free and never sold. You bring the FireRed or LeafGreen you own; a patch makes DAEMONS from it. No ROM is ever shared. #DAEMONS #FanGame |
| 12 | **It never explains itself** | Books hidden in the world. A record you fill in. A story told in pieces, at your own pace. You work it out. #DAEMONS |

# A two-week plan {.t-GROWTH}

A suggestion, not a schedule. One card a day is plenty; the replies matter more than the reach.

| Day | Post | Why then |
|-|--------|--------|
| 1 | Card 1, *Machines that evolved into creatures* | The hook: what it is, in one look |
| 2 | Card 2, *Say it DAY-mons* | Settles the name before anyone else decides it |
| 3 | Card 4, *Choose how it learns* | The first question a fan of the genre asks: *which starter?* |
| 4 | A short screen recording: the opening to the first battle | Proof it is real, and it plays |
| 5 | Card 3, *LOGIC is resisted by CONTEXT* | The conversation starter -- reply to every guess, confirm none |
| 6 | Card 6, *Two editions* | Gives people a side to pick |
| 7 | Card 11, *Bring your own game* | How to play, said once, clearly, before anyone asks |
| 8 | Card 7, *It doesn't have to stay in the cartridge* | The reveal: the second pillar |
| 9 | A photo of a real board hosting a daemon on a desk | The physical proof -- this sells the companion better than any card |
| 10 | Card 8, *One next step* | The everyday use: why you'd keep it |
| 11 | Card 10, *Any board can host one* | For the makers -- cross-post to their communities |
| 12 | Card 9, *A mind in your house* | For the local-AI crowd -- only after the endpoint setting ships, or say *coming* |
| 13 | Card 5, *Crystal Clear* | A character people can quote |
| 14 | Card 12, *It never explains itself* | Ends on the mystery; invites the long-form players |

# The cards {.t-VECTOR .unnumbered}

Each page that follows is square and stands on its own. They are also in `docs/marketing/cards/` as 1080 x 1080
PNGs. The colour band at the top of each is the type its idea belongs to.

<div class="card" style="--tc:#c7b6ec">
<div class="k">01 · DAEMONS</div>
<h2>Machines evolved into creatures.</h2>
<p>Now they need friends.</p>
<div class="art">{{sprite ROVERCUB ARTSAI LOOP}}</div>
<div class="foot"><span><b>DAEMONS</b> · say it DAY-mons</span><span>a free fan game for the GBA</span></div>
</div>

<div class="card t-CONTEXT">
<div class="stripe"></div>
<div class="k">02 · THE NAME</div>
<div class="say" style="margin-top:4mm"><em>DAY</em>-mons.</div>
<p>From the old Greek <i>daimon</i>: a guiding spirit -- the voice that speaks to you from somewhere you don't control.</p>
<div class="art">{{sprite.small PING NIBBLE CRAWLER PACKET SPIKE}}</div>
<div class="foot"><span><b>DAEMONS</b></span><span>THE OLD WORD</span></div>
</div>

<div class="card t-LOGIC">
<div class="stripe"></div>
<div class="k">03 · THE CHART</div>
<h2>LOGIC is resisted by CONTEXT.</h2>
<p>Nobody in the game ever says why.</p>
<div class="art"><div class="chart">
<div style="background:rgb(96,122,158);color:#fff">LOGIC<small>rules</small></div>
<div style="background:#2b2b31;color:#5c9e60;font-size:14pt">×2</div>
<div style="background:rgb(198,188,168);color:#16161a">CONTENT<small>data</small></div>
<div style="background:rgb(96,122,158);color:#fff">LOGIC<small>rules</small></div>
<div style="background:#2b2b31;color:#e9a49c;font-size:14pt">×½</div>
<div style="background:rgb(176,86,158);color:#fff">CONTEXT<small>?</small></div>
</div></div>
<div class="foot"><span><b>DAEMONS</b> · seventeen types</span><span>what do you think?</span></div>
</div>

<div class="card t-GROWTH">
<div class="stripe"></div>
<div class="k">04 · THE FIRST CHOICE</div>
<h2>Choose how it learns.</h2>
<div class="art">{{sprite.named ROVERCUB LABEL CLUSTER}}</div>
<p style="font-size:9pt">By reward. By example. By finding the shape on its own.</p>
<div class="foot" style="margin-top:3mm"><span><b>DAEMONS</b></span><span>which one is yours?</span></div>
</div>

<div class="card light t-CONTEXT">
<div class="stripe"></div>
<div class="k">05 · CRYSTAL CLEAR</div>
<h2>"I study DAEMONS as a profession."</h2>
<div class="art">{{frame crystal}}</div>
<div class="foot"><span><b>DAEMONS</b></span><span>every line a DRAFT</span></div>
</div>

<div class="card" style="--tc:#c7b6ec">
<div class="k">06 · TWO EDITIONS</div>
<div class="say" style="margin-top:4mm"><span style="color:rgb(198,188,168)">CONTENT</span><br><span style="color:rgb(176,86,158)">CONTEXT</span></div>
<p>One story, told two ways. The same type chart in both -- an argument that changes by cartridge isn't one.</p>
<div class="art">{{sprite.small CANON MANIFOLD ROVERBYTE}}</div>
<div class="foot"><span><b>DAEMONS</b></span><span>pick a side</span></div>
</div>

<div class="card t-SIGNAL">
<div class="stripe"></div>
<div class="k">07 · SEND · SYNC</div>
<h2>It doesn't have to stay in the cartridge.</h2>
<div class="art">{{frame party-send|"In your party: SEND."}}</div>
<p style="font-size:9pt">On your phone it gets hungry, sleepy, glad to see you. SYNC, and it goes home changed.</p>
<div class="foot" style="margin-top:2mm"><span><b>DAEMONS</b> · the companion</span><span>in testing</span></div>
</div>

<div class="card light t-GROWTH">
<div class="stripe"></div>
<div class="k">08 · THE GOAL COMPANION</div>
<h2>Tell it what you want done.<br>It finds one next step.</h2>
<div class="art">{{sprite.big ROVERCUB}}</div>
<p>Finish it, and that's a meal.</p>
<div class="foot" style="margin-top:2mm"><span><b>DAEMONS</b></span><span>it never nags</span></div>
</div>

<div class="card t-LATENT">
<div class="stripe"></div>
<div class="k">09 · A MIND IN YOUR HOUSE</div>
<h2>Its mind runs on hardware you own.</h2>
<ul><li>The AX630 module on your hub</li><li>LM Studio on your own computer</li><li>Ollama · any OpenAI-compatible endpoint -- coming</li></ul>
<div class="art">{{sprite.small HUNCH CLUSTER}}</div>
<div class="foot"><span><b>DAEMONS</b> · no cloud required</span><span>collects nothing</span></div>
</div>

<div class="card t-SIGNAL">
<div class="stripe"></div>
<div class="k">10 · HOSTS</div>
<h2>Any board can host one.</h2>
<p>A watch. A pocket keyboard. A radio with a dial. One daemon to each.</p>
<div class="art">{{sprite.small PING NIBBLE PACKET SPIKE FORK HUNCH LOOP CRAWLER}}</div>
<div class="foot"><span><b>DAEMONS</b> · LilyGO · M5Stack · ESP32-S3</span><span>LoRa, too</span></div>
</div>

<div class="card light t-HARDENED">
<div class="stripe"></div>
<div class="k">11 · HOW TO PLAY</div>
<h2>Free. Never sold.<br>Bring your own game.</h2>
<p>A patch turns the FireRed or LeafGreen you own into DAEMONS -- on your computer, in a browser, or on your iPhone and iPad. No ROM is ever shared.</p>
<div class="art">{{sprite.small LABEL CLUSTER ROVERCUB}}</div>
<div class="foot"><span><b>DAEMONS</b></span><span>github.com/CodeMusic/DAEMONS</span></div>
</div>

<div class="card t-LATENT">
<div class="stripe"></div>
<div class="k">12 · THE STORY</div>
<h2>It never explains itself.</h2>
<p>Books hidden in the world. A record you fill in. A story told in pieces, at your own pace.</p>
<div class="art">{{frame index-toc|"THE INDEX"}}</div>
<div class="foot"><span><b>DAEMONS</b></span><span>you work it out</span></div>
</div>
