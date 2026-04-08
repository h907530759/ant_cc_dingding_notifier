#!/usr/bin/env python3
"""
调试 SessionStart hook 的实际数据
"""
import json

# 根据 Claude Code 官方文档，SessionStart hook 可能提供的数据
session_start_data = {
    "cwd": "~/workspace/claude_notifyer"
}

print("=" * 60)
print("SessionStart Hook 实际数据测试")
print("=" * 60)
print()
print("官方文档中 SessionStart hook 提供的字段：")
print("- cwd: 当前工作目录")
print()
print("⚠️ 注意：SessionStart hook 可能不提供 sessionId 和 sessionName！")
print()
print("这意味着：")
print("- sessionId 和 sessionName 字段不存在")
print("- 显示 'Unknown' 是因为使用了 .get() 的默认值")
print()
print("解决方案：")
print("1. 移除这两个字段（因为不存在）")
print("2. 或者使用 cwd 生成一个简单的 session 标识")
print("=" * 60)
