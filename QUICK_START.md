# 易骑公会官方网站 - 快速开始指南

## 🚀 快速开始

### 环境要求

- **Node.js**: 18.0.0 或更高版本
- **Python**: 3.8 或更高版本
- **Git**: 最新版本
- **Docker**: 可选，用于容器化部署

### 1. 克隆项目

```bash
git clone [项目地址]
cd yiqi
```

### 2. 运行迁移脚本

```bash
# 给脚本执行权限
chmod +x scripts/migrate.sh

# 运行迁移脚本
./scripts/migrate.sh
```

### 3. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑环境变量文件
nano .env
```

### 4. 安装依赖

```bash
# 安装所有依赖（包括前端和后端）
npm run install:all

# 或者分别安装
npm install --workspace=frontend
npm install --workspace=backend
```

### 5. 启动开发服务器

```bash
# 同时启动前端和后端
npm run dev

# 或者分别启动
npm run dev:frontend  # 前端 (http://localhost:3000)
npm run dev:backend   # 后端 (http://localhost:8000)
```

### 6. 访问应用

- **前端**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 📁 项目结构

```
yiqi/
├── frontend/          # React前端应用
├── backend/           # FastAPI后端应用
├── shared/            # 共享代码
├── data/              # 数据文件
├── docs/              # 文档
├── scripts/           # 脚本文件
└── infrastructure/    # 基础设施配置
```

## 🛠️ 开发命令

### 工作区命令

```bash
# 开发
npm run dev                    # 启动所有服务
npm run dev:frontend          # 启动前端
npm run dev:backend           # 启动后端

# 构建
npm run build                 # 构建所有项目
npm run build:frontend        # 构建前端
npm run build:backend         # 构建后端

# 测试
npm run test                  # 运行所有测试
npm run test:frontend         # 前端测试
npm run test:backend          # 后端测试

# 代码质量
npm run lint                  # 代码检查
npm run lint:fix              # 自动修复
npm run format                # 代码格式化

# Docker
npm run docker:build          # 构建Docker镜像
npm run docker:up             # 启动Docker服务
npm run docker:down           # 停止Docker服务
```

### 前端命令

```bash
cd frontend

# 开发
npm run dev                   # 启动开发服务器
npm run build                 # 构建生产版本
npm run preview               # 预览构建结果

# 测试
npm run test                  # 运行测试
npm run test:ui               # 测试UI界面
npm run test:coverage         # 测试覆盖率

# 代码质量
npm run lint                  # ESLint检查
npm run lint:fix              # 自动修复
npm run format                # Prettier格式化
npm run type-check            # TypeScript类型检查
```

### 后端命令

```bash
cd backend

# 开发
python main.py                # 启动开发服务器
uvicorn main:app --reload     # 热重载模式

# 测试
pytest                        # 运行测试
pytest --cov                  # 测试覆盖率
pytest -v                     # 详细输出

# 数据库
alembic upgrade head          # 数据库迁移
alembic revision --autogenerate # 生成迁移文件
```

## 🔧 配置说明

### 环境变量

主要的环境变量配置：

```bash
# 应用配置
APP_NAME=易骑公会官方网站
ENVIRONMENT=development
DEBUG=true

# 服务器配置
HOST=0.0.0.0
PORT=8000
FRONTEND_PORT=3000

# 数据库配置
DATABASE_URL=sqlite:///./data/database/guild.db

# API配置
API_BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000

# 暴雪API配置（需要申请）
BLIZZARD_CLIENT_ID=your_client_id
BLIZZARD_CLIENT_SECRET=your_client_secret
```

### 数据库配置

项目支持多种数据库：

```bash
# SQLite (默认)
DATABASE_URL=sqlite:///./data/database/guild.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/yiqi_guild

# MySQL
DATABASE_URL=mysql://user:password@localhost:3306/yiqi_guild
```

## 🐳 Docker部署

### 使用Docker Compose

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 单独构建

```bash
# 构建前端镜像
docker build -t yiqi-frontend ./frontend

# 构建后端镜像
docker build -t yiqi-backend ./backend

# 运行容器
docker run -p 3000:3000 yiqi-frontend
docker run -p 8000:8000 yiqi-backend
```

## 📊 监控和日志

### 应用监控

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

### 日志查看

```bash
# 查看应用日志
tail -f data/logs/app.log

# 查看Docker日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🧪 测试

### 运行测试

```bash
# 前端测试
cd frontend
npm run test

# 后端测试
cd backend
pytest

# 集成测试
npm run test:e2e
```

### 测试覆盖率

```bash
# 前端覆盖率
cd frontend
npm run test:coverage

# 后端覆盖率
cd backend
pytest --cov=src --cov-report=html
```

## 🔍 调试

### 前端调试

1. 打开浏览器开发者工具
2. 查看Console和Network标签
3. 使用React Developer Tools扩展

### 后端调试

1. 使用VS Code调试器
2. 查看日志文件
3. 使用FastAPI的自动文档

### 数据库调试

```bash
# SQLite
sqlite3 data/database/guild.db

# PostgreSQL
psql -h localhost -U user -d yiqi_guild
```

## 🚨 常见问题

### 1. 端口被占用

```bash
# 查看端口占用
lsof -i :3000
lsof -i :8000

# 杀死进程
kill -9 <PID>
```

### 2. 依赖安装失败

```bash
# 清除缓存
npm cache clean --force
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

### 3. 数据库连接失败

```bash
# 检查数据库文件
ls -la data/database/

# 重新初始化数据库
cd backend
python -c "from src.database.connection import init_database; import asyncio; asyncio.run(init_database())"
```

### 4. 环境变量不生效

```bash
# 检查环境变量文件
cat .env

# 重启服务
npm run dev
```

## 📚 更多资源

- [重构计划](REFACTOR_PLAN.md) - 详细的重构计划
- [API文档](http://localhost:8000/docs) - 后端API文档
- [项目文档](docs/) - 详细的项目文档
- [开发指南](docs/development/) - 开发指南

## 🤝 贡献

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📞 支持

- 项目维护者: 易骑公会技术团队
- 公会QQ群: [群号]
- 邮箱: [邮箱地址]

---

**易骑公会** - 让游戏更有趣，让公会更温暖 🎮✨ 