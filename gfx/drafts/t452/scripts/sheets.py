import json, os, sys
from PIL import Image, ImageDraw, ImageFont
R="/Users/christopherhicks/Projects/DAEMONS"; D=R+"/gfx/drafts/t452"
SP="/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/"
PICK=json.load(open(D+"/picks.json"))
try: F=ImageFont.truetype("/System/Library/Fonts/Menlo.ttc",16); FS=ImageFont.truetype("/System/Library/Fonts/Menlo.ttc",12)
except Exception: F=FS=ImageFont.load_default()
PAPER=(236,234,226); INKC=(30,30,34); GAMEBG=(205,205,172)
def sprite(path):  # indexed 4bpp: index 0 transparent
    im=Image.open(path)
    if im.mode=="P":
        a=im.convert("RGBA"); px=im.load(); al=a.load()
        for y in range(im.height):
            for x in range(im.width):
                if px[x,y]==0: al[x,y]=(0,0,0,0)
        return a
    return im.convert("RGBA")
def today(n,k="front"):
    im=Image.open(f"{R}/gfx/daemons/{n}_{k}.png").convert("RGBA")
    return im if im.width==64 else im.resize((64,64),Image.LANCZOS)
def on(im,bg,scale=1):
    b=Image.new("RGBA",im.size,bg+(255,)); b.alpha_composite(im)
    return b.convert("RGB").resize((im.width*scale,im.height*scale),Image.NEAREST)
def daemon_sheet(n,p):
    cols=[]
    cols.append(("today's front (3x)",on(today(n),GAMEBG,3)))
    cols.append(("512 concept (shown 384)",Image.open(f"{D}/{p['front']}").convert("RGB").resize((384,384),Image.NEAREST)))
    red=sprite(f"{D}/reduced/{n}_front.png")
    cols.append(("64x64 1x",on(red,GAMEBG,1)))
    cols.append(("64x64 3x, %s"%p["type"],on(red,GAMEBG,3)))
    if p.get("back"):
        cols.append(("back 512",Image.open(f"{D}/{p['back']}").convert("RGB").resize((192,192),Image.NEAREST)))
        rb=sprite(f"{D}/reduced/{n}_back.png")
        cols.append(("back 1x",on(rb,GAMEBG,1)))
        cols.append(("back 3x",on(rb,GAMEBG,3)))
    if os.path.exists(f"{D}/reduced/{n}_icon.png"):
        ic=sprite(f"{D}/reduced/{n}_icon.png").crop((0,0,32,32))
        cols.append(("icon 1x",on(ic,GAMEBG,1))); cols.append(("icon 3x",on(ic,GAMEBG,3)))
    W=sum(c[1].width for c in cols)+24*(len(cols)+1); H=max(c[1].height for c in cols)+110
    s=Image.new("RGB",(W,H),PAPER); d=ImageDraw.Draw(s)
    d.text((24,12),"%s  (%s, %s)  -- T-452 DRAFT  -- %s"%(p["name"],p["gametype"],p["type"],p["why"]),fill=INKC,font=F)
    x=24
    for lab,im in cols:
        s.paste(im,(x,50)); d.text((x,56+im.height),lab,fill=INKC,font=FS); x+=im.width+24
    s.save(SP+"t452_%s.png"%n)
def battle(foe,plr,out):
    bg=Image.open(SP+"battle_bg_clean.png").convert("RGBA")
    f=sprite(f"{D}/reduced/{foe}_front.png"); b=sprite(f"{D}/reduced/{plr}_back.png")
    bg.alpha_composite(f,(144,8)); bg.alpha_composite(b,(40,48))
    one=bg.convert("RGB")
    s=Image.new("RGB",(240+720+72,520),PAPER); d=ImageDraw.Draw(s)
    s.paste(one,(24,60)); s.paste(one.resize((720,480),Image.NEAREST),(288,30))
    d.text((24,8),"MOCK, T-452 DRAFT: %s front vs %s back, 1x (left) and 3x"%(foe.upper(),plr.upper()),fill=INKC,font=FS)
    d.text((24,236),"boxes and names from\n.theatre/t392f_rel_battle.png\n(POLL vs CODEMUSAI);\nonly the two sprites\nare new",fill=INKC,font=FS)
    s.save(SP+out)
def overview():
    rows=[]
    for n,p in PICK.items():
        rows.append((p["name"],p["type"],today(n),sprite(f"{D}/reduced/{n}_front.png")))
    W=24+6*(128*2+48); H=420
    s=Image.new("RGB",(W,H),PAPER); d=ImageDraw.Draw(s)
    d.text((24,10),"T-452 pilot, DRAFT: today (top) and the new style (bottom), each at 1x and 2x, coloured by type",fill=INKC,font=F)
    x=24
    for name,t,a,b in rows:
        d.text((x,44),"%s  %s"%(name,t),fill=INKC,font=FS)
        s.paste(on(a,GAMEBG,1),(x,70)); s.paste(on(a,GAMEBG,2),(x+80,70))
        s.paste(on(b,GAMEBG,1),(x,230)); s.paste(on(b,GAMEBG,2),(x+80,230))
        x+=128*2+48-56
    s.save(SP+"t452_overview.png")
for n,p in PICK.items(): daemon_sheet(n,p)
overview()
for foe,plr in PICK.get("_battles",[]) if False else []: pass
