# 易骑公会官方网站 - 数据迁移脚本 (PowerShell版本)
# 用于将现有数据迁移到新的数据库结构

param(
    [switch]$SkipBackup,
    [switch]$SkipCleanup,
    [switch]$Force
)

# 颜色定义
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$White = "White"

# 日志函数
function Write-LogInfo {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Blue
}

function Write-LogSuccess {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Green
}

function Write-LogWarning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-LogError {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

# 检查依赖
function Test-Dependencies {
    Write-LogInfo "检查依赖..."
    
    # 检查Python
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-LogSuccess "Python已安装: $pythonVersion"
        } else {
            Write-LogError "Python未安装或不在PATH中"
            exit 1
        }
    } catch {
        Write-LogError "Python未安装"
        exit 1
    }
    
    # 检查Node.js
    try {
        $nodeVersion = node --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-LogSuccess "Node.js已安装: $nodeVersion"
        } else {
            Write-LogWarning "Node.js未安装，某些功能可能不可用"
        }
    } catch {
        Write-LogWarning "Node.js未安装，某些功能可能不可用"
    }
    
    Write-LogSuccess "依赖检查完成"
}

# 备份现有数据
function Backup-Data {
    if ($SkipBackup) {
        Write-LogInfo "跳过备份步骤"
        return
    }
    
    Write-LogInfo "备份现有数据..."
    
    $backupDir = "backups/$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    
    # 备份数据库
    if (Test-Path "data/guild_members.db") {
        Copy-Item "data/guild_members.db" "$backupDir/"
        Write-LogSuccess "数据库已备份到 $backupDir/guild_members.db"
    }
    
    # 备份JSON文件
    if (Test-Path "data") {
        Get-ChildItem "data" -Filter "*.json" | ForEach-Object {
            Copy-Item $_.FullName "$backupDir/"
        }
        Write-LogSuccess "JSON文件已备份到 $backupDir/"
    }
    
    # 备份缓存
    if (Test-Path "cache") {
        Copy-Item "cache" "$backupDir/" -Recurse -Force
        Write-LogSuccess "缓存文件已备份到 $backupDir/"
    }
    
    Write-LogSuccess "数据备份完成"
}

# 创建新的目录结构
function New-DirectoryStructure {
    Write-LogInfo "创建新的目录结构..."
    
    $directories = @(
        "frontend/src/components",
        "frontend/src/pages",
        "frontend/src/hooks",
        "frontend/src/services",
        "frontend/src/utils",
        "frontend/src/styles",
        "frontend/src/assets",
        "frontend/src/types",
        "frontend/public",
        "backend/src/api/routes",
        "backend/src/api/middleware",
        "backend/src/api/controllers",
        "backend/src/services/crawler",
        "backend/src/services/database",
        "backend/src/services/statistics",
        "backend/src/models",
        "backend/src/utils",
        "backend/src/config",
        "backend/src/tests",
        "shared/types",
        "shared/constants",
        "shared/utils",
        "data/database",
        "data/cache",
        "data/logs",
        "data/exports",
        "docs/api",
        "docs/deployment",
        "docs/development",
        "infrastructure/docker",
        "infrastructure/nginx",
        "infrastructure/terraform"
    )
    
    foreach ($dir in $directories) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    
    Write-LogSuccess "目录结构创建完成"
}

# 迁移前端文件
function Move-FrontendFiles {
    Write-LogInfo "迁移前端文件..."
    
    # 迁移HTML文件
    $htmlFiles = @("index.html", "guild_members.html", "H6.html", "H7.html", "gallery.html", "wcl.html")
    foreach ($file in $htmlFiles) {
        if (Test-Path $file) {
            Copy-Item $file "frontend/public/"
            Write-LogSuccess "$file 已迁移"
        }
    }
    
    # 迁移CSS文件
    if (Test-Path "css") {
        Copy-Item "css/*" "frontend/src/styles/" -Recurse -Force
        Write-LogSuccess "CSS文件已迁移"
    }
    
    # 迁移JavaScript文件
    if (Test-Path "js") {
        Copy-Item "js/*" "frontend/src/" -Recurse -Force
        Write-LogSuccess "JavaScript文件已迁移"
    }
    
    # 迁移图片资源
    if (Test-Path "img") {
        Copy-Item "img" "frontend/public/assets/" -Recurse -Force
        Write-LogSuccess "图片资源已迁移"
    }
    
    Write-LogSuccess "前端文件迁移完成"
}

# 迁移后端文件
function Move-BackendFiles {
    Write-LogInfo "迁移后端文件..."
    
    # 迁移Python源码
    if (Test-Path "src") {
        Copy-Item "src/*" "backend/src/" -Recurse -Force
        Write-LogSuccess "Python源码已迁移"
    }
    
    # 迁移主程序文件
    Get-ChildItem -Filter "*.py" | Where-Object { $_.Name -ne "migrate.ps1" } | ForEach-Object {
        Copy-Item $_.FullName "backend/"
        Write-LogSuccess "$($_.Name) 已迁移"
    }
    
    # 迁移配置文件
    if (Test-Path "requirements.txt") {
        Copy-Item "requirements.txt" "backend/"
        Write-LogSuccess "requirements.txt 已迁移"
    }
    
    Write-LogSuccess "后端文件迁移完成"
}

