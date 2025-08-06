# JavaScript 模块化架构

本项目采用模块化的JavaScript架构，将原本的单一`main.js`文件拆分为多个独立的功能模块。

## 文件结构

```
js/
├── main.js                 # 主入口文件，负责初始化和协调各个模块
├── config.js               # 全局配置和错误处理
├── modules/                # 功能模块目录
│   ├── ImageModal.js       # 图片模态框系统
│   ├── ParticleSystem.js   # 粒子动画系统
│   ├── WCLDataLoader.js    # WCL数据处理器
│   ├── ImageUploader.js    # 图片上传功能
│   ├── GuildStatsLoader.js # 公会统计数据加载器
│   └── IframeErrorHandler.js # iframe错误处理
└── components/             # 页面组件
    ├── header.js
    ├── footer.js
    └── nav.js
```

## 模块说明

### 1. config.js
- **功能**: 全局配置管理和错误处理
- **导出**: 
  - `CONFIG`: 全局配置对象
  - `initGlobalErrorHandling()`: 初始化全局错误处理

### 2. ImageModal.js
- **功能**: 图片模态框系统，支持图片预览、导航和键盘操作
- **导出**: `ImageModal` 类
- **主要方法**:
  - `registerImages()`: 注册可点击的图片
  - `openModal()`: 打开模态框
  - `closeModal()`: 关闭模态框

### 3. ParticleSystem.js
- **功能**: 粒子动画系统，创建动态背景效果
- **导出**: `ParticleSystem` 类
- **依赖**: `config.js` 中的 `CONFIG` 对象

### 4. WCLDataLoader.js
- **功能**: WCL数据加载和渲染
- **导出**: `WCLDataLoader` 类
- **主要方法**:
  - `fetchReports()`: 获取WCL报告数据
  - `renderReports()`: 渲染报告列表

### 5. ImageUploader.js
- **功能**: 图片上传和画廊管理
- **导出**: `ImageUploader` 类
- **主要方法**:
  - `handleFormSubmit()`: 处理表单提交
  - `loadGallery()`: 加载图片画廊
  - `addImageToGallery()`: 添加图片到画廊

### 6. GuildStatsLoader.js
- **功能**: 公会统计数据加载和图表渲染
- **导出**: `GuildStatsLoader` 类
- **主要方法**:
  - `loadStats()`: 加载统计数据
  - `renderCharts()`: 渲染各种图表

### 7. IframeErrorHandler.js
- **功能**: iframe错误处理和备用内容显示
- **导出**: `IframeErrorHandler` 类

## 主入口文件 (main.js)

`main.js` 作为应用程序的入口点，负责：

1. **导入所有模块**: 使用ES6模块语法导入各个功能模块
2. **初始化全局错误处理**: 调用 `initGlobalErrorHandling()`
3. **加载页面组件**: 加载header、footer和navigation
4. **条件初始化**: 根据页面内容有选择地初始化特定模块
5. **全局导出**: 将所有类暴露到全局作用域，保持向后兼容性

## 使用方式

### 自动初始化
模块会在页面加载时自动初始化，无需手动调用。

### 手动使用
如果需要手动使用某个模块，可以通过全局对象访问：

```javascript
// 创建图片模态框
const modal = new window.ImageModal();

// 创建粒子系统
const particles = new window.ParticleSystem();

// 加载WCL数据
const wclLoader = new window.WCLDataLoader();
```

## 优势

1. **模块化**: 每个功能独立，便于维护和测试
2. **可重用**: 模块可以在不同页面中复用
3. **可扩展**: 新增功能只需创建新模块
4. **向后兼容**: 保持原有的全局对象访问方式
5. **条件加载**: 只在需要的页面初始化相应模块

## 开发指南

### 添加新模块
1. 在 `js/modules/` 目录下创建新的 `.js` 文件
2. 使用ES6模块语法导出类或函数
3. 在 `main.js` 中导入新模块
4. 在适当的位置初始化新模块
5. 可选择性地暴露到全局作用域

### 修改现有模块
1. 直接修改对应的模块文件
2. 确保导出接口保持一致
3. 测试相关功能是否正常工作

### 调试
- 使用浏览器开发者工具查看模块加载情况
- 检查控制台是否有模块导入错误
- 验证全局对象是否正确暴露 