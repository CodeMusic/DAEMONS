# Building from source

DAEMONS is three repositories joined by symlinks: this one holds the design and the tools, and the engines are
**forks kept beside it**, never merged in, so no Nintendo-derived asset ever enters
[CodeMusic/DAEMONS](https://github.com/CodeMusic/DAEMONS). The pattern and its trade-offs:
[`docs/two-repo-pattern.md`](https://github.com/CodeMusic/DAEMONS/blob/main/docs/two-repo-pattern.md).

## Set up

```sh
git clone https://github.com/CodeMusic/DAEMONS.git
cd DAEMONS
./setup.sh          # clones the engine forks beside it, sets their upstreams, makes the symlinks, builds agbcc
./bindDaemons.sh    # builds CONTENT for the GBA and opens it in mGBA
```

`setup.sh` is idempotent: run it again whenever something looks off. It exists because **a symlink does not survive
`git clone`**, and because **agbcc installs into `engineGba/tools/`**, so it has to be built rather than fetched.

| | |
|---|---|
| `engineGba/` | [pokefirered-daemons](https://github.com/CodeMusic/pokefirered-daemons) -- the GBA engine, **where the game is** |
| `engine/` | [pokered-daemons](https://github.com/CodeMusic/pokered-daemons) -- the Game Boy build, a reference, not updated further |
| `engineAi/` | [gpt-play-pokemon-firered-daemons](https://github.com/CodeMusic/gpt-play-pokemon-firered-daemons) -- the harness that lets a model play it |
| `companion/` | [daemons-companion](https://github.com/CodeMusic/daemons-companion) -- see [The companion](The-companion) |

## The toolchain

| you want | you need |
|---|---|
| **the GBA build** (the default) | `arm-none-eabi-gcc` (Homebrew works), plus **agbcc**, which `setup.sh` builds |
| **the Game Boy build** (`--classic`) | [RGBDS](https://rgbds.gbdev.io/) |

Homebrew's ARM gcc ships no libc, so `MODERN=1` fails on `string.h`. agbcc brings its own headers and is the path that
works.

## Build and run

```sh
./bindDaemons.sh                    # CONTENT, GBA      -> mGBA
./bindDaemons.sh context            # CONTEXT, GBA
./bindDaemons.sh --debug            # the GBA testing build
./bindDaemons.sh --classic          # CONTENT, Game Boy -> SameBoy
./bindDaemons.sh context --classic  # CONTEXT, Game Boy
./bindDaemons.sh --help             # the full list, and the source of truth
```

Or build the GBA ROMs directly:

```sh
make -C engineGba firered           # -> daemonsContent.gba
make -C engineGba leafgreen         # -> daemonsContext.gba
make -C engineGba firered_debug     # -> daemonsContent_debug.gba
make -C engineGba leafgreen_debug   # -> daemonsContext_debug.gba
```

The ROMs are named for the editions, and the `.elf`, `.map`, `.sym` and mGBA's `.sav` follow the same name.

The top-level `make` only reaches the Game Boy build:

| | |
|---|---|
| `make content` / `make context` | build a Game Boy edition |
| `make play` / `make play-debug` | build CONTENT and launch it |
| `make verify-sprites` | prove the Game Boy ROMs contain the art in `gfx/` |
| `make vanilla-check` | prove the toolchain against pristine upstream |

## Check the exit code. Never grep for `error:`

agbcc prints its diagnostics as `warning:` lines and then fails with a bare `Error 1`. So
`make ... | grep -i "error:"` reports a clean build **while the ROM silently keeps the previous binary.** This has
caused real bugs here. Check the exit code instead:

```sh
make -C engineGba firered_debug -j8 >/dev/null 2>&1; echo "exit=$?"
```

`bindDaemons.sh` already gets this right: it runs under `set -euo pipefail`, so a failed build aborts rather than
launching a stale ROM.

## When a build breaks

Check the exit code first (above). For the Game Boy build, run **`make vanilla-check`**: it builds pristine
`pret/pokered` in a throwaway git worktree and checks the hashes without touching your branch. If vanilla matches,
the toolchain is fine and the break is in DAEMONS. For the GBA, a pristine `pret/pokefirered` checkout that passes
`shasum -c firered.sha1` proves the same.

*`shasum -c firered.sha1` fails by design* in the fork -- the ROM carries DAEMONS. It proves the toolchain only on a
pristine `pret/pokefirered` checkout.

## The debug build

`pokefirered` ships no debug build, so the GBA one is DAEMONS' own. It is a **separate ROM with its own save**, so a
debug run never touches a playthrough.

- **A new debug game starts as a normal one does**, so the opening can still be tested.
- **DEBUG > GAME EVENTS** hands out the kit a piece at a time, in story order, each row marked held or not, and A gives
  or takes it. Its first row, EVERYTHING, is the old kit: six daemons picked for their **abilities**, one of each
  **kind** of item (so every description window can be read), all eight MARKS and 999999.
- **HEAL** restores the party; **MART** sets 999999 and adds or takes away any item.
- **JUMP** reaches places without playing to them (and **MORE** has a second page).
- **ENCOUNTER** meets a daemon at a level, and forces the **season** and the **weather**.
- **TIME** forces dawn, day, dusk or night, or AUTO, and relights the map at once.
- **SOUND** plays any song or sound effect, the glitch, and the HARP's and FLUTE's scales.
- Held with **SELECT** on the map: A heals, B restocks, UP plays the next song, DOWN puts the map's own back.
- **Hold B** to walk through grass.

The Game Boy debug build is upstream's own, and a different thing: **SELECT** on the title screen opens its menu, and
holding B skips trainer battles. Its starting party is upstream's, so expect Kanto names in it.

## Worktrees

Run parallel work in git worktrees, but note that **a worktree has no engine symlinks** (they are gitignored), and the
committed ones are relative. Remake them with absolute paths to the sibling repos from inside the worktree.
