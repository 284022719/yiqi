# 重构后的项目结构

```
yiqi/
├── 📁 frontend/                    # 前端代码
│   ├── 📁 src/
│   │   ├── 📁 components/          # React组件
│   │   │   ├── Header/
│   │   │   ├── Footer/
│   │   │   ├── Navigation/
│   │   │   ├── GuildMembers/
│   │   │   ├── Statistics/
│   │   │   └── Gallery/
│   │   ├── 📁 pages/               # 页面组件
│   │   │   ├── Home/
│   │   │   ├── GuildMembers/
│   │   │   ├── Statistics/
│   │   │   ├── Gallery/
│   │   │   ├── H6Guide/
│   │   │   └── H7Guide/
│   │   ├── 📁 hooks/               # 自定义Hooks
│   │   ├── 📁 services/            # API服务
│   │   ├── 📁 utils/               # 工具函数
│   │   ├── 📁 styles/              # 样式文件
│   │   ├── 📁 assets/              # 静态资源
│   │   └── 📁 types/               # TypeScript类型定义
│   ├── 📁 public/                  # 公共资源
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── tailwind.config.js
│
├── 📁 backend/                     # 后端代码
│   ├── 📁 src/
│   │   ├── 📁 api/                 # API路由
│   │   │   ├── 📁 routes/
│   │   │   ├── 📁 middleware/
│   │   │   └── 📁 controllers/
│   │   ├── 📁 services/            # 业务逻辑
│   │   │   ├── 📁 crawler/         # 爬虫服务
│   │   │   ├── 📁 database/        # 数据库服务
│   │   │   └── 📁 statistics/      # 统计服务
│   │   ├── 📁 models/              # 数据模型
│   │   ├── 📁 utils/               # 工具函数
│   │   ├── 📁 config/              # 配置文件
│   │   └── 📁 tests/               # 测试文件
│   ├── requirements.txt
│   ├── main.py
│   └── Dockerfile
│
├── 📁 shared/                      # 共享代码
│   ├── 📁 types/                   # 共享类型定义
│   ├── 📁 constants/               # 常量定义
│   └── 📁 utils/                   # 共享工具函数
│
├── 📁 data/                        # 数据文件
│   ├── 📁 database/                # 数据库文件
│   ├── 📁 cache/                   # 缓存文件
│   ├── 📁 logs/                    # 日志文件
│   └── 📁 exports/                 # 导出文件
│
├── 📁 docs/                        # 文档
│   ├── 📁 api/                     # API文档
│   ├── 📁 deployment/              # 部署文档
│   └── 📁 development/             # 开发文档
│
├── 📁 scripts/                     # 脚本文件
│   ├── setup.sh                    # 环境设置脚本
│   ├── deploy.sh                   # 部署脚本
│   └── backup.sh                   # 备份脚本
│
├── 📁 infrastructure/              # 基础设施
│   ├── 📁 docker/                  # Docker配置
│   ├── 📁 nginx/                   # Nginx配置
│   └── 📁 terraform/               # Terraform配置
│
├── .env.example                    # 环境变量示例
├── .gitignore
├── README.md
├── docker-compose.yml
└── package.json                    # 根目录package.json（工作区管理）
```

## 重构重点

### 1. 前后端分离
- 前端使用React + TypeScript + Vite
- 后端使用FastAPI + Python
- 清晰的API接口定义

### 2. 模块化设计
- 组件化开发
- 服务层抽象
- 数据层分离

### 3. 类型安全
- TypeScript前端
- Python类型注解
- 共享类型定义

### 4. 现代化工具链
- Vite构建工具
- ESLint + Prettier代码规范
- Jest测试框架
- Docker容器化

### 5. 开发体验优化
- 热重载开发
- 自动化测试
- 代码质量检查
- 自动化部署 