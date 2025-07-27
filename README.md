# 一起公会 - 魔兽世界休闲公会官方网站

![魔兽世界主题](img/header-logo.png)

## 📖 项目简介

一起公会是一个专为魔兽世界休闲公会设计的官方网站，集成了公会信息展示、战术攻略分享、成员数据统计等功能。项目采用现代化的Web技术栈，提供响应式设计和良好的用户体验。

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

### 🎮 游戏工具
- **WarcraftLogs集成**: 公会战斗记录查询
- **图片画廊**: 游戏截图和攻略图片展示
- **响应式设计**: 支持PC和移动设备访问

## 🛠️ 技术栈

### 前端技术
- **HTML5**: 语义化标签，良好的SEO
- **CSS3**: 魔兽世界主题风格，响应式设计
- **JavaScript (ES6+)**: 模块化开发，组件化架构
- **Font Awesome**: 图标库

### 后端服务
- **Netlify Functions**: 无服务器后端API
- **Node.js**: 服务端JavaScript运行环境

### 数据采集
- **Python 3.x**: 爬虫脚本
- **Selenium**: 浏览器自动化
- **JSON**: 数据存储格式

### 部署平台
- **Netlify**: 静态网站托管和函数服务

## 📁 项目结构

```
yiqi/
├── 📄 前端页面
│   ├── index.html          # 主页
│   ├── H6.html            # H6攻略页面
│   ├── H7.html            # H7攻略页面
│   ├── mounts.html        # 坐骑统计页面
│   ├── gallery.html       # 图片画廊
│   └── wcl.html          # WarcraftLogs页面
│
├── 🎨 样式文件
│   └── css/
│       └── style.css      # 主样式文件
│
├── ⚡ JavaScript模块
│   └── js/
│       ├── main.js        # 主脚本
│       └── components/    # 组件模块
│           ├── header.js
│           ├── footer.js
│           └── nav.js
│
├── 🐍 Python脚本
│   ├── batch_mounts.py    # 批量爬取坐骑数据
│   ├── cookies.py         # Cookie管理
│   ├── mount.py          # 单次爬取脚本
│   └── view_logs.py      # 日志查看工具
│
├── 📊 数据文件
│   ├── data/
│   │   └── mounts.json    # 坐骑统计数据
│   └── logs/              # 爬虫日志目录
│
├── 🖼️ 图片资源
│   └── img/
│       ├── favicon/       # 网站图标
│       ├── h6/           # H6攻略图片
│       ├── H7/           # H7攻略图片
│       └── nav/          # 导航图片
│
├── ☁️ Netlify函数
│   └── netlify/functions/
│       ├── wcl-proxy.js   # WCL API代理
│       ├── get-images.js  # 图片获取
│       └── handle-upload.js # 文件上传
│
└── 📦 配置文件
    ├── package.json       # Node.js依赖
    └── *.bat             # Windows批处理脚本
```

## 🚀 快速开始

### 环境要求
- Python 3.7+
- Node.js 14+
- Chrome浏览器（用于爬虫）

### 本地开发

1. **克隆项目**
```bash
git clone [项目地址]
cd yiqi
```

2. **安装依赖**
```bash
# 安装Node.js依赖
npm install

# 安装Python依赖
pip install selenium
```

3. **配置环境变量**
```bash
# 创建.env文件（用于Netlify Functions）
WCL_CLIENT_ID=your_wcl_client_id
WCL_CLIENT_SECRET=your_wcl_client_secret
```

4. **运行爬虫脚本**
```bash
# Windows
run_batch.bat

# 或直接运行Python脚本
python batch_mounts.py
```

5. **启动本地服务器**
```bash
# 使用Python内置服务器
python -m http.server 8000

# 或使用Node.js服务器
npx serve .
```

### 部署到Netlify

1. **连接Git仓库**
   - 将代码推送到GitHub/GitLab
   - 在Netlify中连接仓库

2. **配置构建设置**
   - 构建命令: 无需构建（静态网站）
   - 发布目录: `/` (根目录)

3. **设置环境变量**
   - 在Netlify控制台设置`WCL_CLIENT_ID`和`WCL_CLIENT_SECRET`

## 📖 使用说明

### 爬虫系统

#### 批量爬取坐骑数据
```bash
# 运行批量爬取
python batch_mounts.py
```

#### 查看爬虫日志
```bash
# Windows
view_logs.bat

# 或直接运行
python view_logs.py
```

#### 更新Cookie
```bash
# Windows
run_cookies.bat

# 或直接运行
python cookies.py
```

### 网站功能

#### 添加新攻略
1. 在根目录创建新的HTML文件（如`H8.html`）
2. 在`index.html`中添加链接
3. 在`img/`目录下创建对应的图片文件夹

#### 更新坐骑数据
1. 运行`batch_mounts.py`脚本
2. 检查生成的`mounts.html`报告
3. 确认数据准确性

## 🔧 配置说明

### 爬虫配置
在`batch_mounts.py`中修改以下配置：
```python
# 角色名列表
role_names = [
    "久世", "快来骑我吧", "风少爷丶", 
    # 添加或修改角色名
]

# 服务器名称
server = "arthas"  # 修改为您的服务器
```

### 样式定制
在`css/style.css`中修改CSS变量：
```css
:root {
  --color-primary: #FFD700;    /* 主色调 */
  --color-secondary: #785A28;  /* 次要色调 */
  /* 其他颜色变量 */
}
```

## 📝 开发规范

### 文件命名
- HTML文件使用小写字母和连字符
- JavaScript文件使用驼峰命名
- CSS类名使用连字符分隔

### 代码风格
- 使用2个空格缩进
- 添加适当的注释
- 保持代码简洁可读

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢一起公会的所有成员
- 感谢魔兽世界官方提供的API
- 感谢开源社区的支持

## 📞 联系方式

- 项目维护者: [您的名字]
- 公会QQ群: [群号]
- 邮箱: [邮箱地址]

---

**一起公会** - 让游戏更有趣，让公会更温暖 🎮✨ 