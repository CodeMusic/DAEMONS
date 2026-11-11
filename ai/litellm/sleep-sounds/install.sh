#!/usr/bin/env bash
# companion C-334: sleep sounds made by ACE-Step on roverbyteseer, keyed, beside LiteLLM (sleep_sounds.py says why).
#
#   scp -r ai/litellm/sleep-sounds/. roverbyte@roverbyteseer:~/daemons-sleep-sounds/
#   ssh roverbyte@roverbyteseer 'bash ~/daemons-sleep-sounds/install.sh'
#
# Idempotent: re-running restarts it on the copied code.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST="$HOME/Library/LaunchAgents/ca.codemusic.daemons.sleepsounds.plist"
sed "s#__HOME__#$HOME#g" "$HERE/ca.codemusic.daemons.sleepsounds.plist" > "$PLIST"
launchctl bootout "gui/$(id -u)/ca.codemusic.daemons.sleepsounds" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart "gui/$(id -u)/ca.codemusic.daemons.sleepsounds"
for _ in $(seq 1 20); do curl -fsS --max-time 2 http://127.0.0.1:4002/health >/dev/null 2>&1 && break; sleep 0.5; done
curl -fsS --max-time 2 http://127.0.0.1:4002/health >/dev/null && echo "sleep sounds: up on :4002" || { echo "sleep sounds: not answering"; tail -5 "$HOME/Library/Logs/daemons-sleep-sounds.log"; exit 1; }
code=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://127.0.0.1:4002/v1/sleep/make -d '{}')
[ "$code" = 401 ] && echo "sleep sounds: refuses a request with no key" || { echo "sleep sounds: answered $code with no key"; exit 1; }
