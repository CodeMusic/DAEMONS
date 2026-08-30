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
notes are indistinguishable from real ones once they are text. The links below
are for finding and downloading the track, not for Gemini to fetch.

**The prompt is deliberately identical for every track, and never names the
song.** That is not laziness — a title is precisely the material a model would
use to fabricate a transcription it cannot actually hear, so withholding it is
what makes the `NO AUDIO` gate mean something. Copy the whole block as-is.

Do them one at a time and bring the answers back raw.

---

## 1 — Crystal's Lament

`https://soundcloud.com/codemusai/01-crystals-lament`

**CRYSTAL's motif.** Her theme has three homes for one transcription: the lab, Blanche Town, and the Review Board where she records you into the Index.

```
Before anything else: if you have not been given an audio file that you can
actually listen to, reply with exactly NO AUDIO and stop. Do not describe,
infer, or reconstruct this song from a title, a description, lyrics, an artist
page, or anything you may have read. Only transcribe what you can hear.

You are transcribing a song so it can be rearranged for the Game Boy sound
chip: two square-wave voices, one bass voice, and no chords within a voice.

I need ONLY the single most recognisable hook -- the four to eight notes a
listener would hum back afterwards. Not the whole song, not the complete vocal
line, and not a section-by-section breakdown.

Reply in exactly this format and nothing else:

    KEY:    (e.g. D minor)
    TEMPO:  (BPM, a number)
    METER:  (e.g. 4/4)
    HOOK:   note+octave/beats, space separated, 4 to 8 notes
            for example:  D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
    BASS:   same format, one note per chord change underneath that hook
    CHORDS: e.g.  Dm | Dm | Bb | A
    FEEL:   one line -- sparse or dense, driving or still, major or minor
    DOUBT:  what you are least sure of. Say plainly if the key or the hook
            is a guess.

If you cannot hear something clearly, write "unsure" in that field. Do not
fill a field by inference. A wrong key is worse than a blank one, because it
will be checked against a colour-to-pitch mapping and would quietly corrupt
it.
```

---

## 2 — Fit for Work (Scorn's Directive)

`https://soundcloud.com/codemusai/07-fit-for-work-scorns`

**The procedure** — 4.10 by name, and the Quicksilver material.

```
Before anything else: if you have not been given an audio file that you can
actually listen to, reply with exactly NO AUDIO and stop. Do not describe,
infer, or reconstruct this song from a title, a description, lyrics, an artist
page, or anything you may have read. Only transcribe what you can hear.

You are transcribing a song so it can be rearranged for the Game Boy sound
chip: two square-wave voices, one bass voice, and no chords within a voice.

I need ONLY the single most recognisable hook -- the four to eight notes a
listener would hum back afterwards. Not the whole song, not the complete vocal
line, and not a section-by-section breakdown.

Reply in exactly this format and nothing else:

    KEY:    (e.g. D minor)
    TEMPO:  (BPM, a number)
    METER:  (e.g. 4/4)
    HOOK:   note+octave/beats, space separated, 4 to 8 notes
            for example:  D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
    BASS:   same format, one note per chord change underneath that hook
    CHORDS: e.g.  Dm | Dm | Bb | A
    FEEL:   one line -- sparse or dense, driving or still, major or minor
    DOUBT:  what you are least sure of. Say plainly if the key or the hook
            is a guess.

If you cannot hear something clearly, write "unsure" in that field. Do not
fill a field by inference. A wrong key is worse than a blank one, because it
will be checked against a colour-to-pitch mapping and would quietly corrupt
it.
```

---

## 3 — Scorn's Solution

`https://soundcloud.com/codemusai/03-scorns-solution`

**SCORN, and Corpus.** Belongs under Brazen and the lobby.

```
Before anything else: if you have not been given an audio file that you can
actually listen to, reply with exactly NO AUDIO and stop. Do not describe,
infer, or reconstruct this song from a title, a description, lyrics, an artist
page, or anything you may have read. Only transcribe what you can hear.

You are transcribing a song so it can be rearranged for the Game Boy sound
chip: two square-wave voices, one bass voice, and no chords within a voice.

I need ONLY the single most recognisable hook -- the four to eight notes a
listener would hum back afterwards. Not the whole song, not the complete vocal
line, and not a section-by-section breakdown.

Reply in exactly this format and nothing else:

    KEY:    (e.g. D minor)
    TEMPO:  (BPM, a number)
    METER:  (e.g. 4/4)
    HOOK:   note+octave/beats, space separated, 4 to 8 notes
            for example:  D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
    BASS:   same format, one note per chord change underneath that hook
    CHORDS: e.g.  Dm | Dm | Bb | A
    FEEL:   one line -- sparse or dense, driving or still, major or minor
    DOUBT:  what you are least sure of. Say plainly if the key or the hook
            is a guess.

If you cannot hear something clearly, write "unsure" in that field. Do not
fill a field by inference. A wrong key is worse than a blank one, because it
will be checked against a colour-to-pitch mapping and would quietly corrupt
it.
```

