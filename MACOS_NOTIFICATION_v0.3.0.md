# 🍎 macOS 桌面通知功能 - v0.3.0

**发布日期**: 2026-04-04
**版本类型**: 新功能
**从版本**: v0.2.6

---

## ✨ 新功能概述

**macOS 桌面通知**让你在 macOS 系统桌面上直接接收 Claude Code 事件通知，无需切换到钉钉群即可查看消息。

### 核心特性

- ✅ **零依赖** - 使用 macOS 自带的 osascript，无需安装额外软件
- ✅ **双渠道** - 同时发送钉钉和 macOS 通知，互不干扰
- ✅ **简洁清晰** - macOS 通知显示简化的标题和内容
- ✅ **声音提醒** - 可选的声音提示
- ✅ **通知列表** - 多条通知自动堆叠显示，形成列表效果

---

## 🎯 使用场景

### 适合启用 macOS 通知的场景

1. **本地开发** - 在 Mac 上开发时，快速查看通知而不切换应用
2. **专注模式** - 不想被钉钉群消息打扰，只看重要提醒
3. **即时提醒** - 敏感操作、工作完成等关键事件需要立即看到

### 通知内容对比

**钉钉通知** (详细):
```markdown
### 🚀 新会话已启动

📂 项目: ~/ant_cc_dingding_notifier
⏰ 开始时间: 2026-04-04 23:45:00
💡 让我们开始工作吧！
```

**macOS 通知** (简洁):
```
标题: 🚀 会话已启动
内容: test-project 新会话已启动
```

---

## 🚀 快速开始

### 1. 重新配置（启用 macOS 通知）

```bash
# 运行配置命令
cdn setup

# 按照提示：
# 1. 配置钉钉机器人（如果已配置会跳过）
# 2. 选择事件类型
# 3. 配置 settings.json 路径
# 4. 【新功能】配置 macOS 桌面通知
```

### 2. 配置向导

```
🍎 配置 macOS 桌面通知
在 macOS 桌面弹出系统通知，与钉钉通知同时发送

是否启用 macOS 桌面通知？[y/N]: y
是否需要声音提醒？[Y/n]: y
✓ macOS 桌面通知已启用
```

### 3. 重新安装 Hooks

```bash
# 必须重新安装 hooks 才能生效
cdn hooks install
```

### 4. 测试通知

```bash
# 测试钉钉通知
cdn test

# 测试 macOS 通知（可选）
python3 test_macos_notification.py
```

---

## 📋 支持的事件

以下 hooks 已支持 macOS 桌面通知：

| Hook | 钉钉 | macOS | macOS 通知标题 | macOS 通知内容 |
|------|------|-------|--------------|--------------|
| **session_start** | ✅ | ✅ | 🚀 会话已启动 | {项目名} 新会话已启动 |
| **stop** | ✅ | ✅ | ✅ 工作已结束 | {项目名} 所有任务已完成 |
| **pre_tool_use** (敏感) | ✅ | ✅ | 🔐 敏感操作检测 | 即将执行: {工具名} |
| **stop_failure** | ✅ | ✅ | 💥 API 调用失败 | Claude API 调用失败 |
| **notification** (权限) | ✅ | ✅ | 🔐 需要权限确认 | 需要权限确认 |
| **post_tool_use** (错误) | ✅ | ✅ | ❌ 工具执行出错 | 工具执行出错 |
| **tool_failure** | ✅ | ❌ | - | - |
| **session_end** | ✅ | ❌ | - | - |
| **task_created** | ✅ | ❌ | - | - |
| **task_completed** | ✅ | ❌ | - | - |
| **cwd_changed** | ✅ | ❌ | - | - |
| **config_change** | ✅ | ❌ | - | - |
| **subagent_start** | ✅ | ❌ | - | - |
| **subagent_stop** | ✅ | ❌ | - | - |

**原则**：
- 🟢 **重要事件** → 钉钉 + macOS 双通知
- 🔵 **普通记录** → 仅钉钉
- ⚪ **高频事件** → 全部禁用，避免打扰

---

## 🍎 macOS 通知列表效果

### 多条通知堆叠显示

当多个通知同时弹出时，macOS 会自动将它们堆叠显示：

```
┌─────────────────────────────────┐
│ 🚀 会话已启动                   │
│ test-project 新会话已启动        │
├─────────────────────────────────┤
│ ✅ 工作已结束                   │
│ test-project 所有任务已完成      │
├─────────────────────────────────┤
│ 🔐 敏感操作检测                 │
│ 即将执行: rm -rf                │
└─────────────────────────────────┘
```

**特性**：
- ✅ 最新通知显示在最上方
- ✅ 点击通知可展开查看
- ✅ 通知自动归档到通知中心
- ✅ 支持"通知分组"模式（系统设置）

---

## ⚙️ 配置文件

### config.yaml 结构

```yaml
# DingTalk 机器人配置
dingtalk:
  enabled: true
  webhook: "https://oapi.dingtalk.com/robot/send?access_token=..."
  secret: "SEC..."
  msg_type: "markdown"

# macOS 桌面通知配置（新增）
macos:
  enabled: true      # 是否启用 macOS 通知
  sound: true        # 是否播放声音

# 事件配置
events:
  session_start:
    enabled: true
    channels: ["dingtalk", "macos"]  # 同时发送到两个渠道
  stop:
    enabled: true
    channels: ["dingtalk", "macos"]
  pre_tool_use:
    enabled: true
    channels: ["dingtalk", "macos"]
```

