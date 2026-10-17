# CSS 结构

`main.css` 只做 `@import` 组合，其余文件按职责拆分：

```
css/
├── main.css          入口，按顺序 @import 下列模块
├── variables.css     设计 token（颜色、间距、字号、圆角、阴影、渐变）
├── base.css          重置与基础排版
├── layout.css        页面骨架、内容卡片
├── components.css    UI 组件（表格、按钮、表单、上传、状态提示、空状态）
├── navigation.css    顶部导航（含移动端折叠与下拉）
├── stats.css         统计卡片、条形图、饼图、图例
├── tier-list.css     职业天梯（TierList 组件）
├── ranking-nav.css   排名页快捷导航
├── strategy.css      攻略页（H6/H7）
├── utilities.css     工具类与配色预览
├── media.css         模态框、画廊、图片、iframe
├── animations.css    关键帧动画
└── README.md         本说明
```

导入顺序（见 `main.css`）：变量 → 基础 → 布局/组件 → 工具类 → 响应式 → 动画。

## 约定

1. **所有设计 token 只在 `variables.css` 定义**，命名前缀固定为：`--color-*` / `--class-*` / `--tier-*` / `--space-*` / `--text-*` / `--radius-*` / `--shadow-*` / `--gradient-*` / `--transition-*` / `--border-*`。其他文件不再写裸 hex，也不再出现 `--spacing-*`、`--border-radius` 这类旧别名。
2. **刻度允许有空槽**：`--space-xs`、`--space-2xl`、`--text-*` 等暂时没被引用的槽位是留给后续统一的刻度，不算死代码；新增样式优先从刻度取值，而不是随手写 `1.3rem`。
3. **职业颜色的唯一来源**是 `variables.css` 的 `--class-*`；JS 通过 `resolveClassColor()` 读取，不要在两处各写一份。
4. **同值不同义不要合并**：`--color-primary` 与 `--tier-s` 同为金色，但“改品牌色”和“改 S 档颜色”是两件事，各留一个 token。
5. 组件样式跟组件走：`TierList` → `tier-list.css`，`RankingNav` → `ranking-nav.css`，攻略页 → `strategy.css`。
6. 响应式断点统一为 `768px` 与 `480px`。
7. 动画需在 `prefers-reduced-motion: reduce` 下退化（见 `tier-list.css` 末尾）。

整体设计说明见 [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)。
