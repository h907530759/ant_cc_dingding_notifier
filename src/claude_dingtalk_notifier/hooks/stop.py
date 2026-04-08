#!/usr/bin/env python3
"""
Claude Code Stop Hook for DingTalk Notification
Triggered when Claude Code stops working
"""

import sys
from pathlib import Path
from datetime import datetime

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
    # Get project name
    project = str(Path.cwd().name)

    # Load config
    config = get_default_config()

    # Check if enabled
    stop_event = config.events.get("stop")
    if not config.dingtalk.enabled or not stop_event or not stop_event.enabled:
        return

    # Send completion notification
    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    message_data = {
        "project": project,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    message = format_claude_message("stop", message_data)
    if message:
        notifier.send(message)


if __name__ == "__main__":
    main()
