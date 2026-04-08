#!/usr/bin/env python3
"""
Claude Code PostToolUse Hook for DingTalk Notification
Triggered after a tool is used
"""

import sys
import json
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from claude_dingtalk_notifier.config import get_default_config
    from claude_dingtalk_notifier.dingtalk import DingTalkNotifier, format_claude_message
    from claude_dingtalk_notifier.config import EventConfig
except ImportError:
    # Fallback for development
    pass


def main():
    """Main hook function"""
    # Read input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # No input, just exit
        return

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Load config
    config = get_default_config()

    # Check if enabled
    post_tool_use_event = config.events.get("post_tool_use")
    if not config.dingtalk.enabled or not post_tool_use_event or not post_tool_use_event.enabled:
        return

    # Check for errors
    has_error = input_data.get("hasError", False)
    tool_name = input_data.get("name", "")

    if has_error:
        # Send error notification
        notifier = DingTalkNotifier(
            webhook=config.dingtalk.webhook,
            secret=config.dingtalk.secret
        )

        message_data = {
            "project": project,
            "name": tool_name,
            "hasError": has_error
        }

        message = format_claude_message("post_tool_use", message_data)
        if message:
            notifier.send(message)


if __name__ == "__main__":
    main()
