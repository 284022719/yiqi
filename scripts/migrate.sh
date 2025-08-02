#!/bin/bash

# 易骑公会官方网站 - 数据迁移脚本
# 用于将现有数据迁移到新的数据库结构

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装"
        exit 1
    fi
    
    if ! command -v sqlite3 &> /dev/null; then
        log_warning "SQLite3 未安装，某些功能可能不可用"
    fi
    
    log_success "依赖检查完成"
}

# 备份现有数据
backup_data() {
    log_info "备份现有数据..."
    
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # 备份数据库
    if [ -f "data/guild_members.db" ]; then
        cp "data/guild_members.db" "$BACKUP_DIR/"
        log_success "数据库已备份到 $BACKUP_DIR/guild_members.db"
    fi
    
    # 备份JSON文件
    if [ -d "data" ]; then
        cp -r data/*.json "$BACKUP_DIR/" 2>/dev/null || true
        log_success "JSON文件已备份到 $BACKUP_DIR/"
    fi
    
    # 备份缓存
    if [ -d "cache" ]; then
        cp -r cache "$BACKUP_DIR/" 2>/dev/null || true
        log_success "缓存文件已备份到 $BACKUP_DIR/"
    fi
    
    log_success "数据备份完成"
}

# 创建新的目录结构
create_directories() {
    log_info "创建新的目录结构..."
    
    mkdir -p frontend/src/{components,pages,hooks,services,utils,styles,assets,types}
    mkdir -p frontend/public
    mkdir -p backend/src/{api/{routes,middleware,controllers},services/{crawler,database,statistics},models,utils,config,tests}
    mkdir -p shared/{types,constants,utils}
    mkdir -p data/{database,cache,logs,exports}
    mkdir -p docs/{api,deployment,development}
    mkdir -p scripts
    mkdir -p infrastructure/{docker,nginx,terraform}
    
    log_success "目录结构创建完成"
}

# 迁移前端文件
migrate_frontend() {
    log_info "迁移前端文件..."
    
    # 迁移HTML文件
    if [ -f "index.html" ]; then
        cp index.html frontend/public/
        log_success "index.html 已迁移"
    fi
    
    if [ -f "guild_members.html" ]; then
        cp guild_members.html frontend/public/
        log_success "guild_members.html 已迁移"
    fi
    
    if [ -f "H6.html" ]; then
        cp H6.html frontend/public/
        log_success "H6.html 已迁移"
    fi
    
    if [ -f "H7.html" ]; then
        cp H7.html frontend/public/
        log_success "H7.html 已迁移"
    fi
    
    if [ -f "gallery.html" ]; then
        cp gallery.html frontend/public/
        log_success "gallery.html 已迁移"
    fi
    
    if [ -f "wcl.html" ]; then
        cp wcl.html frontend/public/
        log_success "wcl.html 已迁移"
    fi
    
    # 迁移CSS文件
    if [ -d "css" ]; then
        cp -r css/* frontend/src/styles/
        log_success "CSS文件已迁移"
    fi
    
    # 迁移JavaScript文件
    if [ -d "js" ]; then
        cp -r js/* frontend/src/
        log_success "JavaScript文件已迁移"
    fi
    
    # 迁移图片资源
    if [ -d "img" ]; then
        cp -r img frontend/public/assets/
        log_success "图片资源已迁移"
    fi
    
    log_success "前端文件迁移完成"
}

# 迁移后端文件
migrate_backend() {
    log_info "迁移后端文件..."
    
    # 迁移Python文件
    if [ -d "src" ]; then
        cp -r src/* backend/src/
        log_success "Python源码已迁移"
    fi
    
    # 迁移主程序文件
    for file in *.py; do
        if [ -f "$file" ] && [ "$file" != "migrate.py" ]; then
            cp "$file" backend/
            log_success "$file 已迁移"
        fi
    done
    
    # 迁移配置文件
    if [ -f "requirements.txt" ]; then
        cp requirements.txt backend/
        log_success "requirements.txt 已迁移"
    fi
    
    log_success "后端文件迁移完成"
}

# 迁移数据文件
migrate_data() {
    log_info "迁移数据文件..."
    
    # 迁移数据库
    if [ -f "data/guild_members.db" ]; then
        cp data/guild_members.db data/database/
        log_success "数据库已迁移"
    fi
    
    # 迁移JSON文件
    if [ -d "data" ]; then
        find data -name "*.json" -exec cp {} data/exports/ \;
        log_success "JSON数据文件已迁移"
    fi
    
    # 迁移缓存
    if [ -d "cache" ]; then
        cp -r cache/* data/cache/
        log_success "缓存文件已迁移"
    fi
    
    # 迁移日志
    if [ -d "logs" ]; then
        cp -r logs/* data/logs/
        log_success "日志文件已迁移"
    fi
    
    log_success "数据文件迁移完成"
}

# 创建配置文件
create_config_files() {
    log_info "创建配置文件..."
    
    # 复制工作区package.json
    if [ -f "package-workspace.json" ]; then
        cp package-workspace.json package.json
        log_success "package.json 已创建"
    fi
    
    # 复制Docker配置
    if [ -f "docker-compose.yml" ]; then
        log_success "docker-compose.yml 已存在"
    fi
    
    # 复制环境变量示例
    if [ -f "env.example" ]; then
        cp env.example .env.example
        log_success ".env.example 已创建"
    fi
    
    log_success "配置文件创建完成"
}

# 验证迁移结果
verify_migration() {
    log_info "验证迁移结果..."
    
    # 检查目录结构
    if [ -d "frontend" ] && [ -d "backend" ] && [ -d "shared" ]; then
        log_success "目录结构验证通过"
    else
        log_error "目录结构验证失败"
        exit 1
    fi
    
    # 检查数据文件
    if [ -f "data/database/guild_members.db" ] || [ -d "data/exports" ]; then
        log_success "数据文件验证通过"
    else
        log_warning "数据文件可能未完全迁移"
    fi
    
    # 检查前端文件
    if [ -f "frontend/public/index.html" ] || [ -d "frontend/src/styles" ]; then
        log_success "前端文件验证通过"
    else
        log_warning "前端文件可能未完全迁移"
    fi
    
    # 检查后端文件
    if [ -d "backend/src" ] || [ -f "backend/requirements.txt" ]; then
        log_success "后端文件验证通过"
    else
        log_warning "后端文件可能未完全迁移"
    fi
    
    log_success "迁移验证完成"
}

# 清理旧文件
cleanup_old_files() {
    log_info "清理旧文件..."
    
    # 询问用户是否清理
    read -p "是否清理原始文件？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 备份原始文件到临时目录
        TEMP_DIR="temp_old_files_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$TEMP_DIR"
        
        # 移动原始文件
        mv *.html "$TEMP_DIR/" 2>/dev/null || true
        mv css "$TEMP_DIR/" 2>/dev/null || true
        mv js "$TEMP_DIR/" 2>/dev/null || true
        mv img "$TEMP_DIR/" 2>/dev/null || true
        mv src "$TEMP_DIR/" 2>/dev/null || true
        mv *.py "$TEMP_DIR/" 2>/dev/null || true
        mv requirements.txt "$TEMP_DIR/" 2>/dev/null || true
        
        log_success "原始文件已移动到 $TEMP_DIR/"
        log_info "如需恢复，请从 $TEMP_DIR/ 复制文件"
    else
        log_info "跳过清理步骤"
    fi
}

# 主函数
main() {
    log_info "开始易骑公会官方网站重构迁移..."
    log_info "时间: $(date)"
    
    # 检查是否在项目根目录
    if [ ! -f "README.md" ]; then
        log_error "请在项目根目录运行此脚本"
        exit 1
    fi
    
    # 执行迁移步骤
    check_dependencies
    backup_data
    create_directories
    migrate_frontend
    migrate_backend
    migrate_data
    create_config_files
    verify_migration
    cleanup_old_files
    
    log_success "迁移完成！"
    log_info "下一步："
    log_info "1. 复制 .env.example 为 .env 并配置环境变量"
    log_info "2. 运行 'npm install' 安装依赖"
    log_info "3. 运行 'npm run dev' 启动开发服务器"
    log_info "4. 查看 REFACTOR_PLAN.md 了解详细的重构计划"
}

# 运行主函数
main "$@" 