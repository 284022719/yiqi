# 魔兽世界公会成员信息获取API文档

## 概述

本API文档描述了如何使用魔兽世界角色信息API批量获取公会成员的详细信息，包括装备等级、成就点数、专精等数据。

## 功能特性

- 批量获取公会成员详细信息
- 支持CSV文件导入公会成员列表
- 自动处理角色名称编码
- 完整的错误处理和重试机制
- 数据缓存和性能优化
- 多种输出格式支持

## 核心组件

### WoWCharacterAPI 类

主要的API客户端类，负责与魔兽世界角色信息API的交互。

#### 初始化

```python
api_client = WoWCharacterAPI(cookie_token)
```

**参数**:
- `cookie_token` (str): blizzard_user_info cookie值

#### 主要方法

##### get_character_info(realm_slug, character_name)

获取单个角色的详细信息。

**参数**:
- `realm_slug` (str): 服务器标识符
- `character_name` (str): 角色名称

**返回**:
- `Dict` 或 `None`: 角色信息字典，失败时返回None

**示例**:
```python
character_info = api_client.get_character_info("arthas", "快来骑我吧")
if character_info:
    print(f"角色等级: {character_info['character_summary']['level']}")
    print(f"装备等级: {character_info['character_summary']['average_item_level']}")
```

## 数据处理函数

### load_guild_members(csv_file, limit)

从CSV文件加载公会成员基本信息。

**参数**:
- `csv_file` (str): CSV文件路径
- `limit` (int): 限制返回的成员数量

**返回**:
- `List[Dict]`: 公会成员列表

**CSV文件格式**:
```csv
name,rank,level,class,race,sex,last_online,faction
快来骑我吧,暗索高级特工,80,唤魔师,龙希尔,Female,0.02,Horde
```

### get_detailed_member_info(api_client, members, realm_slug)

批量获取公会成员的详细信息。

**参数**:
- `api_client` (WoWCharacterAPI): API客户端实例
- `members` (List[Dict]): 公会成员列表
- `realm_slug` (str): 服务器标识符

**返回**:
- `List[Dict]`: 包含详细信息的公会成员列表

### save_results(members, output_file)

保存结果到JSON文件。

**参数**:
- `members` (List[Dict]): 公会成员数据
- `output_file` (str): 输出文件路径

## 配置参数

### 主要配置

```python
# 文件路径配置
CSV_FILE = "data/guildmember.csv"              # 公会成员CSV文件
OUTPUT_FILE = "guild_members_detailed.json"    # 输出文件

# API配置
REALM_SLUG = "arthas"                          # 服务器标识符
MEMBER_LIMIT = 10                              # 获取成员数量限制

# 请求配置
REQUEST_TIMEOUT = 10                           # 请求超时时间(秒)
REQUEST_DELAY = 1                              # 请求间隔时间(秒)
```

### 请求头配置

```python
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://wow.blizzard.cn',
    'referer': 'https://wow.blizzard.cn/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}
```

## 使用示例

### 完整使用流程

```python
from get_guild_members_info import WoWCharacterAPI, load_guild_members, get_detailed_member_info, save_results

def main():
    # 1. 初始化API客户端
    cookie_token = "YOUR_COOKIE_TOKEN_HERE"
    api_client = WoWCharacterAPI(cookie_token)
    
    # 2. 加载公会成员列表
    members = load_guild_members("data/guildmember.csv", limit=10)
    print(f"加载了 {len(members)} 个公会成员")
    
    # 3. 获取详细信息
    detailed_members = get_detailed_member_info(api_client, members, "arthas")
    
    # 4. 保存结果
    save_results(detailed_members, "guild_members_detailed.json")
    
    # 5. 打印摘要
    print_summary(detailed_members)

if __name__ == "__main__":
    main()
```

### 快速启动脚本

使用 `run_guild_tool.py` 快速启动：

```bash
python run_guild_tool.py
```

**功能菜单**:
1. 测试API连接
2. 获取公会成员详细信息
3. 查看使用说明
4. 退出程序

## 输出格式

### JSON输出示例

