# 安装指南

由于系统 Python 权限限制，提供了三种安装方式。

## 方式一：直接使用（推荐，无需安装）

最简单的方式，使用项目自带的 `run.sh` 脚本：

```bash
# 进入项目目录
cd ~/ant_cc_dingding_notifier

# 使用 run.sh 运行所有命令
./run.sh setup
./run.sh test
./run.sh status
./run.sh hooks install
```

或者创建别名（添加到 `~/.zshrc` 或 `~/.bashrc`）：

```bash
# 添加别名
alias claude-dingtalk='~/ant_cc_dingding_notifier/run.sh'
alias cdn='~/ant_cc_dingding_notifier/run.sh'

# 使用别名
claude-dingtalk setup
cdn test
```

## 方式二：使用安装脚本

```bash
cd ~/ant_cc_dingding_notifier
chmod +x install.sh
./install.sh
```

安装脚本会：
1. 安装依赖到用户目录（`~/.local/`）
2. 创建可执行脚本到 `~/.claude-dingtalk-bin/`
3. 自动添加到 PATH

**安装后需要重新加载 shell 配置：**

```bash
# 如果使用 zsh
source ~/.zshrc

# 如果使用 bash
source ~/.bashrc
# 或在 macOS 上
source ~/.bash_profile
```

然后就可以直接使用命令：

```bash
claude-dingtalk setup
cdn test
```

## 方式三：使用 pipx（推荐用于隔离安装）

如果您有 pipx（Python 包隔离工具）：

```bash
# 安装 pipx（如果尚未安装）
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# 使用 pipx 安装
cd ~/ant_cc_dingding_notifier
pipx install .
```

## 验证安装

运行以下命令验证安装：

```bash
# 查看版本
./run.sh --version

# 查看帮助
./run.sh --help

# 查看状态
./run.sh status
```

## 快速开始

0. **安装 macOS 通知依赖（可选）**

如果需要使用 macOS 桌面通知功能，需要先安装 terminal-notifier：

```bash
# 使用 Homebrew 安装
brew install terminal-notifier

# 验证安装
terminal-notifier -title "测试" -message "安装成功"
```

1. **配置工具**

```bash
./run.sh setup
```

按提示输入：
- 钉钉 Webhook URL
- 加签密钥（可选）
- 选择要启用的事件
- 配置文件路径
- 是否启用 macOS 桌面通知

2. **测试通知**

```bash
./run.sh test
```

3. **安装 Hooks**

```bash
./run.sh hooks install
```

## 常见问题

### Q: 提示权限错误

**A:** 使用方式一（run.sh）不需要任何安装权限。

### Q: 命令找不到

**A:** 确保已重新加载 shell 配置或使用完整路径：
```bash
source ~/.zshrc  # 或 source ~/.bashrc
```

### Q: 依赖缺失

**A:** 手动安装依赖：
```bash
# Python 依赖
pip3 install --user requests pyyaml click rich

# macOS 通知依赖（如果需要桌面通知）
brew install terminal-notifier
```

## 卸载

### 方式一：直接使用

无需卸载，删除项目目录即可。

### 方式二：使用安装脚本

```bash
# 删除可执行文件
rm -rf ~/.claude-dingtalk-bin

# 从 shell 配置中移除 PATH 添加
# 编辑 ~/.zshrc 或 ~/.bashrc，删除相关行

# 删除配置（可选）
rm -rf ~/.claude-dingtalk
```

### 方式三：使用 pipx

```bash
pipx uninstall claude-dingtalk-notifier
```

## 下一步

安装完成后，请参考 [QUICKSTART.md](QUICKSTART.md) 开始使用！
