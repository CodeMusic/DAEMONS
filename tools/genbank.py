#!/usr/bin/env python3
"""T-565 batch 12: our own instruments under our older songs -- in place of the retail samples voicegroup191 played.

    python3 tools/genbank.py            # report: is the engine current
    python3 tools/genbank.py --write    # write it into engineGba

THE USER, 2026-11-17, from two reels of the same songs (A today's retail samples, B these) and a parade of each
instrument: "Yes, use ours". voicegroup191 is the bank tools/gbavoices.py built for our own songs -- the title, the new
game's intro, CALLOW, THE NEXUS, the fourteen groves, the CREATOR'S HOUR pad -- and genchorus.py's dawn chorus borrows
its choir. Nineteen of its programs are played; two of them are PLAY's HARP and FLUTE already (geninstruments.py),
and this makes the other sixteen. gbavoices.py points the slots at them; genchorus.py's choir is ours too.

Each is synthesized (fixed seeds), one note at its root, mono, with a loop for a held sound: additive partials for the
piano, glockenspiel, xylophone, tubular bell and timpani; Karplus-Strong for the guitar, the fingered bass and the
pizzicato; detuned saws through low-pass filters for the strings and the brass; a filtered sawtooth for the synth bass;
three detuned voices through 'ah' formants for the choir; a narrow pulse through formants for the oboe; a sine with
breath for the whistle. Envelopes stay gbavoices.py's, lifted from vanilla's own use of each sample.

WHAT IT WRITES (engineGba/)
    sound/direct_sound_samples/daemons_<name>.wav   sixteen samples at the mixer's 13379 Hz, 16-bit, with a smpl chunk
                    (the root note; the loop) and agbl for a loop's size, as geninstruments.py writes the harp and flute;
                    the build's wav2agb makes each .bin
    sound/direct_sound_data.inc                     DirectSoundWaveData_daemons_<name>, just before geninstruments.py's
                    block (which cuts and rewrites from its own marker on, so it must stay last)
Every sound DRAFT.
"""
import os, re, struct, sys
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT_DIR, "engineGba")
SAMPLES = os.path.join(GBA, "sound", "direct_sound_samples")
DSD = os.path.join(GBA, "sound", "direct_sound_data.inc")
GBA_RATE = 13379
MARK = "@ T-565 batch 12: our own instruments under our older songs (DAEMONS tools/genbank.py)"


SR = 22050
rng = np.random.default_rng(1212)

def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)

def norm(y, peak=0.9):
    return y * (peak / (np.max(np.abs(y)) or 1))

def loop_xfade(y, a, e, L=400):
    """make [a, e) loop seamlessly: crossfade its last L samples into the L before a"""
    y = y.copy()
    w = np.linspace(0, 1, L)
    y[e - L:e] = y[e - L:e] * (1 - w) + y[a - L:a] * w
    return y

def onepole(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x); s = 0.0
    for i, v in enumerate(x):
        s = (1 - a) * v + a * s; y[i] = s
    return y

def bandpass(x, f, q):
    w0 = 2 * np.pi * f / SR; al = np.sin(w0) / (2 * q)
    b0, b2 = al, -al; a0, a1, a2 = 1 + al, -2 * np.cos(w0), 1 - al
    y = np.zeros_like(x); x1 = x2 = y1 = y2 = 0.0
    for i, v in enumerate(x):
        o = (b0 * v + b2 * x2 - a1 * y1 - a2 * y2) / a0
        x2, x1 = x1, v; y2, y1 = y1, o; y[i] = o
    return y

def saw(f, n, detune=0.0, phase=0.0):
    t = np.arange(n) / SR
    return 2 * np.mod(f * (1 + detune) * t + phase, 1) - 1

def additive(f, n, ratios, amps, decays):
    t = np.arange(n) / SR
    y = np.zeros(n)
    for r, a, d in zip(ratios, amps, decays):
        y += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / d)
    return y

