# 魔兽世界坐骑API说明文档（历史调研）

> ⚠️ 本文是 2025 年的原始接口调研。英雄榜现在要求战网登录（`xcxtoken`，约 7 天过期），下面的「直接 GET 就能拿到坐骑数」已不成立；保留作历史参考，现行数据链路见 `DATA_PIPELINE.md`。

## 概述

魔兽世界坐骑API提供了获取玩家坐骑收藏信息的接口，支持查询联盟和部落阵营的坐骑数据。

## API端点

```
GET https://webapi.blizzard.cn/wow-armory-server/api/do
```

## 请求参数

### 查询参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `api` | string | 是 | API类型，固定值：`mounts` |
| `token` | string | 是 | 访问令牌，用于身份验证 |
| `attr` | string | 是 | 阵营属性，可选值：`HORDE`（部落）、`ALLIANCE`（联盟） |

### 请求头

#### 必需请求头

```javascript
{
  "accept": "application/json, text/javascript, */*; q=0.01",
  "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
  "accept-encoding": "gzip, deflate, br, zstd",
  "origin": "https://wow.blizzard.cn",
  "referer": "https://wow.blizzard.cn/",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-site",
  "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/136.0.0.0"
}
```

#### 可选请求头

```javascript
{
  "priority": "u=1, i",
  "xcxtoken": ""
}
```

#### Cookie信息

```
blizzard_user_info=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTYwMjAyODg2LCJiYXR0bGVfdGFnIjoi6ZSI6ZOBIzUxODYxIiwiZW1haWwiOm51bGwsInBob25lIjpudWxsLCJjYXJkIjpudWxsfQ.3S0QMaE_FMB-ZlwW8SCHamuF9sCsxsLS0nlM3wEpDZk
```

## 响应头信息

### 成功响应头

```
HTTP/1.1 200 OK
access-control-allow-credentials: true
access-control-allow-origin: https://wow.blizzard.cn
access-control-expose-headers: Content-Length,Access-Control-Allow-Origin,Access-Control-Allow-Headers,Cache-Control,Content-Language,Content-Type
content-encoding: br
content-type: application/json; charset=utf-8
date: Wed, 06 Aug 2025 14:12:51 GMT
vary: Accept-Encoding
vary: Origin
```

## 请求示例

### 实际请求示例

```
GET https://webapi.blizzard.cn/wow-armory-server/api/do?api=mounts&token=YOUR_TOKEN_HERE&attr=HORDE
```

### JavaScript Fetch

```javascript
fetch("https://webapi.blizzard.cn/wow-armory-server/api/do?api=mounts&token=YOUR_TOKEN_HERE&attr=HORDE", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "accept-encoding": "gzip, deflate, br, zstd",
    "origin": "https://wow.blizzard.cn",
    "referer": "https://wow.blizzard.cn/",
    "priority": "u=1, i",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/136.0.0.0"
  },
  "referrer": "https://wow.blizzard.cn/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### Python Requests

```python
import requests

url = "https://webapi.blizzard.cn/wow-armory-server/api/do"
params = {
    "api": "mounts",
    "token": "YOUR_TOKEN_HERE",
    "attr": "HORDE"
}

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "accept-encoding": "gzip, deflate, br, zstd",
    "origin": "https://wow.blizzard.cn",
    "referer": "https://wow.blizzard.cn/",
    "priority": "u=1, i",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/136.0.0.0"
}

cookies = {
    "blizzard_user_info": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTYwMjAyODg2LCJiYXR0bGVfdGFnIjoi6ZSI6ZOBIzUxODYxIiwiZW1haWwiOm51bGwsInBob25lIjpudWxsLCJjYXJkIjpudWxsfQ.3S0QMaE_FMB-ZlwW8SCHamuF9sCsxsLS0nlM3wEpDZk"
}

response = requests.get(url, params=params, headers=headers, cookies=cookies)
data = response.json()
print(data)
```

### cURL示例

```bash
curl -X GET "https://webapi.blizzard.cn/wow-armory-server/api/do?api=mounts&token=YOUR_TOKEN_HERE&attr=HORDE" \
  -H "accept: application/json, text/javascript, */*; q=0.01" \
  -H "accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6" \
  -H "accept-encoding: gzip, deflate, br, zstd" \
  -H "origin: https://wow.blizzard.cn" \
  -H "referer: https://wow.blizzard.cn/" \
  -H "priority: u=1, i" \
  -H "sec-fetch-dest: empty" \
  -H "sec-fetch-mode: cors" \
  -H "sec-fetch-site: same-site" \
  -H "user-agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/136.0.0.0" \
  -H "cookie: blizzard_user_info=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTYwMjAyODg2LCJiYXR0bGVfdGFnIjoi6ZSI6ZOBIzUxODYxIiwiZW1haWwiOm51bGwsInBob25lIjpudWxsLCJjYXJkIjpudWxsfQ.3S0QMaE_FMB-ZlwW8SCHamuF9sCsxsLS0nlM3wEpDZk"
