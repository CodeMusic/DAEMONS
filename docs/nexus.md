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

## To build, once the cast is settled

1. The fir in all fifteen places (the S.S. Anne and the fourteen groves), flat until the key; `tools/gbagrove.py`.
2. The NEXUS map and its painted tileset (spriteforge, `tools/spriteforge.py`, roverbyteseer by name).
3. Its doors: one per grove, ordinary once the grove has been entered (a flag per grove), grey and smudging before.
4. The GUARDIAN's lines at each door; the bear and his lines; the residents, their names, entries and painted sprites.
