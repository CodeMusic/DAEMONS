# DAEMONS v11.415.1 — release notes

*Released 2026-11-24 01:04 · built against the design bible v11.415*

- **Engine**: CodeMusic/pokefirered-daemons `0b2411e0f` (context-content)
- **Design**: CodeMusic/DAEMONS `227c53ef`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9428a08c709f1b1b5562be7b14ea142bab5a757c` |
| `daemonsContext.gba` | CONTEXT | `543f41e42a8a3a948357f75942e13e349cc2b86e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `02674ddcfff79fc2e7ef422e8adb9eb25d59bdbb` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e91952e9f79369dd983019ef94ca68d7192e8782` |

## The engine since v11.413.3

- `0b2411e0f` T-604: stage 8 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (ELATION's lilac lower body, DELTA's orange gills and cheek, SHAPING's gilded leaf and crown tuft, DEFUNCT's LATENT wings, QUINE's lavender crown, tail and paws, ZEROSHOT's spines in bloom, BURSTMODE's afterburner wings and speed line, PAIRWISE's CONTEXT claws, SYLLABUS's gilded antlers and dapples, ECLIPSE's gold corona and indigo coat, WITHDRAWAL's HARDENED plates, ATTUNE's green tutu, SEETHE's ember crest and tail, HEATDEATH's back gone to a cold violet, DUSTDEVIL's sunset wing panes), DRAFT
- `76a84271f` T-613 THE VERSES (DRAFT; DAEMONS docs/song-verses-draft.md): every song a line of verses -- each form's part its verse, set to its quote a note a syllable (T-599's draft where it has one, its INDEX entry standing in), one key and tempo a line; every summon the form's seven-note hook, unique in shape across all 400 (none lengthened, none left out); the hidden CHORUS (sSongChorusParts) sung between a final form's verses once a held daemon knows its verse whole (SHARE_CHORUS; never for a form nobody holds, SONG_NO_CHORUS); a note sounds at most NOTE_RING half beats, the rest a breath; a summoned daemon sings its whole song as it knows it (DaemonSong_StartSummoned: held, its share; nobody's, its own verse unlearned); ALMOST -- a hook in the wrong key comes back flat with PLAY's own line (EventScript_DaemonSummonAlmost); T-602's shiny notes and T-597's colour ties re-derived
- `cedc8d360` T-604: stage 7 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (SEMAPHORE's pale-gold belly, KERNEL's rose robe and tail, POLICY's rose tail tip, CANOPY's blossom, LASVEGAS's neon-violet wings, MONTECARLO's ember wings, feet and tuft, CALLOUS's magma shell grooves, SHIMMER's periwinkle wing panels, THENCASE's violet upper wings, BLOATWARE's violet dome, PERMAFROST's gold-and-russet wool crown, RIPTIDE's violet fins and lilac belly, ARCFLASH's violet spikes and mane, POSTERIOR's terracotta cap, OPTIMUM's rose crest and tail end), DRAFT
- `cf44d98c8` README: latest is v11.413.3

## The design and tools since v11.413.3

- `227c53ef` qa: T-604 stages 7 and 8, thirty later forms, built
- `92c9a613` TODO: Redmine's mirror
- `f23f10a9` T-604: stage 8 -- fifteen later forms colour in (engine 0b2411e0f), DRAFT
- `ed2f50f8` T-604 (draft): stage 8 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (ELATION's lilac lower body, DELTA's orange gills and cheek, SHAPING's gilded leaf and crown tuft, DEFUNCT's LATENT wings, QUINE's lavender crown, tail and paws, ZEROSHOT's spines in bloom, BURSTMODE's afterburner wings and speed line, PAIRWISE's CONTEXT claws, SYLLABUS's gilded antlers and dapples, ECLIPSE's gold corona and indigo coat, WITHDRAWAL's HARDENED plates, ATTUNE's green tutu, SEETHE's ember crest and tail, HEATDEATH's back gone to a cold violet, DUSTDEVIL's sunset wing panes), DRAFT, nothing built
- `d7c68517` T-613 (2): THE VERSES built (DRAFT) -- gensongs.build is the verses (genverses.parts_for, every final form's line composed once and cached by fingerprint), the T-594 songs kept as build_t594 for comparison; every summon the seven-note hook (400 different, none lengthened); the chorus table for the engine (sSongChorusParts) and the companion (songs.json chorus, ring); an INDEX entry cut to a quote's length standing in until T-599; the bass kept above C2; engine 76a84271f
- `f6bb77bc` E-20: tools/egg_sync.sh -- the newest release's ROMs and patches, and the cart backups when they change, carried hourly to roverbyteseer for THE EASTER EGG (the user, 2026-11-23: "please automate syncing new releases to roverbyteseer")
- `8548b297` C-496: ai/airun.sh's start returns at once -- the reporter's subshell holds none of the job's output open, so THE HANDS are free for other jobs while the run plays
- `4ac83a73` qa: C-493 IN PLAY on PLACES (DRAFT)
- `94845971` T-604: stage 7 -- fifteen later forms colour in (engine cedc8d360), DRAFT
- `12a4550c` T-604 (draft): stage 7 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (SEMAPHORE's pale-gold belly, KERNEL's rose robe and tail, POLICY's rose tail tip, CANOPY's blossom, LASVEGAS's neon-violet wings, MONTECARLO's ember wings, feet and tuft, CALLOUS's magma shell grooves, SHIMMER's periwinkle wing panels, THENCASE's violet upper wings, BLOATWARE's violet dome, PERMAFROST's gold-and-russet wool crown, RIPTIDE's violet fins and lilac belly, ARCFLASH's violet spikes and mane, POSTERIOR's terracotta cap, OPTIMUM's rose crest and tail end), DRAFT, nothing built
- `3ff422d2` C-496 DRAFT: ai/airun.sh -- an AI run-through started and ended from THE ENGINE ROOM (THE HANDS' ai-start, ai-stop): a copy of the newest CONTENT build with its own save and notes (~/.local/share/daemons-ai), mGBA 0.11 loading the bridge's script itself (no manual step), an mGBA of its own (the player's never closed), no build, a local mind only (paid refused); ai/inplay_beat.py reports it to IN PLAY (C-478) and stops it when END is pressed (engineAi 907c089)
- `a5ea6499` qa: C-488 the SPELL CHECK all seven days, and with its capital (DRAFT; companion 0c83d650)
- `fed2d2da` Bible v11.415: a daemon's three notes and the player's balance (T-612, T-609; the user's picks, every recommendation) -- KEY, DAY and MONTH, an outside note its own accidental; the lean the paired MARKS minus the understandings, never a number, HARMONIA in balance and the title's choice naming TECHNE or SOPHROSYNE, each type's side nine a side; T-615 and T-616 asked again after a field test
- `dbba5ed0` qa: 23Nov2026 C454 37 -- C-454 RESEARCH on a scratch site (DRAFT; companion 3058104a)
- `088bf3d9` qa: C-488 the day's SPELL CHECK on TODAY (DRAFT)
- `cb71869d` T-612 and T-609, the proposals (DRAFT): a daemon's three notes and colours (its type's key, its number on the week's and the year's wheels -- 332 sets of three against 107 for the week alone, 155 of 400 with both inside their key), and the player's balance (MARKS minus understandings, the TRUE MARK on neither side, never shown as a number) with each type's side, nine a side, 199 daemons against 201; the user's choices in each section 7
- `c2c38142` Bible v11.414: 9.37 THE SPELL LEFT RUNNING, the book of shadows (T-606; the user, 2026-11-23: "for sure have it in the vision")
- `265c4c19` T-613 (1): THE VERSES sampler (DRAFT) -- tools/genverses.py composes a line as verses set to their quotes, a note a syllable (each verse's 7-note hook ending open and unique in shape across all 400: 400 of 400, none lengthened), a hidden chorus from the line's old cry, one key and tempo a line, chords fitted to the tune; six lines and today's ROVERCUB line in audio/drafts/t613_verses, a sheet each; placeholder words where T-599 has none
- `583435bb` T-613: THE VERSES, the proposal (DRAFT) -- why 82 forms open with another's first seven notes (a line's shared cry, a type's two-note motif repeated, CONTENT and CONTEXT on one wheel), a line's song as verses with a hidden chorus and a quote a verse, the user's decisions of 2026-11-23, and the plan for ~400
- `0a9274a8` README and wiki: latest is v11.413.3
- `73d868a1` ROM release v11.413.3: T-604 stage 6, fifteen more later forms colour in as they learn their part (DRAFT)

## The design bible's own entry for v11.415

### v11.415 — 2026-11-23

- **0.7 Balance** (T-609; the user, 2026-11-23, by multiple choice, every recommendation): the player's lean is the paired MARKS held minus the understandings held, the TRUE MARK on neither side -- 0 in balance, more MARKS toward REASON, more understandings toward INSTINCT; never a number, only heard and seen (a battle's end song, C-487; a dream's integrated part, C-486); the edition mirrors the sides, never the meaning; HARMONIA in balance, and out of it the title's choice names TECHNE or SOPHROSYNE; each type's side, nine a side (199 daemons against 201). Whether balance is shown is asked again after a field test (T-616).
- **9.36 A daemon's three notes and colours** (T-612; the same answers): its KEY (its first type's, bright major, dim minor), its DAY (INDEX number mod 7 + 1 on the week's wheel) and its MONTH (mod 12 + 1 on the year's) -- its kind, what it practises, what it brings; a note outside the key its own accidental, never held; a second type adds nothing for now (T-615). What it makes with in the companion (C-490); its song unchanged. The proposals: `docs/three-notes-draft.md`, `docs/balance-draft.md`.
- Section 10: one Settled entry, two Open questions (T-615, T-616).

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