```

## 响应格式

### 成功响应

```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "mounts": [
      {
        "is_favorite": true,
        "is_useable": true,
        "mount": {
          "description": "全世界公认的复仇象征。",
          "id": 123,
          "name": "坐骑名称",
          "icon": "mount_icon_url",
          "spell_id": 456,
          "quality": "epic",
          "source": "成就奖励"
        }
      }
    ],
    "now": 369,
    "total": 1047
  }
}
```

### 响应字段说明

#### 顶层字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `code` | integer | 响应状态码，0表示成功 |
| `message` | string | 响应消息 |
| `data` | object | 响应数据对象 |

#### data字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `mounts` | array | 坐骑列表数组 |
| `now` | integer | 当前拥有的坐骑数量 |
| `total` | integer | 总坐骑数量 |

#### mounts数组中的对象

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `is_favorite` | boolean | 是否为收藏坐骑 |
| `is_useable` | boolean | 是否可使用 |
| `mount` | object | 坐骑详细信息 |

#### mount对象字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `description` | string | 坐骑描述 |
| `id` | integer | 坐骑ID |
| `name` | string | 坐骑名称 |
| `icon` | string | 坐骑图标URL |
| `spell_id` | integer | 法术ID |
| `quality` | string | 品质（common, uncommon, rare, epic, legendary） |
| `source` | string | 获取来源 |

## 错误响应

### 常见错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1 | 参数错误 |
| 2 | 令牌无效 |
| 3 | 权限不足 |
| 4 | 服务器错误 |

### 错误响应示例

```json
{
  "code": 2,
  "message": "令牌无效",
  "data": null
}
```

## 使用注意事项

1. **令牌管理**：token参数需要有效的访问令牌，通常从登录接口获取
2. **阵营选择**：attr参数决定了返回哪个阵营的坐骑数据
3. **请求频率**：建议控制请求频率，避免过于频繁的API调用
4. **错误处理**：始终检查响应中的code字段，处理可能的错误情况
5. **数据缓存**：坐骑数据变化不频繁，建议适当缓存以减少API调用
6. **请求头要求**：必须包含正确的origin和referer头，否则可能被拒绝访问
7. **Cookie认证**：某些情况下可能需要包含blizzard_user_info cookie进行身份验证
8. **CORS限制**：API设置了严格的CORS策略，只允许来自https://wow.blizzard.cn的请求
9. **User-Agent**：建议使用真实的浏览器User-Agent，避免被识别为机器人
10. **压缩支持**：API支持多种压缩格式（gzip, deflate, br, zstd），建议在请求头中声明支持

## 完整使用示例

```javascript
class WowMountsAPI {
  constructor(token) {
    this.baseUrl = 'https://webapi.blizzard.cn/wow-armory-server/api/do';
    this.token = token;
  }

  async getMounts(faction = 'HORDE') {
    try {
      const params = new URLSearchParams({
        api: 'mounts',
        token: this.token,
        attr: faction
      });

      const response = await fetch(`${this.baseUrl}?${params}`, {
        method: 'GET',
        headers: {
          'accept': 'application/json, text/javascript, */*; q=0.01',
          'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-site',
          'xcxtoken': ''
        },
        referrer: 'https://wow.blizzard.cn/',
        referrerPolicy: 'strict-origin-when-cross-origin',
        mode: 'cors',
        credentials: 'include'
      });

      const data = await response.json();
      
      if (data.code === 0) {
        return {
          success: true,
          data: data.data,
          message: data.message
        };
      } else {
        return {
          success: false,
          error: data.message,
          code: data.code
        };
      }
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 获取收藏坐骑
  async getFavoriteMounts(faction = 'HORDE') {
    const result = await this.getMounts(faction);
    if (result.success) {
      return result.data.mounts.filter(mount => mount.is_favorite);
    }
    return [];
  }

  // 获取可用坐骑
  async getUseableMounts(faction = 'HORDE') {
    const result = await this.getMounts(faction);
    if (result.success) {
      return result.data.mounts.filter(mount => mount.is_useable);
    }
    return [];
  }
}

// 使用示例
const api = new WowMountsAPI('YOUR_TOKEN_HERE');

// 获取部落坐骑
api.getMounts('HORDE').then(result => {
  if (result.success) {
    console.log(`拥有 ${result.data.now}/${result.data.total} 个坐骑`);
    console.log('坐骑列表:', result.data.mounts);
  } else {
    console.error('获取失败:', result.error);
  }
});

// 获取联盟坐骑
api.getMounts('ALLIANCE').then(result => {
  if (result.success) {
    console.log(`拥有 ${result.data.now}/${result.data.total} 个坐骑`);
  }
});
```

## 更新日志

- **v1.1** - 完善请求和响应头信息
  - 添加详细的必需和可选请求头说明
  - 包含实际的Cookie认证信息
  - 添加完整的响应头信息
  - 提供cURL命令行示例
  - 更新使用注意事项，包含CORS和认证要求
  - 使用实际请求中的token示例

- **v1.0** - 初始版本，支持基本的坐骑查询功能
  - 支持联盟和部落阵营查询
  - 提供收藏和可用性状态
  - 包含坐骑详细信息（名称、描述、图标等）

---

*本文档基于魔兽世界中国服务器API编写，适用于国服玩家使用。* 