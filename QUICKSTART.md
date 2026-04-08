# 快速开始指南

## 5 分钟快速配置

### 步骤 1: 进入项目目录

```bash
cd /Users/suchen/workspace/claude_notifyer
```

### 步骤 2: 创建钉钉机器人

1. 打开钉钉群
2. 点击右上角 "..." -> "群设置"
3. 选择 "智能群助手" -> "添加机器人" -> "自定义"
4. 设置机器人名称（如 "Claude Code"）
5. 安全设置选择 "加签"（推荐）
6. 复制 Webhook URL 和加签密钥

### 步骤 3: 配置工具

```bash
# 使用 run.sh 脚本（推荐）
./run.sh setup
```

按提示输入：
1. 钉钉 Webhook URL
2. 加签密钥（可选）
3. 选择事件类型（建议全部启用）
4. 确认 settings.json 路径

### 步骤 4: 测试

```bash
./run.sh test
```

检查钉钉群是否收到测试消息。

### 步骤 5: 安装 Hooks

```bash
./run.sh hooks install
```

### 完成！

现在当您使用 Claude Code 时，会在以下情况收到钉钉通知：
- 检测到敏感操作（sudo、rm、docker 等）
- 工具执行出错
- 任务完成
- 需要权限确认

## 常用命令

所有命令都通过 `./run.sh` 运行：

```bash
# 配置
./run.sh setup           # 配置向导
./run.sh setup --auto    # 自动配置（使用环境变量）

# 测试
./run.sh test            # 测试通知
./run.sh status          # 查看状态

# 消息
./run.sh send "消息"     # 发送自定义消息

# Hooks
./run.sh hooks install   # 安装 hooks
./run.sh hooks status    # 查看 hooks 状态
./run.sh hooks uninstall # 卸载 hooks

# 帮助
./run.sh --help          # 查看帮助
./run.sh --version       # 查看版本
```

## 创建别名（可选）

为了更方便使用，可以创建别名：

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
alias claude-dingtalk='/Users/suchen/workspace/claude_notifyer/run.sh'
alias cdn='/Users/suchen/workspace/claude_notifyer/run.sh'
```

然后就可以使用简短命令：

```bash
claude-dingtalk setup
cdn test
cdn status
```

## 配置文件

配置文件位置：`~/.claude-dingtalk/config.yaml`

您可以手动编辑此文件来：
- 修改敏感操作检测规则
- 启用/禁用特定事件
- 添加更多 settings.json 路径

## 故障排除

### 问题：通知未收到

**解决方案：**
```bash
# 1. 检查配置
./run.sh status

# 2. 测试通知
./run.sh test

# 3. 检查 Webhook 和密钥是否正确
```

### 问题：Hooks 未生效

**解决方案：**
```bash
# 1. 检查 hooks 状态
./run.sh hooks status

# 2. 重新安装 hooks
./run.sh hooks install
```

### 问题：权限错误

**解决方案：**
```bash
chmod +x ~/.claude-dingtalk/hooks/*.py
```

## 使用环境变量配置

可以使用环境变量快速配置：

```bash
export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=..."
export DINGTALK_SECRET="SEC..."

./run.sh setup --auto
```

## 通知示例

### 敏感操作通知
```
🔐 Claude Code 敏感操作检测

⚠️ 检测到敏感操作

📂 项目: my-project
⚡ 工具: Bash
📝 输入: sudo rm -rf /tmp/test

💡 请在终端中确认是否继续执行
```

### 任务完成通知
```
✅ Claude Code 任务完成

🎉 工作完成，可以休息了！

📂 项目: my-project
⏰ 时间: 2026-04-03 18:00:00
📊 状态: 所有任务已完成

☕ 建议您休息一下或检查结果
```

## 下一步

- 阅读完整文档：[docs/USAGE.md](docs/USAGE.md)
- 查看项目总结：[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- 自定义敏感操作规则
- 配置多个项目

## 卸载

```bash
# 卸载 hooks
./run.sh hooks uninstall

# 删除配置（可选）
rm -rf ~/.claude-dingtalk

# 删除别名（从 ~/.zshrc 或 ~/.bashrc 中移除）
```
