# 使用指南

## 安装

### 方式一：使用安装脚本（推荐）

```bash
# 克隆仓库
git clone https://github.com/h907530759/ant_cc_dingding_notifier.git
cd ant_cc_dingding_notifier

# 运行安装脚本
chmod +x install.sh
./install.sh
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/h907530759/ant_cc_dingding_notifier.git
cd ant_cc_dingding_notifier

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

## 配置

### 1. 创建钉钉机器人

在钉钉群中添加自定义机器人：

1. 打开钉钉群设置
2. 选择"智能群助手" -> "添加机器人" -> "自定义"
3. 设置机器人名称
4. 安全设置选择"加签"（推荐）
5. 复制 Webhook URL 和加签密钥

### 2. 配置通知工具

```bash
# 交互式配置
claude-dingtalk setup

# 或使用简短命令
cdn setup
```

配置向导会引导您：
- 输入钉钉 Webhook URL
- 输入加签密钥（可选）
- 选择要启用的事件类型
- 配置 Claude Code settings.json 路径

### 3. 安装 Hooks

```bash
# 安装 Claude Code hooks
claude-dingtalk hooks install
```

这将在您的 settings.json 中添加以下配置：

```json
{
  "hooks": {
    "preToolUse": "~/.claude-dingtalk/hooks/pre_tool_use.py",
    "postToolUse": "~/.claude-dingtalk/hooks/post_tool_use.py",
    "stop": "~/.claude-dingtalk/hooks/stop.py",
    "notification": "~/.claude-dingtalk/hooks/notification.py"
  }
}
```

## 使用示例

### 测试通知

```bash
claude-dingtalk test
```

### 查看状态

```bash
claude-dingtalk status
```

输出示例：
```
📊 配置状态

┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 配置项          ┃ 值                                   ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
┃ 状态            ┃ ✓ 启用                              ┃
┃ Webhook         ┃ https://oapi.dingtalk.com/robot/... ┃
┃ 加签密钥        ┃ ✓ 已配置                            ┃
└────────────────┴──────────────────────────────────────┘

事件配置:

┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ 事件            ┃ 状态        ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
┃ pre_tool_use    ┃ ✓ 启用      ┃
┃ post_tool_use   ┃ ✓ 启用      ┃
┃ stop            ┃ ✓ 启用      ┃
┃ notification    ┃ ✓ 吟用      ┃
└────────────────┴──────────────┘
```

### 发送自定义消息

```bash
claude-dingtalk send "Hello from Claude Code!"
```

### 管理 Hooks

```bash
# 查看 hooks 状态
claude-dingtalk hooks status

# 卸载 hooks
claude-dingtalk hooks uninstall
```

## 事件类型说明

### pre_tool_use

在工具使用前触发，用于检测敏感操作。

**敏感操作列表（默认）:**
- sudo
- rm -
- git push
- docker
- kubectl
- npm publish

**通知示例:**
```
🔐 Claude Code 敏感操作检测

⚠️ 检测到敏感操作

📂 项目: my-project
⚡ 工具: Bash
📝 输入: sudo systemctl restart nginx

💡 请在终端中确认是否继续执行
```

### post_tool_use

在工具使用后触发，用于记录执行结果。

**仅在发生错误时通知**，避免消息过多。

### stop

当 Claude Code 停止工作时触发，发送任务完成通知。

**通知示例:**
```
✅ Claude Code 任务完成

🎉 工作完成，可以休息了！

📂 项目: my-project
⏰ 时间: 2026-04-03 18:00:00
📊 状态: 所有任务已完成

☕ 建议您休息一下或检查结果
```

### notification

处理权限请求和提示。

**通知示例:**
```
🔐 Claude Code 权限请求

💡 请在终端中确认操作
```

## 配置文件

配置文件位于 `~/.claude-dingtalk/config.yaml`：

```yaml
# 钉钉机器人配置
dingtalk:
  enabled: true
  webhook: "https://oapi.dingtalk.com/robot/send?access_token=..."
  secret: "SEC..."
  msg_type: "markdown"  # markdown or actionCard

# Claude Code settings.json 路径
settings_paths:
  - "~/.claude/settings.json"
  - "~/work/project1/.claude/settings.json"

# 通知事件配置
events:
  pre_tool_use:
    enabled: true
    channels:
      - dingtalk
  post_tool_use:
    enabled: true
    channels:
      - dingtalk
  stop:
    enabled: true
    channels:
      - dingtalk
  notification:
    enabled: true
    channels:
      - dingtalk

# 敏感操作检测
sensitive_operations:
  patterns:
    - "sudo"
    - "rm -"
    - "git push"
    - "docker"
    - "kubectl"
    - "npm publish"
  enabled: true
```

## 多项目配置

如果您有多个项目需要不同的配置，可以指定多个 settings.json 路径：

```bash
claude-dingtalk setup
```

在配置向导中添加多个路径，例如：
- ~/.claude/settings.json（全局配置）
- ~/work/project1/.claude/settings.json（项目1）
- ~/work/project2/.claude/settings.json（项目2）

工具会自动为所有配置文件安装 hooks。

## 故障排除

### 通知未收到

1. 检查配置：`claude-dingtalk status`
2. 测试通知：`claude-dingtalk test`
3. 检查钉钉机器人配置
4. 查看 Claude Code 日志

### Hooks 未生效

1. 确认 hooks 已安装：`claude-dingtalk hooks status`
2. 检查 settings.json 中的 hooks 配置
3. 重新安装 hooks：`claude-dingtalk hooks install`

### 权限错误

确保 hook 脚本有执行权限：

```bash
chmod +x ~/.claude-dingtalk/hooks/*.py
```

## 高级用法

### 自定义敏感操作模式

编辑配置文件：

```yaml
sensitive_operations:
  patterns:
    - "sudo"
    - "rm -"
    - "docker"
    - "production"  # 添加自定义模式
  enabled: true
```

### 禁用特定事件

```yaml
events:
  pre_tool_use:
    enabled: false  # 禁用 pre_tool_use
```

### 环境变量配置

可以使用环境变量快速配置：

```bash
export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=..."
export DINGTALK_SECRET="SEC..."

claude-dingtalk setup --auto
```
