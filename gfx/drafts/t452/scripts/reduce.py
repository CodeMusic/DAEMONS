"""reduce.py NAME TYPE FRONT_DRAFT [BACK_DRAFT] [--icon]
cleandraft.py --streaks -> gbasprite.place_rich in the type's ramp -> 4bpp 64x64 PNG (+ normal.pal), icon optional.
Writes only under gfx/drafts/t452/."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gbs
R="/Users/christopherhicks/Projects/DAEMONS"; PY=os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
D=os.path.join(R,"gfx/drafts/t452")
args=[a for a in sys.argv[1:] if not a.startswith("--")]
name,typ,front=args[:3]; back=args[3] if len(args)>3 else None
os.makedirs(D+"/clean",exist_ok=True); os.makedirs(D+"/reduced",exist_ok=True)
pal=None; grid_f=None
for kind,src in (("front",front),("back",back)):
    if not src: continue
    clean=f"{D}/clean/{name}_{kind}.png"
    r=subprocess.run([PY,os.path.join(R,"tools/cleandraft.py"),os.path.join(D,src),clean,"--streaks"]+[a.replace("--box-%s="%kind,"--streak-box=") for a in sys.argv if a.startswith("--box-%s="%kind)],capture_output=True,text=True)
    print(r.stdout.strip(), r.stderr.strip()[-300:])
    if r.returncode:   # streak placement failed; clean without streaks
        r=subprocess.run([PY,os.path.join(R,"tools/cleandraft.py"),os.path.join(D,src),clean],capture_output=True,text=True)
        print("  (no streaks)", r.stdout.strip()[-200:])
    grid,p=gbs.place_rich(clean,gbs.TYPE_COLOR[typ],shared=pal if kind=="back" else None)
    if kind=="front": pal=p; grid_f=grid
    gbs.write_png4(f"{D}/reduced/{name}_{kind}.png",grid,p)
    print(f"  {name} {kind}: {len(p)} colours")
with open(f"{D}/reduced/{name}_normal.pal","w") as f:
    f.write("JASC-PAL\r\n0100\r\n16\r\n"+"".join("%d %d %d\r\n"%tuple(c) for c in (pal+[(0,0,0)]*16)[:16]))
if "--icon" in sys.argv:
    ic,info=gbs.derive_icon(grid_f,pal)
    gbs.write_png4(f"{D}/reduced/{name}_icon.png",ic,gbs.icon_palettes()[info[0]],32,64)
    print("  icon pal %d err %.0f"%info)
