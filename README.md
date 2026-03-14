# Omi Voice Assistant

A macOS local voice front-end for OpenClaw.

## Features
- Always-listening wake phrase detection (`hi omi`, `omi`, `欧米`)
- Local speech recognition with macOS Speech.framework via Swift helpers
- Voice activity detection for end-of-command capture
- OpenClaw CLI integration through a dedicated voice session
- ElevenLabs TTS with cache, with automatic fallback to macOS `say`
- 5-second follow-up window after each reply for more natural conversations

## Requirements
- macOS
- Python 3.11+
- OpenClaw installed and working in the shell
- Microphone permission granted to Terminal
- `swiftc` available

## Install
```bash
pip3 install -r requirements.txt
```

## Configure
Optional ElevenLabs support:
```bash
export ELEVENLABS_API_KEY="your_key"
export ELEVENLABS_VOICE_ID="your_voice_id"
```

Without those variables, the assistant will fall back to macOS `say`.

## Run
List microphones:
```bash
python3 voice_assistant.py --list-devices
```

Start:
```bash
python3 voice_assistant.py --device 1
```

## Notes
- The assistant keeps a dedicated OpenClaw voice session per run so it does not reuse unrelated chat context.
- After each spoken reply, it stays in follow-up mode for 5 seconds so you can continue talking without a wake phrase.
