# 魔兽世界大秘境赛季API文档

## 概述

大秘境赛季API提供了获取角色大秘境详细信息的接口，包括最佳记录、地下城信息、团队成员、词缀等完整的赛季数据。

## API端点

### 大秘境赛季信息
- **URL**: `https://webapi.blizzard.cn/wow-armory-server/api/do`
- **方法**: GET
- **参数**:
  - `api`: `mythic_keystone_season`
  - `token`: 访问令牌

### 完整URL示例
```
https://webapi.blizzard.cn/wow-armory-server/api/do?api=mythic_keystone_season&token=fe2a685ceecc0abb9a435b89f2e9c37c
```

## 请求头

```javascript
{
  "accept": "application/json, text/javascript, */*; q=0.01",
  "accept-language": "zh-CN,zh;q=0.9",
  "priority": "u=1, i",
  "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Linux\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-site",
  "xcxtoken": ""
}
```

## 响应数据结构

### 基础响应格式

```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "best_runs": [...],
    "character": {...},
    "mythic_rating": {...},
    "season": {...}
  }
}
```

### 主要数据字段

#### 1. best_runs (最佳记录数组)
包含角色的所有大秘境最佳记录，按时间倒序排列。

#### 2. character (角色信息)
当前角色的基本信息。

#### 3. mythic_rating (大秘境评分)
角色的总体大秘境评分。

#### 4. season (赛季信息)
当前赛季的详细信息。

## 详细字段说明

### best_runs 数组中的单个记录

```json
{
  "completed_timestamp": 1745678444000,
  "dungeon": {
    "icon": "https://wow.res.netease.com/xt/manage/20250311/9bd6339faf65cd64c15dcdfd79e571ad_1741669357703.jpg",
    "id": 504,
    "key": {"href": ""},
    "name": "暗焰裂口"
  },
  "duration": 2235111,
  "is_completed_within_time": false,
  "keystone_affixes": [...],
  "keystone_level": 14,
  "map_rating": {
    "color": {"a": 1, "b": 0, "g": 128, "r": 255},
    "rating": 455.50998
  },
  "members": [...],
  "mythic_rating": {
    "color": {"a": 1, "b": 0, "g": 128, "r": 255},
    "rating": 312.4373
  }
}
```

#### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| completed_timestamp | number | 完成时间戳 (毫秒) |
| dungeon | object | 地下城信息 |
| duration | number | 完成时间 (毫秒) |
| is_completed_within_time | boolean | 是否在规定时间内完成 |
| keystone_affixes | array | 词缀信息数组 |
| keystone_level | number | 钥石等级 |
| map_rating | object | 地图评分 |
| members | array | 团队成员信息 |
| mythic_rating | object | 本次记录的大秘境评分 |

### dungeon (地下城信息)

```json
{
  "icon": "https://wow.res.netease.com/xt/manage/20250311/9bd6339faf65cd64c15dcdfd79e571ad_1741669357703.jpg",
  "id": 504,
  "key": {"href": ""},
  "name": "暗焰裂口"
}
```

| 字段名 | 类型 | 描述 |
|--------|------|------|
| icon | string | 地下城图标URL |
| id | number | 地下城ID |
| key | object | 钥石信息 (通常为空) |
| name | string | 地下城名称 |

### keystone_affixes (词缀信息)

```json
[
  {
    "description": "非首领敌人的生命值提高20%，造成的伤害最多提高20%。",
    "icon": "https://wow.res.netease.com/xt/manage/20250421/3e5c2a933174088907a93396af393940_1745208519960.jpg",
    "id": 10,
    "name": "强韧"
  },
  {
    "description": "首领的生命值提高25%，首领及其爪牙造成的伤害最多提高15%。",
    "icon": "https://wow.res.netease.com/xt/manage/20250421/d4632195ba0508babac485fae52a07be_1745208518872.jpg",
    "id": 9,
    "name": "残暴"
  },
  {
    "description": "萨拉塔斯背叛了玩家，撤销了自己的交易，而且每次角色死亡都会让剩余时间减少15秒。",
    "icon": "https://wow.res.netease.com/xt/manage/20250421/dbb9dd4c0043cfd2fddd3e502e09a229_1745208562096.jpg",
    "id": 147,
    "name": "萨拉塔斯的狡诈"
  }
]
```

| 字段名 | 类型 | 描述 |
|--------|------|------|
| description | string | 词缀效果描述 |
| icon | string | 词缀图标URL |
| id | number | 词缀ID |
| name | string | 词缀名称 |

### members (团队成员信息)

```json
[
  {
    "character": {
      "class_id": 0,
      "id": 92472796,
      "name": "妙不可言",
      "realm": {
        "id": 844,
        "slug": "arthas"
      }
    },
    "equipped_item_level": 671,
    "race": {
      "id": 36,
      "name": "玛格汉兽人"
    },
    "specialization": {
      "id": 254,
      "name": "射击"
    }
  }
]
```

#### character (角色信息)
| 字段名 | 类型 | 描述 |
|--------|------|------|
| class_id | number | 职业ID |
| id | number | 角色ID |
| name | string | 角色名称 |
| realm | object | 服务器信息 |

#### realm (服务器信息)
| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | number | 服务器ID |
| slug | string | 服务器标识符 |

#### 其他字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
| equipped_item_level | number | 装备等级 |
| race | object | 种族信息 |
| specialization | object | 专精信息 |