---

## 4 — Slumbering S.T.A.R.R.

`https://soundcloud.com/codemusai/08-slumbering-s-t-a-r-r`

**4.7** — the thing in the ruins.

```
Before anything else: if you have not been given an audio file that you can
actually listen to, reply with exactly NO AUDIO and stop. Do not describe,
infer, or reconstruct this song from a title, a description, lyrics, an artist
page, or anything you may have read. Only transcribe what you can hear.

You are transcribing a song so it can be rearranged for the Game Boy sound
chip: two square-wave voices, one bass voice, and no chords within a voice.

I need ONLY the single most recognisable hook -- the four to eight notes a
listener would hum back afterwards. Not the whole song, not the complete vocal
line, and not a section-by-section breakdown.

Reply in exactly this format and nothing else:

    KEY:    (e.g. D minor)
    TEMPO:  (BPM, a number)
    METER:  (e.g. 4/4)
    HOOK:   note+octave/beats, space separated, 4 to 8 notes
            for example:  D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
    BASS:   same format, one note per chord change underneath that hook
    CHORDS: e.g.  Dm | Dm | Bb | A
    FEEL:   one line -- sparse or dense, driving or still, major or minor
    DOUBT:  what you are least sure of. Say plainly if the key or the hook
            is a guess.

If you cannot hear something clearly, write "unsure" in that field. Do not
fill a field by inference. A wrong key is worse than a blank one, because it
will be checked against a colour-to-pitch mapping and would quietly corrupt
it.
```

---

## 5 — Fox in the Shadows (Ty's Dilemma)

`https://soundcloud.com/codemusai/02-fox-in-the-shadows-tys`

**TY** — buried in the Quicksilver ruins.

```
Before anything else: if you have not been given an audio file that you can
actually listen to, reply with exactly NO AUDIO and stop. Do not describe,
infer, or reconstruct this song from a title, a description, lyrics, an artist
page, or anything you may have read. Only transcribe what you can hear.

You are transcribing a song so it can be rearranged for the Game Boy sound
chip: two square-wave voices, one bass voice, and no chords within a voice.

I need ONLY the single most recognisable hook -- the four to eight notes a
listener would hum back afterwards. Not the whole song, not the complete vocal
line, and not a section-by-section breakdown.

Reply in exactly this format and nothing else:

    KEY:    (e.g. D minor)
    TEMPO:  (BPM, a number)
    METER:  (e.g. 4/4)
    HOOK:   note+octave/beats, space separated, 4 to 8 notes
            for example:  D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
    BASS:   same format, one note per chord change underneath that hook
    CHORDS: e.g.  Dm | Dm | Bb | A
    FEEL:   one line -- sparse or dense, driving or still, major or minor
    DOUBT:  what you are least sure of. Say plainly if the key or the hook
            is a guess.

If you cannot hear something clearly, write "unsure" in that field. Do not
fill a field by inference. A wrong key is worse than a blank one, because it
will be checked against a colour-to-pitch mapping and would quietly corrupt
it.
```

---

## 6 — ScornSolutions Blues

`https://soundcloud.com/codemusai/12-scornsolutions-blues`

**Corpus, later.** Compare against track 3: if they share a hook, Scorn's motif is already transforming across the act.

```
Before anything else: if you have not been given an audio file that you can
actually listen to, reply with exactly NO AUDIO and stop. Do not describe,
infer, or reconstruct this song from a title, a description, lyrics, an artist
page, or anything you may have read. Only transcribe what you can hear.

You are transcribing a song so it can be rearranged for the Game Boy sound
chip: two square-wave voices, one bass voice, and no chords within a voice.

I need ONLY the single most recognisable hook -- the four to eight notes a
listener would hum back afterwards. Not the whole song, not the complete vocal
line, and not a section-by-section breakdown.

Reply in exactly this format and nothing else:

    KEY:    (e.g. D minor)
    TEMPO:  (BPM, a number)
    METER:  (e.g. 4/4)
    HOOK:   note+octave/beats, space separated, 4 to 8 notes
            for example:  D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
    BASS:   same format, one note per chord change underneath that hook
    CHORDS: e.g.  Dm | Dm | Bb | A
    FEEL:   one line -- sparse or dense, driving or still, major or minor
    DOUBT:  what you are least sure of. Say plainly if the key or the hook
            is a guess.

If you cannot hear something clearly, write "unsure" in that field. Do not
fill a field by inference. A wrong key is worse than a blank one, because it
will be checked against a colour-to-pitch mapping and would quietly corrupt
it.
```

