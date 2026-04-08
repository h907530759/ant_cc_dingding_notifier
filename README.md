# Claude Code 钉钉通知工具

Claude Code 钉钉机器人通知集成工具，支持在 hook 节点触发钉钉机器人通知和 macOS 桌面通知。

## ✨ 功能特性

- ✅ 支持 Claude Code hook 机制集成
- 📱 钉钉机器人消息推送（Markdown 格式）
- 🍎 macOS 桌面通知（使用 terminal-notifier）
- 📊 支持多个 settings.json 文件配置
- 📝 完整的日志系统，清晰显示每个通知渠道的执行结果
- 🔧 简单易用的命令行工具

## 🚀 快速开始

### 方式一：直接使用（推荐，无需安装）

```bash
# 克隆项目
git clone https://github.com/h907530759/ant_cc_dingding_notifier.git
cd ant_cc_dingding_notifier

# 运行配置向导
./run.sh setup

# 测试通知
./run.sh test

# 安装 Hooks
./run.sh hooks install
```

### 方式二：安装到系统

```bash
# 运行安装脚本
./install.sh

# 重新加载 shell 配置
source ~/.zshrc  # 或 source ~/.bashrc

# 使用命令
claude-dingtalk setup
```

### 🔄 如何更新升级

如果你已经安装了旧版本：

```bash
# 1. 进入项目目录
cd ~/workspace/claude_notifyer  # 或你的项目路径

# 2. 拉取最新代码
git pull origin main

# 3. 重新安装
./install.sh

# 4. 重新加载 shell 配置
source ~/.zshrc  # 或 source ~/.bashrc

# 5. 重新安装 Hooks
# 方式一：快速升级（推荐）
claude-dingtalk hooks install

# 方式二：彻底升级（如果遇到问题）
# claude-dingtalk hooks uninstall
# claude-dingtalk hooks install

# 6. 测试新功能
claude-dingtalk hooks logs -n 10
```

## 📱 常用命令

```bash
# 配置管理
claude-dingtalk setup           # 配置向导
claude-dingtalk status          # 查看状态

# 测试通知
claude-dingtalk test            # 测试钉钉通知

# 发送自定义消息
claude-dingtalk send "消息内容"

# Hooks 管理
claude-dingtalk hooks install   # 安装 hooks
claude-dingtalk hooks status    # 查看 hooks 状态
claude-dingtalk hooks uninstall # 卸载 hooks

# 查看日志（新功能）
claude-dingtalk hooks logs      # 查看最近 50 行日志
claude-dingtalk hooks logs -n 20    # 查看最近 20 行
claude-dingtalk hooks logs -f       # 实时跟踪日志
claude-dingtalk hooks logs -a       # 查看所有日志

# 简写命令（cdn）
cdn setup
cdn status
cdn test
cdn hooks logs -f
```

## ⚙️ 配置文件

配置文件位于 `~/.claude-dingtalk/config.yaml`：

```yaml
# 钉钉机器人配置
dingtalk:
  enabled: true
  webhook: "https://oapi.dingtalk.com/robot/send?access_token=..."
  secret: "SEC..."
  msg_type: markdown

# macOS 桌面通知配置
macos:
  enabled: true      # 是否启用 macOS 通知
  sound: true        # 是否播放声音

# Claude Code settings.json 路径
settings_paths:
  - "~/.claude/settings.json"
  - "~/.codefuse/engine/cc/settings.json"

# 通知事件配置
events:
  pre_tool_use:
    enabled: true
  post_tool_use:
    enabled: true
  stop:
    enabled: true
  session_start:
    enabled: true
  session_end:
    enabled: true
  tool_failure:
    enabled: true

# 敏感操作检测
sensitive_operations:
  patterns:
    - "sudo"
    - "rm -"
    - "git push"
    - "docker"
    - "kubectl"
  enabled: true
```

## 📋 日志系统

### 查看日志

所有 hook 调用和通知发送都会自动记录到 `~/.claude-dingtalk/hook.log`：

```bash
# 查看最近日志
cdn hooks logs -n 20

# 实时监控日志
cdn hooks logs -f
```

### 日志格式

