# 多机器部署 Claude Code 钉钉通知指南

## 📋 使用场景

在多台机器上部署 Claude Code，所有机器连接到同一个钉钉机器人，方便团队监控和协作。

## 🎯 当前限制

### 问题
- ❌ 消息中没有机器/主机标识
- ❌ 无法区分消息来自哪台机器
- ❌ 同名项目会导致混淆

### 示例
```
# 机器 A (MBP-办公)
📁 项目: myproject
✅ 任务完成

# 机器 B (MBP-家用)
📁 项目: myproject
✅ 任务完成

# 问题: 无法区分是哪台机器的消息
```

## ✅ 解决方案

### 方案 1: 添加机器名称标识（推荐）

在每个 Hook 脚本中添加主机名信息。

#### 优点
- ✅ 自动获取机器名称
- ✅ 消息来源清晰
- ✅ 无需手动配置

#### 实现方式

修改 Hook 脚本，在消息数据中添加主机名：

```python
import socket

def main():
    # Get project name
    project = str(Path.cwd().name)

    # Get hostname
    hostname = socket.gethostname()

    message_data = {
        "project": project,
        "hostname": hostname,  # 新增
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
```

消息效果：
```
💻 机器: MBP-Office
📁 项目: myproject
✅ 任务完成
```

### 方案 2: 配置自定义机器标识

在配置文件中添加自定义的机器名称。

#### 优点
- ✅ 可以使用友好的机器名称
- ✅ 灵活配置
- ✅ 支持中文标识

#### 实现方式

**配置文件** (`~/.claude-dingtalk/config.yaml`):
```yaml
dingtalk:
  webhook: "https://oapi.dingtalk.com/robot/send?access_token=xxx"
  secret: "SECxxx"

# 新增：机器标识
machine:
  name: "办公电脑"  # 自定义机器名称
  # 或使用环境变量
  # name: "${MACHINE_NAME}"
```

**Hook 脚本**:
```python
message_data = {
    "project": project,
    "machine": config.machine.name,  # 从配置读取
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
```

消息效果：
```
💻 机器: 办公电脑
📁 项目: myproject
✅ 任务完成
```

### 方案 3: 环境变量配置

使用环境变量来标识不同的机器。

#### 优点
- ✅ 无需修改代码
- ✅ 灵活部署
- ✅ 适合容器化环境

#### 实现方式

**设置环境变量**:
```bash
# 机器 A
export CLAUDE_MACHINE_NAME="开发机"

# 机器 B
export CLAUDE_MACHINE_NAME="测试机"
```

**Hook 脚本**:
```python
import os

message_data = {
    "project": project,
    "hostname": os.getenv("CLAUDE_MACHINE_NAME", socket.gethostname()),
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
```

### 方案 4: 综合方案（最灵活）

结合以上所有方案，按优先级获取机器标识：

```python
import socket
import os

def get_machine_identifier():
    """获取机器标识，优先级：配置 > 环境变量 > 主机名"""
    # 1. 尝试从配置获取
    try:
        config = get_default_config()
        if hasattr(config, 'machine') and config.machine.name:
            return config.machine.name
    except:
        pass

    # 2. 尝试从环境变量获取
    env_name = os.getenv("CLAUDE_MACHINE_NAME")
    if env_name:
        return env_name

    # 3. 使用主机名
    return socket.gethostname()

message_data = {
    "project": project,
    "hostname": get_machine_identifier(),
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
```

## 🚀 快速部署指南

### 机器 A (办公电脑)

1. **安装工具**
   ```bash
   cd /path/to/claude_notifyer
   pip install -e .
   ```

2. **配置钉钉机器人**
   ```bash
   python -m claude_dingtalk_notifier.cli setup
   ```

3. **设置机器标识**
   ```bash
   # 方式 1: 环境变量
   export CLAUDE_MACHINE_NAME="办公电脑"
   echo 'export CLAUDE_MACHINE_NAME="办公电脑"' >> ~/.zshrc

   # 方式 2: 配置文件（需要先实现此功能）
   # 编辑 ~/.claude-dingtalk/config.yaml
   # 添加: machine.name: "办公电脑"
   ```

4. **安装 Hooks**
   ```bash
   python -m claude_dingtalk_notifier.cli hooks install
   ```

### 机器 B (家用电脑)

重复相同步骤，但使用不同的机器标识：

```bash
export CLAUDE_MACHINE_NAME="家用电脑"
```

### 机器 C (服务器)

```bash
export CLAUDE_MACHINE_NAME="生产服务器"
```

## 📨 消息效果对比

### 改进前
```
### ✅ Claude Code 任务完成

📁 **项目:** myproject
⏰ **时间:** 2026-04-03 19:42:30
```

**问题**: 无法区分是哪台机器的消息

### 改进后
```
### ✅ Claude Code 任务完成

💻 **机器:** 办公电脑 (MBP-Office.local)
📁 **项目:** myproject
⏰ **时间:** 2026-04-03 19:42:30
```

**优点**: 清晰显示消息来源