---

## 7 — track 11 — listed as Crystal's Stand, slugged *reprise*

`https://soundcloud.com/codemusai/11-reprise-final-extension`

**Worth doing for a different reason.** If it reprises track 1, the source material is already doing leitmotif work — and comparing the two hooks says whether Crystal's motif *transforms* or merely *returns*. That decides how it behaves between Blanche and the Review Board.

```
Before anything else: if you have not been given an audio file that you can
actually listen to, reply with exactly NO AUDIO and stop. Do not describe,
infer, or reconstruct this song from a title, a description, lyrics, an artist
page, or anything you may have read. Only transcribe what you can hear.

You are transcribing a song so it can be rearranged for the Game Boy sound
chip: two square-wave voices, one bass voice, and no chords within a voice.

I need ONLY the single most recognisable hook -- the four to eight notes a
listener would hum back afterwards. Not the whole song, not the complete vocal
line, and not a section-by-section breakdown.

Reply in exactly this format and nothing else:

    KEY:    (e.g. D minor)
    TEMPO:  (BPM, a number)
    METER:  (e.g. 4/4)
    HOOK:   note+octave/beats, space separated, 4 to 8 notes
            for example:  D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
    BASS:   same format, one note per chord change underneath that hook
    CHORDS: e.g.  Dm | Dm | Bb | A
    FEEL:   one line -- sparse or dense, driving or still, major or minor
    DOUBT:  what you are least sure of. Say plainly if the key or the hook
            is a guess.

If you cannot hear something clearly, write "unsure" in that field. Do not
fill a field by inference. A wrong key is worse than a blank one, because it
will be checked against a colour-to-pitch mapping and would quietly corrupt
it.

One extra question for this track only: if this hook is a variation of another
song's hook, say so, and describe how it differs -- transposed, slower, mode
changed, inverted, or re-harmonised.
```

---

## 8 — Echoes of the Algorithm

`https://soundcloud.com/codemusai/05-echoes-of-the-algorithm`

**The one that may show the decay predates the machine.** If this starts
mechanical and turns natural, it is the *same* progression as the Quicksilver
log — which would mean the pattern is Crystal's first and S.T.A.R.R. only
inherits it. Worth transcribing for that alone.

```
Before anything else: if you have not been given an audio file that you can
actually listen to, reply with exactly NO AUDIO and stop. Do not describe,
infer, or reconstruct this song from a title, a description, lyrics, an artist
page, or anything you may have read. Only transcribe what you can hear.

You are transcribing a song so it can be rearranged for the Game Boy sound
chip: two square-wave voices, one bass voice, and no chords within a voice.

I need ONLY the single most recognisable hook -- the four to eight notes a
listener would hum back afterwards. Not the whole song, not the complete vocal
line, and not a section-by-section breakdown.

Reply in exactly this format and nothing else:

    KEY:    (e.g. D minor)
    TEMPO:  (BPM, a number)
    METER:  (e.g. 4/4)
    HOOK:   note+octave/beats, space separated, 4 to 8 notes
            for example:  D4/1 F4/1 A4/2 G4/1 F4/1 D4/2
    BASS:   same format, one note per chord change underneath that hook
    CHORDS: e.g.  Dm | Dm | Bb | A
    FEEL:   one line -- sparse or dense, driving or still, major or minor
    DOUBT:  what you are least sure of. Say plainly if the key or the hook
            is a guess.

If you cannot hear something clearly, write "unsure" in that field. Do not
fill a field by inference. A wrong key is worse than a blank one, because it
will be checked against a colour-to-pitch mapping and would quietly corrupt
it.
```

---

## The remaining four

Not needed yet, listed so the set is complete: `04-lines-in-the-sand`,
`06-crystal-clear-or-crystal`, `09-nine-scars-nine-breaches`,
`10-1001-fatal-error`.

`05. Echoes of the Algorithm` may belong to the Index rather than to a person,
and `10. 1001 - Fatal Error` shares its number with *A Painted Christmas* —
both worth a look once the six above are in.

---

## Bringing the answers back

Paste them raw. [`tools/hook2asm.py`](../tools/hook2asm.py) turns each one into
music asm and checks it rather than trusting it — it refuses on an unparseable
hook, stops on `NO AUDIO`, flags an `unsure` key or tempo, prints what 7.2's
spectrum mapping reads the key as, and compares total channel lengths.

    python3 tools/hook2asm.py answer.txt --label Music_CrystalMotif

**If an answer comes back `NO AUDIO`, that is the system working.** It means
the file did not reach Gemini — not that the track is untranscribable.
