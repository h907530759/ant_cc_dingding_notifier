# 🔍 缺失文件检测功能

## 📋 更新说明

**版本**: v0.2.2
**日期**: 2026-04-03
**类型**: 用户体验改进

---

## 🎯 问题描述

### v0.2.1 及之前版本的问题

在之前的版本中，如果用户配置了多个 settings.json 文件（例如同时配置了开源 Claude Code 和内部 antcc 系统），但其中某些文件不存在，工具会**静默跳过**这些缺失的文件，用户不知道：

1. 哪些文件被跳过了
2. 是否配置错误
3. 为什么某些系统没有收到通知

### 用户体验问题

```bash
# v0.2.1 之前的体验
$ cdn hooks install

处理配置文件: ~/.claude/settings.json
  ✓ Hooks 已安装

✅ Hooks 安装完成！
```

**问题**: 用户不知道还配置了 `~/.claude/settings.json`，但这个文件不存在。

---

## 🔧 解决方案

### 新增函数：check_settings_paths_status()

**文件**: `src/claude_dingtalk_notifier/config.py` (第 178-196 行)

```python
def check_settings_paths_status(self) -> tuple[List[Path], List[str]]:
    """检查配置文件状态

    Returns:
        (existing_paths, missing_paths)
        - existing_paths: 存在的文件列表 (Path 对象)
        - missing_paths: 缺失的文件列表 (原始路径字符串)
    """
    existing_paths = []
    missing_paths = []

    for path_str in self.settings_paths:
        path = Path(path_str).expanduser()
        if path.exists():
            existing_paths.append(path)
        else:
            missing_paths.append(path_str)

    return existing_paths, missing_paths
```

### 工作原理

1. **遍历配置的路径**: 检查 `config.settings_paths` 中的所有路径
2. **展开用户目录**: 将 `~` 展开为实际路径（如 `/Users/username`）
3. **检查文件存在**: 使用 `path.exists()` 判断文件是否存在
4. **分类返回**: 将路径分为 `existing_paths` 和 `missing_paths` 两组

---

## 📊 实际效果对比

### 场景 1: 默认配置，只有开源 Claude Code

**配置**:
```yaml
settings_paths:
  - ~/.claude/settings.json              # 存在
  - ~/.claude/settings.json  # 不存在
```

#### v0.2.1 的行为

```bash
$ cdn hooks install

处理配置文件: ~/.claude/settings.json
  ✓ Hooks 已安装 (备份: settings.json.backup)

✅ Hooks 安装完成！
```

**问题**: 用户不知道 antcc 配置文件不存在

#### v0.2.2 的行为

```bash
$ cdn hooks install

⚠️  以下配置文件不存在，将跳过:
  - ~/.claude/settings.json

将处理 1 个配置文件

处理配置文件: ~/.claude/settings.json
  ✓ Hooks 已安装 (备份: settings.json.backup)

✅ Hooks 安装完成！
```

**改进**: 明确告知用户哪些文件缺失

---

### 场景 2: 查看 Hooks 状态

```bash
$ cdn hooks status

⚠️  以下配置文件不存在:
  - ~/.claude/settings.json

配置文件: ~/.claude/settings.json
  ✓ 已安装 Hooks:
    - PreToolUse
    - Stop
    - SessionEnd
    ...
```

---

### 场景 3: 卸载 Hooks (--all 选项)

```bash
$ cdn hooks uninstall --all

⚠️  以下配置文件不存在，将跳过:
  - ~/.claude/settings.json

卸载所有配置文件中的 hooks (1 个文件)

处理配置文件: ~/.claude/settings.json
  ✓ 已删除 10 个 claude-dingtalk hooks (备份: settings.json.backup)

✅ Hooks 卸载完成！
```

---

### 场景 4: 删除单个 Hook

```bash
$ cdn hooks remove PreToolUse --all

🗑️  删除 Hook: PreToolUse

⚠️  以下配置文件不存在，将跳过:
  - ~/.claude/settings.json

从所有配置文件中删除 (1 个文件)

处理配置文件: ~/.claude/settings.json
  ✓ 已删除 PreToolUse hook (备份: settings.json.backup)

✅ Hook 删除完成！
```

---

## 🛠️ 受影响的命令

以下 4 个命令都已更新，支持缺失文件检测：

| 命令 | 检测时机 | 显示信息 |
|------|---------|---------|
| `cdn hooks install` | 安装前 | 显示缺失文件 + 处理文件数量 |
| `cdn hooks uninstall` | 卸载前 | 显示缺失文件 + 处理文件数量 |
| `cdn hooks remove` | 删除前 | 显示缺失文件 + 处理文件数量 |
| `cdn hooks status` | 查看时 | 显示缺失文件列表 |

---

## 💡 使用建议

### 对于个人用户（只使用开源 Claude Code）

**默认配置**:
```yaml
settings_paths:
  - ~/.claude/settings.json
```

**如果 antcc 文件不存在**:
```bash
$ cdn hooks install

⚠️  以下配置文件不存在，将跳过:
  - ~/.claude/settings.json

将处理 1 个配置文件

...
```

**建议**:
- ✅ 不影响使用，忽略警告即可
- ✅ 或者修改配置文件，移除 antcc 路径：
  ```bash
  cdn setup
  # 只选择 ~/.claude/settings.json
  ```

### 对于团队用户（同时使用两个系统）

**期望的输出**:
```bash
$ cdn hooks install

将处理 2 个配置文件  # 没有警告，说明两个文件都存在

处理配置文件: ~/.claude/settings.json
  ✓ Hooks 已安装

处理配置文件: ~/.claude/settings.json
  ✓ Hooks 已安装

✅ Hooks 安装完成！
```

**如果看到警告**:
```bash
⚠️  以下配置文件不存在，将跳过:
  - ~/.claude/settings.json
```

