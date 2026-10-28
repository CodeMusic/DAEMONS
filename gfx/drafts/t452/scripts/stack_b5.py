import sys
from PIL import Image
ns=sys.argv[2:]; ims=[Image.open(f't452b5_cand_{n}.png') for n in ns]
w=max(i.width for i in ims); s=Image.new('RGB',(w,sum(i.height for i in ims)),(236,234,226)); y=0
for i in ims: s.paste(i,(0,y)); y+=i.height
s.save(sys.argv[1])
