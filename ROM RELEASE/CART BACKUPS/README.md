# Cart backups

Dumps of the user's own *FireRed* and *LeafGreen* cartridges, read with a GBxCart RW. **Everything in this folder
except this file is gitignored and never leaves this machine** -- a retail ROM is Nintendo's, and this repository
promises never to distribute one (`../WHERES_THE_ROMS.md`). Keep a second copy somewhere that is not git.

**What they are for: the patcher test (T-344).** Every release makes four BPS patches against pret's rebuilds of
the retail ROMs. A real cart's dump is the ROM a player actually owns, so applying each release's patch to it and
checking the result against our own build is the test that the patches work for the people who download them.

**A good dump is exactly 16,777,216 bytes and matches one of these SHA-1s** (pret's `*.sha1`, the same four the
patches are made against):

| Game | Revision | SHA-1 |
|---|---|---|
| FireRed  | 1.0   | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| FireRed  | Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| LeafGreen | 1.0   | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| LeafGreen | Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |

```sh
shasum "ROM RELEASE/CART BACKUPS/"*.gba
```

A dump that matches none of them is a bad read (clean the contacts and dump again) or not a genuine cart.

**Name them by what the hash says**, not by the label: `FireRed 1.0.gba`, `FireRed Rev 1.gba`,
`LeafGreen 1.0.gba`, `LeafGreen Rev 1.gba`. The cart's save, if backed up, goes beside it as `.sav` and is just as
private.
