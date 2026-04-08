# 功能特性

## ✨ 核心功能

### 1. 交互式 Hook 事件选择 🎯

**新增功能！** 现在在配置时，系统会列出所有可用的 Hook 事件，让您选择需要启用哪些通知。

#### 支持的事件类型

| 编号 | 事件 | 说明 | 推荐度 |
|------|------|------|--------|
| 1 | pre_tool_use | 工具使用前触发，检测敏感操作 | ⭐⭐⭐ |
| 2 | post_tool_use | 工具使用后触发，记录错误 | ⭐⭐⭐ |
| 3 | stop | Claude 停止时触发，任务完成通知 | ⭐⭐⭐ |
| 4 | notification | 处理权限请求和提示 | ⭐⭐ |

#### 使用方式

```bash
./run.sh setup
```

系统会显示：
```
🎯 选择要启用的事件类型

┏━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┃ 编号 ┃ 事件         ┃ 说明                           ┃ 推荐 ┃
┡━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│ 1   │ pre_tool_use │ 检测敏感操作（sudo、rm、docker等）│ ⭐ 推荐│
│ 2   │ post_tool_use│ 记录执行结果和错误              │ ⭐ 推荐│
│ 3   │ stop         │ 任务完成通知                    │ ⭐ 推荐│
│ 4   │ notification │ 处理权限请求                    │ 可选  │
└━━━━┴━━━━━━━━━━━━━┴━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┴━━━━━━┘

请选择要启用的事件（输入编号，用逗号分隔，如: 1,2,3）
您的选择 (1,2,3): 
```

#### 选择方式

- **直接回车**: 启用推荐事件（1,2,3）
- **输入 `1,2,3,4`**: 启用所有事件
- **输入 `1,3`**: 自定义选择
- **输入 `0`**: 禁用所有事件

### 2. 敏感操作检测 🛡️

自动检测以下敏感操作并发送通知：

- `sudo` - 提权操作
- `rm -` - 删除操作
- `git push` - 代码推送
- `docker` - 容器操作
- `kubectl` - K8s 操作
- `npm publish` - 包发布

### 3. 多项目支持 📊

支持配置多个 settings.json 文件路径：

```bash
./run.sh setup
```

在配置时添加多个路径：
- `~/.claude/settings.json`（全局）
- `~/work/project1/.claude/settings.json`（项目1）
- `~/work/project2/.claude/settings.json`（项目2）

工具会自动为所有配置文件安装 hooks。

### 4. 智能通知过滤 🎯

- **错误通知**: 只在工具执行出错时通知
- **成功静默**: 成功操作不发送通知，避免打扰
- **完成通知**: 任务完成时发送庆祝消息

### 5. 美观的通知样式 🎨

#### 敏感操作通知（ActionCard）

```
🔐 Claude Code 敏感操作检测

⚠️ 检测到敏感操作

📂 项目: my-project
⚡ 工具: Bash
📝 输入: sudo systemctl restart nginx

💡 请在终端中确认是否继续执行
```

#### 任务完成通知（Markdown）

```
✅ Claude Code 任务完成

🎉 工作完成，可以休息了！

📂 项目: my-project
⏰ 时间: 2026-04-03 18:00:00
📊 状态: 所有任务已完成

☕ 建议您休息一下或检查结果
```

## 🛠️ 技术特性

### 1. Hook 机制

完全兼容 Claude Code Hooks API：

- **PreToolUse**: 工具使用前
- **PostToolUse**: 工具使用后
- **Stop**: 停止工作
- **Notification**: 权限和提示

### 2. 配置管理

- YAML 配置文件
- 热重载支持
- 配置验证
- 备份机制

### 3. 安全性

- 加签支持
- 环境变量配置
- 本地配置存储

### 4. 易用性

- 交互式配置向导
- 命令行自动补全
- 详细的错误提示
- 测试功能

## 📱 命令行工具

### 基础命令

```bash
./run.sh setup           # 配置向导
./run.sh status          # 查看状态
./run.sh test            # 测试通知
./run.sh send "消息"     # 发送消息
```

### Hook 管理

```bash
./run.sh hooks install   # 安装 hooks
./run.sh hooks status    # 查看状态
./run.sh hooks uninstall # 卸载 hooks
```

### 配置选项

```bash
./run.sh setup --auto    # 自动配置（使用环境变量）
```

## 🔧 高级配置

### 自定义敏感操作

编辑 `~/.claude-dingtalk/config.yaml`:

```yaml
sensitive_operations:
  patterns:
    - "sudo"
    - "rm -"
    - "production"  # 添加自定义模式
  enabled: true
```

### 禁用特定事件

```yaml
events:
  pre_tool_use:
    enabled: false  # 禁用
  post_tool_use:
    enabled: true   # 启用
```

### 环境变量配置

```bash
export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=..."
export DINGTALK_SECRET="SEC..."

./run.sh setup --auto
```

## 📊 使用场景

### 场景 1: 日常开发

推荐配置：`1,2,3`

- 安全防护
- 错误提醒
- 任务完成通知

### 场景 2: 调试模式

推荐配置：`1,2,3,4`

- 全面监控
- 所有操作反馈

### 场景 3: 生产环境

推荐配置：`1,3`

- 安全监控
- 重要通知
- 减少打扰

## 🎯 最佳实践

1. **初次使用**: 启用推荐配置（1,2,3）
2. **调试阶段**: 启用所有事件（1,2,3,4）
3. **生产环境**: 只启用重要事件（1,3）
4. **按需调整**: 根据实际使用情况调整

详细使用说明请查看 [DEMO.md](DEMO.md)
