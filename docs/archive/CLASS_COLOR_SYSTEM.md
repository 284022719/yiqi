# 魔兽世界职业颜色系统

## 概述

本项目实现了完整的魔兽世界职业颜色系统，严格遵循官方标准颜色值，提供了CSS变量、工具类和JavaScript API，方便在网站的任何位置一致地应用职业颜色。

## 官方颜色标准

| 职业 | 颜色值 | 中文名 |
|------|--------|--------|
| Death Knight | #C41E3A | 死亡骑士 |
| Demon Hunter | #A330C9 | 恶魔猎手 |
| Druid | #FF7C0A | 德鲁伊 |
| Evoker | #33937F | 唤魔师 |
| Hunter | #AAD372 | 猎人 |
| Mage | #3FC7EB | 法师 |
| Monk | #00FF98 | 武僧 |
| Paladin | #F48CBA | 圣骑士 |
| Priest | #FFFFFF | 牧师 |
| Rogue | #FFF468 | 潜行者 |
| Shaman | #0070DD | 萨满 |
| Warlock | #8788EE | 术士 |
| Warrior | #C69B6D | 战士 |

## 文件结构

```
css/
├── variables.css          # CSS变量定义
├── utilities.css          # 工具类
└── main.css              # 主样式文件（导入所有模块）

js/
├── data/
│   └── wow-classes.js     # 职业数据定义
├── components/
│   ├── ClassIcon.js       # 职业图标组件
│   └── ClassColorPalette.js # 颜色预览组件
└── modules/
    └── GuildStatsLoader.js # 公会数据加载器（已更新）

pages/
└── class-colors.html      # 职业颜色预览页面
```

## 使用方法

### 1. CSS 变量使用

```css
/* 直接使用CSS变量 */
.character-name {
  color: var(--class-warrior); /* 战士颜色 */
}

.character-card {
  background-color: var(--class-paladin); /* 圣骑士背景 */
  color: var(--class-text-dark); /* 深色文本 */
}

/* 文本颜色变量 */
.text-light { color: var(--class-text-light); }
.text-dark { color: var(--class-text-dark); }
```

### 2. 工具类使用

```html
<!-- 背景颜色 -->
<div class="class-color-warrior">战士背景</div>
<div class="class-color-paladin">圣骑士背景</div>

<!-- 文本颜色 -->
<span class="class-text-mage">法师文字</span>
<span class="class-text-rogue">潜行者文字</span>

<!-- 边框颜色 -->
<div class="class-border-shaman">萨满边框</div>

<!-- 发光效果 -->
<div class="class-glow-warlock">术士发光</div>
```

### 3. JavaScript API

```javascript
import { 
  getClassInfo, 
  getClassColor, 
  getClassIcon, 
  getClassEmoji,
  getTextColor 
} from './js/data/wow-classes.js';

// 获取职业信息
const classInfo = getClassInfo('warrior');
console.log(classInfo);
// {
//   id: 1,
//   name: "战士",
//   slug: "warrior",
//   color: "var(--class-warrior)",
//   textColor: "var(--class-text-light)"
// }

// 获取职业颜色
const color = getClassColor('warrior');
console.log(color); // "var(--class-warrior)"

// 获取职业图标
const icon = getClassIcon('warrior');
console.log(icon); // 图标URL

// 获取职业表情符号
const emoji = getClassEmoji('warrior');
console.log(emoji); // "⚔️"

// 获取文本颜色（根据背景色自动选择）
const textColor = getTextColor('var(--class-warrior)');
console.log(textColor); // "var(--class-text-light)"
```

### 4. 职业图标组件

```javascript
import ClassIcon from './js/components/ClassIcon.js';

// 创建职业图标
const icon = new ClassIcon('warrior', {
  size: 48,
  showText: true,
  showBorder: true,
  isInteractive: true
});

// 渲染到容器
icon.render(document.getElementById('icon-container'));
```

### 5. 颜色预览组件

```javascript
import ClassColorPalette from './js/components/ClassColorPalette.js';

// 创建颜色预览
new ClassColorPalette('color-palette');
```

## 在排行榜中的应用

系统已更新 `GuildStatsLoader.js`，在排行榜中自动应用职业颜色：

```javascript
// 自动应用职业颜色和文本颜色
const classInfo = getClassInfo(item.class);
const classColor = classInfo ? classInfo.color : 'var(--color-text)';
const textColor = classInfo ? classInfo.textColor : 'var(--color-text)';

// 在HTML中使用
<span class="class-icon" style="background: ${classColor}; color: ${textColor};">
  ${getClassIcon(item.class)}
</span>
```

## 职业主题系统

系统提供了完整的职业主题支持：

```css
/* 战士主题 */
.theme-warrior {
  --primary: var(--class-warrior);
  --secondary: #E0C9AC;
  --text: var(--class-text-light);
}

/* 圣骑士主题 */
.theme-paladin {
  --primary: var(--class-paladin);
  --secondary: #F0F0F0;
  --text: var(--class-text-dark);
}
```

## 响应式设计

系统支持响应式设计，在不同设备上都能正常显示：

```css
/* 移动端优化 */
@media (max-width: 768px) {
  .color-palette {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
```

## 深色模式支持

系统自动适配深色模式：

```css
@media (prefers-color-scheme: dark) {
  :root {
    --class-priest: #E0E0E0; /* 调整白色 */
    --class-text-dark: #F5F5F5;
  }
}
```

## 性能优化

- 使用CSS变量减少重复代码
- 工具类提供快速应用方式
- 组件化设计提高复用性
- 自动文本颜色计算确保可读性

## 浏览器兼容性

- 现代浏览器：完全支持
- IE11+：部分支持（需要polyfill）
- 移动端：完全支持

## 使用示例

访问 `pages/class-colors.html` 查看完整的颜色预览和使用示例。

## 最佳实践

1. **一致性**：在整个网站中使用相同的颜色定义
2. **可读性**：自动计算文本颜色确保对比度
3. **主题化**：使用职业主题创建沉浸式体验
4. **响应式**：确保在所有设备上正常显示
5. **性能**：合理使用工具类和组件

## 扩展性

系统设计为可扩展的，可以轻松添加：
- 新的职业颜色
- 自定义主题
- 动画效果
- 交互功能

## 维护

- 颜色值严格遵循官方标准
- 定期检查官方颜色更新
- 保持文档和代码同步
- 测试所有使用场景 