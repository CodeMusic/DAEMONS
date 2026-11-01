# DAEMONS v11.337.1 — release notes

*Released 2026-11-01 14:34 · built against the design bible v11.337*

- **Engine**: CodeMusic/pokefirered-daemons `ee8c7f1b1` (context-content)
- **Design**: CodeMusic/DAEMONS `4b001184`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e06f225cab5d57a697664f1d34e03b9b07c52faa` |
| `daemonsContext.gba` | CONTEXT | `304f2c8ecc1da9f48ce7bb59e9f2815022fe5a6f` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `afb3e8f094dd6691eb8080ba7d7076aaf4a92077` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `7bcbbfbff3f68fb0a5a15a4d5ce75f7975b2066b` |

## The engine since v11.335.6

- `ee8c7f1b1` README: daemons are said DAY-mons
- `159fd8d26` README: the latest release is v11.335.6 (2026-11-01)
- `ae8f3708c` T-509: the tarot decks in both books (DRAFT) -- a CARDS section under each layer book's cover

## The design and tools since v11.335.6

- `4b001184` qa: C-273 the hermetic cards in the app (THE SUBTLE LAYER's picture, committed for it)
- `4adee637` README and wiki: daemons are said DAY-mons, as the three books now say
- `5738d2d5` README and wiki: the newest release is v11.335.6 (2026-11-01)
- `80706c2a` TODO: T-509 the GBA half of the tarot decks (engine ae8f3708c)
- `1fc58ca6` T-509: tools/port_arcana.py, the decks' words and frames for the GBA, the theatre route, and the picture (DRAFT)
- `2ee99e52` qa: C-264 HOW TO PLAY from the iPad menu bar's Help (companion 6cc5764)
- `9702edda` bible v11.337 and T-509: a short phrase on every card, and a prophecy under it in the iOS app only (the user)
- `668f6232` qa: C-272 the tarot words as prophecy, four decks (DRAFT)
- `5d6529c3` qa: T-509 tarot frames round two (approved)
- `b23d9fed` T-509 and bible 4.39: the hermetic selector reads 'as The Deck Above, so The Deck Below, or Both as One' (the user); the Above/Below frames approved
- `58cdadf4` gfx/drafts: T-509 round two, DRAFT -- The Deck Above & The Deck Below replace SPELLCRAFT's face (stars and rays down, courses and roots up, one pulse on index 14), the deck selectors in the engine's font, and a page for a card's words
- `97581591` Manuals: DAY-mons, and not the similarly spelt, frightening word that forked from it -- the user's wording in all three books
- `8ee7436f` bible v11.336: 4.39, the two tarot decks in both books (T-509, the user) -- REASON/INSTINCT, The Deck Above & The Deck Below, four draws, prophetic words
- `43e653a4` qa: T-509 the first tarot card frames
- `2599882c` TODO: T-509 THE HERMETIC LAYER's pair is The Deck Above & The Deck Below (the user, 2026-11-01)
- `cc85f3c0` gfx/drafts: T-509 tarot card frames, DRAFT -- REASON circuit, INSTINCT gold net, SPELLCRAFT emerald on the pulse, shiny palettes, one shared back, a PAST / PRESENT / FUTURE mock
- `97c34c67` TODO: T-509 the tarot decks in both books, app and GBA (the user's design, 2026-11-01)
- `f016bc66` ai/n8n: the voice says DAEMONS as DAY-mons -- daemon/talk, daemon/voice and daemon/chat respell it in what their TTS is handed (companion C-270)
- `5fa83154` Manuals: DAY-mons and the Greek daimon, with no demon in them -- the micro start, the quick start and the player's manual
- `0375d258` ROM release v11.335.6: T-483 (5) the last spell, the thirteenth

## The design bible's own entry for v11.337

### v11.337 — 2026-11-01

- **4.39, two texts on every card (T-509, the user).** Each face keeps a short phrase on the card itself, and that is what the game and the watches show. Underneath it, a prophecy of two or three sentences in the voice of the user's universe cards is shown in the iOS app only.
- The Settled entry in section 10 now says the same.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
