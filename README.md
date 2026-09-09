# CONTEXT / CONTENT

**A total conversion where the creatures are AI daemons and the type chart is an argument about consciousness.**

Machines evolved into creatures. This is a game about what happened next, and it makes its argument in damage numbers rather than dialogue.

---

## What this is

A total conversion. It was built first on [pret/pokered](https://github.com/pret/pokered) — the Game Boy — and **ported to the GBA on 2026-09-03**, onto [pret/pokefirered](https://github.com/pret/pokefirered).

| | |
|---|---|
| [**CodeMusic/pokefirered-daemons**](https://github.com/CodeMusic/pokefirered-daemons) | the engine — **this is where the work is** |
| [**CodeMusic/pokered-daemons**](https://github.com/CodeMusic/pokered-daemons) | the Game Boy build, where the vertical slice was made. Kept as a reference, not updated further |
| [**CodeMusic/gpt-play-pokemon-firered-daemons**](https://github.com/CodeMusic/gpt-play-pokemon-firered-daemons) | the harness that lets a **model play it** — fork of [Clad3815](https://github.com/Clad3815/gpt-play-pokemon-firered) |

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

So the fifteen types are the vocabulary of thinking machines — CONTENT and CONTEXT, LOGIC and LATENT, ENTROPY, FLOW, GROWTH, SWARM. The matchups between them aren't decorative. Rules parse data brilliantly and fail at framing, and the combat math says so in every battle, without a single line of dialogue explaining it.

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

**Design is still ahead of implementation, but the slice is walkable.**

You can play **Blanche Town → The Bleed → Callow → The Undertone → Underpaint → Slate → Benchmark 1** end to end. The type chart is in and complete, the routes carry both their names, several towns have their own music, and the story's documents are where they belong — a requisition, a set of minutes, a carving, an engraving, none of them signed and none of them explained.

**The slice has a cast now.** Thirty-two daemons carry our names, our art and an Index entry — the three starter lines, the six wild lines, and the MUSAI, ARTSAI and S.T.A.R.R. Every creature the player meets in the slice is drawn.

**And a model plays it.** [`engineAi/`](ai/README.md) drives mGBA over a Lua socket, reads the game out of RAM by symbol name, and decides. It keeps a self-model, four humor axes derived from what happens to it, and dreams at every summary fold — and any of it can be spoken aloud.

**What is not done:** the bestiary is thirty-two, not 151. Enough ROM hacks have died designing a full roster before shipping a single town.

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

**Before blaming anything, prove the toolchain.** `make vanilla-check` builds
pristine upstream in a throwaway worktree and checks the hashes without
touching your branch. If vanilla matches, the break is ours.

*`shasum -c firered.sha1` fails by design* — the ROM carries our content. It
proves the toolchain on a pristine `pret/pokefirered` checkout and is not a
regression check for this fork.

| Command | What it does |
|---|---|
| `make content` / `make context` | build a **Game Boy** edition — the `make` shim only reaches `engine/` |
| `make play` | build CONTENT and launch it in an emulator |
| `make play-debug` | the same, with debug mode compiled in |
| `make vanilla-check` | prove the toolchain against pristine upstream |
| `./bindDaemons.sh` | build an edition and run it — **`--help` is the full list** |
| `./bindDaemons.sh --classic` | the Game Boy build; the GBA one is the default |
| `./bindDaemons.sh --ai` | a model plays it, through `engineAi` — see [`ai/README.md`](ai/README.md) |

*The table above is the short version on purpose.* **`./bindDaemons.sh --help`
is the source of truth** and works with nothing checked out and no toolchain
installed — which is when someone needs to read it. This README used to list
the flags itself and went stale twice.

**When a build breaks, run `make vanilla-check` first.** It builds pristine
`upstream/master` in a throwaway worktree and checks the hashes without touching
your branch. If vanilla matches, the toolchain is fine and the break is ours.

### Debug mode

Both engines have one, and they are **not the same thing**.

```sh
./bindDaemons.sh --debug              # GBA — ours
./bindDaemons.sh --classic --debug    # Game Boy — upstream's
```

`pokefirered` ships no debug build at all, so the GBA one is ours: a new game
starts with six daemons picked for their **abilities**, one of each *kind* of
item so the description window can be read, all eight MARKS and 999999, and
**hold B** walks through grass.

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
docs/       vision.md — the living design bible, incl. the decision log
            versioned PDF snapshots, type-system build notes
tools/      the port tools — every rename crossed to the GBA through one
ai/         n8n workflows, the LiteLLM config, and how a model plays it
patches/    drop-in files and diffs against a clean upstream checkout
gfx/        original sprite work (front/, back/, overworld/, ui/)
audio/      original music (music/, sfx/)

engine/     -> pokered-daemons        Game Boy, reference
engineGba/  -> pokefirered-daemons    GBA, where the work happens
engineAi/   -> gpt-play-...-daemons   the harness that lets a model play it
```

The three `engine*` entries are **gitignored symlinks**. Nothing is ever
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
