#!/usr/bin/env python3
"""T-415: how often the sky is not clear. Replays src/daemons_weather.c's generator (its tables read from the C, its
hash and draws copied) over 400 days at every third ordinary outdoor section, every half hour, and prints the share of
the time each season has weather somewhere a player stands. Report only: the numbers live in the C.

    python3 tools/skyodds.py
"""
import re,random
import os
E=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'engineGba')+'/'
t=open(E+'src/data/region_map/region_map_entries.h').read()
corn=t.split('sMapSectionTopLeftCorners')[1].split('sMapSectionDimensions')[0]
dims=t.split('sMapSectionDimensions')[1]
C=dict((m,tuple(map(int,v.split(',')))) for m,v in re.findall(r'\[(MAPSEC_\w+) - KANTO_MAPSEC_START\] = \{ (\d+, \d+) \}',corn))
D=dict((m,tuple(map(int,v.split(',')))) for m,v in re.findall(r'\[(MAPSEC_\w+) - KANTO_MAPSEC_START\] = \{ (\d+, \d+) \}',dims))
order=list(C.keys())  # in enum order from Pallet
rm=open(E+'src/region_map.c').read()
sev=re.findall(r'\[REGIONMAP_(SEVII\d+) - 1\] =\s*\{(.*?)\}',rm,re.S)
sheetof={}
for i,(n,body) in enumerate(sev):
    for m in re.findall(r'MAPSEC_\w+',body):
        if m!='MAPSEC_NONE': sheetof.setdefault(m,i+1)
iO=order.index('MAPSEC_ONE_ISLAND')
def place(m):
    if m=='MAPSEC_SPECIAL_AREA': return None
    x,y=C[m]
    if (x,y)==(0,0): return None
    i=order.index(m)
    sh=0 if i<iO else sheetof.get(m,0)
    return sh,x,y,*D[m]
M=0xFFFFFFFF
def H(x):
    x&=M; x^=x>>16; x=(x*0x7FEB352D)&M; x^=x>>15; x=(x*0x846CA68B)&M; x^=x>>16; return x
class R:
    def __init__(s,v): s.v=v
    def n(s): s.v=H(s.v+0x6D2B79F5); return s.v
def pick(w,roll):
    tot=sum(w); a=roll%tot
    for i,x in enumerate(w):
        if a<x: return i
        a-=x
W=open(E+'src/daemons_weather.c').read()
SEAS={'WINTER':0,'SPRING':1,'SUMMER':2,'AUTUMN':3}
def table(name):
    return re.search(name+r'\[.*?\] = \{(.*?)\n\};', W, re.S).group(1)
def nums(t): return [int(x) for x in re.findall(r'\b\d+\b', t.replace('SKY_SIZE_REGION','254').replace('SKY_SIZE_BOTH','255'))]
EPD={SEAS[k]:nums(v) for k,v in re.findall(r'\[SEASON_(\w+)\] = \{(.*?)\}', table('sSkyEventsPerDay'))}
KIND={SEAS[k]:nums(v) for k,v in re.findall(r'\[SEASON_(\w+)\] = \{(.*?)\}', table('sSkyKinds'))}
def rows(name): return [tuple(nums(r)) for r in re.findall(r'\{([^{}]*?)\}', table(name))]
LEN=rows('sSkyLengths'); SZ=rows('sSkySizes')
CR=nums(re.search(r'sSkyCentreRegion\[2\] = \{(.*?)\}', W).group(1))
def rp(rows,st):
    r=rows[pick([w for _,_,w in rows],st.n())]; return r[0]+st.n()%(r[1]-r[0]+1)
N=len(order)-1  # SPECIAL_AREA excluded
def events(day,season,salt=0x544E4F43):
    st=R(H((day*0x9E3779B9)^salt)); n=pick(EPD[season],st.n()); ev=[]
    for _ in range(n):
        s=st.n()%1440; L=rp(LEN,st); k=pick(KIND[season],st.n()); rad=rp(SZ,st)
        isl=pick(CR,st.n())
        for tr in range(48):
            m=order[st.n()%N]; p=place(m)
            if p and (p[0]!=0)==isl: break
        else: p=place('MAPSEC_ONE_ISLAND' if isl else 'MAPSEC_SAFFRON_CITY')
        ev.append((s,L,k,p[0],p[1]+p[3]//2,p[2]+p[4]//2,rad))
    return ev
def covers(e,p):
    sh,x,y,w,h=p; r=e[6]
    if r==255: return True
    if (sh!=0)!=(e[3]!=0): return False
    if r==254: return True
    if sh!=e[3]: return False
    cx,cy=e[4],e[5]
    dx= x-cx if cx<x else (cx-(x+w-1) if cx>=x+w else 0)
    dy= y-cy if cy<y else (cy-(y+h-1) if cy>=y+h else 0)
    return max(dx,dy)<=r
import glob,json
sunny=sorted({json.load(open(f))['region_map_section'] for f in glob.glob(E+'data/maps/*/map.json') if json.load(open(f))['weather']=='WEATHER_SUNNY'})
for season in range(4):
    hit=tot=0
    for day in range(1,400):
        evs=[(s+1440,L,*r) for (s,L,*r) in events(day,season)]+[(s,L,*r) for (s,L,*r) in events(day-1,season)]
        for minute in range(0,1440,30):
            now=minute+1440
            for m in sunny[::3]:
                p=place(m); tot+=1
                if any(now>=e[0] and now<e[0]+e[1] and covers(e,p) for e in evs): hit+=1
    print(['winter','spring','summer','autumn'][season], round(100*hit/tot,1),'% of the time somewhere outdoors has weather')
