# 🎉 版本 0.2.0 更新说明

## 📋 更新概览

**发布日期**: 2026-04-03
**版本**: 0.2.0
**类型**: 重大功能更新

---

## 🚀 重大改进

### Hook 事件支持从 4 个扩展到 12 个

在 0.1.x 版本中，我们只支持了 4 个基本的 hook 事件。现在，我们扩展到了 **12 个 hook 事件**，覆盖了 Claude Code 的更多生命周期！

### 新增的 Hook 事件

#### 🔥 高优先级事件（⭐ 推荐）

1. **sessionStart** - 会话开始通知
   - 当 Claude Code 启动新会话时触发
   - 显示项目名称和开始时间
   - 默认启用

2. **sessionEnd** - 会话结束通知
   - 当 Claude Code 会话结束时触发
   - 显示项目名称和结束时间
   - 默认启用

3. **postToolUseFailure** - 工具失败通知
   - 当工具执行失败时触发
   - 比普通的 postToolUse 错误信息更详细
   - 包含完整的错误堆栈信息
   - 默认启用

4. **taskCreated** - 任务创建通知
   - 当 Claude Code 创建新任务时触发
   - 显示任务 ID 和任务描述
   - 默认启用

5. **taskCompleted** - 任务完成通知
   - 当 Claude Code 完成任务时触发
   - 显示任务 ID 和任务描述
   - 默认启用

#### 🟡 可选事件

6. **cwdChanged** - 目录切换通知
   - 当 Claude Code 切换工作目录时触发
   - 显示旧目录和新目录路径
   - 默认禁用

7. **configChange** - 配置更改通知
   - 当 Claude Code 检测到配置文件更改时触发
   - 默认禁用

8. **subagentStart** - 子代理启动通知
   - 当 Claude Code 启动子代理时触发
   - 显示子代理类型（如 general-purpose, explore 等）
   - 默认禁用

9. **subagentStop** - 子代理完成通知
   - 当 Claude Code 子代理完成工作时触发
   - 默认禁用

---

## 🎨 配置界面改进

### 新的事件选择界面

运行 `./run.sh setup` 时，现在会显示完整的事件列表：

```
🎯 选择要启用的事件类型

┏━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┃ 编号 ┃ 事件           ┃ 说明                           ┃ 推荐 ┃
┡━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│ 1  │ pre_tool_use   │ 检测敏感操作（sudo、rm、docker等）│ ⭐ 推荐│
│ 2  │ post_tool_use  │ 记录执行结果和错误              │ ⭐ 推荐│
│ 3  │ stop           │ 任务完成通知                    │ ⭐ 推荐│
│ 4  │ session_start  │ 会话开始                        │ ⭐ 推荐│
│ 5  │ session_end    │ 会话结束                        │ ⭐ 推荐│
│ 6  │ tool_failure   │ 工具失败                        │ ⭐ 推荐│
│ 7  │ task_created   │ 任务创建                        │ ⭐ 推荐│
│ 8  │ task_completed │ 任务完成                        │ ⭐ 推荐│
│ 9  │ cwd_changed    │ 目录切换                        │ 可选  │
│ 10 │ config_change  │ 配置更改                        │ 可选  │
│ 11 │ subagent_start │ 子代理启动                      │ 可选  │
│ 12 │ subagent_stop  │ 子代理完成                      │ 可选  │
└━━━━┴━━━━━━━━━━━━━━━┴━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┴━━━━━━┘

请选择要启用的事件（输入编号，用逗号分隔，如: 1,2,3,8）
您的选择 (1,2,3,4,5,6,7,8):
```

### 默认配置变更

- **之前**: 默认启用 3 个事件（1,2,3）
- **现在**: 默认启用 8 个推荐事件（1-8）

---

## 💾 配置文件结构

### 新的配置格式

`~/.claude-dingtalk/config.yaml` 现在包含所有 12 个事件：

```yaml
# 钉钉机器人配置
dingtalk:
  enabled: true
  webhook: "https://oapi.dingtalk.com/robot/send?access_token=..."
  secret: "SEC..."
  msg_type: markdown

# Claude Code settings.json 路径
settings_paths:
  - "~/.claude/settings.json"

# 通知事件配置（扩展到 12 个事件）
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
    enabled: false
    channels:
      - dingtalk
  session_start:
    enabled: true
    channels:
      - dingtalk
  session_end:
    enabled: true
    channels:
      - dingtalk
  tool_failure:
    enabled: true
    channels:
      - dingtalk
  task_created:
    enabled: true
    channels:
      - dingtalk
  task_completed:
    enabled: true
    channels:
      - dingtalk
  cwd_changed:
    enabled: false
    channels:
      - dingtalk
  config_change:
    enabled: false
    channels:
      - dingtalk
  subagent_start:
    enabled: false
    channels:
      - dingtalk
  subagent_stop:
    enabled: false
    channels:
      - dingtalk

# 敏感操作检测
sensitive_operations:
  patterns:
    - sudo
    - rm -
    - git push
    - docker
    - kubectl
    - npm publish
  enabled: true
```

---

## 🔧 Hook 脚本

### 自动生成的 Hook 脚本

系统会自动在 `~/.claude-dingtalk/hooks/` 目录下生成对应的 Python 脚本：