```json
[
  {
    "name": "快来骑我吧",
    "rank": "暗索高级特工",
    "level": "80",
    "class": "唤魔师",
    "race": "龙希尔",
    "sex": "Female",
    "last_online": "0.02",
    "faction": "Horde",
    "detailed_info": {
      "character_summary": {
        "name": "快来骑我吧",
        "level": 80,
        "average_item_level": 676,
        "equipped_item_level": 675,
        "achievement_points": 19840,
        "active_spec": {
          "name": "湮灭"
        },
        "guild": {
          "name": "一起"
        },
        "last_login_timestamp": 1753980571000,
        "covenant_progress": {
          "chosen_covenant": {
            "name": "通灵领主"
          },
          "renown_level": 23
        }
      },
      "list": [
        "equipment",
        "statistics",
        "specializations",
        "raids",
        "pvp_summary",
        "pvp",
        "mythic_keystone_season",
        "default_specializations",
        "default_journal_expansion_index",
        "pets",
        "mounts",
        "hunter_pets",
        "default_journal_expansion_index_v2",
        "mythic-keystone/dungeon",
        "journal-instance",
        "achievement_category_index",
        "achievement_category_detail",
        "character_achievement",
        "item_detail",
        "reputations",
        "achievement_detail"
      ],
      "token": "9326f8a8f1b1c11ecd5c1dc3df050da7",
      "encounters_json": "https://wow.res.netease.com/xt/manage/20250425/d6dcd2ae86ca7cf553bb96bbb7c8bfdd_1745553229269.json",
      "achievement_category_json": "https://wow.res.netease.com/images/20250605/1749093082272_bc9cf35dbb.json"
    }
  }
]
```

## 获取的数据类型

### 基本信息 (来自CSV)
- 角色名称
- 公会职位
- 等级
- 职业
- 种族
- 性别
- 最后在线时间
- 阵营

### 详细信息 (来自API)
- 平均装备等级
- 已装备装备等级
- 成就点数
- 当前专精
- 公会信息
- 最后登录时间戳
- 盟约进度
- 称号信息
- 可用数据模块列表
- 访问令牌
- 外部数据链接

## 错误处理

### 网络错误
- 请求超时处理
- 连接失败重试
- 网络异常提示

### API错误
- 认证失败处理
- 角色不存在处理
- 权限不足处理

### 数据错误
- CSV文件格式验证
- JSON解析错误处理
- 编码问题处理

## 性能优化

### 请求优化
- 会话复用
- 请求间隔控制
- 超时设置

### 内存优化
- 流式处理
- 及时释放资源
- 批量处理

## 安全考虑

### 认证安全
- Cookie token验证
- 请求头完整性
- 域名限制

### 数据安全
- 本地文件存储
- 敏感信息保护
- 错误信息脱敏

## 扩展功能

### 数据分析
```python
def analyze_guild_data(members):
    """分析公会数据"""
    total_members = len(members)
    avg_item_level = sum(m['detailed_info']['character_summary']['average_item_level'] 
                        for m in members if m.get('detailed_info')) / total_members
    
    class_distribution = {}
    for member in members:
        class_name = member['class']
        class_distribution[class_name] = class_distribution.get(class_name, 0) + 1
    
    return {
        'total_members': total_members,
        'average_item_level': avg_item_level,
        'class_distribution': class_distribution
    }
```

### 数据导出
```python
def export_to_csv(members, output_file):
    """导出为CSV格式"""
    import csv
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'rank', 'level', 'class', 'item_level', 'achievement_points'])
        
        for member in members:
            detailed = member.get('detailed_info', {}).get('character_summary', {})
            writer.writerow([
                member['name'],
                member['rank'],
                member['level'],
                member['class'],
                detailed.get('average_item_level', 0),
                detailed.get('achievement_points', 0)
            ])
```

## 常见问题

### Q: 如何获取Cookie Token？
A: 
1. 访问 https://wow.blizzard.cn/
2. 登录你的账号
3. 打开浏览器开发者工具 (F12)
4. 在Network标签页中找到任意请求
5. 复制 `blizzard_user_info` cookie的值

### Q: CSV文件格式要求？
A: CSV文件应包含以下列：
- name: 角色名称
- rank: 公会职位
- level: 等级
- class: 职业
- race: 种族
- sex: 性别
- last_online: 最后在线时间
- faction: 阵营

### Q: 如何处理大量公会成员？
A: 
1. 使用 `MEMBER_LIMIT` 参数限制处理数量
2. 增加 `REQUEST_DELAY` 避免请求过于频繁
3. 实现数据缓存机制
4. 分批处理数据

### Q: API请求失败怎么办？
A: 
1. 检查Cookie Token是否有效
2. 确认网络连接正常
3. 验证角色名称和服务器名称
4. 查看错误日志获取详细信息

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基础角色信息获取
- 完整的错误处理机制
- 用户友好的界面

### 计划功能
- 支持更多服务器
- 添加数据分析功能
- 支持导出更多格式
- 添加图形界面

## 许可证

本项目仅供学习和研究使用，请遵守魔兽世界官方服务条款。

## 技术支持

如有问题或建议，请通过以下方式联系：
- 项目仓库：GitHub
- 邮箱：support@example.com

---

**注意**: 使用本工具时请确保遵守魔兽世界官方服务条款和相关法律法规。 