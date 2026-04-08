# 🔒 Hooks 安全卸载说明

## ⚠️ 重要修复：保护其他应用的 Hooks

### 问题描述

之前的版本在卸载 hooks 时存在**严重的安全问题**：

```python
# ❌ 危险的旧代码
del settings_data["hooks"]  # 删除所有 hooks！
```

**影响**：
- ❌ 会删除 **所有应用的 hooks**（包括 codefuse、其他工具）
- ❌ 导致其他应用的功能失效
- ❌ 用户需要重新配置所有 hooks

### 示例场景

用户的 `settings.json` 中有两类 hooks：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "WebSearch",
        "hooks": [{
          "type": "command",
          "command": "~/.codefuse/fuse/engine/hooks/mac-arm64/cfuse-hook-cli cc_PreToolUse"
        }]
      },
      {
        "hooks": [{
          "type": "command",
          "command": "~/.claude-dingtalk/hooks/pre_tool_use.py"
        }]
      }
    ]
  }
}
```

**旧版本行为**：
- 运行 `cdn hooks remove PreToolUse`
- ❌ **整个 `PreToolUse` 被删除**
- ❌ codefuse 的 PreToolUse hook 也被删除
- ❌ codefuse 功能失效

---

## ✅ 修复后的行为

### 安全的卸载逻辑

**新版本**（v0.2.1+）会智能识别并只删除 claude-dingtalk 的 hooks：

```python
# ✅ 安全的新代码
# 1. 遍历所有 hooks
# 2. 检查命令路径是否包含 ".claude-dingtalk/hooks/"
# 3. 只删除匹配的 hooks
# 4. 保留其他应用的 hooks
```

### `hooks uninstall` 命令

**行为**：只删除 claude-dingtalk 的所有 hooks

```bash
$ cdn hooks uninstall

处理配置文件: ~/.claude/settings.json
  ✓ 已删除 7 个 claude-dingtalk hooks (保留其他应用的 hooks)

处理配置文件: ~/.claude/settings.json
  ✓ 已删除 7 个 claude-dingtalk hooks (保留其他应用的 hooks)
```

**结果**：
- ✅ claude-dingtalk 的 hooks 被删除
- ✅ codefuse 的 hooks 完好无损
- ✅ 其他应用的 hooks 完好无损

### `hooks remove <HookName>` 命令

**行为**：智能处理单个 hook 的删除

#### 场景 1: 只有一个来源的 hook

如果 `PreToolUse` 只有 claude-dingtalk 使用：

```bash
$ cdn hooks remove PreToolUse

处理配置文件: ~/.claude/settings.json
  ✓ Hook 已删除
```

**结果**：整个 `PreToolUse` 被删除（因为没有其他应用使用）

#### 场景 2: 多个来源的 hook（重要！）⭐

如果 `PreToolUse` 被 claude-dingtalk 和 codefuse 同时使用：

```bash
$ cdn hooks remove PreToolUse

处理配置文件: ~/.claude/settings.json
  ✓ 已删除 claude-dingtalk 的 PreToolUse hook (保留其他应用的 hook)
```

**结果**：
- ✅ claude-dingtalk 的 PreToolUse 被删除
- ✅ codefuse 的 PreToolUse **保留**
- ✅ PreToolUse hook 配置仍然存在（包含 codefuse 的配置）

---

## 🔍 技术实现

### 识别策略

通过检查 **命令路径** 来识别 hook 的归属：

```python
# 判断是否为 claude-dingtalk 的 hook
if ".claude-dingtalk/hooks/" in command:
    # 这是我们的 hook，可以删除
else:
    # 这是其他应用的 hook，必须保留
```

### 过滤逻辑

```python
# 伪代码
for hook_name, hook_configs in settings_data["hooks"].items():
    filtered_configs = []
    
    for hook_config in hook_configs:
        if is_claude_dingtalk_hook(hook_config):
            # 跳过（删除）
            continue
        else:
            # 保留
            filtered_configs.append(hook_config)
    
    # 更新配置（只保留其他应用的 hooks）
    settings_data["hooks"][hook_name] = filtered_configs
```

---

## 📊 安全对比

| 场景 | 旧版本 | 新版本 |
|------|--------|--------|
| **卸载所有 hooks** | ❌ 删除所有应用 | ✅ 只删除 claude-dingtalk |
| **删除单个 hook（独占）** | ✅ 正常删除 | ✅ 正常删除 |
| **删除单个 hook（共享）** | ❌ 删除所有应用 | ✅ 只删除 claude-dingtalk |
| **其他应用功能** | ❌ 会受影响 | ✅ 不受影响 |

---

## 🎯 使用建议

### 1. 卸载前查看状态

```bash
# 查看已安装的 hooks
cdn hooks status

# 确认哪些是 claude-dingtalk 的
# 路径包含 ".claude-dingtalk/hooks/"
```

### 2. 交互式删除（推荐）

```bash
# 交互式选择，安全删除
cdn hooks remove PreToolUse
```

**优点**：
- 清晰显示哪些配置文件被修改
- 可以选择特定配置文件
- 看到详细的结果反馈

### 3. 备份自动创建

所有修改操作都会自动创建备份：

```bash
settings.json → settings.json.backup
```

如果误操作，可以恢复：

```bash
cp /path/to/settings.json.backup /path/to/settings.json
```

---

## 🧪 测试验证

### 测试场景 1: 删除 claude-dingtalk hooks（保留 codefuse）

```bash
# 1. 查看当前状态
cdn hooks status

# 2. 删除某个 hook
cdn hooks remove PreToolUse

# 3. 验证 codefuse hooks 仍然存在
cat ~/.claude/settings.json | grep -A 10 "PreToolUse"
```

**预期结果**：
- ✅ claude-dingtalk 的 PreToolUse 被删除
- ✅ codefuse 的 PreToolUse 仍然存在

### 测试场景 2: 完全卸载

```bash
# 卸载所有 claude-dingtalk hooks
cdn hooks uninstall

# 验证其他应用的 hooks
cdn hooks status
```

**预期结果**：
- ✅ claude-dingtalk 的所有 hooks 被删除
- ✅ 其他应用的 hooks 仍然存在

---

## 🔒 安全保障

### 1. 路径检查

只删除路径包含 `.claude-dingtalk/hooks/` 的 hooks

### 2. 备份保护

每次操作都创建 `.backup` 文件

### 3. 详细日志

清晰显示哪些 hooks 被删除，哪些被保留

### 4. 交互确认

默认使用交互式选择，避免误操作

---

## 📝 总结

### 关键改进

✅ **安全优先**：只删除自己的 hooks
✅ **保护其他应用**：不影响 codefuse 等其他工具
✅ **智能识别**：通过路径准确判断 hook 归属
✅ **自动备份**：防止误操作
✅ **清晰反馈**：详细显示操作结果

### 团队使用

现在可以**安全地**在团队中使用：

- ✅ 不会影响其他成员的 hooks 配置
- ✅ 不会破坏其他应用的功能
- ✅ 可以随时卸载或删除特定 hooks

---

**重要**: 这是 v0.2.1 的关键安全修复！如果团队成员使用旧版本，请立即更新！
