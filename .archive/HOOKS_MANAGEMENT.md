# 🔧 Hooks 管理指南

## 📋 可用的管理命令

### 1. `hooks list` - 列出所有可用的 Hooks

显示所有支持的 Hooks 及其当前状态。

**使用方法**:
```bash
python -m claude_dingtalk_notifier.cli hooks list
# 或
cdn hooks list
```

**输出示例**:
```
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Hook 名称         ┃ 事件标识          ┃ 说明                       ┃ 状态    ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ SessionStart      │ session_start     │ 会话开始时触发             │ ✓ 启用  │
│ SessionEnd        │ session_end       │ 会话结束时触发             │ ✓ 启用  │
│ PreToolUse        │ pre_tool_use      │ 工具使用前触发             │ ✓ 启用  │
│ Stop              │ stop              │ Claude 停止时触发          │ ✓ 启用  │
│ StopFailure       │ stop_failure      │ API 失败时触发             │ ✓ 启用  │
│ ...
└───────────────────┴───────────────────┴────────────────────────────┴─────────┘

Hook 脚本文件:
  ✓ pre_tool_use.py
  ✓ stop.py
  ✓ session_end.py
  ...
```

**功能**:
- ✓ 显示所有 14 个支持的 Hooks
- ✓ 显示每个 Hook 的说明
- ✓ 显示当前启用/禁用状态
- ✓ 列出已生成的 Hook 脚本文件

---

### 2. `hooks status` - 查看已安装的 Hooks 状态

显示 settings.json 中实际安装的 Hooks。

**使用方法**:
```bash
python -m claude_dingtalk_notifier.cli hooks status
# 或
cdn hooks status
```

**输出示例**:
```
📊 Hooks 状态

配置文件: ~/.claude/settings.json
  ✓ 已安装 Hooks:
    - PreToolUse: [{'hooks': [{'type': 'command', 'command': '.../pre_tool_use.py'}]}]
    - Stop: [{'hooks': [{'type': 'command', 'command': '.../stop.py'}]}]
    - SessionEnd: [{'hooks': [{'type': 'command', 'command': '.../session_end.py'}]}]
    ...

配置文件: ~/.claude/settings.json
  ✓ 已安装 Hooks:
    - PreToolUse: [{'matcher': 'WebSearch', 'hooks': [...]}]
    ...
```

**功能**:
- ✓ 显示每个 settings.json 中的 Hooks
- ✓ 显示完整的 Hook 配置（包括其他工具的 Hooks）
- ✓ 识别多个配置文件

---

### 3. `hooks remove` - 删除单个 Hook

从 settings.json 中删除指定的 Hook。

**使用方法**:
```bash
# 基本用法 - 只删除 settings.json 中的配置
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse

# 同时删除 hook 脚本文件
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --delete-script

# 或使用短命令
cdn hooks remove Stop
cdn hooks remove SessionEnd --delete-script
```

**可用的 Hook 名称**:
```
SessionStart, SessionEnd, PreToolUse, PostToolUse,
PostToolUseFailure, Stop, StopFailure, Notification,
TaskCreated, TaskCompleted, CwdChanged, ConfigChange,
SubagentStart, SubagentStop
```

**输出示例**:
```bash
$ cdn hooks remove PreToolUse

🗑️  删除 Hook: PreToolUse

处理配置文件: ~/.claude/settings.json
  ✓ Hook 已删除 (备份: settings.json.backup)
处理配置文件: ~/.claude/settings.json
  ✓ Hook 已删除 (备份: settings.json.backup)

✅ 成功从 2 个配置文件中删除 Hook
```

**功能**:
- ✓ 从指定的 settings.json 中删除单个 Hook
- ✓ 自动备份配置文件
- ✓ 可选：同时删除 Hook 脚本文件
- ✓ 支持多个配置文件

**选项**:
- `--delete-script`: 同时删除 hook 脚本文件

---

### 4. `hooks install` - 安装 Hooks

根据当前配置安装所有启用的 Hooks。

