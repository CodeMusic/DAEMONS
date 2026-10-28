#!/bin/bash
# batch 9 drafts (ALARM to RELEASE, 161-181), one job at a time; batch.py's run() waits for an idle server queue before each job
W=/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b9_work
PY=~/.pyenv/versions/3.12.2/bin/python3
export T452_ROOT=$W
st=$1; shift
for n in "$@"; do echo "== $st $n"; $PY $W/scripts/batch.py $st --dir=l --seed=5700 --prefix=t452b9 $n; done
echo ALL-DONE
