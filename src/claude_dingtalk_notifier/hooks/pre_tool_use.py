#!/usr/bin/env python3
"""
Claude Code PreToolUse Hook for DingTalk Notification
Triggered before a tool is used
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
        # No input, just allow
        json.dump({"authorized": True}, sys.stdout)
        return

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Load config
    config = get_default_config()

    # Check if enabled
    pre_tool_use_event = config.events.get("pre_tool_use")
    if not config.dingtalk.enabled or not pre_tool_use_event or not pre_tool_use_event.enabled:
        json.dump({"authorized": True}, sys.stdout)
        return

    # Check for sensitive operations
    tool_name = input_data.get("name", "")
    tool_input = input_data.get("input", {})
    sensitive_patterns = config.sensitive_operations.get("patterns", [])

    is_sensitive = any(
        pattern in str(tool_input).lower()
        for pattern in sensitive_patterns
    )

    if is_sensitive:
        # Send notification
        notifier = DingTalkNotifier(
            webhook=config.dingtalk.webhook,
            secret=config.dingtalk.secret
        )

        message_data = {
            "project": project,
            "name": tool_name,
            "input": tool_input,
            "sensitive_patterns": sensitive_patterns
        }

        message = format_claude_message("pre_tool_use", message_data)
        if message:
            notifier.send(message)

    # Always allow the operation
    json.dump({"authorized": True}, sys.stdout)


if __name__ == "__main__":
    main()
