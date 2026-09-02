#!/usr/bin/env python3
"""Prove the built ROMs actually contain the sprites in gfx/.

    make verify-sprites

A .pic is an *intermediate*: make builds it from the .png, links it, and then
deletes it. So a .pic that is somehow newer than its .png is invisible -- make
calls it up to date, every ROM built afterwards embeds it, and the file is gone
before anyone could look at it. That happened: rattata.pic carried a timestamp
newer than our NIBBLE art, so four ROMs shipped vanilla Rattata and nothing in
the build said a word.

Compiling is not evidence here. The only check that sees what shipped is to
rebuild each pic from the art on disk and search the ROM for its exact bytes --
the same reasoning as decoding the ROM with the charmap to check strings.

Every .pic this touches is deleted afterwards, on purpose: a stale one is the
bug, and the safe state is none at all.
"""
import os, subprocess, sys, glob

ENG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine")
os.chdir(ENG)

def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True).stdout.split()

pngs = git("diff", "--name-only", "upstream/master", "--", "gfx/pokemon/")
if not pngs:
    sys.exit("no daemon sprites differ from upstream -- is `upstream` fetched?")
pics = [p[:-4] + ".pic" for p in pngs]

for p in pics:                       # a stale one is exactly what we are hunting
    if os.path.exists(p): os.remove(p)
if subprocess.run(["make", *pics], stdout=subprocess.DEVNULL).returncode:
    sys.exit("could not build the pics")

roms = sorted(r for r in glob.glob("daemons*.gbc"))
data = {r: open(r, "rb").read() for r in roms}
bad = {r: [] for r in roms}
for p in pics:
    b = open(p, "rb").read()
    for r in roms:
        if b not in data[r]: bad[r].append(os.path.basename(p)[:-4])
for p in pics:
    os.remove(p)

print("%d daemon sprites, %d ROMs" % (len(pics), len(roms)))
for r in roms:
    print("  %-28s %s" % (r, "all present" if not bad[r]
                          else "MISSING %d: %s" % (len(bad[r]), " ".join(bad[r]))))
sys.exit(1 if any(bad.values()) else 0)
