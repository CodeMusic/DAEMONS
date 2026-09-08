# n8n workflows for the AI-play mode

Ten files, in the two-tier shape the RealDex workflows already use: an
**internal** workflow does the work against the model servers, and a **public
relay** on `n8n.codemusic.ca` forwards to `10.0.0.136:5678` with
`x-dex-secret`, `continueOnFail`, and a shaped fallback so a dead backend
degrades instead of erroring.

| endpoint | internal | relay | what it does |
|---|---|---|---|
| `daemon/health` | ✅ | ✅ | probes text, vision, image and TTS and says which are ready |
| `daemon/look` | ✅ | ✅ | describes a screenshot, on request only |
| `daemon/sprite` | ✅ | ✅ | Bonsai draft of a daemon, in §9.4's neutral greys |
| `daemon/voice` | ✅ | ✅ | speaks one line of inner voice in the INDEX voice |
| `daemon/chat` | ⚠️ inactive | ⚠️ inactive | OpenAI chat-completions + thought extraction + TTS |

Reuses `DEX_SHARED_SECRET`, `DEX_KEY`, `MLX_VLM_URL`, `DEX_LLM_URL`,
`BONSAI_URL` and `DEXTER_TTS_URL`, with `DAEMONS_*` overrides where a separate
model is wanted. No new configuration is required to import them.

**The decision loop does not come through here.** It streams, and n8n cannot
relay a stream — see [`../litellm/README.md`](../litellm/README.md) for the
transport split and why Tailscale removes the home/away question entirely.

## Why `daemon/chat` is inactive

**The harness does not speak chat-completions.** `server/src/core/gameLoop.js`
calls `openai.responses.create()` at four sites — the **Responses API** — with
`input:` rather than `messages:`, plus `reasoning: {effort, summary}`,
`service_tier`, `store: true` and `stream: true` consumed as typed events.

`llama.cpp`, LM Studio and Ollama implement `/v1/chat/completions` and **not**
`/v1/responses`, so the `OPENAI_BASE_URL` patch alone gets a 404 on the first
call. It is necessary and nowhere near sufficient.

**And n8n is the wrong instrument for that path anyway.** Proxying streaming
SSE through a webhook node is fighting the tool. Use **LiteLLM proxy** between
the harness and the model — translating Responses to chat, dropping unsupported
parameters, handling the stream is its entire job:

```
harness  --/v1/responses-->  LiteLLM  --/v1/chat/completions-->  roverbyteseer.local:1234
```

`daemon/chat` is kept because it is a working chat-completions endpoint with
the thought extraction and the TTS hook in it, and something else here will
want that. It is simply not what drives the game.

## Reasoning in the console

The one-line-of-reasoning-per-decision idea is worth having, and it comes from
the harness rather than from here — it already streams reasoning summaries, so
surfacing them is a change at the consumer, not a second brain in n8n.
`daemon/chat` shows the shape: lift a labelled `Thought:` line, else the first
sentence under 240 characters, never invent one when absent.

## Speaking, and the voice

`daemon/chat` speaks only when the caller passes `speak: true`, with
`voice: 'index'` by default — the INDEX is what this game calls its record of
daemons (§4.2), so it is the right narrator for a decision worth hearing. Every
step of walking down a route is not.

## `daemon/voice`, and why it is not `daemon/chat`

`daemon/chat` already had a TTS hook, so the obvious move was to reuse it. It
is the wrong shape: `daemon/chat` **runs a model and then speaks what the
model said**. The dashboard already has the thought on screen — the agent
wrote it, we logged it, it is sitting in the panel. Asking a second model what
it thinks about it would produce a different sentence in the same voice, which
is worse than useless: you would be listening to something the player never
thought.

So `daemon/voice` runs no model. Text in, mp3 out, `voice: 'index'` by
default.

**The dashboard proxies it rather than calling it from page JavaScript.** Two
reasons, and the second is the real one — the page would need CORS on the
relay, and the page would need `x-dex-secret` **in its JavaScript**, where
anyone with the dashboard open can read it. A shared secret that ships to the
browser is not a shared secret. `POST /speak` on the harness server holds it.

**Nothing to export at home.** `bindDaemons.sh` defaults `DAEMONS_VOICE_URL`
to the internal workflow, because the machine that runs the harness is the
machine that reaches it — measured 2026-09-08, `10.0.0.136:5678` answers this
Mac in 60ms. Set it only to change tier, or to `""` to turn the button off:

```sh
export DAEMONS_VOICE_URL=https://n8n.codemusic.ca/webhook/daemon/voice  # away
export DAEMONS_VOICE_URL=""                                            # off
```

The export belongs on **whichever machine runs the harness**, not on the n8n
host — `/speak` is a route on the dashboard's own server, and it is that
process that makes the outbound call.

`DEX_SHARED_SECRET` **is not currently set on the n8n side.** Every internal
workflow guards with `if (expected && ...)`, so an unset secret skips the
check; a probe of `daemon/health` with no header returns 200. The harness
forwards the header regardless, so turning the secret on in n8n is the only
change that would be needed.

**Cached twice, on the text both times.** The browser keeps an object URL per
line (60, then it evicts and revokes — an unrevoked blob is a leak that grows
by one mp3 per thought), and the TTS server keys its own cache on a hash of
text and voice. The same thought recurs constantly in this game —
*"I should heal before going further"* — so the second hearing is free at
whichever layer catches it first.

## On using Bonsai for sprites

`daemon/sprite` prompts for **neutral greys with at most one accent**, because
§9.4 is explicit: the art is type-agnostic and the type ramp is a *parameter*
applied at build time, not paint. A colourful generation is one `gbasprite.py`
cannot use.

Treat it as a **drafting tool**. §9.4 also says nothing in a finished sprite is
accidental, and a four-step 384px generation is not that. What it is good for
is seeing a hundred creature ideas quickly without spending a hundred Gemini
prompts — and the good ones then get drawn properly.
