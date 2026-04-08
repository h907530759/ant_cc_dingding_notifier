# 📨 Hook 消息内容对照表 (v0.2.3)

## 📋 所有 Hook 的钉钉消息内容

| Hook 名称 | 消息标题 | 消息内容 | 默认状态 |
|---------|---------|---------|---------|
| **stop** | ✅ 工作已结束 | `### ✅ 工作结束`<br><br>`🎉 所有任务已完成，工作结束！`<br><br>`**📂 项目:** {project}`<br>`**⏰ 时间:** {time}`<br><br>`💡 工作已全部完成，可以查看结果了` | ✅ 启用 |
| **session_start** | 🚀 会话已启动 | `### 🚀 新会话已启动`<br>`**📂 项目:** {project}`<br>`**🆔 会话ID:** {session_id}`<br>`**📝 会话名称:** {session_name}`<br>`**⏰ 开始时间:** {time}`<br><br>`💡 让我们开始工作吧！` | ✅ 启用 |
| **session_end** | 👋 会话已结束 | `### 👋 会话已结束`<br>`**📂 项目:** {project}`<br>`**🆔 会话ID:** {session_id}`<br>`**📝 会话名称:** {session_name}`<br>`**⏰ 结束时间:** {time}`<br><br>`👋 感谢使用，再见！` | ✅ 启用 |
| **config_change** | ⚙️ 配置文件已更改 | `### ⚙️ 配置文件已更改`<br>`**📂 项目:** {project}`<br>`**📁 文件:** {config_path}`<br><br>`💡 Claude Code 配置文件已更新` | ❌ 禁用 |
| **subagent_start** | 🤖 子代理已启动 | `### 🤖 子代理已启动`<br>`**📂 项目:** {project}`<br>`**🆔 代理ID:** {agent_id}`<br>`**📝 代理名称:** {agent_name}`<br>`**🔧 代理类型:** {agent_type}`<br><br>`🚀 子代理开始工作...` | ❌ 禁用 |
| **subagent_stop** | ✅ 子代理工作已结束 | `### ✅ 子代理工作已完成`<br>`**📂 项目:** {project}`<br>`**🆔 代理ID:** {agent_id}`<br>`**📝 代理名称:** {agent_name}`<br>`**🔧 代理类型:** {agent_type}`<br><br>`✅ 子代理任务完成，工作已结束` | ❌ 禁用 |

---

## 📊 v0.2.2 vs v0.2.3 对比

### stop Hook

| 项目 | v0.2.2 | v0.2.3 |
|------|--------|--------|
| **标题** | ✅ Claude Code 任务完成 | ✅ 工作已结束 |
| **项目字段** | project | project |
| **数据来源** | Path.cwd().name | stdin (cwd) |
| **特点** | 强调"任务完成" | 强调"工作结束" |

### session_start Hook

| 项目 | v0.2.2 | v0.2.3 |
|------|--------|--------|
| **标题** | 🚀 Claude Code 会话开始 | 🚀 会话已启动 |
| **项目字段** | project | project |
| **会话ID** | ❌ 无 | ✅ session_id |
| **会话名称** | ❌ 无 | ✅ session_name |
| **数据来源** | Path.cwd().name | stdin (cwd, sessionId, sessionName) |

### session_end Hook

| 项目 | v0.2.2 | v0.2.3 |
|------|--------|--------|
| **标题** | 👋 Claude Code 会话结束 | 👋 会话已结束 |
| **项目字段** | project | project |
| **会话ID** | ❌ 无 | ✅ session_id |
| **会话名称** | ❌ 无 | ✅ session_name |
| **数据来源** | Path.cwd().name | stdin (cwd, sessionId, sessionName) |

### config_change Hook

| 项目 | v0.2.2 | v0.2.3 |
|------|--------|--------|
| **标题** | ⚙️ Claude Code 配置更改 | ⚙️ 配置文件已更改 |
| **项目字段** | project | project |
| **文件路径** | ❌ 无 | ✅ config_path |
| **数据来源** | stdin (cwd) | stdin (cwd, path) |

