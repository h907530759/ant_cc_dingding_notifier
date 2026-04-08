# 🎯 扩展更多 Hooks 支持

您说得对！让我们扩展支持更多有用的 hooks。

## 建议优先支持的 Hooks（与钉钉通知相关）

### 🔥 高优先级（强烈推荐）

1. **SessionStart** - 会话开始通知
   - "开始新的 Claude Code 会话"
   
2. **SessionEnd** - 会话结束通知
   - "Claude Code 会话已结束"

3. **PostToolUseFailure** - 工具失败通知
   - "工具执行失败"（比 error 更详细）

4. **TaskCreated** - 任务创建通知
   - "新任务已创建: [任务名称]"

5. **TaskCompleted** - 任务完成通知
   - "任务已完成: [任务名称]"

6. **CwdChanged** - 目录切换通知
   - "切换到目录: [新目录]"

### 🟡 中优先级（有用）

7. **ConfigChange** - 配置更改通知
   - "配置文件已更改"

8. **SubagentStart** - 子代理启动
   - "启动子代理: [类型]"

9. **SubagentStop** - 子代理完成
   - "子代理已完成"

### ⚪ 低优先级（可选）

10. **UserPromptSubmit** - 提交提示
11. **PermissionRequest** - 权限请求
12. **StopFailure** - API 错误

---

## 实现计划

我可以立即为您实现这些 hooks，让配置时可以选择更多事件类型。

### 新的配置选项

```
🎯 选择要启用的事件类型

┏━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┃ 编号 ┃ 事件           ┃ 说明                           ┃ 推荐 ┃
┡━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│ 1  │ pre_tool_use   │ 敏感操作检测                    │ ⭐ 推荐│
│ 2  │ post_tool_use  │ 工具成功后（仅错误通知）       │ ⭐ 推荐│
│ 3  │ stop           │ 任务完成                        │ ⭐ 推荐│
│ 4  │ session_start  │ 会话开始                        │ ⭐ 推荐│
│ 5  │ session_end    │ 会话结束                        │ ⭐ 推荐│
│ 6  │ tool_failure   │ 工具失败                        │ ⭐ 推荐│
│ 7  │ task_created   │ 任务创建                        │ ⭐ 推荐│
│ 8  │ task_completed │ 任务完成                        │ ⭐ 推荐│
│ 9  │ cwd_changed    │ 目录切换                        │ 可选  │
│ 10 │ config_change  │ 配置更改                        │ 可选  │
│ 11 │ subagent_start │ 子代理启动                      │ 可选  │
│ 12 │ subagent_stop  │ 子代理完成                      │ 可选  │
│ 13 │ notification   │ 权限/提示                       │ 可选  │
└━━━━┴━━━━━━━━━━━━━━━┴━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┴━━━━━━┘

请选择要启用的事件（输入编号，用逗号分隔，如: 1,2,3,4,5）
您的选择 (1,2,3): 
```

---

## 要不要现在实现？

我可以立即为您：

1. ✅ 添加所有 hooks 的实现代码
2. ✅ 更新配置界面，支持选择更多事件
3. ✅ 更新文档，说明每个 hook 的用途
4. ✅ 提供推荐的配置组合

### 推荐配置组合

**日常开发**: `1,2,3,4,5,6,7,8` (核心事件)
**完整监控**: `1,2,3,4,5,6,7,8,9,10,11,12` (所有推荐事件)
**最小化**: `1,3,4,5` (最精简)

您想让我现在就实现这些吗？

Sources:
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Automate workflows with hooks](https://code.claude.com/docs/en/hooks-guide)
