# DAEMONS v11.337.2 — release notes

*Released 2026-11-01 19:55 · built against the design bible v11.337*

- **Engine**: CodeMusic/pokefirered-daemons `a785f2965` (context-content)
- **Design**: CodeMusic/DAEMONS `1201aa81`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `de3ae8c54419e90b4d0d3cdfe0858121e20428e6` |
| `daemonsContext.gba` | CONTEXT | `28a075b1477c5cf8d466a6dc39683ecd40e286fc` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `be2613c3ba7e2fabb746e35708d2622ebf5485f4` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `245c694be2965b7c52ce9e462b79d8963ef16d71` |

## The engine since v11.337.1

- `a785f2965` README and wiki: THE OLD WORD (DAEMONS docs/DAEMONS-etymology.pdf), how daimon branched and why it is said DAY-mons, beside the player's manual
- `687111a31` T-483 (5): THE FIELD's intent -- the foe telegraphs its settled routine by its type's colour and a motion (DRAFT)
- `7a0eca330` README: under v11.335.6, the newest change that can be told

## The design and tools since v11.337.1

- `1201aa81` README and wiki: THE OLD WORD (docs/DAEMONS-etymology.pdf), how daimon branched and why it is said DAY-mons, beside the player's manual
- `d0888290` TODO: T-518 the books read aloud again, DAY-mons and a voice for each book (claimed, WIP)
- `27db3ca9` TODO: T-483 (5) FIELD's intent (engine 687111a31)
- `bdf76400` qa: T-483 FIELD's intent, filmed
- `31f4417e` TODO: T-510..T-516, the user's choices on THE SUBTLE LAYER's loose ends (CLOSURE, THE LOG, the INTERPRETER, Ty's words, the bands, the lioness's card, the practices)
- `62e45eee` T-483 (5): the route that films THE FIELD's intent (four turns, the foe's settled routine read beside each breath); not yet played -- the theatre was down
- `7fac61cf` TODO: T-517 THE OLD WORD done (f71bc9da)
- `f71bc9da` T-517: THE OLD WORD -- an illustrated book of how daimon branched, printed beside MICRO-START and QUICK-START
- `ea9ebada` TODO: THE OLD WORD moves from T-510 to T-517 -- another session's unpushed T-510..T-516 (THE SUBTLE LAYER's loose ends) keep their numbers
- `035b55b5` bookaudio.py: the books' voice says DAEMONS as DAY-mons -- daemon(s) respelled daymon(s) in what Kokoro is handed, as the hub's voices do (companion C-270); the MP3s are still the old reading until they are made again
- `a173bf3c` TODO: T-510's where column
- `11c588f4` TODO: T-510 claimed -- THE OLD WORD, an illustrated book of how daimon branched (the user, 2026-11-01)
- `96b90d65` README and wiki: under v11.335.6, the newest change that can be told (v11.335.1's lioness) and what comes next (THE SUBTLE LAYER's CARDS)
- `35a48bfb` Books read aloud: MP3s with chapter markers, the third sealed like the vault
- `1fdbaacd` ROM release v11.337.1: the v11.335.x seal's notes PDF
- `7de38eed` ROM release v11.337.1: T-509 the tarot decks in both books on the GBA -- the card of the day, a single draw, PAST/PRESENT/FUTURE and MIND/BODY/SPIRIT; v11.335.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
