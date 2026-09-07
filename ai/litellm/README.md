# Home and away

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
