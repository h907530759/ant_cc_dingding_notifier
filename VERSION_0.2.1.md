# 🐛 版本 0.2.1 更新说明 - Bug 修复

## 📋 更新概览

**发布日期**: 2026-04-03
**版本**: 0.2.1
**类型**: Bug 修复版

---

## 🐛 关键 Bug 修复

### Hook 名称错误修复

**问题**: 在版本 0.2.0 中，我们使用了一个不存在的 Hook 名称 `"error"`，但这不是 Claude Code 官方支持的 Hook。

**修复**: 根据 Claude Code 官方文档验证，正确的 Hook 名称应该是 **`StopFailure`**（而非 "error"）。

**影响**:
- ❌ 旧版本的 "error" Hook 无法正常工作（因为 Claude Code 不认识这个 Hook）
- ✅ 新版本的 "stop_failure" Hook 使用官方支持的 `StopFailure` Hook
- ✅ 自动迁移：已有配置文件会自动将 "error" 设置迁移到 "stop_failure"

### Hooks 配置格式错误修复 ⚠️ **关键修复**

**问题**: 在版本 0.2.1 初次发布时，Hooks 配置使用了错误的格式，导致所有 Hooks 显示 "Invalid key in record" 错误。

**错误格式** (0.2.1 初版):
```json
{
  "hooks": {
    "PreToolUse": "/path/to/hook.py"
  }
}
```

**正确格式** (0.2.1 修复版):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hook.py"
          }
        ]
      }
    ]
  }
}
```

**修复内容**:
1. ✅ 修改 `hooks_install()` 函数，使用正确的数组格式
2. ✅ 添加自动清理旧格式 Hooks 的逻辑
3. ✅ 添加缺失的 `EventConfig` 导入
4. ✅ 更新 hooks 显示逻辑以正确提取命令路径

**影响**:
- ❌ 旧格式 Hooks 不会被 Claude Code 识别，全部显示 "Invalid key in record" 错误
- ✅ 新格式 Hooks 符合 Claude Code 官方规范，可以正常工作
- ✅ 自动清理：重新安装 Hooks 会自动删除旧格式的配置

### Hook 脚本导入路径修复 ⚠️ **关键修复**

**问题**: Hook 脚本执行时出现 `NameError: name 'get_default_config' is not defined` 错误。

**原因**:
1. Hook 脚本的 Python 路径设置错误，无法找到 `claude_dingtalk_notifier` 包
2. 缺少 `EventConfig` 类的导入
3. 导入失败时的错误处理不当（只是 `pass`，导致后续使用未定义函数时报错）

**错误代码**:
```python
# 错误的路径设置
sys.path.insert(0, str(Path(__file__).parent.parent))  # 指向 ~/.claude-dingtalk

# 缺少 EventConfig 导入
from claude_dingtalk_notifier.config import get_default_config  # 缺少 EventConfig

# 导入失败时只是 pass
except ImportError:
    pass  # 导致后续使用 get_default_config 时报 NameError
```

**修复代码**:
```python
# 正确的路径设置（指向 src 目录）
package_path = Path(r"/Users/suchen/workspace/claude_notifyer/src")
if package_path.exists():
    sys.path.insert(0, str(package_path))

# 添加 EventConfig 导入
from claude_dingtalk_notifier.config import get_default_config, EventConfig

# 导入失败时优雅退出
except ImportError as e:
    print(f"Warning: Could not import claude_dingtalk_notifier: {e}", file=sys.stderr)
    sys.exit(0)  # 优雅退出，避免中断 Claude Code
```

**影响**:
- ❌ 修复前：Hook 脚本无法运行，所有 Hooks 执行失败并报错
- ✅ 修复后：Hook 脚本可以正常导入和执行

---

## 📚 官方文档验证

参考以下 Claude Code 官方文档进行验证：
- **英文**: https://code.claude.com/docs/en/hooks
- **中文**: https://code.claude.com/docs/zh-CN/hooks

Claude Code 官方支持 **26 个 Hook**，本次修复确保我们的实现与官方规范一致。

---

## 🔄 具体变更

### 1. CLI 事件列表更新

**文件**: `src/claude_dingtalk_notifier/cli.py`

```python
# 旧版本 (错误)
("error", "error", "错误通知", "Claude 错误通知", "⭐ 推荐"),

