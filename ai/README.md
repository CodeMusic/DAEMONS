# Playing it with a model

`./bindDaemons.sh --ai` builds the CONTENT edition, regenerates the symbol
table from that build, and starts the bridge and the agent.

The harness is **our fork** of [Clad3815/gpt-play-pokemon-firered][h] —
[CodeMusic/gpt-play-pokemon-firered-daemons][f], symlinked as `engineAi/` and
set up by `setup.sh` exactly like `engine/` and `engineGba/`: our fork as
`origin`, Clad3815 as `upstream`, on the `context-content` branch.

*It was a read-only clone at first, with our one change as a loose patch file.*
That is fine until the second change — **and there will be a second one**,
because this drives our ROM and reads our symbols. `patches/ai-local-model.patch`
is kept as the readable statement of what we changed and why.

[h]: https://github.com/Clad3815/gpt-play-pokemon-firered
[f]: https://github.com/CodeMusic/gpt-play-pokemon-firered-daemons

## It reads RAM first, and the screen second

**The state comes out of memory, by symbol name.** mGBA exposes a Lua socket, a
Python bridge reads the party, position, battle and flags out of RAM, and the
agent decides. It knows the exact HP of every daemon and the tile it is
standing on, because it read them — not because it looked.

**Screenshots go along with it**, two turns' worth by default
(`DAEMONS_KEEP_IMAGES`). *This section used to say there was no vision anywhere
in this, and that was wrong* — one run recorded `num_media_prompt: 4` against
OpenRouter, which is what corrected it. The images cover what RAM does not
say: an unexpected cutscene, a menu with no symbol behind it, whether the thing
in front of you looks like a door.

**Why it still matters that the state is read rather than seen.** A model
squinting at 240×160 to count HP will get it wrong sometimes and be confidently
wrong when it does. Reading it is exact, and it is why a small local model is
plausible here at all — the vision is a supplement, not the interface.

*Cost note:* images are the expensive half of the prompt, which is why the
default is two turns and not ten. `DAEMONS_KEEP_IMAGES=0` turns them off
entirely and the loop still plays.

## Why the symbols are regenerated every run

The harness resolves game state **by symbol name**, from a `pokefirered.sym`
whose loader honours `FIRERED_SYM_PATH`. The one it ships describes retail
FireRed. Measured against ours:

| region | symbols | agree |
|---|---|---|
| EWRAM + IWRAM — live state | 892 | **99.3%** |
| ROM — static data | 48,804 | **3.8%** |

Their file against our ROM reads party, position and battle state **correctly**,
and move names, item names and **the type chart** as garbage. That is the worst
failure mode available: it looks like it is working.

`tools/gbasym.py` emits ours from `pokefirered.elf`, so it cannot drift — rename
a symbol or move a struct and the table follows on the next build.
`FIRERED_BRIDGE_STRICT_SYMBOLS=1` is set so a missing symbol fails loudly
instead of reading zeroes.

*What did not shift, checked:* `CONSENSUS` is **appended** after
`MOVE_PSYCHO_BOOST` rather than inserted, and `PERSPECTIVE` is a renamed string
on `MOVE_TRANSFORM` rather than a new constant. Move IDs are vanilla.

## The local model

`--ai` defaults to an OpenAI-compatible endpoint on `127.0.0.1:8080`:

```
OPENAI_BASE_URL=http://127.0.0.1:8080/v1
OPENAI_MODEL=ternary-bonsai-8b
```

Override any of them in the environment. Set `OPENAI_BASE_URL` to nothing and
it goes back to OpenAI unchanged.

**Two things to expect.** The config sends `reasoning_effort` and
`reasoning_summary`; lenient servers ignore unknown parameters and strict ones
return 400 — that is the first thing to check in `ai/logs/agent.log`. And small
models drift over long horizons: they forget the objective and loop. The
harness already separates `OPENAI_MODEL_PATHFINDING`, which concedes the point
— navigation is A* over a tile map, not an LLM problem, and every token spent
on *press up, press up* is waste.

## The bridge has its own venv, and why

`ai/bridgevenv/` — created on first `--ai`, gitignored, rebuilt if deleted.

**Not fussiness.** This machine has four `python3`s (pyenv 3.12.2, conda base
3.12.9, Homebrew 3.13.5, `/usr/bin` 3.9.6) and *this script picks one of them
as a side effect*: the GBA branch puts `/opt/homebrew/bin` first so agbcc can
find the ARM binutils, which also puts Homebrew's Python ahead of conda's. So
the interpreter the bridge runs on is decided by a toolchain fix, and
`pip install` typed in any shell aims somewhere else. *Two rounds of installing
into the wrong Python before that was visible.*

Homebrew's 3.13 is also externally managed, so it cannot be pip-installed into
directly at all. The venv answers both. `bpvenv` set the precedent for exactly
this problem.

## When the agent logs ECONNREFUSED on :8000

**It is not always the Lua step.** Three different failures look identical from
the agent's log, and the order to check them in is:

1. **The bridge crashed on import.** `tail ai/logs/bridge.log`. A missing
   Python module kills it at line 11 and the agent just sees a dead port.
   `bindDaemons.sh --ai` now checks the imports before starting anything.
2. **mGBA is not running**, or the Lua script was never loaded. The bridge then
   falls back from the socket to mGBA's HTTP interface on :5000 and reports
   **`403 Forbidden`** — which looks like a permissions problem and is really
   *nothing is listening*.
3. **The Lua script is not loaded** but mGBA is up — same 403.

`lsof -nP -iTCP:8888 -sTCP:LISTEN` answers 2 and 3 in one line: if mGBA holds
8888 and 8889, the script is loaded and running.

## The loop, once you are running

**The Lua script lives as long as the emulator does, not as long as the window.**
Verified both ways: with the Scripting window closed mGBA still held 8888 and
8889; when mGBA quit, both ports went.

So it is **once per emulator launch** — and `--ai` quits and relaunches mGBA
every time, so once per `--ai`:

1. `./bindDaemons.sh --ai` — builds, regenerates symbols, starts the bridge,
   the agent **and the dashboard** on <http://localhost:5173>
2. **Tools → Scripting**, paste the `dofile(...)` line it printed, press Run
3. **Close the window.** Nothing stops.

`./bindDaemons.sh --stop` ends the run. **Ctrl+C does not** — it stops whatever
is in the foreground, and the bridge and agent are started by the script and
outlive it, so a leftover bridge keeps holding :8000.

*You do not have to remember that.* `--ai` detects a run that is still up and
stops it properly first — waiting for the port to be released rather than
firing a `pkill` and moving on, which would leave the new bridge dying on bind.

## The one manual step

mGBA 0.10.5 has no `--script`; that arrived in 0.11.

**Tools → Scripting** opens a window whose only obvious control is a text box
and a **Run** button — and *that box is a Lua REPL, not a file picker.* A path
typed into it fails with `unexpected symbol near '~'`. Paste this instead
(absolute: Lua does not expand `~`):

```lua
dofile("/ABSOLUTE/PATH/TO/mgba/scripts/DaemonsBridgeSocketServer.lua")
```

`--ai` prints the exact line. The menu route also works — **File → Load
script…**, in the macOS menu bar with the Scripting window focused.

## An open question worth keeping

An agent reading RAM has **perfect information a player never gets** — exact
matchups, exact HP, the whole chart. §2.6 spent a section on whether a *human*
can generalise the chart from names and colour. A model that skips all of that
and reads the multiplier directly is playing a different game, in the sense the
game itself is about. Feeding it only what a player could see would be the more
interesting experiment.
