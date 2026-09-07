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

## It reads RAM, not the screen

There is no vision model anywhere in this. mGBA exposes a Lua socket, a Python
bridge reads memory and sends buttons, and the agent decides. The model's job
is *given this game state, pick a button* — text in, button out.

That is the whole reason a local model is plausible here, and it is also why
the frontier-API cost most of these projects report does not apply.

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

## The one manual step

mGBA 0.10.5 has no `--script`; that arrived in 0.11.

**Tools → Scripting** opens a window whose only obvious control is a text box
and a **Run** button — and *that box is a Lua REPL, not a file picker.* A path
typed into it fails with `unexpected symbol near '~'`. Paste this instead
(absolute: Lua does not expand `~`):

```lua
dofile("/ABSOLUTE/PATH/TO/mgba/scripts/FireRedBridgeSocketServer.lua")
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