## 🔧 实现步骤

### 步骤 1: 修改 Hook 脚本模板

更新所有 Hook 脚本，添加机器标识：

```python
import socket
import os

def main():
    # Get machine identifier
    hostname = os.getenv("CLAUDE_MACHINE_NAME", socket.gethostname())

    # Get project name
    project = str(Path.cwd().name)

    message_data = {
        "hostname": hostname,  # 新增
        "project": project,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
```

### 步骤 2: 更新消息格式化

更新 `format_claude_message()` 函数，在所有消息中添加机器标识：

```python
def format_claude_message(event_type: str, data: Dict[str, Any]) -> DingTalkMessage:
    hostname = data.get("hostname", "Unknown")
    project = data.get("project", "Unknown")

    # 在所有消息格式中添加机器标识
    text = f"""### ✅ Claude Code 任务完成

💻 **机器:** {hostname}
📁 **项目:** {project}
⏰ **时间:** {data.get('time', '')}
"""
```

### 步骤 3: 更新配置结构

添加可选的机器标识配置：

```python
@dataclass
class MachineConfig:
    """Machine identifier configuration"""
    name: Optional[str] = None  # Custom machine name

@dataclass
class DingTalkConfig:
    """DingTalk configuration"""
    webhook: str
    secret: str
    enabled: bool = True
    machine: MachineConfig = field(default_factory=MachineConfig)
```

## 📋 配置示例

### 场景 1: 个人多台设备

```yaml
# config.yaml
dingtalk:
  webhook: "https://oapi.dingtalk.com/robot/send?access_token=xxx"
  secret: "SECxxx"

machine:
  name: "我的MacBook"  # 可选
```

### 场景 2: 团队共享

```yaml
# config.yaml
dingtalk:
  webhook: "https://oapi.dingtalk.com/robot/send?access_token=xxx"
  secret: "SECxxx"

machine:
  name: "张三的电脑"  # 团队成员标识
```

### 场景 3: 环境区分

```yaml
# 开发环境
machine:
  name: "开发环境-张三"

# 测试环境
machine:
  name: "测试环境-共享"

# 生产环境
machine:
  name: "生产服务器"
```

## 🎨 消息样式建议

### 简洁样式
```
✅ 任务完成 [办公电脑] myproject
```

### 详细样式
```
### ✅ Claude Code 任务完成

💻 **机器:** 办公电脑 (MBP-Office.local)
📁 **项目:** myproject
⏰ **时间:** 2026-04-03 19:42:30
📊 **状态:** 成功
```

### 团队样式
```
### ✅ Claude Code 任务完成

👤 **用户:** 张三
💻 **机器:** 办公电脑
📁 **项目:** myproject
⏰ **时间:** 2026-04-03 19:42:30
```

## 🔍 消息过滤和路由

### 使用 @ 机制

可以在不同机器上使用不同的关键词，然后在群中 @ 相关人员：

```python
# 办公电脑
message = f"@张三 任务完成: {project}"

# 家用电脑
message = f"@张三 (家庭) 任务完成: {project}"
```

### 使用多个钉钉机器人

为不同机器使用不同的机器人：

```yaml
# 机器 A
dingtalk:
  webhook: "${WEBHOOK_OFFICE}"  # 办公电脑机器人
  machine:
    name: "办公电脑"

# 机器 B
dingtalk:
  webhook: "${WEBHOOK_HOME}"  # 家用电脑机器人
  machine:
    name: "家用电脑"
```

## ⚠️ 注意事项

1. **安全性**
   - 确保钉钉机器人 webhook 不要泄露
   - 使用加签验证消息来源
   - 定期更换密钥

2. **消息频率**
   - 多台机器可能导致消息过多
   - 考虑添加消息去重或合并
   - 设置合理的通知事件

3. **命名规范**
   - 使用清晰的机器命名
   - 包含环境信息（开发/测试/生产）
   - 包含用户信息（团队场景）

4. **配置管理**
   - 使用版本控制管理配置模板
   - 敏感信息使用环境变量
   - 文档化每台机器的配置

## 📊 监控和调试

### 消息追踪

添加消息 ID 用于追踪：

```python
import uuid

message_data = {
    "message_id": str(uuid.uuid4())[:8],  # 短 ID
    "hostname": hostname,
    "project": project,
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
```

### 健康检查

定期检查连接状态：

```bash
# 测试每台机器的通知
ssh machine-a "cd /path/to/claude_notifyer && python -m claude_dingtalk_notifier.cli test"
ssh machine-b "cd /path/to/claude_notifyer && python -m claude_dingtalk_notifier.cli test"
```

## 🚀 下一步

### 立即可用（无需修改）

当前版本已经可以在多台机器上使用，只需要：

1. 每台机器执行相同安装步骤
2. 使用相同的钉钉机器人配置
3. 通过项目名称区分消息

### 改进版本（需要实现）

添加机器标识功能，让消息来源更清晰。

---

**总结**: 多机器部署完全可行，建议添加机器标识功能以便更好地区分消息来源。
