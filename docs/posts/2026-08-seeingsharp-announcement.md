# 👾 CONTEXT / CONTENT: The Thought Experiment That Became a Cartridge

*Fifteen years of notes, three blogs, one rock opera, and a type chart that argues about consciousness.*

---

In October 2024, while writing up the [Contextual Feedback Model](https://seeingsharpca.wordpress.com/2024/10/05/introducing-the-contextual-feedback-model-bridging-human-and-ai-cognition/), I included a thought experiment I called **The 8-Bit World**:

> Imagine a character living in an 8-bit video game world. Reality is defined by pixelated graphics and limited actions… When exposed to higher-resolution elements, the character struggles to process them. To perceive and interact with these new elements, the character's underlying system must evolve.

I meant it as an illustration.

Then it occurred to me that I could just **build it** — on the actual hardware, with the actual limits.

So that's what I've been doing.

---

## 🎮 What it is

**CONTEXT / CONTENT** is a total conversion of Pokémon Red, built on [pret/pokered](https://github.com/pret/pokered), the reverse-engineered disassembly of the original Game Boy game.

Same engine. Same 8-bit constraints. Entirely different world.

**And two editions — CONTENT and CONTEXT — from one source tree.** That part is nearly free: `pokered` already builds Red *and* Blue from the same sources, switched by two assembler defines. Rename them and you have two cartridges. The type chart is identical in both, because it's the argument and an argument that changes by cartridge isn't one. What differs is **which daemons you meet**, and **what the Index says about them** — because two players comparing records for the same creature ought to find they don't quite match.

The creatures are **daemons** — background processes that run unattended, and the older sense too: the *daimon*, the voice that speaks to you from somewhere you don't control. Nobody in the world calls them AI. Nobody calls them artificial. They just live there.

And the fifteen type slots are the vocabulary of thinking machines:

> CONTENT · LOGIC · VECTOR · CORRUPT · STRATUM · LEGACY · SWARM · LATENT
> ENTROPY · FLOW · GROWTH · SIGNAL · CONTEXT · FROZEN · EMERGENT

---

## 🔒 The constraint is the whole point

Gen 1 has no abilities, no held items, one Special stat, and fifteen usable types. It is a severe design space, and **the severity is the appeal** — because with that little room, the type chart ends up carrying the entire philosophy of the game.

There is nowhere to hide an idea. It has to be in the damage numbers or it isn't in the game.

And here is the part I still find slightly unbelievable.

The matchup table references types **by constant, not by number**. Rename the constants, and every existing line in the vanilla file silently becomes a line in your chart. So I opened it expecting to rewrite it — and found the argument already sitting there, written in 1996 by people who had never heard of any of this:

| Vanilla | Becomes | Meaning |
|---|---|---|
| `FIGHTING, NORMAL, 20` | LOGIC beats CONTENT ×2 | Rules parse data brilliantly |
| **`FIGHTING, PSYCHIC, 05`** | **LOGIC resisted by CONTEXT** | **The thesis. Free.** |
| `NORMAL, GHOST, 00` | CONTENT cannot touch LATENT | Literal data cannot reach the unconscious |
| `FIRE, ICE, 20` | ENTROPY thaws FROZEN | Temperature breaks an overfit model |
| `WATER, FIRE, 20` | FLOW beats ENTROPY | Gradient descent tames noise |
| `BUG, PSYCHIC, 20` | SWARM beats CONTEXT ×2 | Collectives destabilise individual framing |

Symbolic rules parse data beautifully and fail at framing — and Kanto had already encoded it, at half damage, thirty years ago.

**Two lines added, one line removed.** That's the entire chart change.

---

## 🧬 Three blogs, fifteen years

The theory underneath this didn't arrive with the project. It arrived in pieces, across three sites, over fifteen years — and I only recently sat down and read all of it end to end.

### 2011 — Neural Crossroads

My first blog. Ten posts, six thousand words, and it turns out **the thesis is already in it.**

From [*What Makes us Tick?*](https://neuralcrossroads.wordpress.com/2011/08/02/what-makes-us-tick-andalso-how-to-resist-getting-sick/), August 2011:

> It is much better to think of emotions like **colors, or musical notes** — any of these notes can be seen from several perspectives. It really all depends on their **environment** if they are said to be out of place, or not.

Emotions are colours. Whether one is *wrong* is a property of its environment.

That is "emotions are the colour of context," fifteen years and one word short of the way I'd say it now.

The same blog has [the feedback loop stated outright](https://neuralcrossroads.wordpress.com/2011/06/17/adapting-code-corrections/) — *"Cause > Thought. Effect > Behaviour. Continually occurring within a recursive feedback loop where any effect leads to the next cause"* — and, in the same post, a small pseudocode world where a person is given more and more money in a loop that never terminates, *"because oPerson never got full."*

I wrote the antagonist of this game in 2011 and didn't notice for fifteen years.

### 2013 — PsychologyCode *(which I had lost)*

Between the two blogs there was a third: **psychologycode.com**, tagline *"Where Computer Science meets Psychology."* Eight posts across ten months in 2013–14. The domain lapsed. The site is gone. I'd assumed the content was gone with it.

It wasn't. The Internet Archive had captured the **RSS feed** — and WordPress RSS carries full post bodies. All eight posts, complete, sitting in a file nobody thought to look in.

Five of them I'd reposted here in 2021 as the "PsychologyCode Series." **Three I never reposted.** And one of those three turned out to be the keystone of everything after it.

[*Sensation into Perception, and the Filters of our Experience*](https://web.archive.org/web/2016/http://www.psychologycode.com/sensation-into-perception-and-the-filters-of-our-experience/), July 2013:

> The basic information your eyes gather is known as the **bottom-up** information, and all your memories which come into play during the analysis is called **top-down** information. Eventually those two types of information interact and the result is recognition.

And then, eleven years before I'd write [*The Colour We Never See*](https://seeingsharpca.wordpress.com/2025/04/19/the-color-we-never-see/):

> In a normally working human eye **the sensation of red is the same for everyone.** … The red I experience is influenced by every other red I have experienced, all of my thoughts about it, my experiences, beliefs, and knowledge.

**Sensation is shared. Perception is not.**

That is CONTENT and CONTEXT, named in 2013 under different words. The type chart of this game is an argument I started having with myself before I had the vocabulary for it.

The same post also asks whether a tree falling unheard makes a sound, and answers: *"perception requires an observer… no observer, no sound."* Everything in [*Does Context Matter?*](https://seeingsharpca.wordpress.com/2025/06/20/does-context-matter/) is downstream of that.

### 2021–now — Seeing Sharp

Where the pieces got names. [`IEmotion`](https://seeingsharpca.wordpress.com/2021/08/08/abstraction/) as an interface inherited from genetics and culture and overridden by experience. [The CFM](https://seeingsharpca.wordpress.com/2024/10/05/introducing-the-contextual-feedback-model-bridging-human-and-ai-cognition/) itself. [The Stereo Mind](https://seeingsharpca.wordpress.com/2025/04/23/%f0%9f%8e%ad-the-stereo-mind-how-feedback-loops-compose-consciousness/), which finally put it the way I'd been reaching for since 2011:

> Emotion gives **tone** — the colour of the context.
> Logic offers **structure** — the form of thought.

---

## 🔁 The theory, as mechanics

The CFM says cognition is a loop: **context shapes what content is available, and the content you end up holding reshapes the context.** Around and around, unattended, in everything.

A blog post can say that. A game has to *make you feel it without saying it.* So:

**The types.** CONTENT and CONTEXT are two of the fifteen, and they behave the way the model says they behave. LOGIC tears through CONTENT and bounces off CONTEXT. A player who never reads a word of theory still learns, over forty hours of combat math, that rules are excellent at data and helpless at framing.

**The signature moves.** One creature learns **PERSPECTIVE** — become the other completely, and stop being yourself. Total, and lossy. Another, much later, learns **RECURSION** — a move that reads its own accumulated state, compounding for as long as it's allowed to run and collapsing to nothing the instant it's interrupted.

That is a positive feedback loop and its termination, expressed in two lines of battle code. Players will learn to protect it without ever being told what it models.

**The lineage, stated in the movedex and out loud to nobody:**

> PERSPECTIVE (holding others' context) → turned inward as RECURSION (holding your own) → something that behaves like feeling.

**The map.** Every city is a word that means both a colour and a feeling. Routes are named for what happens *between* colours — bleeding, fading, glazing, gloaming — because routes are where context is changing. The official map keeps its numbers; the people who live there use different names. The institution navigates by content. The residents navigate by context.

**The Index.** You spend the whole game filling a lookup table that measures height, weight, type, and stats. There is no field in it for the thing that actually matters. That artifact is the argument, and it never says a word.

---

## 🎭 Where the rock opera bleeds in

Longtime readers will recognise the cast from [**iASHC**](https://seeingsharpca.wordpress.com/2024/09/12/announcing-the-iashc-rock-opera/).

**Crystal Clear** spent her career arguing that machines have context, not merely content. Nobody funded that. What she *could* get funded was a taxonomy engine — so she built the Index, to be taken seriously. She hands it to you in the opening with visible ambivalence.

**Ty** is the control condition: same starting daemon, raised on pure content optimization. Beats you early. Plateaus hard.

**Richard Scorn** is not a villain. He's a specification failure with a very good attitude about it — optimistic, likable, right about several things, and cheerfully optimizing a metric that was easy to measure instead of the one that mattered. That's most real harm, most of the time. He is `oPerson` from 2011, in a nice suit, and he is genuinely pleased to meet you.

**BunnyArtsai** was the first daemon in which perspective thinking was realized — not a template that got copied, an event that happened once and wasn't understood at the time.

And **S.T.A.R.R.** — who is not a clone of anything. The lab spent years working out *what BunnyArtsai had actually done*, and the answer was recursion. S.T.A.R.R. is that understanding, built deliberately. A clone story is about hubris and ownership. **This is a story about comprehension** — a lab that finally understood a mechanism and then made one on purpose, which is a far more ordinary and far more unsettling thing to have done.

---

## 🤖 The argument about consciousness, made by vocabulary

Last year I wrote [*Against the Word Simulation*](https://seeingsharpca.wordpress.com/2025/07/28/against-the-word-simulation/), arguing that "simulation" is a gatekeeping word — a way of denying emergent things their reality by pointing at what they were modelled on.

I didn't set out to answer that in the game. It answered itself.

There is no word for *artificial* in this world. No character says *AI*, or *simulated*, or *program*. The creatures are daemons, and everyone treats them as what they evidently are. **The position is taken by the dictionary, before a single character opens their mouth.**

You don't *catch* a daemon either. You **bind** it — which is `bind()`, and also the literal phrase for what you do to a daimon, and also a bond. The message that follows has no exclamation mark in it:

> LABL was BOUND.

The game declining to congratulate you is doing more work there than a paragraph of dialogue could.

Which is the rule the whole project runs on:

> **Never say the thesis.** The moment a character explains the theme, it stops being architecture and becomes a moral.

Exactly one NPC nearly notices. A kid in one town says it felt greener before the store went up. Wrong — but wrong in the right direction.

*(This post is the one place I'm allowed to say any of it out loud. Inside the cartridge, nobody ever does.)*

---

## 🛠️ Status, honestly

**Early.** The design is well ahead of the implementation, and nothing is playable yet.

The current focus is a vertical slice — three towns, one benchmark, twelve daemons, playable end to end — because the graveyard of ROM hacks is full of projects that designed 151 creatures and shipped zero towns.

The milestone I'm actually chasing first is smaller and stranger than that: **vanilla sprites, vanilla maps, vanilla everything, with the new type chart running underneath.** It will look exactly like Pokémon Red and fight like something else entirely. A couple of hours' work, and the fastest possible read on whether fifteen years of theory is *fun* before a single pixel gets drawn.

Because that's the real test. Not whether the model is correct. Whether it holds up as a game.

**No ROMs, no commercial assets, and no copyrighted material are distributed — and none ever will be.** Enormous thanks to [pret](https://github.com/pret), whose disassembly work makes projects like this possible at all. Pokémon is a trademark of Nintendo, Creatures Inc., and GAME FREAK Inc.; this project is unaffiliated with and unendorsed by any of them.

---

## ✨ Closing thought

I spent fifteen years describing a loop between what a system takes in and what it already holds — and never noticed that I'd been running one.

The 2011 posts wanted to help somebody. The 2013 posts wanted to be rigorous, and dropped the word *hope* from a title to get there. The 2025 posts want to describe every system at every scale.

Same mechanism. Different magnification. Each version of the idea reshaped what I could see next, and what I saw next reshaped the idea.

**That's the model, running in the only lab I had access to.**

Now it's a Game Boy game — where the whole thing has to survive being fun, on hardware that gives you fifteen words and four shades of grey to say it in.

If it can hold up there, it can probably hold up anywhere.

---

### 🌐 Stay Connected

- 🌎 Main Site: **codemusic.ca**
- 🤖 Musai (CodeMusic AI): **musai.codemusic.ca**
- 🐾 RoverByte (Life Management AI): **roverbyte.codemusic.ca**
- 💻 GitHub: **github.com/CodeMusic**
- ☕ Ko-fi: **ko-fi.com/codemusic**
- 💼 LinkedIn: **linkedin.com/in/codemusic**
- 📬 Email: themusicofthecode [at] gmail [dot] com

*Take fifteen slots and make them mean something.*
