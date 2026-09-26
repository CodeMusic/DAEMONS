# How to play DAEMONS from your own cartridge

DAEMONS is released as **patches**, not as a game file. A patch is a small list of differences: applied to a
*Pokémon FireRed* or *LeafGreen* ROM that you made from your own cartridge, it turns that ROM into DAEMONS. You
supply the ROM; we supply only our own work. No Nintendo file is shared.

**The one rule: use a ROM you backed up yourself, from a cartridge you own.** Nobody here can give you one, and
please don't ask anyone else to.

---

## 1. Back up your cartridge

You need a copy of your cartridge's contents, called a *dump*. Any GBA cartridge reader does this (for example a GB
Operator, a GBxCart RW, or a Nintendo DS Lite with a homebrew dumping tool). Follow its instructions and save
the result as a `.gba` file.

## 2. Which edition, and which version you have

| You own | You get | Patch to use |
|---|---|---|
| *Pokémon FireRed* | **DAEMONS: CONTENT** | `DAEMONS CONTENT for FireRed …` |
| *Pokémon LeafGreen* | **DAEMONS: CONTEXT** | `DAEMONS CONTEXT for LeafGreen …` |

Both editions play the same story. Like Red and Blue, they differ in which daemons you meet.

Each game was printed twice, as **1.0** and as **Rev 1**, and a patch fits only the exact version it was made
from. You don't need to know which one you have: check your file against this table. [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/)
shows these numbers as soon as you open your ROM. They must match one row exactly.

| Your ROM | CRC32 | SHA-1 | Patch |
|---|---|---|---|
| Pokémon FireRed (USA) **1.0** | `DD88761C` | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | `DAEMONS.CONTENT.for.FireRed.1.0.bps` |
| Pokémon FireRed (USA, Europe) **Rev 1** | `84EE4776` | `dd5945db9b930750cb39d00c84da8571feebf417` | `DAEMONS.CONTENT.for.FireRed.Rev.1.bps` |
| Pokémon LeafGreen (USA) **1.0** | `D69C96CC` | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | `DAEMONS.CONTEXT.for.LeafGreen.1.0.bps` |
| Pokémon LeafGreen (USA, Europe) **Rev 1** | `DAFFECEC` | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | `DAEMONS.CONTEXT.for.LeafGreen.Rev.1.bps` |

*(MD5, if your tool shows that instead: FireRed 1.0 `e26ee0d44e809351c8ce2d73c7400cdd`, FireRed Rev 1
`51901a6e40661b3914aa333c802e24e8`, LeafGreen 1.0 `612ca9473451fa42b51d1711031ed5f6`, LeafGreen Rev 1
`9d33a02159e018d09073e700e1fd10fd`.)*

**If none of the rows match**, the patch will refuse to apply. A BPS patch checks the ROM before it changes
anything, so it can't damage your file. The usual reasons for a mismatch are:

- a ROM from another region (Japanese, French, German, Spanish or Italian);
- a hack that is already patched;
- a bad or incomplete dump. Dump the cartridge again.

## 3. Download the patch

Open the [**Releases** page](https://github.com/CodeMusic/DAEMONS/releases) and take the newest release. Under
**Assets**, download the one `.bps` file that matches your row above. (GitHub shows the names with dots where
the spaces were, as in the table.)

## 4. Apply it

Pick whichever of these suits you.

### In a browser, on any computer or phone (Rom Patcher JS)

1. Go to <https://www.marcrobledo.com/RomPatcher.js/>.
2. Under **ROM file**, choose your `.gba`. Check that its CRC32 or SHA-1 matches your row.
3. Under **Patch file**, choose the `.bps` you downloaded.
4. Press **Apply patch**. It saves a new file; rename it to something like `DAEMONS CONTENT.gba`.

Your original ROM is left untouched. The patching happens on your own device; nothing is uploaded.

### In mGBA, without making a new file (soft patching)

Put the patch **next to** your ROM with **the same name**, for example `FireRed.gba` and `FireRed.bps`. Open
`FireRed.gba` in [mGBA](https://mgba.io) and it applies the patch automatically each time it loads. Remove or rename
the `.bps` to play the original game again.

### On an iPhone or iPad (Delta and similar)

Delta can't patch by itself. Patch in Safari with Rom Patcher JS (above), which saves the result to **Files**. Then
in Delta, press **+** and import the patched file from Files.

### Anywhere else

Any BPS patcher works: Floating IPS (Windows), MultiPatch (Mac), or the patching built into RetroArch. The steps
are always the same: your ROM, then the patch, then save the result.

## 5. Your save file

- **Start a new game.** A save from the original *FireRed* or *LeafGreen* isn't meant for DAEMONS, so keep your
  DAEMONS ROM under its own name and it gets a save of its own.
- **When a new release comes out**, patch your **original, clean** ROM again with the new `.bps`. Never patch
  an already-patched ROM. To keep playing your game, give the new patched ROM the **same file name** as the
  old one so your emulator finds the same `.sav`. **Copy your `.sav` somewhere safe first.** Releases are built to
  keep saves working, but a backup costs nothing.

## 6. Something went wrong?

| What you see | Why |
|---|---|
| "Source checksum mismatch" / "wrong input file" | Your ROM isn't the version that patch was made for. Check the table in step 2 and pick the other patch. |
| The game says FIRERED or LEAFGREEN on the title screen | The patch wasn't applied. Open the *patched* file, or, when soft patching, check the two names match exactly. |
| A white screen, or it won't start | Usually a bad dump. Dump the cartridge again and check its checksum. |

Found a bug in the game itself? Please open an issue on the repository and say which release you're playing (it's
in the release's name, like `v11.288.10`).

---

*Why patches and not a download: [`WHERES_THE_ROMS.md`](WHERES_THE_ROMS.md). To build DAEMONS from source instead,
see the repository's [`README.md`](../README.md).*
