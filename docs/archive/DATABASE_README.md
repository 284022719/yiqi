# 数据库模块说明

## 概述

本模块负责管理公会角色数据的存储、查询和前端数据生成。

## 文件结构

```
data/Database/
├── database_manager.py      # 数据库管理器
├── database_query_tool.py   # 数据库查询工具
├── generate_page_data.py    # 页面数据生成器
├── update_page_data.py      # 自动更新脚本
├── delete_tables.py         # 数据库清理工具
└── README.md               # 本文件
```

## 数据流程

### 1. 数据采集
- 爬虫脚本从魔兽世界API获取角色数据
- 数据保存到 `guild_database.db` 数据库

### 2. 数据存储
- `guild_characters` 表：存储角色基础信息
- `character_equipment` 表：存储装备信息
- `character_mounts` 表：存储坐骑信息
- `character_achievements` 表：存储成就信息

### 3. 数据转换
- `generate_page_data.py` 从数据库读取数据
- 生成 `data/page_data.json` 供前端使用

### 4. 前端展示
- `index.html` 通过 `GuildStatsLoader.js` 加载 `page_data.json`
- 展示公会统计、图表和排行榜

## 使用方法

### 手动更新页面数据

```bash
# 生成页面数据
python data/Database/generate_page_data.py

# 或者使用自动更新脚本
python data/Database/update_page_data.py
```

### 查询数据库

```bash
# 使用查询工具
python data/Database/database_query_tool.py
```

### 数据库管理

```bash
# 查看数据库信息
python data/Database/database_query_tool.py

# 清理数据库（谨慎使用）
python data/Database/delete_tables.py
```

## 自动化流程

### 爬虫完成后自动更新

当运行 `crawler/wow_database_crawler.py` 时，爬虫完成后会自动：

1. 保存数据到数据库
2. 生成统计报告
3. 自动运行 `update_page_data.py`
4. 更新 `page_data.json`

### 数据同步

- 爬虫更新数据库 ✅
- 数据库生成JSON ✅
- 前端加载JSON ✅
- 页面显示最新数据 ✅

## 数据格式

### 数据库表结构

#### guild_characters
```sql
CREATE TABLE guild_characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    class TEXT,
    level INTEGER,
    achievement_points INTEGER,
    average_item_level REAL,
    faction TEXT,
    realm TEXT,
    spec TEXT,
    guild TEXT
);
```



### page_data.json 格式

```json
{
  "lastUpdated": "2025-08-05 21:22:58",
  "stats": {
    "totalMembers": 965,
    "activeMembers": 702,
    "dataCompleteness": {
      "total": 965,
      "complete": 702,
      "incomplete": 263,
      "percentage": 72.7
    }
  },
  "charts": {
    "classDistribution": [...],
    "activityDistribution": [...],
    "factionDistribution": [...],
    "realmDistribution": [...]
  },
  "rankings": {
    "achievementRanking": [...],
    "itemLevelRanking": [...]
  }
}
```

## 注意事项

1. **数据一致性**：确保爬虫和数据库使用相同的角色列表
2. **更新频率**：建议定期运行爬虫更新数据
3. **备份**：重要数据建议定期备份
4. **权限**：确保脚本有读写数据库和文件的权限

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库文件是否存在
   - 检查文件权限

2. **页面数据生成失败**
   - 检查数据库是否有数据
   - 检查JSON文件写入权限

3. **前端数据不更新**
   - 确认 `page_data.json` 已更新
   - 清除浏览器缓存
   - 检查网络请求

### 日志查看

```bash
# 查看数据库日志
tail -f logs/database.log

# 查看爬虫日志
tail -f logs/wow_database_crawler_*.log
```

## 扩展功能

### 添加新的统计维度

1. 在 `generate_page_data.py` 中添加新的统计函数
2. 更新 `page_data.json` 格式
3. 在前端添加对应的展示组件

### 添加新的数据源

1. 创建新的爬虫脚本
2. 在 `database_manager.py` 中添加数据保存方法
3. 更新数据生成逻辑

## 技术支持

如有问题，请检查：
1. 日志文件中的错误信息
2. 数据库连接状态
3. 文件权限设置
4. 网络连接状态 