#!/bin/bash

# 发布前检查脚本
# 用途: 检查项目是否准备好发布

set -e

echo "🔍 检查发布准备状态..."
echo ""

ERRORS=0
WARNINGS=0

# 检查版本号一致性
echo "📋 1. 检查版本号..."
PYPROJECT_VERSION=$(grep "^version = " pyproject.toml | sed 's/version = "\(.*\)"/\1/')
SETUP_VERSION=$(grep "^version " setup.cfg | sed 's/version = \(.*\)/\1/')

if [ "$PYPROJECT_VERSION" = "$SETUP_VERSION" ]; then
    echo "   ✅ 版本号一致: $PYPROJECT_VERSION"
else
    echo "   ❌ 版本号不一致!"
    echo "      pyproject.toml: $PYPROJECT_VERSION"
    echo "      setup.cfg: $SETUP_VERSION"
    ((ERRORS++))
fi

# 检查必要文件
echo ""
echo "📋 2. 检查必要文件..."
REQUIRED_FILES=(
    "README.md"
    "pyproject.toml"
    "setup.cfg"
    "LICENSE"
    "src/claude_dingtalk_notifier/__init__.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ 缺少: $file"
        ((ERRORS++))
    fi
done

# 检查 __version__
echo ""
echo "📋 3. 检查 __version__ 定义..."
if grep -q "__version__" src/claude_dingtalk_notifier/__init__.py; then
    INIT_VERSION=$(grep "__version__" src/claude_dingtalk_notifier/__init__.py | sed 's/.*"\(.*\)"/\1/')
    if [ "$INIT_VERSION" = "$PYPROJECT_VERSION" ]; then
        echo "   ✅ __version__ = $INIT_VERSION"
    else
        echo "   ⚠️  __version__ ($INIT_VERSION) 与 pyproject.toml ($PYPROJECT_VERSION) 不一致"
        ((WARNINGS++))
    fi
else
    echo "   ⚠️  未在 __init__.py 中定义 __version__"
    ((WARNINGS++))
fi

# 检查构建工具
echo ""
echo "📋 4. 检查构建工具..."
for tool in "build" "twine"; do
    if python -c "import $tool" 2>/dev/null; then
        echo "   ✅ $tool 已安装"
    else
        echo "   ❌ $tool 未安装，运行: pip install $tool"
        ((ERRORS++))
    fi
done

# 检查语法
echo ""
echo "📋 5. 检查 Python 语法..."
if python -m py_compile src/claude_dingtalk_notifier/*.py src/claude_dingtalk_notifier/hooks/*.py 2>/dev/null; then
    echo "   ✅ 所有 Python 文件语法正确"
else
    echo "   ❌ 存在语法错误"
    ((ERRORS++))
fi

# 检查文档
echo ""
echo "📋 6. 检查文档..."
DOC_FILES=("README.md" "INSTALL.md" "QUICKSTART.md" "CHANGELOG.md")
for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ⚠️  建议添加: $file"
        ((WARNINGS++))
    fi
done

# 总结
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ 所有检查通过！可以开始构建和发布"
    echo ""
    echo "📝 下一步:"
    echo "1. ./build.sh          # 构建包"
    echo "2. ./publish.sh --test # 测试发布"
    echo "3. ./publish.sh        # 正式发布"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  发现 $WARNINGS 个警告，建议修复后发布"
    exit 0
else
    echo "❌ 发现 $ERRORS 个错误和 $WARNINGS 个警告，请修复后再发布"
    exit 1
fi