# 新版本 (正确)
("stop_failure", "stopFailure", "API失败时触发", "Claude API调用失败", "⭐ 推荐"),
```

### 2. Hook 配置更新

在 `hooks_install()` 函数中添加正确的 Hook 配置：

```python
hooks_config = {
    # ... 其他 hooks ...
    "stopFailure": str(hook_dir / "stop_failure.py"),  # 新增
}
```

### 3. Hook 脚本生成

自动生成 `stop_failure.py` Hook 脚本，位于 `~/.claude-dingtalk/hooks/stop_failure.py`。

### 4. 配置文件更新

**默认事件配置** (config.py):
- 新增 `"stop_failure": EventConfig(enabled=True)`

**自动迁移逻辑**:
```python
# 迁移旧的 "error" 事件到 "stop_failure"
if "error" in self.events:
    if "stop_failure" not in self.events:
        self.events["stop_failure"] = self.events["error"]
    del self.events["error"]
```

### 5. 消息格式化

添加 `stop_failure` 事件的消息格式化逻辑：

```python
elif event_type == "stop_failure":
    error = data.get("error", "Unknown error")
    project = data.get("project", "Unknown")

    return DingTalkMessage(
        title="💥 Claude Code API失败",
        text=f"""### 💥 Claude Code API调用失败

**📂 项目:** {project}
**❌ 错误信息:** ```
{error[:500]}
```

💡 Claude Code encountered an API error and had to stop""",
        msg_type="markdown"
    )
```

---

## 📋 当前支持的 Hooks (14/26)

### ✅ 已支持的 Hooks (14个)

1. **SessionStart** (`session_start`) - 会话开始
2. **SessionEnd** (`session_end`) - 会话结束
3. **PreToolUse** (`pre_tool_use`) - 工具使用前
4. **PostToolUse** (`post_tool_use`) - 工具使用后
5. **PostToolUseFailure** (`tool_failure`) - 工具执行失败
6. **Stop** (`stop`) - 停止事件
7. **StopFailure** (`stop_failure`) - API失败 ⭐ **[本次修复]**
8. **Notification** (`notification`) - 通知消息
9. **TaskCreated** (`task_created`) - 任务创建
10. **TaskCompleted** (`task_completed`) - 任务完成
11. **CwdChanged** (`cwd_changed`) - 目录切换
12. **ConfigChange** (`config_change`) - 配置更改
13. **SubagentStart** (`subagent_start`) - 子代理启动
14. **SubagentStop** (`subagent_stop`) - 子代理完成

### ❌ 尚未支持的 Hooks (12个)

以下官方 Hook 暂未实现，计划在未来版本中添加：

**高优先级**:
- UserPromptSubmit - 用户提交提示
- PermissionRequest - 权限请求
- PermissionDenied - 权限拒绝
- TeammateIdle - 队友空闲
- InstructionsLoaded - 指令加载

**中优先级**:
- FileChanged - 文件更改
- WorktreeCreate - 工作树创建
- WorktreeRemove - 工作树移除
- PreCompact - 预压缩
- PostCompact - 后压缩

**低优先级**:
- Elicitation - 功能启发
- ElicitationResult - 功能启发结果

---

## 🚀 升级指南

### 从 0.2.0 升级到 0.2.1

1. **拉取最新代码**
   ```bash
   cd /Users/suchen/workspace/claude_notifyer
   git pull
   ```

2. **重新配置** (推荐)
   ```bash
   ./run.sh setup
   ```
   - 现在事件列表中 "error" 已被替换为 "stop_failure"
   - 推荐事件 (1-8) 现在包括 `stop_failure`

3. **重新安装 Hooks**
   ```bash
   ./run.sh hooks install
   ```
   - 这会在 settings.json 中安装正确的 `stopFailure` Hook
   - 旧的 "error" Hook (如果存在) 会被移除

4. **验证配置**
   ```bash
   ./run.sh status
   ```

5. **测试通知**
   ```bash
   ./run.sh test
   ```

### 自动迁移

如果您的配置文件中包含旧的 `"error"` 事件设置，系统会自动将其迁移到 `"stop_failure"`。

**迁移示例**:
```yaml
# 旧配置 (0.2.0)
events:
  error:
    enabled: true
    channels:
      - dingtalk

# 自动迁移后 (0.2.1)
events:
  stop_failure:
    enabled: true
    channels:
      - dingtalk
