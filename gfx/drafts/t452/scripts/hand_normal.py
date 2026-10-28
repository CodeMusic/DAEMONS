"""T-452 forms: OVERLOADED's NORMAL form re-cleaned (the user, 2026-10-28: "re-clean the normal form's open top on a
keyed ground"). Batch 18's chosen draft (w/overloaded_front_i2i_6622, copied as z/overloaded_normal_front_b18_6622) on
a keyed ground (prekey_hull.py: its white body met the white page through a broken line, and the clean took the top
of the cloud with the page), reduced by reduce2 as batch 18 did, then batch 18's hand edits again, unchanged:
    a pale sun (NORMAL's hue trap: yellow is 40), a blue-grey snowflake and a blue raindrop round it (hand_b18's stamps);
    the outline closed across the top (rows 8-24: an ink cell on every light cell at the silhouette's edge);
    the back the front mirrored with the face flattened, as the three weathers' backs (batch 18 blurred it; the four
    forms' backs now match); accents trimmed under 15% (the weathers kept), the hue trap, near-marker colours.
Writes z/hand/overloaded_normal_{front,back}.png."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ["T452_ROOT"] = os.path.dirname(HERE)
import hand4 as h4, hand_b5 as hb, hand_b10lib as hx
F = os.environ["T452_ROOT"] + "/z"; H = F + "/hand"
for m in (h4, hb, hx): m.F, m.H = F, H
from hand4 import load_any, save, sanitize, stamp, outline, INK
from hand_ov import flat_face
N = "overloaded_normal"; hx.P = {N: {"type": "NORMAL"}}
#  hand_b18.py's stamps, copied
SUN = [" #  #  # ", "  #####  ", " #WWWWW# ", "##WWYWW##", " #WWWWW# ", "  #####  ", " #  #  # "]
SUNK = {"#": INK, "W": (252, 250, 240, 255), "Y": (238, 230, 204, 255)}
SNOW = ["   S   ", " S S S ", "  SSS  ", "SSSSSSS", "  SSS  ", " S S S ", "   S   "]
SNOWK = {"S": (110, 130, 186, 255)}
DROP = ["  #  ", " #W# ", " #W# ", "#WCC#", "#CCC#", "#CCC#", " ### "]
BLUEK = {"#": INK, "W": (236, 246, 255, 255), "C": (90, 150, 230, 255)}
KEEP = (0, 0, 64, 30)
FACE = (14, 24, 54, 42)
if __name__ == "__main__":
    os.makedirs(H, exist_ok=True)
    for k in ("front", "back"):
        p = f"{H}/{N}_{k}.png"
        if os.path.exists(p): os.remove(p)
    a = load_any(N, "front"); outline(a, rows=(8, 24)); save(a, N, "front")
    g = hx.specks(N, "front"); print("stray cells off", g)
    a = load_any(N, "front")
    stamp(a, 1, 4, SUN, SUNK, behind=True); stamp(a, 52, 3, SNOW, SNOWK, behind=True); stamp(a, 56, 20, DROP, BLUEK, behind=True)
    save(a, N, "front")
    a = load_any(N, "front"); print("back, face cells", flat_face(a, FACE)); save(a[:, ::-1].copy(), N, "back")
    for k in ("front", "back"):
        kp = KEEP if k == "front" else (64 - KEEP[2], KEEP[1], 64 - KEEP[0], KEEP[3])
        g = hx.trim(N, k, keep=kp)
        if g: print(k, "accent cells greyed for the cap", g)
        left = hx.trap(N, k, "grey", s_min=0.25, acc_only=True)
        if left: print(k, "in NORMAL's hue reach, greyed:", left)
        a = load_any(N, k); s = sanitize(a)
        if s: save(a, N, k); print(k, "near-marker cells fixed:", s)
