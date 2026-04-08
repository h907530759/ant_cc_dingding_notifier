# 👥 Claude Code 钉钉通知 - 团队部署指南

## 🚀 快速开始（推荐）

### 一键安装

```bash
# 1. 克隆项目
git clone <your-repo-url> claude_notifyer
cd claude_notifyer

# 2. 运行安装脚本
./install.sh

# 3. 加载配置
source ~/.zshrc  # 或 source ~/.bash_profile

# 4. 配置钉钉机器人
cdn setup

# 5. 安装 hooks
cdn hooks install
```

**就这么简单！** 🎉

---

## 📋 系统要求

### Mac 电脑
- macOS 10.15 或更高版本
- Python 3.8+ (系统自带或自行安装)

### Python 环境（任选其一）

✅ **支持的 Python 环境**:
1. Homebrew Python (推荐)
2. pyenv
3. asdf
4. 系统 Python (可能功能受限)

❌ **不支持**:
- 不使用 Python 2.x
- 不使用低于 3.8 的版本

---

## 🔧 安装方式

### 方式 1: 自动安装（推荐）⭐

```bash
./install.sh
```

**自动完成**:
- ✅ 检测 Python 环境
- ✅ 安装依赖
- ✅ 创建 CLI 命令 (`cdn`)
- ✅ 配置 PATH
- ✅ 适配不同 Mac 环境

### 方式 2: 手动安装

如果自动安装失败，可以手动安装：

#### 步骤 1: 安装依赖

```bash
pip3 install --user requests pyyaml click rich
```

#### 步骤 2: 创建命令别名

在 `~/.zshrc` 或 `~/.bash_profile` 中添加：

```bash
# Claude DingTalk Notifier
export PYTHONPATH="/path/to/claude_notifyer/src:$PYTHONPATH"
alias cdn="python3 -m claude_dingtalk_notifier.cli"
```

#### 步骤 3: 加载配置

```bash
source ~/.zshrc  # 或 source ~/.bash_profile
```

---

## 🎯 使用指南

### 基本命令

```bash
# 查看帮助
cdn --help

# 配置钉钉机器人
cdn setup

# 安装 hooks
cdn hooks install

# 查看状态
cdn status

# 测试通知
cdn test
```

### Hooks 管理

```bash
# 列出所有可用的 hooks
cdn hooks list

# 查看已安装的 hooks
cdn hooks status

# 删除单个 hook
cdn hooks remove PreToolUse

# 卸载所有 hooks
cdn hooks uninstall
```

### 按文件维度管理（多环境）

```bash
# 交互式选择配置文件
cdn hooks remove PreToolUse
cdn hooks uninstall

# 指定单个配置文件
cdn hooks remove PreToolUse --settings ~/.claude/settings.json
cdn hooks uninstall --settings ~/.claude/settings.json

# 操作所有配置文件
cdn hooks remove PreToolUse --all
cdn hooks uninstall --all
```

---

## 👥 多机器部署

### 场景: 多台 Mac 使用同一个钉钉群

#### 机器 A (办公电脑)

```bash
cd /path/to/claude_notifyer
./install.sh
cdn setup
# 设置机器标识（可选）
export CLAUDE_MACHINE_NAME="办公电脑"
cdn hooks install
```

#### 机器 B (家用电脑)

```bash
cd /path/to/claude_notifyer
./install.sh
cdn setup
# 使用相同的钉钉机器人配置
export CLAUDE_MACHINE_NAME="家用电脑"
cdn hooks install
```

**结果**: 两台机器的通知都会发送到同一个钉钉群。

---

## 🔒 安全与备份

### 自动备份机制

**重要**: 所有修改 settings.json 的操作都会**自动创建备份**！

```bash
# 每次操作前都会自动备份
cdn hooks install    # → settings.json.backup
cdn hooks uninstall  # → settings.json.backup
cdn hooks remove X   # → settings.json.backup
```

### 备份位置

```bash
# 备份文件与原文件在同一目录
~/.claude/settings.json → ~/.claude/settings.json.backup
~/.claude/settings.json → ~/.claude/settings.json.backup
```

### 恢复备份

```bash
# 如果操作出错，可以立即恢复
cp ~/.claude/settings.json.backup ~/.claude/settings.json
```

### 安全保障

✅ **自动备份** - 所有操作自动备份
✅ **保护其他应用** - 只删除 claude-dingtalk 的 hooks
✅ **独立备份** - 每个配置文件独立备份
✅ **随时恢复** - 可从备份快速恢复

详细说明请查看：[BACKUP_POLICY.md](BACKUP_POLICY.md) 和 [HOOKS_SAFETY.md](HOOKS_SAFETY.md)

---

## 🔧 故障排查

### 问题 1: 命令找不到

```bash
# 检查 PATH
which cdn

# 如果没有输出，重新加载配置
source ~/.zshrc  # 或 source ~/.bash_profile

# 如果还是没有，检查命令文件
ls -la ~/.local/bin/cdn  # 或 ~/bin/cdn
```

### 问题 2: Python 版本过低

```bash
# 安装 Homebrew Python
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.11

# 重新运行安装脚本
./install.sh
```

### 问题 3: 依赖安装失败

