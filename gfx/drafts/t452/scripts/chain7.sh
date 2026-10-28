#!/bin/bash
# batch 7 drafts, one stage at a time; waits for an idle server before each (chain6.sh's way)
W=/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b7_work
PY=~/.pyenv/versions/3.12.2/bin/python3
export T452_ROOT=$W
idle() { while true; do local q; q=$(curl -s -m 10 http://roverbyteseer:8008/queue | $PY -c "import json,sys;q=json.load(sys.stdin);print(len(q['queue_running'])+len(q['queue_pending']))" 2>/dev/null); [ "$q" = "0" ] && return; echo "busy ($q), waiting"; sleep 20; done; }
for job in "$@"; do st=${job%%:*}; n=${job#*:}; idle; echo "== $st $n"; $PY $W/scripts/batch.py $st --dir=j --seed=5500 --prefix=t452b7 $n; done
echo ALL-DONE
