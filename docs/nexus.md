# THE NEXUS (T-395)

*Designing with the user, 2026-10-09. Lineage: **THE PAINTED MIRROR** (`docs/archive/The Painted Mirror.rtf`), a
seven-episode story in the user's voice. Every in-game word here is DRAFT. Who each figure stands for in the user's
life is private (`docs/private/`); in the game each is only an animal and a word.*

## The way in

- **The singing fir stands in every grove**, as well as on the S.S. Anne's empty pier (T-10). **Until the player
  holds the key** (THE BAND'S SHEET), every fir is flat: a dim, washed-out overlay on its colours, and its tune a
  semitone wrong. The player remarks on it -- the source: *"The song sounded perfect... so why did this look out of
  place?"*
- **With the key, any fir is a door**: A on it, and the player walks into the NEXUS.

## The NEXUS

**A place between the worlds, made entirely of paint** (the source: *"a universe made entirely of paint"*): its own
environment art -- ground, trees, sky -- drawn for it with spriteforge, as everything in it is. Night, with light
coming from the creatures and the music.

- **Its trees are doors to the groves.** A grove the player has been in: an ordinary-looking tree, and through it the
  player arrives in that grove beside its fir, which leads back. A grove not yet found: a **greyer tree**, and A on it
  says the source's line -- *"the harder I tried to open the door, the less real it became... until it changed back
  into mere dots and lines"*: the door will not open; the more one tries, the more it turns to smudge. (A grove is
  found by finding its tree in the world; the NEXUS never gives one away.)
- **One Christmas tree in the NEXUS** -- the way home, to the S.S. Anne's pier.
- **The GUARDIAN OF THE NEXUS is a voice, never seen.** Leaving by any door, it speaks -- a different line at each,
  each taken from what it says in the source: *"Remember what you have learned!"*; *"You were never lost..."*; *"Those
  notes were never flat -- they were just misunderstood"*; *"Every universe has a mirror, and it is your heart
  alongside your head that will be your compass."*
- **THE (NOT A) HUNTER**: an NPC, **a bear in red plaid**. *"Hunter? I'm no hunter... not anymore."* Then guidance
  close to the source's: the animals are precious; charm balanced with firmness; walls where doors should be.

## Who lives there (SETTLED with the user 2026-10-09; names DRAFT until played)

Every resident is NEXUS-only and **drawn new, in paint** -- made of paint, as the NEXUS itself is -- with spriteforge;
the species underneath is only a slot for its type, stats and routines, chosen so the type says something true.

| from the source | daemon | slot (type) | the drawing |
|---|---|---|---|
| the small wolf that brings the painted mirror | **REFLECTION** | ABSOL (OPAQUE), one stage | a small wolf, a little painted mirror in its mouth |
| the deer whose light shows the wolves are friends | **LODESTAR** -- a star, compassion, hope | JIRACHI (HARDENED / CONTEXT), the wish star; it does not evolve | a deer, a star's light in it |
| the Tutoring Tiger (the dedications) | **PERIHELION** | RAIKOU (SIGNAL) | a tiger with a comet's look, cosmic, and a teacher's |
| the Lovely Lioness (the dedications) | **LYUBOV** | ENTEI (ENTROPY) | a lion, proud and full of class, a Russian feel |
| the shadows of animal forms: those the narrator could not reach, and walked away from for their own well-being | **MULTIMAL** -> **ILLUMINED** | FEEBAS -> MILOTIC (FLOW): the overlooked, then radiant | a silhouette of many animals at once -- not all dark: something within it holds hope and light; grown, that light is what it is |
| the lynx point, and the Egyptian Siamese | **LYNX** -> **BASTET** | SKITTY -> DELCATTY (CONTENT) | a lynx point Siamese kitten; grown, a cat that looks Egyptian |
| the phoenix whose cry makes the shadows clear | **PHOENIX** (already ours, HO-OH) | -- | met here too; its sprite is shared with the rest of the game |
| the Christmas penguin, the narrator's inner penguin | **PENGUIN** (already ours) | -- | the penguin of PENPHEN (episode 5); its sprite is shared too |

