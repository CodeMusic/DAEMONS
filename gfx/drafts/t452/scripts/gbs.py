# gbasprite.py's functions without its whole-tree loop: exec the file up to the loop.
import sys, os
T="/Users/christopherhicks/Projects/DAEMONS/tools"
sys.path.insert(0,T)
src=open(os.path.join(T,"gbasprite.py")).read()
src=src[:src.index("pairs = renamed()")]
G={"__file__":os.path.join(T,"gbasprite.py"),"__name__":"gbs"}
sys_argv=sys.argv; sys.argv=[sys.argv[0]]
exec(compile(src,"gbasprite.py","exec"),G)
sys.argv=sys_argv
globals().update({k:v for k,v in G.items() if not k.startswith("__")})
