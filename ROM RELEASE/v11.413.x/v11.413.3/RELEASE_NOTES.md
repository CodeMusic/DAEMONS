# DAEMONS v11.413.3 — release notes

*Released 2026-11-23 20:56 · built against the design bible v11.413*

- **Engine**: CodeMusic/pokefirered-daemons `e2d65ea7d` (context-content)
- **Design**: CodeMusic/DAEMONS `e95d83cf`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0075edfecf13e615c3a7984565711bb158fb7f07` |
| `daemonsContext.gba` | CONTEXT | `fc0a8eab3c9daa5e931221633bf43028c0b1414c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `66104910bf773b425e5f2bfb29d49a05f7fb87a1` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `2f9d170d02f13400beaebf9c47d4e9fab04be674` |

## The engine since v11.413.2

- `e2d65ea7d` T-604: stage 6 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (TURBULENCE's violet tail, IMPULSE's STRATUM mane, MULTICAST's night-blue wings, OBSESSION's amber muzzle and chest, SOUNDING's SIGNAL lantern and tail fin, HIBERNATE's lilac ears and paws, BUILDUP's gold wool, RESTLESS's orange crown and ruff, WIRETAP's terracotta crowns, DYNAMO's blue belly and dome, OUTLIER's violet eye and hem, MUTEX's violet trunks, MONOLITH's cyan bowl in front, PRESCIENCE's coral flight feathers, ENGRAM's gold ears), DRAFT
- `7cc04a3de` README: latest is v11.413.2

## The design and tools since v11.413.2

- `e95d83cf` qa: T-604 stage 6, fifteen later forms, built
- `7a63eb2c` C-408/C-83: n8n's public address is n8n.daemons.codemusic.ca -- straight to roverbyteseer, the relay workflows no longer needed; /webhook/daemon/ needs x-dex-secret from outside
- `62f15cc1` qa: C-484 the seven days and SIGNS & SYMBOLS in a dream book (DRAFT)
- `91a2b889` TODO: Redmine's mirror
- `842dfb13` T-604: stage 6 -- fifteen later forms colour in (engine e2d65ea7d), DRAFT
- `01ea7615` T-604 (draft): stage 6 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (TURBULENCE's violet tail, IMPULSE's STRATUM mane, MULTICAST's night-blue wings, OBSESSION's amber muzzle and chest, SOUNDING's SIGNAL lantern and tail fin, HIBERNATE's lilac ears and paws, BUILDUP's gold wool, RESTLESS's orange crown and ruff, WIRETAP's terracotta crowns, DYNAMO's blue belly and dome, OUTLIER's violet eye and hem, MUTEX's violet trunks, MONOLITH's cyan bowl in front, PRESCIENCE's coral flight feathers, ENGRAM's gold ears), DRAFT
- `51fac39c` qa: C-483 DAEMON DREAMS, a book a dreamer shelved by type (DRAFT)
- `c68917cb` README and wiki: latest is v11.413.2
- `da2a4bf7` ROM release v11.413.2: T-604 stage 5, fifteen more later forms colour in as they learn their part (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
