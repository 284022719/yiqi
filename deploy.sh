#!/bin/bash

# 一起公会网站部署脚本
# 适用于传统服务器环境

set -e

echo "🚀 开始部署一起公会网站..."

# 检查Python版本
echo "📋 检查Python版本..."
python3 --version

# 检查Node.js版本
echo "📋 检查Node.js版本..."
node --version
npm --version

# 创建必要的目录
echo "📁 创建目录结构..."
mkdir -p data/database
mkdir -p data/logs
mkdir -p data/cache
mkdir -p logs

# 后端部署
echo "🐍 部署后端服务..."
cd backend-refactor

# 安装Python依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 初始化数据库
echo "🗄️ 初始化数据库..."
python database_setup.py

# 启动后端服务
echo "🚀 启动后端服务..."
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "后端服务已启动，PID: $BACKEND_PID"

cd ..

# 前端部署
echo "⚛️ 部署前端服务..."
cd frontend-refactor

# 安装Node.js依赖
echo "📦 安装Node.js依赖..."
npm install

# 构建生产版本
echo "🔨 构建前端应用..."
npm run build

# 安装serve工具
echo "📦 安装serve工具..."
npm install -g serve

# 启动前端服务
echo "🚀 启动前端服务..."
nohup serve -s dist -l 3000 > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端服务已启动，PID: $FRONTEND_PID"

cd ..

# 保存进程ID
echo $BACKEND_PID > logs/backend.pid
echo $FRONTEND_PID > logs/frontend.pid

echo "✅ 部署完成！"
echo "🌐 前端地址: http://localhost:3000"
echo "🔧 后端API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo "📋 日志文件: logs/"

# 显示服务状态
echo "📊 服务状态:"
ps aux | grep -E "(uvicorn|serve)" | grep -v grep 