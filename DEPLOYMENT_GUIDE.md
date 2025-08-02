# 🚀 一起公会网站部署指南

## 📋 部署前准备

### 环境要求
- **操作系统**: Windows 10/11, Linux, macOS
- **Python**: 3.11+ 
- **Node.js**: 18+
- **内存**: 至少2GB可用内存
- **磁盘空间**: 至少1GB可用空间

### 检查环境
```bash
# 检查Python版本
python --version

# 检查Node.js版本
node --version
npm --version
```

## 🐳 方案一：Docker容器化部署（推荐）

### 1. 安装Docker Desktop
- **Windows**: 下载并安装 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
- **Linux**: 按照 [Docker官方文档](https://docs.docker.com/engine/install/) 安装
- **macOS**: 下载并安装 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)

### 2. 启动Docker服务
```bash
# 启动Docker Desktop（Windows/macOS）
# 或在Linux上启动Docker服务
sudo systemctl start docker
```

### 3. 部署应用
```bash
# 构建并启动生产环境
docker-compose -f docker-compose.prod.yml up -d --build

# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f
```

### 4. 访问应用
- **前端**: http://localhost:80
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

### 5. 停止服务
```bash
docker-compose -f docker-compose.prod.yml down
```

## ⚙️ 方案二：传统部署（Windows）

### 1. 使用PowerShell脚本部署
```powershell
# 以管理员身份运行PowerShell
.\deploy.ps1
```

### 2. 手动部署步骤

#### 后端部署
```powershell
# 进入后端目录
cd backend-refactor

# 安装Python依赖
pip install -r requirements.txt

# 初始化数据库
python database_setup.py

# 启动后端服务
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 前端部署
```powershell
# 进入前端目录
cd frontend-refactor

# 安装Node.js依赖
npm install

# 构建生产版本
npm run build

# 安装serve工具
npm install -g serve

# 启动前端服务
npx serve -s dist -l 3000
```

### 3. 停止服务
```powershell
# 使用停止脚本
.\stop-services.ps1

# 或手动停止
# 按 Ctrl+C 停止服务
```

## 🐧 方案三：传统部署（Linux/macOS）

### 1. 使用Shell脚本部署
```bash
# 给脚本执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

### 2. 手动部署步骤

#### 后端部署
```bash
# 进入后端目录
cd backend-refactor

# 安装Python依赖
pip install -r requirements.txt

# 初始化数据库
python database_setup.py

# 启动后端服务（后台运行）
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
```

#### 前端部署
```bash
# 进入前端目录
cd frontend-refactor

# 安装Node.js依赖
npm install

# 构建生产版本
npm run build

# 安装serve工具
npm install -g serve

# 启动前端服务（后台运行）
nohup serve -s dist -l 3000 > ../logs/frontend.log 2>&1 &
```

### 3. 停止服务
```bash
# 查找并停止进程
pkill -f uvicorn
pkill -f serve
```

## 🔧 配置说明

### 环境变量配置
创建 `.env` 文件：
```env
# 数据库配置
DATABASE_URL=sqlite:///./data/guild_members.db

# 安全配置
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000", "http://your-domain.com"]

# 日志配置
LOG_LEVEL=INFO
LOGS_DIR=./logs

# 监控配置
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
```

### 端口配置
- **前端**: 3000 (开发) / 80 (生产)
- **后端**: 8000
- **Grafana**: 3001
- **Prometheus**: 9090

## 📊 监控和日志

### 查看日志
```bash
# 后端日志
tail -f logs/backend.log

# 前端日志
tail -f logs/frontend.log

# Docker日志
docker-compose -f docker-compose.prod.yml logs -f [service-name]
```

### 健康检查
```bash
# 检查后端健康状态
curl http://localhost:8000/health

# 检查前端服务
curl http://localhost:3000

# 检查Docker容器状态
docker-compose -f docker-compose.prod.yml ps
```

## 🚨 故障排除

### 常见问题

#### 1. 端口被占用
```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID>

# Linux/macOS
lsof -i :8000
kill -9 <PID>
```

#### 2. 权限问题
```bash
# Linux/macOS
sudo chmod +x deploy.sh
sudo chown -R $USER:$USER .

# Windows
# 以管理员身份运行PowerShell
```

#### 3. 依赖安装失败
```bash
# 清理缓存
npm cache clean --force
pip cache purge

# 重新安装
rm -rf node_modules package-lock.json
npm install
```

#### 4. 数据库问题
```bash
# 重新初始化数据库
cd backend-refactor
python database_setup.py
```

### 调试模式
```bash
# 启用调试日志
export LOG_LEVEL=DEBUG

# 启动调试模式
docker-compose -f docker-compose.yml up --build
```

## 🔄 更新部署

### 代码更新
```bash
# 拉取最新代码
git pull origin main

# 重新部署
# Docker方式
docker-compose -f docker-compose.prod.yml up -d --build

# 传统方式
./deploy.sh  # Linux/macOS
.\deploy.ps1 # Windows
```

### 数据库迁移
```bash
cd backend-refactor
python database_setup.py
```

## 📞 技术支持

如果遇到部署问题，请：

1. 检查环境要求是否满足
2. 查看日志文件获取错误信息
3. 确认端口没有被其他服务占用
4. 检查防火墙设置

### 联系信息
- 项目维护者: 一起公会技术团队
- 公会QQ群: [群号]
- 邮箱: [邮箱地址]

---

**一起公会** - 让游戏更有趣，让公会更温暖 🎮✨ 