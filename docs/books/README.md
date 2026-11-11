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
DAY-mon. So are the manuals and THE OLD WORD, which stand beside them on the companion's LIBRARY shelves. There are chapter markers at every entry. Each `.chapters.json` gives every section's and entry's start and
end in seconds, so a chapter can be cut from the MP3 without re-rendering. It also names the voice the book was read in.
Made by `python3 tools/bookaudio.py <book> <out_dir>` from the companion's `server/data/<book>.json`; the TEXTBOOK and
the manuals from the markdown `tools/manual.py` prints them from (`../manual*/manual.md`), the TEXTBOOK's placards and
boards from the companion's `school.json`. `python3 tools/bookaudio.py --check` says which recordings are behind their
words, and fails on any book that has no voice yet: a new book gets one too. Like the PDFs they are DRAFT, and
each says so at its start and in its tags.

| File | The book | Its voice |
|---|---|---|
| [`audio/guide.mp3`](audio/guide.mp3) | THE PROGRAMMER'S GUIDE TO THE HUMAN MIND, 19 min | Reason: a blend made for it (`am_michael` and `bm_george`), even and unhurried |
| [`audio/the-subtle-layer.mp3`](audio/the-subtle-layer.mp3) | THE SUBTLE LAYER, 32 min | Instinct: `af_bella`, warm and full |
| [`audio/principles-of-mind.mp3`](audio/principles-of-mind.mp3) | PRINCIPLES OF MIND, CALLOW SCHOOL's TEXTBOOK ([`../DAEMONS-textbook.pdf`](../DAEMONS-textbook.pdf)), 117 min | A professor: a blend made for it (`bm_fable` and `bm_lewis`), grave and warm. The References and each chapter's Further Reading are left to the page. |
| [`audio/quick-start.mp3`](audio/quick-start.mp3) | QUICK START ([`../DAEMONS-quickstart.pdf`](../DAEMONS-quickstart.pdf)), 14 min | Patient: a blend made for it (`af_heart` and `af_sarah`), slow, with time between sentences |
| [`audio/the-players-manual.mp3`](audio/the-players-manual.mp3) | THE PLAYER'S MANUAL ([`../DAEMONS-manual.pdf`](../DAEMONS-manual.pdf)), 54 min | The adventure: a blend made for it (`am_fenrir` and `am_puck`), clear and keen |
| [`audio/the-companion.mp3`](audio/the-companion.mp3) | THE COMPANION ([`../DAEMONS-companion-manual.pdf`](../DAEMONS-companion-manual.pdf)), 58 min | A friend: a blend made for it (`af_kore` and `af_aoede`), warm and encouraging |
| [`audio/playing-together.mp3`](audio/playing-together.mp3) | PLAYING TOGETHER ([`../DAEMONS-social-manual.pdf`](../DAEMONS-social-manual.pdf)), 15 min | Two as one: half `af_jessica`, half `am_liam` |
| [`audio/a-bigger-mind.mp3`](audio/a-bigger-mind.mp3) | A BIGGER MIND ([`../DAEMONS-tiiny-manual.pdf`](../DAEMONS-tiiny-manual.pdf)), 16 min | The mind: a blend made for it (`af_nova` and `af_alloy`), calm and exact, a little bright |
| [`audio/the-old-word.mp3`](audio/the-old-word.mp3) | THE OLD WORD ([`../DAEMONS-etymology.pdf`](../DAEMONS-etymology.pdf)), 11 min | The elder: a blend made for it (`bm_daniel` and `am_santa`), slow, an old story. Where it comes from is left to the page. |
| [`audio/the-vault-audio.zip`](audio/the-vault-audio.zip) | **Sealed**, by the same name as the vault. | Its own |
| [`audio/the-vault-audio-2.zip`](audio/the-vault-audio-2.zip) | **Sealed**, by the same name as the second vault. | Its own |
| [`audio/the-vault-audio-3.zip`](audio/the-vault-audio-3.zip) | **Sealed**, by the same name as the third vault. | Its own |
| [`audio/the-origin-audio.zip`](audio/the-origin-audio.zip) | **Sealed**: THE ORIGIN OF A DAEMON, read whole -- in the companion it opens on the phone once every chapter of the book has come back. | Its teller's own: a blend made for it (`af_river` and `am_echo`), half one voice and half another, even and unhurried -- the whole, before it branched |

The companion plays each one inside its book (LISTEN, with its chapters, and SHARE to keep it), streamed from here.
