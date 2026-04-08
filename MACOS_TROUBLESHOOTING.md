# 🍎 macOS 通知故障排除指南

本文档帮助你排查和解决 macOS 桌面通知无法弹出的问题。

---

## 🎯 最常见原因（90%的情况）

### ⚠️ 系统通知权限未开启

**症状**：
- 钉钉群正常收到消息
- Mac 桌面完全没有通知
- 没有声音，也没有弹窗

**原因**：Python 或 Terminal 应用没有通知权限（**最常见！**）

**快速修复（30秒解决）**：

#### 步骤 1: 打开系统设置

```bash
# 方法 1: 点击左上角  菜单
# 系统设置 > 通知

# 方法 2: 使用命令直接打开
open "x-apple.systempreferences:com.apple.preference.notifications"
```

#### 步骤 2: 找到 Python 或 Terminal

在左侧应用列表中找到：
- **Python**（如果使用安装方式）
- **Terminal**（如果使用 run.sh 方式）
- **iTerm2**（如果使用 iTerm）

#### 步骤 3: 启用通知

确保以下选项已开启：

```
✅ 允许通知                    ← 必须勾选！
✅ 横幅样式: 持续                ← 推荐（显示时间更长）
✅ 声音: 默认                    ← 可选
```

#### 步骤 4: 安装 terminal-notifier

```bash
# 检查是否已安装
which terminal-notifier

# 如果未安装，使用 Homebrew 安装
brew install terminal-notifier
```

#### 步骤 5: 测试通知

```bash
# 测试是否能弹出通知
terminal-notifier -title "测试标题" -message "测试消息" -sound default

# 如果成功弹出，说明安装成功
```

---

## 📋 其他问题（10%的情况）

### 问题 1: macOS 通知功能未启用

**症状**：权限设置正常，但还是没有通知

**检查配置**：
```bash
cat ~/.claude-dingtalk/config.yaml | grep -A 2 macos
```

**期望输出**：
```yaml
macos:
  enabled: true   # 必须是 true
  sound: true
```

**如果是 `enabled: false`**：
```bash
# 重新配置
cdn setup
# 当问到"是否启用 macOS 桌面通知？"时选择 y
```

---

### 问题 2: Hooks 未更新

**症状**：权限正常，配置正确，但还是没通知

**重新安装 Hooks**（重要！）：
```bash
# 配置修改后必须重新安装 hooks
cdn hooks install
```

**验证安装**：
```bash
# 检查 hook 脚本是否包含 MacOSNotifier
grep -c "MacOSNotifier" ~/.claude-dingtalk/hooks/session_start.py

# 如果输出 0，说明脚本未更新
# 需要重新安装 hooks
```

---

### 问题 3: 请勿打扰模式

**症状**：
- 有声音但没弹窗
- 或完全没反应

**检查**：
```bash
# 查看控制中心（右上角）
# 或者：系统设置 > 通知
# 确保"请勿打扰"未开启
```

---

### 问题 4: 通知样式为"临时"

**症状**：
- 通知一闪而过（1-2秒就消失）
- 来不及看内容

**解决**：
```
系统设置 > 通知 > Python (或 Terminal)

横幅样式: 
  ❌ 临时（太快了）
  ✅ 持续（推荐，显示时间更长）
```

---

### 问题 2: 通知有声音但没有弹窗

**症状**：
- 能听到提示音
- 但看不到通知气泡

**可能原因**：
1. "请勿打扰"模式已开启
2. 横幅样式设置为"临时"（显示时间太短）
3. 通知被系统自动隐藏

**解决步骤**：

#### 步骤 1: 检查请勿打扰模式

```bash
# 查看请勿打扰状态
defaults -currentHost read com.apple.notificationcenterui doNotDisturb

# 如果显示 1，表示请勿打扰已开启
# 在控制中心或系统设置中关闭
```

#### 步骤 2: 调整横幅样式

