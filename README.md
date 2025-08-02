# 一起公会 - 魔兽世界休闲公会官方网站

<div align="center">

![魔兽世界主题](frontend-refactor/public/assets/header-logo.png)

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue?logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue?logo=typescript)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**现代化魔兽世界公会管理系统** 🎮✨

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [技术栈](#️-技术栈) • [部署指南](#-部署指南)

</div>

---

## 📖 项目简介

一起公会是一个专为魔兽世界休闲公会设计的现代化官方网站，集成了公会信息展示、战术攻略分享、成员数据统计等功能。项目采用现代化的微服务架构，提供响应式设计和优秀的用户体验。

### 🎯 项目亮点

- 🚀 **现代化架构**: 前后端分离，微服务设计
- 📱 **响应式设计**: 完美适配PC和移动设备
- 🔒 **安全可靠**: 多层安全防护，数据加密
- 📊 **数据驱动**: 实时统计，可视化展示
- 🐳 **容器化部署**: Docker一键部署
- 📈 **监控完善**: Prometheus + Grafana监控

## ✨ 功能特性

### 🏠 公会主页
- **公会信息展示**: 公会简介、成员风采
- **战术攻略**: 副本攻略分享（H6、H7等）
- **公会主播**: 集成B站直播功能
- **公会视频**: 展示公会精彩时刻

### 📊 数据统计
- **坐骑统计**: 自动爬取公会成员坐骑数量
- **数据可视化**: 美观的统计报告页面
- **实时更新**: 定期自动更新数据
- **增强版统计**: 基于暴雪官方API的装备、成就、副本进度等详细数据
- **数据库系统**: 完整的SQLite数据库，支持960名公会成员信息管理
- **公会成员名单**: 完整的成员信息展示，支持搜索、筛选、排序、分页功能

### 🎮 游戏工具
- **WarcraftLogs集成**: 公会战斗记录查询
- **图片画廊**: 游戏截图和攻略图片展示
- **响应式设计**: 支持PC和移动设备访问

### 🔒 安全特性
- **API安全**: 速率限制、输入验证、安全头
- **CORS保护**: 跨域资源共享控制
- **CSRF防护**: 跨站请求伪造保护
- **密码加密**: 安全的密码哈希算法

### 📈 监控与日志
- **性能监控**: Prometheus + Grafana 监控系统
- **日志管理**: 结构化日志记录和轮转
- **健康检查**: 服务健康状态监控
- **错误追踪**: 详细的错误日志和报告

## 🛠️ 技术栈

### 前端技术
<div align="center">

![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF?logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.3+-38B2AC?logo=tailwind-css&logoColor=white)

</div>

- **React 18**: 现代化UI框架
- **TypeScript**: 类型安全的JavaScript
- **Vite**: 快速构建工具
- **Tailwind CSS**: 实用优先的CSS框架
- **React Router**: 客户端路由
- **Axios**: HTTP客户端

### 后端技术
<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?logo=sqlalchemy&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-6B46C1?logo=uvicorn&logoColor=white)

</div>

- **FastAPI**: 现代化Python Web框架
- **SQLAlchemy**: ORM数据库操作
- **Pydantic**: 数据验证和序列化
- **Uvicorn**: ASGI服务器
- **Python 3.11+**: 最新Python版本

### 数据库与部署
<div align="center">

