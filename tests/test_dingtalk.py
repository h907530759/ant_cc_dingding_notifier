"""Tests for DingTalk notification handler"""

import pytest
from unittest.mock import Mock, patch

from claude_dingtalk_notifier.dingtalk import (
    DingTalkNotifier,
    DingTalkMessage,
    format_claude_message
)


def test_dingtalk_message_creation():
    """Test creating DingTalk message"""
    message = DingTalkMessage(
        title="Test Title",
        text="Test content",
        msg_type="markdown"
    )

    assert message.title == "Test Title"
    assert message.text == "Test content"
    assert message.msg_type == "markdown"


def test_dingtalk_notifier_init():
    """Test DingTalk notifier initialization"""
    notifier = DingTalkNotifier(
        webhook="https://oapi.dingtalk.com/robot/test",
        secret="SEC123"
    )

    assert notifier.webhook == "https://oapi.dingtalk.com/robot/test"
    assert notifier.secret == "SEC123"


def test_build_url_without_secret():
    """Test building URL without secret"""
    notifier = DingTalkNotifier(
        webhook="https://oapi.dingtalk.com/robot/test"
    )

    url = notifier._build_url()
    assert url == "https://oapi.dingtalk.com/robot/test"


@patch('claude_dingtalk_notifier.dingtalk.requests.post')
def test_send_markdown(mock_post):
    """Test sending markdown message"""
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}
    mock_post.return_value = mock_response

    notifier = DingTalkNotifier(
        webhook="https://oapi.dingtalk.com/robot/test"
    )

    result = notifier.send_markdown("Test", "### Test Message")

    assert result["success"] == True
    mock_post.assert_called_once()


@patch('claude_dingtalk_notifier.dingtalk.requests.post')
def test_send_error(mock_post):
    """Test handling send error"""
    # Mock error response
    mock_response = Mock()
    mock_response.json.return_value = {"errcode": 1, "errmsg": "Error"}
    mock_post.return_value = mock_response

    notifier = DingTalkNotifier(
        webhook="https://oapi.dingtalk.com/robot/test"
    )

    result = notifier.send_markdown("Test", "Test")

    assert result["success"] == False
    assert "Error" in result["error"]


def test_format_claude_message_pre_tool_use():
    """Test formatting pre_tool_use event"""
    data = {
        "project": "test-project",
        "name": "Bash",
        "input": "sudo rm -rf /tmp/test",
        "sensitive_patterns": ["sudo", "rm -"]
    }

    message = format_claude_message("pre_tool_use", data)

    assert message is not None
    assert "敏感操作" in message.title
    assert message.msg_type == "actionCard"


def test_format_claude_message_stop():
    """Test formatting stop event"""
    data = {
        "project": "test-project",
        "time": "2026-04-03 18:00:00"
    }

    message = format_claude_message("stop", data)

    assert message is not None
    assert "任务完成" in message.title
    assert message.msg_type == "markdown"


def test_format_claude_message_post_tool_use_success():
    """Test formatting post_tool_use event (success)"""
    data = {
        "project": "test-project",
        "name": "Bash",
        "hasError": False
    }

    message = format_claude_message("post_tool_use", data)

    # Success messages are skipped
    assert message is None


def test_format_claude_message_post_tool_use_error():
    """Test formatting post_tool_use event (error)"""
    data = {
        "project": "test-project",
        "name": "Bash",
        "hasError": True
    }

    message = format_claude_message("post_tool_use", data)

    assert message is not None
    assert "执行错误" in message.title


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
