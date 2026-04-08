#!/bin/bash

# PyPI 构建脚本
# 用途: 构建 Python 包分发包

set -e

echo "🔨 开始构建 claude-dingtalk-notifier..."

# 检查必要工具
echo "📋 检查构建工具..."
python3 -m pip install --upgrade build twine setuptools wheel

# 清理旧的构建文件
echo "🧹 清理旧构建文件..."
rm -rf dist/ build/ *.egg-info src/*.egg-info

# 构建包
echo "📦 构建分发包..."
python3 -m build

# 检查包
echo "🔍 检查分发包..."
twine check dist/*

# 显示构建结果
echo ""
echo "✅ 构建完成！"
echo "📁 构建文件:"
ls -lh dist/

echo ""
echo "📝 下一步:"
echo "1. 测试安装: pip install dist/claude-dingtalk-notifier-*.whl"
echo "2. 发布到 TestPyPI: ./publish.sh --test"
echo "3. 发布到 PyPI: ./publish.sh"
