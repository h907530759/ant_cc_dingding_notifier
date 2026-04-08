# 👥 团队部署指南 - Claude Code 钉钉通知

## 🎯 目标

让团队成员能够**快速、简单**地在不同的 Mac 电脑上部署和使用本工具。

---

## 📋 当前问题分析

### 问题 1: 项目路径硬编码
```bash
# ❌ 当前的 wrapper 脚本
export PYTHONPATH="/Users/suchen/workspace/claude_notifyer/src:$PYTHONPATH"
```
每个人克隆项目的路径不同，导致无法复用。

### 问题 2: Python 环境差异
- **Xcode Python**: 无法安装用户包（禁用 site-packages）
- **Homebrew Python**: 可正常安装
- **pyenv/asdf**: 可正常安装
- **conda**: 可正常安装

### 问题 3: 安装复杂度高
需要手动配置 PYTHONPATH、创建 wrapper 脚本等。

---

## ✅ 解决方案

### 方案 1: 智能安装脚本（推荐）⭐

创建一个自动检测环境的安装脚本。

### 方案 2: 使用 Homebrew Python

建议团队成员安装 Homebrew Python。

### 方案 3: 容器化部署

使用 Docker 容器（可选）。

---

## 🚀 方案 1: 智能安装脚本

### 步骤 1: 创建智能安装脚本

我会创建一个 `install.sh` 脚本，自动：
- ✅ 检测 Python 环境
- ✅ 检测项目路径
- ✅ 选择最佳安装方式
- ✅ 自动创建 wrapper 脚本
- ✅ 配置 PATH

### 步骤 2: 用户只需执行

```bash
git clone <repo-url> claude_notifyer
cd claude_notifyer
./install.sh
```

---

## 🛠️ 实现智能安装脚本

让我创建这个安装脚本：
