# 🗑️ 完整卸载指南

## 🎯 卸载功能

提供了完整的卸载脚本，可以安全地移除所有组件。

---

## ⚡ 快速卸载

### 一键卸载

```bash
cd claude_notifyer
./uninstall.sh
```

**脚本会自动**：
- ✅ 卸载所有 Claude Code hooks（不影响其他应用）
- ✅ 删除配置文件
- ✅ 删除 CLI wrapper 脚本
- ✅ 清理 PATH 配置
- ✅ 清理环境变量配置
- ✅ 备份重要数据

---

## 📋 卸载详情

### 1. 卸载 Hooks

**安全卸载**：只删除 claude-dingtalk 的 hooks，保留其他应用（如 codefuse）

```bash
# 自动调用
cdn hooks uninstall --all
```

**效果**：
- ✅ claude-dingtalk 的 hooks 被删除
- ✅ codefuse 的 hooks 完好无损
- ✅ 其他应用的 hooks 完好无损

### 2. 删除配置文件

```bash
# 配置目录
~/.claude-dingtalk/
```

**删除前会自动备份**：
```bash
~/.claude-dingtalk.backup.20260403_201234/
```

### 3. 删除 Wrapper 脚本

删除以下位置的 CLI 脚本：
- `~/.local/bin/cdn`
- `~/.local/bin/claude-dingtalk`
- `~/bin/cdn`
- `~/Library/Python/3.9/bin/cdn`

### 4. 清理 PATH 配置

从以下文件中移除 PATH 配置：
- `~/.zshrc`
- `~/.bash_profile`

移除内容：
```bash
# Claude DingTalk Notifier
export PATH="$HOME/.local/bin:$PATH"
```

### 5. 清理环境变量

清理以下环境变量：
- `CLAUDE_MACHINE_NAME`
- `CLAUDE_CONFIG_DIR`
- `DINGTALK_WEBHOOK`
- `DINGTALK_SECRET`

从以下文件中清理：
- `~/.zshrc`
- `~/.bash_profile`
- `~/.zshenv`

---

## 🔄 卸载流程

### 步骤 1: 确认

```bash
$ ./uninstall.sh

╔═══════════════════════════════════════════════════════╗
║     Claude Code 钉钉通知工具 - 卸载脚本              ║
║     Uninstall Script                                  ║
╚═══════════════════════════════════════════════════════╝

⚠ 此操作将：
  1. 卸载所有 Claude Code hooks
  2. 删除配置文件和脚本
  3. 清理 PATH 和环境变量配置
  4. 保留项目文件（需手动删除）

确认卸载？[y/N]:
```

### 步骤 2: 执行

输入 `y` 确认后，脚本会自动执行所有清理操作。

### 步骤 3: 完成

```bash
✓ 卸载完成！

已清理：
  ✓ Claude Code hooks
  ✓ 配置文件 (~/.claude-dingtalk/)
  ✓ CLI wrapper 脚本 (cdn, claude-dingtalk)
  ✓ PATH 配置
  ✓ 环境变量配置

需要手动操作：
  1. 重新加载 shell 配置:
     source ~/.zshrc

  2. 删除项目目录（如果不再需要）:
     rm -rf /path/to/claude_notifyer
```

---

## 🛡️ 安全保障

### 1. 确认机制

默认需要用户确认才会执行卸载，防止误操作。

### 2. 自动备份

配置文件在删除前会自动备份：
```bash
~/.claude-dingtalk.backup.20260403_201234/
```

### 3. 安全的 Hooks 卸载

只删除 claude-dingtalk 的 hooks，不影响其他应用：
- ✅ codefuse hooks 保留
- ✅ 其他工具的 hooks 保留

### 4. 清理确认

每个步骤都有清晰的反馈，知道哪些文件被删除。

---

## 🧹 手动清理（如果脚本失败）

### 步骤 1: 卸载 Hooks

```bash
# 使用 CDN 命令（如果仍可用）
cdn hooks uninstall --all

# 或手动编辑 settings.json
# 删除包含 ".claude-dingtalk/hooks/" 的 hooks
```