```
~/.claude-dingtalk/hooks/
├── pre_tool_use.py        # 敏感操作检测
├── post_tool_use.py       # 工具执行结果
├── tool_failure.py        # 工具失败通知
├── stop.py                # 任务完成
├── session_start.py       # 会话开始
├── session_end.py         # 会话结束
├── task_created.py        # 任务创建
├── task_completed.py      # 任务完成
├── cwd_changed.py         # 目录切换
├── config_change.py       # 配置更改
├── subagent_start.py      # 子代理启动
└── subagent_stop.py       # 子代理完成
```

每个脚本都包含：
- 完整的导入和配置加载逻辑
- 事件数据处理
- 钉钉消息格式化和发送

---

## 📱 消息格式

### 新增事件的消息示例

#### SessionStart（会话开始）
```markdown
### 🚀 新会话已启动

**📂 项目:** my-project
**⏰ 开始时间:** 2026-04-03 14:30:00

💡 让我们开始工作吧！
```

#### TaskCreated（任务创建）
```markdown
### 📋 新任务已创建

**📂 项目:** my-project
**🆔 任务ID:** 123
**📝 任务:** 实现新功能

🚀 任务已添加到队列
```

#### TaskCompleted（任务完成）
```markdown
### ✅ 任务已完成

**📂 项目:** my-project
**🆔 任务ID:** 123
**📝 任务:** 实现新功能

🎉 太棒了，又完成一个任务！
```

#### ToolFailure（工具失败）
```markdown
### 💥 工具执行失败

**📂 项目:** my-project
**⚡ 工具:** Bash
**❌ 错误信息:** ```
Command failed with exit code 1
...
```

💡 请检查终端了解详情
```

---

## 🎯 推荐配置

### 日常开发（推荐）
```
事件选择: 1,2,3,4,5,6,7,8（所有推荐事件）
配置文件: ~/.claude/settings.json
```

### 完整监控
```
事件选择: 1,2,3,4,5,6,7,8,9,10,11,12（所有事件）
配置文件:
  - ~/.claude/settings.json
  - ~/work/project1/.claude/settings.json
```

### 最小化配置
```
事件选择: 1,3,4（核心事件）
配置文件: ~/.claude/settings.json
```

---

## 🔄 升级指南

### 从 0.1.x 升级到 0.2.0

1. **拉取最新代码**
   ```bash
   cd ~/ant_cc_dingding_notifier
   git pull
   ```

2. **重新运行配置**
   ```bash
   ./run.sh setup
   ```

3. **选择新的事件**
   - 推荐直接回车，使用默认的 8 个推荐事件
   - 或输入 `1,2,3,4,5,6,7,8`

4. **重新安装 Hooks**
   ```bash
   ./run.sh hooks install
   ```

5. **测试通知**
   ```bash
   ./run.sh test
   ```

### 配置迁移

旧版本的配置文件会自动兼容。新增的事件会自动添加到配置中，默认启用推荐的事件。

---

## 🛠️ 技术细节

### 代码变更

#### 1. `src/claude_dingtalk_notifier/config.py`
- 扩展 `__post_init__` 方法，初始化 12 个事件配置
- 新增事件：session_start, session_end, tool_failure, task_created, task_completed, cwd_changed, config_change, subagent_start, subagent_stop

#### 2. `src/claude_dingtalk_notifier/cli.py`
- 更新事件选择表格，从 4 个扩展到 12 个
- 修改事件选择逻辑，支持更多选项
- 更新 hooks_install 函数，生成所有 hook 脚本
- 扩展 _create_hook_scripts 函数，包含所有新 hook 的实现

#### 3. `src/claude_dingtalk_notifier/dingtalk.py`
- 扩展 format_claude_message 函数，支持所有新事件类型
- 为每个新事件添加专门的消息格式化逻辑
- 优化消息内容，提供更详细的上下文信息

#### 4. `src/claude_dingtalk_notifier/__init__.py`
- 版本号更新为 0.2.0

#### 5. `pyproject.toml`
- 版本号更新为 0.2.0

---

## 📚 相关文档

- **[HOOKS_EXPANSION.md](HOOKS_EXPANSION.md)** - Hook 扩展计划（已实现）
- **[CHANGELOG.md](CHANGELOG.md)** - 完整更新日志
- **[README.md](README.md)** - 项目说明（已更新）
- **[FEATURES.md](FEATURES.md)** - 功能特性说明
- **[QUICKSTART.md](QUICKSTART.md)** - 快速开始指南

---

## ✅ 总结

版本 0.2.0 是一次重大功能更新：

1. ✅ **Hook 事件从 4 个扩展到 12 个**
2. ✅ **新增会话管理、任务管理、工具失败等关键事件**
3. ✅ **改进配置界面，更清晰的事件分类**
4. ✅ **优化消息格式，提供更详细的上下文信息**
5. ✅ **保持向后兼容，旧配置自动迁移**

立即体验新功能：
```bash
cd ~/ant_cc_dingding_notifier
./run.sh setup
```

---

## 🙏 反馈

如果您在使用过程中遇到问题或有建议，请：
- 提交 Issue 到 GitHub
- 加入钉钉群反馈
- 查看文档获取帮助

感谢您的使用！🎉
