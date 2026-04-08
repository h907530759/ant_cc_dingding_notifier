"""Claude Code DingTalk Notifier"""

__version__ = "0.3.1"
__author__ = "suchen"
__license__ = "MIT"

from .config import Config
from .dingtalk import DingTalkNotifier

__all__ = ["Config", "DingTalkNotifier"]
