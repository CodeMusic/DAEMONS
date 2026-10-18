#!/usr/bin/env python3
"""Our own HARP and FLUTE -- one voice for the game and the companion (T-425, the user 2026-10-18).

    python3 tools/geninstruments.py            # report
    python3 tools/geninstruments.py --write    # audio/instruments/{harp,flute}.wav + instruments.json

The game's PLAY voices were pokefirered's retail samples (sc88pro_harp, sc88pro_flute), which can never go into the
public companion. The user chose to make our own, used by BOTH, so every screen truly shares one voice and nothing is
Nintendo's; approved by ear 2026-10-18. A CONTENT save plays the HARP, a CONTEXT save the FLUTE.

  HARP   a plucked string: Karplus-Strong with a softened noise burst and a short sine body, one long decay.
  FLUTE  a breathy tone: sine with two soft partials, vibrato that grows in, filtered breath noise at the start,
         a held body that loops.

Each is one note at C4 (MIDI 60), mono 16-bit at 22050 Hz, deterministic (fixed seeds), with the loop and the
envelope a player needs in instruments.json: sample_rate, root_midi, loop_start/loop_end (samples), attack_ms,
decay_ms, sustain (0..1), release_ms, edition. The companion's screens resample it per note; the game takes the same
WAVs into a voicegroup (a later step).
"""
import io, json, os, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "audio", "instruments")
SR, ROOT_MIDI = 22050, 60
F0 = 440 * 2 ** ((ROOT_MIDI - 69) / 12)


def harp():
    rng = np.random.default_rng(1)
    N, n = int(SR / F0), int(SR * 2.0)
    b = np.convolve(rng.uniform(-1, 1, N), np.ones(4) / 4, "same")
    out, idx = np.zeros(n), 0
    for i in range(n):
        out[i] = b[idx]
        nxt = (idx + 1) % N
        b[idx] = 0.996 * 0.5 * (b[idx] + b[nxt])
        idx = nxt
    t = np.arange(n) / SR
    out += 0.25 * np.sin(2 * np.pi * F0 * t) * np.exp(-t / 0.6)
    out /= np.max(np.abs(out))
    #  a pluck rings out: no loop (the whole sample plays), the envelope only shapes the release
    return out, {"loop_start": None, "loop_end": None, "attack_ms": 0, "decay_ms": 0, "sustain": 1.0,
                 "release_ms": 250, "edition": "CONTENT"}


def flute():
    dur = 1.6
    t = np.arange(int(SR * dur)) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t) * np.clip(t / 0.4, 0, 1)
    ph = 2 * np.pi * F0 * np.cumsum(vib) / SR
    tone = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    rng = np.random.default_rng(2)
    breath = np.convolve(rng.normal(0, 1, len(t)), np.ones(8) / 8, "same") * 0.06
    out = tone + breath * (0.5 + 0.5 * np.exp(-t * 6))
    out /= np.max(np.abs(out))
    #  the held body loops: from 0.6 s to the last whole vibrato cycle before 1.4 s, at a zero crossing
    a, e = int(SR * 0.6), int(SR * 0.6 + round(0.8 * 5.2) / 5.2 * SR)
    def zc(i):
        while i < len(out) - 1 and not (out[i] <= 0 < out[i + 1]):
            i += 1
        return i
    a, e = zc(a), zc(e)
    return out, {"loop_start": a, "loop_end": e, "attack_ms": 80, "decay_ms": 0, "sustain": 1.0,
                 "release_ms": 150, "edition": "CONTEXT"}


def wav_bytes(x):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.int16(np.clip(x, -1, 1) * 30000).tobytes())
    return buf.getvalue()


def build():
    files, meta = {}, {"_about": "T-425 (the user, 2026-10-18): our own HARP and FLUTE, one voice for the game and the "
                       "companion; a CONTENT save plays the harp, CONTEXT the flute. Written by DAEMONS "
                       "tools/geninstruments.py. Each WAV is one note at root_midi; pitch a note by resampling at "
                       "2^((note - root_midi)/12). loop_start/loop_end in samples (null: no loop, play it out); "
                       "the envelope in ms, sustain 0..1."}
    for name, fn in (("harp", harp), ("flute", flute)):
        x, m = fn()
        files[name + ".wav"] = wav_bytes(x)
        meta[name] = {"file": name + ".wav", "sample_rate": SR, "root_midi": ROOT_MIDI, **m}
    files["instruments.json"] = (json.dumps(meta, indent=1) + "\n").encode()
    return files


def main():
    files = build()
    changed = [n for n, d in files.items()
               if not os.path.exists(os.path.join(OUT, n)) or open(os.path.join(OUT, n), "rb").read() != d]
    print("  %d files (harp.wav, flute.wav, instruments.json): %s" % (len(files),
          "unchanged" if not changed else ("written" if "--write" in sys.argv else "would write " + ", ".join(changed))))
    if "--write" in sys.argv and changed:
        os.makedirs(OUT, exist_ok=True)
        for n in changed:
            open(os.path.join(OUT, n), "wb").write(files[n])


if __name__ == "__main__":
    main()
