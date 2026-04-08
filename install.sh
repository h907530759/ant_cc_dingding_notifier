#!/bin/bash
#
# Claude Code 钉钉通知工具 - 智能安装脚本
# 适用于团队部署，自动适配不同的 Mac 环境
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 打印函数
print_banner() {
    echo -e "${CYAN}"
    cat << "BANNER"
╔═══════════════════════════════════════════════════════╗
║     Claude Code 钉钉通知工具 - 智能安装脚本          ║
║     Team Deployment Installer                         ║
╚═══════════════════════════════════════════════════════╝
BANNER
    echo -e "${NC}"
}

print_system_info() {
    echo ""
    echo -e "${BLUE}📱 本工具将为以下系统安装钉钉通知能力:${NC}"
    echo ""
    echo -e "  ${GREEN}1. 开源 Claude Code${NC}"
    echo -e "     配置文件: ${CYAN}~/.claude/settings.json${NC}"
    echo ""
    echo -e "  ${GREEN}2. 内部 antcc 系统${NC}"
    echo -e "     配置文件: ${CYAN}~/.codefuse/engine/cc/settings.json${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  注意:${NC} 两个系统的 hooks 将共享使用同一个 hook 脚本"
    echo ""
    echo -e "${BLUE}ℹ️ 如需修改配置，可在安装后运行:${NC}"
    echo -e "   ${CYAN}cdn setup${NC} - 重新配置钉钉机器人"
    echo -e "   ${CYAN}cdn hooks status${NC} - 查看 hooks 状态"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# 检测项目路径
detect_project_path() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # 检查是否在项目根目录
    if [ -f "$SCRIPT_DIR/pyproject.toml" ] && [ -d "$SCRIPT_DIR/src" ]; then
        echo "$SCRIPT_DIR"
    else
        # 不在根目录，返回上级
        echo "$(dirname "$SCRIPT_DIR")"
    fi
}

# 检测 Python 环境
detect_python() {
    print_info "检测 Python 环境..."

    PYTHON_CMD=""

    # 优先级: Homebrew > pyenv > asdf > 系统 Python
    if command -v brew &> /dev/null; then
        HOMEBREW_PYTHON=$(brew --prefix python3 2>/dev/null)/bin/python3
        if [ -f "$HOMEBREW_PYTHON" ]; then
            PYTHON_CMD="$HOMEBREW_PYTHON"
            print_success "找到 Homebrew Python"
        fi
    fi

    if [ -z "$PYTHON_CMD" ] && command -v pyenv &> /dev/null; then
        PYENV_PYTHON=$(pyenv which python3 2>/dev/null)
        if [ -n "$PYENV_PYTHON" ]; then
            PYTHON_CMD="$PYENV_PYTHON"
            print_success "找到 pyenv Python"
        fi
    fi

    if [ -z "$PYTHON_CMD" ] && command -v asdf &> /dev/null; then
        ASDF_PYTHON=$(asdf which python3 2>/dev/null)
        if [ -n "$ASDF_PYTHON" ]; then
            PYTHON_CMD="$ASDF_PYTHON"
            print_success "找到 asdf Python"
        fi
    fi

    # 最后使用系统 Python
    if [ -z "$PYTHON_CMD" ]; then
        PYTHON_CMD="python3"
        print_warning "使用系统 Python (功能可能受限)"
    fi

    # 验证 Python 版本
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_success "Python 版本: $PYTHON_VERSION"
}

# 检查依赖
check_dependencies() {
    print_info "检查依赖..."
    
    DEPS_OK=true
    for dep in requests pyyaml click rich; do
        if ! $PYTHON_CMD -c "import $dep" 2>/dev/null; then
            print_warning "缺少依赖: $dep"
            DEPS_OK=false
        fi
    done
    
    if [ "$DEPS_OK" = false ]; then
        print_info "安装依赖..."
        $PYTHON_CMD -m pip install --user requests pyyaml click rich || {
            print_error "依赖安装失败，请手动安装:"
            echo "  $PYTHON_CMD -m pip install --user requests pyyaml click rich"
            exit 1
        }
        print_success "依赖安装完成"
    else
        print_success "所有依赖已安装"
    fi
}

# 创建 wrapper 脚本
create_wrapper() {
    local project_path="$1"
    local bin_dir="$2"

    print_info "创建 CLI wrapper 脚本..."

    mkdir -p "$bin_dir"

    # 创建 cdn wrapper
    cat > "$bin_dir/cdn" << WRAPPER
#!/bin/bash
# Claude DingTalk Notifier CLI
# 项目路径: $project_path

PROJECT_ROOT="$project_path"
export PYTHONPATH="\${PROJECT_ROOT}/src:\${PYTHONPATH}"
exec python3 -m claude_dingtalk_notifier.cli "\$@"
WRAPPER

    chmod +x "$bin_dir/cdn"
    print_success "创建: $bin_dir/cdn"
    
    # 创建长命令名
    cat > "$bin_dir/claude-dingtalk" << WRAPPER
#!/bin/bash
exec "$bin_dir/cdn" "\$@"
WRAPPER
    chmod +x "$bin_dir/claude-dingtalk"
    print_success "创建: $bin_dir/claude-dingtalk"
}

# 配置 PATH
configure_path() {
    local bin_dir="$1"
    
    print_info "配置 PATH..."
    
    # 检测 shell
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bash_profile"
    else
        SHELL_RC=""
    fi
    
    if [ -n "$SHELL_RC" ]; then
        # 检查是否已配置
        if ! grep -q "$bin_dir" "$SHELL_RC" 2>/dev/null; then
            echo "" >> "$SHELL_RC"
            echo "# Claude DingTalk Notifier" >> "$SHELL_RC"
            echo "export PATH=\"$bin_dir:\$PATH\"" >> "$SHELL_RC"
            print_success "已添加到 $SHELL_RC"
            echo ""
            print_info "请运行: source $SHELL_RC"
        else
            print_success "PATH 已配置"
        fi
    else
        print_warning "无法检测 shell，请手动添加:"
        echo "  export PATH=\"$bin_dir:\$PATH\""
    fi
}

# 主安装流程
main() {
    print_banner

    print_system_info
    
    PROJECT_PATH=$(detect_project_path)
    print_info "项目路径: $PROJECT_PATH"
    
    detect_python
    check_dependencies
    
    # 确定 bin 目录
    if [ -d "$HOME/.local/bin" ]; then
        BIN_DIR="$HOME/.local/bin"
    else
        BIN_DIR="$HOME/bin"
        mkdir -p "$BIN_DIR" 2>/dev/null || BIN_DIR="$HOME/Library/Python/3.9/bin"
    fi
    
    print_info "Bin 目录: $BIN_DIR"
    
    create_wrapper "$PROJECT_PATH" "$BIN_DIR"
    configure_path "$BIN_DIR"
    
    # 完成
    echo ""
    print_success "安装完成！"
    echo ""
    print_info "下一步:"
    echo "  1. source ~/.zshrc  (或 source ~/.bash_profile)"
    echo "  2. cdn setup"
    echo "  3. cdn hooks install"
    echo ""
}

main "$@"
