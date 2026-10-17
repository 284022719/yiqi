# CSS 结构

`main.css` 只做 `@import` 组合，其余文件按职责拆分：

```
css/
├── main.css          入口，按顺序 @import 下列模块
├── variables.css     CSS 变量（颜色、职业色、间距、圆角）
├── base.css          重置与基础排版
├── layout.css        页面骨架、内容卡片
├── components.css    UI 组件（表格、按钮、表单、状态提示、空状态）
├── navigation.css    顶部下拉导航
├── stats.css         统计卡片、条形图、饼图、图例
├── tier-list.css     职业天梯（TierList 组件）
├── ranking-nav.css   排名页快捷导航
├── utilities.css     工具类与配色预览
├── media.css         模态框、画廊、图片、iframe
├── animations.css    关键帧动画
└── README.md         本说明
```

导入顺序（见 `main.css`）：变量 → 基础 → 布局/组件 → 工具类 → 响应式 → 动画。

## 约定

1. **职业颜色的唯一来源**是 `variables.css` 的 `--class-*`；JS 通过 `resolveClassColor()` 读取，不要在两处各写一份。
2. 组件样式跟组件走：`TierList` → `tier-list.css`，`RankingNav` → `ranking-nav.css`。
3. 新增页面级样式优先复用已有变量（`--spacing-*`、`--border-radius`、`--color-*`）。
4. 响应式断点统一为 `768px` 与 `480px`。
5. 动画需在 `prefers-reduced-motion: reduce` 下退化（见 `tier-list.css` 末尾）。

整体设计说明见 [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)。
