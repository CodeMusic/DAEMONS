# Getting the songs into the game

The tracks cannot be imported. Gen 1 audio is **two pulse channels, one 4-bit
wave channel and noise**, and every note is an assembler instruction — there is
no sampling and no playback. So the question is not conversion, it is
**transcription, then arrangement**.

And the constraint that shapes everything: **Claude cannot hear audio.** Gemini
can. So Gemini is the ear, the same division of labour `sprite-prompts.md` uses
for images.

---

## Ask for the hook, not the song

**Eight notes, not three minutes.** Two reasons, and both matter more than they
sound.

**It is the only part an LLM transcribes reliably.** Key, tempo and a short
monophonic hook are within reach. A full multi-track transcription is where
these models invent — confidently, and in a form nobody can check by reading it.
A hook is short enough that you can hum it back and know instantly whether it is
right.

**And it is the only part the hardware wants.** Four channels cannot hold an
arrangement with vocals. They hold a **leitmotif** perfectly — which is the
better design anyway: Crystal's motif surfacing inside Blanche's theme and again
at the Review Board does what 7 actually asks for, *"the rock opera stops
sitting on top of the game and starts being its level design."*

---

## The prompt

Give Gemini the audio file and this, verbatim:

> You are transcribing a song so it can be rearranged for the Game Boy sound
> chip — two square-wave voices, one bass voice, no chords per voice.
>
> I need **only the single most recognisable hook**: the four to eight notes a
> listener would hum back. Not the whole song, not the vocal line in full, not
> a section-by-section breakdown.
>
> Answer in exactly this format and nothing else:
>
> ```
> KEY:    <e.g. D minor>
> TEMPO:  <BPM, a number>
> METER:  <e.g. 4/4>
> HOOK:   <note><octave>/<beats>  … space separated, 4-8 notes
>         example -> D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
> BASS:   same format, one note per chord change under that hook
> CHORDS: e.g. Dm | Dm | Bb | A
> FEEL:   one line — sparse or dense, driving or still, major or minor
> DOUBT:  what you are least sure of, and say plainly if the key or the
>         hook is a guess
> ```
>
> If you cannot hear something clearly, write `unsure` in that field. **Do not
> fill a field by inference.** A wrong key is worse than a blank one, because
> it will be checked against a colour mapping and quietly corrupt it.

**The `DOUBT` field is not politeness.** It is the only error-detection in the
loop — nobody downstream can hear the source either.

---

## What happens on the way back

Each answer is checked before a note is written:

- **KEY against 7.2's mapping.** Town keys come from the octave-folded visible
  spectrum, and character motifs have to sit inside the key of wherever they
  appear. A motif in the wrong key is not a small problem — the whole of 7 is
  the key relationships.
- **TEMPO into `tempo`**, roughly 1:1 with BPM.
- **HOOK into `note` / `octave`**, and the pitch set gets checked — Blanche is
  strictly pentatonic, so a motif appearing there must be too, or it must be
  the moment the pentatonic breaks, deliberately.
- **CHORDS become the second pulse channel**, BASS the wave channel.
- All channels are then verified to the same total length, mechanically. A
  desync is inaudible in source and obvious in play.

---

## Order to do them in

**1. `01. Crystal's Lament`.** Her motif has the most places to be: the lab,
Blanche, and the Review Board where she records you into the Index. One
transcription, three appearances.

**2. `07. Fit for Work (Scorn's Directive)`** — 4.10's procedure, and the
Quicksilver material.

**3. `03. Scorn's Solution`** — Scorn and Corpus, so Brazen and the lobby.

**4. `08. Slumbering S.T.A.R.R.`** and **`02. Fox in the Shadows`** — the two
things buried in the ruins.

*Not needed yet:* the town themes themselves. Those are composed from the
colour mapping, not transcribed — Blanche already was.

---

## If MIDI ever exists

If anything in the chain can export MIDI, say so — that removes Gemini from the
loop entirely and a MIDI → `pokered` asm converter is a small tool worth
writing once. Suno and ACE-Step do not export it; a DAW would.

**ACE-Step is the wrong tool for this job.** It generates music, it does not
analyse it. It cannot tell you what is in a track you already have.

