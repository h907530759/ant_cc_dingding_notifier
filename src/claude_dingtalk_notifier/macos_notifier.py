"""macOS 系统通知器"""

import subprocess
import sys
import shutil
from typing import Dict, Any


class MacOSNotifier:
    """macOS 系统通知器

    使用 terminal-notifier 发送系统通知
    需要安装: brew install terminal-notifier
    """

    def __init__(self, enabled: bool = True, sound: bool = True, logger=None):
        """初始化 macOS 通知器

        Args:
            enabled: 是否启用通知
            sound: 是否播放声音
            logger: 可选的日志记录器
        """
        self.enabled = enabled
        self.sound = sound
        self.logger = logger
        self._check_terminal_notifier()

    def _check_terminal_notifier(self) -> bool:
        """检查 terminal-notifier 是否已安装

        Returns:
            bool: 是否已安装
        """
        return shutil.which("terminal-notifier") is not None

    def send(self, title: str, message: str) -> bool:
        """发送 macOS 系统通知

        Args:
            title: 通知标题
            message: 通知内容

        Returns:
            bool: 是否发送成功
        """
        if not self.enabled:
            if self.logger:
                self.logger.debug("macOS notification disabled, skipping")
            return False

        # 检查 terminal-notifier 是否安装
        if not self._check_terminal_notifier():
            error_msg = "terminal-notifier not found. Install with: brew install terminal-notifier"
            if self.logger:
                self.logger.log_channel_failure("macOS-notifier", error_msg)
            else:
                print(f"Warning: {error_msg}", file=sys.stderr)
            return False

        try:
            # 构建 terminal-notifier 命令
            cmd = [
                "terminal-notifier",
                "-title", title,
                "-message", message,
                "-sender", "com.apple.Terminal"  # 指定发送者
            ]

            # 添加声音选项
            if self.sound:
                cmd.extend(["-sound", "default"])

            # 不捕获输出，让错误信息可见
            result = subprocess.run(
                cmd,
                capture_output=False,
                check=False
            )

            # 检查返回码并记录日志
            if result.returncode != 0:
                error_msg = f"terminal-notifier returned code: {result.returncode}"
                if self.logger:
                    self.logger.log_channel_failure("macOS-notifier", error_msg)
                else:
                    print(f"Warning: {error_msg}", file=sys.stderr)
                return False

            if self.logger:
                self.logger.log_channel_success("macOS-notifier", f"Notification sent: {title}")

            return True
        except Exception as e:
            # macOS 通知失败不应该影响钉钉通知
            error_msg = f"macOS notification failed: {e}"
            if self.logger:
                self.logger.log_channel_failure("macOS-notifier", error_msg)
            else:
                print(f"Warning: {error_msg}", file=sys.stderr)
            return False

    def test(self) -> Dict[str, Any]:
        """测试 macOS 通知

        Returns:
            测试结果
        """
        success = self.send(
            title="🍎 macOS 通知测试",
            message="这是一条测试消息，macOS 通知功能正常！"
        )

        return {
            "success": success,
            "message": "macOS 通知测试成功" if success else "macOS 通知测试失败"
        }