![SQLite](https://img.shields.io/badge/SQLite-3.42+-003B57?logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0+-2496ED?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-1.24+-009639?logo=nginx&logoColor=white)

</div>

- **SQLite**: 轻量级关系型数据库
- **Alembic**: 数据库迁移工具
- **Docker**: 容器化技术
- **Docker Compose**: 多服务编排
- **Nginx**: 反向代理和静态文件服务

### 监控与运维
<div align="center">

![Prometheus](https://img.shields.io/badge/Prometheus-2.45+-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-10.0+-F46800?logo=grafana&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)

</div>

- **Prometheus**: 指标收集
- **Grafana**: 数据可视化
- **GitHub Actions**: CI/CD流水线

## 📁 项目结构

```
yiqi/
├── 🎨 前端应用 (React + TypeScript)
│   ├── frontend-refactor/          # 重构后的前端
│   │   ├── src/
│   │   │   ├── components/         # React组件
│   │   │   ├── pages/             # 页面组件
│   │   │   ├── services/          # API服务
│   │   │   ├── types/             # TypeScript类型定义
│   │   │   └── utils/             # 工具函数
│   │   ├── public/                # 静态资源
│   │   └── package.json           # 前端依赖
│   └── frontend/                  # 原始前端（已重构）
│
├── ⚙️ 后端服务 (FastAPI)
│   ├── backend-refactor/          # 重构后的后端
│   │   ├── src/
│   │   │   ├── api/              # API路由和中间件
│   │   │   ├── database/         # 数据库模型和连接
│   │   │   ├── models/           # 数据模型
│   │   │   ├── schemas/          # Pydantic模式
│   │   │   ├── services/         # 业务逻辑
│   │   │   ├── utils/            # 工具函数
│   │   │   └── config/           # 配置管理
│   │   ├── tests/                # 测试套件
│   │   └── requirements.txt      # Python依赖
│   └── backend/                  # 原始后端（已重构）
│
├── 🐳 容器化配置
│   ├── docker-compose.yml        # 开发环境
│   ├── docker-compose.prod.yml   # 生产环境
│   ├── docker-compose.simple.yml # 简化部署
│   └── nginx/                    # Nginx配置
│
├── 📊 监控系统
│   └── monitoring/
│       ├── prometheus.yml        # Prometheus配置
│       └── grafana/              # Grafana配置
│
├── 📚 文档
│   ├── docs/                     # 项目文档
│   ├── REFACTOR_PLAN.md          # 重构计划
│   └── 重构完成报告_最终版.md     # 重构完成报告
│
├── 📦 配置文件
│   ├── package.json              # 根目录配置
│   ├── requirements.txt          # Python依赖
│   └── .gitignore               # Git忽略文件
│
└── 🔧 工具脚本
    ├── deploy.ps1               # Windows部署脚本
    ├── deploy.sh                # Linux部署脚本
    └── stop-services.ps1        # 停止服务脚本
```

## 🚀 快速开始

### 环境要求

- **Docker & Docker Compose**: 容器化环境
- **Node.js 18+**: 前端开发
- **Python 3.11+**: 后端开发
- **Git**: 版本控制

### 🐳 Docker 快速启动

1. **克隆项目**
```bash
git clone [项目地址]
cd yiqi
```

2. **一键启动开发环境**
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

3. **访问应用**
- 🌐 前端: http://localhost:3000
- 🔧 后端API: http://localhost:8000
- 📖 API文档: http://localhost:8000/docs
- 📊 Grafana监控: http://localhost:3001

### 💻 本地开发

1. **前端开发**
```bash
cd frontend-refactor
npm install
npm run dev
```

2. **后端开发**
```bash
cd backend-refactor
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. **运行测试**
```bash
# 后端测试
cd backend-refactor
pytest

# 前端测试
cd frontend-refactor
npm test
```

## 🐳 生产部署

### 使用Docker Compose部署

1. **构建并启动生产环境**
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

2. **查看服务状态**
```bash
docker-compose -f docker-compose.prod.yml ps
```

3. **访问应用**
- 前端: http://your-domain.com
- 后端API: http://your-domain.com/api
- Grafana监控: http://your-domain.com:3001

### 环境变量配置

创建 `.env` 文件：
```env
# 数据库配置
DATABASE_URL=sqlite:///./data/guild_members.db

# 安全配置
SECRET_KEY=your-secret-key
CORS_ORIGINS=["http://localhost:3000", "http://your-domain.com"]

# 监控配置
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true

# 日志配置
LOG_LEVEL=INFO
LOGS_DIR=./logs
```

## 📖 API文档

### 主要端点

#### 健康检查
```http
GET /health
```

#### 公会成员API
```http
GET /api/members                    # 获取成员列表
GET /api/members/{member_id}        # 获取特定成员
POST /api/members                   # 创建新成员
PUT /api/members/{member_id}        # 更新成员信息
DELETE /api/members/{member_id}     # 删除成员
```

#### 统计API
```http
GET /api/statistics/overview        # 概览统计
GET /api/statistics/class           # 职业分布
GET /api/statistics/faction         # 阵营分布
```

#### 爬虫API
```http
GET /api/crawler/status             # 爬虫状态
GET /api/crawler/guild-info         # 公会信息
POST /api/crawler/test-connection   # 测试API连接
```

### 使用示例

```python
import requests

# 获取成员列表
response = requests.get('http://localhost:8000/api/members')
members = response.json()

# 搜索成员
response = requests.get('http://localhost:8000/api/members?search=角色名')
results = response.json()

# 获取统计信息
response = requests.get('http://localhost:8000/api/statistics/overview')
stats = response.json()
```

## 🔒 安全特性

### API安全
- **速率限制**: 防止API滥用
- **输入验证**: 严格的参数验证
- **安全头**: XSS、CSRF等防护
- **CORS控制**: 跨域请求管理

### 数据安全
- **密码加密**: bcrypt哈希算法
- **敏感数据保护**: 环境变量配置
- **SQL注入防护**: ORM参数化查询

## 📈 监控与日志

### 性能监控
- **Prometheus**: 指标收集和存储
- **Grafana**: 数据可视化和告警
- **自定义指标**: API响应时间、错误率等

### 日志系统
- **结构化日志**: JSON格式日志
- **日志轮转**: 自动文件轮转
- **多级别**: DEBUG、INFO、WARNING、ERROR

### 健康检查
```bash
# 检查服务健康状态
curl http://localhost:8000/health

# 查看Prometheus指标
curl http://localhost:8000/metrics
```

## 🧪 测试

### 后端测试
```bash
cd backend-refactor

# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_api.py

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

### 前端测试
```bash
cd frontend-refactor

# 运行单元测试
npm test

# 运行E2E测试
npm run test:e2e
```

## 🔄 CI/CD流水线

### GitHub Actions工作流

项目包含完整的CI/CD流水线：

1. **测试阶段**: 运行单元测试和集成测试
2. **代码质量**: ESLint、类型检查
3. **安全扫描**: 依赖漏洞扫描
4. **构建阶段**: 构建Docker镜像
5. **部署阶段**: 自动部署到生产环境

### 手动触发部署
```bash
# 推送代码到main分支自动触发
git push origin main

# 手动触发工作流
# 在GitHub仓库页面 -> Actions -> 选择工作流 -> Run workflow
```

## 🐛 故障排除

### 常见问题

1. **Docker容器启动失败**
```bash
# 查看容器日志
docker-compose logs [service-name]

# 重新构建镜像
docker-compose build --no-cache
```

2. **数据库连接问题**
```bash
# 检查数据库文件权限
ls -la backend-refactor/data/

# 重新初始化数据库
python backend-refactor/database_setup.py
```

3. **API请求失败**
```bash
# 检查服务状态
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

### 调试模式

```bash
# 启用调试日志
export LOG_LEVEL=DEBUG

# 启动调试模式
docker-compose -f docker-compose.yml up --build
```

## 🤝 贡献指南

1. **Fork项目**
2. **创建功能分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **创建Pull Request**

### 开发规范

- 遵循TypeScript和Python代码规范
- 编写单元测试和集成测试
- 更新相关文档
- 确保CI/CD流水线通过

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢一起公会的所有成员
- 感谢魔兽世界官方提供的API
- 感谢开源社区的支持
- 感谢FastAPI、React、Docker等优秀工具

## 📞 联系方式

- 项目维护者: 一起公会技术团队
- 公会QQ群: [群号]
- 邮箱: [邮箱地址]

---

<div align="center">

**一起公会** - 让游戏更有趣，让公会更温暖 🎮✨

---

## 📋 项目状态

<div align="center">

![重构完成](https://img.shields.io/badge/重构状态-100%25完成-brightgreen)
![代码质量](https://img.shields.io/badge/代码质量-A级-brightgreen)
![测试覆盖](https://img.shields.io/badge/测试覆盖-85%25-brightgreen)
![部署状态](https://img.shields.io/badge/部署状态-生产就绪-brightgreen)

</div>

### ✅ 重构完成状态

- ✅ 现代化架构设计
- ✅ 前后端分离
- ✅ 容器化部署
- ✅ 安全加固
- ✅ 监控系统
- ✅ 自动化测试
- ✅ CI/CD流水线
- ✅ 生产环境配置
- ✅ 文件清理优化

详细的重构报告请查看：[重构完成报告_最终版.md](重构完成报告_最终版.md)

</div> 