**可能原因**:
1. antcc 系统未安装
2. 配置文件路径错误
3. 文件被删除或移动

**解决方法**:
- 检查 antcc 是否正确安装
- 或修改配置，移除该路径

---

## 🔍 技术细节

### 代码变更位置

#### 1. config.py (新增函数)

```python
# 第 178-196 行
def check_settings_paths_status(self) -> tuple[List[Path], List[str]]:
    """检查配置文件状态"""
    existing_paths = []
    missing_paths = []

    for path_str in self.settings_paths:
        path = Path(path_str).expanduser()
        if path.exists():
            existing_paths.append(path)
        else:
            missing_paths.append(path_str)

    return existing_paths, missing_paths
```

#### 2. cli.py (hooks_install)

```python
# 第 454-467 行
existing_paths, missing_paths = config.check_settings_paths_status()

# Show warnings for missing files
if missing_paths:
    rprint("\n[yellow]⚠️  以下配置文件不存在，将跳过:[/yellow]")
    for path_str in missing_paths:
        rprint(f"  [dim]  - {path_str}[/dim]")
    rprint("")

if not existing_paths:
    rprint("[yellow]⚠[/yellow] 未找到有效的 settings.json 文件")
    rprint("[dim]请先运行 setup 命令配置文件路径[/dim]")
    return

rprint(f"[bold]将处理 {len(existing_paths)} 个配置文件[/bold]\n")

for settings_path in existing_paths:
    # ... 安装逻辑
```

#### 3. cli.py (hooks_uninstall)

```python
# 第 1082-1102 行
elif all:
    existing_paths, missing_paths = config.check_settings_paths_status()

    if missing_paths:
        rprint("\n[yellow]⚠️  以下配置文件不存在，将跳过:[/yellow]")
        for path_str in missing_paths:
            rprint(f"  [dim]  - {path_str}[/dim]")
        rprint("")

    if not existing_paths:
        rprint("[yellow]⚠[/yellow] 未找到有效的 settings.json 文件")
        return

    settings_paths = existing_paths
    rprint(f"[dim]卸载所有配置文件中的 hooks ({len(settings_paths)} 个文件)[/dim]\n")
```

#### 4. cli.py (hooks_status)

```python
# 第 1446-1460 行
existing_paths, missing_paths = config.check_settings_paths_status()

if missing_paths:
    rprint("[yellow]⚠️  以下配置文件不存在:[/yellow]")
    for path_str in missing_paths:
        rprint(f"  [dim]  - {path_str}[/dim]")
    rprint("")

if not existing_paths:
    rprint("[yellow]⚠[/yellow] 未找到有效的 settings.json 文件")
    return

for settings_path in existing_paths:
    # ... 状态显示逻辑
```

---

## ✅ 测试验证

### 测试 1: 正常情况（所有文件都存在）

```bash
# 1. 检查配置
python3 -c "
import sys
sys.path.insert(0, 'src')
from claude_dingtalk_notifier.config import get_default_config

config = get_default_config()
existing, missing = config.check_settings_paths_status()

print(f'存在: {len(existing)} 个')
print(f'缺失: {len(missing)} 个')
"

# 2. 安装 hooks
cdn hooks install

# 3. 验证：应该没有警告，直接显示 "将处理 2 个配置文件"
```

### 测试 2: 缺失文件情况

```bash
# 1. 临时删除一个文件
mv ~/.claude/settings.json ~/.claude/settings.json.bak

# 2. 安装 hooks
cdn hooks install

# 3. 验证：应该显示警告
# ⚠️  以下配置文件不存在，将跳过:
#   - ~/.claude/settings.json

# 4. 恢复文件
mv ~/.claude/settings.json.bak ~/.claude/settings.json
```

### 测试 3: 所有文件都不存在

```bash
# 1. 临时删除所有配置文件
mv ~/.claude/settings.json ~/.claude/settings.json.bak
mv ~/.claude/settings.json ~/.claude/settings.json.bak

# 2. 安装 hooks
cdn hooks install

# 3. 验证：应该显示
# ⚠️  以下配置文件不存在，将跳过:
#   - ~/.claude/settings.json
#   - ~/.claude/settings.json
#
# ⚠ 未找到有效的 settings.json 文件
# 请先运行 setup 命令配置文件路径

# 4. 恢复文件
mv ~/.claude/settings.json.bak ~/.claude/settings.json
mv ~/.claude/settings.json.bak ~/.claude/settings.json
```

---

## 📚 相关文档

- **ANTCC_INTEGRATION.md** - antcc 系统集成说明
- **DEFAULT_SETTINGS_FILE.md** - 默认配置文件说明
- **HOOKS_SAFETY.md** - Hooks 安全卸载说明

---

## 🎯 总结

### 核心改进

✅ **明确提示** - 告知用户哪些文件缺失
✅ **不影响操作** - 只处理存在的文件
✅ **用户友好** - 清晰的警告信息
✅ **全面覆盖** - 所有 hooks 命令都支持

### 用户体验提升

| 场景 | v0.2.1 | v0.2.2 |
|------|--------|--------|
| **配置文件缺失** | 静默跳过 ❌ | 明确提示 ✅ |
| **用户困惑** | 不知道哪些文件被跳过 ❌ | 清楚看到缺失文件 ✅ |
| **问题排查** | 难以定位问题 ❌ | 一目了然 ✅ |

### 向后兼容

✅ **完全兼容** - 不影响现有配置和使用方式
✅ **平滑升级** - 从 0.2.1 升级无需额外操作
✅ **默认行为** - 只对现有功能增加提示，不改变逻辑

---

**更新日期**: 2026-04-03
**版本**: v0.2.2
**状态**: ✅ 完成并测试通过
