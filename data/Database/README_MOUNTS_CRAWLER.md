# 魔兽世界坐骑数据爬虫使用说明

## 概述

这个爬虫系统用于自动获取数据库中每个角色的坐骑数量信息，使用魔兽世界中国服务器的官方API。

## 文件结构

```
data/Database/
├── mounts_crawler.py      # 主爬虫脚本
├── test_mounts_api.py     # API测试脚本
├── config.py              # 配置文件管理
├── config.json            # 配置文件（自动生成）
├── database_manager.py    # 数据库管理
└── README_MOUNTS_CRAWLER.md  # 本说明文档
```

## 快速开始

### 1. 环境准备

确保已安装必要的Python包：

```bash
pip install requests sqlite3
```

### 2. 配置API令牌

编辑 `config.json` 文件，设置您的API令牌：

```json
{
  "tokens": {
    "default": "your_api_token_here",
    "characters": {
      "角色名-服务器": "specific_token_here"
    }
  }
}
```

### 3. 测试API连接

运行测试脚本验证API是否正常工作：

```bash
cd data/Database
python test_mounts_api.py
```

### 4. 运行爬虫

```bash
cd data/Database
python mounts_crawler.py
```

## 详细配置

### 配置文件说明

`config.json` 包含以下配置项：

```json
{
  "api": {
    "base_url": "https://webapi.blizzard.cn/wow-armory-server/api/do",
    "headers": {
      "accept": "application/json, text/javascript, */*; q=0.01",
      "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
      "priority": "u=1, i",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-site",
      "xcxtoken": "",
      "referer": "https://wow.blizzard.cn/"
    },
    "timeout": 30,
    "max_retries": 3
  },
  "crawler": {
    "delay_between_requests": 2,
    "batch_size": 10,
    "max_concurrent": 1
  },
  "database": {
    "path": "../guild_database.db",
    "backup_before_update": true
  },
  "logging": {
    "level": "INFO",
    "file": "logs/mounts_crawler.log",
    "max_size": "10MB",
    "backup_count": 5
  },
  "tokens": {
    "default": "your_default_token",
    "characters": {}
  }
}
```

### 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `api.base_url` | API基础地址 | 魔兽世界中国服务器API |
| `api.timeout` | 请求超时时间（秒） | 30 |
| `api.max_retries` | 最大重试次数 | 3 |
| `crawler.delay_between_requests` | 请求间隔（秒） | 2 |
| `database.path` | 数据库文件路径 | ../guild_database.db |
| `logging.level` | 日志级别 | INFO |

## 使用方法

### 基本使用

```python
from mounts_crawler import MountsCrawler

# 创建爬虫实例
crawler = MountsCrawler()

# 爬取所有角色的坐骑数据
success = crawler.crawl_all_characters()

# 导出报告
if success:
    report_file = crawler.export_mounts_report()
    print(f"报告已保存到: {report_file}")
```

### 高级使用

```python
from mounts_crawler import MountsCrawler
from config import config

# 自定义配置
config.set("crawler.delay_between_requests", 1)  # 减少请求间隔
config.set("api.timeout", 60)  # 增加超时时间

# 创建爬虫实例
crawler = MountsCrawler()

# 获取特定角色的坐骑数据
character = {
    "name": "角色名",
    "realm_slug": "服务器",
    "faction": "HORDE"
}
success = crawler.crawl_character_mounts(character)
```

## 数据库结构

爬虫会在 `guild_characters` 表中添加以下字段：

- `mounts_now`: 当前拥有的坐骑数量
- `mounts_total`: 总坐骑数量

### 查看坐骑数据

```python
from database_manager import GuildDatabaseManager

db_manager = GuildDatabaseManager()
characters = db_manager.get_all_characters()

for character in characters:
    print(f"{character['name']}: {character['mounts_now']}/{character['mounts_total']} 坐骑")
```

## 输出文件

### 日志文件

- `logs/mounts_crawler.log`: 爬虫运行日志

### 报告文件

- `mounts_report_YYYYMMDD_HHMMSS.json`: 坐骑数据报告

报告文件包含：
- 爬取统计信息
- 所有角色的坐骑数据
- 按坐骑数量排序的角色列表

## 错误处理

### 常见错误及解决方案

1. **令牌无效**
   ```
   错误: API返回错误: 令牌无效
   解决: 检查config.json中的令牌是否正确
   ```

2. **网络超时**
   ```
   错误: 请求超时
   解决: 增加api.timeout配置值，检查网络连接
   ```

3. **数据库连接失败**
   ```
   错误: 数据库文件不存在
   解决: 确保数据库文件路径正确，先运行其他爬虫获取角色数据
   ```

### 重试机制

爬虫内置重试机制：
- 网络错误自动重试
- 可配置最大重试次数
- 重试间隔递增

## 性能优化

### 提高爬取速度

1. 减少请求间隔：
   ```json
   {
     "crawler": {
       "delay_between_requests": 1
     }
   }
   ```

2. 增加并发数（需要修改代码）：
   ```json
   {
     "crawler": {
       "max_concurrent": 3
     }
   }
   ```

### 降低服务器压力

1. 增加请求间隔：
   ```json
   {
     "crawler": {
       "delay_between_requests": 5
     }
   }
   ```

2. 分批处理：
   ```json
   {
     "crawler": {
       "batch_size": 5
     }
   }
   ```

## 监控和维护

### 查看运行状态

```bash
# 查看最新日志
tail -f logs/mounts_crawler.log

# 查看数据库中的坐骑数据
python -c "
from database_manager import GuildDatabaseManager
db = GuildDatabaseManager()
stats = db.get_mounts_statistics()
print(f'总角色数: {stats[\"total_characters\"]}')
print(f'平均坐骑数: {stats[\"average_mounts\"]:.1f}')
"
```

### 定期维护

1. **清理日志文件**：定期清理过大的日志文件
2. **备份数据库**：重要数据更新前备份数据库
3. **更新令牌**：定期更新API令牌

## 故障排除

### 调试模式

设置日志级别为DEBUG：

```json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

### 测试单个角色

```python
from mounts_crawler import MountsCrawler

crawler = MountsCrawler()
character = {"name": "测试角色", "realm_slug": "测试服务器", "faction": "HORDE"}
result = crawler.crawl_character_mounts(character)
print(f"爬取结果: {result}")
```

## 注意事项

1. **API限制**：遵守暴雪API的使用条款和频率限制
2. **数据准确性**：坐骑数据可能有延迟，建议定期更新
3. **令牌安全**：不要将API令牌提交到版本控制系统
4. **网络环境**：确保网络连接稳定，建议使用稳定的网络环境

## 更新日志

- **v1.0** - 初始版本，支持基本的坐骑数据爬取
- 支持联盟和部落阵营
- 自动重试机制
- 详细的日志记录
- 配置文件管理

---

如有问题，请查看日志文件或联系开发者。 