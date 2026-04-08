# 🎯 Hooks 按文件卸载指南

## 📋 问题

之前 `uninstall` 和 `remove` 命令会对**所有** settings.json 文件生效，无法选择特定文件。

## ✅ 解决方案

现在两个命令都支持按文件维度操作！

---

## 🗑️ hooks uninstall - 卸载 Hooks

### 方式 1: 交互式选择（推荐）

```bash
python -m claude_dingtalk_notifier.cli hooks uninstall
```

**效果**:
```
请选择要卸载 Hooks 的配置文件:

  1. /Users/suchen/.claude/settings.json
  2. /Users/suchen/.codefuse/engine/cc/settings.json
  3. 所有文件
  0. 取消

请输入选项:
```

**优点**:
- ✅ 清晰显示所有配置文件
- ✅ 可以精确选择要操作的文件
- ✅ 支持选择"所有文件"

### 方式 2: 指定单个文件

```bash
python -m claude_dingtalk_notifier.cli hooks uninstall --settings /Users/suchen/.claude/settings.json
```

**效果**: 只从指定的 settings.json 中卸载 hooks

**使用场景**:
- 只想卸载某个配置文件的 hooks
- 多个配置文件，想保留某些文件的 hooks

### 方式 3: 卸载所有文件

```bash
python -m claude_dingtalk_notifier.cli hooks uninstall --all
```

**效果**: 从所有配置文件中卸载 hooks（与之前的行为相同）

---

## 🗑️ hooks remove - 删除单个 Hook

### 方式 1: 交互式选择（推荐）

```bash
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse
```

**效果**:
```
请选择要删除 Hook 的配置文件:

  1. /Users/suchen/.claude/settings.json
  2. /Users/suchen/.codefuse/engine/cc/settings.json
  3. 所有文件
  0. 取消

请输入选项:
```

**优点**:
- ✅ 精确选择要删除的配置文件
- ✅ 避免误操作影响其他配置
- ✅ 可视化选择界面

### 方式 2: 指定单个文件

```bash
# 只从主配置中删除
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --settings /Users/suchen/.claude/settings.json

# 只从工作配置中删除
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --settings /Users/suchen/.codefuse/engine/cc/settings.json
```

**使用场景**:
- 不同配置文件有不同的 hook 需求
- 只想禁用某个环境的特定 hook

### 方式 3: 从所有文件中删除

```bash
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --all
```

**效果**: 从所有配置文件中删除该 hook

### 方式 4: 同时删除脚本文件

```bash
# 交互式选择 + 删除脚本
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --delete-script

# 指定文件 + 删除脚本
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --settings ~/.claude/settings.json --delete-script
```

---

## 🎯 使用场景

### 场景 1: 多环境配置

**情况**: 有两个配置文件
- `~/.claude/settings.json` - 个人开发
- `/Users/suchen/.codefuse/engine/cc/settings.json` - 工作项目

**需求**: 只在工作项目中禁用 PreToolUse hook

**解决方案**:
```bash
# 方式 1: 交互式（推荐）
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse
# 选择: 2 (工作项目)

# 方式 2: 直接指定
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --settings /Users/suchen/.codefuse/engine/cc/settings.json
```

### 场景 2: 清理特定环境的所有 hooks

**情况**: 想清理工作环境的 hooks，但保留个人环境的

**解决方案**:
```bash
# 方式 1: 交互式
python -m claude_dingtalk_notifier.cli hooks uninstall
# 选择: 2 (工作项目)

# 方式 2: 直接指定
python -m claude_dingtalk_notifier.cli hooks uninstall --settings /Users/suchen/.codefuse/engine/cc/settings.json
```

### 场景 3: 测试不同的 hook 配置

**情况**: 想在主配置中测试禁用某个 hook，但不想影响其他配置

**解决方案**:
```bash
# 只从主配置中删除
python -m claude_dingtalk_notifier.cli hooks remove Stop --settings ~/.claude/settings.json

# 测试后如果需要恢复
python -m claude_dingtalk_notifier.cli hooks install --settings ~/.claude/settings.json
```

### 场景 4: 精细化管理不同环境的 hooks

**情况**:
- 个人环境: 需要所有 hooks
- 工作环境: 只需要 Stop 和 TaskCompleted
- 测试环境: 只需要 StopFailure

