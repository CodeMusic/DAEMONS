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

**How to play it later.** The plan is a small program that takes a copy of *FireRed* you legally own and turns it
into DAEMONS, so nobody needs to be handed a ROM at all.
