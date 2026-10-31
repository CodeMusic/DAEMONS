# DAEMONS v11.335.1 — release notes

*Released 2026-10-31 17:40 · built against the design bible v11.335*

- **Engine**: CodeMusic/pokefirered-daemons `de6e0d270` (context-content)
- **Design**: CodeMusic/DAEMONS `58eca6b4`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `75deab2fbfccc4bb35afc087045c4422464b76c0` |
| `daemonsContext.gba` | CONTEXT | `0df4a5785b3e20b9f3fa7b87abe9d5dd2ed9f3f0` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `afd1ae4220cbd68077e8eb62058bf2be7b723b5e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `bb806ac7a4b5dac75fbd5ef3a724d1005e2bf59e` |

## The engine since v11.334.1

- `de6e0d270` T-494/T-495/T-496: the user's choices -- at the gangway she passes on the teacher's line; on the deck she holds an orange ball
- `46ba718f9` README and wiki: MICRO-START (five pages) ahead of QUICK-START (25) and the player's manual
- `725875d7a` README and wiki: QUICK START (DAEMONS docs/DAEMONS-quickstart.pdf) beside the player's manual
- `0022d35d5` README: latest release v11.334.1

## The design and tools since v11.334.1

- `58eca6b4` field-test.json: three drifted stops -- 19 clears FLAG_HIDE_LYREBIRD (CONTEXT's run sets it on the shared save), 24 chooses the SONGBOOK and its page by label, 33 checks the take against the coins lost
- `a42b4bb8` T-493..T-496, the user's choices -- bible v11.335 (9.33): the painting, the card, the line passed on, the ball (engine de6e0d270)
- `45d89792` TODO: T-506 -- the manual's two third-book lines kept for now; whether to keep them is a question for later (the user)
- `7a907d06` README and wiki: MICRO-START (five pages) ahead of QUICK-START (25) and the player's manual
- `96be45d6` TODO: T-508 struck -- MICRO-START and the quick start's cover (cd51e23c); qa 31Oct2026 T508 52-53
- `cd51e23c` T-508: MICRO-START -- docs/DAEMONS-microstart.pdf (5 pages, a little smaller: the cover, what it is and getting it going, the buttons, playing, the words and where next); tools/manual.py --book micro, which refuses more than five pages and prints a book with no contents page once; QUICK-START, large, on the quick start's cover (a book's tag)
- `6fdab1f7` TODO: T-508 -- MICRO-START, and QUICK-START on the quick start's cover (the user)
- `30aa324e` qa: C-210 App Store screenshots of the companion, iPhone 6.9in and iPad 13in, from the playground's CONTEXT companion
- `52208259` README and wiki: QUICK START (DAEMONS docs/DAEMONS-quickstart.pdf) beside the player's manual
- `33057449` TODO: T-507 struck -- QUICK START built (8abb6663); qa 31Oct2026 T507 38-39
- `8abb6663` T-507: QUICK START -- docs/DAEMONS-quickstart.pdf (A5, 25 pages, large type): what DAEMONS is (the world, the stories, the two books, the third only as rumour), getting it going (the app, the playground), ten steps of how to play a page each, where to read more, and the words to know; tools/manual.py --book quick prints it from docs/manual-quick/ (the player's manual unchanged); ten theatre frames copied from the manual's, the iPad picture, and a drawing of the buttons
- `0aea7f13` TODO: T-507 -- QUICK START, a short manual in large type (the user, relayed)
- `d482f99b` qa: theatre film of v11.334.1's story fixes (T-500, T-502..T-505); route film_t50x.json
- `42fd7e34` README and wiki: the newest release is v11.334.1
- `1b8d971c` manual: rebuilt for v11.334.1
- `c15df69e` ROM release v11.334.1: T-500 OSRIC HATTER's sign; T-502 CRYSTAL's last words in the lab; T-503 BRAZEN reads and steers; T-504 MOM's ship line ends and DAVID called; T-505 the WAREHOUSE's remnants; v11.333.x sealed (all DRAFT)

## The design bible's own entry for v11.335

### v11.335 — 2026-10-31

- **9.33, the user's choices for the lioness (T-493 to T-496).** The painting reads IT'S REAL. IT'S YOURS. and the card reads IT GOT THERE. At the gangway she passes on the teacher's line. On the deck only, she holds an orange ball, the same in both editions, on the game's first graphics id past 255.
- A Settled entry in section 10.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
