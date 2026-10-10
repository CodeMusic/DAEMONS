# THE NEXUS's environment, drawn on spriteforge (T-395, 2026-10-10) -- DRAFT

Twenty-six drafts were drawn; every one's record is here (`<name>.json`: prompt, negative, seed, steps), so any can be
drawn again exactly with `python3 tools/spriteforge.py again <json>`. Only the five the game is built from are kept as
PNGs; `tools/gbanexusmap.py` reads them (its `ART` table says which crop of each).

| piece | drawing | why |
|---|---|---|
| the ground | `calm_12001` | swirls of indigo and violet paint, a floor made of paint; the first grounds (`ground_*`) were meadows, too busy to walk on |
| the meadow | `meadow_11003` | grass and flowers in paint, where the residents are met |
| the wall | `wall_11001` | dark leaves, darkened further for a place that is always night |
| the door tree | `tree_11004` | its canopy, cropped and given a drawn round silhouette; the grey door's three states are its own pixels |
| the Christmas tree | `xmas_11002` | every branch a different colour -- "it seemed to sparkle a different color as each unique note was sung" |

No cut-out model could lift a tree out of a whole painted scene (isnet-general-use, isnet-anime and u2net were tried),
so the trees are crops inside a silhouette drawn by the tool: the paint is the draft's, the edge is ours. The
`gametree_*` drafts asked for a game asset and came back as pixel art, which is not this place.
