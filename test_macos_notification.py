#!/usr/bin/env python3
"""测试 macOS 通知功能"""
import sys
sys.path.insert(0, 'src')

from claude_dingtalk_notifier.macos_notifier import MacOSNotifier

print("测试 macOS 桌面通知功能\n")
print("=" * 60)

# 创建通知器
notifier = MacOSNotifier(enabled=True, sound=True)

# 测试 1: 会话启动
print("\n1️⃣ 测试会话启动通知...")
notifier.send("🚀 会话已启动", "test-project 新会话已启动")
print("✓ 已发送")

# 测试 2: 工作完成
print("\n2️⃣ 测试工作完成通知...")
notifier.send("✅ 工作已结束", "test-project 所有任务已完成")
print("✓ 已发送")

# 测试 3: 敏感操作
print("\n3️⃣ 测试敏感操作通知...")
notifier.send("🔐 敏感操作检测", "即将执行: rm -rf")
print("✓ 已发送")

print("\n" + "=" * 60)
print("✅ 所有测试通知已发送！")
print("\n请检查右上角 macOS 通知中心")
print("如果多条通知同时弹出，会自动堆叠显示为列表")
