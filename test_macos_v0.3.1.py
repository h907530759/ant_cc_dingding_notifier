#!/usr/bin/env python3
"""测试更新后的 macOS 通知格式"""
import sys
sys.path.insert(0, 'src')

from claude_dingtalk_notifier.macos_notifier import MacOSNotifier

print("测试 macOS 通知格式（v0.3.1）")
print("=" * 60)
print("\n新格式要求：")
print("1. 标题必须包含：项目名 - 触发原因")
print("2. 内容说明具体事件")
print("\n" + "=" * 60)

notifier = MacOSNotifier(enabled=True, sound=True)

# 测试 1: 会话启动
print("\n1️⃣ 会话启动通知")
print("   标题: my-project - 会话已启动")
print("   内容: Claude Code 新会话已启动")
notifier.send("my-project - 会话已启动", "Claude Code 新会话已启动")
print("   ✓ 已发送")

# 测试 2: 任务完成
print("\n2️⃣ 任务完成通知")
print("   标题: my-project - 任务完成")
print("   内容: 所有任务已完成")
notifier.send("my-project - 任务完成", "所有任务已完成")
print("   ✓ 已发送")

# 测试 3: 敏感操作
print("\n3️⃣ 敏感操作通知")
print("   标题: my-project - 敏感操作")
print("   内容: 即将执行: Bash")
notifier.send("my-project - 敏感操作", "即将执行: Bash")
print("   ✓ 已发送")

print("\n" + "=" * 60)
print("✅ 所有测试通知已发送！")
print("\n新格式特点：")
print("✅ 标题包含项目名")
print("✅ 标题明确说明触发原因")
print("✅ 内容补充具体信息")
print("\n请检查右上角 macOS 通知，查看效果")
