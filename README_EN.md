# Omi -- OpenClaw Voice Companion

A local macOS voice front-end for OpenClaw.

## Why this project is useful

- **Local speech recognition, so always-listening input does not burn extra model tokens**
- **ElevenLabs support for more natural, expressive, and character-like voice output**
- **Custom and cloned voices, as long as you have suitable voice sample material**
- **Both Chinese and English script variants for different usage scenarios**
- **You can later rename the companion and change prompts or wake phrases to fit your own style**
- **A 5-second follow-up window after each reply for more natural conversations**

This project helps **OpenClaw on macOS** become more than a text-based assistant by giving it a real voice.  
You can not only talk to it, but also decide how it sounds: choose a voice you like, clone a character voice you want, or shape it into the speaking companion you imagine.  
You can also keep customizing the companion's name, prompts, and wake phrases over time so it becomes your own version of a voice companion.  

Note:
- If you are using a **Mac mini**, you will need an external microphone because the machine does not include a built-in mic.

中文版: [README.md](./README.md)

## Features
- Always-listening wake phrase detection
- Local speech recognition using macOS Speech.framework
- Voice activity detection for automatic end-of-command capture
- ElevenLabs TTS with caching, with automatic fallback to macOS `say`
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

## Optional configuration
For ElevenLabs voice output:
```bash
export ELEVENLABS_API_KEY="your_key"
export ELEVENLABS_VOICE_ID="your_voice_id"
```

If these variables are missing, the assistant falls back to macOS `say`, but you will lose the more expressive, natural, customizable, and cloneable voice options.

You can choose or create the voice you want here:
- [https://elevenlabs.io](https://elevenlabs.io)

## Script variants
### Chinese version
File: `voice_assistant.py`

Defaults:
- Wake phrases: `hi omi` / `omi` / `欧米`
- Chinese-first transcription
- Better suited for Chinese conversations

Run:
```bash
python3 voice_assistant.py --device 1
```

### English version
File: `voice_assistant_en.py`

Defaults:
- Wake phrases: `hi omi` / `hey omi` / `omi`
- English-first transcription
- Better suited for English conversations

Run:
```bash
python3 voice_assistant_en.py --device 1
```

## List microphones
Chinese version:
```bash
python3 voice_assistant.py --list-devices
```

English version:
```bash
python3 voice_assistant_en.py --list-devices
```

## Notes
- After each spoken reply, the assistant stays in follow-up mode for 5 seconds so you can continue without repeating the wake phrase.
