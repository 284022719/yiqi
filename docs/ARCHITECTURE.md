# 架构说明

## 1. 页面与入口

所有页面共用 `js/main.js`：它在 `DOMContentLoaded` 时加载 Header / 导航 / Footer，再按「页面上是否存在某个元素」条件初始化功能模块。

| 页面 | 额外入口 | 初始化的模块 |
|---|---|---|
| `index.html` | — | `GuildStatsLoader`、`ImageModal`、`ParticleSystem`、`IframeErrorHandler` |
| `pages/all-rankings.html` | 内联 module | `TierList` × 6、`RankingNav` + `main.js` 的通用逻辑 |
| `pages/gallery.html` | — | `ImageUploader`、`ImageModal` |
| `pages/wcl.html` | — | `WCLDataLoader` |
| `pages/class-colors.html` | 内联 module | `ClassColorPalette` + `main.js` 的通用逻辑 |
| `pages/H6.html` / `H7.html` | — | `ImageModal`（图片放大） |

> 页面里不要再写静态 `<footer class="footer-container">`：footer 由 `components/footer.js` 统一追加，重复会生成两个节点。

## 2. JS 分层

```
js/
  main.js          入口与页面级装配
  config.js        CONFIG（含 debug 开关）、log()、全局错误处理
  core/            无业务依赖的工具（dom.js: escapeHtml / escapeAttr / byId）
  data/            纯数据：职业表、专精注册表、天梯排名、图表配色
  components/      可复用 UI：TierList、Chart、RankingNav、Header、Footer、Nav
  modules/         页面级控制器：统计、WCL、画廊、灯箱、粒子
```

依赖方向：`modules` → `components` → `data` / `core`；`data` 不得反向依赖其他层。

## 3. 渲染约定

### 3.1 转义

所有把数据拼进 HTML 的位置都走 `escapeHtml` / `escapeAttr`。当前数据源可信度较高，但 `page_data.json` 与 Cloudinary 返回内容属于外部输入，必须转义。

### 3.2 颜色

职业颜色的唯一来源是 `css/variables.css`：

```css
:root { --class-paladin: #F48CBA; /* ... */ }
```

JS 侧需要十六进制值时调用 `js/data/wow-classes.js#resolveClassColor(className)`，它从 CSS 变量解析并按职业缓存。不要再在 JS 里维护 `{'圣骑士': '#F48CBA', ...}` 这类色表——历史上存在过 5 份副本。

### 3.3 样式归属

| 样式 | 位置 |
|---|---|
| 变量与基础 | `variables.css` / `base.css` |
| 布局与卡片 | `layout.css` / `components.css` |
| 导航 | `navigation.css` |
| 统计图表 | `stats.css` |
| 职业天梯 | `tier-list.css` |
| 排名页快捷导航 | `ranking-nav.css` |
| 攻略页（H6/H7） | `strategy.css` |
| 工具类与响应式 | `utilities.css` / `media.css` / `animations.css` |

`main.css` 只做 `@import` 组合。JS 不负责样式注入。

### 3.4 天梯数据

- `js/data/specs.js`：专精注册表，key 形如 `paladin|防护`，值为 `{ class, spec, icon }`
- `js/data/*-tier-list.js`：只保存层级与 id 列表，例如 `S: { specs: ['paladin|防护'] }`
- `js/components/TierList.js`：渲染，颜色取自 `resolveClassColor`

新增一个专精时只改 `specs.js`，6 份天梯文件共享同一份图标定义。

## 4. 数据流

```
Blizzard API ──tools/mounts_crawler.py──▶ SQLite(data/guild_database.db)
                                              │
                                              └──tools/build_page_data.py──▶ data/page_data.json
                                                                                    │
首页 GuildStatsLoader ──fetch──▶ data/page_data.json ◀──────────────────────────────┘

WarcraftLogs ──netlify/functions/wcl-proxy.js──▶ pages/wcl.html
Cloudinary   ──handle-upload.js / get-images.js──▶ pages/gallery.html
```

`page_data.json` 的字段契约见 [DATA_PIPELINE.md](DATA_PIPELINE.md#输出结构)。

## 5. 取舍与已知限制

| 决策 | 原因 | 代价 |
|---|---|---|
| 不引入框架/构建链 | 站点仅 8 个页面，构建链维护成本高于收益 | 无组件化、无 tree-shaking、依赖靠浏览器原生 ESM |
| Netlify Functions 用 CommonJS | Netlify 默认打包方式，`package.json` 未设 `type: module` | 不能直接复用前端 ESM 模块 |
| `page_data.json` 随仓库分发 | 无需运行时后端，首屏快 | 数据新鲜度依赖手动重跑管道 |
| 静态 HTML 无模板引擎 | 页面少、改动少 | 重复的 `<head>` 需要手工保持一致 |

## 6. 后续可做

1. **CSP**：目前未启用。页面含内联 module script 与 B 站 iframe，需先梳理白名单，并考虑给内联脚本加 nonce 或外链化。
2. **图片优化**：`img/` 共 21 MB，两个 GIF 各 3.8 MB；可转 WebM/WebP 并按需加载。
3. **数据自动化**：把 `tools/build_page_data.py` 放进 CI（定时任务），配合 `validate.py --strict` 防止数据长期停滞。
4. **视觉回归**：页面无自动化测试，改动 CSS 后依赖人工核对。
