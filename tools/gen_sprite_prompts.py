#!/usr/bin/env python3
"""Emit the per-daemon Gemini prompts for full-colour GBA sprites.

    python3 tools/gen_sprite_prompts.py > docs/gemini-prompts-gba-sprites.txt

Generated rather than written by hand so the type and its hue are always the
ones tools/gbasprite.py actually assigned. A prompt that names the wrong colour
is worse than no prompt.
"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location(
    "gs", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gbasprite.py"))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB = os.path.join(ROOT, "engine")

TYPE_NAME = {"NORMAL":"CONTENT","FIGHTING":"LOGIC","FLYING":"VECTOR","POISON":"CORRUPT",
             "GROUND":"STRATUM","ROCK":"LEGACY","BUG":"SWARM","GHOST":"LATENT",
             "FIRE":"ENTROPY","WATER":"FLOW","GRASS":"GROWTH","ELECTRIC":"SIGNAL",
             "PSYCHIC":"CONTEXT","ICE":"FROZEN","DRAGON":"EMERGENT"}
HUE = {"FLYING":"red","FIRE":"amber","GHOST":"dark violet","ICE":"pale blue",
       "NORMAL":"bone / warm off-white","FIGHTING":"cold steel blue",
       "POISON":"sickly olive","GROUND":"earth brown","ROCK":"slate grey",
       "BUG":"olive green","WATER":"deep blue","GRASS":"green",
       "ELECTRIC":"cyan","PSYCHIC":"magenta","DRAGON":"iridescent teal"}

def upstream(p):
    return subprocess.run(["git","-C",GB,"show","upstream/master:"+p],
                          capture_output=True,text=True).stdout
pat = r'dname\s+"([^"]*)"'
pairs = {v: o for v, o in zip(re.findall(pat, upstream("data/pokemon/names.asm")),
                              re.findall(pat, open(os.path.join(GB,"data/pokemon/names.asm")).read()))
         if v != o}
FIX = {"NIDORAN♀":"nidoran_f","NIDORAN♂":"nidoran_m","FARFETCH'D":"farfetchd","MR.MIME":"mr_mime"}
def slot(v): return FIX.get(v, v.lower().replace(" ","_").replace(".",""))
def ptype(d):
    p = os.path.join(GB,"data/pokemon/base_stats", d.replace("_","")+".asm")
    m = re.search(r'db\s+([A-Z_]+)\s*,\s*[A-Z_]+\s*;\s*type', open(p).read())
    t = m.group(1)
    return t[:-5] if t.endswith("_TYPE") else t

STYLE = ("Draw it as a flat illustration with a hard pure black (#000000) outline around the whole "
         "creature. Use AT MOST 15 flat colours plus a pure white background, with hard edges "
         "between them and no gradients, no anti-aliasing, no glow, no texture and no shading "
         "ramps longer than three steps. The outline must stay pure black - it must not take the "
         "body colour. Plain pure-white background, nothing behind the creature, no ground shadow. "
         "Whole creature visible with a small even margin, filling the frame.")

print("""GEMINI PROMPTS - full-colour GBA sprites
======================================================================

The GBA gives each creature SIXTEEN colours. What is in the ROM now is the
Game Boy art with a palette laid over it: three shades of one hue plus an
outline, four colours of the sixteen. This is how to spend the rest.

ONE RULE SURVIVES THE UPGRADE. Colour is by TYPE (vision.md 9.4), so it
carries the argument rather than decorating it. Each prompt below names the
hue that daemon's type was assigned, and the art must be built around it -
accents and secondary colours are welcome, a different dominant hue is not.

HOW TO USE THIS FILE

  1. Attach the CURRENT sprite named in the block. It is the silhouette we
     already tuned; the new art should be recognisably the same creature.
  2. Paste the prompt.
  3. Save what comes back anywhere, then convert:

         python3 tools/gbacolour.py <saved>.png <daemon> front
         python3 tools/gbacolour.py <saved>.png <daemon> back

  4. When a few are in: make -C engineGba firered

DO THE FRONT FIRST. Twice over.

In the conversation, because a fresh one invents a different creature and a
back sprite that does not match its front is worse than none -- so attach the
finished front to the back prompt.

And in the conversion, because Gen 3 gives a species ONE palette shared by both
sprites. gbacolour.py builds it from the front and maps the back into it. Run
them the other way round and the back would recolour the front.
""")

for vanilla, ours in sorted(pairs.items(), key=lambda kv: kv[1]):
    d = slot(vanilla)
    t = ptype(d)
    if t not in TYPE_NAME: continue
    for kind, view in (("front", "facing the viewer"), ("back", "seen from directly behind")):
        src = "engine/gfx/pokemon/%s/%s%s.png" % (kind, d.replace("_",""), "" if kind=="front" else "b")
        print("-" * 70)
        print("%s - %s sprite" % (ours, kind))
        print("  type    %s (%s)" % (TYPE_NAME[t], HUE[t]))
        print("  attach  %s" % src)
        print("  convert python3 tools/gbacolour.py <saved>.png %s %s" % (ours, kind))
        print("-" * 70)
        extra = ("" if kind == "front" else
                 " This is the same creature as the attached front sprite, from behind: same "
                 "proportions, same colours, same markings. No face is visible.")
        print("The attached image is a small monochrome sprite of a creature called %s. Redraw it "
              "at higher fidelity in full colour, %s, keeping the same pose, the same silhouette "
              "and the same readable features so it is unmistakably the same creature.%s Build the "
              "colour scheme around %s as the dominant colour. %s"
              % (ours, view, extra, HUE[t], STYLE))
        print()
