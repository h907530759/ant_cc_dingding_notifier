"""CLI tool for Claude DingTalk Notifier"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from .config import Config, EventConfig, get_default_config, find_claude_settings
from .dingtalk import DingTalkNotifier, format_claude_message

console = Console()


def print_banner():
    """Print welcome banner"""
    banner = """
[bold cyan]╔═══════════════════════════════════════════════════════╗
║         Claude Code 钉钉通知工具 v0.2.1               ║
║         Claude Code DingTalk Notifier                  ║
╚═══════════════════════════════════════════════════════╝[/bold cyan]
"""
    rprint(banner)


@click.group()
@click.version_option(version="0.2.1")
def main():
    """Claude Code DingTalk Notifier - 钉钉机器人通知工具"""
    print_banner()


@main.command()
@click.option('--webhook', '-w', help='DingTalk webhook URL')
@click.option('--secret', '-s', help='DingTalk robot secret')
@click.option('--auto', '-a', is_flag=True, help='Auto configure with default settings')
def setup(webhook, secret, auto):
    """配置钉钉通知工具"""
    print_banner()

    config = get_default_config()

    # Auto mode: use environment variables or defaults
    if auto:
        rprint("[bold green]🚀 自动配置模式[/bold green]\n")

        # Try to get from environment
        webhook = webhook or os.getenv('DINGTALK_WEBHOOK')
        secret = secret or os.getenv('DINGTALK_SECRET')

        if webhook:
            config.dingtalk.webhook = webhook
            config.dingtalk.secret = secret or ""
            config.dingtalk.enabled = True
            rprint(f"[green]✓[/green] 从环境变量读取配置")
        else:
            rprint("[yellow]⚠[/yellow] 未检测到环境变量配置")
            webhook = Prompt.ask("请输入钉钉 Webhook URL")

    # Manual configuration
    if not webhook or not auto:
        rprint("\n[bold cyan]📱 配置钉钉机器人[/bold cyan]")

        # Input webhook
        if not webhook:
            webhook = Prompt.ask("\n请输入钉钉机器人 Webhook URL")

        config.dingtalk.webhook = webhook

        # Input secret (optional)
        if not secret:
            use_secret = Confirm.ask("钉钉机器人是否加签？", default=True)
            if use_secret:
                secret = Prompt.ask("请输入加签密钥 (SEC...)", password=True)
                config.dingtalk.secret = secret
            else:
                config.dingtalk.secret = ""

        config.dingtalk.enabled = True

    # Select events
    rprint("\n[bold cyan]🎯 选择要启用的事件类型[/bold cyan]")
    rprint("[dim]提示: 您可以选择需要启用钉钉通知的 Hook 事件[/dim]\n")

    events_table = Table(show_header=True, header_style="bold magenta")
    events_table.add_column("编号", style="cyan", width=6)
    events_table.add_column("事件", style="cyan")
    events_table.add_column("说明")
    events_table.add_column("推荐", style="yellow")

    events_info = [
        ("pre_tool_use", "preToolUse", "工具使用前触发", "检测敏感操作（sudo、rm、docker等）", "⭐ 推荐"),
        ("post_tool_use", "postToolUse", "工具使用后触发", "记录执行结果和错误", "⭐ 推荐"),
        ("stop", "stop", "停止时触发", "任务完成通知", "⭐ 推荐"),
        ("stop_failure", "stopFailure", "API失败时触发", "Claude API调用失败", "⭐ 推荐"),
        ("notification", "notification", "通知消息", "处理通知消息（权限、空闲等）", "⭐ 推荐"),
        ("session_start", "sessionStart", "会话开始", "开始新的 Claude Code 会话", "⭐ 推荐"),
        ("session_end", "sessionEnd", "会话结束", "Claude Code 会话已结束", "⭐ 推荐"),
        ("tool_failure", "postToolUseFailure", "工具失败", "工具执行失败", "⭐ 推荐"),
        ("task_created", "taskCreated", "任务创建", "新任务已创建", "⭐ 推荐"),
        ("task_completed", "taskCompleted", "任务完成", "任务已完成", "⭐ 推荐"),
        ("cwd_changed", "cwdChanged", "目录切换", "切换工作目录", "可选"),
        ("config_change", "configChange", "配置更改", "配置文件已更改", "可选"),
        ("subagent_start", "subagentStart", "子代理启动", "启动子代理", "可选"),
        ("subagent_stop", "subagentStop", "子代理完成", "子代理已完成", "可选"),
    ]

    for i, (config_key, hook_name, desc, detail, recommend) in enumerate(events_info, 1):
        events_table.add_row(str(i), hook_name, detail, recommend)

    console.print(events_table)

    rprint("\n[bold cyan]请选择要启用的事件（输入编号，用逗号分隔，如: 1,2,3,8）[/bold cyan]")
    rprint("[dim]提示: 直接回车表示启用所有推荐事件（1-8），输入 0 表示全部禁用[/dim]\n")

    choice_input = Prompt.ask("您的选择", default="1,2,3,4,5,6,7,8")

    # Parse choices
    if choice_input.strip() == "0":
        # Disable all
        for event_name in config.events:
            config.events[event_name].enabled = False
        rprint("[yellow]⚠[/yellow] 所有事件已禁用")
    elif choice_input.strip() == "" or choice_input.strip() == "1,2,3,4,5,6,7,8":
        # Default: enable recommended (1-8)
        recommended_events = ["pre_tool_use", "post_tool_use", "stop", "stop_failure",
                             "notification", "session_start", "session_end", "tool_failure"]
        for event_name in config.events:
            config.events[event_name].enabled = event_name in recommended_events
        rprint(f"[green]✓[/green] 已启用推荐事件: {', '.join(recommended_events)}")
    else:
        # Parse user input
        try:
            choices = [int(x.strip()) for x in choice_input.split(",")]

            # Reset all to disabled
            for event_name in config.events:
                config.events[event_name].enabled = False

            # Enable selected
            enabled_events = []
            for choice in choices:
                if 1 <= choice <= len(events_info):
                    config_key = events_info[choice - 1][0]
                    if config_key in config.events:
                        config.events[config_key].enabled = True
                        enabled_events.append(config_key)

            if enabled_events:
                rprint(f"[green]✓[/green] 已启用事件: {', '.join(enabled_events)}")
            else:
                rprint("[yellow]⚠[/yellow] 未选择任何事件")
        except ValueError:
            rprint("[red]✗[/red] 输入格式错误，已启用所有推荐事件")
            recommended_events = ["pre_tool_use", "post_tool_use", "stop", "stop_failure",
                                 "notification", "session_start", "session_end", "tool_failure"]
            for event_name in config.events:
                config.events[event_name].enabled = event_name in recommended_events

    # Show final selection
    rprint("\n[bold]最终配置:[/bold]")
    for event_name, event_config in config.events.items():
        status = "[green]✓ 启用[/green]" if event_config.enabled else "[dim]✗ 禁用[/dim]"
        rprint(f"  {event_name}: {status}")

    # Configure Claude Code settings paths
    rprint("\n[bold cyan]📂 配置 Claude Code settings.json 路径[/bold cyan]\n")

    # Find existing settings files
    found_paths = find_claude_settings()
    if found_paths:
        rprint("[green]发现以下 Claude Code 配置文件:[/green]")
        for i, path in enumerate(found_paths, 1):
            rprint(f"  {i}. {path}")
        rprint("")

        use_found = Confirm.ask("是否使用发现的配置文件？", default=True)
        if use_found:
            config.settings_paths = found_paths
            # Ask if user wants to add more paths
            rprint("\n")
            add_more = Confirm.ask("是否添加更多配置文件路径？", default=False)
            if add_more:
                additional_paths = _input_custom_paths()
                # Add to existing paths
                for path in additional_paths:
                    if path not in config.settings_paths:
                        config.settings_paths.append(path)
        else:
            config.settings_paths = _input_custom_paths()
    else:
        rprint("[yellow]未找到 Claude Code 配置文件[/yellow]")
        rprint("[dim]默认路径: ~/.claude/settings.json[/dim]\n")

        config.settings_paths = _input_custom_paths()

    # Show final paths
    rprint("\n[bold]已配置的 settings.json 路径:[/bold]")
    for i, path in enumerate(config.settings_paths, 1):
        rprint(f"  {i}. {path}")

    # Configure macOS notifications
    rprint("\n[bold cyan]🍎 配置 macOS 桌面通知[/bold cyan]")
    rprint("[dim]在 macOS 桌面弹出系统通知，与钉钉通知同时发送[/dim]\n")

    enable_macos = Confirm.ask("是否启用 macOS 桌面通知？", default=False)
    if enable_macos:
        config.macos.enabled = True
        use_sound = Confirm.ask("是否需要声音提醒？", default=True)
        config.macos.sound = use_sound
        rprint("[green]✓[/green] macOS 桌面通知已启用")
    else:
        config.macos.enabled = False
        rprint("[dim]✓ macOS 桌面通知已禁用[/dim]")

    # Save configuration
    rprint("\n[bold cyan]💾 保存配置[/bold cyan]\n")

    if config.save():
        rprint(f"[green]✓[/green] 配置已保存到: {config.config_path}")

        # Validate configuration
        is_valid, errors = config.validate()
        if is_valid:
            rprint("[green]✓[/green] 配置验证通过")
        else:
            rprint("[yellow]⚠[/yellow] 配置验证警告:")
            for error in errors:
                rprint(f"  - {error}")

        # Ask if install hooks
        rprint("\n")
        install_hooks = Confirm.ask("是否现在安装 Claude Code hooks？", default=True)
        if install_hooks:
            ctx = click.get_current_context()
            ctx.invoke(hooks_install)

        rprint("\n[bold green]✅ 配置完成！[/bold green]")
        rprint("\n[bold]下一步:[/bold]")
        rprint("  1. 运行 [cyan]claude-dingtalk test[/cyan] 测试通知")
        rprint("  2. 运行 [cyan]claude-dingtalk status[/cyan] 查看状态")
    else:
        rprint("[red]✗[/red] 配置保存失败")
        sys.exit(1)


def _input_custom_paths() -> list[str]:
    """Input custom settings paths"""
    paths = []

    rprint("\n[bold cyan]添加 Claude Code 配置文件路径[/bold cyan]\n")

    # Ask if user wants to add default path first
    use_default = Confirm.ask("是否添加默认路径 (~/.claude/settings.json)?", default=True)
    if use_default:
        paths.append("~/.claude/settings.json")
        rprint(f"[green]✓[/green] 已添加: ~/.claude/settings.json")

    # Add additional paths
    if paths:
        add_more = Confirm.ask("\n是否添加更多配置文件路径？", default=False)
    else:
        add_more = True

    while add_more:
        rprint("\n[dim]提示: 可以输入项目特定的 settings.json 路径[/dim]")
        rprint("[dim]例如: ~/work/project1/.claude/settings.json[/dim]\n")

        custom_path = Prompt.ask("请输入配置文件路径")

        # Validate path
        expanded_path = Path(custom_path).expanduser()
        if expanded_path.exists():
            if custom_path not in paths:
                paths.append(custom_path)
                rprint(f"[green]✓[/green] 已添加: {custom_path}")
            else:
                rprint(f"[yellow]⚠[/yellow] 路径已存在: {custom_path}")
        else:
            rprint(f"[yellow]⚠[/yellow] 警告: 路径不存在: {custom_path}")
            use_anyway = Confirm.ask("是否仍要添加此路径？", default=False)
            if use_anyway and custom_path not in paths:
                paths.append(custom_path)
                rprint(f"[green]✓[/green] 已添加: {custom_path}")

        if len(paths) > 0:
            rprint(f"\n[bold]当前已添加 {len(paths)} 个路径:[/bold]")
            for i, path in enumerate(paths, 1):
                rprint(f"  {i}. {path}")

        add_more = Confirm.ask("\n是否继续添加？", default=False)

    # Ensure at least one path
    if not paths:
        rprint("[yellow]⚠[/yellow] 未添加任何路径，使用默认路径")
        paths.append("~/.claude/settings.json")

    return paths


@main.command()
def test():
    """测试钉钉通知"""
    config = get_default_config()

    if not config.dingtalk.enabled:
        rprint("[red]✗[/red] 钉钉通知未启用，请先运行配置")
        return

    rprint("[bold cyan]🧪 测试钉钉通知[/bold cyan]\n")

    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    rprint("发送测试消息...")
    result = notifier.test_connection()

    if result.get("success"):
        rprint("[green]✓[/green] 测试成功！请检查钉钉群消息")
    else:
        rprint(f"[red]✗[/red] 测试失败: {result.get('error', 'Unknown error')}")


@main.command()
def status():
    """查看配置状态"""
    config = get_default_config()

    rprint("[bold cyan]📊 配置状态[/bold cyan]\n")

    # DingTalk configuration
    dt_table = Table(show_header=True, header_style="bold magenta")
    dt_table.add_column("配置项", style="cyan")
    dt_table.add_column("值")

    status = "✓ 启用" if config.dingtalk.enabled else "✗ 禁用"
    webhook_status = config.dingtalk.webhook[:50] + "..." if len(config.dingtalk.webhook) > 50 else config.dingtalk.webhook
    secret_status = "✓ 已配置" if config.dingtalk.secret else "✗ 未配置"

    dt_table.add_row("状态", status)
    dt_table.add_row("Webhook", webhook_status)
    dt_table.add_row("加签密钥", secret_status)

    console.print(dt_table)

    # Events configuration
    rprint("\n[bold]事件配置:[/bold]\n")

    events_table = Table(show_header=True, header_style="bold magenta")
    events_table.add_column("事件", style="cyan")
    events_table.add_column("状态")

    for event_name, event_config in config.events.items():
        status = "✓ 启用" if event_config.enabled else "✗ 禁用"
        events_table.add_row(event_name, status)

    console.print(events_table)

    # Settings paths
    rprint("\n[bold]Claude Code 配置文件:[/bold]\n")

    paths = config.get_expanded_settings_paths()
    if paths:
        for i, path in enumerate(paths, 1):
            rprint(f"  {i}. {path}")
    else:
        rprint("  [yellow]未找到有效配置文件[/yellow]")

    # Validation
    is_valid, errors = config.validate()
    rprint("\n[bold]配置验证:[/bold]\n")

    if is_valid:
        rprint("[green]✓[/green] 配置有效")
    else:
        rprint("[red]✗[/red] 配置存在问题:")
        for error in errors:
            rprint(f"  - {error}")


@main.command()
@click.argument('message', required=False)
def send(message):
    """发送自定义消息"""
    if not message:
        message = Prompt.ask("请输入消息内容")

    config = get_default_config()

    if not config.dingtalk.enabled:
        rprint("[red]✗[/red] 钉钉通知未启用")
        return

    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    result = notifier.send_markdown("📨 自定义消息", message)

    if result.get("success"):
        rprint("[green]✓[/green] 消息发送成功")
    else:
        rprint(f"[red]✗[/red] 发送失败: {result.get('error', 'Unknown error')}")


@main.group()
def hooks():
    """Hook 管理命令"""
    pass


@hooks.command('install')
def hooks_install():
    """安装 Claude Code hooks"""
    config = get_default_config()
    rprint("[bold cyan]🔧 安装 Claude Code Hooks[/bold cyan]\n")

    # Get hook directory
    hook_dir = config.config_dir / "hooks"
    hook_dir.mkdir(parents=True, exist_ok=True)

    # Generate hook scripts (only for enabled events)
    enabled_hooks = {}
    event_mapping = {
        "pre_tool_use": "PreToolUse",
        "post_tool_use": "PostToolUse",
        "tool_failure": "PostToolUseFailure",
        "stop": "Stop",
        "stop_failure": "StopFailure",
        "notification": "Notification",
        "session_start": "SessionStart",
        "session_end": "SessionEnd",
        "task_created": "TaskCreated",
        "task_completed": "TaskCompleted",
        "cwd_changed": "CwdChanged",
        "config_change": "ConfigChange",
        "subagent_start": "SubagentStart",
        "subagent_stop": "SubagentStop",
    }

    for event_key, hook_event_name in event_mapping.items():
        if config.events.get(event_key, EventConfig()).enabled:
            hook_script = str(hook_dir / f"{event_key}.py")
            # Use correct Claude Code hooks format: array of objects with "hooks" field
            enabled_hooks[hook_event_name] = [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_script
                        }
                    ]
                }
            ]

    # Create hook scripts (only for enabled events)
    _create_hook_scripts(hook_dir, config)

    # Check settings paths status
    existing_paths, missing_paths = config.check_settings_paths_status()

    # Show warnings for missing files
    if missing_paths:
        rprint("\n[yellow]⚠️  以下配置文件不存在，将跳过:[/yellow]")
        for path_str in missing_paths:
            rprint(f"  [dim]  - {path_str}[/dim]")
        rprint("")

    if not existing_paths:
        rprint("[yellow]⚠[/yellow] 未找到有效的 settings.json 文件")
        rprint("[dim]请先运行 setup 命令配置文件路径[/dim]")
        return

    rprint(f"[bold]将处理 {len(existing_paths)} 个配置文件[/bold]\n")

    for settings_path in existing_paths:
        rprint(f"处理配置文件: {settings_path}")

        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
        except Exception as e:
            rprint(f"  [red]✗[/red] 读取失败: {e}")
            continue

        # Add hooks configuration
        if "hooks" not in settings_data:
            settings_data["hooks"] = {}

        # Remove old format hooks (simple string values) and keep only new format (array values)
        hooks_to_remove = [k for k, v in settings_data["hooks"].items() if isinstance(v, str)]
        for hook_name in hooks_to_remove:
            del settings_data["hooks"][hook_name]

        # Add new hooks in correct format
        settings_data["hooks"].update(enabled_hooks)

        # Backup and save
        backup_path = settings_path.with_suffix('.json.backup')
        try:
            # Backup
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)

            # Save
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)

            rprint(f"  [green]✓[/green] Hooks 已安装 (备份: {backup_path.name})")

        except Exception as e:
            rprint(f"  [red]✗[/red] 保存失败: {e}")

    rprint("\n[bold green]✅ Hooks 安装完成！[/bold green]")
    rprint("\n[bold]已安装的 Hooks:[/bold]")
    for hook_name, hook_config in enabled_hooks.items():
        # Extract the command path from the nested structure
        if hook_config and len(hook_config) > 0:
            hooks_array = hook_config[0].get("hooks", [])
            if hooks_array and len(hooks_array) > 0:
                command_path = hooks_array[0].get("command", "未知")
                rprint(f"  - {hook_name}: {command_path}")


def _create_hook_scripts(hook_dir: Path, config: Config):
    """Create hook scripts"""

    # Get package source path for imports
    try:
        import claude_dingtalk_notifier
        # Get the src directory containing the package
        package_source_path = Path(claude_dingtalk_notifier.__file__).parent.parent
    except (ImportError, AttributeError):
        # Fallback: try to find src directory relative to hook dir
        # Hook dir is ~/.claude-dingtalk/hooks, so we go up to find the project
        package_source_path = hook_dir.parent.parent / "workspace" / "claude_notifyer" / "src"

        # If that doesn't exist, try another common location
        if not package_source_path.exists():
            # Try current directory's src
            import os
            cwd = Path(os.getcwd())
            for parent in [cwd] + list(cwd.parents):
                candidate = parent / "src"
                if candidate.exists() and (candidate / "claude_dingtalk_notifier").exists():
                    package_source_path = candidate
                    break

    # Common imports and setup
    common_header = f'''#!/usr/bin/env python3
"""
Claude Code Hook for DingTalk Notification
"""

import sys
import json
from pathlib import Path

# Add package source to path
package_path = Path(r"{package_source_path}")
if package_path.exists():
    sys.path.insert(0, str(package_path))

try:
    from claude_dingtalk_notifier.config import get_default_config, EventConfig
    from claude_dingtalk_notifier.dingtalk import DingTalkNotifier, format_claude_message, DingTalkMessage
    from claude_dingtalk_notifier.macos_notifier import MacOSNotifier
    from claude_dingtalk_notifier.logger import get_logger
except ImportError as e:
    # If import fails, exit gracefully to avoid breaking Claude Code
    print(f"Warning: Could not import claude_dingtalk_notifier: {{e}}", file=sys.stderr)
    sys.exit(0)

'''

    # PreToolUse hook
    pre_tool_hook = common_header + '''def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Load config
    config = get_default_config()

    event_config = config.events.get("pre_tool_use", EventConfig())
    if not event_config.enabled:
        json.dump({"authorized": True}, sys.stdout)
        return

    # Check for sensitive operations
    tool_name = input_data.get("name", "")
    tool_input = input_data.get("input", {})
    sensitive_patterns = config.sensitive_operations.get("patterns", [])

    is_sensitive = any(
        pattern in str(tool_input).lower()
        for pattern in sensitive_patterns
    )

    if is_sensitive:
        # Send DingTalk notification
        if config.dingtalk.enabled:
            notifier = DingTalkNotifier(
                webhook=config.dingtalk.webhook,
                secret=config.dingtalk.secret
            )

            message_data = {
                "project": project,
                "name": tool_name,
                "input": tool_input,
                "sensitive_patterns": sensitive_patterns
            }

            message = format_claude_message("pre_tool_use", message_data)
            if message:
                notifier.send(message)

        # Send macOS notification
        if config.macos.enabled:
            macos_notifier = MacOSNotifier(
                enabled=config.macos.enabled,
                sound=config.macos.sound
            )
            project_name = Path(project).name if project != "Unknown" else project
            macos_notifier.send(
                title=f"{project_name} - 敏感操作",
                message=f"即将执行: {tool_name}"
            )

    # Always allow
    json.dump({"authorized": True}, sys.stdout)

if __name__ == "__main__":
    main()
'''

    # PostToolUse hook
    post_tool_hook = common_header + '''def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Load config
    config = get_default_config()

    if not config.dingtalk.enabled or not config.events.get("post_tool_use", EventConfig()).enabled:
        return

    # Check for errors
    has_error = input_data.get("hasError", False)
    tool_name = input_data.get("name", "")

    if has_error:
        # Send error notification
        notifier = DingTalkNotifier(
            webhook=config.dingtalk.webhook,
            secret=config.dingtalk.secret
        )

        message_data = {
            "project": project,
            "name": tool_name,
            "hasError": has_error
        }

        message = format_claude_message("post_tool_use", message_data)
        if message:
            notifier.send(message)

if __name__ == "__main__":
    main()
'''

    # PostToolUseFailure hook
    tool_failure_hook = common_header + '''def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Load config
    config = get_default_config()

    if not config.dingtalk.enabled or not config.events.get("tool_failure", EventConfig()).enabled:
        return

    # Send failure notification
    tool_name = input_data.get("name", "")
    error = input_data.get("error", "Unknown error")

    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    message_data = {
        "project": project,
        "name": tool_name,
        "error": error
    }

    message = format_claude_message("tool_failure", message_data)
    if message:
        notifier.send(message)

if __name__ == "__main__":
    main()
'''

    # Stop hook
    stop_hook = common_header + '''from datetime import datetime

def main():
    hook_name = "stop"

    # Initialize logger
    logger = get_logger()
    logger.log_hook_start(hook_name)

    try:
        # Read input from stdin (Stop hook may provide data)
        try:
            input_data = json.load(sys.stdin)
            project = input_data.get("cwd", "Unknown")
        except:
            # If no stdin data, use current directory
            project = str(Path.cwd().name)

        # Load config
        config = get_default_config()

        event_config = config.events.get("stop", EventConfig())
        if not event_config.enabled:
            logger.debug(f"{hook_name} hook is disabled")
            return

        # Send DingTalk notification
        if config.dingtalk.enabled:
            logger.log_channel_trigger(hook_name, "dingtalk")
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
                result = notifier.send(message)

                if result.get("success"):
                    logger.log_hook_success(hook_name, "All notifications sent successfully")
                else:
                    logger.log_hook_error(
                        hook_name,
                        Exception(result.get("error", "Unknown error")),
                        "Failed to send DingTalk notification"
                    )

        # Send macOS notification
        if config.macos.enabled:
            logger.log_channel_trigger(hook_name, "macOS-notifier")
            macos_notifier = MacOSNotifier(
                enabled=config.macos.enabled,
                sound=config.macos.sound,
                logger=logger
            )
            project_name = Path(project).name if project != "Unknown" else project
            macos_notifier.send(
                title=f"{project_name} - 任务完成",
                message="所有任务已完成"
            )

    except Exception as e:
        logger.log_hook_error(hook_name, e, "Unexpected error in hook execution")
        # Don't raise - hook failures shouldn't break Claude Code
        sys.exit(0)

if __name__ == "__main__":
    main()
'''

    # SessionStart hook
    session_start_hook = common_header + '''from datetime import datetime

def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Load config
    config = get_default_config()

    event_config = config.events.get("session_start", EventConfig())
    if not event_config.enabled:
        return

    # Send DingTalk notification
    if config.dingtalk.enabled:
        notifier = DingTalkNotifier(
            webhook=config.dingtalk.webhook,
            secret=config.dingtalk.secret
        )

        message_data = {
            "project": project,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        message = format_claude_message("session_start", message_data)
        if message:
            notifier.send(message)

    # Send macOS notification
    if config.macos.enabled:
        macos_notifier = MacOSNotifier(
            enabled=config.macos.enabled,
            sound=config.macos.sound
        )
        # Extract project name from path for cleaner display
        project_name = Path(project).name if project != "Unknown" else project
        macos_notifier.send(
            title=f"{project_name} - 会话已启动",
            message="Claude Code 新会话已启动"
        )

if __name__ == "__main__":
    main()
'''

    # SessionEnd hook
    session_end_hook = common_header + '''from datetime import datetime

def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Load config
    config = get_default_config()

    if not config.dingtalk.enabled or not config.events.get("session_end", EventConfig()).enabled:
        return

    # Send session end notification
    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    message_data = {
        "project": project,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    message = format_claude_message("session_end", message_data)
    if message:
        notifier.send(message)

if __name__ == "__main__":
    main()
'''

    # TaskCreated hook
    task_created_hook = common_header + '''def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Load config
    config = get_default_config()

    if not config.dingtalk.enabled or not config.events.get("task_created", EventConfig()).enabled:
        return

    # Get task info
    task_id = input_data.get("taskId", "")
    subject = input_data.get("subject", "Unknown task")

    # Send task created notification
    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    message_data = {
        "project": project,
        "task_id": task_id,
        "subject": subject
    }

    message = format_claude_message("task_created", message_data)
    if message:
        notifier.send(message)

if __name__ == "__main__":
    main()
'''

    # TaskCompleted hook
    task_completed_hook = common_header + '''def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Load config
    config = get_default_config()

    if not config.dingtalk.enabled or not config.events.get("task_completed", EventConfig()).enabled:
        return

    # Get task info
    task_id = input_data.get("taskId", "")
    subject = input_data.get("subject", "Unknown task")

    # Send task completed notification
    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    message_data = {
        "project": project,
        "task_id": task_id,
        "subject": subject
    }

    message = format_claude_message("task_completed", message_data)
    if message:
        notifier.send(message)

if __name__ == "__main__":
    main()
'''

    # CwdChanged hook
    cwd_changed_hook = common_header + '''def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get directories
    old_cwd = input_data.get("oldCwd", "Unknown")
    new_cwd = input_data.get("newCwd", "Unknown")

    # Load config
    config = get_default_config()

    if not config.dingtalk.enabled or not config.events.get("cwd_changed", EventConfig()).enabled:
        return

    # Send directory changed notification
    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    message_data = {
        "old_cwd": old_cwd,
        "new_cwd": new_cwd
    }

    message = format_claude_message("cwd_changed", message_data)
    if message:
        notifier.send(message)

if __name__ == "__main__":
    main()
'''

    # ConfigChange hook
    config_change_hook = common_header + '''def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Get config file path
    config_path = input_data.get("path", "Unknown")

    # Get change type (may not exist in older versions)
    change_type = input_data.get("changeType", "modified")
    change_type_map = {
        "created": "创建",
        "modified": "修改",
        "deleted": "删除"
    }
    change_type_text = change_type_map.get(change_type, "修改")

    # Load config
    config = get_default_config()

    if not config.dingtalk.enabled or not config.events.get("config_change", EventConfig()).enabled:
        return

    # Send config change notification
    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    message_data = {
        "project": project,
        "config_path": config_path,
        "change_type": change_type_text
    }

    message = format_claude_message("config_change", message_data)
    if message:
        notifier.send(message)

if __name__ == "__main__":
    main()
'''

    # SubagentStart hook
    subagent_start_hook = common_header + '''def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Get subagent info
    agent_type = input_data.get("subagentType", "Unknown")
    agent_id = input_data.get("subagentId", "Unknown")
    agent_name = input_data.get("subagentName", "Unknown")

    # Get task description (may not exist in older versions)
    task = input_data.get("task", f"{agent_name}任务")

    # Load config
    config = get_default_config()

    if not config.dingtalk.enabled or not config.events.get("subagent_start", EventConfig()).enabled:
        return

    # Send subagent start notification
    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    message_data = {
        "project": project,
        "agent_type": agent_type,
        "agent_id": agent_id,
        "agent_name": agent_name,
        "task": task
    }

    message = format_claude_message("subagent_start", message_data)
    if message:
        notifier.send(message)

if __name__ == "__main__":
    main()
'''

    # SubagentStop hook
    subagent_stop_hook = common_header + '''def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Get subagent info
    agent_type = input_data.get("subagentType", "Unknown")
    agent_id = input_data.get("subagentId", "Unknown")
    agent_name = input_data.get("subagentName", "Unknown")

    # Get task and result (may not exist in older versions)
    task = input_data.get("task", f"{agent_name}任务")
    result = input_data.get("result", "已完成")

    # Load config
    config = get_default_config()

    if not config.dingtalk.enabled or not config.events.get("subagent_stop", EventConfig()).enabled:
        return

    # Send subagent stop notification
    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    message_data = {
        "project": project,
        "agent_type": agent_type,
        "agent_id": agent_id,
        "agent_name": agent_name,
        "task": task,
        "result": result
    }

    message = format_claude_message("subagent_stop", message_data)
    if message:
        notifier.send(message)

if __name__ == "__main__":
    main()
'''

    # StopFailure hook
    stop_failure_hook = common_header + '''def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Get project name
    project = input_data.get("cwd", "Unknown")

    # Load config
    config = get_default_config()

    if not config.dingtalk.enabled or not config.events.get("stop_failure", EventConfig()).enabled:
        return

    # Get error info
    error = input_data.get("error", "Unknown error")

    # Send stop failure notification
    notifier = DingTalkNotifier(
        webhook=config.dingtalk.webhook,
        secret=config.dingtalk.secret
    )

    message_data = {
        "project": project,
        "error": error
    }

    message = format_claude_message("stop_failure", message_data)
    if message:
        notifier.send(message)

if __name__ == "__main__":
    main()
'''

    # Write hooks
    hooks = {
        "pre_tool_use.py": pre_tool_hook,
        "post_tool_use.py": post_tool_hook,
        "tool_failure.py": tool_failure_hook,
        "stop.py": stop_hook,
        "stop_failure.py": stop_failure_hook,
        "session_start.py": session_start_hook,
        "session_end.py": session_end_hook,
        "task_created.py": task_created_hook,
        "task_completed.py": task_completed_hook,
        "cwd_changed.py": cwd_changed_hook,
        "config_change.py": config_change_hook,
        "subagent_start.py": subagent_start_hook,
        "subagent_stop.py": subagent_stop_hook,
    }

    for hook_name, hook_content in hooks.items():
        hook_path = hook_dir / hook_name
        with open(hook_path, 'w', encoding='utf-8') as f:
            f.write(hook_content)
        # Make executable
        hook_path.chmod(0o755)


@hooks.command('uninstall')
@click.option('--settings', type=click.Path(exists=True), help='指定要操作的 settings.json 文件路径')
@click.option('--all', is_flag=True, help='卸载所有配置文件中的 hooks')
def hooks_uninstall(settings, all):
    """卸载 Claude Code hooks

    默认会提示选择要卸载的配置文件，或使用 --all 卸载所有文件
    """
    config = get_default_config()
    rprint("[bold cyan]🔧 卸载 Claude Code Hooks[/bold cyan]\n")

    # Determine which settings files to process
    if settings:
        # User specified a specific file
        settings_paths = [Path(settings)]
        rprint(f"[dim]指定文件: {settings}[/dim]\n")
    elif all:
        # Uninstall from all files
        existing_paths, missing_paths = config.check_settings_paths_status()

        # Show warnings for missing files
        if missing_paths:
            rprint("\n[yellow]⚠️  以下配置文件不存在，将跳过:[/yellow]")
            for path_str in missing_paths:
                rprint(f"  [dim]  - {path_str}[/dim]")
            rprint("")

        if not existing_paths:
            rprint("[yellow]⚠[/yellow] 未找到有效的 settings.json 文件")
            return

        settings_paths = existing_paths
        rprint(f"[dim]卸载所有配置文件中的 hooks ({len(settings_paths)} 个文件)[/dim]\n")
    else:
        # Interactive selection
        existing_paths, missing_paths = config.check_settings_paths_status()

        # Show warnings for missing files
        if missing_paths:
            rprint("\n[yellow]⚠️  以下配置文件不存在，将跳过:[/yellow]")
            for path_str in missing_paths:
                rprint(f"  [dim]  - {path_str}[/dim]")
            rprint("")

        if not existing_paths:
            rprint("[yellow]⚠[/yellow] 未找到有效的 settings.json 文件")
            return

        all_settings_paths = existing_paths

        rprint("[bold]请选择要卸载 Hooks 的配置文件:[/bold]\n")
        for i, path in enumerate(all_settings_paths, 1):
            rprint(f"  {i}. {path}")
        rprint(f"  {len(all_settings_paths) + 1}. [bold]所有文件[/bold]")
        rprint(f"  0. [dim]取消[/dim]\n")

        choice = Prompt.ask(
            "请输入选项",
            choices=[str(i) for i in range(len(all_settings_paths) + 2)],
            show_default=False
        )

        choice = int(choice)

        if choice == 0:
            rprint("[yellow]⚠[/yellow] 已取消")
            return
        elif choice == len(all_settings_paths) + 1:
            settings_paths = all_settings_paths
            rprint("[dim]选择: 所有文件[/dim]\n")
        else:
            settings_paths = [all_settings_paths[choice - 1]]
            rprint(f"[dim]选择: {settings_paths[0]}[/dim]\n")

    if not settings_paths:
        rprint("[yellow]⚠[/yellow] 未找到有效的 settings.json 文件")
        return

    for settings_path in settings_paths:
        rprint(f"处理配置文件: {settings_path}")

        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
        except Exception as e:
            rprint(f"  [red]✗[/red] 读取失败: {e}")
            continue

        # Remove only claude-dingtalk hooks (preserve other apps' hooks)
        if "hooks" in settings_data:
            removed_count = 0
            hooks_to_remove = []

            # Find all claude-dingtalk hooks
            for hook_name, hook_configs in settings_data["hooks"].items():
                if not isinstance(hook_configs, list):
                    continue

                # Check if any of the hook configs belong to claude-dingtalk
                for hook_config in hook_configs:
                    if not isinstance(hook_config, dict):
                        continue

                    hook_list = hook_config.get("hooks", [])
                    if not isinstance(hook_list, list):
                        continue

                    # Check if command path contains .claude-dingtalk
                    for hook_item in hook_list:
                        if isinstance(hook_item, dict):
                            command = hook_item.get("command", "")
                            if ".claude-dingtalk/hooks/" in command:
                                hooks_to_remove.append(hook_name)
                                removed_count += 1
                                break
                    if hook_name in hooks_to_remove:
                        break

            # Remove identified hooks
            for hook_name in hooks_to_remove:
                del settings_data["hooks"][hook_name]

            # Clean up empty hooks object if no hooks left
            if len(settings_data["hooks"]) == 0:
                del settings_data["hooks"]

            # Backup and save if we made changes
            if removed_count > 0:
                backup_path = settings_path.with_suffix('.json.backup')
                try:
                    # Backup
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        json.dump(settings_data, f, indent=2, ensure_ascii=False)

                    # Save
                    with open(settings_path, 'w', encoding='utf-8') as f:
                        json.dump(settings_data, f, indent=2, ensure_ascii=False)

                    rprint(f"  [green]✓[/green] 已删除 {removed_count} 个 claude-dingtalk hooks (备份: {backup_path.name})")

                except Exception as e:
                    rprint(f"  [red]✗[/red] 保存失败: {e}")
            else:
                rprint(f"  [dim]−[/dim] 未找到 claude-dingtalk hooks")
        else:
            rprint(f"  [dim]−[/dim] 未安装 hooks")

    rprint("\n[bold green]✅ Hooks 卸载完成！[/bold green]")


@hooks.command('remove')
@click.argument('hook_name')
@click.option('--delete-script', is_flag=True, help='同时删除 hook 脚本文件')
@click.option('--settings', type=click.Path(exists=True), help='指定要操作的 settings.json 文件路径')
@click.option('--all', is_flag=True, help='从所有配置文件中删除此 hook')
def hooks_remove(hook_name, delete_script, settings, all):
    """删除单个 Hook

    HOOK_NAME: 要删除的 Hook 名称 (如: PreToolUse, Stop, SessionEnd)

    默认会提示选择要操作的配置文件，或使用 --all 操作所有文件
    """
    config = get_default_config()
    rprint(f"[bold cyan]🗑️  删除 Hook: {hook_name}[/bold cyan]\n")

    # Determine which settings files to process
    if settings:
        # User specified a specific file
        settings_paths = [Path(settings)]
        rprint(f"[dim]指定文件: {settings}[/dim]\n")
    elif all:
        # Remove from all files
        existing_paths, missing_paths = config.check_settings_paths_status()

        # Show warnings for missing files
        if missing_paths:
            rprint("\n[yellow]⚠️  以下配置文件不存在，将跳过:[/yellow]")
            for path_str in missing_paths:
                rprint(f"  [dim]  - {path_str}[/dim]")
            rprint("")

        if not existing_paths:
            rprint("[yellow]⚠[/yellow] 未找到有效的 settings.json 文件")
            return

        settings_paths = existing_paths
        rprint(f"[dim]从所有配置文件中删除 ({len(settings_paths)} 个文件)[/dim]\n")
    else:
        # Interactive selection
        existing_paths, missing_paths = config.check_settings_paths_status()

        # Show warnings for missing files
        if missing_paths:
            rprint("\n[yellow]⚠️  以下配置文件不存在，将跳过:[/yellow]")
            for path_str in missing_paths:
                rprint(f"  [dim]  - {path_str}[/dim]")
            rprint("")

        if not existing_paths:
            rprint("[yellow]⚠[/yellow] 未找到有效的 settings.json 文件")
            return

        all_settings_paths = existing_paths

    # Map hook name to event key
    hook_to_event = {
        "PreToolUse": "pre_tool_use",
        "PostToolUse": "post_tool_use",
        "PostToolUseFailure": "tool_failure",
        "Stop": "stop",
        "StopFailure": "stop_failure",
        "Notification": "notification",
        "SessionStart": "session_start",
        "SessionEnd": "session_end",
        "TaskCreated": "task_created",
        "TaskCompleted": "task_completed",
        "CwdChanged": "cwd_changed",
        "ConfigChange": "config_change",
        "SubagentStart": "subagent_start",
        "SubagentStop": "subagent_stop",
    }

    if hook_name not in hook_to_event:
        rprint(f"[red]✗[/red] 未知的 Hook 名称: {hook_name}")
        rprint("\n[bold]可用的 Hook 名称:[/bold]")
        for name in sorted(hook_to_event.keys()):
            rprint(f"  - {name}")
        return

    event_key = hook_to_event[hook_name]
    removed_count = 0

    for settings_path in settings_paths:
        rprint(f"处理配置文件: {settings_path}")

        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
        except Exception as e:
            rprint(f"  [red]✗[/red] 读取失败: {e}")
            continue

        # Remove specific hook (only claude-dingtalk's, preserve other apps')
        if "hooks" in settings_data and hook_name in settings_data["hooks"]:
            hook_configs = settings_data["hooks"][hook_name]
            made_changes = False

            # Check if this hook has multiple sources (claude-dingtalk + other apps)
            if isinstance(hook_configs, list) and len(hook_configs) > 1:
                # Multiple hook sources, filter out only claude-dingtalk
                filtered_configs = []
                for hook_config in hook_configs:
                    if not isinstance(hook_config, dict):
                        filtered_configs.append(hook_config)
                        continue

                    hook_list = hook_config.get("hooks", [])
                    if not isinstance(hook_list, list):
                        filtered_configs.append(hook_config)
                        continue

                    # Check if this is a claude-dingtalk hook
                    is_claude_dingtalk = False
                    for hook_item in hook_list:
                        if isinstance(hook_item, dict):
                            command = hook_item.get("command", "")
                            if ".claude-dingtalk/hooks/" in command:
                                is_claude_dingtalk = True
                                break

                    # Only keep non-claude-dingtalk hooks
                    if not is_claude_dingtalk:
                        filtered_configs.append(hook_config)

                # Update with filtered configs
                if len(filtered_configs) > 0:
                    settings_data["hooks"][hook_name] = filtered_configs
                    rprint(f"  [green]✓[/green] 已删除 claude-dingtalk 的 {hook_name} hook (保留其他应用的 hook)")
                    removed_count += 1
                    made_changes = True
                else:
                    # No hooks left, remove the entire entry
                    del settings_data["hooks"][hook_name]
                    rprint(f"  [green]✓[/green] 已删除 {hook_name} hook")
                    removed_count += 1
                    made_changes = True
            else:
                # Single hook or simple structure, safe to delete
                del settings_data["hooks"][hook_name]
                rprint(f"  [green]✓[/green] Hook 已删除")
                removed_count += 1
                made_changes = True

            # Backup and save if we made changes
            if made_changes:
                backup_path = settings_path.with_suffix('.json.backup')
                try:
                    # Backup
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        json.dump(settings_data, f, indent=2, ensure_ascii=False)

                    # Save
                    with open(settings_path, 'w', encoding='utf-8') as f:
                        json.dump(settings_data, f, indent=2, ensure_ascii=False)

                except Exception as e:
                    rprint(f"  [red]✗[/red] 保存失败: {e}")
        else:
            rprint(f"  [dim]−[/dim] 未找到此 Hook")

    # Delete hook script if requested
    if delete_script:
        hook_script = config.config_dir / "hooks" / f"{event_key}.py"
        if hook_script.exists():
            try:
                hook_script.unlink()
                rprint(f"\n[green]✓[/green] Hook 脚本已删除: {hook_script}")
            except Exception as e:
                rprint(f"\n[red]✗[/red] 删除脚本失败: {e}")
        else:
            rprint(f"\n[dim]−[/dim] Hook 脚本不存在: {hook_script}")

    if removed_count > 0:
        rprint(f"\n[bold green]✅ 成功从 {removed_count} 个配置文件中删除 Hook[/bold green]")
    else:
        rprint("\n[yellow]⚠[/yellow] 未删除任何 Hook")


@hooks.command('list')
def hooks_list():
    """列出所有可用的 Hooks"""
    config = get_default_config()
    rprint("[bold cyan]📋 可用的 Hooks 列表[/bold cyan]\n")

    all_hooks = [
        ("SessionStart", "session_start", "会话开始时触发"),
        ("SessionEnd", "session_end", "会话结束时触发"),
        ("PreToolUse", "pre_tool_use", "工具使用前触发"),
        ("PostToolUse", "post_tool_use", "工具使用后触发"),
        ("PostToolUseFailure", "tool_failure", "工具执行失败时触发"),
        ("Stop", "stop", "Claude 停止时触发"),
        ("StopFailure", "stop_failure", "API 失败时触发"),
        ("Notification", "notification", "通知消息"),
        ("TaskCreated", "task_created", "任务创建时触发"),
        ("TaskCompleted", "task_completed", "任务完成时触发"),
        ("CwdChanged", "cwd_changed", "目录切换时触发"),
        ("ConfigChange", "config_change", "配置更改时触发"),
        ("SubagentStart", "subagent_start", "子代理启动时触发"),
        ("SubagentStop", "subagent_stop", "子代理完成时触发"),
    ]

    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Hook 名称", style="cyan", width=20)
    table.add_column("事件标识", style="green", width=20)
    table.add_column("说明", style="white", width=30)
    table.add_column("状态", width=10)

    for hook_name, event_key, description in all_hooks:
        # Check if enabled
        is_enabled = config.events.get(event_key, EventConfig()).enabled
        status = "[green]✓ 启用[/green]" if is_enabled else "[dim]✗ 禁用[/dim]"
        table.add_row(hook_name, event_key, description, status)

    console.print(table)

    # Show hook script files
    rprint("\n[bold]Hook 脚本文件:[/bold]")
    hook_dir = config.config_dir / "hooks"
    if hook_dir.exists():
        for hook_file in sorted(hook_dir.glob("*.py")):
            rprint(f"  [green]✓[/green] {hook_file.name}")
    else:
        rprint("  [dim]−[/dim] Hook 目录不存在")


@hooks.command('status')
def hooks_status():
    """查看 Hooks 状态"""
    config = get_default_config()
    rprint("[bold cyan]📊 Hooks 状态[/bold cyan]\n")

    # Check settings paths status
    existing_paths, missing_paths = config.check_settings_paths_status()

    # Show warnings for missing files
    if missing_paths:
        rprint("[yellow]⚠️  以下配置文件不存在:[/yellow]")
        for path_str in missing_paths:
            rprint(f"  [dim]  - {path_str}[/dim]")
        rprint("")

    if not existing_paths:
        rprint("[yellow]⚠[/yellow] 未找到有效的 settings.json 文件")
        return

    for settings_path in existing_paths:
        rprint(f"[bold]配置文件:[/bold] {settings_path}")

        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
        except Exception as e:
            rprint(f"  [red]✗[/red] 读取失败: {e}\n")
            continue

        hooks = settings_data.get("hooks", {})
        if hooks:
            rprint("  [green]✓[/green] 已安装 Hooks:")
            for hook_name, hook_path in hooks.items():
                rprint(f"    - {hook_name}: {hook_path}")
        else:
            rprint("  [dim]−[/dim] 未安装 Hooks")
        rprint("")


@hooks.command('logs')
@click.option('--lines', '-n', default=50, help='显示最后 N 行日志')
@click.option('--follow', '-f', is_flag=True, help='实时跟踪日志')
@click.option('--all', '-a', is_flag=True, help='显示所有日志')
def hooks_logs(lines, follow, all):
    """查看 Hook 执行日志"""
    import subprocess

    config = get_default_config()
    log_file = config.config_dir / "hook.log"

    if not log_file.exists():
        rprint("[yellow]⚠[/yellow] 日志文件不存在")
        rprint(f"[dim]日志路径: {log_file}[/dim]")
        return

    rprint(f"[bold cyan]📋 Hook 执行日志[/bold cyan]\n")
    rprint(f"[dim]日志文件: {log_file}[/dim]\n")

    if follow:
        # Follow mode (like tail -f)
        rprint("[bold green]实时跟踪模式 (Ctrl+C 退出)[/bold green]\n")
        try:
            # Use tail -f command
            subprocess.run(['tail', '-f', str(log_file)], check=False)
        except KeyboardInterrupt:
            rprint("\n\n[dim]已停止跟踪日志[/dim]")
    elif all:
        # Show all logs
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    rprint(content)
                else:
                    rprint("[dim]日志文件为空[/dim]")
        except Exception as e:
            rprint(f"[red]✗[/red] 读取日志失败: {e}")
    else:
        # Show last N lines
        try:
            result = subprocess.run(
                ['tail', '-n', str(lines), str(log_file)],
                capture_output=True,
                text=True,
                check=False
            )
            if result.stdout:
                rprint(result.stdout)
            else:
                rprint("[dim]日志文件为空[/dim]")
        except Exception as e:
            rprint(f"[red]✗[/red] 读取日志失败: {e}")


if __name__ == "__main__":
    main()
