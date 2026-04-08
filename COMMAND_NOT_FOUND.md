# ⚠️ 命令找不到？快速修复

## 问题：`claude-dingtalk: command not found`

**原因**：安装脚本已执行，但 shell 配置未重新加载

---

## ✅ 立即修复（3 种方法，选一个）

### 方法 1：重新加载 Shell 配置（推荐）

```bash
# 如果你使用 zsh（默认）
source ~/.zshrc

# 如果你使用 bash
source ~/.bash_profile

# 验证
claude-dingtalk --version
```

### 方法 2：使用完整路径（临时）

```bash
# 查看命令在哪里
which claude-dingtalk

# 直接使用完整路径
~/.local/bin/claude-dingtalk setup
```

### 方法 3：重启终端

```bash
# 完全退出终端应用，重新打开
claude-dingtalk --version
```

---

## 🔍 诊断问题

### 检查 PATH 是否配置

```bash
echo $PATH | grep -o "/Users/[^:]*bin"
```

**期望输出**：应该包含 `/Users/你的用户名/.local/bin` 或类似路径

**如果为空**：说明 PATH 未配置，运行：
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 检查命令是否存在

```bash
ls -la ~/.local/bin/claude-dingtalk
ls -la ~/.local/bin/cdn
```

**期望输出**：应该显示这两个文件

**如果不存在**：需要重新运行安装脚本

---

## 🚀 完整修复流程

### 步骤 1：重新加载配置

```bash
source ~/.zshrc  # 或 source ~/.bash_profile
```

### 步骤 2：验证命令

```bash
claude-dingtalk --version
```

**如果显示版本号** → ✅ 成功！

**如果还是提示找不到** → 继续下一步

### 步骤 3：手动添加 PATH（临时）

```bash
export PATH="$HOME/.local/bin:$PATH"
claude-dingtalk --version
```

### 步骤 4：永久添加 PATH（如果步骤 2-3 失败）

```bash
# 添加到 shell 配置
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# 重新加载
source ~/.zshrc

# 验证
claude-dingtalk --version
```

---

## 🛠️ 如果以上都失败，重新安装

```bash
cd ~/ant_cc_dingding_notifier

# 删除旧的安装
rm -rf ~/.local/bin/cdn ~/.local/bin/claude-dingtalk

# 重新安装
./install.sh

# 重新加载配置
source ~/.zshrc

# 验证
claude-dingtalk --version
```

---

## 📋 验证成功标志

修复成功后，你应该能看到：

```bash
$ claude-dingtalk --version
claude-dingtalk 0.3.1

$ claude-dingtalk status
# 显示配置状态
```

---

## 💡 预防措施

### 每次打开新终端窗口

如果不想每次都运行 `source`，确保：

1. ✅ `~/.zshrc` 或 `~/.bash_profile` 中有：
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. ✅ 安装脚本显示"已添加到 ~/.zshrc"

### 快速检查

```bash
# 查看 shell 配置文件
cat ~/.zshrc | grep -A 1 "Claude DingTalk"

# 应该看到：
# # Claude DingTalk Notifier
# export PATH="$HOME/.local/bin:$PATH"
```

---

## 🆘 还是不行？

收集以下信息并反馈：

```bash
# 1. Shell 类型
echo $SHELL

# 2. PATH 配置
echo $PATH

# 3. 命令位置
which claude-dingtalk
ls -la ~/.local/bin/ | grep claude

# 4. Shell 配置
cat ~/.zshrc | grep -A 2 "Claude"
```

---

**最后更新**: 2026-04-08
**版本**: v0.3.1
