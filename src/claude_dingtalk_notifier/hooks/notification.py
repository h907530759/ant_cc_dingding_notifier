#!/usr/bin/env python3
"""
Claude Code Notification Hook for DingTalk Notification
Triggered for permission requests and idle prompts
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
    notification_event = config.events.get("notification")
    if not config.dingtalk.enabled or not notification_event or not notification_event.enabled:
        return

    # Get notification type
    notif_type = input_data.get("type", "")

    if notif_type == "permission_prompt":
        # Send notification
        notifier = DingTalkNotifier(
            webhook=config.dingtalk.webhook,
            secret=config.dingtalk.secret
        )

        message_data = {
            "project": project,
            "type": notif_type,
            "text": input_data.get("text", "")
        }

        message = format_claude_message("notification", message_data)
        if message:
            notifier.send(message)


if __name__ == "__main__":
    main()
