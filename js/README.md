# JavaScript 结构

```text
js/
├── main.js          入口：加载 Header/导航/Footer，按页面元素条件初始化模块
├── config.js        CONFIG（含 debug 开关）、log()、全局错误处理
├── core/
│   ├── dom.js       escapeHtml / escapeAttr / byId
│   └── icons.js     内联 SVG 图标集（sword/heart/shield/castle/bolt/trophy/key/tv）
├── data/
│   ├── wow-classes.js      13 个职业的名称、slug、图标；resolveClassColor 解析 CSS 变量
│   ├── specs.js            专精注册表（class + spec + icon），key 形如 'paladin|防护'
│   ├── palettes.js         图表配色（种族/服务器/阵营/性别）
│   ├── dps-tier-list.js    团本 DPS 排名（只存专精 id）
│   ├── healer-tier-list.js 团本治疗
│   ├── tank-tier-list.js   团本坦克
│   └── mplus-*.js          大秘境三系
├── pages/
│   ├── all-rankings.js  排名总览页装配（6 个 TierList）
│   └── class-colors.js  配色预览页装配
├── components/
│   ├── TierList.js         天梯渲染（样式见 css/tier-list.css）
│   ├── Chart.js            renderBarChart / renderPieChart
│   ├── ranking-nav.js      排名页快捷跳转（样式见 css/ranking-nav.css）
│   ├── ClassColorPalette.js
│   ├── header.js / nav.js / footer.js
└── modules/
    ├── GuildStatsLoader.js 首页统计（取数 + 交给 Chart 渲染）
    ├── WCLDataLoader.js    WarcraftLogs 表格
    ├── ImageUploader.js    画廊上传与加载
    ├── ImageModal.js       图片灯箱
    ├── IframeErrorHandler.js
    └── ParticleSystem.js   背景粒子
```

## 约定

1. 拼接 HTML 必须转义：`import { escapeHtml, escapeAttr } from '../core/dom.js'`。
2. 调试输出用 `log()`（`js/config.js`），默认静默；不要留 `console.log`。
3. 职业颜色不要新增色表：用 `resolveClassColor(className)`，颜色定义在 `css/variables.css`。
4. 天梯专精图标改 `data/specs.js`；天梯层级**不要手改** `data/*-tier-list.js`（由 `tools/fetch_tier_lists.py` 生成）。
5. 样式属于 `css/`，JS 里不要 `createElement('style')`。

架构与数据流详见 [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)。
