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

## Who lives there (proposed; names DRAFT, psychology's register -- it is a mainland grove)

Every resident is NEXUS-only and drawn new, in paint, with spriteforge; the species underneath is only a slot for its
type, stats and routines, chosen so the type says something true.

| from the source | daemon | slot (type) | note |
|---|---|---|---|
| the shadows of animal forms -- those the narrator tried to heal and could not reach, and walked away from for their own well-being | **MULTIMAL** (the user's name) | SABLEYE (OPAQUE / LATENT) | a silhouette of many animals at once; what cannot be reached, unseen and latent |
| the phoenix whose cry makes the shadows clear | **PHOENIX** (already ours, HO-OH) | -- | the user: "I like Phoenix"; it can be met here |
| the wolves cloaked in the dark, feared, then friends; the small wolf with the painted mirror | a family: the small wolf, then the grown | POOCHYENA -> MIGHTYENA (OPAQUE) | names to choose |
| the deer whose light shows the wolves are friends | a deer -- **a star, compassion, hope** | JIRACHI (HARDENED / CONTEXT), the wish star; or CELEBI (CONTEXT / GROWTH) | name to choose |
| the lynx point and the Egyptian Siamese | **LYNX** -- a lynx point Siamese that looks Egyptian | SKITTY -> DELCATTY (CONTENT) | one cat or two: open |
| the Christmas penguin, the narrator's "inner penguin" | **PENGUIN** (already ours) | -- | the same penguin that pairs with the dolphin (the source's episode 5 is PENPHEN) |
| *(the dedications, not the NEXUS scenes)* the Tutoring Tiger | a tiger -- a comet's look, a teacher's | RAIKOU (SIGNAL) | name to choose |
| *(the dedications)* the Lovely Lioness | a lioness -- a Russian feel | ABSOL (OPAQUE: the one not seen in time) or ENTEI (ENTROPY) | open |

**Not placed**: the dolphin (episode 5 is after the NEXUS, and no free species is a dolphin), the Dignified Deer of the
dedications (the NEXUS deer already), the Egyptian Bastet, the Mole-mole (DIGLETT is TAPPOINT), the Eagle, the comet,
Santa (on the road home, not the NEXUS).

## To build, once the cast is settled

1. The fir in all fifteen places (the S.S. Anne and the fourteen groves), flat until the key; `tools/gbagrove.py`.
2. The NEXUS map and its painted tileset (spriteforge, `tools/spriteforge.py`, roverbyteseer by name).
3. Its doors: one per grove, ordinary once the grove has been entered (a flag per grove), grey and smudging before.
4. The GUARDIAN's lines at each door; the bear and his lines; the residents, their names, entries and painted sprites.