```bash
# 手动安装依赖
python3 -m pip install --user requests pyyaml click rich

# 验证安装
python3 -c "import requests, pyyaml, click, rich; print('OK')"
```

### 问题 4: Hook 导入错误

```bash
# 检查 PYTHONPATH
echo $PYTHONPATH

# 重新安装 hooks
cd ~/.claude-dingtalk/hooks
ls -la *.py

# 重新安装
cdn hooks uninstall
cdn hooks install
```

---

## 📊 不同 Python 环境的兼容性

| Python 环境 | 支持情况 | 说明 |
|------------|---------|------|
| **Homebrew Python** | ✅ 完美支持 | 推荐使用 |
| **pyenv** | ✅ 完美支持 | 推荐使用 |
| **asdf** | ✅ 完美支持 | 推荐使用 |
| **系统 Python (Xcode)** | ⚠️ 受限支持 | 无法安装包，但可使用 wrapper |
| **conda** | ✅ 支持 | 需要激活环境 |

### 推荐安装 Homebrew Python

```bash
# 安装 Homebrew（如果没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python
brew install python@3.11

# 验证
python3.11 --version
```

---

## 🎨 自定义配置

### 修改安装位置

编辑 `install.sh`，修改 `BIN_DIR` 变量：

```bash
# 默认: ~/.local/bin 或 ~/bin
# 可以改为: /usr/local/bin (需要 sudo)
```

### 使用不同的命令名

在 `install.sh` 中修改：

```bash
# 创建自定义命令名
cat > "$bin_dir/mycommand" << 'EOF'
#!/bin/bash
exec "$bin_dir/cdn" "$@"
EOF
chmod +x "$bin_dir/mycommand"
```

---

## 📚 高级用法

### 1. 环境变量配置

```bash
# ~/.zshrc 或 ~/.bash_profile

# 机器标识（多机器场景）
export CLAUDE_MACHINE_NAME="我的Mac"

# 自定义配置目录
export CLAUDE_CONFIG_DIR="$HOME/.claude-dingtalk"
```

### 2. 多配置文件管理

```bash
# 查看所有配置文件
cdn hooks status

# 只操作特定配置文件
cdn hooks remove PreToolUse --settings /path/to/settings.json
```

### 3. 团队共享配置

创建配置模板 `config.template.yaml`:

```yaml
dingtalk:
  # 使用环境变量
  webhook: "${DINGTALK_WEBHOOK}"
  secret: "${DINGTALK_SECRET}"

machine:
  # 机器标识
  name: "${CLAUDE_MACHINE_NAME}"
```

团队成员设置自己的环境变量：

```bash
export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=xxx"
export DINGTALK_SECRET="SECxxx"
export CLAUDE_MACHINE_NAME="张三的Mac"
```

---

## 🔒 安全建议

### 1. 保护敏感信息

```bash
# ✅ 好的做法：使用环境变量
export DINGTALK_WEBHOOK="your-webhook-url"

# ❌ 不好的做法：硬编码在配置文件中
# webhook: "https://oapi.dingtalk.com/robot/send?access_token=xxx"
```

### 2. 配置文件权限

```bash
# 限制配置文件权限
chmod 600 ~/.claude-dingtalk/config.yaml
```

### 3. 不提交敏感文件

在 `.gitignore` 中添加：

```gitignore
# 配置文件（包含敏感信息）
.claude-dingtalk/
config.yaml
*.backup
```

---

## 📈 团队协作最佳实践

### 1. 统一开发环境

建议团队成员都安装 Homebrew Python：

```bash
# 统一安装脚本
#!/bin/bash
# install_python.sh

if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew install python@3.11
pip3.11 install --user requests pyyaml click rich
```

### 2. 文档化配置

创建团队 Wiki 文档，包含：
- ✅ 钉钉机器人创建步骤
- ✅ 项目安装步骤
- ✅ 常见问题解决方案
- ✅ 团队联系方式

### 3. 版本管理

```bash
# 查看当前版本
cdn --version

# 更新到最新版本
cd claude_notifyer
git pull
./install.sh
```

---

## 🎓 团队培训建议

### 新成员入职清单

- [ ] 安装 Homebrew Python
- [ ] 克隆项目仓库
- [ ] 运行 `./install.sh`
- [ ] 创建钉钉机器人
- [ ] 运行 `cdn setup`
- [ ] 运行 `cdn hooks install`
- [ ] 运行 `cdn test` 验证
- [ ] 阅读 README 和故障排查文档

---

## 📞 获取帮助

### 命令行帮助

```bash
cdn --help
cdn hooks --help
cdn hooks remove --help
```

### 文档

- **TEAM_DEPLOYMENT.md**: 团队部署指南
- **HOOKS_MANAGEMENT.md**: Hooks 管理指南
- **HOOKS_UNINSTALL_GUIDE.md**: 按文件卸载指南
- **MULTI_MACHINE_SETUP.md**: 多机器部署指南

### 团队支持

如有问题，请联系团队负责人或查看团队 Wiki。

---

## 🎉 开始使用

准备好了吗？开始安装：

```bash
git clone <your-repo> claude_notifyer
cd claude_notifyer
./install.sh
```

**祝使用愉快！** 🚀
