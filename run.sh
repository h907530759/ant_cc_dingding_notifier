#!/bin/bash
# Quick run script for Claude DingTalk Notifier (without installation)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export PYTHONPATH="$SCRIPT_DIR/src:$PYTHONPATH"

python3 -m claude_dingtalk_notifier.cli "$@"
