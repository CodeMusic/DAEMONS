# DAEMONS v11.413.2 — release notes

*Released 2026-11-23 19:47 · built against the design bible v11.413*

- **Engine**: CodeMusic/pokefirered-daemons `ac21d422e` (context-content)
- **Design**: CodeMusic/DAEMONS `0fccd2c9`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `fd60073ad5cdd7986f75781f9953e7965d4023c3` |
| `daemonsContext.gba` | CONTEXT | `0c168e3035dddf62c42535e76ab1224afba0529b` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `1f3018f6a6d3941e446ad15ee4415e7c6e12e594` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `1fc8584bc11d159143b52d7187a3e991138254bf` |

## The engine since v11.413.1

- `ac21d422e` T-604: stage 5 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (THREAD's blue ears, AXIOMKICK's orange kicking leg and feet, SHELL's violet whorls, COLDVAULT's violet outer plates, TRIPLECORE's brown plumage, OVERRUN's foxfire-violet tail, SUSPEND's pink curl, crown and feet, INJECTOR's gold abdomen, CRAVING's gold ring and honey paws, LOCKUP's coral pincers, RESENTMENT's blue rim, PIPELINE's STRATUM horn, ears and plates, GRIEVANCE's green head, COLDREAD's violet wings and facial discs, CIRCULAR's violet legs), DRAFT
- `495c9ffcd` README: latest is v11.413.1

## The design and tools since v11.413.1

- `0fccd2c9` qa: T-604 stage 5, fifteen later forms, built
- `9666a88c` TODO: Redmine's mirror (T-609 and the rest)
- `24e57f2e` T-604: stage 5 -- fifteen later forms colour in (engine ac21d422e), DRAFT
- `887a62e5` T-604 (draft): stage 5 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (THREAD's blue ears, AXIOMKICK's orange kicking leg and feet, SHELL's violet whorls, COLDVAULT's violet outer plates, TRIPLECORE's brown plumage, OVERRUN's foxfire-violet tail, SUSPEND's pink curl, crown and feet, INJECTOR's gold abdomen, CRAVING's gold ring and honey paws, LOCKUP's coral pincers, RESENTMENT's blue rim, PIPELINE's STRATUM horn, ears and plates, GRIEVANCE's green head, COLDREAD's violet wings and facial discs, CIRCULAR's violet legs), DRAFT
- `67619e9a` Merge branch 'main' of https://github.com/CodeMusic/DAEMONS
- `da6c6537` Book audio for v11.413.1 (the minor release): THE SPELL LEFT RUNNING recorded (sorcerer, 38.1 min, sources c367519d), THE COMPANION (friend, 81.4 min, sources 59ce4938) and THE PLAYER'S MANUAL (adventure, 56.4 min, sources b9865374) re-recorded -- the user: record once the hemispheres were found not to touch them
- `152afed8` qa: E-1, E-4, E-13, E-14 -- THE CHANGES, a space made public, town palettes, the egg downloaded (DRAFT)
- `24273d6f` README and wiki: latest is v11.413.1
- `52173101` ROM release v11.413.1: T-604 stage 4, fifteen more later forms colour in as they learn their part (DRAFT); seals v11.412.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
