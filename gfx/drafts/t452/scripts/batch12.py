"""T-452 batch 12 (2026-10-28): REPAY to KAIROS (seed 6000, dir p) -- was DUPLEX to CLINGING (203-224, SIGKILL drawn before), every line whole, the charm recipe (charm8: two t2i fronts 5701/5702, i2i 0.8 = 5721, 0.85 = 5722, one back from today's 0.66 = 5731, one icon 5741; backs turned from the chosen front 5751/5752), drafted into dir l.

    batch9.py icons | sheets   as batch8.py"""
import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
R = "/Users/christopherhicks/Projects/DAEMONS"; T = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452"); D = T + "/p"
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
SP = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/"
NAMES = ['repay', 'buoyancy', 'armouring', 'fixation', 'obsession', 'recall', 'engram', 'illusion', 'imitation', 'cache', 'brontes', 'typhon', 'boreas', 'ruminate', 'brooding', 'grievance', 'triton', 'phoenix', 'kairos']

def icons():
    os.chdir(R); sys.argv = [sys.argv[0], "gen"]
    import round2
    ch = json.load(open(D + "/choose.json")); P = json.load(open(D + "/picks.json"))
    for n in NAMES:
        if n not in P: continue
        if ch[n]["icon"] == "derived":   # icon3 from the clean new front (round two's rule for a lost bust)
            import icon3
            hf = f"{D}/hand/{n}_front.png"   # batch 9: from the hand front where there is one (grounds off)
            P[n]["measured"]["icon3"] = icon3.make(n, P[n]["type"], hf if os.path.exists(hf) else f"{D}/clean/{n}_front.png", f"{D}/reduced/{n}_icon.png")
        else:
            P[n]["measured"]["icon3"] = round2.icon_from_draft("p", n, ch[n]["icon"], P[n]["type"])
        print(n, P[n]["measured"]["icon3"]["icon_palette"], P[n]["measured"]["icon3"]["size"], flush=True)
    json.dump(P, open(D + "/picks.json", "w"), indent=1)

def sheets():
    ch = json.load(open(D + "/choose.json"))
    done = [n for n in NAMES if os.path.exists(f"{D}/reduced/{n}_front.png")]
    for k in range(0, len(done), 5):
        grp = done[k:k + 5]
        args = [f"{n}:p:" + ("LOST KEY: " + ch[n]["failed"] + " -- " if ch[n].get("failed") else "") + ch[n].get("note", "")
                for n in grp]
        subprocess.run([PY, HERE + "/sheet_r2.py", SP + "t452b12_work/sheets/t452b12_sheet%d.png" % (k // 5 + 1),
                        "T-452 batch 12 -- DRAFT, not in the ROM (phase 1, the recommended fixes applied): in ROM | draft, front / back / icon, 1x and 3x, and the draft's shiny"]
                       + args, check=True)
    combined(done, ch)

def combined(done, ch):
    from sheet_r2 import show, on, readpal, BY, G, F, FS, PAPER, INK, GROUND, PARTY
    from PIL import Image, ImageDraw
    CW, RH, per = 3 * (64 * 2 + 70) + 32 * 2 + 40 + 40, 232, 3
    rows = (len(done) + per - 1) // per
    s = Image.new("RGB", (20 + per * (CW + 20), 50 + rows * RH), PAPER); d = ImageDraw.Draw(s)
    d.text((20, 14), "T-452 batch 12 (REPAY to KAIROS, 225-251 less those drawn before) -- DRAFT, not in the ROM, recommended fixes applied: in ROM front | draft front, back, icon (1x and 2x)",
           fill=INK, font=F)
    for i, n in enumerate(done):
        v = BY[n]; rom = G + v["constant"].lower(); npal = readpal(rom + "/normal.pal")
        x = 20 + (i % per) * (CW + 20); y = 46 + (i // per) * RH
        f = ch[n].get("failed", ""); lab = ("LOST KEY" if f.startswith("front") else "FLAGGED") if f else "batch 12"
        d.text((x, y), "%d %s  (%s)" % (v["national"], v["name"], lab), fill=(170, 40, 40) if f else INK, font=FS)
        nd = f"{D}/reduced/{n}_"
        from PIL import Image as I
        p = I.open(nd + "front.png").getpalette()[:48]; fpal = [tuple(p[j:j + 3]) for j in range(0, 48, 3)]
        ims = [(show(rom + "/front.png", npal), GROUND), (show(nd + "front.png"), GROUND),
               (show(nd + "back.png", fpal), GROUND), (show(nd + "icon.png", None, 32), PARTY)]
        xx = x
        for j, (im, bg) in enumerate(ims):
            s.paste(on(im, bg, 1), (xx, y + 20)); s.paste(on(im, bg, 2), (xx, y + 20 + im.height + 4))
            xx += im.width * 2 + (30 if j == 0 else 8)
            if j == 0: d.line((xx - 16, y + 20, xx - 16, y + RH - 10), fill=INK, width=2)
    s.save(SP + "t452b12_work/sheets/t452b12_combined.png"); print(SP + "t452b12_work/sheets/t452b12_combined.png", s.size)

if __name__ == "__main__":
    {"icons": icons, "sheets": sheets}[sys.argv[1]]()
