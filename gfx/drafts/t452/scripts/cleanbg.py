from PIL import Image
import numpy as np
SP="/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/"
a=np.asarray(Image.open("/Users/christopherhicks/Projects/DAEMONS/.theatre/t392f_rel_battle.png").convert("RGB")).copy()
FOE=(144,8,208,78); PLR=(40,48,104,112)   # GBA battle sprite boxes, 64x64
def inbox(b,x,y): return b[0]<=x<b2(b) and b[1]<=y<b[3]
b2=lambda b:b[2]
H,W,_=a.shape
mask=np.zeros((H,W),bool)
for b in (FOE,PLR): mask[b[1]:b[3],b[0]:b[2]]=True
# background colours per row band: colours seen in the same rows outside the boxes
out=a.copy()
for b in (FOE,PLR):
    for y in range(b[1],min(b[3],112)):
        cols=list(range(0,40))+list(range(104,136)) if b==PLR else list(range(208,240))+list(range(100,144))
        row=[tuple(a[y,x]) for x in cols if not mask[y,x]]
        ok=set(row)
        # sprite pixels: colour not in this row's background set
        bad=[x for x in range(b[0],b[2]) if tuple(a[y,x]) not in ok]
        for x in bad:
            # nearest good pixel in this row, alternating left/right, mirror about the box centre first
            for d in range(1,W):
                for xx in (x-d,x+d):
                    if 0<=xx<W and tuple(a[y,xx]) in ok and not (b[0]<=xx<b[2] and xx in bad):
                        out[y,x]=a[y,xx]; break
                else: continue
                break
Image.fromarray(out).save(SP+"battle_bg_clean.png")
Image.fromarray(out).resize((720,480),Image.NEAREST).save(SP+"battle_bg_clean3.png")