### subagent_start Hook

| 项目 | v0.2.2 | v0.2.3 |
|------|--------|--------|
| **标题** | 🤖 Claude Code 子代理启动 | 🤖 子代理已启动 |
| **项目字段** | project | project |
| **代理ID** | ❌ 无 | ✅ agent_id |
| **代理名称** | ❌ 无 | ✅ agent_name |
| **代理类型** | agent_type | agent_type |
| **数据来源** | stdin (cwd, subagentType) | stdin (cwd, subagentType, subagentId, subagentName) |

### subagent_stop Hook

| 项目 | v0.2.2 | v0.2.3 |
|------|--------|--------|
| **标题** | 🤖 Claude Code 子代理完成 | ✅ 子代理工作已结束 |
| **项目字段** | project | project |
| **代理ID** | ❌ 无 | ✅ agent_id |
| **代理名称** | ❌ 无 | ✅ agent_name |
| **代理类型** | agent_type | agent_type |
| **数据来源** | stdin (cwd, subagentType) | stdin (cwd, subagentType, subagentId, subagentName) |
| **强调** | "任务完成" | "工作已结束" |

---

## 🔍 Hook 数据字段映射

### session_start / session_end

| 数据字段 | Hook 输入 | 消息变量 | 说明 |
|---------|----------|---------|------|
| 项目路径 | `cwd` | `project` | 当前工作目录 |
| 会话ID | `sessionId` | `session_id` | 会话唯一标识 |
| 会话名称 | `sessionName` | `session_name` | 会话显示名称 |
| 时间 | - | `time` | 当前时间 (datetime.now()) |

### config_change

| 数据字段 | Hook 输入 | 消息变量 | 说明 |
|---------|----------|---------|------|
| 项目路径 | `cwd` | `project` | 当前工作目录 |
| 文件路径 | `path` | `config_path` | 配置文件的完整路径 |

### subagent_start / subagent_stop

| 数据字段 | Hook 输入 | 消息变量 | 说明 |
|---------|----------|---------|------|
| 项目路径 | `cwd` | `project` | 当前工作目录 |
| 代理ID | `subagentId` | `agent_id` | 子代理唯一标识 |
| 代理名称 | `subagentName` | `agent_name` | 子代理显示名称 |
| 代理类型 | `subagentType` | `agent_type` | 子代理类型 (如 "review-agent") |

### stop

| 数据字段 | Hook 输入 | 消息变量 | 说明 |
|---------|----------|---------|------|
| 项目路径 | `cwd` | `project` | 当前工作目录 |
| 时间 | - | `time` | 当前时间 (datetime.now()) |

---

## ✅ 改进总结

### 信息完整度

| Hook | v0.2.2 | v0.2.3 | 改进 |
|------|--------|--------|------|
| **stop** | ⭐⭐⭐ | ⭐⭐⭐⭐ | 标题更简洁 |
| **session_start** | ⭐⭐ | ⭐⭐⭐⭐⭐ | 新增 ID 和名称 |
| **session_end** | ⭐⭐ | ⭐⭐⭐⭐⭐ | 新增 ID 和名称 |
| **config_change** | ⭐⭐ | ⭐⭐⭐⭐ | 新增文件路径 |
| **subagent_start** | ⭐⭐ | ⭐⭐⭐⭐⭐ | 新增 ID 和名称 |
| **subagent_stop** | ⭐⭐ | ⭐⭐⭐⭐⭐ | 新增 ID 和名称 + 标题改进 |

### 用户体验

| 改进点 | 效果 |
|-------|------|
| **显示 ID** | ✅ 便于追踪和区分 |
| **显示名称** | ✅ 更易识别 |
| **显示文件路径** | ✅ 明确知道变更位置 |
| **标题简化** | ✅ 更简洁专业 |
| **强调工作结束** | ✅ 更符合用户需求 |

---

**版本**: v0.2.3
**更新日期**: 2026-04-04
**状态**: ✅ 完成并测试通过
