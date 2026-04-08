# 🔧 Hooks 配置格式修复总结

## 修复日期
2026-04-03

## 问题描述

### 问题 1: Hook 名称错误
- **错误**: 使用了不存在的 Hook 名称 `"error"`
- **影响**: Claude Code 无法识别此 Hook，导致功能无法正常工作
- **正确名称**: `"StopFailure"`

### 问题 2: Hooks 配置格式错误 ⚠️ 关键问题
- **错误格式**:
  ```json
  {
    "hooks": {
      "PreToolUse": "/path/to/hook.py"
    }
  }
  ```
- **错误信息**: "Invalid key in record" (所有 Hooks 都报错)
- **正确格式**:
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

## 修复内容

### 1. Hook 名称修复
- ✅ 将 `"error"` 更正为 `"stop_failure"` (对应 `StopFailure` Hook)
- ✅ 添加自动迁移逻辑：`config.py` 中自动将旧 "error" 配置迁移到 "stop_failure"
- ✅ 更新所有相关代码：CLI、配置、消息格式化、Hook 脚本生成

### 2. Hooks 配置格式修复 ⚠️ 关键修复
**文件**: `src/claude_dingtalk_notifier/cli.py`

### 3. Hook 脚本导入路径修复 ⚠️ 关键修复
**问题**: Hook 脚本无法导入 `claude_dingtalk_notifier` 包，导致 `NameError: name 'get_default_config' is not defined`

**原因**:
1. Hook 脚本的路径设置错误：`sys.path.insert(0, str(Path(__file__).parent.parent))` 指向错误的目录
2. 缺少 `EventConfig` 的导入
3. 导入失败时只是 `pass`，导致后续使用未定义的函数时报错

**修复**:
```python
# 修复前
sys.path.insert(0, str(Path(__file__).parent.parent))  # 指向 ~/.claude-dingtalk

# 修复后
package_path = Path(r"~/ant_cc_dingding_notifier/src")  # 正确指向 src 目录
if package_path.exists():
    sys.path.insert(0, str(package_path))

# 添加 EventConfig 导入
from claude_dingtalk_notifier.config import get_default_config, EventConfig

# 导入失败时优雅退出
except ImportError as e:
    print(f"Warning: Could not import claude_dingtalk_notifier: {e}", file=sys.stderr)
    sys.exit(0)
```

**测试**:
```bash
✓ Import successful!
✓ get_default_config: True
✓ EventConfig: <class 'claude_dingtalk_notifier.config.EventConfig'>
✓ Hook script loaded successfully!
```

### 4. Hooks 配置格式修复 ⚠️ 关键修复
**文件**: `src/claude_dingtalk_notifier/cli.py`

#### 修复 1: 添加缺失的导入
```python
# Line 15: 添加 EventConfig 导入
from .config import Config, EventConfig, get_default_config, find_claude_settings
```

#### 修复 2: 使用正确的 Hooks 格式
```python
# Lines 440-449: 生成正确的数组格式
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
```

#### 修复 3: 清理旧格式 Hooks
```python
# Lines 472-476: 自动清理旧格式
# Remove old format hooks (simple string values) and keep only new format (array values)
hooks_to_remove = [k for k, v in settings_data["hooks"].items() if isinstance(v, str)]
for hook_name in hooks_to_remove:
    del settings_data["hooks"][hook_name]
```

#### 修复 4: 修正变量引用
```python
# Line 476: 使用 enabled_hooks 而非未定义的 hooks_config
settings_data["hooks"].update(enabled_hooks)

# Lines 496-502: 更新显示逻辑
for hook_name, hook_config in enabled_hooks.items():
    if hook_config and len(hook_config) > 0:
        hooks_array = hook_config[0].get("hooks", [])
        if hooks_array and len(hooks_array) > 0:
            command_path = hooks_array[0].get("command", "未知")
            rprint(f"  - {hook_name}: {command_path}")
```

## 测试验证

### 1. Hooks 安装测试
```bash
$ PYTHONPATH=~/ant_cc_dingding_notifier/src python3 -m claude_dingtalk_notifier.cli hooks install

🔧 安装 Claude Code Hooks

处理配置文件: ~/.claude/settings.json
  ✓ Hooks 已安装 (备份: settings.json.backup)

✅ Hooks 安装完成！

已安装的 Hooks:
  - PreToolUse: ~/.claude-dingtalk/hooks/pre_tool_use.py
  - PostToolUseFailure: ~/.claude-dingtalk/hooks/tool_failure.py
  - Stop: ~/.claude-dingtalk/hooks/stop.py
  - StopFailure: ~/.claude-dingtalk/hooks/stop_failure.py
  - Notification: ~/.claude-dingtalk/hooks/notification.py
  - SessionEnd: ~/.claude-dingtalk/hooks/session_end.py
  - TaskCompleted: ~/.claude-dingtalk/hooks/task_completed.py
```

