#!/bin/bash
# 测试所有 hooks 的钉钉通知

echo "========================================"
echo "触发所有 Hook 的钉钉通知"
echo "========================================"
echo ""

HOOK_DIR="$HOME/.claude-dingtalk/hooks"
PROJECT_NAME="测试项目"

# 1. session_start
echo "1️⃣ 触发 session_start..."
echo '{"sessionId":"test_sess_001","sessionName":"测试会话","cwd":"/Users/suchen/test"}' | python3 "$HOOK_DIR/session_start.py"
echo "✓ session_start 已触发"
echo ""

# 2. task_created
echo "2️⃣ 触发 task_created..."
echo '{"cwd":"/Users/suchen/test","taskId":"task_001","subject":"实现新功能"}' | python3 "$HOOK_DIR/task_created.py"
echo "✓ task_created 已触发"
echo ""

# 3. subagent_start
echo "3️⃣ 触发 subagent_start..."
echo '{"cwd":"/Users/suchen/test","subagentType":"review-agent","subagentId":"agent_001","subagentName":"代码审查代理","task":"审查 PR #123"}' | python3 "$HOOK_DIR/subagent_start.py"
echo "✓ subagent_start 已触发"
echo ""

# 4. task_completed
echo "4️⃣ 触发 task_completed..."
echo '{"cwd":"/Users/suchen/test","taskId":"task_001","subject":"实现新功能"}' | python3 "$HOOK_DIR/task_completed.py"
echo "✓ task_completed 已触发"
echo ""

# 5. subagent_stop
echo "5️⃣ 触发 subagent_stop..."
echo '{"cwd":"/Users/suchen/test","subagentType":"review-agent","subagentId":"agent_001","subagentName":"代码审查代理","task":"审查 PR #123","result":"成功"}' | python3 "$HOOK_DIR/subagent_stop.py"
echo "✓ subagent_stop 已触发"
echo ""

# 6. config_change
echo "6️⃣ 触发 config_change..."
echo '{"cwd":"/Users/suchen/test","path":"/Users/suchen/.claude/settings.json","changeType":"modified"}' | python3 "$HOOK_DIR/config_change.py"
echo "✓ config_change 已触发"
echo ""

# 7. stop
echo "7️⃣ 触发 stop..."
echo '{"cwd":"/Users/suchen/test"}' | python3 "$HOOK_DIR/stop.py"
echo "✓ stop 已触发"
echo ""

# 8. session_end
echo "8️⃣ 触发 session_end..."
echo '{"sessionId":"test_sess_001","sessionName":"测试会话","cwd":"/Users/suchen/test"}' | python3 "$HOOK_DIR/session_end.py"
echo "✓ session_end 已触发"
echo ""

echo "========================================"
echo "✅ 所有 Hook 通知已触发！"
echo "========================================"
echo ""
echo "请检查钉钉群消息，应该收到 8 条通知"
