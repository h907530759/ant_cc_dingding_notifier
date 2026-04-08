#!/bin/bash
#
# Claude Code 钉钉通知工具 - 完全卸载脚本
# 安全地卸载所有组件
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
║     Claude Code 钉钉通知工具 - 卸载脚本              ║
║     Uninstall Script                                  ║
╚═══════════════════════════════════════════════════════╝
BANNER
    echo -e "${NC}"
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

# 确认操作
confirm_uninstall() {
    echo ""
    print_warning "此操作将："
    echo "  1. 卸载所有 Claude Code hooks"
    echo "  2. 删除配置文件和脚本"
    echo "  3. 清理 PATH 和环境变量配置"
    echo "  4. 保留项目文件（需手动删除）"
    echo ""
    read -p "确认卸载？[y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "已取消卸载"
        exit 0
    fi
}

# 卸载 hooks
uninstall_hooks() {
    print_info "卸载 Claude Code hooks..."
    
    # 检查 cdn 命令是否存在
    if command -v cdn &> /dev/null; then
        cdn hooks uninstall --all 2>/dev/null || true
        print_success "Hooks 已卸载"
    else
        # 使用 PYTHONPATH
        export PYTHONPATH="$(pwd)/src:$PYTHONPATH"
        python3 -m claude_dingtalk_notifier.cli hooks uninstall --all 2>/dev/null || true
        print_success "Hooks 已卸载（手动方式）"
    fi
}

# 删除配置文件
remove_config_files() {
    print_info "删除配置文件..."
    
    CONFIG_DIR="$HOME/.claude-dingtalk"
    
    if [ -d "$CONFIG_DIR" ]; then
        # 备份配置
        BACKUP_DIR="$HOME/.claude-dingtalk.backup.$(date +%Y%m%d_%H%M%S)"
        cp -r "$CONFIG_DIR" "$BACKUP_DIR" 2>/dev/null || true
        
        # 删除配置
        rm -rf "$CONFIG_DIR"
        print_success "配置文件已删除 (备份: $BACKUP_DIR)"
    else
        print_info "配置目录不存在"
    fi
}

# 删除 wrapper 脚本
remove_wrapper_scripts() {
    print_info "删除 CLI wrapper 脚本..."
    
    REMOVED_COUNT=0
    
    # 可能的位置
    BIN_DIRS=(
        "$HOME/.local/bin"
        "$HOME/bin"
        "$HOME/Library/Python/3.9/bin"
    )
    
    for bin_dir in "${BIN_DIRS[@]}"; do
        if [ -f "$bin_dir/cdn" ]; then
            rm -f "$bin_dir/cdn"
            print_success "已删除: $bin_dir/cdn"
            REMOVED_COUNT=$((REMOVED_COUNT + 1))
        fi
        
        if [ -f "$bin_dir/claude-dingtalk" ]; then
            rm -f "$bin_dir/claude-dingtalk"
            print_success "已删除: $bin_dir/claude-dingtalk"
            REMOVED_COUNT=$((REMOVED_COUNT + 1))
        fi
    done
    
    if [ $REMOVED_COUNT -eq 0 ]; then
        print_info "未找到 wrapper 脚本"
    fi
}

# 清理 PATH 配置
clean_path_config() {
    print_info "清理 PATH 配置..."
    
    CLEANED_COUNT=0
    
    # 清理 .zshrc
    if [ -f "$HOME/.zshrc" ]; then
        if grep -q "Claude DingTalk Notifier" "$HOME/.zshrc" 2>/dev/null; then
            # 创建临时文件
            tmp_file=$(mktemp)
            grep -v "Claude DingTalk Notifier" "$HOME/.zshrc" > "$tmp_file"
            grep -v "\.local/bin" "$tmp_file" > "$tmp_file.2" || true
            mv "$tmp_file.2" "$HOME/.zshrc"
            rm -f "$tmp_file"
            print_success "已清理 ~/.zshrc"
            CLEANED_COUNT=$((CLEANED_COUNT + 1))
        fi
    fi
    
    # 清理 .bash_profile
    if [ -f "$HOME/.bash_profile" ]; then
        if grep -q "Claude DingTalk Notifier" "$HOME/.bash_profile" 2>/dev/null; then
            tmp_file=$(mktemp)
            grep -v "Claude DingTalk Notifier" "$HOME/.bash_profile" > "$tmp_file"
            grep -v "\.local/bin" "$tmp_file" > "$tmp_file.2" || true
            mv "$tmp_file.2" "$HOME/.bash_profile"
            rm -f "$tmp_file"
            print_success "已清理 ~/.bash_profile"
            CLEANED_COUNT=$((CLEANED_COUNT + 1))
        fi
    fi
    
    if [ $CLEANED_COUNT -eq 0 ]; then
        print_info "未找到 PATH 配置"
    fi
}

