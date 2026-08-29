"""Shared helpers: read any PNG, area-resample, quantise to Game Boy values."""
import zlib, struct

def read_png(path):
    d = open(path,'rb').read(); pos=8; idat=b''; plte=None
    while pos < len(d):
        ln = struct.unpack('>I', d[pos:pos+4])[0]
        typ, data = d[pos+4:pos+8], d[pos+8:pos+8+ln]
        if typ==b'IHDR': w,h,bd,ct = struct.unpack('>IIBB', data[:10])
        elif typ==b'IDAT': idat += data
        elif typ==b'PLTE': plte = data
        pos += 12+ln
    nch = {0:1,2:3,3:1,4:2,6:4}[ct]
    bpp = max(1, nch*bd//8)
    stride = (w*nch*bd+7)//8
    raw = zlib.decompress(idat); rows=[]; prev=bytearray(stride); i=0
    for _ in range(h):
        f = raw[i]; i+=1; line = bytearray(raw[i:i+stride]); i+=stride
        for x in range(stride):
            a = line[x-bpp] if x>=bpp else 0
            b = prev[x]; c = prev[x-bpp] if x>=bpp else 0
            if f==1: line[x] = (line[x]+a)&255
            elif f==2: line[x] = (line[x]+b)&255
            elif f==3: line[x] = (line[x]+((a+b)>>1))&255
            elif f==4:
                p=a+b-c; pa,pb,pc = abs(p-a),abs(p-b),abs(p-c)
                line[x] = (line[x]+(a if pa<=pb and pa<=pc else b if pb<=pc else c))&255
        rows.append(bytes(line)); prev=line
    def lum(x,y):
        if ct in (2,6):
            o = x*nch; r,g,b = rows[y][o],rows[y][o+1],rows[y][o+2]
            return (r*299+g*587+b*114)//1000
        if ct==3:
            r,g,b = plte[rows[y][x]*3:rows[y][x]*3+3]
            return (r*299+g*587+b*114)//1000
        if bd==8: return rows[y][x]
        v = (rows[y][x*bd//8] >> (8-bd-(x*bd)%8)) & ((1<<bd)-1)
        return v*255//((1<<bd)-1)
    return w, h, lum

def resample(src_w, src_h, lum, dst_w, dst_h):
    """Box-average down to the target size."""
    out = [[0]*dst_w for _ in range(dst_h)]
    for dy in range(dst_h):
        y0, y1 = dy*src_h//dst_h, max(dy*src_h//dst_h+1, (dy+1)*src_h//dst_h)
        for dx in range(dst_w):
            x0, x1 = dx*src_w//dst_w, max(dx*src_w//dst_w+1, (dx+1)*src_w//dst_w)
            tot = n = 0
            for y in range(y0,y1):
                for x in range(x0,x1): tot += lum(x,y); n += 1
            out[dy][dx] = tot//n
    return out

def quantise(grid, levels=4):
    """0 = darkest ink, levels-1 = lightest. Even thresholds."""
    return [[ min(levels-1, v*levels//256) for v in row ] for row in grid]

def write_png(path, grid, bitdepth):
    H=len(grid); W=len(grid[0]); ppb = 8//bitdepth
    stride = (W*bitdepth+7)//8; raw=b''
    for row in grid:
        line = bytearray(stride)
        for x,v in enumerate(row):
            line[x//ppb] |= (v << (8-bitdepth-(x%ppb)*bitdepth))
        raw += b'\x00'+bytes(line)
    def chunk(t,d):
        c=t+d; return struct.pack('>I',len(d))+c+struct.pack('>I',zlib.crc32(c)&0xffffffff)
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', W,H,bitdepth,0,0,0,0))
           + chunk(b'IDAT', zlib.compress(raw,9)) + chunk(b'IEND', b''))
    open(path,'wb').write(png)
