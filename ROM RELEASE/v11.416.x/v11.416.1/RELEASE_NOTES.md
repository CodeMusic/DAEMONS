# DAEMONS v11.416.1 — release notes

*Released 2026-11-24 02:44 · built against the design bible v11.416*

- **Engine**: CodeMusic/pokefirered-daemons `7dc39e511` (context-content)
- **Design**: CodeMusic/DAEMONS `80fec110`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `de27dfc6bd333cf9e5c6011818f470958e2516aa` |
| `daemonsContext.gba` | CONTEXT | `cb82db18390de82c2e1aff32f200123d3b6096aa` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `cfc880552c4d343663c713a75081b353c157660c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `36466ec3a53df30f75d71e92989909ff4a47dd7b` |

## The engine since v11.415.1

- `7dc39e511` T-604: stage 9 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (CRYWOLF's tawny head and umber dapples, SIGKILL's HARDENED dome, HEARTBEAT's rose lower body, CHECKMATE's LOGIC chequered board, FORGETTING's dusk-blue hood, MINDWANDER's sky-blue head fur and lilac thought bubbles, SHIFTLEFT's brass ears, SUBTEXT's hood in its eyes' teal, BIGIRON's steel dome, TRUNKLINE's blue-violet helmet, GESTALT's lilac shell crown, ENTRAPMENT's gold web, SHALLOWS's sea-glass fins and tail, BLACKWATER's OPAQUE oil-black shell, CADENCE's hat in flower and blushing belly), DRAFT
- `485a9fc82` T-613: THE CRY IS THE HOOK (DRAFT; DAEMONS tools/gencries.py) -- every cry plays its form's own seven-note hook, the notes a player plays on the harp to summon it: the verse's pitches, its rhythm kept and quickened to 1.5 s (the user's pick, 2026-11-24), the type's voice kept, a second type ending on the flute on the hook's own last note; 399 written, pret's two unused slots unchanged; all pass DOUBLES, BACKWARD and FAINT, no two alike; ROM 13.1 MB of 16
- `d589bcf06` README: latest is v11.415.1

## The design and tools since v11.415.1

- `80fec110` qa: T-604 stage 9, fifteen later forms, built
- `143e23e5` qa: the README entries for the DASHBOARD and ACCOUNT pictures (C-511, C-513)
- `151dcfcd` T-604: stage 9 -- fifteen later forms colour in (engine 7dc39e511), DRAFT
- `12ccf2f5` T-604 (draft): stage 9 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (CRYWOLF's tawny head and umber dapples, SIGKILL's HARDENED dome, HEARTBEAT's rose lower body, CHECKMATE's LOGIC chequered board, FORGETTING's dusk-blue hood, MINDWANDER's sky-blue head fur and lilac thought bubbles, SHIFTLEFT's brass ears, SUBTEXT's hood in its eyes' teal, BIGIRON's steel dome, TRUNKLINE's blue-violet helmet, GESTALT's lilac shell crown, ENTRAPMENT's gold web, SHALLOWS's sea-glass fins and tail, BLACKWATER's OPAQUE oil-black shell, CADENCE's hat in flower and blushing belly), DRAFT, nothing built
- `c6f706df` TODO: Redmine's mirror (T-617 opened)
- `ceb794ee` qa: T-617, DAEMONS EMBODIED's design book -- its cover and seven of its parts, and its nine drawings
- `ef569298` T-617: DAEMONS EMBODIED, a daemon in a robot body -- the design, as a book for the user's review (DRAFT, nothing built), and the bible's 9.38 at v11.416
- `b41a9a82` T-613: the cry is the hook (DRAFT) -- tools/gencries.py makes every cry its form's seven-note hook, 1.5 s (the user's pick, 2026-11-24), the verse's pitches and rhythm quickened about 2.3 times, the type's voice kept and a second type ending on the flute on the hook's own last note; the first note moves on within a beat and the last rings at most a beat and a half, so all 401 pass the three checks; listening in audio/drafts/t613_cries (cry_then_hook.mp3: six cries, each followed by its hook at its song's pace); engine.md's budget at 13.1 MB of 16; engine 485a9fc82
- `e19ff1f0` qa: C-539, DAEMONS Server's dashboard, paired and in THE MESH
- `39015e98` qa: the Pi devices' DASHBOARD and ACCOUNT apps (C-511, C-513; companion cd2b0f04)
- `e93a8240` README and wiki: latest is v11.415.1
- `fbda9c9c` ROM release v11.415.1: T-604 stages 7 and 8, thirty more later forms colour in as they learn their part, and T-613 THE VERSES from the music lane (DRAFT); seals v11.413.x

## The design bible's own entry for v11.416

### v11.416 — 2026-11-24

- **9.38 DAEMONS EMBODIED** (T-617; the user, 2026-11-24): a daemon in a robot body -- designed, nothing built, DRAFT. One body program and a wrapper for each kind of body (a sheet and a driver; the PiDog first); actions the only way a daemon moves, through one gate, STOP a reflex outside any model (HANDS, C-462, built as the gate); the answer's actions in braces, performed as beats in order, as RoverByteOS did; actions the body's, the self the daemon's; a body a device that carries (C-80, 9.25, 9.26); three ways to learn a body, the starters' three (8.2); Bluetooth near, Wi-Fi for the rest, Tailscale off; THE BRAIN's regions; its own repository. The game is unchanged.
- **The design as a book**: `docs/DAEMONS-embodied.pdf`, `tools/manual.py`'s thirteenth book and the first that is a design (`docs/manual-embodied/`, nine drawings, a body on its cover).
- Section 10: one Settled entry, one Open (the design's twelve questions).

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
