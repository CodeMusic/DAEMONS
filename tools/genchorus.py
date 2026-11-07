#!/usr/bin/env python3
"""THE DAWN CHORUS (T-528 (d), vision.md 4.40): rising whistles under THE CREATOR'S HOUR's choir, in a grove, on the
morning after a night of light.

    python3 tools/genchorus.py                       # report: is the engine's chorus current
    python3 tools/genchorus.py --write               # write it into engineGba
    python3 tools/genchorus.py --preview OUT.wav     # what the game plays, mixed at 13379 Hz: the pad and the chirps
                                                     #   (--chirps-only: the chirps alone), two loops

THE SOUND. Radio listeners named it: a VLF "chorus" of rising tones, each a few hundred milliseconds, in bursts,
strongest on the dawn side of the Earth, that sounds like birdsong. So ONE CHIRP, synthesized and never recorded: a
sine that rises about an octave and a fifth in a quarter of a second, a little faster as it goes (the elements bend
upward), with a faint second partial and a breath of filtered noise at its onset, swelling in and fading out. It is
pitched per note, so one 0.26-second sample (3.5 KB of ROM) makes every chirp.

THE PATTERN. A track of bursts on a fixed seed: three to five chirps a burst, each starting a little higher than the
one before (bursts step up, as the real ones do), never two at once -- so the chorus takes at most ONE of the mixer's
five DirectSound channels (gengrovemusic.py: the hardware's limit is five) -- and one to two and a half seconds of quiet
between bursts. Its loop is the pad's: four bars at 120 BPM, eight seconds.

THE LOUDNESS (the user has not yet heard the choir's): the chirp's sample is scaled to the choir sample's own RMS
(classical_choir_voice_ahhs, 0.39), its track's volume is the pad's (48 of 127, under the song's 80) and its notes
are struck softer than the pad's (velocity 40-52 against 64). It never rises above the choir.

THE SONG. SE_DAWN_CHORUS is SE_AAH_PAD and the chirps in one song, on the same SE3 player, so daemons_hours.c's tone
fades it in and out exactly as it fades the pad, and the weather still takes the player first. Track 1 is the pad,
note for note (voicegroup191's choir, E3, held); track 2 the chirps. Both on its own voicegroup, VOICEGROUP below:
voice 0 the choir (voicegroup191's slot 52, the same sample and envelope), voice 1 the chirp.

WHAT IT WRITES (engineGba/)
    sound/direct_sound_samples/daemons_chorus.wav   the chirp, 13379 Hz 16-bit, smpl unity 60, one silent sample past
                                                    the end (the mixer interpolates toward it); wav2agb makes the .bin
    sound/direct_sound_data.inc    DirectSoundWaveData_daemons_chorus, just before geninstruments.py's block (which
                                   that tool cuts and rewrites from its own marker to the end of the file)
    sound/voice_groups.inc         voicegroup194, just before voicegroup193 (the same reason)
    sound/songs/midi/se_dawn_chorus.mid   the two tracks (format 0, 24 ticks a beat, the loop marked [ and ])
The song's entry (midi.cfg, song_table.inc, songs.h, ld_script.ld) is a line each, written by hand in T-528 part 2
and checked here.
"""
import io, math, os, struct, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
RATE = 13379
SAMPLES = os.path.join(GBA, "sound", "direct_sound_samples")
DSD = os.path.join(GBA, "sound", "direct_sound_data.inc")
VG = os.path.join(GBA, "sound", "voice_groups.inc")
MID = os.path.join(GBA, "sound", "songs", "midi", "se_dawn_chorus.mid")
VOICEGROUP = 194
CHOIR_RMS = 0.388               # classical_choir_voice_ahhs.wav, measured: the loudness the chirp is matched to
CHOIR = "\tvoice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 255, 0, 255, 0"
CHIRP = "\tvoice_directsound 60, 0, DirectSoundWaveData_daemons_chorus, 255, 0, 255, 0"
MARK_DSD = "@ T-528: the dawn chorus's chirp (DAEMONS tools/genchorus.py)"
MARK_VG = "voicegroup%03d::  @ T-528: the dawn chorus -- the choir (0, voicegroup191's 52) and the chirp (1) (DAEMONS tools/genchorus.py)" % VOICEGROUP

F0 = 880.0                      # where the chirp starts at MIDI note 60 (the sample's unity): A5
RISE = 1.6                      # octaves it climbs
DUR = 0.26                      # seconds

