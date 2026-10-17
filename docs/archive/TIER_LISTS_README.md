# 职业层级排名功能

## 功能概述

本功能基于 [Wowhead](https://www.wowhead.com/cn/guide/classes/tier-lists/) 的排名数据，在公会网站中展示魔兽世界各职业专精的层级排名，包括团本和大秘境两种场景的DPS、治疗和坦克三种类型。

## 数据来源

### 团本排名

#### DPS排名
- **来源**: [DPS Rankings for Manaforge Omega Raid](https://www.wowhead.com/cn/guide/classes/tier-lists/dps-rankings-raids)
- **作者**: Dratnos
- **更新时间**: 2025/08/09

#### 治疗排名
- **来源**: [Healer Rankings for Manaforge Omega Raid](https://www.wowhead.com/cn/guide/classes/tier-lists/healer-rankings-raids)
- **作者**: korimae
- **更新时间**: 2025/07/29

#### 坦克排名
- **来源**: [Tank Rankings for Manaforge Omega Raid](https://www.wowhead.com/cn/guide/classes/tier-lists/tank-rankings-raids)
- **作者**: Dratnos
- **更新时间**: 2025/08/09

### 大秘境排名

#### DPS排名
- **来源**: [大秘境DPS Rankings](https://www.wowhead.com/cn/guide/classes/tier-lists/dps-rankings-mythic-plus)
- **作者**: tettles
- **更新时间**: 2025/08/03

#### 治疗排名
- **来源**: [大秘境Healer Rankings](https://www.wowhead.com/cn/guide/classes/tier-lists/healer-rankings-mythic-plus)
- **作者**: AutomaticJak
- **更新时间**: 2025/07/29

#### 坦克排名
- **来源**: [大秘境Tank Rankings](https://www.wowhead.com/cn/guide/classes/tier-lists/tank-rankings-mythic-plus)
- **作者**: YoDaTV
- **更新时间**: 2025/07/29

## 文件结构

```
js/
├── data/
│   ├── dps-tier-list.js              # 团本DPS排名数据
│   ├── healer-tier-list.js           # 团本治疗排名数据
│   ├── tank-tier-list.js             # 团本坦克排名数据
│   ├── mplus-dps-tier-list.js        # 大秘境DPS排名数据
│   ├── mplus-healer-tier-list.js     # 大秘境治疗排名数据
│   └── mplus-tank-tier-list.js       # 大秘境坦克排名数据
├── modules/
│   ├── DPSTierList.js               # DPS Tier List显示模块
│   └── TierList.js                  # 通用Tier List显示模块
└── main.js                          # 主文件（已更新）

pages/
├── all-rankings.html                # 排名总览页面（团本+大秘境）
├── dps-tier-list.html               # 团本DPS排名页面
├── healer-tier-list.html            # 团本治疗排名页面
├── tank-tier-list.html              # 团本坦克排名页面
├── all-tier-lists.html              # 团本综合排名页面
├── mplus-dps-tier-list.html         # 大秘境DPS排名页面
├── mplus-healer-tier-list.html      # 大秘境治疗排名页面
├── mplus-tank-tier-list.html        # 大秘境坦克排名页面
└── mplus-all-tier-lists.html        # 大秘境综合排名页面

index.html                           # 主页面（已添加DPS排名容器）
```

## 功能特点

### 1. 综合总览
- **排名总览页面**: 在一个页面中展示所有团本和大秘境的排名
- **快速导航**: 提供便捷的跳转按钮，快速定位到特定排名
- **场景区分**: 清晰区分团本和大秘境两种游戏内容

### 2. 层级分类
- **S**: 
- **A**:   
- **B**: 
- **C**: 
- **D**: 较
- **F**: 最

### 3. 显示内容
- 专精图标（使用官方专精技能图标）
- 专精名称（使用职业颜色）
- 职业名称
- 层级标签（使用参考图片中的标准颜色）
- 专精卡片（统一宽度，带有职业底色和左侧边框）

### 4. 交互效果
- 悬停动画效果
- 渐进式加载动画
- 响应式设计
- 平滑滚动跳转

### 5. 数据引用
- 明确标注数据来源
- 链接到原始Wowhead页面
- 显示作者和更新时间

## 使用方法

### 在主页面显示
DPS排名已集成到主页面中，会自动显示在成就点数排行榜之前。

### 访问专门页面
可以通过导航菜单的"职业排名"下拉菜单访问：

#### 综合排名
1. **🎯 排名总览** - 包含所有团本和大秘境的排名

#### 团本排名
1. **🏰 团本综合排名** - 包含所有三种类型的团本排名
2. **⚔️ 团本DPS排名** - 仅显示团本DPS职业排名
3. **💚 团本治疗排名** - 仅显示团本治疗职业排名
4. **🛡️ 团本坦克排名** - 仅显示团本坦克职业排名

#### 大秘境排名
1. **⚡ 大秘境综合排名** - 包含所有三种类型的大秘境排名
2. **⚔️ 大秘境DPS排名** - 仅显示大秘境DPS职业排名
3. **💚 大秘境治疗排名** - 仅显示大秘境治疗职业排名
4. **🛡️ 大秘境坦克排名** - 仅显示大秘境坦克职业排名

### 页面链接
```
# 综合排名
/pages/all-rankings.html                # 排名总览（团本+大秘境）

# 团本排名
/pages/all-tier-lists.html              # 团本综合排名
/pages/dps-tier-list.html               # 团本DPS排名
/pages/healer-tier-list.html            # 团本治疗排名
/pages/tank-tier-list.html              # 团本坦克排名

# 大秘境排名
/pages/mplus-all-tier-lists.html        # 大秘境综合排名
/pages/mplus-dps-tier-list.html         # 大秘境DPS排名
/pages/mplus-healer-tier-list.html      # 大秘境治疗排名
/pages/mplus-tank-tier-list.html        # 大秘境坦克排名
```

## 技术实现

### 模块化设计
- 数据与显示逻辑分离
- 可复用的组件设计
- 易于维护和更新

### 响应式布局
- 支持桌面和移动设备
- 自适应网格布局
- 优化的移动端体验

### 性能优化
- 懒加载图片
- CSS动画优化
- 渐进式渲染

## 更新说明

当Wowhead发布新的排名时，只需要更新对应的数据文件：

### 团本排名
- `js/data/dps-tier-list.js` - 团本DPS排名数据
- `js/data/healer-tier-list.js` - 团本治疗排名数据
- `js/data/tank-tier-list.js` - 团本坦克排名数据

### 大秘境排名
- `js/data/mplus-dps-tier-list.js` - 大秘境DPS排名数据
- `js/data/mplus-healer-tier-list.js` - 大秘境治疗排名数据
- `js/data/mplus-tank-tier-list.js` - 大秘境坦克排名数据

## 层级颜色标准

根据参考图片，各层级的标准颜色为：
- **S Tier**: #FFD700 (金色)
- **A Tier**: #FF6B6B (红色)  
- **B Tier**: #4ECDC4 (青色)
- **C Tier**: #A8E6CF (浅绿色)
- **D Tier**: #FFB6C1 (浅粉色)
- **F Tier**: #D3D3D3 (浅灰色)

## 卡片设计

每个专精卡片具有以下特点：
- **统一宽度**: 200px (桌面端) / 180px (平板) / 160px (手机)
- **职业底色**: 使用对应职业颜色的20%透明度作为背景
- **左侧边框**: 使用对应职业颜色的实线边框
- **悬停效果**: 鼠标悬停时显示金色边框和阴影效果

## 注意事项

1. 团本排名基于团队副本表现，大秘境排名基于大秘境表现，两者可能不同
2. 排名会随游戏版本更新而变化
3. 个人技术水平和装备对实际表现影响很大
4. 建议选择喜欢的职业专精，享受游戏乐趣
5. 数据来源于Wowhead，仅供参考使用
6. 团本和大秘境的职业表现差异较大，请根据具体游戏内容选择合适的职业专精
