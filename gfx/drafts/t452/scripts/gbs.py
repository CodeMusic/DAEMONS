# gbasprite.py's functions without its whole-tree loop: exec the file up to the loop.
import sys, os
#  T-532: the tools beside THIS checkout, not the main one -- a sandbox or worktree read the main tree's drawings here.
T=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))),"tools")
sys.path.insert(0,T)
src=open(os.path.join(T,"gbasprite.py")).read()
src=src[:src.index("pairs = renamed()")]
G={"__file__":os.path.join(T,"gbasprite.py"),"__name__":"gbs"}
sys_argv=sys.argv; sys.argv=[sys.argv[0]]
exec(compile(src,"gbasprite.py","exec"),G)
sys.argv=sys_argv
globals().update({k:v for k,v in G.items() if not k.startswith("__")})
