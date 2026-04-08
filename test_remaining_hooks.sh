#!/bin/bash
# 测试剩余的 hooks

echo "========================================"
echo "触发剩余 Hook 的钉钉通知"
echo "========================================"
echo ""

HOOK_DIR="$HOME/.claude-dingtalk/hooks"

# 9. pre_tool_use (普通)
echo "9️⃣ 触发 pre_tool_use (普通操作)..."
echo '{"cwd":"~/test","name":"Bash","input":{"command":"ls -la"}}' | python3 "$HOOK_DIR/pre_tool_use.py"
echo "✓ pre_tool_use (普通) 已触发"
echo ""

# 10. pre_tool_use (敏感操作)
echo "🔟 触发 pre_tool_use (敏感操作)..."
echo '{"cwd":"~/test","name":"Bash","input":{"command":"rm -rf /tmp/test"}}' | python3 "$HOOK_DIR/pre_tool_use.py"
echo "✓ pre_tool_use (敏感) 已触发"
echo ""

# 11. post_tool_use (错误)
echo "1️⃣1️⃣ 触发 post_tool_use (错误)..."
echo '{"cwd":"~/test","name":"Bash","hasError":true}' | python3 "$HOOK_DIR/post_tool_use.py"
echo "✓ post_tool_use (错误) 已触发"
echo ""

# 12. stop_failure
echo "1️⃣2️⃣ 触发 stop_failure..."
echo '{"cwd":"~/test","error":"API rate limit exceeded"}' | python3 "$HOOK_DIR/stop_failure.py"
echo "✓ stop_failure 已触发"
echo ""

# 13. tool_failure
echo "1️⃣3️⃣ 触发 tool_failure..."
echo '{"cwd":"~/test","name":"WebSearch","error":"Connection timeout"}' | python3 "$HOOK_DIR/tool_failure.py"
echo "✓ tool_failure 已触发"
echo ""

# 14. cwd_changed
echo "1️⃣4️⃣ 触发 cwd_changed..."
echo '{"cwd":"~/test","old_cwd":"~/old","new_cwd":"~/new"}' | python3 "$HOOK_DIR/cwd_changed.py"
echo "✓ cwd_changed 已触发"
echo ""

# 15. notification (权限请求)
echo "1️⃣5️⃣ 触发 notification (权限请求)..."
echo '{"cwd":"~/test","type":"permission_prompt","text":"需要执行删除操作"}' | python3 "$HOOK_DIR/notification.py"
echo "✓ notification (权限) 已触发"
echo ""

echo "========================================"
echo "✅ 剩余 Hook 通知已触发！"
echo "========================================"
echo ""
echo "总共触发了 15 个 hooks，请检查钉钉群"
