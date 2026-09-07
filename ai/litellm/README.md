# Home and away

**LiteLLM does not make this work remotely. It makes it work at all.**

Two separate problems, and conflating them is what makes this confusing:

| problem | solved by | status |
|---|---|---|
| the harness speaks `/v1/responses`, the model speaks `/v1/chat/completions` | **LiteLLM** | done, verified on roverbyteseer |
| reaching roverbyteseer from a hotel | **transport** — Tailscale, or the iMac proxy | **not done** |

LiteLLM listens on `roverbyteseer:4000` and is reachable from anything on the
LAN. From outside the house it is reachable from nothing at all. It is the
translator, never the tunnel.

The AI-play mode has **two kinds of traffic**, and trying to push both down one
pipe is what makes this feel harder than it is.

| | shape | transport |
|---|---|---|
| `daemon/look`, `daemon/sprite`, `daemon/health` | one request, one JSON reply | **n8n**, exactly the `dex/*` relay pattern |
| the decision loop | **streaming SSE**, hundreds of calls a run | **not n8n** |

n8n is right for the first row and wrong for the second, and not by a little.
`respondToWebhook` returns a body once; the httpRequest node buffers. A
streaming `/v1/responses` call relayed through a workflow arrives as one blob
after the model has finished, and the SDK — which is doing
`for await (const event of stream)` — cannot parse that. It is not a tuning
problem, it is the wrong instrument.

## Recommended: Tailscale, and the question disappears

Put the laptop and `roverbyteseer` on the same tailnet. Then:

```
OPENAI_BASE_URL=http://roverbyteseer:4000/v1     # at home
OPENAI_BASE_URL=http://roverbyteseer:4000/v1     # in a hotel
```

**The same line.** There is no home/away mode, because there is no longer a
home/away distinction — which is better than code that knows about both.
Streaming works because it is ordinary TCP, no certificate is involved, and the
model server is never exposed to the internet at all.

The public n8n relays stay exactly as they are for `look`, `sprite` and
`health`. They are already built and already work.

## Alternative: reverse-proxy it on the iMac

If you would rather not add a VPN, the iMac already terminates TLS for
`n8n.codemusic.ca`. One block adds a path that proxies to LiteLLM, reusing the
certificate you already have:

```
n8n.codemusic.ca {
    handle_path /llm/* {
        reverse_proxy 10.0.0.136:4000
        flush_interval -1        # stream, do not buffer -- the whole point
    }
    reverse_proxy localhost:5678
}
```

Then away it is `https://n8n.codemusic.ca/llm/v1`, and at home the direct
`http://roverbyteseer.local:4000/v1`.

**This is genuinely fine, with one condition: `master_key` is now the only
thing between the internet and your model server.** LiteLLM checks it on every
call and the harness already sends it as `OPENAI_API_KEY`, so the auth exists —
but set `LITELLM_MASTER_KEY` to something long, and know that Tailscale avoids
the exposure rather than authenticating it.

`flush_interval -1` is not optional. Caddy buffers proxied responses by
default, which reintroduces exactly the problem n8n has.

## Verified 2026-09-07, on the machine

Installed to `~/.litellm-venv` (litellm 1.83.9, system Python 3.9.6 — the
guardrail plugin logs two load errors on 3.9 and the proxy serves regardless).

- `/v1/responses` non-streaming returns a proper Responses object
- `/v1/responses` with `stream: true` emits the full event sequence the harness
  consumes: `response.created`, `in_progress`, `output_item.added`,
  `content_part.added`, `output_text`, `content_part.done`, `response.completed`
- reachable from the laptop at `http://10.0.0.136:4000` — it binds `*:4000`,
  unlike LM Studio, which binds loopback only

**Three things the machine corrected in this config**, all of which would have
looked like a broken bridge:

- LM Studio listens on `127.0.0.1:1234`, so `roverbyteseer.local:1234` resolves
  to an address nothing answers on. LiteLLM runs on the same box, so loopback
  is right — and it is the *proxy* that gets exposed, never LM Studio.
- **Nothing is serving port 8890.** The dex workflows' `MLX_VLM_URL` default
  points at a vision server that is not running; vision is in LM Studio with
  everything else.
- The real model ids are `ternary-bonsai-8b-mlx`, `qwen3.5-0.8b` and
  `minicpm-v-4.6-abliterated-and-disinhibited`. `qwen/qwen3-vl-8b` is loaded
  too, if MiniCPM disappoints on menu text.

## Installing it

`install.sh` does the whole thing and is idempotent:

```
scp -r ai/litellm roverbyte@10.0.0.136:~/daemons-litellm
ssh roverbyte@10.0.0.136 'bash ~/daemons-litellm/install.sh'
```

It picks the newest Python >= 3.9, makes a venv at `~/.litellm-venv`, installs
`litellm[proxy]` — **the `[proxy]` extra matters; plain `litellm` is the SDK
only and serves no `/v1/responses` at all** — then probes the text and vision
backends and prints the model ids they actually report.

*That last step is not padding.* The config says `openai/local-model`, and LM
Studio and llama.cpp each name their loaded model differently. A mismatch is a
404 that reads exactly like a bridge failure, so the installer shows you the
real ids before you go looking in the wrong place.

## Running it

On `roverbyteseer`, beside the models:

```
export LITELLM_MASTER_KEY=<something long>
litellm --config ai/litellm/config.yaml --port 4000
```

Check the bridge before trusting a long run — this is the call that 404s if
`use_chat_completions_api` is missing:

```
curl -s http://roverbyteseer.local:4000/v1/responses \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"daemons","input":"say ready"}' | head -c 300
```

Then `./bindDaemons.sh --ai` with `OPENAI_BASE_URL` set to whichever of the two
lines applies, and `OPENAI_API_KEY` set to the master key.
