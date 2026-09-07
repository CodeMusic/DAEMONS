#!/usr/bin/env bash
# Install and verify LiteLLM on roverbyteseer, beside the model servers.
#
#   scp -r ai/litellm roverbyte@10.0.0.136:~/daemons-litellm
#   ssh roverbyte@10.0.0.136 'bash ~/daemons-litellm/install.sh'
#
# Idempotent: re-running upgrades in place and re-runs the checks.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$HOME/.litellm-venv"
PORT="${LITELLM_PORT:-4000}"

say() { printf '\n== %s\n' "$1"; }

say "python"
PY=""
for c in python3.12 python3.11 python3; do
  command -v "$c" >/dev/null || continue
  v="$($c -c 'import sys;print("%d.%d"%sys.version_info[:2])')"
  # LiteLLM wants 3.8+; 3.11 is what the rest of this project settled on after
  # basic-pitch. Take the newest that is at least 3.9.
  case "$v" in 3.9|3.1[0-9]) PY="$c"; break ;; esac
done
[ -n "$PY" ] || { echo "no python >= 3.9 found" >&2; exit 1; }
echo "   $PY $($PY -c 'import sys;print(sys.version.split()[0])')"

say "venv"
[ -d "$VENV" ] || "$PY" -m venv "$VENV"
"$VENV/bin/pip" install --quiet --upgrade pip
echo "   $VENV"

say "litellm"
# The proxy extra is the one that provides the server; plain `litellm` is the
# SDK only and gives you no /v1/responses at all.
"$VENV/bin/pip" install --quiet --upgrade 'litellm[proxy]'
echo "   $("$VENV/bin/litellm" --version 2>&1 | head -1)"

say "backends this config points at"
# Checked BEFORE starting the proxy, because a proxy in front of nothing starts
# perfectly happily and only fails on the first real call.
for probe in "text:http://127.0.0.1:1234/v1/models" \
             "vision:http://127.0.0.1:8890/v1/models"; do
  name="${probe%%:*}"; url="${probe#*:}"
  if curl -fsS --max-time 4 "$url" >/dev/null 2>&1; then echo "   $name  up"
  else echo "   $name  DOWN — $url"; fi
done

say "model ids"
# The config names `openai/local-model`, but LM Studio and llama.cpp each have
# their own id and a mismatch is a 404 that reads like a bridge failure.
curl -fsS --max-time 4 http://127.0.0.1:1234/v1/models 2>/dev/null \
  | "$VENV/bin/python" -c 'import json,sys
try:
    d=json.load(sys.stdin)
    for m in d.get("data",[]): print("   ", m.get("id"))
except Exception: print("   (could not read model list)")' || echo "   (text backend down)"

cat <<NOTE

== next
   1. Put the real model id into config.yaml if it is not "local-model".
   2. export LITELLM_MASTER_KEY=<something long>
   3. $VENV/bin/litellm --config $HERE/config.yaml --port $PORT

   Then prove the BRIDGE, which is the only thing that actually decides whether
   the harness works. Without use_chat_completions_api this 404s, and the error
   looks like a network fault rather than a missing setting:

   curl -s http://127.0.0.1:$PORT/v1/responses \\
     -H "Authorization: Bearer \$LITELLM_MASTER_KEY" \\
     -H 'Content-Type: application/json' \\
     -d '{"model":"daemons","input":"say ready"}' | head -c 300
NOTE
