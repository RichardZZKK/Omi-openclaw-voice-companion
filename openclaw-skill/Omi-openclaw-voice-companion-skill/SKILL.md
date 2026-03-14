---
name: Omi-openclaw-voice-companion-skill
description: "Use for Omi's local macOS voice companion workflow: starting or stopping the assistant, checking microphone and Terminal launch behavior, and iterating on the OpenClaw + speech + TTS pipeline."
---

# Omi OpenClaw Voice Companion Skill

Use this skill when the task involves Omi's local voice companion on macOS.

## What this skill covers
- Start or stop the assistant in the human's frontmost `Terminal`
- Debug wake phrase, recording, transcription, OpenClaw reply, and TTS behavior
- Keep the workflow aligned with the human's preference that local interactive commands should be run for them when possible
- Work with the open-source project copy at `omi-voice-companion`

## Default behavior
1. Prefer launching through the human's `Terminal` via AppleScript.
2. Stop old assistant processes before starting a new one.
3. Treat microphone, speech recognition, and TTS problems as local macOS workflow issues first.
4. If setup details are needed, read `references/setup.md`.
5. Use the scripts in `scripts/` rather than rewriting launch commands.

## Project path
By default the scripts look for the voice project in one of these places:
- `$OMI_VOICE_ASSISTANT_DIR`
- `$HOME/Esetting/omi-voice-companion`
- a sibling folder named `omi-voice-companion`

## Common commands
Start:
```bash
scripts/start_voice_assistant.sh
```

Stop:
```bash
scripts/stop_voice_assistant.sh
```
