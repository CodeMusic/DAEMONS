# Releases

Every release is on the [**Releases** page](https://github.com/CodeMusic/DAEMONS/releases). What a release
**publishes is patches, never ROMs**: a built ROM is Nintendo's program with DAEMONS inside it, and that is not the
project's to post ([why](https://github.com/CodeMusic/DAEMONS/blob/main/ROM%20RELEASE/WHERES_THE_ROMS.md)).

## How a release is named

**`v<design bible>.<n>`** -- `v11.299.1`, `v11.299.2`, `v11.299.3` ... -- so a ROM always says which version of the
[design bible](https://github.com/CodeMusic/DAEMONS/blob/main/docs/vision.md) it was built against. The bible's own
version is the line at the top of `vision.md`; the last number counts releases under it.

## What a release holds

On GitHub, under **Assets**, four BPS patches:

| Patch | Apply it to |
|---|---|
| `DAEMONS.CONTENT.for.FireRed.1.0.bps` | *FireRed* (USA) 1.0 |
| `DAEMONS.CONTENT.for.FireRed.Rev.1.bps` | *FireRed* (USA, Europe) Rev 1 |
| `DAEMONS.CONTEXT.for.LeafGreen.1.0.bps` | *LeafGreen* (USA) 1.0 |
| `DAEMONS.CONTEXT.for.LeafGreen.Rev.1.bps` | *LeafGreen* (USA, Europe) Rev 1 |

A patch only fits the exact ROM it was made from, which is why there are four. Each is made against pret's own
byte-identical rebuild of the retail game and checked by hash. **The Rev 1 patches are tested on ROMs dumped from real
cartridges**, and a release refuses to publish unless the patched result matches its build byte for byte; the 1.0
patches are tested the same way against an exact rebuild of 1.0. Each release's notes say which test each patch
passed.

The release page is the release's notes, with [how to patch](Playing) at the top: each ROM's SHA-1, the engine and
design commits it was built from, and every commit since the release before.

## Where else a release goes

- **The companion's one app** reads the list of releases and the patches' hashes as data
  (`patches.json` in daemons-companion), so it can patch a player's own ROM on the device and offer each new release
  with one tap ([The one app](https://github.com/CodeMusic/daemons-companion/wiki/The-one-app)).
- **daemons-playground** always serves the newest release from a local `ROM RELEASE/`, and its WHAT'S NEW tab shows the
  last twelve releases' notes ([its wiki](https://github.com/CodeMusic/daemons-playground/wiki)).

## In the repository

[`ROM RELEASE/`](https://github.com/CodeMusic/DAEMONS/tree/main/ROM%20RELEASE) files every release by bible version,
`v11.315.x/<release>/`, with its `RELEASE_NOTES.md`. **The notes are committed; the ROMs and patches are not** (ROMs
never, patches for size -- they are published as downloads). When the bible moves on, the first release after it
**seals** the old group: every note set as one `ReleaseNotes_v11.NNN.x.pdf`.

## How one is cut

Maintainers, from the repository root:

```sh
python3 tools/check_fresh_clone.py   # clone the engine from GitHub, build both editions, compare byte for byte
python3 tools/romrelease.py --write  # build all four ROMs, file them, make the patches, write the notes
python3 tools/ghrelease.py --write   # tag it, publish the notes, upload the four .bps files
```

- **`check_fresh_clone.py`** runs before any release someone else will download. It clones the engine fresh, builds
  both editions and compares them with the local build, byte for byte (about five minutes). A mismatch means the
  build depends on something that is not in git.
- **`romrelease.py`** refuses a dirty tree, and reports what it would do without `--write`. The patches come from
  `tools/bps.py`.
- **`ghrelease.py`** uploads only the four `.bps` files and refuses outright if a `.gba` would be uploaded.
