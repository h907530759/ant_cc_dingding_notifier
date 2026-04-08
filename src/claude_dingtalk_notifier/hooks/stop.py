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
    from claude_dingtalk_notifier.dingtalk import DingTalkNotifier, format_claude_message, DingTalkMessage
    from claude_dingtalk_notifier.logger import get_logger
    from claude_dingtalk_notifier.config import EventConfig
except ImportError as e:
    # Import error - print warning and exit
    print(f"Warning: Could not import claude_dingtalk_notifier: {e}", file=sys.stderr)
    sys.exit(0)


def main():
    """Main hook function"""
    hook_name = "stop"

    # Initialize logger
    logger = get_logger()
    logger.log_hook_start(hook_name)

    try:
        # Get project name
        project = str(Path.cwd().name)

        # Load config
        config = get_default_config()

        # Check if enabled
        stop_event = config.events.get("stop")
        if not config.dingtalk.enabled or not stop_event or not stop_event.enabled:
            logger.debug(f"{hook_name} hook is disabled")
            return

        # Send completion notification
        notifier = DingTalkNotifier(
            webhook=config.dingtalk.webhook,
            secret=config.dingtalk.secret,
            logger=logger
        )

        message_data = {
            "project": project,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        message = format_claude_message("stop", message_data)
        if message:
            result = notifier.send(DingTalkMessage(
                title="Claude Code 任务完成",
                text=message,
                msg_type="markdown"
            ))

            if result.get("success"):
                logger.log_hook_success(hook_name, "Notification sent successfully")
            else:
                logger.log_hook_error(
                    hook_name,
                    Exception(result.get("error", "Unknown error")),
                    "Failed to send notification"
                )
        else:
            logger.warning(f"Failed to format message for {hook_name} hook")

    except Exception as e:
        logger.log_hook_error(hook_name, e, "Unexpected error in hook execution")
        # Don't raise - hook failures shouldn't break Claude Code
        sys.exit(0)


if __name__ == "__main__":
    main()
