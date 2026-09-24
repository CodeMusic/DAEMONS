# Where are the ROMs?

Not in this repository, on purpose.

Every release is filed here: its notes, the checksum of each ROM, and, once a version is superseded, one PDF of
everything that changed in it. The `.gba` files themselves are never checked in.

**Why.** DAEMONS replaces nearly everything a player sees and reads: the creatures, their names, the type chart,
the towns, the writing, the music. But it is built on a decompilation of *Pokémon FireRed*, and the game still
runs on Nintendo's engine. A built ROM is Nintendo's program with our work inside it, and that is not ours to
post.

**How to play it now.** Build it yourself from the source:

```sh
./setup.sh           # clones the engine forks and builds the toolchain
./bindDaemons.sh     # builds CONTENT and opens it in mGBA
```

**Or patch a ROM you own.** Every release makes four BPS patches: CONTENT for *FireRed*, CONTEXT for *LeafGreen*,
each for version 1.0 and for Rev 1, because a patch only fits the exact ROM it was made from. Apply one in any BPS
patcher ([Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/) runs in a browser) to the matching game you
own, and you have DAEMONS. The patches are kept out of git for their size and are published as downloads; each
release's notes name the ROM every patch expects, with its SHA-1.

**Later**, a small program may wrap the same step, so nobody needs to be handed a ROM at all.
