#!/usr/bin/env python3
"""
Omi Voice Assistant V2 (English)

Single persistent microphone stream with a simple state machine:
- idle: keep a rolling wake buffer
- listening: record the command until silence
- thinking: transcribe + call OpenClaw
- speaking: TTS reply
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
import time
import wave
from collections import deque
from enum import Enum
from pathlib import Path

import numpy as np
import sounddevice as sd


ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / ".voice_cache"
SAMPLE_RATE = 16_000
CHANNELS = 1
BLOCKSIZE = 1024
WAKE_PHRASES = ("hi omi", "hey omi", "omi")
EXIT_PHRASES = ("stop listening", "quit assistant", "goodbye assistant", "exit assistant")


class State(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"


def normalize(text: str) -> str:
    lowered = text.lower().strip()
    lowered = lowered.replace("-", " ")
    lowered = " ".join(lowered.split())
    return lowered


def matches_any(text: str, phrases: tuple[str, ...]) -> bool:
    normalized = normalize(text)
    return any(normalize(phrase) in normalized for phrase in phrases)


def save_wav(path: Path, audio: np.ndarray) -> None:
    pcm = np.clip(audio, -1.0, 1.0)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(CHANNELS)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes((pcm * 32767).astype(np.int16).tobytes())


def ensure_swift_binary(source_name: str, binary_name: str) -> Path:
    source = ROOT / source_name
    binary = ROOT / binary_name
    if binary.exists() and binary.stat().st_mtime >= source.stat().st_mtime:
        return binary
    subprocess.run(["swiftc", str(source), "-o", str(binary)], check=True, cwd=str(ROOT))
    return binary


def transcribe_with_swift(wav_path: Path, locale: str) -> str:
    if locale == "zh":
        binary = ensure_swift_binary("native_speech_cn.swift", "native_speech_cn")
    else:
        binary = ensure_swift_binary("native_speech.swift", "native_speech")
    result = subprocess.run(
        [str(binary), str(wav_path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def transcribe_candidates(wav_path: Path) -> list[str]:
    seen: set[str] = set()
    candidates: list[str] = []
    for locale in ("en", "zh"):
        text = transcribe_with_swift(wav_path, locale).strip()
        if text and text not in seen:
            seen.add(text)
            candidates.append(text)
    return candidates


def transcribe(wav_path: Path) -> str:
    english = transcribe_with_swift(wav_path, "en").strip()
    if english:
        return english
    chinese = transcribe_with_swift(wav_path, "zh").strip()
    return chinese


def transcribe_audio_chunks(audio: np.ndarray, chunk_seconds: float = 8.0, min_chunk_seconds: float = 1.0) -> str:
    chunk_samples = int(chunk_seconds * SAMPLE_RATE)
    min_chunk_samples = int(min_chunk_seconds * SAMPLE_RATE)
    texts: list[str] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        offset = 0
        index = 0
        while offset < len(audio):
            chunk = audio[offset:offset + chunk_samples]
            offset += chunk_samples
            if len(chunk) < min_chunk_samples:
                break
            wav_path = temp_root / f"chunk-{index}.wav"
            save_wav(wav_path, chunk)
            text = transcribe(wav_path).strip()
            if text:
                texts.append(text)
            index += 1
    return "".join(texts).strip()


def ask_openclaw(message: str, timeout: int, session_id: str) -> str:
    result = subprocess.run(
        [
            "openclaw",
            "agent",
            "--agent",
            "main",
            "--session-id",
            session_id,
            "--message",
            message,
            "--json",
            "--timeout",
            str(timeout),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        return f"OpenClaw call failed: {stderr}"
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return "OpenClaw returned an unreadable result."
    payloads = payload.get("payloads")
    if not isinstance(payloads, list):
        payloads = payload.get("result", {}).get("payloads", [])
    texts = [item.get("text", "").strip() for item in payloads if item.get("text")]
    return "\n".join(texts).strip() or "OpenClaw returned no text."


from elevenlabs import ElevenLabs

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "").strip()
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY) if ELEVENLABS_API_KEY else None


def get_tts_cache_path(text: str) -> Path:
    CACHE_DIR.mkdir(exist_ok=True)
    safe_name = "".join(ch for ch in text if ch.isalnum())[:24] or "tts"
    return CACHE_DIR / f"{safe_name}.mp3"


def ensure_tts_audio(text: str) -> Path | None:
    clean = " ".join(text.split())
    if not clean:
        return None
    if eleven_client is None or not ELEVENLABS_VOICE_ID:
        return None
    cache_path = get_tts_cache_path(clean)
    if cache_path.exists() and cache_path.stat().st_size > 0:
        return cache_path
    try:
        audio = eleven_client.text_to_speech.convert(
            voice_id=ELEVENLABS_VOICE_ID,
            text=clean,
            model_id="eleven_v3",
        )
        with open(cache_path, "wb") as handle:
            for chunk in audio:
                handle.write(chunk)
        return cache_path
    except Exception:
        return None


def speak(text: str, voice: str) -> None:
    """Speak with ElevenLabs when available, otherwise fall back to macOS say."""
    clean = " ".join(text.split())
    if not clean:
        return

    try:
        subprocess.run(["osascript", "-e", "set volume output volume 60"], check=False)
    except Exception:
        pass

    try:
        cache_path = ensure_tts_audio(clean)
        if cache_path is None:
            raise RuntimeError("failed to build ElevenLabs audio")
        subprocess.run(["afplay", str(cache_path)], check=True)
    except Exception as e:
        print(f"TTS error: {e}, falling back to say")
        subprocess.run(["say", "-v", voice, clean], check=False)


def speak_hint(text: str, voice: str) -> subprocess.Popen[bytes] | None:
    clean = " ".join(text.split())
    if not clean:
        return None
    try:
        cache_path = ensure_tts_audio(clean)
        if cache_path is not None:
            return subprocess.Popen(
                ["afplay", str(cache_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    except Exception:
        pass
    try:
        return subprocess.Popen(
            ["say", "-v", voice, clean],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return None


def audio_to_text_candidates(audio: np.ndarray) -> list[str]:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as handle:
        wav_path = Path(handle.name)
    try:
        save_wav(wav_path, audio)
        return transcribe_candidates(wav_path)
    finally:
        wav_path.unlink(missing_ok=True)


def run_voice_assistant(device: int, voice: str, timeout: int) -> None:
    state = State.IDLE
    wake_buffer: deque[np.ndarray] = deque()
    command_chunks: list[np.ndarray] = []
    last_wake_check = 0.0
    last_voice_time = 0.0
    wake_detected_at = 0.0
    command_started = False
    command_listen_started_at = 0.0
    voice_session_id = f"voice-companion-{int(time.time())}"
    followup_until = 0.0

    wake_window_seconds = 2.5
    wake_window_samples = int(wake_window_seconds * SAMPLE_RATE)
    wake_check_interval = 1.0
    wake_min_voice_samples = int(0.8 * SAMPLE_RATE)
    wake_amplitude_threshold = 0.008
    command_amplitude_threshold = 0.006
    silence_wait = 2.2
    command_start_timeout = 8.0

    print("=" * 50)
    print("🎤 Omi Voice Assistant V2 - Always Listening")
    print("Wake phrases: hi omi / hey omi / omi")
    print("Press Ctrl+C to quit")
    print("=" * 50)

    def current_wake_audio() -> np.ndarray:
        if not wake_buffer:
            return np.array([], dtype=np.float32)
        stacked = np.concatenate(list(wake_buffer), axis=0)
        if len(stacked) > wake_window_samples:
            stacked = stacked[-wake_window_samples:]
        return stacked

    def callback(indata, frames, time_info, status) -> None:
        nonlocal last_voice_time, command_started
        audio = indata.reshape(-1).copy()
        amplitude = float(np.sqrt(np.mean(np.square(audio))))
        if state == State.IDLE:
            wake_buffer.append(audio)
            total = sum(len(chunk) for chunk in wake_buffer)
            while total > wake_window_samples and wake_buffer:
                removed = wake_buffer.popleft()
                total -= len(removed)
            if amplitude > wake_amplitude_threshold:
                last_voice_time = time.time()
        elif state == State.LISTENING:
            command_chunks.append(audio)
            if amplitude > command_amplitude_threshold:
                command_started = True
                last_voice_time = time.time()

    try:
        with sd.InputStream(
            callback=callback,
            channels=CHANNELS,
            samplerate=SAMPLE_RATE,
            dtype="float32",
            device=device,
            blocksize=BLOCKSIZE,
        ):
            while True:
                now = time.time()

                if state == State.IDLE:
                    wake_audio = current_wake_audio()
                    enough_voice = len(wake_audio) >= wake_min_voice_samples
                    if enough_voice and now - last_voice_time < 1.5 and now - last_wake_check >= wake_check_interval:
                        last_wake_check = now
                        candidates = audio_to_text_candidates(wake_audio)
                        if candidates:
                            print(f"[wake] {' | '.join(candidates)}")
                        if any(matches_any(candidate, WAKE_PHRASES) for candidate in candidates):
                            print("✅ Wake detected!")
                            wake_detected_at = now
                            command_chunks = []
                            command_started = False
                            command_listen_started_at = time.time()
                            wake_buffer.clear()
                            state = State.SPEAKING
                            speak("I'm here", voice)
                            command_chunks = []
                            state = State.LISTENING
                            command_listen_started_at = time.time()
                            last_voice_time = 0.0
                            print("🎙️ Listening...")

                elif state == State.LISTENING:
                    if now - wake_detected_at > 120:
                        print("⚠️ Timed out, returning to wake listening")
                        state = State.IDLE
                        command_chunks = []
                        command_started = False
                        followup_until = 0.0
                        wake_buffer.clear()
                    elif followup_until > 0.0 and not command_started and now >= followup_until:
                        print("🫧 Follow-up window ended, returning to wake listening")
                        state = State.IDLE
                        command_chunks = []
                        command_started = False
                        followup_until = 0.0
                    elif not command_started and now - command_listen_started_at >= command_start_timeout:
                        print("⚠️ No command detected, returning to wake listening")
                        state = State.IDLE
                        command_chunks = []
                        command_started = False
                    elif command_started and command_chunks and now - last_voice_time >= silence_wait:
                        print("✅ Recording finished")
                        state = State.THINKING

                elif state == State.THINKING:
                    audio = np.concatenate(command_chunks, axis=0) if command_chunks else np.array([], dtype=np.float32)
                    command_chunks = []
                    command_started = False
                    if len(audio) == 0:
                        state = State.IDLE
                        continue
                    print(f"📏 Duration: {len(audio) / SAMPLE_RATE:.1f}s")
                    print("🔄 Transcribing...")
                    command = transcribe_audio_chunks(audio).strip()
                    if not command:
                        print("❌ I didn't catch that")
                        state = State.SPEAKING
                        speak("I didn't catch that", voice)
                        state = State.IDLE
                        followup_until = 0.0
                        continue
                    print(f"[command] {command}")
                    if matches_any(command, EXIT_PHRASES):
                        state = State.SPEAKING
                        speak("Okay, goodbye", voice)
                        state = State.IDLE
                        followup_until = 0.0
                        continue
                    print("🤔 Thinking...")
                    hint_proc = speak_hint("Let me think", voice)
                    reply = ask_openclaw(command, timeout=timeout, session_id=voice_session_id)
                    if hint_proc is not None and hint_proc.poll() is None:
                        hint_proc.terminate()
                    preview = reply if len(reply) <= 160 else f"{reply[:160]}..."
                    print(f"[reply] {preview}")
                    state = State.SPEAKING
                    speak(reply, voice)
                    state = State.LISTENING
                    command_chunks = []
                    command_started = False
                    command_listen_started_at = time.time()
                    wake_detected_at = command_listen_started_at
                    followup_until = command_listen_started_at + 5.0
                    last_voice_time = 0.0
                    print("🎧 Follow-up mode... ask again within 5 seconds")

                time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nVoice assistant stopped.")


def print_devices() -> None:
    devices = sd.query_devices()
    for index, device in enumerate(devices):
        if device["max_input_channels"] > 0:
            print(f"{index}: {device['name']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Omi Voice Assistant V2 (English)")
    parser.add_argument("--list-devices", action="store_true", help="List microphones")
    parser.add_argument("--device", type=int, default=1, help="Input device")
    parser.add_argument("--voice", default="Samantha", help="macOS say voice fallback")
    parser.add_argument("--timeout", type=int, default=120, help="OpenClaw timeout")
    args = parser.parse_args()

    if not ELEVENLABS_API_KEY or not ELEVENLABS_VOICE_ID:
        print("ℹ️ ElevenLabs is not configured. Falling back to macOS say.")

    if args.list_devices:
        print_devices()
        return

    run_voice_assistant(args.device, args.voice, args.timeout)


if __name__ == "__main__":
    main()
