# 魔兽世界角色信息API文档

## 概述

魔兽世界角色信息API提供了获取游戏角色详细信息的接口，包括角色基本信息、装备、成就、公会、副本进度、PVP数据、收集品等全面的游戏数据。

## 基本信息

- **基础URL**: `https://webapi.blizzard.cn/wow-armory-server/api/index`
- **请求方法**: GET
- **内容类型**: application/json
- **认证方式**: Cookie认证 (blizzard_user_info)

## 请求参数

### 查询参数

| 参数名 | 类型 | 必需 | 描述 | 示例 |
|--------|------|------|------|------|
| realm_slug | string | 是 | 服务器标识符 | arthas |
| role_name | string | 是 | 角色名称（URL编码） | %E5%BF%AB%E6%9D%A5%E9%AA%91%E6%88%91%E5%90%A7 |

### 请求头

| 头部名称 | 值 | 描述 |
|----------|-----|------|
| accept | application/json, text/javascript, */*; q=0.01 | 接受的内容类型 |
| accept-language | zh-CN,zh;q=0.9 | 语言偏好 |
| origin | https://wow.blizzard.cn | 请求来源 |
| referer | https://wow.blizzard.cn/ | 引用页面 |
| cookie | blizzard_user_info=... | 用户认证信息 |

## 响应格式

### 成功响应

```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "character_summary": {
      "name": "角色名称",
      "gender": {
        "type": "FEMALE",
        "name": "女性"
      },
      "faction": {
        "type": "HORDE",
        "name": "部落"
      },
      "race": {
        "name": "龙希尔"
      },
      "character_class": {
        "id": 13,
        "name": "唤魔师"
      },
      "active_spec": {
        "name": "湮灭"
      },
      "realm": {
        "name": "阿尔萨斯",
        "slug": "arthas"
      },
      "guild": {
        "name": "一起",
        "realm": {
          "name": "阿尔萨斯",
          "slug": "arthas"
        },
        "faction": {
          "type": "HORDE",
          "name": "部落"
        }
      },
      "level": 80,
      "experience": 0,
      "achievement_points": 19840,
      "last_login_timestamp": 1753980571000,
      "average_item_level": 676,
      "equipped_item_level": 675,
      "active_title": {
        "name": "",
        "display_string": ""
      },
      "covenant_progress": {
        "chosen_covenant": {
          "name": "通灵领主"
        },
        "renown_level": 23,
        "soulbinds": {}
      },
      "name_search": "角色名称"
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
    "is_self": true,
    "allow": true,
    "encounters_json": "https://wow.res.netease.com/xt/manage/20250425/d6dcd2ae86ca7cf553bb96bbb7c8bfdd_1745553229269.json",
    "achievement_category_json": "https://wow.res.netease.com/images/20250605/1749093082272_bc9cf35dbb.json"
  }
}
```

### 响应字段说明

#### character_summary 角色摘要

| 字段名 | 类型 | 描述 |
|--------|------|------|
| name | string | 角色名称 |
| gender | object | 性别信息 |
| gender.type | string | 性别类型 (MALE/FEMALE) |
| gender.name | string | 性别显示名称 |
| faction | object | 阵营信息 |
| faction.type | string | 阵营类型 (ALLIANCE/HORDE) |
| faction.name | string | 阵营显示名称 |
| race | object | 种族信息 |
| race.name | string | 种族名称 |
| character_class | object | 职业信息 |
| character_class.id | number | 职业ID |
| character_class.name | string | 职业名称 |
| active_spec | object | 当前专精 |
| active_spec.name | string | 专精名称 |
| realm | object | 服务器信息 |
| realm.name | string | 服务器名称 |
| realm.slug | string | 服务器标识符 |
| guild | object | 公会信息 |
| guild.name | string | 公会名称 |
| level | number | 角色等级 |
| experience | number | 经验值 |
| achievement_points | number | 成就点数 |
| last_login_timestamp | number | 最后登录时间戳 |
| average_item_level | number | 平均装等 |
| equipped_item_level | number | 已装备装等 |
| active_title | object | 当前称号 |
| covenant_progress | object | 盟约进度 |
| name_search | string | 搜索用角色名 |

#### 其他字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| list | array | 可用的数据模块列表 (21个模块) |
| token | string | 访问令牌 (用于其他API调用) |
| is_self | boolean | 是否为当前用户角色 |
| allow | boolean | 是否允许访问 |
| encounters_json | string | 副本数据JSON链接 (可直接访问) |
| achievement_category_json | string | 成就分类JSON链接 (可直接访问) |

## 数据模块说明

API提供了21个数据模块，涵盖角色的各个方面：

### 角色信息模块 (4个)
- **equipment**: 装备信息
- **statistics**: 角色统计数据
- **specializations**: 专精信息
- **default_specializations**: 默认专精设置

### 副本相关模块 (4个)
- **raids**: 团队副本进度
- **mythic_keystone_season**: 大秘境赛季信息
- **mythic-keystone/dungeon**: 大秘境地下城数据
- **journal-instance**: 副本日志信息

### PVP相关模块 (2个)
- **pvp_summary**: PVP摘要信息
- **pvp**: 详细PVP数据

### 收集品模块 (3个)
- **pets**: 宠物收集
- **mounts**: 坐骑收集
- **hunter_pets**: 猎人宠物

### 成就相关模块 (4个)
- **achievement_category_index**: 成就分类索引
- **achievement_category_detail**: 成就分类详情
- **character_achievement**: 角色成就进度
- **achievement_detail**: 成就详细信息

### 其他模块 (4个)
- **default_journal_expansion_index**: 默认日志扩展索引
- **default_journal_expansion_index_v2**: 默认日志扩展索引v2
- **item_detail**: 物品详细信息
- **reputations**: 声望信息

## 外部JSON数据访问

### 副本数据 (encounters_json)

通过 `encounters_json` 链接可以获取角色的副本进度数据：

```json
[
  {
    "id": 1001,
    "name": "副本名称",
    "modes": [
      {
        "difficulty": {
          "type": "NORMAL",
          "name": "普通"
        },
        "status": {
          "type": "COMPLETE",
          "name": "已完成"
        }
      }
    ],
    "category_type": "RAID"
  }
]
```

**数据特点**:
- 数据大小: 约182KB
- 包含1,083个副本项目
- 涵盖所有难度和进度状态

### 成就数据 (achievement_category_json)

通过 `achievement_category_json` 链接可以获取完整的成就分类数据：

```json
[
  {
    "id": 1,
    "name": "成就分类名称",
    "en_name": "English Name",
    "display_order": 1,
    "is_guild_category": false,
    "parent_category": null,
    "subcategories": [],
    "achievements": [
      {
        "id": 1,
        "name": "成就名称",
        "description": "成就描述"
      }
    ],
    "aggregates_by_faction": {}
  }
]
```

**数据特点**:
- 数据大小: 约3MB
- 包含15个主要成就分类
- 涵盖所有成就的详细信息

## 错误响应

### 常见错误码

| 错误码 | 消息 | 描述 |
|--------|------|------|
| 0 | 成功 | 请求成功 |
| 1 | 角色不存在 | 指定的角色不存在 |
| 2 | 服务器不存在 | 指定的服务器不存在 |
| 3 | 未授权 | 需要登录或权限不足 |
| 4 | 角色数据不可用 | 角色数据暂时不可用 |

## 使用示例

### cURL 示例

```bash
curl 'https://webapi.blizzard.cn/wow-armory-server/api/index?realm_slug=arthas&role_name=%E5%BF%AB%E6%9D%A5%E9%AA%91%E6%88%91%E5%90%A7' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'cookie: blizzard_user_info=YOUR_TOKEN_HERE' \
  -H 'origin: https://wow.blizzard.cn' \
  -H 'referer: https://wow.blizzard.cn/'
```

### JavaScript 示例

```javascript
fetch("https://webapi.blizzard.cn/wow-armory-server/api/index?realm_slug=arthas&role_name=%E5%BF%AB%E6%9D%A5%E9%AA%91%E6%88%91%E5%90%A7", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "blizzard_user_info=YOUR_TOKEN_HERE",
    "Referer": "https://wow.blizzard.cn/"
  },
  "method": "GET"
})
.then(response => response.json())
.then(data => {
  console.log(data);
  
  // 获取外部JSON数据
  if (data.data.encounters_json) {
    fetch(data.data.encounters_json)
      .then(response => response.json())
      .then(encounters => console.log('副本数据:', encounters));
  }
  
  if (data.data.achievement_category_json) {
    fetch(data.data.achievement_category_json)
      .then(response => response.json())
      .then(achievements => console.log('成就数据:', achievements));
  }
});
```

### Python 示例

```python
import requests
import json

def get_character_info(realm_slug, character_name, cookie_token):
    """获取角色信息"""
    url = "https://webapi.blizzard.cn/wow-armory-server/api/index"
    
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'blizzard_user_info={cookie_token}',
        'origin': 'https://wow.blizzard.cn',
        'referer': 'https://wow.blizzard.cn/'
    }
    
    params = {
        'realm_slug': realm_slug,
        'role_name': character_name
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_external_data(session, url):
    """获取外部JSON数据"""
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取外部数据失败: {e}")
        return None

# 使用示例
session = requests.Session()
character_data = get_character_info('arthas', '快来骑我吧', 'YOUR_TOKEN_HERE')

if character_data['code'] == 0:
    data = character_data['data']
    
    # 获取副本数据
    if data.get('encounters_json'):
        encounters = get_external_data(session, data['encounters_json'])
        print(f"副本数据大小: {len(str(encounters))} 字符")
    
    # 获取成就数据
    if data.get('achievement_category_json'):
        achievements = get_external_data(session, data['achievement_category_json'])
        print(f"成就数据大小: {len(str(achievements))} 字符")
```

### PowerShell 示例

```powershell
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$session.Cookies.Add((New-Object System.Net.Cookie("blizzard_user_info", "YOUR_TOKEN_HERE", "/", ".blizzard.cn")))

Invoke-WebRequest -UseBasicParsing -Uri "https://webapi.blizzard.cn/wow-armory-server/api/index?realm_slug=arthas&role_name=%E5%BF%AB%E6%9D%A5%E9%AA%91%E6%88%91%E5%90%A7" `
-WebSession $session `
-Headers @{
  "accept"="application/json, text/javascript, */*; q=0.01"
  "accept-language"="zh-CN,zh;q=0.9"
  "origin"="https://wow.blizzard.cn"
  "referer"="https://wow.blizzard.cn/"
}
```

## 数据获取最佳实践

### 1. 分步获取数据
```python
# 第一步：获取基本信息
basic_info = get_character_basic_info(realm, character, token)