**使用方法**:
```bash
python -m claude_dingtalk_notifier.cli hooks install
# 或
cdn hooks install
```

**功能**:
- ✓ 生成所有 Hook 脚本
- ✓ 安装到 settings.json
- ✓ 只安装启用的 Hooks
- ✓ 自动清理旧格式的 Hooks
- ✓ 备份配置文件

---

### 5. `hooks uninstall` - 卸载所有 Hooks

删除所有已安装的 Hooks。

**使用方法**:
```bash
python -m claude_dingtalk_notifier.cli hooks uninstall
# 或
cdn hooks uninstall
```

**功能**:
- ✓ 删除 settings.json 中的所有 Hooks
- ✓ 保留 Hook 脚本文件
- ✓ 自动备份配置文件

---

## 🔒 备份与恢复

### 自动备份机制

**所有修改 settings.json 的操作都会自动创建备份！**

| 操作 | 备份文件 | 说明 |
|------|---------|------|
| `hooks install` | `settings.json.backup` | 安装前备份 |
| `hooks uninstall` | `settings.json.backup` | 卸载前备份 |
| `hooks remove <Hook>` | `settings.json.backup` | 删除前备份 |

### 查看备份

```bash
# 查看所有备份文件
find ~ -name "settings.json.backup"

# 查看特定备份
cat ~/.claude/settings.json.backup | python3 -m json.tool
```

### 恢复备份

```bash
# 恢复到备份状态
cp ~/.claude/settings.json.backup ~/.claude/settings.json

# 验证恢复
cdn hooks status
```

### 备份验证

```bash
# 检查备份完整性
python3 -m json.tool ~/.claude/settings.json.backup > /dev/null && echo "✓ 备份文件正常" || echo "✗ 备份文件损坏"
```

**重要**: 
- ✅ 每次操作都会自动备份，无需手动操作
- ✅ 备份文件会覆盖，只保留最后一次
- ✅ 如需保留历史，请手动创建带时间戳的备份

详细说明: [BACKUP_POLICY.md](BACKUP_POLICY.md)

---

## 🎯 常见使用场景

### 场景 1: 禁用某个 Hook 的通知

如果你不想接收某个特定 Hook 的通知（比如 PreToolUse），有两种方法：

**方法 1: 从配置中删除（推荐）**
```bash
# 删除 Hook 配置
cdn hooks remove PreToolUse

# Hook 脚本保留，但不会被调用
```

**方法 2: 修改配置文件**
```bash
# 重新配置
cdn setup

# 在事件选择时不选择该事件
```

### 场景 2: 临时禁用所有 Hooks

```bash
# 卸载所有 Hooks（保留脚本）
cdn hooks uninstall

# 需要时重新安装
cdn hooks install
```

### 场景 3: 清理不需要的 Hook 脚本

```bash
# 删除 Hook 配置和脚本
cdn hooks remove SessionStart --delete-script
cdn hooks remove SessionEnd --delete-script
cdn hooks remove CwdChanged --delete-script
```

### 场景 4: 查看哪些 Hooks 已启用

```bash
# 查看所有可用 Hooks 及状态
cdn hooks list

# 查看已安装的 Hooks
cdn hooks status
```

### 场景 5: 重置 Hooks 配置

```bash
# 1. 卸载所有 Hooks
cdn hooks uninstall

# 2. 重新配置
cdn setup

# 3. 重新安装
cdn hooks install
```

---

## 📊 Hooks 说明

### 会话管理

| Hook 名称 | 说明 | 推荐度 |
|----------|------|--------|
| **SessionStart** | Claude Code 会话开始时 | ⭐⭐ |
| **SessionEnd** | Claude Code 会话结束时 | ⭐⭐⭐ |

### 工具执行

| Hook 名称 | 说明 | 推荐度 |
|----------|------|--------|
| **PreToolUse** | 工具使用前（敏感操作检测） | ⭐⭐⭐ |
| **PostToolUse** | 工具使用后 | ⭐⭐ |
| **PostToolUseFailure** | 工具执行失败 | ⭐⭐⭐ |

