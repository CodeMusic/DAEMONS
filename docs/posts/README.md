# docs/posts/

Blog drafts written for **Seeing Sharp**, kept in the repo so they version with
the design they describe. **Nothing here has been published** — these are drafts
for review and manual posting.

| Draft | For | Status |
|---|---|---|
| [`2026-08-seeingsharp-announcement.md`](2026-08-seeingsharp-announcement.md) | The project announcement — three blogs, the theory, the cast, the engine | draft, ~2,300 words |
| [`2026-08-seeingsharp-announcement.html`](2026-08-seeingsharp-announcement.html) | Same post as clean HTML, for the WordPress **Code editor** | generated |
| `feature-image.jpeg` | Header image | — |

## House style, from reading 77 Seeing Sharp posts

- Emoji section markers (🧠 🎭 🔁 🎨 ✨ 🌀), one per `##`
- Short paragraphs; single-sentence lines used for rhythm
- Blockquotes carry the load-bearing claims, not decoration
- Bold on the phrase that would survive being the only thing remembered
- `---` between movements
- Closing **Stay Connected** block with the standard link list

## Publishing

WordPress does not reliably convert pasted Markdown. Two working routes:

1. **Code editor.** In the block editor: Options (⋮) → Code editor, or
   `Ctrl/Cmd + Shift + Alt + M`. Paste the `.html` file, then switch back to
   Visual. Most reliable.
2. **Rendered page.** Copy from a rendered view of the post and paste into the
   Visual editor — headings, bold, links, quotes and tables all carry over.

Regenerate the HTML after editing the Markdown:

```sh
pandoc docs/posts/<post>.md --from=gfm --to=html5 -o docs/posts/<post>.html
```


## Spoiler discipline

The design bible's craft rule 1 is *never say the thesis* — that governs
characters inside the game, not posts outside it. But three things stay out of
public writing regardless, because a reader who knows them cannot un-know them:

- The Five Witnesses lock and its number
- Ty Clear's parentage, which the game asks the player to infer
- The Corpus lobby engraving

The current draft keeps all three back.
