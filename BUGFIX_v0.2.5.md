# 🐛 Bug 修复 - v0.2.5

**发布日期**: 2026-04-04
**版本类型**: Bug 修复
**从版本**: v0.2.4

---

## 🐛 问题描述

### 用户反馈

用户收到的 stop hook 通知显示：
```
✅ 工作已结束
📂 项目: claude_notifyer
📝 结束原因: Unknown  ← 问题：显示 "Unknown"
⏰ 时间: 2026-04-04 23:15:03
💡 工作已结束，可以查看结果了
```

---

## 🔍 根本原因

### 问题 1: Stop hook 没有提供 reason 字段

**原因**:
- Claude Code 的 Stop hook **根本不传递** `reason` 字段
- 代码尝试从 stdin 读取 `reason` 字段，但实际不存在
- 导致显示 "Unknown"

**实际情况**:
```python
# Stop hook 只传递 cwd 字段
{
    "cwd": "/Users/suchen/workspace/claude_notifyer"
}
```

### 问题 2: 其他 hook 字段可能缺失

类似问题可能存在于：
- **config_change**: `changeType` 字段可能不存在
- **subagent_start/stop**: `task` 和 `result` 字段可能不存在

---

## ✅ 修复方案

### 1. stop Hook - 移除 reason 字段

**修改前 (v0.2.4)**:
```python
# 尝试读取不存在的字段
reason = input_data.get("reason", "Unknown")
reason_map = {...}
reason_text = reason_map.get(reason, reason)

# 消息包含 reason
title=f"✅ 工作已结束 - {reason}"
**📝 结束原因:** {reason}
```

**修改后 (v0.2.5)**:
```python
# 不尝试读取 reason，使用简单的结束消息
title="✅ 工作已结束"
# 移除了 "结束原因" 字段
```

**效果**:
```markdown
✅ 工作已结束

### ✅ 工作已结束
**📂 项目:** claude_notifyer
**⏰ 时间:** 2026-04-04 23:15:03
💡 工作已全部完成，可以查看结果了
```

---

### 2. config_change Hook - changeType 默认值

**修改**:
```python
# 如果 changeType 不存在，默认为 "modified"
change_type = input_data.get("changeType", "modified")
```

**效果**:
- 即使字段不存在，也会显示"修改"而不是"Unknown"

---

### 3. subagent_start/stop Hooks - task 和 result 默认值

**修改**:
```python
# subagent_start
task = input_data.get("task", f"{agent_name}任务")

# subagent_stop
task = input_data.get("task", f"{agent_name}任务")
result = input_data.get("result", "已完成")
```

**效果**:
- 如果字段不存在，显示"Code Review Agent任务"而不是"Unknown"
- 如果字段不存在，显示"已完成"而不是"Unknown"

---

## 📋 具体修改

### dingtalk.py (消息格式化)

**stop hook**:
```python
# 移除了 reason 字段
elif event_type == "stop":
    return DingTalkMessage(
        title="✅ 工作已结束",  # 不再包含 reason
        text=f"""### ✅ 工作已结束

**📂 项目:** {data.get("project", "Unknown")}
**⏰ 时间:** {data.get("time", "")}

💡 工作已全部完成，可以查看结果了""",
        msg_type="markdown"
    )
```

### cli.py (Hook 脚本)

**stop_hook**:
```python
# 移除了 reason 读取逻辑
# 使用 try-except 处理可能没有 stdin 数据的情况
try:
    input_data = json.load(sys.stdin)
    project = input_data.get("cwd", "Unknown")
except:
    project = str(Path.cwd().name)

message_data = {
    "project": project,
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 不再包含 reason
}
```

**config_change_hook**:
```python
# changeType 默认为 "modified"
change_type = input_data.get("changeType", "modified")
```

**subagent_start_hook**:
```python
# task 默认为 "{agent_name}任务"
task = input_data.get("task", f"{agent_name}任务")
```

**subagent_stop_hook**:
```python
# task 默认为 "{agent_name}任务"
# result 默认为 "已完成"
task = input_data.get("task", f"{agent_name}任务")
result = input_data.get("result", "已完成")
```

---

## 🔄 升级步骤

### 对于用户

**重要**: 需要重新安装 hooks 才能生效！

```bash
# 1. 拉取最新代码
cd claude_notifyer
git pull

# 2. 重新安装（会自动更新版本）
./install.sh
source ~/.zshrc

# 3. 重新安装 hooks（必须！）
cdn hooks install

# 4. 验证安装
cdn hooks status
```

### 验证效果

重新安装后，stop hook 通知应该显示为：

```markdown
✅ 工作已结束

### ✅ 工作已结束
**📂 项目:** your-project
**⏰ 时间:** 2026-04-04 23:30:00
💡 工作已全部完成，可以查看结果了
```

✅ **不再显示 "Unknown"**

---

## 📊 字段可用性对照表

| Hook | 字段 | 是否存在 | 默认值 | 处理方式 |
|------|------|---------|-------|---------|
| **stop** | reason | ❌ 不存在 | - | 移除该字段 |
| **config_change** | changeType | ✅ 通常存在 | "modified" | 使用默认值 |
| **subagent_start** | task | ✅ 通常存在 | "{agent_name}任务" | 使用默认值 |
| **subagent_stop** | task | ✅ 通常存在 | "{agent_name}任务" | 使用默认值 |
| **subagent_stop** | result | ✅ 通常存在 | "已完成" | 使用默认值 |

---

## 🎓 经验教训

### 1. 不要假设字段存在

**错误做法**:
```python
reason = input_data.get("reason", "Unknown")  # 显示 "Unknown" 很尴尬
```

**正确做法**:
```python
# 如果字段可能不存在，应该在代码逻辑中处理
# 而不是显示 "Unknown" 给用户
```

### 2. 验证 Hook 数据结构

在添加新字段前，应该：
1. 查阅官方文档确认字段存在
2. 测试验证字段实际存在
3. 为可能缺失的字段提供合理的默认值

### 3. 用户友好的错误处理

- ❌ 显示 "Unknown"
- ✅ 移除该字段或使用合理的默认值

---

## 📚 相关文档

- **官方 Hooks 文档**: https://code.claude.com/docs/en/hooks
- **MESSAGE_CONTENT_V0.2.4.md** - v0.2.4 消息内容说明

---

**更新日期**: 2026-04-04
**版本**: v0.2.5
**状态**: ✅ Bug 已修复
