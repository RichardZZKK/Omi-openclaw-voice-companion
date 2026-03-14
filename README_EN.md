# Omi -- OpenClaw Voice Companion

A local macOS voice front-end for OpenClaw.

## Why this project is useful

- **Local speech recognition, so always-listening input does not burn extra model tokens**
- **ElevenLabs support for more natural, expressive, and character-like voice output, with custom and cloned voices when you have suitable sample material**
- **Both Chinese and English script variants for different usage scenarios**
- **You can later rename the companion and change prompts or wake phrases to fit your own style**

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

## Requirements
- macOS
- Python 3.11+
- OpenClaw installed and working in the shell
- Microphone permission granted to Terminal
- `swiftc` available

## Install
Clone the project and enter the folder:

```bash
git clone git@github.com:RichardZZKK/Omi-openclaw-voice-assistant.git
cd Omi-openclaw-voice-assistant
```

If you prefer HTTPS, you can use:

```bash
git clone https://github.com/RichardZZKK/Omi-openclaw-voice-assistant.git
cd Omi-openclaw-voice-assistant
```

Install dependencies:

```bash
pip3 install -r requirements.txt
```

If you get a permission error such as `Permission denied` or `externally-managed-environment`, use:

```bash
python3 -m pip install --user -r requirements.txt
```

If a package install fails, try upgrading `pip` first and then retry:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --user -r requirements.txt
```

The first time you run the assistant, macOS may ask for permissions.

Allow:
- `Microphone`
- `Speech Recognition` (if prompted)

If nothing pops up, check manually:
- `System Settings -> Privacy & Security -> Microphone`
- `System Settings -> Privacy & Security -> Speech Recognition`

Make sure `Terminal` is allowed.

## Configuration
For ElevenLabs voice output:
```bash
export ELEVENLABS_API_KEY="your_key"
export ELEVENLABS_VOICE_ID="your_voice_id"
```

If these variables are missing, the assistant falls back to macOS `say`, but you will lose the more expressive, natural, customizable, and cloneable voice options.

Getting an API key is simple:
- Sign in to ElevenLabs
- Open your account or developer settings
- Create an API key

You can also choose, create, or clone the voice you want here:
- [https://elevenlabs.io](https://elevenlabs.io)

## Optional configuration
If you want to change the companion name, prompts, or wake phrases, edit the script files directly:

- Chinese version: `voice_assistant.py`
- English version: `voice_assistant_en.py`

The most common places to customize are:
- `WAKE_PHRASES`: change the wake phrases
- `EXIT_PHRASES`: change the exit phrases
- Spoken prompt text: lines such as “我在”, “我没有听清”, or “让我想想” in the Chinese script, and their English equivalents in the English script

If you want to turn it into your own named companion, the usual approach is:
- change the wake phrases to the name you want to use
- update the spoken prompts to match the personality you want

## Run modes
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

## Author
- [RichardZZKK](https://github.com/RichardZZKK)