---

# The prompts, one per song

**Attach the audio file.** Gemini cannot stream from SoundCloud — given only a
link it will read the *page* and can produce a confident, wholly invented
transcription. That is the worst failure available here, because fabricated
notes are indistinguishable from real ones once they are text. Every prompt
below therefore opens with a gate that forces Gemini to declare whether it can
actually hear anything.

The links are for finding and downloading the track, not for Gemini to fetch.

Paste one at a time and bring the answers back.

---

## 1 — Crystal's Lament → CRYSTAL's motif

`https://soundcloud.com/codemusai/01-crystals-lament`

> Before anything else: if you have not been given an audio file you can
> actually listen to, reply exactly `NO AUDIO` and stop. Do not describe, infer
> or reconstruct this song from its title, description, lyrics or any web page.
>
> You are transcribing a song so it can be rearranged for the Game Boy sound
> chip — two square-wave voices, one bass voice, no chords per voice.
>
> I need **only the single most recognisable hook**: the four to eight notes a
> listener would hum back. Not the whole song, not the full vocal line, not a
> section-by-section breakdown.
>
> Answer in exactly this format and nothing else:
>
> ```
> KEY:    <e.g. D minor>
> TEMPO:  <BPM, a number>
> METER:  <e.g. 4/4>
> HOOK:   <note><octave>/<beats> … space separated, 4-8 notes
>         example -> D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
> BASS:   same format, one note per chord change under that hook
> CHORDS: e.g. Dm | Dm | Bb | A
> FEEL:   one line — sparse or dense, driving or still, major or minor
> DOUBT:  what you are least sure of; say plainly if the key or hook is a guess
> ```
>
> If you cannot hear something clearly, write `unsure` in that field. **Do not
> fill a field by inference.** A wrong key is worse than a blank one — it will
> be checked against a colour-to-pitch mapping and would quietly corrupt it.

## 2 — Fit for Work (Scorn's Directive) → the procedure

`https://soundcloud.com/codemusai/07-fit-for-work-scorns`

> *(same prompt as above)*

## 3 — Scorn's Solution → SCORN, and Corpus

`https://soundcloud.com/codemusai/03-scorns-solution`

> *(same prompt as above)*

## 4 — Slumbering S.T.A.R.R. → the thing in the ruins

`https://soundcloud.com/codemusai/08-slumbering-s-t-a-r-r`

> *(same prompt as above)*

## 5 — Fox in the Shadows (Ty's Dilemma) → TY

`https://soundcloud.com/codemusai/02-fox-in-the-shadows-tys`

> *(same prompt as above)*

## 6 — ScornSolutions Blues → Corpus, later

`https://soundcloud.com/codemusai/12-scornsolutions-blues`

> *(same prompt as above)*

## 7 — track 11, the reprise → worth doing for a different reason

`https://soundcloud.com/codemusai/11-reprise-final-extension`

Listed as *Crystal's Stand*; the URL says *reprise*. **If it reprises track 1,
the source material is already doing leitmotif work** — and comparing the two
hooks tells us whether Crystal's motif transforms or merely returns. That
difference decides how it should behave between Blanche and the Review Board.

> *(same prompt as above — and additionally: if this hook is a variation of
> another song's hook, say which, and describe how it differs: transposed,
> slower, mode changed, inverted.)*

---

## The remaining five

Not needed yet, listed so the set is complete: `04-lines-in-the-sand`,
`05-echoes-of-the-algorithm`, `06-crystal-clear-or-crystal`,
`09-nine-scars-nine-breaches`, `10-1001-fatal-error`.

`05. Echoes of the Algorithm` may belong to the Index rather than to a person,
and `10. 1001 - Fatal Error` shares its number with *A Painted Christmas* —
both worth a look once the six above are in.

---

## Bringing the answers back

Paste them raw, all together or one at a time. Each gets checked before a note
is written — key against 7.2's spectrum mapping, hook against the pitch set of
whichever town it has to appear in, then all channels verified to equal length.

**If any answer comes back `NO AUDIO`, that is the system working.** It means
the file did not reach Gemini, not that the track is untranscribable.
