"""DingTalk robot notification handler"""

import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class DingTalkMessage:
    """DingTalk message data class"""
    title: str
    text: str
    msg_type: str = "markdown"
    btn_orientation: str = "1"  # 0: vertical, 1: horizontal
    btns: Optional[List[Dict[str, str]]] = None


class DingTalkNotifier:
    """DingTalk robot notification handler"""

    def __init__(self, webhook: str, secret: str = ""):
        """
        Initialize DingTalk notifier

        Args:
            webhook: DingTalk robot webhook URL
            secret: DingTalk robot secret (optional, for signature verification)
        """
        self.webhook = webhook
        self.secret = secret

    def _generate_sign(self, timestamp: int) -> str:
        """Generate signature for DingTalk webhook"""
        if not self.secret:
            return ""

        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')

        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        return sign

    def _build_url(self) -> str:
        """Build complete webhook URL with signature"""
        if not self.secret:
            return self.webhook

        timestamp = int(time.time() * 1000)
        sign = self._generate_sign(timestamp)

        return f"{self.webhook}&timestamp={timestamp}&sign={sign}"

    def _build_message(self, message: DingTalkMessage) -> Dict[str, Any]:
        """Build DingTalk message payload"""
        if message.msg_type == "markdown":
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "title": message.title,
                    "text": message.text
                }
            }
        elif message.msg_type == "actionCard":
            payload = {
                "msgtype": "actionCard",
                "actionCard": {
                    "title": message.title,
                    "text": message.text,
                    "btnOrientation": message.btn_orientation
                }
            }

            # Add buttons if provided
            if message.btns:
                payload["actionCard"]["btns"] = message.btns
        else:
            # Default to text
            payload = {
                "msgtype": "text",
                "text": {
                    "content": message.text
                }
            }

        return payload

    def send(self, message: DingTalkMessage) -> Dict[str, Any]:
        """
        Send message to DingTalk

        Args:
            message: DingTalkMessage instance

        Returns:
            Response from DingTalk API
        """
        try:
            url = self._build_url()
            payload = self._build_message(message)

            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            result = response.json()

            if result.get("errcode") == 0:
                return {"success": True, "data": result}
            else:
                return {
                    "success": False,
                    "error": result.get("errmsg", "Unknown error"),
                    "errcode": result.get("errcode")
                }

        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timeout"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_markdown(self, title: str, text: str) -> Dict[str, Any]:
        """
        Send markdown message

        Args:
            title: Message title
            text: Markdown formatted text

        Returns:
            Response from DingTalk API
        """
        message = DingTalkMessage(title=title, text=text, msg_type="markdown")
        return self.send(message)

    def send_action_card(self, title: str, text: str,
                        btns: Optional[List[Dict[str, str]]] = None,
                        btn_orientation: str = "1") -> Dict[str, Any]:
        """
        Send action card message

        Args:
            title: Message title
            text: Message text
            btns: List of buttons [{"title": "Button", "actionURL": "https://..."}]
            btn_orientation: Button orientation (0: vertical, 1: horizontal)

        Returns:
            Response from DingTalk API
        """
        message = DingTalkMessage(
            title=title,
            text=text,
            msg_type="actionCard",
            btns=btns,
            btn_orientation=btn_orientation
        )
        return self.send(message)

    def send_text(self, content: str) -> Dict[str, Any]:
        """
        Send text message

        Args:
            content: Text content

        Returns:
            Response from DingTalk API
        """
        message = DingTalkMessage(title="Notification", text=content, msg_type="text")
        return self.send(message)

    def test_connection(self) -> Dict[str, Any]:
        """
        Test DingTalk webhook connection

        Returns:
            Test result
        """
        test_message = DingTalkMessage(
            title="🔔 Claude Code 钉钉通知测试",
            text="### ✅ 连接成功\n\n这是一条测试消息，您的钉钉机器人配置正常！",
            msg_type="markdown"
        )

        return self.send(test_message)


