#!/bin/bash

# PyPI 发布脚本
# 用途: 发布 Python 包到 PyPI 或 TestPyPI

set -e

# 检查参数
TEST_MODE=false
if [ "$1" = "--test" ]; then
    TEST_MODE=true
fi

# 仓库配置
if [ "$TEST_MODE" = true ]; then
    REPOSITORY="testpypi"
    echo "🧪 测试模式: 发布到 TestPyPI"
else
    REPOSITORY="pypi"
    echo "🚀 生产模式: 发布到 PyPI"
fi

# 检查是否已构建
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    echo "❌ 未找到构建文件，请先运行 ./build.sh"
    exit 1
fi

# 显示将要发布的文件
echo ""
echo "📦 即将发布的文件:"
ls -lh dist/

# 确认发布
echo ""
if [ "$TEST_MODE" = true ]; then
    echo "⚠️  即将发布到 TestPyPI (测试环境)"
    echo "   测试安装: pip install --index-url https://test.pypi.org/simple/ claude-dingtalk-notifier"
else
    echo "⚠️  即将发布到 PyPI (生产环境)"
    echo "   安装命令: pip install claude-dingtalk-notifier"
fi

echo ""
read -p "确认发布? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ 发布已取消"
    exit 0
fi

# 发布
echo ""
echo "📤 正在发布..."
twine upload --repository $REPOSITORY dist/*

echo ""
echo "✅ 发布完成！"
echo ""
echo "📝 验证安装:"
if [ "$TEST_MODE" = true ]; then
    echo "pip install --index-url https://test.pypi.org/simple/ claude-dingtalk-notifier"
else
    echo "pip install claude-dingtalk-notifier"
fi
echo ""
echo "🌐 查看包:"
if [ "$TEST_MODE" = true ]; then
    echo "https://test.pypi.org/project/claude-dingtalk-notifier/"
else
    echo "https://pypi.org/project/claude-dingtalk-notifier/"
fi