TPB = 24                        # ticks a beat; 120 BPM, so 48 ticks a second
LOOP = 4 * 4 * TPB              # the pad's loop: four bars
LEAD = TPB                      # the pad's first beat, before the loop point


def chirp():
    n = int(RATE * DUR)
    t = np.arange(n) / RATE
    u = t / DUR
    f = F0 * 2 ** (RISE * u ** 1.35)                           # rising, a little faster as it goes
    ph = 2 * np.pi * np.cumsum(f) / RATE
    tone = np.sin(ph) + 0.12 * np.sin(2 * ph)
    rng = np.random.default_rng(528)
    breath = np.convolve(rng.normal(0, 1, n), np.ones(6) / 6, "same") * 0.05 * np.exp(-t / 0.03)
    env = np.minimum(1.0, t / 0.025) * np.clip((DUR - t) / 0.09, 0, 1) ** 1.5 * (0.75 + 0.25 * np.sin(np.pi * u))
    x = (tone + breath) * env
    body = x[int(0.03 * RATE):int(0.17 * RATE)]
    x *= CHOIR_RMS / np.sqrt((body ** 2).mean())                # the held part as loud as the choir's held part
    peak = np.abs(x).max()
    if peak > 0.97:
        x *= 0.97 / peak
    return np.concatenate([x, [0.0]])                           # one silent sample past the end


def wav(x):
    pcm = np.int16(np.clip(x, -1, 1) * 32000).tobytes()
    smpl = struct.pack("<9I", 0, 0, round(1e9 / RATE), 60, 0, 0, 0, 0, 0)
    chunks = [(b"fmt ", struct.pack("<HHIIHH", 1, 1, RATE, RATE * 2, 2, 16)), (b"smpl", smpl), (b"data", pcm)]
    body = b"WAVE" + b"".join(c + struct.pack("<I", len(d)) + d + (b"\0" if len(d) & 1 else b"") for c, d in chunks)
    return b"RIFF" + struct.pack("<I", len(body)) + body


def bursts():
    """[(tick in the loop, note, velocity, length in ticks)]: never two chirps at once."""
    rng = np.random.default_rng(4281)
    out, t = [], 12
    length = int(round(DUR * 48)) + 1                         # 13 ticks: the sample plays out
    while True:
        k = int(rng.integers(3, 6))
        base = int(rng.integers(55, 62))
        burst = []
        for i in range(k):
            burst.append((t, base + 2 * i + int(rng.integers(0, 2)), int(rng.integers(40, 53)), length))
            t += length + int(rng.integers(1, 9))
        if burst[-1][0] + length > LOOP - 4:
            break
        out += burst
        t += int(rng.integers(48, 120))                        # one to two and a half seconds of quiet
    return out


def vlq(n):
    b = [n & 0x7F]
    n >>= 7
    while n:
        b.insert(0, 0x80 | (n & 0x7F))
        n >>= 7
    return bytes(b)


def midi():
    """Format 0: channel 0 the pad as se_aah_pad.mid has it, channel 1 the chirps; the loop [ at LEAD, ] at the end."""
    ev = [(0, 0, b"\xff\x51\x03\x07\xa1\x20"),               # 120 BPM
          (0, 1, b"\xc0\x00"), (0, 2, b"\xb0\x07\x30"), (0, 3, b"\xb0\x0a\x40"), (0, 4, b"\x90\x40\x40"),
          (0, 5, b"\xc1\x01"), (0, 6, b"\xb1\x07\x30"), (0, 7, b"\xb1\x0a\x40"),
          (LEAD, 8, b"\xff\x06\x01["), (LEAD + LOOP, 90, b"\xff\x06\x01]"),
          (LEAD + LOOP + TPB, 95, b"\x80\x40\x00")]
    for t, note, vel, ln in bursts():
        ev.append((LEAD + t, 20, bytes([0x91, note, vel])))
        ev.append((LEAD + t + ln, 10, bytes([0x81, note, 0])))
    ev.sort()
    body, now = b"", 0
    for t, _, e in ev:
        body += vlq(t - now) + e
        now = t
    body += b"\x00\xff\x2f\x00"
    return b"MThd" + struct.pack(">IHHH", 6, 0, 1, TPB) + b"MTrk" + struct.pack(">I", len(body)) + body


