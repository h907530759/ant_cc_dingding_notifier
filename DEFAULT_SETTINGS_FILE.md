# 📂 默认 Settings 文件配置

## 🎯 默认行为

### 安装脚本默认修改的文件

**默认只修改一个文件**：
```bash
~/.claude/settings.json
```

**前提条件**：这个文件必须存在才会被修改！

---

## 📋 配置逻辑

### 1. 默认配置

**源码位置**：`src/claude_dingtalk_notifier/config.py` 第 38 行

```python
# 默认配置
settings_paths: List[str] = ["~/.claude/settings.json"]
```

### 2. Setup 配置流程

#### 情况 A: 找到现有配置文件

```bash
$ cdn setup

📂 配置 Claude Code settings.json 路径

发现以下 Claude Code 配置文件:
  1. /Users/suchen/.claude/settings.json
  2. /Users/suchen/.codefuse/engine/cc/settings.json

是否使用发现的配置文件？[Y/n]:
```

**如果选择 Y**：使用找到的所有文件
**如果选择 N**：手动输入路径

#### 情况 B: 未找到配置文件

```bash
$ cdn setup

📂 配置 Claude Code settings.json 路径

⚠ 未找到 Claude Code 配置文件
默认路径: ~/.claude/settings.json

请输入 settings.json 路径（多个路径用逗号分隔）:
```

### 3. 文件过滤机制

**源码位置**：`src/claude_dingtalk_notifier/config.py` 第 169-176 行

```python
def get_expanded_settings_paths(self) -> List[Path]:
    """Get expanded settings.json paths"""
    paths = []
    for path_str in self.settings_paths:
        path = Path(path_str).expanduser()  # 展开 ~
        if path.exists():  # 关键：只返回存在的文件！
            paths.append(path)
    return paths
```

**关键点**：
- ✅ 展开路径：`~` → `/Users/username`
- ✅ 检查存在：`path.exists()`
- ✅ **只处理存在的文件**

---

## 🧪 实际测试

### 测试 1: 默认安装

```bash
# 1. 查看 Claude Code 默认 settings 文件
ls -la ~/.claude/settings.json
# 输出: -rw-r--r-- 1 suchen  staff  2345 Apr  3 20:12 .claude/settings.json

# 2. 运行 setup（使用默认配置）
cdn setup
# 输入: 1,2,3,4,5,6,7,8（启用推荐事件）
# 选择: Y（使用发现的配置文件）

# 3. 查看配置文件
cat ~/.claude-dingtalk/config.yaml | grep -A 5 "settings_paths"
```

**结果**：
```yaml
settings_paths:
  - ~/.claude/settings.json
  # 或
  - /Users/suchen/.claude/settings.json
```

### 测试 2: 安装 Hooks

```bash
$ cdn hooks install

处理配置文件: /Users/suchen/.claude/settings.json
  ✓ Hooks 已安装 (备份: settings.json.backup)

✅ Hooks 安装完成！
```

**只修改了**：`~/.claude/settings.json`

### 测试 3: 文件不存在的情况

```bash
# 1. 假设删除默认文件
rm ~/.claude/settings.json

# 2. 运行 setup
cdn setup
```

**输出**：
```
⚠ 未找到 Claude Code 配置文件
默认路径: ~/.claude/settings.json

请输入 settings.json 路径:
```

**用户必须手动输入**：
```bash
/Users/suchen/.claude/settings.json
```

**才会创建并修改这个文件**。

---

## 📊 配置文件发现逻辑

### 自动发现的路径

**源码**：`find_claude_settings()` 函数

```python
def find_claude_settings():
    """Find Claude Code settings.json files"""
    # 常见位置
    common_paths = [
        Path.home() / ".claude" / "settings.json",
        Path.home() / ".codefuse" / "engine" / "cc" / "settings.json",
        # ... 更多路径
    ]
    
    # 只返回存在的
    return [p for p in common_paths if p.exists()]
```

**发现顺序**：
1. `~/.claude/settings.json`（主配置）
2. `~/.codefuse/engine/cc/settings.json`（codefuse 配置）
3. 其他常见位置

---

## 🎯 团队使用场景

### 场景 1: 个人开发

**默认配置**：
```bash
# 只修改主配置文件
~/.claude/settings.json
```

**适用**：个人使用 Claude Code

### 场景 2: 个人 + 工作项目

**Setup 过程**：
```bash
$ cdn setup

发现以下 Claude Code 配置文件:
  1. /Users/suchen/.claude/settings.json
  2. /Users/suchen/.codefuse/engine/cc/settings.json

是否使用发现的配置文件？[Y/n]: Y
```

**结果**：修改两个文件
- `~/.claude/settings.json`
- `~/.codefuse/engine/cc/settings.json`

### 场景 3: 自定义路径

```bash
$ cdn setup

未找到 Claude Code 配置文件

请输入 settings.json 路径:
/home/john/.claude/settings.json
```

**结果**：只修改用户指定的文件

---

## 🔍 查看当前配置

### 方法 1: 查看配置文件

```bash
cat ~/.claude-dingtalk/config.yaml | grep -A 10 "settings_paths"
```

### 方法 2: 查看 Hooks 状态

```bash
$ cdn hooks status

配置文件: /Users/suchen/.claude/settings.json
  ✓ 已安装 Hooks: ...

配置文件: /Users/suchen/.codefuse/engine/cc/settings.json
  ✓ 已安装 Hooks: ...
```

### 方法 3: 测试命令

```bash
# 查看会修改哪些文件
cdn hooks install --dry-run  # 如果有这个选项的话
```

---

## ✅ 总结

### 默认行为

| 情况 | 默认修改的文件 | 条件 |
|------|--------------|------|
| **首次安装** | `~/.claude/settings.json` | 文件必须存在 |
| **找到多个配置** | 所有找到的文件 | 用户确认使用 |
| **未找到配置** | 用户手动输入 | 用户指定路径 |

### 关键点

✅ **默认只修改一个文件**：`~/.claude/settings.json`
✅ **文件必须存在**：不存在的文件会被过滤掉
✅ **用户可控**：setup 时可以选择或添加路径
✅ **自动发现**：自动找到现有的 settings.json 文件

### 实际使用

**个人用户**（最常见）：
```bash
# 默认只会修改
~/.claude/settings.json
```

**团队用户**：
```bash
# 可能修改多个文件
~/.claude/settings.json
~/path/to/project/settings.json
```

### 安全性

✅ **不会意外修改**：只修改配置文件中存在的路径
✅ **用户确认**：setup 时会显示将要修改的文件
✅ **自动备份**：修改前自动创建 `.backup` 文件

---

**重要**: 默认只修改 `~/.claude/settings.json`，其他文件需要用户在 setup 时明确添加！
