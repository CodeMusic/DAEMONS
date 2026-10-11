# Editions: CONTENT and CONTEXT

The project is called **CONTEXT / CONTENT** and the slash is literal: **two editions, one source tree.** The engines
DAEMONS is built on already made a pair of games from one set of sources -- Red and Blue, FireRed and LeafGreen -- so
the two editions cost almost nothing to build.

| | **CONTENT** | **CONTEXT** |
|---|---|---|
| patched onto | *FireRed* | *LeafGreen* |
| built by | `make -C engineGba firered` | `make -C engineGba leafgreen` |
| ROM file | `daemonsContent.gba` | `daemonsContext.gba` |
| on the Game Boy build | `_RED` | `_BLUE` |
| leans toward, early | CONTENT, LOGIC, STRATUM, LEGACY -- the literal, the rule-based, the physical layer | CONTEXT, LATENT, VECTOR, ENTROPY -- framing, the unconscious, embeddings, noise |

CONTENT is the default build. The title puts CONTEXT first anyway: everyone says content is king, and the title
disagrees before the player has read a word.

## What never differs

**The type chart is byte-identical in both editions.** It is the argument, and an argument that changes by cartridge
is not one. The story is the same story, the towns are the same towns, and every daemon exists in both ROMs.

## What does

- **Which daemons you meet.** Each edition simply cannot bind some of them, and the rosters lean the way the table
  above says. So the two editions are hard in different places, and two players comparing notes will each have built
  a different, sincere intuition about what is strong.
- **What the INDEX says.** For a handful of daemons, the two editions' entries disagree -- different heights,
  different weights, different flat sentences about the same creature, each stated as fact. Nobody in the game
  explains it.
- **The INDEX cannot be completed alone.** With edition-exclusive daemons, finishing it takes someone else's
  playthrough: another person's context, over a link cable.

## Saves

The two editions keep **separate saves**, because each ROM has its own name. The debug builds
(`daemonsContent_debug.gba`, `daemonsContext_debug.gba`) have saves of their own too, so testing never touches a
playthrough.

More: [`docs/vision.md`](https://github.com/CodeMusic/DAEMONS/blob/main/docs/vision.md) section 8.4, *The two editions*.
