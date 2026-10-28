#!/bin/bash
# batch 10 drafts (GOLDSET to RESENTMENT, 182-202 with VALENCE 350 and RANKLE 360), one job at a time; batch.py's run() waits for an idle queue before each job
W=/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b10_work
PY=~/.pyenv/versions/3.12.2/bin/python3
export T452_ROOT=$W
st=$1; shift
for n in "$@"; do echo "== $st $n"; $PY $W/scripts/batch.py $st --dir=n --seed=5800 --prefix=t452b10 $n; done
echo ALL-DONE
