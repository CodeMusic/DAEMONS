# DAEMONS v11.365.1 — release notes

*Released 2026-11-14 16:40 · built against the design bible v11.365*

- **Engine**: CodeMusic/pokefirered-daemons `2ab19d87a` (context-content)
- **Design**: CodeMusic/DAEMONS `7f0ed131`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e19af209bab42e54d579878deac7f8dec17cbf6e` |
| `daemonsContext.gba` | CONTEXT | `a890ca08ee2ec84c2a23279595b4b40d6ea9250d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `6f4862732c21014c4eda61c9287814a3a2106fcf` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `5839e4077a96671c23104d1f6992412b0018a973` |

## A note on the book audio

A minor release, released with two recordings deferred (the user, 2026-11-14: "Release now, record after"): THE COMPANION's manual changed since its recording, and the new T-GLASSES book has not been recorded yet.

## The engine since v11.363.1

- `2ab19d87a` T-554: the menu leftovers in A TERMINAL (the user's picks, 2026-11-14)
- `7769547d9` The Fifth Review's tickets renumbered T-560..T-564 -> T-555..T-559 in every comment
- `e1cd3b830` Merge origin/context-content into the Fifth Review's branch (T-561 DURABLE, T-562 the dream's pointer, T-564 the grunt's HARD CODED and AL's fade), all four ROMs exit 0
- `5bcd28335` The branch's tickets renumbered T-560 to T-564 in every comment (main took T-550 and T-551 meanwhile)
- `a2a445435` README: the release line names v11.363.1
- `5d9802f27` T-554: a HARD CODED on the hideout's first grunt; AL's party fades fight by fight
- `38982aab6` T-552: the ending's two gates -- the dream points at TANOBY's seventh chamber; the sixty dropped
- `2812837c9` T-551: DURABLE holds a daemon at 1 HP when one hit from full would take it down

## The design and tools since v11.363.1