**Their colour (the user, 2026-10-09): full natural colour, as paint -- with their type's colour emphasised** (its
drips, a glow, brush accents): REFLECTION OPAQUE's near-black ink; LODESTAR HARDENED's straw gold and CONTEXT's magenta;
PERIHELION SIGNAL's teal comet; LYUBOV ENTROPY's golden yellow; MULTIMAL and ILLUMINED FLOW's deep blue; LYNX and BASTET
CONTENT's bone. **An explicit exception to invariant 5 for the NEXUS residents** -- to go in the bible's decision log
with the next design change.

**Not placed**: the dolphin (episode 5 is after the NEXUS, and no free species is a dolphin), the Dignified Deer of the
dedications (the NEXUS deer already), the Egyptian Bastet, the Mole-mole (DIGLETT is TAPPOINT), the Eagle, the comet,
Santa (on the road home, not the NEXUS).

## The drawings (spriteforge, `gfx/drafts/nexus/`; each draft's seed and prompt beside it)

Chosen by the user, 2026-10-09 -- still to be cleaned to the 64px sprite and approved on a sheet:

- **REFLECTION**: `try4/reflection_p7202` -- the painted wolf, the mirror in its jaws; **the glass black** (the
  source's painted mirror is dark: "even the trees grow in the darkness of night"), a white glint so it still reads
  as a mirror -- **`try6/reflection_black_7302`, chosen: the black glass without the tree** (the user, 2026-10-09).
- **LODESTAR**: `round5/lodestar_8102` (the middle deer).
- **PERIHELION**: `round5/perihelion_8102` (the tiger with the stars).
- **LYNX**: `round5/lynx_8101`; **BASTET**: `round5/bastet_8103` (the user: "looks good"; seeds picked by the session, to confirm).
- **LYUBOV**: `round7/lyubov_full_9404` -- a lioness, folk flowers, whole (chosen 2026-10-09).
- **MULTIMAL**: `round7/multimal_9201` -- facing right, a light glowing in its chest (chosen).
- **ILLUMINED**: `round7/illumined_9101_lit` -- the white cat in a halo of light (chosen).

## In the game: eight NEW daemons (the user, 2026-10-09)

The slots first proposed above (ABSOL, JIRACHI, RAIKOU, ENTEI, FEEBAS, MILOTIC, SKITTY, DELCATTY) were already named
daemons -- `docs/still-vanilla.md` was stale (T-210 named all 386 by 2026-10-03). So the NEXUS residents are **eight new
daemons** in the engine's unused species slots (`SPECIES_OLD_UNOWN_C`..`J`), each taking its type, stats and routines
from the daemon it was modelled on. **INDEX numbers 387-394; MISSINGNO moves from 387 to 395**, still one past the
end (8.9: the entry the register does not hold), and the INDEX's count becomes 394. The save is unchanged: its INDEX
flags are sized by NUM_SPECIES (412). **MULTIMAL evolves by friendship** (Feebas's beauty cannot be raised in this
game); LYNX by the MOON STONE.

### The INDEX entries (APPROVED by the user, 2026-10-09)

| daemon | category | CONTENT | CONTEXT |
|---|---|---|---|
| REFLECTION | CANVAS | It brings a painted mirror in its mouth to anyone lost in the night. Blank canvases come in many forms, it seems to say. | The mirror reflects what its holder needs to learn. Held long enough, it is also a window into other worlds. |
| LODESTAR | GUIDESTAR | A familiar glow in the dark. In its light, fears calm, and the shapes that frightened you are seen to be friends. | Those who once saw its light walk their own path after, sure of their footing even at night. |
| PERIHELION | COMET | It passes close only once in a long while. In that pass it teaches the lesson that stays: being different is good. | Its pupils hardly saw it go. Long after, they still hear what it taught them, now in their own voices. |
| LYUBOV | DEVOTION | It sees others before they are willing to see themselves. It crosses great distances to visit, and asks nothing for the fare. | Those it saw rarely see it in time. After, they mean more to it than they can ever express, and cannot say so. |
| MULTIMAL | SHADOWS | A shadow in the shapes of many animals: those someone tried to heal, but could not reach. A small light stays lit within. | Those who walked away for their own well-being meet it again in the dark. Once they accept it, its shadow fades. |
| ILLUMINED | RADIANT | The light within it grew until it was all there was. It was always a friend. It was only that the night was dark. | Near it, the ones who were afraid feel the strength of reconnection, and are no longer afraid. |
| LYNX | FAMILIAR | A small cat that seems somehow familiar. Its tufted ears hear what most cannot, and it never forgets a visitor. | When a guest leaves, it waits by the door. It knows before they do who will be missed. |
| BASTET | BOUNDLESS | It sits as still as a temple statue. Those it watches begin to reach for more, and make things beyond their day's work. | Its keepers learn that their only limits were ever the ones they imagined. |

### OPUS's margins (DRAFT; in the game 2026-10-09, `tools/genmargins.py`)

| daemon | carried | neglected |
|---|---|---|
| REFLECTION | You have looked into the mirror it carries. You looked for a long time. | It is still holding the mirror out. Nobody has taken it. |
| LODESTAR | You have walked a long way by its light. You have not once looked lost. | It is still shining where it was left. Somebody, somewhere, is walking toward it. |
| PERIHELION | It has stayed close to you a long while now. That is not like it. | It has gone round again. It will be back. |
| LYUBOV | You saw it in time. | It came all this way. You put it away. |
| MULTIMAL | You did not walk away from this one. | You walked away. It understands. Its light is still on. |
| ILLUMINED | You stayed until it was all light. | Even put away, it is not dark in there. |
| LYNX | It follows you from room to room now. | It is waiting by the door. |
| BASTET | You have made more since you started carrying it. | It is sitting very still. It is waiting for you to begin. |

## Built (2026-10-10, DRAFT throughout)

1. **The fir in all fifteen places** (the S.S. Anne and the fourteen groves; `tools/gbagrove.py`): two objects on one
   tile, the fir before the key (`OBJ_EVENT_GFX_SINGING_FIR_DIM`, NPC_GREEN washed out, `fir_dim.pal` from
   `tools/gensingingfir.py`) and the fir, swapped the moment the sheet gives it its key. One script for every fir,
   `EventScript_SingingFir`: without the key, the off tune and the remark; with it, the tune right and **"The branches
   part, like a door. Go through?"** Arriving in a grove sets its FOUND flag.
2. **THE NEXUS** (`tools/gbanexusmap.py`): 26x23, its own tileset `gTileset_Nexus` -- the ground, the meadow, the wall of
   trees, the door tree and the Christmas tree all drawn on spriteforge (`gfx/drafts/nexus/env/`, seed and prompt beside
   each) and cleaned in the tool. The meadow is where the residents are met (TILE_ENCOUNTER_LAND).
3. **Its doors**: the mainland's seven groves down the left, the islands' down the right. A grove found is an ordinary
   tree and a door to it; one not yet found is grey -- tried, it smudges; tried again, it is only dots and lines; then
   "Only a drawing of a tree." Whole again on the next visit. **The Christmas tree** sings in key and goes home to the
   pier.
4. **The GUARDIAN** speaks at every door as the player leaves, a different line of the source's at each (fifteen).
   **THE (NOT A) HUNTER** stands in the meadow (`tools/genhunter.py`). **PHOENIX** waits once (level 35); the meadow holds
   REFLECTION, LYNX, MULTIMAL and PENGUIN, LODESTAR more rarely, PERIHELION and LYUBOV once in a long while.

Debug: JUMP > MORE > NEXUS; GAME EVENTS: THE FIR IN ITS KEY, EVERY GROVE FOUND.
