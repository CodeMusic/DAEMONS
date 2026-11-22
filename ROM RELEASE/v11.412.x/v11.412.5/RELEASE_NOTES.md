# DAEMONS v11.412.5 — release notes

*Released 2026-11-21 23:42 · built against the design bible v11.412*

- **Engine**: CodeMusic/pokefirered-daemons `f95c824c3` (context-content)
- **Design**: CodeMusic/DAEMONS `8a1aa00d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e154ff39cdbcba3ef9ae8a474660d2a3c22de36c` |
| `daemonsContext.gba` | CONTEXT | `671b680e78d976a1bedf66965e43a23c700d5aef` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b7b686126289638cd1b0319e6b479eb7678a4bac` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ad48733269451bcc225efca320f60057ae78c43d` |

## The engine since v11.412.4

- `f95c824c3` T-445: the seven TANOBY chambers each show the shared card in their own palette (the user, 2026-11-21: OWN CARD EACH, BAND; DRAFT)
- `1f5a7ea23` README: latest is v11.412.4

## The design and tools since v11.412.4

- `8a1aa00d` Merge branch 't445'
- `5a537b3d` T-445: the TANOBY chambers' cards BUILT as BAND (engine f95c824c3; the user, 2026-11-21: OWN CARD EACH, BAND; DRAFT)
- `b9362879` T-445 (draft): the TANOBY chambers, a card each? -- BAND (today's card, the band's own palette index set to each chamber's colour) and OWN (painted afresh, seeds 4611-4617) for all seven, sheets t445t_chambers_1/2; nothing written
- `a3f67b63` qa: C-468, the Game HAT build seen on the Mac
- `6918b523` qa: T-608 the debug row before and after, and the bag's path (v11.412.4)
- `27f71a9c` README and wiki: latest is v11.412.4
- `d6374554` ROM release v11.412.4: T-608 DEBUG's USE THE ITEM ON SLOT 1 with an evolution item ends on the field (testing builds only; the release ROMs are unchanged)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
