# 升级指南

## 如何升级到最新版本

### 方式一：从 GitHub 拉取最新代码

```bash
cd ~/ant_cc_dingding_notifier
git pull origin main

# 重新安装
./install.sh

# 重新安装 Hooks
claude-dingtalk hooks install
```

### 升级后检查

```bash
# 检查版本
claude-dingtalk --version

# 检查状态
claude-dingtalk status

# 测试通知
claude-dingtalk test
```

### 版本兼容性

| 你的版本 | 目标版本 | 需要操作 |
|---------|---------|---------|
| v0.1.x | v0.2.x | 升级后重新安装 Hooks |
| v0.2.x | v0.3.x | 升级后重新配置 |

### 升级前建议

1. **备份配置**
   ```bash
   cp ~/.claude-dingtalk/config.yaml ~/.claude-dingtalk/config.yaml.backup
   ```

2. **记录当前 Hooks**
   ```bash
   claude-dingtalk hooks status > hooks-backup.txt
   ```

3. **查看更新日志**
   - 查看 [CHANGELOG.md](CHANGELOG.md)
   - 查看 GitHub Releases

### 常见问题

**Q: 升级后通知不工作？**

A: 重新安装 Hooks：
```bash
claude-dingtalk hooks uninstall
claude-dingtalk hooks install
```

**Q: 配置文件会丢失吗？**

A: 不会，配置文件在 `~/.claude-dingtalk/config.yaml`，升级不会删除

**Q: 如何回滚到旧版本？**

A:
```bash
cd ~/ant_cc_dingding_notifier
git checkout v0.2.1
./install.sh
claude-dingtalk hooks install
```
