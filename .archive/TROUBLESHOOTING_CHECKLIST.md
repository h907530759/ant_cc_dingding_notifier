# 🔍 测试者排查清单

如果钉钉通知正常但 macOS 桌面通知没有弹出，请按以下步骤排查：

---

## ✅ 第一步：快速测试（30秒）

运行以下命令测试系统通知权限：

```bash
osascript -e 'display notification "测试消息" with title "测试标题" sound name "default"'
```

**结果判断**：
- ✅ **右上角弹出通知** → 权限正常，跳到第三步
- ❌ **没有弹出** → 权限未开启，执行第二步

---

## 🔐 第二步：开启系统通知权限

### 方法 1：系统设置（推荐）

1. 打开 **系统设置**
2. 点击左侧 **通知**
3. 找到以下应用之一：
   - **Python**（如果有）
   - **Terminal**（如果使用 Terminal）
   - **iTerm2**（如果使用 iTerm）
4. 确保以下选项已勾选：
   ```
   ✅ 允许通知
   ✅ 横幅样式: 持续（不要选"临时"）
   ✅ 声音: 默认（可选）
   ```

### 方法 2：命令行打开

```bash
open "x-apple.systempreferences:com.apple.preference.notifications"
```

权限开启后，**重新运行第一步的测试命令验证**。

---

## 🔧 第三步：检查配置

### 1. 检查 macOS 通知是否启用

```bash
cat ~/.claude-dingtalk/config.yaml | grep -A 2 "macos:"
```

**期望输出**：
```yaml
macos:
  enabled: true
  sound: true
```

**如果不是 `enabled: true`**：
```bash
claude-dingtalk setup
# 当问到"是否启用 macOS 桌面通知？"时选择 y
```

### 2. 重新安装 Hooks（重要！）

```bash
claude-dingtalk hooks install
```

**原因**：配置修改后必须重新安装 hooks 才能生效。

---

## 🧪 第四步：手动测试通知

创建测试脚本并运行：

```bash
# 方法 1: 使用项目中的测试脚本
cd ~/ant_cc_dingding_notifier
python3 test_macos_notification.py

# 方法 2: 直接测试
python3 -c "
from claude_dingtalk_notifier.macos_notifier import MacOSNotifier
notifier = MacOSNotifier(enabled=True, sound=True)
notifier.send('手动测试', '如果看到这条通知，说明功能正常')
"
```

**应该看到**：右上角弹出测试通知

---

## 📋 第五步：检查 Hooks 版本

### 1. 检查脚本是否包含 MacOSNotifier

```bash
grep -c "MacOSNotifier" ~/.claude-dingtalk/hooks/session_start.py
```

**期望输出**：`2` 或更大的数字

**如果是 `0`**：说明 hooks 未更新，运行：
```bash
claude-dingtalk hooks install
```

### 2. 检查包路径

```bash
head -20 ~/.claude-dingtalk/hooks/session_start.py | grep "package_path"
```

**期望输出**：
```python
package_path = Path(r"/Users/suchen/workspace/claude_notifyer/src")
```

**如果路径不存在**：需要重新安装：
```bash
cd ~/ant_cc_dingding_notifier
./install.sh
claude-dingtalk hooks install
```

---

## 🎯 最常见问题和解决方案

### 问题 1：通知一闪而过

**原因**：横幅样式设置为"临时"

**解决**：
```
系统设置 > 通知 > Python（或 Terminal）
横幅样式: 持续  ← 选这个
```

### 问题 2：配置正确但还是没通知

**可能原因**：Hooks 未重新安装

**解决**：
```bash
# 任何配置修改后都必须运行
claude-dingtalk hooks install
```

### 问题 3：测试命令有通知，实际使用没有

**可能原因**：Claude Code 未重启

**解决**：
1. 完全关闭 Claude Code
2. 重新打开
3. 开始新会话

---

## 📊 向开发者反馈信息

如果以上步骤都无法解决，请提供以下信息：

### 1. 系统信息

```bash
# macOS 版本
sw_vers

# Python 版本
python3 --version
```

### 2. 配置信息

```bash
# 查看配置（隐藏敏感信息）
cat ~/.claude-dingtalk/config.yaml
```

### 3. Hook 状态

```bash
# Hooks 安装状态
claude-dingtalk hooks status
```

### 4. 测试结果

```bash
# 手动测试输出
echo '{"cwd":"~/test"}' | python3 ~/.claude-dingtalk/hooks/session_start.py 2>&1
```

### 5. 系统通知测试结果

```bash
# 系统通知测试
osascript -e 'display notification "测试" with title "测试"' && echo "✅ 系统通知正常" || echo "❌ 系统通知失败"
```

---

## ✅ 成功标志

修复成功后，你应该看到：

1. ✅ 系统通知测试命令能弹出通知
2. ✅ 手动测试脚本能弹出通知
3. ✅ Claude Code 会话启动时弹出 "项目名 - 会话已启动"
4. ✅ Claude Code 任务完成时弹出 "项目名 - 任务完成"

---

## 🆘 需要帮助？

如果完成以上所有步骤后仍有问题：

1. 截图系统设置中的通知权限配置
2. 复制上述"向开发者反馈信息"的输出
3. 反馈给项目维护者

---

**最后更新**: 2026-04-08
