#!/bin/bash

echo "🔍 macOS 桌面通知快速诊断"
echo "================================"
echo ""

# 测试 1: 系统通知权限
echo "1️⃣ 测试系统通知权限..."
if osascript -e 'display notification "测试消息" with title "测试标题" sound name "default"' 2>/dev/null; then
    echo "   ✅ 系统通知权限正常"
else
    echo "   ❌ 系统通知权限未开启"
    echo "   请打开: 系统设置 > 通知 > Python (或 Terminal)"
    echo "   勾选'允许通知'"
fi
echo ""

# 测试 2: 配置文件
echo "2️⃣ 检查配置文件..."
if [ -f ~/.claude-dingtalk/config.yaml ]; then
    if grep -q "enabled: true" ~/.claude-dingtalk/config.yaml | grep -A 1 "macos:"; then
        echo "   ✅ macOS 通知已启用"
    else
        echo "   ❌ macOS 通知未启用"
        echo "   运行: claude-dingtalk setup"
    fi
else
    echo "   ❌ 配置文件不存在"
    echo "   运行: claude-dingtalk setup"
fi
echo ""

# 测试 3: Hooks 安装
echo "3️⃣ 检查 Hooks..."
if [ -f ~/.claude-dingtalk/hooks/session_start.py ]; then
    macos_count=$(grep -c "MacOSNotifier" ~/.claude-dingtalk/hooks/session_start.py 2>/dev/null || echo "0")
    if [ "$macos_count" -gt 0 ]; then
        echo "   ✅ Hooks 已安装且包含 macOS 通知"
    else
        echo "   ❌ Hooks 未更新"
        echo "   运行: claude-dingtalk hooks install"
    fi
else
    echo "   ❌ Hooks 未安装"
    echo "   运行: claude-dingtalk hooks install"
fi
echo ""

# 测试 4: Python 导入
echo "4️⃣ 测试 Python 模块..."
if python3 -c "from claude_dingtalk_notifier.macos_notifier import MacOSNotifier" 2>/dev/null; then
    echo "   ✅ Python 模块可以正常导入"
else
    echo "   ❌ Python 模块导入失败"
    echo "   请确保已运行: ./install.sh"
fi
echo ""

echo "================================"
echo "📝 下一步操作建议："
echo ""
echo "如果所有检查都通过，运行测试："
echo "  cd ~/ant_cc_dingding_notifier"
echo "  python3 test_macos_notification.py"
echo ""
echo "如果有任何 ❌ 标记，请按照提示修复"