### 步骤 2: 删除配置文件

```bash
# 备份（可选）
cp -r ~/.claude-dingtalk ~/.claude-dingtalk.backup

# 删除
rm -rf ~/.claude-dingtalk
```

### 步骤 3: 删除 Wrapper 脚本

```bash
# 查找并删除
rm -f ~/.local/bin/cdn
rm -f ~/.local/bin/claude-dingtalk
rm -f ~/bin/cdn
rm -f ~/Library/Python/3.9/bin/cdn
```

### 步骤 4: 清理 Shell 配置

编辑 `~/.zshrc` 或 `~/.bash_profile`，删除：

```bash
# Claude DingTalk Notifier
export PATH="$HOME/.local/bin:$PATH"

# 环境变量
export CLAUDE_MACHINE_NAME="..."
export DINGTALK_WEBHOOK="..."
export DINGTALK_SECRET="..."
```

### 步骤 5: 重新加载配置

```bash
source ~/.zshrc  # 或 source ~/.bash_profile
```

### 步骤 6: 删除项目目录

```bash
rm -rf /path/to/claude_notifyer
```

---

## 🔄 重新安装

如果改变主意，可以重新安装：

```bash
# 1. 重新克隆或进入项目目录
cd claude_notifyer

# 2. 运行安装脚本
./install.sh

# 3. 配置
cdn setup
cdn hooks install
```

所有配置都可以重新设置。

---

## 📊 卸载前后对比

### 卸载前

```bash
$ cdn --version
claude-dingtalk-notifier, version 0.2.1

$ cdn hooks status
✓ 已安装 Hooks: PreToolUse, Stop, ...

$ ls -la ~/.claude-dingtalk/
config.yaml
hooks/
...

$ echo $CLAUDE_MACHINE_NAME
我的Mac
```

### 卸载后

```bash
$ cdn
zsh: command not found: cdn

$ ls ~/.claude-dingtalk
ls: ~/.claude-dingtalk: No such file or directory

$ echo $CLAUDE_MACHINE_NAME
（空）
```

---

## ⚠️ 注意事项

### 1. settings.json 备份

卸载 hooks 时会自动创建 `settings.json.backup`：

```bash
~/.claude/settings.json.backup
~/.claude/settings.json.backup
```

这些备份会保留，不会被删除。

### 2. 配置备份

配置目录会在删除前备份：

```bash
~/.claude-dingtalk.backup.20260403_201234/
```

如果需要恢复配置：
```bash
cp -r ~/.claude-dingtalk.backup.* ~/.claude-dingtalk/
```

### 3. 项目文件

**项目目录不会被删除**，需要手动删除：

```bash
rm -rf /path/to/claude_notifyer
```

这样可以防止误删项目代码。

### 4. 其他应用不受影响

卸载只影响 claude-dingtalk，其他应用（如 codefuse）的 hooks 和功能完全正常。

---

## 🆘 故障排查

### 问题 1: 命令仍然可用

```bash
# 检查 PATH
which cdn

# 如果仍然存在，手动删除
rm -f $(which cdn)

# 重新加载配置
source ~/.zshrc
```

### 问题 2: Hooks 未完全卸载

```bash
# 检查 settings.json
cat ~/.claude/settings.json | grep -A 5 "hooks"

# 手动删除包含 ".claude-dingtalk" 的 hooks
```

### 问题 3: 配置文件未删除

```bash
# 手动删除
rm -rf ~/.claude-dingtalk
```

---

## ✅ 总结

### 自动卸载（推荐）

```bash
./uninstall.sh
```

**优点**：
- ✅ 一键完成所有清理
- ✅ 自动备份配置
- ✅ 清理所有痕迹
- ✅ 安全保护其他应用

### 手动卸载

参考"手动清理"章节，逐步执行。

---

**重要**: 卸载脚本会保护其他应用的 hooks，确保只删除 claude-dingtalk 的配置！
