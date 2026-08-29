# docs/

| File | What it is | Status |
|---|---|---|
| [`vision.md`](vision.md) | **The living design bible.** Every decision, including reversed ones and the reasoning behind them. Updated as work proceeds. | v3.0, working |
| [`CONTEXT-CONTENT-design-bible-v4.5.pdf`](CONTEXT-CONTENT-design-bible-v4.5.pdf) | Typeset **snapshot** at v4.5. Current. | frozen |
| [`CONTEXT-CONTENT-design-bible-v1.0.pdf`](CONTEXT-CONTENT-design-bible-v1.0.pdf) | Typeset snapshot at v1.0. | frozen |
| [`build-pdf.sh`](build-pdf.sh) · [`style.css`](style.css) | Regenerates a snapshot: `./docs/build-pdf.sh 3.1` | — |
| [`CHANGELOG.md`](CHANGELOG.md) | Version-by-version record of what moved and why. | current |
| [`two-repo-pattern.md`](two-repo-pattern.md) | Why this is two repos joined by a symlink — tradeoffs, alternatives, the gotchas we hit, and how to apply it elsewhere. | current |
| [`lineage.md`](lineage.md) | **How the theory evolved, 2011 → 2026.** A full reading of all three blogs — Neural Crossroads (2011–12), PsychologyCode (2013–14), Seeing Sharp (2021–26) — against the design bible. What the game inherits, what it has gone past, where it diverges from the iASHC rock opera, and an article-by-article map of all three sites onto the modern concept. | current |
| [`archive/psychologycode/`](archive/psychologycode/) | **Recovered.** All eight posts from the lost `psychologycode.com` (2013–14), pulled from the Internet Archive's capture of its RSS feed. Three were never reposted anywhere. | recovered 2026-08-28 |
| [`codemusic-repos.md`](codemusic-repos.md) | **All 47 CodeMusic repositories read as a bestiary.** What they give the game, what to leave alone, and the two that turn out to be the game's own argument already built. | current |
| [`sprite-prompts.md`](sprite-prompts.md) | **Generation prompts for the step-9 art pass** — starters, Crystal, the ball→box redesign. Carries the specs that constrain them, and which assets are too small to generate at all. | current |
| [`step2-type-system-notes.md`](step2-type-system-notes.md) | Build-order notes for the type system — sections 2 and 9.2 of the bible, expanded into instructions you can work from at the keyboard. | current |

## How these relate

`vision.md` is the only document that changes. The PDF is a periodic export — cut a new one when a version's worth of decisions has accumulated, name it for the version, and leave the older ones alone. They are the record of what the project believed at the time, which is worth keeping now that the bible has a Reversed section.

**Do not edit the PDFs.** Regenerate from the markdown:

```sh
./docs/build-pdf.sh 3.1
```

Bump the version line at the top of `vision.md` first, so the document and its
filename agree.

*Toolchain note:* v1.0 was cut with wkhtmltopdf, which is no longer installed.
`build-pdf.sh` uses **pandoc + headless Chrome** and targets the same A4 page.
Output is a little more generously set than v1.0 — deliberate, and the reason
the snapshots run longer than the growth in content alone would explain.
