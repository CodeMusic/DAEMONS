# DAEMONS: CONTEXT / CONTENT

**A total conversion of *Pokémon FireRed* and *LeafGreen* where the creatures are daemons and the type chart is an
argument about consciousness.**

Machines evolved into creatures. This is a game about what happened next, and it makes its argument in damage
numbers rather than dialogue. Nothing in the game explains it; that is the rule the whole project runs on.

> **Your daemons can leave the game.** The [companion](The-companion) lets your phone -- or most LilyGO and M5Stack
> boards -- **host** a daemon you **SEND** away from your party. It lives there, you look after it, it helps you get
> one thing done at a time, and it comes home to your save with what it learned. See
> [CodeMusic/daemons-companion](https://github.com/CodeMusic/daemons-companion).

## Two editions

The slash in the title is literal: **CONTEXT** and **CONTENT** are two editions built from one source tree, the way
Red and Blue (and FireRed and LeafGreen) always were.

| You patch | You get |
|---|---|
| *FireRed* | **DAEMONS: CONTENT** |
| *LeafGreen* | **DAEMONS: CONTEXT** |

Both play the same story. They differ in which daemons you meet, and in what the INDEX says about some of them. The
type chart is byte-identical in both, because it is the argument, and an argument that changes by cartridge is not
one. More on [Editions](Editions).

## A few words you will meet

| You knew | Here it is |
|---|---|
| Pokémon | **DAEMON** |
| Pokédex | **THE INDEX** |
| Trainer | **USER** |
| Wild | **UNBOUND** |
| Catching | **BINDING**, with a **USERBOX** up to a **ROOTBOX** |
| Moves | **ROUTINES** |
| Gym, Badge | **BENCHMARK**, **MARK** |
| Fainted | **HALTED** |
| Evolution | **RECOMPILE** |
| Pokémon Center | **CHECKPOINT** |
| PC storage | **COLD STORAGE** |

The types are the vocabulary of thinking machines: CONTENT and CONTEXT, LOGIC and LATENT, ENTROPY, FLOW, GROWTH,
SWARM and the rest. The one-sheet chart is [`docs/type-chart.pdf`](https://github.com/CodeMusic/DAEMONS/blob/main/docs/type-chart.pdf).

## Where it stands

**Design is ahead of implementation, and the game is playable.** DAEMONS was built first on the Game Boy
([pret/pokered](https://github.com/pret/pokered)) and moved to the GBA
([pret/pokefirered](https://github.com/pret/pokefirered)) in September 2026. **The GBA build is the game**; the Game
Boy build still compiles and runs its vertical slice, and is kept as a reference.

Releases come often, each one named for the version of the design bible it was built against
(see [Releases](Releases)). What is done and what is not is kept honestly in the
[design bible](https://github.com/CodeMusic/DAEMONS/blob/main/docs/vision.md) and the
[TODO list](https://github.com/CodeMusic/DAEMONS/blob/main/docs/TODO.md).

**No ROM is ever distributed.** DAEMONS is published as BPS patches you apply to a cartridge you own
([why](https://github.com/CodeMusic/DAEMONS/blob/main/ROM%20RELEASE/WHERES_THE_ROMS.md)).

## Pages

- [Playing](Playing) -- patch your own cartridge's ROM and play, on an emulator, an iPhone or a real GBA
- [Editions](Editions) -- CONTENT and CONTEXT: what differs, and what never does
- [The companion](The-companion) -- a daemon hosted on your phone or a board
- [Building](Building) -- build both editions from source
- [Releases](Releases) -- how a release is named and what it holds
- [Contributing](Contributing) -- the documents, the tools, and the rules they keep

## The repositories

| | |
|---|---|
| [CodeMusic/DAEMONS](https://github.com/CodeMusic/DAEMONS) | the design: the bible, the changelog, the tools. Neither engine |
| [CodeMusic/pokefirered-daemons](https://github.com/CodeMusic/pokefirered-daemons) | the GBA engine, **where the work is** |
| [CodeMusic/pokered-daemons](https://github.com/CodeMusic/pokered-daemons) | the Game Boy build, a reference |
| [CodeMusic/gpt-play-pokemon-firered-daemons](https://github.com/CodeMusic/gpt-play-pokemon-firered-daemons) | the harness that lets a model play it |
| [CodeMusic/daemons-companion](https://github.com/CodeMusic/daemons-companion) | the companion: app, server and firmware |

*DAEMONS is a fan project, unaffiliated with and unendorsed by Nintendo, Creatures Inc. or GAME FREAK Inc. Pokémon is
their trademark. Enormous thanks to [pret](https://github.com/pret), whose decompilations make it possible.*