- `7f0ed131` Secret 2 redacted from the public bible and CHANGELOG (the user, 2026-11-14: redact going forward, no history rewrite) -- the 'son at the door' lines now read [private: SECRETS §2]; found by check_secrets
- `85d84b8b` THE COMPANION manual: Routines is what the daemon does -- IT SINGS (new), THE EASEL and SLEEP SOUNDS there; ITS GALLERIES (companion C-368, build 980)
- `6821575c` T-552, T-553 followers: the 27 picked fronts at follower size (T-534's reduction), and the backs-and-icons drawing script
- `47097a1f` ai/README: which mind plays the AI harness -- DAEMONS_MIND, the hub's mind by default, the Tiiny's 35B (T-560)
- `5680651e` T-552, T-553 reduced: the picks at 64x64/16 on their type ramps, autumn in grey fur, the winter ski feet by hand (the user: "Yes, reduce my picks")
- `297ae453` T-553 seasons: each MUSAI form across the year, MASKMUSAI's ski-feet passes (the user: "Fix MASKMUSAI, then seasons")
- `d7c41baa` T-552, T-553 concepts: the Rover line's cub, seer and byte; the MUSAI branch round two with its head kept (the user's pick)
- `9baff0d2` T-554 BUILT (engine 2ab19d87a): the menu leftovers -- std frame 1, every piece A
- `27e6dae7` CLAUDE.md: the push routine runs check_secrets.py and check_todo.py (the user, 2026-11-14)
- `6eeca913` The Fifth Review's follow-up: tickets T-560..T-564 renumbered to T-555..T-559, the Quicksilver order redacted, the push routine as it was
- `3bc5ef63` TODO: T-554 drafted -- the menu leftovers, A/B/C and the std frame's two versions (nothing in the engine)
- `be55f825` T-554 DRAFT: the menu leftovers drawn in A TERMINAL's family -- nothing in the engine
- `4d8219b1` qa: C-362 the song player and IT SINGS; C-361 THE ENGINE ROOM's CREATIONS
- `911728f6` Merge origin/main (the Fourth Review revised for v11.361.1, press kit) over the Fifth Review's merge
- `a64d9c0d` Merge the Fifth Review's branch: bible v11.365, tickets T-560 to T-564, the record tidied
- `b330aab1` Merge PR #1: The Fourth Review, revised for v11.361.1; press kit updated
- `6e314993` Press kit card 9 (PR #1 review): the Tiiny gets its own point, LM Studio and Ollama share one, and THE MIND's one-mind mesh is said on the card and in the third pillar
- `7ba32ad9` The Fourth Review revised for v11.361.1: every finding re-checked, a new part on what moved since v11.338; the press kit's mind caught up (any endpoint, from the phone, in testing)
- `2baad9a4` TODO: T-554 filed -- the menu leftovers, batch 1 of the 2026-11-14 re-census (the user's pick)
- `5d0c1b1b` TODO: T-552 the ROVER line's flow, T-553 the MUSAI branch creature first (the user, 2026-11-14)
- `38b2b503` Merge origin/main: the Fifth Review's five jobs as bible v11.365 over main's v11.347 to v11.364, tickets T-560 to T-564
- `303d452d` The Fifth Review's five tickets move to T-560 to T-564: main took T-550 and T-551 while the branch waited
- `54cf3d5a` qa: T-438 the Nintendo art left, 14 Nov re-census -- the top three batches at 2x (menu leftovers, field overlays, the towns' last pret tiles)
- `db64b0c0` Bible v11.364: THE SUBTLE LAYER at evolving, at naming and in crowds (T-548, T-549, T-550, v11.363.1)
- `9ea5f0bc` README and wiki Home name v11.363.1
- `9e0a9b6e` ROM release v11.363.1: THE SUBTLE LAYER at evolving ('Still me.', T-548), at naming ('A direction, not a verdict.', T-549) and in crowds (CHORUS, T-550), DRAFT; seals v11.362.x; T-GLASSES' recording deferred
- `826f7226` T-554: the Third Review's accepted sweeps, swept (engine 5d9802f2) -- bible v11.355: eleven passages amended, two rulings recorded, Al's fade in 8.6a; TODO struck
- `4ac8946d` Merge origin/main: the Fifth Review's four jobs collapsed to bible v11.354 over main's v11.347 to v11.353
- `88ff7b1e` T-550: the secrets swept again, and tools/check_secrets.py so they stay swept
- `d8f87655` Merge origin/main into the Fifth Review's branch: the bible's three versions renumbered v11.349 to v11.351
- `f1090767` T-552: the ending's two gates (engine 38982aab) -- bible v11.349: TANOBY as 4.34's step 2a, 9.17 corrected (the sixty was dead since T-27, now dropped), the Fifth Review annotated; TODO struck
- `641be46a` T-551: DURABLE holds from full HP (engine 2812837c) -- bible v11.348: 2.11, 5.3 and 5.3b say what the ability now does, 5.3b's row 1 amended; TODO struck
- `922601d4` TODO: T-553 done (caba9176) -- the record tidied; T-449 stays open, the sealed v11.337.x notes left for the user
- `caba9176` T-553: the record tidied so a session can trust it -- bible v11.347, TODO re-filed, anchors brought to the ROM, check_todo.py
- `62d63b16` TODO: T-550 to T-553 -- the Fifth Review's jobs: the secrets sweep with a check, DURABLE from full HP, the ending's two gates, the record tidied
- `5d8d6cd1` The Fifth Review (v11.338): cohesion, flow and whether the design does what it set out to do

## The design bible's own entry for v11.365

### v11.365 — 2026-11-14

*The Fifth Review's five jobs (T-555 to T-559), done on a branch 2026-11-11 and 2026-11-12 and merged over main's v11.347 to v11.364; the branch's own version numbers and its first ticket ids (T-550 to T-554) were taken by main while it waited, so one version carries all five and the tickets moved.* *Renumbered once more on 2026-11-14 (the user), to close the gap check_lexicon caught: the branch had them as T-560 to T-564 (560→555 the secrets sweep, 561→556 DURABLE, 562→557 the ending's two gates, 563→558 the record tidied, 564→559 the Third Review's sweeps); the merge commits still say the old ids. The same day the user had four CHANGELOG lines that stated the Quicksilver order redacted to [private: SECRETS §4] going forward (history unchanged), and judged two CALLOW SCHOOL chalkboard rows clues, which check_secrets.py now accepts by exact line.*

- **The Third Review's accepted sweeps, finally swept (T-559; 8.7 accepted them 2026-09-10 and no ticket carried them).** The colour sweep: 4.6 and 7.14c no longer describe a greyscale game. The tempo sweep: 7.9 re-read at n=4 — S.T.A.R.R. is the outlier only asleep; it wakes at the people's 128. The SLEEP sweep: 4.5 and 4.25 say SUSPENDED, and SUSPEND being SUSPENDED is kept as the joke (the user). Brazen's B-section: 7.11's row and 7.13 corrected to the re-scanned hook, the music owned as a composition choice (the user). The small faults: Vera's birth order, Ty's key, 4.14's inversion and 4.17's reachability annotated. 8.7's ideas taken: HARD CODED (the Choice Band's name since 1.6c) on the hideout's first grunt; Al's party fading fight by fight, 255 to 0, in 8.6a; the INDEX-sprite idea noted as superseded by T-424's grey INDEX.
- **The ending's two gates (T-557, the Fifth Review's third finding; the user by multiple choice).** 4.34's order gains step 2a, TANOBY's seventh chamber: it was the cave's second gate in the flags and in 0.7 and never in the ending's own table. The dream the unread cave wakes you from (T-254) now ends on one line in S.T.A.R.R.'s register, DRAFT: *SEVEN ISLAND. SEVEN CHAMBERS. / THE SEVENTH HAS NOT BEEN READ.* And 9.17 is corrected: in play the GLOBAL INDEX has come from the aide on `FLAG_CRYSTAL_GONE` alone since T-27, so the sixty-daemon count the bible, the Fourth Review and the Fifth all named as a gate was dead code on an unreachable path. The user dropped it outright; Act 2 opens on the REVIEW BOARD and only that.
- **The secrets swept again (T-555, the Fifth Review's first finding).** Three of the four things CLAUDE.md keeps out of public writing had become readable in tracked files since the 2026-09-27 redaction: the lineage (twice), this log (nine lines, three older than the first redaction), the bible (4.3, 4.6, 4.24 and the renames table), the school document's notebook table, the Second and Third Reviews, and a port tool's docstring. Each now reads `[private: SECRETS §n]` or says the fact without the relation; the posts README names all four. `tools/check_secrets.py` greps every tracked file for them on each push, from a patterns file that lives in `docs/private/` and is never committed.
- **DURABLE holds from full HP (T-556, the Fifth Review's second finding).** 2.11, 5.3 and 5.3b said CAIRN's line "cannot be knocked out in one blow, at any level"; the ability was vanilla's STURDY, which in Gen 3 stops only the four one-hit-KO routines, so a strong hit took HEAP down in one and BENCHMARK 1 had no mechanic. The later generations' rule is built: a daemon with DURABLE at full HP survives any single hit with 1 HP left (ENDURE and FAILSAFE keep precedence; a SUBSTITUTE takes the hit; the one-hit-KO block stays). Its line, DRAFT: *did not go down to one hit!* Its description, DRAFT, in 2.11's register: *No one hit takes it from full.* The three sections say so; 5.3b's row 1 is amended.
- **The record tidied (T-558, the Fifth Review's plans section).** No design moved; eight bodies were brought to what the build already does. 8.1's slice list says the chart is seventeen types, as it has been since 2026-09-10. 8.4's "trap to avoid" is read with 0.4's 2026-09-04 ruling and logged as **Reversed**: the pair is a pair on purpose, and neither entry reports a feeling. 8.6's "restraint clause holds at two" is logged as **Reversed** by the dozen meanings colour now carries; what survived is invariant 5 as practised, one meaning per colour and none explained. 4.5's ORPHAN is marked superseded on the GBA build (REMNANT to COREFILE, MISSINGNO's blank entry) and its open sequencing question answered by the build. 8.2a's "he is not the same" is reconciled with 4.37's "SCORN is unchanged": the staff's account and the fact. 4.1's opening row no longer says the thesis is stated. 4.3's "Ty is not in the endgame" survives as *not on the ladder*. 4.33's placement is settled (T-22); his name stays OPEN.
- **8.7's accepted sweeps have a ticket at last**: T-559 carries the colour, tempo and SLEEP sweeps, Brazen's B-section, the small continuity faults, CONVICTION, Al's desaturating party and the INDEX sprite's fixed saturation.
- **Outside the bible, the same ticket**: 21 open rows re-filed from under TODO's Closed heading, T-456, T-457 and T-433 struck, the PKRS question struck (MEME, T-258), the T-267 reservation cleared; CLAUDE.md no longer carries a bible version to drift (it said v11.296 for five weeks) and names the GBA fork in its first line; the READMEs and the wiki name v11.346.2; wiki/Editions says 398 entries; docs/README's dead PDF links gone, engine.md's "eight traps" forty-three, school.md and its row say built; `tools/check_todo.py` fails the push on an open row under Closed, a spent reservation or a stale release line.
- **Decision log**: five Settled rows, and two rows in Reversed (8.4's trap, 8.6's restraint clause).

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