# 第二步：获取外部JSON数据
if basic_info['code'] == 0:
    data = basic_info['data']
    
    # 获取副本数据
    encounters = get_external_json_data(data['encounters_json'])
    
    # 获取成就数据
    achievements = get_external_json_data(data['achievement_category_json'])
```

### 2. 错误处理和重试
```python
def get_data_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # 指数退避
```

### 3. 数据缓存
```python
import hashlib
import os

def get_cached_data(url, cache_dir="cache"):
    # 创建缓存目录
    os.makedirs(cache_dir, exist_ok=True)
    
    # 生成缓存文件名
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_file = os.path.join(cache_dir, f"{cache_key}.json")
    
    # 检查缓存
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 获取新数据
    data = get_external_json_data(url)
    
    # 保存到缓存
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data
```

## 注意事项

1. **认证要求**: 需要有效的 `blizzard_user_info` cookie 进行认证
2. **角色名称编码**: 角色名称需要进行URL编码
3. **服务器标识符**: 使用服务器的slug而不是显示名称
4. **访问限制**: 某些角色数据可能需要特定权限才能访问
5. **数据更新**: 角色数据可能有延迟，不是实时更新
6. **外部数据访问**: 副本和成就数据通过外部JSON链接获取
7. **数据大小**: 外部JSON数据较大，建议实现缓存机制
8. **请求频率**: 避免过于频繁的请求，建议添加适当的延迟

## 相关链接

- 魔兽世界官网: https://wow.blizzard.cn/
- 角色查询页面: https://wow.blizzard.cn/character/
- 成就数据: 通过 `achievement_category_json` 链接获取
- 副本数据: 通过 `encounters_json` 链接获取

## 测试结果

### API可用性测试
- ✅ 基本信息API: 正常工作
- ✅ 外部JSON数据: 正常工作
- ❌ 直接模块端点: 返回404错误

### 数据规模
- 副本数据: 182,503 字符 (1,083个项目)
- 成就数据: 3,003,966 字符 (15个分类)
- 可用模块: 21个

### 测试环境
- 测试角色: Acg (法师 - 亡灵)
- 服务器: arthas (阿尔萨斯)
- 测试时间: 2024年1月

## 更新日志

- **2024-01-XX**: 初始版本，支持基础角色信息查询
- **2024-01-XX**: 添加21个数据模块说明
- **2024-01-XX**: 添加外部JSON数据访问方式
- **2024-01-XX**: 添加测试结果和最佳实践
- 支持龙希尔种族和唤魔师职业数据
- 包含盟约系统进度信息
- 添加副本和成就数据的详细说明
- 提供多种编程语言的使用示例 