# Claude Code 钉钉通知工具

Claude Code 钉钉机器人通知集成工具，支持在 hook 节点触发钉钉机器人通知。

## ✨ 功能特性

- ✅ 支持 Claude Code hook 机制集成
- 📱 钉钉机器人消息推送（ActionCard + Markdown 格式）
- 🎯 智能检测敏感操作和任务完成
- 📊 支持多个 settings.json 文件配置
- 🔧 简单易用的命令行工具
- 🎨 美观的交互式配置界面

## 🚀 快速开始

### 方式一：直接使用（推荐，无需安装）

```bash
# 克隆或进入项目目录
git clone https://github.com/h907530759/ant_cc_dingding_notifier.git
cd ant_cc_dingding_notifier

# 运行配置
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

详细安装说明请查看 [INSTALL.md](INSTALL.md)

### 🔄 如何更新升级

如果你已经安装了旧版本，只需：

```bash
# 1. 进入项目目录
cd ~/workspace/claude_notifyer  # 或你的项目路径

# 2. 拉取最新代码
git pull origin main

# 3. 重新安装
./install.sh

# 4. 重新加载 shell 配置
source ~/.zshrc  # 或 source ~/.bashrc

# 5. 重新安装 Hooks（重要！）
# 方式一：快速升级（推荐）
claude-dingtalk hooks install

# 方式二：彻底升级（如果遇到问题）
# claude-dingtalk hooks uninstall
# claude-dingtalk hooks install

# 6. 测试新功能
claude-dingtalk hooks logs -n 10
```

详细升级说明请查看 [UPGRADE_GUIDE.md](UPGRADE_GUIDE.md)

## 📚 文档

- **[INSTALL.md](INSTALL.md)** - 安装指南
- **[QUICKSTART.md](QUICKSTART.md)** - 5 分钟快速配置
- **[UPGRADE_GUIDE.md](UPGRADE_GUIDE.md)** - 升级指南
- **[docs/USAGE.md](docs/USAGE.md)** - 完整使用指南
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 项目总结
- **[MACOS_TROUBLESHOOTING.md](MACOS_TROUBLESHOOTING.md)** - macOS 通知故障排除（⭐ 推荐）

### macOS 桌面通知

- ✅ 使用 terminal-notifier，兼容所有终端工具（iTerm2、Terminal 等）
- ✅ 与钉钉通知同时发送
- ✅ 简洁的通知标题和内容
- 📦 **需要安装**: `brew install terminal-notifier`
- 📖 **[macOS 通知使用说明](MACOS_NOTIFICATION_v0.3.0.md)**
- 🔧 **[macOS 通知故障排除](MACOS_TROUBLESHOOTING.md)** - 通知没弹出？查看安装步骤

## 🎯 核心功能

### 1. 敏感操作检测

自动检测以下敏感操作并发送通知：
- sudo
- rm -
- git push
- docker
- kubectl
- npm publish

### 2. 任务完成通知

当 Claude Code 停止工作时自动发送完成通知。

### 3. 错误通知

工具执行出错时立即发送通知。

### 4. 权限请求通知

处理权限请求和提示。

## 📱 命令行工具

```bash
# 配置管理
./run.sh setup           # 配置向导
./run.sh status          # 查看状态

# 测试
./run.sh test            # 测试通知

# 消息
./run.sh send "消息"     # 发送自定义消息

# Hooks 管理
./run.sh hooks install   # 安装 hooks
./run.sh hooks status    # 查看 hooks 状态
./run.sh hooks uninstall # 卸载 hooks

# 帮助
./run.sh --help          # 查看帮助
```

## 📁 项目结构

```
claude-dingtalk-notifier/
├── src/claude_dingtalk_notifier/
│   ├── cli.py              # CLI 工具
│   ├── config.py           # 配置管理
│   ├── dingtalk.py         # 钉钉机器人
│   ├── utils.py            # 工具函数
│   └── hooks/              # Hook 脚本
├── docs/                   # 文档
├── tests/                  # 测试
├── run.sh                  # 快速运行脚本
├── install.sh              # 安装脚本
└── README.md
```

## ⚙️ 配置文件

配置文件位于 `~/.claude-dingtalk/config.yaml`：

```yaml
# 钉钉机器人配置
dingtalk:
  enabled: true
  webhook: "https://oapi.dingtalk.com/robot/send?access_token=..."
  secret: "SEC..."

# Claude Code settings.json 路径
settings_paths:
  - "~/.claude/settings.json"

# 通知事件配置
events:
  pre_tool_use:
    enabled: true
  post_tool_use:
    enabled: true
  stop:
    enabled: true
  notification:
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

## 🎨 支持的 Hook 类型

### 核心事件（⭐ 推荐）

- **PreToolUse**: 工具使用前触发（检测敏感操作）
- **PostToolUse**: 工具使用后触发（记录结果）
- **Stop**: Claude 停止工作时触发（任务完成）
- **SessionStart**: 会话开始时触发
- **SessionEnd**: 会话结束时触发
- **PostToolUseFailure**: 工具执行失败时触发
- **TaskCreated**: 新任务创建时触发
- **TaskCompleted**: 任务完成时触发

### 可选事件

- **CwdChanged**: 工作目录切换时触发
- **ConfigChange**: 配置文件更改时触发
- **SubagentStart**: 子代理启动时触发
- **SubagentStop**: 子代理完成时触发

更多 Hook 事件支持请查看 [HOOKS_EXPANSION.md](HOOKS_EXPANSION.md)

## 🔧 依赖

- Python 3.8+
- requests >= 2.31.0
- pyyaml >= 6.0.0
- click >= 8.1.0
- rich >= 13.0.0

## 📝 许可证

MIT License

## 🙏 致谢

本项目参考了 [kdush/Claude-Code-Notifier](https://github.com/kdush/Claude-Code-Notifier) 的设计理念。