```
系统设置 > 通知 > Python (或 Terminal)

横幅样式: 
  ❌ 临时（1-2秒就消失，太快了）
  ✅ 持续（推荐，显示时间更长）
```

#### 步骤 3: 检查通知历史

即使通知气泡消失了，也会在通知中心保存：

```
# 打开通知中心
# 方法 1: 点击右上角通知图标
# 方法 2: 触摸板三指向上滑动（如果使用触控板）
# 方法 3: 查看是否有未读通知
```

---

### 问题 3: 只有部分事件有通知

**症状**：
- 会话启动有通知
- 任务完成没有通知
- 或者相反

**可能原因**：
1. 某些事件未启用
2. Hook 脚本未更新

**解决步骤**：

#### 步骤 1: 检查事件启用状态

```bash
# 查看配置
cat ~/.claude-dingtalk/config.yaml | grep -A 15 "events:"
```

**检查关键事件**：
```yaml
events:
  session_start:
    enabled: true   # 会话启动
  stop:
    enabled: true   # 任务完成
  pre_tool_use:
    enabled: true   # 敏感操作
```

**如果某个事件是 `enabled: false`**：
```bash
# 重新配置
cdn setup
# 选择要启用的事件
```

#### 步骤 2: 检查 Hook 脚本版本

```bash
# 查看 hook 脚本最后修改时间
ls -lh ~/.claude-dingtalk/hooks/session_start.py
ls -lh ~/.claude-dingtalk/hooks/stop.py

# 检查脚本中是否包含 MacOSNotifier
grep -c "MacOSNotifier" ~/.claude-dingtalk/hooks/session_start.py

# 如果输出 0，说明脚本未更新，需要重新安装
cdn hooks install
```

---

### 问题 4: macOS 通知失败但钉钉正常

**症状**：
- 钉钉群正常收到消息
- macOS 没有通知
- 没有错误提示

**这是正常的！** 

**说明**：
- macOS 通知和钉钉通知是**两个独立的渠道**
- macOS 通知失败不会影响钉钉通知
- 两个渠道互不干扰

**可能原因**：
1. terminal-notifier 未安装
2. 系统资源不足
3. Hook 脚本异常退出

**验证方法**：
```bash
# 手动测试 macOS 通知
python3 -c "
import sys
sys.path.insert(0, 'src')
from claude_dingtalk_notifier.macos_notifier import MacOSNotifier

notifier = MacOSNotifier(enabled=True, sound=False)
result = notifier.send('手动测试', '测试通知')
print(f'发送结果: {result}')
"

# 如果返回 False，检查 terminal-notifier 是否已安装
which terminal-notifier

# 如果返回 True 但没看到通知，检查系统设置
```

---

### 问题 5: 通知弹出但内容不完整

**症状**：
- 通知弹出了
- 但是项目名显示为 "Unknown"
- 或者缺少触发原因

**可能原因**：
1. Hook 脚本版本太旧
2. 使用了旧版本的代码

**解决步骤**：

#### 步骤 1: 检查版本

```bash
# 查看当前版本
python3 -c "
import sys
sys.path.insert(0, 'src')
from claude_dingtalk_notifier import __version__
print(__version__)
"

# 期望输出: 0.3.1 或更高
```

**如果版本低于 0.3.1**：
```bash
# 拉取最新代码
git pull

# 重新安装
./install.sh
source ~/.zshrc

# 重新安装 hooks
cdn hooks install
```

#### 步骤 2: 验证通知格式

```bash
# 查看已安装的 hook 脚本
grep -A 3 "macos_notifier.send" ~/.claude-dingtalk/hooks/session_start.py

# 期望输出类似：
# macos_notifier.send(
#     title=f"{project_name} - 会话已启动",
#     message="Claude Code 新会话已启动"
# )
```

---

## 🔧 高级诊断

### 诊断 1: 查看 Hook 执行日志