def format_claude_message(event_type: str, data: Dict[str, Any]) -> DingTalkMessage:
    """
    Format Claude Code event to DingTalk message

    Args:
        event_type: Event type
        data: Event data

    Returns:
        Formatted DingTalkMessage or None
    """
    if event_type == "pre_tool_use":
        tool_name = data.get("name", "Unknown")
        input_data = data.get("input", {})
        project = data.get("project", "Unknown")

        # Check if sensitive operation
        sensitive_patterns = data.get("sensitive_patterns", [])
        is_sensitive = any(
            pattern in str(input_data).lower()
            for pattern in sensitive_patterns
        )

        if is_sensitive:
            return DingTalkMessage(
                title="🔐 Claude Code 敏感操作检测",
                text=f"""### ⚠️ 检测到敏感操作

> Claude Code 已检测到可能的敏感操作

---
**📂 项目:** {project}
**⚡ 工具:** {tool_name}
**📝 输入:** ```{str(input_data)[:200]}...```

💡 请在终端中确认是否继续执行""",
                msg_type="actionCard",
                btns=[
                    {"title": "📱 查看终端", "actionURL": "https://code.anthropic.com"}
                ]
            )
        else:
            return DingTalkMessage(
                title="🔧 Claude Code 工具使用",
                text=f"""### 🔧 工具使用中

**📂 项目:** {project}
**⚡ 工具:** {tool_name}""",
                msg_type="markdown"
            )

    elif event_type == "post_tool_use":
        tool_name = data.get("name", "Unknown")
        has_error = data.get("hasError", False)
        project = data.get("project", "Unknown")

        if has_error:
            return DingTalkMessage(
                title="❌ Claude Code 执行错误",
                text=f"""### ❌ 工具执行出错

**📂 项目:** {project}
**⚡ 工具:** {tool_name}
**❌ 错误:** 工具执行过程中出现错误，请检查终端输出""",
                msg_type="markdown"
            )
        # Skip success notifications to reduce noise
        return None

    elif event_type == "stop":
        # Stop hook doesn't provide reason info, use simple message
        return DingTalkMessage(
            title="✅ 工作已结束",
            text=f"""### ✅ 工作已结束

**📂 项目:** {data.get("project", "Unknown")}
**⏰ 时间:** {data.get("time", "")}

💡 工作已全部完成，可以查看结果了""",
            msg_type="markdown"
        )

    elif event_type == "notification":
        notif_type = data.get("type", "")
        project = data.get("project", "Unknown")

        if notif_type == "permission_prompt":
            return DingTalkMessage(
                title="🔐 Claude Code 权限请求",
                text=f"""### 🔐 需要权限确认

> Claude Code 请求执行操作权限

---
**📂 项目:** {project}
**📝 说明:** {data.get("text", "")}

💡 请在终端中确认操作""",
                msg_type="actionCard",
                btns=[{"title": "📱 查看终端", "actionURL": "https://code.anthropic.com"}]
            )
        elif notif_type == "idle_prompt":
            # Skip idle notifications
            return None

    elif event_type == "session_start":
        return DingTalkMessage(
            title="🚀 会话已启动",
            text=f"""### 🚀 新会话已启动

**📂 项目:** {data.get("project", "Unknown")}
**⏰ 开始时间:** {data.get("time", "")}

💡 让我们开始工作吧！""",
            msg_type="markdown"
        )

    elif event_type == "session_end":
        return DingTalkMessage(
            title="👋 会话已结束",
            text=f"""### 👋 会话已结束

**📂 项目:** {data.get("project", "Unknown")}
**⏰ 结束时间:** {data.get("time", "")}

👋 感谢使用，再见！""",
            msg_type="markdown"
        )

    elif event_type == "tool_failure":
        tool_name = data.get("name", "Unknown")
        error = data.get("error", "Unknown error")
        project = data.get("project", "Unknown")

        return DingTalkMessage(
            title="💥 Claude Code 工具失败",
            text=f"""### 💥 工具执行失败

**📂 项目:** {project}
**⚡ 工具:** {tool_name}
**❌ 错误信息:** ```
{error[:500]}
```

💡 请检查终端了解详情""",
            msg_type="markdown"
        )

    elif event_type == "task_created":
        task_id = data.get("task_id", "")
        subject = data.get("subject", "Unknown task")
        project = data.get("project", "Unknown")

        return DingTalkMessage(
            title="📋 Claude Code 任务创建",
            text=f"""### 📋 新任务已创建

**📂 项目:** {project}
**🆔 任务ID:** {task_id}
**📝 任务:** {subject}

🚀 任务已添加到队列""",
            msg_type="markdown"
        )

    elif event_type == "task_completed":
        task_id = data.get("task_id", "")
        subject = data.get("subject", "Unknown task")
        project = data.get("project", "Unknown")

        return DingTalkMessage(
            title="✅ Claude Code 任务完成",
            text=f"""### ✅ 任务已完成

**📂 项目:** {project}
**🆔 任务ID:** {task_id}
**📝 任务:** {subject}

🎉 太棒了，又完成一个任务！""",
            msg_type="markdown"
        )

    elif event_type == "cwd_changed":
        old_cwd = data.get("old_cwd", "Unknown")
        new_cwd = data.get("new_cwd", "Unknown")
        project = data.get("project", "Unknown")

        return DingTalkMessage(
            title="📂 目录切换",
            text=f"""### 📂 工作目录已切换

**📂 项目:** {project}
**📍 从:** `{old_cwd}`
**➡️ 到:** `{new_cwd}`

💡 已切换到新目录""",
            msg_type="markdown"
        )

    elif event_type == "config_change":
        project = data.get("project", "Unknown")
        config_path = data.get("config_path", "Unknown")
        change_type = data.get("change_type", "修改")

        return DingTalkMessage(
            title=f"⚙️ 配置文件已{change_type}",
            text=f"""### ⚙️ 配置文件已{change_type}

**📂 项目:** {project}
**📁 文件:** {config_path}
**🔄 变更类型:** {change_type}

💡 Claude Code 配置文件已{change_type}""",
            msg_type="markdown"
        )

    elif event_type == "subagent_start":
        agent_type = data.get("agent_type", "Unknown")
        agent_id = data.get("agent_id", "Unknown")
        agent_name = data.get("agent_name", "Unknown")
        task = data.get("task", "Unknown")
        project = data.get("project", "Unknown")

        return DingTalkMessage(
            title=f"🤖 {agent_name} 开始工作",
            text=f"""### 🤖 子代理已启动

**📂 项目:** {project}
**🤖 代理:** {agent_name} ({agent_type})
**🆔 代理ID:** {agent_id}
**📝 任务:** {task}

🚀 子代理开始执行任务...""",
            msg_type="markdown"
        )

    elif event_type == "subagent_stop":
        agent_type = data.get("agent_type", "Unknown")
        agent_id = data.get("agent_id", "Unknown")
        agent_name = data.get("agent_name", "Unknown")
        task = data.get("task", "Unknown")
        result = data.get("result", "Unknown")
        project = data.get("project", "Unknown")

        return DingTalkMessage(
            title=f"✅ {agent_name} 工作已完成",
            text=f"""### ✅ 子代理工作已完成

**📂 项目:** {project}
**🤖 代理:** {agent_name} ({agent_type})
**🆔 代理ID:** {agent_id}
**📝 任务:** {task}
**✓ 结果:** {result}

💡 {agent_name} 已完成任务，工作已结束""",
            msg_type="markdown"
        )

    elif event_type == "stop_failure":
        error = data.get("error", "Unknown error")
        project = data.get("project", "Unknown")

        return DingTalkMessage(
            title="💥 Claude Code API失败",
            text=f"""### 💥 Claude Code API调用失败

**📂 项目:** {project}
**❌ 错误信息:** ```
{error[:500]}
```

💡 Claude Code encountered an API error and had to stop""",
            msg_type="markdown"
        )

    return None
