# 更新日志

## [0.2.1] - 2026-04-03

### Bug 修复 🐛

#### 关键修复：Hook 名称错误

**问题**: 版本 0.2.0 使用了不存在的 Hook 名称 `"error"`，这不符合 Claude Code 官方规范。

**修复**:
- ✅ 将 `"error"` Hook 更正为官方支持的 `"stop_failure"` (对应 `StopFailure` Hook)
- ✅ 根据 Claude Code 官方文档验证：https://code.claude.com/docs/en/hooks
- ✅ 自动迁移：已有配置中的 "error" 设置会自动迁移到 "stop_failure"
- ✅ 更新所有相关代码：CLI、配置、消息格式化、Hook 脚本生成

#### 关键修复：Hooks 配置格式错误 ⚠️

**问题**: 0.2.1 初版使用了错误的 Hooks 配置格式，导致所有 Hooks 显示 "Invalid key in record" 错误。

**修复**:
- ✅ 修正 Hooks 配置格式为符合 Claude Code 官方规范的数组结构
- ✅ 添加自动清理旧格式 Hooks 的逻辑
- ✅ 修复缺失的 `EventConfig` 导入
- ✅ 更新 hooks 显示逻辑

#### 关键修复：Hook 脚本导入路径错误 ⚠️

**问题**: Hook 脚本执行时出现 `NameError: name 'get_default_config' is not defined` 错误。

**修复**:
- ✅ 修正 Hook 脚本的 Python 路径设置，正确指向 `src` 目录
- ✅ 添加 `EventConfig` 类的导入
- ✅ 改进导入失败时的错误处理，优雅退出而不是中断
- ✅ 自动检测正确的包路径

**正确的格式**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hook.py"
          }
        ]
      }
    ]
  }
}
```

### 改进

- 更新默认推荐事件，现在包括 `stop_failure` (事件 1-8)
- 在配置加载时添加自动迁移逻辑，确保平滑升级
- 更新 Hook 安装脚本，生成正确的 `stop_failure.py` 脚本
- Hook 安装时自动清理旧格式的配置，避免重复

### 文档

- 新增 [VERSION_0.2.1.md](VERSION_0.2.1.md) - 详细的 Bug 修复说明
- 更新官方 Hook 覆盖率统计：14/26 (53.8%)
- 添加官方文档验证链接

### 技术细节

**修改的文件**:
- `src/claude_dingtalk_notifier/__init__.py` - 版本号更新
- `src/claude_dingtalk_notifier/cli.py` - 事件列表和 Hook 配置
- `src/claude_dingtalk_notifier/config.py` - 默认事件和迁移逻辑
- `src/claude_dingtalk_notifier/dingtalk.py` - 消息格式化
- `pyproject.toml` - 版本号更新

**配置迁移**:
```python
# 自动迁移旧 "error" 到 "stop_failure"
if "error" in self.events:
    if "stop_failure" not in self.events:
        self.events["stop_failure"] = self.events["error"]
    del self.events["error"]
```

### 升级说明

从 0.2.0 升级到 0.2.1：
1. 拉取最新代码
2. 运行 `./run.sh setup` (可选，查看新事件列表)
3. 运行 `./run.sh hooks install` (安装正确的 Hook)
4. 配置会自动迁移 "error" → "stop_failure"

---

## [0.2.0] - 2026-04-03

### 重大更新 🎉

#### Hook 事件大幅扩展
- ✅ 从 4 个 hook 事件扩展到 12 个
- ✅ 新增会话管理事件（session_start, session_end）
- ✅ 新增任务管理事件（task_created, task_completed）
- ✅ 新增工具失败事件（tool_failure）
- ✅ 新增目录切换事件（cwd_changed）
- ✅ 新增配置更改事件（config_change）
- ✅ 新增子代理事件（subagent_start, subagent_stop）

### 新功能

#### 1. 交互式 Hook 事件选择增强
- ✅ 配置时列出 12 个可用的 Hook 事件（之前只有 4 个）
- ✅ 分类显示：高优先级（⭐ 推荐）和可选事件
- ✅ 默认启用前 8 个推荐事件（1-8）
- ✅ 支持自定义组合
- ✅ 显示每个事件的详细说明

#### 2. Hook 脚本自动生成
- ✅ 自动为所有启用的 hook 事件生成对应的 Python 脚本
- ✅ 脚本包含完整的事件处理逻辑
- ✅ 自动设置执行权限（0o755）

#### 3. 消息格式优化
- ✅ 为所有新事件类型添加专门的消息格式化
- ✅ 使用 Markdown 格式提供更好的可读性
- ✅ 包含详细的上下文信息（项目、时间、任务等）

### 改进

- 更新配置文件结构，支持所有新事件
- 优化 hook 安装流程，仅安装用户启用的 hooks
- 改进事件选择 UI，更清晰的事件分类
- 更新文档和示例

### 技术细节

- 新增 8 个 hook 脚本模板
- 扩展 format_claude_message 函数支持所有新事件
- 更新 config.py 默认事件配置
- 改进 hooks_config 生成逻辑

### 文档更新

- 更新 [HOOKS_EXPANSION.md](HOOKS_EXPANSION.md) - 完整的 hook 扩展计划
- 更新 [CHANGELOG.md](CHANGELOG.md) - 版本历史

## [0.1.1] - 2026-04-03

### 新增功能 🎉

#### 1. 交互式 Hook 事件选择
- ✅ 配置时列出所有可用的 Hook 事件
- ✅ 用户可以选择要启用哪些事件
- ✅ 提供推荐配置（1,2,3）
- ✅ 支持自定义组合（如：1,3 或 2,4）
- ✅ 显示每个事件的说明和推荐度

#### 2. 多配置文件路径管理
- ✅ 自动检测现有 settings.json 文件
- ✅ 支持添加多个自定义路径
- ✅ 路径验证和提示
- ✅ 显示当前已配置的所有路径
- ✅ 支持继续添加更多路径

### 改进

- 优化配置流程，更加直观
- 添加详细的配置说明
- 改进错误提示
- 显示最终配置摘要

### 文档更新

- 新增 [DEMO.md](DEMO.md) - Hook 事件选择演示
- 新增 [FEATURES.md](FEATURES.md) - 完整功能说明
- 更新 [INSTALL.md](INSTALL.md) - 安装指南
- 更新 [QUICKSTART.md](QUICKSTART.md) - 快速开始

## [0.1.0] - 2026-04-03

### 新增
- 🎉 首次发布
- ✅ 支持钉钉机器人消息通知
- ✅ 支持 4 种 Claude Code hooks（pre_tool_use, post_tool_use, stop, notification）
- ✅ 敏感操作自动检测
- ✅ 任务完成通知
- ✅ 多 settings.json 文件支持
- ✅ 交互式配置向导
- ✅ 完整的 CLI 工具
- ✅ 美观的终端输出（使用 Rich）
- ✅ 配置验证和测试功能

### 功能特性
- PreToolUse: 工具使用前触发，检测敏感操作
- PostToolUse: 工具使用后触发，记录错误
- Stop: Claude 停止时触发，发送完成通知
- Notification: 处理权限请求

### 配置支持
- 支持多个 settings.json 路径
- YAML 配置文件
- 环境变量配置
- 事件开关配置
- 敏感操作模式自定义

### 文档
- 完整的 README
- 使用指南
- 测试用例