```bash
# 手动运行 hook 脚本，查看错误
echo '{"cwd":"~/test"}' | python3 ~/.claude-dingtalk/hooks/session_start.py

# 检查是否有错误输出
# 如果有 ImportError，说明 Python 路径配置有问题
```

### 诊断 2: 测试 terminal-notifier

```bash
# 直接测试 terminal-notifier
terminal-notifier -title "测试标题" -message "测试消息" -sound default

# 如果这条命令不工作，检查是否已安装
which terminal-notifier

# 如果未安装，执行安装
brew install terminal-notifier

# 安装后重新测试
```

### 诊断 3: 重启通知服务

```bash
# 重载通知中心（macOS 10.15+）
killall NotificationCenter
# macOS 会自动重启通知中心
```

---

## 📊 完整排查流程图

```
macOS 通知没有弹出
         ↓
   [配置是否启用?]
         ↓
   NO → 运行 cdn setup，启用 macOS 通知
         ↓
   YES → [Hooks 是否重新安装?]
         ↓
   NO → 运行 cdn hooks install
         ↓
   YES → [事件是否启用?]
         ↓
   NO → 运行 cdn setup，启用对应事件
         ↓
   YES → [系统通知权限?]
         ↓
   NO → 系统设置 > 通知 > Python
         ↓
   YES → [请勿打扰模式?]
         ↓
   YES → 关闭请勿打扰
         ↓
   NO → [terminal-notifier 是否安装?]
         ↓
   NO → 运行 brew install terminal-notifier
         ↓
   YES → [手动测试是否成功?]
         ↓
   NO → 重载通知中心
         ↓
   YES → ✅ 问题解决
```

---

## 🆘 仍然无法解决？

### 收集诊断信息

如果以上方法都无法解决问题，请收集以下信息：

```bash
# 1. 版本信息
python3 -c "import sys; sys.path.insert(0, 'src'); from claude_dingtalk_notifier import __version__; print(__version__)"

# 2. 配置信息
cat ~/.claude-dingtalk/config.yaml

# 3. Hook 状态
cdn hooks status

# 4. 手动测试
echo '{"cwd":"~/test"}' | python3 ~/.claude-dingtalk/hooks/session_start.py 2>&1

# 5. 系统通知测试
terminal-notifier -title "测试" -message "测试消息"
```

### 常见错误信息及含义

| 错误信息 | 含义 | 解决方法 |
|---------|------|---------|
| `Warning: Could not import claude_dingtalk_notifier` | Python 路径配置错误 | 重新运行 `./install.sh` |
| `NameError: name 'MacOSNotifier' is not defined` | Hook 脚本未更新 | 运行 `cdn hooks install` |
| `Warning: terminal-notifier not found` | 未安装 terminal-notifier | 运行 `brew install terminal-notifier` |
| 没有错误但也没通知 | 权限或配置问题 | 检查系统设置中的通知权限 |

---

## ✅ 验证修复成功的标志

修复成功后，你应该看到：

1. **配置正确**：
   ```bash
   $ cat ~/.claude-dingtalk/config.yaml | grep -A 2 macos
   macos:
     enabled: true
     sound: true
   ```

2. **手动测试成功**：
   ```bash
   $ python3 test_macos_v0.3.1.py
   # 右上角应该弹出 3 条通知
   ```

3. **实际使用正常**：
   - 启动 Claude Code 会话 → 弹出 "项目名 - 会话已启动"
   - 完成任务 → 弹出 "项目名 - 任务完成"
   - 执行敏感操作 → 弹出 "项目名 - 敏感操作"

---

## 📚 相关文档

- **[MACOS_NOTIFICATION_v0.3.0.md](MACOS_NOTIFICATION_v0.3.0.md)** - macOS 通知功能说明
- **[README.md](README.md)** - 项目主文档
- **[INSTALL.md](INSTALL.md)** - 安装指南

---

**最后更新**: 2026-04-04
**版本**: v0.3.1
