#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_HOME_PROJECT="$HOME/Esetting/omi-voice-assistant"
DEFAULT_SIBLING_PROJECT="$(cd "$SCRIPT_DIR/../../.." && pwd)/omi-voice-assistant"
PROJECT_DIR="${OMI_VOICE_ASSISTANT_DIR:-}"
VOICE_SCRIPT="${OMI_VOICE_ASSISTANT_SCRIPT:-voice_assistant.py}"
DEVICE="${OMI_VOICE_ASSISTANT_DEVICE:-1}"

if [[ -z "$PROJECT_DIR" ]]; then
  if [[ -d "$DEFAULT_HOME_PROJECT" ]]; then
    PROJECT_DIR="$DEFAULT_HOME_PROJECT"
  elif [[ -d "$DEFAULT_SIBLING_PROJECT" ]]; then
    PROJECT_DIR="$DEFAULT_SIBLING_PROJECT"
  else
    echo "Could not find the voice assistant project. Set OMI_VOICE_ASSISTANT_DIR first." >&2
    exit 1
  fi
fi

if [[ ! -f "$PROJECT_DIR/$VOICE_SCRIPT" ]]; then
  echo "Could not find $VOICE_SCRIPT in $PROJECT_DIR" >&2
  exit 1
fi

pkill -f "python3 $VOICE_SCRIPT --device $DEVICE" >/dev/null 2>&1 || true
pkill -f "/Python .*${VOICE_SCRIPT} --device ${DEVICE}" >/dev/null 2>&1 || true

COMMAND="cd ${PROJECT_DIR:q} && python3 ${VOICE_SCRIPT:q} --device ${DEVICE:q}"
osascript -e 'tell application "Terminal" to activate' -e "tell application \"Terminal\" to do script \"${COMMAND}\""