### 2. 配置文件验证
```bash
$ cat ~/.claude/settings.json | python3 -c "import json, sys; data = json.load(sys.stdin); hooks = data.get('hooks', {}); print('Total hooks:', len(hooks)); print('\\nFormat check:'); [print(f'  {k}: {\"✓ New format\" if isinstance(v, list) else \"✗ Old format\"}') for k,v in hooks.items()]"

Total hooks: 7

Format check:
  PreToolUse: ✓ New format
  Stop: ✓ New format
  SessionEnd: ✓ New format
  PostToolUseFailure: ✓ New format
  StopFailure: ✓ New format
  Notification: ✓ New format
  TaskCompleted: ✓ New format
```

### 3. 通知测试
```bash
$ PYTHONPATH=~/ant_cc_dingding_notifier/src python3 -m claude_dingtalk_notifier.cli test

🧪 测试钉钉通知

发送测试消息...
✓ 测试成功！请检查钉钉群消息
```

## 官方文档验证

根据 Claude Code 官方文档验证：
- **英文**: https://code.claude.com/docs/en/hooks
- **中文**: https://code.claude.com/docs/zh-CN/hooks

Claude Code 官方支持 **26 个 Hook**，当前实现支持 **14 个 Hook** (53.8%)。

### 已支持的 Hooks (14个)
1. **SessionStart** (`session_start`)
2. **SessionEnd** (`session_end`)
3. **PreToolUse** (`pre_tool_use`)
4. **PostToolUse** (`post_tool_use`)
5. **PostToolUseFailure** (`tool_failure`)
6. **Stop** (`stop`)
7. **StopFailure** (`stop_failure`) ⭐ [本次修复]
8. **Notification** (`notification`)
9. **TaskCreated** (`task_created`)
10. **TaskCompleted** (`task_completed`)
11. **CwdChanged** (`cwd_changed`)
12. **ConfigChange** (`config_change`)
13. **SubagentStart** (`subagent_start`)
14. **SubagentStop** (`subagent_stop`)

### 尚未支持的 Hooks (12个)
- UserPromptSubmit
- PermissionRequest, PermissionDenied
- TeammateIdle
- InstructionsLoaded
- FileChanged
- WorktreeCreate, WorktreeRemove
- PreCompact, PostCompact
- Elicitation, ElicitationResult

## 修改的文件

1. **src/claude_dingtalk_notifier/cli.py**
   - 添加 `EventConfig` 导入
   - 修复 Hook 配置格式
   - 添加清理旧格式逻辑
   - 更新显示逻辑

2. **src/claude_dingtalk_notifier/config.py**
   - 添加 "stop_failure" 到默认事件
   - 添加 "error" → "stop_failure" 迁移逻辑

3. **src/claude_dingtalk_notifier/dingtalk.py**
   - 添加 stop_failure 消息格式化

4. **src/claude_dingtalk_notifier/__init__.py**
   - 版本号更新: 0.2.0 → 0.2.1

5. **pyproject.toml**
   - 版本号更新: 0.2.0 → 0.2.1

6. **VERSION_0.2.1.md**
   - 添加 Hooks 格式修复说明
   - 更新配置示例

7. **CHANGELOG.md**
   - 添加 Hooks 格式修复条目

## 影响范围

### 修复前
- ❌ "error" Hook 无法工作 (不存在的 Hook)
- ❌ 所有 Hooks 显示 "Invalid key in record" 错误
- ❌ Claude Code 无法识别任何 Hook
- ❌ 通知功能完全无法使用

### 修复后
- ✅ 使用正确的 "StopFailure" Hook
- ✅ 所有 Hooks 使用正确的数组格式
- ✅ Claude Code 可以正常识别和执行 Hooks
- ✅ 通知功能完全正常
- ✅ 自动清理旧格式配置

## 升级建议

对于使用 0.2.1 初版的用户：

1. **拉取最新代码**
   ```bash
   git pull
   ```

2. **重新安装 Hooks**
   ```bash
   ./run.sh hooks install
   ```

3. **验证配置**
   ```bash
   cat ~/.claude/settings.json | grep -A 20 '"hooks"'
   ```

4. **测试通知**
   ```bash
   ./run.sh test
   ```

## 技术要点

### Claude Code Hooks 官方格式规范

根据官方文档，Hooks 配置必须遵循以下格式：

```json
{
  "hooks": {
    "HookName": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/hook/script"
          }
        ]
      }
    ]
  }
}
```

**关键点**:
1. Hook 名称使用 PascalCase (如 "PreToolUse")
2. 每个 Hook 是一个数组 `[]`
3. 数组包含对象，对象有 "hooks" 字段
4. "hooks" 字段值是命令数组
5. 每个命令包含 "type": "command" 和 "command" 字段
6. "command" 必须是绝对路径

## 后续计划

### 版本 0.3.0
- 添加剩余 12 个官方 Hook 支持
- 实现完整的 Hook 覆盖 (26/26 = 100%)

### 优先级
1. **高优先级**: UserPromptSubmit, PermissionRequest, PermissionDenied
2. **中优先级**: TeammateIdle, InstructionsLoaded, FileChanged
3. **低优先级**: Worktree, Compact, Elicitation 相关 Hooks

---

**修复完成时间**: 2026-04-03
**修复人员**: Claude
**测试状态**: ✅ 通过
**文档状态**: ✅ 已更新
