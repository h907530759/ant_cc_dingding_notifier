# 🔒 Hook 识别逻辑与安全保障

## 🎯 核心问题

**如何保证删除 hook 时不会删除别的程序的 hook？**

---

## 📋 实际配置分析

### 真实的 settings.json 结构

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "WebSearch",
        "hooks": [{
          "type": "command",
          "command": "~/.codefuse/fuse/engine/hooks/mac-arm64/cfuse-hook-cli cc_PreToolUse",
          "timeout": 30
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

**两个来源**：
1. **codefuse**: 路径包含 `.codefuse/fuse/engine/hooks/`
2. **claude-dingtalk**: 路径包含 `.claude-dingtalk/hooks/`

---

## 🔍 识别逻辑

### 路径特征分析

| 程序 | 路径特征 | 唯一标识 |
|------|---------|---------|
| **claude-dingtalk** | `~/.claude-dingtalk/hooks/` | ✅ `.claude-dingtalk/hooks/` |
| **codefuse** | `~/.codefuse/fuse/engine/hooks/` | ✅ `.codefuse/fuse/` |
| **其他工具** | 通常是 `/usr/local/bin/` 或其他 | 各不相同 |

### 识别代码

```python
def is_claude_dingtalk_hook(hook_config):
    """检查是否为 claude-dingtalk 的 hook"""
    
    # 获取 hooks 数组
    hook_list = hook_config.get("hooks", [])
    
    # 检查每个 hook item
    for hook_item in hook_list:
        if isinstance(hook_item, dict):
            command = hook_item.get("command", "")
            
            # 关键判断：路径必须包含 .claude-dingtalk/hooks/
            if ".claude-dingtalk/hooks/" in command:
                return True  # 这是我们的 hook
    
    return False  # 这是其他程序的 hook
```

---

## 🛡️ 安全保证

### 保证 1: 路径唯一性

**特征**: claude-dingtalk 的 hook 脚本都安装在 `~/.claude-dingtalk/hooks/` 目录

```bash
# 检查安装位置
ls -la ~/.claude-dingtalk/hooks/
# pre_tool_use.py
# stop.py
# session_end.py
# ...
```

**保证**: 其他程序不会使用这个目录。

### 保证 2: 路径检查

**逻辑**: 只有路径包含 `.claude-dingtalk/hooks/` 的才会被删除

```python
# ✅ 会删除
if ".claude-dingtalk/hooks/" in command:
    # 删除

# ✅ 会保留
if ".codefuse/" in command:
    # 保留（不包含 .claude-dingtalk/hooks/）

if "/usr/local/bin/" in command:
    # 保留（不包含 .claude-dingtalk/hooks/）
```

### 保证 3: 精确匹配

使用 **子字符串匹配**，而不是模糊匹配：

```python
# ✅ 正确：精确子字符串匹配
if ".claude-dingtalk/hooks/" in command:
    # 只匹配完整的路径特征

# ❌ 危险：模糊匹配（不使用）
if "claude" in command:
    # 可能匹配到其他包含 "claude" 的路径
```

---

## 🧪 实际测试

### 测试 1: 识别准确性

```bash
# 查看 PreToolUse 的所有配置
cat ~/.claude/settings.json | python3 -m json.tool | grep -A 10 "PreToolUse"
```

**结果**：
```json
"PreToolUse": [
  {
    "hooks": [{
      "command": "~/.codefuse/fuse/engine/hooks/.../cfuse-hook-cli cc_PreToolUse"
    }]
  },
  {
    "hooks": [{
      "command": "~/.claude-dingtalk/hooks/pre_tool_use.py"
    }]
  }
]
```

**识别**：
- ✅ codefuse hook: 路径不包含 `.claude-dingtalk/hooks/` → 保留
- ✅ claude-dingtalk hook: 路径包含 `.claude-dingtalk/hooks/` → 删除

### 测试 2: 删除操作验证

```bash
# 执行删除
cdn hooks remove PreToolUse

# 查看结果
cat ~/.claude/settings.json | python3 -m json.tool | grep -A 10 "PreToolUse"
```

**预期结果**：
```json
"PreToolUse": [
  {
    "matcher": "WebSearch",
    "hooks": [{
      "type": "command",
      "command": "~/.codefuse/fuse/engine/hooks/.../cfuse-hook-cli cc_PreToolUse"
    }]
  }
]
```

**验证**：
- ✅ claude-dingtalk 的 PreToolUse 被删除
- ✅ codefuse 的 PreToolUse 被保留
- ✅ codefuse 功能不受影响

---

## 🔒 多层保障

### 保障 1: 路径特征

```python
# 唯一的路径特征
CLAUDE_DINGTALK_PATH_MARKER = ".claude-dingtalk/hooks/"
```

### 保障 2: 目录约定

```bash
# 安装约定
所有 hook 脚本安装到：~/.claude-dingtalk/hooks/

# 路径格式
~/.claude-dingtalk/hooks/<event_name>.py
```

### 保障 3: 备份保护

```python
# 删除前自动备份
backup_path = settings_path.with_suffix('.json.backup')
with open(backup_path, 'w') as f:
    json.dump(settings_data, f)  # 备份原始配置
```

如果误删除，可以立即恢复。

---

## 📊 路径对比表

| 程序 | Hook 路径 | 包含特征 | 是否删除 |
|------|----------|---------|---------|
| **claude-dingtalk** | `~/.claude-dingtalk/hooks/pre_tool_use.py` | ✅ `.claude-dingtalk/hooks/` | ✅ 删除 |
| **codefuse** | `~/.codefuse/fuse/engine/hooks/.../cfuse-hook-cli` | ❌ 不包含 | ✅ 保留 |
| **其他工具 A** | `/usr/local/bin/tool-hook.sh` | ❌ 不包含 | ✅ 保留 |
| **其他工具 B** | `~/.myapp/hooks/hook.py` | ❌ 不包含 | ✅ 保留 |

---

## 🎯 关键特征

### 唯一性保证

1. **目录名称唯一**: `.claude-dingtalk/`
2. **子目录固定**: `hooks/`
3. **完整路径**: `.claude-dingtalk/hooks/`

**其他程序不太可能使用这个路径**，因为：
- 目录名包含项目名称 `claude-dingtalk`
- 不是通用的目录名（如 `hooks/`、`bin/`）
- 有明确的项目归属

### 冲突概率

假设其他程序也使用类似的路径：

```python
# 冲突场景（极不可能）
其他程序路径: /some/path/.claude-dingtalk/hooks/hook.py
```

**即使发生冲突**：
- 该其他程序违反了命名约定
- 应该使用自己的目录名（如 `.otherapp/hooks/`）
- 这是程序本身的配置问题

---

## 🔬 验证方法

### 方法 1: 检查备份

```bash
# 删除前
ls -lh ~/.claude/settings.json.backup

# 删除后
cat ~/.claude/settings.json.backup | python3 -m json.tool | grep "codefuse"
# 应该能看到 codefuse 的配置
```

### 方法 2: 对比差异

```bash
# 备份
cp ~/.claude/settings.json ~/.claude/settings.json.before

# 删除操作
cdn hooks remove PreToolUse

# 对比
diff ~/.claude/settings.json.before ~/.claude/settings.json
```

**应该看到**：
- 删除了包含 `.claude-dingtalk/hooks/` 的行
- 保留了其他路径的行

### 方法 3: 功能验证

```bash
# 删除 claude-dingtalk hooks
cdn hooks uninstall

# 验证 codefuse 仍能工作
# codefuse 功能应该正常
```

---

## 💇 如果出现误删除怎么办？

### 立即恢复

```bash
# 从备份恢复
cp ~/.claude/settings.json.backup ~/.claude/settings.json

# 重新安装
cdn hooks install
```

### 验证恢复

```bash
# 检查所有 hooks 都恢复
cdn hooks status

# 验证其他程序正常工作
```

---

## ✅ 总结

### 识别机制

**核心**: 通过**路径特征**识别 hook 的归属

```python
if ".claude-dingtalk/hooks/" in command:
    return IS_CLAUDE_DINGTALK
else:
    return IS_OTHER_APP
```

### 安全保证

✅ **路径唯一性** - `.claude-dingtalk/hooks/` 是唯一的
✅ **精确匹配** - 使用子字符串匹配，不模糊
✅ **自动备份** - 删除前自动备份
✅ **可恢复** - 一条命令恢复

### 实际验证

通过实际的 settings.json 可以看到：
- ✅ codefuse hooks 路径：`.codefuse/fuse/engine/hooks/...`
- ✅ claude-dingtalk hooks 路径：`.claude-dingtalk/hooks/...`
- ✅ 路径特征完全不同，不会混淆

### 团队使用

可以放心使用，因为：
1. 路径特征是唯一的
2. 识别逻辑是精确的
3. 有自动备份保护
4. 可以随时恢复

---

**结论**: 通过路径特征识别 + 自动备份，可以安全地只删除自己的 hooks！✅
