"""T-452 SYMBOL: the 28 forms (A-Z, ! and ?) -- shared names and paths."""
import os
R = "/Users/christopherhicks/Projects/DAEMONS"; G = R + "/engineGba/graphics/pokemon/unown"
W = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452sym_work"
D = W + "/y"
FORMS = [chr(c) for c in range(ord("a"), ord("z") + 1)] + ["exclamation_mark", "question_mark"]
GLYPH = {f: f.upper() for f in FORMS}; GLYPH["exclamation_mark"] = "!"; GLYPH["question_mark"] = "?"
CONST = {f: "UNOWN_" + f.upper() for f in FORMS}; CONST["a"] = "UNOWN"; CONST["exclamation_mark"] = "UNOWN_EMARK"; CONST["question_mark"] = "UNOWN_QMARK"
def key(f): return "sym_" + {"exclamation_mark": "emark", "question_mark": "qmark"}.get(f, f)
