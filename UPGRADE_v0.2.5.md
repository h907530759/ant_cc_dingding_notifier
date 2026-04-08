# 🚀 快速升级指南 - v0.2.5

## ⚠️ 重要：修复了 "Unknown" 显示问题

如果你看到通知显示"结束原因: Unknown"，请立即升级！

---

## 📋 升级步骤（2分钟）

```bash
# 1. 进入项目目录
cd claude_notifyer

# 2. 拉取最新代码
git pull

# 3. 重新安装
./install.sh

# 4. 重新加载 shell 配置
source ~/.zshrc
# 或者
source ~/.bash_profile

# 5. 【必须】重新安装 hooks
cdn hooks install

# 6. 验证版本
cdn --version
# 应该显示: v0.2.5
```

---

## ✅ 升级后效果

### stop Hook 通知

**升级前 (v0.2.4)**:
```
✅ 工作已结束
📂 项目: claude_notifyer
📝 结束原因: Unknown  ← Bug
⏰ 时间: 2026-04-04 23:15:03
```

**升级后 (v0.2.5)**:
```
✅ 工作已结束

### ✅ 工作已结束
📂 项目: claude_notifyer
⏰ 时间: 2026-04-04 23:30:00
💡 工作已全部完成，可以查看结果了
```

✅ **不再显示 "Unknown"**

---

## 🔧 修复的问题

| Hook | 问题 | 修复 |
|------|------|------|
| **stop** | 显示"结束原因: Unknown" | 移除 reason 字段 |
| **config_change** | 可能显示"变更类型: Unknown" | 默认为"修改" |
| **subagent_start** | 可能显示"任务: Unknown" | 默认为"{代理名称}任务" |
| **subagent_stop** | 可能显示"任务/结果: Unknown" | 默认为"{代理名称}任务"和"已完成" |

---

## 💡 为什么会显示 "Unknown"？

v0.2.4 尝试从 hook 数据中读取某些字段，但 Claude Code 实际并不提供这些字段：
- **Stop hook** 不提供 `reason` 字段
- 其他 hook 的某些字段也可能不存在

v0.2.5 修复了这个问题，为可能缺失的字段提供合理的默认值。

---

## 📞 如果还有问题

```bash
# 查看 hooks 状态
cdn hooks status

# 重新安装 hooks
cdn hooks install

# 测试连接
cdn test
```

---

**版本**: v0.2.5
**更新日期**: 2026-04-04
**状态**: ✅ 生产就绪
