# docs/books/

The game's books as PDFs, so they can be read away from the game. Each one is printed from the same text the game
prints, by `python3 tools/bookpdf.py --write`, which reprints a book only when its words or pictures change. **Do not edit
these by hand.** Every word in them is still a DRAFT, as it is in the game.

| File | The book |
|---|---|
| [`guide.pdf`](guide.pdf) | **THE PROGRAMMER'S GUIDE TO THE HUMAN MIND**, by Christopher Art Hicks. The mind read *like* software: its routines, its bugs, and how a habit gets rewritten one line at a time. 28 entries in nine chapters, from [`../guide.md`](../guide.md). |
| [`the-subtle-layer.pdf`](the-subtle-layer.pdf) | **THE SUBTLE LAYER**, *a USER's handbook*. Reading, writing and linking, the seven centres and a daily routine, taught as practice rather than doctrine. 51 entries, each with its picture, from [`../subtle-layer.md`](../subtle-layer.md). |
| [`the-vault.zip`](the-vault.zip) | **Sealed.** See below. |
| [`the-second-vault.zip`](the-second-vault.zip) | **Sealed.** See below. |
| [`the-third-vault.zip`](the-third-vault.zip) | **Sealed.** See below. |

## The vaults

People who have read both books sometimes talk about a third one. They call it THE HERMETIC LAYER, or just the
spellbook, and no two of them describe it the same way. It is said to open with a warning, to treat words as spells,
and to come after the other two, and late. The [wiki's page on it](https://github.com/CodeMusic/DAEMONS/wiki/The-Hermetic-Layer)
collects what is said about it, and the real history the rumour grew from.

`the-vault.zip` is locked with a password. It might hold that book, or it might hold nothing worth the trouble.

**A hint, in case it does exist:** in the game, a strange man lives on QUICKSILVER island. His first and last name,
written in title case with a space between them (`Firstname Lastname`), might open the vault.

Some say the spellbook was torn in two, and that the other half was read by someone else, somewhere brighter, who
thought the first half was the bad one. Some say that once, somebody put the two halves back together.

`the-second-vault.zip` and `the-third-vault.zip` are locked too.

**If the second holds anything**, it was read by an early riser in the game, a bird. What she is, with "The"
in front, in title case with a space (`The Something`), might open it.

**If the third holds anything**, it is read by whoever knows who read the other two. What each reader *is*, not
their name, the man's first, in title case and joined by "and" (`Something and Something`), might open it.

## Audio

The same books read aloud by Kokoro TTS, **each in its own voice, chosen for what the book is**, and every daemon said
DAY-mon. There are chapter markers at every entry. Each `.chapters.json` gives every section's and entry's start and
end in seconds, so a chapter can be cut from the MP3 without re-rendering. It also names the voice the book was read in.
Made by `python3 tools/bookaudio.py <book> <out_dir>` from the companion's `server/data/<book>.json`; the TEXTBOOK from
[`../manual-textbook/manual.md`](../manual-textbook/manual.md), its placards and boards from the companion's `school.json`.
`python3 tools/bookaudio.py --check` says which recordings are behind their words. Like the PDFs they are DRAFT, and
each says so at its start and in its tags.

| File | The book | Its voice |
|---|---|---|
| [`audio/guide.mp3`](audio/guide.mp3) | THE PROGRAMMER'S GUIDE TO THE HUMAN MIND, 19 min | Reason: a blend made for it (`am_michael` and `bm_george`), even and unhurried |
| [`audio/the-subtle-layer.mp3`](audio/the-subtle-layer.mp3) | THE SUBTLE LAYER, 32 min | Instinct: `af_bella`, warm and full |
| [`audio/principles-of-mind.mp3`](audio/principles-of-mind.mp3) | PRINCIPLES OF MIND, CALLOW SCHOOL's TEXTBOOK ([`../DAEMONS-textbook.pdf`](../DAEMONS-textbook.pdf)), 117 min | A professor: a blend made for it (`bm_fable` and `bm_lewis`), grave and warm. The References and each chapter's Further Reading are left to the page. |
| [`audio/the-vault-audio.zip`](audio/the-vault-audio.zip) | **Sealed**, by the same name as the vault. | Its own |
| [`audio/the-vault-audio-2.zip`](audio/the-vault-audio-2.zip) | **Sealed**, by the same name as the second vault. | Its own |
| [`audio/the-vault-audio-3.zip`](audio/the-vault-audio-3.zip) | **Sealed**, by the same name as the third vault. | Its own |

The companion plays each one inside its book (LISTEN, with its chapters, and SHARE to keep it), streamed from here.
