# CONTEXT / CONTENT

**A total conversion where the creatures are AI daemons and the type chart is an argument about consciousness.**

Machines evolved into creatures. This is a game about what happened next, and it makes its argument in damage numbers rather than dialogue.

**New to it? Start with [the player's manual](docs/DAEMONS-manual.pdf)** — every way to play, getting started, the
world, the daemons and the seventeen types with the chart, the BENCHMARKS, MARKS and ROOTS, the INDEX, the NOTEBOOK,
PLAY, the GAME CORNER and the companion, and a glossary, in one PDF. It says how things work, never where.

---

## Play it

**From your own cartridge:** download a patch from [Releases](https://github.com/CodeMusic/DAEMONS/releases) and
apply it to a *FireRed* or *LeafGreen* ROM you backed up yourself. [`ROM RELEASE/HOW_TO_PATCH.md`](ROM%20RELEASE/HOW_TO_PATCH.md)
walks through it and lists the checksum each patch expects. **From source:** `./setup.sh`, then `./bindDaemons.sh`.
No ROM is ever distributed here ([why](ROM%20RELEASE/WHERES_THE_ROMS.md)). The newest release is **v11.330.1**
(2026-10-28); each one on GitHub carries four BPS patches — CONTENT for *FireRed* 1.0 and Rev 1, CONTEXT for
*LeafGreen* 1.0 and Rev 1 — and the [**wiki**](https://github.com/CodeMusic/DAEMONS/wiki) walks through playing,
building and the two editions.

**In a browser:** [daemons-playground](https://github.com/CodeMusic/daemons-playground) serves the game from a DAEMONS
checkout to the people on your own network, with the companion in a tab beside it. **On an iPhone or iPad:** the
companion's [one app](https://github.com/CodeMusic/daemons-companion/wiki/The-one-app) takes your own *FireRed* or
*LeafGreen*, applies the patch on the device and plays it beside the companion (internal and in testing; a Mac
version is coming).

---

## What this is

A total conversion. It was built first on [pret/pokered](https://github.com/pret/pokered) — the Game Boy — and **ported to the GBA on 2026-09-03**, onto [pret/pokefirered](https://github.com/pret/pokefirered).

| | |
|---|---|
| [**CodeMusic/pokefirered-daemons**](https://github.com/CodeMusic/pokefirered-daemons) | the engine — **this is where the work is** |
| [**CodeMusic/pokered-daemons**](https://github.com/CodeMusic/pokered-daemons) | the Game Boy build, where the vertical slice was made. Kept as a reference, not updated further |
| [**CodeMusic/gpt-play-pokemon-firered-daemons**](https://github.com/CodeMusic/gpt-play-pokemon-firered-daemons) | the harness that lets a **model play it** — fork of [Clad3815](https://github.com/Clad3815/gpt-play-pokemon-firered) |
| [**CodeMusic/daemons-companion**](https://github.com/CodeMusic/daemons-companion) | the **goal companion** — your phone, a watch or a board hosts a daemon you SEND from your party, one to each device, and it helps you get things done; its app, its server (on a computer or a small hub at home, with an AI board of its own) and firmware. Ours from the first line, no fork |
| [**CodeMusic/daemons-playground**](https://github.com/CodeMusic/daemons-playground) | the game **in a browser**, for demos and beta tests on your own network, with the companion and each release's notes in tabs. Holds no ROM |

Each has a wiki: [this one](https://github.com/CodeMusic/DAEMONS/wiki) for the game,
[the engine's](https://github.com/CodeMusic/pokefirered-daemons/wiki) for the fork,
[the companion's](https://github.com/CodeMusic/daemons-companion/wiki) and
[the playground's](https://github.com/CodeMusic/daemons-playground/wiki).

**Why the move.** A spike was run to answer one question — are abilities, item descriptions and a real scripting language worth rebuilding 334 files for? Gen 1 stores **no item descriptions at all**, which is a writing-led project running on the one generation with nowhere to write. Abilities give the chart a second axis. The Index went from six lines of eighteen characters to three of forty-two.

**What it cost.** Greyscale stops being a constraint: on a DMG the machine and the meaning agreed. The answer is in `docs/vision.md` §9.4 — colour is now **by type**, so it carries the argument instead of decorating it.

**This repository is neither engine.** It is the design: the bible, the changelog, the lineage, and every tool that did the porting. `docs/` has never been engine-specific and that is the whole reason the move was affordable.

**Two editions, one source tree.** The slash in the title is literal. Both
upstreams already build a paired game from one set of sources — Red and Blue,
FireRed and LeafGreen — so **CONTENT** and **CONTEXT** cost three lines of
Makefile, and the split survived the port unchanged, which was the first good
sign the move was affordable. The type chart is byte-identical in both — it's the argument, and an argument that changes by cartridge isn't one. What differs is which daemons you meet, and what the Index says about them.

Creatures are **daemons** — background processes that run unattended, and the older sense too: the *daimon*, the voice that speaks to you from somewhere you don't control. They are not robots and nobody in the world calls them AI. They just live there.

## The idea

Gen 1 had no abilities, no held items, one Special stat, and fifteen type slots. That severity is where the design came from: **the type chart carries the entire philosophy of the game**, because on that machine nothing else could.

That remains true on the GBA. The chart is still the argument — §2's *only* change to the matchup table, `CONTEXT ↔ LATENT` at mutual 2×, was finally built there. What the newer machine adds is room to *say* things: descriptions, longer entries, and abilities as a second axis alongside the chart rather than a replacement for it.

So the fifteen type names are the vocabulary of thinking machines (the GBA plays seventeen: its Steel and Dark slots became HARDENED and OPAQUE) — CONTENT and CONTEXT, LOGIC and LATENT, ENTROPY, FLOW, GROWTH, SWARM. The matchups between them aren't decorative. Rules parse data brilliantly and fail at framing, and the combat math says so in every battle, without a single line of dialogue explaining it.

The rest follows the same principle. Kanto's towns were already named after colors and the original game never did anything with it, so this one finishes the job: every city is a word that means both a color and a feeling. Routes are named for what happens *between* colors — bleeding, fading, glazing, gloaming. The official map keeps its numbers. The people who live there use different names.

Nothing in the game explains any of this. That's the rule the whole project runs on.

There is also a rock opera bleeding into it, but that's a longer story.

## Design philosophy

A few rules the project holds itself to, in case they're useful to anyone building something similar:

- **Lessons must be mechanical.** If a gym's lesson can be skipped by grinding, it isn't a lesson.
- **Name the process, not the pathology.** Place names describe what happened to a place, never what a place supposedly *is*.
- **Never say the thesis.** The moment a character explains the theme, it stops being architecture and becomes a moral.
- **The antagonist is not wrong on purpose.** He's optimistic, likable, and optimizing a metric that was easy to measure instead of the one that mattered. That's most real harm, most of the time.

## Status

**Design is still ahead of implementation, and the whole game is playable** — both editions, start to finish, from
BLANCHE TOWN to the REVIEW BOARD.

**Every daemon is ours.** All 386 species carry our names, plus twelve new ones in slots the original left empty --
three of them a line that grows only while carried on the companion; the INDEX's 398 entries are rewritten, and the
two editions say something different about every one. 1,464 of the original's 1,469 sprites are redrawn, daemons
coloured by their type — and every daemon has now been **drawn again**, as big, readable pixel portraits with a party
icon each, a daemon's other forms too. The daemon that follows you
walks as a small picture of its own, at the player's size. The landmarks the story turns on are getting art drawn from
the story, and the region map has a look of its own: paper and ink, the sea a shuffle of bits and notes. The type chart is in and complete, the routes
carry both their names, several towns have their own music, and the story's documents are where they belong — a
requisition, a set of minutes, a carving, an engraving, none of them signed and none of them explained.

**The world keeps time.** A cartridge clock if there is one, play time if not: dawn, day, dusk and night, the weekday,
and seasons that repaint the world in two hemispheres — CONTENT keeps a northern year and CONTEXT a southern one.
The **weather** follows the season, and **holidays** follow the real calendar — three a month, each month with its own
colour and note. Each edition has an **instrument** — a HARP in CONTENT, a FLUTE in CONTEXT — played note by note in
colour, with seven songs to hear in the world and learn, and a SONGBOOK for what you play. A daemon's **colour is its
friendship**, nearly grey until it trusts you. There is a NOTEBOOK for what you find (a DREAM LOG among it), a school
with a DIPLOMA, a GAME CORNER that plays like the companion's CASINO, and places the game never points to, each with
music of its own. Every routine carries a **signature** of its own in battle, bits and a three-note figure. Daemons
have **feelings** the game reads from play and never names. And there are books to find: once THE SUBTLE LAYER is
held, you start to **notice** things, marked in its purple, and the NOTEBOOK keeps an honest log of what landed.
Some players talk of a third, a grimoire, though no one agrees where it came from
([THE HERMETIC LAYER](https://github.com/CodeMusic/DAEMONS/wiki/The-Hermetic-Layer), on the wiki).

**Your daemons can leave.** SEND one from your party and the
[companion](https://github.com/CodeMusic/daemons-companion) hosts it on your phone, a watch or a board; it comes home
at the next SYNC with what it learned. While it is away it can be **traded** with another player, or lent, through
the companion — the game holds a daemon on offer where it is, and finishes one that arrives, a trade evolution and
all. While it is away the game can hear how it is doing (**SOUNDINGS**). On a watch
it sleeps when you do and dreams, and the dream comes home too, into the NOTEBOOK (**ITS DREAMS**). It can even
evolve while it is carried. At home, a small hub can serve the companion with an **AX630** AI board on it, which
talks as your daemon, tells its dreams and answers as the GUIDE, all in the house; the **T-Watch Ultra** keeps its
nights, its walks and its alarms — and a spike will try the classic Game Boy build on it (DAEMONS T-465,
companion C-214).

**And a model plays it.** [`engineAi/`](ai/README.md) drives mGBA over a Lua socket, reads the game out of RAM by symbol name, and decides. It keeps a self-model, four humor axes derived from what happens to it, and dreams at every summary fold — and any of it can be spoken aloud.

**What is not done:** every new word in the game is still a draft until it is approved, and some decided work is not
built yet — the rest of the daemons' new art, the rest of the landmarks, the cave preview screens. The
[TODO list](docs/TODO.md) is the honest picture of what is next.

See [`docs/`](docs/) for the design bible, which is the honest picture of where this stands — including the decisions that were reversed and why.

## Building

**Two engines, and the GBA one is where the work happens.** §9.3 opened
`pokefirered` as a spike — are abilities, item descriptions and a real
scripting language worth rebuilding 334 files for? — and the spike answered in
a day. `engine/` still compiles and still runs the slice; it is a **reference**
now, and the source the port tools read from.

```sh
git clone https://github.com/CodeMusic/DAEMONS.git
cd DAEMONS && ./setup.sh          # clones both forks, builds agbcc, remakes the symlinks
./bindDaemons.sh                  # CONTENT on the GBA
```

`setup.sh` is idempotent and does the awkward part: **agbcc** installs *into*
`engineGba/tools/`, so it does not survive a fresh clone and has to be built
rather than fetched.

| you want | you need |
|---|---|
| **the GBA build** (default) | `arm-none-eabi-gcc` from Homebrew, plus `agbcc` — `setup.sh` builds it |
| **the Game Boy build** (`--classic`) | [RGBDS](https://rgbds.gbdev.io/) |

Homebrew's ARM gcc ships no libc, so `MODERN=1` fails on `string.h`. agbcc
brings its own headers and is the path that works here.

*`shasum -c firered.sha1` fails by design* — the ROM carries our content. It
proves the toolchain on a pristine `pret/pokefirered` checkout and is not a
regression check for this fork.

| Command | What it does |
|---|---|
| `make content` / `make context` | build a **Game Boy** edition — the `make` shim only reaches `engine/` |
| `make play` | build CONTENT and launch it in an emulator |
| `make play-debug` | the same, with debug mode compiled in |
| `make -C engineGba firered` / `leafgreen` | build a **GBA** edition directly — `daemonsContent.gba`, `daemonsContext.gba` |
| `make vanilla-check` | prove the Game Boy toolchain against pristine upstream |
| `./bindDaemons.sh` | build an edition and run it — **`--help` is the full list** |
| `./bindDaemons.sh --classic` | the Game Boy build; the GBA one is the default |
| `./bindDaemons.sh --ai` | a model plays it, through `engineAi` — see [`ai/README.md`](ai/README.md) |

*The table above is the short version on purpose.* **`./bindDaemons.sh --help`
is the source of truth** and works with nothing checked out and no toolchain
installed — which is when someone needs to read it. This README used to list
the flags itself and went stale twice.

**Check the exit code, never grep for `error:`.** agbcc prints its diagnostics
as `warning:` lines and then fails with a bare `Error 1`, so a filtered build
looks clean while the ROM silently keeps the previous binary. `bindDaemons.sh`
runs under `set -euo pipefail` and gets this right.

**When the Game Boy build breaks, run `make vanilla-check` first.** It builds
pristine `pret/pokered` in a throwaway worktree and checks the hashes without
touching your branch. If vanilla matches, the toolchain is fine and the break is
ours.

### Debug mode

Both engines have one, and they are **not the same thing**.

```sh
./bindDaemons.sh --debug              # GBA — ours
./bindDaemons.sh --classic --debug    # Game Boy — upstream's
```

`pokefirered` ships no debug build at all, so the GBA one is ours. A new debug
game **starts as a normal one does**, and **START → DEBUG → GAME EVENTS** hands
out the kit a piece at a time, in story order — its first row, EVERYTHING, is six
daemons picked for their **abilities**, one of each *kind* of item, all eight
MARKS and 999999. Its other pages **JUMP** to places without playing to them,
force the **TIME** of day, the season, the weather and the date, and play any
**SOUND**.
**Hold B** walks through grass. The engine's
[README](https://github.com/CodeMusic/pokefirered-daemons#the-debug-build) has
the whole menu.

The Game Boy one is upstream's, which `pokered` has always carried behind its
`_DEBUG` define and only ever wired to a Blue build:

- **SELECT on the title screen** opens the debug menu — start a game with a
  party in hand and fly-anywhere enabled
- **Hold B** to skip trainer battles, the Safari step counter, and some NPC
  scripts

It builds a **separate ROM with its own save** (`daemonsContentDebug.gbc`), so a
debug run never touches a real playthrough, and it is deliberately not part of
`make all`. Its starting party is upstream's, so expect Kanto names in it — it
is for reaching places quickly, not for judging how the game feels.

`setup.sh` clones **all three** repos beside this one, wires each `upstream` to
its source, remakes the gitignored symlinks — because **a symlink does not
survive `git clone`** — and builds agbcc. It is idempotent; run it again
whenever something looks off.

The engines are **forks**, kept as sibling repos rather than merged in, so no
Nintendo-derived asset ever enters this repository. The pattern, its
tradeoffs and the alternatives are written up in
[`docs/two-repo-pattern.md`](docs/two-repo-pattern.md).

**No ROMs, no commercial assets, and no copyrighted material are distributed in this repository, and none ever will be.** This is a personal project. Bring your own legally-obtained cartridge dump if you want something to compare against.

## Layout

```
docs/         vision.md — the living design bible, incl. the decision log
              versioned PDF snapshots, the changelog, TODO, engine notes
tools/        the port tools and generators — everything crosses to the GBA through one
ai/           n8n workflows, the LiteLLM config, and how a model plays it
patches/      drop-in files and diffs against a clean upstream checkout
gfx/          original art (daemons/, characters/, overworld/, nexus/, ui/ ...)
audio/        original music (music/, sfx/)
ROM RELEASE/  every release's notes, by bible version (the ROMs themselves never)
qa/           what each build looked like, filed with the picture's caption
wiki/         the GitHub wiki's pages; wiki/publish.sh publishes them

engine/       -> pokered-daemons        Game Boy, reference
engineGba/    -> pokefirered-daemons    GBA, where the work happens
engineAi/     -> gpt-play-...-daemons   the harness that lets a model play it
companion/    -> daemons-companion      the goal companion: app, server, devices
playground/   -> daemons-playground     the game in a browser, for demos and beta tests
```

The three `engine*` entries, `companion/` and `playground/` are **gitignored symlinks**. Nothing is ever
vendored in here.

The bible is [`docs/vision.md`](docs/vision.md). It is the only document that
changes; the PDFs are periodic snapshots, kept because the project now has a
Reversed section and what it used to believe is part of the record.

## Credits

Enormous thanks to **[pret](https://github.com/pret)**, whose disassembly work makes projects like this possible at all, and to the **RGBDS** maintainers. Neither is affiliated with this project.

Pokémon is a trademark of Nintendo, Creatures Inc., and GAME FREAK Inc. This project is unaffiliated with and unendorsed by any of them.

## License

Original code, text, art, and music here are released under [choose one — MIT and CC BY-SA 4.0 are the usual pairing]. Nothing in this repository grants any rights to the underlying game.

---

*If you're here because you want to build something strange on an old engine: the constraints are the good part. Take fifteen slots and make them mean something.*
