# 魔兽世界大秘境API使用指南

## 概述

本指南详细介绍了如何使用魔兽世界大秘境赛季API获取和分析角色的大秘境数据。

## API端点

### 大秘境赛季信息
```
GET https://webapi.blizzard.cn/wow-armory-server/api/do?api=mythic_keystone_season&token={token}
```

### 参数说明
- `api`: 固定值 `mythic_keystone_season`
- `token`: 从角色信息API获取的访问令牌

## 获取Token的步骤

1. **获取角色基本信息**
   ```bash
   GET https://webapi.blizzard.cn/wow-armory-server/api/index?realm_slug={realm}&role_name={character}
   ```

2. **提取Token**
   ```json
   {
     "code": 0,
     "data": {
       "token": "fe2a685ceecc0abb9a435b89f2e9c37c"
     }
   }
   ```

3. **调用大秘境API**
   ```bash
   GET https://webapi.blizzard.cn/wow-armory-server/api/do?api=mythic_keystone_season&token=fe2a685ceecc0abb9a435b89f2e9c37c
   ```

## 响应数据结构

### 成功响应示例
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

## 数据字段详解

### best_runs 中的单个记录
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

### 字段说明

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

## 使用示例

### JavaScript 示例
```javascript
// 1. 获取角色基本信息
async function getCharacterInfo(realm, character) {
  const response = await fetch(`https://webapi.blizzard.cn/wow-armory-server/api/index?realm_slug=${realm}&role_name=${character}`);
  const data = await response.json();
  return data.data.token;
}

// 2. 获取大秘境数据
async function getMythicData(token) {
  const response = await fetch(`https://webapi.blizzard.cn/wow-armory-server/api/do?api=mythic_keystone_season&token=${token}`);
  const data = await response.json();
  return data.data;
}

// 3. 使用示例
async function analyzeMythicData(realm, character) {
  try {
    // 获取token
    const token = await getCharacterInfo(realm, character);
    
    // 获取大秘境数据
    const mythicData = await getMythicData(token);
    
    // 分析数据
    console.log(`角色: ${mythicData.character.name}`);
    console.log(`总体评分: ${mythicData.mythic_rating.rating}`);
    console.log(`最佳记录数: ${mythicData.best_runs.length}`);
    
    // 显示最佳记录
    mythicData.best_runs.forEach((run, index) => {
      console.log(`${index + 1}. ${run.dungeon.name} ${run.keystone_level}层`);
      console.log(`   时间: ${formatDuration(run.duration)}`);
      console.log(`   评分: ${run.mythic_rating.rating}`);
    });
    
  } catch (error) {
    console.error('获取数据失败:', error);
  }
}

// 格式化时间
function formatDuration(durationMs) {
  const totalSeconds = Math.floor(durationMs / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}
```

### Python 示例
```python
import requests
import json
from datetime import datetime

class MythicKeystoneAPI:
    def __init__(self):
        self.base_url = "https://webapi.blizzard.cn/wow-armory-server/api"
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        })
    
    def get_character_token(self, realm_slug, character_name):
        """获取角色访问令牌"""
        url = f"{self.base_url}/index"
        params = {
            'realm_slug': realm_slug,
            'role_name': character_name
        }
        
        response = self.session.get(url, params=params)
        data = response.json()
        
        if data.get('code') == 0:
            return data['data']['token']
        else:
            raise Exception(f"获取token失败: {data.get('message')}")
    
    def get_mythic_data(self, token):
        """获取大秘境数据"""
        url = f"{self.base_url}/do"
        params = {
            'api': 'mythic_keystone_season',
            'token': token
        }
        
        response = self.session.get(url, params=params)
        data = response.json()
        
        if data.get('code') == 0:
            return data['data']
        else:
            raise Exception(f"获取大秘境数据失败: {data.get('message')}")
    
    def analyze_data(self, mythic_data):
        """分析大秘境数据"""
        character = mythic_data['character']
        rating = mythic_data['mythic_rating']
        runs = mythic_data['best_runs']
        
        print(f"角色: {character['name']} ({character['realm']['name']})")
        print(f"总体评分: {rating['rating']:.2f}")
        print(f"最佳记录数: {len(runs)}")
        
        # 统计信息
        completed_within_time = sum(1 for run in runs if run['is_completed_within_time'])
        completion_rate = (completed_within_time / len(runs)) * 100 if runs else 0
        
        print(f"限时完成率: {completion_rate:.1f}%")
        
        # 显示最佳记录
        for i, run in enumerate(runs[:5], 1):
            duration = self.format_duration(run['duration'])
            status = "✅" if run['is_completed_within_time'] else "❌"
            
            print(f"{i}. {status} {run['dungeon']['name']} {run['keystone_level']}层")
            print(f"   时间: {duration} | 评分: {run['mythic_rating']['rating']:.2f}")
    
    def format_duration(self, duration_ms):
        """格式化时间显示"""
        total_seconds = duration_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

# 使用示例
def main():
    api = MythicKeystoneAPI()
    
    try:
        # 获取token
        token = api.get_character_token("arthas", "久世")
        print(f"获取到token: {token}")
        
        # 获取大秘境数据
        mythic_data = api.get_mythic_data(token)
        
        # 分析数据
        api.analyze_data(mythic_data)
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()
```

## 数据分析工具

### 使用内置分析工具
```bash
# 运行分析脚本
python3 analyze_mythic_data.py

# 运行测试
python3 test_mythic_analysis.py
```

### 分析功能包括
1. **基本信息**: 角色名称、服务器、总体评分
2. **记录统计**: 总记录数、限时完成率、平均等级
3. **地下城分析**: 各地下城的完成情况
4. **详细记录**: 显示每条记录的详细信息

## 数据解读

### 评分系统
- **总体评分**: 基于所有最佳记录计算的综合评分
- **单次评分**: 基于完成时间和钥石等级计算的单次评分
- **地图评分**: 特定地下城的评分

### 时间格式
- **duration**: 毫秒为单位
- **completed_timestamp**: 毫秒时间戳

### 词缀系统
当前赛季包含三种词缀：
1. **强韧**: 小怪增强
2. **残暴**: 首领增强  
3. **萨拉塔斯的狡诈**: 特殊机制

## 注意事项

1. **认证要求**: 需要有效的访问令牌
2. **数据更新**: 大秘境数据可能有延迟
3. **赛季限制**: 数据仅包含当前赛季的记录
4. **评分计算**: 评分基于完成时间和钥石等级
5. **词缀轮换**: 词缀每周轮换，影响难度

## 错误处理

### 常见错误码
- `code: 0`: 成功
- `code: 1`: 角色不存在
- `code: 2`: 服务器不存在
- `code: 3`: 未授权
- `code: 4`: 数据不可用

### 错误处理示例
```python
try:
    data = api.get_mythic_data(token)
    # 处理数据
except requests.exceptions.RequestException as e:
    print(f"网络错误: {e}")
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

## 相关链接

- [大秘境API文档](mythic-keystone-api-docs.md)
- [角色信息API文档](wow-armory-api-docs.md)
- [魔兽世界官网](https://wow.blizzard.cn/)

---

**注意**: 使用本API时请确保遵守魔兽世界官方服务条款。 