def engine():
    out = {os.path.join(SAMPLES, "daemons_chorus.wav"): wav(chirp()), MID: midi()}
    t = open(DSD, encoding="utf-8").read()
    if MARK_DSD not in t:
        k = t.find("\t.align 2\n@ T-425")
        k = len(t.rstrip("\n")) + 1 if k < 0 else k
        t = t[:k] + ("\t.align 2\n%s\nDirectSoundWaveData_daemons_chorus::\n"
                     "\t.incbin \"sound/direct_sound_samples/daemons_chorus.bin\"\n\n" % MARK_DSD) + t[k:]
    out[DSD] = t
    t = open(VG, encoding="utf-8").read()
    if MARK_VG not in t:
        k = t.find("\t.align 2\nvoicegroup193::")
        assert k >= 0, "voice_groups.inc has no voicegroup193 to sit before"
        t = t[:k] + "\t.align 2\n%s\n%s\n%s\n\n" % (MARK_VG, CHOIR, CHIRP) + t[k:]
    out[VG] = t
    return out


def preview(path, chirps_only):
    """Two loops as the m4a mixer would play them: notes resampled linearly, velocity and the track volume applied."""
    x = chirp()
    sec = LOOP / 48
    n = int(RATE * (sec * 2 + 1))
    mix = np.zeros(n)
    vol = 48 * 80 / 127 / 127                                  # the track's VOL under the song's master volume
    for loop in range(2):
        for t, note, vel, _ in bursts():
            step = 2 ** ((note - 60) / 12)
            idx = np.arange(0, len(x) - 1, step)
            y = np.interp(idx, np.arange(len(x)), x) * vel / 127 * vol
            at = int(RATE * (loop * sec + t / 48))
            mix[at:at + len(y)] += y[:n - at]
    if not chirps_only:
        w = wave.open(os.path.join(SAMPLES, "classical_choir_voice_ahhs.wav"))
        c = (np.frombuffer(w.readframes(w.getnframes()), dtype=np.uint8).astype(float) - 128) / 128
        step = 2 ** ((64 - 60) / 12)                           # E4, as voicegroup191's choir sounds the pad's note
        idx = np.arange(0, n * step) % (len(c) - 1)            # held: the sample's own loop is near enough for a preview
        pad = np.interp(idx[:n], np.arange(len(c)), c) * 64 / 127 * vol
        mix += pad
    mix = mix / max(1.0, np.abs(mix).max()) * 0.9
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(np.int16(mix * 32000).tobytes())
    print("  preview: %s (%.1f s)" % (path, n / RATE))


def main():
    if "--preview" in sys.argv:
        preview(sys.argv[sys.argv.index("--preview") + 1], "--chirps-only" in sys.argv)
        return
    if not os.path.isdir(SAMPLES):
        print("  the game: no engineGba/ here, skipped")
        return
    b = bursts()
    print("  the chirp: %.2f s at %d Hz, %.0f-%.0f Hz at note 60; %d chirps in the 8-second loop, velocity %d-%d" % (
        DUR, RATE, F0, F0 * 2 ** RISE, len(b), min(v for _, _, v, _ in b), max(v for _, _, v, _ in b)))
    changed = []
    for p, d in engine().items():
        mode = "b" if isinstance(d, bytes) else ""
        old = open(p, "r" + mode, **({} if mode else {"encoding": "utf-8"})).read() if os.path.exists(p) else None
        if old != d:
            changed.append(os.path.relpath(p, GBA))
            if "--write" in sys.argv:
                tmp = p + ".tmp"
                open(tmp, "w" + mode, **({} if mode else {"encoding": "utf-8"})).write(d)
                if os.path.exists(p):
                    os.chmod(tmp, os.stat(p).st_mode)
                os.replace(tmp, p)
    entries = {"sound/songs/midi/midi.cfg": "se_dawn_chorus.mid:", "sound/song_table.inc": "song se_dawn_chorus, 3, 3",
               "include/constants/songs.h": "#define SE_DAWN_CHORUS", "ld_script.ld": "se_dawn_chorus.o(.rodata)"}
    missing = [f for f, s in entries.items() if s not in open(os.path.join(GBA, f), encoding="utf-8").read()]
    print("  the game (voicegroup%03d, SE_DAWN_CHORUS): %s%s" % (VOICEGROUP, "unchanged" if not changed else
          ("written " if "--write" in sys.argv else "would write ") + ", ".join(changed),
          "" if not missing else "; the song's entry MISSING in " + ", ".join(missing)))


if __name__ == "__main__":
    main()
