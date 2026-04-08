"""Configuration management for Claude DingTalk Notifier"""

import os
import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class DingTalkConfig:
    """DingTalk robot configuration"""
    enabled: bool = True
    webhook: str = ""
    secret: str = ""
    msg_type: str = "markdown"  # markdown or actionCard


@dataclass
class MacOSConfig:
    """macOS system notification configuration"""
    enabled: bool = False  # 默认禁用，避免打扰
    sound: bool = True     # 是否播放声音


@dataclass
class EventConfig:
    """Event notification configuration"""
    enabled: bool = True
    channels: List[str] = field(default_factory=lambda: ["dingtalk"])


@dataclass
class Config:
    """Main configuration class"""

    config_dir: Path = field(default_factory=lambda: Path.home() / ".claude-dingtalk")
    config_file: str = "config.yaml"

    # DingTalk configuration
    dingtalk: DingTalkConfig = field(default_factory=DingTalkConfig)

    # macOS notification configuration
    macos: MacOSConfig = field(default_factory=MacOSConfig)

    # Claude Code settings.json paths
    # 默认包含开源 Claude Code 和内部 antcc 系统的配置文件
    settings_paths: List[str] = field(default_factory=lambda: [
        "~/.claude/settings.json",
        "~/.codefuse/engine/cc/settings.json"  # 内部 antcc 系统
    ])

    # Event configurations
    events: Dict[str, EventConfig] = field(default_factory=dict)

    # Sensitive operation patterns
    sensitive_operations: Dict[str, Any] = field(default_factory=lambda: {
        "patterns": [
            "sudo",
            "rm -",
            "git push",
            "docker",
            "kubectl",
            "npm publish",
        ],
        "enabled": True
    })

    def __post_init__(self):
        """Initialize default events"""
        if not self.events:
            self.events = {
                "pre_tool_use": EventConfig(enabled=True),
                "post_tool_use": EventConfig(enabled=True),
                "stop": EventConfig(enabled=True),
                "stop_failure": EventConfig(enabled=True),
                "notification": EventConfig(enabled=False),
                "session_start": EventConfig(enabled=True),
                "session_end": EventConfig(enabled=True),
                "tool_failure": EventConfig(enabled=True),
                "task_created": EventConfig(enabled=True),
                "task_completed": EventConfig(enabled=True),
                "cwd_changed": EventConfig(enabled=False),
                "config_change": EventConfig(enabled=False),
                "subagent_start": EventConfig(enabled=False),
                "subagent_stop": EventConfig(enabled=False),
            }

    @property
    def config_path(self) -> Path:
        """Get full configuration file path"""
        return self.config_dir / self.config_file

    def load(self) -> bool:
        """Load configuration from file"""
        if not self.config_path.exists():
            return False

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data:
                return False

            # Load DingTalk config
            if "dingtalk" in data:
                dt_config = data["dingtalk"]
                self.dingtalk = DingTalkConfig(
                    enabled=dt_config.get("enabled", True),
                    webhook=dt_config.get("webhook", ""),
                    secret=dt_config.get("secret", ""),
                    msg_type=dt_config.get("msg_type", "markdown")
                )

            # Load macOS config
            if "macos" in data:
                macos_config = data["macos"]
                self.macos = MacOSConfig(
                    enabled=macos_config.get("enabled", False),
                    sound=macos_config.get("sound", True)
                )

            # Load settings paths
            if "settings_paths" in data:
                self.settings_paths = data["settings_paths"]

            # Load events
            if "events" in data:
                for event_name, event_data in data["events"].items():
                    if isinstance(event_data, dict):
                        self.events[event_name] = EventConfig(
                            enabled=event_data.get("enabled", True),
                            channels=event_data.get("channels", ["dingtalk"])
                        )
                    else:
                        self.events[event_name] = EventConfig(enabled=bool(event_data))

                # Migrate old "error" event to "stop_failure"
                if "error" in self.events:
                    if "stop_failure" not in self.events:
                        self.events["stop_failure"] = self.events["error"]
                    del self.events["error"]

            # Load sensitive operations
            if "sensitive_operations" in data:
                self.sensitive_operations = data["sensitive_operations"]

            return True

        except Exception as e:
            print(f"Error loading config: {e}")
            return False

    def save(self) -> bool:
        """Save configuration to file"""
        try:
            # Create config directory if not exists
            self.config_dir.mkdir(parents=True, exist_ok=True)

            # Prepare data
            data = {
                "dingtalk": {
                    "enabled": self.dingtalk.enabled,
                    "webhook": self.dingtalk.webhook,
                    "secret": self.dingtalk.secret,
                    "msg_type": self.dingtalk.msg_type
                },
                "macos": {
                    "enabled": self.macos.enabled,
                    "sound": self.macos.sound
                },
                "settings_paths": self.settings_paths,
                "events": {
                    name: {
                        "enabled": event.enabled,
                        "channels": event.channels
                    }
                    for name, event in self.events.items()
                },
                "sensitive_operations": self.sensitive_operations
            }

            # Write to file
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

            return True

        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get_expanded_settings_paths(self) -> List[Path]:
        """Get expanded settings.json paths"""
        paths = []
        for path_str in self.settings_paths:
            path = Path(path_str).expanduser()
            if path.exists():
                paths.append(path)
        return paths

    def check_settings_paths_status(self) -> tuple[List[Path], List[str]]:
        """Check settings paths status

        Returns:
            (existing_paths, missing_paths)
            - existing_paths: List of Path objects for existing files
            - missing_paths: List of path strings for missing files
        """
        existing_paths = []
        missing_paths = []

        for path_str in self.settings_paths:
            path = Path(path_str).expanduser()
            if path.exists():
                existing_paths.append(path)
            else:
                missing_paths.append(path_str)

        return existing_paths, missing_paths

    def validate(self) -> tuple[bool, List[str]]:
        """Validate configuration"""
        errors = []

        # Check DingTalk config
        if self.dingtalk.enabled:
            if not self.dingtalk.webhook:
                errors.append("DingTalk webhook is not configured")
            if not self.dingtalk.webhook.startswith("https://oapi.dingtalk.com/"):
                errors.append("Invalid DingTalk webhook URL")

        # Check settings paths
        valid_paths = self.get_expanded_settings_paths()
        if not valid_paths:
            errors.append("No valid Claude Code settings.json paths found")

        return len(errors) == 0, errors


def get_default_config() -> Config:
    """Get default configuration instance"""
    config = Config()
    if config.config_path.exists():
        config.load()
    return config


def find_claude_settings() -> List[str]:
    """Find all Claude Code settings.json files

    包括开源 Claude Code 和内部系统（如 antcc）
    """
    default_paths = [
        "~/.claude/settings.json",           # 开源 Claude Code
        "~/.codefuse/engine/cc/settings.json",  # 内部 antcc 系统
    ]

    found_paths = []
    for path_str in default_paths:
        path = Path(path_str).expanduser()
        if path.exists():
            found_paths.append(str(path))

    return found_paths
