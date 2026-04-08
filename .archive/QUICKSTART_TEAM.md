# ⚡ 快速开始 - 3 分钟配置

## 🚀 一键安装

```bash
# 1. 进入项目目录
cd claude_notifyer

# 2. 运行安装脚本
./install.sh

# 3. 重新加载配置
source ~/.zshrc
```

## ⚙️ 配置

```bash
# 配置钉钉机器人
cdn setup

# 安装 hooks
cdn hooks install

# 测试
cdn test
```

## ✅ 完成！

现在当您使用 Claude Code 时，重要事件会自动发送到钉钉群！

---

## 📝 常用命令

```bash
cdn --help              # 查看帮助
cdn hooks list          # 查看所有 hooks
cdn hooks status        # 查看已安装的 hooks
cdn hooks remove <Hook>  # 删除单个 hook
cdn test                # 测试通知
```

## ❓ 遇到问题？

```bash
# 命令找不到？
source ~/.zshrc

# 查看完整文档
cat README_TEAM.md
```

## 👥 多台电脑？

在其他 Mac 上重复相同步骤，使用**相同的钉钉机器人配置**即可。
