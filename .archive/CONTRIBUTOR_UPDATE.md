# 🔄 如何更新 GitHub 项目代码

本文档说明如何获取/更新项目代码。

---

## 📥 情况一：首次获取项目（新用户）

### 方法 1：克隆项目（推荐）

```bash
# 克隆仓库到本地
git clone https://github.com/h907530759/ant_cc_dingding_notifier.git

# 进入项目目录
cd ant_cc_dingding_notifier
```

### 方法 2：下载 ZIP（不推荐，无法后续更新）

1. 访问：https://github.com/h907530759/ant_cc_dingding_notifier
2. 点击绿色按钮 **Code** → **Download ZIP**
3. 解压到本地

---

## 🔄 情况二：已有项目，更新到最新版本

### 检查当前版本

```bash
cd ~/ant_cc_dingding_notifier  # 或你的项目路径

# 查看当前提交
git log --oneline -1

# 查看当前分支
git branch
```

### 更新到最新版本

```bash
# 方法 1: 拉取最新代码（推荐）
git pull origin main

# 方法 2: 先获取远程信息，再合并
git fetch origin
git merge origin/main

# 方法 3: 使用 rebase（保持提交历史整洁）
git pull --rebase origin main
```

### 更新后检查

```bash
# 查看最新提交
git log --oneline -3

# 查看更新的文件
git log --name-only -1
```

---

## ⚠️ 常见情况处理

### 情况 1：本地有修改，想保留修改并更新

```bash
# 1. 先暂存本地修改
git stash

# 2. 拉取最新代码
git pull origin main

# 3. 恢复本地修改
git stash pop

# 4. 如果有冲突，手动解决后：
git add .
git commit -m "Merge changes"
```

### 情况 2：本地有修改，想放弃修改并更新

```bash
# 放弃所有本地修改，使用远程代码
git fetch origin
git reset --hard origin/main

# ⚠️ 警告：这会删除所有本地未提交的修改！
```

### 情况 3：更新失败，提示冲突

```bash
# 查看冲突文件
git status

# 手动解决冲突后
git add <解决冲突的文件>
git commit

# 或放弃更新
git merge --abort
```

---

## 🚀 更新后必须做的操作

### 1. 重新安装（如果有代码更新）

```bash
# 重新运行安装脚本
./install.sh

# 重新加载 shell 配置
source ~/.zshrc  # 或 source ~/.bashrc
```

### 2. 重新安装 Hooks（重要！）

```bash
# 任何代码更新后都必须重新安装 hooks
claude-dingtalk hooks install
```

### 3. 测试验证

```bash
# 检查版本
claude-dingtalk status

# 测试通知
claude-dingtalk test
```

---

## 📋 完整更新流程示例

```bash
# 1. 进入项目目录
cd ~/ant_cc_dingding_notifier

# 2. 查看当前版本
git log --oneline -1

# 3. 拉取最新代码
git pull origin main

# 4. 查看更新内容
git log --oneline -3

# 5. 重新安装（如果有代码更新）
./install.sh

# 6. 重新安装 Hooks
claude-dingtalk hooks install

# 7. 测试验证
claude-dingtalk test
```

---

## 🔍 如何知道有新版本？

### 方法 1：手动检查

```bash
cd ~/ant_cc_dingding_notifier
git fetch origin
git log HEAD..origin/main --oneline
```

如果有输出，说明有新提交。

### 方法 2：查看 GitHub

访问：https://github.com/h907530759/ant_cc_dingding_notifier/commits/main

### 方法 3：使用 Watch（推荐）

1. 访问项目主页
2. 点击右上角 **Watch** → **Custom**
3. 勾选 **Releases** 和 **Activity**
4. 有更新时会收到邮件通知

---

## 💡 最佳实践

### ✅ 推荐做法

1. **定期更新**：每周或每月运行一次 `git pull`
2. **更新前备份**：重要修改前先 `git stash`
3. **更新后重装 Hooks**：确保使用最新功能
4. **查看更新日志**：了解新功能和改动

### ❌ 避免的做法

1. ❌ 不要直接修改项目源码（建议 fork）
2. ❌ 不要在项目目录下存放个人文件
3. ❌ 不要跳过 `hooks install` 步骤
4. ❌ 不要在敏感操作中途更新

---

## 🆘 更新失败怎么办？

### 问题 1：提示 "Permission denied"

```bash
# 检查远程仓库地址
git remote -v

# 如果地址错误，重新设置
git remote set-url origin https://github.com/h907530759/ant_cc_dingding_notifier.git
```

### 问题 2：提示 "Not a git repository"

```bash
# 说明你下载的是 ZIP，不是 git clone
# 需要重新克隆：
cd ..
mv ant_cc_dingding_notifier ant_cc_dingding_notifier.old
git clone https://github.com/h907530759/ant_cc_dingding_notifier.git
```

### 问题 3：网络问题

```bash
# 使用代理（如果有）
export https_proxy=http://127.0.0.1:7890
git pull origin main

# 或使用 SSH（如果配置了）
git remote set-url origin git@github.com:h907530759/ant_cc_dingding_notifier.git
```

---

## 📞 需要帮助？

如果遇到问题：
1. 查看 [TROUBLESHOOTING_CHECKLIST.md](TROUBLESHOOTING_CHECKLIST.md)
2. 提交 Issue: https://github.com/h907530759/ant_cc_dingding_notifier/issues

---

**最后更新**: 2026-04-08
**版本**: v0.3.1
