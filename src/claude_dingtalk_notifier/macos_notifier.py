"""macOS 系统通知器"""

import subprocess
import sys
from typing import Dict, Any


class MacOSNotifier:
    """macOS 系统通知器

    使用 osascript 调用 macOS NotificationCenter 发送系统通知
    零外部依赖，使用系统自带功能
    """

    def __init__(self, enabled: bool = True, sound: bool = True):
        """初始化 macOS 通知器

        Args:
            enabled: 是否启用通知
            sound: 是否播放声音
        """
        self.enabled = enabled
        self.sound = sound

    def send(self, title: str, message: str) -> bool:
        """发送 macOS 系统通知

        Args:
            title: 通知标题
            message: 通知内容

        Returns:
            bool: 是否发送成功
        """
        if not self.enabled:
            return False

        # 转义引号和反斜杠
        title_escaped = title.replace('"', '\\"').replace('\\', '\\\\')
        message_escaped = message.replace('"', '\\"').replace('\\', '\\\\')

        # 构建 AppleScript
        sound_option = 'sound name "default"' if self.sound else ''

        script = f'''display notification "{message_escaped}" with title "{title_escaped}" {sound_option}'''

        try:
            subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                check=False
            )
            return True
        except Exception as e:
            # macOS 通知失败不应该影响钉钉通知
            print(f"macOS notification failed: {e}", file=sys.stderr)
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
