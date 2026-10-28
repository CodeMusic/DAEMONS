#!/bin/bash
# batch 8 drafts, one stage at a time; waits for an idle server before each (chain6's rule: the server is shared)
W=/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/t452b8_work
PY=~/.pyenv/versions/3.12.2/bin/python3
export T452_ROOT=$W
idle() { while true; do local q; q=$(curl -s -m 10 http://roverbyteseer:8008/queue | $PY -c "import json,sys;q=json.load(sys.stdin);print(len(q['queue_running'])+len(q['queue_pending']))" 2>/dev/null); [ "$q" = "0" ] && return; echo "busy ($q), waiting"; sleep 20; done; }
for job in "$@"; do st=${job%%:*}; n=${job#*:}; idle; echo "== $st $n"; if [ "$st" = extra ]; then $PY $W/scripts/extra8.py $n; else $PY $W/scripts/batch.py $st --dir=k --seed=5600 --prefix=t452b8 $n; fi; done
echo ALL-DONE