def ks(f, n, damp=0.996, bright=0.5):
    """Karplus-Strong: a noise burst through a delay line that loses a little each pass"""
    p = int(round(SR / f))
    buf = rng.uniform(-1, 1, p)
    buf = onepole(buf, 1500 + 6000 * bright)
    y = np.zeros(n)
    for i in range(n):
        y[i] = buf[i % p]
        nxt = buf[(i + 1) % p]
        buf[i % p] = damp * (bright * buf[i % p] + (1 - bright) * 0.5 * (buf[i % p] + nxt))
    return y

def env(n, a=0.01, r=None):
    t = np.arange(n) / SR
    e = np.clip(t / max(a, 1e-4), 0, 1)
    if r:
        e *= np.clip((n / SR - t) / r, 0, 1)
    return e

# ---- the instruments: name -> (samples, root midi, loop or None) -------------------------------------------------------
def piano():
    f, n = hz(60), int(1.6 * SR)
    ks_ = [(k, 1.0 / k ** 1.8, 1.4 / (1 + 0.5 * k)) for k in range(1, 11)]
    t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * k * np.sqrt(1 + 0.0004 * k * k) * t) * np.exp(-t / d) for k, a, d in ks_)
    y += 0.25 * rng.uniform(-1, 1, n) * np.exp(-t / 0.004)
    return norm(y * env(n, 0.002, 0.05)), 60, None

def glockenspiel():
    f, n = hz(84), int(1.2 * SR)
    y = additive(f, n, [1, 2.76, 5.40, 8.93], [1, .4, .2, .1], [1.0, .45, .2, .12])
    return norm(y * env(n, 0.001, 0.05)), 84, None

def xylophone():
    f, n = hz(72), int(0.6 * SR)
    y = additive(f, n, [1, 3.93, 9.54], [1, .3, .12], [.3, .08, .03])
    return norm(y * env(n, 0.001, 0.03)), 72, None

def tubular_bell():
    f, n = hz(72), int(2.4 * SR)
    y = additive(f, n, [0.5, 1, 2.0, 2.76, 3.76, 5.4], [.3, 1, .5, .35, .2, .1], [2.0, 1.8, 1.0, .7, .45, .3])
    return norm(y * env(n, 0.002, 0.1)), 72, None

def nylon_guitar():
    n = int(1.5 * SR)
    y = ks(hz(48), n, damp=0.997, bright=0.3)
    return norm(onepole(y, 2200) * env(n, 0.003, 0.05)), 48, None

def fingered_bass():
    n = int(1.3 * SR)
    y = ks(hz(36), n, damp=0.998, bright=0.2)
    y = onepole(y, 900)
    return norm(y * env(n, 0.004, 0.05)), 36, None

def synth_bass():
    n = int(1.2 * SR); f = hz(36); t = np.arange(n) / SR
    x = saw(f, n) + 0.5 * saw(f, n, 0.004)
    cut = 300 + 2200 * np.exp(-t / 0.12)
    y = np.zeros(n); s = 0.0
    for i in range(n):
        a = np.exp(-2 * np.pi * cut[i] / SR); s = (1 - a) * x[i] + a * s; y[i] = s
    a, e = int(0.5 * SR), int(1.1 * SR)
    return norm(loop_xfade(y * env(n, 0.003), a, e)), 36, (a, e)

def pizzicato():
    n = int(0.5 * SR)
    y = ks(hz(60), n, damp=0.985, bright=0.4)
    return norm(onepole(y, 2500) * env(n, 0.002, 0.04)), 60, None

def timpani():
    n = int(1.6 * SR); t = np.arange(n) / SR; f = hz(48)
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.04 * np.exp(-t / 0.05))) / SR
    y = np.sin(ph) * np.exp(-t / 0.7) + 0.35 * np.sin(1.5 * ph) * np.exp(-t / 0.3)
    y += 0.5 * onepole(rng.uniform(-1, 1, n), 600) * np.exp(-t / 0.03)
    return norm(y * env(n, 0.002, 0.05)), 48, None

