# Voice Assistant Setup Notes

## Expected project files
- `voice_assistant.py`
- `voice_assistant_en.py`
- `native_speech.swift`
- `native_speech_cn.swift`

## Environment variables
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID`
- `OMI_VOICE_ASSISTANT_DIR` (optional project path override)
- `OMI_VOICE_ASSISTANT_DEVICE` (optional microphone device id, default `1`)
- `OMI_VOICE_ASSISTANT_SCRIPT` (optional script name, default `voice_assistant.py`)

If ElevenLabs variables are missing, the assistant should still work and fall back to `say`.

## Run behavior
- Default device: `--device 1`
- The assistant should be launched in the frontmost `Terminal` window
- If the project path is not obvious, set `OMI_VOICE_ASSISTANT_DIR` before running the start script
