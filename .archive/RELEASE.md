# PyPI 发布指南

本文档介绍如何将 `claude-dingtalk-notifier` 发布到 PyPI。

## 📋 发布前准备

### 1. PyPI 账号注册
- 访问 https://pypi.org/account/register/
- 创建账号并验证邮箱
- **启用两步认证（2FA）**（发布必需）

### 2. 创建 API Token
1. 访问 https://pypi.org/manage/account/token/
2. 创建新的 API Token
3. Scope 选择 "Entire account"
4. **保存 Token**（只显示一次）

### 3. 配置认证
```bash
# 方式一：使用 API Token（推荐）
# 创建 ~/.pypirc
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <your-api-token>

[testpypi]
username = __token__
password = <your-test-pypi-api-token>
EOF

# 方式二：使用 keyring（更安全）
pip install keyring
keyring set https://upload.pypi.org/legacy/ __token__
# 粘贴你的 API Token
```

## 🚀 发布流程

### 步骤 1: 检查项目
```bash
./check_release.sh
```

这会检查：
- 版本号一致性
- 必要文件存在
- 构建工具安装
- Python 语法

### 步骤 2: 更新版本号

如果需要发布新版本：
1. 更新 `pyproject.toml` 中的 `version`
2. 更新 `setup.cfg` 中的 `version`
3. 更新 `src/claude_dingtalk_notifier/__init__.py` 中的 `__version__`
4. 更新 `CHANGELOG.md`

### 步骤 3: 构建包
```bash
./build.sh
```

这会创建：
- `dist/claude_dingtalk_notifier-X.Y.Z-py3-none-any.whl`
- `dist/claude-dingtalk-notifier-X.Y.Z.tar.gz`

### 步骤 4: 测试发布（强烈推荐）
```bash
# 发布到 TestPyPI
./publish.sh --test

# 等待几分钟后测试安装
pip install --index-url https://test.pypi.org/simple/ claude-dingtalk-notifier

# 测试运行
claude-dingtalk --help
```

### 步骤 5: 正式发布
```bash
./publish.sh
```

### 步骤 6: 验证
```bash
# 安装测试
pip install claude-dingtalk-notifier

# 运行测试
claude-dingtalk --help
claude-dingtalk status

# 查看 PyPI 页面
open https://pypi.org/project/claude-dingtalk-notifier/
```

## 🔄 发布新版本

```bash
# 1. 更新版本号
vim pyproject.toml setup.cfg src/claude_dingtalk_notifier/__init__.py

# 2. 更新 CHANGELOG.md
vim CHANGELOG.md

# 3. 提交到 Git
git add .
git commit -m "Bump version to X.Y.Z"
git tag vX.Y.Z
git push origin main --tags

# 4. 构建和发布
./build.sh
./publish.sh
```

## 🐛 回滚/撤销

如果发现问题需要撤销：

```bash
# 删除 PyPI 上的版本（只能删除，不能重新上传相同版本）
# 访问: https://pypi.org/manage/project/claude-dingtalk-notifier/releases/

# 或使用 twine
twine delete claude-dingtalk-notifier X.Y.Z -c pypi
```

注意：
- PyPI 不允许覆盖已发布的版本
- 如果发现问题，必须发布新版本（如 0.2.2 → 0.2.3）

## 📊 发布后

1. **更新文档**
   - 在 README.md 添加 PyPI 徽章
   - 更新安装说明

2. **创建 GitHub Release**
   ```bash
   gh release create vX.Y.Z --notes "Release X.Y.Z"
   ```

3. **推广**
   - 分享到社交媒体
   - 通知用户

## 🔧 常见问题

### Q: 提示 403 Forbidden
**A:** 检查 API Token 是否正确，或重新生成 Token

### Q: 提示版本已存在
**A:** 必须更新版本号，PyPI 不允许覆盖

### Q: 构建失败
**A:** 确保安装了最新工具：
```bash
pip install --upgrade build twine setuptools wheel
```

### Q: 如何使用 TestPyPI？
**A:** TestPyPI 是测试环境，需要单独注册：
- 注册: https://test.pypi.org/account/register/
- 创建 Token: https://test.pypi.org/manage/account/token/

## 📚 参考资源

- [PyPI 官方文档](https://packaging.python.org/tutorials/packaging-projects/)
- [TestPyPI](https://test.pypi.org/)
- [Twine 文档](https://twine.readthedocs.io/)