# 清理环境变量
clean_env_vars() {
    print_info "清理环境变量配置..."
    
    CLEANED_COUNT=0
    
    # 清理 .zshrc
    if [ -f "$HOME/.zshrc" ]; then
        if grep -q "CLAUDE_MACHINE_NAME" "$HOME/.zshrc" 2>/dev/null; then
            tmp_file=$(mktemp)
            grep -v "CLAUDE_MACHINE_NAME" "$HOME/.zshrc" > "$tmp_file"
            grep -v "CLAUDE_CONFIG_DIR" "$tmp_file" > "$tmp_file.2" || true
            grep -v "DINGTALK_" "$tmp_file.2" > "$tmp_file.3" || true
            mv "$tmp_file.3" "$HOME/.zshrc"
            rm -f "$tmp_file" "$tmp_file.2"
            print_success "已清理 ~/.zshrc 中的环境变量"
            CLEANED_COUNT=$((CLEANED_COUNT + 1))
        fi
    fi
    
    # 清理 .bash_profile
    if [ -f "$HOME/.bash_profile" ]; then
        if grep -q "CLAUDE_MACHINE_NAME" "$HOME/.bash_profile" 2>/dev/null; then
            tmp_file=$(mktemp)
            grep -v "CLAUDE_MACHINE_NAME" "$HOME/.bash_profile" > "$tmp_file"
            grep -v "CLAUDE_CONFIG_DIR" "$tmp_file" > "$tmp_file.2" || true
            grep -v "DINGTALK_" "$tmp_file.2" > "$tmp_file.3" || true
            mv "$tmp_file.3" "$HOME/.bash_profile"
            rm -f "$tmp_file" "$tmp_file.2"
            print_success "已清理 ~/.bash_profile 中的环境变量"
            CLEANED_COUNT=$((CLEANED_COUNT + 1))
        fi
    fi
    
    # 清理 .zshenv
    if [ -f "$HOME/.zshenv" ]; then
        if grep -q "CLAUDE_" "$HOME/.zshenv" 2>/dev/null || grep -q "DINGTALK_" "$HOME/.zshenv" 2>/dev/null; then
            tmp_file=$(mktemp)
            grep -v "CLAUDE_" "$HOME/.zshenv" > "$tmp_file"
            grep -v "DINGTALK_" "$tmp_file" > "$tmp_file.2" || true
            mv "$tmp_file.2" "$HOME/.zshenv"
            rm -f "$tmp_file"
            print_success "已清理 ~/.zshenv"
            CLEANED_COUNT=$((CLEANED_COUNT + 1))
        fi
    fi
    
    if [ $CLEANED_COUNT -eq 0 ]; then
        print_info "未找到环境变量配置"
    fi
}

# 显示卸载总结
show_summary() {
    echo ""
    print_banner
    print_success "卸载完成！"
    echo ""
    print_info "已清理："
    echo "  ✓ Claude Code hooks"
    echo "  ✓ 配置文件 (~/.claude-dingtalk/)"
    echo "  ✓ CLI wrapper 脚本 (cdn, claude-dingtalk)"
    echo "  ✓ PATH 配置"
    echo "  ✓ 环境变量配置"
    echo ""
    print_warning "需要手动操作："
    echo "  1. 重新加载 shell 配置:"
    echo "     source ~/.zshrc  # 或 source ~/.bash_profile"
    echo ""
    echo "  2. 删除项目目录（如果不再需要）:"
    echo "     rm -rf $(pwd)"
    echo ""
    print_info "备份文件位置:"
    echo "  - 配置备份: ~/.claude-dingtalk.backup.*"
    echo "  - settings.json.backup: (在各自的配置目录中)"
    echo ""
}

# 主卸载流程
main() {
    print_banner
    
    # 确认
    confirm_uninstall
    
    # 执行卸载
    uninstall_hooks
    remove_config_files
    remove_wrapper_scripts
    clean_path_config
    clean_env_vars
    
    # 显示总结
    show_summary
}

# 运行主程序
main "$@"
