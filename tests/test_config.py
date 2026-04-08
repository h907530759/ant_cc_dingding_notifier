"""Tests for configuration management"""

import pytest
import tempfile
import json
from pathlib import Path

from claude_dingtalk_notifier.config import Config, DingTalkConfig, EventConfig


def test_config_defaults():
    """Test default configuration values"""
    config = Config()

    assert config.dingtalk.enabled == True
    assert isinstance(config.events, dict)
    assert "pre_tool_use" in config.events
    assert "post_tool_use" in config.events
    assert "stop" in config.events
    assert "notification" in config.events


def test_config_save_and_load():
    """Test saving and loading configuration"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config()
        config.config_dir = Path(tmpdir)
        config.dingtalk.webhook = "https://oapi.dingtalk.com/robot/test"
        config.dingtalk.secret = "SEC123"

        # Save
        assert config.save() == True
        assert config.config_path.exists()

        # Load
        new_config = Config()
        new_config.config_dir = Path(tmpdir)
        assert new_config.load() == True
        assert new_config.dingtalk.webhook == "https://oapi.dingtalk.com/robot/test"
        assert new_config.dingtalk.secret == "SEC123"


def test_config_validate():
    """Test configuration validation"""
    config = Config()
    config.dingtalk.webhook = "https://oapi.dingtalk.com/robot/test"

    # Valid webhook but no settings file
    is_valid, errors = config.validate()
    assert is_valid == False
    assert len(errors) > 0
    assert "No valid Claude Code settings.json paths found" in errors


def test_get_expanded_settings_paths():
    """Test expanding settings paths"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test settings file
        settings_file = Path(tmpdir) / "settings.json"
        settings_file.write_text('{}')

        config = Config()
        config.settings_paths = [str(settings_file)]

        paths = config.get_expanded_settings_paths()
        assert len(paths) == 1
        assert paths[0] == settings_file


def test_find_claude_settings():
    """Test finding Claude Code settings"""
    from claude_dingtalk_notifier.config import find_claude_settings

    # Should not crash
    paths = find_claude_settings()
    assert isinstance(paths, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