def strings():
    n = int(1.6 * SR); f = hz(60)
    x = sum(saw(f, n, d, rng.random()) for d in (-0.006, -0.003, 0, 0.003, 0.006, 0.009))
    t = np.arange(n) / SR
    x *= 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t)
    y = onepole(onepole(x, 1500), 2600)
    a, e = int(0.6 * SR), int(1.5 * SR)
    return norm(loop_xfade(y, a, e, 1200)), 60, (a, e)

def choir():
    n = int(1.6 * SR); f = hz(60); t = np.arange(n) / SR
    x = np.zeros(n)
    for d, vr in ((-0.005, 5.0), (0, 5.6), (0.006, 4.7)):
        fv = f * (1 + d) * (1 + 0.006 * np.sin(2 * np.pi * vr * t))
        x += 2 * np.mod(np.cumsum(fv) / SR, 1) - 1
    y = 1.0 * bandpass(x, 700, 6) + 0.6 * bandpass(x, 1220, 8) + 0.25 * bandpass(x, 2600, 10)
    y += 0.02 * bandpass(rng.uniform(-1, 1, n), 1500, 1)
    a, e = int(0.6 * SR), int(1.5 * SR)
    return norm(loop_xfade(y, a, e, 1500)), 60, (a, e)

def brass(root, cut0, cut1, bright_t):
    n = int(1.4 * SR); f = hz(root); t = np.arange(n) / SR
    fv = f * (1 + 0.003 * np.sin(2 * np.pi * 5.0 * t) * np.clip((t - 0.25) / 0.2, 0, 1))
    x = 2 * np.mod(np.cumsum(fv) / SR, 1) - 1
    cut = cut1 + (cut0 - cut1) * np.exp(-t / bright_t)
    y = np.zeros(n); s = s2 = 0.0
    for i in range(n):
        a = np.exp(-2 * np.pi * cut[i] / SR); s = (1 - a) * x[i] + a * s; s2 = (1 - a) * s + a * s2; y[i] = s2
    a, e = int(0.55 * SR), int(1.3 * SR)
    return norm(loop_xfade(y, a, e, 900)), root, (a, e)

def trumpet():
    return brass(60, 3200, 1800, 0.08)

def tuba():
    return brass(36, 900, 600, 0.1)

def french_horn():
    return brass(48, 1500, 1000, 0.1)

def oboe():
    n = int(1.4 * SR); f = hz(60); t = np.arange(n) / SR
    fv = f * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.2) / 0.2, 0, 1))
    ph = np.mod(np.cumsum(fv) / SR, 1)
    x = np.where(ph < 0.12, 1.0, -0.14)
    y = bandpass(x, 1100, 3) + 0.5 * bandpass(x, 2900, 5) + 0.3 * onepole(x, 700)
    a, e = int(0.5 * SR), int(1.3 * SR)
    return norm(loop_xfade(y, a, e, 900)), 60, (a, e)

def whistle():
    n = int(1.4 * SR); f = hz(84); t = np.arange(n) / SR
    fv = f * (1 + 0.006 * np.sin(2 * np.pi * 5.8 * t))
    y = np.sin(2 * np.pi * np.cumsum(fv) / SR) + 0.08 * bandpass(rng.uniform(-1, 1, n), f, 4)
    a, e = int(0.5 * SR), int(1.3 * SR)
    return norm(loop_xfade(y, a, e, 900)), 84, (a, e)

# program -> (name, maker); 46 and 73 are the harp and flute we already have (audio/instruments/)
OURS = {0: ("piano", piano), 1: ("piano", piano), 9: ("glockenspiel", glockenspiel), 13: ("xylophone", xylophone),
        14: ("tubular_bell", tubular_bell), 24: ("nylon_guitar", nylon_guitar), 33: ("fingered_bass", fingered_bass),
        38: ("synth_bass", synth_bass), 45: ("pizzicato", pizzicato), 47: ("timpani", timpani), 48: ("strings", strings),
        52: ("choir", choir), 56: ("trumpet", trumpet), 58: ("tuba", tuba), 60: ("french_horn", french_horn),
        68: ("oboe", oboe), 78: ("whistle", whistle)}


