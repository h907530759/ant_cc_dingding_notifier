# 💾 自动备份机制说明

## 🎯 核心原则

**所有修改 settings.json 的操作都会自动创建备份！**

---

## 📋 备份策略

### 备份文件命名

```bash
<settings文件路径>.json.backup
```

**示例**：
- `~/.claude/settings.json` → `~/.claude/settings.json.backup`
- `~/.claude/settings.json` → `~/.claude/settings.json.backup`

### 备份时机

**每次修改 settings.json 前都会备份**：
- ✅ 安装 hooks 前
- ✅ 卸载 hooks 前
- ✅ 删除单个 hook 前
- ✅ 修改任何 hook 配置前

---

## 🔒 备份保障

### 1. 自动备份

所有操作自动创建备份，无需手动干预。

```python
# 伪代码
backup_path = settings_path.with_suffix('.json.backup')

# 1. 先备份
with open(backup_path, 'w') as f:
    json.dump(settings_data, f)

# 2. 再修改
with open(settings_path, 'w') as f:
    json.dump(new_settings_data, f)
```

### 2. 备份覆盖

每次操作会**覆盖**之前的备份文件（不是追加）。

**示例**：
```bash
# 第1次操作
settings.json.backup  # 包含第1次操作前的状态

# 第2次操作
settings.json.backup  # 包含第2次操作前的状态（覆盖第1次）
```

### 3. 多文件独立备份

每个 settings.json 文件都有独立的备份：

```bash
~/.claude/settings.json.backup
~/.claude/settings.json.backup
/path/to/other/settings.json.backup
```

---

## 📊 备份覆盖范围

### ✅ 有备份的操作

| 操作 | 备份 | 说明 |
|------|------|------|
| **hooks install** | ✅ | 安装前备份 |
| **hooks uninstall** | ✅ | 卸载前备份 |
| **hooks remove** | ✅ | 删除前备份 |
| **hooks remove <HookName>** | ✅ | 删除单个 hook 前备份 |

### 📝 备份位置

备份文件与原文件在同一目录：

```bash
原文件: ~/.claude/settings.json
备份文件: ~/.claude/settings.json.backup
```

---

## 🔄 从备份恢复

### 情况 1: 误操作恢复

```bash
# 查看所有备份
ls -la ~/.claude/settings.json.backup
ls -la ~/.claude/settings.json.backup

# 恢复备份
cp ~/.claude/settings.json.backup ~/.claude/settings.json

# 验证恢复
cat ~/.claude/settings.json | python3 -m json.tool | head -20
```

### 情况 2: 比较差异

```bash
# 查看当前配置
cat ~/.claude/settings.json

# 查看备份配置
cat ~/.claude/settings.json.backup

# 使用 diff 比较
diff ~/.claude/settings.json.backup ~/.claude/settings.json
```

### 情况 3: 选择性恢复

```bash
# 1. 查看备份内容
cat ~/.claude/settings.json.backup | python3 -m json.tool > /tmp/backup.json

# 2. 手动编辑，复制需要的部分
# 3. 恢复到原文件
```

---

## 🛡️ 备份验证

### 验证备份存在

```bash
# 检查所有备份文件
find ~ -name "settings.json.backup" 2>/dev/null

# 检查特定备份
ls -lh ~/.claude/settings.json.backup
```

### 验证备份完整性

```bash
# 验证 JSON 格式
python3 -m json.tool ~/.claude/settings.json.backup > /dev/null && echo "✓ 备份文件格式正确" || echo "✗ 备份文件损坏"
```

### 查看备份时间

```bash
# 查看文件修改时间
ls -lh ~/.claude/settings.json.backup
stat ~/.claude/settings.json.backup
```

---

## 💡 最佳实践

### 1. 定期清理旧备份

```bash
# 删除所有备份文件
find ~ -name "settings.json.backup" -delete

# 或归档备份
mkdir -p ~/backups/settings
cp ~/.claude/settings.json.backup ~/backups/settings/settings.$(date +%Y%m%d).json
```

### 2. 重要操作前手动备份

```bash
# 手动创建带时间戳的备份
cp ~/.claude/settings.json ~/.claude/settings.json.manual.$(date +%Y%m%d_%H%M%S)
```

### 3. 验证备份可用性

```bash
# 在执行重要操作前
cdn hooks status
cp ~/.claude/settings.json ~/.claude/settings.json.pre-operation

# 执行操作
cdn hooks remove PreToolUse

# 如果出问题，立即恢复
cp ~/.claude/settings.json.pre-operation ~/.claude/settings.json
```

---

## ⚠️ 注意事项

### 1. 备份覆盖

每次操作会覆盖之前的备份，**不会保留历史版本**。

**解决方法**：如果需要保留历史，手动创建带时间戳的备份。

### 2. 备份位置

备份文件与原文件在同一目录，确保有写权限。

### 3. 磁盘空间

备份文件很小（通常几KB），不会占用太多空间。

---

## 🔧 操作日志示例

### 示例 1: 安装 Hooks

```bash
$ cdn hooks install

处理配置文件: ~/.claude/settings.json
  ✓ Hooks 已安装 (备份: settings.json.backup)

✅ Hooks 安装完成！
```

**备份内容**：安装前的 settings.json

### 示例 2: 删除 Hook

```bash
$ cdn hooks remove PreToolUse

处理配置文件: ~/.claude/settings.json
  ✓ Hook 已删除 (备份: settings.json.backup)
```

**备份内容**：删除前的 settings.json

### 示例 3: 卸载所有 Hooks

```bash
$ cdn hooks uninstall

处理配置文件: ~/.claude/settings.json
  ✓ 已删除 7 个 claude-dingtalk hooks (备份: settings.json.backup)
```

**备份内容**：卸载前的 settings.json

---

## 📝 总结

### 核心原则

✅ **自动备份** - 所有操作自动备份
✅ **操作前备份** - 修改前先备份
✅ **原位备份** - 备份文件与原文件同目录
✅ **覆盖模式** - 每次操作覆盖之前的备份

### 保障机制

| 场景 | 保障 |
|------|------|
| **误操作** | ✅ 可从备份恢复 |
| **实验性更改** | ✅ 随时恢复到之前状态 |
| **多文件操作** | ✅ 每个文件独立备份 |
| **多次操作** | ⚠️ 只保留最后一次备份 |

### 安全使用

```bash
# 1. 操作前检查备份
ls -lh ~/.claude/settings.json.backup

# 2. 执行操作
cdn hooks remove SomeHook

# 3. 如果出现问题，立即恢复
cp ~/.claude/settings.json.backup ~/.claude/settings.json
```

---

**重要**: 所有修改 settings.json 的操作都会自动备份！✅
