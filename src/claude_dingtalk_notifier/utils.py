"""Utility functions for Claude DingTalk Notifier"""

import os
import sys
from pathlib import Path
from typing import Optional


def get_project_name(cwd: Optional[str] = None) -> str:
    """
    Get project name from current working directory

    Args:
        cwd: Current working directory path

    Returns:
        Project name
    """
    if not cwd:
        cwd = os.getcwd()

    return Path(cwd).name


def find_git_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Find git repository root directory

    Args:
        start_path: Starting path to search from

    Returns:
        Path to git root or None
    """
    if not start_path:
        start_path = Path.cwd()

    current = start_path
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent

    return None


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}分钟"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}小时"


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Truncate text to maximum length

    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def is_valid_dingtalk_webhook(webhook: str) -> bool:
    """
    Validate DingTalk webhook URL

    Args:
        webhook: Webhook URL to validate

    Returns:
        True if valid, False otherwise
    """
    if not webhook:
        return False

    return webhook.startswith("https://oapi.dingtalk.com/robot/send")


def sanitize_input(text: str) -> str:
    """
    Sanitize user input for safe display

    Args:
        text: Input text

    Returns:
        Sanitized text
    """
    # Remove potential dangerous characters
    dangerous_chars = ['\x00', '\r']
    for char in dangerous_chars:
        text = text.replace(char, '')

    return text.strip()