NAMES = sorted({nm for nm, _ in OURS.values()})


def gba_wav(x, root, loop):
    """13379 Hz 16-bit, smpl (unity = root, the loop), agbl for a loop's size, one sample past the end."""
    from scipy.signal import resample
    y = resample(x, int(round(len(x) * GBA_RATE / SR)))
    y = y / (np.max(np.abs(y)) or 1) * 0.95
    lp = None
    if loop:
        a = int(round(loop[0] * GBA_RATE / SR)); e = int(round(loop[1] * GBA_RATE / SR))
        y = np.concatenate([y[:e], y[a:a + 1]])
        lp = (a, e)
    else:
        f = min(len(y), int(0.03 * GBA_RATE))
        y[-f:] *= np.linspace(1, 0, f)
        y = np.concatenate([y, [0.0]])
    pcm = (np.clip(y, -1, 1) * 32767).astype("<i2").tobytes()
    smpl = struct.pack("<9I", 0, 0, round(1e9 / GBA_RATE), root, 0, 0, 0, 1 if lp else 0, 0)
    if lp:
        smpl += struct.pack("<6I", 0, 0, lp[0], lp[1], 0, 0)       # end inclusive: wav2agb writes e+1 samples
    chunks = [(b"fmt ", struct.pack("<HHIIHH", 1, 1, GBA_RATE, GBA_RATE * 2, 2, 16)), (b"smpl", smpl)]
    if lp:
        chunks.append((b"agbl", struct.pack("<I", lp[1])))
    chunks.append((b"data", pcm))
    body = b"WAVE" + b"".join(c + struct.pack("<I", len(d)) + d + (b"\0" if len(d) & 1 else b"") for c, d in chunks)
    return b"RIFF" + struct.pack("<I", len(body)) + body


def engine():
    out, makers = {}, {nm: fn for nm, fn in OURS.values()}
    for nm in NAMES:
        y, root, loop = makers[nm]()
        out[os.path.join(SAMPLES, "daemons_%s.wav" % nm)] = gba_wav(y, root, loop)
    t = open(DSD, encoding="utf-8").read()
    block = "\t.align 2\n%s\n" % MARK + "\n\t.align 2\n".join(
        "DirectSoundWaveData_daemons_%s::\n\t.incbin \"sound/direct_sound_samples/daemons_%s.bin\"" % (n, n)
        for n in NAMES) + "\n\n"
    k = t.find(MARK)
    if k >= 0:
        s = t.rfind("\t.align 2", 0, k)
        e = t.find("\t.align 2\n@ T-425", k)
        t = t[:s] + block + t[e:]
    else:
        e = t.find("\t.align 2\n@ T-425")
        assert e >= 0, "direct_sound_data.inc has no geninstruments.py block to sit before"
        t = t[:e] + block + t[e:]
    out[DSD] = t
    return out


def main():
    if not os.path.isdir(SAMPLES):
        print("  the game: no engineGba/ here, skipped")
        return
    changed = []
    for path, data in engine().items():
        mode = "b" if isinstance(data, bytes) else ""
        old = open(path, "r" + mode, **({} if mode else {"encoding": "utf-8"})).read() if os.path.exists(path) else None
        if old != data:
            changed.append(os.path.relpath(path, GBA))
            if "--write" in sys.argv:
                tmp = path + ".tmp"
                open(tmp, "w" + mode, **({} if mode else {"encoding": "utf-8"})).write(data)
                if os.path.exists(path):
                    os.chmod(tmp, os.stat(path).st_mode)
                os.replace(tmp, path)
    print("  %d instruments of ours: %s" % (len(NAMES), ", ".join(NAMES)))
    if not changed:
        print("  the game: unchanged")
    else:
        print("  the game: %s %d file(s): %s" % ("wrote" if "--write" in sys.argv else "would write", len(changed),
                                                 ", ".join(changed[:6]) + (" ..." if len(changed) > 6 else "")))


if __name__ == "__main__":
    main()