```

---

## 🔧 技术细节

### 修改的文件

1. **src/claude_dingtalk_notifier/__init__.py**
   - 版本号更新: 0.2.0 → 0.2.1

2. **src/claude_dingtalk_notifier/cli.py**
   - 事件列表: "error" → "stop_failure"
   - Hooks 配置格式: 修复为符合 Claude Code 官方规范的数组格式 ⚠️
   - 添加缺失的 `EventConfig` 导入 ⚠️
   - 自动清理旧格式 Hooks 的逻辑 ⚠️
   - Hook 脚本: 添加 stop_failure_hook 模板
   - 版本号更新: 0.2.0 → 0.2.1

3. **src/claude_dingtalk_notifier/config.py**
   - 默认事件: 添加 "stop_failure"
   - 迁移逻辑: 自动将 "error" 迁移到 "stop_failure"

4. **src/claude_dingtalk_notifier/dingtalk.py**
   - 消息格式化: 添加 "stop_failure" 处理

5. **pyproject.toml**
   - 版本号更新: 0.2.0 → 0.2.1

### 配置文件变更

**settings.json Hooks 配置** (符合 Claude Code 官方格式):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/pre_tool_use.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/post_tool_use.py"
          }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/tool_failure.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/stop.py"
          }
        ]
      }
    ],
    "StopFailure": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/stop_failure.py"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/session_start.py"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/session_end.py"
          }
        ]
      }
    ],
    "TaskCreated": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/task_created.py"
          }
        ]
      }
    ],
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/task_completed.py"
          }
        ]
      }
    ],
    "CwdChanged": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/cwd_changed.py"
          }
        ]
      }
    ],
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/config_change.py"
          }
        ]
      }
    ],
    "SubagentStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/subagent_start.py"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/suchen/.claude-dingtalk/hooks/subagent_stop.py"
          }
        ]
      }
    ]
  }
}
```

**重要**: 此格式符合 Claude Code 官方文档规范：
- Hook 名称使用 PascalCase (如 "PreToolUse")
- 每个Hook是一个数组，包含对象结构
- 对象包含 "hooks" 字段，值为命令数组
- 每个命令包含 "type": "command" 和 "command" 字段

---

## ✅ 测试验证

### 1. Hook 脚本生成测试

```bash
# 安装 hooks
./run.sh hooks install

# 检查 stop_failure.py 是否生成
ls -la ~/.claude-dingtalk/hooks/stop_failure.py
# 应该显示文件存在且权限为 -rwxr-xr-x (0o755)
```

### 2. 配置文件测试

```bash
# 检查 settings.json 中的 hooks 配置
cat ~/.claude/settings.json | grep -A 15 '"hooks"'
# 应该包含 "stopFailure": "~/.claude-dingtalk/hooks/stop_failure.py"
```

### 3. 配置迁移测试

```bash
# 如果有旧的配置 (包含 error 事件)
cat ~/.claude-dingtalk/config.yaml | grep -A 3 'stop_failure'
# 应该看到 stop_failure 事件配置

# 旧的 error 事件应该已自动迁移并删除
cat ~/.claude-dingtalk/config.yaml | grep 'error'
# 应该没有输出（已删除）
```

### 4. 通知测试

```bash
# 测试钉钉通知
./run.sh test
# 应该收到测试消息
```

---

## 📊 官方 Hook 覆盖率

**当前进度**: 14/26 hooks 支持 (53.8%)

| Hook 类别 | 已支持 | 总数 | 覆盖率 |
|----------|--------|------|--------|
| 会话管理 | 2 | 2 | 100% |
| 用户交互 | 0 | 1 | 0% |
| 工具执行 | 3 | 5 | 60% |
| 通知 | 1 | 1 | 100% |
| 子代理 | 2 | 2 | 100% |
| 任务管理 | 2 | 2 | 100% |
| 停止事件 | 2/2 | 2 | 100% ⭐ |
| 团队协作 | 0 | 1 | 0% |
| 文档 | 0 | 1 | 0% |
| 配置 | 2 | 2 | 100% |
| 文件监控 | 0 | 1 | 0% |
| 工作树 | 0 | 2 | 0% |
| 压缩 | 0 | 2 | 0% |
| MCP | 0 | 2 | 0% |

---

## 🙏 致谢

感谢 Claude Code 官方文档提供的详细 Hook 规范：
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/zh-CN/hooks

本次修复确保了我们的实现与官方规范完全一致。

---

## 📝 后续计划

### 版本 0.3.0 计划

计划添加剩余的 12 个官方 Hook 支持，特别是高优先级的 Hooks：
- UserPromptSubmit
- PermissionRequest / PermissionDenied
- TeammateIdle
- InstructionsLoaded

目标是实现对所有 26 个官方 Hook 的 100% 覆盖。

---

**感谢您的使用和支持！🎉**
