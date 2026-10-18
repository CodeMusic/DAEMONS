# Playing

DAEMONS is released as **patches**, not as a game file. A patch is a small list of differences: applied to a
*FireRed* or *LeafGreen* ROM that **you made from your own cartridge**, it turns that ROM into DAEMONS. You supply the
ROM; the project supplies only its own work.

**Use a ROM you backed up yourself, from a cartridge you own.** Nobody here can give you one, and please don't ask.

The full guide, with every checksum, is
[`ROM RELEASE/HOW_TO_PATCH.md`](https://github.com/CodeMusic/DAEMONS/blob/main/ROM%20RELEASE/HOW_TO_PATCH.md). In short:

## 1. Back up your cartridge

Any GBA cartridge reader makes a *dump* of it (a GB Operator, a GBxCart RW, a DS Lite with a homebrew dumping tool).
Save it as a `.gba`.

## 2. Pick the patch that fits it

| You own | You get | Patch |
|---|---|---|
| *FireRed* (USA) **1.0** | **CONTENT** | `DAEMONS.CONTENT.for.FireRed.1.0.bps` |
| *FireRed* (USA, Europe) **Rev 1** | **CONTENT** | `DAEMONS.CONTENT.for.FireRed.Rev.1.bps` |
| *LeafGreen* (USA) **1.0** | **CONTEXT** | `DAEMONS.CONTEXT.for.LeafGreen.1.0.bps` |
| *LeafGreen* (USA, Europe) **Rev 1** | **CONTEXT** | `DAEMONS.CONTEXT.for.LeafGreen.Rev.1.bps` |

Each game was printed twice, as 1.0 and Rev 1, and a patch fits only the exact ROM it was made from. You don't need
to know which you have: [HOW_TO_PATCH.md](https://github.com/CodeMusic/DAEMONS/blob/main/ROM%20RELEASE/HOW_TO_PATCH.md)
lists the CRC32, SHA-1 and MD5 of each, and a patcher shows them as soon as you open your ROM. A BPS patch checks the
ROM before it changes anything, so the wrong one simply refuses; it cannot damage your file.

Other regions (Japanese, French, German, Spanish, Italian), already-patched ROMs and bad dumps will not match.

## 3. Download and apply

Take the newest release from the [**Releases** page](https://github.com/CodeMusic/DAEMONS/releases) and download the
one `.bps` under **Assets** that matches your ROM. Then:

- **In a browser, on any computer or phone:** [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/). Choose your
  ROM, then the patch, then **Apply patch**. It runs on your own device; nothing is uploaded.
- **Anywhere else:** any BPS patcher -- Floating IPS, MultiPatch, RetroArch's built-in patching.

Your original ROM is left untouched. Keep it: every new release is applied to the **clean original**, never to an
already-patched file.

## Emulators

- **[mGBA](https://mgba.io)** (Windows, Mac, Linux) is what DAEMONS is built and tested in. It can also **soft-patch**:
  put the `.bps` beside your ROM with the same name (`FireRed.gba`, `FireRed.bps`) and it applies it on every load.
- **Delta** (iPhone, iPad) can't patch by itself. Patch in Safari with Rom Patcher JS, which saves to **Files**, then
  in Delta press **+** and import the patched file.

## A real Game Boy Advance

A flash cartridge (an EZ-Flash, an EverDrive and the like) plays the patched file on the hardware itself.

- Copy the patched `.gba` to the cartridge's SD card.
- **Save type:** leave it on automatic. DAEMONS saves exactly as *FireRed* does (128 KB flash).
- **The clock:** DAEMONS reads a cartridge clock if there is one -- the days of the week and the time of day come
  from it, and so do the seasons and the weather ([The world](The-world)). Switch the cartridge's RTC on for this game
  in its own settings. Without one the game still plays, and its days follow your play time. The terminal in your bedroom answers **TIME** with a CLOCK line when it is being read.
- **Moving a save from mGBA:** a flash cart wants exactly 131,072 bytes; mGBA's saves are 16 bytes longer (its clock
  data). Trim them (`head -c 131072 in.sav > out.sav`) and back up both copies first.

## Your save

- Start a **new game**. Keep the DAEMONS ROM under its own name so it gets a save of its own.
- **Updating to a new release:** copy your `.sav` somewhere safe, patch your clean original with the new `.bps`, and
  give the result the **same file name** as before so your emulator or cartridge finds the same save.

## Something went wrong?

| What you see | Why |
|---|---|
| "Source checksum mismatch" / "wrong input file" | Your ROM isn't the version that patch was made for. Try the other patch. |
| The title screen says FIRERED or LEAFGREEN | The patch wasn't applied. Open the *patched* file, or check the soft-patch names match. |
| A white screen, or it won't start | Usually a bad dump. Dump the cartridge again. |

Found a bug in the game? Please [open an issue](https://github.com/CodeMusic/DAEMONS/issues) and say which release you
are playing (it is in the release's name, like `v11.302.3`).

Rather build it yourself? See [Building](Building).