### character (当前角色信息)

```json
{
  "id": 93561929,
  "key": {
    "href": "https://partner.apigw.blzdev.cn/GameDataProfileService/v1/wow/character/arthas/%E4%B9%85%E4%B8%96?namespace=profile-cn"
  },
  "name": "久世",
  "realm": {
    "id": 844,
    "key": {
      "href": "https://partner.apigw.blzdev.cn/GameDataService/v1/wow/realm/844?namespace=dynamic-cn"
    },
    "name": "阿尔萨斯",
    "slug": "arthas"
  }
}
```

### mythic_rating (大秘境评分)

```json
{
  "color": {"a": 1, "b": 0, "g": 128, "r": 255},
  "rating": 3551.7637
}
```

| 字段名 | 类型 | 描述 |
|--------|------|------|
| color | object | 评分颜色 (RGBA) |
| rating | number | 评分数值 |

### season (赛季信息)

```json
{
  "Key": {"href": ""},
  "id": 14,
  "season_str": "\"地心之战\"第2赛季"
}
```

| 字段名 | 类型 | 描述 |
|--------|------|------|
| Key | object | 赛季链接 (通常为空) |
| id | number | 赛季ID |
| season_str | string | 赛季名称 |

## 数据示例分析

### 示例记录分析

从提供的API响应中，我们可以看到：

1. **角色信息**: 久世 (阿尔萨斯服务器)
2. **赛季**: "地心之战"第2赛季
3. **总体评分**: 3551.76分
4. **最佳记录**: 包含多个地下城的记录

### 地下城类型

从数据中可以看到的地下城：
- 暗焰裂口 (ID: 504)
- 燧酿酒庄 (ID: 506)
- 麦卡贡行动 - 车间 (ID: 370)
- 圣焰隐修院 (ID: 499)
- 驭雷栖巢 (ID: 500)
- 水闸行动 (ID: 525)
- 伤逝剧场 (ID: 382)
- 暴富矿区！！ (ID: 247)

### 词缀系统

当前赛季的词缀组合：
1. **强韧** (ID: 10): 小怪增强
2. **残暴** (ID: 9): 首领增强
3. **萨拉塔斯的狡诈** (ID: 147): 特殊机制

## 使用示例

### JavaScript 示例

```javascript
fetch("https://webapi.blizzard.cn/wow-armory-server/api/do?api=mythic_keystone_season&token=YOUR_TOKEN", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
  },
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
})
.then(response => response.json())
.then(data => {
  if (data.code === 0) {
    const mythicData = data.data;
    
    // 获取总体评分
    console.log(`总体评分: ${mythicData.mythic_rating.rating}`);
    
    // 获取最佳记录
    mythicData.best_runs.forEach((run, index) => {
      console.log(`${index + 1}. ${run.dungeon.name} ${run.keystone_level}层`);
      console.log(`   完成时间: ${run.duration}ms`);
      console.log(`   是否限时: ${run.is_completed_within_time ? '是' : '否'}`);
      console.log(`   评分: ${run.mythic_rating.rating}`);
    });
  }
});
```

### Python 示例

```python
import requests
import json

def get_mythic_keystone_data(token):
    """获取大秘境赛季数据"""
    url = "https://webapi.blizzard.cn/wow-armory-server/api/do"
    
    params = {
        'api': 'mythic_keystone_season',
        'token': token
    }
    
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site'
    }
    
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def analyze_mythic_data(data):
    """分析大秘境数据"""
    if data['code'] != 0:
        print(f"API错误: {data['message']}")
        return
    
    mythic_data = data['data']
    
    # 基本信息
    character = mythic_data['character']
    season = mythic_data['season']
    rating = mythic_data['mythic_rating']
    
    print(f"角色: {character['name']} ({character['realm']['name']})")
    print(f"赛季: {season['season_str']}")
    print(f"总体评分: {rating['rating']:.2f}")
    print(f"最佳记录数量: {len(mythic_data['best_runs'])}")
    
    # 分析最佳记录
    for i, run in enumerate(mythic_data['best_runs'][:5], 1):
        print(f"\n{i}. {run['dungeon']['name']} {run['keystone_level']}层")
        print(f"   完成时间: {run['duration']}ms")
        print(f"   限时完成: {'是' if run['is_completed_within_time'] else '否'}")
        print(f"   评分: {run['mythic_rating']['rating']:.2f}")
        
        # 显示词缀
        affixes = [affix['name'] for affix in run['keystone_affixes']]
        print(f"   词缀: {', '.join(affixes)}")

# 使用示例
token = "YOUR_TOKEN_HERE"
data = get_mythic_keystone_data(token)
analyze_mythic_data(data)
```

## 注意事项

1. **认证要求**: 需要有效的访问令牌
2. **数据更新**: 大秘境数据可能有延迟
3. **评分计算**: 评分基于完成时间和钥石等级计算
4. **词缀轮换**: 词缀每周轮换，影响难度
5. **赛季限制**: 数据仅包含当前赛季的记录

## 相关链接

- 魔兽世界官网: https://wow.blizzard.cn/
- 大秘境查询: https://wow.blizzard.cn/character/
- 词缀信息: 通过API获取当前词缀详情

---

**注意**: 使用本API时请确保遵守魔兽世界官方服务条款。 