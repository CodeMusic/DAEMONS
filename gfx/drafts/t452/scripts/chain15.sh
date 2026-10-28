#!/bin/bash
# batch 15 drafts (PARTICLE to UNDERTOW 311-331 with PENGUIN 341), one job at a time; batch.py's run() waits for an idle queue before each job and retries a dropped network
W=/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b15_work
PY=~/.pyenv/versions/3.12.2/bin/python3
export T452_ROOT=$W
st=$1; shift
for n in "$@"; do echo "== $st $n"; $PY $W/scripts/batch.py $st --dir=t --seed=6300 --prefix=t452b15 $n; done
echo ALL-DONE
