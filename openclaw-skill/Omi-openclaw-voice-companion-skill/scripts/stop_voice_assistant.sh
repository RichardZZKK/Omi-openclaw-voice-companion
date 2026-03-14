#!/bin/zsh
set -euo pipefail

VOICE_SCRIPT="${OMI_VOICE_ASSISTANT_SCRIPT:-voice_assistant.py}"
DEVICE="${OMI_VOICE_ASSISTANT_DEVICE:-1}"

pkill -f "python3 $VOICE_SCRIPT --device $DEVICE" || true
pkill -f "/Python .*${VOICE_SCRIPT} --device ${DEVICE}" || true
pkill -f 'voice_assistant_v2.py --device 1' || true
