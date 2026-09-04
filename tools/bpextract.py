#!/usr/bin/env python3
"""Run Basic Pitch on one stem and dump its notes as JSON.

    python3.11 -m venv bpvenv
    ./bpvenv/bin/pip install basic-pitch "setuptools<81"
    ./bpvenv/bin/python tools/bpextract.py <stem.mp3> <out.json> [fmin fmax]

Two installation notes, both of which cost an hour:
  * PYTHON 3.11, not 3.12 -- a dependency still imports `imp`, gone in 3.12.
  * SETUPTOOLS < 81 -- another still imports `pkg_resources`, gone in 81.
On macOS basic-pitch 0.4 runs on CoreML and pulls no TensorFlow at all.

Runs inside an isolated Python 3.11 venv, because basic-pitch pulls TensorFlow
and pins numpy < 2 -- the machine's own Python is on numpy 2.2.6 and the rest
of tools/ depends on that. Nothing here does musical work; it only converts
audio into (start, end, pitch, amplitude) so the real tool can read it.
"""
import json, sys, warnings
warnings.filterwarnings("ignore")
from basic_pitch.inference import predict

src, dst = sys.argv[1], sys.argv[2]
kw = {}
if len(sys.argv) > 4:
    kw["minimum_frequency"], kw["maximum_frequency"] = float(sys.argv[3]), float(sys.argv[4])
_, _, notes = predict(src, **kw)
out = [[round(float(s), 4), round(float(e), 4), int(p), round(float(a), 4)]
       for s, e, p, a, *_ in notes]
out.sort()
json.dump(out, open(dst, "w"))
print("  %-14s %5d notes" % (src.split("/")[-1][:-4], len(out)))