### 停止事件

| Hook 名称 | 说明 | 推荐度 |
|----------|------|--------|
| **Stop** | Claude 正常停止 | ⭐⭐⭐ |
| **StopFailure** | API 调用失败 | ⭐⭐⭐ |

### 任务管理

| Hook 名称 | 说明 | 推荐度 |
|----------|------|--------|
| **TaskCreated** | 任务创建 | ⭐⭐ |
| **TaskCompleted** | 任务完成 | ⭐⭐⭐ |

### 其他

| Hook 名称 | 说明 | 推荐度 |
|----------|------|--------|
| **Notification** | 通知消息 | ⭐ |
| **CwdChanged** | 目录切换 | ⭐ |
| **ConfigChange** | 配置更改 | ⭐ |
| **SubagentStart** | 子代理启动 | ⭐ |
| **SubagentStop** | 子代理完成 | ⭐ |

---

## ⚠️ 注意事项

### 1. 备份自动创建
所有修改配置文件的操作都会自动创建 `.backup` 文件：
```bash
settings.json → settings.json.backup
```

### 2. 多配置文件
如果有多个 settings.json 文件，操作会应用到所有文件：
```bash
# 会同时处理:
# - ~/.claude/settings.json
# - ~/.claude/settings.json
```

### 3. Hook 脚本与配置分离
- **删除配置** (`hooks remove`): 只从 settings.json 删除，脚本保留
- **删除脚本** (`--delete-script`): 同时删除脚本文件
- **建议**: 除非确定不再需要，否则只删除配置

### 4. 删除前确认
删除 Hook 前，建议先查看状态：
```bash
# 1. 查看已安装的 Hooks
cdn hooks status

# 2. 确认要删除的 Hook
cdn hooks remove HookName
```

---

## 🔍 故障排查

### 问题 1: Hook 仍然触发

**原因**: Hook 配置已删除，但脚本文件仍存在

**解决**:
```bash
# 检查状态
cdn hooks status

# 如果配置已删除但仍然触发，检查是否有其他配置文件
# 或删除脚本
cdn hooks remove HookName --delete-script
```

### 问题 2: 删除后 Hook 仍在 status 中显示

**原因**: 可能有多个 settings.json 文件

**解决**:
```bash
# 查看所有配置文件的 Hooks
cdn hooks status

# 从所有配置文件中删除
cdn hooks remove HookName
```

### 问题 3: 找不到 Hook 名称

**原因**: Hook 名称拼写错误

**解决**:
```bash
# 查看所有可用的 Hook 名称
cdn hooks list

# 使用正确的 Hook 名称（注意大小写）
# 正确: PreToolUse
# 错误: preToolUse, PreTooluse, pre_tool_use
```

---

## 💡 最佳实践

### 1. 定期清理
定期检查并清理不需要的 Hooks：
```bash
# 查看状态
cdn hooks status

# 删除不需要的
cdn hooks remove UnnecessaryHook --delete-script
```

### 2. 备份管理
定期清理旧的备份文件：
```bash
# 删除备份
rm ~/.claude/settings.json.backup
```

### 3. 测试配置
修改配置后测试：
```bash
# 重新安装
cdn hooks install

# 测试通知
cdn test
```

### 4. 文档记录
记录自定义的 Hook 配置：
```bash
# 导出当前配置
cat ~/.claude-dingtalk/config.yaml

# 保存到文件
cdn hooks status > my-hooks-status.txt
```

---

## 🚀 快速参考

```bash
# 查看所有可用的 Hooks
cdn hooks list

# 查看已安装的 Hooks
cdn hooks status

# 删除单个 Hook
cdn hooks remove HookName

# 删除 Hook 和脚本
cdn hooks remove HookName --delete-script

# 安装所有 Hooks
cdn hooks install

# 卸载所有 Hooks
cdn hooks uninstall

# 测试通知
cdn test
```

---

**总结**: 现在您有完整的 Hook 管理功能，可以灵活地启用、禁用和删除单个 Hook，满足各种使用场景的需求。