```
2026-04-08 22:41:42 - INFO - Hook started: stop
2026-04-08 22:41:42 - INFO - Channel triggered: dingtalk (stop)
2026-04-08 22:41:43 - INFO - ✓ dingtalk: SUCCESS - Notification sent successfully
2026-04-08 22:41:43 - INFO - Channel triggered: macOS-notifier (stop)
2026-04-08 22:41:43 - INFO - ✓ macOS-notifier: SUCCESS - Notification sent: Project - 任务完成
2026-04-08 22:41:43 - INFO - Hook succeeded: stop - All notifications sent successfully
```

- ✓ 表示成功
- ✗ 表示失败
- 清晰显示每个渠道（钉钉、macOS）的执行状态

## 🎯 支持的 Hook 类型

### 核心事件（⭐ 推荐）

- **PreToolUse**: 工具使用前触发（检测敏感操作）
- **PostToolUse**: 工具使用后触发（记录结果）
- **Stop**: Claude 停止工作时触发（任务完成）
- **StopFailure**: Claude 异常停止时触发
- **SessionStart**: 会话开始时触发
- **SessionEnd**: 会话结束时触发
- **PostToolUseFailure**: 工具执行失败时触发
- **Notification**: 通知事件触发

### 可选事件

- **TaskCreated**: 新任务创建时触发
- **TaskCompleted**: 任务完成时触发
- **CwdChanged**: 工作目录切换时触发
- **ConfigChange**: 配置文件更改时触发
- **SubagentStart**: 子代理启动时触发
- **SubagentStop**: 子代理完成时触发

## 🍎 macOS 桌面通知

### 安装依赖

macOS 桌面通知需要安装 `terminal-notifier`：

```bash
# 使用 Homebrew 安装
brew install terminal-notifier

# 验证安装
terminal-notifier -title "测试" -message "安装成功"
```

### 配置通知权限

1. 打开 **系统设置 → 通知 → Terminal**（或你使用的终端应用）
2. 确保 **允许通知** 已开启
3. 建议开启：横幅、声音

### 通知权限问题

如果通知没有弹出：

1. 检查请勿打扰模式是否关闭
2. 检查 Terminal 的通知权限
3. 重启终端应用：`killall Terminal`

## 🔧 常见问题

### Q: 钉钉通知发送失败？

**A:** 检查配置文件中的 webhook 和 secret 是否正确：

```bash
# 查看配置
cat ~/.claude-dingtalk/config.yaml

# 测试钉钉通知
claude-dingtalk test

# 查看错误日志
claude-dingtalk hooks logs -n 20
```

### Q: macOS 通知没有弹出？

**A:** 按以下步骤排查：

1. 检查 terminal-notifier 是否安装：
```bash
which terminal-notifier
```

2. 如果未安装，执行：
```bash
brew install terminal-notifier
```

3. 检查系统设置中的通知权限
4. 查看日志确认是否触发：
```bash
claude-dingtalk hooks logs -n 20
```

### Q: Hooks 不工作？

**A:** 检查 hooks 状态：

```bash
# 查看 hooks 安装状态
claude-dingtalk hooks status

# 查看日志
claude-dingtalk hooks logs -n 50

# 重新安装 hooks
claude-dingtalk hooks uninstall
claude-dingtalk hooks install
```

### Q: 如何查看通知发送记录？

**A:** 使用日志命令：

```bash
# 查看最近 20 条记录
claude-dingtalk hooks logs -n 20

# 实时监控
claude-dingtalk hooks logs -f

# 查看所有记录
claude-dingtalk hooks logs -a
```

### Q: 升级后通知不工作？

**A:** 重新安装 hooks：

```bash
claude-dingtalk hooks uninstall
claude-dingtalk hooks install
```

## 🔧 依赖

### Python 依赖

- Python 3.8+
- requests >= 2.31.0
- pyyaml >= 6.0.0
- click >= 8.1.0
- rich >= 13.0.0

### macOS 通知依赖

- terminal-notifier（通过 Homebrew 安装）

## 📝 许可证

MIT License

## 🙏 致谢

本项目参考了 [kdush/Claude-Code-Notifier](https://github.com/kdush/Claude-Code-Notifier) 的设计理念。
