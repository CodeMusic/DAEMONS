# Speech to text on roverbyteseer (companion C-83)

`whisper_server.py`: MLX Whisper behind an OpenAI-compatible `/v1/audio/transcriptions`, on port 8000. n8n's
`daemon/talk` and `daemon/hear` call it at `DAEMONS_STT_URL` (default `http://host.docker.internal:8000`, which from
n8n's container is roverbyteseer itself).

## Install (on roverbyteseer, once)

```sh
brew install ffmpeg                                   # skip if `ffmpeg -version` already answers
mkdir -p ~/daemons-stt && cd ~/daemons-stt
curl -fsSLO https://raw.githubusercontent.com/CodeMusic/DAEMONS/main/ai/stt/whisper_server.py
python3 -m venv venv && ./venv/bin/pip install --upgrade pip mlx-whisper fastapi uvicorn python-multipart numpy
./venv/bin/python whisper_server.py                   # first run downloads the model (~1.6 GB); Ctrl-C when it says ready
```

## Keep it running (a launch agent: starts at login, restarts if it stops)

```sh
cat > ~/Library/LaunchAgents/ca.codemusic.daemons-stt.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>ca.codemusic.daemons-stt</string>
  <key>ProgramArguments</key><array>
    <string>$HOME/daemons-stt/venv/bin/python</string><string>$HOME/daemons-stt/whisper_server.py</string>
  </array>
  <key>EnvironmentVariables</key><dict>
    <key>PATH</key><string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
  </dict>
  <key>RunAtLoad</key><true/><key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$HOME/daemons-stt/stt.log</string>
  <key>StandardErrorPath</key><string>$HOME/daemons-stt/stt.log</string>
</dict></plist>
EOF
launchctl load ~/Library/LaunchAgents/ca.codemusic.daemons-stt.plist
curl -s localhost:8000/health                         # {"ok": true, "model": "mlx-community/whisper-large-v3-turbo"}
```

A smaller, faster model: set `WHISPER_MODEL` to `mlx-community/whisper-small-mlx` in the plist's EnvironmentVariables.
