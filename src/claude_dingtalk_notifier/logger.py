"""Logger utility for Claude DingTalk Notifier hooks"""

import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional


class HookLogger:
    """Logger for hook execution and errors"""

    _instance: Optional['HookLogger'] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls, log_dir: Optional[Path] = None):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(log_dir)
        return cls._instance

    def _initialize(self, log_dir: Optional[Path] = None):
        """Initialize logger"""
        if self._logger is not None:
            return

        # Default log directory
        if log_dir is None:
            log_dir = Path.home() / ".claude-dingtalk"

        # Create log directory
        log_dir.mkdir(parents=True, exist_ok=True)

        # Setup logger
        self._logger = logging.getLogger("claude_dingtalk_hooks")
        self._logger.setLevel(logging.DEBUG)

        # Clear existing handlers
        self._logger.handlers.clear()

        # File handler - detailed logging
        log_file = log_dir / "hook.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self._logger.addHandler(file_handler)

        # Console handler - errors only
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.ERROR)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)

    def log_hook_start(self, hook_name: str, input_data: dict = None):
        """Log hook execution start"""
        self._logger.info(f"Hook started: {hook_name}")
        if input_data:
            self._logger.debug(f"Input data: {input_data}")

    def log_hook_success(self, hook_name: str, message: str = ""):
        """Log successful hook execution"""
        self._logger.info(f"Hook succeeded: {hook_name} - {message}")

    def log_hook_error(self, hook_name: str, error: Exception, context: str = ""):
        """Log hook error"""
        error_msg = f"Hook failed: {hook_name}"
        if context:
            error_msg += f" - {context}"
        error_msg += f" - Error: {type(error).__name__}: {str(error)}"
        self._logger.error(error_msg, exc_info=True)

    def log_dingtalk_response(self, success: bool, status_code: int = None, response: dict = None):
        """Log DingTalk API response"""
        if success:
            self._logger.info(f"DingTalk notification sent successfully")
        else:
            self._logger.error(
                f"DingTalk notification failed - "
                f"Status: {status_code}, Response: {response}"
            )

    def log_import_error(self, hook_name: str, error: ImportError):
        """Log import error"""
        self._logger.error(
            f"Import error in {hook_name}: {type(error).__name__}: {str(error)}",
            exc_info=True
        )

    def log_config_error(self, hook_name: str, error: Exception):
        """Log configuration error"""
        self._logger.error(
            f"Configuration error in {hook_name}: {type(error).__name__}: {str(error)}",
            exc_info=True
        )

    def debug(self, message: str):
        """Log debug message"""
        self._logger.debug(message)

    def info(self, message: str):
        """Log info message"""
        self._logger.info(message)

    def warning(self, message: str):
        """Log warning message"""
        self._logger.warning(message)

    def error(self, message: str):
        """Log error message"""
        self._logger.error(message)


def get_logger(log_dir: Optional[Path] = None) -> HookLogger:
    """Get logger instance"""
    return HookLogger(log_dir)
