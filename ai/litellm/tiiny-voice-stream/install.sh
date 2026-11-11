#!/usr/bin/env bash
# C-317: the Tiiny's voice, streamed and keyed, beside LiteLLM on roverbyteseer (tiiny_voice_stream.py says why).
#
#   scp -r ai/litellm/tiiny-voice-stream roverbyte@roverbyteseer:~/daemons-tiiny-voice
#   ssh roverbyte@roverbyteseer 'bash ~/daemons-tiiny-voice/install.sh'
#
# Idempotent: re-running restarts it on the copied code.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST="$HOME/Library/LaunchAgents/ca.codemusic.daemons.tiinyvoice.plist"
sed "s#__HOME__#$HOME#g" "$HERE/ca.codemusic.daemons.tiinyvoice.plist" > "$PLIST"
launchctl bootout "gui/$(id -u)/ca.codemusic.daemons.tiinyvoice" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart "gui/$(id -u)/ca.codemusic.daemons.tiinyvoice"   # a fresh bootstrap over ssh may wait to run
for _ in $(seq 1 20); do curl -fsS --max-time 2 http://127.0.0.1:4001/health >/dev/null 2>&1 && break; sleep 0.5; done
curl -fsS --max-time 2 http://127.0.0.1:4001/health >/dev/null && echo "tiiny voice stream: up on :4001" || { echo "tiiny voice stream: not answering"; tail -5 "$HOME/Library/Logs/daemons-tiiny-voice.log"; exit 1; }
code=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://127.0.0.1:4001/v1/audio/speech -d '{}')
[ "$code" = 401 ] && echo "tiiny voice stream: refuses a request with no key" || { echo "tiiny voice stream: answered $code with no key"; exit 1; }
