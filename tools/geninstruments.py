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
decay_ms, sustain (0..1), release_ms, edition. The companion's screens resample it per note.

THE GAME (T-425's game half, 2026-10-18) takes the same two sounds, and this tool writes that too:

  engineGba/sound/direct_sound_samples/daemons_{harp,flute}.wav   the WAVs above resampled to 13379 Hz (the m4a mixer's
      own rate, src/m4a.c), 16-bit, with a `smpl` chunk (unity note 60; the FLUTE's loop) -- the build's wav2agb turns
      each into the .bin the ROM includes (8-bit signed PCM after a 16-byte header: flags, rate*1024 at C4, loop
      start, size), so no .bin is ever made by hand. As retail's samples do, one extra sample follows the end (the
      loop start's, for the FLUTE; silence for the HARP) because the mixer interpolates toward the next sample, and
      the FLUTE's size is pinned by an `agbl` chunk to the loop end. The HARP's last 30 ms fade to nothing so the
      sample's end cannot click when a high note runs it out.
  sound/direct_sound_data.inc   DirectSoundWaveData_daemons_harp / _flute
  sound/voice_groups.inc        voicegroup193: voice 0 the HARP, voice 1 the FLUTE (tools/genplaysounds.py plays them)

  The json's envelope in m4a's terms (it steps once a frame, 60 a second): attack = 255 / frames of attack_ms (255 is
  instant); sustain = 255 * sustain, decay only matters below 255; release = the per-frame factor (x/256) that falls
  to 1/256 (-48 dB) in release_ms.
"""
import io, json, math, os, re, struct, sys, wave
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


GBA = os.path.join(ROOT, "engineGba")
GBA_RATE = 13379
SAMPLES = os.path.join(GBA, "sound", "direct_sound_samples")
DSD = os.path.join(GBA, "sound", "direct_sound_data.inc")
VG = os.path.join(GBA, "sound", "voice_groups.inc")
VOICEGROUP = 193
FRAMES_PER_S = 60


def adsr(m):
    """The json's envelope in m4a's bytes (see the docstring)."""
    att = 255 if m["attack_ms"] <= 0 else min(255, math.ceil(255 / (m["attack_ms"] * FRAMES_PER_S / 1000)))
    sus = max(0, min(255, round(255 * m["sustain"])))
    if sus >= 255:
        dec = 0
    else:
        fr = max(1.0, m["decay_ms"] * FRAMES_PER_S / 1000)
        dec = max(0, min(255, round(256 * (max(sus, 1) / 255) ** (1 / fr))))
    fr = m["release_ms"] * FRAMES_PER_S / 1000
    rel = 0 if fr <= 0 else max(0, min(255, round(256 * (1 / 256) ** (1 / fr))))
    return att, dec, sus, rel


def resample(x):
    from scipy.signal import resample_poly
    return resample_poly(x, GBA_RATE, SR)


def gba_wav(x, m):
    """One engine WAV: 13379 Hz 16-bit, smpl (unity 60, the loop), agbl for a loop's size, one sample past the end."""
    y = resample(x)
    loop = None
    if m["loop_start"] is not None:
        def zc(i):
            while i < len(y) - 1 and not (y[i] <= 0 < y[i + 1]):
                i += 1
            return i
        a = zc(int(round(m["loop_start"] * GBA_RATE / SR)))
        e = zc(int(round(m["loop_end"] * GBA_RATE / SR)))
        y = np.concatenate([y[:e], y[a:a + 1]])          # the extra sample: where the loop goes back to
        loop = (a, e)
    else:
        n = int(GBA_RATE * 0.03)
        y = y * np.concatenate([np.ones(len(y) - n), np.linspace(1, 0, n)])
        y = np.concatenate([y, [0.0]])
    pcm = np.int16(np.clip(y, -1, 1) * 30000).tobytes()
    smpl = struct.pack("<9I", 0, 0, round(1e9 / GBA_RATE), 60, 0, 0, 0, 1 if loop else 0, 0)
    if loop:
        smpl += struct.pack("<6I", 0, 0, loop[0], loop[1], 0, 0)   # end inclusive: wav2agb writes e+1 samples
    chunks = [(b"fmt ", struct.pack("<HHIIHH", 1, 1, GBA_RATE, GBA_RATE * 2, 2, 16)), (b"smpl", smpl)]
    if loop:
        chunks.append((b"agbl", struct.pack("<I", loop[1])))
    chunks.append((b"data", pcm))
    body = b"WAVE" + b"".join(c + struct.pack("<I", len(d)) + d + (b"\0" if len(d) & 1 else b"") for c, d in chunks)
    return b"RIFF" + struct.pack("<I", len(body)) + body, loop, len(y)


def gba():
    """{path: (old text or bytes, new)} for the engine, and a line per sample for the report."""
    out, notes, voices = {}, [], []
    for name, fn in (("harp", harp), ("flute", flute)):
        x, m = fn()
        data, loop, n = gba_wav(x, m)
        p = os.path.join(SAMPLES, "daemons_%s.wav" % name)
        out[p] = data
        a, d, s, r = adsr(m)
        voices.append("\tvoice_directsound 60, 0, DirectSoundWaveData_daemons_%s, %d, %d, %d, %d" % (name, a, d, s, r))
        notes.append("%s: %d samples at %d Hz (%d bytes in ROM), %s, ADSR %d/%d/%d/%d" % (
            name.upper(), n, GBA_RATE, 16 + ((n + 3) // 4) * 4,
            "loop %d..%d" % loop if loop else "no loop", a, d, s, r))

    t = open(DSD, encoding="utf-8").read()
    k = t.find("@ T-425")                                 # ours always sit last: cut them and write them again
    if k >= 0:
        t = t[:t.rfind("\t.align 2", 0, k)]
    t2 = t.rstrip("\n") + "\n\n\t.align 2\n@ T-425: our own HARP and FLUTE (DAEMONS tools/geninstruments.py)\n"
    t2 += "\n\t.align 2\n".join("DirectSoundWaveData_daemons_%s::\n\t.incbin \"sound/direct_sound_samples/daemons_%s.bin\""
                                % (n, n) for n in ("harp", "flute")) + "\n"
    out[DSD] = t2

    t = open(VG, encoding="utf-8").read()
    head = "\t.align 2\nvoicegroup%03d::  @ T-425: PLAY's HARP (0) and FLUTE (1), our own (DAEMONS tools/geninstruments.py)\n" % VOICEGROUP
    k = t.find("voicegroup%03d::" % VOICEGROUP)
    if k >= 0:
        t = t[:t.rfind("\t.align 2", 0, k)].rstrip("\n") + "\n"
    out[VG] = t.rstrip("\n") + "\n\n" + head + "\n".join(voices) + "\n"
    return out, notes


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

    if not os.path.isdir(SAMPLES):
        print("  the game: no engineGba/ here, skipped")
        return
    eng, notes = gba()
    changed = []
    for p, d in eng.items():
        mode = "b" if isinstance(d, bytes) else ""
        old = open(p, "r" + mode, **({} if mode else {"encoding": "utf-8"})).read() if os.path.exists(p) else None
        if old != d:
            changed.append(os.path.relpath(p, GBA))
            if "--write" in sys.argv:
                open(p, "w" + mode, **({} if mode else {"encoding": "utf-8"})).write(d)
    print("  the game (voicegroup%03d): %s" % (VOICEGROUP, "unchanged" if not changed else
          ("written " if "--write" in sys.argv else "would write ") + ", ".join(changed)))
    for n in notes:
        print("    " + n)


if __name__ == "__main__":
    main()