**解决方案**:
```bash
# 1. 先在所有环境安装所有 hooks
python -m claude_dingtalk_notifier.cli hooks install --all

# 2. 工作环境 - 只保留需要的
python -m claude_dingtalk_notifier.cli hooks uninstall --settings /work/settings.json
python -m claude_dingtalk_notifier.cli hooks install --settings /work/settings.json
# 在 setup 时只选择需要的 hooks

# 3. 测试环境 - 只保留 StopFailure
python -m claude_dingtalk_notifier.cli hooks uninstall --settings /test/settings.json
python -m claude_dingtalk_notifier.cli hooks install --settings /test/settings.json
# 在 setup 时只选择 StopFailure
```

---

## 📊 命令对比

| 命令 | 操作范围 | 文件选择 | Hook 选择 |
|------|---------|---------|-----------|
| `uninstall` | 卸载 | ✅ 可选 | ❌ 所有 |
| `remove` | 删除 | ✅ 可选 | ✅ 单个 |
| `install` | 安装 | ❌ 所有 | ❌ 启用的 |
| `list` | 列表 | ❌ 不适用 | ✅ 所有 |
| `status` | 状态 | ❌ 所有 | ✅ 已安装的 |

---

## 💡 最佳实践

### 1. 使用交互式选择

```bash
# 推荐：交互式选择，清晰明了
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse
python -m claude_dingtalk_notifier.cli hooks uninstall
```

**优点**:
- ✅ 不会误操作
- ✅ 清晰看到所有选项
- ✅ 可以取消操作

### 2. 明确指定文件路径

```bash
# 适合脚本自动化
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --settings /path/to/settings.json
```

**优点**:
- ✅ 精确控制
- ✅ 适合自动化脚本
- ✅ 不会误操作其他文件

### 3. 操作前先查看状态

```bash
# 1. 查看已安装的 hooks
python -m claude_dingtalk_notifier.cli hooks status

# 2. 确认要操作的配置文件
# 3. 执行删除/卸载操作
python -m claude_dingtalk_notifier.cli hooks remove HookName --settings /specific/path
```

### 4. 使用备份文件恢复

如果误操作，可以从备份文件恢复：

```bash
# 备份文件自动创建为 settings.json.backup
cp /path/to/settings.json.backup /path/to/settings.json
```

---

## ⚠️ 注意事项

### 1. 默认行为改变

**之前**: 直接卸载/删除所有配置文件中的 hooks

**现在**: 默认进入交互式选择，需要用户确认

### 2. 使用 --all 恢复旧行为

如果想要旧版本的行为（操作所有文件），使用 `--all` 参数：

```bash
python -m claude_dingtalk_notifier.cli hooks uninstall --all
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --all
```

### 3. 文件路径必须是绝对路径

使用 `--settings` 时，需要提供绝对路径：

```bash
# ❌ 错误
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --settings settings.json

# ✅ 正确
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --settings ~/.claude/settings.json
```

### 4. 交互式选择需要终端

交互式选择需要在真正的终端中运行，不能在脚本中使用：

```bash
# ❌ 脚本中无法使用交互式选择
echo "1" | python -m claude_dingtalk_notifier.cli hooks remove PreToolUse

# ✅ 脚本中使用直接指定
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --settings /path/to/settings.json --all
```

---

## 🚀 快速参考

```bash
# 交互式卸载（推荐）
python -m claude_dingtalk_notifier.cli hooks uninstall

# 卸载指定文件
python -m claude_dingtalk_notifier.cli hooks uninstall --settings ~/.claude/settings.json

# 卸载所有文件
python -m claude_dingtalk_notifier.cli hooks uninstall --all

# 交互式删除单个 hook（推荐）
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse

# 删除指定文件中的单个 hook
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --settings ~/.claude/settings.json

# 从所有文件中删除单个 hook
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --all

# 删除 hook 和脚本文件
python -m claude_dingtalk_notifier.cli hooks remove PreToolUse --delete-script
```

---

## 📝 总结

现在您可以：

✅ **按文件维度卸载 hooks** - 只操作指定的配置文件
✅ **交互式选择** - 清晰可视化选择界面
✅ **精细化控制** - 不同环境配置不同的 hooks
✅ **避免误操作** - 默认需要确认，不会影响所有配置

完美支持多环境、多配置文件的场景！🎉
