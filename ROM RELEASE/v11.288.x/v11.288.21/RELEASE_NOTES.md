# DAEMONS v11.288.21 — release notes

*Released 2026-10-01 09:00 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `f23ff3b2f` (context-content)
- **Design**: CodeMusic/DAEMONS `d2f5808b`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2dac4b210a50cf6ca60737da31ffe6980222bf6e` |
| `daemonsContext.gba` | CONTEXT | `d4a267017f52ede38582ea41882d13e2cf8b555b` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `44d391d56049863361e27bc0abe0d38c32fde2ee` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `77fe7dbb5578c34168cc591cc21a1c849ffbab5d` |

## The engine since v11.288.20

- `f23ff3b2f` T-234: PENPHIN's footprints, regenerated from the new art
- `f1c4969de` T-252: the first UNDERSTANDING is arrived at in TANOBY's seventh chamber, reading its inscription
- `98bc89533` T-295: the last of BLUE's lines in AL's mouth -- the HEARSAY handover at DOLDRUM CITY (DRAFT)
- `14b5dab8e` T-232: CONTEXT's own INDEX entries -- all 137 a player can meet (approved as drafts)
- `e68e9b56a` T-224: twenty NOTEBOOK documents placed in the world (approved as drafts); PROSPECTUS 3 held for its dates
- `a74ad6932` T-257: WHAT YOU CHOSE carries its approved words; the rival's line names the rival as the player named them
- `b91c0a04e` T-290: the credits' runners drawn -- the player and AL, redrawn per pose through the sprite server (DRAFT)
- `1228fff39` T-188: INSTINCT's six margins approved; thirteen more daemons get a second line (DRAFT)

## The design and tools since v11.288.20

- `d2f5808b` Goal run, batch 1: T-188, T-249, T-257, T-224, T-232, T-252, T-290, T-295, T-301 recorded (engine 1228fff39..f23ff3b2f)
- `f6c1728f` TODO: T-256's stale WAITING tag too
- `4748c62b` TODO: clear five stale WAITING tags (T-10, T-235, T-234, T-256, T-258), all answered
- `151fc4e5` TODO: T-321 to T-326 -- dialogue metaphors, INDEX entries that teach their names, the bedroom poster, the signs, a path to the fir, MOM's own line (the user, 2026-10-01)
- `2992a0cf` ROM release v11.288.20: DOLPHIN, PENGUIN and PENPHIN

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