# 迁移数据文件
function Move-DataFiles {
    Write-LogInfo "迁移数据文件..."
    
    # 迁移数据库
    if (Test-Path "data/guild_members.db") {
        Copy-Item "data/guild_members.db" "data/database/"
        Write-LogSuccess "数据库已迁移"
    }
    
    # 迁移JSON文件
    if (Test-Path "data") {
        Get-ChildItem "data" -Filter "*.json" -Recurse | ForEach-Object {
            Copy-Item $_.FullName "data/exports/"
        }
        Write-LogSuccess "JSON数据文件已迁移"
    }
    
    # 迁移缓存
    if (Test-Path "cache") {
        Copy-Item "cache/*" "data/cache/" -Recurse -Force
        Write-LogSuccess "缓存文件已迁移"
    }
    
    # 迁移日志
    if (Test-Path "logs") {
        Copy-Item "logs/*" "data/logs/" -Recurse -Force
        Write-LogSuccess "日志文件已迁移"
    }
    
    Write-LogSuccess "数据文件迁移完成"
}

# 创建配置文件
function New-ConfigFiles {
    Write-LogInfo "创建配置文件..."
    
    # 复制工作区package.json
    if (Test-Path "package-workspace.json") {
        Copy-Item "package-workspace.json" "package.json" -Force
        Write-LogSuccess "package.json 已创建"
    }
    
    # 复制Docker配置
    if (Test-Path "docker-compose.yml") {
        Write-LogSuccess "docker-compose.yml 已存在"
    }
    
    # 复制环境变量示例
    if (Test-Path "env.example") {
        Copy-Item "env.example" ".env.example" -Force
        Write-LogSuccess ".env.example 已创建"
    }
    
    Write-LogSuccess "配置文件创建完成"
}

# 验证迁移结果
function Test-Migration {
    Write-LogInfo "验证迁移结果..."
    
    # 检查目录结构
    if ((Test-Path "frontend") -and (Test-Path "backend") -and (Test-Path "shared")) {
        Write-LogSuccess "目录结构验证通过"
    } else {
        Write-LogError "目录结构验证失败"
        exit 1
    }
    
    # 检查数据文件
    if ((Test-Path "data/database/guild_members.db") -or (Test-Path "data/exports")) {
        Write-LogSuccess "数据文件验证通过"
    } else {
        Write-LogWarning "数据文件可能未完全迁移"
    }
    
    # 检查前端文件
    if ((Test-Path "frontend/public/index.html") -or (Test-Path "frontend/src/styles")) {
        Write-LogSuccess "前端文件验证通过"
    } else {
        Write-LogWarning "前端文件可能未完全迁移"
    }
    
    # 检查后端文件
    if ((Test-Path "backend/src") -or (Test-Path "backend/requirements.txt")) {
        Write-LogSuccess "后端文件验证通过"
    } else {
        Write-LogWarning "后端文件可能未完全迁移"
    }
    
    Write-LogSuccess "迁移验证完成"
}

# 清理旧文件
function Remove-OldFiles {
    if ($SkipCleanup) {
        Write-LogInfo "跳过清理步骤"
        return
    }
    
    Write-LogInfo "清理旧文件..."
    
    if (-not $Force) {
        $response = Read-Host "是否清理原始文件？(y/N)"
        if ($response -notmatch "^[Yy]$") {
            Write-LogInfo "跳过清理步骤"
            return
        }
    }
    
    # 备份原始文件到临时目录
    $tempDir = "temp_old_files_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    
    # 移动原始文件
    $filesToMove = @("*.html", "css", "js", "img", "src", "*.py", "requirements.txt")
    foreach ($pattern in $filesToMove) {
        Get-ChildItem -Filter $pattern -ErrorAction SilentlyContinue | ForEach-Object {
            Move-Item $_.FullName $tempDir -Force
        }
    }
    
    Write-LogSuccess "原始文件已移动到 $tempDir/"
    Write-LogInfo "如需恢复，请从 $tempDir/ 复制文件"
}

# 主函数
function Start-Migration {
    Write-LogInfo "开始易骑公会官方网站重构迁移..."
    Write-LogInfo "时间: $(Get-Date)"
    
    # 检查是否在项目根目录
    if (-not (Test-Path "README.md")) {
        Write-LogError "请在项目根目录运行此脚本"
        exit 1
    }
    
    # 执行迁移步骤
    Test-Dependencies
    Backup-Data
    New-DirectoryStructure
    Move-FrontendFiles
    Move-BackendFiles
    Move-DataFiles
    New-ConfigFiles
    Test-Migration
    Remove-OldFiles
    
    Write-LogSuccess "迁移完成！"
    Write-LogInfo "下一步："
    Write-LogInfo "1. 复制 .env.example 为 .env 并配置环境变量"
    Write-LogInfo "2. 运行 'npm install' 安装依赖"
    Write-LogInfo "3. 运行 'npm run dev' 启动开发服务器"
    Write-LogInfo "4. 查看 REFACTOR_PLAN.md 了解详细的重构计划"
}

# 运行主函数
Start-Migration 