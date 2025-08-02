# 一起公会网站部署脚本 (Windows PowerShell)
# 适用于Windows服务器环境

Write-Host "🚀 开始部署一起公会网站..." -ForegroundColor Green

# 检查Python版本
Write-Host "📋 检查Python版本..." -ForegroundColor Yellow
try {
    python --version
} catch {
    Write-Host "❌ Python未安装，请先安装Python 3.11+" -ForegroundColor Red
    exit 1
}

# 检查Node.js版本
Write-Host "📋 检查Node.js版本..." -ForegroundColor Yellow
try {
    node --version
    npm --version
} catch {
    Write-Host "❌ Node.js未安装，请先安装Node.js 18+" -ForegroundColor Red
    exit 1
}

# 创建必要的目录
Write-Host "📁 创建目录结构..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data/database"
New-Item -ItemType Directory -Force -Path "data/logs"
New-Item -ItemType Directory -Force -Path "data/cache"
New-Item -ItemType Directory -Force -Path "logs"

# 后端部署
Write-Host "🐍 部署后端服务..." -ForegroundColor Yellow
Set-Location "backend-refactor"

# 安装Python依赖
Write-Host "📦 安装Python依赖..." -ForegroundColor Yellow
pip install -r requirements.txt

# 初始化数据库
Write-Host "🗄️ 初始化数据库..." -ForegroundColor Yellow
python database_setup.py

# 启动后端服务
Write-Host "🚀 启动后端服务..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" -WindowStyle Hidden
Write-Host "后端服务已启动在端口 8000"

Set-Location ".."

# 前端部署
Write-Host "⚛️ 部署前端服务..." -ForegroundColor Yellow
Set-Location "frontend-refactor"

# 安装Node.js依赖
Write-Host "📦 安装Node.js依赖..." -ForegroundColor Yellow
npm install

# 构建生产版本
Write-Host "🔨 构建前端应用..." -ForegroundColor Yellow
npm run build

# 安装serve工具
Write-Host "📦 安装serve工具..." -ForegroundColor Yellow
npm install -g serve

# 启动前端服务
Write-Host "🚀 启动前端服务..." -ForegroundColor Yellow
Start-Process -FilePath "npx" -ArgumentList "serve", "-s", "dist", "-l", "3000" -WindowStyle Hidden
Write-Host "前端服务已启动在端口 3000"

Set-Location ".."

Write-Host "✅ 部署完成！" -ForegroundColor Green
Write-Host "🌐 前端地址: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 后端API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API文档: http://localhost:8000/docs" -ForegroundColor Cyan

# 显示服务状态
Write-Host "📊 服务状态:" -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*node*"}

Write-Host "`n💡 提示:" -ForegroundColor Yellow
Write-Host "- 使用 'netstat -ano | findstr :8000' 检查后端服务" -ForegroundColor Gray
Write-Host "- 使用 'netstat -ano | findstr :3000' 检查前端服务" -ForegroundColor Gray
Write-Host "- 使用 'taskkill /F /PID <PID>' 停止服务" -ForegroundColor Gray 