---

## 🎛️ macOS 通知设置

### 系统通知偏好设置

在 macOS 系统设置中配置通知行为：

```
系统设置 > 通知 > Python (或 Terminal)
```

**推荐设置**：
- **允许通知**: ✅ 启用
- **锁定屏幕上显示**: ✅ 启用（可选）
- **横幅样式**: 持续（显示时间更长）
- **通知数量**: 5 个（在通知中心显示）
- **通知分组**: 按应用（自动堆叠）

---

## 📊 使用效果

### 场景 1: 启动新会话

```bash
# 你打开 Claude Code 开始新会话
# 立即收到：

🍎 macOS 右上角弹出:
  ┌──────────────────────────────┐
  │ 🚀 会话已启动                │
  │ my-project 新会话已启动      │
  └──────────────────────────────┘

📱 钉钉群同时收到:
   详细的会话信息卡片
```

### 场景 2: 敏感操作

```bash
# 你执行 rm -rf 命令
# 立即收到：

🍎 macOS 右上角弹出:
  ┌──────────────────────────────┐
  │ 🔐 敏感操作检测              │
  │ 即将执行: Bash               │
  └──────────────────────────────┘

📱 钉钉群同时收到:
   详细的敏感操作信息和按钮
```

### 场景 3: 工作完成

```bash
# Claude Code 完成所有任务
# 立即收到：

🍎 macOS 右上角弹出:
  ┌──────────────────────────────┐
  │ ✅ 工作已结束                │
  │ my-project 所有任务已完成    │
  └──────────────────────────────┘

📱 钉钉群同时收到:
   完整的工作报告
```

---

## 🔧 手动配置

### 方法 1: 使用 setup 命令（推荐）

```bash
cdn setup
# 按照提示配置 macOS 通知
```

### 方法 2: 手动编辑配置文件

```bash
# 编辑配置文件
vim ~/.claude-dingtalk/config.yaml

# 添加或修改以下内容：
macos:
  enabled: true   # 改为 true
  sound: true     # 是否需要声音

# 保存后重新安装 hooks
cdn hooks install
```

---

## 🎓 最佳实践

### 1. 通知频率控制

**推荐的启用策略**：
- ✅ **启用**: session_start, stop, pre_tool_use (敏感)
- ❌ **禁用**: task_created, cwd_changed, subagent_start

### 2. 声音提醒

**建议**：
- 开发时：启用声音，不会错过重要通知
- 会议中：禁用声音，只看通知气泡

### 3. 与钉钉配合

**双渠道优势**：
- 📱 **钉钉群**: 完整记录，可追溯历史，适合团队协作
- 🍎 **macOS**: 即时提醒，快速响应，适合个人开发

---

## 🐛 故障排除

### macOS 通知没有弹出

**可能原因**：
1. macOS 通知未启用
2. Python/Terminal 通知权限被禁用

**解决方法**：
```bash
# 1. 检查配置
cat ~/.claude-dingtalk/config.yaml | grep macos

# 应该看到：
# macos:
#   enabled: true

# 2. 检查系统设置
# 系统设置 > 通知 > Python
# 确保通知已启用

# 3. 测试通知
python3 test_macos_notification.py
```

### 钉钉通知正常，macOS 通知失败

**这是正常的！** macOS 通知失败不会影响钉钉通知，两个渠道是独立的。

### 声音不播放

**检查**：
1. 系统音量是否开启
2. `config.yaml` 中 `macos.sound` 是否为 `true`
3. macOS 系统设置中的通知声音是否开启

---

## 📚 技术细节

### 实现原理

**macOSNotifier 类**使用 AppleScript 发送通知：

```python
script = f'''
display notification "{message}" with title "{title}" sound name "default"
'''

subprocess.run(["osascript", "-e", script])
```

**优势**：
- 零外部依赖
- 兼容所有 macOS 版本
- 简单可靠

### Hook 脚本集成

Hook 脚本同时支持两个渠道：

```python
# 发送钉钉通知
if config.dingtalk.enabled:
    notifier = DingTalkNotifier(...)
    message = format_claude_message("session_start", data)
    notifier.send(message)

# 发送 macOS 通知
if config.macos.enabled:
    macos_notifier = MacOSNotifier(...)
    macos_notifier.send(title, message)
```

---

## ✅ 总结

### 新增功能

- ✅ macOS 桌面通知支持
- ✅ 双渠道通知（钉钉 + macOS）
- ✅ 配置向导集成
- ✅ 零外部依赖

### 文件变更

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `macos_notifier.py` | 新建 | macOS 通知器类 |
| `config.py` | 修改 | 添加 MacOSConfig 配置类 |
| `cli.py` | 修改 | 添加 macOS 配置向导 |
| `cli.py` | 修改 | Hook 脚本支持 macOS 通知 |
| `__init__.py` | 修改 | 版本号: 0.2.6 → 0.3.0 |

### 版本信息

**版本**: v0.3.0
**发布日期**: 2026-04-04
**类型**: 新功能
**状态**: ✅ 已完成并测试

---

**享受 macOS 桌面通知的便捷！** 🍎
